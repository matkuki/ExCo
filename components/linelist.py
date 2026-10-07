"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import re
from typing import Any, Callable

# All three line-end forms in one pattern, so "\r\n" is treated as a single
# line end instead of a lone "\r" followed by a lone "\n".
_LINE_END_REGEX = re.compile(r"\r\n|\r|\n")


def split_lines(text: str) -> list[str]:
    """Split text into lines on CRLF, CR or LF line ends."""
    return _LINE_END_REGEX.split(text)


def eol_string(mode: int) -> str:
    """Return the line-end string for a QsciScintilla EolMode value
    (0 = Windows CRLF, 1 = Mac CR, 2 = Unix LF)."""
    if mode == 0:
        return "\r\n"
    if mode == 1:
        return "\r"
    return "\n"


class LineList(list):
    """
    List object that will hold the lines of the CustomEditor.
    It's a subclassed Python built-in list object for easier text manipulation.

    Indexing is standard Python (0-based, slice stops are exclusive).
    Every write forwards the change to the parent editor document.
    """

    # Class variables
    _parent: Any = None

    """
    Class functions/methods
    """

    def __init__(self, parent: Any, initial_text: Any) -> None:
        """Overridden init function"""
        # Initialize superclass
        super().__init__()
        # Set the reference to the parent object
        self._parent = parent
        # Set the initial content (an empty string is one empty line,
        # exactly like the editor document it mirrors)
        if isinstance(initial_text, str):
            self.update_text_to_list(initial_text)

    def __setitem__(self, key: Any, value: Any) -> None:
        """Overridden list method that sets the specified line(item) and
        forwards the change to the parent editor document"""
        # Check if the value is a string or a list
        if isinstance(value, str) == False and isinstance(value, list) == False:
            raise Exception("Value has to be a list or a string!")
        # Set a single line
        if isinstance(value, str):
            if isinstance(key, int) == False:
                raise Exception("A string value needs an integer index!")
            # Translate the possibly negative index to a positive one
            actual_key = key if key >= 0 else len(self) + key
            try:
                super().__setitem__(key, value)
            except IndexError:
                self.append(value, update_parent=False)
            # Update the custom editor document text (line numbers are 1-based)
            self._parent.set_line(value, actual_key + 1)
            return
        # The value is a list, so the key has to be a slice
        if isinstance(key, slice) == False:
            raise Exception("A list value needs a slice!")
        if all(isinstance(item, str) for item in value) == False:
            raise Exception("All value list items must be strings!")
        # Resolve the slice bounds against the current length
        start, stop, step = key.indices(len(self))
        if step != 1:
            raise Exception("Slice steps are not supported!")
        # Check the boundaries - slice length is (stop - start)
        if len(value) != stop - start:
            raise Exception("Ranges of assignment don't match!")
        # Insert the range into the custom list object
        super().__setitem__(slice(start, stop), value)
        # Set the new lines in the custom editor document
        if stop > start:
            self._parent.set_lines(start, stop, value)

    # In-place operators not implemented; delegating to base list would change
# the list without notifying the parent editor.

    def _setitem(self, key: int, value: Any) -> None:
        """Set the item at position-key, without updating the scintilla document"""
        # Check if the value is a string
        if isinstance(value, str) == False:
            return
        try:
            super().__setitem__(key, value)
        except IndexError:
            self.append(value, update_parent=False)

    def _update_list_to_text(self, scroll_to_line: int | None = None) -> None:
        """Update the list of lines to the parent CustomEditor document"""
        # Merge the list into a single string with the
        # newline character as the delimiter
        text = "\n".join(self)
        # Update the text of the document
        self._parent.set_all_text(text)
        # Check if a line to which to scroll to was specified
        if scroll_to_line == None:
            scroll_to_line = self._parent.lines()
        # Scroll to the desired line of the document
        self._parent.setCursorPosition(scroll_to_line, 0)

    def append(self, value: Any, update_parent: bool = True) -> None:
        """
        Overloaded list append method
        Special arguments:
            update_parent   - False: append to list internally without updating
                                     the parent CustomEditor document.
                              True:  append to list and update the parent
                                     CustomEditor document.
        """
        # Check the update_parent parameter type
        if isinstance(update_parent, bool) == False:
            raise Exception("'update_parent' parameter must be of type boolean!")
        # Check the append value type
        if isinstance(value, str):
            # Execute the superclass append method
            super().append(value)
        elif isinstance(value, list):
            exception_text = "Use 'extend' to add multiple lines!"
            raise Exception(exception_text)
        else:
            exception_text = "'append' parameter must be a string!"
            raise Exception(exception_text)
        # Check if updating the parent document is needed
        if update_parent == True:
            self._update_list_to_text()

    def extend(self, value: Any, update_parent: bool = True) -> None:
        """
        Overloaded list extend method
        Special arguments:
            update_parent   - False: append to list internally without updating
                                     the parent CustomEditor document.
                              True:  append to list and update the parent
                                     CustomEditor document.
        """
        # Check the update_parent parameter type
        if isinstance(update_parent, bool) == False:
            raise Exception("'update_parent' parameter must be of type boolean!")
        # Check the extend value type
        if isinstance(value, list) == False:
            raise Exception("Extend parameter must be a list!")
        elif all(isinstance(item, str) for item in value) == False:
            raise Exception("All extend list items must be strings!")
        # Extend the list
        super().extend(value)
        # Check if updating the parent document is needed
        if update_parent == True:
            self._update_list_to_text()

    def insert(self, index: Any, value: Any, update_parent: bool = True) -> None:
        """Overloaded insert method (0-based index, like list.insert)"""
        # Check the insert index type
        if isinstance(index, int) == False:
            raise Exception("Insert index parameter must be an integer!")
        # Check the insert value type
        if isinstance(value, str) == False:
            raise Exception("Insert parameter must be a string!")
        # Translate the possibly negative index to a positive one
        actual_index = index if index >= 0 else len(self) + index
        # Insert the item
        super().insert(index, value)
        # Check if updating the parent document is needed
        if update_parent == True:
            self._update_list_to_text(max(actual_index, 0))

    def pop(self, index: Any = None, update_parent: bool = True) -> Any:
        """Overloaded pop method (0-based index, like list.pop)"""
        # Check the pop index type
        if index is not None and isinstance(index, int) == False:
            raise Exception("Pop index parameter must be an integer!")
        if index is None:
            return_item = super().pop()
            scroll_to_line = max(len(self), 0)
        else:
            # Translate the possibly negative index to a positive one
            actual_index = index if index >= 0 else len(self) + index
            return_item = super().pop(index)
            scroll_to_line = max(actual_index, 0)
        # Check if updating the parent document is needed
        if update_parent == True:
            self._update_list_to_text(scroll_to_line)
        # Return the poped line
        return return_item

    def remove(self, item: Any, update_parent: bool = True) -> None:
        """Overloaded remove method"""
        # Check the insert index type
        if isinstance(item, str) == False:
            raise Exception("Remove item parameter must be a string!")
        # Check if item exists
        if not (item in self):
            raise Exception("Cannot remove item! Item is not in the list!")
        index = self.index(item)
        # Remove the item
        super().remove(item)
        # Check if updating the parent document is needed
        if update_parent == True:
            self._update_list_to_text(max(index - 1, 0))

    def reverse(self, update_parent: bool = True) -> None:
        """Overloaded reverse method"""
        # Reverse the list
        super().reverse()
        # Check if updating the parent document is needed
        if update_parent == True:
            self._update_list_to_text()

    def sort(
        self,
        key: Callable[[str], Any] | None = None,
        reverse: bool = False,
        update_parent: bool = True,
    ) -> None:
        """Overloaded sort method"""
        super().sort(key=key, reverse=reverse)
        if update_parent:
            self._update_list_to_text()

    def update_text_to_list(self, update_text: Any) -> None:
        """Update the list from a string"""
        # Check if the value is a string
        if isinstance(update_text, str) == False:
            return
        # Empty the list
        self._clear()
        # Set the new content
        self.extend(split_lines(update_text), update_parent=False)

    def get_absolute_cursor_position(self) -> int:
        """Get the absolute cursor position in characters, where every
        line end counts as one LF character.
        NOTE:
            This function returns the actual length of characters,
            NOT the length of bytes!
        """
        line, index = self._parent.getCursorPosition()
        absolute_position = 0
        for i in range(line):
            absolute_position += len(self[i]) + 1
        absolute_position += index
        return absolute_position

    def _clear(self) -> None:
        del self[:]
