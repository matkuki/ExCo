
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2023 Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import os
import os.path
import functools

import data
import functions
import themes

from .menu import *

class ThemeIndicator(data.QLabel):
    theme_menu = None
    
    def __init__(self, parent, main_form):
        # Initialize superclass
        super().__init__(parent)
        # Store the reference to the parent
        self._parent = parent
        self.main_form = main_form
        # Initialize the menu
        self.init_theme_menu()
        # Set default font
        self.setFont(data.get_current_font())
    
    def mouseReleaseEvent(self, event):
        # Execute the superclass event method
        super().mouseReleaseEvent(event)
        cursor = data.QCursor.pos()
        self.theme_menu.popup(cursor)
    
    def init_theme_menu(self):
        """
        Initialization of the theme menu used by the theme indicator
        """
        def choose_theme(theme):
            data.theme = themes.get(theme["name"])
            self.main_form.view.refresh_theme()
            self.main_form.display.update_theme_taskbar_icon()
            current_theme = data.theme["name"]
            self.main_form.display.repl_display_message(
                "Changed theme to: {}".format(current_theme), 
                message_type=data.MessageType.SUCCESS
            )
        
        if self.theme_menu is not None:
            # Clear the menu actions from memory
            self.theme_menu.clear()
            for action in self.theme_menu.actions():
                self.theme_menu.removeAction(action)
                action.setParent(None)
                action.deleteLater()
                action = None
        self.theme_menu = Menu(self)
        # Add the theme actions
        for theme in themes.get_all():
            action_theme = data.QAction(theme["name"], self.theme_menu)
            action_theme.triggered.connect(
                functools.partial(choose_theme, theme)
            )
            icon = functions.create_icon(theme["image-file"])
            action_theme.setIcon(icon)
            self.theme_menu.addAction(action_theme)
    
    def set_image(self, image):
        raw_picture = data.QPixmap(
            os.path.join(
                data.resources_directory, image
            )
        )
        picture = raw_picture.scaled(16, 16, data.Qt.AspectRatioMode.KeepAspectRatio)
        self.setPixmap(picture)
    
    def restyle(self):
        self.setStyleSheet("""
QLabel { 
    background-color: transparent;
    border: none;
    padding-top: 0px;
    padding-bottom: 0px;
    padding-left: 0px;
    padding-right: 4px;
}
        """)
