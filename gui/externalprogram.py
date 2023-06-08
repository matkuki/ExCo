# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2023 Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import os
import time
import subprocess
import psutil

import data
import functions
import components

if data.platform == "Windows":
    import win32api
    import win32con
    import win32gui
    import win32process
    
    class ExternalWidget(data.QWidget):
        handle_cache     = []
        
        name             = None
        _parent          = None
        main_form        = None
        current_icon     = None
        internals        = None
        savable          = data.CanSave.NO
        save_name        = None
        process_reference= None
        window_reference = None
        
        def __init__(self, parent, main_form, name):
            super().__init__(parent)
            self.name = name
            self._parent = parent
            self.main_form = main_form
            
            self.current_icon = functions.create_icon("tango_icons/utilities-terminal.png")
            self.internals = components.internals.Internals(
                parent=self, tab_widget=parent
            )
            self.internals.update_icon(self)
            
            self.update_style()
            
            self.my_hwnd = None
            self.external_hwnd = None
        
        def __del__(self):
            try:
                self.main_form.removeEventFilter(self)
            except:
                pass
            try:
                ExternalWidget.handle_cache.remove(hwnd)
                self.process_reference.kill()
            except:
                pass
        
        def set_my_hwnd(self, hwnd):
            self.my_hwnd = hwnd
        
        def set_external_hwnd(self, hwnd):
            self.external_hwnd = hwnd
            ExternalWidget.handle_cache.append(hwnd)
        
        def set_process_reference(self, proc):
            self.process_reference = proc
        
        def set_window_reference(self, window):
            self.window_reference = window
        
        def update_style(self):
            self.setStyleSheet(f"""
    QWidget {{
        padding: 0px;
        margin: 0px;
        border: none;
    }}
            """)
        
        def eventFilter(self, object, event):
            print("Object:", object, "Event-Type:", event.type())
            if event.type() in (data.QEvent.Type.Enter, data.QEvent.Type.MouseButtonPress, data.QEvent.Type.KeyPress):
                print("ENTER")
    #            if self.my_hwnd:
    #                win32gui.SetFocus(self.my_hwnd)
            elif event.type() == data.QEvent.Type.Leave:
                print("LEAVE")
    #            if self.external_hwnd:
    #                win32gui.SetFocus(self.external_hwnd)
            
            return super().eventFilter(object, event)
    
    def __create_external_widget(hwnd, proc, name, parent, main_form):
        main_widget = ExternalWidget(parent, main_form, name)
        main_widget.name = name
        main_widget.set_my_hwnd(int(main_widget.winId()))
        main_widget.set_external_hwnd(hwnd)
        main_widget.set_process_reference(proc)
        
        layout = data.QStackedLayout(main_widget)
        layout.setStackingMode(data.QStackedLayout.StackingMode.StackAll)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        main_widget.setLayout(layout)
        
        window = data.QWindow.fromWinId(hwnd)
        window.installEventFilter(main_form)
        main_widget.installEventFilter(main_form)
        main_widget.set_window_reference(window)
        external_widget = data.QWidget.createWindowContainer(
            window,
            parent=main_widget,
            flags=data.Qt.WindowType.FramelessWindowHint
        )
        main_widget.layout().addWidget(external_widget)
        def _initialize(*args):
            external_widget.hide()
            external_widget.show()
            external_widget.update()
        data.QTimer.singleShot(100, _initialize)
        
        return main_widget
        
    
    def find_window_for_pid(pid):
        result = None
        def callback(hwnd, _):
            nonlocal result
            try:
                if win32gui.IsWindowVisible(hwnd):
                    ctid, cpid = win32process.GetWindowThreadProcessId(hwnd)
                    pyhandle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, cpid)
                    proc_name = win32process.GetModuleFileNameEx(pyhandle, 0)
                    window_text = win32gui.GetWindowText(hwnd)
    #                print(pid, cpid, proc_name)
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
    
    def create_external_widget(parent, main_form, program):
    #    program = "C:\\ProgramData\\chocolatey\\bin\\alacritty.exe"
    #    program = "C:\\ProgramData\\chocolatey\\bin\\nu.exe"
    #    program = "C:\\tools\\LibreSprite-Windows-x86_64\\libresprite.exe"
    #    program = "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"
    #    program = "cmd.exe"
    #    program = "powershell.exe"
        name = os.path.basename(program)
        
        # Old PID's, if any for the application
        old_pids = []
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            if proc.info["name"] == name:
                pid = int(proc.info["pid"])
                old_pids.append(pid)
        
        # Run the process
        p = subprocess.Popen([program], creationflags=subprocess.CREATE_NEW_CONSOLE)
        
        # Embed the program
        external_widget = None
        found = False
        for i in range(100):
            for proc in psutil.process_iter(['pid', 'name', 'username']):
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
    
    class ExternalWidget(data.QWidget):
        handle_cache     = []
        
        name             = None
        _parent          = None
        main_form        = None
        current_icon     = None
        internals        = None
        savable          = data.CanSave.NO
        save_name        = None
        process_reference= None
        window_reference = None