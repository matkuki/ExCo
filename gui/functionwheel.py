
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2019 Matic Kukovec.
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
import gc

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
    #Class custom objects/types
    class ButtonInfo:
        """
        Simple object used as a structure for the custom button information
        """
        #Class variables
        name                = None
        geometry            = None
        pixmap              = None
        function            = None
        function_text       = None
        font                = None
        focus_last_widget   = None
        no_tab_focus_disable        = None
        no_document_focus_disable   = None
        check_last_tab_type = None
        extra_button        = None
        check_text_differ   = None
        tool_tip            = None
        
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
            #Initialize the attributes
            self.name               = input_name
            self.geometry           = input_geometry
            self.pixmap             = input_pixmap
            self.function           = input_function
            self.function_text      = input_function_text
            self.font               = input_font
            self.focus_last_widget  = input_focus_last_widget
            self.no_tab_focus_disable   = input_no_tab_focus_disable
            self.no_document_focus_disable   = input_no_document_focus_disable
            self.check_last_tab_type    = input_check_last_tab_type
            self.extra_button       = input_extra_button
            self.check_text_differ  = input_check_text_differ
            self.tool_tip           = input_tool_tip

    #Class variables
    _parent                 = None
    main_form               = None
    background_image        = None
    display_label           = None
    cursor_show_position    = None
    theme_name              = None
    function_wheel_background_image = None
    
    @staticmethod
    def reset_background_image():
        FunctionWheel.function_wheel_background_image = None
    
    @staticmethod
    def check_theme_state():
        return FunctionWheel.theme_name != data.theme.name
    
    @staticmethod
    def create_background_image():
        """
        Dinamically create the function wheel's background image
        """
        # Check if the QPixmap has been created already
        if FunctionWheel.function_wheel_background_image == None:
            edge_length = 30
            
            FunctionWheel.theme_name = data.theme.name
            
            function_wheel_background_image = data.QImage(
                functions.create_size(600, 555),
                data.QImage.Format_ARGB32_Premultiplied
            )
            function_wheel_background_image.fill(data.Qt.transparent)
            painter = data.QPainter(function_wheel_background_image)
            painter.setRenderHints(
                data.QPainter.Antialiasing | 
                data.QPainter.TextAntialiasing | 
                data.QPainter.SmoothPixmapTransform
            )
            
            offset = (53, 57)
            edge_length = 30
            # Bottom grid
            hex_builder = components.HexBuilder(
                painter, 
                offset, 
                edge_length, 
                1.0, 
                fill_color=data.theme.Settings_Background,
                line_width=2,
                line_color=data.theme.Settings_Hex_Edge,
            )
            
            grid_list = [(1, True)]
            grid_list.extend(5 * [(2, True), (1, True)] + [(3, True)])
            for i in range(4):
                grid_list.extend(5 * [(4, True), (5, True)] + [(4, True), (3, True)])
                grid_list.extend(5 * [(1, True), (2, True)] + [(1, True), (3, True)])
            grid_list.extend(5 * [(4, True), (5, True)] + [(4, True)])
            hex_builder.create_grid(*grid_list)
            # Label field
            hex_builder = components.HexBuilder(
                painter, 
                (0, 0), 
                edge_length, 
                1.0, 
                fill_color=data.theme.Settings_Hex_Background,
                line_width=3,
                line_color=data.QColor(146,146,146),
            )
            hex_builder.set_first_position((offset[0], offset[1] + (16*hex_builder.vertical_step)))
            hex_builder.create_grid(
                2, 1, 5
            )
            
            painter.end()
            original_dialog_image = data.QPixmap.fromImage(function_wheel_background_image)
            FunctionWheel.function_wheel_background_image = data.QPixmap.fromImage(function_wheel_background_image)
        # Return the QPixmap
        return FunctionWheel.function_wheel_background_image
    
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
        # Reset the class variable
        FunctionWheel.function_wheel_background_image = None
        #Store the background image for sizing details
        self.background_image = data.QPixmap(
            FunctionWheel.create_background_image()
        )
        #Set the background color
        self.setStyleSheet("background-color:transparent;")
        self.setStyleSheet("border:0;")
        #Setup the picture
        fw_picture = data.QPixmap(
            FunctionWheel.create_background_image()
        )
        self.picture = data.QLabel(self)
        self.picture.setPixmap(fw_picture)
        self.picture.setGeometry(self.frameGeometry())
        self.picture.setScaledContents(True)
        self.layout = data.QGridLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(
            data.QMargins(0,0,0,0)
        )
        self.layout.addWidget(self.picture)
        self.setLayout(self.layout)
        
        #Initialize the display label that will display the function names
        #when the mouse cursor is over a function button
        self.display_label = data.QLabel(self)
        self.display_label.setGeometry(36, 448, 120, 50)
        font = data.QFont(data.current_font_name, 14)
        font.setBold(True)
        self.display_label.setFont(font)
        self.display_label.setAlignment(
            data.Qt.AlignHCenter | data.Qt.AlignVCenter
        )
        self.display_label.setStyleSheet(
            'color: rgb({}, {}, {})'.format(
                data.theme.Font.Default.red(),
                data.theme.Font.Default.green(),
                data.theme.Font.Default.blue(),
            )
        )
        #Initialize all of the hex function buttons
        self._init_all_buttons()
        #Position the overlay to the center of the screen
        self.center(self.background_image.size())
        #Scale the function wheel size if needed
        self.scale(1, 1)
    
    def _init_all_buttons(self):
        """Function for calling all button initialization subroutines"""
        self._init_file_buttons()
        self._init_basic_buttons()
        self._init_advanced_buttons()
        self._init_system_view_buttons()
        self._init_repl_buttons()
        #Check the states of the hex function buttons
        self._check_hex_button_states()
    
    def _init_basic_buttons(self):
        #Alias the class references to shorten the names
        form    = self.main_form
        #Create the list from which the hex buttons will be constructed
        hex_button_list = [ 
            self.ButtonInfo(
                "button_line_cut", 
                (244, 0, 68, 60), 
                "tango_icons/edit-line-cut.png", 
                form.menubar_functions["line_cut"], 
                "Line Cut", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ), 
            self.ButtonInfo(
                "button_1", 
                (244, 52, 68, 60), 
                "tango_icons/edit-line-copy.png", 
                form.menubar_functions["line_copy"], 
                "Line Copy", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ), 
            self.ButtonInfo(
                "button_2", 
                (199, 26, 68, 60), 
                "tango_icons/edit-line-delete.png", 
                form.menubar_functions["line_delete"], 
                "Line Delete", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_3", 
                (199, 79, 68, 60), 
                "tango_icons/edit-line-transpose.png", 
                form.menubar_functions["line_transpose"], 
                "Line\nTranspose", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_4", 
                (154, 53, 68, 60), 
                "tango_icons/edit-line-duplicate.png", 
                form.menubar_functions["line_duplicate"], 
                "Line\nDuplicate", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_5", 
                (154, 106, 68, 60), 
                "tango_icons/edit-redo.png", 
                form.menubar_functions["redo"], 
                "Redo", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ), 
            self.ButtonInfo(
                "button_6", 
                (109, 79, 68, 60), 
                "tango_icons/edit-undo.png", 
                form.menubar_functions["undo"], 
                "Undo", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ), 
            self.ButtonInfo(
                "button_7", 
                (109, 26, 68, 60), 
                "tango_icons/delete-end-line.png", 
                form.menubar_functions["delete_end_of_line"], 
                "Delete line\nending", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ), 
            self.ButtonInfo(
                "button_8", 
                (63, 0, 68, 60), 
                "tango_icons/delete-start-line.png", 
                form.menubar_functions["delete_start_of_line"], 
                "Delete line\nbeginning", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ), 
            self.ButtonInfo(
                "button_goto_start", 
                (19, 26, 68, 60), 
                "tango_icons/goto-start.png", 
                form.menubar_functions["goto_to_start"], 
                "Goto Start", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ), 
            self.ButtonInfo(
                "button_goto_end", 
                (64, 54, 68, 60), 
                "tango_icons/goto-end.png", 
                form.menubar_functions["goto_to_end"], 
                "Goto End", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ), 
            self.ButtonInfo(
                "button_select_all", 
                (153, 0, 68, 60), 
                "tango_icons/edit-select-all.png", 
                form.menubar_functions["select_all"], 
                "Select All", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ), 
        ]
        self._create_hex_buttons_from_list(hex_button_list)
    
    def _init_advanced_buttons(self):
        #Alias the class references to shorten the names
        form    = self.main_form
        #Create the list from which the hex buttons will be constructed
        hex_button_list = [ 
            self.ButtonInfo(
                "button_find", 
                (514, 0, 68, 60), 
                "tango_icons/edit-find.png", 
                form.menubar_functions["special_find"], 
                "Find", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
                input_check_text_differ=True, 
            ), 
            self.ButtonInfo(
                "button_find_regex", 
                (514, 53, 68, 60), 
                "tango_icons/edit-find-re.png", 
                form.menubar_functions["special_regex_find"], 
                "Regex Find", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
                input_check_text_differ=True, 
            ),
            self.ButtonInfo(
                "button_13", 
                (469, 26, 68, 60), 
                "tango_icons/edit-find-replace.png", 
                form.menubar_functions["special_find_and_replace"], 
                "Find and\nReplace", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_14", 
                (469, 79, 68, 60), 
                "tango_icons/edit-find-replace-re.png", 
                form.menubar_functions["special_regex_find_and_replace"], 
                "Regex Find\nand Replace", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_goto_line", 
                (514, 104, 68, 60), 
                "tango_icons/edit-goto.png", 
                form.menubar_functions["special_goto_line"], 
                "Goto Line", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
                input_check_text_differ=True, 
            ),
            self.ButtonInfo(
                "button_16", 
                (469, 130, 68, 60), 
                "tango_icons/edit-indent-to-cursor.png", 
                form.menubar_functions["special_indent_to_cursor"], 
                "Indent to\ncursor", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_17", 
                (424, 53, 68, 60), 
                "tango_icons/edit-highlight.png", 
                form.menubar_functions["special_highlight"], 
                "Highlight", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_18", 
                (424, 104, 68, 60), 
                "tango_icons/edit-highlight-re.png", 
                form.menubar_functions["special_regex_highlight"], 
                "Regex\nHighlight", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_19", 
                (424, 155, 68, 60), 
                "tango_icons/edit-clear-highlights.png", 
                form.menubar_functions["special_clear_highlights"], 
                "Clear\nHighlights", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_20", 
                (379, 79, 68, 60), 
                "tango_icons/edit-replace-in-selection.png", 
                form.menubar_functions["special_replace_in_selection"], 
                "Replace in\nselection", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_21", 
                (379, 130, 68, 60), 
                "tango_icons/edit-replace-in-selection-re.png", 
                form.menubar_functions["special_regex_replace_in_selection"], 
                "Regex Replace\nin selection", 
                input_font=data.QFont(
                                    data.current_font_name, 11, weight=data.QFont.Bold
                                ), 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_22", 
                (379, 182, 68, 60), 
                "tango_icons/edit-comment-uncomment.png", 
                form.menubar_functions["comment_uncomment"], 
                "Comment\nUncomment", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_23", 
                (334, 105, 68, 60), 
                "tango_icons/edit-replace-all.png", 
                form.menubar_functions["special_replace_all"], 
                "Replace All", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_24", 
                (334, 157, 68, 60), 
                "tango_icons/edit-replace-all-re.png", 
                form.menubar_functions["special_regex_replace_all"], 
                "Regex\nReplace All", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_25", 
                (334, 208, 68, 60), 
                "tango_icons/edit-autocompletion.png", 
                form.menubar_functions["toggle_autocompletions"], 
                "Toggle\nAutocompletions", 
                input_font=data.QFont(
                                    data.current_font_name, 10, weight=data.QFont.Bold
                                ), 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_26", 
                (288, 131, 68, 60), 
                "tango_icons/edit-case-to-upper.png", 
                form.menubar_functions["special_to_uppercase"], 
                "Selection to\nUPPERCASE", 
                input_font=data.QFont(
                                    data.current_font_name, 12, weight=data.QFont.Bold
                                ), 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_27", 
                (289, 183, 68, 60), 
                "tango_icons/edit-case-to-lower.png", 
                form.menubar_functions["special_to_lowercase"], 
                "Selection to\nlowercase", 
                input_font=data.QFont(
                                    data.current_font_name, 12, weight=data.QFont.Bold
                                ), 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_node_tree", 
                (287, 234, 68, 60), 
                "tango_icons/edit-node-tree.png", 
                form.menubar_functions["create_node_tree"], 
                "Create/Reload\n Node Tree", 
                input_font=data.QFont(
                                    data.current_font_name, 11, weight=data.QFont.Bold
                                ), 
                input_focus_last_widget=data.HexButtonFocus.TAB,  
                input_tool_tip=("Create a node tree from the currently\n" +
                                "selected document and display it in the\n" +
                                "upper window.\nSupported programming languages:\n" +
                                "- C\n- Nim\n- Python 3"), 
            ),
            self.ButtonInfo(
                "button_29", 
                (244, 156, 68, 60), 
                "tango_icons/view-refresh.png", 
                form.menubar_functions["reload_file"], 
                "Reload File", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_30", 
                (244, 208, 68, 60), 
                "tango_icons/edit-find-in-open-documents.png", 
                form.menubar_functions["special_find_in_open_documents"], 
                "Find in open\ndocuments", 
                input_font=data.QFont(
                                    data.current_font_name, 12, weight=data.QFont.Bold
                                ), 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_31", 
                (244, 261, 68, 60), 
                "tango_icons/edit-replace-in-open-documents.png", 
                form.menubar_functions["special_find_replace_in_open_documents"], 
                "Find and Replace\nin open documents", 
                input_font=data.QFont(
                                    data.current_font_name, 9, weight=data.QFont.Bold
                                ), 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_replace_all_in_open_documents", 
                (198, 234, 68, 60), 
                "tango_icons/edit-replace-all-in-open-documents.png", 
                form.menubar_functions["special_replace_all_in_open_documents"], 
                "Replace all in\nopen documents", 
                input_font=data.QFont(
                                    data.current_font_name, 10, weight=data.QFont.Bold
                                ), 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_bookmark_toggle", 
                (198, 183, 68, 60), 
                "tango_icons/bookmark.png", 
                form.menubar_functions["bookmark_toggle"], 
                "Toggle\nBookmark", 
                input_font=data.QFont(
                                    data.current_font_name, 14, weight=data.QFont.Bold
                                ), 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_toggle_wordwrap", 
                (424, 0, 68, 60), 
                "tango_icons/wordwrap.png", 
                form.menubar_functions["toggle_wordwrap"], 
                "Toggle\nWord Wrap", 
                input_font=data.QFont(
                                    data.current_font_name, 14, weight=data.QFont.Bold
                                ), 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_toggle_lineendings", 
                (378, 26, 68, 60), 
                "tango_icons/view-line-end.png", 
                form.menubar_functions["toggle_line_endings"], 
                "Toggle\nLine Ending\nVisibility", 
                input_font=data.QFont(
                                    data.current_font_name, 12, weight=data.QFont.Bold
                                ), 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_toggle_cursor_line_highlighting", 
                (334, 53, 68, 60), 
                "tango_icons/edit-show-cursor-line.png", 
                form.menubar_functions["toggle_cursor_line_highlighting"], 
                "Toggle\nCursor Line\nHighlighting", 
                input_font=data.QFont(
                    data.current_font_name, 12, weight=data.QFont.Bold
                ), 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
        ]
        self._create_hex_buttons_from_list(hex_button_list)
    
    def _init_file_buttons(self):
        #Alias the class references to shorten the names
        form    = self.main_form
        #Create the list from which the hex buttons will be constructed
        hex_button_list = [ 
            self.ButtonInfo(
                "button_new", 
                (19, 131, 68, 60), 
                "tango_icons/document-new.png", 
                form.file_create_new, 
                "Create new\ndocument", 
                input_focus_last_widget=data.HexButtonFocus.WINDOW, 
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_open", 
                (109, 182, 68, 60), 
                "tango_icons/document-open.png", 
                form.file_open, 
                "Open\ndocument", 
                input_focus_last_widget=data.HexButtonFocus.WINDOW, 
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_user_funcs_open", 
                (19, 182, 68, 60), 
                "tango_icons/file-user-funcs.png", 
                form.menubar_functions["open_user_func_file"], 
                "Edit User\nFunctions", 
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_user_funcs_reload", 
                (64, 156, 68, 60), 
                "tango_icons/file-user-funcs-reload.png", 
                form.menubar_functions["import_user_functions"], 
                "Reload User\nFunctions", 
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_save", 
                (19, 234, 68, 60), 
                "tango_icons/document-save.png", 
                form.file_save, 
                "Save", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
                input_no_document_focus_disable=True, 
                input_check_last_tab_type=True, 
            ),
            self.ButtonInfo(
                "button_save_as", 
                (64, 208, 68, 60), 
                "tango_icons/document-save-as.png", 
                form.file_saveas, 
                "Save As", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
                input_no_document_focus_disable=True, 
                input_check_last_tab_type=True, 
            ),
            self.ButtonInfo(
                "button_save_all", 
                (109, 234, 68, 60),
                "tango_icons/file-save-all.png", 
                form.file_save_all, 
                "Save All", 
                input_focus_last_widget=data.HexButtonFocus.WINDOW, 
                input_no_document_focus_disable=True, 
                input_check_last_tab_type=True, 
            ),
            
            self.ButtonInfo(
                "button_34", 
                (109, 285, 68, 60), 
                "tango_icons/close-all-tabs.png", 
                form.close_all_tabs, 
                "Close\nAll Tabs", 
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_35", 
                (64, 259, 68, 60), 
                "tango_icons/file-settings-save.png", 
                form.settings.save, 
                "Save\nsettings", 
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_36", 
                (19, 285, 68, 60), 
                "tango_icons/file-settings-load.png", 
                form.settings.restore, 
                "Load\nsettings", 
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_38", 
                (64, 311, 68, 60), 
                "tango_icons/help-browser.png", 
                form.view.show_about, 
                "Show Ex.Co.\nInformation", 
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_39", 
                (514, 468, 68, 60), 
                "tango_icons/system-log-out.png", 
                form.exit, 
                "Exit Ex.Co.", 
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_40", 
                (19, 338, 68, 60), 
                "tango_icons/themes-reload.png", 
                form.view.reload_themes, 
                "Reload\nThemes", 
                input_no_document_focus_disable=False, 
            ),
        ]
        self._create_hex_buttons_from_list(hex_button_list)
    
    def _init_system_view_buttons(self):
        #Alias the class references to shorten the names
        form    = self.main_form
        f_p     = functools.partial
        #Create the list from which the hex buttons will be constructed
        hex_button_list = [ 
            self.ButtonInfo(
                "button_43", 
                (469, 233, 68, 60), 
                "tango_icons/utilities-terminal.png", 
                form.menubar_functions["special_run_command"], 
                "Run Console\nCommand", 
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_44", 
                (469, 286, 68, 60), 
                "tango_icons/view-fullscreen.png", 
                form.view.toggle_window_size, 
                "Maximize/\nNormalize", 
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_45", 
                (424, 260, 68, 60), 
                "tango_icons/view-focus-main.png", 
                f_p(form.view.set_window_focus, "main"), 
                "Focus Main\nWindow", 
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_46", 
                (424, 312, 68, 60), 
                "tango_icons/view-focus-upper.png", 
                f_p(form.view.set_window_focus, "upper"), 
                "Focus Upper\nWindow", 
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_47", 
                (424, 364, 68, 60), 
                "tango_icons/view-focus-lower.png", 
                f_p(form.view.set_window_focus, "lower"), 
                "Focus Lower\nWindow", 
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_48", 
                (469, 338, 68, 60), 
                "tango_icons/view-log.png", 
                form.view.toggle_log_window, 
                "Show/Hide\nLog Window", 
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_49", 
                (379, 286, 68, 60), 
                "tango_icons/view-spin-clock.png", 
                form.view.spin_widgets_clockwise, 
                "Spin Windows\nClockwise", 
                input_focus_last_widget=False, 
                input_font=data.QFont(
                                data.current_font_name, 12, weight=data.QFont.Bold
                            ), 
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_50", 
                (379, 338, 68, 60), 
                "tango_icons/view-spin-counter.png", 
                form.view.spin_widgets_counterclockwise, 
                "Spin Windows\nCounter\nClockwise",  
                input_focus_last_widget=False, 
                input_font=data.QFont(
                                data.current_font_name, 10, weight=data.QFont.Bold
                            ), 
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_51", 
                (334, 363, 68, 60), 
                "tango_icons/view-toggle-window-mode.png", 
                form.view.toggle_window_mode, 
                "Toggle\nWindow Mode",  
                input_focus_last_widget=False, 
                input_font=data.QFont(
                                data.current_font_name, 13, weight=data.QFont.Bold
                            ), 
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_52", 
                (334, 311, 68, 60), 
                "tango_icons/view-toggle-window-side.png", 
                form.view.toggle_main_window_side, 
                "Toggle\nWindow Side",  
                input_focus_last_widget=False, 
                input_font=data.QFont(
                                data.current_font_name, 13, weight=data.QFont.Bold
                            ), 
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_move_tab_left", 
                (334, 415, 68, 60), 
                "tango_icons/view-move-tab-left.png", 
                form.menubar_functions["move_tab_left"], 
                "Move Tab\nLeft",
                input_focus_last_widget=data.HexButtonFocus.TAB, 
                input_no_tab_focus_disable=True,
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_move_tab_right", 
                (379, 389, 68, 60), 
                "tango_icons/view-move-tab-right.png", 
                form.menubar_functions["move_tab_right"], 
                "Move Tab\nRight", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
                input_no_tab_focus_disable=True,
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_close_tab", 
                (289, 441, 68, 60),
                "tango_icons/close-tab.png", 
                form.menubar_functions["close_tab"], 
                "Close Current\nTab", 
                input_font=data.QFont(
                                    data.current_font_name, 11, weight=data.QFont.Bold
                                ), 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
                input_no_tab_focus_disable=True,
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_55", 
                (289, 389, 68, 60), 
                "tango_icons/view-edge-marker.png", 
                form.menubar_functions["show_edge"], 
                "Show/Hide\nEdge Marker", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_zoom_reset", 
                (289, 338, 68, 60), 
                "tango_icons/view-zoom-reset.png", 
                form.menubar_functions["reset_zoom"], 
                "Zoom Reset", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_find_files", 
                (514, 207, 68, 60), 
                "tango_icons/system-find-files.png", 
                form.menubar_functions["special_find_file"], 
                "Find Files",  
                input_no_document_focus_disable=False, 
                input_extra_button=["various/hex-button-dir-dialog.png", 
                                    form.menubar_functions["special_find_file_with_dialog"], 
                                    "Find Files\nwith dialog", 
                                    ],
            ),
            self.ButtonInfo(
                "button_find_in_files", 
                (514, 259, 68, 60), 
                "tango_icons/system-find-in-files.png", 
                form.menubar_functions["special_find_in"], 
                "Find in\nFiles", 
                input_no_document_focus_disable=False, 
                input_extra_button=["various/hex-button-dir-dialog.png", 
                                    form.menubar_functions["special_find_in_with_dialog"], 
                                    "Find in\nFiles with\ndialog", 
                                    ], 
            ),
            self.ButtonInfo(
                "button_replace_in_files", 
                (514, 311, 68, 60), 
                "tango_icons/system-replace-in-files.png", 
                form.menubar_functions["special_replace_in_files"], 
                "Replace all\nin Files", 
                input_no_document_focus_disable=False, 
                input_extra_button=["various/hex-button-dir-dialog.png", 
                                    form.menubar_functions["special_replace_in_files_with_dialog"], 
                                    "Replace all\nin Files\nwith dialog", 
                                    ],  
            ),
            self.ButtonInfo(
                "button_show_session_editor", 
                (514, 364, 68, 60), 
                "tango_icons/sessions-gui.png", 
                form.menubar_functions["show_session_editor"], 
                "Show Session\nEditor", 
                input_no_document_focus_disable=False,
                input_font=data.QFont(
                                    data.current_font_name, 12, weight=data.QFont.Bold
                                ), 
            ),
            self.ButtonInfo(
                "button_cwd_tree", 
                (468, 390, 68, 60), 
                "tango_icons/system-show-cwd-tree.png", 
                form.menubar_functions["create_cwd_tree"], 
                "Show CWD\nFile/Directory\nTree", 
                input_font=data.QFont(
                                    data.current_font_name, 10, weight=data.QFont.Bold
                                ), 
                input_focus_last_widget=data.HexButtonFocus.NONE, 
                input_tool_tip=("Create a file/directory tree for the " + 
                                "current working directory (CWD)"), 
                input_no_document_focus_disable=False,
            ),
            self.ButtonInfo(
                "button_bookmarks_clear", 
                (424, 415, 68, 60), 
                "tango_icons/bookmarks-clear.png", 
                form.menubar_functions["bookmarks_clear"], 
                "Clear All\nBookmarks", 
                input_font=data.QFont(
                                    data.current_font_name, 14, weight=data.QFont.Bold
                                ), 
                input_focus_last_widget=data.HexButtonFocus.NONE, 
                input_no_document_focus_disable=False,
            ),
        ]
        self._create_hex_buttons_from_list(hex_button_list)
    
    def _init_repl_buttons(self):
        #Alias the class references to shorten the names
        form    = self.main_form
        #Create the list from which the hex buttons will be constructed
        hex_button_list = [ 
            self.ButtonInfo(
                "button_57", 
                (199, 338, 68, 60), 
                "tango_icons/repl-focus-single.png", 
                form.menubar_functions["repl_single_focus"], 
                "REPL Focus\n(Single Line)",  
                input_focus_last_widget=False, 
                input_font=data.QFont(
                                data.current_font_name, 13, weight=data.QFont.Bold
                            ), 
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_58", 
                (199, 390, 68, 60), 
                "tango_icons/repl-focus-multi.png", 
                form.menubar_functions["repl_multi_focus"], 
                "REPL Focus\n(Multi Line)",  
                input_focus_last_widget=False, 
                input_font=data.QFont(
                                data.current_font_name, 13, weight=data.QFont.Bold
                            ), 
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_59", 
                (154, 364, 68, 60), 
                "tango_icons/repl-repeat-command.png", 
                form.repl.repeat_last_repl_eval, 
                "Repeat Last\nREPL Command",  
                input_focus_last_widget=False, 
                input_font=data.QFont(
                                data.current_font_name, 13, weight=data.QFont.Bold
                            ), 
                input_no_document_focus_disable=False, 
            ),
        ]
        self._create_hex_buttons_from_list(hex_button_list)
    
    def _create_hex_buttons_from_list(self, hex_button_list):
        #Create all of the buttons from the list
        for button in hex_button_list:
            #Initialize the custom hex buttom
            if button.extra_button != None:
                init_button = DoubleButton(
                    self, 
                    self.main_form, 
                    input_pixmap=functions.create_pixmap(button.pixmap), 
                    input_function=button.function, 
                    input_function_text=button.function_text, 
                    input_font=button.font, 
                    input_focus_last_widget=button.focus_last_widget, 
                    input_no_tab_focus_disable=button.no_tab_focus_disable, 
                    input_no_document_focus_disable=button.no_document_focus_disable, 
                    input_check_last_tab_type=button.check_last_tab_type, 
                    input_check_text_differ=button.check_text_differ, 
                    input_tool_tip=button.tool_tip, 
                )
                init_button.init_extra_button(
                    self, 
                    self.main_form, 
                    functions.create_pixmap(button.extra_button[0]), 
                    input_extra_function=button.extra_button[1],
                    input_extra_function_text=button.extra_button[2], 
                )
            else:
                init_button = CustomButton(
                    self, 
                    self.main_form, 
                    input_pixmap=functions.create_pixmap(button.pixmap), 
                    input_function=button.function, 
                    input_function_text=button.function_text, 
                    input_font=button.font, 
                    input_focus_last_widget=button.focus_last_widget, 
                    input_no_tab_focus_disable=button.no_tab_focus_disable, 
                    input_no_document_focus_disable=button.no_document_focus_disable, 
                    input_check_last_tab_type=button.check_last_tab_type, 
                    input_check_text_differ=button.check_text_differ, 
                    input_tool_tip=button.tool_tip, 
                )
            #Set the button size and location
            init_button.setGeometry(
                int(button.geometry[0]), 
                int(button.geometry[1]), 
                int(button.geometry[2]), 
                int(button.geometry[3])
            )
    
    def _check_hex_button_states(self):
        """Check the hex function button states when displaying the function wheel"""
        for child_widget in self.children():
            #Skip the child widget if it is not a hex or double button
            if (isinstance(child_widget, CustomButton) == False and
                isinstance(child_widget, DoubleButton) == False):
                continue
            #First display and enable the hex button
            child_widget.setVisible(True)
            child_widget.setEnabled(True)
            if isinstance(child_widget, DoubleButton) == True:
                child_widget.extra_button_enable()
            #If the button needs to focus on the last focused widget,
            #check if the last focused widget is valid
            last_widget = self.main_form.last_focused_widget
            last_tab    = self.main_form.last_focused_tab
            result = False
            if last_widget != None and last_widget.count() != 0:
                result = True
            if result == False and child_widget.no_tab_focus_disable == True:
                #Disable if no tab is focused
                child_widget.setEnabled(False)
            elif result == False and child_widget.no_document_focus_disable == True:
                #If document focus is needed by the button, check if a tab is a focused document
                child_widget.setEnabled(False)
            elif (child_widget.no_document_focus_disable == True and
                 (isinstance(last_tab, CustomEditor) == False and
                  isinstance(last_tab, PlainEditor) == False)):
                #If focus is needed by the button, check the tab is an editing widget
                child_widget.setEnabled(False)
            elif (child_widget.check_last_tab_type == True and
                  isinstance(last_tab, CustomEditor) == False):
                #Check tab type for save/save_as/save_all buttons, it must be a CustomEditor
                child_widget.setEnabled(False)
            elif (child_widget.no_document_focus_disable == True and
                  hasattr(last_tab, "actual_parent") == True and
                  isinstance(last_tab.actual_parent, TextDiffer) == True):
                #Check if tab is a TextDiffer, enable only the supported functions
                if (child_widget.function_text != "Find" and
                    child_widget.function_text != "Regex Find" and
                    child_widget.function_text != "Goto Line" and
                    child_widget.function_text != "Move Tab\nLeft" and
                    child_widget.function_text != "Move Tab\nRight" and
                    child_widget.function_text != "Close Current\nTab"):
                    child_widget.setEnabled(False)
            #Call the dim method to draw the hex edge if the button is enabled
            if child_widget.isEnabled() == True:
                child_widget.dim()
            else:
                #Otherwise completley dim the button along with the hex edge
                child_widget.dim(clear_hex_edge=True)
    
    def hideEvent(self, event):
        """Overridden widget hide event"""
        #Set focus to the last focused widget stored on the main form
        last_widget = self.main_form.last_focused_widget
        if last_widget != None:
            if last_widget.currentWidget() != None:
                last_widget.currentWidget().setFocus()
    
    def display(self, string, font):
        """Display string in the display label"""
        #Setup additional font settings
        font.setBold(True)
        self.display_label.setFont(font)
        self.display_label.setAlignment(
            data.Qt.AlignHCenter | data.Qt.AlignVCenter
        )
        #Display the string
        self.display_label.setText(string)
    
    def hide(self):
        """Hide the function wheel overlay"""
        #First clear the hex edge from all of the buttons
        for child_widget in self.children():
            #Skip the child widget if it is not a hex or double button
            if (isinstance(child_widget, CustomButton) == False and
                isinstance(child_widget, DoubleButton) == False):
                continue
            #Dim the button and clear the hex edge
            child_widget.dim(clear_hex_edge=True)
            #Hide the button, fixes a leaveEvent issue with the "Open File" function.
            child_widget.setVisible(False)
            if isinstance(child_widget, DoubleButton) == True:
                child_widget.extra_button_disable()
        #Disable the function wheel
        self.setVisible(False)
        self.setEnabled(False)
    
    def show(self):
        """Show the function wheel overlay"""
        self.setVisible(True)
        self.setEnabled(True)
        #Refresh the states of the hex function buttons
        self._check_hex_button_states()
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


