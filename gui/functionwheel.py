
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2022 Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import os
import sys
import itertools
import inspect
import functools
import keyword
import re
import collections
import textwrap
import importlib
import data
import components
import themes
import functions
import interpreter
import settings
import lexers
import traceback

from .custombuttons import *
from .customeditor import *
from .plaineditor import *
from .textdiffer import *


"""
----------------------------------------------------------------
Overlay helper widget for visually selecting an Ex.Co. function
----------------------------------------------------------------
"""
class FunctionWheel(data.QGroupBox):
    SIZE = (640, 560)
    # Class variables
    _parent = None
    main_form = None
    background_image = None
    display_label = None
    cursor_show_position = None
    theme_name = None

    def clean_up(self):
        self._parent = None
        self.main_form = None
        # Function for deleting an attribute
        def delete_attribute(att_name):
            attr = getattr(self, att_name)
            attr.setParent(None)
            attr.deleteLater()
            delattr(self, att_name)
        # List of attributes for clean up
        clean_up_list = [
            "picture",
            "display_label",
        ]
        for att in clean_up_list:
            delete_attribute(att)
        for child_widget in self.children():
            child_widget.deleteLater()
        # Clean up self
        self.setParent(None)
        self.deleteLater()

    def __init__(self, parent=None, main_form=None):
        #Initialize the superclass
        super().__init__(parent)
        #Store the reference to the parent
        self._parent = parent
        #Store the reference to the main form
        self.main_form = main_form
        # Set default font
        self.setFont(data.get_current_font())
        # Set the layout
#        self.__layout = data.QGridLayout()
#        self.__layout.setSpacing(10)
#        self.__layout.setContentsMargins(
#            data.QMargins(0,0,0,0)
#        )
#        self.setLayout(self.__layout)
        #Initialize the display label that will display the function names
        #when the mouse cursor is over a function button
        self.display_label = data.QLabel(self)
        self.display_label.setGeometry(8, 450, 200, 100)
        font = data.QFont(data.current_font_name, 14)
        font.setBold(True)
        self.display_label.setFont(font)
        self.display_label.setAlignment(
            data.Qt.AlignHCenter | data.Qt.AlignVCenter
        )
        #Initialize all of the hex function buttons
        self.__init_all_buttons()
        #Position the overlay to the center of the screen
        self.center(data.QSize(*self.SIZE))
        #Scale the function wheel size if needed
        self.scale(1, 1)
        self.update_style()

    def __init_all_buttons(self):
        """
        Function for calling all button initialization subroutines
        """
        self.button_x_offset = 8
        self.button_y_offset = 8
        self.button_cache = []
        self.__init_file_buttons()
        self.__init_basic_buttons()
        self.__init_advanced_buttons()
        self.__init_system_view_buttons()
        self.__init_repl_buttons()
        self.__init_special_system_buttons()
        #Check the states of the hex function buttons
        self.__check_hex_button_states()

    def __init_basic_buttons(self):
        # Alias the class references to shorten the names
        form = self.main_form
        menubar_functions = self.main_form.menubar_functions
        # Generate positions/size
        size = (50, 50)
        start = (0, 0)
        row = 0
        col = 0
        geometries = []
        for i in range(12):
            geometries.append((
                (col * size[0])+self.button_x_offset,
                (row * size[1])+self.button_y_offset,
                size[0],
                size[1],
            ))
            col += 1
            if col > 3:
                col = 0
                row += 1
        gi = functions.count_iterator()
        # Create the list from which the hex buttons will be constructed
        hex_button_list = [
            ButtonInfo(
                "button_line_cut",
                geometries[next(gi)],
                "tango_icons/edit-line-cut.png",
                menubar_functions["line_cut"],
                "Line Cut",
                input_focus_last_widget=data.HexButtonFocus.TAB,
            ),
            ButtonInfo(
                "button_1",
                geometries[next(gi)],
                "tango_icons/edit-line-copy.png",
                menubar_functions["line_copy"],
                "Line Copy",
                input_focus_last_widget=data.HexButtonFocus.TAB,
            ),
            ButtonInfo(
                "button_2",
                geometries[next(gi)],
                "tango_icons/edit-line-delete.png",
                menubar_functions["line_delete"],
                "Line Delete",
                input_focus_last_widget=data.HexButtonFocus.TAB,
            ),
            ButtonInfo(
                "button_3",
                geometries[next(gi)],
                "tango_icons/edit-line-transpose.png",
                menubar_functions["line_transpose"],
                "Line\nTranspose",
                input_focus_last_widget=data.HexButtonFocus.TAB,
            ),
            ButtonInfo(
                "button_4",
                geometries[next(gi)],
                "tango_icons/edit-line-duplicate.png",
                menubar_functions["line_duplicate"],
                "Line\nDuplicate",
                input_focus_last_widget=data.HexButtonFocus.TAB,
            ),
            ButtonInfo(
                "button_5",
                geometries[next(gi)],
                "tango_icons/edit-redo.png",
                menubar_functions["redo"],
                "Redo",
                input_focus_last_widget=data.HexButtonFocus.TAB,
            ),
            ButtonInfo(
                "button_6",
                geometries[next(gi)],
                "tango_icons/edit-undo.png",
                menubar_functions["undo"],
                "Undo",
                input_focus_last_widget=data.HexButtonFocus.TAB,
            ),
            ButtonInfo(
                "button_7",
                geometries[next(gi)],
                "tango_icons/delete-end-line.png",
                menubar_functions["delete_end_of_line"],
                "Delete line\nending",
                input_focus_last_widget=data.HexButtonFocus.TAB,
            ),
            ButtonInfo(
                "button_8",
                geometries[next(gi)],
                "tango_icons/delete-start-line.png",
                menubar_functions["delete_start_of_line"],
                "Delete line\nbeginning",
                input_focus_last_widget=data.HexButtonFocus.TAB,
            ),
            ButtonInfo(
                "button_goto_start",
                geometries[next(gi)],
                "tango_icons/goto-start.png",
                menubar_functions["goto_to_start"],
                "Goto Start",
                input_focus_last_widget=data.HexButtonFocus.TAB,
            ),
            ButtonInfo(
                "button_goto_end",
                geometries[next(gi)],
                "tango_icons/goto-end.png",
                menubar_functions["goto_to_end"],
                "Goto End",
                input_focus_last_widget=data.HexButtonFocus.TAB,
            ),
            ButtonInfo(
                "button_select_all",
                geometries[next(gi)],
                "tango_icons/edit-select-all.png",
                menubar_functions["select_all"],
                "Select All",
                input_focus_last_widget=data.HexButtonFocus.TAB,
            ),
        ]
        self.__create_hex_buttons_from_list(hex_button_list)

    def __init_advanced_buttons(self):
        # Alias the class references to shorten the names
        form = self.main_form
        menubar_functions = self.main_form.menubar_functions
        # Generate positions/size
        size = (50, 50)
        start = (224, 0)
        row = 0
        col = 0
        geometries = []
        for i in range(26):
            geometries.append((
                (start[0] + (col * size[0]))+self.button_x_offset,
                (start[1] + (row * size[1]))+self.button_y_offset,
                size[0],
                size[1],
            ))
            col += 1
            if col > 7:
                col = 0
                row += 1
        gi = functions.count_iterator()
        # Create the list from which the hex buttons will be constructed
        hex_button_list = [
            ButtonInfo(
                "button_find",
                geometries[next(gi)],
                "tango_icons/edit-find.png",
                menubar_functions["special_find"],
                "Find",
                input_focus_last_widget=data.HexButtonFocus.TAB,
                input_check_text_differ=True,
            ),
            ButtonInfo(
                "button_find_regex",
                geometries[next(gi)],
                "tango_icons/edit-find-re.png",
                menubar_functions["special_regex_find"],
                "Regex Find",
                input_focus_last_widget=data.HexButtonFocus.TAB,
                input_check_text_differ=True,
            ),
            ButtonInfo(
                "button_13",
                geometries[next(gi)],
                "tango_icons/edit-find-replace.png",
                menubar_functions["special_find_and_replace"],
                "Find and\nReplace",
                input_focus_last_widget=data.HexButtonFocus.TAB,
            ),
            ButtonInfo(
                "button_14",
                geometries[next(gi)],
                "tango_icons/edit-find-replace-re.png",
                menubar_functions["special_regex_find_and_replace"],
                "Regex Find\nand Replace",
                input_focus_last_widget=data.HexButtonFocus.TAB,
            ),
            ButtonInfo(
                "button_goto_line",
                geometries[next(gi)],
                "tango_icons/edit-goto.png",
                menubar_functions["special_goto_line"],
                "Goto Line",
                input_focus_last_widget=data.HexButtonFocus.TAB,
                input_check_text_differ=True,
            ),
            ButtonInfo(
                "button_16",
                geometries[next(gi)],
                "tango_icons/edit-indent-to-cursor.png",
                menubar_functions["special_indent_to_cursor"],
                "Indent to\ncursor",
                input_focus_last_widget=data.HexButtonFocus.TAB,
            ),
            ButtonInfo(
                "button_17",
                geometries[next(gi)],
                "tango_icons/edit-highlight.png",
                menubar_functions["special_highlight"],
                "Highlight",
                input_focus_last_widget=data.HexButtonFocus.TAB,
            ),
            ButtonInfo(
                "button_18",
                geometries[next(gi)],
                "tango_icons/edit-highlight-re.png",
                menubar_functions["special_regex_highlight"],
                "Regex\nHighlight",
                input_focus_last_widget=data.HexButtonFocus.TAB,
            ),
            ButtonInfo(
                "button_19",
                geometries[next(gi)],
                "tango_icons/edit-clear-highlights.png",
                menubar_functions["special_clear_highlights"],
                "Clear\nHighlights",
                input_focus_last_widget=data.HexButtonFocus.TAB,
            ),
            ButtonInfo(
                "button_20",
                geometries[next(gi)],
                "tango_icons/edit-replace-in-selection.png",
                menubar_functions["special_replace_in_selection"],
                "Replace in\nselection",
                input_focus_last_widget=data.HexButtonFocus.TAB,
            ),
            ButtonInfo(
                "button_21",
                geometries[next(gi)],
                "tango_icons/edit-replace-in-selection-re.png",
                menubar_functions["special_regex_replace_in_selection"],
                "Regex Replace\nin selection",
                input_focus_last_widget=data.HexButtonFocus.TAB,
            ),
            ButtonInfo(
                "button_22",
                geometries[next(gi)],
                "tango_icons/edit-comment-uncomment.png",
                menubar_functions["comment_uncomment"],
                "Comment\nUncomment",
                input_focus_last_widget=data.HexButtonFocus.TAB,
            ),
            ButtonInfo(
                "button_23",
                geometries[next(gi)],
                "tango_icons/edit-replace-all.png",
                menubar_functions["special_replace_all"],
                "Replace All",
                input_focus_last_widget=data.HexButtonFocus.TAB,
            ),
            ButtonInfo(
                "button_24",
                geometries[next(gi)],
                "tango_icons/edit-replace-all-re.png",
                menubar_functions["special_regex_replace_all"],
                "Regex\nReplace All",
                input_focus_last_widget=data.HexButtonFocus.TAB,
            ),
            ButtonInfo(
                "button_25",
                geometries[next(gi)],
                "tango_icons/edit-autocompletion.png",
                menubar_functions["toggle_autocompletions"],
                "Toggle\nAutocompletions",
                input_focus_last_widget=data.HexButtonFocus.TAB,
            ),
            ButtonInfo(
                "button_26",
                geometries[next(gi)],
                "tango_icons/edit-case-to-upper.png",
                menubar_functions["special_to_uppercase"],
                "Selection to\nUPPERCASE",
                input_focus_last_widget=data.HexButtonFocus.TAB,
            ),
            ButtonInfo(
                "button_27",
                geometries[next(gi)],
                "tango_icons/edit-case-to-lower.png",
                menubar_functions["special_to_lowercase"],
                "Selection to\nlowercase",
                input_focus_last_widget=data.HexButtonFocus.TAB,
            ),
            ButtonInfo(
                "button_node_tree",
                geometries[next(gi)],
                "tango_icons/edit-node-tree.png",
                menubar_functions["create_node_tree"],
                "Create/Reload\n Node Tree",
                input_focus_last_widget=data.HexButtonFocus.TAB,
                input_tool_tip=("Create a node tree from the currently\n" +
                                "selected document and display it in the\n" +
                                "upper window.\nSupported programming languages:\n" +
                                "- C\n- Nim\n- Python 3"),
            ),
            ButtonInfo(
                "button_29",
                geometries[next(gi)],
                "tango_icons/view-refresh.png",
                menubar_functions["reload_file"],
                "Reload File",
                input_focus_last_widget=data.HexButtonFocus.TAB,
            ),
            ButtonInfo(
                "button_30",
                geometries[next(gi)],
                "tango_icons/edit-find-in-open-documents.png",
                menubar_functions["special_find_in_open_documents"],
                "Find in open\ndocuments",
                input_focus_last_widget=data.HexButtonFocus.TAB,
            ),
            ButtonInfo(
                "button_31",
                geometries[next(gi)],
                "tango_icons/edit-replace-in-open-documents.png",
                menubar_functions["special_find_replace_in_open_documents"],
                "Find and Replace\nin open documents",
                input_focus_last_widget=data.HexButtonFocus.TAB,
            ),
            ButtonInfo(
                "button_replace_all_in_open_documents",
                geometries[next(gi)],
                "tango_icons/edit-replace-all-in-open-documents.png",
                menubar_functions["special_replace_all_in_open_documents"],
                "Replace all in\nopen documents",
                input_focus_last_widget=data.HexButtonFocus.TAB,
            ),
            ButtonInfo(
                "button_bookmark_toggle",
                geometries[next(gi)],
                "tango_icons/bookmark.png",
                menubar_functions["bookmark_toggle"],
                "Toggle\nBookmark",
                input_focus_last_widget=data.HexButtonFocus.TAB,
            ),
            ButtonInfo(
                "button_toggle_wordwrap",
                geometries[next(gi)],
                "tango_icons/wordwrap.png",
                menubar_functions["toggle_wordwrap"],
                "Toggle\nWord Wrap",
                input_focus_last_widget=data.HexButtonFocus.TAB,
            ),
            ButtonInfo(
                "button_toggle_lineendings",
                geometries[next(gi)],
                "tango_icons/view-line-end.png",
                menubar_functions["toggle_line_endings"],
                "Toggle\nLine Ending\nVisibility",
                input_focus_last_widget=data.HexButtonFocus.TAB,
            ),
            ButtonInfo(
                "button_toggle_cursor_line_highlighting",
                geometries[next(gi)],
                "tango_icons/edit-show-cursor-line.png",
                menubar_functions["toggle_cursor_line_highlighting"],
                "Toggle\nCursor Line\nHighlighting",
                input_focus_last_widget=data.HexButtonFocus.TAB,
            ),
        ]
        self.__create_hex_buttons_from_list(hex_button_list)

    def __init_file_buttons(self):
        # Alias the class references to shorten the names
        form = self.main_form
        menubar_functions = self.main_form.menubar_functions
        # Generate positions/size
        size = (50, 50)
        start = (0, 160)
        row = 0
        col = 0
        geometries = []
        for i in range(13):
            geometries.append((
                (start[0] + (col * size[0])) + self.button_x_offset,
                (start[1] + (row * size[1])) + self.button_y_offset,
                size[0],
                size[1],
            ))
            col += 1
            if col > 3:
                col = 0
                row += 1
        gi = functions.count_iterator()
        # Create the list from which the hex buttons will be constructed
        hex_button_list = [
            ButtonInfo(
                "button_new",
                geometries[next(gi)],
                "tango_icons/document-new.png",
                form.file_create_new,
                "Create new\ndocument",
                input_focus_last_widget=data.HexButtonFocus.WINDOW,
                input_no_document_focus_disable=False,
            ),
            ButtonInfo(
                "button_open",
                geometries[next(gi)],
                "tango_icons/document-open.png",
                form.file_open,
                "Open\ndocument",
                input_focus_last_widget=data.HexButtonFocus.WINDOW,
                input_no_document_focus_disable=False,
            ),
            ButtonInfo(
                "button_user_funcs_open",
                geometries[next(gi)],
                "tango_icons/file-user-funcs.png",
                menubar_functions["open_user_func_file"],
                "Edit User\nFunctions",
                input_no_document_focus_disable=False,
            ),
            ButtonInfo(
                "button_user_funcs_reload",
                geometries[next(gi)],
                "tango_icons/file-user-funcs-reload.png",
                menubar_functions["import_user_functions"],
                "Reload User\nFunctions",
                input_no_document_focus_disable=False,
            ),
            ButtonInfo(
                "button_save",
                geometries[next(gi)],
                "tango_icons/document-save.png",
                form.file_save,
                "Save",
                input_focus_last_widget=data.HexButtonFocus.TAB,
                input_no_document_focus_disable=True,
                input_check_last_tab_type=True,
            ),
            ButtonInfo(
                "button_save_as",
                geometries[next(gi)],
                "tango_icons/document-save-as.png",
                form.file_saveas,
                "Save As",
                input_focus_last_widget=data.HexButtonFocus.TAB,
                input_no_document_focus_disable=True,
                input_check_last_tab_type=True,
            ),
            ButtonInfo(
                "button_save_all",
                geometries[next(gi)],
                "tango_icons/file-save-all.png",
                form.file_save_all,
                "Save All",
                input_focus_last_widget=data.HexButtonFocus.WINDOW,
                input_no_document_focus_disable=True,
                input_check_last_tab_type=True,
            ),

            ButtonInfo(
                "button_34",
                geometries[next(gi)],
                "tango_icons/close-all-tabs.png",
                form.close_all_tabs,
                "Close\nAll Tabs",
                input_no_document_focus_disable=False,
            ),
            ButtonInfo(
                "button_35",
                geometries[next(gi)],
                "tango_icons/file-settings-save.png",
                form.settings.save,
                "Save\nsettings",
                input_no_document_focus_disable=False,
            ),
            ButtonInfo(
                "button_36",
                geometries[next(gi)],
                "tango_icons/file-settings-load.png",
                form.settings.restore,
                "Load\nsettings",
                input_no_document_focus_disable=False,
            ),
            ButtonInfo(
                "button_38",
                geometries[next(gi)],
                "tango_icons/help-browser.png",
                form.view.show_about,
                "Show Ex.Co.\nInformation",
                input_no_document_focus_disable=False,
            ),
        ]
        self.__create_hex_buttons_from_list(hex_button_list)

    def __init_system_view_buttons(self):
        # Alias the class references to shorten the names
        form = self.main_form
        menubar_functions = self.main_form.menubar_functions
        f_p = functools.partial
        # Generate positions/size
        size = (50, 50)
        start = (224, 210)
        row = 0
        col = 0
        geometries = []
        for i in range(24):
            geometries.append((
                (start[0] + (col * size[0])) + self.button_x_offset,
                (start[1] + (row * size[1])) + self.button_y_offset,
                size[0],
                size[1],
            ))
            col += 1
            if col > 7:
                col = 0
                row += 1
        gi = functions.count_iterator()
        # Create the list from which the hex buttons will be constructed
        hex_button_list = [
            ButtonInfo(
                "button_43",
                geometries[next(gi)],
                "tango_icons/utilities-terminal.png",
                menubar_functions["special_run_command"],
                "Run Console\nCommand",
                input_no_document_focus_disable=False,
            ),
            ButtonInfo(
                "button_44",
                geometries[next(gi)],
                "tango_icons/view-fullscreen.png",
                form.view.toggle_window_size,
                "Maximize/\nNormalize",
                input_no_document_focus_disable=False,
            ),
            ButtonInfo(
                "button_45",
                geometries[next(gi)],
                "tango_icons/view-focus-main.png",
                f_p(form.view.set_window_focus, "main"),
                "Focus Main\nWindow",
                input_no_document_focus_disable=False,
            ),
            ButtonInfo(
                "button_46",
                geometries[next(gi)],
                "tango_icons/view-focus-upper.png",
                f_p(form.view.set_window_focus, "upper"),
                "Focus Upper\nWindow",
                input_no_document_focus_disable=False,
            ),
            ButtonInfo(
                "button_47",
                geometries[next(gi)],
                "tango_icons/view-focus-lower.png",
                f_p(form.view.set_window_focus, "lower"),
                "Focus Lower\nWindow",
                input_no_document_focus_disable=False,
            ),
            ButtonInfo(
                "button_48",
                geometries[next(gi)],
                "tango_icons/view-log.png",
                form.view.toggle_log_window,
                "Show/Hide\nLog Window",
                input_no_document_focus_disable=False,
            ),
            ButtonInfo(
                "button_49",
                geometries[next(gi)],
                "tango_icons/view-spin-clock.png",
                form.view.spin_widgets_clockwise,
                "Spin Windows\nClockwise",
                input_focus_last_widget=False,
                input_no_document_focus_disable=False,
            ),
            ButtonInfo(
                "button_50",
                geometries[next(gi)],
                "tango_icons/view-spin-counter.png",
                form.view.spin_widgets_counterclockwise,
                "Spin Windows\nCounter\nClockwise",
                input_focus_last_widget=False,
                input_no_document_focus_disable=False,
            ),
            ButtonInfo(
                "button_51",
                geometries[next(gi)],
                "tango_icons/view-toggle-window-mode.png",
                form.view.toggle_window_mode,
                "Toggle\nWindow Mode",
                input_focus_last_widget=False,
                input_no_document_focus_disable=False,
            ),
            ButtonInfo(
                "button_52",
                geometries[next(gi)],
                "tango_icons/view-toggle-window-side.png",
                form.view.toggle_main_window_side,
                "Toggle\nWindow Side",
                input_focus_last_widget=False,
                input_no_document_focus_disable=False,
            ),
            ButtonInfo(
                "button_move_tab_left",
                geometries[next(gi)],
                "tango_icons/view-move-tab-left.png",
                menubar_functions["move_tab_left"],
                "Move Tab\nLeft",
                input_focus_last_widget=data.HexButtonFocus.TAB,
                input_no_tab_focus_disable=True,
                input_no_document_focus_disable=False,
            ),
            ButtonInfo(
                "button_move_tab_right",
                geometries[next(gi)],
                "tango_icons/view-move-tab-right.png",
                menubar_functions["move_tab_right"],
                "Move Tab\nRight",
                input_focus_last_widget=data.HexButtonFocus.TAB,
                input_no_tab_focus_disable=True,
                input_no_document_focus_disable=False,
            ),
            ButtonInfo(
                "button_close_tab",
                geometries[next(gi)],
                "tango_icons/close-tab.png",
                menubar_functions["close_tab"],
                "Close Current\nTab",
                input_focus_last_widget=data.HexButtonFocus.TAB,
                input_no_tab_focus_disable=True,
                input_no_document_focus_disable=False,
            ),
            ButtonInfo(
                "button_55",
                geometries[next(gi)],
                "tango_icons/view-edge-marker.png",
                menubar_functions["show_edge"],
                "Show/Hide\nEdge Marker",
                input_focus_last_widget=data.HexButtonFocus.TAB,
            ),
            ButtonInfo(
                "button_zoom_reset",
                geometries[next(gi)],
                "tango_icons/view-zoom-reset.png",
                menubar_functions["reset_zoom"],
                "Zoom Reset",
                input_focus_last_widget=data.HexButtonFocus.TAB,
            ),
            ButtonInfo(
                "button_find_files",
                geometries[next(gi)],
                "tango_icons/system-find-files.png",
                menubar_functions["special_find_file"],
                "Find Files",
                input_no_document_focus_disable=False,
            ),
            ButtonInfo(
                "button_find_files",
                geometries[next(gi)],
                "tango_icons/system-find-files.png",
                menubar_functions["special_find_file_with_dialog"],
                "Find Files\nwith dialog",
                input_no_document_focus_disable=False,
            ),
            ButtonInfo(
                "button_find_in_files",
                geometries[next(gi)],
                "tango_icons/system-find-in-files.png",
                menubar_functions["special_find_in"],
                "Find in\nFiles",
                input_no_document_focus_disable=False,
            ),
            ButtonInfo(
                "button_find_in_files",
                geometries[next(gi)],
                "tango_icons/system-find-in-files.png",
                menubar_functions["special_find_in_with_dialog"],
                "Find in\nFiles with\ndialog",
                input_no_document_focus_disable=False,
            ),
            ButtonInfo(
                "button_replace_in_files",
                geometries[next(gi)],
                "tango_icons/system-replace-in-files.png",
                menubar_functions["special_replace_in_files"],
                "Replace all\nin Files",
                input_no_document_focus_disable=False,
            ),
            ButtonInfo(
                "button_replace_in_files",
                geometries[next(gi)],
                "tango_icons/system-replace-in-files.png",
                menubar_functions["special_replace_in_files_with_dialog"],
                "Replace all\nin Files\nwith dialog",
                input_no_document_focus_disable=False,
            ),
            ButtonInfo(
                "button_show_session_editor",
                geometries[next(gi)],
                "tango_icons/sessions-gui.png",
                menubar_functions["show_session_editor"],
                "Show Session\nEditor",
                input_no_document_focus_disable=False,
            ),
            ButtonInfo(
                "button_cwd_tree",
                geometries[next(gi)],
                "tango_icons/system-show-cwd-tree.png",
                menubar_functions["create_cwd_tree"],
                "Show CWD\nFile/Directory\nTree",
                input_focus_last_widget=data.HexButtonFocus.NONE,
                input_tool_tip=("Create a file/directory tree for the " +
                                "current working directory (CWD)"),
                input_no_document_focus_disable=False,
            ),
            ButtonInfo(
                "button_bookmarks_clear",
                geometries[next(gi)],
                "tango_icons/bookmarks-clear.png",
                menubar_functions["bookmarks_clear"],
                "Clear All\nBookmarks",
                input_focus_last_widget=data.HexButtonFocus.NONE,
                input_no_document_focus_disable=False,
            ),
        ]
        self.__create_hex_buttons_from_list(hex_button_list)

    def __init_repl_buttons(self):
        # Alias the class references to shorten the names
        form = self.main_form
        menubar_functions = self.main_form.menubar_functions
        # Generate positions/size
        size = (50, 50)
        start = (224, 370)
        row = 0
        col = 0
        geometries = []
        for i in range(24):
            geometries.append((
                (start[0] + (col * size[0])) + self.button_x_offset,
                (start[1] + (row * size[1])) + self.button_y_offset,
                size[0],
                size[1],
            ))
            col += 1
            if col > 7:
                col = 0
                row += 1
        gi = functions.count_iterator()
        # Create the list from which the hex buttons will be constructed
        hex_button_list = [
            ButtonInfo(
                "button_57",
                geometries[next(gi)],
                "tango_icons/repl-focus-single.png",
                menubar_functions["repl_single_focus"],
                "REPL Focus\n(Single Line)",
                input_focus_last_widget=False,
                input_no_document_focus_disable=False,
            ),
            ButtonInfo(
                "button_58",
                geometries[next(gi)],
                "tango_icons/repl-focus-multi.png",
                menubar_functions["repl_multi_focus"],
                "REPL Focus\n(Multi Line)",
                input_focus_last_widget=False,
                input_no_document_focus_disable=False,
            ),
            ButtonInfo(
                "button_59",
                geometries[next(gi)],
                "tango_icons/repl-repeat-command.png",
                form.repl.repeat_last_repl_eval,
                "Repeat Last\nREPL Command",
                input_focus_last_widget=False,
                input_no_document_focus_disable=False,
            ),
        ]
        self.__create_hex_buttons_from_list(hex_button_list)
    
    def __init_special_system_buttons(self):
        # Alias the class references to shorten the names
        form = self.main_form
        menubar_functions = self.main_form.menubar_functions
        # Generate positions/size
        size = (50, 50)
        start = (
            self.SIZE[0]-size[0]-self.button_x_offset*2,
            self.SIZE[1]-size[1]-self.button_y_offset*2
        )
        row = 0
        col = 0
        geometries = []
        for i in range(1):
            geometries.append((
                (start[0] + (col * size[0])) + self.button_x_offset,
                (start[1] + (row * size[1])) + self.button_y_offset,
                size[0],
                size[1],
            ))
            col += 1
            if col > 7:
                col = 0
                row += 1
        gi = functions.count_iterator()
        # Create the list from which the hex buttons will be constructed
        hex_button_list = [
            ButtonInfo(
                "button_39",
                geometries[next(gi)],
                "tango_icons/system-log-out.png",
                form.exit,
                "Exit Ex.Co.",
                input_no_document_focus_disable=False,
            ),
        ]
        self.__create_hex_buttons_from_list(hex_button_list)

    def __create_hex_buttons_from_list(self, hex_button_list):
        def create_click_func(func):
            def wrapper_click_func(*args):
                self.main_form.view.hide_function_wheel()
                func()
            return wrapper_click_func
        def create_enter_func(text, font):
            def wrapper_enter_func(*args):
                self.display(text, font)
            return wrapper_enter_func
        def create_leave_func(font):
            def wrapper_leave_func(*args):
                self.display("", font)
            return wrapper_leave_func
        # Create all of the buttons from the list
        for button in hex_button_list:
            init_button = StandardButton(
                self,
                self.main_form,
            )
            attributes = (
                "function_text",
                "font",
                "focus_last_widget",
                "no_tab_focus_disable",
                "no_document_focus_disable",
                "check_last_tab_type",
                "check_text_differ",
            )
            for att in attributes:
                setattr(init_button, att, getattr(button, att))
            init_button.setIcon(functions.create_icon(button.pixmap))
            init_button.setIconSize(
                data.QSize(
                    int(button.geometry[2]),
                    int(button.geometry[3])
                )
            )
            init_button.setToolTip(button.tool_tip)
            init_button.setStatusTip(button.tool_tip)
            init_button.set_click_function(
                create_click_func(button.function)
            )
            init_button.set_enter_function(
                create_enter_func(button.function_text, button.font)
            )
            init_button.set_leave_function(
                create_leave_func(button.font)
            )
            # Set the button size and location
            init_button.setGeometry(
                int(button.geometry[0]),
                int(button.geometry[1]),
                int(button.geometry[2]),
                int(button.geometry[3])
            )
            self.button_cache.append(init_button)

    def __check_hex_button_states(self):
        """
        Check the hex function button states when displaying the function wheel
        """
        for child_widget in self.children():
            # Skip the child widget if it is not a hex or double button
            if not isinstance(child_widget, StandardButton):
                continue
            # First display and enable the hex button
            child_widget.setVisible(True)
            child_widget.setEnabled(True)
            # If the button needs to focus on the last focused widget,
            # check if the last focused widget is valid
            last_widget = self.main_form.last_focused_widget
            last_tab    = self.main_form.last_focused_tab
            result = False
            if last_widget != None and last_widget.count() != 0:
                result = True
            if result == False and child_widget.no_tab_focus_disable == True:
                # Disable if no tab is focused
                child_widget.setEnabled(False)
            elif result == False and child_widget.no_document_focus_disable == True:
                # If document focus is needed by the button, check if a tab is a focused document
                child_widget.setEnabled(False)
            elif (child_widget.no_document_focus_disable == True and
                 (isinstance(last_tab, CustomEditor) == False and
                  isinstance(last_tab, PlainEditor) == False)):
                # If focus is needed by the button, check the tab is an editing widget
                child_widget.setEnabled(False)
            elif (child_widget.check_last_tab_type == True and
                  isinstance(last_tab, CustomEditor) == False):
                # Check tab type for save/save_as/save_all buttons, it must be a CustomEditor
                child_widget.setEnabled(False)
            elif (child_widget.no_document_focus_disable == True and
                  hasattr(last_tab, "actual_parent") == True and
                  isinstance(last_tab.actual_parent, TextDiffer) == True):
                # Check if tab is a TextDiffer, enable only the supported functions
                if (child_widget.function_text != "Find" and
                    child_widget.function_text != "Regex Find" and
                    child_widget.function_text != "Goto Line" and
                    child_widget.function_text != "Move Tab\nLeft" and
                    child_widget.function_text != "Move Tab\nRight" and
                    child_widget.function_text != "Close Current\nTab"):
                    child_widget.setEnabled(False)

    def hideEvent(self, event):
        """
        Overridden widget hide event
        """
        # Set focus to the last focused widget stored on the main form
        last_widget = self.main_form.last_focused_widget
        if last_widget != None:
            if last_widget.currentWidget() != None:
                last_widget.currentWidget().setFocus()

    def display(self, string, font):
        """
        Display string in the display label
        """
        # Setup additional font settings
        font.setBold(True)
        self.display_label.setFont(font)
        self.display_label.setAlignment(
            data.Qt.AlignHCenter | data.Qt.AlignVCenter
        )
        # Display the string
        self.display_label.setText(string)

    def hide(self):
        """
        Hide the function wheel overlay
        """
        # First clear the hex edge from all of the buttons
        for child_widget in self.children():
            # Skip the child widget if it is not a hex or double button
            if not isinstance(child_widget, StandardButton):
                continue
            # Hide the button, fixes a leaveEvent issue with the "Open File" function.
            child_widget.setVisible(False)
        # Disable the function wheel
        self.setVisible(False)
        self.setEnabled(False)

    def show(self):
        """
        Show the function wheel overlay
        """
        self.setVisible(True)
        self.setEnabled(True)
        #Refresh the states of the hex function buttons
        self.__check_hex_button_states()
        #Center to main form
        self.center(self.size())
        #Set the cursor to the center of the last executed function, if any
        self.highlight_last_clicked_button()
        self.setFocus()

    def scale(self, width_scale_factor=1, height_scale_factor=1):
        """Scale the size of the function wheel and all of its child widgets"""
        #Scale the function wheel form
        geo = self.geometry()
        new_width = int(geo.width() * width_scale_factor)
        new_height = int(geo.height() * height_scale_factor)
        rectangle = functions.create_rect(
            geo.topLeft(),
            functions.create_size(new_width, new_height)
        )
        self.setGeometry(rectangle)
        #Scale all of the function wheel child widgets
        for button in self.children():
            geo = button.geometry()
            new_topLeft = functions.create_point(
                int(geo.topLeft().x() * width_scale_factor),
                int(geo.topLeft().y() * height_scale_factor)
            )
            new_width = int(geo.width() * width_scale_factor)
            new_height = int(geo.height() * height_scale_factor)
            new_size = functions.create_size(new_width, new_height)
            rectangle = functions.create_rect(new_topLeft, new_size)
            button.setGeometry(rectangle)
        #Center to main form
        self.center(self.size())

    def center(self, size):
        """
        Center the function wheel to the main form,
        according to the size parameter
        """
        x_offset = int((self.main_form.size().width() - size.width()) / 2)
        y_offset = int((self.main_form.size().height()*93/100 - size.height()) / 2)
        rectangle_top_left = functions.create_point(x_offset, y_offset)
        rectangle_size = size
        rectangle = functions.create_rect(rectangle_top_left, rectangle_size)
        self.setGeometry(rectangle)

    def highlight_last_clicked_button(self):
        """Name says it all"""
        #Check if there is a stored button function
        last_function_text = self.main_form.view.last_executed_function_text
        if last_function_text == None:
            return
        #Loop through the buttons and check its function
        for button in self.children():
            if isinstance(button, CustomButton):
                #Compare the stored function text with the buttons function text
                if button.function_text == last_function_text:
                    #Only higlight the button if it is enabled
                    if button.isEnabled() == True:
                        button.highlight()
                    button_position = self.mapToGlobal(button.geometry().topLeft())
                    cursor = data.QCursor()
                    cursor.setPos(
                        button_position.x() + int(button.geometry().width()/2),
                        button_position.y() + int(button.geometry().height()/2)
                    )
                    break

    def update_style(self):
        self.setStyleSheet(f"""
            QGroupBox {{
                background-color: {data.theme["fonts"]["default"]["background"]};
                color: {data.theme["fonts"]["default"]["color"]};
                border: 1px solid {data.theme["indication"]["passiveborder"]};
                margin: 0px;
                padding: 0px;
                spacing: 0px;
            }}
        """)
        self.display_label.setStyleSheet(f"""
            QLabel {{
                background-color: {data.theme["fonts"]["default"]["background"]};
                color: {data.theme["fonts"]["default"]["color"]};
                border: 1px solid {data.theme["indication"]["activeborder"]};
                border-radius: 4px;
            }}
        """)
        for b in self.button_cache:
            b.update_style()

class ButtonInfo:
    """
    Simple object used as a structure for the custom button information
    """
    def __init__(self,
                input_name,
                input_geometry,
                input_pixmap,
                input_function,
                input_function_text,
                input_font=data.QFont(
                    data.current_font_name, 14, weight=data.QFont.Bold
                ),
                input_focus_last_widget=data.HexButtonFocus.NONE,
                input_no_tab_focus_disable=False,
                input_no_document_focus_disable=True,
                input_check_last_tab_type=False,
                input_extra_button=None,
                input_check_text_differ=False,
                input_tool_tip=None):
        # Initialize the attributes
        self.name = input_name
        self.geometry = input_geometry
        self.pixmap = input_pixmap
        self.function = input_function
        self.function_text = input_function_text
        self.font = input_font
        self.focus_last_widget = input_focus_last_widget
        self.no_tab_focus_disable = input_no_tab_focus_disable
        self.no_document_focus_disable = input_no_document_focus_disable
        self.check_last_tab_type = input_check_last_tab_type
        self.extra_button = input_extra_button
        self.check_text_differ = input_check_text_differ
        self.tool_tip = input_tool_tip