"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.

Bookmark management.

Stores up to 10 numbered bookmarks per editor session, with
add/remove/goto/clear operations. Used as a namespace class
attached to the MainWindow instance.
"""

from typing import Dict, Any, List, Optional, TYPE_CHECKING

from gui.customeditor import CustomEditor

if TYPE_CHECKING:
    from gui.mainwindow import MainWindow


class Bookmarks:
    """
    All bookmark functionality
    """

    # Class varibles
    _parent: "MainWindow" = None
    # List of all the bookmarks
    marks: Dict[int, Dict[str, Any]] = None

    def __init__(self, parent: "MainWindow") -> None:
        """Initialization of the Bookmarks object instance"""
        # Get the reference to the MainWindow parent object instance
        self._parent = parent
        # Initialize all the bookmarks
        self.init()

    def init(self) -> None:
        self.marks = {}
        for i in range(10):
            self.marks[i] = {
                "editor": None,
                "line": None,
                "handle": None,
            }

    def add(self, editor: CustomEditor, line: int) -> Optional[int]:
        # Bookmarks should only work in editors
        if isinstance(editor, CustomEditor) == False or editor.embedded == True:
            return
        for i in range(10):
            if self.marks[i]["editor"] is None and self.marks[i]["line"] is None:
                self.marks[i]["editor"] = editor
                self.marks[i]["line"] = line
                self._parent.display.repl_display_success(
                    "Bookmark '{:d}' was added!".format(i),
                )
                return i
        else:
            self._parent.display.repl_display_error("All ten bookmarks are occupied!")
            return None

    def add_mark_by_number(
        self, editor: CustomEditor, line: int, mark_number: int
    ) -> None:
        # Bookmarks should only work in editors
        if isinstance(editor, CustomEditor) == False or editor.embedded == True:
            return
        if self.bounds_check(mark_number) == False:
            return
        # The CustomEditor.bookmarks / MainWindow attributes are typed None in
        # the QScintilla and MainWindow stubs; reach them through Any locals.
        editor_bookmarks: Any = editor.bookmarks
        parent: Any = self._parent
        # Toggle-off: pressing the same number again at the same line removes
        # the bookmark, consistent with the toggle_at_line() behaviour
        if (
            self.marks[mark_number]["editor"] == editor
            and self.marks[mark_number]["line"] == line
        ):
            editor_bookmarks.remove_marker_at_line(line)
            self.marks[mark_number]["editor"] = None
            self.marks[mark_number]["line"] = None
            self.marks[mark_number]["handle"] = None
            parent.display.repl_display_success(
                "Bookmark '{:d}' was removed!".format(mark_number)
            )
            return
        # Clear the selected marker slot if it is not empty
        if (
            self.marks[mark_number]["editor"] is not None
            and self.marks[mark_number]["line"] is not None
        ):
            self.marks[mark_number]["editor"].bookmarks.toggle_at_line(
                self.marks[mark_number]["line"]
            )
            self.marks[mark_number]["editor"] = None
            self.marks[mark_number]["line"] = None
            self.marks[mark_number]["handle"] = None
        # If the same bookmark is already stored under a different number,
        # remove it first so the editor line ends up with a single marker
        for i in range(10):
            if i != mark_number:
                if self.marks[i]["editor"] == editor and self.marks[i]["line"] == line:
                    self.marks[i]["editor"].bookmarks.toggle_at_line(
                        self.marks[i]["line"]
                    )
                    break
        # Set and store the marker on the editor
        handle = editor_bookmarks.add_marker_at_line(line)
        self.marks[mark_number]["editor"] = editor
        self.marks[mark_number]["line"] = line
        self.marks[mark_number]["handle"] = handle
        parent.display.repl_display_success(
            "Bookmark '{:d}' was added!".format(mark_number)
        )

    def clear(self) -> None:
        cleared_any = False
        for i in range(10):
            if (
                self.marks[i]["editor"] is not None
                and self.marks[i]["line"] is not None
            ):
                self.marks[i]["editor"].bookmarks.toggle_at_line(self.marks[i]["line"])
                self.marks[i]["editor"] = None
                self.marks[i]["line"] = None
                self.marks[i]["handle"] = None
                cleared_any = True
        if cleared_any == False:
            self._parent.display.repl_display_warning("Bookmarks are clear.")
            return

    def remove_by_number(self, mark_number: int) -> None:
        if self.bounds_check(mark_number) == False:
            return
        self.marks[mark_number]["editor"] = None
        self.marks[mark_number]["line"] = None
        self.marks[mark_number]["handle"] = None

    def remove_by_reference(self, editor: CustomEditor, line: int) -> None:
        for i in range(10):
            if self.marks[i]["editor"] == editor and self.marks[i]["line"] == line:
                self.marks[i]["editor"] = None
                self.marks[i]["line"] = None
                self.marks[i]["handle"] = None
                self._parent.display.repl_display_success(
                    "Bookmark '{:d}' was removed!".format(i)
                )
                break
        else:
            self._parent.display.repl_display_error("Bookmark not found!")

    def get_editor_all(self, editor: CustomEditor) -> List[Dict[str, Any]]:
        """
        Get all bookmarks for a specific editor
        """
        editor_bookmarks: List[Dict[str, Any]] = []
        for number, mark in self.marks.items():
            if mark["editor"] == editor:
                editor_bookmarks.append(mark)
        return editor_bookmarks

    def remove_editor_all(self, editor: CustomEditor) -> None:
        """
        Remove all bookmarks of an editor
        """
        removed_bookmarks = []
        for i in range(10):
            if self.marks[i]["editor"] == editor:
                self.marks[i]["editor"] = None
                self.marks[i]["line"] = None
                self.marks[i]["handle"] = None
                removed_bookmarks.append(i)
        if removed_bookmarks != []:
            close_message = "Bookmarks: "
            close_message += ", ".join(str(mark) for mark in removed_bookmarks)
            close_message += "\nwere removed."
            self._parent.display.repl_display_success(close_message)

    def check(self, editor: CustomEditor, line: int) -> Optional[int]:
        for i in range(10):
            if self.marks[i]["editor"] == editor and self.marks[i]["line"] == line:
                return i
        else:
            return None

    def bounds_check(self, mark_number: int) -> bool:
        if mark_number < 0 or mark_number > 9:
            self._parent.display.repl_display_error("Bookmarks only go from 0 to 9!")
            return False
        else:
            return True

    def goto(self, mark_number: int) -> None:
        if self.bounds_check(mark_number) == False:
            return
        if (
            self.marks[mark_number]["editor"] is None
            and self.marks[mark_number]["line"] is None
        ):
            self._parent.display.repl_display_warning(
                "Bookmark '{:d}' is empty!".format(mark_number)
            )
        else:
            editor = self.marks[mark_number]["editor"]
            line = self.marks[mark_number]["line"]
            # Focus the stored editor and it's parent tab widget
            editor._parent.setCurrentWidget(editor)
            # Go to the stored line
            editor.goto_line(line)
