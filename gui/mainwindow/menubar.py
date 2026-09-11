"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.

Menubar construction (~2400 lines).

Builds the full File / Editing / View / System / REPL / Tools / Help
menu tree with keyboard shortcuts, icons, and signal wiring. Exports
a single `init_menubar(self)` function called by MainWindow.
"""

import functools
import os
import shutil
import sys
import traceback

import components.actionfilter
import constants
import data
import functions
import gui.contextmenu
import qt
import settings
from typing import Any, Callable, List, Optional, Union
from gui.customeditor import CustomEditor
from gui.dialogs import YesNoDialog
from gui.menu import Menu, MenuBar
from gui.treedisplays import TreeExplorer


def init_menubar(self) -> None:
    """
    Initialize the menubar ("QAction.triggered.connect" signals
    first parameter is always "checked: bool").
    This is a very long function that should be trimmed sometime!
    """
    self.menubar = MenuBar()
    # Click filter for the menubar menus
    click_filter = components.actionfilter.ActionFilter(self)

    # Nested function for creating an action
    def create_action(
        name: str,
        key_combo: Optional[Union[str, List[str]]],
        status_tip: str,
        icon: Optional[str],
        function: Optional[Callable[..., Any]],
        enabled: bool = True,
    ) -> qt.QAction:
        action = qt.QAction(name, self)
        # Key combination
        keys = None
        if key_combo is not None and key_combo != "":
            if isinstance(key_combo, list):
                if len(key_combo) == 1:
                    keys = key_combo[0]
                    if keys.startswith("#") == False:
                        action.setShortcut(keys)
                elif any([isinstance(x, str) for x in key_combo]):
                    keys = []
                    for k in key_combo:
                        if k.startswith("#") == False:
                            keys.append(k)
                    action.setShortcuts(keys)
                else:
                    raise Exception("Key combination list has to contain only strings!")
            elif isinstance(key_combo, str):
                keys = key_combo
                if keys.startswith("#") == False:
                    action.setShortcut(keys)
        action.setStatusTip(status_tip)
        # Icon and pixmap
        action.pixmap = None
        if icon is not None:
            action.setIcon(functions.create_icon(icon))
            action.pixmap = functions.create_pixmap_with_size(icon, 32, 32)
        # Function
        if function is not None:
            action.triggered.connect(function)
        action.function = function
        self.menubar_functions[function.__name__] = function
        data.global_function_information[function.__name__] = (
            name,
            function,
            icon,
            keys,
            status_tip,
        )
        # Check if there is a tab character in the function
        # name and remove the part of the string after it
        if "\t" in name:
            name = name[: name.find("\t")]
        # Add the action to the context menu
        # function list in the helper forms module
        gui.contextmenu.add_function(function.__name__, action.pixmap, function, name)
        # Enable/disable action according to passed
        # parameter and return the action
        action.setEnabled(enabled)

        if hasattr(self.menubar, "stored_actions") == False:
            self.menubar.stored_actions = []
        self.menubar.stored_actions.append(action)
        return action

    # Nested function for writing text to the REPL
    def repl_text_input(text: str, cursor_position: int) -> None:
        self.repl.setText(text)
        self.repl.setFocus()
        self.repl.setCursorPosition(cursor_position)

    # File menu
    def construct_file_menu() -> None:
        file_menu = Menu("&File", self.menubar)
        self.menubar.addMenu(file_menu)
        file_menu.installEventFilter(click_filter)

        # New file
        def special_create_new_file() -> None:
            self.file_create_new()

        new_file_action = create_action(
            "New",
            settings.get("keyboard-shortcuts")["general"]["new_file"],
            "Create new empty file",
            "tango_icons/document-new.png",
            special_create_new_file,
        )

        # Open file
        def special_open_file() -> None:
            self.file_open()

        open_file_action = create_action(
            "Open",
            settings.get("keyboard-shortcuts")["general"]["open_file"],
            "Open file",
            "tango_icons/document-open.png",
            special_open_file,
        )

        # Save options need to be saved to a reference for disabling/enabling
        # Save file
        def special_save_file() -> None:
            self.file_save()

        self.save_file_action = create_action(
            "Save",
            settings.get("keyboard-shortcuts")["general"]["save_file"],
            "Save current file in the UTF-8 encoding",
            "tango_icons/document-save.png",
            special_save_file,
            enabled=False,
        )

        # Save file as
        def special_saveas_file() -> None:
            self.file_saveas()

        self.saveas_file_action = create_action(
            "Save As",
            settings.get("keyboard-shortcuts")["general"]["saveas_file"],
            "Save current file as a new file in the UTF-8 encoding",
            "tango_icons/document-save-as.png",
            special_saveas_file,
            enabled=False,
        )

        # Save all
        def special_save_all() -> None:
            self.file_save_all()

        self.save_all_action = create_action(
            "Save All",
            None,
            "Save all modified documents in all windows in the UTF-8 encoding",
            "tango_icons/file-save-all.png",
            special_save_all,
            enabled=False,
        )
        # Exit
        exit_action = create_action(
            "Exit\tAlt+F4",
            None,
            "Exit application",
            "tango_icons/system-log-out.png",
            self.exit,
        )

        # Additional menu for saving in different encodings
        def add_save_in_different_encoding_submenu() -> None:
            # Add the save in encoding menu
            self.save_in_encoding = Menu("Save in encoding...", self.menubar)
            self.save_in_encoding.setEnabled(False)
            temp_icon = functions.create_icon("tango_icons/document-save-as.png")
            self.save_in_encoding.setIcon(temp_icon)
            self.save_in_encoding.installEventFilter(click_filter)
            # Save as ASCII encoding
            temp_string = "Save current file with the ASCII encoding, "
            temp_string += 'unknown characters will be replaced with "?"'

            def save_ascii_file() -> None:
                self.file_save(encoding="ascii")

            self.save_ascii_file_action = create_action(
                "ASCII", None, temp_string, None, save_ascii_file, enabled=False
            )
            # Save in ANSI Windows encoding
            temp_string = "Save current file with the ANSI Windows (CP-1250) encoding with CR+LF line ending, "
            temp_string += 'unknown characters will be replaced with "?"'

            def save_ansi_file() -> None:
                self.file_save(encoding="cp1250", line_ending="\r\n")

            self.save_ansiwin_file_action = create_action(
                "ANSI (Windows)",
                None,
                temp_string,
                None,
                save_ansi_file,
                enabled=False,
            )
            # Add the save options to to parent action
            self.save_in_encoding.addAction(self.save_ascii_file_action)
            self.save_in_encoding.addAction(self.save_ansiwin_file_action)
            # Add the parent action to the menu
            file_menu.addMenu(self.save_in_encoding)

        # Add the closing functions
        # Close tab
        def close_tab() -> None:
            try:
                current_window = self.get_window_by_child_tab()
                current_index = current_window.currentIndex()
                current_window.close_tab(current_index)
                # Focus the newly displayed tab
                if current_window.count() > 0:
                    current_window.currentWidget().setFocus()
            except:
                self.display.repl_display_error(traceback.format_exc())

        close_tab_action = create_action(
            "Close Tab",
            settings.get("keyboard-shortcuts")["general"]["close_tab"],
            "Close the current tab",
            "tango_icons/close-tab.png",
            close_tab,
        )

        # Close all
        close_all_action = create_action(
            "Close All Tabs",
            None,
            "Close all tabs in all windows",
            "tango_icons/close-all-tabs.png",
            self.close_all_tabs,
        )

        # Add recent file list in the file menu
        recent_file_list_menu = self.view.create_recent_file_list_menu()
        clear_recent_file_list_action = create_action(
            "Clear recent files",
            None,
            "Clear the recent files list",
            "tango_icons/edit-clear.png",
            self.view.clear_recent_file_list,
        )

        # Add the actions to the File menu
        file_menu.addAction(new_file_action)
        file_menu.addAction(open_file_action)
        file_menu.addAction(self.save_file_action)
        file_menu.addAction(self.saveas_file_action)
        add_save_in_different_encoding_submenu()
        file_menu.addAction(self.save_all_action)
        file_menu.addSeparator()
        file_menu.addAction(close_tab_action)
        file_menu.addAction(close_all_action)
        file_menu.addSeparator()
        file_menu.addMenu(recent_file_list_menu)
        file_menu.addAction(clear_recent_file_list_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

    # Edit Menus
    # Adding the basic options to the menu
    def construct_edit_basic_menu() -> None:
        edit_menu = Menu("&Editing", self.menubar)
        self.menubar.addMenu(edit_menu)
        edit_menu.installEventFilter(click_filter)

        def copy() -> None:
            try:
                self.get_tab_by_focus().copy()
            except:
                self.display.repl_display_error(traceback.format_exc())

        temp_string = "Copy any selected text in the currently "
        temp_string += "selected window to the clipboard"
        copy_action = create_action(
            "Copy\t" + settings.get("keyboard-shortcuts")["editor"]["copy"],
            "#" + settings.get("keyboard-shortcuts")["editor"]["copy"],
            temp_string,
            "tango_icons/edit-copy.png",
            copy,
        )

        def cut() -> None:
            try:
                self.get_tab_by_focus().cut()
            except:
                self.display.repl_display_error(traceback.format_exc())

        cut_action = create_action(
            "Cut\t" + settings.get("keyboard-shortcuts")["editor"]["cut"],
            "#" + settings.get("keyboard-shortcuts")["editor"]["cut"],
            "Cut any selected text in the currently selected window to the clipboard",
            "tango_icons/edit-cut.png",
            cut,
        )

        def paste() -> None:
            try:
                self.get_tab_by_focus().paste()
            except:
                pass

        paste_action = create_action(
            "Paste\t" + settings.get("keyboard-shortcuts")["editor"]["paste"],
            "#" + settings.get("keyboard-shortcuts")["editor"]["paste"],
            "Paste the text in the clipboard to the currenty selected window",
            "tango_icons/edit-paste.png",
            paste,
        )

        def undo() -> None:
            try:
                self.get_tab_by_focus().undo()
            except:
                self.display.repl_display_error(traceback.format_exc())

        undo_action = create_action(
            "Undo\t" + settings.get("keyboard-shortcuts")["editor"]["undo"],
            "#" + settings.get("keyboard-shortcuts")["editor"]["undo"],
            "Undo last editor action in the currenty selected window",
            "tango_icons/edit-undo.png",
            undo,
        )

        def redo() -> None:
            try:
                self.get_tab_by_focus().redo()
            except:
                self.display.repl_display_error(traceback.format_exc())

        redo_action = create_action(
            "Redo\t" + settings.get("keyboard-shortcuts")["editor"]["redo"],
            "#" + settings.get("keyboard-shortcuts")["editor"]["redo"],
            "Redo last undone editor action in the currenty selected window",
            "tango_icons/edit-redo.png",
            redo,
        )

        def select_all() -> None:
            try:
                self.get_tab_by_focus().selectAll(True)
            except:
                self.display.repl_display_error(traceback.format_exc())

        select_all_action = create_action(
            "Select All\t" + settings.get("keyboard-shortcuts")["editor"]["select_all"],
            "#" + settings.get("keyboard-shortcuts")["editor"]["select_all"],
            "Select all of the text in the currenty selected window",
            "tango_icons/edit-select-all.png",
            select_all,
        )

        def indent() -> None:
            try:
                self.get_tab_by_focus().custom_indent()
            except:
                self.display.repl_display_error(traceback.format_exc())

        indent_action = create_action(
            "Indent\t" + settings.get("keyboard-shortcuts")["editor"]["indent"],
            "#" + settings.get("keyboard-shortcuts")["editor"]["indent"],
            "Indent the selected lines by the default width (4 spaces) in the currenty selected window",
            "tango_icons/format-indent-more.png",
            indent,
        )

        def unindent() -> None:
            try:
                self.get_tab_by_focus().custom_unindent()
            except:
                self.display.repl_display_error(traceback.format_exc())

        unindent_action = create_action(
            "Unindent\t" + settings.get("keyboard-shortcuts")["editor"]["unindent"],
            "#" + settings.get("keyboard-shortcuts")["editor"]["unindent"],
            "Unindent the selected lines by the default width (4 spaces) in the currenty selected window",
            "tango_icons/format-indent-less.png",
            unindent,
        )

        def delete_start_of_word() -> None:
            try:
                send_sci_message = self.get_tab_by_focus().SendScintilla
                send_sci_message(qt.QsciScintillaBase.SCI_DELWORDLEFT)
            except:
                self.display.repl_display_error(traceback.format_exc())

        del_start_word_action = create_action(
            "Delete start of word\t"
            + settings.get("keyboard-shortcuts")["editor"]["delete_start_of_word"],
            "#" + settings.get("keyboard-shortcuts")["editor"]["delete_start_of_word"],
            "Delete the current word from the cursor to the starting index of the word",
            "tango_icons/delete-start-word.png",
            delete_start_of_word,
        )

        def delete_end_of_word() -> None:
            try:
                send_sci_message = self.get_tab_by_focus().SendScintilla
                send_sci_message(qt.QsciScintillaBase.SCI_DELWORDRIGHT)
            except:
                self.display.repl_display_error(traceback.format_exc())

        del_end_word_action = create_action(
            "Delete end of word\t"
            + settings.get("keyboard-shortcuts")["editor"]["delete_end_of_word"],
            "#" + settings.get("keyboard-shortcuts")["editor"]["delete_end_of_word"],
            "Delete the current word from the cursor to the ending index of the word",
            "tango_icons/delete-end-word.png",
            delete_end_of_word,
        )

        def delete_start_of_line() -> None:
            try:
                send_sci_message = self.get_tab_by_focus().SendScintilla
                send_sci_message(qt.QsciScintillaBase.SCI_DELLINELEFT)
            except:
                self.display.repl_display_error(traceback.format_exc())

        del_start_line_action = create_action(
            "Delete start of line\t"
            + settings.get("keyboard-shortcuts")["editor"]["delete_start_of_line"],
            "#" + settings.get("keyboard-shortcuts")["editor"]["delete_start_of_line"],
            "Delete the current line from the cursor to the starting index of the line",
            "tango_icons/delete-start-line.png",
            delete_start_of_line,
        )

        def delete_end_of_line() -> None:
            try:
                send_sci_message = self.get_tab_by_focus().SendScintilla
                send_sci_message(qt.QsciScintillaBase.SCI_DELLINERIGHT)
            except:
                self.display.repl_display_error(traceback.format_exc())

        del_end_line_action = create_action(
            "Delete end of line\t"
            + settings.get("keyboard-shortcuts")["editor"]["delete_end_of_line"],
            "#" + settings.get("keyboard-shortcuts")["editor"]["delete_end_of_line"],
            "Delete the current line from the cursor to the ending index of the line",
            "tango_icons/delete-end-line.png",
            delete_end_of_line,
        )

        def goto_to_start() -> None:
            try:
                send_sci_message = self.get_tab_by_focus().SendScintilla
                send_sci_message(qt.QsciScintillaBase.SCI_DOCUMENTSTART)
            except:
                self.display.repl_display_error(traceback.format_exc())

        go_to_start_action = create_action(
            "Go to start\t"
            + settings.get("keyboard-shortcuts")["editor"]["go_to_start"],
            "#" + settings.get("keyboard-shortcuts")["editor"]["go_to_start"],
            "Move cursor up to the start of the currently selected document",
            "tango_icons/goto-start.png",
            goto_to_start,
        )

        def goto_to_end() -> None:
            try:
                send_sci_message = self.get_tab_by_focus().SendScintilla
                send_sci_message(qt.QsciScintillaBase.SCI_DOCUMENTEND)
            except:
                self.display.repl_display_error(traceback.format_exc())

        go_to_end_action = create_action(
            "Go to end\t" + settings.get("keyboard-shortcuts")["editor"]["go_to_end"],
            "#" + settings.get("keyboard-shortcuts")["editor"]["go_to_end"],
            "Move cursor down to the end of the currently selected document",
            "tango_icons/goto-end.png",
            goto_to_end,
        )

        def select_page_up() -> None:
            try:
                send_sci_message = self.get_tab_by_focus().SendScintilla
                send_sci_message(qt.QsciScintillaBase.SCI_PAGEUPEXTEND)
            except:
                self.display.repl_display_error(traceback.format_exc())

        select_page_up_action = create_action(
            "Select page up\t"
            + settings.get("keyboard-shortcuts")["editor"]["select_page_up"],
            "#" + settings.get("keyboard-shortcuts")["editor"]["select_page_up"],
            "Select text up one page of the currently selected document",
            "tango_icons/Input-keyboard.svg",
            select_page_up,
        )

        def select_page_down() -> None:
            try:
                send_sci_message = self.get_tab_by_focus().SendScintilla
                send_sci_message(qt.QsciScintillaBase.SCI_PAGEDOWN)
            except:
                self.display.repl_display_error(traceback.format_exc())

        select_page_down_action = create_action(
            "Select page down\t"
            + settings.get("keyboard-shortcuts")["editor"]["select_page_down"],
            "#" + settings.get("keyboard-shortcuts")["editor"]["select_page_down"],
            "Select text down one page of the currently selected document",
            "tango_icons/Input-keyboard.svg",
            select_page_down,
        )

        def select_to_start() -> None:
            try:
                send_sci_message = self.get_tab_by_focus().SendScintilla
                send_sci_message(qt.QsciScintillaBase.SCI_DOCUMENTSTARTEXTEND)
            except:
                self.display.repl_display_error(traceback.format_exc())

        select_to_start_action = create_action(
            "Select to start\t"
            + settings.get("keyboard-shortcuts")["editor"]["select_to_start"],
            "#" + settings.get("keyboard-shortcuts")["editor"]["select_to_start"],
            "Select all text up to the start of the currently selected document",
            "tango_icons/Input-keyboard.svg",
            select_to_start,
        )

        def select_to_end() -> None:
            try:
                send_sci_message = self.get_tab_by_focus().SendScintilla
                send_sci_message(qt.QsciScintillaBase.SCI_DOCUMENTENDEXTEND)
            except:
                self.display.repl_display_error(traceback.format_exc())

        select_to_end_action = create_action(
            "Select to end\t"
            + settings.get("keyboard-shortcuts")["editor"]["select_to_end"],
            "#" + settings.get("keyboard-shortcuts")["editor"]["select_to_end"],
            "Select all text down to the start of the currently selected document",
            "tango_icons/Input-keyboard.svg",
            select_to_end,
        )

        def scroll_up() -> None:
            try:
                send_sci_message = self.get_tab_by_focus().SendScintilla
                send_sci_message(qt.QsciScintillaBase.SCI_PAGEUP)
            except:
                self.display.repl_display_error(traceback.format_exc())

        scroll_up_action = create_action(
            "Scroll up\t" + settings.get("keyboard-shortcuts")["editor"]["scroll_up"],
            "#" + settings.get("keyboard-shortcuts")["editor"]["scroll_up"],
            "Scroll up one page of the currently selected document",
            "tango_icons/scroll-up.png",
            scroll_up,
        )

        def scroll_down() -> None:
            try:
                send_sci_message = self.get_tab_by_focus().SendScintilla
                send_sci_message(qt.QsciScintillaBase.SCI_PAGEDOWN)
            except:
                self.display.repl_display_error(traceback.format_exc())

        scroll_down_action = create_action(
            "Scroll down\t"
            + settings.get("keyboard-shortcuts")["editor"]["scroll_down"],
            "#" + settings.get("keyboard-shortcuts")["editor"]["scroll_down"],
            "Scroll down one page of the currently selected document",
            "tango_icons/scroll-down.png",
            scroll_down,
        )

        def line_cut() -> None:
            try:
                send_sci_message = self.get_tab_by_focus().SendScintilla
                send_sci_message(qt.QsciScintillaBase.SCI_LINECUT)
            except:
                self.display.repl_display_error(traceback.format_exc())

        line_cut_action = create_action(
            "Line Cut\t" + settings.get("keyboard-shortcuts")["editor"]["line_cut"],
            "#" + settings.get("keyboard-shortcuts")["editor"]["line_cut"],
            "Cut out the current line/lines of the currently selected document",
            "tango_icons/edit-line-cut.png",
            line_cut,
        )

        def line_copy() -> None:
            try:
                send_sci_message = self.get_tab_by_focus().SendScintilla
                send_sci_message(qt.QsciScintillaBase.SCI_LINECOPY)
            except:
                self.display.repl_display_error(traceback.format_exc())

        line_copy_action = create_action(
            "Line Copy\t" + settings.get("keyboard-shortcuts")["editor"]["line_copy"],
            "#" + settings.get("keyboard-shortcuts")["editor"]["line_copy"],
            "Copy the current line/lines of the currently selected document",
            "tango_icons/edit-line-copy.png",
            line_copy,
        )

        def line_delete() -> None:
            try:
                send_sci_message = self.get_tab_by_focus().SendScintilla
                send_sci_message(qt.QsciScintillaBase.SCI_LINEDELETE)
            except:
                self.display.repl_display_error(traceback.format_exc())

        line_delete_action = create_action(
            "Line Delete\t"
            + settings.get("keyboard-shortcuts")["editor"]["line_delete"],
            "#" + settings.get("keyboard-shortcuts")["editor"]["line_delete"],
            "Delete the current line of the currently selected document",
            "tango_icons/edit-line-delete.png",
            line_delete,
        )

        def line_transpose() -> None:
            try:
                send_sci_message = self.get_tab_by_focus().SendScintilla
                send_sci_message(qt.QsciScintillaBase.SCI_LINETRANSPOSE)
            except:
                self.display.repl_display_error(traceback.format_exc())

        line_transpose_action = create_action(
            "Line Transpose\t"
            + settings.get("keyboard-shortcuts")["editor"]["line_transpose"],
            "#" + settings.get("keyboard-shortcuts")["editor"]["line_transpose"],
            "Switch the current line with the line above it of the currently selected document",
            "tango_icons/edit-line-transpose.png",
            line_transpose,
        )

        def line_duplicate() -> None:
            try:
                send_sci_message = self.get_tab_by_focus().SendScintilla
                # send_sci_message(qt.QsciScintillaBase.SCI_LINEDUPLICATE)
                send_sci_message(qt.QsciScintillaBase.SCI_SELECTIONDUPLICATE)
            except:
                self.display.repl_display_error(traceback.format_exc())

        line_duplicate_action = create_action(
            "Line/Selection Duplicate\t"
            + settings.get("keyboard-shortcuts")["editor"]["line_selection_duplicate"],
            "#"
            + settings.get("keyboard-shortcuts")["editor"]["line_selection_duplicate"],
            "Duplicate the current line/selection of the currently selected document",
            "tango_icons/edit-line-duplicate.png",
            line_duplicate,
        )
        # Rectangular block selection
        action_text = "Rectangular block selection\tAlt+Mouse"
        rect_block_action = qt.QAction(
            functions.create_icon("tango_icons/Input-keyboard.svg"),
            action_text,
            self,
        )
        temp_string = (
            "Select rectangle using the mouse in the currently selected document"
        )
        rect_block_action.setStatusTip(temp_string)
        #            temp_icon = functions.create_icon("")
        #            rect_block_action.setIcon(temp_icon)
        edit_menu.addAction(cut_action)
        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)
        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)
        edit_menu.addAction(indent_action)
        edit_menu.addAction(unindent_action)
        edit_menu.addAction(select_all_action)
        edit_menu.addAction(line_cut_action)
        edit_menu.addAction(line_copy_action)
        edit_menu.addAction(line_delete_action)
        edit_menu.addAction(line_transpose_action)
        edit_menu.addAction(line_duplicate_action)
        edit_menu.addAction(scroll_up_action)
        edit_menu.addAction(scroll_down_action)
        edit_menu.addAction(del_start_word_action)
        edit_menu.addAction(del_end_word_action)
        edit_menu.addAction(del_start_line_action)
        edit_menu.addAction(del_end_line_action)
        edit_menu.addAction(go_to_start_action)
        edit_menu.addAction(go_to_end_action)
        edit_menu.addAction(select_page_up_action)
        edit_menu.addAction(select_page_down_action)
        edit_menu.addAction(select_to_start_action)
        edit_menu.addAction(select_to_end_action)
        edit_menu.addAction(rect_block_action)

    def construct_edit_advanced_menu() -> None:
        edit_menu = Menu("&Advanced", self.menubar)
        self.menubar.addMenu(edit_menu)
        edit_menu.installEventFilter(click_filter)

        # Nested special function for finding text in the currentlly focused custom editor
        def special_find() -> None:
            try:
                focused_tab = self.get_used_tab()
                selected_text = (
                    focused_tab.selectedText()
                    .replace("\\", "\\\\")
                    .replace('"', '\\"')
                    .replace("\n", "\\n")
                )
                temp_string = 'find("{}",'.format(selected_text)
                temp_string += "case_sensitive=False,"
                temp_string += "search_forward=True,"
                temp_string += 'window_name="{}")'.format(focused_tab._parent.name)
                self.repl.setText(temp_string)
            except:
                self.repl.setText('find("",case_sensitive=False)')
            self.view.set_repl_type(constants.ReplType.SINGLE_LINE)
            self.repl.setFocus()
            self.repl.setCursorPosition(self.repl.text().find('",case_sensitive'))

        find_action = create_action(
            "Find",
            settings.get("keyboard-shortcuts")["general"]["find"],
            "Find text in the currently selected document",
            "tango_icons/edit-find.png",
            special_find,
        )

        # Nested special function for finding text in the currentlly focused
        # custom editor using regular expressions
        def special_regex_find() -> None:
            try:
                focused_tab = self.get_used_tab()
                selected_text = (
                    focused_tab.selectedText()
                    .replace("\\", "\\\\")
                    .replace('"', '\\"')
                    .replace("\n", "\\n")
                )
                temp_string = 'regex_find(r"{}",'.format(selected_text)
                temp_string += "case_sensitive=False,"
                temp_string += "search_forward=True,"
                temp_string += 'window_name="{}")'.format(focused_tab._parent.name)
                self.repl.setText(temp_string)
            except:
                self.repl.setText('regex_find(r"",case_sensitive=False)')
            self.view.set_repl_type(constants.ReplType.SINGLE_LINE)
            self.repl.setFocus()
            self.repl.setCursorPosition(self.repl.text().find('",case_sensitive'))

        regex_find_action = create_action(
            "Regex Find",
            settings.get("keyboard-shortcuts")["general"]["regex_find"],
            "Find text in currently selected document using Python regular expressions",
            "tango_icons/edit-find-re.png",
            special_regex_find,
        )

        # Nested special function for finding and replacing one instance of text in the current main window custom editor
        def special_find_and_replace() -> None:
            try:
                focused_tab = self.get_used_tab()
                selected_text = (
                    focused_tab.selectedText()
                    .replace("\\", "\\\\")
                    .replace('"', '\\"')
                    .replace("\n", "\\n")
                )
                temp_string = 'find_and_replace("{}","",'.format(selected_text)
                temp_string += "case_sensitive=False,"
                temp_string += "search_forward=True,"
                temp_string += 'window_name="{}")'.format(focused_tab._parent.name)
                self.repl.setText(temp_string)
            except:
                self.repl.setText('find_and_replace("","",case_sensitive=False)')
            self.view.set_repl_type(constants.ReplType.SINGLE_LINE)
            self.repl.setFocus()
            self.repl.setCursorPosition(self.repl.text().find('",case_sensitive'))

        find_and_replace_action = create_action(
            "Find and Replace",
            settings.get("keyboard-shortcuts")["general"]["find_and_replace"],
            "Find and replace one instance of text from cursor in currently selected document",
            "tango_icons/edit-find-replace.png",
            special_find_and_replace,
        )

        # Nested special function for finding and replacing one instance of text
        # in the current main window custom editor using regular expressions
        def special_regex_find_and_replace() -> None:
            try:
                focused_tab = self.get_used_tab()
                selected_text = (
                    focused_tab.selectedText()
                    .replace("\\", "\\\\")
                    .replace('"', '\\"')
                    .replace("\n", "\\n")
                )
                temp_string = 'regex_find_and_replace(r"{}",r"",'.format(selected_text)
                temp_string += "case_sensitive=False,"
                temp_string += "search_forward=True,"
                temp_string += 'window_name="{}")'.format(focused_tab._parent.name)
                self.repl.setText(temp_string)
            except:
                self.repl.setText(
                    'regex_find_and_replace(r"",r"",case_sensitive=False)'
                )
            self.view.set_repl_type(constants.ReplType.SINGLE_LINE)
            self.repl.setFocus()
            self.repl.setCursorPosition(self.repl.text().find('",case_sensitive'))

        regex_find_and_replace_action = create_action(
            "Regex Find and Replace",
            settings.get("keyboard-shortcuts")["general"]["regex_find_and_replace"],
            "Find and replace one instance of text from cursor in currently selected document using Python regular expressions",
            "tango_icons/edit-find-replace-re.png",
            special_regex_find_and_replace,
        )

        def special_highlight() -> None:
            try:
                focused_tab = self.get_used_tab()
                selected_text = (
                    focused_tab.selectedText()
                    .replace("\\", "\\\\")
                    .replace('"', '\\"')
                    .replace("\n", "\\n")
                )
                temp_string = 'highlight("{}",'.format(selected_text)
                temp_string += "case_sensitive=False,"
                temp_string += 'window_name="{}")'.format(focused_tab._parent.name)
                self.repl.setText(temp_string)
            except:
                self.repl.setText('highlight("",case_sensitive=False)')
            self.view.set_repl_type(constants.ReplType.SINGLE_LINE)
            self.repl.setFocus()
            self.repl.setCursorPosition(self.repl.text().find('",case_sensitive'))

        highlight_action = create_action(
            "Highlight",
            settings.get("keyboard-shortcuts")["general"]["highlight"],
            "Highlight all instances of text in currently selected document",
            "tango_icons/edit-highlight.png",
            special_highlight,
        )

        def special_regex_highlight() -> None:
            try:
                focused_tab = self.get_used_tab()
                selected_text = (
                    focused_tab.selectedText()
                    .replace("\\", "\\\\")
                    .replace('"', '\\"')
                    .replace("\n", "\\n")
                )
                temp_string = 'regex_highlight(r"{}",'.format(selected_text)
                temp_string += "case_sensitive=False,"
                temp_string += 'window_name="{}")'.format(focused_tab._parent.name)
                self.repl.setText(temp_string)
            except:
                self.repl.setText('regex_highlight(r"",case_sensitive=False)')
            self.view.set_repl_type(constants.ReplType.SINGLE_LINE)
            self.repl.setFocus()
            self.repl.setCursorPosition(self.repl.text().find('",case_sensitive'))

        regex_highlight_action = create_action(
            "Regex Highlight",
            settings.get("keyboard-shortcuts")["general"]["regex_highlight"],
            "Highlight all instances of text in currently selected document using Python regular expressions",
            "tango_icons/edit-highlight-re.png",
            special_regex_highlight,
        )

        def special_clear_highlights() -> None:
            try:
                focused_tab = self.get_used_tab()
                self.repl.setText(
                    'clear_highlights(window_name="{}")'.format(
                        focused_tab._parent.name
                    )
                )
            except:
                self.repl.setText("clear_highlights()")
            self.view.set_repl_type(constants.ReplType.SINGLE_LINE)
            self.repl.setFocus()
            self.repl.setCursorPosition(len(self.repl.text()))

        clear_highlights_action = create_action(
            "Clear Highlights",
            settings.get("keyboard-shortcuts")["general"]["clear_highlights"],
            "Clear all higlights in currently selected document",
            "tango_icons/edit-clear-highlights.png",
            special_clear_highlights,
        )

        def special_replace_in_selection() -> None:
            try:
                focused_tab = self.get_used_tab()
                temp_string = 'replace_in_selection("","",case_sensitive=False,'
                temp_string += 'window_name="{}")'.format(focused_tab._parent.name)
                self.repl.setText(temp_string)
            except:
                self.repl.setText('replace_in_selection("","",case_sensitive=False)')
            self.view.set_repl_type(constants.ReplType.SINGLE_LINE)
            self.repl.setFocus()
            self.repl.setCursorPosition(self.repl.text().find('","",case_sensitive'))

        replace_selection_action = create_action(
            "Replace In Selection",
            settings.get("keyboard-shortcuts")["general"]["replace_selection"],
            "Replace all instances of text in the selected text of the current selected document",
            "tango_icons/edit-replace-in-selection.png",
            special_replace_in_selection,
        )

        def special_regex_replace_in_selection() -> None:
            try:
                focused_tab = self.get_used_tab()
                temp_string = 'regex_replace_in_selection(r"",r"",case_sensitive=False,'
                temp_string += 'window_name="{}")'.format(focused_tab._parent.name)
                self.repl.setText(temp_string)
            except:
                self.repl.setText(
                    'regex_replace_in_selection(r"",r"",case_sensitive=False)'
                )
            self.view.set_repl_type(constants.ReplType.SINGLE_LINE)
            self.repl.setFocus()
            self.repl.setCursorPosition(self.repl.text().find('",r"",case_sensitive'))

        temp_string = "Replace all instances of text in the "
        temp_string += "selected text of the current selected document"
        temp_string += "using Python regular expressions"
        regex_replace_selection_action = create_action(
            "Regex Replace In Selection",
            settings.get("keyboard-shortcuts")["general"]["regex_replace_selection"],
            temp_string,
            "tango_icons/edit-replace-in-selection-re.png",
            special_regex_replace_in_selection,
        )

        # Nested special function for replacing all instances of text in
        # the selected custom editor
        def special_replace_all() -> None:
            try:
                focused_tab = self.get_used_tab()
                selected_text = (
                    focused_tab.selectedText()
                    .replace("\\", "\\\\")
                    .replace('"', '\\"')
                    .replace("\n", "\\n")
                )
                temp_string = 'replace_all("{}","",'.format(selected_text)
                temp_string += "case_sensitive=False,"
                temp_string += 'window_name="{}")'.format(focused_tab._parent.name)
                self.repl.setText(temp_string)
            except:
                self.repl.setText('replace_all("","",case_sensitive=False)')
            self.view.set_repl_type(constants.ReplType.SINGLE_LINE)
            self.repl.setFocus()
            self.repl.setCursorPosition(self.repl.text().find('",case_sensitive'))

        replace_all_action = create_action(
            "Replace All",
            settings.get("keyboard-shortcuts")["general"]["replace_all"],
            "Replace all instances of text in currently selected document",
            "tango_icons/edit-replace-all.png",
            special_replace_all,
        )

        # Nested special function for replacing all instances of text in
        # the selected custom editor using regular expressions
        def special_regex_replace_all() -> None:
            try:
                focused_tab = self.get_used_tab()
                selected_text = (
                    focused_tab.selectedText()
                    .replace("\\", "\\\\")
                    .replace('"', '\\"')
                    .replace("\n", "\\n")
                )
                temp_string = 'regex_replace_all(r"{}",r"",'.format(selected_text)
                temp_string += "case_sensitive=False,"
                temp_string += 'window_name="{}")'.format(focused_tab._parent.name)
                self.repl.setText(temp_string)
            except:
                self.repl.setText('regex_replace_all(r"",r"",case_sensitive=False)')
            self.view.set_repl_type(constants.ReplType.SINGLE_LINE)
            self.repl.setFocus()
            self.repl.setCursorPosition(self.repl.text().find('",case_sensitive'))

        regex_replace_all_action = create_action(
            "Regex Replace All",
            settings.get("keyboard-shortcuts")["general"]["regex_replace_all"],
            "Replace all instances of text in currently selected document using Python regular expressions",
            "tango_icons/edit-replace-all-re.png",
            special_regex_replace_all,
        )

        # Nested special function for un/commenting selected lines in the main widget
        def comment_uncomment() -> None:
            try:
                self.get_tab_by_focus().toggle_comment_uncomment()
            except:
                self.display.repl_display_error(traceback.format_exc())

        toggle_comment_action = create_action(
            "Comment/Uncomment",
            settings.get("keyboard-shortcuts")["general"]["toggle_comment"],
            "Toggle comments for the selected lines or single line in the currently selected document",
            "tango_icons/edit-comment-uncomment.png",
            comment_uncomment,
        )

        def toggle_autocompletions() -> None:
            try:
                self.get_tab_by_focus().autocompletion_toggle()
            except:
                self.display.repl_display_error(traceback.format_exc())

        toggle_autocompletion_action = create_action(
            "Enable/Disable Autocompletion",
            settings.get("keyboard-shortcuts")["general"]["toggle_autocompletion"],
            "Enable/Disable autocompletions for the currently selected document",
            "tango_icons/edit-autocompletion.png",
            toggle_autocompletions,
        )

        def toggle_wordwrap() -> None:
            try:
                self.get_tab_by_focus().toggle_wordwrap()
            except:
                self.display.repl_display_error(traceback.format_exc())

        toggle_wrap_action = create_action(
            "Enable/Disable Line Wrapping",
            settings.get("keyboard-shortcuts")["general"]["toggle_wrap"],
            "Enable/Disable line wrapping for the currently selected document",
            "tango_icons/wordwrap.png",
            toggle_wordwrap,
        )

        def reload_file() -> None:
            try:
                self.get_tab_by_focus().reload_file()
            except:
                self.display.repl_display_error(traceback.format_exc())

        reload_file_action = create_action(
            "Reload file",
            settings.get("keyboard-shortcuts")["general"]["reload_file"],
            "Reload file from disk, will prompt if file contains changes",
            "tango_icons/view-refresh.png",
            reload_file,
        )

        def create_node_tree() -> None:
            mw = self.get_tab_by_focus()
            if isinstance(mw, CustomEditor):
                self.display.show_nodes(mw, mw.current_file_type)
            else:
                message = "No document opened in the selected window or\n"
                message += "the document is not an editor!"
                self.display.repl_display_message(
                    message, message_type=constants.MessageType.ERROR
                )

        node_tree_action = create_action(
            "Create/reload node tree (C / Nim / Python / ...)",
            settings.get("keyboard-shortcuts")["general"]["node_tree"],
            "Create a node tree for the code for the currently selected document (C / Nim / Python / ...)",
            "tango_icons/edit-node-tree.png",
            create_node_tree,
        )

        def special_goto_line() -> None:
            try:
                focused_tab = self.get_used_tab()
                self.repl.setText(
                    'goto_line(,window_name="{}")'.format(focused_tab._parent.name)
                )
                self.view.set_repl_type(constants.ReplType.SINGLE_LINE)
                self.repl.setCursorPosition(self.repl.text().find(",window_name"))
            except:
                self.repl.setText("goto_line()")
                self.repl.setCursorPosition(len(self.repl.text()) - 1)
            self.repl.setFocus()

        goto_line_action = create_action(
            "Goto line",
            settings.get("keyboard-shortcuts")["general"]["goto_line"],
            "Go to the specified line in the current main window document",
            "tango_icons/edit-goto.png",
            special_goto_line,
        )

        def special_indent_to_cursor() -> None:
            try:
                self.get_tab_by_focus().indent_lines_to_cursor()
            except:
                self.display.repl_display_error(traceback.format_exc())

        temp_string = "Indent the selected lines to the current cursor position "
        temp_string += "(SPACE ON THE LEFT SIDE OF LINES IS STRIPPED!)"
        indent_to_cursor_action = create_action(
            "Indent to cursor",
            settings.get("keyboard-shortcuts")["general"]["indent_to_cursor"],
            temp_string,
            "tango_icons/edit-indent-to-cursor.png",
            special_indent_to_cursor,
        )

        def special_to_uppercase() -> None:
            self.editing.convert_case(uppercase=True)

        to_uppercase_action = create_action(
            "Selection to UPPERCASE",
            settings.get("keyboard-shortcuts")["general"]["to_uppercase"],
            "Convert selected text to UPPERCASE",
            "tango_icons/edit-case-to-upper.png",
            special_to_uppercase,
        )

        def special_to_lowercase() -> None:
            self.editing.convert_case(uppercase=False)

        to_lowercase_action = create_action(
            "Selection to lowercase",
            settings.get("keyboard-shortcuts")["general"]["to_lowercase"],
            "Convert selected text to lowercase",
            "tango_icons/edit-case-to-lower.png",
            special_to_lowercase,
        )

        # Nested function for finding files in open documents
        def special_find_in_open_documents() -> None:
            try:
                focused_tab = self.get_used_tab()
                selected_text = (
                    focused_tab.selectedText()
                    .replace("\\", "\\\\")
                    .replace('"', '\\"')
                    .replace("\n", "\\n")
                )
                repl_text = 'find_in_open_documents("{}"'.format(selected_text)
                repl_text += ",case_sensitive=False,regular_expression=False"
                repl_text += ',window_name="{}")'.format(focused_tab._parent.name)
                self.repl.setText(repl_text)
            except:
                self.repl.setText(
                    'find_in_open_documents("",case_sensitive=False,regular_expression=False)'
                )
            self.view.set_repl_type(constants.ReplType.SINGLE_LINE)
            self.repl.setCursorPosition(self.repl.text().find('",case_sensitive'))
            self.repl.setFocus()

        find_in_documents_action = create_action(
            "Find in open documents",
            settings.get("keyboard-shortcuts")["general"]["find_in_documents"],
            temp_string,
            "tango_icons/edit-find-in-open-documents.png",
            special_find_in_open_documents,
        )

        # Nested function for finding and replacing text in open documents
        def special_find_replace_in_open_documents() -> None:
            try:
                focused_tab = self.get_used_tab()
                selected_text = (
                    focused_tab.selectedText()
                    .replace("\\", "\\\\")
                    .replace('"', '\\"')
                    .replace("\n", "\\n")
                )
                repl_text = 'find_replace_in_open_documents("{}",""'.format(
                    selected_text
                )
                repl_text += ",case_sensitive=False,regular_expression=False"
                repl_text += ',window_name="{}")'.format(focused_tab._parent.name)
                self.repl.setText(repl_text)
            except:
                self.repl.setText(
                    'find_replace_in_open_documents("","",case_sensitive=False,regular_expression=False)'
                )
            self.view.set_repl_type(constants.ReplType.SINGLE_LINE)
            self.repl.setCursorPosition(self.repl.text().find('",case_sensitive'))
            self.repl.setFocus()

        find_replace_in_documents_action = create_action(
            "Find and replace in open documents",
            settings.get("keyboard-shortcuts")["general"]["find_replace_in_documents"],
            temp_string,
            "tango_icons/edit-replace-in-open-documents.png",
            special_find_replace_in_open_documents,
        )

        # Nested function for replacing all string instances in open documents
        def special_replace_all_in_open_documents() -> None:
            try:
                focused_tab = self.get_used_tab()
                selected_text = (
                    focused_tab.selectedText()
                    .replace("\\", "\\\\")
                    .replace('"', '\\"')
                    .replace("\n", "\\n")
                )
                repl_text = 'replace_all_in_open_documents("{}",""'.format(
                    selected_text
                )
                repl_text += ",case_sensitive=False,regular_expression=False"
                repl_text += ',window_name="{}")'.format(focused_tab._parent.name)
                self.repl.setText(repl_text)
            except:
                self.repl.setText(
                    'replace_all_in_open_documents("","",case_sensitive=False,regular_expression=False)'
                )
            self.view.set_repl_type(constants.ReplType.SINGLE_LINE)
            self.repl.setCursorPosition(self.repl.text().find('",case_sensitive'))
            self.repl.setFocus()

        replace_all_in_documents_action = create_action(
            "Replace all in open documents",
            settings.get("keyboard-shortcuts")["general"]["replace_all_in_documents"],
            "Replace all instances of search text across all open documents in the currently selected window",
            "tango_icons/edit-replace-all-in-open-documents.png",
            special_replace_all_in_open_documents,
        )
        reset_context_menu_action = create_action(
            "Reset context menus",
            None,
            "Reset functions of ALL context menus (right-click menus)",
            "tango_icons/reset-context-menu.png",
            gui.contextmenu.ContextMenuHex.reset_functions,
        )

        # Open in browser
        def open_in_browser(*args: Any) -> None:
            try:
                focused_tab = self.get_used_tab()
                selected_text = focused_tab.selectedText()
                functions.open_url(selected_text)
            except:
                message = (
                    "Cannot open selected editor text in the system's web-browser!"
                )
                self.display.repl_display_error(message)

        open_in_browser_action = create_action(
            "Open in browser",
            None,
            "Open selected editor text in the systems web-browser",
            "tango_icons/gnome-web-browser.png",
            open_in_browser,
        )

        def special_find_in() -> None:
            # The second argument is raw, so that single backslashes work for windows paths
            self.repl.setText(
                'find_in_files("",r"directory",case_sensitive=False,search_subdirs=True,break_on_find=False,file_filter=None)'
            )
            self.view.set_repl_type(constants.ReplType.SINGLE_LINE)
            self.repl.setFocus()
            self.repl.setSelection(
                self.repl.text().index("directory"), len("directory")
            )

        def special_find_in_with_dialog() -> None:
            # The second argument is raw, so that single backslashes work for windows paths
            self.repl.setText(
                'find_in_files("",case_sensitive=False,search_subdirs=True,break_on_find=False,file_filter=None)'
            )
            self.view.set_repl_type(constants.ReplType.SINGLE_LINE)
            self.repl.setFocus()
            self.repl.setCursorPosition(self.repl.text().find('",case_sensitive'))

        self.menubar_functions["special_find_in_with_dialog"] = (
            special_find_in_with_dialog
        )
        temp_string = "Find all the files in a directory/subdirectories "
        temp_string += "that contain the search string"
        find_in_files_action = create_action(
            "Find in files",
            settings.get("keyboard-shortcuts")["general"]["find_in_files"],
            temp_string,
            "tango_icons/system-find-in-files.png",
            special_find_in,
        )

        def special_find_file() -> None:
            # The second argument is raw, so that single backslashes work for windows paths
            self.repl.setText(
                'find_files("",r"directory",case_sensitive=False,search_subdirs=True)'
            )
            self.view.set_repl_type(constants.ReplType.SINGLE_LINE)
            self.repl.setFocus()
            self.repl.setSelection(
                self.repl.text().index("directory"), len("directory")
            )

        def special_find_file_with_dialog() -> None:
            # The second argument is raw, so that single backslashes work for windows paths
            self.repl.setText('find_files("",case_sensitive=False,search_subdirs=True)')
            self.view.set_repl_type(constants.ReplType.SINGLE_LINE)
            self.repl.setFocus()
            self.repl.setCursorPosition(self.repl.text().find('",case_sensitive'))

        self.menubar_functions["special_find_file_with_dialog"] = (
            special_find_file_with_dialog
        )
        temp_string = "Find all the files in a directory/subdirectories "
        temp_string += "that have the search string in them"
        find_files_action = create_action(
            "Find files",
            settings.get("keyboard-shortcuts")["general"]["find_files"],
            temp_string,
            "tango_icons/system-find-files.png",
            special_find_file,
        )

        def special_replace_in_files() -> None:
            # The second argument is raw, so that single backslashes work for windows paths
            temp_string = 'replace_in_files("search_text","replace_text",'
            temp_string += 'r"directory",case_sensitive=False,search_subdirs=True,file_filter=None)'
            self.repl.setText(temp_string)
            self.view.set_repl_type(constants.ReplType.SINGLE_LINE)
            self.repl.setFocus()
            self.repl.setSelection(
                self.repl.text().index("directory"), len("directory")
            )

        def special_replace_in_files_with_dialog() -> None:
            # The second argument is raw, so that single backslashes work for windows paths
            temp_string = 'replace_in_files("search_text","replace_text",'
            temp_string += "case_sensitive=False,search_subdirs=True,file_filter=None)"
            self.repl.setText(temp_string)
            self.view.set_repl_type(constants.ReplType.SINGLE_LINE)
            self.repl.setFocus()
            self.repl.setCursorPosition(self.repl.text().find('",case_sensitive'))

        self.menubar_functions["special_replace_in_files_with_dialog"] = (
            special_replace_in_files_with_dialog
        )

        temp_string = "Find all the files in a directory/subdirectories "
        temp_string += "that have the search string in them and replace all "
        temp_string += "instances in the file with the replace string"
        replace_in_files_action = create_action(
            "Replace in files",
            settings.get("keyboard-shortcuts")["general"]["replace_in_files"],
            temp_string,
            "tango_icons/system-replace-in-files.png",
            special_replace_in_files,
        )

        # Adding the edit menu and constructing all of the options
        edit_menu.addAction(find_action)
        edit_menu.addAction(regex_find_action)
        edit_menu.addAction(find_and_replace_action)
        edit_menu.addAction(regex_find_and_replace_action)
        edit_menu.addAction(goto_line_action)
        edit_menu.addAction(indent_to_cursor_action)
        edit_menu.addAction(highlight_action)
        edit_menu.addAction(regex_highlight_action)
        edit_menu.addAction(clear_highlights_action)
        edit_menu.addAction(replace_selection_action)
        edit_menu.addAction(regex_replace_selection_action)
        edit_menu.addAction(replace_all_action)
        edit_menu.addAction(regex_replace_all_action)
        edit_menu.addAction(toggle_comment_action)
        edit_menu.addAction(toggle_autocompletion_action)
        edit_menu.addAction(toggle_wrap_action)
        edit_menu.addAction(to_uppercase_action)
        edit_menu.addAction(to_lowercase_action)
        edit_menu.addAction(node_tree_action)
        edit_menu.addAction(reload_file_action)
        edit_menu.addAction(open_in_browser_action)
        edit_menu.addAction(reset_context_menu_action)
        edit_menu.addSeparator()
        edit_menu.addAction(find_in_documents_action)
        edit_menu.addAction(find_replace_in_documents_action)
        edit_menu.addAction(replace_all_in_documents_action)
        edit_menu.addSeparator()
        edit_menu.addAction(find_files_action)
        edit_menu.addAction(find_in_files_action)
        edit_menu.addAction(replace_in_files_action)

    # System menu
    def construct_system_menu() -> None:
        system_menu = Menu("S&ystem", self.menubar)
        self.menubar.addMenu(system_menu)
        system_menu.installEventFilter(click_filter)

        # Open the settings file
        def open_settings_file() -> None:
            settings_file = settings.get("settings_filename_with_path")
            # Test if userfunctions file exists
            if os.path.isfile(settings_file) == False:
                self.display.repl_display_error(
                    "User definitions file does not exist!\n"
                )
                return
            self.open_file(settings_file)

        open_settings_file_action = create_action(
            "Open settings",
            None,
            "Open the settings file for editing.",
            "tango_icons/settings.png",
            open_settings_file,
        )

        # Add the editing option for the userfunctions file
        def open_user_func_file() -> None:
            user_definitions_file = os.path.join(
                data.application_directory, data.config_file
            )
            # Test if userfunctions file exists
            if os.path.isfile(user_definitions_file) == False:
                self.display.repl_display_message(
                    "User definitions file does not exist!",
                    message_type=constants.MessageType.ERROR,
                )
                message = "Do you wish to generate the default user definition and function file?"
                reply = YesNoDialog.question(message)
                if reply == constants.DialogResult.Yes.value:
                    functions.create_default_config_file()
                    self.display.repl_display_message(
                        "Default user definitions file generated!",
                        message_type=constants.MessageType.SUCCESS,
                    )
                else:
                    return
            self.open_file(user_definitions_file)

        edit_functions_action = create_action(
            "Open User Definitions",
            None,
            "Open the {} file for editing in the main window".format(data.config_file),
            "tango_icons/file-user-funcs.png",
            open_user_func_file,
        )
        # Add the reload option for the userfunctions file
        reload_functions_action = create_action(
            "Reload User Definitions",
            None,
            "Reload the {} file to refresh user defined definitions and functions".format(
                data.config_file
            ),
            "tango_icons/file-user-funcs-reload.png",
            self.import_user_functions,
        )

        # Open the REPL history file
        def open_repl_history() -> None:
            user_repl_history_file = settings.get("repl_history_filename_with_path")
            # Test if userfunctions file exists
            if os.path.isfile(user_repl_history_file) == False:
                self.display.repl_display_warning(
                    "User definitions file does not exist yet.\n"
                    "Enter a command into the REPL and pres ENTER to create it."
                )
                return
            self.open_file(user_repl_history_file)

        open_repl_history_action = create_action(
            "Open REPL history",
            None,
            "Open the REPL history file for editing.",
            "tango_icons/repl-focus-single.png",
            open_repl_history,
        )

        def create_cwd_tree() -> None:
            self.display.show_directory_tree(os.getcwd())

        cwd_tree_action = create_action(
            "Show current working directory tree",
            settings.get("keyboard-shortcuts")["general"]["cwd_tree"],
            "Create a node tree for the current working directory (CWD)",
            "tango_icons/system-show-cwd-tree.png",
            create_cwd_tree,
        )

        def show_explorer() -> None:
            self.system.show_explorer()

        show_explorer_action = create_action(
            "Open current working directory in operating system explorer",
            settings.get("keyboard-shortcuts")["general"]["cwd_explorer"],
            "Open the current working directory in the operating systems explorer",
            "tango_icons/system-show-cwd.png",
            show_explorer,
        )

        # Edit the PATH environment variable
        path_editor_action = create_action(
            "Environment PATH...",
            None,
            "Edit the PATH environment variable",
            "tango_icons/settings.png",
            self.display.show_path_editor,
        )

        def open_general_explorer() -> None:
            file_explorer = self.get_helper_window().tree_add_tab(
                constants.SpecialTabNames.FileExplorer.value, TreeExplorer
            )
            file_explorer.display_directory(os.getcwd())
            file_explorer.open_file_signal.connect(self.open_file)
            file_explorer.open_file_hex_signal.connect(self.open_file_hex)
            file_explorer.internals.set_icon(
                file_explorer,
                functions.create_icon("tango_icons/system-show-cwd-tree-blue.png"),
            )
            self.get_helper_window().setCurrentWidget(file_explorer)

        show_new_explorer_tree_action = create_action(
            "Show current working directory in tree explorer",
            settings.get("keyboard-shortcuts")["general"]["new_cwd_tree"],
            "Show the current working directory in the tree explorer",
            "tango_icons/system-show-cwd-tree-blue.png",
            open_general_explorer,
        )

        def show_terminal() -> None:
            window = self.get_window_by_indication()
            if window is None:
                window = self.get_largest_window()
            window.terminal_add()
            window.currentWidget().setFocus()

        terminal_shell = settings.get("terminal-shell")
        if not isinstance(terminal_shell, str):
            terminal_shell = " ".join(str(part) for part in terminal_shell)
        show_terminal_action = create_action(
            "Terminal Emulator ({})".format(terminal_shell),
            None,
            "Show an integrater Terminal Emulator",
            "tango_icons/utilities-terminal.png",
            show_terminal,
        )

        def show_external_terminal() -> None:
            self.repl.get_interpreter().create_terminal()

        show_external_terminal_action = create_action(
            "External Terminal",
            None,
            "Show an external OS's Console(Windows) / Terminal(Linux) "
            + "window at the current working directory",
            "tango_icons/utilities-terminal.png",
            show_external_terminal,
        )
        # Add the menu items
        system_menu.addSeparator()
        system_menu.addAction(open_settings_file_action)
        system_menu.addAction(open_repl_history_action)
        system_menu.addAction(edit_functions_action)
        system_menu.addAction(reload_functions_action)
        system_menu.addAction(path_editor_action)
        system_menu.addSeparator()
        system_menu.addAction(cwd_tree_action)
        system_menu.addAction(show_new_explorer_tree_action)
        system_menu.addAction(show_explorer_action)
        system_menu.addSeparator()
        system_menu.addAction(show_terminal_action)

        # Terminals
        if data.platform == "Windows":

            def add_powershell_terminal_emulator() -> None:
                terminal = self.get_helper_window().terminal_emulator_add(
                    "Terminal - PowerShell 5.1", "powershell.exe"
                )
                self.get_helper_window().setCurrentWidget(terminal)

            add_powershell_terminal_emulator_action = create_action(
                "Terminal Emulator (PowerShell 5.1)",
                None,
                "Add a Windows PowerShell 5.1 terminal emulator to the layout",
                "tango_icons/utilities-terminal.png",
                add_powershell_terminal_emulator,
            )
            system_menu.addAction(add_powershell_terminal_emulator_action)

            pwsh_path: Optional[str] = shutil.which("pwsh")
            if pwsh_path is not None:
                version_directory: str = os.path.basename(os.path.dirname(pwsh_path))
                pwsh_version: str = (
                    version_directory if version_directory[:1].isdigit() else "7"
                )

                def add_pwsh_terminal_emulator() -> None:
                    terminal = self.get_helper_window().terminal_emulator_add(
                        "Terminal - PowerShell {}".format(pwsh_version),
                        "pwsh.exe",
                    )
                    self.get_helper_window().setCurrentWidget(terminal)

                add_pwsh_terminal_emulator_action = create_action(
                    "Terminal Emulator (PowerShell {})".format(pwsh_version),
                    None,
                    "Add a PowerShell {} terminal emulator to the layout".format(
                        pwsh_version
                    ),
                    "tango_icons/utilities-terminal.png",
                    add_pwsh_terminal_emulator,
                )
                system_menu.addAction(add_pwsh_terminal_emulator_action)

        system_menu.addAction(show_external_terminal_action)

    # Lexers menu
    def construct_lexers_menu(parent: Menu) -> None:
        def set_lexer(lexer: Any, lexer_name: str) -> None:
            try:
                # Get the focused tab and reset the lexer
                focused_tab = self.get_tab_by_focus()
                focused_tab.clear_lexer()
                # Initialize and set the new lexer
                lexer_instance = lexer()
                focused_tab.set_lexer(lexer_instance, lexer_name)
                # Display the lexer change
                message = "Lexer changed to: {}".format(lexer_name)
                self.display.repl_display_message(message)
            except:
                message = "Error with lexer selection!\n"
                message += "Select a window widget with an opened document first."
                self.display.repl_display_error(traceback.format_exc())
                self.display.repl_display_error(message)
                self.display.write_to_statusbar(message)

        lexers_menu = self.display.create_lexers_menu(
            "Change lexer",
            set_lexer,
            store_menu_to_mainform=False,
            custom_parent=parent,
        )
        lexers_menu.installEventFilter(click_filter)
        temp_icon = functions.create_icon("tango_icons/lexers.png")
        lexers_menu.setIcon(temp_icon)
        parent.addMenu(lexers_menu)

    # View menu
    def construct_view_menu() -> None:
        view_menu = Menu("&View", self.menubar)
        self.menubar.addMenu(view_menu)
        view_menu.installEventFilter(click_filter)
        # Show/hide the function wheel
        function_wheel_toggle_action = create_action(
            "Show/Hide Function Wheel",
            settings.get("keyboard-shortcuts")["general"]["function_wheel_toggle"],
            "Show/hide the Ex.Co. function wheel",
            data.application_icon,
            self.view.toggle_function_wheel,
        )
        # Show/hide the settings manipulator
        settings_manipulator_toggle_action = create_action(
            "Show/Hide Settings",
            settings.get("keyboard-shortcuts")["general"][
                "settings_manipulator_toggle"
            ],
            "Show/hide the Ex.Co. settings manipulator",
            data.application_icon,
            self.view.toggle_settings_manipulator,
        )
        # Maximize/minimize entire Ex.Co. window
        maximize_window_action = create_action(
            "Maximize/Normalize",
            settings.get("keyboard-shortcuts")["general"]["maximize_window"],
            "Maximize/Normalize application window",
            "tango_icons/view-fullscreen.png",
            self.view.toggle_window_size,
        )

        def focus_main_window() -> None:
            window = self.get_largest_window()
            self.view.set_window_focus(window)

        main_focus_action = create_action(
            "Focus Largest window",
            settings.get("keyboard-shortcuts")["general"]["main_focus"],
            "Set focus to the largest window",
            "tango_icons/view-focus-main.png",
            focus_main_window,
        )

        def focus_upper_window() -> None:
            window = self.get_helper_window()
            self.view.set_window_focus(window)

        upper_focus_action = create_action(
            "Focus helper window",
            settings.get("keyboard-shortcuts")["general"]["upper_focus"],
            "Set focus to the helper window",
            "tango_icons/view-focus-upper.png",
            focus_upper_window,
        )

        def focus_lower_window() -> None:
            window = self.get_repl_window()
            self.view.set_window_focus(window)

        lower_focus_action = create_action(
            "Focus messages window",
            settings.get("keyboard-shortcuts")["general"]["lower_focus"],
            "Set focus to the messages window",
            "tango_icons/view-focus-lower.png",
            focus_lower_window,
        )

        def toggle_one_window_mode() -> None:
            self.view.toggle_one_window_mode()

        toggle_one_window_mode_action = create_action(
            "One window mode toggle",
            settings.get("keyboard-shortcuts")["general"]["toggle_mode"],
            "Toggle between one-window and stored layout",
            "tango_icons/view-toggle-window-mode.png",
            toggle_one_window_mode,
        )

        def select_tab_right() -> None:
            try:
                self.get_window_by_child_tab().select_tab(constants.Direction.RIGHT)
            except:
                self.display.repl_display_error(traceback.format_exc())

        select_tab_right_action = create_action(
            "Select tab right",
            settings.get("keyboard-shortcuts")["general"]["select_tab_right"],
            "Select one tab to the right in the currently selected window",
            "tango_icons/view-select-tab-right.png",
            select_tab_right,
        )

        def select_tab_left() -> None:
            try:
                self.get_window_by_child_tab().select_tab(constants.Direction.LEFT)
            except:
                self.display.repl_display_error(traceback.format_exc())

        select_tab_left_action = create_action(
            "Select tab left",
            settings.get("keyboard-shortcuts")["general"]["select_tab_left"],
            "Select one tab to the left in the currently selected window",
            "tango_icons/view-select-tab-left.png",
            select_tab_left,
        )

        def move_tab_right() -> None:
            try:
                self.get_window_by_child_tab().move_tab(constants.Direction.RIGHT)
            except:
                self.display.repl_display_error(traceback.format_exc())

        move_tab_right_action = create_action(
            "Move tab right",
            settings.get("keyboard-shortcuts")["general"]["move_tab_right"],
            "Move the current tab in the currently selected window one position to the right",
            "tango_icons/view-move-tab-right.png",
            move_tab_right,
        )

        def move_tab_left() -> None:
            try:
                self.get_window_by_child_tab().move_tab(constants.Direction.LEFT)
            except:
                self.display.repl_display_error(traceback.format_exc())

        move_tab_left_action = create_action(
            "Move tab left",
            settings.get("keyboard-shortcuts")["general"]["move_tab_left"],
            "Move the current tab in the currently selected window one position to the left",
            "tango_icons/view-move-tab-left.png",
            move_tab_left,
        )

        def show_edge() -> None:
            try:
                self.get_tab_by_focus().edge_marker_toggle()
            except:
                self.display.repl_display_error(traceback.format_exc())

        toggle_edge_action = create_action(
            "Toggle edge marker",
            settings.get("keyboard-shortcuts")["general"]["toggle_edge"],
            "Toggle the display of the edge marker that shows the prefered maximum chars in a line",
            "tango_icons/view-edge-marker.png",
            show_edge,
        )

        def reset_zoom() -> None:
            try:
                self.get_tab_by_focus()._parent.zoom_reset()
            except:
                self.display.repl_display_error(traceback.format_exc())

        reset_zoom_action = create_action(
            "Zoom reset",
            settings.get("keyboard-shortcuts")["general"]["reset_zoom"],
            "Reset the zoom level on the currently focused document",
            "tango_icons/view-zoom-reset.png",
            reset_zoom,
        )

        # Bookmarks
        def bookmark_goto(number: int) -> None:
            self.bookmarks.goto(number)

        self.menubar_functions["bookmark_goto"] = bookmark_goto

        def bookmark_store(number: int) -> None:
            try:
                current_tab = self.get_tab_by_focus()
                current_line = current_tab.getCursorPosition()[0] + 1
                self.bookmarks.add_mark_by_number(current_tab, current_line, number)
            except:
                self.display.repl_display_error(traceback.format_exc())

        def bookmark_toggle() -> None:
            try:
                self.get_tab_by_focus().bookmarks.toggle()
            except:
                self.display.repl_display_error(traceback.format_exc())

        bookmark_menu = Menu("&Bookmarks", self.menubar)
        view_menu.addMenu(bookmark_menu)
        bookmark_menu.installEventFilter(click_filter)
        temp_icon = functions.create_icon("tango_icons/bookmarks.png")
        bookmark_menu.setIcon(temp_icon)
        bookmark_toggle_action = create_action(
            "Toggle Bookmark",
            settings.get("keyboard-shortcuts")["general"]["bookmark_toggle"],
            "Toggle a bookmark at the current document line",
            "tango_icons/bookmark.png",
            bookmark_toggle,
        )
        bookmark_menu.addAction(bookmark_toggle_action)

        def bookmarks_clear() -> None:
            self.bookmarks.clear()

        bookmark_clear_action = create_action(
            "Clear Bookmarks",
            None,
            "Clear Bookmarks",
            "tango_icons/bookmarks-clear.png",
            bookmarks_clear,
        )
        bookmark_menu.addAction(bookmark_clear_action)
        bookmark_menu.addSeparator()
        bookmark_goto_menu = Menu("Go To", self.menubar)
        bookmark_menu.addMenu(bookmark_goto_menu)
        bookmark_goto_menu.installEventFilter(click_filter)
        temp_icon = functions.create_icon("tango_icons/bookmarks-goto.png")
        bookmark_goto_menu.setIcon(temp_icon)
        bookmark_store_menu = Menu("Store", self.menubar)
        bookmark_menu.addMenu(bookmark_store_menu)
        bookmark_store_menu.installEventFilter(click_filter)
        temp_icon = functions.create_icon("tango_icons/bookmarks-store.png")
        bookmark_store_menu.setIcon(temp_icon)
        self.bookmark_menu = bookmark_menu
        for i in range(10):
            # Go To
            def create_goto_bookmark() -> None:
                func = functools.partial(bookmark_goto, i)
                func.__name__ = "bookmark_goto_{}".format(i)
                return func

            bookmark_goto_action = create_action(
                "Bookmark Goto {:d}".format(i),
                settings.get("keyboard-shortcuts")["general"]["bookmark_goto"][i],
                "Go to bookmark number:{:d}".format(i),
                "tango_icons/bookmarks-goto.png",
                create_goto_bookmark(),
            )
            bookmark_goto_menu.addAction(bookmark_goto_action)

            # Store
            def create_store_bookmark() -> None:
                func = functools.partial(bookmark_store, i)
                #                    func.__name__ = "store_bookmark_{}".format(i)
                func.__name__ = "bookmark_store_{}".format(i)
                return func

            bookmark_store_action = create_action(
                "Bookmark Store {:d}".format(i),
                settings.get("keyboard-shortcuts")["general"]["bookmark_store"][i],
                "Store bookmark number:{:d}".format(i),
                "tango_icons/bookmarks-store.png",
                create_store_bookmark(),
            )
            bookmark_store_menu.addAction(bookmark_store_action)

        def toggle_line_endings() -> None:
            try:
                self.get_tab_by_focus().toggle_line_endings()
            except:
                self.display.repl_display_error(traceback.format_exc())

        temp_string = "Toggle the visibility of the End-Of-Line characters "
        temp_string += "for the currently selected document"
        toggle_lineend_action = create_action(
            "Toggle EOL visibility",
            None,
            temp_string,
            "tango_icons/view-line-end.png",
            toggle_line_endings,
        )

        def toggle_cursor_line_highlighting() -> None:
            try:
                self.get_tab_by_focus().toggle_cursor_line_highlighting()
            except:
                self.display.repl_display_error(traceback.format_exc())

        temp_string = "Toggle the visibility of the line that the cursor is"
        temp_string += " on for the currently selected document"
        toggle_cursor_line_action = create_action(
            "Toggle cursor line visibility",
            None,
            temp_string,
            "tango_icons/edit-show-cursor-line.png",
            toggle_cursor_line_highlighting,
        )
        # Add all actions and menus
        view_menu.addAction(function_wheel_toggle_action)
        view_menu.addAction(settings_manipulator_toggle_action)
        view_menu.addSeparator()
        view_menu.addMenu(bookmark_menu)
        view_menu.addSeparator()
        construct_lexers_menu(view_menu)
        view_menu.addSeparator()
        view_menu.addAction(main_focus_action)
        view_menu.addAction(upper_focus_action)
        view_menu.addAction(lower_focus_action)
        view_menu.addAction(toggle_one_window_mode_action)
        view_menu.addAction(maximize_window_action)
        view_menu.addAction(select_tab_right_action)
        view_menu.addAction(select_tab_left_action)
        view_menu.addAction(move_tab_right_action)
        view_menu.addAction(move_tab_left_action)
        view_menu.addAction(toggle_edge_action)
        view_menu.addAction(reset_zoom_action)
        view_menu.addAction(toggle_lineend_action)
        view_menu.addAction(toggle_cursor_line_action)

    # REPL menu
    def construct_repl_menu() -> None:
        repl_menu = Menu("&REPL", self.menubar)
        self.menubar.addMenu(repl_menu)
        repl_menu.installEventFilter(click_filter)
        repeat_eval_action = create_action(
            "REPL Repeat Command",
            settings.get("keyboard-shortcuts")["general"]["repeat_eval"],
            "Repeat the last REPL command",
            "tango_icons/repl-repeat-command.png",
            self.repl.repeat_last_repl_eval,
        )
        repeat_cycle_lang_action = create_action(
            "REPL Cycle Language",
            settings.get("keyboard-shortcuts")["general"]["repl_cycle_language"],
            "Cycle the language used by the REPL",
            "tango_icons/repl-repeat-command.png",
            self.repl_box.cycle_language,
        )

        def repl_single_focus() -> None:
            self.view.set_repl_type(constants.ReplType.SINGLE_LINE)
            self.repl.setFocus()

        repl_focus_action = create_action(
            "Focus REPL(Single)",
            [
                settings.get("keyboard-shortcuts")["general"]["repl_focus_single_1"],
                settings.get("keyboard-shortcuts")["general"]["repl_focus_single_2"],
            ],
            "Set focus to the Python REPL(Single Line)",
            "tango_icons/repl-focus-single.png",
            repl_single_focus,
        )

        def repl_multi_focus() -> None:
            self.view.set_repl_type(constants.ReplType.MULTI_LINE)
            self.repl_helper.setFocus()

        repl_focus_multi_action = create_action(
            "Focus REPL(Multi)",
            settings.get("keyboard-shortcuts")["general"]["repl_focus_multi"],
            "Set focus to the Python REPL(Multi Line)",
            "tango_icons/repl-focus-multi.png",
            repl_multi_focus,
        )
        repl_menu.addAction(repeat_eval_action)
        repl_menu.addAction(repeat_cycle_lang_action)
        repl_menu.addAction(repl_focus_action)
        repl_menu.addAction(repl_focus_multi_action)

    # Sessions menu
    def construct_sessions_menu() -> None:
        sessions_menu = Menu("Sessions", self.menubar)
        self.menubar.addMenu(sessions_menu)
        sessions_menu.installEventFilter(click_filter)

        def add_session() -> None:
            repl_text_input(
                text='session_add("", session_group=None)', cursor_position=13
            )

        add_session_action = create_action(
            "Add Session",
            None,
            "Save the currently opened documents to a session",
            "tango_icons/session-add.png",
            add_session,
        )

        def remove_session() -> None:
            repl_text_input(
                text='session_remove("", session_group=None)', cursor_position=13
            )

        remove_session_action = create_action(
            "Remove Session",
            None,
            "Remove the session with matching name and group",
            "tango_icons/session-remove.png",
            remove_session,
        )
        session_editor_action = create_action(
            "Graphical Session Editor",
            None,
            "Graphical user friendly session editor",
            "tango_icons/sessions-gui.png",
            self.display.show_session_editor,
        )
        # Sessions menu
        self.sessions_menu = Menu("Sessions", self.menubar)
        self.sessions_menu.setIcon(functions.create_icon("tango_icons/sessions.png"))
        sessions_menu.addAction(add_session_action)
        sessions_menu.addAction(remove_session_action)
        sessions_menu.addAction(session_editor_action)
        sessions_menu.addSeparator()
        sessions_menu.addMenu(self.sessions_menu)

    # Settings menu
    def construct_settings_menu() -> None:
        settings_menu = Menu("Settings", self.menubar)
        self.menubar.addMenu(settings_menu)
        settings_menu.installEventFilter(click_filter)

        def show_settings() -> None:
            self.view.toggle_settings_manipulator()

        show_gui_action = create_action(
            "Graphical Settings Editor",
            None,
            "Graphical user friendly settings editor",
            "tango_icons/settings-png",
            show_settings,
        )
        # Add the items
        settings_menu.addAction(show_gui_action)

    # Testing menu (debug mode only)
    def construct_testing_menu() -> None:
        testing_dir = functions.unixify_join(data.application_directory, "testing")
        # Create the testing directory if it doesn't exist
        if os.path.isdir(testing_dir) == False:
            try:
                os.makedirs(testing_dir)
            except Exception:
                return
        testing_menu = Menu("&Testing", self.menubar)
        # Insert before the Help menu
        help_action = None
        for action in self.menubar.actions():
            if action.text() == "&Help":
                help_action = action
                break
        if help_action:
            self.menubar.insertMenu(help_action, testing_menu)
        else:
            self.menubar.addMenu(testing_menu)
        testing_menu.installEventFilter(click_filter)

        # Find all .py files in the testing directory
        test_files = sorted(
            [
                f
                for f in os.listdir(testing_dir)
                if f.endswith(".py") and os.path.isfile(os.path.join(testing_dir, f))
            ]
        )

        if not test_files:
            empty_action = qt.QAction("No test files", self)
            empty_action.setEnabled(False)
            testing_menu.addAction(empty_action)
            return

        for test_file in test_files:
            filepath = os.path.join(testing_dir, test_file)
            test_name = os.path.splitext(test_file)[0]

            def run_test(
                checked: bool = False, fp: str = filepath, tn: str = test_name
            ) -> None:
                process = qt.QProcess(self)
                output_lines: list[str] = []

                def on_stdout() -> None:
                    data = (
                        process.readAllStandardOutput()
                        .data()
                        .decode("utf-8", errors="replace")
                    )
                    if data:
                        output_lines.append(data)

                def on_stderr() -> None:
                    data = (
                        process.readAllStandardError()
                        .data()
                        .decode("utf-8", errors="replace")
                    )
                    if data:
                        output_lines.append(data)

                def on_finished(
                    exit_code: int, exit_status: qt.QProcess.ExitStatus
                ) -> None:
                    if hasattr(process, "_timeout_timer"):
                        process._timeout_timer.stop()
                    output = "".join(output_lines)
                    if exit_code == 0:
                        if output:
                            self.display.repl_display_message(
                                f"Test '{tn}' passed:\n{output}"
                            )
                        else:
                            self.display.repl_display_success(
                                f"Test '{tn}' passed with no output."
                            )
                    else:
                        self.display.repl_display_error(
                            f"Test '{tn}' FAILED (exit {exit_code}):\n{output}"
                        )
                    process.deleteLater()

                def on_error(error: qt.QProcess.ProcessError) -> None:
                    if hasattr(process, "_timeout_timer"):
                        process._timeout_timer.stop()
                    error_msg = {
                        qt.QProcess.ProcessError.FailedToStart: "Failed to start",
                        qt.QProcess.ProcessError.Crashed: "Crashed",
                        qt.QProcess.ProcessError.Timedout: "Timed out",
                    }.get(error, f"Error ({error})")
                    self.display.repl_display_error(f"Test '{tn}' {error_msg}")
                    process.deleteLater()

                def on_timeout() -> None:
                    process.kill()
                    output = "".join(output_lines)
                    self.display.repl_display_error(
                        f"Test '{tn}' timed out (30s):\n{output}"
                    )
                    process.deleteLater()

                process.readyReadStandardOutput.connect(on_stdout)
                process.readyReadStandardError.connect(on_stderr)
                process.finished.connect(on_finished)
                process.errorOccurred.connect(on_error)

                timer = qt.QTimer(self)
                timer.setSingleShot(True)
                timer.timeout.connect(on_timeout)
                timer.start(30000)
                process._timeout_timer = timer

                process.start(sys.executable, [fp])

            action = create_action(
                test_name,
                None,
                f"Run {test_file}",
                None,
                run_test,
            )
            testing_menu.addAction(action)

    # Help menu
    def construct_help_menu() -> None:
        help_menu = Menu("&Help", self.menubar)
        self.menubar.addMenu(help_menu)
        help_menu.installEventFilter(click_filter)
        self.fm = help_menu
        about_action = create_action(
            "About Ex.Co.",
            None,
            "Ex.Co. Information",
            "tango_icons/help-browser.png",
            self.view.show_about,
        )
        help_menu.addAction(about_action)

    # Tools menu
    def construct_tools_menu() -> None:
        tools_menu = Menu("&Tools", self.menubar)
        self.menubar.addMenu(tools_menu)
        tools_menu.installEventFilter(click_filter)

        # Print indicated editor to PDF
        def special_print_pdf() -> None:
            import libraryfunctions

            try:
                text = self.get_tab_by_indication().text()
                filepath = functions.unixify_join(
                    data.settings_directory,
                    "print_document.pdf",
                )
                libraryfunctions.create_pdf_from_text(filepath, text)
                libraryfunctions.open_pdf(filepath)
            except:
                self.display.repl_display_error(traceback.format_exc())

        print_pdf_action = create_action(
            "Print to PDF",
            None,
            "Print indicated editor to PDF",
            "tango_icons/document-print.png",
            special_print_pdf,
        )
        tools_menu.addAction(print_pdf_action)

        tools_menu.addSeparator()

        # === Code formatting ===
        # Menu
        formatting_menu = tools_menu.addMenu("Formatting")
        temp_icon = functions.create_icon("tango_icons/view-edge-marker.png")
        formatting_menu.setIcon(temp_icon)

        # Python
        formatting_menu_python = formatting_menu.addMenu("Python")
        temp_icon = functions.create_icon("language_icons/logo_python.png")
        formatting_menu_python.setIcon(temp_icon)

        ## Formatting Python code
        formatting_libraries = (
            "black",
            "autopep8",
            "yapf",
            "ruff",
        )

        # Selected text
        def format_python_formatting_selection_func_generator(
            library_name: str,
        ) -> Callable[..., Any]:
            def format_python_selection_func(code: str) -> None:
                try:
                    self.tools.format_python_selected_text(library_name)
                except:
                    self.display.repl_display_error(traceback.format_exc())

            return format_python_selection_func

        for fl in formatting_libraries:
            format_python_action = create_action(
                f"Format Python code - selection - {fl}",
                None,
                f"Format Python code in the selected document's selected text using the {fl} library",
                "language_icons/logo_python.png",
                format_python_formatting_selection_func_generator(fl),
            )
            formatting_menu_python.addAction(format_python_action)

        formatting_menu_python.addSeparator()

        # Entire file
        def format_python_formatting_entire_text_func_generator(
            library_name: str,
        ) -> Callable[..., Any]:
            def format_python_entire_text_func(code: str) -> None:
                try:
                    self.tools.format_python_all_text(library_name)
                except:
                    self.display.repl_display_error(traceback.format_exc())

            return format_python_entire_text_func

        for fl in formatting_libraries:
            format_python_action = create_action(
                f"Format Python code - entire file - {fl}",
                None,
                f"Format Python code in the entire selected document using the {fl} library",
                "language_icons/logo_python.png",
                format_python_formatting_entire_text_func_generator(fl),
            )
            formatting_menu_python.addAction(format_python_action)

        # C / C++
        formatting_menu_c_cpp = formatting_menu.addMenu("C/C++")
        temp_icon = functions.create_icon("language_icons/logo_c_cpp.png")
        formatting_menu_c_cpp.setIcon(temp_icon)

        # Format C/C++ code for the entire file - clang-format
        def create_c_cpp_format_fund(style: str) -> Callable[..., Any]:
            def format_c_cpp_code_clang_format() -> None:
                try:
                    self.tools.format_c_cpp_all_text("clang-format", style=style)
                except:
                    self.display.repl_display_error(traceback.format_exc())

            return format_c_cpp_code_clang_format

        clang_format_styles = (
            "LLVM",
            "Google",
            "Chromium",
            "Mozilla",
            "WebKit",
            "Microsoft",
            "GNU",
            "File",
            "Default",
        )
        for style in clang_format_styles:
            format_c_cpp_clang_format_action = create_action(
                f"Format C/C++ code - entire file - clang-format: {style}",
                None,
                (
                    "Format C/C++ code in the entire selected document "
                    f"using the clang-format library with the {style} style"
                ),
                "language_icons/logo_c_cpp.png",
                create_c_cpp_format_fund(style),
            )
            formatting_menu_c_cpp.addAction(format_c_cpp_clang_format_action)

        # Zig
        formatting_menu_zip = formatting_menu.addMenu("Zig")
        temp_icon = functions.create_icon("language_icons/logo_zig.png")
        formatting_menu_zip.setIcon(temp_icon)

        def format_zig() -> None:
            try:
                self.tools.format_zig_all_text()
            except:
                self.display.repl_display_error(traceback.format_exc())

        format_zig_action = create_action(
            "Format Zig code - entire file",
            None,
            (
                "Format Zig code in the entire selected document using the 'zig fmt' command"
            ),
            "language_icons/logo_zig.png",
            format_zig,
        )
        formatting_menu_zip.addAction(format_zig_action)

        # Nim
        formatting_menu_nim = formatting_menu.addMenu("Nim")
        temp_icon = functions.create_icon("language_icons/logo_nim.png")
        formatting_menu_nim.setIcon(temp_icon)

        def format_nim() -> None:
            try:
                self.tools.format_nim_file()
            except:
                self.display.repl_display_error(traceback.format_exc())

        format_nim_action = create_action(
            "Format Nim code - entire file",
            None,
            (
                "Format Nim code in the entire selected document "
                "using the 'nph' command line formatter"
            ),
            "language_icons/logo_nim.png",
            format_nim,
        )
        formatting_menu_nim.addAction(format_nim_action)

        # === Analyzing ===
        # Menu
        analyzing_menu = tools_menu.addMenu("Analyzing")
        temp_icon = functions.create_icon("tango_icons/view-edge-marker.png")
        analyzing_menu.setIcon(temp_icon)

        analyzing_libraries = (
            "Ruff",
            "Pyflakes",
        )

        def analyze_python_file_func_generator(library_name: str) -> Callable[..., Any]:
            def analyze_python_file_func() -> None:
                try:
                    self.tools.analyze_python_file(library_name)
                except:
                    self.display.repl_display_error(traceback.format_exc())

            return analyze_python_file_func

        for al in analyzing_libraries:
            analyze_python_action = create_action(
                f"Analyze Python file - {al}",
                None,
                f"Analyze Python document using the {al} library",
                "language_icons/logo_python.png",
                analyze_python_file_func_generator(al.lower()),
            )
            analyzing_menu.addAction(analyze_python_action)

        # === Pretty printing ===
        # Menu
        pretty_print_menu = tools_menu.addMenu("Petty printing")
        temp_icon = functions.create_icon("tango_icons/view-edge-marker.png")
        pretty_print_menu.setIcon(temp_icon)

        # Pretty print JSON
        def pretty_print_json() -> None:
            try:
                self.tools.pretty_print_text(
                    constants.FormatterType.JSON, sort_keys=False
                )
            except:
                self.display.repl_display_error(traceback.format_exc())

        pretty_print_json_action = create_action(
            "Pretty print JSON text",
            None,
            "Pretty print JSON text in the selected document",
            "language_icons/logo_json.png",
            pretty_print_json,
        )
        pretty_print_menu.addAction(pretty_print_json_action)

        def pretty_print_json_with_key_sorting() -> None:
            try:
                self.tools.pretty_print_text(
                    constants.FormatterType.JSON, sort_keys=True
                )
            except:
                self.display.repl_display_error(traceback.format_exc())

        pretty_print_json_action = create_action(
            "Pretty print JSON text - with key sorting",
            None,
            "Pretty print JSON text with key sorting in the selected document",
            "language_icons/logo_json.png",
            pretty_print_json_with_key_sorting,
        )
        pretty_print_menu.addAction(pretty_print_json_action)

        # Pretty print XML
        def pretty_print_xml() -> None:
            try:
                self.tools.pretty_print_text(constants.FormatterType.XML)
            except:
                self.display.repl_display_error(traceback.format_exc())

        pretty_print_xml_action = create_action(
            "Pretty print XML text",
            None,
            "Pretty print XML text in the selected document",
            "language_icons/logo_xml.png",
            pretty_print_xml,
        )
        pretty_print_menu.addAction(pretty_print_xml_action)

        # Pretty print HTML with BeautifulSoup
        def pretty_print_html_with_beautifulsoup() -> None:
            try:
                self.tools.pretty_print_text(constants.FormatterType.HTML_BeautifulSoup)
            except:
                self.display.repl_display_error(traceback.format_exc())

        pretty_print_html_0_action = create_action(
            "Pretty print HTML text with BeautifulSoup",
            None,
            "Pretty print HTML text in the selected document with the BeautifulSoup library",
            "language_icons/logo_html.png",
            pretty_print_html_with_beautifulsoup,
        )
        pretty_print_menu.addAction(pretty_print_html_0_action)

        # Pretty print HTML with Python's Standard Libary
        def pretty_print_html_with_python_stdlib() -> None:
            try:
                self.tools.pretty_print_text(
                    constants.FormatterType.HTML_Python_Standard_Library
                )
            except:
                self.display.repl_display_error(traceback.format_exc())

        pretty_print_html_1_action = create_action(
            "Pretty print HTML text with Python's Standard Libary",
            None,
            "Pretty print HTML text in the selected document with Python's Standard Libary",
            "language_icons/logo_html.png",
            pretty_print_html_with_python_stdlib,
        )
        pretty_print_menu.addAction(pretty_print_html_1_action)

    # Execute the nested construction functions
    construct_file_menu()
    construct_edit_basic_menu()
    construct_edit_advanced_menu()
    construct_system_menu()
    construct_view_menu()
    construct_repl_menu()
    construct_tools_menu()
    construct_sessions_menu()
    # construct_settings_menu()
    if data.debug_mode:
        construct_testing_menu()
    construct_help_menu()

    # Connect the triggered signal for hiding the function wheel on menubar clicks
    def hide_fw(action: qt.QAction) -> None:
        # Hide the function wheel only when the clicked action is not "Show/Hide Function Wheel"
        if isinstance(action, qt.QAction):
            if action.text() != "Show/Hide Function Wheel":
                # Hide the function wheel if it is shown
                self.view.hide_function_wheel()

    self.menubar.triggered.connect(hide_fw)
    # Add the menubar to the MainWindow
    self.setMenuBar(self.menubar)
