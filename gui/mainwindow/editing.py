"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.

Editor-level actions (indent, comment, scroll, selection, etc.)
and the inner Line helper for line-based operations. Namespace
class attached to the MainWindow instance.
"""

import collections

from typing import List, Optional, Any, TYPE_CHECKING

import constants
from gui.customeditor import CustomEditor

if TYPE_CHECKING:
    from gui.mainwindow import MainWindow


class Editing:
    """
    Document editing functions
    (namespace/nested class to MainWindow)
    """

    # Class varibles
    _parent: "MainWindow"

    def __init__(self, parent: "MainWindow") -> None:
        """Initialization of the Editing object instance"""
        # Get the reference to the MainWindow parent object instance
        self._parent = parent
        # Initialize the namespace classes
        self.line = self.Line(self)

    def find_in_open_documents(
        self,
        search_text: str,
        case_sensitive: bool = False,
        regular_expression: bool = False,
        window_name: Optional[str] = None,
    ) -> bool:
        """
        Find instances of search text accross all open documents
        in the selected window
        """
        # Get the current widget
        tab_widget = self._parent.get_window_by_indication()
        if window_name is None:
            window_name = "Main"
        # Check if there are any documents in the basic widget
        if tab_widget.count() == 0:
            message = "No documents in " + tab_widget.name.lower()
            message += " editing window"
            self._parent.display.repl_display_message(
                message, message_type=constants.MessageType.WARNING
            )
            return
        # Save the current index to reset focus to it if no
        # instances of search string are found
        saved_index = tab_widget.currentIndex()
        # Create a deque of the tab index order and start with the current
        # index, deque is used, because it can be rotated by default
        in_deque = collections.deque(range(tab_widget.count()))
        # Rotate the deque until the first element is the current index
        while in_deque[0] != tab_widget.currentIndex():
            in_deque.rotate(1)
        # Set a flag for the first document
        first_document = True
        for i in in_deque:
            # Skip the current widget if it's not an editor
            if isinstance(tab_widget.widget(i), CustomEditor) == False:
                continue
            # Place the cursor to the top of the document
            # if it is not the current document
            if first_document == True:
                first_document = False
            else:
                tab_widget.widget(i).setCursorPosition(0, 0)
            # Find the text
            result = tab_widget.widget(i).find_text(
                search_text,
                case_sensitive,
                True,  # search_forward
                regular_expression,
            )
            # If a replace was done, return success
            # I can't remember why CYCLED was added here???
            #                if (result == constants.SearchResult.FOUND or
            #                    result == constants.SearchResult.CYCLED):
            if result == constants.SearchResult.FOUND:
                return True
        # Nothing found
        tab_widget.setCurrentIndex(saved_index)
        message = "No instances of '" + search_text + "' found in "
        message += tab_widget.name.lower() + " editing window"
        self._parent.display.repl_display_message(
            message, message_type=constants.MessageType.WARNING
        )
        return False

    def find_replace_in_open_documents(
        self,
        search_text: str,
        replace_text: str,
        case_sensitive: bool = False,
        regular_expression: bool = False,
        window_name: Optional[str] = None,
    ) -> bool:
        """
        Find and replace instaces of search string with replace string
        across all of the open documents in the selected window, one
        instance at a time, starting from the currently selected widget.
        """
        # Get the current widget
        tab_widget = self._parent.get_window_by_indication()
        if window_name is None:
            window_name = "Main"
        # Check if there are any documents in the basic widget
        if tab_widget.count() == 0:
            message = "No documents in the " + tab_widget.name.lower()
            message += " editing window"
            self._parent.display.repl_display_message(
                message, message_type=constants.MessageType.WARNING
            )
            return
        # Save the current index to reset focus to it if no instances of search string are found
        saved_index = tab_widget.currentIndex()
        # Create a deque of the tab index order and start with the current index,
        # deque is used, because it can be rotated by default
        in_deque = collections.deque(range(tab_widget.count()))
        # Rotate the deque until the first element is the current index
        while in_deque[0] != tab_widget.currentIndex():
            in_deque.rotate(1)
        # Find the next instance
        for i in in_deque:
            result = tab_widget.widget(i).find_and_replace(
                search_text, replace_text, case_sensitive, regular_expression
            )
            # If a replace was done, return success
            if result == True:
                message = "Found and replaced in " + tab_widget.name.lower()
                message += " editing window"
                self._parent.display.write_to_statusbar(message)
                return True
        # Nothing found
        tab_widget.setCurrentIndex(saved_index)
        message = "No instances of '" + search_text + "' found in the "
        message += tab_widget.name.lower() + " editing window"
        self._parent.display.repl_display_message(
            message, message_type=constants.MessageType.WARNING
        )
        return False

    def replace_all_in_open_documents(
        self,
        search_text: str,
        replace_text: str,
        case_sensitive: bool = False,
        regular_expression: bool = False,
        window_name: Optional[str] = None,
    ) -> None:
        """
        Replace all instaces of search string with replace string across
        all of the open documents in the selected window
        """
        # Get the current widget
        tab_widget = self._parent.get_window_by_indication()
        if window_name is None:
            window_name = "Main"
        # Loop over each widget and replace all instances of the search text
        for i in range(tab_widget.count()):
            tab_widget.widget(i).replace_all(
                search_text, replace_text, case_sensitive, regular_expression
            )
        message = "Replacing all in open documents completed"
        self._parent.display.repl_display_message(
            message, message_type=constants.MessageType.SUCCESS
        )

    """
    Special wraper functions that take a existing function and
    execute it for the currently focused CustomEditor.
    """

    def run_focused_widget_method(
        self,
        method_name: str,
        argument_list: List[Any],
        window_name: Optional[str] = None,
    ) -> None:
        """Execute a focused widget method"""
        display: Any = self._parent.display
        # Get the current widget
        #            widget = self._parent.get_tab_by_focus()
        widget = self._parent.get_tab_by_indication()
        # None-check the current widget in the selected window
        if widget is None:
            message = "No document in focused window!"
            display.repl_display_message(
                message, message_type=constants.MessageType.WARNING
            )
            return
        # Non-editor tabs (trees, terminals, viewers) don't implement
        # every document operation this wrapper can be asked to run
        method = getattr(widget, method_name, None)
        if method is None:
            message = "'" + type(widget).__name__ + "' does not support '"
            message += method_name + "()'"
            display.repl_display_message(
                message, message_type=constants.MessageType.WARNING
            )
            return
        # Argument list has to be preceded by the '*' character
        method(*argument_list)

    def find(
        self,
        search_text: str,
        case_sensitive: bool = False,
        search_forward: bool = True,
        regular_expression: bool = False,
        window_name: Optional[str] = None,
    ) -> None:
        """Find text in the currently focused window"""
        argument_list = [search_text, case_sensitive, search_forward, regular_expression]
        self.run_focused_widget_method("find_text", argument_list, window_name)

    def find_and_replace(
        self,
        search_text: str,
        replace_text: str,
        case_sensitive: bool = False,
        search_forward: bool = True,
        regular_expression: bool = False,
        window_name: Optional[str] = None,
    ) -> None:
        """Find and replace text in the currently focused window"""
        argument_list = [
            search_text,
            replace_text,
            case_sensitive,
            search_forward,
            regular_expression,
        ]
        self.run_focused_widget_method("find_and_replace", argument_list, window_name)

    def replace_all(
        self,
        search_text: str,
        replace_text: str,
        case_sensitive: bool = False,
        regular_expression: bool = False,
        window_name: Optional[str] = None,
    ) -> None:
        """Replace all occurences of a string in the currently focused window"""
        argument_list = [search_text, replace_text, case_sensitive, regular_expression]
        self.run_focused_widget_method("replace_all", argument_list, window_name)

    def replace_in_selection(
        self,
        search_text: str,
        replace_text: str,
        case_sensitive: bool = False,
        regular_expression: bool = False,
        window_name: Optional[str] = None,
    ) -> None:
        """Replace all occurences of a string in the current selection in the currently focused window"""
        argument_list = [search_text, replace_text, case_sensitive, regular_expression]
        self.run_focused_widget_method("replace_in_selection", argument_list, window_name)

    def highlight(
        self,
        highlight_text: str,
        case_sensitive: bool = False,
        regular_expression: bool = False,
        window_name: Optional[str] = None,
    ) -> None:
        """Highlight all occurences of text in the currently focused window"""
        argument_list = [highlight_text, case_sensitive, regular_expression]
        self.run_focused_widget_method("highlight_text", argument_list, window_name)

    def clear_highlights(self, window_name: Optional[str] = None) -> None:
        """Clear all highlights in the currently focused window"""
        argument_list = []
        self.run_focused_widget_method("clear_highlights", argument_list, window_name)

    def convert_case(self, uppercase: bool = True, window_name: Optional[str] = None) -> None:
        """Change the case of the selected text in the currently focused window"""
        argument_list = [uppercase]
        self.run_focused_widget_method("convert_case", argument_list, window_name)

    class Line:
        # Class varibles
        _parent: "Editing"

        def __init__(self, parent: "Editing") -> None:
            """Initialization of the Editing object instance"""
            # Get the reference to the MainWindow parent object instance
            self._parent = parent

        def _run(self, method_name: str, argument_list: list, window_name=None) -> None:
            self._parent.run_focused_widget_method(method_name, argument_list, window_name)

        def goto(self, line_number: int, window_name: Optional[str] = None) -> None:
            """Set focus and cursor to the selected line in the currently focused window"""
            self._run("goto_line", [line_number], window_name)

        def replace(
            self, replace_text: str, line_number: int, window_name: Optional[str] = None
        ) -> None:
            """Replace the selected line in the currently focused window"""
            self._run("replace_line", [replace_text, line_number], window_name)

        def remove(self, line_number: int, window_name: Optional[str] = None) -> None:
            """Remove the selected line in the currently focused window"""
            self._run("remove_line", [line_number], window_name)

        def get(self, line_number: int, window_name: Optional[str] = None) -> None:
            """Replace the selected line in the currently focused window"""
            self._run("get_line", [line_number], window_name)

        def set(self, line_text: str, line_number: int, window_name: Optional[str] = None) -> None:
            """Replace the selected line in the currently focused window"""
            self._run("set_line", [line_text, line_number], window_name)
