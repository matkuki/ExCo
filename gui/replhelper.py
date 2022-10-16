
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2021 Matic Kukovec.
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

from .customeditor import *
from .tabwidget import *


"""
-----------------------------------------------------
Scintilla class for inputting more than one line into the REPL
-----------------------------------------------------
"""
class ReplHelper(data.QsciScintilla):
    """
    REPL scintilla box for inputting multiple lines into the REPL.
    MUST BE PAIRED WITH A ReplLineEdit OBJECT!
    """
    #Class variables
    _parent         = None
    main_form         = None
    repl_master     = None
    #The scintilla api object(data.QsciAPIs) must be an instace variable, or the underlying c++
    #mechanism deletes the object and the autocompletions compiled with api.prepare() are lost
    api             = None
    #Attribute for indicating if the REPL helper is indicated
    indicated       = False
    # Reference to the custom context menu
    context_menu    = None
    #LineList object copied from the CustomEditor object
    line_list       = None
    
    """
    Built-in and private functions
    """
    def __init__(self, parent, main_form, repl_master):
        #Initialize superclass, from which the current class is inherited, THIS MUST BE DONE SO THAT THE SUPERCLASS EXECUTES ITS __init__ !!!!!!
        super().__init__(parent)
        # Set default font
        self.setFont(data.get_editor_font())
        #Save the reference to the parent(main window)
        self._parent = parent
        self.main_form = main_form
        #Save the reference to the REPL object
        self.repl_master = repl_master
        #Hide the horizontal and show the vertical scrollbar
        self.SendScintilla(data.QsciScintillaBase.SCI_SETVSCROLLBAR, True)
        self.SendScintilla(data.QsciScintillaBase.SCI_SETHSCROLLBAR, False)
        #Hide the margin
        self.setMarginWidth(1, 0)
        #Autoindentation enabled when using "Enter" to indent to the same level as the previous line
        self.setAutoIndent(True)
        #Tabs are spaces by default
        self.setIndentationsUseTabs(False)
        #Set tab space indentation width
        self.setTabWidth(settings.editor['tab_width'])
        #Set encoding format to UTF-8 (Unicode)
        self.setUtf8(True)
        #Set brace matching
        self.setBraceMatching(data.QsciScintilla.BraceMatch.SloppyBraceMatch)
        self.setMatchedBraceBackgroundColor(data.QColor(255, 153, 0))
        #Tabs are spaces by default
        self.setIndentationsUseTabs(False)
        #Set backspace to delete by tab widths
        self.setBackspaceUnindents(True)
        #Disable drops
        self.setAcceptDrops(False)
        #Set line endings to be Unix style ("\n")
        self.setEolMode(data.QsciScintilla.EolMode(settings.editor['end_of_line_mode']))
        #Set the initial zoom factor
        self.zoomTo(settings.editor['zoom_factor'])
        """
        Functionality copied from the CustomEditor to copy some of 
        the neede editing functionality like commenting, ...
        """
        # Add the attributes needed to implement the line nist
        self.line_list = components.LineList(self, self.text())
        # Add the needed functions assigned from the CustomEditor
        self.set_theme = functools.partial(CustomEditor.set_theme, self)
        self.set_line = functools.partial(CustomEditor.set_line, self)
        self.set_lines = functools.partial(CustomEditor.set_lines, self)
        self.toggle_comment_uncomment = functools.partial(CustomEditor.toggle_comment_uncomment, self)
        self.comment_line = functools.partial(CustomEditor.comment_line, self)
        self.comment_lines = functools.partial(CustomEditor.comment_lines, self)
        self.uncomment_line = functools.partial(CustomEditor.uncomment_line, self)
        self.uncomment_lines = functools.partial(CustomEditor.uncomment_lines, self)
        self.prepend_to_line = functools.partial(CustomEditor.prepend_to_line, self)
        self.prepend_to_lines = functools.partial(CustomEditor.prepend_to_lines, self)
        self.replace_line = functools.partial(CustomEditor.replace_line, self)
        self.get_line = functools.partial(CustomEditor.get_line, self)
        self.check_line_numbering = functools.partial(CustomEditor.check_line_numbering, self)
        self.text_to_list = functools.partial(CustomEditor.text_to_list, self)
        self.list_to_text = functools.partial(CustomEditor.list_to_text, self)
        # Add the function and connect the signal to update the line/column positions
        self.cursorPositionChanged.connect(self._signal_editor_cursor_change)
        #Set the lexer to python
        self.set_lexer()
        #Set the initial autocompletions
        self.update_autocompletions()
        #Setup the LineList object that will hold the custom editor text as a list of lines
        self.line_list = components.LineList(self, self.text())
        self.textChanged.connect(self.text_changed)
    
    def _signal_editor_cursor_change(self, cursor_line=None, cursor_column=None):
        """Signal that fires when cursor position changes"""
        self.main_form.display.update_cursor_position(cursor_line, cursor_column)
    
    def _filter_keypress(self, key_event):
        """Filter keypress for appropriate action"""
        pressed_key = key_event.key()
        accept_keypress = False
        #Get key modifiers and check if the Ctrl+Enter was pressed
        key_modifiers = data.QApplication.keyboardModifiers()
        if ((key_modifiers == data.Qt.KeyboardModifier.ControlModifier and pressed_key == data.Qt.Key.Key_Return) or
            pressed_key == data.Qt.Key.Key_Enter):
                #ON MY KEYBOARD Ctrl+Enter CANNOT BE DETECTED!
                #Qt.ControlModifier  MODIFIER SHOWS FALSE WHEN USING data.QApplication.keyboardModifiers() + Enter
                self.repl_master.external_eval_request(self.text(), self)
                accept_keypress = True
        return accept_keypress
    
    def _filter_keyrelease(self, key_event):
        """Filter keyrelease for appropriate action"""
        #Only check indication if the current widget is not indicated
        if self.indicated == False:
            #Check indication
            self.main_form.view.indication_check()
        return False

    """
    Qt QSciScintilla functions
    """
    def keyPressEvent(self, event):
        """QScintila keyPressEvent, to catch which key was pressed"""       
        #Filter the event
        if self._filter_keypress(event) == False:
            #Execute the superclass method, if the filter ignored the event
            super().keyPressEvent(event)
    
    def keyReleaseEvent(self, event):
        """QScintila KeyReleaseEvent, to catch which key was released"""
        #Execute the superclass method first, the same trick as in __init__ !
        super().keyReleaseEvent(event)
        #Filter the event
        self._filter_keyrelease(event)
    
    def mousePressEvent(self, event):
        # Execute the superclass mouse click event
        super().mousePressEvent(event)
        # Reset the main forms last focused widget
        self.main_form.last_focused_widget = None
        # Set focus to the clicked helper
        self.setFocus()
        # Hide the function wheel if it is shown
        self.main_form.view.hide_all_overlay_widgets()
        # Need to set focus to self or the repl helper doesn't get focused,
        # don't know why?
        self.setFocus()
        # Reset the click&drag context menu action
        components.ActionFilter.clear_action()
    
    def setFocus(self):
        """Overridden focus event"""
        # Execute the supeclass focus function
        super().setFocus()
        # Check indication
        self.main_form.view.indication_check()
    
    def wheelEvent(self, wheel_event):
        """Overridden mouse wheel rotate event"""
        key_modifiers = data.QApplication.keyboardModifiers()
        if data.PYQT_MODE == 4:
            delta = wheel_event.delta()
        else:
            delta = wheel_event.angleDelta().y()
        if delta < 0:
            if key_modifiers == data.Qt.KeyboardModifier.ControlModifier:
                #Zoom out the scintilla tab view
                self.zoomOut()
        else:
            if key_modifiers == data.Qt.KeyboardModifier.ControlModifier:
                #Zoom in the scintilla tab view
                self.zoomIn()
        #Handle the event
        if key_modifiers != data.Qt.KeyboardModifier.ControlModifier:
            #Execute the superclass method
            super().wheelEvent(wheel_event)
        else:
            #Propagate(send forward) the wheel event to the parent
            wheel_event.ignore()
    
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
        self.delete_context_menu()
        # Show a context menu according to the current lexer
        offset = (event.x(), event.y())
        self.context_menu = ContextMenu(
            self, self.main_form, offset
        )
        height = self.size().height()
        if height < 100:
            self.context_menu.create_horizontal_multiline_repl_buttons()
        else:
            self.context_menu.create_multiline_repl_buttons()
        self.context_menu.show()
        event.accept()
    
    def set_lexer(self):
        if self.lexer() != None:
            self.lexer().setParent(None)
            self.setLexer(None)
        # Create the new lexer
        lexer = lexers.Python()
        lexer.setParent(self)
        result = lexers.get_comment_style_for_lexer(lexer)
        lexer.open_close_comment_style = result[0]
        lexer.comment_string = result[1]
        lexer.end_comment_string = result[2]
        #Set the lexers default font
        lexer.setDefaultFont(data.get_editor_font())
        #Set the lexer with the initial autocompletions
        self.setLexer(lexer)
        #Set the theme
        self.set_theme(data.theme)
        self.lexer().set_theme(data.theme)
    
    def refresh_lexer(self):
        #Set the theme
        self.set_theme(data.theme)
        self.lexer().set_theme(data.theme)
    
    def text_changed(self):
        """Event that fires when the scintilla document text changes"""
        #Update the line list
        self.line_list.update_text_to_list(self.text())
        
    
    """
    ReplHelper autocompletion functions
    """
    def update_autocompletions(self, new_autocompletions=[]):
        """Function for updating the ReplHelper autocompletions"""
        #Set the lexer
        self.refresh_lexer()
        #Set the scintilla api for the autocompletions (MUST BE AN INSTANCE VARIABLE)
        self.api = data.QsciAPIs(self.lexer())
        #Populate the api with all of the python keywords
        for kw in keyword.kwlist:
            self.api.add(kw)
        for word in new_autocompletions:
            self.api.add(word)
        self.api.prepare()
        #Set how many characters must be typed for the autocompletion popup to appear
        self.setAutoCompletionThreshold(1)
        #Set the source from where the autocompletions will be fetched
        self.setAutoCompletionSource(data.QsciScintilla.AutoCompletionSource.AcsAll)
        #Set autocompletion case sensitivity
        self.setAutoCompletionCaseSensitivity(False)


