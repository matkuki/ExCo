# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-present Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import os
import os.path
import functools

import qt
import data
import constants
import functions
import themes

from .menu import *

class ReplIndicator(qt.QLabel):
    ICONS = {
        constants.ReplLanguage.Python: "language_icons/logo_python.png",
        constants.ReplLanguage.Hy: "language_icons/logo_hy_cuddles.png",
    }
    TOOLTIPS = {
        constants.ReplLanguage.Python: "Python programming language",
        constants.ReplLanguage.Hy: "Hy programming language, a LISP dialect",
    }
    
    selection_menu = None
    
    def __init__(self, parent, main_form, repl_box):
        # Initialize superclass
        super().__init__(parent)
        # Store the reference to the parent
        self._parent = parent
        self.main_form = main_form
        self.repl_box = repl_box
        # Initialize the menu
        self.init_selection_menu()
        # Set default font
        self.setFont(data.get_current_font())
    
    def mouseReleaseEvent(self, event):
        # Execute the superclass event method
        super().mouseReleaseEvent(event)
        cursor = qt.QCursor.pos()
        self.selection_menu.popup(cursor)
    
    def init_selection_menu(self):
        """
        Initialization of the REPL type menu used by the REPL indicator
        """
        
        if self.selection_menu is not None:
            # Clear the menu actions from memory
            self.selection_menu.clear()
            for action in self.selection_menu.actions():
                self.selection_menu.removeAction(action)
                action.setParent(None)
                action.deleteLater()
                action = None
        self.selection_menu = Menu(self)
        # Add the menu label
        action_theme = qt.QAction("Select interpreter:", self.selection_menu)
        action_theme.setEnabled(False)
        self.selection_menu.addAction(action_theme)
        # Add the type actions
        for lang in constants.ReplLanguage:
            action_theme = qt.QAction(lang.name, self.selection_menu)
            action_theme.triggered.connect(
                functools.partial(self.choose_repl_type, lang)
            )
            icon = functions.create_icon(self.ICONS[lang])
            action_theme.setIcon(icon)
            action_theme.setToolTip(self.TOOLTIPS[lang])
            self.selection_menu.addAction(action_theme)
    
    def set_image(self, image):
        raw_picture = qt.QPixmap(os.path.join(data.resources_directory, image))
        picture = raw_picture.scaled(16, 16, qt.Qt.AspectRatioMode.KeepAspectRatio)
        self.setPixmap(picture)
    
    def set_language(self, lang):
        self.set_image(self.ICONS[lang])
        self.setToolTip(lang.name)
    
    def choose_repl_type(self, lang):
        self.repl_box.set_repl(self.repl_box.repl_state, lang)
        self.set_language(lang)
    
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
