"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.

System-level actions (settings file, user functions, REPL history,
terminal emulators, file explorer). Namespace class attached to
the MainWindow instance.
"""

import os
import subprocess
from typing import Optional, TYPE_CHECKING

import constants
import data
import functions
from gui.dialogs import YesNoDialog

if TYPE_CHECKING:
    from gui.mainwindow import MainWindow


class System:
    """
    Functions that interact with the system
    (namespace/nested class to MainWindow)
    """

    # Class varibles
    _parent: "MainWindow" = None

    def __init__(self, parent: "MainWindow") -> None:
        """Initialization of the System object instance"""
        # Get the reference to the MainWindow parent object instance
        self._parent = parent

    def find_files(
        self,
        file_name: str,
        search_dir: Optional[str] = None,
        case_sensitive: bool = False,
        search_subdirs: bool = True,
    ) -> None:
        """Return a list of files that match file_name as a list and display it"""
        # Check if the search directory is none, then use a dialog window
        # to select the real search directory
        if search_dir is None:
            search_dir = self._parent.get_directory_with_dialog()
            # Update the current working directory
            if os.path.isdir(search_dir):
                self._parent.set_cwd(search_dir)
        # Execute the find function
        found_files = functions.find_files_by_name(
            file_name, search_dir, case_sensitive, search_subdirs
        )
        # Check of the function return is valid
        if found_files is None:
            # Check if directory is valid
            self._parent.display.repl_display_message(
                "Invalid search directory!",
                message_type=constants.MessageType.ERROR,
            )
            self._parent.display.write_to_statusbar("Invalid search directory!", 2000)
            return
        elif found_files == []:
            # Check if any files were found
            self._parent.display.repl_display_message(
                "No files found!", message_type=constants.MessageType.WARNING
            )
            self._parent.display.write_to_statusbar("No files found!", 2000)
            return
        # Display the found files
        self._parent.display.show_found_files(
            "'{}' in its name".format(file_name), found_files, search_dir
        )

    def find_in_files(
        self,
        search_text: str,
        search_dir: Optional[str] = None,
        case_sensitive: bool = False,
        search_subdirs: bool = True,
        break_on_find: bool = False,
        file_filter: Optional[str] = None,
    ) -> None:
        """Return a list of files that contain the searched text as a list and display it"""
        # Check if the search directory is none, then use a dialog window
        # to select the real search directory
        if search_dir is None:
            search_dir = self._parent.get_directory_with_dialog()
            # Update the current working directory
            if os.path.isdir(search_dir):
                self._parent.set_cwd(search_dir)
        try:
            # Display the found files
            self._parent.display.show_found_files_with_lines_in_tree(
                "'{}' in its content".format(search_text),
                search_text,
                search_dir,
                case_sensitive,
                search_subdirs,
                break_on_find,
                file_filter,
            )
        except Exception as ex:
            self._parent.display.repl_display_message(
                str(ex), message_type=constants.MessageType.ERROR
            )

    def replace_in_files(
        self,
        search_text: str,
        replace_text: str,
        search_dir: Optional[str] = None,
        case_sensitive: bool = False,
        search_subdirs: bool = True,
        file_filter: Optional[str] = None,
    ) -> None:
        """
        Same as the function in the 'functions' module.
        Replaces all instances of search_string with the replace_string in the files,
        that contain the search string in the search_dir.
        """
        # Close the log window if it is displayed
        warning = "The replaced content will be saved back into the files!\n"
        warning += "You better have a backup of the files if you are unsure,\n"
        warning += "because this action CANNOT be undone!\n"
        warning += "Do you want to continue?"
        reply = YesNoDialog.warning(warning)
        if reply == constants.DialogResult.No.value:
            return
        # Check if the search directory is none, then use a dialog window
        # to select the real search directory
        if search_dir is None:
            search_dir = self._parent.get_directory_with_dialog()
            # Update the current working directory
            if os.path.isdir(search_dir):
                self._parent.set_cwd(search_dir)
        # Replace the text in files
        result = functions.replace_text_in_files_enum(
            search_text,
            replace_text,
            search_dir,
            case_sensitive,
            search_subdirs,
            file_filter,
        )
        if result == -1:
            self._parent.display.repl_display_message(
                "Invalid search&replace in files directory!",
                message_type=constants.MessageType.ERROR,
            )
            self._parent.display.write_to_statusbar("Invalid search directory!", 2000)
            return
        elif result == -2:
            self._parent.display.repl_display_message(
                "Cannot search&replace in files over multiple lines!",
                message_type=constants.MessageType.ERROR,
            )
            self._parent.display.write_to_statusbar("Invalid search directory!", 2000)
            return
        # Check the return type
        if len(result) == 0:
            self._parent.display.repl_display_message(
                "No files with '{}' in its text were found!".format(search_text),
                message_type=constants.MessageType.WARNING,
            )
        elif isinstance(result, dict):
            self._parent.display.show_replaced_text_in_files_in_tree(
                search_text, replace_text, result, search_dir
            )
        else:
            self._parent.display.repl_display_message(
                "Unknown error!", message_type=constants.MessageType.ERROR
            )

    def show_explorer(self) -> None:
        """Open the current working directory in the operating system explorer"""
        directory: Optional[str]
        try:
            directory = os.getcwd()
        except OSError:
            directory = None
        if not directory or not os.path.isdir(directory):
            self._parent.display.repl_display_error(
                "Current working directory is invalid: '{}'".format(directory)
            )
            return
        try:
            if data.on_windows:
                os.startfile(directory)
            else:
                subprocess.Popen(["xdg-open", directory])
        except OSError as ex:
            self._parent.display.repl_display_error(
                "Cannot open directory in system explorer:"
                + " '{}' ({})".format(directory, ex)
            )
