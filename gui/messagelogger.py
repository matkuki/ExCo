"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import os
import os.path
from typing import Any

import qt
import data
import settings
import components.actionfilter


"""
----------------------------------------------------------------------------
Object for showing log messages across all widgets, mostly for debug purposes
----------------------------------------------------------------------------
"""


class MessageLogger(qt.QWidget):
    """Simple subclass for displaying log messages"""

    class MessageTextBox(qt.QTextEdit):
        def contextMenuEvent(self, event: qt.QContextMenuEvent | None) -> None:
            if event is not None:
                event.accept()

    # Controls and variables of the log window  (class variables >> this means that these variables are shared accross instances of this class)
    displaybox: "MessageLogger.MessageTextBox | None" = (
        None  # QTextEdit that will display log messages
    )
    log_layout: qt.QGridLayout | None = None  # The layout of the log window

    def __init__(self, parent: qt.QWidget) -> None:
        """Initialization routine"""
        # Initialize superclass, from which the current class is inherited, THIS MUST BE DONE SO THAT THE SUPERCLASS EXECUTES ITS __init__ !!!!!!
        super().__init__()

        # Initialize the log window
        self.setWindowTitle("LOGGING WINDOW")
        self.resize(500, 300)
        self.setWindowFlags(qt.Qt.WindowType.WindowStaysOnTopHint)
        # Set default font
        self.setFont(settings.get_current_font())

        # Initialize the display box
        self.displaybox = MessageLogger.MessageTextBox(self)
        self.displaybox.setReadOnly(True)
        # Make displaybox click/doubleclick event also fire the log window click/doubleclick method
        self.displaybox.mousePressEvent = self._event_mousepress  # type: ignore[assignment]
        self.displaybox.mouseDoubleClickEvent = self._event_mouse_doubleclick  # type: ignore[assignment]
        self.keyPressEvent = self._keypress  # type: ignore[assignment]

        # Initialize layout
        self.log_layout = qt.QGridLayout()
        self.log_layout.addWidget(self.displaybox)
        self.setLayout(self.log_layout)

        self.append_message("Ex.Co. debug log window loaded")
        self.append_message("LOGGING Mode is enabled")
        self._parent = parent

        # Set the log window icon
        if os.path.isfile(data.application_icon) == True:
            self.setWindowIcon(qt.QIcon(data.application_icon))

    def _event_mouse_doubleclick(self, mouse_event: qt.QMouseEvent | None) -> None:
        """Rereferenced/overloaded displaybox doubleclick event"""
        self.clear_log()

    def _event_mousepress(self, mouse_event: qt.QMouseEvent | None) -> None:
        """Rereferenced/overloaded displaybox click event"""
        # Reset the click&drag context menu action
        components.actionfilter.ActionFilter.clear_action()

    def _keypress(self, key_event: qt.QKeyEvent | None) -> None:
        """Rereferenced/overloaded MessageLogger keypress event"""
        if key_event is None:
            return
        pressed_key = key_event.key()
        if pressed_key == qt.Qt.Key.Key_Escape:
            self.close()

    def clear_log(self) -> None:
        """Clear all messages from the log display"""
        if self.displaybox is not None:
            self.displaybox.clear()

    def append_message(self, *args: Any, **kwargs: Any) -> None:
        """Adds a message as a string to the log display if logging mode is enabled"""
        if len(args) > 1:
            message = " ".join(args)
        else:
            message = args[0]
        # Check if message is a string class, if not then make it a string
        if isinstance(message, str) == False:
            message = str(message)
        # Check if logging mode is enabled
        if data.logging_mode == True and self.displaybox is not None:
            self.displaybox.append(message)
        # Bring cursor to the current message (this is in a QTextEdit not QScintilla)
        if self.displaybox is None:
            return
        cursor = self.displaybox.textCursor()
        cursor.movePosition(qt.QTextCursor.MoveOperation.End)
        cursor.movePosition(qt.QTextCursor.MoveOperation.StartOfLine)
        self.displaybox.setTextCursor(cursor)
