"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

##  FILE DESCRIPTION:
##      Extended pyte screen + stream for maximal terminal emulation
##      compatibility:
##        - Alternate screen (47 / 1047 / 1049)
##        - Mouse tracking modes (1000 / 1002 / 1003 / 1006)
##        - Bracketed paste (2004)
##        - Kitty keyboard protocol (CSI > / < / ? u)
##        - OSC 0/1/2 title & icon, OSC 7 cwd, OSC 8 hyperlinks
##        - OSC 4 palette, OSC 10/11/12 default colours (+ 104/110/111/112)
##        - OSC 9/777 desktop notifications, OSC 52 clipboard
##        - OSC 133 shell-integration prompt/command/output marks
##        - DECSCUSR cursor style
##        - Bell surfacing

import base64
import binascii
import copy
import unicodedata
from collections import deque
from contextlib import contextmanager
from typing import (
    Any,
    Callable,
    Deque,
    Dict,
    Generator,
    Iterable,
    Iterator,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
)

try:
    import pyte
    from pyte import charsets as pyte_charsets
    from pyte import graphics as pyte_graphics
    from pyte import modes as pyte_modes
    from pyte import screens as pyte_screens
    from pyte import streams as pyte_streams
except ImportError:
    msg = """
The terminal emulator needs the following package 'pip install'-ed:
    - pip install pyte

On Windows the backend uses pywinpty (ConPTY), on Linux it uses ptyprocess.
"""
    raise ImportError(msg)

from gui.terminal.graphemes import cluster_width, is_combining, iter_clusters
from gui.terminal.images import ImageStore, Placement
from gui.terminal.reflow import ReflowResult, reflow

# Alternate screen private modes
ALT_SCREEN_MODES: Tuple[int, int, int] = (47, 1047, 1049)

# Mouse tracking private modes
MOUSE_BUTTON_MODE: int = 1000
MOUSE_DRAG_MODE: int = 1002
MOUSE_MOVE_MODE: int = 1003
MOUSE_SGR_MODE: int = 1006

# Focus reporting private mode: the terminal reports CSI I / CSI O to the
# application when the viewport gains / loses focus (xterm 1004).
FOCUS_REPORT_MODE: int = 1004

# Bracketed paste private mode
BRACKETED_PASTE_MODE: int = 2004

# Largest DCS/APC payload the parser will buffer (bytes). Kitty graphics and
# sixel arrive through this branch; anything larger is consumed and dropped.
MAX_ESCAPE_PAYLOAD: int = 16 * 1024 * 1024

# OSC 4 palette tokens. pyte emits an ANSI *name* for SGR 30-37 / 90-97 and a
# bare hex string for a 256-colour index, so an override has to be keyed on
# whichever token the cells will carry. Index 13 is spelled "bfightmagenta" in
# pyte's own background table (a typo, see view.FOREGROUND_COLOR_MAP), so both
# spellings move together.
PALETTE_NAMES: Tuple[Tuple[str, ...], ...] = (
    ("black",),
    ("red",),
    ("green",),
    ("brown",),
    ("blue",),
    ("magenta",),
    ("cyan",),
    ("white",),
    ("brightblack",),
    ("brightred",),
    ("brightgreen",),
    ("brightbrown",),
    ("brightblue",),
    ("brightmagenta", "bfightmagenta"),
    ("brightcyan",),
    ("brightwhite",),
)

_HEX_DIGITS: str = "0123456789abcdefABCDEF"

# OSC 52 payload cap, in decoded bytes. A runaway application must not be
# able to make the emulator allocate and hand over an arbitrarily large
# string; 1 MiB is far above any real "copy from the remote" payload.
MAX_OSC52_BYTES: int = 1024 * 1024

# OSC 9 / 777 notification text is shown in a one-line status area, so both
# parts are collapsed to one line and truncated. A hostile payload then
# cannot cover the UI with its own message.
MAX_NOTIFICATION_TITLE: int = 120
MAX_NOTIFICATION_BODY: int = 480

# OSC 133 shell-integration mark: (stack_row, column, kind, exit_code).
# kind is "A" prompt start, "B" command start, "C" output start, "D" command
# end; exit_code is only meaningful for "D" and None when the shell omitted
# it (cmd.exe cannot report the code from PROMPT).
PromptMark = Tuple[int, int, str, Optional[int]]


def parse_colour_spec(spec: str) -> Optional[str]:
    """Parse an X11 colour spec into ``#rrggbb``, or None when malformed.

    Accepted forms are the ones xterm's OSC 4/10/11/12 uses: ``rgb:r/g/b``
    with 1-4 hex digits per channel, and ``#rgb`` / ``#rrggbb`` /
    ``#rrrrggggbbbb``. A colour *name* or an empty string is rejected rather
    than guessed at, so a malformed payload cannot repaint the terminal.
    """
    text: str = spec.strip()
    if not text:
        return None
    channels: List[str]
    if text.startswith("rgb:"):
        channels = text[4:].split("/")
    elif text.startswith("#"):
        body: str = text[1:]
        if len(body) not in (3, 6, 12):
            return None
        width: int = len(body) // 3
        channels = [body[i * width : (i + 1) * width] for i in range(3)]
    else:
        return None
    if len(channels) != 3:
        return None
    values: List[int] = []
    for channel in channels:
        if (
            not channel
            or len(channel) > 4
            or any(digit not in _HEX_DIGITS for digit in channel)
        ):
            return None
        value: int = int(channel, 16)
        # 1 digit is a nibble (x11 scales it to 8 bits), 3 digits are 12-bit,
        # 4 digits are 16-bit; 2 digits are already 8-bit.
        if len(channel) == 1:
            value *= 17
        elif len(channel) == 3:
            value = value >> 4
        elif len(channel) == 4:
            value = value >> 8
        values.append(min(value, 255))
    return "#{:02x}{:02x}{:02x}".format(values[0], values[1], values[2])


def colour_spec(colour: str) -> str:
    """Format ``#rrggbb`` as the ``rgb:rr/gg/bb`` spec xterm answers with."""
    text: str = colour.lstrip("#")
    if len(text) == 3:
        text = "".join(digit * 2 for digit in text)
    if len(text) != 6:
        return "rgb:00/00/00"
    return "rgb:{0}/{1}/{2}".format(text[0:2], text[2:4], text[4:6])


def expand_sgr_subparameters(
    params: List[int], groups: Dict[int, List[str]]
) -> List[int]:
    """Turn colon-separated SGR parameters into the semicolon form pyte reads.

    *params* holds the first value of every parameter; *groups* maps a
    parameter's index to all of its colon-separated parts (as strings, empty
    meaning "default"). ``38:2::r:g:b`` / ``38:2:cs:r:g:b`` become
    ``38;2;r;g;b``, ``38:5:n`` becomes ``38;5;n``, an underline style
    ``4:s`` becomes plain underline (``s`` = 0 switches it off) and the
    underline colour (58/59) is dropped, since the grid has no such field.
    """

    def number(text: str) -> int:
        return min(int(text), 255) if text else 0

    expanded: List[int] = []
    for index, value in enumerate(params):
        group: Optional[List[str]] = groups.get(index)
        if group is None:
            expanded.append(value)
            continue
        if value in (38, 48):
            rest: List[str] = group[1:]
            mode: int = number(rest[0]) if rest else 0
            if mode == 2:
                channels: List[str] = rest[1:]
                if len(channels) > 3:
                    # An explicit colour-space id precedes the channels.
                    channels = channels[-3:]
                channels = (channels + ["0", "0", "0"])[:3]
                expanded.extend([value, 2] + [number(c) for c in channels])
            elif mode == 5 and len(rest) > 1:
                expanded.extend([value, 5, number(rest[1])])
        elif value == 4:
            style: int = number(group[1]) if len(group) > 1 else 1
            expanded.append(24 if style == 0 else 4)
        elif value in (58, 59):
            continue
        else:
            expanded.append(value)
    return expanded


class _TerminalRow(pyte_screens.StaticDefaultDict):
    """A screen row that remembers whether it continues on the next one.

    pyte has no wrap mark: a row is just a sparse mapping of column to cell, so
    the only thing that distinguishes "the text was exactly this wide and then a
    newline arrived" from "the text wrapped here" is the row object itself.
    ``wrapped`` records that the row ended because the cursor hit the right
    margin with DECAWM set, which is what reflow joins logical lines on.

    The mark lives on the row object on purpose: pyte moves row objects between
    ``buffer`` and ``history.top`` without copying them (scrolling, the bounded
    deque), so the mark follows its text.
    """

    def __init__(self, default: Any) -> None:
        super().__init__(default)
        self.wrapped: bool = False


class _Cell(pyte_screens.Char):
    """A pyte cell that also carries its OSC 8 hyperlink URI.

    pyte's ``Char`` has no hyperlink field, so the screen used to keep the
    links in a separate span list in stack coordinates. A span outlives the
    text it was recorded on: an erase, a redraw over the same cells or an
    alternate-screen scroll left it pointing at different cells, and the view
    underlined whatever it covered - stray horizontal lines across the grid.

    Keeping the URI on the cell makes it part of the text. Overwriting or
    erasing a cell drops it, and scrolling, reflow and history overflow move it
    with the row, so the underline can never detach from its link.

    ``_replace`` is overridden because the generated one only carries the
    ``Char`` fields; without it pyte's ``attrs._replace(...)`` would drop the
    URI on every SGR change. The attribute is only stored when there is a link,
    so an unlinked cell stays as small as pyte's own ``Char``.
    """

    hyperlink: Optional[str] = None
    # SGR 2 (faint / dim). pyte's Char has no such field either, so it rides on
    # the cell the same way the link does, and is likewise only stored when set.
    faint: bool = False

    def _replace(self, **kwargs: Any) -> "_Cell":
        hyperlink: Optional[str] = kwargs.pop(
            "hyperlink", getattr(self, "hyperlink", None)
        )
        faint: bool = kwargs.pop("faint", getattr(self, "faint", False))
        cell: "_Cell" = super()._replace(**kwargs)
        if hyperlink is not None:
            cell.hyperlink = hyperlink
        if faint:
            cell.faint = True
        return cell


class ExtendedScreen(pyte_screens.HistoryScreen):
    """
    HistoryScreen extended with alternate screen, mouse tracking,
    bracketed paste, OSC (title/icon/cwd/hyperlink), DECSCUSR, bell and
    inline images (Kitty graphics / sixel).
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # Per-feed-chunk scroll tracking for the view's repaint decision:
        # pending_scroll is non-zero when the content moved vertically this
        # chunk (the view then does a full repaint). Initialized before
        # super().__init__ because pyte's reset() runs during it; reset()
        # also clears keyboard_flags, so it lives here too.
        self.pending_scroll: int = 0
        self.keyboard_flags: int = 0
        # Inline images (Kitty graphics / sixel). Declared before
        # super().__init__ because pyte's reset() runs during it and clears
        # the store.
        self.images: ImageStore = ImageStore()
        # Bumped whenever an absolute index into history.top could start
        # pointing at different content: the bounded deque overflowing (index)
        # or the scrollback being emptied (_reset_history). The view records it
        # with a selection and drops that selection once it moves on. Declared
        # here because pyte's reset() runs inside super().__init__() below.
        self.history_generation: int = 0
        # OSC 4 / 10 / 11 / 12 palette state. An override is keyed on the
        # token the view will paint (an ANSI name, or pyte's bare hex for a
        # 256-colour index). render_colours is the view's report of what it
        # actually paints each token with, so a query answers what the user
        # sees instead of a second, possibly different, palette.
        self.palette_version: int = 0
        self.palette_overrides: Dict[str, str] = {}
        self.default_fg_override: Optional[str] = None
        self.default_bg_override: Optional[str] = None
        self.cursor_colour_override: Optional[str] = None
        self.render_colours: Dict[str, str] = {}
        self.render_default_fg: str = "#000000"
        self.render_default_bg: str = "#ffffff"
        # OSC query replies (e.g. "which colour is palette index 1?") are
        # written back to the application through the PTY, the same channel
        # the stream's Kitty reply uses; Terminal wires both to one writer.
        self.respond: Optional[Callable[[str], None]] = None
        # True only while pyte's draw() runs: the one place that calls
        # linefeed() from inside draw is the DECAWM wrap, which is how a row
        # gets its wrap mark (see _TerminalRow).
        self._drawing: bool = False
        # Old -> new stack position map from the last resize reflow, for the
        # view to re-anchor its scroll offset on. Consumed (and cleared) by the
        # view; None when the last resize did not reflow.
        self.reflow_map: Optional[ReflowResult] = None
        super().__init__(*args, **kwargs)
        # Alternate screen state
        self._alt_saved: Optional[Dict[str, Any]] = None
        self._alt_modes_active: Set[int] = set()
        # OSC state. The active URI is stamped onto every cell drawn while it
        # is open (see _Cell and draw), so a hyperlink is part of the text and
        # disappears with it.
        self.cwd: Optional[str] = None
        self.hyperlink: Optional[str] = None
        self._active_hyperlink: Optional[str] = None
        # OSC 133 shell-integration marks, in stack coordinates (history rows
        # below the live screen plus the viewport row). Bounded because a
        # prompt is recorded on every command and the list only ever needs to
        # span the retained scrollback.
        self.prompt_marks: List[PromptMark] = []
        # DECSCUSR state
        self.cursor_style: str = "block"
        self.cursor_blink: bool = True
        # Bell
        self.bell_triggered: bool = False
        # OSC 9 / 777 notifications and OSC 52 clipboard. The app owns both
        # surfaces (a status line, the system clipboard), so the screen only
        # parses and calls back; Terminal installs the handlers and copies
        # the settings into the flags. Flags are separate from handlers so a
        # disabled feature is inert even while a handler is installed.
        self.notifications_enabled: bool = False
        self.notification_handler: Optional[Callable[[str, str], None]] = None
        self.clipboard_write_enabled: bool = True
        self.clipboard_read_enabled: bool = False
        self.clipboard_write: Optional[Callable[[str], None]] = None
        self.clipboard_read: Optional[Callable[[], Optional[str]]] = None

    # ------------------------------------------------------------------
    # Alternate screen
    # ------------------------------------------------------------------

    @property
    def in_alt_screen(self) -> bool:
        return self._alt_saved is not None

    def _enter_alt_screen(self) -> None:
        if self._alt_saved is not None:
            return
        self._alt_saved = {
            "buffer": dict(self.buffer),
            "cursor": copy.copy(self.cursor),
            "savepoints": list(self.savepoints),
            "margins": self.margins,
            "columns": self.columns,
            "lines": self.lines,
        }
        self.prompt_marks.clear()
        self.images.clear()
        self.buffer.clear()
        self.cursor_position()
        self.erase_in_display(2)
        self.dirty.update(range(self.lines))

    def _leave_alt_screen(self) -> None:
        saved = self._alt_saved
        if saved is None:
            return
        old_columns: int = saved["columns"]
        old_lines: int = saved["lines"]
        self.buffer.clear()
        self.buffer.update(saved["buffer"])
        self.cursor = saved["cursor"]
        self.savepoints = saved["savepoints"]
        self.margins = saved["margins"]
        self._alt_saved = None
        self.prompt_marks.clear()
        self.images.clear()
        self.dirty.update(range(self.lines))
        if (old_columns, old_lines) == (self.columns, self.lines):
            return
        # The primary screen was frozen at the size it had when the application
        # switched away from it. If the window was resized meanwhile (a TUI
        # owns the alt screen, so nothing reflowed in between), re-wrap the
        # restored rows to the size the user actually has now.
        result: Optional[ReflowResult] = self._reflow_rows(
            list(self.history.top) + [self.buffer[y] for y in range(old_lines)],
            old_columns,
            self.columns,
            self.lines,
            len(self.history.top) + self.cursor.y,
            self.cursor.x,
        )
        if result is None:
            # Paged or unbounded history: leave the restored rows alone rather
            # than guess; pyte would have clipped them anyway.
            self.dirty.update(range(self.lines))
            return
        self._apply_reflow(result, self.lines, self.columns)
        self.reflow_map = None

    def set_mode(self, *modes: int, **kwargs: Any) -> None:
        super().set_mode(*modes, **kwargs)
        if kwargs.get("private"):
            for mode in modes:
                if mode in ALT_SCREEN_MODES:
                    self._alt_modes_active.add(mode)
                    self._enter_alt_screen()

    def reset_mode(self, *modes: int, **kwargs: Any) -> None:
        super().reset_mode(*modes, **kwargs)
        if kwargs.get("private"):
            for mode in modes:
                if mode in ALT_SCREEN_MODES:
                    self._alt_modes_active.discard(mode)
            # Only leave the alternate screen once *all* alt modes that
            # entered it have been reset (47 / 1047 / 1049 interleave).
            if not self._alt_modes_active:
                self._leave_alt_screen()

    #: The last graphic cluster drawn, for REP (``CSI Ps b``).
    _last_graphic: str = ""

    #: pyte stores a private mode shifted left by 5 bits.
    SYNC_OUTPUT_MODE: int = 2026 << 5

    @property
    def sync_output(self) -> bool:
        """True between ``CSI ? 2026 h`` and ``CSI ? 2026 l``: the program is
        mid-frame, so the view holds back painting until it is complete."""
        return self.SYNC_OUTPUT_MODE in self.mode

    def _full_screen_margins(self) -> bool:
        """True when the scrolling region spans the whole screen."""
        top: int
        bottom: int
        top, bottom = self.margins or pyte_screens.Margins(0, self.lines - 1)
        return top == 0 and bottom == self.lines - 1

    def _tint_blank_rows(self, rows: Iterable[int]) -> None:
        """Give the rows a scroll just opened the cursor's background colour.

        pyte opens a scrolled-in row empty, so it falls back to the default
        cell. xterm fills it with the current background (BCE), which is what
        a full-screen program that sets a background and then scrolls (a
        status band, a coloured pager) relies on. Only the row's *default*
        cell is tinted - the row holds no cells yet - so nothing is stored.
        """
        bg: str = self.cursor.attrs.bg
        if bg == "default":
            return
        blank: Any = self.default_char._replace(bg=bg)
        for y in rows:
            self.buffer[y].default = blank

    def index(self) -> None:
        # While the alternate screen is active, keep the scrollback history
        # frozen; scrolled-out lines simply disappear.
        scrolled: bool = self._full_screen_margins() and self.cursor.y == self.lines - 1
        bottom_margin: int = (self.margins or pyte_screens.Margins(0, self.lines - 1))[
            1
        ]
        at_bottom: bool = self.cursor.y == bottom_margin
        if self._alt_saved is None:
            # pyte appends the scrolled-out row to history.top, a bounded
            # deque that then silently drops its leftmost row -- so every
            # absolute index into it shifts. This is the only point where the
            # pre-append length is observable.
            maxlen: Optional[int] = self.history.top.maxlen
            if scrolled and maxlen is not None and len(self.history.top) >= maxlen:
                self.history_generation += 1
                # The append below drops the oldest row, so every remaining
                # stack row (and the prompt marks recorded there) moves up.
                self._shift_prompt_marks(1)
                self.images.shift(1)
            super().index()
        else:
            pyte_screens.Screen.index(self)
            if scrolled:
                # The alternate screen has no history to grow: every row moves
                # up one, so every placement's stack row does too. Entering the
                # alternate screen already cleared the primary screen's images.
                self.images.shift(1)
        if at_bottom:
            self._tint_blank_rows((bottom_margin,))
        if scrolled:
            self.pending_scroll += 1

    def reverse_index(self) -> None:
        scrolled: bool = self._full_screen_margins() and self.cursor.y == 0
        top_margin: int = (self.margins or pyte_screens.Margins(0, self.lines - 1))[0]
        at_top: bool = self.cursor.y == top_margin
        super().reverse_index()
        if at_top:
            self._tint_blank_rows((top_margin,))
        if scrolled:
            self.pending_scroll -= 1

    def linefeed(self) -> None:
        """Index, recording a DECAWM wrap before the row scrolls away.

        ``draw`` only calls this from inside itself, and only after
        ``carriage_return`` has put the cursor in column 0 - the right margin
        was reached and the line continues on the next row. A linefeed from the
        data stream (``\\n``) carries no such mark, so an exactly-full line that
        ended with a newline stays two logical lines.
        """
        if self._drawing and self.cursor.x == 0:
            row: Any = self.buffer[self.cursor.y]
            row.wrapped = True
        super().linefeed()

    @contextmanager
    def _erasing(self) -> Iterator[None]:
        """Make pyte's erase stamp blanks with the background colour only.

        pyte fills erased cells with the whole of ``cursor.attrs``. A program
        that switched on underline (SGR 4) or strike-through (SGR 9) and then
        cleared a line, or left an OSC 8 link open, therefore got blanks that
        the view paints as decorated - a bare foreground-coloured horizontal
        line across the cleared area. Real terminals keep only the background
        (BCE), so that is all the blank inherits here.
        """
        attrs: Any = self.cursor.attrs
        self.cursor.attrs = self.default_char._replace(bg=attrs.bg)
        try:
            yield
        finally:
            self.cursor.attrs = attrs

    def erase_characters(self, count: Optional[int] = None) -> None:
        self._blank_split_head(self.cursor.y, self.cursor.x)
        with self._erasing():
            super().erase_characters(count)

    def erase_in_display(self, how: int = 0, *args: Any, **kwargs: Any) -> None:
        with self._erasing():
            super().erase_in_display(how, *args, **kwargs)
            # A row a scroll tinted keeps that colour as its default cell, and
            # pyte only rewrites the cells a row holds; the rows erased whole
            # take the erase colour instead.
            if how == 0:
                whole: range = range(self.cursor.y + 1, self.lines)
            elif how == 1:
                whole = range(0, self.cursor.y)
            else:
                whole = range(self.lines)
            blank: Any = self.default_char._replace(bg=self.cursor.attrs.bg)
            for y in whole:
                self.buffer[y].default = blank
        # Blanking cells destroys the text a wrap mark described, and pyte
        # erases in place, so the marks have to be dropped by hand.
        if how == 0:
            removed: range = range(self.cursor.y, self.lines)
        elif how == 1:
            removed = range(0, self.cursor.y + 1)
        else:
            removed = range(self.lines)
        for y in removed:
            row: Any = self.buffer.get(y)
            if row is not None:
                row.wrapped = False

    def erase_in_line(self, how: int = 0, *args: Any, **kwargs: Any) -> None:
        if how == 0:
            self._blank_split_head(self.cursor.y, self.cursor.x)
        with self._erasing():
            super().erase_in_line(how, *args, **kwargs)
        row: Any = self.buffer.get(self.cursor.y)
        if row is not None:
            row.wrapped = False

    def insert_lines(self, count: Optional[int] = None) -> None:
        count = count or 1
        top: int
        bottom: int
        top, bottom = self.margins or pyte_screens.Margins(0, self.lines - 1)
        full: bool = top == 0 and bottom == self.lines - 1 and self.cursor.y == top
        start: int = self.cursor.y
        super().insert_lines(count)
        if top <= start <= bottom:
            self._tint_blank_rows(range(start, min(start + count, bottom + 1)))
        if full:
            self.pending_scroll -= count

    def delete_lines(self, count: Optional[int] = None) -> None:
        count = count or 1
        top: int
        bottom: int
        top, bottom = self.margins or pyte_screens.Margins(0, self.lines - 1)
        full: bool = top == 0 and bottom == self.lines - 1 and self.cursor.y == top
        start = self.cursor.y
        super().delete_lines(count)
        if top <= start <= bottom:
            self._tint_blank_rows(range(max(start, bottom - count + 1), bottom + 1))
        if full:
            self.pending_scroll += count

    def resize(
        self, lines: Optional[int] = None, columns: Optional[int] = None
    ) -> None:
        """Resize the screen, re-wrapping the stack to the new width.

        pyte's own resize clips columns off the right and drops lines off the
        top, which destroys wrapped text for good. Here the retained stack
        (history + visible screen) is rebuilt by re-flowing its logical lines,
        the cursor is put back on the same logical position, and the view is
        handed ``reflow_map`` so it can re-anchor a scrolled-back reader.

        The alternate screen keeps pyte's plain resize: a full-screen
        application owns its layout and expects the terminal to clip, not to
        reinterpret its rows.
        """
        lines = lines or self.lines
        columns = columns or self.columns
        self.reflow_map = None
        if lines == self.lines and columns == self.columns:
            return  # No changes.
        if self._alt_saved is not None:
            super().resize(lines, columns)
            self.prompt_marks.clear()
            return
        result: Optional[ReflowResult] = self._reflow_rows(
            list(self.history.top) + [self.buffer[y] for y in range(self.lines)],
            self.columns,
            columns,
            lines,
            len(self.history.top) + self.cursor.y,
            self.cursor.x,
        )
        if result is None:
            super().resize(lines, columns)
            self.prompt_marks.clear()
            return
        self._apply_reflow(result, lines, columns)
        self.reflow_map = result

    def _reflow_rows(
        self,
        rows: Sequence[Any],
        old_columns: int,
        new_columns: int,
        new_lines: int,
        cursor_row: int,
        cursor_column: int,
    ) -> Optional[ReflowResult]:
        """Re-wrap *rows* to the new width, or None when that is not safe.

        ``history.bottom`` is only non-empty while the screen is paged back
        into the past (pyte's ``prev_page``), and an unbounded deque has no
        ``maxlen`` for the bound. Neither happens in this terminal today, but
        guessing there would scramble the stack, so fall back to pyte's own
        resize instead.
        """
        if self.history.bottom or self.history.top.maxlen is None:
            return None
        return reflow(
            rows,
            old_columns,
            new_columns,
            new_lines,
            cursor_row,
            cursor_column,
            self.default_char,
            self.history.top.maxlen,
            self._row_from_cells,
        )

    def _apply_reflow(self, result: ReflowResult, lines: int, columns: int) -> None:
        """Install a reflow result as the new history, screen and cursor."""
        maxlen: Optional[int] = self.history.top.maxlen
        top: Deque[Any] = deque(result.history, maxlen=maxlen)
        self.history = self.history._replace(
            top=top,
            bottom=deque(maxlen=self.history.bottom.maxlen),
            position=self.history.size,
        )
        for y in range(lines):
            self.buffer[y] = result.screen[y]
        for y in [key for key in self.buffer if key >= lines]:
            del self.buffer[y]
        self.lines = lines
        self.columns = columns
        self.set_margins()
        # pyte's Cursor is a plain mutable object, not a NamedTuple.
        cursor: Any = self.cursor
        cursor.x = result.cursor_col
        cursor.y = result.cursor_row
        self.dirty.update(range(lines))
        self._remap_prompt_marks(result)
        self.images.remap(result)

    def _row_from_cells(self, cells: Sequence[Any], wrapped: bool) -> _TerminalRow:
        """Build a sparse row from reflow's padded cell list.

        Padding cells are the default char, which a sparse row already yields
        for a missing column, so they are not stored: a full scrollback of
        dense rows would cost an order of magnitude more memory.
        """
        default: Any = self.default_char
        row: _TerminalRow = _TerminalRow(default)
        for x, cell in enumerate(cells):
            # A hyperlink makes a cell part of the text even when its
            # attributes equal the default char (a linked space), so it is
            # kept rather than dropped as padding.
            if cell != default or getattr(cell, "hyperlink", None):
                row[x] = cell
        row.wrapped = wrapped
        return row

    def _remap_prompt_marks(self, result: ReflowResult) -> None:
        """Move OSC 133 marks onto the re-wrapped stack.

        A mark is a single position, so the same map that moves the cursor
        moves it. Marks whose row fell out of the retained stack are dropped.
        """
        if not self.prompt_marks:
            return
        remapped: List[PromptMark] = []
        for row, column, kind, exit_code in self.prompt_marks:
            position: Optional[Tuple[int, int]] = result.map_position(row, column)
            if position is None:
                continue
            remapped.append((position[0], position[1], kind, exit_code))
        self.prompt_marks = remapped[: self.MAX_PROMPT_MARKS]

    # ------------------------------------------------------------------
    # Mouse tracking / bracketed paste mode helpers
    # ------------------------------------------------------------------

    def _mode_is(self, mode: int) -> bool:
        return (mode << 5) in self.mode

    @property
    def mouse_mode(self) -> int:
        """0 = off, 1 = button (1000), 2 = drag (1002), 3 = move (1003)."""
        if self._mode_is(MOUSE_MOVE_MODE):
            return 3
        if self._mode_is(MOUSE_DRAG_MODE):
            return 2
        if self._mode_is(MOUSE_BUTTON_MODE):
            return 1
        return 0

    @property
    def sgr_mouse(self) -> bool:
        return self._mode_is(MOUSE_SGR_MODE)

    @property
    def bracketed_paste(self) -> bool:
        return self._mode_is(BRACKETED_PASTE_MODE)

    @property
    def focus_report(self) -> bool:
        return self._mode_is(FOCUS_REPORT_MODE)

    # ------------------------------------------------------------------
    # OSC (title / icon / cwd / hyperlink)
    # ------------------------------------------------------------------

    def osc(self, code: str, param: str) -> None:
        # Tuple membership, not substring checks: an empty or unrelated
        # code (e.g. "") must not trigger icon/title changes.
        if code in ("0", "1", "01"):
            self.set_icon_name(param)
        if code in ("0", "2", "02"):
            self.set_title(param)
        if code == "7":
            # OSC 7 - set the current working directory. An empty parameter
            # does not carry a location; keep the previous cwd.
            if param:
                self.cwd = param
        if code == "8":
            # OSC 8 - hyperlink: "params;uri". An empty URI terminates the
            # active link. The URI is stamped onto the cells drawn while it is
            # open (see draw/_Cell), so it is not kept as a separate span.
            parts = param.split(";", 1)
            if len(parts) == 2:
                params, uri = parts
                self._active_hyperlink = uri or None
            else:
                self._active_hyperlink = None
            # Keep the erase/insert attribute template in step immediately: a
            # link that closes must not be re-stamped onto the blanks of the
            # next \x1b[K.
            self._sync_hyperlink_attrs()
        if code == "133":
            # OSC 133 - shell-integration marks: "A", "B", "C",
            # "D;<exit-code>", optionally followed by additional fields the
            # shell may append (xterm-style "D;0;..."). Only the first field
            # of each is needed here.
            self._osc_prompt_mark(param)
        if code == "4":
            # OSC 4 - palette slot: "index;spec[;index;spec...]". A "?" spec
            # is a query and is answered through the PTY.
            self._osc_palette(param)
        elif code in ("10", "11", "12"):
            # OSC 10/11/12 - default foreground, background, cursor colour.
            self._osc_default_colour(int(code), param)
        elif code == "104":
            # OSC 104 - reset one palette slot, a list of them, or all.
            self._osc_reset_palette(param)
        elif code in ("110", "111", "112"):
            # OSC 110/111/112 - reset the 10/11/12 default back to the theme.
            self._osc_reset_default(int(code) - 100)
        elif code in ("9", "777"):
            # OSC 9 / 777 - desktop notification (display only, never grid).
            self._osc_notification(code, param)
        elif code == "52":
            # OSC 52 - read or write the system clipboard.
            self._osc_clipboard(param)

    # ------------------------------------------------------------------
    # OSC 133 shell-integration marks
    # ------------------------------------------------------------------

    # Maximum retained marks. A prompt records four per command, and the list
    # only has to cover the retained scrollback, so this keeps it bounded even
    # when a shell emits a mark per prompt line for a very long session.
    MAX_PROMPT_MARKS: int = 4000

    def _osc_prompt_mark(self, param: str) -> None:
        """Record an OSC 133 prompt/command/output mark.

        The payload's first field selects the kind (``A`` prompt start,
        ``B`` command start, ``C`` output start, ``D`` command end); a ``D``
        may carry the exit code as its second field. Anything else is ignored,
        so a shell that does not emit OSC 133 - or a malformed payload - leaves
        no state behind and every navigation surface stays inert.

        Marks use stack coordinates (history rows below the live screen plus
        the viewport row), so they keep pointing at their line when the bounded
        history deque drops rows. The alternate screen has no scrollback and is
        cleared on both transitions, so a mark arriving there is discarded
        rather than left pointing into a buffer that is about to disappear.
        """
        if self.in_alt_screen:
            return
        parts: List[str] = param.split(";")
        kind: str = parts[0].strip()
        if kind not in ("A", "B", "C", "D"):
            return
        exit_code: Optional[int] = None
        if kind == "D" and len(parts) > 1:
            try:
                exit_code = int(parts[1].strip())
            except ValueError:
                exit_code = None
        row: int = len(self.history.top) + self.cursor.y
        self.prompt_marks.append((row, self.cursor.x, kind, exit_code))
        if len(self.prompt_marks) > self.MAX_PROMPT_MARKS:
            del self.prompt_marks[: len(self.prompt_marks) - self.MAX_PROMPT_MARKS]

    def _shift_prompt_marks(self, rows: int) -> None:
        """Move every recorded mark up by *rows* dropped history rows."""
        marks: Optional[List[PromptMark]] = getattr(self, "prompt_marks", None)
        if not marks or rows <= 0:
            return
        shifted: List[PromptMark] = []
        for row, column, kind, exit_code in marks:
            row -= rows
            if row < 0:
                continue
            shifted.append((row, column, kind, exit_code))
        self.prompt_marks = shifted

    # ------------------------------------------------------------------
    # OSC 9 / 777 notifications and OSC 52 clipboard
    # ------------------------------------------------------------------

    def _osc_notification(self, code: str, param: str) -> None:
        """Surface an OSC 9 / 777 desktop notification.

        Both protocols are parse-only here: the payload is reduced to a title
        and a body and handed to ``notification_handler``, which is installed
        only when ``notifications_enabled`` is set (the
        ``terminal-notifications`` setting, off by default). Nothing is ever
        drawn into the grid, so a malformed payload leaves no trace.
        """
        if not self.notifications_enabled or self.notification_handler is None:
            return
        title: str = ""
        body: str = ""
        if code == "777":
            # rxvt-unicode: 777;notify;<title>;<body>. Any other 777
            # subcommand (precmd/preexec) is a shell hook, not a message.
            parts: List[str] = param.split(";", 2)
            if len(parts) < 3 or parts[0] != "notify":
                return
            title, body = parts[1], parts[2]
        else:
            # OSC 9:<message> (Windows Terminal / ConEmu). OSC 9;4 is
            # ConEmu's progress report, not a notification.
            if param.startswith("4;"):
                return
            body = param
        title = self._one_line(title, MAX_NOTIFICATION_TITLE)
        body = self._one_line(body, MAX_NOTIFICATION_BODY)
        if not title and not body:
            return
        self.notification_handler(title, body)

    @staticmethod
    def _one_line(text: str, limit: int) -> str:
        """Collapse a notification payload to one bounded, control-free line."""
        printable: str = "".join(
            char for char in text if not (ord(char) < 32 or 0x7F <= ord(char) < 0xA0)
        )
        return " ".join(printable.split())[:limit]

    def _osc_clipboard(self, param: str) -> None:
        """Handle OSC 52: read or write the system clipboard.

        ``52;<targets>;<base64>`` sets the clipboard; a payload of ``?`` asks
        for its contents and is answered through the PTY. Only the ``c``
        (system clipboard) target is honoured, because this terminal has no
        primary selection of its own and answering for one would lie.

        The two directions are gated separately because they are different
        risks: a write is what remote tmux/ssh workflows need, while a read
        lets a confined TUI exfiltrate whatever the user copied last.
        """
        parts: List[str] = param.split(";", 1)
        if len(parts) != 2:
            return
        targets: str
        payload: str
        targets, payload = parts
        if targets and "c" not in targets:
            return
        payload = payload.strip()
        if payload == "?":
            if not self.clipboard_read_enabled or self.clipboard_read is None:
                return
            text: Optional[str] = self.clipboard_read()
            if text is None:
                return
            encoded: str = base64.b64encode(text.encode("utf-8")).decode("ascii")
            self._answer_osc("52;c;{}".format(encoded))
            return
        if not self.clipboard_write_enabled or self.clipboard_write is None:
            return
        if not payload:
            # An empty payload would wipe the user's clipboard from a remote
            # sequence; keep it instead of silently clearing it.
            return
        try:
            raw: bytes = base64.b64decode(payload, validate=True)
        except (binascii.Error, ValueError):
            return
        if len(raw) > MAX_OSC52_BYTES:
            return
        self.clipboard_write(raw.decode("utf-8", "replace"))

    # ------------------------------------------------------------------
    # OSC 4 / 10 / 11 / 12 palette
    # ------------------------------------------------------------------

    def set_render_colours(
        self, table: Dict[str, str], default_fg: str, default_bg: str
    ) -> None:
        """Record the colours the view actually paints.

        Called by the view whenever the theme or font style is (re)loaded. An
        OSC query is answered from here, so an application that asks "what is
        palette index 1?" gets the colour on screen rather than a second
        palette of the emulator's own that the user never sees.
        """
        self.render_colours = dict(table)
        self.render_default_fg = default_fg
        self.render_default_bg = default_bg

    @staticmethod
    def _palette_tokens(index: int) -> Tuple[str, ...]:
        """Cell-colour tokens a palette index paints with.

        pyte names an SGR 30-37 / 90-97 colour in a cell ("brightred") but
        stores the ``38;5;<n>`` / ``48;5;<n>`` form as a bare hex string from
        its own 256-colour table, even for ``n`` below 16 - so the same palette
        slot reaches the paint pass under two different tokens and an override
        has to be written under both. Index 13 has two names because pyte's
        background table misspells bright magenta as "bfightmagenta".

        A cell carries no index, only the resolved token, so the two entries
        that share a colour in pyte's table are indistinguishable: ``38;5;16``
        is ``000000``, exactly like slot 0. A repaint of either moves both.
        """
        tokens: List[str] = []
        if 0 <= index < len(PALETTE_NAMES):
            tokens.extend(PALETTE_NAMES[index])
        if 0 <= index < len(pyte_graphics.FG_BG_256):
            hex_token: str = pyte_graphics.FG_BG_256[index]
            if hex_token not in tokens:
                tokens.append(hex_token)
        return tuple(tokens)

    def _palette_colour(self, index: int) -> Optional[str]:
        """Effective ``#rrggbb`` for a palette index, override first."""
        tokens: Tuple[str, ...] = self._palette_tokens(index)
        for token in tokens:
            override: Optional[str] = self.palette_overrides.get(token)
            if override is not None:
                return override
        for token in tokens:
            rendered: Optional[str] = self.render_colours.get(token)
            if rendered is not None:
                return rendered
        return None

    def _set_palette_index(self, index: int, colour: str) -> None:
        tokens: Tuple[str, ...] = self._palette_tokens(index)
        if not tokens:
            # An index pyte's table does not describe cannot be painted;
            # accept it quietly instead of failing the whole sequence.
            return
        for token in tokens:
            self.palette_overrides[token] = colour
        self.palette_version += 1

    def _reset_palette_index(self, index: int) -> None:
        changed: bool = False
        for token in self._palette_tokens(index):
            if token in self.palette_overrides:
                del self.palette_overrides[token]
                changed = True
        if changed:
            self.palette_version += 1

    def _osc_palette(self, param: str) -> None:
        parts: List[str] = param.split(";")
        position: int = 0
        while position + 1 < len(parts):
            index_text: str = parts[position].strip()
            spec: str = parts[position + 1].strip()
            position += 2
            try:
                index: int = int(index_text)
            except ValueError:
                continue
            if spec == "?":
                colour: Optional[str] = self._palette_colour(index)
                if colour is not None:
                    self._answer_osc("4;{};{}".format(index, colour_spec(colour)))
                continue
            parsed: Optional[str] = parse_colour_spec(spec)
            if parsed is not None:
                self._set_palette_index(index, parsed)

    _DEFAULT_COLOUR_ATTRS: Dict[int, str] = {
        10: "default_fg_override",
        11: "default_bg_override",
        12: "cursor_colour_override",
    }

    def _osc_default_colour(self, which: int, param: str) -> None:
        attribute: str = self._DEFAULT_COLOUR_ATTRS[which]
        spec: str = param.strip()
        if spec == "?":
            current: Optional[str] = getattr(self, attribute)
            if current is None:
                # xterm answers an unset cursor colour with the text
                # foreground, which is what the cursor is drawn in.
                current = (
                    self.render_default_bg if which == 11 else self.render_default_fg
                )
            self._answer_osc("{};{}".format(which, colour_spec(current)))
            return
        parsed: Optional[str] = parse_colour_spec(spec)
        if parsed is None:
            return
        setattr(self, attribute, parsed)
        self.palette_version += 1

    def _osc_reset_palette(self, param: str) -> None:
        text: str = param.strip()
        if not text:
            if self.palette_overrides:
                self.palette_overrides.clear()
                self.palette_version += 1
            return
        for token in text.split(";"):
            token = token.strip()
            if not token:
                continue
            try:
                self._reset_palette_index(int(token))
            except ValueError:
                continue

    def _osc_reset_default(self, which: int) -> None:
        attribute: str = self._DEFAULT_COLOUR_ATTRS[which]
        if getattr(self, attribute) is not None:
            setattr(self, attribute, None)
            self.palette_version += 1

    def _answer_osc(self, payload: str) -> None:
        """Write an OSC reply back to the application through the PTY."""
        if self.respond is not None:
            self.respond("\x1b]{}\x1b\\".format(payload))

    def clear_scrollback(self) -> None:
        """Drop the saved history, keeping the visible screen (CSI 3 J).

        pyte's own ``erase_in_display(3)`` also blanks the display, which is
        not what a "clear scrollback" command should do, so only the history
        funnel runs here. It bumps ``history_generation`` and drops the
        stack-coordinate marks, exactly as the CSI form does.
        """
        self._reset_history()

    # ------------------------------------------------------------------
    # Inline images (Kitty graphics / sixel)
    # ------------------------------------------------------------------

    def set_cell_metrics(self, width: float, height: float) -> None:
        """Record the renderer's cell size for pixel -> cell conversion."""
        self.images.set_cell_metrics(width, height)

    def _image_row(self) -> int:
        """Stack row of the cursor, where an inline image is anchored."""
        return len(self.history.top) + self.cursor.y

    def apc(self, payload: str) -> None:
        """Handle one APC payload (Kitty graphics) captured by the stream."""
        before: int = self.images.version
        response, placement = self.images.kitty_apc(
            payload, self._image_row(), self.cursor.x
        )
        if self.images.version != before:
            self.dirty.update(range(self.lines))
        if placement is not None and placement.cursor_policy != 1:
            self._advance_after_image(self.cursor.y, placement.rows)
        if response is not None and self.respond is not None:
            self.respond(response)

    def dcs(self, payload: str) -> None:
        """Handle one DCS payload; only sixel graphics leave a placement."""
        before: int = self.images.version
        placement: Optional[Placement] = self.images.sixel_dcs(
            payload, self._image_row(), self.cursor.x
        )
        if placement is not None:
            self.dirty.update(range(self.lines))
            self._advance_after_image(self.cursor.y, placement.rows)
        elif self.images.version != before:
            self.dirty.update(range(self.lines))

    def _advance_after_image(self, start_y: int, rows: int) -> None:
        """Move the cursor below an image, scrolling when it reaches the end.

        Sixel and Kitty ``C=0`` placements reserve their cell rows the way the
        text they replace would: the cursor ends at column 0 of the row after
        the image. Scrolling here is safe for the placement's anchor - a row
        moving into history and a stack row moving up cancel out exactly, and
        an overflowing deque shifts the store with the spans.
        """
        if rows <= 0:
            return
        target: int = start_y + rows
        if target >= self.lines:
            self.cursor.y = self.lines - 1
            self.cursor.x = 0
            for _ in range(target - self.lines + 1):
                self.index()
            target = self.lines - 1
        self.cursor.y = max(0, target)
        self.cursor.x = 0

    def _sync_hyperlink_attrs(self) -> None:
        """Keep ``cursor.attrs.hyperlink`` equal to the active OSC 8 URI.

        pyte stamps every cell it writes with ``cursor.attrs``, including the
        blanks from an erase or an insert, so the URI has to live there too and
        not only on the cells this screen draws itself. It also has to be
        removed the moment the link closes, or erasing a linked line would
        re-stamp the link onto the blanks.

        The attribute is left as pyte's own ``Char`` whenever no link is open:
        a ``_Cell`` carries the space for an instance ``__dict__``, and the
        whole screen (and scrollback) is stamped from here, so an idle
        ``_Cell`` would cost every cell a few bytes for nothing.
        """
        attrs: Any = self.cursor.attrs
        if self._active_hyperlink is None:
            if isinstance(attrs, _Cell):
                if not attrs.faint:
                    self.cursor.attrs = pyte_screens.Char(*attrs)
                elif attrs.hyperlink is not None:
                    # Faint keeps the cell type, but the link has ended.
                    self.cursor.attrs = attrs._replace(hyperlink=None)
            return
        if not isinstance(attrs, _Cell):
            attrs = _Cell(*attrs)
        if attrs.hyperlink != self._active_hyperlink:
            attrs = attrs._replace(hyperlink=self._active_hyperlink)
        self.cursor.attrs = attrs

    def select_graphic_rendition(self, *attrs: int) -> None:
        """pyte's SGR plus faint (2), which pyte has no field for.

        The parameters are walked in order, skipping the arguments of an
        extended colour (``38;5;n`` / ``38;2;r;g;b``), so the ``2`` of a
        truecolour sequence is not taken for "faint". 0 and 22 clear it.
        """
        faint: bool = bool(getattr(self.cursor.attrs, "faint", False))
        params: Tuple[int, ...] = attrs or (0,)
        index: int = 0
        while index < len(params):
            value: int = params[index]
            if value in (38, 48) and index + 1 < len(params):
                index += 3 if params[index + 1] == 5 else 5
                continue
            if value == 2:
                faint = True
            elif value in (0, 22):
                faint = False
            index += 1
        super().select_graphic_rendition(*attrs)
        current: Any = self.cursor.attrs
        if faint != bool(getattr(current, "faint", False)):
            if not isinstance(current, _Cell):
                current = _Cell(*current)
            self.cursor.attrs = current._replace(faint=faint)
            if not faint:
                self._sync_hyperlink_attrs()

    def draw(self, data: str) -> None:
        self._drawing = True
        try:
            # Stamp the active OSC 8 URI onto the cursor attributes, so every
            # cell written by this chunk carries it.
            self._sync_hyperlink_attrs()
            self._draw_clusters(data)
        finally:
            self._drawing = False

    @property
    def display(self) -> List[str]:
        """The screen as text lines, skipping a two-cell glyph's stub.

        pyte's own renderer decides "wide" from ``wcwidth()`` of the first
        codepoint, so an emoji cluster (a VS16 heart is ``wcwidth()`` 1) leaves
        its stub to be rendered as a cell - and a stub has no first codepoint,
        which raised IndexError. The width has to come from the cluster.
        """
        rows: List[str] = []
        for y in range(self.lines):
            line = self.buffer[y]
            text: List[str] = []
            x: int = 0
            while x < self.columns:
                data: str = line[x].data
                text.append(data)
                x += 2 if cluster_width(data) == 2 else 1
            rows.append("".join(text))
        return rows

    def _blank_split_head(self, y: int, x: int) -> None:
        """If column *x* of row *y* is the trailing stub of a wide glyph and
        is about to be overwritten or erased, blank the glyph's head too.

        Left alone, the head keeps its two-cell glyph, which the view then
        draws across the cell that replaced the stub (a wide pair with an
        ``x`` typed over the stub of the first showed as a glyph under it).
        """
        if x <= 0 or x >= self.columns:
            return
        line: Any = self.buffer[y]
        stub: Any = line.get(x)
        head: Any = line.get(x - 1)
        if stub is not None and stub.data == "" and head is not None:
            line[x - 1] = head._replace(data=" ")

    def _draw_clusters(self, data: str) -> None:
        """Draw a chunk one grapheme cluster at a time.

        A single-codepoint cluster goes straight to pyte's ``draw()``: that is
        the path every existing test exercises, including pyte's own NFC
        folding of a composable combining mark. Only a multi-codepoint cluster
        needs the custom path, because pyte cannot store more than one
        codepoint per cell (except by NFC folding) and *breaks out of the
        whole chunk* on a zero-width codepoint it cannot combine.
        """
        for cluster in iter_clusters(data):
            if len(cluster) == 1 and not (
                is_combining(cluster) and cluster_width(cluster) == 0
            ):
                if self.cursor.x < self.columns and cluster_width(cluster) > 0:
                    self._blank_split_head(self.cursor.y, self.cursor.x)
                super().draw(cluster)
                if cluster.isprintable():
                    self._last_graphic = cluster
                continue
            width: int = cluster_width(cluster)
            if width < 0:
                # pyte stops drawing the rest of the chunk at an unprintable
                # codepoint; keep that, rather than skipping just this unit.
                return
            if self.cursor.x < self.columns and width > 0:
                self._blank_split_head(self.cursor.y, self.cursor.x)
            self._draw_cluster(cluster, width)
            if width > 0:
                self._last_graphic = cluster

    def repeat_character(self, count: Optional[int] = None) -> None:
        """REP (``CSI Ps b``): draw the last graphic character *count* more
        times. ncurses emits it for long runs of one character, so ignoring it
        drops those characters. The count is capped at one screenful: a
        hostile or corrupt value must not stall the GUI thread."""
        if not self._last_graphic:
            return
        times: int = min(count or 1, self.columns * self.lines)
        self._draw_clusters(self._last_graphic * times)

    def cursor_forward_tab(self, count: Optional[int] = None) -> None:
        """CHT (``CSI Ps I``): move forward *count* tab stops."""
        for _ in range(count or 1):
            self.tab()

    def cursor_back_tab(self, count: Optional[int] = None) -> None:
        """CBT (``CSI Ps Z``): move back *count* tab stops (to column 0 at
        the left edge)."""
        if self.cursor.x == self.columns:
            self.cursor.x -= 1
        for _ in range(count or 1):
            stops: List[int] = [stop for stop in self.tabstops if stop < self.cursor.x]
            self.cursor.x = max(stops) if stops else 0

    def _draw_cluster(self, cluster: str, width: int) -> None:
        """Store one multi-codepoint cluster in a single cell.

        Mirrors pyte's ``Screen.draw()`` cursor handling (DECAWM wrap, IRM
        insert, the two-cell stub) but writes the whole cluster as one cell's
        data. A zero-width cluster is appended to the previous cell, exactly
        as pyte appends a combining mark it could not fold.
        """
        if self.cursor.x == self.columns:
            if pyte_modes.DECAWM in self.mode:
                self.dirty.add(self.cursor.y)
                self.carriage_return()
                self.linefeed()
            elif width > 0:
                self.cursor.x -= width
        if pyte_modes.IRM in self.mode and width > 0:
            self.insert_characters(width)
        line = self.buffer[self.cursor.y]
        if width == 0:
            if self.cursor.x:
                previous_cell = line[self.cursor.x - 1]
                line[self.cursor.x - 1] = previous_cell._replace(
                    data=unicodedata.normalize("NFC", previous_cell.data + cluster)
                )
            elif self.cursor.y:
                previous_line = self.buffer[self.cursor.y - 1]
                previous_cell = previous_line[self.columns - 1]
                previous_line[self.columns - 1] = previous_cell._replace(
                    data=unicodedata.normalize("NFC", previous_cell.data + cluster)
                )
        else:
            line[self.cursor.x] = self.cursor.attrs._replace(
                data=unicodedata.normalize("NFC", cluster)
            )
            if width == 2 and self.cursor.x + 1 < self.columns:
                # pyte's two-cell stub: the renderer and the selection path
                # treat it as part of this glyph, never as whitespace.
                line[self.cursor.x + 1] = self.cursor.attrs._replace(data="")
            self.cursor.x = min(self.cursor.x + width, self.columns)
        self.dirty.add(self.cursor.y)

    # ------------------------------------------------------------------
    # DECSCUSR cursor style
    # ------------------------------------------------------------------

    def set_cursor_style(self, *params: int, **kwargs: Any) -> None:
        ps: int = params[0] if params else 0
        if ps in (0, 1, 2):
            self.cursor_style = "block"
        elif ps in (3, 4):
            self.cursor_style = "underline"
        elif ps in (5, 6):
            self.cursor_style = "bar"
        else:
            self.cursor_style = "block"
        # Odd values blink, even values are steady (0 = blinking block).
        self.cursor_blink = (ps % 2 == 1) or ps == 0

    # ------------------------------------------------------------------
    # Bell
    # ------------------------------------------------------------------

    def bell(self, *args: Any) -> None:
        self.bell_triggered = True

    def _reset_history(self) -> None:
        # The single funnel for an emptied scrollback: both reset() and
        # erase_in_display(3) reach it, and every stored history index is
        # invalid afterwards. Prompt marks are stack-coordinate based, so they
        # point at text that no longer exists; hyperlinks live on the cells and
        # go with them.
        self.history_generation += 1
        if hasattr(self, "prompt_marks"):
            self.prompt_marks.clear()
        if hasattr(self, "images"):
            self.images.clear()
        super()._reset_history()

    def reset(self) -> None:
        self.keyboard_flags = 0
        self._alt_saved = None
        self._alt_modes_active = set()
        self._drawing = False
        self.reflow_map = None
        self.cursor_style = "block"
        self.cursor_blink = True
        self.bell_triggered = False
        if hasattr(self, "prompt_marks"):
            self.prompt_marks.clear()
        if hasattr(self, "images"):
            self.images.clear()
        self._active_hyperlink = None
        self.pending_scroll = 0
        # RIS resets the palette too: an application that repainted slots or
        # the defaults must not leave them behind for the next program.
        if self.palette_overrides or (
            self.default_fg_override is not None
            or self.default_bg_override is not None
            or self.cursor_colour_override is not None
        ):
            self.palette_overrides.clear()
            self.default_fg_override = None
            self.default_bg_override = None
            self.cursor_colour_override = None
            self.palette_version += 1
        super().reset()
        # pyte starts with G1 on the DEC special graphics set, which is why a
        # stray SO used to be ignored in UTF-8 mode. SO/SI are honoured now,
        # so G1 starts as ASCII (as in xterm) and only an explicit designation
        # (ESC ) 0) turns it into line drawing.
        self.g1_charset = pyte_charsets.LAT1_MAP
        # The last graphic cluster drawn, for REP (CSI Ps b).
        self._last_graphic = ""
        # pyte's reset() keeps the buffer's factory, so it has to be installed
        # here too: a RIS mid-session must not leave pyte's plain rows behind.
        buffer: Any = self.buffer
        buffer.default_factory = self._new_row

    def _new_row(self) -> _TerminalRow:
        """Buffer row factory: pyte's sparse row plus its wrap mark."""
        return _TerminalRow(self.default_char)


class ExtendedStream(pyte_streams.Stream):
    """
    pyte Stream with extra protocol support: DECSCUSR, OSC 7/8 and the
    Kitty keyboard protocol.

    The parser FSM is copied from pyte 0.8.2 (LGPL, see pyte license) with
    five additions:
      - the OSC branch dispatches to ``screen.osc(code, param)`` so OSC 7
        (cwd) and OSC 8 (hyperlinks) are surfaced;
      - a parameterless CSI ``s`` / CSI ``u`` is dispatched to
        ``screen.save_cursor`` / ``screen.restore_cursor`` (SCOSC / SCORC);
      - a CSI ``... SP q`` sequence (DECSCUSR) is dispatched to
        ``screen.set_cursor_style``;
      - the Kitty keyboard protocol sequences ``CSI > flags u``,
        ``CSI < flags u`` and ``CSI ? u`` set ``screen.keyboard_flags``
        and answer the query via ``respond``;
      - APC and DCS payloads are captured and dispatched to ``screen.apc``
        (Kitty graphics) and ``screen.dcs`` (sixel) instead of only being
        swallowed.

    The CSI table also maps REP (``b``), CHT (``I``) and CBT (``Z``), which
    pyte leaves out.
    """

    csi: Dict[str, str] = {
        **pyte_streams.Stream.csi,
        "b": "repeat_character",
        "I": "cursor_forward_tab",
        "Z": "cursor_back_tab",
    }

    def __init__(self, listener: Any) -> None:
        super().__init__(listener)
        # Optional callback writing terminal-initiated responses (e.g. the
        # Kitty keyboard protocol query reply) back to the PTY.
        self.respond: Optional[Callable[[str], None]] = None

    def feed(self, data: str) -> None:
        screen: Any = self.listener
        if screen is not None:
            screen.pending_scroll = 0
        super().feed(data)

    def _parser_fsm(self) -> Generator[Optional[bool], str, None]:
        basic: Any = self.basic
        assert self.listener is not None
        listener: Any = self.listener
        draw: Any = listener.draw
        debug: Any = listener.debug

        ESC: str = pyte.control.ESC
        CSI_C1: str = pyte.control.CSI_C1
        OSC_C1: str = pyte.control.OSC_C1
        SP_OR_GT: str = pyte.control.SP + ">"
        NUL_OR_DEL: str = pyte.control.NUL + pyte.control.DEL
        CAN_OR_SUB: str = pyte.control.CAN + pyte.control.SUB
        ALLOWED_IN_CSI: str = "".join(
            [
                pyte.control.BEL,
                pyte.control.BS,
                pyte.control.HT,
                pyte.control.LF,
                pyte.control.VT,
                pyte.control.FF,
                pyte.control.CR,
            ]
        )
        OSC_TERMINATORS: Set[str] = set(
            [pyte.control.ST_C0, pyte.control.ST_C1, pyte.control.BEL]
        )

        def create_dispatcher(mapping: Any) -> Any:
            return __import__("collections").defaultdict(
                lambda: debug,
                dict(
                    (event, getattr(listener, attr)) for event, attr in mapping.items()
                ),
            )

        basic_dispatch: Any = create_dispatcher(basic)
        sharp_dispatch: Any = create_dispatcher(self.sharp)
        escape_dispatch: Any = create_dispatcher(self.escape)
        csi_dispatch: Any = create_dispatcher(self.csi)

        while True:
            char: str = yield True

            if char == ESC:
                char = yield None
                if char == "[":
                    char = CSI_C1
                elif char == "]":
                    char = OSC_C1
                else:
                    if char == "#":
                        sharp_dispatch[(yield None)]()
                    elif char == "%":
                        self.select_other_charset((yield None))
                    elif char in "()":
                        code = yield None
                        # xterm honours the DEC special graphics ("0") and
                        # ASCII ("B") designations in UTF-8 mode too, and
                        # ncurses programs rely on it for their line
                        # drawing. The national and IBM PC maps would corrupt
                        # real UTF-8 text, so they stay ignored there.
                        if self.use_utf8 and code not in "0B":
                            continue
                        listener.define_charset(code, mode=char)
                    elif char in "PX^_":
                        # DCS / SOS / PM / APC: capture the payload until ST
                        # (ESC \), BEL or C1 ST. Without this the payload is
                        # drawn as visible text (e.g. DCS "+q" session ids).
                        # APC carries the Kitty graphics protocol and DCS
                        # carries sixel; both are dispatched to the screen.
                        #
                        # A bytearray, not a list of one-character strings:
                        # the FSM is fed one character at a time, so a list
                        # would cost ~50 bytes per payload byte and a multi-MB
                        # image would balloon the process. The cap stops a
                        # runaway producer from buffering forever; the
                        # sequence is still consumed to its terminator so the
                        # parser stays in sync.
                        introducer: str = char
                        payload: bytearray = bytearray()
                        cancelled: bool = False
                        too_large: bool = False
                        while True:
                            nxt = yield None
                            if nxt == ESC:
                                nxt2 = yield None
                                if nxt2 == "\\":
                                    break
                                chunk = nxt + nxt2
                            elif nxt in (
                                pyte.control.BEL,
                                pyte.control.ST_C1,
                            ):
                                break
                            elif nxt in (pyte.control.CAN, pyte.control.SUB):
                                cancelled = True
                                break
                            else:
                                chunk = nxt
                            if too_large:
                                continue
                            if len(payload) + len(chunk) > MAX_ESCAPE_PAYLOAD:
                                too_large = True
                                payload = bytearray()
                                continue
                            for captured in chunk:
                                codepoint = ord(captured)
                                if codepoint < 0x80:
                                    payload.append(codepoint)
                                else:
                                    payload.extend(captured.encode("utf-8", "replace"))
                        if not cancelled and not too_large:
                            text: str = payload.decode("utf-8", "replace")
                            if introducer == "_":
                                listener.apc(text)
                            elif introducer == "P":
                                listener.dcs(text)
                    else:
                        escape_dispatch[char]()
                    continue

            if char in basic:
                basic_dispatch[char]()
            elif char == CSI_C1:
                params: List[int] = []
                current: str = ""
                # Colon-separated sub-parameters (ITU T.416), keyed by the
                # index of the parameter they belong to: "38:2::255:0:0".
                groups: Dict[int, List[str]] = {}
                private: bool = False
                while True:
                    char = yield None
                    if char == "?":
                        private = True
                    elif char in ALLOWED_IN_CSI:
                        basic_dispatch[char]()
                    elif char in SP_OR_GT:
                        if char == " ":
                            # DECSCUSR: CSI Ps SP q / CSI ? Ps SP q
                            nxt = yield None
                            if nxt == "q":
                                if current:
                                    params.append(min(int(current), 9999))
                                listener.set_cursor_style(*params, private=private)
                        else:
                            # '>' starts the Kitty keyboard protocol push or
                            # a private query (XTVERSION, DECRQM, ...).
                            # Consume digits and semicolons, then react to
                            # 'u' or swallow the rest so nothing is drawn as
                            # visible text.
                            flags: str = ""
                            nxt = ""
                            while True:
                                nxt = yield None
                                if nxt.isdigit() or nxt == ";":
                                    flags += nxt
                                    continue
                                break
                            if nxt == "u":
                                current_flags: str = (flags.split(";") or [""])[-1]
                                listener.keyboard_flags = int(current_flags or "1")
                        break
                    elif char == "<":
                        # '<' pops the Kitty keyboard protocol.
                        nxt = yield None
                        while nxt.isdigit() or nxt == ";":
                            nxt = yield None
                        if nxt == "u":
                            listener.keyboard_flags = 0
                        break
                    elif char in CAN_OR_SUB:
                        draw(char)
                        break
                    elif char.isdigit():
                        current += char
                    elif char == ":":
                        # A sub-parameter separator is not a final byte: the
                        # sequence goes on, and the digits that follow belong
                        # to it (otherwise "4:3m" ended at ':' and "3m" was
                        # drawn as text).
                        groups.setdefault(len(params), []).append(current)
                        current = ""
                    elif char == "$":
                        yield None
                        break
                    else:
                        parameterless: bool = not params and not current and not groups
                        group: Optional[List[str]] = groups.get(len(params))
                        if group is not None:
                            group.append(current)
                            params.append(min(int(group[0] or 0), 9999))
                        else:
                            params.append(min(int(current or 0), 9999))
                        if char == ";":
                            current = ""
                        else:
                            if groups and char == "m" and not private:
                                params = expand_sgr_subparameters(params, groups)
                            if private and char == "u":
                                # Kitty keyboard protocol query (CSI ? u):
                                # answer with the supported flags (1 =
                                # disambiguate escape codes).
                                if self.respond is not None:
                                    self.respond("\x1b[>1u")
                            elif private:
                                csi_dispatch[char](*params, private=True)
                            elif parameterless and char == "s":
                                # SCOSC. pyte maps only ESC 7 to save_cursor,
                                # so an application that saves the cursor this
                                # way and homes it before entering the
                                # alternate screen (OpenCode does) would have
                                # the home position restored on exit and the
                                # exit epilogue printed over earlier rows.
                                listener.save_cursor()
                            elif parameterless and char == "u":
                                # SCORC - the counterpart of CSI s above.
                                listener.restore_cursor()
                            else:
                                csi_dispatch[char](*params)
                            break
            elif char == OSC_C1:
                code = yield None
                if code == "R":
                    continue
                elif code == "P":
                    continue
                nxt = yield None
                while nxt.isdigit():
                    code += nxt
                    nxt = yield None
                param: str = ""
                if nxt == ";":
                    while True:
                        char = yield None
                        if char == ESC:
                            char += yield None
                        if char in OSC_TERMINATORS:
                            break
                        else:
                            param += char
                listener.osc(code, param)
            elif char not in NUL_OR_DEL:
                draw(char)
