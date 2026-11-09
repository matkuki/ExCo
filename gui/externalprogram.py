"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import os
import time
import subprocess
from typing import Any

import qt
import data
import constants
import functions
import components
import components.internals

if data.platform == "Windows":

    class ExternalWidget(qt.QWidget):
        handle_cache: list[int] = []

        name: str | None = None
        _parent: Any = None
        main_form: Any = None
        current_icon: Any = None
        internals: Any = None
        savable = constants.CanSave.NO
        save_name: str | None = None
        process_reference: Any = None
        window_reference: Any = None

        def __init__(self, parent: Any, main_form: Any, name: str) -> None:
            super().__init__(parent)
            self.name = name
            self._parent = parent
            self.main_form = main_form

            self.current_icon = functions.create_icon(
                "tango_icons/utilities-terminal.png"
            )
            self.internals = components.internals.Internals(
                parent=self, tab_widget=parent
            )
            self.internals.update_icon(self)

            self.update_style()

            self.my_hwnd: int | None = None
            self.external_hwnd: int | None = None

        def __del__(self) -> None:
            try:
                self.main_form.removeEventFilter(self)
            except:
                pass
            try:
                if (
                    self.my_hwnd is not None
                    and self.my_hwnd in ExternalWidget.handle_cache
                ):
                    ExternalWidget.handle_cache.remove(self.my_hwnd)
                self.process_reference.kill()
            except:
                pass

        def set_my_hwnd(self, hwnd: int) -> None:
            self.my_hwnd = hwnd

        def set_external_hwnd(self, hwnd: int) -> None:
            self.external_hwnd = hwnd
            ExternalWidget.handle_cache.append(hwnd)

        def set_process_reference(self, proc: Any) -> None:
            self.process_reference = proc

        def set_window_reference(self, window: Any) -> None:
            self.window_reference = window

        def update_style(self) -> None:
            self.setStyleSheet(
                f"""
    QWidget {{
        padding: 0px;
        margin: 0px;
        border: none;
    }}
            """
            )

        def eventFilter(self, object: Any, event: Any) -> bool:
            #            if event.type() in (qt.QEvent.Type.Enter, qt.QEvent.Type.MouseButtonPress, qt.QEvent.Type.KeyPress):
            #                if self.my_hwnd:
            #                    win32gui.SetFocus(self.my_hwnd)
            #            elif event.type() == qt.QEvent.Type.Leave:
            #                if self.external_hwnd:
            #                    win32gui.SetFocus(self.external_hwnd)

            return super().eventFilter(object, event)

    def __create_external_widget(
        hwnd: int, proc: Any, name: str, parent: Any, main_form: Any
    ) -> ExternalWidget:
        main_widget = ExternalWidget(parent, main_form, name)
        main_widget.name = name
        main_widget.set_my_hwnd(int(main_widget.winId()))
        main_widget.set_external_hwnd(hwnd)
        main_widget.set_process_reference(proc)

        layout = qt.QStackedLayout(main_widget)
        layout.setStackingMode(qt.QStackedLayout.StackingMode.StackAll)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        main_widget.setLayout(layout)

        window = qt.QWindow.fromWinId(hwnd)  # type: ignore[arg-type]
        assert window is not None
        window.installEventFilter(main_form)
        main_widget.installEventFilter(main_form)
        main_widget.set_window_reference(window)
        external_widget = qt.QWidget.createWindowContainer(
            window, parent=main_widget, flags=qt.Qt.WindowType.FramelessWindowHint
        )
        widget_layout = main_widget.layout()
        assert widget_layout is not None
        widget_layout.addWidget(external_widget)

        def _initialize(*args: Any) -> None:
            external_widget.hide()
            external_widget.show()
            external_widget.update()

        qt.QTimer.singleShot(100, _initialize)

        return main_widget

    def find_window_for_pid(pid: int) -> int | None:
        import win32api
        import win32con
        import win32gui
        import win32process

        result = None

        def callback(hwnd: int, _: Any) -> bool:
            nonlocal result
            try:
                if win32gui.IsWindowVisible(hwnd):
                    ctid, cpid = win32process.GetWindowThreadProcessId(hwnd)
                    pyhandle = win32api.OpenProcess(
                        win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ,
                        False,
                        cpid,
                    )
                    proc_name = win32process.GetModuleFileNameEx(pyhandle, 0)
                    window_text = win32gui.GetWindowText(hwnd)
                    if int(cpid) == int(pid):
                        result = hwnd
                        return False
            except:
                pass
            return True

        try:
            win32gui.EnumWindows(callback, None)
        except:
            pass
        return result

    def create_external_widget(
        parent: Any, main_form: Any, program: str
    ) -> ExternalWidget | None:
        #    program = "C:\\ProgramData\\chocolatey\\bin\\alacritty.exe"
        #    program = "C:\\ProgramData\\chocolatey\\bin\\nu.exe"
        #    program = "C:\\tools\\LibreSprite-Windows-x86_64\\libresprite.exe"
        #    program = "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"
        #    program = "cmd.exe"
        #    program = "powershell.exe"
        name = os.path.basename(program)

        import psutil

        # Old PID's, if any for the application
        old_pids = []
        for proc in psutil.process_iter(["pid", "name", "username"]):
            if proc.info["name"] == name:
                pid = int(proc.info["pid"])
                old_pids.append(pid)

        # Run the process
        p = subprocess.Popen([program], creationflags=subprocess.CREATE_NEW_CONSOLE)

        # Embed the program
        external_widget = None
        found = False
        for i in range(100):
            for proc in psutil.process_iter(["pid", "name", "username"]):
                if proc.info["name"] == name:
                    pid = int(proc.info["pid"])
                    if pid in old_pids:
                        continue
                    _hwnd = find_window_for_pid(pid)
                    if _hwnd is not None:
                        external_widget = __create_external_widget(
                            _hwnd, proc, name, parent, main_form
                        )
                        found = True
                        break
            else:
                time.sleep(0.01)
            if found:
                break

        return external_widget

else:

    class ExternalWidget(qt.QWidget):  # type: ignore[no-redef]
        handle_cache: list[int] = []

        name: str | None = None
        _parent: Any = None
        main_form: Any = None
        current_icon: Any = None
        internals: Any = None
        savable = constants.CanSave.NO
        save_name: str | None = None
        process_reference: Any = None
        window_reference: Any = None
