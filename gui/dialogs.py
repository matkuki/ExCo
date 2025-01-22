# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import qt
import data
import constants
import functions

from .custombuttons import *
from .stylesheets import *
from .templates import *


"""
---------------------------------------------------------
Custom Yes/No dialog window
---------------------------------------------------------
"""
class BaseDialog(qt.QDialog):
    def __init__(self, text, dialog_type=None, parent=None):
        super().__init__(parent)
        # Set the internal state
        self.state = None
        # Make the dialog stay on top
        self.setWindowFlags(qt.Qt.WindowType.WindowStaysOnTopHint)
        # Set the dialog icon and title
        self.setWindowIcon(qt.QIcon(data.application_icon))
        self.setWindowTitle(dialog_type.title())
        self.init_layout(text, dialog_type)
        # Set default font
        self.setFont(data.get_current_font())
        # Update style
        self.update_style()

    def create_button_list(self):
        raise Exception("[BaseDialog] This method needs to be overridden!")

    def init_layout(self, text, dialog_type):
        self.button_cache = []

        # Create the main layout
        main_layout = create_layout(
            layout=LayoutType.Vertical,
            margins=(8,8,8,8),
            spacing=4
        )
        self.setLayout(main_layout)

        # Add the label
        label = qt.QLabel(self)
        label.setWordWrap(True)
        label.setAlignment(qt.Qt.AlignmentFlag.AlignCenter)
        label.setText(text)
        main_layout.addWidget(label)

        # Add the button groupbox
        button_frame = create_frame(
            layout=LayoutType.Horizontal,
            spacing=10,
            parent=self,
        )
        button_layout = button_frame.layout()
        main_layout.addWidget(button_frame)

        button_list = self.create_button_list()
        # Create all of the buttons from the list
        for button in button_list:
            new_button = StandardButton(
                self,
                None,
            )
            if button["text"] is not None:
                new_button.setText(button["text"])
            if button["icon"] is not None:
                icon = functions.create_icon(button["icon"])
                new_button.setIcon(button)
                if button["size"] is not None:
                    new_button.setIconSize(
                        qt.QSize(
                            int(button["size"][0] * 0.8),
                            int(button["size"][1] * 0.8)
                        )
                    )
            new_button.setToolTip(button["tooltip"])
            new_button.setStatusTip(button["tooltip"])
            new_button.set_click_function(button["click-func"])
            new_button.state = button["state"]
#            new_button.set_enter_function(
#                create_enter_func(button.function_text, button.font)
#            )
#            new_button.set_leave_function(
#                create_leave_func(button.font)
#            )
            if button["size"] is not None:
                new_button.setFixedSize(
                    qt.QSize(
                        int(button["size"][0]),
                        int(button["size"][1])
                    )
                )

            button_layout.addWidget(new_button)
            self.button_cache.append(new_button)

        self.set_state(len(self.button_cache) - 1)

        self.setWindowFlags(qt.Qt.WindowType.FramelessWindowHint)

    def showEvent(self, event):
        super().showEvent(event)
        self.center()

    def __set_button_states(self, button_states):
        if len(button_states) != len(self.button_cache):
            raise Exception(
                "Length mismatch: {} != {}".format(
                    len(button_states), len(self.button_cache)
                )
            )
        for i,item in enumerate(self.button_cache):
            item.set_focused(button_states[i])

    def __state_cycle(self, none_index, _reversed):
        if self.state is None:
            button = self.button_cache[none_index]
            button.set_focused(True)
            self.state = button.state

        next_state = -1
        button_list = self.button_cache
        if _reversed:
            button_list = reversed(self.button_cache)
        for i,button in enumerate(button_list):
            if self.state == button.state:
                next_state = i + 1 if i < (len(self.button_cache) - 1) else i
            if next_state == i:
                button.set_focused(True)
                self.state = button.state
            else:
                button.set_focused(False)

    def state_cycle_right(self):
        self.__state_cycle(0, False)

    def state_cycle_left(self):
        self.__state_cycle(len(self.button_cache) - 1, True)

    def set_state(self, index):
        for i,button in enumerate(self.button_cache):
            if index == i:
                button.set_focused(True)
                self.state = button.state
            else:
                button.set_focused(False)

    def center(self):
        if self.parent() is not None:
            qr = self.frameGeometry()
            geo = self.parent().frameGeometry()
            cp = functions.create_point(
                int((geo.width() / 2) - (qr.width() / 2)),
                int((geo.height() / 2) - (qr.height() / 2))
            )
            self.move(cp)
        else:
            qr = self.frameGeometry()
            cp = self.screen().geometry().center()
            qr.moveCenter(cp)
            self.move(qr.topLeft())

    def keyPressEvent(self, key_event):
        pressed_key = key_event.key()
        #Check for escape keypress
        if pressed_key == qt.Qt.Key.Key_Escape:
            rightmost_button = self.button_cache[len(self.button_cache)-1]
            rightmost_button.set_focused(True)
            self.repaint()
            time.sleep(0.1)
            self.done(rightmost_button.state)
        elif pressed_key == qt.Qt.Key.Key_Right:
            self.state_cycle_right()
        elif pressed_key == qt.Qt.Key.Key_Left:
            self.state_cycle_left()
        elif pressed_key == qt.Qt.Key.Key_Enter or pressed_key == qt.Qt.Key.Key_Return:
            if self.state is None:
                self.state = self.button_cache[len(self.button_cache)-1].state
            self.done(self.state)

    def update_style(self):
        self.setStyleSheet(f"""
QDialog {{
    background-color: {data.theme["fonts"]["default"]["background"]};
    color: {data.theme["fonts"]["default"]["color"]};
    border: 1px solid {data.theme["indication"]["passiveborder"]};
    margin: 0px;
    padding: 0px;
    spacing: 0px;
}}
QGroupBox, QFrame {{
    background-color: {data.theme["fonts"]["default"]["background"]};
    color: {data.theme["fonts"]["default"]["color"]};
    border: none;
    margin: 0px;
    padding: 0px;
    spacing: 0px;
}}
QLabel {{
    background-color: {data.theme["fonts"]["default"]["background"]};
    color: {data.theme["fonts"]["default"]["color"]};
    border: none;
    font-family: {data.current_font_name};
    font-size: {data.current_font_size};
}}
{StyleSheetButton.standard()}
        """)
        for button in self.button_cache:
            button.update_style()

    @classmethod
    def blank(cls, text):
        return cls(text).exec()

    @classmethod
    def question(cls, text):
        return cls(text, "question").exec()

    @classmethod
    def warning(cls, text):
        return cls(text, "warning").exec()

    @classmethod
    def error(cls, text):
        return cls(text, "error").exec()

class YesNoDialog(BaseDialog):
    def create_button_list(self):
        return (
            {
                "name": "yes",
                "text": "Yes",
                "icon": None,
                "size": (data.standard_button_size, data.standard_button_size),
                "tooltip": "Confirm the action",
                "state": constants.DialogResult.Yes.value,
                "click-func": lambda *args: self.done(constants.DialogResult.Yes.value),
            },
            {
                "name": "no",
                "text": "No",
                "icon": None,
                "size": (data.standard_button_size, data.standard_button_size),
                "tooltip": "Decline the action",
                "state": constants.DialogResult.No.value,
                "click-func": lambda *args: self.done(constants.DialogResult.No.value),
            },
        )

class OkDialog(BaseDialog):
    def create_button_list(self):
        return (
            {
                "name": "ok",
                "text": "OK",
                "icon": None,
                "size": (data.standard_button_size, data.standard_button_size),
                "tooltip": "Close the dialog window",
                "state": constants.DialogResult.No.value,
                "click-func": lambda *args: self.done(constants.DialogResult.No.value),
            },
        )

class CloseEditorDialog(BaseDialog):
    def create_button_list(self):
        return (
            {
                "name": "save-and-close",
                "text": "Save \n&& Close",
                "icon": None,
                "size": (int(data.standard_button_size*1.5), data.standard_button_size),
                "tooltip": "Save document and close it",
                "state": constants.DialogResult.SaveAndClose.value,
                "click-func": lambda *args: self.done(constants.DialogResult.SaveAndClose.value),
            },
            {
                "name": "close",
                "text": "Close",
                "icon": None,
                "size": (data.standard_button_size, data.standard_button_size),
                "tooltip": "Close the document without saving",
                "state": constants.DialogResult.Close.value,
                "click-func": lambda *args: self.done(constants.DialogResult.Close.value),
            },
            {
                "name": "cancel",
                "text": "Cancel",
                "icon": None,
                "size": (data.standard_button_size, data.standard_button_size),
                "tooltip": "Cancel closing of the document",
                "state": constants.DialogResult.Cancel.value,
                "click-func": lambda *args: self.done(constants.DialogResult.Cancel.value),
            },
        )

class ToggleOneWindowDialog(BaseDialog):
    def create_button_list(self):
        return (
            {
                "name": "restore",
                "text": "Restore",
                "icon": None,
                "size": (data.standard_button_size, data.standard_button_size),
                "tooltip": "Restore the layout to the pre-one-window one",
                "state": constants.DialogResult.Restore.value,
                "click-func": lambda *args: self.done(constants.DialogResult.Restore.value),
            },
            {
                "name": "cancel",
                "text": "Cancel",
                "icon": None,
                "size": (data.standard_button_size, data.standard_button_size),
                "tooltip": "Cancel closing of the document",
                "state": constants.DialogResult.Cancel.value,
                "click-func": lambda *args: self.done(constants.DialogResult.Cancel.value),
            },
        )


class QuitDialog(BaseDialog):
    def create_button_list(self):
        return (
            {
                "name": "save-and-quit",
                "text": "Save all\n&& Quit",
                "icon": None,
                "size": (int(data.standard_button_size*1.5), data.standard_button_size),
                "tooltip": "Save all unsaved documents and quit ExCo",
                "state": constants.DialogResult.SaveAllAndQuit.value,
                "click-func": lambda *args: self.done(constants.DialogResult.SaveAllAndQuit.value),
            },
            {
                "name": "quit",
                "text": "Quit",
                "icon": None,
                "size": (data.standard_button_size, data.standard_button_size),
                "tooltip": "Quit ExCo without saving",
                "state": constants.DialogResult.Quit.value,
                "click-func": lambda *args: self.done(constants.DialogResult.Quit.value),
            },
            {
                "name": "cancel",
                "text": "Cancel",
                "icon": None,
                "size": (data.standard_button_size, data.standard_button_size),
                "tooltip": "Cancel quitting ExCo",
                "state": constants.DialogResult.Cancel.value,
                "click-func": lambda *args: self.done(constants.DialogResult.Cancel.value),
            },
        )

class RestoreSessionDialog(BaseDialog):
    def create_button_list(self):
        return (
            {
                "name": "save-and-restore",
                "text": "Save \n&& Restore",
                "icon": None,
                "size": (int(data.standard_button_size*1.5), data.standard_button_size),
                "tooltip": "Save all documents and restore session",
                "state": constants.DialogResult.SaveAndRestore.value,
                "click-func": lambda *args: self.done(constants.DialogResult.SaveAndRestore.value),
            },
            {
                "name": "close",
                "text": "Close",
                "icon": None,
                "size": (data.standard_button_size, data.standard_button_size),
                "tooltip": "Restore the session without saving",
                "state": constants.DialogResult.Restore.value,
                "click-func": lambda *args: self.done(constants.DialogResult.Close.value),
            },
            {
                "name": "cancel",
                "text": "Cancel",
                "icon": None,
                "size": (data.standard_button_size, data.standard_button_size),
                "tooltip": "Cancel restoring of the session",
                "state": constants.DialogResult.Cancel.value,
                "click-func": lambda *args: self.done(constants.DialogResult.Cancel.value),
            },
        )
