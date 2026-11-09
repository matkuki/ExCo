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

import bisect
import functools
import math
import os

import data
import functions
import gui.menu
import qt
import settings
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Iterable,
    List,
    NamedTuple,
    Optional,
    Set,
    Tuple,
    Union,
    cast,
)

from gui.terminal.findbar import TerminalFindBar
from gui.terminal.graphemes import cluster_width
from gui.terminal.screen import ExtendedScreen, PromptMark

if TYPE_CHECKING:
    from gui.terminal.terminal import Terminal

# A selection is either a bare anchor (start cell) or a (start, end) pair;
# all cells are (stack_row, column) tuples.
Selection = Union[Tuple[int, int], Tuple[int, int, int, int]]


class RowContext(NamedTuple):
    """Per-row paint state hoisted out of the per-cell loop.

    _cell_style needs the row's stack index, its OSC 8 link columns, the
    selection bounds and the find highlights. Deriving them per cell made a
    full repaint call _history_len/_stack_row/_refresh_link_index and
    _is_selected twice for every cell, which was about a third of the paint
    time; the values only change per row, so they are computed once in
    _row_context.
    """

    stack_row: int
    links: Optional[Dict[int, str]]
    selection: Optional[Tuple[int, int, int, int]]
    find: Optional[List[Tuple[int, int]]]
    find_current: Optional[Tuple[int, int]]


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
    # pyte's own BG_AIXTERM table spells SGR 105 "bfightmagenta" (graphics.py),
    # so that is the string a cell carries. Without this alias it fell through
    # to the hex parser, QColor left it invalid, and fillRect painted the cell
    # black - a bright-magenta background became the darkest one.
    "bfightmagenta": qt.QColor("#ff55ff"),
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

    # Cursor blink period in milliseconds (the default for the
    # terminal-cursor-blink-ms setting, and the fallback when it is unset)
    BLINK_INTERVAL_MS: int = 530
    # A setting below this would blink too fast to read (and would keep the
    # repaint timer permanently busy), so the configured rate is clamped.
    MIN_BLINK_INTERVAL_MS: int = 100
    # How many whitespace-separated chunks a double-click may bridge over
    # while looking for a path separator or a path prefix. Bounded so a stray
    # prose line cannot turn into a whole-line selection.
    PATH_BRIDGE_CHUNKS: int = 4

    # Bundled monospace families Qt should try, in order, for a glyph the
    # configured family lacks. Without this list Qt merges in whichever system
    # font happens to cover the character: '✕' (U+2715, opencode's tab close
    # button) came from MS UI Gothic at a 13px advance in an 8px cell, and
    # every following glyph in the run was pushed out of the grid.
    FALLBACK_FAMILIES: Tuple[str, ...] = ("Source Code Pro", "Inconsolata")

    # Ranges whose glyph *size* is part of what the character means, so the
    # font's own ink box must be kept: block elements encode fill height
    # (U+2581-U+2588 lower blocks), braille patterns are a fixed dot grid, and
    # shape glyphs come in named sizes. opencode's working indicator is a
    # size-coded trail (U+25A0 'black square' active vs U+2B1D 'very small
    # square' inactive; or U+2B25/U+25C6/U+2B29/U+2B2A diamonds), and growing
    # the fallback 2px square to the cap height made every inactive cell as big
    # as the active one. U+2715 'multiplication x' is deliberately outside: it
    # is a symbol, not a size.
    SIZE_SEMANTIC_RANGES: Tuple[Tuple[int, int], ...] = (
        (0x2500, 0x257F),  # box drawing
        (0x2580, 0x259F),  # block elements
        (0x25A0, 0x25FF),  # geometric shapes
        (0x2800, 0x28FF),  # braille patterns
        (0x2B00, 0x2BFF),  # miscellaneous symbols and arrows
    )

    # Bounds for the per-cell memo caches (see _cell_style / _resolve_color /
    # _glyph_shape). A truecolour animation - opencode's "Free token limit
    # reached" shimmer, a gradient spinner - puts a brand-new fg/bg string in
    # every animated cell on every frame, so an unbounded memo gained one entry
    # per cell per frame: measured 7,200 style + 7,200 colour entries and
    # +3.6 MB of RSS for each 160x45 frame, i.e. a terminal that grew by ~100 MB
    # a minute and slowed down until it was unusable. A cap far above any static
    # palette (a theme uses tens of colours) only ever trips under exactly that
    # animation, and a bulk clear costs one repaint, never correctness.
    STYLE_CACHE_LIMIT: int = 4096
    COLOR_CACHE_LIMIT: int = 4096
    GLYPH_SHAPE_LIMIT: int = 4096

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

        # Theme colours before any OSC 10/11 override; _load_style resolves the
        # effective defaults from both and reports the palette to the screen so
        # its OSC queries answer with the colours actually painted.
        self._theme_fg: qt.QColor = qt.QColor("#000000")
        self._theme_bg: qt.QColor = qt.QColor("#ffffff")
        # Session-only font zoom driven by the context menu (the persisted
        # size stays in settings; the menu adjusts this terminal for now).
        self._font_zoom: float = 0.0
        # Screen palette generation already reflected in the caches below.
        self._palette_version: int = 0

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
        self._blink_timer.setInterval(self._cursor_blink_interval())
        self._blink_timer.timeout.connect(self._on_blink)
        self._blink_timer.start()

        # Selection state (start/end cells in stack coordinates)
        self._selection: Optional[Selection] = None
        self._selection_active: bool = False
        # Rectangular (column) selection, started with Alt+left-drag. The
        # stored cells are still a normal anchor/end pair; this flag only
        # changes how they resolve into selected cells and copied text.
        self._block_selection: bool = False
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

        # Inline-image QImage cache, keyed by Placement.serial (not id(): a
        # freed placement's address is reused). A placement's pixels never
        # change, so the cache only has to be pruned when the screen's image
        # store version moves on (add / delete / clear).
        self._image_cache: Dict[int, qt.QImage] = {}
        self._image_version: int = -1

        # History generation already accounted for while anchoring a scrolled
        # view (see _anchor_scrollback). The delta is the number of rows the
        # bounded deque dropped since the last repaint; the last length seen
        # tells an overflow (length unchanged) from a cleared scrollback.
        self._hist_gen: int = self._history_generation()
        self._hist_seen: int = self._history_len()

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

        # Scrollback search state (see the Find section). Matches are kept in
        # stack coordinates, so a hit in the scrollback is addressed exactly
        # like a hit on the live screen; _find_spans is the per-row column
        # range the paint pass highlights.
        self._find_query: str = ""
        self._find_matches: List[Tuple[int, int]] = []
        self._find_spans: Dict[int, List[Tuple[int, int]]] = {}
        self._find_index: int = -1
        self._find_current_row: int = -1
        self._find_current_span: Optional[Tuple[int, int]] = None
        # history_generation the matches were scanned against (a deque
        # overflow moves every stack row, exactly like a selection).
        self._find_gen: int = self._history_generation()
        self._find_bg: qt.QColor = qt.QColor("#ffe082")
        self._find_current_bg: qt.QColor = qt.QColor("#ffb300")
        self._find_fg: qt.QColor = qt.QColor("#000000")
        self._find_bar: TerminalFindBar = TerminalFindBar(self)
        self._find_bar.query_changed.connect(self._on_find_query)
        self._find_bar.next_requested.connect(self.find_next)
        self._find_bar.previous_requested.connect(self.find_previous)
        self._find_bar.closed.connect(self.close_find)
        self._find_bar.hide()
        self._style_find_bar()

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
        # Session-only zoom from the context menu, applied on top of whatever
        # size the settings produced (a positive point size means the font is
        # not pixel-sized, where adding points would be meaningless).
        if self._font_zoom and font.pointSizeF() > 0:
            font.setPointSizeF(max(font.pointSizeF() + self._font_zoom, 4.0))
        # Qt's own fallback picks arbitrary system fonts for glyphs the family
        # lacks, and those are neither cell-sized nor cell-advanced. Name the
        # bundled monospace families explicitly: Qt tries them before it
        # merges in a system font, so symbols like '✕' stay on the grid while
        # characters no bundled font covers (CJK, emoji) keep working.
        families: List[str] = [font.family()]
        available: List[str] = qt.QFontDatabase.families()
        for fallback in self.FALLBACK_FAMILIES:
            if fallback != font.family() and fallback in available:
                families.append(fallback)
        font.setFamilies(families)
        return font

    def _cursor_blink_interval(self) -> int:
        """Configured cursor blink half-period, clamped to a readable rate.

        The setting is read once, when the view is built, exactly like the
        terminal font: a terminal opened afterwards picks up a changed value.
        """
        value: Any = settings.get("terminal-cursor-blink-ms")
        if value is None:
            return self.BLINK_INTERVAL_MS
        try:
            interval: int = int(value)
        except (TypeError, ValueError):
            return self.BLINK_INTERVAL_MS
        return max(interval, self.MIN_BLINK_INTERVAL_MS)

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
        self._theme_fg = qt.QColor(theme["fonts"]["default"]["color"])
        self._theme_bg = qt.QColor(theme["fonts"]["default"]["background"])
        self._apply_screen_defaults()
        self._measure_font()
        self._style_copy_toast()
        self._style_find_bar()
        self._palette_version = self.terminal.term_screen.palette_version

    def _apply_screen_defaults(self) -> None:
        """Resolve the effective default foreground/background.

        The theme supplies them unless an application replaced them with
        OSC 10/11. The view also reports the palette it paints with, so the
        screen can answer an OSC 4/10/11 query with the colour actually on
        screen instead of a second, possibly different, palette.
        """
        screen: ExtendedScreen = self.terminal.term_screen
        fg_spec: str = screen.default_fg_override or self._theme_fg.name()
        bg_spec: str = screen.default_bg_override or self._theme_bg.name()
        self._default_fg = qt.QColor(fg_spec)
        self._default_bg = qt.QColor(bg_spec)
        table: Dict[str, str] = {
            token: colour.name()
            for token, colour in FOREGROUND_COLOR_MAP.items()
            if colour is not None
        }
        screen.set_render_colours(table, self._theme_fg.name(), self._theme_bg.name())

    def _measure_font(self) -> None:
        font_metrics: qt.QFontMetricsF = qt.QFontMetricsF(self._font)
        self._char_width: float = max(font_metrics.horizontalAdvance("M"), 1.0)
        self._char_height: float = max(
            font_metrics.lineSpacing(), font_metrics.height(), 1.0
        )
        # Baseline offset inside one row: what AlignVCenter would use for a
        # rect of this height. Every glyph is drawn from this baseline at its
        # own cell's x, so a run is never laid out as one string (which let a
        # fallback glyph's advance shift the rest of the run) and never
        # clipped by a per-cell rect.
        self._baseline: float = (
            self._char_height - font_metrics.height()
        ) / 2.0 + font_metrics.ascent()
        # Cap height is the reference size a fallback symbol is grown to: a
        # family that lacks a glyph often draws the replacement symbol much
        # smaller than its own letters (Inconsolata's U+2715 is a 5px cross in
        # a 17px row), so a narrow fallback glyph whose ink is shorter than
        # this is scaled up to it (see _draw_glyph).
        self._cap_height: float = max(font_metrics.capHeight(), 0.0)
        # Glyph coverage/shape caches, keyed on the style font's id; the style
        # fonts are rebuilt whenever the style is (see _load_style), so the ids
        # cannot outlive the fonts they describe.
        self._raw_fonts: Dict[int, Optional[qt.QRawFont]] = {}
        self._glyph_coverage: Dict[Tuple[int, str], bool] = {}
        self._glyph_shapes: Dict[
            Tuple[int, str], Tuple[float, Tuple[float, float, float, float]]
        ] = {}
        # The screen converts inline-image pixel sizes to cell spans, so it
        # needs the same cell metrics the painter uses.
        self.terminal.term_screen.set_cell_metrics(self._char_width, self._char_height)

    def _terminal_size(self) -> Tuple[int, int]:
        cols: int = max(int(self._content_width / self._char_width), 1)
        rows: int = max(int(self.height() / self._char_height), 1)
        return cols, rows

    def _row_band(self, y: int) -> qt.QRect:
        """Integer rectangle that fully covers the row's pixel band. The
        char height is often fractional (e.g. 13.3px), so naive rounding of
        the row rect would leave 1px gaps between adjacent rows that never
        get repainted; floor/ceil guarantees gapless coverage."""
        return self._row_band_span(y, y)

    def _row_band_span(self, first: int, last: int) -> qt.QRect:
        """Integer rectangle covering rows *first*..*last* inclusively, with
        the same floor/ceil guarantee as :meth:`_row_band`."""
        top: int = math.floor(first * self._char_height)
        bottom: int = math.ceil((last + 1) * self._char_height)
        return qt.QRect(0, top, self._content_width, bottom - top)

    def _repaint_rows(self, rows: Iterable[int], lines: int) -> None:
        """Invalidate the given rows, coalescing each run of adjacent rows
        into one rectangle. A frame that dirties a whole viewport otherwise
        issues one ``QWidget.update(QRect)`` per line, and Qt has to merge
        those regions itself; a contiguous run is a single band."""
        valid: List[int] = sorted({y for y in rows if 0 <= y < lines})
        if not valid:
            return
        first: int = valid[0]
        previous: int = first
        for y in valid[1:]:
            if y == previous + 1:
                previous = y
                continue
            self.update(self._row_band_span(first, previous))
            first = previous = y
        self.update(self._row_band_span(first, previous))

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
        # Keep the scrollbar's strip out of the grid even while it is hidden.
        # Shrinking the content only when it appears changed the column count
        # without emitting a resize (the screen/PTY kept the wider grid), so
        # the rightmost columns sat underneath the bar as soon as the user
        # scrolled up - the last characters of every line disappeared.
        self._content_width = max(self.width() - scrollbar_width, 1)
        self._place_find_bar()

    def resizeEvent(self, event: qt.QResizeEvent) -> None:  # type: ignore[override]
        self._clear_selection()
        self._recompute_geometry()
        cols: int
        rows: int
        cols, rows = self._terminal_size()
        # Capture the stack row the reader is looking at *before* the screen
        # re-wraps its rows; the reflow map then moves it to wherever that text
        # ended up. Only meaningful while scrolled back - at the bottom the
        # cursor's row is the anchor and the screen keeps it visible itself.
        anchor: Optional[int] = None
        if self._scroll_offset > 0:
            anchor = self._stack_row(0)
        self.resize_event.emit(cols, rows)
        self._anchor_after_reflow(anchor)
        self._place_copy_toast()
        if getattr(self, "_find_query", ""):
            # The column count changed, so every recorded match column is
            # stale; rescan rather than highlight the wrong cells.
            self._rescan_find()
        return super().resizeEvent(event)

    def _anchor_after_reflow(self, anchor: Optional[int]) -> None:
        """Put the reader back on the text reflow moved.

        A resize re-wraps the whole stack, so a row index computed before it
        names different content afterwards. The screen reports the old -> new
        position map; *anchor* is the stack row that was at the top of the
        viewport. When its text fell out of the retained stack (the re-wrapped
        history is longer than the bound) the reader goes back to the live
        screen instead of dangling past the end.
        """
        screen: ExtendedScreen = self.terminal.term_screen
        result: Optional[Any] = screen.reflow_map
        screen.reflow_map = None
        if result is not None and anchor is not None:
            new_row: Optional[int] = result.map_row(anchor)
            history_len: int = self._history_len()
            if new_row is None:
                self._scroll_offset = 0
            else:
                self._scroll_offset = max(0, min(history_len - new_row, history_len))
        self._refresh_scrollbar()

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

    def _row_context(self, viewport_y: int) -> RowContext:
        """Row-level state shared by every cell of viewport row *viewport_y*."""
        stack_row: int = self._stack_row(viewport_y)
        links: Optional[Dict[int, str]] = None
        if stack_row >= 0:
            self._refresh_link_index()
            links = self._link_index.get(stack_row)
        find: Optional[List[Tuple[int, int]]] = None
        current: Optional[Tuple[int, int]] = None
        if self._find_spans:
            find = self._find_spans.get(stack_row)
            if stack_row == self._find_current_row:
                current = self._find_current_span
        return RowContext(stack_row, links, self._normalized_selection(), find, current)

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

    def _scroll_to_top(self) -> None:
        """Jump to the oldest scrollback row (Shift+Home)."""
        if self._in_alt():
            return
        self._scroll_offset = self._history_len()
        self._refresh_scrollbar()
        self.update()

    def _scroll_to_bottom(self) -> None:
        """Jump back to the live screen (Shift+End)."""
        if self._in_alt():
            return
        self._scroll_offset = 0
        self._refresh_scrollbar()
        self.update()

    def _prompt_rows(self, kind: str = "A") -> List[int]:
        """Stack rows of the OSC 133 marks of *kind*, in emission order.

        A shell that never emitted OSC 133 leaves the list empty, so every
        navigation surface built on it is inert.
        """
        marks: List[PromptMark] = self.terminal.term_screen.prompt_marks
        return [row for row, _column, mark_kind, _exit in marks if mark_kind == kind]

    def _scroll_to_previous_prompt(self) -> None:
        """Jump so the previous prompt starts at the top of the viewport."""
        if self._in_alt():
            return
        rows: List[int] = self._prompt_rows("A")
        if not rows:
            return
        anchor: int = self._history_len() - self._scroll_offset
        index: int = bisect.bisect_left(rows, anchor) - 1
        if index < 0:
            return
        self._scroll_offset = max(
            0, min(self._history_len() - rows[index], self._history_len())
        )
        self._refresh_scrollbar()
        self.update()

    def _scroll_to_next_prompt(self) -> None:
        """Jump so the next prompt starts at the top of the viewport."""
        if self._in_alt():
            return
        rows: List[int] = self._prompt_rows("A")
        if not rows:
            return
        anchor: int = self._history_len() - self._scroll_offset
        index: int = bisect.bisect_right(rows, anchor)
        if index >= len(rows):
            return
        self._scroll_offset = max(
            0, min(self._history_len() - rows[index], self._history_len())
        )
        self._refresh_scrollbar()
        self.update()

    def _page_rows(self) -> int:
        return max(self.terminal.term_screen.lines - 1, 1)

    def _anchor_scrollback(self) -> None:
        """Keep the text under the reader still when the bounded history drops
        rows.

        A scrolled-out row is appended to ``history.top``, so a stack index
        stays valid while the deque merely grows. Once it is full the append
        drops the leftmost row instead and every remaining row moves one index
        towards zero; a reader parked in the scrollback would watch the text
        crawl upwards. The screen counts those drops in ``history_generation``.
        The offset is measured from the live screen upwards, so following the
        text means *adding* the delta (a row that moved from index 6 to 5 is
        one row further back), and a cleared scrollback - the same counter,
        but with fewer rows left than before - returns to the bottom.
        """
        generation: int = self._history_generation()
        history_len: int = self._history_len()
        previous_generation: Optional[int] = self._hist_gen
        previous_len: int = self._hist_seen
        self._hist_gen = generation
        self._hist_seen = history_len
        if previous_generation is None or generation == previous_generation:
            return
        if history_len < previous_len:
            # The scrollback was emptied (CSI 3 J / RIS); there is nothing
            # left to stay anchored to.
            self._scroll_offset = 0
            return
        if self._scroll_offset > 0:
            self._scroll_offset = min(
                self._scroll_offset + (generation - previous_generation),
                history_len,
            )

    def _refresh_scrollbar(self) -> None:
        if self._in_alt():
            self._scroll_offset = 0
            self._sb_visible = False
            self._scrollbar.hide()
            self._recompute_geometry()
            return
        self._anchor_scrollback()
        history_len: int = self._history_len()
        # A cleared scrollback (CSI 3 J, RIS) leaves the offset past the new
        # end, and the slider below is signal-blocked so it cannot correct it.
        # Without this clamp paintEvent stops at the first negative stack row
        # and draws nothing until the user scrolls down.
        self._scroll_offset = max(0, min(self._scroll_offset, history_len))
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
        if screen.palette_version != self._palette_version:
            # An application set a palette slot or a default colour (OSC
            # 4/10/11/12) or reset one. Every memoised style may name the old
            # colour, so the caches are dropped and the whole viewport is
            # repainted; the theme defaults are re-resolved around the
            # overrides.
            self._palette_version = screen.palette_version
            self._apply_screen_defaults()
            self._style_cache.clear()
            self._color_cache.clear()
            self._style_copy_toast()
            self._style_find_bar()
            self.update()
        if self._find_query and self._find_gen != screen.history_generation:
            # The scrollback shifted under the highlight (deque overflow or a
            # clear), so the recorded stack rows no longer point at the text
            # that matched; rescan it, exactly as the selection is dropped.
            self._rescan_find()
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
            rows: List[int] = [y for y in dirty if 0 <= y < lines]
            cursor_y = screen.cursor.y
            if screen.cursor.hidden or cursor_y != self._last_cursor_y:
                # The cursor moved or vanished: repaint its previous cell so
                # the old block cursor does not linger (pyte cursor moves do
                # not mark rows dirty).
                if self._last_cursor_y is not None and 0 <= self._last_cursor_y < lines:
                    rows.append(self._last_cursor_y)
                self._last_cursor_y = cursor_y if not screen.cursor.hidden else None
            rows.append(cursor_y)
            self._repaint_rows(rows, lines)
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
            self._repaint_rows(self._blink_rows, lines)
        # The cursor blinks unless it is hidden or the application asked for a
        # steady style (DECSCUSR with an even parameter). Only the cursor cells
        # (previous + current row) change on its phase toggle; no need to
        # repaint the whole viewport.
        if not screen.cursor.hidden and screen.cursor_blink:
            self._blink_phase = not self._blink_phase
            cursor_rows: List[int] = []
            if self._last_cursor_y is not None and 0 <= self._last_cursor_y < lines:
                cursor_rows.append(self._last_cursor_y)
            if 0 <= screen.cursor.y < lines:
                cursor_rows.append(screen.cursor.y)
            self._repaint_rows(cursor_rows, lines)
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
        # A palette override (OSC 4) is keyed on exactly the token the cell
        # carries, so it is resolved before the built-in map: an application
        # that repaints "red" must change every cell painted red.
        override: Optional[str] = self.terminal.term_screen.palette_overrides.get(
            color_string
        )
        if override is not None:
            color_string = override
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
            if not color.isValid():
                # An unknown name or a malformed truecolour string leaves
                # QColor invalid, and fillRect with an invalid colour paints
                # black - a visible defect (pyte's "bfightmagenta" typo hit
                # exactly this). Fall back to the cell's default role.
                return self._default_fg if is_fg else self._default_bg
            if len(self._color_cache) >= self.COLOR_CACHE_LIMIT:
                self._color_cache.clear()
            self._color_cache[color_string] = color
        return color

    # ------------------------------------------------------------------
    # Painting
    # ------------------------------------------------------------------

    def paintEvent(self, event: qt.QPaintEvent) -> None:  # type: ignore[override]
        painter: qt.QPainter = qt.QPainter(self)
        painter.fillRect(event.rect(), self._default_bg)
        screen: ExtendedScreen = self.terminal.term_screen
        # Inline images sit beneath the glyph pass; the painter's clip region
        # already limits this to the invalidated band.
        self._paint_images(painter, screen)
        lines: int = screen.lines
        columns: int = screen.columns
        for y in range(lines):
            if not event.rect().intersects(self._row_band(y)):
                continue
            context: RowContext = self._row_context(y)
            if context.stack_row < 0:
                break
            row: Any = self._stack_row_cells(context.stack_row)
            self._paint_cells(painter, y, row, columns, context)
        self._paint_cursor(painter)
        if self._flash:
            # Visual bell: one final wash over the whole viewport, the glyphs
            # included. Filling only event.rect() behind the grid lit just the
            # band of a dirty-row repaint, and never the text at all.
            painter.fillRect(self.rect(), qt.QColor(255, 255, 255, 40))
        painter.end()

    # ------------------------------------------------------------------
    # Inline images (Kitty graphics / sixel)
    # ------------------------------------------------------------------

    def _paint_images(self, painter: qt.QPainter, screen: ExtendedScreen) -> None:
        """Draw the screen's placements beneath the glyph pass.

        Every visible image is re-issued on each paint; the painter's clip
        region keeps it to the rows Qt actually invalidated, so a one-row
        repaint still repaints just that slice of an image.
        """
        placements: List[Any] = screen.images.placements
        self._sync_image_cache(placements)
        if not placements:
            return
        top_stack: int = self._history_len() - self._scroll_offset
        viewport: qt.QRectF = qt.QRectF(self.rect())
        for placement in sorted(placements, key=lambda item: item.z_index):
            image: Optional[qt.QImage] = self._image_cache.get(placement.serial)
            if image is None:
                continue
            target: qt.QRectF = self._image_rect(placement, top_stack)
            if not target.intersects(viewport):
                continue
            painter.drawImage(target, image)

    def _image_rect(self, placement: Any, top_stack: int) -> qt.QRectF:
        """Widget rectangle a placement occupies, clipped later by Qt.

        A protocol-sized placement (Kitty ``c``/``r``) is stretched into its
        cell box; a pixel-sized one keeps its natural pixel dimensions, so a
        sixel or a bare Kitty transmission is never resampled to a rounded-up
        cell boundary.
        """
        viewport_row: int = placement.row - top_stack
        if placement.cell_sized:
            width: float = placement.columns * self._char_width
            height: float = placement.rows * self._char_height
        else:
            width = float(placement.image.width)
            height = float(placement.image.height)
        return qt.QRectF(
            placement.column * self._char_width,
            viewport_row * self._char_height,
            width,
            height,
        )

    def _sync_image_cache(self, placements: List[Any]) -> None:
        """Drop stale entries and decode any placement that has no QImage."""
        screen: ExtendedScreen = self.terminal.term_screen
        version: int = screen.images.version
        if version != self._image_version:
            self._image_version = version
            live: Set[int] = {placement.serial for placement in placements}
            self._image_cache = {
                key: value for key, value in self._image_cache.items() if key in live
            }
        for placement in placements:
            key: int = placement.serial
            if key in self._image_cache:
                continue
            image: Optional[qt.QImage] = self._qimage_for(placement)
            if image is not None:
                self._image_cache[key] = image

    def _qimage_for(self, placement: Any) -> Optional[qt.QImage]:
        """Decode a placement's pixels into a detached QImage, or None."""
        data: Any = placement.image
        if not data.data or data.width <= 0 or data.height <= 0:
            return None
        if data.kind == "png":
            image: qt.QImage = qt.QImage.fromData(data.data, "PNG")
        elif data.kind == "rgb":
            image = qt.QImage(
                data.data,
                data.width,
                data.height,
                data.width * 3,
                qt.QImage.Format.Format_RGB888,
            )
        elif data.kind == "rgba":
            image = qt.QImage(
                data.data,
                data.width,
                data.height,
                data.width * 4,
                qt.QImage.Format.Format_RGBA8888,
            )
        else:
            return None
        if image.isNull():
            return None
        # Detach from the Python buffer so a later store mutation cannot leave
        # Qt reading freed memory, then honour a Kitty source-rect crop. Kitty
        # lets w/h default to "rest of the image" when only x/y or one of them
        # is given.
        image = image.copy()
        if (
            placement.source_x
            or placement.source_y
            or placement.source_width
            or placement.source_height
        ):
            source_width: int = (
                placement.source_width
                if placement.source_width > 0
                else image.width() - placement.source_x
            )
            source_height: int = (
                placement.source_height
                if placement.source_height > 0
                else image.height() - placement.source_y
            )
            if source_width > 0 and source_height > 0:
                cropped: qt.QImage = image.copy(
                    qt.QRect(
                        placement.source_x,
                        placement.source_y,
                        source_width,
                        source_height,
                    )
                )
                if not cropped.isNull():
                    image = cropped
        return image

    def _paint_cells(
        self,
        painter: qt.QPainter,
        y: int,
        row: Any,
        columns: int,
        context: Optional[RowContext] = None,
    ) -> None:
        if context is None:
            context = self._row_context(y)
        cell_width: float = self._char_width
        cell_height: float = self._char_height
        baseline: float = y * cell_height + self._baseline
        x: int = 0
        last_pen: Optional[qt.QColor] = None
        last_font: Optional[qt.QFont] = None
        # Whether any cell of this row carries SGR-5 blink. The paint loop
        # already reads 'blink' off every cell it lays out (see the run loop
        # below), so tracking it here costs one assignment per cell and keeps
        # _on_blink from having to rescan the grid on every tick.
        row_blinks: bool = False
        # A style run is resolved one cell ahead: the cell that breaks the run
        # is measured to detect the break, so its style is carried into the
        # next run instead of being resolved a second time as that run's first
        # cell. With per-cell truecolour (an animation) every cell is its own
        # run, so without the carry-over the pass resolves every cell twice.
        pending: Optional[Tuple[qt.QColor, qt.QColor, qt.QFont]] = None
        while x < columns:
            cell: Any = row[x]
            style: Tuple[qt.QColor, qt.QColor, qt.QFont]
            if pending is None:
                style = self._cell_style(cell, y, x, context)
            else:
                style = pending
                pending = None
            # (column, character, cell span) for every glyph of this style run.
            # The columns are kept, rather than only the concatenated text,
            # because each glyph is drawn into its own cell: drawing the run
            # as one string lets a fallback glyph's advance (e.g. Inconsolata's
            # 6px '✕' or MS UI Gothic's 13px one) shift every following glyph
            # away from the grid, and clipping the string to the run rect cut
            # the tail of the last character.
            glyphs: List[Tuple[int, str, int]] = []
            run_start: int = x
            while x < columns:
                current: Any = row[x]
                if current.blink:
                    # Recorded before the style break below, so the cell that
                    # ends the run is counted too.
                    row_blinks = True
                # The run's first cell already has its style (computed above),
                # so it is not resolved a second time; every following cell is
                # resolved exactly once, and the one that breaks the run hands
                # its style to the next run.
                if x > run_start:
                    current_style: Tuple[qt.QColor, qt.QColor, qt.QFont] = (
                        self._cell_style(current, y, x, context)
                    )
                    if current_style != style:
                        pending = current_style
                        break
                char_w: int = cluster_width(current.data)
                # A full-width character and its trailing stub (pyte marks
                # the stub with empty data) form one atomic unit: absorb the
                # stub unconditionally so selection or style changes at the
                # stub can never split the glyph into a one-cell box.
                if x + 1 < columns and char_w == 2 and row[x + 1].data == "":
                    char: str = current.data
                    if current.blink and not self._sgr_blink_phase:
                        char = " "
                    glyphs.append((x, char, 2))
                    x += 2
                    continue
                char = current.data
                if char == "" or (current.blink and not self._sgr_blink_phase):
                    char = " "
                    char_w = 1
                glyphs.append((x, char, 2 if char_w == 2 else 1))
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
            if glyphs:
                font: qt.QFont = style[2]
                if style[0] != last_pen:
                    painter.setPen(style[0])
                    last_pen = style[0]
                if font != last_font:
                    painter.setFont(font)
                    last_font = font
                # A blank cell shows only its background, so skip it - unless
                # the font decorates it (an underlined or struck-out blank is
                # part of the line, not a gap).
                decorated: bool = font.underline() or font.strikeOut()
                for column, char, cells in glyphs:
                    if char == " " and not decorated:
                        continue
                    self._draw_glyph(painter, font, char, column, cells, baseline)
        # Publish (or retract) this row for the blink tick. Retracting matters
        # as much as publishing: a row whose blinking cells were overwritten
        # must stop being repainted on every phase toggle.
        if row_blinks:
            self._blink_rows.add(y)
        else:
            self._blink_rows.discard(y)

    def _draw_glyph(
        self,
        painter: qt.QPainter,
        font: qt.QFont,
        char: str,
        column: int,
        cells: int,
        baseline: float,
    ) -> None:
        """Draw one glyph at its own cell's origin and the row's baseline.

        No clip rect is involved: a glyph's ink is allowed to overhang its
        advance (box drawing, blocks, italics) instead of being cut at the
        cell edge. A glyph the font lacks comes from a fallback family whose
        sizing has nothing to do with the grid, so it is measured once and
        fitted into its cell span: scaled down when its advance is wider than
        the span, and - for a narrow symbol whose ink is shorter than the cap
        height - scaled up towards that height, because fallback families often
        draw symbols (e.g. Inconsolata's 5px U+2715) far smaller than their
        letters. A fitted glyph is positioned by its ink box, centred in the
        cell, so growing it cannot push it off the cell.

        Glyphs whose size is the message (see SIZE_SEMANTIC_RANGES) are never
        rescaled in either direction: the font's ink box is the value, so only
        their horizontal position is corrected.
        """
        x: float = column * self._char_width
        span: float = cells * self._char_width
        if self._font_has_glyph(font, char):
            painter.drawText(qt.QPointF(x, baseline), char)
            return
        advance: float
        ink: Tuple[float, float, float, float]
        advance, ink = self._glyph_shape(font, char)
        if advance <= 0.0:
            painter.drawText(qt.QPointF(x, baseline), char)
            return
        ink_width: float = ink[2]
        ink_height: float = ink[3]
        if self._is_size_semantic(char):
            if ink_width > 0.0 and ink_height > 0.0:
                self._draw_natural_centred(painter, char, ink, x, span, baseline)
            else:
                painter.drawText(qt.QPointF(x, baseline), char)
            return
        scale: float = span / advance if advance > span else 1.0
        if scale == 1.0 and cells == 1:
            scale = self._fit_scale(char, ink, span)
        if scale == 1.0 or ink_width <= 0.0 or ink_height <= 0.0:
            # Natural size: centre the advance in the cell, as drawing the
            # glyph into a cell-wide rect used to do.
            offset: float = max((span - advance) / 2.0, 0.0)
            if offset == 0.0:
                painter.drawText(qt.QPointF(x, baseline), char)
                return
            painter.save()
            painter.translate(x + offset, baseline)
            painter.drawText(qt.QPointF(0.0, 0.0), char)
            painter.restore()
            return
        # Fitted: scale about the ink box's centre and put that centre in the
        # middle of the cell, so the glyph grows and shrinks symmetrically
        # instead of climbing away from the baseline.
        ink_centre_x: float = ink[0] + ink_width / 2.0
        ink_centre_y: float = ink[1] + ink_height / 2.0
        row_centre: float = baseline - self._baseline + self._char_height / 2.0
        painter.save()
        painter.translate(
            x + span / 2.0 - ink_centre_x * scale,
            row_centre - ink_centre_y * scale,
        )
        painter.scale(scale, scale)
        painter.drawText(qt.QPointF(0.0, 0.0), char)
        painter.restore()

    def _draw_natural_centred(
        self,
        painter: qt.QPainter,
        char: str,
        ink: Tuple[float, float, float, float],
        x: float,
        span: float,
        baseline: float,
    ) -> None:
        """Draw a size-encoded glyph at the font's own size and baseline.

        Only the horizontal position is corrected: a fallback family's advance
        has nothing to do with the cell, so the ink box is centred in the span
        (opencode's U+2B25 diamond has an 11px advance in an 8px cell and would
        otherwise bleed into its neighbour). The glyph is *not* moved
        vertically, because block elements encode their fill height in where
        the ink sits relative to the baseline.
        """
        ink_centre_x: float = ink[0] + ink[2] / 2.0
        painter.save()
        painter.translate(x + span / 2.0 - ink_centre_x, baseline)
        painter.drawText(qt.QPointF(0.0, 0.0), char)
        painter.restore()

    def _is_size_semantic(self, char: str) -> bool:
        """Whether *char*'s ink size is meaningful (see SIZE_SEMANTIC_RANGES)."""
        code: int = ord(char[0])
        return any(low <= code <= high for low, high in self.SIZE_SEMANTIC_RANGES)

    def _fit_scale(
        self, char: str, ink: Tuple[float, float, float, float], span: float
    ) -> float:
        """Up-scale factor for a small narrow fallback glyph, at least 1.0.

        The glyph's ink should read at the size of the surrounding letters, so
        it is grown until it is as tall as the cap height - but never so wide
        that it loses its margin inside the cell. Glyphs already taller than
        the cap height (CJK, emoji, heavy symbols) are left alone, and
        size-encoded symbols never reach this method at all (they are drawn by
        _draw_natural_centred instead).
        """
        ink_width: float = ink[2]
        ink_height: float = ink[3]
        if ink_width <= 0.0 or ink_height <= 0.0 or self._cap_height <= 0.0:
            return 1.0
        grow: float = self._cap_height / ink_height
        if grow <= 1.0:
            return 1.0
        # One pixel of margin keeps the scaled symbol from touching its
        # neighbours (a solid 8px-wide cross in an 8px cell reads as a block).
        width_limit: float = max(span - 1.0, 1.0) / ink_width
        return max(1.0, min(grow, width_limit))

    def _font_has_glyph(self, font: qt.QFont, char: str) -> bool:
        """Whether the style font itself covers *char* (no fallback family)."""
        key: Tuple[int, str] = (id(font), char)
        covered: Optional[bool] = self._glyph_coverage.get(key)
        if covered is None:
            raw: Optional[qt.QRawFont] = self._raw_font(font)
            if raw is None or not raw.isValid():
                covered = True
            else:
                indexes: List[int] = list(raw.glyphIndexesForString(char))
                covered = bool(indexes) and indexes[0] != 0
            self._glyph_coverage[key] = covered
        return covered

    def _raw_font(self, font: qt.QFont) -> Optional[qt.QRawFont]:
        key: int = id(font)
        if key not in self._raw_fonts:
            try:
                self._raw_fonts[key] = qt.QRawFont.fromFont(font)
            except Exception:
                self._raw_fonts[key] = None
        return self._raw_fonts[key]

    def _glyph_shape(
        self, font: qt.QFont, char: str
    ) -> Tuple[float, Tuple[float, float, float, float]]:
        """Advance and ink box actually used for *char*, including font merging.

        QFontMetricsF reports the primary family's advance, which is the
        .notdef width for a glyph the family lacks; shaping the character once
        gives the fallback's real advance, and the glyph run's raw font knows
        where the ink actually sits (origin-relative, in pixels). The ink box is
        empty for a multi-glyph run (ligature/cluster), which leaves the caller
        with the plain advance.
        """
        key: Tuple[int, str] = (id(font), char)
        shape: Optional[Tuple[float, Tuple[float, float, float, float]]] = (
            self._glyph_shapes.get(key)
        )
        if shape is None:
            layout: qt.QTextLayout = qt.QTextLayout(char)
            layout.setFont(font)
            layout.beginLayout()
            line: qt.QTextLine = layout.createLine()
            line.setLineWidth(10000.0)
            layout.endLayout()
            advance: float = line.naturalTextWidth()
            ink: Tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)
            runs: List[qt.QGlyphRun] = list(line.glyphRuns())
            if runs:
                run: qt.QGlyphRun = runs[0]
                indexes: List[int] = list(run.glyphIndexes())
                if len(indexes) == 1:
                    try:
                        box: qt.QRectF = run.rawFont().boundingRect(indexes[0])
                    except Exception:
                        box = qt.QRectF()
                    if box.width() > 0.0 and box.height() > 0.0:
                        ink = (box.x(), box.y(), box.width(), box.height())
            shape = (advance, ink)
            if len(self._glyph_shapes) >= self.GLYPH_SHAPE_LIMIT:
                self._glyph_shapes.clear()
            self._glyph_shapes[key] = shape
        return shape

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
        self,
        cell: Any,
        y: int,
        x: int,
        context: Optional[RowContext] = None,
    ) -> Tuple[qt.QColor, qt.QColor, qt.QFont]:
        """Resolved (fg, bg, font) for a cell, memoised on its style key.

        *context* is the row's hoisted state (see _row_context); when it is
        omitted - a caller outside the paint loop - the row is described here.
        """
        if context is None:
            context = self._row_context(y)
        links: Optional[Dict[int, str]] = context.links
        link: bool = links is not None and x in links
        selection: Optional[Tuple[int, int, int, int]] = context.selection
        selected: bool = selection is not None and self._cell_in_selection(
            selection, context.stack_row, x, self._block_selection
        )
        find_spans: Optional[List[Tuple[int, int]]] = context.find
        matched: bool = find_spans is not None and any(
            start <= x <= end for start, end in find_spans
        )
        current: bool = context.find_current is not None and (
            context.find_current[0] <= x <= context.find_current[1]
        )
        key: Tuple[Any, ...] = (
            cell.bg,
            cell.fg,
            cell.bold,
            cell.italics,
            cell.underscore,
            cell.strikethrough,
            cell.reverse,
            selected,
            link,
            matched,
            current,
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
            if matched:
                # A find hit is a search overlay, so it wins over the selection
                # highlight: "next match" must stay visible even when the match
                # lies inside a region the user selected earlier.
                fg = self._find_fg
                bg = self._find_current_bg if current else self._find_bg
            elif selected:
                # One highlight pair for every selected cell, taken from the
                # theme's defaults instead of swapping the cell's own colours a
                # second time: a selected reverse-video cell came out exactly
                # like unselected plain text, so a selection spanning mixed
                # content had holes in it. It also keeps the highlight uniform
                # instead of following each cell's palette.
                fg, bg = self._default_bg, self._default_fg
            style = (fg, bg, font)
            # Bounded on purpose: an animation gives every frame a new key (see
            # STYLE_CACHE_LIMIT). Clearing costs a repaint, not correctness.
            if len(self._style_cache) >= self.STYLE_CACHE_LIMIT:
                self._style_cache.clear()
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
        # Resolve the cell exactly as the grid painted it - reverse video, the
        # selection highlight and the link underline included. Deriving the
        # colours from the raw cell ignored the selection, so the block cursor
        # over a selected cell filled with the very colour the highlight had
        # and disappeared.
        fg: qt.QColor
        bg: qt.QColor
        font: qt.QFont
        fg, bg, font = self._cell_style(cell, y, x, self._row_context(y))
        cursor_style: str = screen.cursor_style
        char: str = cell.data if cell.data != "" else " "
        wide: bool = cluster_width(char) == 2
        has_stub: bool = wide and x + 1 < screen.columns and row[x + 1].data == ""
        cells: int = 2 if has_stub else 1
        rect: qt.QRectF = qt.QRectF(
            x * self._char_width,
            y * self._char_height,
            self._char_width * cells,
            self._char_height,
        )
        baseline: float = y * self._char_height + self._baseline
        # OSC 12 may give the cursor its own colour; without it the cursor is
        # drawn in the cell's painted foreground, as before.
        cursor_spec: Optional[str] = screen.cursor_colour_override
        fill: qt.QColor = qt.QColor(cursor_spec) if cursor_spec else fg
        # An unfocused terminal draws a hollow block: the cell's own glyph is
        # left untouched and only the outline says where the cursor is, the
        # convention every mainstream terminal uses so the window that is not
        # receiving keystrokes does not look like the active one.
        focused: bool = self.hasFocus()
        if cursor_style == "underline":
            underline: qt.QRectF = qt.QRectF(
                rect.x(),
                rect.y() + rect.height() - max(self._char_height * 0.15, 2.0),
                rect.width(),
                max(self._char_height * 0.15, 2.0),
            )
            painter.fillRect(underline, fill)
            painter.setPen(fg)
            painter.setFont(font)
            self._draw_glyph(painter, font, char, x, cells, baseline)
        elif cursor_style == "bar":
            bar: qt.QRectF = qt.QRectF(
                rect.x(),
                rect.y(),
                max(self._char_width * 0.15, 2.0),
                rect.height(),
            )
            painter.fillRect(bar, fill)
        elif not focused:
            # Hollow block: outline drawn inside the cell so the grid's own
            # glyph stays legible. The pen is the block fill colour, so an
            # OSC 12 override applies to the outline too.
            pen: qt.QPen = qt.QPen(fill)
            pen.setWidthF(max(self._char_width * 0.12, 1.0))
            painter.setPen(pen)
            painter.setBrush(qt.Qt.BrushStyle.NoBrush)
            painter.drawRect(rect.adjusted(0.5, 0.5, -0.5, -0.5))
        else:
            # Block cursor inverts the painted cell: fill with the painted
            # foreground and draw the glyph in the painted background so the
            # block stays visible on plain, reverse-video and highlighted
            # cells alike.  (Filling with the background and drawing the
            # glyph in the foreground would reproduce the cell exactly and
            # make the cursor invisible.)
            painter.fillRect(rect, fill)
            painter.setPen(bg)
            painter.setFont(font)
            self._draw_glyph(painter, font, char, x, cells, baseline)

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

    def _normalized_selection(self) -> Optional[Tuple[int, int, int, int]]:
        """Selection bounds normalized for a reverse drag, or None.

        A linear selection is a start/end pair in reading order, so a single
        swap puts it right. A block selection keeps its columns independent
        of its rows, so a diagonal drag has to be clamped on each axis.
        """
        bounds: Optional[Selection] = self._selection_bounds()
        if bounds is None:
            return None
        r0, c0, r1, c1 = cast(Tuple[int, int, int, int], bounds)
        if self._block_selection:
            return min(r0, r1), min(c0, c1), max(r0, r1), max(c0, c1)
        # Normalize reverse drags (start after end) so the highlight is
        # correct while the mouse is still held down.
        if (r0, c0) > (r1, c1):
            r0, c0, r1, c1 = r1, c1, r0, c0
        return r0, c0, r1, c1

    def _is_selected(self, y: int, x: int) -> bool:
        bounds: Optional[Tuple[int, int, int, int]] = self._normalized_selection()
        if bounds is None:
            return False
        return self._cell_in_selection(
            bounds, self._stack_row(y), x, self._block_selection
        )

    @staticmethod
    def _cell_in_selection(
        bounds: Tuple[int, int, int, int],
        stack_row: int,
        x: int,
        block: bool = False,
    ) -> bool:
        """Whether stack cell (stack_row, x) lies inside normalized *bounds*.

        A linear selection also covers the whole width of the rows between
        its endpoints; a block selection is the rectangle the two corners
        delimit and covers only those columns.
        """
        if stack_row < 0:
            return False
        r0, c0, r1, c1 = bounds
        if block:
            return r0 <= stack_row <= r1 and c0 <= x <= c1
        if r0 == r1:
            return stack_row == r0 and c0 <= x <= c1
        if r0 < stack_row < r1:
            return True
        if stack_row == r0:
            return x >= c0
        if stack_row == r1:
            return x <= c1
        return False

    def _row_text(self, stack_row: int) -> str:
        """Full text of a stack row, one character per column (a wide glyph's
        stub contributes nothing, exactly as pyte stores it)."""
        row: Any = self._stack_row_cells(stack_row)
        columns: int = self.terminal.term_screen.columns
        return "".join(row[x].data or "" for x in range(columns))

    def _selection_text(self) -> str:
        bounds: Optional[Tuple[int, int, int, int]] = self._normalized_selection()
        if bounds is None:
            return ""
        r0, c0, r1, c1 = bounds
        columns: int = self.terminal.term_screen.columns
        lines: List[str] = []
        for stack_row in range(r0, r1 + 1):
            row: Any = self._stack_row_cells(stack_row)
            if self._block_selection:
                # A block keeps the same column window on every row.
                start: int = c0
                end: int = min(c1, columns - 1)
            else:
                start = c0 if stack_row == r0 else 0
                end = c1 if stack_row == r1 else columns - 1
            text: str = "".join(row[x].data for x in range(start, end + 1))
            lines.append(text.rstrip())
        return "\n".join(lines)

    def copy_selection(self) -> None:
        text: str = self._selection_text()
        if text:
            application: Any = data.application
            application.clipboard().setText(text)
            self._show_copy_toast()

    def _all_text(self) -> str:
        """Whole scrollback + screen as text, trailing blank rows dropped (the
        blank tail below the last printed line is not content)."""
        screen: ExtendedScreen = self.terminal.term_screen
        lines: List[str] = []
        for stack_row in range(self._history_len() + screen.lines):
            lines.append(self._row_text(stack_row).rstrip())
        while lines and not lines[-1]:
            lines.pop()
        return "\n".join(lines)

    def select_all(self) -> None:
        """Select the whole stack (scrollback + screen)."""
        screen: ExtendedScreen = self.terminal.term_screen
        self._block_selection = False
        self._selection = (
            0,
            0,
            self._history_len() + screen.lines - 1,
            screen.columns - 1,
        )
        self._selection_active = False
        self._sel_hist_gen = self._history_generation()
        self.update()

    def copy_all(self) -> None:
        text: str = self._all_text()
        if text:
            application: Any = data.application
            application.clipboard().setText(text)
            self._show_copy_toast()

    def _last_output_text(self) -> str:
        """The last command's output, from its OSC 133 C mark to its D mark.

        A ``C`` mark records where output began; the following ``D`` marks the
        next prompt and therefore the end of that output (its column is
        exclusive, so a mark at column 0 ends before the prompt row). The
        bottom of the stack stands in while the command is still running.

        Without a ``C`` mark - cmd.exe can only stamp prompts from PROMPT, and
        PowerShell falls back when PSReadLine is unavailable - the text between
        the previous two prompt starts is used instead, which is the same
        region minus the command line itself.
        """
        screen: ExtendedScreen = self.terminal.term_screen
        marks: List[PromptMark] = screen.prompt_marks
        last_stack_row: int = self._history_len() + screen.lines - 1
        start_row: int = 0
        start_column: int = 0
        end_row: int = 0
        end_column: Optional[int] = None
        found: bool = False
        for index in range(len(marks) - 1, -1, -1):
            row, column, kind, _exit = marks[index]
            if kind != "C":
                continue
            start_row, start_column = row, column
            end_row = last_stack_row
            for later_row, later_column, later_kind, _later_exit in marks[index + 1 :]:
                if later_kind == "D":
                    end_row, end_column = later_row, later_column
                    break
            found = True
            break
        if not found:
            prompts: List[PromptMark] = [mark for mark in marks if mark[2] == "A"]
            if len(prompts) < 2:
                return ""
            start_row = prompts[-2][0] + 1
            start_column = 0
            end_row = prompts[-1][0] - 1
        if start_column > 0:
            # A C mark at a column sits at the end of the submitted command
            # line, not at the start of the output row; the output begins on
            # the following row (Enter has already moved there).
            start_row += 1
            start_column = 0
        if start_row > last_stack_row or end_row < start_row:
            return ""
        end_row = min(end_row, last_stack_row)
        lines: List[str] = []
        for row in range(start_row, end_row + 1):
            text: str = self._row_text(row)
            if row == start_row:
                text = text[start_column:]
            if row == end_row and end_column is not None:
                text = text[:end_column]
            lines.append(text.rstrip())
        while lines and not lines[0]:
            lines.pop(0)
        while lines and not lines[-1]:
            lines.pop()
        return "\n".join(lines)

    def copy_last_output(self) -> None:
        """Copy the last command's output to the clipboard."""
        text: str = self._last_output_text()
        if text:
            application: Any = data.application
            application.clipboard().setText(text)
            self._show_copy_toast()

    def put_clipboard_text(self, text: str) -> None:
        """Put *text* on the system clipboard without the copy toast.

        An OSC 52 write comes from the application, not from a user copy, so
        claiming "Copied to clipboard" would describe something the user did
        not do.
        """
        application: Any = data.application
        if application is not None:
            application.clipboard().setText(text)

    def clipboard_text(self) -> str:
        """The system clipboard's text, or ``""`` without an application."""
        application: Any = data.application
        if application is None:
            return ""
        return application.clipboard().text()

    def osc52_clipboard_text(self) -> Optional[str]:
        """Clipboard contents for an OSC 52 read, or None when refused.

        A read is refused while the view does not have focus: an application
        that never sees the user's keystrokes has no business reading what
        they copied in another window.
        """
        if not self.hasFocus():
            return None
        return self.clipboard_text()

    def show_notification(self, title: str, body: str) -> None:
        """Surface an OSC 9 / 777 notification in the status bar.

        The terminal has no desktop-notification surface of its own and the
        emulator must never print into its grid, so the app's status line is
        the display path. Without a main form (a screen-level harness or
        headless use) the notification is dropped, never raised.
        """
        text: str = "{}: {}".format(title, body) if title else body
        main_form: Any = getattr(self.terminal, "main_form", None)
        display: Any = getattr(main_form, "display", None)
        write: Any = getattr(display, "write_to_statusbar", None)
        if not callable(write):
            return
        try:
            write("Terminal: " + text, 6000)
        except Exception:
            # A statusbar that is already torn down (application shutting
            # down) must not break the PTY reader thread mid-feed.
            pass

    def _copy_link(self, uri: str) -> None:
        """Copy a hyperlink's target rather than its visible text."""
        application: Any = data.application
        application.clipboard().setText(uri)
        self._show_copy_toast()

    def clear_scrollback(self) -> None:
        """Drop the saved lines, keeping the visible screen (xterm CSI 3 J)."""
        screen: ExtendedScreen = self.terminal.term_screen
        screen.clear_scrollback()
        self._scroll_offset = 0
        self._clear_selection()
        self._clear_find_highlights()
        self._refresh_scrollbar()
        self.update()

    def reset_terminal(self) -> None:
        """Reset the emulation state (RIS) without restarting the shell."""
        reset: Any = getattr(self.terminal, "reset_terminal", None)
        if callable(reset):
            reset()
        else:
            self.terminal.term_screen.reset()
        self._scroll_offset = 0
        self._clear_selection()
        self._clear_find_highlights()
        self.update()

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
        return self.clipboard_text()

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
                if cluster_width(row[col].data or "") == 2:
                    return col + 1
            return col
        owner: Optional[int] = self._wide_stub_owner(row, col)
        return col if owner is None else owner

    def _start_selection(self, position: qt.QPointF, block: bool = False) -> None:
        """Start a linear drag selection, or a block one when *block* is set:
        Alt+left-drag selects the rectangle the two corners delimit."""
        stack_row, col = self._pos_cell(position)
        self._block_selection = block
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
        self._block_selection = False
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
            # A block drag that never moved selected nothing either.
            self._block_selection = False
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
        return x - 1 if cluster_width(previous) == 2 else None

    def _word_boundary(self, row: Any, x: int) -> bool:
        """True when the cell at *x* ends the word being scanned: real
        whitespace, or any empty cell that is not a wide glyph's stub.

        Without the stub exemption every double-width glyph terminates a word,
        so a space-free script (CJK) could only ever be selected one character
        at a time."""
        if self._wide_stub_owner(row, x) is not None:
            return False
        return self._cell_blank(row, x)

    def _chunk_start(self, row: Any, x: int) -> int:
        """First column of the whitespace-delimited chunk containing *x*."""
        while x > 0 and not self._word_boundary(row, x - 1):
            x -= 1
        return x

    def _chunk_end(self, row: Any, x: int, columns: int) -> int:
        """Last column of the whitespace-delimited chunk containing *x*."""
        while x < columns - 1 and not self._word_boundary(row, x + 1):
            x += 1
        return x

    @staticmethod
    def _chunk_text(row: Any, start: int, end: int) -> str:
        return "".join(row[x].data for x in range(start, end + 1))

    @staticmethod
    def _has_path_separator(chunk: str) -> bool:
        return "\\" in chunk or "/" in chunk

    @staticmethod
    def _is_path_prefix(chunk: str) -> bool:
        """Whether *chunk* starts like the head of a path.

        A drive (``C:\\``), a UNC share, a rooted POSIX path, a home path or
        an explicitly relative path is strong enough evidence to bridge the
        spaces after it; a bare word is not.
        """
        if (
            len(chunk) >= 3
            and chunk[0].isalpha()
            and chunk[1] == ":"
            and chunk[2] in "\\/"
        ):
            return True
        if chunk.startswith(("\\\\", "//", "/", "\\", "~")):
            return True
        return chunk.startswith(("./", ".\\", "../", "..\\"))

    def _bridge_right(self, row: Any, end: int, columns: int) -> int:
        """Extend a selection end past spaces to a chunk with a separator.

        Paths may contain spaces (``C:\\Program Files\\App``). A double-click
        on any of their chunks should take the whole path, so the scan steps
        over up to PATH_BRIDGE_CHUNKS chunks and stops at the first one that
        contains ``\\`` or ``/``. Nothing is bridged when no such chunk turns
        up, which keeps prose untouched. The limitation is deliberate: a path
        split after its last separator (``Some Path\\file.txt`` without a
        prefix) has nothing to bridge towards.
        """
        position: int = end + 1
        for _ in range(self.PATH_BRIDGE_CHUNKS):
            while position < columns and self._word_boundary(row, position):
                position += 1
            if position >= columns:
                return end
            chunk_end: int = self._chunk_end(row, position, columns)
            chunk: str = self._chunk_text(row, position, chunk_end)
            if self._has_path_separator(chunk):
                return chunk_end
            position = chunk_end + 1
        return end

    def _bridge_left(self, row: Any, start: int) -> int:
        """Extend a selection start back to a path prefix.

        The clicked chunk may be the tail of a path whose head was split off
        by spaces (``C:\\Some Path\\file.txt`` clicked on ``file.txt``). Scan
        back over up to PATH_BRIDGE_CHUNKS chunks for a path prefix and start
        there. Without a prefix the selection keeps its chunk, so a prose
        line is not swallowed.
        """
        position: int = start - 1
        for _ in range(self.PATH_BRIDGE_CHUNKS):
            while position >= 0 and self._word_boundary(row, position):
                position -= 1
            if position < 0:
                return start
            chunk_start: int = self._chunk_start(row, position)
            chunk: str = self._chunk_text(row, chunk_start, position)
            if self._is_path_prefix(chunk):
                return chunk_start
            position = chunk_start - 1
        return start

    def _word_range(
        self, position: qt.QPointF
    ) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """Return (start_cell, end_cell) of the word under *position*. Both
        cells share the clicked stack row; the range always includes the
        clicked cell (which may be a single glyph).

        A word that looks like part of a path may span spaces: see
        _bridge_left/_bridge_right for the (bounded, deliberately
        conservative) rules.
        """
        stack_row, col = self._pos_cell(position)
        row: Any = self._stack_row_cells(stack_row)
        columns: int = self.terminal.term_screen.columns
        # Clicking the stub half of a wide glyph selects the word that glyph
        # belongs to, exactly as clicking the glyph itself does.
        owner: Optional[int] = self._wide_stub_owner(row, col)
        if owner is not None:
            col = owner
        start: int = self._chunk_start(row, col)
        end: int = self._chunk_end(row, col, columns)
        chunk: str = self._chunk_text(row, start, end)
        if self._is_path_prefix(chunk) or self._has_path_separator(chunk):
            end = self._bridge_right(row, end, columns)
            start = self._bridge_left(row, start)
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
            self._block_selection = False
            self.update()
            return
        start, end = self._word_range(position)
        self._block_selection = False
        self._selection = (start[0], start[1], end[0], end[1])
        self._selection_active = True
        self._sel_hist_gen = self._history_generation()
        self.update()

    def _select_line(self, position: qt.QPointF) -> None:
        """Select the whole physical line under *position* (triple-click).
        Trailing blanks are already trimmed by _selection_text."""

        stack_row: int = self._pos_cell(position)[0]
        columns: int = self.terminal.term_screen.columns
        self._block_selection = False
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
    # Find (scrollback search)
    # ------------------------------------------------------------------

    def open_find(self) -> None:
        """Show the scrollback find bar and focus its query editor."""
        self._find_bar.show()
        self._place_find_bar()
        self._find_bar.focus_editor()
        if self._in_alt():
            # A full-screen application owns this grid; there is no scrollback
            # of ours under it. Keep the bar open so the message is visible.
            self._find_bar.set_status("No scrollback here")
            return
        if self._find_query:
            self._rescan_find()

    def close_find(self) -> None:
        """Hide the bar, drop the highlights and give the shell its focus."""
        self._find_bar.hide()
        self._clear_find_highlights()
        self.setFocus()
        self.update()

    def find_next(self) -> None:
        self._step_find(1)

    def find_previous(self) -> None:
        self._step_find(-1)

    def _rescan_find(self) -> None:
        """Rebuild the hits after the stack or the grid changed under them.

        A history overflow or a clear shifts every recorded stack row; a
        resize or a font zoom changes every recorded column. Either way the old
        matches would highlight whatever now occupies those cells, so they are
        rescanned and the first visible hit is selected again - leaving the
        counter on a stale "3 of 12" would be a lie.
        """
        if not self._find_query:
            return
        self._rebuild_find_matches()
        self._find_index = -1
        self._find_current_row = -1
        self._find_current_span = None
        if self._find_matches:
            self.find_next()
        else:
            self._find_bar.set_status("No matches")
            self.update()

    def _clear_find_highlights(self) -> None:
        self._find_query = ""
        self._find_matches = []
        self._find_spans = {}
        self._find_index = -1
        self._find_current_row = -1
        self._find_current_span = None
        self._find_bar.set_status("")

    def _on_find_query(self, text: str) -> None:
        """Rescan for a new query and jump to the first visible hit."""
        self._find_query = text
        self._find_index = -1
        self._find_current_row = -1
        self._find_current_span = None
        self._rebuild_find_matches()
        if not text:
            self._find_bar.set_status("")
            self.update()
            return
        if not self._find_matches:
            self._find_bar.set_status("No matches")
            self.update()
            return
        self._find_bar.set_status("{} matches".format(len(self._find_matches)))
        self.find_next()

    def _rebuild_find_matches(self) -> None:
        """Scan the whole stack for the current query.

        Rows are scanned top to bottom and columns left to right, so the match
        list is already in navigation order. Case folding is applied per row
        and only when it preserves the length: a fold that changed the length
        would shift every column the highlight is drawn at, so such a row is
        matched case-sensitively instead.
        """
        self._find_matches = []
        self._find_spans = {}
        self._find_gen = self._history_generation()
        needle: str = self._find_query
        if not needle or self._in_alt():
            return
        needle_folded: str = needle.lower()
        screen: ExtendedScreen = self.terminal.term_screen
        stack_end: int = self._history_len() + screen.lines
        for stack_row in range(max(stack_end, 0)):
            text: str = self._row_text(stack_row)
            folded: str = text.lower()
            if len(folded) == len(text):
                haystack: str = folded
                target: str = needle_folded
            else:
                haystack = text
                target = needle
            spans: List[Tuple[int, int]] = []
            start: int = haystack.find(target)
            while start != -1:
                spans.append((start, start + len(target) - 1))
                self._find_matches.append((stack_row, start))
                start = haystack.find(target, start + 1)
            if spans:
                self._find_spans[stack_row] = spans

    def _step_find(self, direction: int) -> None:
        if not self._find_matches:
            if self._find_query:
                self._find_bar.set_status("No matches")
            return
        index: int
        if self._find_index < 0:
            # First hit after typing: start from the top visible row so a
            # match already on screen is not skipped.
            top: int = self._history_len() - self._scroll_offset
            if direction > 0:
                index = 0
                for candidate, (row, _column) in enumerate(self._find_matches):
                    if row >= top:
                        index = candidate
                        break
            else:
                index = len(self._find_matches) - 1
                for candidate in range(len(self._find_matches) - 1, -1, -1):
                    if self._find_matches[candidate][0] <= top:
                        index = candidate
                        break
        else:
            index = (self._find_index + direction) % len(self._find_matches)
        self._select_find_match(index)

    def _select_find_match(self, index: int) -> None:
        self._find_index = index
        stack_row: int
        start: int
        stack_row, start = self._find_matches[index]
        end: int = start + len(self._find_query) - 1
        self._find_current_row = stack_row
        self._find_current_span = (start, end)
        self._scroll_to_stack_row(stack_row)
        self._find_bar.set_status("{} of {}".format(index + 1, len(self._find_matches)))
        self.update()

    def _scroll_to_stack_row(self, stack_row: int) -> None:
        """Park the viewport so *stack_row* is its top row, clamped to the
        scrollback range."""
        history_len: int = self._history_len()
        self._scroll_offset = max(0, min(history_len - stack_row, history_len))
        self._refresh_scrollbar()
        self.update()

    def _style_find_bar(self) -> None:
        bar: Optional[TerminalFindBar] = getattr(self, "_find_bar", None)
        if bar is None:
            return
        bar.apply_style(self._default_fg, self._default_bg)

    def _place_find_bar(self) -> None:
        """Right-align the find strip over the top of the grid, inside the
        content width (never under the scrollbar)."""
        bar: Optional[TerminalFindBar] = getattr(self, "_find_bar", None)
        if bar is None or not bar.isVisibleTo(self):
            return
        width: int = min(420, max(self._content_width - 8, 160))
        bar.setGeometry(
            max(self._content_width - width - 4, 0),
            4,
            width,
            bar.sizeHint().height(),
        )
        bar.raise_()

    # ------------------------------------------------------------------
    # Font zoom (context menu)
    # ------------------------------------------------------------------

    def increase_font_size(self) -> None:
        self._change_font_zoom(1.0)

    def decrease_font_size(self) -> None:
        self._change_font_zoom(-1.0)

    def reset_font_size(self) -> None:
        self._change_font_zoom(-self._font_zoom)

    def _change_font_zoom(self, delta: float) -> None:
        """Grow/shrink this terminal's font for the session.

        The persisted size stays in settings; a menu adjustment is a per-tab
        view option, like a browser's zoom. Column and row counts change, so
        the screen and PTY are resized through the normal resize event.
        """
        zoom: float = max(-4.0, min(self._font_zoom + delta, 10.0))
        if zoom == self._font_zoom:
            return
        self._font_zoom = zoom
        self._load_style()
        self._recompute_geometry()
        self._place_copy_toast()
        self._place_find_bar()
        if self._find_query:
            self._rescan_find()
        if self.isVisible():
            cols: int
            rows: int
            cols, rows = self._terminal_size()
            self.resize_event.emit(cols, rows)
        self.update()

    # ------------------------------------------------------------------
    # Mouse
    # ------------------------------------------------------------------

    def _mouse_cell(self, position: qt.QPointF) -> Tuple[int, int]:
        x: int = int(position.x() / self._char_width)
        y: int = int(position.y() / self._char_height)
        return x, y

    def _refresh_link_index(self) -> None:
        """Rebuild the cell->URI lookup from screen.hyperlink_spans when the
        span list changed. Spans are recorded in stack coordinates (the screen
        adds the history length to the cursor row), so the index maps a
        stack_row to {column: uri} and renders identically over scrollback
        history; the screen shifts the spans when the bounded deque drops a
        row, so a scrolled-out link stays on the line it was drawn on."""
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
            # Alt+left-drag starts a rectangular (column) selection, the
            # gesture every classic terminal uses. It applies to the primary
            # screen only: inside a mouse-capturing TUI the app owns the
            # gesture and Alt is just another modifier to forward.
            block_drag: bool = bool(
                event.modifiers() & qt.Qt.KeyboardModifier.AltModifier
            )
            if block_drag and not shifted:
                self._press_select(event.position(), block=True)
            # Shift extends what is already selected instead of throwing it
            # away and starting over; with nothing selected it stays a plain
            # click. (Inside a mouse-capturing TUI Shift means "bypass" and
            # returns above.)
            elif not (shifted and self._extend_selection(event.position())):
                self._press_select(event.position())
        # A right-click keeps the selection so the context menu's Copy
        # action stays enabled; the next left-press starts a new selection.
        # Accept the press so the ignored default QWidget handling does not
        # propagate it up to the tab widget (which would steal focus)
        event.accept()

    def _press_select(self, position: qt.QPointF, block: bool = False) -> None:
        """Start a selection on a left press, honouring a triple-click: a
        third press within the double-click interval selects the whole line
        instead of starting a drag. A block press never counts as the third
        click of an armed triple-click."""
        if not block and self._double_clicked:
            self._select_line(position)
            self._double_clicked = False
            self._triple_click_timer.stop()
        else:
            self._start_selection(position, block=block)

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
        # The unfocused cursor is hollow, so gaining focus must repaint the
        # cursor cell even without any output.
        self.update()
        return super().focusInEvent(event)

    def focusOutEvent(self, event: qt.QFocusEvent) -> None:  # type: ignore[override]
        if self.terminal.term_screen.focus_report:
            self.send_text.emit("\x1b[O")
        self.update()
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
            copy_link_action: qt.QAction = qt.QAction("Copy Link Address", self)
            copy_link_action.setToolTip("Copy the hyperlink target to the clipboard")
            copy_link_action.triggered.connect(functools.partial(self._copy_link, uri))
            context_menu.addAction(copy_link_action)
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
        context_menu.addSeparator()
        find_action: qt.QAction = qt.QAction("Find…", self)
        find_action.setToolTip("Search the scrollback (Ctrl+F)")
        find_action.triggered.connect(self.open_find)
        select_all_action: qt.QAction = qt.QAction("Select All", self)
        select_all_action.setToolTip("Select the scrollback and the screen")
        select_all_action.triggered.connect(self.select_all)
        copy_all_action: qt.QAction = qt.QAction("Copy All", self)
        copy_all_action.setToolTip("Copy the scrollback and the screen")
        copy_all_action.triggered.connect(self.copy_all)
        context_menu.addAction(find_action)
        context_menu.addAction(select_all_action)
        context_menu.addAction(copy_all_action)
        context_menu.addSeparator()
        prompt_rows: List[int] = self._prompt_rows("A")
        anchor_row: int = self._history_len() - self._scroll_offset
        previous_prompt_action: qt.QAction = qt.QAction("Jump to Previous Prompt", self)
        previous_prompt_action.setToolTip(
            "Scroll to the previous OSC 133 prompt (Ctrl+Shift+Up)"
        )
        previous_prompt_action.triggered.connect(self._scroll_to_previous_prompt)
        previous_prompt_action.setEnabled(any(row < anchor_row for row in prompt_rows))
        next_prompt_action: qt.QAction = qt.QAction("Jump to Next Prompt", self)
        next_prompt_action.setToolTip(
            "Scroll to the next OSC 133 prompt (Ctrl+Shift+Down)"
        )
        next_prompt_action.triggered.connect(self._scroll_to_next_prompt)
        next_prompt_action.setEnabled(any(row > anchor_row for row in prompt_rows))
        last_output_action: qt.QAction = qt.QAction("Copy Last Command Output", self)
        last_output_action.setToolTip("Copy the output between the last OSC 133 marks")
        last_output_action.triggered.connect(self.copy_last_output)
        last_output_action.setEnabled(
            any(mark[2] == "C" for mark in self.terminal.term_screen.prompt_marks)
            or len(prompt_rows) >= 2
        )
        context_menu.addAction(previous_prompt_action)
        context_menu.addAction(next_prompt_action)
        context_menu.addAction(last_output_action)
        context_menu.addSeparator()
        clear_action: qt.QAction = qt.QAction("Clear Scrollback", self)
        clear_action.setToolTip("Drop the saved lines, keep the screen")
        clear_action.triggered.connect(self.clear_scrollback)
        clear_action.setEnabled(self._history_len() > 0)
        reset_action: qt.QAction = qt.QAction("Reset Terminal", self)
        reset_action.setToolTip("Reset the emulation state, keep the shell running")
        reset_action.triggered.connect(self.reset_terminal)
        context_menu.addAction(clear_action)
        context_menu.addAction(reset_action)
        context_menu.addSeparator()
        increase_action: qt.QAction = qt.QAction("Increase Font Size", self)
        increase_action.setToolTip("Enlarge this terminal's font")
        increase_action.triggered.connect(self.increase_font_size)
        decrease_action: qt.QAction = qt.QAction("Decrease Font Size", self)
        decrease_action.setToolTip("Shrink this terminal's font")
        decrease_action.triggered.connect(self.decrease_font_size)
        reset_font_action: qt.QAction = qt.QAction("Reset Font Size", self)
        reset_font_action.setToolTip(
            "Return this terminal's font to its configured size"
        )
        reset_font_action.triggered.connect(self.reset_font_size)
        reset_font_action.setEnabled(self._font_zoom != 0.0)
        context_menu.addAction(increase_action)
        context_menu.addAction(decrease_action)
        context_menu.addAction(reset_font_action)
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

        # Escape closes the find bar even when focus has moved back to the
        # grid (clicking the terminal leaves the query open and highlighted).
        if key == qt.Qt.Key.Key_Escape and self._find_bar.isVisible():
            self.close_find()
            event.accept()
            return

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

        # Find in the scrollback. Inside the alternate screen the key belongs
        # to the application: a full-screen TUI has no scrollback of ours to
        # search, and Ctrl+F is a common in-app binding.
        if (
            not self._in_alt()
            and modifiers == qt.Qt.KeyboardModifier.ControlModifier
            and key == qt.Qt.Key.Key_F
        ):
            self.open_find()
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
            if not ctrl and not alt and shift and key == qt.Qt.Key.Key_Home:
                self._scroll_to_top()
                event.accept()
                return
            if not ctrl and not alt and shift and key == qt.Qt.Key.Key_End:
                self._scroll_to_bottom()
                event.accept()
                return
            if ctrl and shift and not alt and key == qt.Qt.Key.Key_Up:
                self._scroll_to_previous_prompt()
                event.accept()
                return
            if ctrl and shift and not alt and key == qt.Qt.Key.Key_Down:
                self._scroll_to_next_prompt()
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
