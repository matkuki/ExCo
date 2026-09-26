"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.

Display utilities for the REPL, tree views, file finding,
lexer menus, and statusbar output. Namespace class attached
to the MainWindow instance.
"""

import functools
import os
import re
import traceback
from typing import Any, List, Optional

import constants
import functions
import gui.contextmenu
import gui.stylesheets
import lexers
import qt
import settings
from gui.customeditor import CustomEditor
from gui.menu import Menu
from gui.replindicator import ReplIndicator
from gui.sessionguimanipulator import SessionGuiManipulator
from gui.systempathmanipulator import SystemPathManipulator
from gui.textdiffer import TextDiffer
from gui.themeindicator import ThemeIndicator


class Display:
    """
    Functions for displaying of various functions such as:
    show_nodes, find_in_open_documents, ...
    (namespace/nested class to MainWindow)
    """

    # Class varibles
    _parent = None
    # Attribute for storing which type of tab is used for dispaying node trees
    node_view_type = constants.NodeDisplayType.TREE
    # Theme indicator label
    theme_indicator = None
    repl_indicator = None
    # Theme actions
    action_air = None
    action_earth = None
    action_water = None
    action_mc = None
    # References to the dynamically created menus
    stored_menus = []
    # Icons used for the special widgets
    node_tree_icon = None
    repl_messages_icon = None
    system_found_files_icon = None
    system_found_in_files_icon = None
    system_replace_in_files_icon = None
    system_show_cwd_tree_icon = None

    def __init__(self, parent: "MainWindow") -> None:
        """
        Initialization of the Display object instance
        """
        # Get the reference to the MainWindow parent object instance
        self._parent = parent
        # Initialize the stored icons
        self.node_tree_icon = functions.create_icon("tango_icons/edit-node-tree.png")
        self.repl_messages_icon = functions.create_icon("tango_icons/repl-messages.png")
        self.system_found_files_icon = functions.create_icon("tango_icons/system-find-files.png")
        self.system_found_in_files_icon = functions.create_icon(
            "tango_icons/system-find-in-files.png"
        )
        self.system_replace_in_files_icon = functions.create_icon(
            "tango_icons/system-replace-in-files.png"
        )
        self.system_show_cwd_tree_icon = functions.create_icon(
            "tango_icons/system-show-cwd-tree.png"
        )

    def init_theme_indicator(self) -> None:
        """
        Initialization of the theme indicator in the statusbar
        """
        self.theme_indicator = ThemeIndicator(self._parent.statusbar, self._parent)
        self.theme_indicator.set_image(settings.get_theme()["image-file"])
        self.theme_indicator.setToolTip(settings.get_theme()["tooltip"])
        self.theme_indicator.restyle()
        self._parent.statusbar.addPermanentWidget(self.theme_indicator)

    def update_theme_taskbar_icon(self) -> None:
        # Check if the indicator is initialized
        if self.theme_indicator is None:
            return
        # Set the theme icon and tooltip
        self.theme_indicator.set_image(settings.get_theme()["image-file"])
        self.theme_indicator.setToolTip(settings.get_theme()["tooltip"])
        self.theme_indicator.restyle()

    def init_repl_indicator(self) -> None:
        """
        Initialization of the REPL indicator in the statusbar
        """
        self.repl_indicator = ReplIndicator(
            self._parent.statusbar,
            self._parent,
            self._parent.repl_box,
        )
        self.repl_indicator.restyle()
        self._parent.statusbar.addPermanentWidget(self.repl_indicator)

    def write_to_statusbar(self, message: str, msec: int = 0) -> None:
        """Write a message to the statusbar"""
        self._parent.statusbar.setStyleSheet(gui.stylesheets.StyleSheetStatusbar.standard())
        self._parent.statusbar.showMessage(message, msec)

    def update_cursor_position(
        self,
        cursor_line: Optional[int] = None,
        cursor_column: Optional[int] = None,
        index: Optional[int] = None,
    ) -> None:
        """
        Update the position of the cursor in the current widget
        to the statusbar.
        """
        if cursor_line is None and cursor_column is None:
            self._parent.statusbar_label_left.setText("")
        else:
            statusbar_text = "LINE: {} COLUMN: {} / INDEX: {}".format(
                cursor_line + 1, cursor_column + 1, index
            )
            self._parent.statusbar_label_left.setText(statusbar_text)

    def repl_display_success(self, *message: Any) -> None:
        self.repl_display_message(*message, message_type=constants.MessageType.SUCCESS)

    def repl_display_error(self, *message: Any) -> None:
        self.repl_display_message(*message, message_type=constants.MessageType.ERROR)

    def repl_display_warning(self, *message: Any) -> None:
        self.repl_display_message(*message, message_type=constants.MessageType.WARNING)

    __repl_suppressed = False
    __repl_cache = []

    def repl_suppress(self) -> None:
        self.__repl_suppressed = True

    def repl_unsuppress(self) -> None:
        self.__repl_suppressed = False
        for items in self.__repl_cache:
            self.repl_display_message(
                *items[0],
                scroll_to_end=items[1],
                focus_repl_messages=items[2],
                message_type=items[3],
            )
        self.__repl_cache = []

    def repl_display_message(
        self,
        *message: Any,
        scroll_to_end: bool = True,
        focus_repl_messages: bool = True,
        message_type: Optional[constants.MessageType] = None,
    ) -> None:
        """
        Display the REPL return message in a scintilla tab
        named "REPL Messages" in one of the basic widgets
        """
        if self.__repl_suppressed:
            self.__repl_cache.append((message, scroll_to_end, focus_repl_messages, message_type))
            return

        # Nested function for styling REPL MESSAGES text
        def style_repl_text(start: int, end: int, color: str, lexer_number: int) -> None:
            """
            Initialize the style and style the text.
            Look at the Scintilla/Scite documentation for more details!
            This part is very cryptic, here are some hints:
                - do not use the SCI_STYLECLEARALL message, it will erase
                  all the previous styling in the document
                - when the lexer is None, the displayed style is 0. Use another style
                  number for custom styling
            """
            parent.repl_messages_tab.SendScintilla(
                qt.QsciScintillaBase.SCI_STYLESETFONT,
                lexer_number,
                settings.get("current_editor_font_name").encode("utf-8"),
            )
            parent.repl_messages_tab.SendScintilla(
                qt.QsciScintillaBase.SCI_STYLESETSIZE,
                lexer_number,
                settings.get("current_editor_font_size"),
            )
            parent.repl_messages_tab.SendScintilla(
                qt.QsciScintillaBase.SCI_STYLESETBOLD, lexer_number, True
            )
            parent.repl_messages_tab.SendScintilla(
                qt.QsciScintillaBase.SCI_STYLESETUNDERLINE, lexer_number, False
            )
            parent.repl_messages_tab.SendScintilla(
                qt.QsciScintillaBase.SCI_STYLESETFORE,
                lexer_number,
                qt.QColor(color),
            )
            parent.repl_messages_tab.SendScintilla(
                qt.QsciScintillaBase.SCI_STYLESETBACK,
                lexer_number,
                qt.QColor(settings.get_theme()["fonts"]["default"]["background"]),
            )
            parent.repl_messages_tab.SendScintilla(
                qt.QsciScintillaBase.SCI_STARTSTYLING, start, lexer_number
            )
            parent.repl_messages_tab.SendScintilla(
                qt.QsciScintillaBase.SCI_SETSTYLING, end - start, lexer_number
            )

        # Define references directly to the parent and mainform for performance and clarity
        parent = self._parent
        # Find the "REPL Message" tab in the basic widgets
        parent.repl_messages_tab = self.find_repl_messages_tab()
        # Create a new REPL tab in the lower basic widget if it doesn't exist
        if parent.repl_messages_tab is None:
            parent.repl_messages_tab = parent.get_repl_window().plain_add_document(
                constants.SpecialTabNames.Messages.value
            )
            rmt = parent.repl_messages_tab
            rmt.internals.set_icon(rmt, self.repl_messages_icon)
        # Parse the message arguments
        if len(message) > 1:
            message = " ".join([str(x) for x in message])
        else:
            message = message[0]
        # Check if message is a string class, if not then make it a string
        if message is None:
            return
        elif isinstance(message, str) == False:
            message = str(message)
        # Check if the message should be error colored
        if message_type is not None:
            # Convert the text to a byte array to get the correct length of the text
            # if it contains non-ASCII characters
            start_bytes = parent.repl_messages_tab.text().encode("utf-8")
            # Get the point from which the text will be highlighted
            start = len(start_bytes) - 1
            if start < 0:
                start = 0
            # Add the error message
            parent.repl_messages_tab.append("{}\n".format(message))
            # Convert the text to a byte array to get the correct length of the text
            # if it contains non-ASCII characters
            end_bytes = parent.repl_messages_tab.text().encode("utf-8")
            # Get the end point to which the text will be highlighted
            end = len(end_bytes) - 1
            if end < 0:
                end = 0
            elif end < start:
                end = start
            # THE MESSAGE COLORS ARE: 0xBBGGRR (BB-blue,GG-green,RR-red)
            if message_type == constants.MessageType.ERROR:
                style_repl_text(start, end, settings.get_theme()["fonts"]["error"]["color"], 1)
            elif message_type == constants.MessageType.WARNING:
                style_repl_text(
                    start,
                    end,
                    settings.get_theme()["fonts"]["warning"]["color"],
                    2,
                )
            elif message_type == constants.MessageType.SUCCESS:
                style_repl_text(
                    start,
                    end,
                    settings.get_theme()["fonts"]["success"]["color"],
                    3,
                )
            elif message_type == constants.MessageType.DIFF_UNIQUE_1:
                style_repl_text(
                    start,
                    end,
                    settings.get_theme()["fonts"]["diff-unique-1"]["color"],
                    4,
                )
            elif message_type == constants.MessageType.DIFF_UNIQUE_2:
                style_repl_text(
                    start,
                    end,
                    settings.get_theme()["fonts"]["diff-unique-2"]["color"],
                    5,
                )
            elif message_type == constants.MessageType.DIFF_SIMILAR:
                style_repl_text(
                    start,
                    end,
                    settings.get_theme()["fonts"]["diff-similar"]["color"],
                    6,
                )
        else:
            # Add REPL message to the REPL message tab
            parent.repl_messages_tab.append("{}\n".format(message))

        rmt = parent.repl_messages_tab
        if qt.sip.isdeleted(rmt):
            return
        if qt.sip.isdeleted(rmt._parent):
            return
        # Bring the REPL tab to the front
        if focus_repl_messages == True:

            def focus_repl() -> None:
                if qt.sip.isdeleted(rmt):
                    return
                if qt.sip.isdeleted(rmt._parent):
                    return
                rmt._parent.setCurrentWidget(parent.repl_messages_tab)

            qt.QTimer.singleShot(0, focus_repl)

        # Bring cursor to the current message
        if scroll_to_end == True:

            def scroll_to_end() -> None:
                if qt.sip.isdeleted(rmt):
                    return
                if qt.sip.isdeleted(rmt._parent):
                    return
                if parent.repl_messages_tab is None:
                    return
                rmt.setCursorPosition(parent.repl_messages_tab.lines(), 0)
                rmt.setFirstVisibleLine(parent.repl_messages_tab.lines())

            qt.QTimer.singleShot(1, scroll_to_end)

    def repl_scroll_to_bottom(self) -> None:
        """Scroll the REPL MESSAGES tab to the bottom"""
        # Find the "REPL Message" tab in the basic widgets
        self._parent.repl_messages_tab = self.find_repl_messages_tab()
        if self._parent.repl_messages_tab is not None:
            self._parent.repl_messages_tab.goto_line(self._parent.repl_messages_tab.lines())

    def repl_clear_tab(self) -> None:
        """Clear text from the REPL messages tab"""
        # Find the "REPL Message" tab in the basic widgets
        self._parent.repl_messages_tab = self.find_repl_messages_tab()
        # Check if REPL messages tab exists
        if self._parent.repl_messages_tab is not None:
            self._parent.repl_messages_tab.setText("")
            self._parent.repl_messages_tab.SendScintilla(qt.QsciScintillaBase.SCI_STYLECLEARALL)
            self._parent.repl_messages_tab.set_theme(settings.get_theme())
            # Bring the REPL tab to the front
            self._parent.repl_messages_tab._parent.setCurrentWidget(self._parent.repl_messages_tab)

    def find_repl_messages_tab(self) -> Any:
        """Find the "REPL Message" tab in the basic widgets of the MainForm"""
        # Call the MainForm function to find the repl tab by name
        self._parent.repl_messages_tab = self._parent.get_tab_by_name(
            constants.SpecialTabNames.Messages.value
        )
        return self._parent.repl_messages_tab

    def show_nodes(self, custom_editor: Optional[CustomEditor], parser: str) -> None:
        """
        Function for selecting which type of node tree will be displayed
        """
        if self.node_view_type == constants.NodeDisplayType.DOCUMENT:
            self.show_nodes_in_document(custom_editor, parser)
        elif self.node_view_type == constants.NodeDisplayType.TREE:
            self.show_nodes_in_tree(custom_editor, parser)

    def show_nodes_in_tree(self, custom_editor: Optional[CustomEditor], parser: str) -> None:
        """
        Show the node tree of a parsed file in a "NODE TREE" tree
        display widget in the upper window
        """
        # Define references directly to the parent and mainform for performance and clarity
        parent = self._parent
        # Check if the custom editor is valid
        if custom_editor is None:
            parent.display.repl_display_message(
                "No document selected for node tree creation!",
                message_type=constants.MessageType.ERROR,
            )
            parent.display.write_to_statusbar("No document selected for node tree creation!", 5000)
            return
        # Check if the document type is valid for node tree parsing
        valid_parsers = [
            "PYTHON",
            "C",
            "C++",
            "D",
            "NIM",
            "PASCAL",
            "PHP",
            "JAVASCRIPT",
            "ASSEMBLY",
            "MAKEFILE",
            "HTML",
            "JSON",
        ]
        if not (parser in valid_parsers):
            parsers = ", ".join((x.title() for x in valid_parsers))
            message = "Document type is not in ({}),\nbut is of type '{}'!".format(parsers, parser)
            parent.display.repl_display_message(message, message_type=constants.MessageType.ERROR)
            parent.display.write_to_statusbar(message, 5000)
            return
        # Define a name for the NODE tab
        node_tree_tab_name = "NODE TREE/LIST"
        # Find the "NODE TREE/LIST" tab in the basic widgets
        parent.node_tree_tab = parent.get_tab_by_name(node_tree_tab_name)
        if parent.node_tree_tab:
            parent.node_tree_tab._parent.close_tab(node_tree_tab_name)
        # Create a new NODE tab in the upper basic widget and set its icon
        parent.node_tree_tab = parent.get_helper_window().tree_add_tab(node_tree_tab_name)
        parent.node_tree_tab.current_icon = self.node_tree_icon
        node_tree_tab = parent.node_tree_tab
        node_tree_tab_index = node_tree_tab._parent.indexOf(node_tree_tab)
        node_tree_tab._parent.setTabIcon(node_tree_tab_index, self.node_tree_icon)
        # Connect the editor destruction signal to the tree display
        custom_editor.destroyed.connect(node_tree_tab.parent_destroyed)
        # Focus the node tree tab
        parent.node_tree_tab._parent.setCurrentWidget(parent.node_tree_tab)
        # Display the nodes according to file type
        if parser == "PYTHON":
            # Get all the file information
            try:
                python_node_tree = functions.get_python_node_tree(custom_editor.text())
                parser_error = False
            except Exception as ex:
                # Exception, probably an error in the file's syntax
                python_node_tree = []
                parser_error = ex
            # Display the information in the tree tab
            parent.node_tree_tab.display_python_nodes_in_tree(
                custom_editor, python_node_tree, parser_error
            )
            new_keywords = [x.name for x in python_node_tree if x.type == "import"]
            new_keywords.extend([x.name for x in python_node_tree if x.type == "class"])
            new_keywords.extend([x.name for x in python_node_tree if x.type == "function"])
            new_keywords.extend([x.name for x in python_node_tree if x.type == "global_variable"])
            if lexers.nim_lexers_found == True:
                custom_editor.set_lexer(
                    lexers.CustomPython(custom_editor, additional_keywords=new_keywords),
                    "PYTHON",
                )
        elif parser == "NIM":
            import components.codequality

            #                # Get all the file information
            #                nim_nodes = functions.get_nim_node_tree(custom_editor.text())
            #                # Display the information in the tree tab
            #                parent.node_tree_tab.display_nim_nodes(custom_editor, nim_nodes)
            # Get all the file information
            nim_nodes = components.codequality.parse_nim_file(custom_editor.save_path)
            # Display the information in the tree tab
            parent.node_tree_tab.display_nim_nodes_new(custom_editor, nim_nodes)
        elif parser in (
            "C",
            "C++",
            "D",
            "PASCAL",
            "PHP",
            "JAVASCRIPT",
            "MAKEFILE",
            "HTML",
        ):
            # Get all the file information
            try:
                icons = {
                    "C": functions.create_icon("language_icons/logo_c.png"),
                    "C++": functions.create_icon("language_icons/logo_cpp.png"),
                    "D": functions.create_icon("language_icons/logo_d.png"),
                    "PASCAL": functions.create_icon("language_icons/logo_pascal.png"),
                    "PHP": functions.create_icon("language_icons/logo_php.png"),
                    "JAVASCRIPT": functions.create_icon("language_icons/logo_javascript.png"),
                    "ASSEMBLY": functions.create_icon("various/node_unknown.png"),
                    "MAKEFILE": functions.create_icon("various/node_unknown.png"),
                    "HTML": functions.create_icon("language_icons/logo_html.png"),
                }
                result = functions.get_node_tree_with_ctags(
                    custom_editor.text(),
                    parser,
                )
            except:
                parent.display.repl_display_error(traceback.format_exc())
                return
            # Display the information in the tree tab
            parent.node_tree_tab.display_nodes(
                custom_editor,
                result,
                icons[parser],
            )

    def show_nodes_in_document(self, custom_editor: Optional[CustomEditor], parser: str) -> None:
        """
        Show the node tree of a parsed file in a "NODE TREE" Scintilla
        document in the upper window
        """
        # Define references directly to the parent and
        # mainform for performance and clarity
        parent = self._parent
        # Check if the custom editor is valid
        if custom_editor is None:
            parent.display.repl_display_message(
                "No document selected for node tree creation!",
                message_type=constants.MessageType.ERROR,
            )
            parent.display.write_to_statusbar("No document selected for node tree creation!", 5000)
            return
        # Check if the document type is Python or C
        if parser != "PYTHON" and parser != "C":
            parent.display.repl_display_message(
                "Document is not Python or C!",
                message_type=constants.MessageType.ERROR,
            )
            parent.display.write_to_statusbar("Document is not Python or C", 5000)
            return

        # Nested hotspot function
        def create_hotspot(node_tab: Any) -> None:
            # Create the hotspot boundaries
            hotspot_line = node_tab.lines() - 2
            hotspot_first_ch = node_tab.text(hotspot_line).index("-")
            hotspot_line_length = node_tab.lineLength(hotspot_line)
            hotspot_start = node_tab.positionFromLineIndex(hotspot_line, hotspot_first_ch)
            hotspot_end = node_tab.positionFromLineIndex(hotspot_line, hotspot_line_length)
            hotspot_length = hotspot_end - hotspot_start
            # Style the hotspot on the node tab
            node_tab.hotspots.style(node_tab, hotspot_start, hotspot_length, color=0xFF0000)

        # Create the function and connect the hotspot release signal to it
        def hotspot_release(position: int, modifiers: int) -> None:
            # Get the line and index at where the hotspot was clicked
            line, index = parent.node_tree_tab.lineIndexFromPosition(position)
            # Get the document name and focus on the tab with the document
            document_name = re.search(r"DOCUMENT\:\s*(.*)\n", parent.node_tree_tab.text(0)).group(1)
            goto_line_number = int(
                re.search(r".*\(line\:(\d+)\).*", parent.node_tree_tab.text(line)).group(1)
            )
            # Find the document, set focus to it and go to the line the hotspot points to
            document_tab = parent.get_tab_by_name(document_name)
            # Check if the document was modified
            if document_tab is None:
                # Then it has stars(*) in the name
                document_tab = parent.get_tab_by_name("*{}*".format(document_name))
            try:
                document_tab._parent.setCurrentWidget(document_tab)
                document_tab.goto_line(goto_line_number)
            except:
                return

        # Define a name for the NODE tab
        node_tree_tab_name = "NODE TREE/LIST"
        # Find the "NODE" tab in the basic widgets
        parent.node_tree_tab = parent.get_tab_by_name(node_tree_tab_name)
        if parent.node_tree_tab:
            parent.node_tree_tab._parent.close_tab(node_tree_tab_name)
        # Create a new NODE tab in the upper basic widget
        parent.node_tree_tab = parent.get_helper_window().plain_add_document(node_tree_tab_name)
        parent.node_tree_tab.current_icon = self.node_tree_icon
        # Set the NODE document to be ReadOnly
        parent.node_tree_tab.setReadOnly(True)
        parent.node_tree_tab.setText("")
        parent.node_tree_tab.SendScintilla(qt.QsciScintillaBase.SCI_STYLECLEARALL)
        parent.node_tree_tab.parentWidget().setCurrentWidget(parent.node_tree_tab)
        # Check if the custom editor is valid
        if isinstance(custom_editor, CustomEditor) == False:
            message = "The editor is not valid!"
            parent.display.repl_display_message(message, message_type=constants.MessageType.ERROR)
            parent.display.write_to_statusbar(message, 2000)
            return
        else:
            # Check the type of document in the custom editor
            parser = custom_editor.current_file_type
        # Get the node tree for the current widget in the custom editor
        if parser == "PYTHON":
            import_nodes, class_tree_nodes, function_nodes, global_vars = (
                functions.get_python_node_list(custom_editor.text())
            )
            init_space = "    -"
            extra_space = "     "
            # Display document name, used for finding the tab when clicking the hotspot
            document_name = os.path.basename(custom_editor.save_path)
            document_text = "DOCUMENT: {}\n".format(document_name)
            parent.node_tree_tab.append(document_text)
            parent.node_tree_tab.append("TYPE: {}\n\n".format(parser))
            # Display class nodes
            parent.node_tree_tab.append("CLASS/METHOD TREE:\n")
            for node in class_tree_nodes:
                node_text = init_space + str(node[0].name) + "(line:"
                node_text += str(node[0].lineno) + ")\n"
                parent.node_tree_tab.append(node_text)
                create_hotspot(parent.node_tree_tab)
                for child in node[1]:
                    child_text = (child[0] + 1) * extra_space + init_space
                    child_text += str(child[1].name) + "(line:"
                    child_text += str(child[1].lineno) + ")\n"
                    parent.node_tree_tab.append(child_text)
                    create_hotspot(parent.node_tree_tab)
                parent.node_tree_tab.append("\n")
            # Check if there were any nodes found
            if class_tree_nodes == []:
                parent.node_tree_tab.append("No classes found\n\n")
            # Display function nodes
            parent.node_tree_tab.append("FUNCTIONS:\n")
            for func in function_nodes:
                func_text = init_space + func.name + "(line:"
                func_text += str(func.lineno) + ")\n"
                parent.node_tree_tab.append(func_text)
                create_hotspot(parent.node_tree_tab)
            # Check if there were any nodes found
            if function_nodes == []:
                parent.node_tree_tab.append("No functions found\n\n")
            # Connect the hotspot mouserelease signal
            parent.node_tree_tab.SCN_HOTSPOTRELEASECLICK.connect(hotspot_release)
        elif parser == "C":
            function_nodes = functions.get_c_function_list(custom_editor.text())
            init_space = "    -"
            extra_space = "     "
            # Display document name, used for finding the tab when clicking the hotspot
            document_name = os.path.basename(custom_editor.save_path)
            document_text = "DOCUMENT: {}\n".format(document_name)
            parent.node_tree_tab.append(document_text)
            parent.node_tree_tab.append("TYPE: {}\n\n".format(parser))
            # Display functions
            parent.node_tree_tab.append("FUNCTION LIST:\n")
            for func in function_nodes:
                node_text = init_space + func[0] + extra_space
                node_text += "(line:" + str(func[1]) + ")\n"
                parent.node_tree_tab.append(node_text)
                create_hotspot(parent.node_tree_tab)
            # Check if there were any nodes found
            if function_nodes == []:
                parent.node_tree_tab.append("No functions found\n\n")
            # Connect the hotspot mouserelease signal
            parent.node_tree_tab.SCN_HOTSPOTRELEASECLICK.connect(hotspot_release)

    def show_found_files(self, search_text: str, file_list: List[str], directory: str) -> None:
        """
        Function for selecting which type of node tree will be displayed
        """
        if self.node_view_type == constants.NodeDisplayType.DOCUMENT:
            self.show_found_files_in_document(file_list, directory)
        elif self.node_view_type == constants.NodeDisplayType.TREE:
            self.show_found_files_in_tree(search_text, file_list, directory)

    def show_found_files_in_document(self, file_list: List[str], directory: str) -> None:
        """
        Display the found files returned from the find_files system function
        in the REPL MESSAGES tab
        """
        # Create lines that will be displayed in the REPL messages window
        display_file_info = []
        for file in file_list:
            display_file_info.append("{} ({})".format(os.path.basename(file), file))
        # Display all found files
        self._parent.display.repl_display_message("Found {:d} files:".format(len(file_list)))

        # Use scintilla HOTSPOTS to create clickable file links
        # Create the function and connect the hotspot release signal to it
        def hotspot_release(position: int, modifiers: int) -> None:
            # Get the line and index at where the hotspot was clicked
            line, index = self._parent.repl_messages_tab.lineIndexFromPosition(position)
            file = (
                re.search(r".*\((.*)\)", self._parent.repl_messages_tab.text(line))
                .group(1)
                .replace("\n", "")
            )
            # Open the files
            self._parent.open_file(file, self._parent.get_largest_window())
            # Because open_file updates the new CWD in the REPL MESSAGES,
            # it is needed to set the cursor back to where the hotspot was clicked
            self._parent.repl_messages_tab.setCursorPosition(line, index)

        self._parent.repl_messages_tab.SCN_HOTSPOTRELEASECLICK.connect(hotspot_release)
        # Get the start position
        pos = self._parent.repl_messages_tab.getCursorPosition()
        hotspot_start = self._parent.repl_messages_tab.positionFromLineIndex(pos[0], pos[1])
        # self.display.repl_display_message("\n".join(found_files))
        self._parent.display.repl_display_message("\n".join(display_file_info))
        # Get the end position
        pos = self._parent.repl_messages_tab.getCursorPosition()
        hotspot_end = self._parent.repl_messages_tab.positionFromLineIndex(pos[0], pos[1])
        # Style the hotspot on the node tab
        self._parent.repl_messages_tab.hotspots.style(
            self._parent.repl_messages_tab,
            hotspot_start,
            hotspot_end,
            color=0xFF0000,
        )

    def show_directory_tree(self, directory: str) -> None:
        """
        Display the directory information in a TreeDisplay widget
        """
        # Define references directly to the parent and mainform for performance and clarity
        parent = self._parent
        # Define a name for the FOUND FILES tab
        found_files_tab_name = "FILE/DIRECTORY TREE"
        # Find the "FILE/DIRECTORY TREE" tab in the basic widgets
        parent.found_files_tab = parent.get_tab_by_name(found_files_tab_name)
        if parent.found_files_tab:
            parent.found_files_tab._parent.close_tab(found_files_tab_name)
        # Create a new FOUND FILES tab in the upper basic widget
        found_files_tab = parent.get_helper_window().tree_add_tab(found_files_tab_name)
        found_files_tab.internals.set_icon(found_files_tab, self.system_show_cwd_tree_icon)
        # Focus the node tree tab
        found_files_tab._parent.setCurrentWidget(found_files_tab)
        # Display the directory information in the tree tab
        found_files_tab.display_directory_tree(directory)

    def show_found_files_in_tree(
        self, search_text: str, file_list: List[str], directory: str
    ) -> None:
        """
        Display the found files returned from the find_files system function
        in a TreeDisplay widget
        """
        # Define references directly to the parent and mainform for performance and clarity
        parent = self._parent
        # Define a name for the FOUND FILES tab
        found_files_tab_name = "FOUND FILES"
        # Find the "FOUND FILES" tab in the basic widgets
        parent.found_files_tab = parent.get_tab_by_name(found_files_tab_name)
        if parent.found_files_tab:
            parent.found_files_tab._parent.close_tab(found_files_tab_name)
        found_files_tab = parent.found_files_tab
        # Create a new FOUND FILES tab in the upper basic widget
        found_files_tab = parent.get_helper_window().tree_add_tab(found_files_tab_name)
        found_files_tab.internals.set_icon(found_files_tab, self.system_found_files_icon)
        # Focus the node tree tab
        found_files_tab._parent.setCurrentWidget(found_files_tab)
        # Display the found files information in the tree tab
        found_files_tab.display_found_files(search_text, file_list, directory)

    def show_found_files_with_lines_in_tree(
        self,
        search_title: str,
        search_text: str,
        search_dir: str,
        case_sensitive: bool,
        search_subdirs: bool,
        break_on_find: bool,
        file_filter: str,
    ) -> None:
        """
        Display the found files with line information returned from the
        find_in_files and replace_in_files system function in a TreeDisplay
        """
        # Define references directly to the parent and mainform for performance and clarity
        parent = self._parent
        # Define a name for the FOUND FILES tab
        found_files_tab_name = "FOUND FILES"
        # Find the FOUND FILES tab in the basic widgets
        parent.found_files_tab = parent.get_tab_by_name(found_files_tab_name)
        if parent.found_files_tab:
            parent.found_files_tab._parent.close_tab(found_files_tab_name)
        found_files_tab = parent.found_files_tab
        # Create a new FOUND FILES tab in the upper basic widget
        found_files_tab = parent.get_helper_window().tree_add_tab(found_files_tab_name)
        found_files_tab.internals.set_icon(found_files_tab, self.system_found_files_icon)
        # Focus the node tree tab
        found_files_tab._parent.setCurrentWidget(found_files_tab)
        # Display the found files information in the tree tab
        found_files_tab.display_found_files_with_lines(
            search_title,
            search_text,
            search_dir,
            case_sensitive,
            search_subdirs,
            break_on_find,
            file_filter,
        )

    def show_replaced_text_in_files_in_tree(
        self, search_text: str, replace_text: str, file_list: List[str], directory: str
    ) -> None:
        """
        Display the found files with line information returned from the
        find_in_files and replace_in_files system function in a TreeDisplay
        """
        # Define references directly to the parent and mainform for performance and clarity
        parent = self._parent
        # Define a name for the FOUND FILES tab
        found_files_tab_name = "REPLACEMENTS IN FILES"
        # Find the FOUND FILES tab in the basic widgets
        parent.found_files_tab = parent.get_tab_by_name(found_files_tab_name)
        if parent.found_files_tab:
            parent.found_files_tab._parent.close_tab(found_files_tab_name)
        # Create a new FOUND FILES tab in the upper basic widget
        parent.found_files_tab = parent.get_helper_window().tree_add_tab(found_files_tab_name)
        parent.found_files_tab.internals.set_icon(
            parent.found_files_tab, self.system_replace_in_files_icon
        )
        # Focus the node tree tab
        parent.found_files_tab._parent.setCurrentWidget(parent.found_files_tab)
        # Display the found files information in the tree tab
        parent.found_files_tab.display_replacements_in_files(
            search_text, replace_text, file_list, directory
        )

    def show_text_difference(
        self,
        text_1: str,
        text_2: str,
        text_name_1: Optional[str] = None,
        text_name_2: Optional[str] = None,
        text_path_1: Optional[str] = None,
        text_path_2: Optional[str] = None,
    ) -> None:
        """
        Display the difference between two texts in a TextDiffer
        """
        # Check if text names are valid
        if text_name_1 is None:
            text_name_1 = "TEXT 1"
        if text_name_2 is None:
            text_name_2 = "TEXT 2"
        # Create a reference to the main form for less typing
        parent = self._parent
        largest_window = parent.get_largest_window()
        # Create and initialize a text differ
        text_differ = TextDiffer(
            largest_window,
            parent,
            text_1,
            text_2,
            text_name_1,
            text_name_2,
            text_path_1,
            text_path_2,
        )
        # Find the "DIFF(...)" tab in the basic widgets and close it
        diff_tab_string = "DIFF("
        diff_tab = parent.get_tab_by_string_in_name(diff_tab_string)
        if diff_tab:
            diff_tab_index = diff_tab._parent.indexOf(diff_tab)
            diff_tab._parent.close_tab(diff_tab_index)
        # Add the created text differ to the main window
        diff_index = largest_window.addTab(
            text_differ, "DIFF({} / {})".format(text_name_1, text_name_2)
        )
        # Set focus to the text differ tab
        largest_window.setCurrentIndex(diff_index)

    def show_session_editor(self) -> None:
        """Display a window for editing sessions"""
        # Create the SessionGuiManipulator
        sessions_manipulator = SessionGuiManipulator(self._parent.get_helper_window(), self._parent)
        # Find the old "SESSIONS" tab in the basic widgets and close it
        sessions_tab_name = "SESSIONS"
        sessions_tab = self._parent.get_tab_by_name(sessions_tab_name)
        if sessions_tab:
            sessions_tab._parent.close_tab(sessions_tab_name)
        # Show the sessions in the manipulator
        sessions_manipulator.show_sessions()
        # Add the created session manipulator to the upper window
        sm_index = self._parent.get_helper_window().addTab(sessions_manipulator, "SESSIONS")
        # Set focus to the text differ tab
        self._parent.get_helper_window().setCurrentIndex(sm_index)

    def show_path_editor(self) -> None:
        """Display a tab for editing the PATH environment variable"""
        # Create the SystemPathManipulator
        path_manipulator = SystemPathManipulator(
            self._parent.get_helper_window(), self._parent
        )
        # Find the old "PATH" tab in the basic widgets and close it
        path_tab_name = SystemPathManipulator.TAB_NAME
        path_tab = self._parent.get_tab_by_name(path_tab_name)
        if path_tab:
            path_tab._parent.close_tab(path_tab_name)
        # Add the created path manipulator to the helper window
        path_icon = functions.create_icon("tango_icons/settings.png")
        path_index = self._parent.get_helper_window().addTab(path_manipulator, path_icon, path_tab_name)
        # Set focus to the path editor tab
        self._parent.get_helper_window().setCurrentIndex(path_index)

    def create_lexers_menu(
        self,
        menu_name: str,
        set_lexer_func: Any,
        store_menu_to_mainform: bool = True,
        custom_parent: Any = None,
    ) -> Menu:
        """
        Create a lexer menu. Currently used in the View menu and
        the CustomEditor tab menu.
        Parameter set_lexer_func has to have:
            - parameter lexer: a lexers.Lexer object
            - parameter lexer_name: a string
        """
        set_lexer = set_lexer_func

        # Nested function for creating an action
        def create_action(
            name: str, key_combo: Any, status_tip: str, icon: Any, function: Any, menu_parent: Any
        ) -> qt.QAction:
            action = qt.QAction(name, menu_parent)
            # Key combination
            if key_combo is not None and key_combo != "" and key_combo != []:
                if isinstance(key_combo, list):
                    action.setShortcuts(key_combo)
                else:
                    action.setShortcut(key_combo)
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
            self._parent.menubar_functions[function.__name__] = function
            # Check if there is a tab character in the function
            # name and remove the part of the string after it
            if "\t" in name:
                name = name[: name.find("\t")]
            # Add the action to the context menu
            # function list in the helper forms module
            gui.contextmenu.add_function(function.__name__, action.pixmap, function, name)
            # Enable/disable action according to passed
            # parameter and return the action
            action.setEnabled(True)
            return action

        # The owner of the lexers menu is always the MainWindow
        if custom_parent is not None:
            parent = custom_parent
        else:
            parent = self._parent
        lexers_menu = Menu(menu_name, parent)

        def create_lexer(lexer: Any, description: str) -> Any:
            func = functools.partial(set_lexer, lexer, description)
            func.__name__ = "set_lexer_{}".format(lexer.__name__)
            return func

        NONE_action = create_action(
            "No lexer",
            None,
            "Disable document lexer",
            "tango_icons/file.png",
            create_lexer(lexers.Text, "Plain text"),
            lexers_menu,
        )
        ADA_action = create_action(
            "Ada",
            None,
            "Change document lexer to: Ada",
            "language_icons/logo_ada.png",
            create_lexer(lexers.Ada, "Ada"),
            lexers_menu,
        )
        AWK_action = create_action(
            "AWK",
            None,
            "Change document lexer to: AWK",
            "language_icons/logo_awk.png",
            create_lexer(lexers.AWK, "AWK"),
            lexers_menu,
        )
        BASH_action = create_action(
            "Bash",
            None,
            "Change document lexer to: Bash",
            "language_icons/logo_bash.png",
            create_lexer(lexers.Bash, "Bash"),
            lexers_menu,
        )
        BATCH_action = create_action(
            "Batch",
            None,
            "Change document lexer to: Batch",
            "language_icons/logo_batch.png",
            create_lexer(lexers.Batch, "Batch"),
            lexers_menu,
        )
        CMAKE_action = create_action(
            "CMake",
            None,
            "Change document lexer to: CMake",
            "language_icons/logo_cmake.png",
            create_lexer(lexers.CMake, "CMake"),
            lexers_menu,
        )
        C_CPP_action = create_action(
            "C / C++",
            None,
            "Change document lexer to: C / C++",
            "language_icons/logo_c_cpp.png",
            create_lexer(lexers.CPP, "C / C++"),
            lexers_menu,
        )
        CSS_action = create_action(
            "CSS",
            None,
            "Change document lexer to: CSS",
            "language_icons/logo_css.png",
            create_lexer(lexers.CSS, "CSS"),
            lexers_menu,
        )
        D_action = create_action(
            "D",
            None,
            "Change document lexer to: D",
            "language_icons/logo_d.png",
            create_lexer(lexers.D, "D"),
            lexers_menu,
        )
        FORTRAN_action = create_action(
            "Fortran",
            None,
            "Change document lexer to: Fortran",
            "language_icons/logo_fortran.png",
            create_lexer(lexers.Fortran, "Fortran"),
            lexers_menu,
        )
        HTML_action = create_action(
            "HTML",
            None,
            "Change document lexer to: HTML",
            "language_icons/logo_html.png",
            create_lexer(lexers.HTML, "HTML"),
            lexers_menu,
        )
        LUA_action = create_action(
            "Lua",
            None,
            "Change document lexer to: Lua",
            "language_icons/logo_lua.png",
            create_lexer(lexers.Lua, "Lua"),
            lexers_menu,
        )
        MAKEFILE_action = create_action(
            "MakeFile",
            None,
            "Change document lexer to: MakeFile",
            "language_icons/logo_makefile.png",
            create_lexer(lexers.Makefile, "MakeFile"),
            lexers_menu,
        )
        MATLAB_action = create_action(
            "Matlab",
            None,
            "Change document lexer to: Matlab",
            "language_icons/logo_matlab.png",
            create_lexer(lexers.Matlab, "Matlab"),
            lexers_menu,
        )
        Markdown_action = create_action(
            "Markdown",
            None,
            "Change document lexer to: Markdown",
            "tango_icons/markdown.png",
            create_lexer(lexers.Markdown, "Markdown"),
            lexers_menu,
        )
        NIM_action = create_action(
            "Nim",
            None,
            "Change document lexer to: Nim",
            "language_icons/logo_nim.png",
            create_lexer(lexers.Nim, "Nim"),
            lexers_menu,
        )
        OBERON_action = create_action(
            "Oberon / Modula",
            None,
            "Change document lexer to: Oberon / Modula",
            "language_icons/logo_oberon.png",
            create_lexer(lexers.Oberon, "Oberon / Modula"),
            lexers_menu,
        )
        PASCAL_action = create_action(
            "Pascal",
            None,
            "Change document lexer to: Pascal",
            "language_icons/logo_pascal.png",
            create_lexer(lexers.Pascal, "Pascal"),
            lexers_menu,
        )
        PERL_action = create_action(
            "Perl",
            None,
            "Change document lexer to: Perl",
            "language_icons/logo_perl.png",
            create_lexer(lexers.Perl, "Perl"),
            lexers_menu,
        )
        PYTHON_action = create_action(
            "Python",
            None,
            "Change document lexer to: Python",
            "language_icons/logo_python.png",
            create_lexer(lexers.Python, "Python"),
            lexers_menu,
        )
        RUBY_action = create_action(
            "Ruby",
            None,
            "Change document lexer to: Ruby",
            "language_icons/logo_ruby.png",
            create_lexer(lexers.Ruby, "Ruby"),
            lexers_menu,
        )
        ROUTEROS_action = create_action(
            "RouterOS",
            None,
            "Change document lexer to: RouterOS",
            "language_icons/logo_routeros.png",
            create_lexer(lexers.RouterOS, "RouterOS"),
            lexers_menu,
        )
        Spice_action = create_action(
            "Spice",
            None,
            "Change document lexer to: Spice",
            "language_icons/logo_spice.png",
            create_lexer(lexers.Spice, "Spice"),
            lexers_menu,
        )
        SQL_action = create_action(
            "SQL",
            None,
            "Change document lexer to: SQL",
            "language_icons/logo_sql.png",
            create_lexer(lexers.SQL, "SQL"),
            lexers_menu,
        )
        TCL_action = create_action(
            "TCL",
            None,
            "Change document lexer to: TCL",
            "language_icons/logo_tcl.png",
            create_lexer(lexers.TCL, "TCL"),
            lexers_menu,
        )
        TEX_action = create_action(
            "TeX",
            None,
            "Change document lexer to: TeX",
            "language_icons/logo_tex.png",
            create_lexer(lexers.TeX, "TeX"),
            lexers_menu,
        )
        VERILOG_action = create_action(
            "Verilog",
            None,
            "Change document lexer to: Verilog",
            "language_icons/logo_verilog.png",
            create_lexer(lexers.Verilog, "Verilog"),
            lexers_menu,
        )
        VHDL_action = create_action(
            "VHDL",
            None,
            "Change document lexer to: VHDL",
            "language_icons/logo_vhdl.png",
            create_lexer(lexers.VHDL, "VHDL"),
            lexers_menu,
        )
        XML_action = create_action(
            "XML",
            None,
            "Change document lexer to: XML",
            "language_icons/logo_xml.png",
            create_lexer(lexers.XML, "XML"),
            lexers_menu,
        )
        YAML_action = create_action(
            "YAML",
            None,
            "Change document lexer to: YAML",
            "language_icons/logo_yaml.png",
            create_lexer(lexers.YAML, "YAML"),
            lexers_menu,
        )
        Zig_action = create_action(
            "Zig",
            None,
            "Change document lexer to: Zig",
            "language_icons/logo_zig.png",
            create_lexer(lexers.Zig, "Zig"),
            lexers_menu,
        )
        CSharp_action = create_action(
            "C#",
            None,
            "Change document lexer to: C#",
            "language_icons/logo_csharp.png",
            create_lexer(lexers.CPP, "C#"),
            lexers_menu,
        )
        Java_action = create_action(
            "Java",
            None,
            "Change document lexer to: Java",
            "language_icons/logo_java.png",
            create_lexer(lexers.Java, "Java"),
            lexers_menu,
        )
        JavaScript_action = create_action(
            "JavaScript",
            None,
            "Change document lexer to: JavaScript",
            "language_icons/logo_javascript.png",
            create_lexer(lexers.JavaScript, "JavaScript"),
            lexers_menu,
        )
        Octave_action = create_action(
            "Octave",
            None,
            "Change document lexer to: Octave",
            "language_icons/logo_octave.png",
            create_lexer(lexers.Octave, "Octave"),
            lexers_menu,
        )
        PostScript_action = create_action(
            "PostScript",
            None,
            "Change document lexer to: PostScript",
            "language_icons/logo_postscript.png",
            create_lexer(lexers.PostScript, "PostScript"),
            lexers_menu,
        )
        Fortran77_action = create_action(
            "Fortran77",
            None,
            "Change document lexer to: Fortran77",
            "language_icons/logo_fortran77.png",
            create_lexer(lexers.Fortran77, "Fortran77"),
            lexers_menu,
        )
        IDL_action = create_action(
            "IDL",
            None,
            "Change document lexer to: IDL",
            "language_icons/logo_idl.png",
            create_lexer(lexers.IDL, "IDL"),
            lexers_menu,
        )
        cicode_action = create_action(
            "CiCode",
            None,
            "Change document lexer to: CiCode",
            "language_icons/logo_cicode.png",
            create_lexer(lexers.CiCode, "CiCode"),
            lexers_menu,
        )
        json_action = create_action(
            "JSON",
            None,
            "Change document lexer to: JSON",
            "language_icons/logo_json.png",
            create_lexer(lexers.JSON, "JSON"),
            lexers_menu,
        )
        lexers_menu.addAction(NONE_action)
        lexers_menu.addSeparator()
        lexers_menu.addAction(ADA_action)
        lexers_menu.addAction(AWK_action)
        lexers_menu.addAction(BASH_action)
        lexers_menu.addAction(BATCH_action)
        lexers_menu.addAction(CMAKE_action)
        lexers_menu.addAction(C_CPP_action)
        lexers_menu.addAction(cicode_action)
        lexers_menu.addAction(CSharp_action)
        lexers_menu.addAction(CSS_action)
        lexers_menu.addAction(D_action)
        lexers_menu.addAction(Fortran77_action)
        lexers_menu.addAction(FORTRAN_action)
        lexers_menu.addAction(HTML_action)
        lexers_menu.addAction(IDL_action)
        lexers_menu.addAction(Java_action)
        lexers_menu.addAction(JavaScript_action)
        lexers_menu.addAction(json_action)
        lexers_menu.addAction(LUA_action)
        lexers_menu.addAction(MAKEFILE_action)
        lexers_menu.addAction(MATLAB_action)
        lexers_menu.addAction(Markdown_action)
        lexers_menu.addAction(NIM_action)
        lexers_menu.addAction(OBERON_action)
        lexers_menu.addAction(Octave_action)
        lexers_menu.addAction(PASCAL_action)
        lexers_menu.addAction(PERL_action)
        lexers_menu.addAction(PostScript_action)
        lexers_menu.addAction(PYTHON_action)
        lexers_menu.addAction(RUBY_action)
        lexers_menu.addAction(ROUTEROS_action)
        lexers_menu.addAction(Spice_action)
        lexers_menu.addAction(SQL_action)
        lexers_menu.addAction(TCL_action)
        lexers_menu.addAction(TEX_action)
        lexers_menu.addAction(VERILOG_action)
        lexers_menu.addAction(VHDL_action)
        lexers_menu.addAction(XML_action)
        lexers_menu.addAction(YAML_action)
        lexers_menu.addAction(Zig_action)
        # Clean-up the stored menus
        """
        This is needed only because the lexer menu is created on the fly!
        If this clean-up is ommited, then try clicking the CustomEditor lexer
        menu button 20x times and watch the memory usage ballon up!
        """
        for i in range(len(self.stored_menus)):
            # Delete the QObjects by setting it's parent to None
            for l in self.stored_menus[i].actions():
                l.setParent(None)
            self.stored_menus[i].setParent(None)
        self.stored_menus = []
        # Add the newly created menu to the internal list for future cleaning
        if store_menu_to_mainform == True:
            self.stored_menus.append(lexers_menu)
        # Return the created menu
        return lexers_menu

    """
    Docking overlay
    """

    def docking_overlay_show(self) -> None:
        functions.process_events(1, delay=0.01)
        parent = self._parent
        docking_overlay = parent.docking_overlay
        if docking_overlay is not None:
            window_list = parent.get_all_windows()
            docking_overlay.show_on_parent(window_list)

    def docking_overlay_hide(self) -> None:
        functions.process_events(1, delay=0.01)
        parent = self._parent
        if parent.docking_overlay is not None:
            parent.docking_overlay.hide()
