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
import time
import traceback
from typing import (
    Any,
    ClassVar,
    Iterable,
    List,
    Match,
    Optional,
    Set,
    Tuple,
    Union,
    cast,
)
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

    # pyte parses only about 0.13-0.2 M characters a second, so these two
    # bound how far the screen can fall behind a fast producer (cat of a large
    # file on a raw PTY; ConPTY throttles to its frame rate by itself).
    # MAX_PENDING_OUTPUT is the most output (characters) the reader thread
    # queues before it stops reading - one to two seconds of parsing; the
    # child then blocks on its own writes, and Ctrl+C output stops promptly
    # instead of a long backlog replaying after it. FEED_SLICE is the most one
    # flush feeds before the next flush is queued, so the event loop paints
    # and takes input in between: measured with a raw 1.5 M-character flood,
    # the longest GUI stall is ~110 ms, where draining everything at once
    # froze the window for the whole 11 seconds.
    MAX_PENDING_OUTPUT: ClassVar[int] = 256 * 1024
    FEED_SLICE: ClassVar[int] = 8 * 1024
    # While a backlog is queued behind the slice just fed, the repaint (and
    # the prompt-cwd scan that goes with it) happens at most every
    # PRESENT_INTERVAL_S, not after every slice: a full-screen animation
    # is ~27 slices a frame, and repainting after each one painted the
    # screen ~3.5 times over per frame. The slice that empties the queue
    # always presents, and PRESENT_MAX_DELAY_MS bounds the wait should
    # that slice never come.
    PRESENT_INTERVAL_S: ClassVar[float] = 0.04
    PRESENT_MAX_DELAY_MS: ClassVar[int] = 100
    _last_present: float = 0.0
    _present_full: bool = False
    _present_timer: Optional[qt.QTimer] = None
    _osc7_applied_last: bool = False

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
    # OSC 7 verdict cache (see __stdout_received); class defaults so a
    # Terminal built without __init__ (the tree_terminal harness) still feeds.
    _osc7_seen: Optional[str] = None
    _osc7_valid: bool = False
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
        cwd: Optional[str] = None,
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
        # query reply, or an OSC 4/10/11/12 colour query) are written back to
        # the PTY through the same path as user input.
        self.stream.respond = self.__input_sent
        self.term_screen.respond = self.__input_sent

        # Incremental UTF-8 decoder for the PTY byte path: a multi-byte
        # character split across two read chunks must carry over instead of
        # raising UnicodeDecodeError and dropping the partial bytes.
        self._decoder: codecs.IncrementalDecoder = codecs.getincrementaldecoder(
            "utf-8"
        )("replace")
        # Set by shutdown() to break the reader thread promptly.
        self._reader_stop: threading.Event = threading.Event()
        # Output read by the reader thread and not yet fed to the screen (see
        # _queue_output / __send_buffer). One queued signal used to carry each
        # 4 KB read, so a fast producer (cat of a large file) filled the GUI
        # event queue faster than pyte could parse it and the window lagged
        # further and further behind; now the reader appends here and only
        # wakes the GUI thread when no flush is already pending.
        self._pending_condition: threading.Condition = threading.Condition()
        self._pending_output: List[Union[bytes, str]] = []
        self._pending_size: int = 0
        self._flush_scheduled: bool = False
        # Last OSC 7 value examined and whether it named an existing
        # directory, so an unchanged cwd costs no filesystem call per chunk.
        self._osc7_seen = None
        self._osc7_valid = False

        self.backend: Optional[TerminalBackend] = create_terminal_backend(
            shell=shell,
            cwd=cwd,
            dimensions=(CONSOLE_HEIGHT, CONSOLE_WIDTH),
        )
        self.backend.spawn()

        if cwd is not None and os.path.isdir(cwd):
            self.current_working_directory = cwd

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
        # Queued even when emitted from the GUI thread: a flush that leaves a
        # backlog re-emits it to continue after the event loop has painted
        # (an automatic connection would call straight back into the slot),
        # and Qt drops a queued call to a receiver that has been deleted.
        # (PyQt6 takes the connection type; its stub's connect() omits it.)
        self.pty_add_to_buffer.connect(  # type: ignore[call-arg]
            self.__send_buffer, qt.Qt.ConnectionType.QueuedConnection
        )
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

        # OSC 9 / 777 notifications and OSC 52 clipboard: the screen only
        # parses, the view owns both surfaces (status line, system
        # clipboard).
        self._install_osc_surfaces()

        # Add the widgets to a vertical layout
        layout = qt.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.view)

        self.update_style()

    def _install_osc_surfaces(self) -> None:
        """Wire the screen's OSC 9/777 and OSC 52 hooks to this view.

        The screen only parses; the view owns both surfaces (the status line
        and the system clipboard). The flags mirror the settings, so an
        application can neither pop UI nor read the clipboard unless the user
        allowed it. Changing a setting applies to terminals opened afterwards.
        """
        self.term_screen.notifications_enabled = bool(
            settings.get("terminal-notifications")
        )
        self.term_screen.notification_handler = self.view.show_notification
        self.term_screen.clipboard_write_enabled = bool(
            settings.get("terminal-osc52-write")
        )
        self.term_screen.clipboard_read_enabled = bool(
            settings.get("terminal-osc52-read")
        )
        self.term_screen.clipboard_write = self.view.put_clipboard_text
        self.term_screen.clipboard_read = self.view.osc52_clipboard_text

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
                self._queue_output(data)
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

    def _queue_output(self, data: Union[bytes, str]) -> None:
        """Reader thread: queue *data* for the GUI thread.

        Only the first chunk after a flush emits the wake-up signal; the rest
        ride along with it. While more than MAX_PENDING_OUTPUT is queued the
        reader waits here (re-checking the stop event), which leaves the rest
        in the PTY and makes the child wait instead of the GUI.
        """
        with self._pending_condition:
            while (
                self._pending_size >= self.MAX_PENDING_OUTPUT
                and not self._reader_stop.is_set()
            ):
                self._pending_condition.wait(0.05)
            self._pending_output.append(data)
            self._pending_size += len(data)
            if self._flush_scheduled:
                return
            self._flush_scheduled = True
        try:
            self.pty_add_to_buffer.emit(None)
        except RuntimeError:
            # The widget is being destroyed; nothing left to feed.
            pass

    def _take_pending_output(self) -> Tuple[List[Union[bytes, str]], bool]:
        """GUI thread: up to FEED_SLICE of the queued output, joined per data
        type, and whether more is still queued.

        Whole read chunks are taken (at least one), so a slice never splits a
        read. While a backlog remains the flush stays scheduled, so the reader
        does not emit a second wake-up for it; the caller queues the next
        flush itself.
        """
        with self._pending_condition:
            taken: int = 0
            count: int = 0
            for queued in self._pending_output:
                if count and taken + len(queued) > self.FEED_SLICE:
                    break
                taken += len(queued)
                count += 1
            chunks: List[Union[bytes, str]] = self._pending_output[:count]
            del self._pending_output[:count]
            self._pending_size -= taken
            more: bool = bool(self._pending_output)
            self._flush_scheduled = more
            self._pending_condition.notify_all()
        joined: List[Union[bytes, str]] = []
        run: List[Union[bytes, str]] = []
        for chunk in chunks:
            if run and type(chunk) is not type(run[0]):
                joined.append(self._join_chunks(run))
                run = []
            run.append(chunk)
        if run:
            joined.append(self._join_chunks(run))
        return joined, more

    @staticmethod
    def _join_chunks(run: List[Union[bytes, str]]) -> Union[bytes, str]:
        if isinstance(run[0], bytes):
            return b"".join(cast(List[bytes], run))
        return "".join(cast(List[str], run))

    def __send_buffer(self, _wake: object = None) -> None:
        # One feed (and one repaint) per slice of what the reader queued. A
        # backend that mixes bytes and str (none does today) is fed one run at
        # a time, in order. A remaining backlog is continued by a queued
        # wake-up, i.e. after the event loop has painted and taken input.
        chunks: List[Union[bytes, str]]
        more: bool
        chunks, more = self._take_pending_output()
        for chunk in chunks:
            self.pty_data_received.emit(chunk)
        if more:
            self.pty_add_to_buffer.emit(None)

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
        if self.term_screen.cwd and self.term_screen.cwd == self._osc7_seen:
            # Unchanged since the last chunk: reuse the verdict instead of a
            # urlparse + os.path.isdir round trip for every chunk of output.
            osc7_applied = self._osc7_valid
        elif self.term_screen.cwd:
            self._osc7_seen = self.term_screen.cwd
            self._osc7_valid = False
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
                    if path != self.current_working_directory:
                        self.current_working_directory = path
                        self.__cwd_changed()
                    osc7_applied = True
                    self._osc7_valid = True
            except Exception as ex:
                self.__report_error("OSC 7 cwd", ex)
        self._osc7_applied_last = osc7_applied
        # Surface the bell (visual flash)
        if self.term_screen.bell_triggered:
            self.term_screen.bell_triggered = False
            self.view.flash()
        # The prompt-cwd scan and the repaint of the changed lines, unless
        # more output is queued right behind this slice
        if not self._defer_present():
            self._present()

    def _defer_present(self) -> bool:
        """Whether to hold the repaint back: a backlog follows and the last
        one was less than PRESENT_INTERVAL_S ago.

        Nothing is lost by waiting: the dirty rows stay on the screen until
        the next present. A slice that scrolled is remembered, because the
        next feed resets ``pending_scroll`` and the scroll would otherwise
        go unnoticed; that costs one full repaint when presenting.
        """
        # Read through __dict__: on a Terminal built without its backend (the
        # tests do) a missing attribute raises RuntimeError from sip, which
        # getattr's default does not catch.
        if not self.__dict__.get("_pending_output"):
            return False
        if time.monotonic() - self._last_present >= self.PRESENT_INTERVAL_S:
            return False
        if self.term_screen.pending_scroll:
            self._present_full = True
        timer: Optional[qt.QTimer] = self._present_timer
        if timer is None:
            timer = qt.QTimer(self)
            timer.setSingleShot(True)
            timer.setInterval(self.PRESENT_MAX_DELAY_MS)
            timer.timeout.connect(self._present)
            self._present_timer = timer
        if not timer.isActive():
            timer.start()
        return True

    def _present(self) -> None:
        """Scan the changed rows for a prompt cwd and repaint them.

        Covers everything fed since the previous present, which is one slice
        normally and a whole burst of them during a backlog.
        """
        if self._present_timer is not None:
            self._present_timer.stop()
        self._last_present = time.monotonic()
        # Fall back to parsing the cwd from the prompt only when OSC 7 did
        # not already provide it; scan just the lines that changed.
        if not self._osc7_applied_last:
            dirty_rows: List[int] = list(self.term_screen.dirty)
            self._parse_cwd(dirty_rows if dirty_rows else None)
        # Schedule a repaint of the changed screen lines
        self.view.schedule_repaint()
        if self._present_full:
            self._present_full = False
            self.view.update()

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
                    if directory != self.current_working_directory:
                        self.current_working_directory = directory
                        self.__cwd_changed()
        except Exception as ex:
            self.__report_error("prompt cwd parse", ex)

    def __cwd_changed(self) -> None:
        """
        Persist the terminal's new working directory into the saved layout.

        Called from the OSC 7 and prompt-parsing paths after the
        'current_working_directory' actually changes, so the on-disk layout
        stays in sync with the shell even between unrelated layout changes.
        """
        if self._process_exited or self.main_form is None:
            return
        view: Any = getattr(self.main_form, "view", None)
        layout_save: Any = getattr(view, "layout_save", None)
        if layout_save is not None:
            try:
                layout_save()
            except Exception as ex:
                self.__report_error("cwd layout save", ex)

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
            # The screen and the PTY get exactly the grid the view measured.
            # A one-column (and on Unix one-row) trim dated from the pre-ConPTY
            # text-widget renderer; since the screen and the PTY were always
            # trimmed together it never fixed a mismatch, it only left the
            # view's last column (and row) permanently empty. Measured on
            # ConPTY with cmd.exe and PowerShell/PSReadLine at full width:
            # exact-width output, wrapped output and typing past the edge
            # all land correctly.
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

    def reset_terminal(self) -> None:
        """Reset the emulation state (RIS) while leaving the shell running.

        The sequence is fed through the stream rather than calling
        ``term_screen.reset()`` directly, so it takes exactly the path an
        application sending ESC c takes: pyte resets modes, margins and tabs,
        the extended screen also drops the alternate screen, hyperlinks and an
        OSC-painted palette, and the view repaints through the usual path.
        """
        self.stream.feed("\x1bc")
        self.term_screen.dirty = set(range(self.term_screen.lines))
        if self._last_title:
            # RIS clears the title, which the tab title was following; put the
            # terminal's own name back instead of leaving a stale one.
            self._last_title = None
            self.title_changed.emit(self.name)
        self.view.schedule_repaint()

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
            """
QWidget {
    background: transparent;
    border: none;
    margin: 0px;
    spacing: 0px;
    padding: 0px;
}
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
