"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

##  FILE DESCRIPTION:
##      QPainter grid renderer for the integrated terminal emulator.
##      Paints the pyte screen (and styled scrollback history) cell by cell,
##      with incremental repaints driven by the screen's dirty-line set.

import functools
import math
import os

import data
import functions
import gui.menu
import qt
import settings
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Set, Tuple, Union, cast
from wcwidth import wcwidth

from gui.terminal.screen import ExtendedScreen

if TYPE_CHECKING:
    from gui.terminal.terminal import Terminal

# A selection is either a bare anchor (start cell) or a (start, end) pair;
# all cells are (stack_row, column) tuples.
Selection = Union[Tuple[int, int], Tuple[int, int, int, int]]

# ANSI color palettes. 'default' is resolved at render time to the
# terminal's default foreground/background. The bright variants use the
# classic VGA/xterm bright shades so they stay distinct from the normal ones.
FOREGROUND_COLOR_MAP: Dict[str, Optional[qt.QColor]] = {
    "default": None,
    "black": qt.QColor(qt.Qt.GlobalColor.black),
    "red": qt.QColor(qt.Qt.GlobalColor.red),
    "green": qt.QColor(qt.Qt.GlobalColor.green),
    "brown": qt.QColor(qt.Qt.GlobalColor.yellow),
    "blue": qt.QColor(qt.Qt.GlobalColor.blue),
    "magenta": qt.QColor(qt.Qt.GlobalColor.magenta),
    "cyan": qt.QColor(qt.Qt.GlobalColor.cyan),
    "white": qt.QColor(qt.Qt.GlobalColor.lightGray),
    "brightblack": qt.QColor("#555555"),
    "brightred": qt.QColor("#ff5555"),
    "brightgreen": qt.QColor("#55ff55"),
    "brightbrown": qt.QColor("#ffff55"),
    "brightblue": qt.QColor("#5555ff"),
    "brightmagenta": qt.QColor("#ff55ff"),
    "brightcyan": qt.QColor("#55ffff"),
    "brightwhite": qt.QColor("#ffffff"),
}


class TerminalView(qt.QWidget):
    """
    Custom QWidget that renders a pyte screen (and its scrollback history)
    using QPainter on a monospace cell grid.
    """

    # Signals
    send_text = qt.pyqtSignal(str)
    resize_event = qt.pyqtSignal(int, int)
    paste_event = qt.pyqtSignal(str)
    focused = qt.pyqtSignal()

    # Cursor blink period in milliseconds
    BLINK_INTERVAL_MS: int = 530

    def __init__(
        self, terminal: "Terminal", parent: Optional[qt.QWidget] = None
    ) -> None:
        super().__init__(parent)
        self.terminal: "Terminal" = terminal

        self.setFocusPolicy(qt.Qt.FocusPolicy.StrongFocus)
        self.setMouseTracking(True)
        # Accept file/text drops so dragging a path into the terminal sends
        # it to the shell instead of the main window's drop-to-open handler.
        self.setAcceptDrops(True)

        # Monospace font and its measured cell size
        self._style_fonts: Dict[Tuple[bool, bool, bool, bool], qt.QFont] = {}
        self._load_style()

        # Scrollback state
        self._scroll_offset: int = 0
        self._sb_visible: bool = False
        self._content_width: int = 0

        # Cursor blink
        self._blink_phase: bool = True
        # SGR-5 (blink) cells blink on their own phase, independent of the
        # cursor's: a hidden cursor or a steady DECSCUSR style must not stop
        # text from blinking, and the two must not share a phase - parking the
        # shared one on 'visible' (so a cursor that reappears is never caught
        # mid-blink) would freeze the text instead.
        self._sgr_blink_phase: bool = True
        # Viewport rows carrying SGR-5 (blink) cells, recorded as a byproduct
        # of painting (see _paint_cells) and consumed by _on_blink. A row is
        # only ever added or removed by a paint, so the set always describes
        # the rows actually on screen - live buffer and scrollback alike.
        self._blink_rows: Set[int] = set()
        self._blink_timer: qt.QTimer = qt.QTimer(self)
        self._blink_timer.setInterval(self.BLINK_INTERVAL_MS)
        self._blink_timer.timeout.connect(self._on_blink)
        self._blink_timer.start()

        # Selection state (start/end cells in stack coordinates)
        self._selection: Optional[Selection] = None
        self._selection_active: bool = False
        # Cell the current left-press started on; hyperlink activation on
        # release requires the press and release to share a cell.
        self._press_cell: Optional[Tuple[int, int]] = None
        # Shift-bypass of mouse tracking: while Shift is held, mouse events
        # drive native selection / scrollback scroll instead of reports.
        self._shift_selecting: bool = False
        # TUI right-click state: inside a mouse-capturing app the right
        # button is forwarded (press + release) so the app acts on it.
        # _tui_right_synth is set when a short synthetic drag first replayed
        # the native selection into the app, giving opencode the text it needs
        # to copy and draw its own toast. Both flags span press -> release ->
        # contextMenuEvent (Windows order) and are consumed there.
        self._tui_right_forwarded: bool = False
        self._tui_right_synth: bool = False

        # Triple-click (line selection) tracking: a double-click arms a
        # single-shot timer timed to the system double-click interval; a
        # third press while it still runs selects the whole line instead of
        # starting a drag.
        self._double_clicked: bool = False
        self._triple_click_timer: qt.QTimer = qt.QTimer(self)
        self._triple_click_timer.setSingleShot(True)
        self._triple_click_timer.setInterval(int(qt.QApplication.doubleClickInterval()))
        self._triple_click_timer.timeout.connect(self._triple_click_expired)

        # Drag auto-scroll: while a selection is dragged past the top or
        # bottom edge this timer scrolls the scrollback one row per tick and
        # extends the selection into the newly revealed rows.
        self._autoscroll_timer: qt.QTimer = qt.QTimer(self)
        self._autoscroll_timer.setInterval(50)
        self._autoscroll_timer.timeout.connect(self._tick_autoscroll)
        self._autoscroll_dir: int = 0
        self._autoscroll_pos: Optional[qt.QPointF] = None

        # Last painted cursor row (for clearing the previous cursor position)
        self._last_cursor_y: Optional[int] = None

        # Whether the last repaint batch saw the alternate screen, so entering
        # it can be told apart from simply being in it (see schedule_repaint).
        self._was_in_alt: bool = self._in_alt()

        # Selection tracking to survive history overflow. pyte's history.top is a
        # bounded deque, so an overflow (or a scrollback clear) shifts every
        # absolute stack_row index a selection is expressed in. The screen's
        # history_generation is recorded alongside the selection and compared
        # on every repaint; once it has moved on, the stored rows no longer
        # delimit the text that was selected. Recording history.top's *length*
        # would not do: it also grows when the user merely scrolls up, which
        # shifts nothing and would drop the selection on every new line.
        self._sel_hist_gen: Optional[int] = None

        # Last reported mouse-motion cell (mode 1003 throttle)
        self._last_motion_cell: Optional[Tuple[int, int]] = None

        # High-resolution wheel accumulation: touchpads deliver angleDelta
        # values well below the 120 eighth-degree wheel step; they are
        # summed until a full step is reached.
        self._wheel_accumulator: float = 0.0

        # Visual bell flash state
        self._flash: bool = False

        # Memo caches for cell style resolution (see _cell_style /
        # _resolve_color); cleared on style reloads.
        self._style_cache: Dict[
            Tuple[Any, ...], Tuple[qt.QColor, qt.QColor, qt.QFont]
        ] = {}
        self._color_cache: Dict[str, qt.QColor] = {}

        # OSC 8 hyperlinks: the screen records spans in stack coordinates;
        # this per-cell {stack_row: {column: uri}} index is rebuilt only when
        # the span list changes. _link_version is (len, id of tail) so a
        # moved/redrawn link (new tail object) still invalidates it.
        self._link_index: Dict[int, Dict[int, str]] = {}
        self._link_version: Optional[Tuple[int, Optional[int]]] = None

        # Scrollbar
        self._scrollbar: qt.QScrollBar = qt.QScrollBar(qt.Qt.Orientation.Vertical, self)
        self._scrollbar.setRange(0, 0)
        self._scrollbar.valueChanged.connect(self._scroll_to_value)
        self._scrollbar.hide()

        # In-terminal "Copied to clipboard" toast: shown for the copies Ex.Co.
        # performs itself (native-selection auto-copy, the menu's Copy action).
        # A mouse-capturing TUI's right-click is forwarded to the app, which
        # draws its own banner (opencode), so Ex.Co. shows nothing for it.
        # Drawn over the grid; mouse-transparent so it never steals a click.
        self._copy_toast: qt.QLabel = qt.QLabel("", self)
        self._copy_toast.setAlignment(qt.Qt.AlignmentFlag.AlignCenter)
        self._copy_toast.setAttribute(
            qt.Qt.WidgetAttribute.WA_TransparentForMouseEvents
        )
        self._copy_toast.hide()
        self._copy_toast_timer: qt.QTimer = qt.QTimer(self)
        self._copy_toast_timer.setSingleShot(True)
        self._copy_toast_timer.setInterval(1300)
        self._copy_toast_timer.timeout.connect(self._copy_toast.hide)
        self._style_copy_toast()

    def event(self, event: Optional[qt.QEvent]) -> bool:
        # Claim every key for the shell: accepting ShortcutOverride vetoes
        # the main window's QAction shortcuts (Ctrl+P, Ctrl+W, Ctrl+N, ...)
        # so the key event reaches keyPressEvent instead of firing an action.
        if event is not None:
            if event.type() == qt.QEvent.Type.ShortcutOverride:
                event.accept()
                return True
            if event.type() == qt.QEvent.Type.KeyPress:
                key_event: qt.QKeyEvent = cast(qt.QKeyEvent, event)
                if key_event.key() in (
                    qt.Qt.Key.Key_Tab,
                    qt.Qt.Key.Key_Backtab,
                ):
                    # QWidget::event performs focus-friend navigation for
                    # Tab/Backtab without calling keyPressEvent (the focus
                    # moves to the tab bar). Forward Tab to the shell first.
                    self.keyPressEvent(key_event)
                    return True
        return super().event(event)

    # ------------------------------------------------------------------
    # Geometry / sizing
    # ------------------------------------------------------------------

    def _terminal_font(self) -> qt.QFont:
        """Font for the terminal: configured override or the editor font.

        The configured size is applied in both modes, so changing only the
        size also takes effect while the family is inherited.
        """
        font_name: Any = settings.get("terminal-font-name")
        font_size: Any = settings.get("terminal-font-size")
        if font_name:
            font: qt.QFont = qt.QFont(font_name)
        else:
            font = qt.QFont(settings.get_editor_font())
        if font_size:
            font.setPointSizeF(font_size)
        return font

    def _load_style(self) -> None:
        """(Re)apply the configured font and theme-derived default colors."""
        self._clear_selection()
        self._font: qt.QFont = self._terminal_font()
        self._font.setStyleHint(qt.QFont.StyleHint.Monospace)
        self._font.setFixedPitch(True)
        self.setFont(self._font)
        self._base_font: qt.QFont = qt.QFont(self._font)
        # Per-cell style font cache (see _cell_font)
        self._style_fonts = {}
        # Memo caches (see _cell_style / _resolve_color)
        self._style_cache = {}
        self._color_cache = {}
        theme: Any = settings.get_theme()
        self._default_fg: qt.QColor = qt.QColor(theme["fonts"]["default"]["color"])
        self._default_bg: qt.QColor = qt.QColor(theme["fonts"]["default"]["background"])
        self._measure_font()
        self._style_copy_toast()

    def _measure_font(self) -> None:
        font_metrics: qt.QFontMetricsF = qt.QFontMetricsF(self._font)
        self._char_width: float = max(font_metrics.horizontalAdvance("M"), 1.0)
        self._char_height: float = max(
            font_metrics.lineSpacing(), font_metrics.height(), 1.0
        )

    def _terminal_size(self) -> Tuple[int, int]:
        cols: int = max(int(self._content_width / self._char_width), 1)
        rows: int = max(int(self.height() / self._char_height), 1)
        return cols, rows

    def _row_band(self, y: int) -> qt.QRect:
        """Integer rectangle that fully covers the row's pixel band. The
        char height is often fractional (e.g. 13.3px), so naive rounding of
        the row rect would leave 1px gaps between adjacent rows that never
        get repainted; floor/ceil guarantees gapless coverage."""
        top: int = math.floor(y * self._char_height)
        bottom: int = math.ceil((y + 1) * self._char_height)
        return qt.QRect(0, top, self._content_width, bottom - top)

    def _recompute_geometry(self) -> None:
        scrollbar: qt.QScrollBar = self._scrollbar
        scrollbar_width: int = scrollbar.sizeHint().width()
        self._sb_visible = self._scroll_offset > 0
        scrollbar.setGeometry(
            self.width() - scrollbar_width,
            0,
            scrollbar_width,
            self.height(),
        )
        scrollbar.raise_()
        if not self._sb_visible:
            scrollbar.hide()
        else:
            scrollbar.show()
        self._content_width = self.width() - (
            scrollbar_width if self._sb_visible else 0
        )

    def resizeEvent(self, event: qt.QResizeEvent) -> None:  # type: ignore[override]
        self._clear_selection()
        self._recompute_geometry()
        cols: int
        rows: int
        cols, rows = self._terminal_size()
        self.resize_event.emit(cols, rows)
        self._place_copy_toast()
        return super().resizeEvent(event)

    # ------------------------------------------------------------------
    # Scrollback
    # ------------------------------------------------------------------

    def _in_alt(self) -> bool:
        return self.terminal.term_screen.in_alt_screen

    def _history_len(self) -> int:
        return len(self.terminal.term_screen.history.top)

    def _stack_row(self, viewport_y: int) -> int:
        """Map a viewport row to a row index in the (history + screen) stack."""
        return (self._history_len() - self._scroll_offset) + viewport_y

    def _stack_row_cells(self, stack_row: int) -> Any:
        """Return the cell row (StaticDefaultDict) for a stack row index."""
        screen: ExtendedScreen = self.terminal.term_screen
        history_len: int = self._history_len()
        if stack_row < history_len:
            return screen.history.top[stack_row]
        return screen.buffer[stack_row - history_len]

    def _scroll_up(self, rows: int) -> None:
        if self._in_alt():
            return
        self._scroll_offset = min(self._scroll_offset + rows, self._history_len())
        self._refresh_scrollbar()
        self.update()

    def _scroll_down(self, rows: int) -> None:
        if self._in_alt():
            return
        self._scroll_offset = max(self._scroll_offset - rows, 0)
        self._refresh_scrollbar()
        self.update()

    def _page_rows(self) -> int:
        return max(self.terminal.term_screen.lines - 1, 1)

    def _refresh_scrollbar(self) -> None:
        if self._in_alt():
            self._scroll_offset = 0
            self._sb_visible = False
            self._scrollbar.hide()
            self._recompute_geometry()
            return
        history_len: int = self._history_len()
        self._scrollbar.blockSignals(True)
        self._scrollbar.setRange(0, history_len)
        if not self._scrollbar.isSliderDown():
            # Leave the slider value alone while the user is dragging it so
            # new output does not fight the drag.
            self._scrollbar.setValue(history_len - self._scroll_offset)
        self._scrollbar.blockSignals(False)
        visible: bool = self._scroll_offset > 0
        if visible != self._sb_visible:
            self._recompute_geometry()

    def _scroll_to_value(self, value: int) -> None:
        self._scroll_offset = self._history_len() - value
        self.update()

    # ------------------------------------------------------------------
    # Repaint scheduling
    # ------------------------------------------------------------------

    def schedule_repaint(self) -> None:
        """
        Mark the recently changed screen lines for repaint and refresh the
        scrollbar. Multiple calls within one event-loop iteration are
        coalesced by Qt into a single paint event.
        """
        screen: ExtendedScreen = self.terminal.term_screen
        dirty: Any = screen.dirty
        pending_scroll: int = screen.pending_scroll
        lines: int = screen.lines
        if self._in_alt():
            self._scroll_offset = 0
            if not self._was_in_alt:
                # Just entered the alternate screen. A selection made on the
                # normal screen is expressed in that screen's stack rows and
                # would now highlight whatever the app happens to draw there,
                # so drop it. Only on the transition: selecting *inside* a
                # mouse-capturing TUI is supported (the Shift bypass and the
                # plain-drag overlay both rely on it).
                self._clear_selection()
        if self._selection is not None or self._selection_active:
            # The scrollback shifted under the selection (it overflowed or was
            # cleared), so its stored rows no longer delimit the text the user
            # selected. Copying would hand over whatever now occupies them.
            if self._sel_hist_gen != self._history_generation():
                self._clear_selection()
        self._was_in_alt = self._in_alt()
        if self._scroll_offset > 0:
            # History grew / content shifted; repaint everything visible.
            self.update()
        elif pending_scroll != 0:
            # Content scrolled a whole viewport's worth of lines. A full
            # repaint is cheap on a terminal-sized grid and avoids the
            # QWidget::scroll() artifacts seen on some platforms; the
            # cursor and selection overlays are repainted in the same pass.
            self.update()
        else:
            for y in dirty:
                if 0 <= y < lines:
                    self.update(self._row_band(y))
            cursor_y = screen.cursor.y
            if screen.cursor.hidden or cursor_y != self._last_cursor_y:
                # The cursor moved or vanished: repaint its previous cell so
                # the old block cursor does not linger (pyte cursor moves do
                # not mark rows dirty).
                if self._last_cursor_y is not None and 0 <= self._last_cursor_y < lines:
                    self.update(self._row_band(self._last_cursor_y))
                self._last_cursor_y = cursor_y if not screen.cursor.hidden else None
            self.update(self._row_band(cursor_y))
        dirty.clear()
        # The scroll delta is only meaningful for the chunk just fed; consume
        # it so a second schedule_repaint in the same iteration does not
        # trigger another full repaint.
        screen.pending_scroll = 0
        self._refresh_scrollbar()

    def _on_blink(self) -> None:
        if not self.isVisible():
            return
        screen: ExtendedScreen = self.terminal.term_screen
        lines: int = screen.lines
        # SGR-5 cells blink on their own phase, driven only by the rows that
        # actually carry one. This is deliberately independent of the cursor
        # below: a hidden cursor, or a steady DECSCUSR style, must not stop
        # text from blinking. The set is maintained by the paint pass, so this
        # is O(blinking rows) - and, unlike a rescan of 'screen.buffer', it
        # covers scrollback rows too: a blinking line that has scrolled out of
        # the live buffer is still on screen and would otherwise freeze
        # mid-phase.
        if self._blink_rows:
            self._sgr_blink_phase = not self._sgr_blink_phase
            for y in self._blink_rows:
                if 0 <= y < lines:
                    self.update(self._row_band(y))
        # The cursor blinks unless it is hidden or the application asked for a
        # steady style (DECSCUSR with an even parameter). Only the cursor cells
        # (previous + current row) change on its phase toggle; no need to
        # repaint the whole viewport.
        if not screen.cursor.hidden and screen.cursor_blink:
            self._blink_phase = not self._blink_phase
            if self._last_cursor_y is not None and 0 <= self._last_cursor_y < lines:
                self.update(self._row_band(self._last_cursor_y))
            if 0 <= screen.cursor.y < lines:
                self.update(self._row_band(screen.cursor.y))
        else:
            # Park on the visible phase, so a cursor that reappears - or a
            # style change back to a blinking one - is never caught mid-blink.
            self._blink_phase = True

    def flash(self) -> None:
        """Visual bell: briefly lighten the viewport."""
        self._flash = True
        self.update()
        qt.QTimer.singleShot(150, self._clear_flash)

    def _clear_flash(self) -> None:
        self._flash = False
        self.update()

    # ------------------------------------------------------------------
    # Color resolution
    # ------------------------------------------------------------------

    def _resolve_color(self, color_string: str, is_fg: bool) -> qt.QColor:
        if color_string in FOREGROUND_COLOR_MAP:
            color: Optional[qt.QColor] = FOREGROUND_COLOR_MAP[color_string]
            if color is not None:
                return color
            return self._default_fg if is_fg else self._default_bg
        if color_string == "default":
            return self._default_fg if is_fg else self._default_bg
        color = self._color_cache.get(color_string)
        if color is None:
            if color_string.startswith("#"):
                color = qt.QColor(color_string)
            else:
                color = qt.QColor("#" + color_string)
            self._color_cache[color_string] = color
        return color

    # ------------------------------------------------------------------
    # Painting
    # ------------------------------------------------------------------

    def paintEvent(self, event: qt.QPaintEvent) -> None:  # type: ignore[override]
        painter: qt.QPainter = qt.QPainter(self)
        painter.fillRect(event.rect(), self._default_bg)
        if self._flash:
            painter.fillRect(event.rect(), qt.QColor(255, 255, 255, 40))
        screen: ExtendedScreen = self.terminal.term_screen
        lines: int = screen.lines
        columns: int = screen.columns
        for y in range(lines):
            stack_row: int = self._stack_row(y)
            if stack_row < 0:
                break
            if not event.rect().intersects(self._row_band(y)):
                continue
            row: Any = self._stack_row_cells(stack_row)
            self._paint_cells(painter, y, row, columns)
        self._paint_cursor(painter)
        painter.end()

    def _paint_cells(
        self, painter: qt.QPainter, y: int, row: Any, columns: int
    ) -> None:
        cell_width: float = self._char_width
        cell_height: float = self._char_height
        x: int = 0
        last_pen: Optional[qt.QColor] = None
        last_font: Optional[qt.QFont] = None
        # Whether any cell of this row carries SGR-5 blink. The paint loop
        # already reads 'blink' off every cell it lays out (see the run loop
        # below), so tracking it here costs one assignment per cell and keeps
        # _on_blink from having to rescan the grid on every tick.
        row_blinks: bool = False
        while x < columns:
            cell: Any = row[x]
            style: Tuple[qt.QColor, qt.QColor, qt.QFont] = self._cell_style(cell, y, x)
            run_text: List[str] = []
            run_start: int = x
            needs_clip: bool = False
            while x < columns:
                current: Any = row[x]
                if current.blink:
                    # Recorded before the style break below, so the cell that
                    # ends the run is counted too.
                    row_blinks = True
                if self._cell_style(current, y, x) != style:
                    break
                char_w: int = wcwidth(current.data)
                # A full-width character and its trailing stub (pyte marks
                # the stub with empty data) form one atomic unit: absorb the
                # stub unconditionally so selection or style changes at the
                # stub can never split the glyph into a one-cell box.
                if x + 1 < columns and char_w == 2 and row[x + 1].data == "":
                    run_text.append(current.data)
                    x += 2
                    continue
                char: str = current.data
                if char == "" or (current.blink and not self._sgr_blink_phase):
                    char = " "
                    char_w = 1
                if char_w == 2:
                    # Wide glyph without a stub (last column): it cannot lay
                    # out at natural width in a one-cell rect, so clip the
                    # run so the glyph cannot bleed into the neighbor cell.
                    needs_clip = True
                run_text.append(char)
                x += 1
            rect: qt.QRectF = qt.QRectF(
                run_start * cell_width,
                y * cell_height,
                (x - run_start) * cell_width,
                cell_height,
            )
            if style[1] != self._default_bg:
                # The viewport background is already painted in paintEvent;
                # only runs with a non-default background need a fill.
                painter.fillRect(rect, style[1])
            if run_text:
                if style[0] != last_pen:
                    painter.setPen(style[0])
                    last_pen = style[0]
                if style[2] != last_font:
                    painter.setFont(style[2])
                    last_font = style[2]
                if needs_clip:
                    painter.save()
                    painter.setClipRect(rect)
                painter.drawText(
                    rect,
                    qt.Qt.AlignmentFlag.AlignLeft | qt.Qt.AlignmentFlag.AlignVCenter,
                    "".join(run_text),
                )
                if needs_clip:
                    painter.restore()
        # Publish (or retract) this row for the blink tick. Retracting matters
        # as much as publishing: a row whose blinking cells were overwritten
        # must stop being repainted on every phase toggle.
        if row_blinks:
            self._blink_rows.add(y)
        else:
            self._blink_rows.discard(y)

    def _cell_font(self, cell: Any, link: bool = False) -> qt.QFont:
        """Styled font for a cell, drawn from a small cache keyed on the
        style flags (bold/italic/underline/strike) and the OSC 8 hyperlink
        state, so painting does not allocate a fresh QFont for every cell."""
        key: Tuple[bool, bool, bool, bool] = (
            cell.bold,
            cell.italics,
            cell.underscore or link,
            cell.strikethrough,
        )
        font: Optional[qt.QFont] = self._style_fonts.get(key)
        if font is None:
            font = qt.QFont(self._base_font)
            if cell.bold:
                font.setBold(True)
            if cell.italics:
                font.setItalic(True)
            if cell.underscore or link:
                font.setUnderline(True)
            if cell.strikethrough:
                font.setStrikeOut(True)
            self._style_fonts[key] = font
        return font

    def _cell_style(
        self, cell: Any, y: int, x: int
    ) -> Tuple[qt.QColor, qt.QColor, qt.QFont]:
        link: bool = self._link_at_stack(self._stack_row(y), x) is not None
        key: Tuple[Any, ...] = (
            cell.bg,
            cell.fg,
            cell.bold,
            cell.italics,
            cell.underscore,
            cell.strikethrough,
            cell.reverse,
            self._is_selected(y, x),
            link,
        )
        style: Optional[Tuple[qt.QColor, qt.QColor, qt.QFont]] = self._style_cache.get(
            key
        )
        if style is None:
            reverse: bool = cell.reverse
            bg: qt.QColor = self._resolve_color(cell.bg, False)
            fg: qt.QColor = self._resolve_color(cell.fg, True)
            if reverse:
                fg, bg = bg, fg
            font: qt.QFont = self._cell_font(cell, link=link)
            if self._is_selected(y, x):
                fg, bg = bg, fg
            style = (fg, bg, font)
            self._style_cache[key] = style
        return style

    def _paint_cursor(self, painter: qt.QPainter) -> None:
        screen: ExtendedScreen = self.terminal.term_screen
        if self._scroll_offset != 0 or screen.cursor.hidden:
            return
        # A live selection deliberately does NOT suppress the cursor: it
        # outlives the gesture (only a bare anchor is cleared on release), so
        # hiding it left the shell with no visible cursor at all while the
        # user typed.  The block style below paints its own inversion, so it
        # stays legible on a highlighted cell.
        x: int = screen.cursor.x
        y: int = screen.cursor.y
        if y >= screen.lines or x >= screen.columns:
            return
        if screen.cursor_blink and not self._blink_phase:
            return
        row: Any = screen.buffer[y]
        cell: Any = row[x]
        fg: qt.QColor = self._resolve_color(cell.fg, True)
        bg: qt.QColor = self._resolve_color(cell.bg, False)
        if cell.reverse:
            fg, bg = bg, fg
        cursor_style: str = screen.cursor_style
        char: str = cell.data if cell.data != "" else " "
        wide: bool = wcwidth(char) == 2
        has_stub: bool = wide and x + 1 < screen.columns and row[x + 1].data == ""
        rect: qt.QRectF = qt.QRectF(
            x * self._char_width,
            y * self._char_height,
            self._char_width * (2 if has_stub else 1),
            self._char_height,
        )
        clip_glyph: bool = wide and not has_stub
        if cursor_style == "underline":
            underline: qt.QRectF = qt.QRectF(
                rect.x(),
                rect.y() + rect.height() - max(self._char_height * 0.15, 2.0),
                rect.width(),
                max(self._char_height * 0.15, 2.0),
            )
            painter.fillRect(underline, fg)
            painter.setPen(fg)
            painter.setFont(self._cell_font(cell))
            if clip_glyph:
                painter.save()
                painter.setClipRect(rect)
            painter.drawText(
                rect,
                qt.Qt.AlignmentFlag.AlignLeft | qt.Qt.AlignmentFlag.AlignVCenter,
                char,
            )
            if clip_glyph:
                painter.restore()
        elif cursor_style == "bar":
            bar: qt.QRectF = qt.QRectF(
                rect.x(),
                rect.y(),
                max(self._char_width * 0.15, 2.0),
                rect.height(),
            )
            painter.fillRect(bar, fg)
        else:
            # Block cursor inverts the painted cell: fill with the painted
            # foreground and draw the glyph in the painted background so the
            # block stays visible on plain, reverse-video and highlighted
            # cells alike.  (Filling with the background and drawing the
            # glyph in the foreground would reproduce the cell exactly and
            # make the cursor invisible.)
            painter.fillRect(rect, fg)
            painter.setPen(bg)
            painter.setFont(self._cell_font(cell))
            if clip_glyph:
                painter.save()
                painter.setClipRect(rect)
            painter.drawText(
                rect,
                qt.Qt.AlignmentFlag.AlignLeft | qt.Qt.AlignmentFlag.AlignVCenter,
                char,
            )
            if clip_glyph:
                painter.restore()

    # ------------------------------------------------------------------
    # Selection
    # ------------------------------------------------------------------

    def _history_generation(self) -> int:
        """The screen's history_generation, stamped onto a selection when it is
        made so a later shift of the scrollback can be detected."""
        screen: ExtendedScreen = self.terminal.term_screen
        return screen.history_generation

    def _pos_cell(self, position: qt.QPointF) -> Tuple[int, int]:
        screen: ExtendedScreen = self.terminal.term_screen
        cols: int = screen.columns
        lines: int = screen.lines
        x: int = int(position.x() / self._char_width)
        y: int = int(position.y() / self._char_height)
        x = max(0, min(x, cols - 1))
        y = max(0, min(y, lines - 1))
        return self._stack_row(y), x

    def _selection_viewport_corners(
        self,
    ) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Normalized selection corners mapped to (row, col) viewport cells
        for a synthetic drag, or None when no part of the selection is above
        the visible region. Off-screen corners are clamped onto the bottom
        edge so the replay still spans the visible highlight."""
        bounds: Optional[Selection] = self._selection_bounds()
        if bounds is None:
            return None
        r0, c0, r1, c1 = cast(Tuple[int, int, int, int], bounds)
        if (r0, c0) > (r1, c1):
            r0, c0, r1, c1 = r1, c1, r0, c0
        screen: ExtendedScreen = self.terminal.term_screen
        lines: int = screen.lines
        top: int = self._history_len() - self._scroll_offset
        v_r0: int = r0 - top
        v_r1: int = r1 - top
        # Entire selection lives outside the viewport: forward the plain
        # right-click instead of replaying a drag that would not match what
        # the user sees.
        if v_r0 < 0 and v_r1 < 0:
            return None
        if v_r0 > lines - 1 and v_r1 > lines - 1:
            return None
        v_r0 = max(0, min(v_r0, lines - 1))
        v_r1 = max(0, min(v_r1, lines - 1))
        return (v_r0, c0), (v_r1, c1)

    def _selection_bounds(self) -> Optional[Selection]:
        """Normalize _selection to (r0, c0, r1, c1); a bare anchor is a
        single-cell selection. Returns None when there is no selection."""
        sel: Optional[Selection] = self._selection
        if sel is None:
            return None
        if len(sel) == 2:
            r, c = cast(Tuple[int, int], sel)
            return r, c, r, c
        return sel

    def _is_selected(self, y: int, x: int) -> bool:
        if self._selection is None:
            return False
        stack_row: int = self._stack_row(y)
        if stack_row < 0:
            return False
        bounds: Optional[Selection] = self._selection_bounds()
        if bounds is None:
            return False
        r0, c0, r1, c1 = cast(Tuple[int, int, int, int], bounds)
        # Normalize reverse drags (start after end) so the highlight is
        # correct while the mouse is still held down.
        if (r0, c0) > (r1, c1):
            r0, c0, r1, c1 = r1, c1, r0, c0
        if r0 == r1:
            return stack_row == r0 and c0 <= x <= c1
        if r0 < stack_row < r1:
            return True
        if stack_row == r0:
            return x >= c0
        if stack_row == r1:
            return x <= c1
        return False

    def _selection_text(self) -> str:
        bounds: Optional[Selection] = self._selection_bounds()
        if bounds is None:
            return ""
        r0, c0, r1, c1 = cast(Tuple[int, int, int, int], bounds)
        if (r0, c0) > (r1, c1):
            r0, c0, r1, c1 = r1, c1, r0, c0
        columns: int = self.terminal.term_screen.columns
        lines: List[str] = []
        for stack_row in range(r0, r1 + 1):
            row: Any = self._stack_row_cells(stack_row)
            start: int = c0 if stack_row == r0 else 0
            end: int = c1 if stack_row == r1 else columns - 1
            text: str = "".join(row[x].data for x in range(start, end + 1))
            lines.append(text.rstrip())
        return "\n".join(lines)

    def copy_selection(self) -> None:
        text: str = self._selection_text()
        if text:
            application: Any = data.application
            application.clipboard().setText(text)
            self._show_copy_toast()

    def _style_copy_toast(self) -> None:
        """Theme the "Copied to clipboard" panel from the terminal's default
        foreground/background so it stays readable on any palette."""
        toast: Optional[qt.QLabel] = getattr(self, "_copy_toast", None)
        if toast is None:
            return
        fg: qt.QColor = qt.QColor(self._default_fg)
        bg: qt.QColor = qt.QColor(self._default_bg)
        toast.setStyleSheet(
            "background-color: rgba({0},{1},{2},235);"
            "color: rgba({3},{4},{5},255);"
            "border: 1px solid rgba({3},{4},{5},150);"
            "border-radius: 4px;"
            "padding: 2px 10px;".format(
                bg.red(),
                bg.green(),
                bg.blue(),
                fg.red(),
                fg.green(),
                fg.blue(),
            )
        )

    def _place_copy_toast(self) -> None:
        """Centre the copy toast at the top of the viewport (or re-centre it
        after a resize) while it is visible."""
        if not self._copy_toast.isVisibleTo(self):
            return
        self._copy_toast.adjustSize()
        self._copy_toast.move(
            max((self.width() - self._copy_toast.width()) // 2, 0),
            max(int(self._char_height * 0.75), 4),
        )
        self._copy_toast.raise_()

    def _show_copy_toast(self) -> None:
        """Show the transient "Copied to clipboard" panel and (re)arm its
        hide timer."""
        self._copy_toast.setText("Copied to clipboard")
        self._copy_toast.show()
        self._place_copy_toast()
        self._copy_toast_timer.stop()
        self._copy_toast_timer.start()

    def paste(self) -> None:
        text: str = self._paste_source()
        if text:
            if self.terminal.term_screen.bracketed_paste:
                text = "\x1b[200~" + text + "\x1b[201~"
            self.paste_event.emit(text)

    def _paste_source(self) -> str:
        """Text for a paste: the current selection, falling back to the
        clipboard (the X11 primary-selection convention shared by the
        middle-click paste and the context menu's Paste action)."""
        selected: str = self._selection_text()
        if selected:
            return selected
        application: Any = data.application
        return application.clipboard().text()

    def _snap_col(self, stack_row: int, col: int, forward: bool) -> int:
        """Widen a selection edge so it lands on a whole glyph.

        A double-width glyph covers two cells, the second left empty as its
        stub. An edge starting on a stub would paint only half of its glyph
        and an edge stopping on a glyph would leave half of it unpainted --
        and because the stub contributes no character to the copied text,
        the glyph would be dropped from the copy as well."""
        row: Any = self._stack_row_cells(stack_row)
        columns: int = self.terminal.term_screen.columns
        if forward:
            if col + 1 < columns and row[col + 1].data == "":
                if wcwidth(row[col].data or "") == 2:
                    return col + 1
            return col
        owner: Optional[int] = self._wide_stub_owner(row, col)
        return col if owner is None else owner

    def _start_selection(self, position: qt.QPointF) -> None:
        stack_row, col = self._pos_cell(position)
        self._selection = (
            stack_row,
            self._snap_col(stack_row, col, forward=False),
        )
        self._press_cell = self._pos_cell(position)
        self._selection_active = True
        self._sel_hist_gen = self._history_generation()
        self.update()

    def _extend_selection(self, position: qt.QPointF) -> bool:
        """Grow the existing selection to *position* (Shift+click; Shift+drag
        reuses the same anchor through _update_selection). Returns False when
        there is nothing to extend, so the caller starts a fresh selection.

        The anchor stays the endpoint the gesture originally pressed on, which
        is what _update_selection already uses for a drag -- picking the
        nearest endpoint here instead would make a press alone and a
        press-then-drag re-anchor differently. Shift+click inside the range
        therefore trims it toward the anchor, as shift+Home does in an
        editor."""
        start: Optional[Selection] = self._selection
        if start is None or len(start) == 2:
            # Only a bare anchor is there, so there is no range to grow; the
            # caller falls back to a plain click.
            return False
        self._selection_active = True
        self._press_cell = self._pos_cell(position)
        self._update_selection(position)
        return True

    def _clear_selection(self) -> None:
        """
        Drop the current selection. Called when the cell grid geometry
        changes (resize, font change): stored cell coordinates would
        otherwise point at unrelated cells. Tolerates being called from
        _load_style before the selection state is initialized.
        """
        had_selection: bool = getattr(self, "_selection", None) is not None or getattr(
            self, "_selection_active", False
        )
        self._selection = None
        self._selection_active = False
        self._sel_hist_gen = None
        if had_selection:
            self.update()

    def _update_selection(self, position: qt.QPointF) -> None:
        if not self._selection_active:
            return
        start: Optional[Selection] = self._selection
        if start is None:
            return
        end: Tuple[int, int] = self._pos_cell(position)
        anchor_row, anchor_col = start[0], start[1]
        end_row, end_col = end
        if (end_row, end_col) < (anchor_row, anchor_col):
            # Dragged up and/or left of the anchor, so the anchor is now the
            # far edge and has to widen forwards rather than backwards.
            anchor_col = self._snap_col(anchor_row, anchor_col, forward=True)
            end_col = self._snap_col(end_row, end_col, forward=False)
        else:
            end_col = self._snap_col(end_row, end_col, forward=True)
        self._selection = (anchor_row, anchor_col, end_row, end_col)
        self._sel_hist_gen = self._history_generation()
        self.update()

    def _end_selection(self) -> None:
        self._selection_active = False
        bounds: Optional[Selection] = self._selection_bounds()
        if bounds is None:
            return
        bare_anchor: bool = (
            isinstance(self._selection, tuple) and len(self._selection) == 2
        )
        r0, c0, r1, c1 = cast(Tuple[int, int, int, int], bounds)
        if bare_anchor:
            # A plain click without drag: no selection, so the shell cursor
            # stays/returns to the active text line. A resolved word/line
            # selection or a real drag is a 4-tuple and survives even when it
            # spans exactly one cell (e.g. a single-char word double-click).
            self._selection = None
        elif (r0, c0) > (r1, c1):
            self._selection = (r1, c1, r0, c0)
        if self._selection is not None and self._auto_copy_enabled():
            self.copy_selection()
        self.update()

    def _auto_copy_enabled(self) -> bool:
        """True when a finished selection is copied to the clipboard on
        release. Behind the ``editor.auto_copy_on_select`` setting (default
        off); the editor facade is shared with the main editor widgets."""
        screen: ExtendedScreen = self.terminal.term_screen
        if screen.mouse_mode != 0:
            # A mouse-capturing application owns the copy/selection semantics
            # (e.g. opencode draws its own "Copied to clipboard" toast on its
            # own copy). Avoid double-copying when a TUI drag was forwarded.
            return False
        editor_settings: Any = settings.get("editor")
        return bool(editor_settings.get("auto_copy_on_select", False))

    def _cell_blank(self, row: Any, x: int) -> bool:
        """True when the cell holds no visible glyph: a plain space, or the
        empty trailing cell of a wide glyph."""
        char: str = row[x].data or ""
        return char == "" or char.isspace()

    def _wide_stub_owner(self, row: Any, x: int) -> Optional[int]:
        """Column of the wide glyph whose trailing stub sits at *x*, else None.

        pyte keeps a double-width glyph in one cell and leaves the next cell
        empty as its continuation, so that empty cell is part of a visible
        character rather than whitespace."""
        if x <= 0 or row[x].data != "":
            return None
        previous: str = row[x - 1].data or ""
        return x - 1 if wcwidth(previous) == 2 else None

    def _word_boundary(self, row: Any, x: int) -> bool:
        """True when the cell at *x* ends the word being scanned: real
        whitespace, or any empty cell that is not a wide glyph's stub.

        Without the stub exemption every double-width glyph terminates a word,
        so a space-free script (CJK) could only ever be selected one character
        at a time."""
        if self._wide_stub_owner(row, x) is not None:
            return False
        return self._cell_blank(row, x)

    def _word_range(
        self, position: qt.QPointF
    ) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """Return (start_cell, end_cell) of the whitespace-delimited word
        under *position*. Both cells share the clicked stack row; the range
        always includes the clicked cell (which may be a single glyph)."""
        stack_row, col = self._pos_cell(position)
        row: Any = self._stack_row_cells(stack_row)
        columns: int = self.terminal.term_screen.columns
        # Clicking the stub half of a wide glyph selects the word that glyph
        # belongs to, exactly as clicking the glyph itself does.
        owner: Optional[int] = self._wide_stub_owner(row, col)
        if owner is not None:
            col = owner
        start: int = col
        while start > 0 and not self._word_boundary(row, start - 1):
            start -= 1
        end: int = col
        while end < columns - 1 and not self._word_boundary(row, end + 1):
            end += 1
        return (stack_row, start), (stack_row, end)

    def _select_word(self, position: qt.QPointF) -> None:
        """Select the word under *position* (double-click). Clicking blank
        space collapses the pending selection instead."""
        stack_row, col = self._pos_cell(position)
        row: Any = self._stack_row_cells(stack_row)
        owner: Optional[int] = self._wide_stub_owner(row, col)
        if owner is not None:
            col = owner
        if self._cell_blank(row, col):
            self._selection = None
            self._selection_active = False
            self.update()
            return
        start, end = self._word_range(position)
        self._selection = (start[0], start[1], end[0], end[1])
        self._selection_active = True
        self._sel_hist_gen = self._history_generation()
        self.update()

    def _select_line(self, position: qt.QPointF) -> None:
        """Select the whole physical line under *position* (triple-click).
        Trailing blanks are already trimmed by _selection_text."""

        stack_row: int = self._pos_cell(position)[0]
        columns: int = self.terminal.term_screen.columns
        self._selection = (stack_row, 0, stack_row, columns - 1)
        self._selection_active = True
        self._sel_hist_gen = self._history_generation()
        self.update()

    def _arm_triple_click(self) -> None:
        """Arm the requirement that a third press within the system
        double-click interval selects a whole line."""
        self._double_clicked = True
        self._triple_click_timer.start()

    def _triple_click_expired(self) -> None:
        self._double_clicked = False

    # ------------------------------------------------------------------
    # Mouse
    # ------------------------------------------------------------------

    def _mouse_cell(self, position: qt.QPointF) -> Tuple[int, int]:
        x: int = int(position.x() / self._char_width)
        y: int = int(position.y() / self._char_height)
        return x, y

    def _refresh_link_index(self) -> None:
        """Rebuild the cell->URI lookup from screen.hyperlink_spans when the
        span list changed. Spans are recorded in stack coordinates (draw()
        logs the absolute cursor position), so the index maps a stack_row to
        {column: uri} and renders identically over scrollback history."""
        screen: ExtendedScreen = self.terminal.term_screen
        spans: List[Tuple[Tuple[int, int], Tuple[int, int], str]] = (
            screen.hyperlink_spans
        )
        version: Tuple[int, Optional[int]] = (
            len(spans),
            id(spans[-1]) if spans else None,
        )
        if version == self._link_version:
            return
        index: Dict[int, Dict[int, str]] = {}
        columns: int = screen.columns
        for (r0, c0), (r1, c1), uri in spans:
            for r in range(r0, r1 + 1):
                start: int = c0 if r == r0 else 0
                end: int = c1 if r == r1 else columns - 1
                for x in range(start, end + 1):
                    index.setdefault(r, {})[x] = uri
        self._link_index = index
        self._link_version = version

    def _link_at_stack(self, stack_row: int, x: int) -> Optional[str]:
        """URI of the hyperlink covering stack cell (stack_row, x), if any."""
        if stack_row < 0:
            return None
        self._refresh_link_index()
        row_index: Optional[Dict[int, str]] = self._link_index.get(stack_row)
        if row_index is None:
            return None
        return row_index.get(x)

    def _hyperlink_at(self, position: qt.QPointF) -> Optional[str]:
        stack_row: int
        x: int
        stack_row, x = self._pos_cell(position)
        return self._link_at_stack(stack_row, x)

    def _maybe_activate_hyperlink(self, position: qt.QPointF) -> None:
        """Open the URI under the release cell when this left press was a
        plain click on the spot: press and release in the same cell, no drag,
        no surviving selection and not part of a double/triple-click. Drags
        keep their selection (which trumps the open) and are blocked anyway."""
        if self._double_clicked:
            return
        press_cell: Optional[Tuple[int, int]] = self._press_cell
        self._press_cell = None
        if press_cell is None:
            return
        if self._pos_cell(position) != press_cell:
            return
        if self._selection is not None:
            return
        uri: Optional[str] = self._hyperlink_at(position)
        if uri is not None:
            functions.open_url(uri)

    def _mouse_button_code(self, button: qt.Qt.MouseButton) -> int:
        if button == qt.Qt.MouseButton.LeftButton:
            return 0
        if button == qt.Qt.MouseButton.MiddleButton:
            return 1
        if button == qt.Qt.MouseButton.RightButton:
            return 2
        return 0

    def _mouse_report(
        self,
        button: int,
        x: int,
        y: int,
        pressed: bool = True,
        wheel: bool = False,
        motion: bool = False,
        horizontal: bool = False,
        drag: bool = False,
    ) -> None:
        """Emit a mouse report to the application when a mouse mode is set."""
        screen: ExtendedScreen = self.terminal.term_screen
        if screen.mouse_mode == 0:
            return
        cx: int = x + 1
        cy: int = y + 1
        if wheel:
            if horizontal:
                # Horizontal wheel: xterm buttons 66 (left) / 67 (right)
                code: int = 67 if button > 0 else 66
            else:
                # Vertical wheel: xterm buttons 4 (up, 64) / 5 (down, 65)
                code = 64 if button > 0 else 65
        elif motion:
            # Motion without a button pressed (mode 1003)
            code = 35
        elif drag:
            # Motion with a button held (drag): the SGR motion bit (32) OR'd
            # with the held button, emitted as a release-style 'm' pressRelease
            # -- the xterm/WezTerm convention openTUI's own MockMouse also
            # produces. openTUI's core only grows its selection from these
            # "drag" events; forwarding the button alone (a burst of downs) is
            # what left opencode with no selectable region to copy and no
            # "Copied to clipboard" toast. Without SGR the distinction is
            # inexpressible, so fall back to the plain button code.
            code = (32 | button) if screen.sgr_mouse else button
        elif pressed:
            code = button
        elif screen.sgr_mouse:
            # SGR (1006) marks the release with the SAME button number in a
            # lowercase 'm' (the xterm/WeZTerm convention). openTUI reads
            # button = raw & 3, so keeping the number is what actually unbinds
            # the held button on release; the old button+3 encoding left the
            # app's "pressed" set dirty.
            code = button
        else:
            # X10-style has no release marker: the release uses button + 3
            # (left=3, middle=4, right=5).
            code = button + 3
        if screen.sgr_mouse:
            # SGR (1006): CSI < b ; x ; y M/m. Motion-drags use the lowercase
            # 'm' pressRelease like the xterm/WezTerm convention.
            press_char: str = "M" if (pressed and not drag) else "m"
            self.send_text.emit("\x1b[<{};{};{}{}".format(code, cx, cy, press_char))
        else:
            # X10-style: CSI M b+32 x+32 y+32. The encoding is limited to
            # 223 columns/rows; larger coordinates are clipped, matching
            # xterm (otherwise chr() wraps into the C0 control range and
            # the application receives garbage).
            cx = min(cx, 223)
            cy = min(cy, 223)
            self.send_text.emit("\x1b[M" + chr(code + 32) + chr(cx + 32) + chr(cy + 32))

    def _handle_click_focus(self) -> None:
        """Grab focus and announce it, then match the editor widgets: any
        click outside the overlays closes the settings panel and the
        function wheel."""
        self.setFocus()
        self.focused.emit()
        main_form: Any = getattr(self.terminal, "main_form", None)
        if main_form is not None:
            view: Any = getattr(main_form, "view", None)
            if view is not None and hasattr(view, "hide_all_overlay_widgets"):
                view.hide_all_overlay_widgets()

    def mousePressEvent(self, event: qt.QMouseEvent) -> None:  # type: ignore[override]
        self._handle_click_focus()
        # Ctrl+click opens the hyperlink under the pointer in every mouse
        # mode: a mouse-capturing TUI (vim, htop) must not be able to
        # swallow a deliberate link click.
        if (
            event.button() == qt.Qt.MouseButton.LeftButton
            and event.modifiers() & qt.Qt.KeyboardModifier.ControlModifier
        ):
            uri: Optional[str] = self._hyperlink_at(event.position())
            if uri is not None:
                functions.open_url(uri)
                # A deliberate link click is not a press the app should ever
                # see: drop the anchor so the release reports nothing.
                self._press_cell = None
                event.accept()
                return
        screen: ExtendedScreen = self.terminal.term_screen
        if screen.mouse_mode != 0:
            # A new press inside a mouse-capturing app starts a fresh
            # gesture; the previous gesture's right-click flags are gone.
            self._tui_right_forwarded = False
            self._tui_right_synth = False
            if event.modifiers() & qt.Qt.KeyboardModifier.ShiftModifier:
                # Shift bypass: the app never sees the event, so native
                # selection works inside mouse-capturing TUIs (OpenCode, ...).
                self._shift_selecting = True
                self._last_motion_cell = None
                if event.button() == qt.Qt.MouseButton.LeftButton:
                    # Shift extends the overlay selection rather than
                    # restarting it; with none, it starts a fresh one.
                    if not self._extend_selection(event.position()):
                        self._press_select(event.position())
                event.accept()
                return
            self._shift_selecting = False
            self._last_motion_cell = None
            if event.button() == qt.Qt.MouseButton.MiddleButton:
                # Middle-click paste: the decided default makes the selection
                # (falling back to the clipboard) the paste source, exactly
                # like the menu's Paste action, even while an app captures
                # the mouse.
                self.paste()
                event.accept()
                return
            if event.button() == qt.Qt.MouseButton.RightButton:
                # The TUI owns the right button (WezTerm parity): forward press
                # and release so the app performs its own copy and draws its own
                # toast (opencode's "Copied to clipboard"). opencode clears its
                # own selection at the drag's release (copy-on-select), so before
                # the forward it must be rebuilt: replay the native selection as a
                # short synthetic left-drag between the two selection corners, then
                # hand the right-click to the app while it still "holds" the left
                # button. With no native selection the click forwards alone; if the
                # selection is entirely off-screen it falls back to that too.
                rx: int
                ry: int
                rx, ry = self._mouse_cell(event.position())
                if self._selection is not None:
                    corners: Optional[Tuple[Tuple[int, int], Tuple[int, int]]] = (
                        self._selection_viewport_corners()
                    )
                    if corners is not None:
                        (r0, c0), (r1, c1) = corners
                        # Replay the native selection as a real left-drag the
                        # way openTUI's MockMouse builds one (down at one
                        # corner, then SGR motion-drags stepping to the other,
                        # keeping the button held). The corner-pair-only burst
                        # produced "down" events openTUI never grows a
                        # selection from, leaving its renderer selection
                        # empty -- and with it opencode's copy-on-select (and
                        # its "Copied to clipboard" toast) silent.
                        self._mouse_report(0, c0, r0, pressed=True)
                        for step in range(1, 6):
                            sr: int = r0 + round((r1 - r0) * step / 5)
                            sc: int = c0 + round((c1 - c0) * step / 5)
                            self._mouse_report(0, sc, sr, drag=True)
                        self._tui_right_synth = True
                self._tui_right_forwarded = True
                self._mouse_report(2, rx, ry, pressed=True)
                event.accept()
                return
            # A left press is reported immediately (a standard terminal
            # forwards the gesture) and anchors the native selection overlay
            # drawn on top; the drag follows as SGR motion-drags (see
            # mouseMoveEvent), so opencode builds its own selection and draws
            # its "Copied to clipboard" toast on release, while the
            # highlighted overlay gives the right-click a selection to replay
            # into the app.
            x: int
            y: int
            x, y = self._mouse_cell(event.position())
            self._mouse_report(0, x, y, pressed=True)
            self._press_select(event.position())
            event.accept()
            return
        if event.button() == qt.Qt.MouseButton.MiddleButton:
            self.paste()
            event.accept()
            return
        if event.button() == qt.Qt.MouseButton.LeftButton:
            shifted: bool = bool(
                event.modifiers() & qt.Qt.KeyboardModifier.ShiftModifier
            )
            # Shift extends what is already selected instead of throwing it
            # away and starting over; with nothing selected it stays a plain
            # click. (Inside a mouse-capturing TUI Shift means "bypass" and
            # returns above.)
            if not (shifted and self._extend_selection(event.position())):
                self._press_select(event.position())
        # A right-click keeps the selection so the context menu's Copy
        # action stays enabled; the next left-press starts a new selection.
        # Accept the press so the ignored default QWidget handling does not
        # propagate it up to the tab widget (which would steal focus)
        event.accept()

    def _press_select(self, position: qt.QPointF) -> None:
        """Start a selection on a left press, honouring a triple-click: a
        third press within the double-click interval selects the whole line
        instead of starting a drag."""
        if self._double_clicked:
            self._select_line(position)
            self._double_clicked = False
            self._triple_click_timer.stop()
        else:
            self._start_selection(position)

    def mouseDoubleClickEvent(self, event: qt.QMouseEvent) -> None:  # type: ignore[override]
        if event.button() != qt.Qt.MouseButton.LeftButton:
            event.ignore()
            return super().mouseDoubleClickEvent(event)
        self._handle_click_focus()
        self._select_word(event.position())
        self._arm_triple_click()
        event.accept()

    def focusInEvent(self, event: qt.QFocusEvent) -> None:  # type: ignore[override]
        self.focused.emit()
        if self.terminal.term_screen.focus_report:
            self.send_text.emit("\x1b[I")
        return super().focusInEvent(event)

    def focusOutEvent(self, event: qt.QFocusEvent) -> None:  # type: ignore[override]
        if self.terminal.term_screen.focus_report:
            self.send_text.emit("\x1b[O")
        return super().focusOutEvent(event)

    def _tick_autoscroll(self) -> None:
        """One drag-auto-scroll tick: scroll a row toward the edge the
        pointer left, then extend the selection into the revealed row."""
        if not self._selection_active:
            self._autoscroll_timer.stop()
            return
        if self._autoscroll_dir > 0:
            self._scroll_up(1)
        elif self._autoscroll_dir < 0:
            self._scroll_down(1)
        pos: Optional[qt.QPointF] = self._autoscroll_pos
        if pos is not None:
            self._update_selection(pos)

    def _stop_autoscroll(self) -> None:
        self._autoscroll_timer.stop()
        self._autoscroll_dir = 0
        self._autoscroll_pos = None

    def _update_selection_with_autoscroll(self, position: qt.QPointF) -> None:
        """Extend a dragged selection, auto-scrolling when the pointer leaves
        the top or bottom edge: each tick scrolls one row and the selection
        is extended into the newly revealed row at the clamped edge."""
        y: float = position.y()
        if y < 0.0:
            self._autoscroll_dir = 1
            self._autoscroll_pos = qt.QPointF(position.x(), 0.0)
        elif y > float(self.height()):
            self._autoscroll_dir = -1
            self._autoscroll_pos = qt.QPointF(
                position.x(), max(0.0, float(self.height()) - 1.0)
            )
        else:
            self._autoscroll_dir = 0
            self._autoscroll_pos = position
        if self._autoscroll_dir != 0:
            if not self._autoscroll_timer.isActive():
                # Prime the first tick immediately so an edge crossing feels
                # responsive, then let the timer sustain the scroll.
                self._autoscroll_timer.start()
            self._tick_autoscroll()
        else:
            self._autoscroll_timer.stop()
            self._update_selection(position)

    def mouseMoveEvent(self, event: qt.QMouseEvent) -> None:  # type: ignore[override]
        # Hover feedback: a pointing hand over a hyperlink, an I-beam over
        # selected cells, the default arrow everywhere else. Both the
        # selection I-beam and the link hand are computed for the hover cell
        # so a link inside a selected region still reads as selected.
        hover_col: int = int(event.position().x() / self._char_width)
        hover_row: int = int(event.position().y() / self._char_height)
        if self._link_at_stack(
            self._stack_row(hover_row), hover_col
        ) is not None and not self._is_selected(hover_row, hover_col):
            self.setCursor(qt.Qt.CursorShape.PointingHandCursor)
        else:
            self.setCursor(
                qt.Qt.CursorShape.IBeamCursor
                if self._is_selected(hover_row, hover_col)
                else qt.Qt.CursorShape.ArrowCursor
            )
        screen: ExtendedScreen = self.terminal.term_screen
        if self._shift_selecting:
            self._update_selection_with_autoscroll(event.position())
            return super().mouseMoveEvent(event)
        if screen.mouse_mode != 0 and event.buttons() & qt.Qt.MouseButton.LeftButton:
            # A left-held drag inside a mouse-capturing TUI keeps the native
            # selection overlay (the highlight that survives for the
            # right-click copy) and, when the app asked for drag/move
            # tracking (1002/1003), forwards the motion as SGR drags
            # (motion bit 32, the xterm/WezTerm convention). openTUI only
            # builds its selection from those "drag" events, so this is what
            # lets opencode draw its own "Copied to clipboard" toast on
            # release. Button-only (1000) apps get no motion, exactly like a
            # standard terminal
            self._update_selection_with_autoscroll(event.position())
            if screen.mouse_mode >= 2:
                drag_col: int
                drag_row: int
                drag_col, drag_row = self._mouse_cell(event.position())
                if (drag_col, drag_row) != self._last_motion_cell:
                    self._last_motion_cell = (drag_col, drag_row)
                    self._mouse_report(0, drag_col, drag_row, drag=True)
            return super().mouseMoveEvent(event)
        if screen.mouse_mode == 3:
            x: int
            y: int
            x, y = self._mouse_cell(event.position())
            # Throttle: only report when the mouse crosses a cell boundary so
            # per-pixel moves do not flood the application with reports.
            if (x, y) == self._last_motion_cell:
                return super().mouseMoveEvent(event)
            self._last_motion_cell = (x, y)
            buttons: qt.Qt.MouseButton = event.buttons()
            if buttons & qt.Qt.MouseButton.MiddleButton:
                self._mouse_report(1, x, y, drag=True)
            elif buttons & qt.Qt.MouseButton.RightButton:
                self._mouse_report(2, x, y, drag=True)
            else:
                # Motion without buttons: X10 code 35 or SGR code 35.
                self._mouse_report(0, x, y, motion=True)
            return super().mouseMoveEvent(event)
        if event.buttons() & qt.Qt.MouseButton.LeftButton:
            self._update_selection_with_autoscroll(event.position())
        return super().mouseMoveEvent(event)

    def leaveEvent(self, event: Optional[qt.QEvent]) -> None:  # type: ignore[override]
        # Reset the hover cursor state when the pointer leaves the viewport;
        # otherwise the I-beam from _selection-aware mouseMoveEvent lingers.
        self.setCursor(qt.Qt.CursorShape.ArrowCursor)
        return super().leaveEvent(event)

    def mouseReleaseEvent(self, event: qt.QMouseEvent) -> None:  # type: ignore[override]
        self._stop_autoscroll()
        if self._shift_selecting:
            self._shift_selecting = False
            if event.button() == qt.Qt.MouseButton.LeftButton:
                self._end_selection()
            event.accept()
            return
        if self.terminal.term_screen.mouse_mode != 0:
            if event.button() == qt.Qt.MouseButton.RightButton:
                # Complete the forwarded right-click: the app performs its own
                # copy on this mouse-up and draws its toast (opencode). A
                # synthetic drag earlier left the left button "held" in the
                # app's parser (its selection already copied on the right
                # release), so release it with a trailing left-up; the native
                # overlay is cleared too, matching the copy-and-clear
                # convention. The flags are consumed by contextMenuEvent.
                rx: int
                ry: int
                rx, ry = self._mouse_cell(event.position())
                self._mouse_report(2, rx, ry, pressed=False)
                if self._tui_right_synth:
                    self._mouse_report(0, rx, ry, pressed=False)
                    self._clear_selection()
                event.accept()
                return
            # Close the native selection overlay (a bare click collapses to
            # nothing, a real drag keeps its highlight) and forward the
            # release so the app completes the gesture it pressed: without
            # this mouse-up, opencode never runs its copy handler and never
            # draws the "Copied to clipboard" toast.
            self._end_selection()
            button: int = self._mouse_button_code(event.button())
            x: int
            y: int
            x, y = self._mouse_cell(event.position())
            self._mouse_report(button, x, y, pressed=False)
            event.accept()
            return
        if event.button() == qt.Qt.MouseButton.LeftButton:
            self._end_selection()
            self._maybe_activate_hyperlink(event.position())
        event.accept()

    def _wheel_steps(self, delta: int) -> int:
        """
        Accumulate a wheel angle delta and return the number of full
        120-degree steps it produced (negative for the reverse direction).

        High-resolution devices (touchpads) deliver many small angleDelta
        values; summing them yields one step per accumulated 120 eighth-degrees
        and the remainder stays for the next event. Shared by the scrollback
        path and the wheel-report path, so both scroll and report one line per
        genuine step.
        """
        if delta == 0:
            return 0
        self._wheel_accumulator += delta
        steps: int = int(abs(self._wheel_accumulator) // 120)
        if steps == 0:
            return 0
        direction: int = 1 if self._wheel_accumulator > 0 else -1
        self._wheel_accumulator -= steps * 120 * direction
        return steps * direction

    def _wheel_scroll(self, delta: int) -> None:
        """
        Accumulate wheel deltas and scroll one page-row per full step.

        High-resolution devices (touchpads) deliver many small angleDelta
        values; the previous 'int(delta / 120)' truncated them to zero, so
        touchpad scrolling stayed dead until a full-size delta arrived.
        """
        steps: int = self._wheel_steps(delta)
        if steps > 0:
            self._scroll_up(steps)
        elif steps < 0:
            self._scroll_down(-steps)

    def wheelEvent(self, event: qt.QWheelEvent) -> None:  # type: ignore[override]
        delta_y: int = event.angleDelta().y()
        delta_x: int = event.angleDelta().x()
        if self.terminal.term_screen.mouse_mode != 0:
            if event.modifiers() & qt.Qt.KeyboardModifier.ShiftModifier:
                # Shift bypass: scroll the history instead of reporting the
                # wheel to the app.
                self._wheel_scroll(delta_y)
                event.accept()
                return
            x: int
            y: int
            x, y = self._mouse_cell(event.position())
            # One report per accumulated 120-degree step, so fractional
            # touchpad deltas are forwarded at the same rate the scrollback
            # path scrolls them.
            steps: int = self._wheel_steps(delta_y)
            if steps != 0:
                self._mouse_report(
                    1 if steps > 0 else 0, x, y, pressed=True, wheel=True
                )
            if delta_x != 0:
                self._mouse_report(
                    1 if delta_x > 0 else 0,
                    x,
                    y,
                    pressed=True,
                    wheel=True,
                    horizontal=True,
                )
            event.accept()
            return
        self._wheel_scroll(delta_y)
        event.accept()

    def _drop_path_quoted(self, path: str) -> str:
        """Shell-escaped form of a dropped path: single path kept bare,
        any whitespace wrapped in double quotes so the shell does not split
        it into two arguments."""
        if " " in path or "\t" in path:
            return '"' + path + '"'
        return path

    def dragEnterEvent(self, event: qt.QDragEnterEvent) -> None:  # type: ignore[override]
        mime: Optional[qt.QMimeData] = event.mimeData()
        if mime is not None and (mime.hasUrls() or mime.hasText()):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: qt.QDropEvent) -> None:  # type: ignore[override]
        mime: Optional[qt.QMimeData] = event.mimeData()
        if mime is None:
            event.ignore()
            return
        if mime.hasUrls():
            pieces: List[str] = [
                self._drop_path_quoted(url.toLocalFile().replace("/", os.sep))
                for url in mime.urls()
                if url.toLocalFile()
            ]
            text: str = " ".join(pieces)
        else:
            text = mime.text()
        if text:
            # Reuse the paste channel: UTF-8-sanitized in the terminal slot
            # and wrapped in bracketed-paste markers when the app asked for
            # them, exactly like a middle-click or menu paste.
            self.paste_event.emit(text)
        event.acceptProposedAction()

    def contextMenuEvent(self, event: qt.QContextMenuEvent) -> None:  # type: ignore[override]
        screen: ExtendedScreen = self.terminal.term_screen
        if screen.mouse_mode != 0 and not (
            event.modifiers() & qt.Qt.KeyboardModifier.ShiftModifier
        ):
            # A mouse-capturing TUI owns the right button: the press and
            # release were already forwarded (mousePressEvent/mouseReleaseEvent)
            # so the app performs its own copy and draws its own toast
            # (opencode's "Copied to clipboard"). Ex.Co. raises no menu, copies
            # nothing and pastes nothing here; that keeps the app from also
            # opening a menu or pasting on top of the forwarded gesture. The
            # gesture is over, so consume the flags. Shift+right-click still
            # raises the native menu below.
            self._tui_right_forwarded = False
            self._tui_right_synth = False
            event.accept()
            return
        context_menu: Any = gui.menu.Menu(parent=self)
        uri: Optional[str] = self._hyperlink_at(qt.QPointF(event.pos()))
        if uri is not None:
            open_action: qt.QAction = qt.QAction("Open Link", self)
            open_action.setToolTip("Open the hyperlink in the browser")
            open_action.triggered.connect(functools.partial(functions.open_url, uri))
            context_menu.addAction(open_action)
            context_menu.addSeparator()
        copy_action: qt.QAction = qt.QAction("Copy", self)
        copy_action.setToolTip("Copy the selection to the clipboard")
        copy_action.setIcon(functions.create_icon("tango_icons/edit-copy.png"))
        copy_action.triggered.connect(self.copy_selection)
        copy_action.setEnabled(self._selection is not None)
        paste_action: qt.QAction = qt.QAction("Paste", self)
        paste_action.setToolTip("Paste the clipboard into the terminal")
        paste_action.setIcon(functions.create_icon("tango_icons/edit-paste.png"))
        paste_action.triggered.connect(self.paste)
        context_menu.addAction(copy_action)
        context_menu.addAction(paste_action)
        context_menu.popup(qt.QCursor.pos())
        event.accept()

    # ------------------------------------------------------------------
    # Keyboard
    # ------------------------------------------------------------------

    _MODIFIER_PARAM: Dict[int, int] = {
        0: 1,
        cast(int, qt.Qt.KeyboardModifier.ShiftModifier.value): 2,
        cast(int, qt.Qt.KeyboardModifier.AltModifier.value): 3,
        cast(
            int,
            (
                qt.Qt.KeyboardModifier.ShiftModifier
                | qt.Qt.KeyboardModifier.AltModifier
            ).value,
        ): 4,
        cast(int, qt.Qt.KeyboardModifier.ControlModifier.value): 5,
        cast(
            int,
            (
                qt.Qt.KeyboardModifier.ShiftModifier
                | qt.Qt.KeyboardModifier.ControlModifier
            ).value,
        ): 6,
        cast(
            int,
            (
                qt.Qt.KeyboardModifier.AltModifier
                | qt.Qt.KeyboardModifier.ControlModifier
            ).value,
        ): 7,
        cast(
            int,
            (
                qt.Qt.KeyboardModifier.ShiftModifier
                | qt.Qt.KeyboardModifier.AltModifier
                | qt.Qt.KeyboardModifier.ControlModifier
            ).value,
        ): 8,
    }

    _FUNCTION_KEYS: Dict[int, str] = {
        qt.Qt.Key.Key_F1: "\x1bOP",
        qt.Qt.Key.Key_F2: "\x1bOQ",
        qt.Qt.Key.Key_F3: "\x1bOR",
        qt.Qt.Key.Key_F4: "\x1bOS",
        qt.Qt.Key.Key_F5: "\x1b[15~",
        qt.Qt.Key.Key_F6: "\x1b[17~",
        qt.Qt.Key.Key_F7: "\x1b[18~",
        qt.Qt.Key.Key_F8: "\x1b[19~",
        qt.Qt.Key.Key_F9: "\x1b[20~",
        qt.Qt.Key.Key_F10: "\x1b[21~",
        qt.Qt.Key.Key_F11: "\x1b[23~",
        qt.Qt.Key.Key_F12: "\x1b[24~",
    }

    def _modifier_param(self, modifiers: qt.Qt.KeyboardModifier) -> int:
        return self._MODIFIER_PARAM.get(cast(int, modifiers.value), 1)

    def _csi_sequence(self, letter: str, mod_param: int) -> str:
        if mod_param > 1:
            return "\x1b[1;{}{}".format(mod_param, letter)
        return "\x1b[{}".format(letter)

    def _tilde_sequence(self, code: str, mod_param: int) -> str:
        if mod_param > 1:
            return "\x1b[{};{}~".format(code, mod_param)
        return "\x1b[{}~".format(code)

    def keyPressEvent(self, event: qt.QKeyEvent) -> None:  # type: ignore[override]
        modifiers: qt.Qt.KeyboardModifier = event.modifiers()
        key: int = event.key()
        text: str = event.text()
        mod_param: int = self._modifier_param(modifiers)
        shift: qt.Qt.KeyboardModifier = modifiers & qt.Qt.KeyboardModifier.ShiftModifier
        ctrl: qt.Qt.KeyboardModifier = (
            modifiers & qt.Qt.KeyboardModifier.ControlModifier
        )
        alt: qt.Qt.KeyboardModifier = modifiers & qt.Qt.KeyboardModifier.AltModifier
        meta: qt.Qt.KeyboardModifier = modifiers & qt.Qt.KeyboardModifier.MetaModifier

        # Copy / paste
        if modifiers == (
            qt.Qt.KeyboardModifier.ControlModifier
            | qt.Qt.KeyboardModifier.ShiftModifier
        ):
            if key == qt.Qt.Key.Key_C:
                self.copy_selection()
                event.accept()
                return
            if key == qt.Qt.Key.Key_V:
                self.paste()
                event.accept()
                return

        # Scrollback navigation (only in the primary screen)
        if not self._in_alt():
            if ctrl and not alt and not shift and key == qt.Qt.Key.Key_Up:
                self._scroll_up(1)
                event.accept()
                return
            if ctrl and not alt and not shift and key == qt.Qt.Key.Key_Down:
                self._scroll_down(1)
                event.accept()
                return
            if not ctrl and not alt and key == qt.Qt.Key.Key_PageUp:
                self._scroll_up(self._page_rows())
                event.accept()
                return
            if not ctrl and not alt and key == qt.Qt.Key.Key_PageDown:
                self._scroll_down(self._page_rows())
                event.accept()
                return

        # Cursor keys and editing keys
        output: Optional[str] = None
        if key == qt.Qt.Key.Key_Up:
            output = self._csi_sequence("A", mod_param)
        elif key == qt.Qt.Key.Key_Down:
            output = self._csi_sequence("B", mod_param)
        elif key == qt.Qt.Key.Key_Left:
            output = self._csi_sequence("D", mod_param)
        elif key == qt.Qt.Key.Key_Right:
            output = self._csi_sequence("C", mod_param)
        elif key == qt.Qt.Key.Key_Home:
            output = self._csi_sequence("H", mod_param)
        elif key == qt.Qt.Key.Key_End:
            output = self._csi_sequence("F", mod_param)
        elif key == qt.Qt.Key.Key_PageUp:
            output = self._tilde_sequence("5", mod_param)
        elif key == qt.Qt.Key.Key_PageDown:
            output = self._tilde_sequence("6", mod_param)
        elif key == qt.Qt.Key.Key_Insert:
            output = self._tilde_sequence("2", mod_param)
        elif key == qt.Qt.Key.Key_Delete:
            output = self._tilde_sequence("3", mod_param)
        elif key in self._FUNCTION_KEYS:
            base: str = self._FUNCTION_KEYS[key]
            if mod_param > 1 and key <= qt.Qt.Key.Key_F4:
                # F1-F4 with modifiers: CSI 1 ; <mod> P/Q/R/S
                letters: Dict[int, str] = {
                    qt.Qt.Key.Key_F1: "P",
                    qt.Qt.Key.Key_F2: "Q",
                    qt.Qt.Key.Key_F3: "R",
                    qt.Qt.Key.Key_F4: "S",
                }
                output = "\x1b[1;{};{}".format(mod_param, letters[key])
            elif mod_param > 1:
                output = base.replace("~", ";{}~".format(mod_param), 1)
            else:
                output = base
        elif key == qt.Qt.Key.Key_Backspace:
            output = "\x7f"
        elif key in (qt.Qt.Key.Key_Return, qt.Qt.Key.Key_Enter):
            if ctrl and not alt and not meta:
                # Ctrl+Enter: Windows Terminal sends a line feed (Ctrl+J)
                # here, and opencode binds Ctrl+J to insert a newline. The
                # Windows console host does not translate a CSI-u Ctrl+Enter
                # reliably, so follow the Windows Terminal convention.
                output = "\n"
            elif self.terminal.term_screen.keyboard_flags & 1 and (
                alt or shift or meta
            ):
                # Kitty keyboard protocol: a modified Enter arrives as
                # CSI u (key 13 + XTerm-style modifier) so applications
                # can tell it apart from a plain Enter.
                mod_param = (
                    1
                    + (1 if shift else 0)
                    + (2 if alt else 0)
                    + (4 if ctrl else 0)
                    + (8 if meta else 0)
                )
                output = "\x1b[13;{}u".format(mod_param)
            else:
                output = "\r"
        elif key in (qt.Qt.Key.Key_Tab, qt.Qt.Key.Key_Backtab):
            if shift:
                output = "\x1b[Z"
            else:
                output = "\t"
        elif key == qt.Qt.Key.Key_Escape:
            output = "\x1b"
        if output is not None:
            self.send_text.emit(output)
            event.accept()
            return

        # Control letters (e.g. Ctrl+C -> 0x03, Ctrl+Z -> 0x1a)
        if ctrl and not alt and qt.Qt.Key.Key_A <= key <= qt.Qt.Key.Key_Z:
            code: int = ord(chr(key).lower()) - ord("a") + 1
            self.send_text.emit(chr(code))
            event.accept()
            return

        # Ctrl+Alt+letter -> ESC + control code (e.g. Ctrl+Alt+C -> ESC 0x03).
        # Plain Alt would only prefix the printable text, losing the control.
        # Windows reports AltGr as Ctrl+Alt; when the layout produced a
        # character (e.g. AltGr+F = "{" on some layouts), send it as-is.
        if (
            ctrl
            and alt
            and not shift
            and qt.Qt.Key.Key_A <= key <= qt.Qt.Key.Key_Z
            and not text
        ):
            code = ord(chr(key).lower()) - ord("a") + 1
            self.send_text.emit("\x1b" + chr(code))
            event.accept()
            return

        # Ctrl+Space -> NUL
        if ctrl and not alt and key == qt.Qt.Key.Key_Space:
            self.send_text.emit("\x00")
            event.accept()
            return

        # Alt / Meta: prefix printable text with ESC. AltGr (Ctrl+Alt) is
        # excluded so layout characters (e.g. AltGr+F = "{") pass through
        # unmodified to the shell below.
        if alt and not ctrl and not meta and text:
            self.send_text.emit("\x1b" + text)
            event.accept()
            return

        if text:
            self.send_text.emit(text)
            event.accept()

    def update_style(self) -> None:
        # Re-apply the configured font and theme colors (theme switches and
        # font setting changes take effect here), then re-layout and resize.
        self._load_style()
        self._recompute_geometry()
        if self.isVisible():
            # The screen is resized on show; only re-emit once visible so a
            # style change with a real geometry takes effect.
            cols: int
            rows: int
            cols, rows = self._terminal_size()
            self.resize_event.emit(cols, rows)
        self.update()
