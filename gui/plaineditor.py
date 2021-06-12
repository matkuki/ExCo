
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2019 Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import os
import sys
import itertools
import inspect
import functools
import keyword
import re
import collections
import textwrap
import importlib
import data
import components
import themes
import functions
import interpreter
import settings
import lexers
import traceback
import gc

from .contextmenu import *
from .baseeditor import *

"""
-----------------------------
Subclassed QScintilla widget used for displaying REPL messages, Python/C node trees, ...
-----------------------------
""" 
class PlainEditor(BaseEditor):
    # Class variables
    name            = None
    _parent         = None
    main_form       = None
    current_icon    = None
    icon_manipulator= None
    savable         = data.CanSave.NO
    # Reference to the custom context menu
    context_menu    = None
    """Namespace references for grouping functionality"""
    hotspots        = None

    
    def clean_up(self):
        self.hotspots = None
        try:
            # Clean up the lexer
            self.lexer().setParent(None)
            self.setLexer(None)
        except:
            pass
        try:
            # REPL MESSAGES only clean up
            self.main_form.repl_messages_tab = None
        except:
            pass
        # Clean up the decorated mouse press event
        self.mousePressEvent = None
        # Clean up references
        self._parent = None
        self.main_form = None
        self.icon_manipulator = None
        # Destroy self
        self.setParent(None)
        self.deleteLater()
    
    def __init__(self, parent, main_form):
        # Initialize the superclass
        super().__init__()
        # Initialize components
        self.icon_manipulator = components.IconManipulator(self, parent)
        self.add_corner_buttons()
        # Store the main form and parent widget references
        self._parent = parent
        self.main_form = main_form
        # Set font family and size
        self.setFont(settings.Editor.font)
        # Set encoding format to UTF-8 (Unicode)
        self.setUtf8(True)
        # Tabs are spaces by default
        self.setIndentationsUseTabs(False)
        # Set line endings to be Unix style ("\n")
        self.setEolMode(settings.Editor.end_of_line_mode)
        # Initialize the namespace references
        self.hotspots = components.Hotspots()
        # Set the initial zoom factor
        self.zoomTo(settings.Editor.zoom_factor)
        # Set the theme
        self.set_theme(data.theme)
    
    def add_corner_buttons(self):
        def clear():
            self.main_form.display.repl_clear_tab()
        # Clear messages
        self.icon_manipulator.add_corner_button(
            "tango_icons/edit-clear.png",
            "Clear messages",
            clear
        )
    
    def delete_context_menu(self):
        # Clean up the context menu
        if self.context_menu != None:
            self.context_menu.hide()
            for b in self.context_menu.button_list:
                b.setParent(None)
            self.context_menu.setParent(None)
            self.context_menu = None
    
    def contextMenuEvent(self, event):
        # Built-in context menu
#        super().contextMenuEvent(event)
        self.delete_context_menu()
        # Show a context menu according to the current lexer
        offset = (event.x(), event.y())
        self.context_menu = ContextMenu(
            self, self.main_form, offset
        )
        self.context_menu.create_plain_buttons()
        self.context_menu.show()
        event.accept()
    
    def mousePressEvent(self, event):
        """Overloaded mouse click event"""
        #Execute the superclass mouse click event
        super().mousePressEvent(event)
        #Set focus to the clicked editor
        self.setFocus()
        #Set the last focused widget to the parent basic widget
        self.main_form.last_focused_widget = self._parent
        data.print_log(
            "Stored \"{}\" as last focused widget".format(self._parent.name)
        )
        #Hide the function wheel if it is shown
        self.main_form.view.hide_all_overlay_widgets()
        # Reset the click&drag context menu action
        components.ActionFilter.clear_action()
    
    def setFocus(self):
        """Overridden focus event"""
        #Execute the supeclass focus function
        super().setFocus()
        #Check indication
        self.main_form.view.indication_check()
    
    def goto_line(self, line_number):
        """Set focus and cursor to the selected line"""
        #Move the cursor to the start of the selected line
        self.setCursorPosition(line_number, 0)
        #Move the first displayed line to the top of the viewving area
        self.SendScintilla(
            data.QsciScintillaBase.SCI_GOTOLINE, 
            line_number
        )
    
    def convert_case(self, uppercase=False):
        """Convert selected text in the scintilla document into the selected case letters"""
        #Get the start and end point of the selected text
        start_line, start_index,  end_line, end_index = self.getSelection()
        #Get the currently selected text
        selected_text   = self.selectedText()
        #Convert it to the selected case
        if uppercase == False:
            selected_text   = selected_text.lower()
        else:
            selected_text   = selected_text.upper()
        #Replace the selection with the new upercase text
        self.replaceSelectedText(selected_text)
        #Reselect the previously selected text
        self.setSelection(start_line, start_index,  end_line, end_index)
    
    def set_theme(self, theme):
        # Set the lexer
        self.setLexer(lexers.Text(self))
        # Run the super-class method
        super().set_theme(theme)


