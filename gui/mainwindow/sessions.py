"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.

Session save/restore logic.

Handles saving/loading editor state, recent file lists,
and restoring window layouts. Namespace class attached to
the MainWindow instance.
"""

import functools
import os
import traceback

from typing import Any, List, Optional, TYPE_CHECKING

import constants
import functions
import qt
import settings
from gui.dialogs import RestoreSessionDialog
from gui.menu import Menu

if TYPE_CHECKING:
    from gui.mainwindow import MainWindow


class Sessions:
    """
    Functions for manipulating sessions
    (namespace/nested class to MainWindow)
    """

    # Class varibles
    _parent: "MainWindow"

    def __init__(self, parent: "MainWindow") -> None:
        """Initialization of the Sessions object instance"""
        # Get the reference to the MainWindow parent object instance
        self._parent = parent

    def add(self, session_name: str, session_group_chain: Optional[List[str]] = None) -> Optional[bool]:
        """Add the current opened documents in the main and upper window"""
        if session_group_chain is None:
            session_group_chain = []
        # Check if the session name is too short
        if len(session_name) < 3:
            self._parent.display.repl_display_message(
                "Session name is too short!",
                message_type=constants.MessageType.ERROR,
            )
            return None
        if isinstance(session_group_chain, tuple):
            session_group_chain = list(session_group_chain)
        if isinstance(session_group_chain, list) == False:
            self._parent.display.repl_display_message(
                "Group name must be a tuple/list of strings!",
                message_type=constants.MessageType.ERROR,
            )
            return None
        # Create lists of files in each window
        try:
            all_windows = self._parent.get_all_windows()
            #                if len(all_windows) > 0 and any([x.count() > 0 for x in all_windows]) > 0:
            if len(all_windows) > 0:
                # Walk the group chain and check if the session is already stored
                session_found = False
                group = settings.get("stored_sessions")["main"]
                for c in session_group_chain:
                    if c not in group["groups"].keys():
                        message = "Group '{}' in the session chain was not found!".format(c)
                        self._parent.display.repl_display_message(
                            message, message_type=constants.MessageType.ERROR
                        )
                        self._parent.display.write_to_statusbar(message, 1500)
                        return False
                    group = group["groups"][c]
                if session_name in group["sessions"].keys():
                    session_found = True
                # Store the session
                settings.get_sessions().add_session(
                    session_name,
                    session_group_chain,
                    self._parent.view.layout_generate(),
                )
                if session_found == True:
                    message = "Session '{}/{}' overwritten!".format(
                        "/".join(session_group_chain), session_name
                    )
                else:
                    message = "Session '{}/{}' added!".format(
                        "/".join(session_group_chain), session_name
                    )
                self._parent.display.repl_display_message(
                    message, message_type=constants.MessageType.SUCCESS
                )
                # Refresh the sessions menu in the menubar
                self.update_menu()
                # Return success
                return True
            else:
                self._parent.display.repl_display_message(
                    "No documents to store!",
                    message_type=constants.MessageType.ERROR,
                )
                self._parent.display.write_to_statusbar("No documents to store!", 1500)
                # Return error
                return False
        except:
            self._parent.display.repl_display_error(traceback.format_exc())
            message = "An error occurred while storing the session!"
            self._parent.display.repl_display_error(message)
            self._parent.display.write_to_statusbar(message, 1500)
            # Return error
            return False

    def restore(self, session: dict) -> None:
        """
        Restore the files as stored in the selected session
        """
        # Check if the session was found
        if session is None:
            message = "Session was not found!"
            self._parent.display.repl_display_message(
                message, message_type=constants.MessageType.ERROR
            )
            self._parent.display.write_to_statusbar(message, 1500)
            return
        # Check if there are any modified documents
        if self._parent.check_document_states() == True:
            message = (
                "Restoring session: '{}'\n".format(session["name"])
                + "You have modified documents!\n"
                + "What do you wish to do?"
            )
            reply = RestoreSessionDialog.question(message)
            if reply == constants.DialogResult.SaveAndRestore.value:
                self.file_save_all()
            elif reply == constants.DialogResult.Cancel.value:
                return
        # Clear all documents from the main and upper window
        self._parent.close_all_tabs()
        # Add files to windows
        self._parent.view.layout_restore(session["layout"])

    def exco_restore(self) -> None:
        """
        Open all the source files for Ex.Co.
        """
        # Check if there are any modified documents
        if self._parent.check_document_states() == True:
            message = (
                "Restoring Ex.Co. development session\n"
                + "You have modified documents!\n"
                + "What do you wish to do?"
            )
            reply = RestoreSessionDialog.question(message)
            if reply == constants.DialogResult.SaveAndRestore.value:
                self.file_save_all()
            elif reply == constants.DialogResult.Cancel.value:
                return
        # Clear all documents from the main and upper window
        self._parent.get_largest_window().clear()
        # Loop through the aplication directory and add the relevant files
        exco_main_files = []
        exco_dir = settings.get("application-directory")
        exco_dirs = [
            exco_dir,
            os.path.join(exco_dir, "themes"),
            os.path.join(exco_dir, "cython"),
        ]
        for directory in exco_dirs:
            if os.path.isdir(directory) == False:
                continue
            for item in os.listdir(directory):
                file_extension = os.path.splitext(item)[1].lower()
                if (
                    file_extension == ".py"
                    or file_extension == ".pyw"
                    or file_extension == ".pyx"
                    or file_extension == ".pxd"
                    or file_extension == ".pxi"
                    or file_extension == ".cfg"
                ):
                    file = os.path.join(directory, item)
                    exco_main_files.append(file)
        # Sort the files by name
        exco_main_files.sort()
        # Add the files to the main window
        for file in exco_main_files:
            self._parent.open_file(file, self._parent.get_largest_window())

    def remove(self, session_name: str, session_group_chain: Optional[List[str]] = None) -> None:
        """
        Delete the session with the matching name and group chain
        """
        if session_group_chain is None:
            session_group_chain = []
        try:
            session = settings.get_sessions().get_session(
                session_name, list(session_group_chain)
            )
        except KeyError:
            session = None
        if session is None:
            # Session was not found
            message = "Session '{}/{}' was not found!".format(
                "/".join(session_group_chain), session_name
            )
            self._parent.display.repl_display_message(
                message, message_type=constants.MessageType.ERROR
            )
            self._parent.display.write_to_statusbar(message, 1500)
        else:
            result = settings.get_sessions().remove_session(session)
            if result == False:
                # Session was not found
                message = "Session '{}/{}' was not found!".format(
                    "/".join(session_group_chain), session_name
                )
                self._parent.display.repl_display_message(
                    message, message_type=constants.MessageType.ERROR
                )
                self._parent.display.write_to_statusbar(message, 1500)
            else:
                # Session was removed successfully
                message = "Session '{}/{}' was removed!".format(
                    "/".join(session_group_chain), session_name
                )
                self._parent.display.repl_display_message(
                    message, message_type=constants.MessageType.WARNING
                )
        # Refresh the sessions menu in the menubar
        self.update_menu()

    def update_menu(self) -> None:
        """Update the displayed items in the Sessions menu in the menubar"""

        # Nested function for retrieving the sessions name attribute case insensitively
        def get_case_insensitive_group_name(item: tuple) -> str:
            name = item[0]
            return name.lower()

        # Clear the sessions list
        self._parent.sessions_menu.clear()
        # First add the Ex.Co. session (all Ex.Co. source files)
        session_name = "Ex.Co. source files"
        exco_session_action = qt.QAction(session_name, self._parent)
        exco_session_action.setStatusTip("Open all Ex.Co. source files")
        exco_session_method = self.exco_restore
        exco_session_action.setIcon(functions.create_icon("exco-icon.png"))
        exco_session_action.triggered.connect(exco_session_method)
        self._parent.sessions_menu.addAction(exco_session_action)
        self._parent.sessions_menu.addSeparator()

        ## Create the Sessions menu
        # Group processing function
        def process_group(in_group: dict, in_menu: qt.QMenu, create_menu: bool = True) -> None:
            # Create the new group and attach it to the parent menu
            if create_menu:
                folder_name = in_group["name"].replace("&", "&&")
                new_group_menu = Menu(folder_name, self._parent.menubar)
                in_menu.addMenu(new_group_menu)
                new_group_menu.setIcon(functions.create_icon("tango_icons/folder.png"))
            else:
                new_group_menu = in_menu
            # Add the groups
            for g, v in sorted(in_group["groups"].items(), key=lambda x: x[0].lower()):
                process_group(v, new_group_menu)
            # Add the sessions
            for s, v in sorted(in_group["sessions"].items(), key=lambda x: x[0].lower()):
                session_name = s.replace("&", "&&")
                new_session_action = qt.QAction(session_name, new_group_menu)
                new_session_action.setStatusTip("Restore Session: {}".format(s))
                new_session_method = functools.partial(self.restore, v)
                new_session_action.setIcon(functions.create_icon("tango_icons/sessions.png"))
                new_session_action.triggered.connect(new_session_method)
                new_group_menu.addAction(new_session_action)

        # Process the groups
        sessions_menu = self._parent.sessions_menu
        main_session_group = settings.get("stored_sessions")["main"]
        process_group(main_session_group, sessions_menu, create_menu=False)

    def get_window_documents(self) -> List[str]:
        """
        Return all the editor document paths in the selected window as a list
        """
        window = self._parent.get_window_by_indication()
        documents = [
            window.widget(i).save_path
            for i in range(window.count())
            if window.widget(i).savable == constants.CanSave.YES
            and window.widget(i).save_path != ""
        ]
        return documents
