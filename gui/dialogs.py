
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2019 Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import os
import traceback
import inspect

import data
import settings
import functions
import components
import themes

from .custombuttons import *
from .stylesheets import *
from .templates import *


"""
---------------------------------------------------------
Custom Yes/No dialog window
---------------------------------------------------------
""" 
class YesNoDialog(data.QDialog):    
    def __init__(self, text, dialog_type=None, parent=None):
        super().__init__(parent)
        # Set the internal state
        self.state = None
        # Make the dialog stay on top
        self.setWindowFlags(data.Qt.WindowType.WindowStaysOnTopHint)
        # Set the dialog icon and title
        self.setWindowIcon(data.QIcon(data.application_icon))
        self.setWindowTitle(dialog_type.title())
        self.init_layout(text, dialog_type)
        # Set default font
        self.setFont(data.get_current_font())
        # Update style
        self.update_style()
    
    def create_button_list(self):
        return (
            {
                "name": "yes",
                "text": "Yes",
                "icon": None,
                "size": (data.standard_button_size, data.standard_button_size),
                "tooltip": "Confirm the action",
                "click-func": lambda *args: self.done(data.DialogResult.Yes.value),
            },
            {
                "name": "no",
                "text": "No",
                "icon": None,
                "size": (data.standard_button_size, data.standard_button_size),
                "tooltip": "Decline the action",
                "click-func": lambda *args: self.done(data.DialogResult.No.value),
            },
        )
    
    def init_layout(self, text, dialog_type):
        self.button_cache = {}
        
        # Create the main layout
        main_layout = create_layout(
            layout=LayoutType.Vertical,
            margins=(8,8,8,8),
            spacing=4
        )
        self.setLayout(main_layout)
        
        # Add the label
        label = data.QLabel(self)
        label.setWordWrap(True)
        label.setAlignment(data.Qt.AlignmentFlag.AlignCenter)
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
                        data.QSize(
                            int(button["size"][0] * 0.8),
                            int(button["size"][1] * 0.8)
                        )
                    )
            new_button.setToolTip(button["tooltip"])
            new_button.setStatusTip(button["tooltip"])
            new_button.set_click_function(button["click-func"])
#            new_button.set_enter_function(
#                create_enter_func(button.function_text, button.font)
#            )
#            new_button.set_leave_function(
#                create_leave_func(button.font)
#            )
            if button["size"] is not None:
                new_button.setFixedSize(
                    data.QSize(
                        int(button["size"][0]),
                        int(button["size"][1])
                    )
                )
            
            button_layout.addWidget(new_button)
            self.button_cache[button["name"]] = new_button
        
        self.setWindowFlags(data.Qt.WindowType.FramelessWindowHint)
    
    def showEvent(self, event):
        super().showEvent(event)
        self.center()
    
    def state_on(self):
        self.state = True
        self.button_cache["no"].set_focused(False)
        self.button_cache["yes"].set_focused(True)
    
    def state_off(self):
        self.state = False
        self.button_cache["no"].set_focused(True)
        self.button_cache["yes"].set_focused(False)
    
    def state_reset(self):
        self.state = None
        self.button_cache["no"].set_focused(False)
        self.button_cache["yes"].set_focused(False)
    
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
        if pressed_key == data.Qt.Key.Key_Escape:
            self.button_cache["no"].set_focused(True)
            self.repaint()
            time.sleep(0.1)
            self.done(data.DialogResult.No.value)
        elif pressed_key == data.Qt.Key.Key_Right:
            self.state_off()
        elif pressed_key == data.Qt.Key.Key_Left:
            self.state_on()
        elif pressed_key == data.Qt.Key.Key_Enter or pressed_key == data.Qt.Key.Key_Return:
            if self.state == True:
                self.done(data.DialogResult.Yes.value)
            elif self.state == False:
                self.done(data.DialogResult.No.value)
    
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
        for k,v in self.button_cache.items():
            v.update_style()
    
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

class OkDialog(YesNoDialog):
    def create_button_list(self):
        return (
            {
                "name": "ok",
                "text": "OK",
                "icon": None,
                "size": (data.standard_button_size, data.standard_button_size),
                "tooltip": "Close the dialog window",
                "click-func": lambda *args: self.done(data.DialogResult.No.value),
            },
        )
    
    def keyPressEvent(self, key_event):
        pressed_key = key_event.key()
        # Check for escape keypress
        if pressed_key == data.Qt.Key.Key_Escape:
            self.button_cache["ok"].set_focused(True)
            self.repaint()
            time.sleep(0.1)
            self.done(data.DialogResult.No.value)
        elif pressed_key == data.Qt.Key.Key_Left or pressed_key == data.Qt.Key.Key_Right:
            self.state_off()
        # Check for Enter/Return keypress
        elif pressed_key == data.Qt.Key.Key_Enter or pressed_key == data.Qt.Key.Key_Return:
            self.done(data.DialogResult.No.value)

class QuitDialog(YesNoDialog):
    def create_button_list(self):
        return (
            {
                "name": "save-and-quit",
                "text": "Save all\n&& Quit",
                "icon": None,
                "size": (int(data.standard_button_size*1.5), data.standard_button_size),
                "tooltip": "Quit ExCo",
                "click-func": lambda *args: self.done(data.DialogResult.SaveAllAndQuit.value),
            },
            {
                "name": "quit",
                "text": "Quit",
                "icon": None,
                "size": (data.standard_button_size, data.standard_button_size),
                "tooltip": "Quit ExCo",
                "click-func": lambda *args: self.done(data.DialogResult.Quit.value),
            },
            {
                "name": "cancel",
                "text": "Cancel",
                "icon": None,
                "size": (data.standard_button_size, data.standard_button_size),
                "tooltip": "Cancel quitting ExCo",
                "click-func": lambda *args: self.done(data.DialogResult.No.value),
            },
        )
    
    def __set_button_states(self,
                            button_save_and_quit,
                            button_quit,
                            button_no):
        self.button_cache["save-and-quit"].set_focused(button_save_and_quit)
        self.button_cache["quit"].set_focused(button_quit)
        self.button_cache["cancel"].set_focused(button_no)
    
    def state_cycle_right(self):
        if self.state == data.DialogResult.SaveAllAndQuit.value:
            self.state = data.DialogResult.Quit.value
            self.__set_button_states(False, True, False)
        else:
            self.state = data.DialogResult.No.value
            self.__set_button_states(False, False, True)
    
    def state_cycle_left(self):
        if self.state == data.DialogResult.No.value:
            self.state = data.DialogResult.Quit.value
            self.__set_button_states(False, True, False)
        else:
            self.state = data.DialogResult.SaveAllAndQuit.value
            self.__set_button_states(True, False, False)
    
    def keyPressEvent(self, key_event):
        pressed_key = key_event.key()
        # Check for escape keypress
        if pressed_key == data.Qt.Key.Key_Escape:
            self.button_cache["cancel"].set_focused(True)
            self.repaint()
            time.sleep(0.1)
            self.done(data.DialogResult.No.value)
        elif pressed_key == data.Qt.Key.Key_Left:
            self.state_cycle_left()
        elif pressed_key == data.Qt.Key.Key_Right:
            self.state_cycle_right()
        # Check for Enter/Return keypress
        elif pressed_key == data.Qt.Key.Key_Enter or pressed_key == data.Qt.Key.Key_Return:
            if self.state is None:
                self.state = data.DialogResult.No.value
            self.done(self.state)