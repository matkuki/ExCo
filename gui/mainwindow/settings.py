"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.

Settings GUI dialog launcher and menu wiring.

Provides the settings manipulator window, recent-file-list
management, and keyboard-shortcut reloading. Namespace class
attached to the MainWindow instance.
"""

import functools
import os
from typing import Optional, TYPE_CHECKING

import constants
import gui.contextmenu
import qt
import settings

if TYPE_CHECKING:
    from gui.mainwindow import MainWindow


class Settings:
    """
    Functions for manipulating the application settings
    (namespace/nested class to MainWindow)
    """

    # Class varibles
    _parent: "MainWindow" = None
    # GUI Settings manipulator
    gui_manipulator = None

    def __init__(self, parent: "MainWindow") -> None:
        """
        Initialization of the Settings object instance
        """
        # Get the reference to the MainWindow parent object instance
        self._parent = parent

    def update_recent_list(self, new_file: Optional[str] = None) -> None:
        """
        Update the settings manipulator with the new file
        """

        # Nested function for opening the recent file
        def new_file_function(file):
            try:
                self._parent.open_file(file=file, tab_widget=None)
                self._parent.get_largest_window().currentWidget().setFocus()
            except:
                pass

        # Update the file manipulator
        if new_file is not None:
            settings.add_recent_file(new_file)
        # Refresh the menubar recent list
        recent_files_menu = self._parent.recent_files_menu
        # !!Clear all of the actions from the menu OR YOU'LL HAVE MEMORY LEAKS!!
        for action in recent_files_menu.actions():
            recent_files_menu.removeAction(action)
            action.setParent(None)
            action.deleteLater()
            action = None
        recent_files_menu.clear()
        # Add the new recent files list to the menu
        for recent_file in reversed(settings.get("recent_files")):
            # Iterate in the reverse order, so that the last file will be displayed
            # on the top of the menubar "Recent Files" menu
            recent_file_name = recent_file
            # Check if the filename has too many characters
            if len(recent_file_name) > 30:
                # Shorten the name that will appear in the menubar
                recent_file_name = "...{}".format(
                    os.path.splitdrive(recent_file)[1][-30:]
                )
            new_file_action = qt.QAction(recent_file_name, recent_files_menu)
            new_file_action.setStatusTip("Open: {}".format(recent_file))
            # Create a function reference for opening the recent file
            temp_function = functools.partial(new_file_function, recent_file)
            new_file_action.triggered.connect(temp_function)
            recent_files_menu.addAction(new_file_action)

    def clear_recent_list(self) -> None:
        settings.clear_recent_files()

    def restore(self) -> None:
        """Restore the previously stored settings"""
        # Load the settings from the initialization file
        result = settings.load()
        # Update the theme
        self._parent.view.refresh_theme()
        # Update recent files list in the menubar
        self.update_recent_list()
        # Update sessions list in the menubar
        self._parent.sessions.update_menu()
        # Display message in statusbar
        self._parent.display.write_to_statusbar("Restored settings", 1000)
        # Update custon context menu functions
        for func_type in settings.get("context_menu_functions").keys():
            funcs = settings.get("context_menu_functions")[func_type]
            for func_key in funcs.keys():
                getattr(gui.contextmenu.ContextMenuHex, func_type)[func_key] = funcs[
                    func_key
                ]
        # Display the settings load error AFTER the theme has been set
        # Otherwise the error text color will not be styled correctly
        if result == False:
            self._parent.display.repl_display_message(
                "Error loading the settings file, using the default settings values!\nTHE SETTINGS FILE WILL NOT BE UPDATED!",
                message_type=constants.MessageType.ERROR,
            )
