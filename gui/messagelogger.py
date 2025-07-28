"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import os
import os.path
import qt
import data
import components.actionfilter


"""
----------------------------------------------------------------------------
Object for showing log messages across all widgets, mostly for debug purposes
----------------------------------------------------------------------------
"""


class MessageLogger(qt.QWidget):
    """Simple subclass for displaying log messages"""

    class MessageTextBox(qt.QTextEdit):
        def contextMenuEvent(self, event):
            event.accept()

    # Controls and variables of the log window  (class variables >> this means that these variables are shared accross instances of this class)
    displaybox = None  # QTextEdit that will display log messages
    layout = None  # The layout of the log window
    parent = None

    def __init__(self, parent):
        """Initialization routine"""
        # Initialize superclass, from which the current class is inherited, THIS MUST BE DONE SO THAT THE SUPERCLASS EXECUTES ITS __init__ !!!!!!
        super().__init__()

        # Initialize the log window
        self.setWindowTitle("LOGGING WINDOW")
        self.resize(500, 300)
        self.setWindowFlags(qt.Qt.WindowStaysOnTopHint)
        # Set default font
        self.setFont(settings.get_current_font())

        # Initialize the display box
        self.displaybox = MessageLogger.MessageTextBox(self)
        self.displaybox.setReadOnly(True)
        # Make displaybox click/doubleclick event also fire the log window click/doubleclick method
        self.displaybox.mousePressEvent = self._event_mousepress
        self.displaybox.mouseDoubleClickEvent = self._event_mouse_doubleclick
        self.keyPressEvent = self._keypress

        # Initialize layout
        self.layout = qt.QGridLayout()
        self.layout.addWidget(self.displaybox)
        self.setLayout(self.layout)

        self.append_message("Ex.Co. debug log window loaded")
        self.append_message("LOGGING Mode is enabled")
        self._parent = parent

        # Set the log window icon
        if os.path.isfile(data.application_icon) == True:
            self.setWindowIcon(qt.QIcon(data.application_icon))

    def _event_mouse_doubleclick(self, mouse_event):
        """Rereferenced/overloaded displaybox doubleclick event"""
        self.clear_log()

    def _event_mousepress(self, mouse_event):
        """Rereferenced/overloaded displaybox click event"""
        # Reset the click&drag context menu action
        components.actionfilter.ActionFilter.clear_action()

    def _keypress(self, key_event):
        """Rereferenced/overloaded MessageLogger keypress event"""
        pressed_key = key_event.key()
        if pressed_key == qt.Qt.Key_Escape:
            self.close()

    def clear_log(self):
        """Clear all messages from the log display"""
        self.displaybox.clear()

    def append_message(self, *args, **kwargs):
        """Adds a message as a string to the log display if logging mode is enabled"""
        if len(args) > 1:
            message = " ".join(args)
        else:
            message = args[0]
        # Check if message is a string class, if not then make it a string
        if isinstance(message, str) == False:
            message = str(message)
        # Check if logging mode is enabled
        if data.logging_mode == True:
            self.displaybox.append(message)
        # Bring cursor to the current message (this is in a QTextEdit not QScintilla)
        cursor = self.displaybox.textCursor()
        cursor.movePosition(qt.QTextCursor.End)
        cursor.movePosition(qt.QTextCursor.StartOfLine)
        self.displaybox.setTextCursor(cursor)
