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

import math

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

        # Monospace font and its measured cell size
        self._style_fonts: Dict[Tuple[bool, bool, bool, bool], qt.QFont] = {}
        self._load_style()

        # Scrollback state
        self._scroll_offset: int = 0
        self._sb_visible: bool = False
        self._content_width: int = 0

        # Cursor blink
        self._blink_phase: bool = True
        self._blink_timer: qt.QTimer = qt.QTimer(self)
        self._blink_timer.setInterval(self.BLINK_INTERVAL_MS)
        self._blink_timer.timeout.connect(self._on_blink)
        self._blink_timer.start()

        # Selection state (start/end cells in stack coordinates)
        self._selection: Optional[Selection] = None
        self._selection_active: bool = False
        # Shift-bypass of mouse tracking: while Shift is held, mouse events
        # drive native selection / scrollback scroll instead of reports.
        self._shift_selecting: bool = False

        # Last painted cursor row (for clearing the previous cursor position)
        self._last_cursor_y: Optional[int] = None

        # Last reported mouse-motion cell (mode 1003 throttle)
        self._last_motion_cell: Optional[Tuple[int, int]] = None

        # Visual bell flash state
        self._flash: bool = False

        # Memo caches for cell style resolution (see _cell_style /
        # _resolve_color); cleared on style reloads.
        self._style_cache: Dict[
            Tuple[Any, ...], Tuple[qt.QColor, qt.QColor, qt.QFont]
        ] = {}
        self._color_cache: Dict[str, qt.QColor] = {}

        # Scrollbar
        self._scrollbar: qt.QScrollBar = qt.QScrollBar(qt.Qt.Orientation.Vertical, self)
        self._scrollbar.setRange(0, 0)
        self._scrollbar.valueChanged.connect(self._scroll_to_value)
        self._scrollbar.hide()

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
        """Font for the terminal: configured override or the editor font."""
        font_name: Any = settings.get("terminal-font-name")
        font_size: Any = settings.get("terminal-font-size")
        if font_name:
            font: qt.QFont = qt.QFont(font_name)
            if font_size:
                font.setPointSizeF(font_size)
            return font
        return qt.QFont(settings.get_editor_font())

    def _load_style(self) -> None:
        """(Re)apply the configured font and theme-derived default colors."""
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
        self._recompute_geometry()
        cols: int
        rows: int
        cols, rows = self._terminal_size()
        self.resize_event.emit(cols, rows)
        return super().resizeEvent(event)

    # ------------------------------------------------------------------
    # Scrollback
    # ------------------------------------------------------------------

    def _in_alt(self) -> bool:
        return self.terminal.screen.in_alt_screen

    def _history_len(self) -> int:
        return len(self.terminal.screen.history.top)

    def _stack_row(self, viewport_y: int) -> int:
        """Map a viewport row to a row index in the (history + screen) stack."""
        return (self._history_len() - self._scroll_offset) + viewport_y

    def _stack_row_cells(self, stack_row: int) -> Any:
        """Return the cell row (StaticDefaultDict) for a stack row index."""
        screen: ExtendedScreen = self.terminal.screen
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
        return max(self.terminal.screen.lines - 1, 1)

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
        screen: ExtendedScreen = self.terminal.screen
        dirty: Any = screen.dirty
        edited: Set[int] = screen.edited
        pending_scroll: int = screen.pending_scroll
        lines: int = screen.lines
        if self._in_alt():
            self._scroll_offset = 0
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
        edited.clear()
        # The scroll delta is only meaningful for the chunk just fed; consume
        # it so a second schedule_repaint in the same iteration does not
        # trigger another full repaint.
        screen.pending_scroll = 0
        self._refresh_scrollbar()

    def _on_blink(self) -> None:
        if not self.isVisible():
            return
        screen: ExtendedScreen = self.terminal.screen
        if screen.cursor.hidden:
            # Reset the phase so the cursor is immediately visible when it
            # reappears instead of staying hidden for up to one blink period.
            self._blink_phase = True
            return
        if not screen.cursor_blink:
            # Steady cursor (DECSCUSR even param): nothing to blink.
            self._blink_phase = True
            return
        self._blink_phase = not self._blink_phase
        # Only the cursor cells (previous + current row) change on a blink
        # toggle; no need to repaint the whole viewport.
        lines: int = screen.lines
        if self._last_cursor_y is not None and 0 <= self._last_cursor_y < lines:
            self.update(self._row_band(self._last_cursor_y))
        if 0 <= screen.cursor.y < lines:
            self.update(self._row_band(screen.cursor.y))
        # SGR-5 blink-attributed cells elsewhere on screen toggle with the
        # phase too; repaint the rows that carry one (the scan is cheap and
        # runs once per blink period).
        for y in range(lines):
            row: Any = screen.buffer.get(y)
            if row is not None and any(cell.blink for cell in row.values()):
                self.update(self._row_band(y))

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
        screen: ExtendedScreen = self.terminal.screen
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
        while x < columns:
            cell: Any = row[x]
            style: Tuple[qt.QColor, qt.QColor, qt.QFont] = self._cell_style(cell, y, x)
            run_text: List[str] = []
            run_start: int = x
            while x < columns:
                current: Any = row[x]
                if self._cell_style(current, y, x) != style:
                    break
                char: str = current.data
                if char == "" or (current.blink and not self._blink_phase):
                    char = " "
                run_text.append(char)
                x += 1
                if x < columns and wcwidth(current.data) == 2 and row[x].data == "":
                    # A full-width character spans two cells: absorb the
                    # trailing stub cell (pyte marks it with empty data) so
                    # the glyph lays out at its natural width.
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
                painter.drawText(
                    rect,
                    qt.Qt.AlignmentFlag.AlignLeft | qt.Qt.AlignmentFlag.AlignVCenter,
                    "".join(run_text),
                )

    def _cell_font(self, cell: Any) -> qt.QFont:
        """Styled font for a cell, drawn from a small cache keyed on the
        style flags (bold/italic/underline/strike) so painting does not
        allocate a fresh QFont for every cell."""
        key: Tuple[bool, bool, bool, bool] = (
            cell.bold,
            cell.italics,
            cell.underscore,
            cell.strikethrough,
        )
        font: Optional[qt.QFont] = self._style_fonts.get(key)
        if font is None:
            font = qt.QFont(self._base_font)
            if cell.bold:
                font.setBold(True)
            if cell.italics:
                font.setItalic(True)
            if cell.underscore:
                font.setUnderline(True)
            if cell.strikethrough:
                font.setStrikeOut(True)
            self._style_fonts[key] = font
        return font

    def _cell_style(
        self, cell: Any, y: int, x: int
    ) -> Tuple[qt.QColor, qt.QColor, qt.QFont]:
        key: Tuple[Any, ...] = (
            cell.bg,
            cell.fg,
            cell.bold,
            cell.italics,
            cell.underscore,
            cell.strikethrough,
            cell.reverse,
            self._is_selected(y, x),
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
            font: qt.QFont = self._cell_font(cell)
            if self._is_selected(y, x):
                fg, bg = bg, fg
            style = (fg, bg, font)
            self._style_cache[key] = style
        return style

    def _paint_cursor(self, painter: qt.QPainter) -> None:
        screen: ExtendedScreen = self.terminal.screen
        if self._scroll_offset != 0 or screen.cursor.hidden:
            return
        if self._selection is not None:
            return
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
        rect: qt.QRectF = qt.QRectF(
            x * self._char_width,
            y * self._char_height,
            self._char_width,
            self._char_height,
        )
        cursor_style: str = screen.cursor_style
        char: str = cell.data if cell.data != "" else " "
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
            painter.drawText(
                rect,
                qt.Qt.AlignmentFlag.AlignLeft | qt.Qt.AlignmentFlag.AlignVCenter,
                char,
            )
        elif cursor_style == "bar":
            bar: qt.QRectF = qt.QRectF(
                rect.x(),
                rect.y(),
                max(self._char_width * 0.15, 2.0),
                rect.height(),
            )
            painter.fillRect(bar, fg)
        else:
            # Block cursor: fill with foreground, draw text with background.
            painter.fillRect(rect, fg)
            painter.setPen(bg)
            painter.setFont(self._cell_font(cell))
            painter.drawText(
                rect,
                qt.Qt.AlignmentFlag.AlignLeft | qt.Qt.AlignmentFlag.AlignVCenter,
                char,
            )

    # ------------------------------------------------------------------
    # Selection
    # ------------------------------------------------------------------

    def _pos_cell(self, position: qt.QPointF) -> Tuple[int, int]:
        screen: ExtendedScreen = self.terminal.screen
        cols: int = screen.columns
        lines: int = screen.lines
        x: int = int(position.x() / self._char_width)
        y: int = int(position.y() / self._char_height)
        x = max(0, min(x, cols - 1))
        y = max(0, min(y, lines - 1))
        return self._stack_row(y), x

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
        columns: int = self.terminal.screen.columns
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

    def paste(self) -> None:
        application: Any = data.application
        text: str = application.clipboard().text()
        if text:
            if self.terminal.screen.bracketed_paste:
                text = "\x1b[200~" + text + "\x1b[201~"
            self.paste_event.emit(text)

    def _start_selection(self, position: qt.QPointF) -> None:
        self._selection = self._pos_cell(position)
        self._selection_active = True
        self.update()

    def _update_selection(self, position: qt.QPointF) -> None:
        if not self._selection_active:
            return
        start: Optional[Selection] = self._selection
        if start is None:
            return
        end: Tuple[int, int] = self._pos_cell(position)
        self._selection = (start[0], start[1], end[0], end[1])
        self.update()

    def _end_selection(self) -> None:
        self._selection_active = False
        bounds: Optional[Selection] = self._selection_bounds()
        if bounds is None:
            return
        r0, c0, r1, c1 = cast(Tuple[int, int, int, int], bounds)
        if (r0, c0) == (r1, c1):
            # Plain click without drag: no selection, so the shell cursor
            # stays/returns to the active text line.
            self._selection = None
        elif (r0, c0) > (r1, c1):
            self._selection = (r1, c1, r0, c0)
        self.update()

    # ------------------------------------------------------------------
    # Mouse
    # ------------------------------------------------------------------

    def _mouse_cell(self, position: qt.QPointF) -> Tuple[int, int]:
        x: int = int(position.x() / self._char_width)
        y: int = int(position.y() / self._char_height)
        return x, y

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
    ) -> None:
        """Emit a mouse report to the application when a mouse mode is set."""
        screen: ExtendedScreen = self.terminal.screen
        if screen.mouse_mode == 0:
            return
        cx: int = x + 1
        cy: int = y + 1
        if wheel:
            code: int = 64 if button > 0 else 65
        elif motion:
            # Motion without a button pressed (mode 1003)
            code = 35
        elif pressed:
            code = button
        else:
            # Release: button number + 3 (left=3, middle=4, right=5)
            code = button + 3
        if screen.sgr_mouse:
            # SGR (1006): CSI < b ; x ; y M/m
            self.send_text.emit(
                "\x1b[<{};{};{}{}".format(code, cx, cy, "M" if pressed else "m")
            )
        else:
            # X10-style: CSI M b+32 x+32 y+32
            self.send_text.emit("\x1b[M" + chr(code + 32) + chr(cx + 32) + chr(cy + 32))

    def mousePressEvent(self, event: qt.QMouseEvent) -> None:  # type: ignore[override]
        self.setFocus()
        self.focused.emit()
        if self.terminal.screen.mouse_mode != 0:
            if event.modifiers() & qt.Qt.KeyboardModifier.ShiftModifier:
                # Shift bypass: the app never sees the event, so native
                # selection works inside mouse-capturing TUIs (OpenCode, ...).
                self._shift_selecting = True
                self._last_motion_cell = None
                if event.button() == qt.Qt.MouseButton.LeftButton:
                    self._start_selection(event.position())
                event.accept()
                return
            self._shift_selecting = False
            self._last_motion_cell = None
            button: int = self._mouse_button_code(event.button())
            x: int
            y: int
            x, y = self._mouse_cell(event.position())
            self._mouse_report(button, x, y, pressed=True)
            event.accept()
            return
        if event.button() == qt.Qt.MouseButton.LeftButton:
            self._start_selection(event.position())
        # A right-click keeps the selection so the context menu's Copy
        # action stays enabled; the next left-press starts a new selection.
        # Accept the press so the ignored default QWidget handling does not
        # propagate it up to the tab widget (which would steal focus)
        event.accept()

    def focusInEvent(self, event: qt.QFocusEvent) -> None:  # type: ignore[override]
        self.focused.emit()
        return super().focusInEvent(event)

    def mouseMoveEvent(self, event: qt.QMouseEvent) -> None:  # type: ignore[override]
        screen: ExtendedScreen = self.terminal.screen
        if self._shift_selecting:
            self._update_selection(event.position())
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
            if buttons & qt.Qt.MouseButton.LeftButton:
                self._mouse_report(0, x, y, pressed=True)
            elif buttons & qt.Qt.MouseButton.MiddleButton:
                self._mouse_report(1, x, y, pressed=True)
            elif buttons & qt.Qt.MouseButton.RightButton:
                self._mouse_report(2, x, y, pressed=True)
            else:
                # Motion without buttons: X10 code 35 or SGR code 35.
                self._mouse_report(0, x, y, motion=True)
            return super().mouseMoveEvent(event)
        if screen.mouse_mode == 2 and event.buttons() & qt.Qt.MouseButton.LeftButton:
            x, y = self._mouse_cell(event.position())
            self._mouse_report(0, x, y, pressed=True)
            return super().mouseMoveEvent(event)
        if event.buttons() & qt.Qt.MouseButton.LeftButton:
            self._update_selection(event.position())
        return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: qt.QMouseEvent) -> None:  # type: ignore[override]
        if self._shift_selecting:
            self._shift_selecting = False
            if event.button() == qt.Qt.MouseButton.LeftButton:
                self._end_selection()
            event.accept()
            return
        if self.terminal.screen.mouse_mode != 0:
            button: int = self._mouse_button_code(event.button())
            x: int
            y: int
            x, y = self._mouse_cell(event.position())
            self._mouse_report(button, x, y, pressed=False)
            event.accept()
            return
        if event.button() == qt.Qt.MouseButton.LeftButton:
            self._end_selection()
        event.accept()

    def wheelEvent(self, event: qt.QWheelEvent) -> None:  # type: ignore[override]
        delta: int = event.angleDelta().y()
        if self.terminal.screen.mouse_mode != 0:
            if event.modifiers() & qt.Qt.KeyboardModifier.ShiftModifier:
                # Shift bypass: scroll the history instead of reporting the
                # wheel to the app.
                if delta > 0:
                    self._scroll_up(int(delta / 120))
                else:
                    self._scroll_down(int(abs(delta) / 120))
                event.accept()
                return
            x: int
            y: int
            x, y = self._mouse_cell(event.position())
            self._mouse_report(1 if delta > 0 else 0, x, y, pressed=True, wheel=True)
            event.accept()
            return
        if delta > 0:
            self._scroll_up(int(delta / 120))
        else:
            self._scroll_down(int(abs(delta) / 120))
        event.accept()

    def contextMenuEvent(self, event: qt.QContextMenuEvent) -> None:  # type: ignore[override]
        if self.terminal.screen.mouse_mode != 0:
            event.ignore()
            return
        context_menu: Any = gui.menu.Menu(parent=self)
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
            elif self.terminal.screen.keyboard_flags & 1 and (alt or shift or meta):
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
