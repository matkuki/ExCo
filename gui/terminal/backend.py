"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

##  FILE DESCRIPTION:
##      Pluggable PTY backends for the integrated terminal emulator.
##      Windows uses ConPTY (via pywinpty), Linux uses ptyprocess.

import os
import subprocess
import tempfile
from typing import Any, Dict, List, Optional, Tuple, Union

import data
import settings

# Shells recognized as PowerShell (Windows-only naming).
_POWERSHELL_NAMES: Tuple[str, ...] = (
    "powershell.exe",
    "pwsh.exe",
    "powershell",
    "pwsh",
)


def get_default_shell() -> str:
    return settings.get("terminal-shell")


def create_terminal_backend(
    shell: Optional[Union[str, List[str]]] = None,
    cwd: Optional[str] = None,
    env: Optional[Dict[str, str]] = None,
    dimensions: Tuple[int, int] = (24, 80),
) -> TerminalBackend:
    """
    Create the appropriate PTY backend for the current platform.

    Arguments:
        shell:      command to run inside the terminal. Defaults to the
                    configured 'terminal-shell' setting.
        cwd:        initial working directory of the spawned process.
        env:        environment dictionary for the spawned process.
        dimensions: (rows, columns) size of the terminal.
    """
    if shell is None:
        shell = get_default_shell()
    if data.on_windows:
        return ConPtyBackend(shell, cwd, env, dimensions)
    else:
        return PtyProcessBackend(shell, cwd, env, dimensions)


class TerminalBackend:
    """
    Base class for a PTY backend.

    Subclasses must implement the PTY accessors; the emulator talks only to
    this interface, never to the underlying process library directly.
    """

    shell: Union[str, List[str]]
    cwd: Optional[str]
    env: Optional[Dict[str, str]]
    dimensions: Tuple[int, int]
    process: Any

    def __init__(
        self,
        shell: Union[str, List[str]],
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        dimensions: Tuple[int, int] = (24, 80),
    ) -> None:
        self.shell = shell
        self.cwd = cwd
        self.env = env
        self.dimensions = dimensions
        self.process = None

    def spawn(self) -> None:
        raise NotImplementedError

    def isalive(self) -> bool:
        raise NotImplementedError

    def read(self, size: Optional[int] = None) -> Union[bytes, str]:
        raise NotImplementedError

    def write(self, text: str) -> None:
        raise NotImplementedError

    def setwinsize(self, rows: int, cols: int) -> None:
        raise NotImplementedError

    def close(self) -> None:
        raise NotImplementedError

    def pid(self) -> Optional[int]:
        return None


class ConPtyBackend(TerminalBackend):
    """
    Windows backend using the Windows Pseudo Console (ConPTY).
    """

    # Startup statements written to a temporary script and applied via
    # '-NoExit -File' so they are active before the first prompt renders.
    POWERSHELL_INIT_STATEMENTS: Tuple[str, ...] = (
        "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8",
        "Set-PSReadLineOption -PredictionSource History",
        "Set-PSReadLineOption -PredictionViewStyle ListView",
    )
    # Statements for the legacy typed-injection path only: 'Set-ExecutionPolicy'
    # works when typed between prompts, but its module fails to autoload in a
    # '-File' startup script - there the equivalent is passed as a command
    # line flag instead.
    POWERSHELL_POLICY_STATEMENT: str = (
        "Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force"
    )

    def __init__(
        self,
        shell: Union[str, List[str]],
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        dimensions: Tuple[int, int] = (24, 80),
    ) -> None:
        super().__init__(shell, cwd, env, dimensions)
        self._startup_baked: bool = False
        self._shell_name: str = ""
        self._init_script_path: Optional[str] = None

    def spawn(self) -> None:
        import winpty

        command: Union[str, List[str]] = self.shell
        tokens: List[str] = (
            [str(part) for part in command]
            if isinstance(command, (list, tuple))
            else self._tokenize_windows_command(command)
        )
        name: str = os.path.basename(tokens[0]).lower() if tokens else ""
        self._shell_name = name
        # PowerShell initialization is applied through a generated startup
        # script (-NoExit -File); typing it into the PTY races shell
        # startup, and '-Command' context discards PSReadLine options.
        spawn_command: Optional[str] = None
        if name in _POWERSHELL_NAMES:
            spawn_command = self._build_powershell_spawn_string(tokens)
        self._startup_baked = spawn_command is not None
        if spawn_command is None:
            spawn_command = (
                " ".join(str(part) for part in command)
                if isinstance(command, (list, tuple))
                else command
            )
        self.process = winpty.PtyProcess.spawn(
            spawn_command,
            cwd=self.cwd,
            env=self.env,
            dimensions=(self.dimensions[0], self.dimensions[1]),
            backend=0,
        )
        self._inject_startup_commands()

    @staticmethod
    def _tokenize_windows_command(command: str) -> List[str]:
        """
        Split a Windows command line into tokens on whitespace, honoring
        double quotes (the quotes themselves are dropped).
        """
        tokens: List[str] = []
        current: str = ""
        in_quotes: bool = False
        for char in command:
            if char == '"':
                in_quotes = not in_quotes
            elif char in (" ", "\t") and not in_quotes:
                if current:
                    tokens.append(current)
                    current = ""
            else:
                current += char
        if current:
            tokens.append(current)
        return tokens

    def _build_powershell_spawn_string(self, tokens: List[str]) -> Optional[str]:
        """
        Bake the startup initialization into the spawned command line by
        writing it to a temporary script and launching PowerShell with
        '-NoExit -File'.

        The script-file context matters: options applied via '-Command'
        (or typed into the PTY before the first prompt) are discarded by
        PSReadLine when its first interactive session initializes, while
        options set from a startup *script* - like ones set in a profile -
        persist from the very first prompt. The user may configure
        arbitrary arguments in the 'terminal-shell' setting; flags they
        already supplied (-NoExit, -NoLogo, ...) are honored and never
        duplicated.

        Returns None when the command line cannot be rewritten safely
        ('-Command', '-File' or '-EncodedCommand' already present); the
        caller then falls back to typing the initialization into the PTY.
        """
        executable: str = tokens[0]
        args: List[str] = tokens[1:]
        lowered: List[str] = [arg.lower() for arg in args]
        for arg in lowered:
            if arg in ("-e", "-ec", "-encodedcommand") or arg.startswith(
                ("-command", "-file")
            ):
                return None
        extras: List[str] = []
        if "-nologo" not in lowered:
            extras.append("-NoLogo")
        if "-executionpolicy" not in lowered:
            extras.extend(["-ExecutionPolicy", "Bypass"])
        if "-noexit" not in lowered:
            extras.append("-NoExit")
        # '-File' must be last: anything after the script path would be
        # passed to the script as arguments.
        script_path: str = self._write_powershell_init_script()
        return subprocess.list2cmdline(
            [executable] + args + extras + ["-File", script_path]
        )

    def _write_powershell_init_script(self) -> str:
        """
        Write the startup statements to a temporary .ps1 script and return
        its path. The file is removed again in close().

        Each statement is echoed in dim gray right before it runs, so the
        terminal visibly shows the initialization at the top of the
        scrollback, before the first prompt and any automatic 'cd'.
        """
        descriptor: int
        path: str
        descriptor, path = tempfile.mkstemp(prefix="exco-terminal-init-", suffix=".ps1")
        with os.fdopen(descriptor, "w", encoding="utf-8-sig") as handle:
            for statement in self.POWERSHELL_INIT_STATEMENTS:
                shown: str = statement.replace("'", "''")
                handle.write(f"Write-Host '+ {shown}' -ForegroundColor DarkGray\n")
                handle.write(statement + "\n")
        self._init_script_path = path
        return path

    def _remove_init_script(self) -> None:
        path: Optional[str] = self._init_script_path
        if path is not None:
            self._init_script_path = None
            try:
                os.remove(path)
            except OSError:
                pass

    def _inject_startup_commands(self) -> None:
        """
        Type shell-specific initialization commands into the PTY right
        after spawn.

        This is the legacy path, kept for shells whose command line cannot
        carry the initialization: cmd.exe needs its codepage switch typed,
        and PowerShell uses it only as a fallback when the user's arguments
        prevent baking the setup into the command line (see
        _build_powershell_spawn_string).

        ConPTY passes the child's raw console output through unchanged, and
        pywinpty decodes it as UTF-8. cmd.exe writes OEM-codepage bytes, so
        non-ASCII text would be garbled unless the console codepage is set to
        UTF-8 first. For PowerShell a Process-scoped execution policy is also
        set so local scripts (e.g. '.venv\\Scripts\\activate') run for this
        session only; the machine/user policy in the registry stays untouched.
        PSReadLine predictive IntelliSense (history source, list view) is
        enabled too; an outdated PSReadLine (the one bundled with Windows
        PowerShell 5.1) prints a visible parameter error here, signaling
        that 'Install-Module PSReadLine' should be run.

        Commands are terminated with a bare carriage return, never CRLF:
        ConPTY turns the CR into Enter, but a following LF reaches the next
        prompt as Ctrl+J, which PSReadLine binds to AddLine - it opens an
        empty '>>' continuation that corrupts the first typed command.
        """
        if self._shell_name in ("cmd.exe", "cmd", "command.com"):
            self.write("@chcp 65001 >nul\r")
        elif self._shell_name in _POWERSHELL_NAMES and not self._startup_baked:
            self.write(self.POWERSHELL_POLICY_STATEMENT + "\r")
            for statement in self.POWERSHELL_INIT_STATEMENTS:
                self.write(statement + "\r")

    def isalive(self) -> bool:
        return self.process.isalive()

    def read(self, size: Optional[int] = None) -> str:
        if size is None:
            size = 4096
        return self.process.read(size)

    def write(self, text: str) -> None:
        self.process.write(text)

    def setwinsize(self, rows: int, cols: int) -> None:
        self.process.setwinsize(rows, cols)

    def close(self) -> None:
        try:
            self.process.terminate(force=True)
        except Exception:
            pass
        self._remove_init_script()

    def pid(self) -> int:
        return self.process.pid


class PtyProcessBackend(TerminalBackend):
    """
    Linux/Unix backend using ptyprocess.
    """

    def spawn(self) -> None:
        import shlex

        import ptyprocess

        argv: Union[str, List[str]] = self.shell
        if isinstance(argv, str):
            argv = shlex.split(argv)
        self.process = ptyprocess.PtyProcessUnicode.spawn(
            argv,
            cwd=self.cwd,
            env=self.env,
        )

    def isalive(self) -> bool:
        return self.process.isalive()

    def read(self, size: Optional[int] = None) -> str:
        if size is None:
            size = 4096
        return self.process.read(size)

    def write(self, text: str) -> None:
        self.process.write(text)

    def setwinsize(self, rows: int, cols: int) -> None:
        self.process.setwinsize(rows, cols)

    def close(self) -> None:
        try:
            self.process.close()
        except Exception:
            pass

    def pid(self) -> int:
        return self.process.pid
