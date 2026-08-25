"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

##  FILE DESCRIPTION:
##      Integrated terminal emulator package.
##      Consolidates the emulator previously split across gui/terminal.py,
##      gui/terminalview.py, components/terminal_backend.py and
##      components/terminal_screen.py:
##        - terminal.Terminal       -- the terminal emulator widget
##        - view.TerminalView       -- QPainter grid renderer
##        - backend.*               -- pluggable PTY backends
##        - screen.*                -- extended pyte screen/stream

from typing import List

from gui.terminal.backend import (
    ConPtyBackend,
    PtyProcessBackend,
    TerminalBackend,
    create_terminal_backend,
    get_default_shell,
)
from gui.terminal.screen import ExtendedScreen, ExtendedStream
from gui.terminal.terminal import Terminal, shutdown_all_terminals
from gui.terminal.view import TerminalView

__all__: List[str] = [
    "Terminal",
    "shutdown_all_terminals",
    "TerminalView",
    "ExtendedScreen",
    "ExtendedStream",
    "TerminalBackend",
    "ConPtyBackend",
    "PtyProcessBackend",
    "create_terminal_backend",
    "get_default_shell",
]
