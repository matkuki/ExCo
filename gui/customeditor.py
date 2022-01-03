
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
from .dialogs import *
from .baseeditor import *


"""
---------------------------------------------
Subclassed QScintilla widget used for editing
---------------------------------------------
""" 
class CustomEditor(BaseEditor):
    """
    QScintilla widget with added custom functions
    
    COMMENT:    
        Functions treat items as if the starting index is 1 instead of 0!
        It's a little confusing at first, but you will get the hang of it.
        This is done because scintilla displays line numbers from index 1.
    """
    # Class variables
    _parent                 = None
    main_form               = None
    name                    = ""
    save_name               = ""
    save_status             = data.FileStatus.OK
    savable                 = data.CanSave.NO
    embedded                = False
    # Current document type, initialized to text
    current_file_type       = "TEXT"
    # Current tab icon
    current_icon            = None
    icon_manipulator        = None
    # Comment character/s that will be used in comment/uncomment functions
    comment_string          = None
    # Oberon/Modula-2/CP have the begin('(*')/end('*)') commenting style,
    # set the attribute to signal this commenting style and the beginning
    # and end commenting string
    open_close_comment_style    = False
    end_comment_string      = None
    # Indicator enumerations
    HIGHLIGHT_INDICATOR     = 0
    FIND_INDICATOR          = 2
    REPLACE_INDICATOR       = 3
    SELECTION_INDICATOR     = 4
    # Line strings in a list, gets updated on every text change,
    # can be used like any other python list(append, extend, reverse, ...)
    line_list               = None
    # List that holds the line numbers, gets updated on every text change
    line_count              = None
    # Reference to the custom context menu
    context_menu            = None
    # Selection anti-recursion lock
    selection_lock          = None
    """Namespace references for grouping functionality"""
    hotspots                = None
    bookmarks               = None
    keyboard                = None
    

    """
    Built-in and private functions
    """
    def clean_up(self):
        # Clean up references
        self.line_list.parent = None
        self.line_list._clear()
        self._parent = None
        self.main_form = None
        # Disconnect signals
        self.cursorPositionChanged.disconnect()
        self.marginClicked.disconnect()
        self.linesChanged.disconnect()
        # Clean up namespaces
        self.hotspots = None
        self.bookmarks.parent = None
        self.bookmarks = None
        self.keyboard.parent = None
        self.keyboard = None
        # Clean up special functions
        self.find = None
        self.save = None
        self.clear = None
        self.highlight = None
        # Clean up the corner widget
        self.current_icon = None
        self.icon_manipulator = None
        # Clear the lexer
        self.clear_lexer()
        # Clean up the context menu if necessary
        self.delete_context_menu()
        # Disengage self from the parent and clean up self
        self.setParent(None)
        self.deleteLater()
    
    def __init__(self, parent, main_form, file_with_path=None):
        """Initialize the scintilla widget"""
        # Initialize superclass, from which the current class is inherited,
        # THIS MUST BE DONE SO THAT THE SUPERCLASS EXECUTES ITS __init__ !!!!!!
        super().__init__(parent)
        # Set encoding format to UTF-8 (Unicode)
        self.setUtf8(True)
        # Set font family and size
        self.setFont(settings.Editor.font)
        # Set the margin type (0 is by default line numbers, 1 is for non code folding symbols and 2 is for code folding)
        self.setMarginType(0, data.QsciScintilla.NumberMargin)
        # Set margin width and font
        self.setMarginWidth(0, "00")
        self.setMarginsFont(settings.Editor.font)
        # Reset the modified status of the document
        self.setModified(False)
        # Set brace matching
        self.setBraceMatching(data.QsciScintilla.SloppyBraceMatch)
        self.setMatchedBraceBackgroundColor(settings.Editor.brace_color)
        # Autoindentation enabled when using "Enter" to indent to the same level as the previous line
        self.setAutoIndent(True)
        # Tabs are spaces by default
        self.setIndentationsUseTabs(False)
        # Set automatic adjustment of the horizontal scrollbar, if available
        try:
            self.setScrollWidthTracking(True)
        except:
            pass
        # Set tab space indentation width
        self.setTabWidth(settings.Editor.tab_width)
        # Set backspace to delete by tab widths
        self.setBackspaceUnindents(True)
        # Scintilla widget must not accept drag/drop events, the cursor freezes if it does!!!
        self.setAcceptDrops(False)
        # Set line endings to be Unix style ("\n")
        self.setEolMode(settings.Editor.end_of_line_mode)
        # Set the initial zoom factor
        self.zoomTo(settings.Editor.zoom_factor)
        # Correct the file name if it is unspecified
        if file_with_path == None:
            file_with_path = ""
        # Add attributes for status of the document (!!you can add attributes to objects that have the __dict__ attribute!!)
        self._parent     = parent
        self.main_form  = main_form
        self.name       = os.path.basename(file_with_path)
        # Set save name with path
        if os.path.dirname(file_with_path) != "":
            self.save_name  = file_with_path
        else:
            self.save_name  = ""
        # Replace back-slashes to forward-slashes on Windows
        if data.platform == "Windows":
            self.save_name  = self.save_name.replace("\\", "/")
        # Reset the file save status 
        self.save_status = data.FileStatus.OK
        # Enable saving of the scintilla document
        self.savable = data.CanSave.YES
        # Initialize instance variables
        self._init_special_functions()
        # Make second margin (the one to the right of the line number margin),
        # sensitive to mouseclicks
        self.setMarginSensitivity(1, True)
        # Add needed signals
        self.cursorPositionChanged.connect(
            self._parent._signal_editor_cursor_change
        )
        self.marginClicked.connect(self._margin_clicked)
        self.linesChanged.connect(self._lines_changed)
        self.selectionChanged.connect(self._selection_changed)
        # Initialize components
        self.icon_manipulator = components.IconManipulator(
            parent=self, tab_widget=parent
        )
        # Set the lexer to the default Plain Text
        self.choose_lexer("text")
        self.add_corner_buttons()
        # Setup autocompletion
        self.init_autocompletions()
        # Setup the LineList object that will hold the custom editor text as a list of lines
        self.line_list = components.LineList(self, self.text())
        # Reset the selection anti-recursion lock
        self.selection_lock = False
        # Bookmark initialization
        self._init_bookmark_marker()
        # Initialize the namespace references
        self.hotspots   = components.Hotspots()
        self.bookmarks  = self.Bookmarks(self)
        self.keyboard   = self.Keyboard(self)
        # Set cursor line visibility and color
        self.set_cursor_line_visibility(
            settings.Editor.cursor_line_visible
        )
        # Make last line scrollable to the top
        self.SendScintilla(self.SCI_SETENDATLASTLINE, False)
        # Enable multiple cursors and multi-cursor typing
        self.SendScintilla(self.SCI_SETMULTIPLESELECTION, True)
        self.SendScintilla(self.SCI_SETADDITIONALSELECTIONTYPING, True)
    
    def __setattr__(self, name, value):
        """
        Special/magic method that is called everytime an attribute of
        the CustomEditor class is set.
        """
        #Filter out the line_list attribute
        if name == "line_list":
            #Check if the assigned object is NOT a LineList object
            if isinstance(value, components.LineList) == False:
                #Check the extend value type
                if isinstance(value, list) == False:
                    raise Exception("Reassignment value of line_list must be a list!")
                elif all(isinstance(item, str) for item in value) == False:
                    raise Exception("All value list items must be strings!")
                text = self.list_to_text(value)
                self.set_all_text(text)
                self.line_list.update_text_to_list(text)
                #Cancel the assignment
                return
        #Call the superclasses/original __setattr__() special method
        super().__setattr__(name, value)
        
    def _init_special_functions(self):
        """Initialize the methods for document manipulation"""
        #Set references to the special functions
        self.find           = self.find_text
        self.save           = self.save_document
        self.clear          = self.clear_editor
        self.highlight      = self.highlight_text

    def _filter_keypress(self, key_event):
        """Filter keypress for appropriate action"""
        #pressed_key = key_event.key()
        accept_keypress = False
        return accept_keypress

    def _filter_keyrelease(self, key_event):
        """Filter keyrelease for appropriate action"""
        #released_key = key_event.key()
        accept_keyrelease = False
        return accept_keyrelease
    
    def _init_bookmark_marker(self):
        """Initialize the marker for the bookmarks"""
        image_scale_size = data.QSize(16, 16)
        bookmark_image  = functions.create_pixmap('tango_icons/bookmark.png')
        bookmark_image  = bookmark_image.scaled(image_scale_size)
        self.bookmark_marker = self.markerDefine(bookmark_image, 1)
    
    def _margin_clicked(self, margin, line, state):
        """Signal for a mouseclick on the margin"""
        #Adjust line index to the line list indexing (1..lines)
        adjusted_line = line + 1
        #Add/remove bookmark
        self.bookmarks.toggle_at_line(adjusted_line)
    
    def _lines_changed(self):
        """Signal that fires when the number of lines changes"""
        self.markerDeleteAll(self.bookmark_marker)
        bookmarks = self.main_form.bookmarks.marks
        for i in bookmarks:
            if bookmarks[i][0] == self:
                self.bookmarks.add_marker_at_line(bookmarks[i][1])
    
    selection_lock = False
    def _selection_changed(self):
        """
        Signal that fires when selected text changes
        """
        # This function seems to be asynchronous so a lock
        # is required in order to prevent recursive access to
        # Python's objects
        if CustomEditor.selection_lock == False:
            CustomEditor.selection_lock = True
            selected_text = self.selectedText()
            self.clear_selection_highlights()
            if selected_text.isidentifier():
                self._highlight_selected_text(
                    selected_text,
                    case_sensitive=False, 
                    regular_expression=True
                )
            CustomEditor.selection_lock = False
    
    def _skip_next_repl_focus(self):
        """
        Private function that is used to skip focusing the REPL after 
        executing a REPL command, which I use to skip the REPL focusing 
        when using the goto_line function for example.
        """
        #Disable REPL focus after the REPL evaluation
        self.main_form.repl.skip_next_repl_focus()
        #Set focus to the basic widget that holds this document
        self.main_form.view.set_window_focus(self._parent.name.lower())
    
    def add_corner_buttons(self):
        def show_lexer_menu():
            def set_lexer(lexer, lexer_name):
                try:
                    self.clear_lexer()
                    # Initialize and set the new lexer
                    lexer_instance = lexer()
                    self.set_lexer(lexer_instance, lexer_name)
                    # Change the corner widget (button) icon
                    self.icon_manipulator.update_corner_button_icon(
                        self.current_icon
                    )
                    self.icon_manipulator.update_icon(self)
                    # Display the lexer change
                    message = "Lexer changed to: {}".format(lexer_name)
                    self.main_form.display.repl_display_message(message)
                except Exception as ex:
                    print(ex)
                    message = "Error with lexer selection!\n"
                    message += "Select a window widget with an opened document first."
                    self.main_form.display.repl_display_message(
                        message, 
                        message_type=data.MessageType.ERROR
                    )
                    self.main_form.display.write_to_statusbar(message)
            lexers_menu = self.main_form.display.create_lexers_menu(
                "Change lexer", set_lexer
            )
            cursor = data.QCursor.pos()
            lexers_menu.popup(cursor)
            if data.custom_menu_scale != None:
                components.TheSquid.customize_menu_style(lexers_menu)
        # Edit session
        self.icon_manipulator.add_corner_button(
            self.current_icon,
            "Change the current lexer",
            show_lexer_menu
        )


    """
    Qt QSciScintilla functions
    """
    def keyPressEvent(self, event):
        """QScintila keyPressEvent, to catch which key was pressed"""
        # Hide the context menu if it is shown
        if self.context_menu != None:
            self.delete_context_menu()
        #Filter out TAB and SHIFT+TAB key combinations to override
        #the default indent/unindent functionality
        key = event.key()
#        char = event.text()
#        key_modifiers = data.QApplication.keyboardModifiers()
        if key == data.Qt.Key_Tab:
            self.custom_indent()
        elif key == data.Qt.Key_Backtab:
            self.custom_unindent()
        elif (key == data.Qt.Key_Enter or
              key == data.Qt.Key_Return):
            super().keyPressEvent(event)
            #Check for autoindent character list
            if hasattr(self.lexer(), "autoindent_characters"):
                line_number = self.get_line_number()
                #Check that the last line is valid
                if len(self.line_list[line_number-1]) == 0:
                    return
                elif len(self.line_list[line_number-1].rstrip()) == 0:
                    return
                last_character = self.line_list[line_number-1].rstrip()[-1]
                last_word = self.line_list[line_number-1].split()[-1].lower()
                if (last_character in self.lexer().autoindent_characters or
                    last_word in self.lexer().autoindent_characters):
                    line = self.line_list[line_number]
                    stripped_line = self.line_list[line_number].strip()
                    if stripped_line == "":
                        self.line_list[line_number] = (self.line_list[line_number] +
                                                       " " * settings.Editor.tab_width)
                        self.setCursorPosition(
                            line_number-1, 
                            len(self.line_list[line_number])
                        )
                    else:
                        whitespace = len(line) - len(line.lstrip())
                        self.line_list[line_number] = (" " * whitespace + 
                                                       " " * settings.Editor.tab_width + 
                                                       stripped_line)
                        #The line is not empty, move the cursor to the first
                        #non-whitespace character
                        self.setCursorPosition(
                            line_number-1, 
                            whitespace + settings.Editor.tab_width
                        )
        else:
            #Execute the superclass method first, the same trick as in __init__ !
            super().keyPressEvent(event)
            #Filter the event
            self._filter_keypress(event)

    def keyReleaseEvent(self, event):
        """QScintila KeyReleaseEvent, to catch which key was released"""
        #Execute the superclass method first, the same trick as in __init__ !
        super().keyReleaseEvent(event)
        #Filter the event
        self._filter_keyrelease(event)

    def mousePressEvent(self, event):
        """Overloaded mouse click event"""
        # Execute the superclass method first, the same trick as in __init__ !
        super().mousePressEvent(event)
        # Set focus to the clicked editor
        self.setFocus()
        # Set Save/SaveAs buttons in the menubar
        self._parent._set_save_status()
        # Update the cursor positions in the statusbar
        line = self.getCursorPosition()[0]
        column = self.getCursorPosition()[1]
        index = self.positionFromLineIndex(line, column)
        self.main_form.display.update_cursor_position(line, column, index)
        # Set the last focused widget to the parent basic widget
        self.main_form.last_focused_widget = self._parent
        data.print_log("Stored \"{}\" as last focused widget".format(self._parent.name))
        # Hide the function wheel if it is shown
        self.main_form.view.hide_all_overlay_widgets()
        # Hide the context menu if it is shown
        if self.context_menu != None:
            self.delete_context_menu()
        # Reset the click&drag context menu action
        components.ActionFilter.clear_action()
    
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
        # If the parent is a text differ return from this function
        if hasattr(self, "actual_parent"):
            return
        self.delete_context_menu()
        # Show a context menu according to the current lexer
        offset = (event.x(), event.y())
        self.context_menu = ContextMenu(
            self, self.main_form, offset
        )
        lexer = self.lexer()
#        if (self.current_file_type == "C" or
#            isinstance(lexer, lexers.Python) or
#            isinstance(lexer, lexers.CustomPython) or
#            (hasattr(lexer, "get_name") and lexer.get_name() == "Nim")):
#                self.context_menu.create_special_buttons()
#                self.context_menu.show()
#        else:
#            if self.getSelection() != (-1,-1,-1,-1):
#                self.context_menu.create_standard_buttons()
#                self.context_menu.show()
#            else:
#                self.context_menu.create_standard_buttons()
#                self.context_menu.show()
        self.context_menu.create_special_buttons()
        self.context_menu.show()
        event.accept()

    def wheelEvent(self, event):
        """Mouse scroll event of the custom editor"""
        key_modifiers = data.QApplication.keyboardModifiers()
        if key_modifiers != data.Qt.ControlModifier:
            #Execute the superclass method
            super().wheelEvent(event)
        else:
            #Ignore the event, it will be propageted up to the parent objects
            event.ignore()

    def text_changed(self):
        """Event that fires when the scintilla document text changes"""
        #Update the line list
        self.line_list.update_text_to_list(self.text())
        #Update the line count list with a list comprehention
        self.line_count = [line for line in range(1, self.lines()+1)]
        #Execute the parent basic widget signal
        self._parent._signal_text_changed()
    
    def setFocus(self):
        """Overridden focus event"""
        #Execute the supeclass focus function
        super().setFocus()
        #Check the save button status of the menubar
        self._parent._set_save_status()
        #Check indication
        self.main_form.view.indication_check()

    """
    Line manipulation functions
    """
    def goto_line(self, line_number, skip_repl_focus=True):
        """Set focus and cursor to the selected line"""
        #Check if the selected line is within the line boundaries of the current document
        line_number = self.check_line_numbering(line_number)
        #Move the cursor to the start of the selected line
        self.setCursorPosition(line_number, 0)
        #Move the first displayed line to the top of the viewing area minus an offset
        self.set_first_visible_line(line_number - 10)
        #Disable REPL focus after the REPL evaluation
        if skip_repl_focus == True:
            self._skip_next_repl_focus()
    
    def goto_index(self, index):
        self.SendScintilla(self.SCI_GOTOPOS, index)
        line, line_index = self.lineIndexFromPosition(index)
        self.set_first_visible_line(line - 10)
        self.setFocus()
    
    def set_first_visible_line(self, line_number):
        """Move the top of the viewing area to the selected line"""
        if line_number < 0:
            line_number = 0
        self.SendScintilla(
            data.QsciScintillaBase.SCI_SETFIRSTVISIBLELINE, 
            line_number
        )

    def remove_line(self, line_number):
        """Remove a line from the custom editor"""
        #Check if the selected line is within the line boundaries of the current document
        line_number = self.check_line_numbering(line_number)
        #Select the whole line text, "tab.lineLength(line_number)" doesn't work because a single UTF-8 character has the length of 2
        self.setSelection(line_number, 0, line_number+1, 0)
        #Replace the line with an empty string
        self.replaceSelectedText("")
    
    def replace_line(self, replace_text, line_number):
        """
        Replace an entire line in a scintilla document
            - line_number has to be as displayed in a QScintilla widget, which is ""from 1 to number_of_lines""
        """
        #Check if the selected line is within the line boundaries of the current document
        line_number = self.check_line_numbering(line_number)
        #Select the whole line text, "tab.lineLength(line_number)" doesn't work because a single UTF-8 character has the length of 2
        self.setSelection(line_number, 0, line_number+1, 0)
        #Replace the selected text with the new
        if "\n" in self.selectedText() or "\r\n" in self.selectedText():
            self.replaceSelectedText(replace_text + "\n")
        else:
            #The last line, do not add the newline character
            self.replaceSelectedText(replace_text)

    def set_line(self, line_text, line_number):
        """Set the text of a line"""
        self.replace_line(line_text, line_number)
    
    def set_lines(self, line_from, line_to, list_of_strings):
        """
        Set the text of multiple lines in one operation.
        This function is almost the same as "prepend_to_lines" and "append_to_lines",
        they may be merged in the future.
        """
        #Check the boundaries
        if line_from < 0:
            line_from = 0
        if line_to < 0:
            line_to = 0
        #Select the text from the lines and test if line_to is the last line in the document
        if line_to == self.lines()-1:
            self.setSelection(line_from, 0, line_to, len(self.text(line_to)))
        else:
            self.setSelection(line_from, 0, line_to, len(self.text(line_to))-1)
        #Split get the selected lines and add them to a list
        selected_lines = []
        for i in range(line_from, line_to+1):
            selected_lines.append(self.text(i))
        #Loop through the list and replace the line text
        for i in range(len(selected_lines)):
            selected_lines[i] = list_of_strings[i]
        #Replace the selected text with the prepended list merged into one string
        self.replaceSelectedText(self.list_to_text(selected_lines))
        #Set the cursor to the beginning of the last set line
        self.setCursorPosition(line_to, 0)

    def set_all_text(self, text):
        """
        Set the entire scintilla document text with a single select/replace routine.
        This function was added, because "setText()" function from Qscintilla
        cannot be undone!
        """
        #Check if the text is a list of lines
        if isinstance(text, list):
            #Join the list items into one string with newline as the delimiter
            text = "\n".join(text)
        #Select all the text in the document
        self.setSelection(0,0,self.lines(),0)
        #Replace it with the new text
        self.replaceSelectedText(text)
    
    def get_line_number(self):
        """return the line on which the cursor is"""
        return self.getCursorPosition()[0] + 1

    def get_line(self, line_number):
        """Return the text of the selected line in the scintilla document"""
        line_text = self.text(line_number - 1)
        return line_text.replace("\n", "")

    def get_lines(self, line_from=None, line_to=None):
        """Return the text of the entire scintilla document as a list of lines"""
        #Check if boundaries are valid
        if line_from == None or line_to == None:
            return self.line_list
        else:
            #Slice up the line_list list according to the boundaries
            return self.line_list[line_from:line_to]
    
    def get_absolute_cursor_position(self):
        """
        Get the absolute cursor position using the line list
        NOTE:
            This function returns the actual length of characters,
            NOT the length of bytes!
        """
        return self.line_list.get_absolute_cursor_position()
    
    def append_to_line(self, append_text,  line_number):
        """Add text to the back of the line"""
        #Check if the appending text is valid
        if append_text != "" and append_text != None:
            #Append the text, stripping the newline characters from the current line text
            self.replace_line(self.get_line(line_number).rstrip() + append_text, line_number)
    
    def append_to_lines(self, *args, **kwds):
        """Add text to the back of the line range"""
        #Check the arguments and keyword arguments
        appending_text = ""
        sel_line_from, sel_index_from, sel_line_to, sel_index_to = self.getSelection()
        if len(args) == 1 and isinstance(args[0], str) and (sel_line_from == sel_line_to):
            #Append text to all lines
            appending_text = args[0]
            line_from = 1
            line_to = self.lines()
        elif (len(args) == 3 and
              isinstance(args[0], str) and
              isinstance(args[1], int) and
              isinstance(args[2], int)):
            #Append text to specified lines
            appending_text  = args[0]
            line_from       = args[1]
            line_to         = args[2]
        elif sel_line_from != sel_line_to:
            #Append text to selected lines
            appending_text  = args[0]
            line_from       = sel_line_from + 1
            line_to         = sel_line_to + 1
        else:
            self.main_form.display.write_to_statusbar("Wrong arguments to 'append' function!", 1000)
            return
        #Check if the appending text is valid
        if appending_text != "" and appending_text != None:
            #Adjust the line numbers to standard(0..lines()) numbering
            line_from -= 1
            line_to  -= 1
            #Check the boundaries
            if line_from < 0:
                line_from = 0
            if line_to < 0:
                line_to = 0
            #Select the text from the lines
            self.setSelection(line_from, 0, line_to,  len(self.text(line_to).replace("\n", "")))
            #Split the line text into a list
            selected_lines = self.text_to_list(self.selectedText())
            #Loop through the list and prepend the prepend text
            for i in range(len(selected_lines)):
                selected_lines[i] = selected_lines[i] + appending_text
            #Replace the selected text with the prepended list merged into one string
            self.replaceSelectedText(self.list_to_text(selected_lines))
            # Select the appended lines, to enable consecutive prepending
            self.setSelection(
                line_from, 
                0, 
                line_to, 
                len(self.text(line_to))-1
            )
    
    def prepend_to_line(self, append_text, line_number):
        """Add text to the front of the line"""
        #Check if the appending text is valid
        if append_text != "" and append_text != None:
            #Prepend the text, stripping the newline characters from the current line text
            self.replace_line(
                append_text + self.get_line(line_number).rstrip(),
                line_number
            )
    
    def prepend_to_lines(self, *args, **kwds):
        """Add text to the front of the line range"""
        #Check the arguments and keyword arguments
        prepending_text = ""
        sel_line_from, sel_index_from, sel_line_to, sel_index_to = self.getSelection()
        if len(args) == 1 and isinstance(args[0], str) and (sel_line_from == sel_line_to):
            #Prepend text to all lines
            prepending_text = args[0]
            line_from = 1
            line_to = self.lines()
        elif (len(args) == 3 and 
              isinstance(args[0], str) and
              isinstance(args[1], int) and
              isinstance(args[2], int)):
            #Prepend text to specified lines
            prepending_text = args[0]
            line_from       = args[1]
            line_to         = args[2]
        elif sel_line_from != sel_line_to:
            #Prepend text to selected lines
            prepending_text  = args[0]
            line_from       = sel_line_from + 1
            line_to         = sel_line_to + 1
        else:
            self.main_form.display.write_to_statusbar("Wrong arguments to 'prepend' function!", 1000)
            return
        #Check if the appending text is valid
        if prepending_text != "" and prepending_text != None:
            # Adjust the line numbers to standard(0..lines()) numbering
            line_from   -= 1
            line_to     -= 1
            # Check the boundaries
            if line_from < 0:
                line_from = 0
            if line_to < 0:
                line_to = 0
            # Select the text from the lines
            self.setSelection(line_from, 0, line_to, len(self.text(line_to))-1)
            # Split the line text into a list
            selected_lines = self.text_to_list(self.selectedText())
            # Loop through the list and prepend the prepend text
            for i in range(len(selected_lines)):
                selected_lines[i] = prepending_text + selected_lines[i]
            # Replace the selected text with the prepended list merged into one string
            self.replaceSelectedText(self.list_to_text(selected_lines))
            # Select the prepended lines, to enable consecutive prepending
            self.setSelection(
                line_from, 
                0, 
                line_to, 
                len(self.text(line_to))-1 # -1 to offset the newline character ('\n')
            )

    def comment_line(self, line_number=None):
        """Comment a single line according to the currently set lexer"""
        if line_number == None:
            line_number = self.getCursorPosition()[0] + 1
        #Check commenting style
        if self.lexer().open_close_comment_style == True:
            self.prepend_to_line(self.lexer().comment_string, line_number)
            self.append_to_line(self.lexer().end_comment_string, line_number)
        else:
            self.prepend_to_line(self.lexer().comment_string, line_number)
        #Return the cursor to the commented line
        self.setCursorPosition(line_number-1, 0)

    def comment_lines(self, line_from=0, line_to=0):
        """Comment lines according to the currently set lexer"""
        if line_from == line_to:
            return
        else:
            #Check commenting style
            if self.lexer().open_close_comment_style == True:
                self.prepend_to_lines(self.lexer().comment_string, line_from, line_to)
                self.append_to_lines(self.lexer().end_comment_string, line_from, line_to)
            else:
                self.prepend_to_lines(self.lexer().comment_string, line_from, line_to)
            #Select the commented lines again, reverse the boundaries,
            #so that the cursor will be at the beggining of the selection
            line_to_length = len(self.line_list[line_to])
            self.setSelection(line_to-1, line_to_length, line_from-1, 0)

    def uncomment_line(self, line_number=None):
        """Uncomment a single line according to the currently set lexer"""
        if line_number == None:
            line_number = self.getCursorPosition()[0] + 1
        line_text       = self.get_line(line_number)
        #Check the commenting style
        if self.lexer().open_close_comment_style == True:
            if line_text.lstrip().startswith(self.lexer().comment_string):
                new_line = line_text.replace(self.lexer().comment_string, "", 1)
                new_line = functions.right_replace(new_line, self.lexer().end_comment_string, "", 1)
                self.replace_line(new_line, line_number)
                #Return the cursor to the uncommented line
                self.setCursorPosition(line_number-1, 0)
        else:
            if line_text.lstrip().startswith(self.lexer().comment_string):
                self.replace_line(line_text.replace(self.lexer().comment_string, "", 1), line_number)
                #Return the cursor to the uncommented line
                self.setCursorPosition(line_number-1, 0)

    def uncomment_lines(self, line_from, line_to):
        """Uncomment lines according to the currently set lexer"""
        if line_from == line_to:
            return
        else:
            # Select the lines
            selected_lines = self.line_list[line_from:line_to]
            # Loop through the list and remove the comment string if it's in front of the line
            for i in range(len(selected_lines)):
                # Check the commenting style
                if self.lexer().open_close_comment_style == True:
                    if selected_lines[i].lstrip().startswith(self.lexer().comment_string):
                        selected_lines[i] = selected_lines[i].replace(
                            self.lexer().comment_string, 
                            "", 
                            1
                        )
                        selected_lines[i] = functions.right_replace(
                            selected_lines[i], 
                            self.lexer().end_comment_string, 
                            "", 
                            1
                        )
                else:
                    if selected_lines[i].lstrip().startswith(self.lexer().comment_string):
                        selected_lines[i] = selected_lines[i].replace(self.lexer().comment_string, "", 1)
            # Replace the selected text with the prepended list merged into one string
            self.line_list[line_from:line_to] = selected_lines
            # Select the uncommented lines again, reverse the boundaries,
            # so that the cursor will be at the beggining of the selection
            line_to_length = len(self.line_list[line_to])
            self.setSelection(line_to-1, line_to_length, line_from-1, 0)
    
    def indent_lines_to_cursor(self):
        """
        Indent selected lines to the current cursor position in the document.
        P.S.:   Ex.Co. uses spaces as tabs by default, so if you copy text that
                contains tabs, the indent will not be correct unless you run the
                tabs_to_spaces function first!
        """
        #Get the cursor index in the current line and selected lines
        cursor_position     = self.getCursorPosition()
        indent_space        = cursor_position[1] * " "
        #Test if indenting one or many lines
        if self.getSelection() == (-1, -1, -1, -1):
            line_number = cursor_position[0] + 1
            line = self.line_list[line_number].lstrip()
            self.line_list[line_number] = indent_space + line
        else:
            #Get the cursor index in the current line and selected lines
            start_line_number   = self.getSelection()[0] + 1
            end_line_number     = self.getSelection()[2] + 1
            #Get the lines text as a list
            indented_lines = []
            line_list = self.get_lines(start_line_number, end_line_number)
            for i in range(len(line_list)):
                line = line_list[i].lstrip()
                indented_lines.append(indent_space + line)
            #Adjust the line numbers to standard(0..lines()) numbering
            start_line_number   -= 1
            end_line_number     -= 1
            #Select the text from the lines
            if end_line_number == (self.lines()-1):
                #The last selected line is at the end of the document,
                #select every character to the end.
                self.setSelection(start_line_number, 0, end_line_number, self.lineLength(end_line_number))
            else:
                self.setSelection(start_line_number, 0, end_line_number, self.lineLength(end_line_number)-1)
            #Replace the selected text with the prepended list merged into one string
            self.replaceSelectedText(self.list_to_text(indented_lines))
            #Move the cursor to the beggining of the restore line
            #to reset the document view to the beginning of the line
            self.setCursorPosition(cursor_position[0], 0)
            #Restore cursor back to the original position
            self.setCursorPosition(cursor_position[0], cursor_position[1])
    
    def custom_indent(self):
        """
        Scintila indents line-by-line, which is very slow for a large amount of lines. Try indenting 20000 lines.
        This is a custom indentation function that indents all lines in one operation.
        """
        tab_width = settings.Editor.tab_width
        # Check QScintilla's tab width
        if self.tabWidth() != tab_width:
            self.setTabWidth(tab_width)
        # Indent according to selection
        selection = self.getSelection()
        if selection == (-1, -1, -1, -1):
            line_number, position = self.getCursorPosition()
            # Adjust index to the line list indexing
            line_number += 1
            # Check if the indentation is the first function
            # that is exected in an empty editor
            if len(self.line_list) == 0:
                line_text = ""
            else:
                line_text = self.line_list[line_number]
            # Check if there is no text before the cursor position in the current line
            if line_text[:position].strip() == "":
                for i, ch in enumerate(line_text):
                    # Find the first none space character
                    if ch != " ":
                        diff = (tab_width - (i % tab_width))
                        adding_text = diff * " "
                        new_line = adding_text + line_text
                        self.line_list[line_number] = new_line
                        self.setCursorPosition(line_number-1, i+diff)
                        break
                else:
                    # No text in the current line
                    diff = (tab_width - (position % tab_width))
                    adding_text = diff * " "
                    new_line = line_text[:position] + adding_text + line_text[position:]
                    self.line_list[line_number] = new_line
                    self.setCursorPosition(line_number-1, len(new_line))
            else:
                # There is text before the cursor
                diff = (tab_width - (position % tab_width))
                adding_text = diff * " "
                new_line = line_text[:position] + adding_text + line_text[position:]
                self.line_list[line_number] = new_line
                self.setCursorPosition(line_number-1, position+diff)
        else:
            # MULTILINE INDENT
            selected_line = self.getCursorPosition()[0]
            # Adjust the 'from' and 'to' indexes to the line list indexing
            line_from = selection[0]+1
            line_to = selection[2]+1
            # This part is to mimic the default indent functionality of Scintilla
            if selection[3] == 0:
                line_to = selection[2]
            # Get the selected line list
            lines = self.line_list[line_from:line_to]
            # Set the indentation width
            indentation_string = tab_width * " "
            ## # Select the indentation function
            ## if sys.version_info.minor <= 2:
            ##     def nested_indent(line, indent_string):
            ##         if line.strip() != " ":
            ##             line = indent_string + line
            ##         return line
            ##     indent_func = nested_indent
            ## else:
            ##     indent_func = textwrap.indent
            ## #Indent the line list in place
            ## for i, line in enumerate(lines):
            ##     lines[i] = indent_func(line, indentation_string)
            # Smart indentation that tabs to tab-width columns
            def indent_func(line):
                if line.strip() != " ":
                    if line.startswith(" "):
                        leading_spaces = len(line) - len(line.lstrip())
                        diff = (tab_width - (leading_spaces % tab_width))
                        adding_text = diff * " "
                        line = adding_text + line
                    else:
                        line = (tab_width * " ") + line
                return line
            # Indent the line list in place
            for i, line in enumerate(lines):
                lines[i] = indent_func(line)
            # Set the new line list in one operation
            self.line_list[line_from:line_to] = lines
            # Set the selection again according to which line was selected before the indent
            if selected_line == selection[0]:
                # This part is also to mimic the default indent functionality of Scintilla
                if selection[3] == 0:
                    select_from = selection[2]
                else:
                    select_from = selection[2] + 1
                select_from_length = 0
                select_to = selection[0]
                select_to_length = 0
            else:
                select_from = selection[0]
                select_from_length = 0
                select_to = selection[2]
                # This part is also to mimic the default indent functionality of Scintilla
                if selection[3] == 0:
                    select_to = selection[2]
                else:
                    select_to = selection[2] + 1
                select_to_length = 0
            self.setSelection(
                select_from, 
                select_from_length, 
                select_to, 
                select_to_length
            )
    
    def custom_unindent(self):
        """
        Scintila unindents line-by-line, which is very slow for a large amount of lines. Try unindenting 20000 lines.
        This is a custom unindentation function that unindents all lines in one operation.
        """
        tab_width = settings.Editor.tab_width
        #Check QScintilla's tab width
        if self.tabWidth() != tab_width:
            self.setTabWidth(tab_width)
        #Unindent according to selection
        selection = self.getSelection()
        if selection == (-1, -1, -1, -1):
            line_number, position = self.getCursorPosition()
            #Adjust index to the line list indexing
            line_number += 1
            line_text = self.line_list[line_number]
            if line_text == "":
                return
            elif line_text.strip() == "":
                #The line contains only spaces
                diff = len(line_text) % tab_width
                if diff == 0:
                    diff = tab_width
                new_length = len(line_text) - diff
                self.line_list[line_number] = self.line_list[line_number][:new_length]
                self.setCursorPosition(line_number-1, new_length)
            else:
                if line_text[0] != " ":
                    #Do not indent, just move the cursor back
                    if position == 0:
                        return
                    diff = position % tab_width
                    if diff == 0:
                        diff = tab_width
                    self.setCursorPosition(line_number-1, position-diff)
                elif line_text[:position].strip() == "":
                    #The line has spaces in the beginning
                    for i, ch in enumerate(line_text):
                        if ch != " ":
                            diff = i % tab_width
                            if diff == 0:
                                diff = tab_width
                            self.line_list[line_number] = self.line_list[line_number][diff:]
                            self.setCursorPosition(line_number-1, i-diff)
                            break
                else:
                    #Move the cursor to the first none space character then repeat above code
                    diff = position % tab_width
                    if diff == 0:
                        diff = tab_width
                    self.setCursorPosition(line_number-1, position-diff)
        else:
            #MULTILINE UNINDENT
            selected_line = self.getCursorPosition()[0]
            #Adjust the 'from' and 'to' indexes to the line list indexing
            line_from = selection[0]+1
            line_to = selection[2]+1
            #This part is to mimic the default indent functionality of Scintilla
            if selection[3] == 0:
                line_to = selection[2]
            #Get the selected line list
            lines = self.line_list[line_from:line_to]
            ## Remove the leading tab-width number of spaces in every line
            ## for i in range(0, len(lines)):
            ##     for j in range(0, tab_width):
            ##         if lines[i].startswith(" "):
            ##             lines[i] = lines[i].replace(" ", "", 1)                   
            # Smart unindentation that unindents each line to the nearest tab column
            def unindent_func(line):
                if line.startswith(" "):
                    leading_spaces = len(line) - len(line.lstrip())
                    diff = leading_spaces % tab_width
                    if diff == 0:
                        diff = tab_width
                    line = line.replace(diff * " ", "", 1)
                return line
            #Unindent the line list in place
            for i, line in enumerate(lines):
                lines[i] = unindent_func(line)
            #Set the new line list in one operation
            self.line_list[line_from:line_to] = lines
            #Set the selection again according to which line was selected before the indent
            if selected_line == selection[0]:
                #This part is also to mimic the default indent functionality of Scintilla
                if selection[3] == 0:
                    select_from = selection[2]
                else:
                    select_from = selection[2] + 1
                select_from_length = 0
                select_to = selection[0]
                select_to_length = 0
            else:
                select_from = selection[0]
                select_to = selection[2]
                select_from_length = 0
                # This part is also to mimic the default indent functionality of Scintilla
                if selection[3] == 0:
                    select_to = selection[2]
                else:
                    select_to = selection[2] + 1
                select_to_length = 0
            self.setSelection(
                select_from, 
                select_from_length, 
                select_to, 
                select_to_length
            )
    
    def text_to_list(self, input_text):
        """Split the input text into a list of lines according to the document EOL delimiter"""
        out_list = []
        if self.eolMode() == data.QsciScintilla.EolUnix:
            out_list = input_text.split("\n")
        elif self.eolMode() == data.QsciScintilla.EolWindows:
            out_list = input_text.split("\r\n")
        elif self.eolMode() == data.QsciScintilla.EolMac:
            out_list = input_text.split("\r")
        return out_list
    
    def list_to_text(self, line_list):
        """Convert a list of lines to one string according to the document EOL delimiter"""
        out_text = ""
        if self.eolMode() == data.QsciScintilla.EolUnix:
            out_text = "\n".join(line_list)
        elif self.eolMode() == data.QsciScintilla.EolWindows:
            out_text = "\r\n".join(line_list)
        elif self.eolMode() == data.QsciScintilla.EolMac:
            out_text = "\r".join(line_list)
        return out_text

    def toggle_comment_uncomment(self):
        """Toggle commenting for the selected lines"""
        #Check if the document is a valid programming language
        if self.lexer().comment_string == None:
            self.main_form.display.repl_display_message(
                "Lexer '{}' has no comment abillity!".format(self.lexer().language()), 
                message_type=data.MessageType.WARNING
            )
            return
        #Test if there is no selected text
        if (self.getSelection() == (-1, -1, -1, -1) or
            self.getSelection()[0] == self.getSelection()[2]):
            #No selected text
            line_number = self.getCursorPosition()[0] + 1
            line_text   = self.get_line(line_number)
            #Un/comment only the current line (no arguments un/comments current line)
            if line_text.lstrip().startswith(self.lexer().comment_string):
                self.uncomment_line()
            else:
                self.comment_line()
        else:
            #Text is selected 
            start_line_number   = self.getSelection()[0] + 1
            first_selected_chars = self.selectedText()[0:len(self.lexer().comment_string)]
            end_line_number     = self.getSelection()[2] + 1
            #Choose un/commenting according to the first line in selection
            if first_selected_chars == self.lexer().comment_string:
                self.uncomment_lines(start_line_number, end_line_number)
            else:
                self.comment_lines(start_line_number, end_line_number)
    
    def for_each_line(self, in_func):
        """Apply function 'in_func' to lines"""
        #Check that in_func is really a function
        if callable(in_func) == False:
            self.main_form.display.repl_display_message(
                "'for_each_line' argument has to be a function!", 
                message_type=data.MessageType.ERROR
            )
            return
        # Loop through the lines and apply the function to each line
        if (self.getSelection() == (-1, -1, -1, -1) or
            self.getSelection()[0] == self.getSelection()[2]):
            #No selected text, apply function to the every line
            try:
                new_line_list = []
                function_returns_none = False
                for line in self.line_list:
                    new_line = in_func(line)
                    if new_line == None:
                        function_returns_none = True
                        continue
                    new_line_list.append(new_line)
                if function_returns_none == False:
                    #Assign the new list over the old one
                    self.line_list = new_line_list
            except Exception as ex:
                self.main_form.display.repl_display_message(
                    "'for_each_line' has an error:\n" + str(ex), 
                    message_type=data.MessageType.ERROR
                )
                return
        else:
            #Selected text, apply function to the selected lines only
            try:
                #Get the starting and end line
                start_line_number   = self.getSelection()[0] + 1
                end_line_number     = self.getSelection()[2] + 1
                #Apply the function to the lines
                new_line_list = []
                function_returns_none = False
                for line in self.line_list[start_line_number:end_line_number]:
                    new_line = in_func(line)
                    if new_line == None:
                        function_returns_none = True
                        continue
                    new_line_list.append(new_line)
                if function_returns_none == False:
                    #Assign the new list over the old one
                    self.line_list[start_line_number:end_line_number] = new_line_list
            except Exception as ex:
                self.main_form.display.repl_display_message(
                    "'for_each_line' has an error:\n" + str(ex), 
                    message_type=data.MessageType.ERROR
                )
                return
    
    def remove_empty_lines(self):
        new_line_list = []
        for line in self.line_list:
            if line.strip() != "":
                new_line_list.append(line)
        #Assign the new list over the old one
        self.line_list = new_line_list

    """
    Search and replace functions
    """
    def find_text(self, 
                  search_text, 
                  case_sensitive=False, 
                  search_forward=True, 
                  regular_expression=False):
        """
        (SAME AS THE QSciScintilla.find, BUT THIS RETURNS A RESULT)
        Function to find an occurance of text in the current tab of a basic widget:
            - Python reguler expressions are used, not the Scintilla built in ones
            - function executes cyclically over the scintilla document, when it reaches the end of the document
            ! THERE IS A BUG WHEN SEARCHING FOR UNICODE STRINGS, THESE ARE ALWAYS CASE SENSITIVE
        """
        def focus_entire_found_text():
            """
            Nested function for selection the entire found text
            """
            # Save the currently found text selection attributes
            position = self.getSelection()
            # Set the cursor to the beginning of the line, so that in case the
            # found string index is behind the previous cursor index, the whole
            # found text is shown!
            self.setCursorPosition(position[0], 0)
            self.setSelection(position[0], position[1], position[2], position[3])
        # Set focus to the tab that will be searched
        self._parent.setCurrentWidget(self)
        if regular_expression == True:
            # Get the absolute cursor index from line/index position
            line, index = self.getCursorPosition()
            absolute_position = self.positionFromLineIndex(line, index)
            # Compile the search expression according to the case sensitivity
            if case_sensitive == True:
                compiled_search_re = re.compile(search_text)
            else:
                compiled_search_re = re.compile(search_text, re.IGNORECASE)
            # Search based on the search direction
            if search_forward == True:
                # Regex search from the absolute position to the end for the search expression
                search_result = re.search(compiled_search_re, self.text()[absolute_position:])
                if search_result != None:
                    #Select the found expression
                    result_start    = absolute_position + search_result.start()
                    result_end      = result_start + len(search_result.group(0))
                    self.setCursorPosition(0, result_start)
                    self.setSelection(0, result_start, 0, result_end)
                    # Return successful find
                    return data.SearchResult.FOUND
                else:
                    # Begin a new search from the top of the document
                    search_result = re.search(compiled_search_re, self.text())
                    if search_result != None:
                        # Select the found expression
                        result_start    = search_result.start()
                        result_end      = result_start + len(search_result.group(0))
                        self.setCursorPosition(0, result_start)
                        self.setSelection(0, result_start, 0, result_end)
                        self.main_form.display.write_to_statusbar("Reached end of document, started from the top again!")
                        # Return cycled find
                        return data.SearchResult.CYCLED
                    else:
                        self.main_form.display.write_to_statusbar("Text was not found!")
                        return data.SearchResult.NOT_FOUND
            else:
                # Move the cursor one character back when searching backard
                # to not catch the same search result again
                cursor_position = self.get_absolute_cursor_position()
                search_text = self.text()[:cursor_position]
                # Regex search from the absolute position to the end for the search expression
                search_result = [m for m in re.finditer(compiled_search_re, search_text)]
                if search_result != []:
                    #Select the found expression
                    result_start    = search_result[-1].start()
                    result_end      = search_result[-1].end()
                    self.setCursorPosition(0, result_start)
                    self.setSelection(0, result_start, 0, result_end)
                    # Return successful find
                    return data.SearchResult.FOUND
                else:
                    # Begin a new search from the top of the document
                    search_result = [m for m in re.finditer(compiled_search_re, self.text())]
                    if search_result != []:
                        # Select the found expression
                        result_start    = search_result[-1].start()
                        result_end      = search_result[-1].end()
                        self.setCursorPosition(0, result_start)
                        self.setSelection(0, result_start, 0, result_end)
                        self.main_form.display.write_to_statusbar("Reached end of document, started from the top again!")
                        # Return cycled find
                        return data.SearchResult.CYCLED
                    else:
                        self.main_form.display.write_to_statusbar("Text was not found!")
                        return data.SearchResult.NOT_FOUND
        else:
            # Move the cursor one character back when searching backard
            # to not catch the same search result again
            if search_forward == False:
                line, index = self.getCursorPosition()
                self.setCursorPosition(line, index-1)
            # "findFirst" is the QScintilla function for finding text in a document
            search_result = self.findFirst(search_text, 
                False, 
                case_sensitive, 
                False, 
                False, 
                forward=search_forward
            )
            if search_result == False:
                # Try to find text again from the top or at the bottom of 
                # the scintilla document, depending on the search direction
                if search_forward == True:
                    s_line = 0
                    s_index = 0
                else:
                    s_line = len(self.line_list)-1
                    s_index = len(self.text())
                inner_result = self.findFirst(
                    search_text, 
                    False, 
                    case_sensitive, 
                    False, 
                    False, 
                    forward=search_forward, 
                    line=s_line, 
                    index=s_index
                )
                if inner_result == False:
                    self.main_form.display.write_to_statusbar("Text was not found!")
                    return data.SearchResult.NOT_FOUND
                else:
                    self.main_form.display.write_to_statusbar("Reached end of document, started from the other end again!")
                    focus_entire_found_text()
                    # Return cycled find
                    return data.SearchResult.CYCLED
            else:
                # Found text
                self.main_form.display.write_to_statusbar("Found text: \"" + search_text + "\"")
                focus_entire_found_text()
                # Return successful find
                return data.SearchResult.FOUND
    
    def find_all(self,
                 search_text, 
                 case_sensitive=False, 
                 regular_expression=False, 
                 text_to_bytes=False,
                 whole_words=False):
        """Find all instances of a string and return a list of (line, index_start, index_end)"""
        #Find all instances of the search string and return the list
        matches = functions.index_strings_in_text(
            search_text, 
            self.text(), 
            case_sensitive, 
            regular_expression, 
            text_to_bytes,
            whole_words
        )
        return matches
    
    def find_and_replace(self, 
                         search_text, 
                         replace_text, 
                         case_sensitive=False, 
                         search_forward=True, 
                         regular_expression=False):
        """Find next instance of the search string and replace it with the replace string"""
        if regular_expression == True:
            #Check if expression exists in the document
            search_result = self.find_text(
                search_text, case_sensitive, search_forward, regular_expression
            )
            if search_result != data.SearchResult.NOT_FOUND:
                if case_sensitive == True:
                    compiled_search_re = re.compile(search_text)
                else:
                    compiled_search_re = re.compile(search_text, re.IGNORECASE)
                #The search expression is already selected from the find_text function
                found_expression = self.selectedText()
                #Save the found selected text line/index information
                saved_selection = self.getSelection()
                #Replace the search expression with the replace expression
                replacement = re.sub(compiled_search_re, replace_text, found_expression)
                #Replace selected text with replace text
                self.replaceSelectedText(replacement)
                #Select the newly replaced text
                self.main_form.display.repl_display_message(replacement)
                self.setSelection(
                    saved_selection[0], 
                    saved_selection[1], 
                    saved_selection[2], 
                    saved_selection[1]+len(replacement)
                )
                return True
            else:
                #Search text not found
                self.main_form.display.write_to_statusbar("Text was not found!")
                return False
        else:
            #Check if string exists in the document
            search_result = self.find_text(search_text, case_sensitive)
            if search_result != data.SearchResult.NOT_FOUND:
                #Save the found selected text line/index information
                saved_selection = self.getSelection()
                #Replace selected text with replace text
                self.replaceSelectedText(replace_text)
                #Select the newly replaced text
                self.setSelection(
                    saved_selection[0], 
                    saved_selection[1], 
                    saved_selection[2], 
                    saved_selection[1]+len(replace_text)
                )
                return True
            else:
                #Search text not found
                self.main_form.display.write_to_statusbar("Text was not found!")
                return False
    
    def replace_all(self,
                    search_text, 
                    replace_text, 
                    case_sensitive=False,
                    regular_expression=False):
        """Replace all occurences of a string in a scintilla document"""
        #Store the current cursor position
        current_position = self.getCursorPosition()
        #Move cursor to the top of the document, so all the search string instances will be found
        self.setCursorPosition(0, 0)
        #Clear all previous highlights
        self.clear_highlights()
        #Setup the indicator style, the replace indicator is 1
        self.set_indicator("replace")
        #Correct the displayed file name
        if self.save_name == None or self.save_name == "":
            file_name = self._parent.tabText(self._parent.currentIndex())
        else:
            file_name = os.path.basename(self.save_name)
        #Check if there are any instances of the search text in the document
        #based on the regular expression flag
        search_result = None
        if regular_expression == True:
            #Check case sensitivity for regular expression
            if case_sensitive == True:
                compiled_search_re = re.compile(search_text)
            else:
                compiled_search_re = re.compile(search_text, re.IGNORECASE)
            search_result = re.search(compiled_search_re, self.text())
        else:
            search_result = self.find_text(search_text, case_sensitive)
        if search_result == data.SearchResult.NOT_FOUND:
            message = "No matches were found in '{}'!".format(file_name)
            self.main_form.display.repl_display_message(
                message, 
                message_type=data.MessageType.WARNING
            )
            return
        #Use the re module to replace the text
        text = self.text()
        matches, replaced_text  =   functions.replace_and_index(
                                        text, 
                                        search_text, 
                                        replace_text, 
                                        case_sensitive, 
                                        regular_expression, 
                                    )
        #Check if there were any matches or
        #if the search and replace text were equivalent!
        if matches != None:
            #Replace the text
            self.replace_entire_text(replaced_text)
            #Matches can only be displayed for non-regex functionality
            if regular_expression == True:
                #Build the list of matches used by the highlight_raw function
                corrected_matches = []
                for i in matches:
                    index = self.positionFromLineIndex(i, 0)
                    corrected_matches.append(
                        (
                            0, 
                            index, 
                            0, 
                            index+len(self.text(i)), 
                        )
                    )
                #Display the replacements in the REPL tab
                if len(corrected_matches) < settings.Editor.maximum_highlights:
                    message = "{} replacements:".format(file_name)
                    self.main_form.display.repl_display_message(
                        message, 
                        message_type=data.MessageType.SUCCESS
                    )
                    for match in corrected_matches:
                        line    = self.lineIndexFromPosition(match[1])[0] + 1
                        index   = self.lineIndexFromPosition(match[1])[1]
                        message = "    replacement made in line:{:d}".format(line)
                        self.main_form.display.repl_display_message(
                            message, 
                            message_type=data.MessageType.SUCCESS
                        )
                else:
                    message = "{:d} replacements made in {}!\n".format(
                                                                    len(corrected_matches), 
                                                                    file_name
                                                                )
                    message += "Too many to list individually!"
                    self.main_form.display.repl_display_message(
                        message, 
                        message_type=data.MessageType.WARNING
                    )
                #Highlight and display the line difference between the old and new texts
                self.highlight_raw(corrected_matches)
            else:
                #Display the replacements in the REPL tab
                if len(matches) < settings.Editor.maximum_highlights:
                    message = "{} replacements:".format(file_name)
                    self.main_form.display.repl_display_message(
                        message, 
                        message_type=data.MessageType.SUCCESS
                    )
                    for match in matches:
                        line    = self.lineIndexFromPosition(match[1])[0] + 1
                        index   = self.lineIndexFromPosition(match[1])[1]
                        message = "    replaced \"{}\" in line:{:d} column:{:d}".format(
                                                                                search_text, 
                                                                                line, 
                                                                                index
                                                                            )
                        self.main_form.display.repl_display_message(
                            message, 
                            message_type=data.MessageType.SUCCESS
                        )
                else:
                    message = "{:d} replacements made in {}!\n".format(
                                                                    len(matches), 
                                                                    file_name
                                                                )
                    message += "Too many to list individually!"
                    self.main_form.display.repl_display_message(
                        message, 
                        message_type=data.MessageType.WARNING
                    )
                #Highlight and display the replaced text
                self.highlight_raw(matches)
            #Restore the previous cursor position
            self.setCursorPosition(current_position[0], current_position[1])
        else:
            message = "The search string and replace string are equivalent!\n"
            message += "Change the search/replace string or change the case sensitivity!"
            self.main_form.display.repl_display_message(
                message,
                message_type=data.MessageType.ERROR
            )
    
    def replace_in_selection(self, 
                             search_text, 
                             replace_text, 
                             case_sensitive=False, 
                             regular_expression=False):
        """Replace all occurences of a string in the current selection in the scintilla document"""
        #Get the start and end point of the selected text
        start_line, start_index,  end_line, end_index = self.getSelection()
        #Get the currently selected text and use the re module to replace the text
        selected_text = self.selectedText()
        replaced_text = functions.regex_replace_text(
                selected_text, 
                search_text, 
                replace_text, 
                case_sensitive, 
                regular_expression
        )
        #Check if any replacements were made
        if replaced_text != selected_text:
            #Put the text back into the selection space and select it again
            self.replaceSelectedText(replaced_text)
            new_end_line = start_line
            new_end_index = start_index + len(bytearray(replaced_text, "utf-8"))
            self.setSelection(start_line, start_index, new_end_line, new_end_index)
        else:
            message = "No replacements were made!"
            self.main_form.display.repl_display_message(
                message,
                message_type=data.MessageType.WARNING
            )    
    
    def replace_entire_text(self, new_text):
        """Replace the entire text of the document"""
        #Select the entire text
        self.selectAll(True)
        #Replace the text with the new
        self.replaceSelectedText(new_text)
    
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
    
    
    """
    Highligting functions
    """
    def highlight_text(self, 
                       highlight_text, 
                       case_sensitive=False, 
                       regular_expression=False):
        """
        Highlight all instances of the selected text with a selected colour
        """
        #Setup the indicator style, the highlight indicator will be 0
        self.set_indicator("highlight")
        #Get all instances of the text using list comprehension and the re module
        matches = self.find_all(
            highlight_text, 
            case_sensitive, 
            regular_expression, 
            text_to_bytes=True
        )
        #Check if the match list is empty
        if matches:
            #Use the raw highlight function to set the highlight indicators
            self.highlight_raw(matches)
            self.main_form.display.repl_display_message(
                "{:d} matches highlighted".format(len(matches)) 
            )
            # Set the cursor to the first highlight (I don't like this feature)
#            self.find_text(highlight_text, case_sensitive, True, regular_expression)
        else:
            self.main_form.display.repl_display_message(
                "No matches found!",
                message_type=data.MessageType.WARNING
            )
    
    def highlight_raw(self, highlight_list):
        """
        Core highlight function that uses Scintilla messages to style indicators.
        QScintilla's fillIndicatorRange function is to slow for large numbers of
        highlights!
        INFO:   This is done using the scintilla "INDICATORS" described in the official
                scintilla API (http://www.scintilla.org/ScintillaDoc.html#Indicators)
        """
        scintilla_command = data.QsciScintillaBase.SCI_INDICATORFILLRANGE
        for highlight in highlight_list:
            start   = highlight[1]
            length  = highlight[3] - highlight[1]
            self.SendScintilla(
                scintilla_command, 
                start, 
                length
            )
    
    def _highlight_selected_text(self, 
                        highlight_text, 
                        case_sensitive=False, 
                        regular_expression=False):
        """
        Same as the highlight_text function, but adapted for the use
        with the _selection_changed functionality.
        """
        # Setup the indicator style, the highlight indicator will be 0
        self.set_indicator("selection")
        # Get all instances of the text using list comprehension and the re module
        matches = self.find_all(
            highlight_text, 
            case_sensitive, 
            regular_expression, 
            text_to_bytes=True,
            whole_words=True
        )
        # Check if the match list is empty
        if matches:
            # Use the raw highlight function to set the highlight indicators
            self.highlight_raw(matches)
    
    def clear_highlights(self):
        """Clear all highlighted text"""
        #Clear the highlight indicators
        self.clearIndicatorRange(
            0, 
            0, 
            self.lines(), 
            self.lineLength(self.lines()-1), 
            self.HIGHLIGHT_INDICATOR
        )
        #Clear the replace indicators
        self.clearIndicatorRange(
            0, 
            0, 
            self.lines(), 
            self.lineLength(self.lines()-1), 
            self.REPLACE_INDICATOR
        )
        #Clear the find indicators
        self.clearIndicatorRange(
            0, 
            0, 
            self.lines(), 
            self.lineLength(self.lines()-1), 
            self.FIND_INDICATOR
        )
        
    def clear_selection_highlights(self):
        #Clear the selection indicators
        self.clearIndicatorRange(
            0, 
            0, 
            self.lines(), 
            self.lineLength(self.lines()-1), 
            self.SELECTION_INDICATOR
        )
    
    def _set_indicator(self,
                       indicator, 
                       fore_color):
        """Set the indicator settings"""
        self.indicatorDefine(
            data.QsciScintillaBase.INDIC_ROUNDBOX,
            indicator
        )
        self.setIndicatorForegroundColor(
            fore_color, 
            indicator
        )
        self.SendScintilla(
            data.QsciScintillaBase.SCI_SETINDICATORCURRENT, 
            indicator
        )

    def set_indicator(self, indicator):
        """
        Select the indicator that will be used for use with
        Scintilla's indicator functionality
        """
        if indicator == "highlight":
            self._set_indicator(
                self.HIGHLIGHT_INDICATOR, 
                data.theme.Indication.Highlight
            )
        elif indicator == "selection":
            self._set_indicator(
                self.SELECTION_INDICATOR, 
                data.theme.Indication.Selection
            )
        elif indicator == "replace":
            self._set_indicator(
                self.REPLACE_INDICATOR, 
                data.theme.Indication.Replace
            )
        elif indicator == "find":
            self._set_indicator(
                self.FIND_INDICATOR, 
                data.theme.Indication.Find
            )
        else:
            raise Exception("Unknown indicator: {}".format(indicator))


    """
    Various CustomEditor functions
    """
    def check_line_numbering(self, line_number):
        """
        Check if the line number is in the bounds of the current document
        and return the filtered line number
        """
        #Convert the line numbering from the displayed 1-to-n to the array numbering of python 0-to-n
        line_number -= 1
        #Check if the line number is below the index 0
        if line_number < 0:
            line_number = 0
        elif line_number > self.lines()-1:
            line_number = self.lines()-1
        return line_number
    
    def save_document(self, saveas=False, encoding="utf-8", line_ending=None):
        """Save a document to a file"""
        if self.save_name == "" or saveas != False:
            # Tab has an empty directory attribute or "SaveAs" was invoked, select file using the QFileDialog
            # Get the filename from the QFileDialog window
            temp_save_name = data.QFileDialog.getSaveFileName(
                self, 
                "Save File", 
                os.getcwd() + self.save_name, 
                "All Files(*)"
            )
            if data.PYQT_MODE == 5:
                # PyQt5's getOpenFileNames returns a tuple (files_list, selected_filter),
                # so pass only the files to the function
                temp_save_name = temp_save_name[0]
            # Check if the user has selected a file
            if temp_save_name == "":
                return
            # Replace back-slashes to forward-slashes on Windows
            if data.platform == "Windows":
                temp_save_name = temp_save_name.replace("\\", "/")
            # Save the chosen file name to the document "save_name" attribute
            self.save_name = temp_save_name
        # Set the tab name by filtering it out from the QFileDialog result
        self.name = os.path.basename(self.save_name)
        # Change the displayed name of the tab in the basic widget
        self._parent.set_tab_name(self, self.name)
        # Check if a line ending was specified
        if line_ending == None:
            # Write contents of the tab into the specified file
            save_result = functions.write_to_file(self.text(), self.save_name, encoding)
        else:
            # The line ending has to be a string
            if isinstance(line_ending, str) == False:
                self.main_form.display.repl_display_message(
                    "Line ending has to be a string!", 
                    message_type=data.MessageType.ERROR
                )
                return
            else:
                # Convert the text into a list and join it together with the specified line ending
                text_list = self.line_list
                converted_text = line_ending.join(text_list)
                save_result = functions.write_to_file(converted_text, self.save_name, encoding)
        # Check result of the functions.write_to_file function
        if save_result == True:
            # Saving has succeded
            self._parent.reset_text_changed(self._parent.indexOf(self))
            # Update the lexer for the document only if the lexer is not set
            if isinstance(self.lexer(), lexers.Text):
                file_type = functions.get_file_type(self.save_name)
                self.choose_lexer(file_type)
            # Update the settings manipulator with the new file
            self.main_form.settings.update_recent_list(self.save_name)
        else:
            # Saving has failed
            error_message = "Error while trying to write file to disk:\n"
            error_message += str(save_result)
            self.main_form.display.repl_display_message(
                error_message, 
                message_type=data.MessageType.ERROR
            )
            self.main_form.display.write_to_statusbar(
                "Saving to file failed, check path and disk space!"
            )
    
    def refresh_lexer(self):
        """ Refresh the current lexer (used by themes) """
        self.set_theme(data.theme)
        self.lexer().set_theme(data.theme)
    
    def choose_lexer(self, file_type):
        """Choose the lexer from the file type parameter for the scintilla document"""
        #Set the lexer for syntax highlighting according to file type
        self.current_file_type, lexer = lexers.get_lexer_from_file_type(file_type)
        #Check if a lexer was chosen
        if lexer != None:
            self.set_lexer(lexer, file_type)
        else:
            self.main_form.display.repl_display_message(
                "Error while setting the lexer!",
                message_type=data.MessageType.ERROR
            )
    
    def clear_lexer(self):
        """Remove the lexer from the editor"""
        if self.lexer() != None:
            self.lexer().deleteLater()
            self.lexer().setParent(None)
            self.setLexer(None)
    
    def set_lexer(self, lexer, file_type):
        """Function that actually sets the lexer"""
        # First clear the lexer
        self.clear_lexer()
        # Save the current file type to a string
        self.current_file_type = file_type.upper()
        # Set the lexer default font family
        lexer.setDefaultFont(settings.Editor.font)
        # Set the comment options
        result = lexers.get_comment_style_for_lexer(lexer)
        lexer.open_close_comment_style = result[0]
        lexer.comment_string = result[1]
        lexer.end_comment_string = result[2]
        # Set the lexer for the current scintilla document
        lexer.setParent(self)
        self.setLexer(lexer)
        # Reset the brace matching color
        self.reset_brace_matching()
        # Change the font style of comments so that they are the same as the default scintilla text
        # This is done using the low-level API function "SendScintilla" that is documented here: http://pyqt.sourceforge.net/Docs/QScintilla2/classQsciScintillaBase.html
        # With it you can invoke C functions documented here: http://www.scintilla.org/ScintillaDoc.html
        self.SendScintilla(data.QsciScintillaBase.SCI_STYLESETFONT, 1, settings.Editor.comment_font)
        # Enable code folding for the file type
        self.setFolding(data.QsciScintilla.PlainFoldStyle)
        # Set all fonts in the current lexer to the default style
        # and set the keyword styles to bold
        if (isinstance(lexer, lexers.Ada) or
            isinstance(lexer, lexers.Oberon) or
            (hasattr(lexer, "get_name") and lexer.get_name() == "Nim")):
            # Set the margin font for the lexers in the lexers.py module
            self.setMarginsFont(lexer.default_font)
        # Get the icon according to the file type
        self.current_icon = functions.get_language_file_icon(file_type)
        # Update the icon on the parent basic widget
        self.icon_manipulator.update_icon(self)
        # Set the theme
        self.set_theme(data.theme)
        # Update corner icons
        self.icon_manipulator.update_corner_button_icon(self.current_icon)
        self.icon_manipulator.update_icon(self)
        
    def reset_brace_matching(self):
        # Reset the brace matching color
        self.setBraceMatching(data.QsciScintilla.SloppyBraceMatch)
#        self.setMatchedBraceBackgroundColor(settings.Editor.brace_color)
#        self.setMatchedBraceForegroundColor(data.theme.Font.Default)
    
    def clear_editor(self):
        """Clear the text from the scintilla document"""
        self.SendScintilla(data.QsciScintillaBase.SCI_CLEARALL)
    
    def tabs_to_spaces(self):
        """Convert all tab(\t) characters to spaces"""
        spaces = " " * settings.Editor.tab_width
        self.setText(self.text().replace("\t", spaces))

    def undo_all(self):
        """Repeat undo until there is something to undo"""
        while self.isUndoAvailable() == True:
            self.undo()

    def redo_all(self):
        """Repeat redo until there is something to redo"""
        while self.isRedoAvailable() == True:
            self.redo()
    
    def update_margin(self):
        """
        Update margin width according to the number of lines in the document
        """
        line_count  = self.lines()
        # Set margin width
        self.setMarginWidth(0, str(line_count) + "0")

    def edge_marker_show(self):
        """Show the marker at the specified column number"""
        #Set the marker color to blue
        marker_color = settings.Editor.edge_marker_color
        #Set the column number where the marker will be shown
        marker_column = settings.Editor.edge_marker_column 
        #Set the marker options
        self.setEdgeColor(marker_color)
        self.setEdgeColumn(marker_column)
        self.setEdgeMode(data.QsciScintilla.EdgeLine)

    def edge_marker_hide(self):
        """Hide the column marker"""
        self.setEdgeMode(data.QsciScintilla.EdgeNone)
    
    def edge_marker_toggle(self):
        """Toggle edge marker display"""
        if self.edgeMode() == data.QsciScintilla.EdgeNone:
            self.edge_marker_show()
        else:
            self.edge_marker_hide()
    
    def reload_file(self):
        """Reload current document from disk"""
        #Check if file was loaded from or saved to disk
        if self.save_name == "":
            self.main_form.display.write_to_statusbar(
                "Document has no file on disk!", 3000
            )
            return
        #Check the file status
        if self.save_status == data.FileStatus.MODIFIED:
            #Close the log window if it is displayed
            self.main_form.view.set_log_window(False)
            #Display the close notification
            reload_message = "Document '" + self.name+ "' has been modified!\nReload it from disk anyway?"
            reply = YesNoDialog.question(reload_message)
            if reply == data.QMessageBox.No:
                #Cancel tab file reloading
                return
        #Check if the name of the document is valid
        if self.name == "" or self.name == None:
            return
        #Open the file and read the contents
        try:
            disk_file_text = functions.read_file_to_string(self.save_name)
        except:
            self.main_form.display.write_to_statusbar("Error reloading file!", 3000)
            return
        #Save the current cursor position
        temp_position = self.getCursorPosition()
        #Reload the file
        self.replace_entire_text(disk_file_text)
        #Restore saved cursor position
        self.setCursorPosition(temp_position[0], temp_position[1])
    
    def copy(self):
        super().copy()
        selected_text = self.selectedText()
        if selected_text:
            cb = data.application.clipboard()
            cb.clear(mode=cb.Clipboard)
            cb.setText(selected_text, mode=cb.Clipboard)
    
    def copy_self(self, new_editor):
        """Copy everything needed from self to the destination editor"""
        if new_editor == None:
            return
        # Copy all of the settings
        lexer_copy = self.lexer().__class__(new_editor)
        new_editor.set_lexer(lexer_copy, self.current_file_type)
        new_editor.setText(self.text())
    
    def toggle_wordwrap(self):
        """ 
        Toggle word wrap on/off.
        Wrap modes:
            data.QsciScintilla.WrapNone - Lines are not wrapped.
            data.QsciScintilla.WrapWord - Lines are wrapped at word boundaries.
            data.QsciScintilla.WrapCharacter - Lines are wrapped at character boundaries.
            data.QsciScintilla.WrapWhitespace - Lines are wrapped at whitespace boundaries. 
        Wrap visual flags:
            data.QsciScintilla.WrapFlagNone - No wrap flag is displayed.
            data.QsciScintilla.WrapFlagByText - A wrap flag is displayed by the text.
            data.QsciScintilla.WrapFlagByBorder - A wrap flag is displayed by the border.
            data.QsciScintilla.WrapFlagInMargin - A wrap flag is displayed in the line number margin. 
        Wrap indentation:
            data.QsciScintilla.WrapIndentFixed - Wrapped sub-lines are indented by the amount set by setWrapVisualFlags().
            data.QsciScintilla.WrapIndentSame - Wrapped sub-lines are indented by the same amount as the first sub-line.
            data.QsciScintilla.WrapIndentIndented - Wrapped sub-lines are indented by the same amount as the first sub-line plus one more level of indentation. 
        """
        if self.wrapMode() == data.QsciScintilla.WrapNone:
            self.setWrapMode(data.QsciScintilla.WrapWord)
            self.setWrapVisualFlags(data.QsciScintilla.WrapFlagByText)
            self.setWrapIndentMode(data.QsciScintilla.WrapIndentSame)
            self.main_form.display.repl_display_message(
                "Line wrapping ON", 
                message_type=data.MessageType.WARNING
            )
        else:
            self.setWrapMode(data.QsciScintilla.WrapNone)
            self.setWrapVisualFlags(data.QsciScintilla.WrapFlagNone)
            self.main_form.display.repl_display_message(
                "Line wrapping OFF", 
                message_type=data.MessageType.WARNING
            )
    
    def toggle_line_endings(self):
        """Set the visibility of the End-Of-Line character"""
        if self.eolVisibility() == True:
            self.setEolVisibility(False)
            self.main_form.display.repl_display_message(
                "EOL characters hidden", 
                message_type=data.MessageType.WARNING
            )
        else:
            self.setEolVisibility(True)
            self.main_form.display.repl_display_message(
                "EOL characters shown", 
                message_type=data.MessageType.WARNING
            )
    
    def set_cursor_line_visibility(self, new_state):
        self.setCaretLineVisible(new_state)
        if new_state == True:
            if hasattr(data.theme, "Cursor_Line_Background") == False:
                self.main_form.display.repl_display_message(
                    "'Cursor_Line_Background' color is not defined in the current theme!", 
                    message_type=data.MessageType.ERROR
                )
            else:
                self.setCaretLineBackgroundColor(data.theme.Cursor_Line_Background)
    
    def toggle_cursor_line_highlighting(self):
        new_state = bool(not self.SendScintilla(self.SCI_GETCARETLINEVISIBLE))
        self.set_cursor_line_visibility(new_state)
        if new_state == True:
            self.main_form.display.repl_display_message(
                "Cursor line highlighted", 
                message_type=data.MessageType.WARNING
            )
        else:
            self.main_form.display.repl_display_message(
                "Cursor line not highlighted", 
                message_type=data.MessageType.WARNING
            )
    

    """
    CustomEditor autocompletion functions
    """
    def init_autocompletions(self, new_autocompletions=[]):
        """Set the initial autocompletion functionality for the document"""
        self.disable_autocompletions()
    
    autocompletions_connected = False
    def enable_autocompletions(self, new_autocompletions=[]):
        """Function for enabling the CustomEditor autocompletions"""
        # Set how many characters must be typed for the autocompletion popup to appear
        self.setAutoCompletionThreshold(1)
        # Set the source from where the autocompletions will be fetched
        self.setAutoCompletionSource(data.QsciScintilla.AcsDocument)
        # Set autocompletion case sensitivity
        self.setAutoCompletionCaseSensitivity(False)
        # Correct autocompletion behaviour to select
        # the documents word case style instead of the
        # autocompletion's list's.
        if not self.autocompletions_connected:
            self.autocompletions_connected = True
            self.SCN_AUTOCCOMPLETED.connect(self._correct_autocompletion)
    
    splitter = re.compile(r"(\{\.|\.\}|\#|\'|\"\"\"|\n|\s+|\w+|\W)")
    def _correct_autocompletion(self, *args):
        word, from_index, to_index, length = args
        word = word.decode("utf-8")
        current_line = self.getCursorPosition()[0] + 1
        line = self.line_list[current_line]
        for token in self.splitter.findall(self.text()):
            if token.lower() == word.lower():
                self.line_list[current_line] = token.join(line.rsplit(word, 1))
                self.setCursorPosition(current_line-1, len(self.line_list[current_line]))
                break
    
    def disable_autocompletions(self):
        """Disable the CustomEditor autocompletions"""
        self.setAutoCompletionSource(data.QsciScintilla.AcsNone)
    
    def toggle_autocompletions(self):
        """Enable/disable autocompletions for the CustomEditor"""
        #Initilize the document name for displaying
        if self.save_name == None or self.save_name == "":
            document_name = self._parent.tabText(self._parent.currentIndex())
        else:
            document_name = os.path.basename(self.save_name)
        #Check the autocompletion source
        if self.autoCompletionSource() == data.QsciScintilla.AcsDocument:
            self.disable_autocompletions()
            message = "Autocompletions DISABLED in {}".format(document_name)
            self.main_form.display.repl_display_message(
                message, 
                message_type=data.MessageType.WARNING
            )
            self.main_form.display.write_to_statusbar("Autocompletions DISABLED")
        else:
            self.enable_autocompletions()
            message = "Autocompletions ENABLED in {}".format(document_name)
            self.main_form.display.repl_display_message(
                message, 
                message_type=data.MessageType.SUCCESS
            )
            self.main_form.display.write_to_statusbar("Autocompletions ENABLED")
    
    class Bookmarks:
        """
        Bookmark functionality
        """
        def __init__(self, parent):
            """Initialization of the Editing object instance"""
            #Get the reference to the MainWindow parent object instance
            self._parent = parent
        
        def toggle(self):
            """Add/Remove a bookmark at the current line"""
            #Get the cursor line position
            current_line = self._parent.getCursorPosition()[0] + 1
            #Toggle the bookmark
            self.toggle_at_line(current_line)
        
        def toggle_at_line(self, line):
            """
            Toggle a bookmarks at the specified line
            (Line indexing has to be 1..lines)
            """
            #MarkerAdd function needs the standard line indexing
            scintilla_line = line - 1
            #Check if the line is already bookmarked
            if self._parent.main_form.bookmarks.check(self._parent, line) == None:
                if self._parent.main_form.bookmarks.add(self._parent, line) != None:
                    self._parent.markerAdd(scintilla_line, self._parent.bookmark_marker)
            else:
                self._parent.main_form.bookmarks.remove_by_reference(self._parent, line)
                self._parent.markerDelete(scintilla_line, self._parent.bookmark_marker)
        
        def add_marker_at_line(self, line):
            #MarkerAdd function needs the standard line indexing
            scintilla_line = line - 1
            self._parent.markerAdd(scintilla_line, self._parent.bookmark_marker)
        
        def remove_marker_at_line(self, line):
            #MarkerAdd function needs the standard line indexing
            scintilla_line = line - 1
            self._parent.markerDelete(scintilla_line, self._parent.bookmark_marker)
    
    class Keyboard:
        """
        Keyboard command assignment, ...
        Relevant Scintilla items:
            SCI_ASSIGNCMDKEY(int keyDefinition, int sciCommand)
            SCI_CLEARCMDKEY(int keyDefinition)
            SCI_CLEARALLCMDKEYS
            SCI_NULL
        """
        _parent = None
        #GNU/Linux and Windows bindings copied from Scintila source 'KeyMap.cxx'
        bindings = None
        scintilla_keys = None
        valid_modifiers = None
        
        def init_bindings(self):
            self.bindings = {
                "Down" : data.QsciScintillaBase.SCI_LINEDOWN,
                "Down+Shift" : data.QsciScintillaBase.SCI_LINEDOWNEXTEND,
                "Down+Ctrl" : data.QsciScintillaBase.SCI_LINESCROLLDOWN,
                "Down+Alt+Shift" : data.QsciScintillaBase.SCI_LINEDOWNRECTEXTEND,
                "Up" : data.QsciScintillaBase.SCI_LINEUP,
                "Up+Shift" : data.QsciScintillaBase.SCI_LINEUPEXTEND,
                "Up+Ctrl" : data.QsciScintillaBase.SCI_LINESCROLLUP,
                "Up+Alt+Shift" : data.QsciScintillaBase.SCI_LINEUPRECTEXTEND,
                "[+Ctrl" : data.QsciScintillaBase.SCI_PARAUP,
                "[+Ctrl+Shift" : data.QsciScintillaBase.SCI_PARAUPEXTEND,
                "]+Ctrl" : data.QsciScintillaBase.SCI_PARADOWN,
                "]+Ctrl+Shift" : data.QsciScintillaBase.SCI_PARADOWNEXTEND,
                "Left" : data.QsciScintillaBase.SCI_CHARLEFT,
                "Left+Shift" : data.QsciScintillaBase.SCI_CHARLEFTEXTEND,
                "Left+Ctrl" : data.QsciScintillaBase.SCI_WORDLEFT,
                "Left+Shift+Ctrl" : data.QsciScintillaBase.SCI_WORDLEFTEXTEND,
                "Left+Alt+Shift" : data.QsciScintillaBase.SCI_CHARLEFTRECTEXTEND,
                "Right" : data.QsciScintillaBase.SCI_CHARRIGHT,
                "Right+Shift" : data.QsciScintillaBase.SCI_CHARRIGHTEXTEND,
                "Right+Ctrl" : data.QsciScintillaBase.SCI_WORDRIGHT,
                "Right+Shift+Ctrl" : data.QsciScintillaBase.SCI_WORDRIGHTEXTEND,
                "Right+Alt+Shift" : data.QsciScintillaBase.SCI_CHARRIGHTRECTEXTEND,
                "/+Ctrl" : data.QsciScintillaBase.SCI_WORDPARTLEFT,
                "/+Ctrl+Shift" : data.QsciScintillaBase.SCI_WORDPARTLEFTEXTEND,
                "\\+Ctrl" : data.QsciScintillaBase.SCI_WORDPARTRIGHT,
                "\\+Ctrl+Shift" : data.QsciScintillaBase.SCI_WORDPARTRIGHTEXTEND,
                "Home" : data.QsciScintillaBase.SCI_VCHOME,
                "Home+Shift" : data.QsciScintillaBase.SCI_VCHOMEEXTEND,
                settings.Editor.Keys.go_to_start : data.QsciScintillaBase.SCI_DOCUMENTSTART,
                settings.Editor.Keys.select_to_start : data.QsciScintillaBase.SCI_DOCUMENTSTARTEXTEND,
                "Home+Alt" : data.QsciScintillaBase.SCI_HOMEDISPLAY,
                "Home+Alt+Shift" : data.QsciScintillaBase.SCI_VCHOMERECTEXTEND,
                "End" : data.QsciScintillaBase.SCI_LINEEND,
                "End+Shift" : data.QsciScintillaBase.SCI_LINEENDEXTEND,
                settings.Editor.Keys.go_to_end : data.QsciScintillaBase.SCI_DOCUMENTEND,
                settings.Editor.Keys.select_to_end : data.QsciScintillaBase.SCI_DOCUMENTENDEXTEND,
                "End+Alt" : data.QsciScintillaBase.SCI_LINEENDDISPLAY,
                "End+Alt+Shift" : data.QsciScintillaBase.SCI_LINEENDRECTEXTEND,
                settings.Editor.Keys.scroll_up : data.QsciScintillaBase.SCI_PAGEUP,
                settings.Editor.Keys.select_page_up : data.QsciScintillaBase.SCI_PAGEUPEXTEND,
                "PageUp+Alt+Shift" : data.QsciScintillaBase.SCI_PAGEUPRECTEXTEND,
                settings.Editor.Keys.scroll_down : data.QsciScintillaBase.SCI_PAGEDOWN,
                settings.Editor.Keys.select_page_down : data.QsciScintillaBase.SCI_PAGEDOWNEXTEND,
                "PageDown+Alt+Shift" : data.QsciScintillaBase.SCI_PAGEDOWNRECTEXTEND,
                "Delete" : data.QsciScintillaBase.SCI_CLEAR,
                "Delete+Shift" : data.QsciScintillaBase.SCI_CUT,
                settings.Editor.Keys.delete_end_of_word: data.QsciScintillaBase.SCI_DELWORDRIGHT,
                settings.Editor.Keys.delete_end_of_line : data.QsciScintillaBase.SCI_DELLINERIGHT,
                "Insert" : data.QsciScintillaBase.SCI_EDITTOGGLEOVERTYPE,
                "Insert+Shift" : data.QsciScintillaBase.SCI_PASTE,
                "Insert+Ctrl" : data.QsciScintillaBase.SCI_COPY,
                "Escape" : data.QsciScintillaBase.SCI_CANCEL,
                "Backspace" : data.QsciScintillaBase.SCI_DELETEBACK,
                "Backspace+Shift" : data.QsciScintillaBase.SCI_DELETEBACK,
                settings.Editor.Keys.delete_start_of_word : data.QsciScintillaBase.SCI_DELWORDLEFT,
                "Backspace+Alt" : data.QsciScintillaBase.SCI_UNDO,
                settings.Editor.Keys.delete_start_of_line : data.QsciScintillaBase.SCI_DELLINELEFT,
                settings.Editor.Keys.undo : data.QsciScintillaBase.SCI_UNDO,
                settings.Editor.Keys.redo : data.QsciScintillaBase.SCI_REDO,
                settings.Editor.Keys.cut : data.QsciScintillaBase.SCI_CUT,
                settings.Editor.Keys.copy : data.QsciScintillaBase.SCI_COPY,
                settings.Editor.Keys.paste : data.QsciScintillaBase.SCI_PASTE,
                settings.Editor.Keys.select_all : data.QsciScintillaBase.SCI_SELECTALL,
                settings.Editor.Keys.indent : data.QsciScintillaBase.SCI_TAB,
                settings.Editor.Keys.unindent : data.QsciScintillaBase.SCI_BACKTAB,
                "Return" : data.QsciScintillaBase.SCI_NEWLINE,
                "Return+Shift" : data.QsciScintillaBase.SCI_NEWLINE,
                "Add+Ctrl" : data.QsciScintillaBase.SCI_ZOOMIN,
                "Subtract+Ctrl" : data.QsciScintillaBase.SCI_ZOOMOUT,
                "Divide+Ctrl" : data.QsciScintillaBase.SCI_SETZOOM,
                settings.Editor.Keys.line_cut : data.QsciScintillaBase.SCI_LINECUT,
                settings.Editor.Keys.line_delete : data.QsciScintillaBase.SCI_LINEDELETE,
                settings.Editor.Keys.line_copy : data.QsciScintillaBase.SCI_LINECOPY,
                settings.Editor.Keys.line_transpose : data.QsciScintillaBase.SCI_LINETRANSPOSE,
                settings.Editor.Keys.line_selection_duplicate : data.QsciScintillaBase.SCI_SELECTIONDUPLICATE,
                "U+Ctrl" : data.QsciScintillaBase.SCI_LOWERCASE,
                "U+Ctrl+Shift" : data.QsciScintillaBase.SCI_UPPERCASE,
            }
            self.scintilla_keys = {
                "down" : data.QsciScintillaBase.SCK_DOWN,
                "up" : data.QsciScintillaBase.SCK_UP,
                "left" : data.QsciScintillaBase.SCK_LEFT,
                "right" : data.QsciScintillaBase.SCK_RIGHT,
                "home" : data.QsciScintillaBase.SCK_HOME,
                "end" : data.QsciScintillaBase.SCK_END,
                "pageup" : data.QsciScintillaBase.SCK_PRIOR,
                "pagedown" : data.QsciScintillaBase.SCK_NEXT,
                "delete" : data.QsciScintillaBase.SCK_DELETE,
                "insert" : data.QsciScintillaBase.SCK_INSERT,
                "escape" : data.QsciScintillaBase.SCK_ESCAPE,
                "backspace" : data.QsciScintillaBase.SCK_BACK,
                "tab" : data.QsciScintillaBase.SCK_TAB,
                "return" : data.QsciScintillaBase.SCK_RETURN,
                "add" : data.QsciScintillaBase.SCK_ADD,
                "subtract" : data.QsciScintillaBase.SCK_SUBTRACT,
                "divide" : data.QsciScintillaBase.SCK_DIVIDE,
                "win" : data.QsciScintillaBase.SCK_WIN,
                "rwin" : data.QsciScintillaBase.SCK_RWIN,
                "menu" : data.QsciScintillaBase.SCK_MENU,
            }
            self.valid_modifiers = [
                data.QsciScintillaBase.SCMOD_NORM, 
                data.QsciScintillaBase.SCMOD_SHIFT, 
                data.QsciScintillaBase.SCMOD_CTRL, 
                data.QsciScintillaBase.SCMOD_ALT, 
                data.QsciScintillaBase.SCMOD_SUPER, 
                data.QsciScintillaBase.SCMOD_META
            ]
        
        def __init__(self, parent):
            """Initialization of the Keyboard object instance"""
            #Get the reference to the MainWindow parent object instance
            self._parent = parent
            #Assign keyboard commands
            self.init_bindings()
            self.clear_all_keys()
            bindings = self.bindings
            set_key_combination = self.set_key_combination
            for keys in bindings:
                set_key_combination(
                    keys, bindings[keys]
                )
        
        def _parse_key_string(self, key_string):
            """ Parse a '+' delimited string for a key combination """
            split_keys = key_string.replace(" ", "").lower().split("+")
            #Check for to many keys in binding
            if len(split_keys) > 4:
                raise ValueError("Too many items in key string!")
            #Parse the items
            modifiers = []
            key_combination = 0
            if "ctrl" in split_keys:
                modifiers.append(data.QsciScintillaBase.SCMOD_CTRL)
                split_keys.remove("ctrl")
            if "alt" in split_keys:
                modifiers.append(data.QsciScintillaBase.SCMOD_ALT)
                split_keys.remove("alt")
            if "shift" in split_keys:
                modifiers.append(data.QsciScintillaBase.SCMOD_SHIFT)
                split_keys.remove("shift")
            if "meta" in split_keys:
                modifiers.append(data.QsciScintillaBase.SCMOD_META)
                split_keys.remove("meta")
            base_key = split_keys[0]
            if len(split_keys) == 0:
                raise ValueError("Key string has to have a base character!")
            if len(base_key) != 1:
                if base_key in self.scintilla_keys:
                    key_combination = self.scintilla_keys[base_key]
                else:
                    raise ValueError("Unknown base key!")
            else:
                key_combination = ord(base_key.upper())
            if modifiers != []:
                for m in modifiers:
                    key_combination += (m << 16)
            return key_combination
        
        def _check_keys(self, key, modifier=None):
            """ Check the validity of the key and modifier """
            if isinstance(key, str) == True:
                if len(key) != 1:
                    if modifier != None:
                        raise ValueError("modifier argument has to be 'None' with a key string!")
                    #key argument is going to be parsed as a combination
                    key = self._parse_key_string(key)
                else:
                    if key in self.scintilla_keys:
                        key = self.scintilla_keys[key]
                    else:
                        key = ord(key)
            if modifier == None:
                key_combination = key
            else:
                if not(modifier in self.valid_modifiers):
                    raise ValueError("The keyboard modifier is not valid: {}".format(modifier))
                key_combination = key + (modifier << 16)
            return key_combination
        
        def clear_all_keys(self):
            """
            Clear all mappings from the internal Scintilla mapping table
            """
            self._parent.SendScintilla(
                data.QsciScintillaBase.SCI_CLEARALLCMDKEYS
            )
        
        def clear_key_combination(self, key, modifier=None):
            """
            Clear the key combination from the internal Scintilla Mapping
            Raw example of clearing the CTRL+X (Cut text function) combination:
                cmain.SendScintilla(
                    data.QsciScintillaBase.SCI_CLEARCMDKEY, 
                    ord('X') + (data.QsciScintillaBase.SCMOD_CTRL << 16)
                )
            """
            try:
                key_combination = self._check_keys(key, modifier)
            except Exception as ex:
                self._parent.main_form.display.repl_display_message(
                    str(ex), 
                    message_type=data.MessageType.ERROR
                )
                return
            self._parent.SendScintilla(
                data.QsciScintillaBase.SCI_CLEARCMDKEY, 
                key_combination
            )
        
        def set_key_combination(self, key, command, modifier=None):
            """
            Assign a key combination to a command.
            Parameters:
                key - character or key string combination
                command - Scintilla command that will execute on the key combination
                modifier - Ctrl, Alt, ...
            Raw example of assigning CTRL+D to the Cut function:
                cmain.SendScintilla(
                    data.QsciScintillaBase.SCI_ASSIGNCMDKEY, 
                    ord('D') + (data.QsciScintillaBase.SCMOD_CTRL << 16),
                    data.QsciScintillaBase.SCI_CUT
                )
            """
            try:
                key_combination = self._check_keys(key, modifier)
            except Exception as ex:
                self._parent.main_form.display.repl_display_message(
                    str(ex), 
                    message_type=data.MessageType.ERROR
                )
                return
            self._parent.SendScintilla(
                data.QsciScintillaBase.SCI_ASSIGNCMDKEY, 
                key_combination,
                command
            )



