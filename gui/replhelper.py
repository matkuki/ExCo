"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import functools
import keyword
from typing import Any

import qt
import data
import constants
import components.actionfilter
import components.linelist
import settings
import lexers
import gui.contextmenu

from gui.customeditor import *
from gui.tabwidget import *


"""
-----------------------------------------------------
Scintilla class for inputting more than one line into the REPL
-----------------------------------------------------
"""


class ReplHelper(qt.QsciScintilla):
    """
    REPL scintilla box for inputting multiple lines into the REPL.
    MUST BE PAIRED WITH A ReplLineEdit OBJECT!
    """

    # Class variables
    main_form: Any = None
    repl_master: Any = None
    # The scintilla api object(qt.QsciAPIs) must be an instace variable, or the underlying c++
    # mechanism deletes the object and the autocompletions compiled with api.prepare() are lost
    api: Any = None
    # Attribute for indicating if the REPL helper is indicated
    indicated: bool = False
    # Reference to the custom context menu
    context_menu: Any = None
    # LineList object copied from the CustomEditor object
    line_list: Any = None
    # Interpreter language

    """
    Built-in and private functions
    """

    def __init__(self, parent: Any, main_form: Any, repl_master: Any) -> None:
        # Initialize superclass, from which the current class is inherited, THIS MUST BE DONE SO THAT THE SUPERCLASS EXECUTES ITS __init__ !!!!!!
        super().__init__(parent)
        # Set default font
        self.setFont(settings.get_editor_font())
        self.main_form = main_form
        # Save the reference to the REPL object
        self.repl_master = repl_master
        # Hide the horizontal and show the vertical scrollbar
        self.SendScintilla(qt.QsciScintillaBase.SCI_SETVSCROLLBAR, True)
        self.SendScintilla(qt.QsciScintillaBase.SCI_SETHSCROLLBAR, False)
        # H ide the margin
        self.setMarginWidth(1, 0)
        # Autoindentation enabled when using "Enter" to indent to the same level as the previous line
        self.setAutoIndent(True)
        # Tabs are spaces by default
        self.setIndentationsUseTabs(False)
        # Set tab space indentation width
        self.setTabWidth(settings.get("editor")["tab_width"])
        # Set encoding format to UTF-8 (Unicode)
        self.setUtf8(True)
        # Set brace matching
        self.setBraceMatching(qt.QsciScintilla.BraceMatch.SloppyBraceMatch)
        self.setMatchedBraceBackgroundColor(qt.QColor(255, 153, 0))
        # Tabs are spaces by default
        self.setIndentationsUseTabs(False)
        # Set backspace to delete by tab widths
        self.setBackspaceUnindents(True)
        # Disable drops
        self.setAcceptDrops(False)
        # Set line endings to be Unix style ("\n")
        self.setEolMode(qt.QsciScintilla.EolMode.EolUnix)
        # Set the initial zoom factor
        self.zoomTo(settings.get("editor")["zoom_factor"])
        """
        Functionality copied from the CustomEditor to copy some of
        the neede editing functionality like commenting, ...
        """
        # Add the attributes needed to implement the line nist
        self.line_list = components.linelist.LineList(self, self.text())
        # Add the needed functions assigned from the CustomEditor
        partial_self: Any = self
        self.set_theme = functools.partial(CustomEditor.set_theme, partial_self)
        self.set_line = functools.partial(CustomEditor.set_line, partial_self)
        self.set_lines = functools.partial(CustomEditor.set_lines, partial_self)
        self.toggle_comment_uncomment = functools.partial(
            CustomEditor.toggle_comment_uncomment, partial_self
        )
        self.comment_line = functools.partial(CustomEditor.comment_line, partial_self)
        self.comment_lines = functools.partial(CustomEditor.comment_lines, partial_self)
        self.uncomment_line = functools.partial(
            CustomEditor.uncomment_line, partial_self
        )
        self.uncomment_lines = functools.partial(
            CustomEditor.uncomment_lines, partial_self
        )
        self.prepend_to_line = functools.partial(
            CustomEditor.prepend_to_line, partial_self
        )
        self.prepend_to_lines = functools.partial(
            CustomEditor.prepend_to_lines, partial_self
        )
        self.replace_line = functools.partial(CustomEditor.replace_line, partial_self)
        self.get_line = functools.partial(CustomEditor.get_line, partial_self)
        self.check_line_numbering = functools.partial(
            CustomEditor.check_line_numbering, partial_self
        )
        self.text_to_list = functools.partial(CustomEditor.text_to_list, partial_self)
        self.list_to_text = functools.partial(CustomEditor.list_to_text, partial_self)
        # Add the function and connect the signal to update the line/column positions
        self.cursorPositionChanged.connect(self._signal_editor_cursor_change)
        # Set the lexer to python
        self.set_lexer()
        # Set the initial autocompletions
        self.update_autocompletions()
        # Setup the LineList object that will hold the custom editor text as a list of lines
        self.line_list = components.linelist.LineList(self, self.text())
        self.textChanged.connect(self.text_changed)

    def _signal_editor_cursor_change(
        self, cursor_line: int | None = None, cursor_column: int | None = None
    ) -> None:
        """Signal that fires when cursor position changes"""
        self.main_form.display.update_cursor_position(cursor_line, cursor_column)

    def _filter_keypress(self, key_event: qt.QKeyEvent | None) -> bool:
        """Filter keypress for appropriate action"""
        if key_event is None:
            return False
        pressed_key = key_event.key()
        accept_keypress = False
        # Get key modifiers and check if the Ctrl+Enter was pressed
        key_modifiers = qt.QApplication.keyboardModifiers()
        if (
            key_modifiers == qt.Qt.KeyboardModifier.ControlModifier
            and pressed_key == qt.Qt.Key.Key_Return
        ) or pressed_key == qt.Qt.Key.Key_Enter:
            # ON MY KEYBOARD Ctrl+Enter CANNOT BE DETECTED!
            # Qt.ControlModifier MODIFIER SHOWS FALSE WHEN USING qt.QApplication.keyboardModifiers() + Enter
            self.repl_master.external_eval_request(self.text(), self)
            accept_keypress = True
        return accept_keypress

    def _filter_keyrelease(self, key_event: qt.QKeyEvent | None) -> bool:
        """Filter keyrelease for appropriate action"""
        # Only check indication if the current widget is not indicated
        if self.indicated == False:
            # Check indication
            self.main_form.view.indication_check()
        return False

    """
    Qt QSciScintilla functions
    """

    def keyPressEvent(self, event: qt.QKeyEvent | None) -> None:
        """QScintila keyPressEvent, to catch which key was pressed"""
        # Filter the event
        if self._filter_keypress(event) == False:
            # Execute the superclass method, if the filter ignored the event
            if event is not None:
                super().keyPressEvent(event)

    def keyReleaseEvent(self, event: qt.QKeyEvent | None) -> None:
        """QScintila KeyReleaseEvent, to catch which key was released"""
        # Execute the superclass method first, the same trick as in __init__ !
        if event is not None:
            super().keyReleaseEvent(event)
        # Filter the event
        self._filter_keyrelease(event)

    def mousePressEvent(self, event: qt.QMouseEvent | None) -> None:
        # Execute the superclass mouse click event
        if event is not None:
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
        components.actionfilter.ActionFilter.clear_action()

    def setFocus(
        self, reason: qt.Qt.FocusReason = qt.Qt.FocusReason.OtherFocusReason
    ) -> None:
        """Overridden focus event"""
        # Execute the supeclass focus function
        super().setFocus(reason)
        # Check indication
        self.main_form.view.indication_check()

    def wheelEvent(self, wheel_event: qt.QWheelEvent | None) -> None:
        """Overridden mouse wheel rotate event"""
        if wheel_event is None:
            return
        key_modifiers = qt.QApplication.keyboardModifiers()
        delta = wheel_event.angleDelta().y()
        if delta < 0:
            if key_modifiers == qt.Qt.KeyboardModifier.ControlModifier:
                # Zoom out the scintilla tab view
                self.zoomOut()
        else:
            if key_modifiers == qt.Qt.KeyboardModifier.ControlModifier:
                # Zoom in the scintilla tab view
                self.zoomIn()
        # Handle the event
        if key_modifiers != qt.Qt.KeyboardModifier.ControlModifier:
            # Execute the superclass method
            super().wheelEvent(wheel_event)
        else:
            # Propagate(send forward) the wheel event to the parent
            wheel_event.ignore()

    def delete_context_menu(self) -> None:
        # Clean up the context menu
        if self.context_menu != None:
            self.context_menu.hide()
            for b in self.context_menu.button_list:
                b.setParent(None)
            self.context_menu.setParent(None)
            self.context_menu = None

    def contextMenuEvent(self, event: qt.QContextMenuEvent | None) -> None:
        # Built-in context menu
        self.delete_context_menu()
        # Show a context menu according to the current lexer
        if event is None:
            return
        offset = (event.x(), event.y())
        height = self.size().height()
        if height < 100:
            _type = "multiline-repl-horizontal"
        else:
            _type = "multiline-repl-normal"
        self.context_menu = gui.contextmenu.create(
            self, self.main_form, offset=offset, _type=_type
        )
        self.context_menu.popup_at_cursor()
        event.accept()

    def set_lexer(self) -> None:
        current_lexer: Any = self.lexer()
        if current_lexer is not None:
            current_lexer.setParent(None)
            self.setLexer(None)
        # Create the new lexer
        lexer: Any = lexers.Python()
        lexer.setParent(self)
        result = lexers.get_comment_style_for_lexer(lexer)
        lexer.open_close_comment_style = result[0]
        lexer.comment_string = result[1]
        lexer.end_comment_string = result[2]
        # Set the lexers default font
        lexer.setDefaultFont(settings.get_editor_font())
        # Set the lexer with the initial autocompletions
        self.setLexer(lexer)
        # Set the theme
        self.set_theme(settings.get_theme())
        active_lexer: Any = self.lexer()
        active_lexer.set_theme(settings.get_theme())

    def refresh_lexer(self) -> None:
        # Set the theme
        self.set_theme(settings.get_theme())
        active_lexer: Any = self.lexer()
        active_lexer.set_theme(settings.get_theme())

    def text_changed(self) -> None:
        """Event that fires when the scintilla document text changes"""
        # Update the line list
        self.line_list.update_text_to_list(self.text())

    """
    ReplHelper autocompletion functions
    """

    def update_autocompletions(self, new_autocompletions: list[str] = []) -> None:
        """Function for updating the ReplHelper autocompletions"""
        # Set the lexer
        self.refresh_lexer()
        # Set the scintilla api for the autocompletions (MUST BE AN INSTANCE VARIABLE)
        self.api = qt.QsciAPIs(self.lexer())
        # Populate the api with all of the python keywords
        for kw in keyword.kwlist:
            self.api.add(kw)
        for word in new_autocompletions:
            self.api.add(word)
        self.api.prepare()
        # Set how many characters must be typed for the autocompletion popup to appear
        self.setAutoCompletionThreshold(1)
        # Set the source from where the autocompletions will be fetched
        self.setAutoCompletionSource(qt.QsciScintilla.AutoCompletionSource.AcsAll)
        # Set autocompletion case sensitivity
        self.setAutoCompletionCaseSensitivity(False)
