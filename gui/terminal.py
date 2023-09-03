# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2023 Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import os
import sys
import math
import time
import threading
import traceback

import data
import functions
import gui.menu
import gui.stylesheets

try:
    import pyte
    if data.on_windows:
        import winpty
    else:
        import ptyprocess
except:
    msg = """
The terminal emulator needs the following packages 'pip install'-ed.
    On Windows:
        - pip install pyte
        - pip install pywinpty
    
    On Linux:
        - pip3 install pyte
        - pip3 install ptyprocess
"""
    raise Exception(msg)

PYTE_FOREGROUND_COLOR_MAP = {
    "black": data.QColor(data.Qt.GlobalColor.black),
    "red": data.QColor(data.Qt.GlobalColor.red),
    "green": data.QColor(data.Qt.GlobalColor.green),
    "brown": data.QColor(data.Qt.GlobalColor.yellow),
    "blue": data.QColor(data.Qt.GlobalColor.blue),
    "magenta": data.QColor(data.Qt.GlobalColor.magenta),
    "cyan": data.QColor(data.Qt.GlobalColor.cyan),
    "white": data.QColor(data.Qt.GlobalColor.lightGray),
    "default": data.QColor(data.Qt.GlobalColor.white),
    
    "brightblack": data.QColor(data.Qt.GlobalColor.darkGray),
    "brightred": data.QColor(data.Qt.GlobalColor.red),
    "brightgreen": data.QColor(data.Qt.GlobalColor.green),
    "brightbrown": data.QColor(data.Qt.GlobalColor.yellow),
    "brightblue": data.QColor(data.Qt.GlobalColor.blue),
    "brightmagenta": data.QColor(data.Qt.GlobalColor.magenta),
    "brightcyan": data.QColor(data.Qt.GlobalColor.cyan),
    "brightwhite": data.QColor(data.Qt.GlobalColor.white),
}
PYTE_BACKGROUND_COLOR_MAP = {
    "black": data.QColor(data.Qt.GlobalColor.black),
    "red": data.QColor(data.Qt.GlobalColor.red),
    "green": data.QColor(data.Qt.GlobalColor.green),
    "brown": data.QColor(data.Qt.GlobalColor.yellow),
    "blue": data.QColor(data.Qt.GlobalColor.blue),
    "magenta": data.QColor(data.Qt.GlobalColor.magenta),
    "cyan": data.QColor(data.Qt.GlobalColor.cyan),
    "white": data.QColor(data.Qt.GlobalColor.lightGray),
    "default": data.QColor(data.Qt.GlobalColor.black),
    
    "brightblack": data.QColor(data.Qt.GlobalColor.darkGray),
    "brightred": data.QColor(data.Qt.GlobalColor.red),
    "brightgreen": data.QColor(data.Qt.GlobalColor.green),
    "brightbrown": data.QColor(data.Qt.GlobalColor.yellow),
    "brightblue": data.QColor(data.Qt.GlobalColor.blue),
    "bfightmagenta": data.QColor(data.Qt.GlobalColor.magenta),
    "brightcyan": data.QColor(data.Qt.GlobalColor.cyan),
    "brightwhite": data.QColor(data.Qt.GlobalColor.white),
}

class CustomTextEdit(data.QPlainTextEdit):
    input_event = data.pyqtSignal(int, str, object)
    resize_event = data.pyqtSignal(int, int)
    paste_event = data.pyqtSignal(str)
    scroll_up_event = data.pyqtSignal(int)
    scroll_down_event = data.pyqtSignal(int)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__cache_width = None
        self.__cache_height = None
        self.document().setDocumentMargin(0)
        self.document().rootFrame().frameFormat().setBottomMargin(0)
        
        self.setHorizontalScrollBarPolicy(data.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(data.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.setFocusPolicy(data.Qt.FocusPolicy.StrongFocus)
        
        self.update_style()
    
    def setFocus(self):
        """
        Overridden focus event
        """
        # Execute the supeclass focus function
        super().setFocus()
        # Check indication
        self.parent().main_form.view.indication_check()
    
    def keyPressEvent(self, event):
        modifiers = data.QApplication.keyboardModifiers()
        key = event.key()
        text = event.text()
        self.input_event.emit(key, text, modifiers)
#        super().keyPressEvent(event)

    def mousePressEvent(self, event):
        """
        Overloaded mouse click event
        """
        # Execute the superclass mouse click event
        super().mousePressEvent(event)
        # Set focus to the clicked editor
        self.setFocus()

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            # Up
            self.scroll_up_event.emit(event.angleDelta().y())
        else:
            # Down
            self.scroll_down_event.emit(event.angleDelta().y())
        event.accept()
    
    def resizeEvent(self, event):
        w = self.viewport().size().width()
        h = self.viewport().size().height()
        font = self.document().defaultFont()
        font_metrics = data.QFontMetricsF(font)
        char_size = font_metrics.size(0, "X")
        width_in_chars = math.ceil(w / char_size.width())
        height_in_chars = math.floor(h / char_size.height())
        if self.__cache_width != width_in_chars or self.__cache_height != height_in_chars:
            self.__cache_width = width_in_chars
            self.__cache_height = height_in_chars
            self.resize_event.emit(width_in_chars, height_in_chars)
        return super().resizeEvent(event)
    
    def contextMenuEvent(self, event):
        # Show a context menu
        context_menu = gui.menu.Menu(parent=self)
        actions = {
            "copy": {
                "name": "Copy",
                "tooltip": "Copy",
                "icon": "tango_icons/edit-copy.png",
                "function": self.copy,
            },
            "cut": {
                "name": "Cut",
                "tooltip": "Cut",
                "icon": "tango_icons/edit-cut.png",
                "function": self.cut,
            },
            "paste": {
                "name": "Paste",
                "tooltip": "Paste",
                "icon": "tango_icons/edit-paste.png",
                "function": self.paste,
            },
            "undo": {
                "name": "Undo",
                "tooltip": "Undo",
                "icon": "tango_icons/edit-undo.png",
                "function": self.undo,
            },
            "redo": {
                "name": "Redo",
                "tooltip": "Redo",
                "icon": "tango_icons/edit-redo.png",
                "function": self.redo,
            },
        }
        for k,v in actions.items():
            action = data.QAction(v["name"], self)
            action.setToolTip(v["tooltip"])
            action.setStatusTip(v["tooltip"])
            action.setIcon(functions.create_icon(v["icon"]))
            if v["function"] is not None:
                action.triggered.connect(v["function"])
            action.setEnabled(True)
            context_menu.addAction(action)
        # Show menu
        cursor = data.QCursor.pos()
        context_menu.popup(cursor)
        # Accept event
        event.accept()
    
    def paste(self):
        paste_text = data.application.clipboard().text()
        self.paste_event.emit(paste_text)
    
    def update_style(self):
        self.setStyleSheet(f"""
QPlainTextEdit {{
    background-color: {PYTE_BACKGROUND_COLOR_MAP["default"].name()};
    color: {PYTE_FOREGROUND_COLOR_MAP["default"].name()};
    selection-background-color: {PYTE_FOREGROUND_COLOR_MAP["default"].name()};
    selection-color: {PYTE_BACKGROUND_COLOR_MAP["default"].name()};
    border: none;
    margin: 0px;
    spacing: 0px;
    padding: 0px;
}}

{gui.stylesheets.StyleSheetMenu.standard()}
        """)


class Terminal(data.QWidget):
    pty_data_received = data.pyqtSignal(object)
    pty_add_to_buffer = data.pyqtSignal(object)
    
    # Class variables
    name         = None
    _parent      = None
    main_form    = None
    current_icon = None
    savable      = data.CanSave.NO
    save_name    = None
    # Reference to the custom context menu
    context_menu = None
    
    def __init__(self, parent, main_form, name):
        super().__init__(parent)
        self.name = name
        self._parent = parent
        self.main_form = main_form
        self.current_icon = functions.create_icon('tango_icons/utilities-terminal.png')
        
        CONSOLE_WIDTH = 120
        CONSOLE_HEIGHT = 26
        
        self.screen = pyte.HistoryScreen(
            CONSOLE_WIDTH,
            CONSOLE_HEIGHT,
            history=1000,
            ratio=0.1,
        )
        self.stream = pyte.Stream(self.screen)
        
        if data.on_windows:
            self.pty_process = winpty.PtyProcess.spawn(
                "cmd",
                dimensions=(CONSOLE_HEIGHT, CONSOLE_WIDTH),
                backend=1,
            )
            
            self.pty_data_received.connect(self.__stdout_received)
            self.pty_add_to_buffer.connect(self.__send_buffer)
            # Reading
            self.__thread_pty_read = threading.Thread(
                target=self.__pty_read_loop_windows,
                args=[],
                daemon=True,
            )
            self.__thread_pty_read.start()
        else:
            self.pty_process = ptyprocess.PtyProcessUnicode.spawn(["/bin/bash"])
            
            self.pty_data_received.connect(self.__stdout_received)
            self.pty_add_to_buffer.connect(self.__send_buffer)
            
            # Reading
            self.__thread_pty_read = threading.Thread(
                target=self.__pty_read_loop_linux,
                args=[],
                daemon=True,
            )
            self.__thread_pty_read.start()
        
        # Create the console output widget
        self.output_widget = CustomTextEdit(self)
#        self.output_widget.setReadOnly(True)
        self.output_widget.setOverwriteMode(True)
        self.output_widget.setFont(data.get_editor_font())
        self.output_widget.setWordWrapMode(data.QTextOption.WrapMode.NoWrap)
#        self.output_widget.setWordWrapMode(data.QTextOption.WrapMode.WrapAnywhere)
        self.output_widget.input_event.connect(self.__input_event)
        self.output_widget.resize_event.connect(self.__resize_event)
        self.output_widget.paste_event.connect(self.__paste_event)
        self.output_widget.scroll_up_event.connect(self.__scroll_up_event)
        self.output_widget.scroll_down_event.connect(self.__scroll_down_event)
        
        # Add the widgets to a vertical layout
        layout = data.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.output_widget)
        
        self.update_style()
    
    def __del__(self):
        self.pty_process = None
        self.output_widget.setParent(None)
        self.output_widget = None
        self.__thread_pty_read = None
    
    def __pty_read_loop_windows(self):
        while self.pty_process.isalive():
#            data = self.pty_process.read(1)
            data = self.pty_process.read()
#            print("RAW-READ:", data)
#            print("RAW-DECODED-READ:", data.decode('utf-8'))
            if data is not None and data != b'':
                self.pty_add_to_buffer.emit(data)
            else:
                time.sleep(0.001)
    
    def __pty_read_loop_linux(self):
        while self.pty_process.isalive():
            data = self.pty_process.read().encode("utf-8")
            if data is not None and data != b'':
                self.pty_add_to_buffer.emit(data)
            else:
                time.sleep(0.001)
    
    def __send_buffer(self, new_data):
#        joined_buffer = b''.join(self.buffer).replace(b'\r', b'')
        if len(new_data) > 0:
            if isinstance(new_data, bytes):
                joined_buffer = new_data
            elif isinstance(new_data, str):
                joined_buffer = new_data
                joined_buffer.encode("utf-8")
            else:
                raise Exception("Unknown type: '{}'".format(new_data.__class__))
        else:
            joined_buffer = b''
        self.pty_data_received.emit(joined_buffer)
        self.buffer = []
    
    @data.pyqtSlot()
    def __update_display(self):
        # Timing initialization
        time_start = time.perf_counter()
        
        # Cursor
        cursor = self.output_widget.textCursor()
        cursor.setPosition(0)
        
        # Clear all text
        self.output_widget.clear()
        
        # Format the text
        bg = "default"
        fg = "default"
        new_formatting = data.QTextCharFormat()
        new_formatting.setBackground(PYTE_BACKGROUND_COLOR_MAP[bg])
        new_formatting.setForeground(PYTE_FOREGROUND_COLOR_MAP[fg])
        cursor.setCharFormat(new_formatting)
        current_char_list = []
        entire_height_in_lines = self.screen.lines
        for y in range(self.screen.lines):
            line = self.screen.buffer[y]
            for x in range(self.screen.columns):
                character = line[x]
                if character.bg != bg or character.fg != fg:
                    text = ''.join(current_char_list)
                    cursor.insertText(text)
                    current_char_list = []
                    bg = character.bg
                    fg = character.fg
                    new_formatting = data.QTextCharFormat()
                    # Byckground
                    if bg in PYTE_BACKGROUND_COLOR_MAP.keys():
                        new_formatting.setBackground(PYTE_BACKGROUND_COLOR_MAP[bg])
                    else:
                        new_color = data.QColor("#{}".format(bg))
                        new_formatting.setBackground(new_color)
                    # Foreground
                    if fg in PYTE_FOREGROUND_COLOR_MAP.keys():
                        new_formatting.setForeground(PYTE_FOREGROUND_COLOR_MAP[fg])
                    else:
                        new_color = data.QColor("#{}".format(fg))
                        new_formatting.setForeground(new_color)
                        
                    cursor.setCharFormat(new_formatting)
                
                current_char_list.append(character.data)
            current_char_list.append('\n')
        else:
            if len(current_char_list) > 0:
                text = ''.join(current_char_list)
                cursor.insertText(text)
        
        self.output_widget.setTextCursor(cursor)
        
        # Position the cursor
        left = cursor.columnNumber()
        cursor.setPosition(0)
        cursor.movePosition(
            data.QTextCursor.MoveOperation.Down,
            data.QTextCursor.MoveMode.MoveAnchor,
            self.screen.cursor.y
        )
        cursor.movePosition(
            data.QTextCursor.MoveOperation.Right,
            data.QTextCursor.MoveMode.MoveAnchor,
            self.screen.cursor.x
        )
        
        # Reset scrolling to top
        self.output_widget.verticalScrollBar().setValue(0)
        
        # Activate cursor
        self.output_widget.setTextCursor(cursor)
        self.output_widget.ensureCursorVisible()
        
        # Loop timing
        end_count = time.perf_counter() - time_start
    
    @data.pyqtSlot(bytes)
    def __stdout_received(self, raw_text):
        if isinstance(raw_text, bytes):
            self.stream.feed(raw_text.decode("utf-8"))
        else:
            self.stream.feed(raw_text)
        # Display output and error streams in console
        self.__update_display()
        
    
    def __input_event(self, key, text, modifiers):
#        print(modifiers, key, text, bytes(text, "utf-8"))

        update = False
        if modifiers == data.Qt.KeyboardModifier.ControlModifier:
            if key == data.Qt.Key.Key_Up:
#                self.screen.cursor_up()
                self.screen.prev_page()
                update = True
            elif key == data.Qt.Key.Key_Down:
                self.screen.next_page()
                update = True
                
        else:
            if key == data.Qt.Key.Key_Up:
                text = "\u001b[A"
                update = True
            elif key == data.Qt.Key.Key_Down:
                text = "\u001b[B"
                update = True
            elif key == data.Qt.Key.Key_Left:
                text = "\u001b[D"
                update = True
            elif key == data.Qt.Key.Key_Right:
                text = "\u001b[C"
                update = True
            elif key == data.Qt.Key.Key_PageUp:
                self.screen.prev_page()
                update = True
            elif key == data.Qt.Key.Key_PageDown:
                self.screen.next_page()
                update = True
        if update:
            self.__update_display()
        
        try:
            self.pty_process.write(text)
        except Exception as ex:
            self.main_form.display.repl_display_error(
                "Terminal has probably already been closed," +
                "the process returned: '{}'".format(ex)
            )
        
    stored_width = -1
    def __resize_event(self, width, height):
#        print("resize:", width, "x", height)
        if data.on_windows:
            width -= 1
        else:
            width -= 1
            height -= 1
        if width < 0:
            width = 0
        if height < 0:
            height = 0
        self.screen.resize(height, width)
        self.__update_display()
        self.pty_process.setwinsize(height, width)
    
    def __paste_event(self, paste_text):
        self.pty_process.write(paste_text)
        self.__update_display()
        self.output_widget.setFocus()
    
    def __scroll_up_event(self, value):
        value = int(value / 120)
        for i in range(value):
            self.screen.prev_page()
        self.__update_display()
    
    def __scroll_down_event(self, value):
        value = int(abs(value / 120))
        for i in range(value):
            self.screen.next_page()
        self.__update_display()
    
    def execute_command(self, command: str):
        self.pty_process.write(command + "\r\n")
    
    def setFocus(self):
        """
        Overridden focus event
        """
        self.output_widget.setFocus()
    
    def hasFocus(self):
        return self.output_widget.hasFocus()
    
    def update_style(self):
        self.setStyleSheet(f"""
QWidget {{
    background: transparent;
    border: none;
    margin: 0px;
    spacing: 0px;
    padding: 0px;
}}
        """)
        self.output_widget.update_style()


def test():
    app = data.QApplication(sys.argv)
    console = Terminal(None, None)
    console.resize(640, 480)
    console.show()
    sys.exit(app.exec())