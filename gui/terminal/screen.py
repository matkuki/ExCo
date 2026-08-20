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
##        - DECSCUSR cursor style
##        - Bell surfacing

import copy
from typing import Any, Callable, Dict, Generator, List, Optional, Set, Tuple

try:
    import pyte
    from pyte import screens as pyte_screens
    from pyte import streams as pyte_streams
except ImportError:
    msg = """
The terminal emulator needs the following package 'pip install'-ed:
    - pip install pyte

On Windows the backend uses pywinpty (ConPTY), on Linux it uses ptyprocess.
"""
    raise ImportError(msg)

# Alternate screen private modes
ALT_SCREEN_MODES: Tuple[int, int, int] = (47, 1047, 1049)

# Mouse tracking private modes
MOUSE_BUTTON_MODE: int = 1000
MOUSE_DRAG_MODE: int = 1002
MOUSE_MOVE_MODE: int = 1003
MOUSE_SGR_MODE: int = 1006

# Bracketed paste private mode
BRACKETED_PASTE_MODE: int = 2004


class ExtendedScreen(pyte_screens.HistoryScreen):
    """
    HistoryScreen extended with alternate screen, mouse tracking,
    bracketed paste, OSC (title/icon/cwd/hyperlink), DECSCUSR and bell.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # Per-feed-chunk scroll tracking for the view's repaint decision:
        # pending_scroll is non-zero when the content moved vertically this
        # chunk (the view then does a full repaint). Initialized before
        # super().__init__ because pyte's reset() runs during it; reset()
        # also clears keyboard_flags, so it lives here too.
        self.pending_scroll: int = 0
        self.keyboard_flags: int = 0
        super().__init__(*args, **kwargs)
        # Alternate screen state
        self._alt_saved: Optional[Dict[str, Any]] = None
        self._alt_modes_active: Set[int] = set()
        # OSC state
        self.cwd: Optional[str] = None
        self.hyperlink: Optional[str] = None
        self.hyperlink_spans: List[Tuple[Tuple[int, int], Tuple[int, int], str]] = []
        self._active_hyperlink: Optional[str] = None
        # DECSCUSR state
        self.cursor_style: str = "block"
        self.cursor_blink: bool = True
        # Bell
        self.bell_triggered: bool = False

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
        }
        self.hyperlink_spans.clear()
        self.buffer.clear()
        self.cursor_position()
        self.erase_in_display(2)
        self.dirty.update(range(self.lines))

    def _leave_alt_screen(self) -> None:
        saved = self._alt_saved
        if saved is None:
            return
        self.buffer.clear()
        self.buffer.update(saved["buffer"])
        self.cursor = saved["cursor"]
        self.savepoints = saved["savepoints"]
        self.margins = saved["margins"]
        self._alt_saved = None
        self.hyperlink_spans.clear()
        self.dirty.update(range(self.lines))

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

    def _full_screen_margins(self) -> bool:
        """True when the scrolling region spans the whole screen."""
        top: int
        bottom: int
        top, bottom = self.margins or pyte_screens.Margins(0, self.lines - 1)
        return top == 0 and bottom == self.lines - 1

    def index(self) -> None:
        # While the alternate screen is active, keep the scrollback history
        # frozen; scrolled-out lines simply disappear.
        scrolled: bool = self._full_screen_margins() and self.cursor.y == self.lines - 1
        if self._alt_saved is None:
            super().index()
        else:
            pyte_screens.Screen.index(self)
        if scrolled:
            self.pending_scroll += 1

    def reverse_index(self) -> None:
        scrolled: bool = self._full_screen_margins() and self.cursor.y == 0
        super().reverse_index()
        if scrolled:
            self.pending_scroll -= 1

    def insert_lines(self, count: Optional[int] = None) -> None:
        count = count or 1
        top: int
        bottom: int
        top, bottom = self.margins or pyte_screens.Margins(0, self.lines - 1)
        full: bool = top == 0 and bottom == self.lines - 1 and self.cursor.y == top
        super().insert_lines(count)
        if full:
            self.pending_scroll -= count

    def delete_lines(self, count: Optional[int] = None) -> None:
        count = count or 1
        top: int
        bottom: int
        top, bottom = self.margins or pyte_screens.Margins(0, self.lines - 1)
        full: bool = top == 0 and bottom == self.lines - 1 and self.cursor.y == top
        super().delete_lines(count)
        if full:
            self.pending_scroll += count

    def resize(
        self, lines: Optional[int] = None, columns: Optional[int] = None
    ) -> None:
        super().resize(lines, columns)
        # Hyperlink spans are cell-coordinate bound; drop them on resize.
        self.hyperlink_spans.clear()

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

    # ------------------------------------------------------------------
    # OSC (title / icon / cwd / hyperlink)
    # ------------------------------------------------------------------

    def osc(self, code: str, param: str) -> None:
        if code in "01":
            self.set_icon_name(param)
        if code in "02":
            self.set_title(param)
        if code == "7":
            # OSC 7 - set the current working directory. An empty parameter
            # does not carry a location; keep the previous cwd.
            if param:
                self.cwd = param
        if code == "8":
            # OSC 8 - hyperlink: "params;uri". An empty URI terminates the
            # active link; previously drawn spans are retained for hover.
            parts = param.split(";", 1)
            if len(parts) == 2:
                params, uri = parts
                self._active_hyperlink = uri or None
            else:
                self._active_hyperlink = None

    # Maximum retained hyperlink spans (the view does not render them yet, so
    # cap the list to keep memory bounded).
    MAX_HYPERLINK_SPANS: int = 1000

    def draw(self, data: str) -> None:
        if self._active_hyperlink is not None:
            start: Tuple[int, int] = (self.cursor.y, self.cursor.x)
            super().draw(data)
            end: Tuple[int, int] = (self.cursor.y, self.cursor.x)
            if start != end:
                self.hyperlink_spans.append((start, end, self._active_hyperlink))
                if len(self.hyperlink_spans) > self.MAX_HYPERLINK_SPANS:
                    del self.hyperlink_spans[
                        : len(self.hyperlink_spans) - self.MAX_HYPERLINK_SPANS
                    ]
        else:
            super().draw(data)

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

    def reset(self) -> None:
        # A full reset (RIS) also drops the Kitty keyboard protocol mode;
        # the app re-pushes it on the next enable.
        self.keyboard_flags = 0
        super().reset()


class ExtendedStream(pyte_streams.Stream):
    """
    pyte Stream with extra protocol support: DECSCUSR, OSC 7/8 and the
    Kitty keyboard protocol.

    The parser FSM is copied from pyte 0.8.2 (LGPL, see pyte license) with
    three additions:
      - the OSC branch dispatches to ``screen.osc(code, param)`` so OSC 7
        (cwd) and OSC 8 (hyperlinks) are surfaced;
      - a CSI ``... SP q`` sequence (DECSCUSR) is dispatched to
        ``screen.set_cursor_style``;
      - the Kitty keyboard protocol sequences ``CSI > flags u``,
        ``CSI < flags u`` and ``CSI ? u`` set ``screen.keyboard_flags``
        and answer the query via ``respond``.
    """

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
                        if self.use_utf8:
                            continue
                        listener.define_charset(code, mode=char)
                    elif char in "PX^_":
                        # DCS / SOS / PM / APC: swallow the payload until ST
                        # (ESC \), BEL or C1 ST. Without this the payload is
                        # drawn as visible text (e.g. DCS "+q" session ids).
                        while True:
                            nxt = yield None
                            if nxt == ESC:
                                nxt2 = yield None
                                if nxt2 == "\\":
                                    break
                            elif nxt in (
                                pyte.control.BEL,
                                pyte.control.CAN,
                                pyte.control.SUB,
                                pyte.control.ST_C1,
                            ):
                                break
                    else:
                        escape_dispatch[char]()
                    continue

            if char in basic:
                if (
                    char == pyte.control.SI or char == pyte.control.SO
                ) and self.use_utf8:
                    continue
                basic_dispatch[char]()
            elif char == CSI_C1:
                params: List[int] = []
                current: str = ""
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
                    elif char == "$":
                        yield None
                        break
                    else:
                        params.append(min(int(current or 0), 9999))
                        if char == ";":
                            current = ""
                        else:
                            if private and char == "u":
                                # Kitty keyboard protocol query (CSI ? u):
                                # answer with the supported flags (1 =
                                # disambiguate escape codes).
                                if self.respond is not None:
                                    self.respond("\x1b[>1u")
                            elif private:
                                csi_dispatch[char](*params, private=True)
                            else:
                                csi_dispatch[char](*params)
                            break
            elif char == OSC_C1:
                code = yield None
                if code == "R":
                    continue
                elif code == "P":
                    continue

                param: str = ""
                while True:
                    char = yield None
                    if char == ESC:
                        char += yield None
                    if char in OSC_TERMINATORS:
                        break
                    else:
                        param += char

                param = param[1:]  # Drop the ;.
                listener.osc(code, param)
            elif char not in NUL_OR_DEL:
                draw(char)
