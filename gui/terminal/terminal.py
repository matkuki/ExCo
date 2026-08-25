"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import codecs
import os
import re
import threading
import traceback
from typing import Any, ClassVar, Iterable, List, Match, Optional, Set, Union
from urllib.parse import ParseResult, unquote, urlparse

import components.internals
import constants
import data
import functions
import pyte
import qt
import settings

from gui.terminal.backend import TerminalBackend, create_terminal_backend
from gui.terminal.screen import ExtendedScreen, ExtendedStream
from gui.terminal.view import TerminalView

# Windows console prompt: "PS C:\path>" or "C:\path>". Requires a drive
# letter and a path separator so ordinary output lines ending in '>' are
# not mistaken for a prompt.
_WINDOWS_PROMPT_RE: "re.Pattern[str]" = re.compile(r"^(?:PS\s+)?([A-Za-z]:[\\/].+)>$")
# Bash-style prompt: "user@host:/path$". The path must be absolute; the
# trailing '$' is matched separately so it never lands in the captured path.
_BASH_PROMPT_RE: "re.Pattern[str]" = re.compile(r"^[^@\s]+@[^:\s]+:(/.+)\$$")


class Terminal(qt.QWidget):
    pty_data_received = qt.pyqtSignal(object)
    pty_add_to_buffer = qt.pyqtSignal(object)
    title_changed = qt.pyqtSignal(str)
    process_exited = qt.pyqtSignal()

    # Registry of live terminal instances; iterated by
    # 'shutdown_all_terminals' when the application quits so no PTY
    # child process outlives Ex.Co.
    _live_terminals: ClassVar[Set["Terminal"]] = set()
    # Guard so the 'aboutToQuit' hook is connected exactly once.
    _quit_hook_connected: ClassVar[bool] = False

    # Class variables
    name: Optional[str] = None
    _parent: Any = None
    main_form: Any = None
    current_icon: Optional[qt.QIcon] = None
    savable: int = constants.CanSave.NO
    save_name: Optional[str] = None
    # Reference to the custom context menu
    context_menu: Any = None
    current_working_directory: Optional[str] = None

    def __init__(
        self,
        parent: Optional[qt.QWidget],
        main_form: Any,
        name: str,
        shell: Optional[Union[str, List[str]]] = None,
    ) -> None:
        super().__init__(parent)
        self.name = name
        self._parent = parent
        self.main_form = main_form
        self.current_icon = functions.create_icon("tango_icons/utilities-terminal.png")

        # Initialize components
        self.internals: components.internals.Internals = components.internals.Internals(
            parent=self, tab_widget=parent
        )

        CONSOLE_WIDTH: int = 120
        CONSOLE_HEIGHT: int = 26

        # Named 'term_screen' so it does not shadow QWidget.screen().
        self.term_screen: ExtendedScreen = ExtendedScreen(
            CONSOLE_WIDTH,
            CONSOLE_HEIGHT,
            history=settings.get("terminal-history"),
            ratio=0.1,
        )
        self.term_screen.set_mode(pyte.modes.DECAWM)
        self.stream: ExtendedStream = ExtendedStream(self.term_screen)
        # Terminal-initiated responses (e.g. the Kitty keyboard protocol
        # query reply) are written back to the PTY through the same path
        # as user input.
        self.stream.respond = self.__input_sent

        # Incremental UTF-8 decoder for the PTY byte path: a multi-byte
        # character split across two read chunks must carry over instead of
        # raising UnicodeDecodeError and dropping the partial bytes.
        self._decoder: codecs.IncrementalDecoder = codecs.getincrementaldecoder(
            "utf-8"
        )("replace")
        # Set by shutdown() to break the reader thread promptly.
        self._reader_stop: threading.Event = threading.Event()

        self.backend: Optional[TerminalBackend] = create_terminal_backend(
            shell=shell,
            dimensions=(CONSOLE_HEIGHT, CONSOLE_WIDTH),
        )
        self.backend.spawn()

        self._process_exited: bool = False
        self._last_title: Optional[str] = None
        self.process_exited.connect(self.__process_exited)

        # Track this instance and make sure quitting the application closes
        # every PTY (the tab-close path only covers explicit tab closes).
        Terminal._live_terminals.add(self)
        if not Terminal._quit_hook_connected:
            application: Any = qt.QApplication.instance()
            if application is not None:
                Terminal._quit_hook_connected = True
                application.aboutToQuit.connect(shutdown_all_terminals)

        self.pty_data_received.connect(self.__stdout_received)
        self.pty_add_to_buffer.connect(self.__send_buffer)
        # Reading
        self.__thread_pty_read: threading.Thread = threading.Thread(
            target=self.__pty_read_loop,
            args=[],
            daemon=True,
        )
        self.__thread_pty_read.start()

        # Create the terminal rendering widget
        self.view: TerminalView = TerminalView(self, self)
        self.view.send_text.connect(self.__input_sent)
        self.view.resize_event.connect(self.__resize_event)
        self.view.paste_event.connect(self.__paste_event)
        self.view.focused.connect(self.__view_focused)
        # Route keyboard focus straight to the view: this widget only
        # contains the view, and container focus would let Tab/keys fall
        # through to base QWidget handling (focus navigation).
        self.setFocusProxy(self.view)

        # Add the widgets to a vertical layout
        layout = qt.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.view)

        self.update_style()

    def __del__(self) -> None:
        # Last-resort safety net; the explicit teardown path is shutdown().
        shutdown: Any = getattr(self, "shutdown", None)
        if callable(shutdown):
            try:
                shutdown()
            except Exception:
                pass

    def shutdown(self) -> None:
        """
        Explicit teardown of the terminal: stop the reader thread and close
        the PTY backend. Idempotent. Called from 'tabwidget.close_tab' and
        from 'shutdown_all_terminals' when the application quits.
        """
        self._process_exited = True
        self._reader_stop.set()
        Terminal._live_terminals.discard(self)
        view: Optional[TerminalView] = getattr(self, "view", None)
        if view is not None:
            try:
                view.send_text.disconnect(self.__input_sent)
                view.resize_event.disconnect(self.__resize_event)
                view.paste_event.disconnect(self.__paste_event)
                view.focused.disconnect(self.__view_focused)
            except (TypeError, RuntimeError):
                pass
        backend: Optional[TerminalBackend] = getattr(self, "backend", None)
        if backend is not None:
            try:
                backend.close()
            except Exception:
                pass

    def __pty_read_loop(self) -> None:
        while True:
            if self._reader_stop.is_set():
                break
            backend: Optional[TerminalBackend] = self.backend
            if backend is None or not backend.isalive():
                self._mark_process_exited()
                break
            try:
                data = backend.read()
            except EOFError:
                self._mark_process_exited()
                break
            except Exception:
                # Reader thread: 'main_form.display' is not thread-safe
                # here, so the trace goes to stderr instead of the UI.
                traceback.print_exc()
                if self._reader_stop.wait(0.001):
                    break
                continue
            if data is not None and data != b"" and data != "":
                self.pty_add_to_buffer.emit(data)
            else:
                # No data available: block on the stop event instead of
                # spinning, so an idle terminal does not wake the CPU.
                if self._reader_stop.wait(0.05):
                    break

    def _mark_process_exited(self) -> None:
        if self._process_exited:
            return
        self._process_exited = True
        try:
            self.process_exited.emit()
        except RuntimeError:
            pass

    def __process_exited(self) -> None:
        # The shell has terminated; close the terminal tab (if any) so the
        # dead tab does not linger and accept input.
        try:
            parent: Any = getattr(self, "_parent", None)
            if parent is not None and hasattr(parent, "close_tab"):
                parent.close_tab(self)
        except Exception:
            pass

    def __send_buffer(self, new_data: Union[bytes, str]) -> None:
        if len(new_data) > 0:
            if isinstance(new_data, bytes):
                joined_buffer: Union[bytes, str] = new_data
            elif isinstance(new_data, str):
                joined_buffer = new_data
            else:
                raise Exception("Unknown type: '{}'".format(new_data.__class__))
        else:
            joined_buffer = b""
        self.pty_data_received.emit(joined_buffer)

    @qt.pyqtSlot(object)
    def __stdout_received(self, raw_text: object) -> None:
        try:
            if isinstance(raw_text, bytes):
                self.stream.feed(self._decoder.decode(raw_text))
            elif isinstance(raw_text, str):
                self.stream.feed(raw_text)
        except Exception as ex:
            self.__report_error("output processing failed", ex)
        # Surface OSC title changes
        if self.term_screen.title != getattr(self, "_last_title", None):
            self._last_title = self.term_screen.title
            if self.term_screen.title:
                self.title_changed.emit(self.term_screen.title)
        # Surface OSC 7 cwd
        osc7_applied: bool = False
        if self.term_screen.cwd:
            try:
                parsed: ParseResult = urlparse(self.term_screen.cwd)
                path: str = unquote(parsed.path)
                if parsed.netloc and parsed.netloc.lower() != "localhost":
                    path = "//" + parsed.netloc + path
                if (
                    data.on_windows
                    and path.startswith("/")
                    and len(path) > 2
                    and path[1:2].isalpha()
                ):
                    path = path[1:]
                if os.path.isdir(path):
                    self.current_working_directory = path
                    osc7_applied = True
            except Exception as ex:
                self.__report_error("OSC 7 cwd", ex)
        # Fall back to parsing the cwd from the prompt only when OSC 7 did
        # not already provide it this feed; scan just the lines that changed.
        if not osc7_applied:
            dirty_rows: List[int] = list(self.term_screen.dirty)
            self._parse_cwd(dirty_rows if dirty_rows else None)
        # Surface the bell (visual flash)
        if self.term_screen.bell_triggered:
            self.term_screen.bell_triggered = False
            self.view.flash()
        # Schedule a repaint of the changed screen lines
        self.view.schedule_repaint()

    def _parse_cwd(self, rows: Optional[Iterable[int]] = None) -> None:
        """
        Parse the current working directory from prompt lines.

        Arguments:
            rows: screen row indices to scan; defaults to every row. The
                  caller passes the feed's dirty rows so unchanged output
                  is not rescanned on every chunk.
        """
        try:
            screen: ExtendedScreen = self.term_screen
            row_indices: Iterable[int] = range(screen.lines) if rows is None else rows
            for y in row_indices:
                if not 0 <= y < screen.lines:
                    continue
                line: str = "".join(
                    screen.buffer[y][x].data for x in range(screen.columns)
                )
                stripped_line: str = line.strip()
                directory: Optional[str] = None
                windows_match: Optional[Match[str]] = _WINDOWS_PROMPT_RE.match(
                    stripped_line
                )
                bash_match: Optional[Match[str]] = _BASH_PROMPT_RE.match(stripped_line)
                if windows_match:
                    directory = windows_match.group(1).strip()
                elif bash_match:
                    directory = bash_match.group(1).strip()
                if directory is not None and os.path.isdir(directory):
                    self.current_working_directory = directory
        except Exception as ex:
            self.__report_error("prompt cwd parse", ex)

    def __report_error(self, context: str, error: Exception) -> None:
        """Report a terminal error through the main window display."""
        if self.main_form is None:
            return
        try:
            self.main_form.display.repl_display_error(
                "Terminal {}: '{}'".format(context, error)
            )
        except Exception:
            pass

    def __input_sent(self, text: str) -> None:
        if self._process_exited:
            # The shell has already terminated; drop the input instead of
            # failing on a closed PTY.
            return
        backend: Optional[TerminalBackend] = self.backend
        if backend is None:
            return
        try:
            backend.write(text)
        except Exception as ex:
            self.main_form.display.repl_display_error(
                "Terminal has probably already been closed,"
                + "the process returned: '{}'".format(ex)
            )

    def __view_focused(self) -> None:
        try:
            self.main_form.view.indication_check()
        except Exception:
            pass

    def __resize_event(self, width: int, height: int) -> None:
        try:
            if data.on_windows:
                # ConPTY reports one column fewer than the viewport; keep the
                # PTY one column larger so the last column is usable.
                width -= 1
            else:
                # X11/Unix terminals commonly report one row and column fewer
                # than the pixel-derived grid.
                width -= 1
                height -= 1
            width = max(width, 1)
            height = max(height, 1)
            self.term_screen.resize(height, width)
            self.view.update()
            backend: Optional[TerminalBackend] = self.backend
            if backend is not None:
                backend.setwinsize(height, width)
        except Exception:
            # Resize failures are non-actionable; never propagate them out
            # of a geometry handler during interactive resizing.
            pass

    def __paste_event(self, paste_text: str) -> None:
        if self._process_exited:
            # The shell has already terminated; drop the paste.
            self.view.setFocus()
            return
        backend: Optional[TerminalBackend] = self.backend
        if backend is not None:
            try:
                # Lone-surrogate clipboard text cannot be UTF-8 encoded;
                # replace the unencodable characters instead of crashing the
                # slot.
                sanitized: str = paste_text.encode("utf-8", errors="replace").decode(
                    "utf-8"
                )
                backend.write(sanitized)
            except Exception as ex:
                self.main_form.display.repl_display_error(
                    "Terminal has probably already been closed,"
                    + "the process returned: '{}'".format(ex)
                )
        self.view.setFocus()

    def execute_command(self, command: str) -> None:
        if self._process_exited:
            return
        backend: Optional[TerminalBackend] = self.backend
        if backend is not None:
            # Terminate with a bare carriage return, never CRLF: ConPTY
            # turns the CR into Enter, but a following LF reaches the next
            # prompt as Ctrl+J, which PSReadLine binds to AddLine - it
            # leaves a pending '>>' continuation that swallows the user's
            # first typed line and suppresses the prediction popup.
            backend.write(command + "\r")

    def get_cwd(self) -> Optional[str]:
        return self.current_working_directory

    def set_cwd(self, directory: str) -> None:
        # Quote the directory so paths containing spaces survive the shell
        # (cmd, PowerShell and bash all accept double-quoted paths).
        self.execute_command('cd "{}"'.format(directory))

    def setFocus(
        self, reason: qt.Qt.FocusReason = qt.Qt.FocusReason.NoFocusReason
    ) -> None:
        """
        Overridden focus event
        """
        self.view.setFocus()

    def hasFocus(self) -> bool:
        return self.view.hasFocus()

    def update_style(self) -> None:
        self.setStyleSheet(
            f"""
QWidget {{
    background: transparent;
    border: none;
    margin: 0px;
    spacing: 0px;
    padding: 0px;
}}
        """
        )
        self.view.update_style()

    def set_theme(self, theme: Any) -> None:
        # Matches the editor widgets' set_theme contract so the theme
        # refresh dispatch picks the terminal up; colors are re-read from
        # settings inside update_style().
        self.update_style()


def shutdown_all_terminals() -> None:
    """
    Shut down every live terminal instance. Connected to the application's
    'aboutToQuit' signal so spawned shell processes never outlive Ex.Co.,
    even when quitting without closing terminal tabs first.
    """
    for terminal in list(Terminal._live_terminals):
        try:
            terminal.shutdown()
        except Exception:
            pass
