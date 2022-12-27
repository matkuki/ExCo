
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2019 Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import os
import os.path
import collections
import traceback
import ast
import inspect
import math
import functools
import textwrap
import difflib
import re
import time
import settings
import functions
import data
import components
import themes
import pprint
import subprocess

from .dialogs import *
from .menu import *

"""
----------------------------------------------------------------------------
Object for displaying various results in a tree structure
----------------------------------------------------------------------------
"""
class TreeDisplay(data.QTreeView):
    #Class custom objects/types
    class Directory():
        """
        Object for holding directory/file information when building directory trees
        """
        item        = None
        directories = None
        files       = None
        
        def __init__(self, input_item):
            """Initialization"""
            self.item = input_item
            self.directories = {}
            self.files = {}
        
        def add_directory(self, dir_name, dir_item):
            # Create a new instance of Directory class using the __class__ dunder method
            new_directory = self.__class__(dir_item)
            # Add the new directory to the dictionary
            self.directories[dir_name] = new_directory
            # Add the new directory item to the parent(self)
            self.item.appendRow(dir_item)
            # Return the directory object reference
            return new_directory
        
        def add_file(self, file_name, file_item):
            self.files[file_name] = file_item
            # Add the new file item to the parent(self)
            self.item.appendRow(file_item)
    
    # Class variables
    parent                  = None
    main_form               = None
    name                    = ""
    savable                 = data.CanSave.NO
    current_icon            = None
    icon_manipulator        = None
    tree_display_type       = None
    tree_menu               = None
    bound_tab               = None
    worker_thread           = None
    # Attributes specific to the display data
    bound_node_tab          = None
    # Node icons
    node_icons = None
    folder_icon             = None
    goto_icon               = None
    python_icon             = None
    nim_icon                = None
    c_icon                  = None
    cpp_icon                = None
    
    
    def clean_up(self):
        # Clean up the tree model
        self.clean_model()
        # Disconnect signals
        self.doubleClicked.disconnect()
        self.expanded.disconnect()
        # Clean up main references
        self.main_form.node_tree_tab = None
        self._parent = None
        self.main_form = None
        self.icon_manipulator = None
        self.bound_tab = None
        if self.tree_menu is not None:
            self.tree_menu.setParent(None)
            self.tree_menu = None
        if self.worker_thread is not None:
            self.worker_thread.stop()
            self.worker_thread.wait()
            self.worker_thread.quit()
            self.worker_thread = None
        # Clean up self
        self.setParent(None)
        self.deleteLater()
    
    def parent_destroyed(self, event):
        # Connect the bound tab 'destroy' signal to this function
        # for automatic closing of this tree widget
        if self._parent is not None:
            self._parent.close_tab(self)
    
    def __init__(self, parent=None, main_form=None):
        """Initialization"""
        # Initialize the superclass
        super().__init__(parent)
        # Set default font
        self.setFont(data.get_current_font())
        # Initialize components
        self.icon_manipulator = components.IconManipulator()
        # Store the reference to the parent
        self._parent = parent
        # Store the reference to the main form
        self.main_form = main_form
        # Store name of self
        self.name = "Tree display"
        # Disable node expansion on double click
        self.setExpandsOnDoubleClick(False)
        # Connect the click and doubleclick signal
        self.doubleClicked.connect(self._item_double_click)
#        self.clicked.connect(self._item_click)
        # Connect the doubleclick signal
        self.expanded.connect(self._check_contents)
        # Initialize the icons
        # Node icons
        self.node_icons = {
            "module": functions.create_icon("various/node_module.png"),
            "import": functions.create_icon("various/node_module.png"),
            "function": functions.create_icon("various/node_procedure.png"),
            "procedure": functions.create_icon("various/node_procedure.png"),
            "method": functions.create_icon("various/node_method.png"),
            "getter": functions.create_icon("various/node_method.png"),
            "property": functions.create_icon("various/node_method.png"),
            "var": functions.create_icon("various/node_variable.png"),
            "variable": functions.create_icon("various/node_variable.png"),
            "alias": functions.create_icon("various/node_alias.png"),
            "externvar": functions.create_icon("various/node_variable.png"),
            "prototype": functions.create_icon("various/node_function.png"),
            "typedef": functions.create_icon("various/node_type.png"),
            "struct": functions.create_icon("various/node_type.png"),
            "enum": functions.create_icon("various/node_type.png"),
            "union": functions.create_icon("various/node_type.png"),
            "type": functions.create_icon("various/node_type.png"),
            "constant": functions.create_icon("various/node_const.png"),
            "const": functions.create_icon("various/node_const.png"),
            "enumerator": functions.create_icon("various/node_const.png"),
            "include": functions.create_icon("various/node_module.png"),
            "define": functions.create_icon("various/node_macro.png"),
            "pragma": functions.create_icon("various/node_pragma.png"),
            "undef": functions.create_icon("various/node_macro.png"),
            "error": functions.create_icon("various/node_macro.png"),
            "macro": functions.create_icon("various/node_macro.png"),
            "member": functions.create_icon("various/node_method.png"),
            "converter": functions.create_icon("various/node_converter.png"),
            "namespace": functions.create_icon("various/node_namespace.png"),
            "template": functions.create_icon("various/node_template.png"),
            "class": functions.create_icon("various/node_class.png"),
            "iterator": functions.create_icon("various/node_iterator.png"),
            "nothing": functions.create_icon("tango_icons/dialog-warning.png"),
            "unknown": functions.create_icon("various/node_unknown.png"),
        }
        self.python_icon = functions.create_icon("language_icons/logo_python.png")
        self.nim_icon = functions.create_icon("language_icons/logo_nim.png")
        self.c_icon = functions.create_icon("language_icons/logo_c.png")
        self.cpp_icon = functions.create_icon("language_icons/logo_cpp.png")
        # File searching icons
        self.file_icon = functions.create_icon("tango_icons/file.png")
        self.folder_icon = functions.create_icon("tango_icons/folder.png")
        self.goto_icon = functions.create_icon('tango_icons/edit-goto.png')
        
        # Set the icon size for every node
        self.update_icon_size()
        
    def update_icon_size(self):
        self.setIconSize(
            functions.create_size(
                data.tree_display_icon_size,
                data.tree_display_icon_size
            )
        )
    
    def get_node_icon(self, icon_name):
        if icon_name in self.node_icons.keys():
            return self.node_icons[icon_name]
        else:
            return self.node_icons["unknown"]
    
    def setFocus(self):
        """Overridden focus event"""
        # Execute the supeclass focus function
        super().setFocus()
        # Check indication
        self.main_form.view.indication_check()
    
    def mousePressEvent(self, event):
        """Function connected to the clicked signal of the tree display"""
        super().mousePressEvent(event)
        # Set the focus
        self.setFocus()
        # Set the last focused widget to the parent basic widget
        self.main_form.last_focused_widget = self._parent
        # Set Save/SaveAs buttons in the menubar
        self._parent._set_save_status()
        # Get the index of the clicked item and execute the item's procedure
        if event.button() == data.Qt.MouseButton.RightButton:
            index = self.indexAt(event.pos())
            self._item_click(index)
        # Reset the click&drag context menu action
        components.ActionFilter.clear_action()
    
    def _item_click(self, model_index):
        if self.tree_display_type == data.TreeDisplayType.FILES:
            item = self.model().itemFromIndex(model_index)
            if (hasattr(item, "is_dir") == True or 
                hasattr(item, "is_base") == True):
                def update_cwd():
                    self.main_form.set_cwd(item.full_name)
                cursor = data.QCursor.pos()
                
                if self.tree_menu is not None:
                    self.tree_menu.setParent(None)
                    self.tree_menu = None

                self.tree_menu = Menu(self)
                
                # Open path in explorer
                open_in_explorer_action = data.QAction("Open in explorer", self)
                def open_in_explorer():
                    path = item.full_name
                    try:
                        result = functions.open_item_in_explorer(path)
                    except:
                        result = False
                    if result == False:
                        self.main_form.display.repl_display_error(
                            "Error opening path in explorer: {}".format(path)
                        )
                open_in_explorer_action.setIcon(
                    functions.create_icon('tango_icons/document-open.png')
                )
                open_in_explorer_action.triggered.connect(open_in_explorer)
                self.tree_menu.addAction(open_in_explorer_action)
                self.tree_menu.addSeparator()
                
                # Clipboard copy name
                clipboard_copy_action = data.QAction("Copy directory name to clipboard", self)
                def clipboard_copy():
                    cb = data.application.clipboard()
                    cb.clear(mode=cb.Mode.Clipboard)
                    cb.setText(item.text(), mode=cb.Mode.Clipboard)
                clipboard_copy_action.setIcon(
                    functions.create_icon('tango_icons/edit-copy.png')
                )
                clipboard_copy_action.triggered.connect(clipboard_copy)
                self.tree_menu.addAction(clipboard_copy_action)
                # Clipboard copy path
                clipboard_copy_path_action = data.QAction("Copy directory path to clipboard", self)
                def clipboard_copy():
                    cb = data.application.clipboard()
                    cb.clear(mode=cb.Mode.Clipboard)
                    cb.setText(item.full_name, mode=cb.Mode.Clipboard)
                clipboard_copy_path_action.setIcon(
                    functions.create_icon('tango_icons/edit-copy.png')
                )
                clipboard_copy_path_action.triggered.connect(clipboard_copy)
                self.tree_menu.addAction(clipboard_copy_path_action)
                self.tree_menu.addSeparator()
                
                # Update CWD
                action_update_cwd = data.QAction("Update CWD", self.tree_menu)
                action_update_cwd.triggered.connect(update_cwd)
                icon = functions.create_icon('tango_icons/update-cwd.png')
                action_update_cwd.setIcon(icon)
                self.tree_menu.addAction(action_update_cwd)
                
                if hasattr(item, "is_base") == True:
                    def update_to_parent():
                        parent_directory = os.path.abspath(
                            os.path.join(item.full_name, os.pardir)
                        )
                        self.main_form.set_cwd(parent_directory)
                    action_update_to_parent = data.QAction(
                        "Update CWD to parent", self.tree_menu
                    )
                    action_update_to_parent.triggered.connect(update_to_parent)
                    icon = functions.create_icon('tango_icons/update-cwd.png')
                    action_update_to_parent.setIcon(icon)
                    self.tree_menu.addAction(action_update_to_parent)
                    self.tree_menu.addSeparator()
                    def one_dir_up():
                        def func():
                            parent_directory = os.path.abspath(
                                os.path.join(item.full_name, os.pardir)
                            )
                            self.main_form.display.show_directory_tree(
                                parent_directory
                            )
                        data.QTimer.singleShot(250, func)
                    action_one_dir_up = data.QAction(
                        "One directory up ..", self.tree_menu
                    )
                    action_one_dir_up.triggered.connect(one_dir_up)
                    icon = functions.create_icon('tango_icons/one-dir-up.png')
                    action_one_dir_up.setIcon(icon)
                    self.tree_menu.addAction(action_one_dir_up)
                self.tree_menu.popup(cursor)
            elif hasattr(item, "full_name") == True:
                def open_file():
                    self.main_form.open_file(item.full_name)
                cursor = data.QCursor.pos()
                
                if self.tree_menu is not None:
                    self.tree_menu.setParent(None)
                    self.tree_menu = None
                
                self.tree_menu = Menu(self)
                # Open in Ex.Co.
                action_open_file = data.QAction("Open", self.tree_menu)
                action_open_file.triggered.connect(open_file)
                icon = functions.create_icon('tango_icons/document-open.png')
                action_open_file.setIcon(icon)
                self.tree_menu.addAction(action_open_file)
                # Open with system
                def open_system():
                    try:
                        if data.platform == 'Windows':
                            os.startfile(item.full_name)
                        else:
                            subprocess.call(["xdg-open", item.full_name])
                    except:
                        self.main_form.display.repl_display_error(traceback.format_exc())
                action_open = data.QAction("Open with system", self.tree_menu)
                action_open.triggered.connect(open_system)
                icon = functions.create_icon('tango_icons/open-with-default-app.png')
                action_open.setIcon(icon)
                self.tree_menu.addAction(action_open)
                # Open in Hex-View
                def open_hex():
                    if item.attributes.itype == TreeExplorer.ItemType.FILE:
                        file_path = item.attributes.path
                        self.open_file_hex_signal.emit(file_path)
                    else:
                        self.main_form.display.repl_display_error(
                            "Item of type '{}' cannot be opened in the Hex-View!".format(
                                item.attributes.itype
                            )
                        )
                action_open_hex = data.QAction("Open with Hex-View", self.tree_menu)
                action_open_hex.triggered.connect(open_hex)
                icon = functions.create_icon('various/node_template.png')
                action_open_hex.setIcon(icon)
                self.tree_menu.addAction(action_open_hex)
                # Open path in explorer
                open_in_explorer_action = data.QAction("Open in explorer", self)
                def open_in_explorer():
                    path = item.full_name
                    try:
                        result = functions.open_item_in_explorer(path)
                    except:
                        result = False
                    if result == False:
                        self.main_form.display.repl_display_error(
                            "Error opening path in explorer: {}".format(path)
                        )
                open_in_explorer_action.setIcon(
                    functions.create_icon('tango_icons/document-open.png')
                )
                open_in_explorer_action.triggered.connect(open_in_explorer)
                self.tree_menu.addAction(open_in_explorer_action)
                self.tree_menu.addSeparator()
                
                # Copy name to clipboard
                clipboard_copy_action = data.QAction("Copy file name to clipboard", self)
                def clipboard_copy():
                    cb = data.application.clipboard()
                    cb.clear(mode=cb.Mode.Clipboard)
                    cb.setText(item.text(), mode=cb.Mode.Clipboard)
                clipboard_copy_action.setIcon(
                    functions.create_icon('tango_icons/edit-copy.png')
                )
                clipboard_copy_action.triggered.connect(clipboard_copy)
                self.tree_menu.addAction(clipboard_copy_action)
                # Clipboard copy path
                clipboard_copy_path_action = data.QAction("Copy file path to clipboard", self)
                def clipboard_copy():
                    cb = data.application.clipboard()
                    cb.clear(mode=cb.Mode.Clipboard)
                    cb.setText(item.full_name, mode=cb.Mode.Clipboard)
                clipboard_copy_path_action.setIcon(
                    functions.create_icon('tango_icons/edit-copy.png')
                )
                clipboard_copy_path_action.triggered.connect(clipboard_copy)
                self.tree_menu.addAction(clipboard_copy_path_action)
                self.tree_menu.addSeparator()
                
                def update_to_parent():
                    directory = os.path.dirname(item.full_name)
                    self.main_form.set_cwd(directory)
                action_update_to_parent = data.QAction(
                    "Update CWD", self.tree_menu
                )
                action_update_to_parent.triggered.connect(update_to_parent)
                icon = functions.create_icon('tango_icons/update-cwd.png')
                action_update_to_parent.setIcon(icon)
                self.tree_menu.addAction(action_update_to_parent)
                self.tree_menu.popup(cursor)
        
        elif self.tree_display_type == data.TreeDisplayType.NODES:
            def goto_item():
                #Parse the node
                self._node_item_parse(item)
            
            def copy_node_to_clipboard():
                try:
                    cb = data.application.clipboard()
                    cb.clear(mode=cb.Mode.Clipboard)
                    cb.setText(item_text.split()[0], mode=cb.Mode.Clipboard)
                except:
                    pass
            
            def open_document():
                #Focus the bound tab in its parent window
                self.bound_tab._parent.setCurrentWidget(self.bound_tab)
            
            item = self.model().itemFromIndex(model_index)
            if item == None:
                return
            item_text = item.text()
            cursor = data.QCursor.pos()
            
            if self.tree_menu is not None:
                self.tree_menu.setParent(None)
                self.tree_menu = None
            
            self.tree_menu = Menu(self)
            
            show_menu = True
            if (hasattr(item, "line_number") == True or "line:" in item_text):
                action_goto_line = data.QAction("Goto node item", self.tree_menu)
                action_goto_line.triggered.connect(goto_item)
                icon = functions.create_icon('tango_icons/edit-goto.png')
                action_goto_line.setIcon(icon)
                self.tree_menu.addAction(action_goto_line)
                action_copy = data.QAction("Copy name", self.tree_menu)
                action_copy.triggered.connect(copy_node_to_clipboard)
                icon = functions.create_icon('tango_icons/edit-copy.png')
                action_copy.setIcon(icon)
                self.tree_menu.addAction(action_copy)
            elif "DOCUMENT" in item_text:
                action_open = data.QAction("Focus document", self.tree_menu)
                action_open.triggered.connect(open_document)
                icon = functions.create_icon('tango_icons/document-open.png')
                action_open.setIcon(icon)
                self.tree_menu.addAction(action_open)
            else:
                show_menu = False
            
            if show_menu:
                self.tree_menu.popup(cursor)
    
    def _item_double_click(self, model_index):
        """
        Function connected to the doubleClicked signal of the tree display
        """
        # Use the item text according to the tree display type
        if self.tree_display_type == data.TreeDisplayType.NODES:
            # Get the text of the double clicked item
            item = self.model().itemFromIndex(model_index)
            self._node_item_parse(item)
        elif self.tree_display_type == data.TreeDisplayType.FILES:
            # Get the double clicked item
            item = self.model().itemFromIndex(model_index)
            # Test if the item has the 'full_name' attribute
            if hasattr(item, "is_dir") == True:
                # Expand/collapse the directory node
                if self.isExpanded(item.index()) == True:
                    self.collapse(item.index())
                else:
                    self.expand(item.index())
                return
            elif hasattr(item, "full_name") == True:
                # Open the file
                self.main_form.open_file(file=item.full_name)
        elif self.tree_display_type == data.TreeDisplayType.FILES_WITH_LINES:
            # Get the double clicked item
            item = self.model().itemFromIndex(model_index)
            #Test if the item has the 'full_name' attribute
            if hasattr(item, "full_name") == False:
                return
            # Open the file
            self.main_form.open_file(file=item.full_name)
            # Check if a line item was clicked
            if hasattr(item, "line_number") == True:
                # Goto the stored line number
                document = self.main_form.get_tab_by_save_name(item.full_name)
                document.goto_line(item.line_number)
    
    def _node_item_parse(self, item):
        # Check if the bound tab has been cleaned up and has no parent
        if self.bound_tab == None or self.bound_tab._parent == None:
            self.main_form.display.repl_display_message(
                "The bound tab has been closed! Reload the tree display.", 
                message_type=data.MessageType.ERROR
            )
            return
        # Check the item text
        item_text = item.text()
        if hasattr(item, "line_number") == True:
            # Goto the stored line number
            self.bound_tab._parent.setCurrentWidget(self.bound_tab)
            self.bound_tab.goto_line(item.line_number)
        elif "line:" in item_text:
            # Parse the line number out of the item text
            line = item_text.split()[-1]
            start_index = line.index(":") + 1
            end_index   = -1
            line_number = int(line[start_index:end_index])
            # Focus the bound tab in its parent window
            self.bound_tab._parent.setCurrentWidget(self.bound_tab)
            # Go to the item line number
            self.bound_tab.goto_line(line_number)
        elif "DOCUMENT" in item_text:
            # Focus the bound tab in its parent window
            self.bound_tab._parent.setCurrentWidget(self.bound_tab)
    
    def _check_contents(self):
        #Update the horizontal scrollbar width
        self.resize_horizontal_scrollbar()
    
    def set_display_type(self, tree_type):
        """Set the tree display type attribute"""
        self.tree_display_type = tree_type
    
    def resize_horizontal_scrollbar(self):
        """
        Resize the header so the horizontal scrollbar will have the correct width
        """
        for i in range(self.model().rowCount()):
            self.resizeColumnToContents(i)
    
    def display_python_nodes_in_list(self, 
                                     custom_editor,
                                     import_nodes, 
                                     class_nodes,
                                     function_nodes,
                                     global_vars, 
                                     parse_error=False):
        """Display the input python data in the tree display"""
        #Store the custom editor tab that for quicker navigation
        self.bound_tab = custom_editor
        #Set the tree display type to NODE
        self.set_display_type(data.TreeDisplayType.NODES)
        #Define the document name, type
        document_name       = os.path.basename(custom_editor.save_name)
        document_name_text  = "DOCUMENT: {:s}".format(document_name)
        document_type_text  = "TYPE: {:s}".format(custom_editor.current_file_type)
        #Define the display structure texts
        import_text         = "IMPORTS:"
        class_text          = "CLASS/METHOD TREE:"
        function_text       = "FUNCTIONS:"
        #Initialize the tree display to Python file type
        self.setSelectionBehavior(data.QAbstractItemView.SelectionBehavior.SelectRows)
        tree_model = data.QStandardItemModel()
        tree_model.setHorizontalHeaderLabels([document_name])
        self.clean_model()
        self.setModel(tree_model)
        self.setUniformRowHeights(True)
        #Add the file attributes to the tree display
        description_brush = data.QBrush(
            data.QColor(data.theme["fonts"]["keyword"]["color"])
        )
        description_font = data.QFont(
            data.current_font_name, data.current_font_size, data.QFont.Weight.Bold
        )
        item_document_name  = data.QStandardItem(document_name_text)
        item_document_name.setEditable(False)
        item_document_name.setForeground(description_brush)
        item_document_name.setFont(description_font)
        item_document_type = data.QStandardItem(document_type_text)
        item_document_type.setEditable(False)
        item_document_type.setForeground(description_brush)
        item_document_type.setFont(description_font)
        item_document_type.setIcon(self.python_icon)
        tree_model.appendRow(item_document_name)
        tree_model.appendRow(item_document_type)
        #Set the label properties
        label_brush = data.QBrush(
            data.QColor(data.theme["fonts"]["singlequotedstring"]["color"])
        )
        label_font = data.QFont(
            data.current_font_name, data.current_font_size, data.QFont.Weight.Bold
        )
        #Check if there was a parsing error
        if parse_error != False:
            error_brush = data.QBrush(data.QColor(180, 0, 0))
            error_font  = data.QFont(
                data.current_font_name, data.current_font_size, data.QFont.Weight.Bold
            )
            item_error = data.QStandardItem("ERROR PARSING FILE!")
            item_error.setEditable(False)
            item_error.setForeground(error_brush)
            item_error.setFont(error_font)
            item_error.setIcon(self.get_node_icon("nothing"))
            tree_model.appendRow(item_error)
            #Show the error message
            error_font = data.get_current_font()
            item_error_msg = data.QStandardItem(str(parse_error))
            item_error_msg.setEditable(False)
            item_error_msg.setForeground(error_brush)
            item_error_msg.setFont(error_font)
            line_number = int(re.search(r"line (\d+)",str(parse_error)).group(1))
            item_error_msg.line_number = line_number
            tree_model.appendRow(item_error_msg)
            return
        """Imported module filtering"""
        item_imports = data.QStandardItem(import_text)
        item_imports.setEditable(False)
        item_imports.setForeground(label_brush)
        item_imports.setFont(label_font)
        for node in import_nodes:
            node_text = str(node[0]) + " (line:"
            node_text += str(node[1]) + ")"
            item_import_node = data.QStandardItem(node_text)
            item_import_node.setEditable(False)
            item_import_node.setIcon(self.get_node_icon("import"))
            item_imports.appendRow(item_import_node)
        if import_nodes == []:
            item_no_imports = data.QStandardItem("No imports found")
            item_no_imports.setEditable(False)
            item_no_imports.setIcon(self.get_node_icon("nothing"))
            item_imports.appendRow(item_no_imports)
        #Append the import node to the model
        tree_model.appendRow(item_imports)
        if import_nodes == []:
            self.expand(item_imports.index())
        """Class nodes filtering"""
        item_classes = data.QStandardItem(class_text)
        item_classes.setEditable(False)
        item_classes.setForeground(label_brush)
        item_classes.setFont(label_font)
        #Check deepest nest level and store it
        max_level = 0
        for node in class_nodes:
            for child in node[1]:
                child_level = child[0] + 1
                if child_level > max_level:
                    max_level = child_level
        #Initialize the base level references to the size of the deepest nest level
        base_node_items = [None] * max_level
        base_node_type  = [None] * max_level
        #Create class nodes as tree items
        for node in class_nodes:
            #Construct the parent node
            node_text = str(node[0].name) + " (line:"
            node_text += str(node[0].lineno) + ")"
            parent_tree_node = data.QStandardItem(node_text)
            parent_tree_node.setEditable(False)
            parent_tree_node.setIcon(self.get_node_icon("class"))
            #Create a list that will hold the child nodes
            child_nodes = []
            #Create base nodes
            #Create the child nodes and add them to list
            for i, child in enumerate(node[1]):
                """!! child_level IS THE INDENTATION LEVEL !!"""
                child_level     = child[0]  
                child_object    = child[1]
                child_text  = str(child_object.name) + " (line:"
                child_text  += str(child_object.lineno) + ")"
                child_tree_node = data.QStandardItem(child_text)
                child_tree_node.setEditable(False)
                #Save the base node, its type for adding children to it
                base_node_items[child_level]    = child_tree_node
                if isinstance(child_object, ast.ClassDef) == True:
                    base_node_type[child_level] = 0
                elif isinstance(child_object, ast.FunctionDef) == True:
                    base_node_type[child_level] = 1
                #Check if the child is a child of a child.
                if child_level != 0:
                    #Set the child icon
                    if isinstance(child_object, ast.ClassDef) == True:
                        child_tree_node.setIcon(self.get_node_icon("class"))
                    else:
                        #Set method/function icon according to the previous base node type
                        if base_node_type[child_level-1] == 0:
                            child_tree_node.setIcon(self.get_node_icon("method"))
                        elif base_node_type[child_level-1] == 1:
                            child_tree_node.setIcon(self.get_node_icon("procedure"))
                    #Determine the parent node level
                    level_retraction    = 1
                    parent_level        = child_level - level_retraction
                    parent_node         = None
                    while parent_node == None and parent_level >= 0:
                        parent_node = base_node_items[parent_level]
                        level_retraction += 1
                        parent_level = child_level - level_retraction
                    #Add the child node to the parent node
                    parent_node.appendRow(child_tree_node)
                    #Sort the base node children
                    parent_node.sortChildren(0)
                else:
                    #Set the icon for the 
                    if isinstance(child_object, ast.ClassDef) == True:
                        child_tree_node.setIcon(self.get_node_icon("class"))
                    elif isinstance(child_object, ast.FunctionDef) == True:
                        child_tree_node.setIcon(self.get_node_icon("method"))
                    child_nodes.append(child_tree_node)
            #Append the child nodes to the parent and sort them
            for cn in child_nodes:
                parent_tree_node.appendRow(cn)
            parent_tree_node.sortChildren(0)
            #Append the parent to the model and sort them
            item_classes.appendRow(parent_tree_node)
            item_classes.sortChildren(0)
        #Append the class nodes to the model
        tree_model.appendRow(item_classes)
        #Check if there were any nodes found
        if class_nodes == []:
            item_no_classes = data.QStandardItem("No classes found")
            item_no_classes.setEditable(False)
            item_no_classes.setIcon(self.get_node_icon("nothing"))
            item_classes.appendRow(item_no_classes)
        """Function nodes filtering"""
        item_functions = data.QStandardItem(function_text)
        item_functions.setEditable(False)
        item_functions.setForeground(label_brush)
        item_functions.setFont(label_font)
        #Create function nodes as tree items
        for func in function_nodes:
            #Set the function node text
            func_text = func.name + " (line:"
            func_text += str(func.lineno) + ")"
            #Construct the node and add it to the tree
            function_node = data.QStandardItem(func_text)
            function_node.setEditable(False)
            function_node.setIcon(self.get_node_icon("procedure"))
            item_functions.appendRow(function_node)
        item_functions.sortChildren(0)
        #Check if there were any nodes found
        if function_nodes == []:
            item_no_functions = data.QStandardItem("No functions found")
            item_no_functions.setEditable(False)
            item_no_functions.setIcon(self.get_node_icon("nothing"))
            item_functions.appendRow(item_no_functions)
        #Append the function nodes to the model
        tree_model.appendRow(item_functions)
        #Expand the base nodes
        self.expand(item_classes.index())
        self.expand(item_functions.index())
        #Resize the header so the horizontal scrollbar will have the correct width
        self.resize_horizontal_scrollbar()
    
    def construct_node(self, node, parent_is_class=False):
        # Construct the node text
        node_text = str(node.name) + " (line:"
        node_text += str(node.line_number) + ")"
        tree_node = data.QStandardItem(node_text)
        tree_node.setEditable(False)
        if node.type == "class":
            tree_node.setIcon(self.get_node_icon("class"))
        elif node.type == "function":
            if parent_is_class == False:
                tree_node.setIcon(self.get_node_icon("procedure"))
            else:
                tree_node.setIcon(self.get_node_icon("method"))
        elif node.type == "global_variable":
            tree_node.setIcon(self.get_node_icon("variable"))
        # Append the children
        node_is_class = False
        if node.type == "class":
            node_is_class = True
        for child_node in node.children:
            tree_node.appendRow(self.construct_node(child_node, node_is_class))
        # Sort the child node alphabetically
        tree_node.sortChildren(0)
        # Return the node
        return tree_node
    
    def display_python_nodes_in_tree(self, 
                                     custom_editor,
                                     python_node_tree, 
                                     parse_error=False):
        """Display the input python data in the tree display"""
        #Store the custom editor tab that for quicker navigation
        self.bound_tab = custom_editor
        #Set the tree display type to NODE
        self.set_display_type(data.TreeDisplayType.NODES)
        #Define the document name, type
        document_name       = os.path.basename(custom_editor.save_name)
        document_name_text  = "DOCUMENT: {:s}".format(document_name)
        document_type_text  = "TYPE: {:s}".format(custom_editor.current_file_type)
        #Define the display structure texts
        import_text         = "IMPORTS:"
        global_vars_text    = "GLOBALS:"
        class_text          = "CLASS/METHOD TREE:"
        function_text       = "FUNCTIONS:"
        #Initialize the tree display to Python file type
        self.setSelectionBehavior(data.QAbstractItemView.SelectionBehavior.SelectRows)
        tree_model = data.QStandardItemModel()
#        tree_model.setHorizontalHeaderLabels([document_name])
        self.header().hide()
        self.clean_model()
        self.setModel(tree_model)
        self.setUniformRowHeights(True)
        #Add the file attributes to the tree display
        description_brush = data.QBrush(
            data.QColor(data.theme["fonts"]["keyword"]["color"])
        )
        description_font = data.QFont(
            data.current_font_name, data.current_font_size, data.QFont.Weight.Bold
        )
        item_document_name  = data.QStandardItem(document_name_text)
        item_document_name.setEditable(False)
        item_document_name.setForeground(description_brush)
        item_document_name.setFont(description_font)
        item_document_type  = data.QStandardItem(document_type_text)
        item_document_type.setEditable(False)
        item_document_type.setForeground(description_brush)
        item_document_type.setFont(description_font)
        item_document_type.setIcon(self.python_icon)
        tree_model.appendRow(item_document_name)
        tree_model.appendRow(item_document_type)
        #Set the label properties
        label_brush = data.QBrush(
            data.QColor(data.theme["fonts"]["singlequotedstring"]["color"])
        )
        label_font  = data.QFont(
            data.current_font_name, data.current_font_size, data.QFont.Weight.Bold
        )
        #Check if there was a parsing error
        if parse_error != False:
            error_brush = data.QBrush(data.QColor(180, 0, 0))
            error_font  = data.QFont(
                data.current_font_name, data.current_font_size, data.QFont.Weight.Bold
            )
            item_error = data.QStandardItem("ERROR PARSING FILE!")
            item_error.setEditable(False)
            item_error.setForeground(error_brush)
            item_error.setFont(error_font)
            item_error.setIcon(self.get_node_icon("nothing"))
            tree_model.appendRow(item_error)
            #Show the error message
            error_font = data.get_current_font()
            item_error_msg = data.QStandardItem(str(parse_error))
            item_error_msg.setEditable(False)
            item_error_msg.setForeground(error_brush)
            item_error_msg.setFont(error_font)
            try:
                line_number = int(re.search(r"line (\d+)",str(parse_error)).group(1))
                item_error_msg.line_number = line_number
            except:
                pass
            tree_model.appendRow(item_error_msg)
            return
        # Create the filtered node lists
        import_nodes = [x for x in python_node_tree if x.type == "import"]
        class_nodes = [x for x in python_node_tree if x.type == "class"]
        function_nodes = [x for x in python_node_tree if x.type == "function"]
        globals_nodes = [x for x in python_node_tree if x.type == "global_variable"]
        """Imported module filtering"""
        item_imports = data.QStandardItem(import_text)
        item_imports.setEditable(False)
        item_imports.setForeground(label_brush)
        item_imports.setFont(label_font)
        for node in import_nodes:
            node_text = str(node.name) + " (line:"
            node_text += str(node.line_number) + ")"
            item_import_node = data.QStandardItem(node_text)
            item_import_node.setEditable(False)
            item_import_node.setIcon(self.get_node_icon("import"))
            item_imports.appendRow(item_import_node)
        if import_nodes == []:
            item_no_imports = data.QStandardItem("No imports found")
            item_no_imports.setEditable(False)
            item_no_imports.setIcon(self.get_node_icon("nothing"))
            item_imports.appendRow(item_no_imports)
        #Append the import node to the model
        tree_model.appendRow(item_imports)
        if import_nodes == []:
            self.expand(item_imports.index())
        """Global variable nodes filtering"""
        item_globals = data.QStandardItem(global_vars_text)
        item_globals.setEditable(False)
        item_globals.setForeground(label_brush)
        item_globals.setFont(label_font)
        #Check if there were any nodes found
        if globals_nodes == []:
            item_no_globals = data.QStandardItem("No global variables found")
            item_no_globals.setEditable(False)
            item_no_globals.setIcon(self.get_node_icon("nothing"))
            item_globals.appendRow(item_no_globals)
        else:
            # Create the function nodes and add them to the tree
            for node in globals_nodes:
                item_globals.appendRow(self.construct_node(node))
        #Append the function nodes to the model
        tree_model.appendRow(item_globals)
        if globals_nodes == []:
            self.expand(item_globals.index())
        """Class nodes filtering"""
        item_classes = data.QStandardItem(class_text)
        item_classes.setEditable(False)
        item_classes.setForeground(label_brush)
        item_classes.setFont(label_font)
        # Check if there were any nodes found
        if class_nodes == []:
            item_no_classes = data.QStandardItem("No classes found")
            item_no_classes.setEditable(False)
            item_no_classes.setIcon(self.get_node_icon("nothing"))
            item_classes.appendRow(item_no_classes)
        else:
            # Create the class nodes and add them to the tree
            for node in class_nodes:
                item_classes.appendRow(self.construct_node(node, True))
        # Append the class nodes to the model
        tree_model.appendRow(item_classes)
        """Function nodes filtering"""
        item_functions = data.QStandardItem(function_text)
        item_functions.setEditable(False)
        item_functions.setForeground(label_brush)
        item_functions.setFont(label_font)
        #Check if there were any nodes found
        if function_nodes == []:
            item_no_functions = data.QStandardItem("No functions found")
            item_no_functions.setEditable(False)
            item_no_functions.setIcon(self.get_node_icon("nothing"))
            item_functions.appendRow(item_no_functions)
        else:
            # Create the function nodes and add them to the tree
            for node in function_nodes:
                item_functions.appendRow(self.construct_node(node))
        #Append the function nodes to the model
        tree_model.appendRow(item_functions)
        """Finalization"""
        #Expand the base nodes
        self.expand(item_classes.index())
        self.expand(item_functions.index())
        #Resize the header so the horizontal scrollbar will have the correct width
        self.resize_horizontal_scrollbar()
    
    def display_nodes(self,
                      custom_editor,
                      module,
                      parser_icon):
        """
        Display the input general (Ctags) data in a tree structure
        """
        # Store the custom editor tab that for quicker navigation
        self.bound_tab = custom_editor
        # Set the tree display type to NODE
        self.set_display_type(data.TreeDisplayType.NODES)
        # Set the label properties
        label_brush = data.QBrush(
            data.QColor(data.theme["fonts"]["singlequotedstring"]["color"])
        )
        label_font  = data.QFont(
            data.current_font_name, data.current_font_size, data.QFont.Weight.Bold
        )
        # Filter the nodes
        def display_node(tree_node, c_node):
            node_group = {}
            for v in c_node.children:
                if v.type in node_group.keys():
                    node_group[v.type].append(v)
                else:
                    node_group[v.type] = [v]
            # Initialize a list of struct references for later addition of their members
            item_cache = {}
            node_cache = {}
            # Add The nodes to the tree using the parent tree node
            for k in sorted(node_group.keys()):
                if k == "member":
                    continue
                group_name = k.upper()
                item = data.QStandardItem("{}:".format(group_name))
                current_list = node_group[k]
                if k in self.node_icons.keys():
                    icon = self.get_node_icon(k)
                else:
                    icon = self.get_node_icon("unknown")
                    self.main_form.display.repl_display_warning(
                        "[TreeDisplay] Unknown node: {}".format(k)
                    )
                    
                item.setEditable(False)
                item.setForeground(label_brush)
                item.setFont(label_font)
                # Create nodes as tree items
                current_list = sorted(current_list, key=lambda x: x.name)
                for n in current_list:
                    node_string = "{}:{}".format(n.type, n.name)
                    if node_string not in node_cache.keys() and n.parent is None:
                        # Set the function node text
                        node_text = n.name + " (line:"
                        node_text += str(n.line_number) + ")"
                        # Construct the node and add it to the tree
                        node = data.QStandardItem(node_text)
                        node.setEditable(False)
                        node.setIcon(icon)
                        
                        if n.children != []:
                            display_node(node, n)
                        
                        item.appendRow(node)
                        
                        node_cache[node_string] = node
                    
                # Check if there were any nodes found
#                if current_list == []:
#                    item_no_nodes = data.QStandardItem("No items found")
#                    item_no_nodes.setEditable(False)
#                    item.appendRow(item_no_nodes)
                # Append the nodes to the parent node
                tree_node.appendRow(item)
                item_cache[k] = item
            
            # Add the struct members directly to the structs
            for k,v in node_group.items():
                for n in v:
                    if n.parent is None:
                        continue
                    # Set the function node text
                    node_text = n.name + " (line:"
                    node_text += str(n.line_number) + ")"
                    # Construct the node and add it to the tree
                    node = data.QStandardItem(node_text)
                    node.setEditable(False)
                    node.setIcon(self.get_node_icon(n.type))
                    parent_string = "{}:{}".format(n.parent_type, n.parent)
                    if parent_string not in node_cache.keys():
                        parent_node_text = "{} (undefined)".format(n.parent)
                        parent_node = data.QStandardItem(parent_node_text)
                        parent_node.setEditable(False)
                        parent_node.setIcon(self.get_node_icon(n.parent_type))
                        node_cache[parent_string] = parent_node
                        parent_type_string = n.parent_type
                        if parent_type_string not in item_cache.keys():
                            item = data.QStandardItem("{}:".format(parent_type_string.upper()))
                            item.setEditable(False)
                            item.setForeground(label_brush)
                            item.setFont(label_font)
                            tree_node.appendRow(item)
                            item_cache[parent_type_string] = item
                        item_cache[parent_type_string].appendRow(parent_node)
                    node_cache[parent_string].appendRow(node)
        
        # Define the document name, type
        document_name       = os.path.basename(custom_editor.save_name)
        document_name_text  = "DOCUMENT: {:s}".format(document_name)
        document_type_text  = "TYPE: {:s}".format(custom_editor.current_file_type)
        document_type_icon  = parser_icon
        # Initialize the tree display
        self.setSelectionBehavior(data.QAbstractItemView.SelectionBehavior.SelectRows)
        tree_model = data.QStandardItemModel()
#        tree_model.setHorizontalHeaderLabels([document_name])
        self.header().hide()
        self.clean_model()
        self.setModel(tree_model)
        self.setUniformRowHeights(True)
        # Add the file attributes to the tree display
        description_brush   = data.QBrush(
            data.QColor(data.theme["fonts"]["keyword"]["color"])
        )
        description_font    = data.QFont(
            data.current_font_name, data.current_font_size, data.QFont.Weight.Bold
        )
        item_document_name  = data.QStandardItem(document_name_text)
        item_document_name.setEditable(False)
        item_document_name.setForeground(description_brush)
        item_document_name.setFont(description_font)
        item_document_type  = data.QStandardItem(document_type_text)
        item_document_type.setEditable(False)
        item_document_type.setForeground(description_brush)
        item_document_type.setFont(description_font)
        item_document_type.setIcon(document_type_icon)
        tree_model.appendRow(item_document_name)
        tree_model.appendRow(item_document_type)
        # Add the items recursively
        display_node(tree_model, module[0])
        # Clean the empty base items
        empty_nodes = [
            i for i in range(self.model().rowCount())
                if not self.model().item(i, 0).hasChildren() and i > 1
        ]
        empty_nodes.reverse()
        for en in empty_nodes:
            self.model().removeRow(en)
        # Resize the header so the horizontal scrollbar will have the correct width
        self.resize_horizontal_scrollbar()
    
    def display_nim_nodes(self, custom_editor, nim_nodes):
        """Display the Nim nodes in a tree structure"""
        #Store the custom editor tab that for quicker navigation
        self.bound_tab = custom_editor
        #Set the tree display type to NODE
        self.set_display_type(data.TreeDisplayType.NODES)
        #Define the document name, type
        document_name       = os.path.basename(custom_editor.save_name)
        document_name_text  = "DOCUMENT: {:s}".format(document_name)
        document_type_text  = "TYPE: {:s}".format(custom_editor.current_file_type)
        #Initialize the tree display
        self.setSelectionBehavior(data.QAbstractItemView.SelectionBehavior.SelectRows)
        tree_model = data.QStandardItemModel()
#        tree_model.setHorizontalHeaderLabels([document_name])
        self.header().hide()
        self.clean_model()
        self.setModel(tree_model)
        self.setUniformRowHeights(True)
        #Add the file attributes to the tree display
        description_brush = data.QBrush(
            data.QColor(data.theme["fonts"]["keyword"]["color"])
        )
        description_font = data.QFont(
            data.current_font_name, data.current_font_size, data.QFont.Weight.Bold
        )
        item_document_name  = data.QStandardItem(document_name_text)
        item_document_name.setEditable(False)
        item_document_name.setForeground(description_brush)
        item_document_name.setFont(description_font)
        item_document_type  = data.QStandardItem(document_type_text)
        item_document_type.setEditable(False)
        item_document_type.setForeground(description_brush)
        item_document_type.setFont(description_font)
        item_document_type.setIcon(self.nim_icon)
        tree_model.appendRow(item_document_name)
        tree_model.appendRow(item_document_type)
        """Add the nodes"""
        label_brush = data.QBrush(
            data.QColor(data.theme["fonts"]["singlequotedstring"]["color"])
        )
        label_font  = data.QFont(
            data.current_font_name, data.current_font_size, data.QFont.Weight.Bold
        )
        #Nested function for creating a tree node
        def create_tree_node(node_text, 
                             node_text_brush, 
                             node_text_font, 
                             node_icon, 
                             node_line_number):
            tree_node = data.QStandardItem(node_text)
            tree_node.setEditable(False)
            if node_text_brush is not None:
                tree_node.setForeground(node_text_brush)
            if node_text_font is not None:
                tree_node.setFont(node_text_font)
            if node_icon is not None:
                tree_node.setIcon(node_icon)
            if node_line_number is not None:
                tree_node.line_number = node_line_number
            return tree_node
        #Nested recursive function for displaying nodes
        def show_nim_node(tree, parent_node, new_node):
            #Nested function for retrieving the nodes name attribute case insensitively
            def get_case_insensitive_name(item):
                name = item.name
                return name.lower()
            #Check if parent node is set, else append to the main tree model
            appending_node = parent_node
            if parent_node == None:
                appending_node = tree
            if new_node.imports != []:
                item_imports_node = create_tree_node("IMPORTS:", label_brush, label_font, None, None)
                appending_node.appendRow(item_imports_node)
                #Sort the list by the name attribute
                new_node.imports.sort(key=get_case_insensitive_name)
                #new_node.imports.sort(key=operator.attrgetter('name'))
                for module in new_node.imports:
                    item_module_node =  create_tree_node(
                                            module.name, 
                                            None, 
                                            None, 
                                            self.get_node_icon("import"), 
                                            module.line + 1
                                        )
                    item_imports_node.appendRow(item_module_node)
            if new_node.types != []:
                item_types_node = create_tree_node("TYPES:", label_brush, label_font, None, None)
                appending_node.appendRow(item_types_node)
                #Sort the list by the name attribute
                new_node.types.sort(key=get_case_insensitive_name)
                for type in new_node.types:
                    item_type_node =    create_tree_node(
                                            type.name, 
                                            None, 
                                            None, 
                                            self.get_node_icon("type"), 
                                            type.line + 1
                                        )
                    item_types_node.appendRow(item_type_node)
            if new_node.consts != []:
                item_consts_node = create_tree_node("CONSTANTS:", label_brush, label_font, None, None)
                appending_node.appendRow(item_consts_node)
                #Sort the list by the name attribute
                new_node.consts.sort(key=get_case_insensitive_name)
                for const in new_node.consts:
                    item_const_node =   create_tree_node(
                                            const.name, 
                                            None, 
                                            None, 
                                            self.get_node_icon("const"), 
                                            const.line + 1
                                        )
                    item_consts_node.appendRow(item_const_node)
            if new_node.lets != []:
                item_lets_node = create_tree_node("SINGLE ASSIGNMENT VARIABLES:", label_brush, label_font, None, None)
                appending_node.appendRow(item_lets_node)
                #Sort the list by the name attribute
                new_node.consts.sort(key=get_case_insensitive_name)
                for let in new_node.lets:
                    item_let_node =   create_tree_node(
                                            let.name, 
                                            None, 
                                            None, 
                                            self.get_node_icon("const"), 
                                            let.line + 1
                                        )
                    item_lets_node.appendRow(item_let_node)
            if new_node.vars != []:
                item_vars_node = create_tree_node("VARIABLES:", label_brush, label_font, None, None)
                appending_node.appendRow(item_vars_node)
                #Sort the list by the name attribute
                new_node.vars.sort(key=get_case_insensitive_name)
                for var in new_node.vars:
                    item_var_node = create_tree_node(
                                        var.name, 
                                        None, 
                                        None, 
                                        self.get_node_icon("variable"), 
                                        var.line + 1
                                    )
                    item_vars_node.appendRow(item_var_node)
            if new_node.procedures != []:
                item_procs_node = create_tree_node("PROCEDURES:", label_brush, label_font, None, None)
                appending_node.appendRow(item_procs_node)
                #Sort the list by the name attribute
                new_node.procedures.sort(key=get_case_insensitive_name)
                for proc in new_node.procedures:
                    item_proc_node = create_tree_node(
                                        proc.name, 
                                        None, 
                                        None, 
                                        self.get_node_icon("procedure"), 
                                        proc.line + 1
                                    )
                    item_procs_node.appendRow(item_proc_node)
                    show_nim_node(None, item_proc_node, proc)
            if new_node.forward_declarations != []:
                item_fds_node = create_tree_node("FORWARD DECLARATIONS:", label_brush, label_font, None, None)
                appending_node.appendRow(item_fds_node)
                #Sort the list by the name attribute
                new_node.forward_declarations.sort(key=get_case_insensitive_name)
                for proc in new_node.forward_declarations:
                    item_fd_node = create_tree_node(
                                        proc.name, 
                                        None, 
                                        None, 
                                        self.get_node_icon("procedure"), 
                                        proc.line + 1
                                    )
                    item_fds_node.appendRow(item_fd_node)
                    show_nim_node(None, item_fd_node, proc)
            if new_node.converters != []:
                item_converters_node = create_tree_node("CONVERTERS:", label_brush, label_font, None, None)
                appending_node.appendRow(item_converters_node)
                #Sort the list by the name attribute
                new_node.converters.sort(key=get_case_insensitive_name)
                for converter in new_node.converters:
                    item_converter_node =   create_tree_node(
                                                converter.name, 
                                                None, 
                                                None, 
                                                self.get_node_icon("converter"),  
                                                converter.line + 1
                                            )
                    item_converters_node.appendRow(item_converter_node)
                    show_nim_node(None, item_converter_node, converter)
            if new_node.iterators != []:
                item_iterators_node = create_tree_node("ITERATORS:", label_brush, label_font, None, None)
                appending_node.appendRow(item_iterators_node)
                #Sort the list by the name attribute
                new_node.iterators.sort(key=get_case_insensitive_name)
                for iterator in new_node.iterators:
                    item_iterator_node =   create_tree_node(
                                                iterator.name, 
                                                None, 
                                                None, 
                                                self.get_node_icon("iterator"),  
                                                iterator.line + 1
                                            )
                    item_iterators_node.appendRow(item_iterator_node)
                    show_nim_node(None, item_iterator_node, iterator)
            if new_node.methods != []:
                item_methods_node = create_tree_node("METHODS:", label_brush, label_font, None, None)
                appending_node.appendRow(item_methods_node)
                #Sort the list by the name attribute
                new_node.methods.sort(key=get_case_insensitive_name)
                for method in new_node.methods:
                    item_method_node = create_tree_node(
                                        method.name, 
                                        None, 
                                        None, 
                                        self.get_node_icon("method"), 
                                        method.line + 1
                                    )
                    item_methods_node.appendRow(item_method_node)
                    show_nim_node(None, item_method_node, method)
            if new_node.properties != []:
                item_properties_node = create_tree_node("PROPERTIES:", label_brush, label_font, None, None)
                appending_node.appendRow(item_properties_node)
                #Sort the list by the name attribute
                new_node.properties.sort(key=get_case_insensitive_name)
                for property in new_node.properties:
                    item_property_node = create_tree_node(
                                            property.name, 
                                            None, 
                                            None, 
                                            self.get_node_icon("method"), 
                                            property.line + 1
                                        )
                    item_properties_node.appendRow(item_property_node)
                    show_nim_node(None, item_property_node, property)
            if new_node.macros != []:
                item_macros_node = create_tree_node("MACROS:", label_brush, label_font, None, None)
                appending_node.appendRow(item_macros_node)
                #Sort the list by the name attribute
                new_node.macros.sort(key=get_case_insensitive_name)
                for macro in new_node.macros:
                    item_macro_node = create_tree_node(
                                        macro.name, 
                                        None, 
                                        None, 
                                        self.get_node_icon("macro"), 
                                        macro.line + 1
                                    )
                    item_macros_node.appendRow(item_macro_node)
                    show_nim_node(None, item_macro_node, macro)
            if new_node.templates != []:
                item_templates_node = create_tree_node("TEMPLATES:", label_brush, label_font, None, None)
                appending_node.appendRow(item_templates_node)
                #Sort the list by the name attribute
                new_node.templates.sort(key=get_case_insensitive_name)
                for template in new_node.templates:
                    item_template_node = create_tree_node(
                                        template.name, 
                                        None, 
                                        None, 
                                        self.get_node_icon("template"), 
                                        template.line + 1
                                    )
                    item_templates_node.appendRow(item_template_node)
                    show_nim_node(None, item_template_node, template)
            if new_node.objects != []:
                item_classes_node = create_tree_node("OBJECTS:", label_brush, label_font, None, None)
                appending_node.appendRow(item_classes_node)
                #Sort the list by the name attribute
                new_node.objects.sort(key=get_case_insensitive_name)
                for obj in new_node.objects:
                    item_class_node = create_tree_node(
                                        obj.name, 
                                        None, 
                                        None, 
                                        self.get_node_icon("class"), 
                                        obj.line + 1
                                    )
                    item_classes_node.appendRow(item_class_node)
                    show_nim_node(None, item_class_node, obj)
            if new_node.namespaces != []:
                item_namespaces_node = create_tree_node("NAMESPACES:", label_brush, label_font, None, None)
                appending_node.appendRow(item_namespaces_node)
                #Sort the list by the name attribute
                new_node.namespaces.sort(key=get_case_insensitive_name)
                for namespace in new_node.namespaces:
                    item_namespace_node = create_tree_node(
                                        namespace.name, 
                                        None, 
                                        None, 
                                        self.get_node_icon("namespace"), 
                                        namespace.line + 1
                                    )
                    item_namespaces_node.appendRow(item_namespace_node)
                    show_nim_node(None, item_namespace_node, namespace)
        show_nim_node(tree_model, None, nim_nodes)
    
    def clean_model(self):
        if self.model() is not None:
            self.model().setParent(None)
            self.setModel(None)
    
    def _init_found_files_options(self, search_text, directory, custom_text=None):
        #Initialize the tree display to the found files type
        self.horizontalScrollbarAction(1)
        self.setSelectionBehavior(data.QAbstractItemView.SelectionBehavior.SelectRows)
        tree_model = data.QStandardItemModel()
        tree_model.setHorizontalHeaderLabels(["FOUND FILES TREE"])
        self.header().hide()
        self.clean_model()
        self.setModel(tree_model)
        self.setUniformRowHeights(True)
        """Define the description details"""
        #Font
        description_brush = data.QBrush(
            data.QColor(data.theme["fonts"]["keyword"]["color"])
        )
        description_font    = data.QFont(
            data.current_font_name, data.current_font_size, data.QFont.Weight.Bold
        )
        #Directory item
        item_directory  = data.QStandardItem(
            "BASE DIRECTORY: {:s}".format(directory.replace("\\", "/"))
        )
        item_directory.setEditable(False)
        item_directory.setForeground(description_brush)
        item_directory.setFont(description_font)
        #Search item, display according to the custom text parameter
        if custom_text == None:
            item_search_text = data.QStandardItem(
                "FILE HAS: {:s}".format(search_text)
            )
        else:
            item_search_text = data.QStandardItem(custom_text)
        item_search_text.setEditable(False)
        item_search_text.setForeground(description_brush)
        item_search_text.setFont(description_font)
        tree_model.appendRow(item_directory)
        tree_model.appendRow(item_search_text)
        return tree_model
    
    def _init_replace_in_files_options(self, search_text, replace_text, directory):
        #Initialize the tree display to the found files type
        self.horizontalScrollbarAction(1)
        self.setSelectionBehavior(data.QAbstractItemView.SelectionBehavior.SelectRows)
        tree_model = data.QStandardItemModel()
        tree_model.setHorizontalHeaderLabels(["REPLACED IN FILES TREE"])
        self.header().hide()
        self.clean_model()
        self.setModel(tree_model)
        self.setUniformRowHeights(True)
        """Define the description details"""
        #Font
        description_brush = data.QBrush(
            data.QColor(data.theme["fonts"]["default"]["color"])
        )
        description_font = data.QFont(
            data.current_font_name, data.current_font_size, data.QFont.Weight.Bold
        )
        #Directory item
        item_directory  = data.QStandardItem(
            "BASE DIRECTORY: {:s}".format(directory.replace("\\", "/"))
        )
        item_directory.setEditable(False)
        item_directory.setForeground(description_brush)
        item_directory.setFont(description_font)
        #Search item
        item_search_text = data.QStandardItem(
                            "SEARCH TEXT: {:s}".format(search_text)
                           )
        item_search_text.setEditable(False)
        item_search_text.setForeground(description_brush)
        item_search_text.setFont(description_font)
        #Replace item
        item_replace_text = data.QStandardItem(
                            "REPLACE TEXT: {:s}".format(replace_text)
                           )
        item_replace_text.setEditable(False)
        item_replace_text.setForeground(description_brush)
        item_replace_text.setFont(description_font)
        tree_model.appendRow(item_directory)
        tree_model.appendRow(item_search_text)
        tree_model.appendRow(item_replace_text)
        return tree_model
    
    def _sort_item_list(self, items, base_directory):
        """
        Helper function for sorting a file/directory list so that
        all of the directories are before any files in the list
        """
        sorted_directories = []
        sorted_files = []
        for item in items:
            _dir = None
            if os.path.isdir(item):
                _dir = item
            else:
                _dir = os.path.dirname(item)
            if (not _dir in sorted_directories):
                sorted_directories.append(_dir)
            if os.path.isfile(item):
                sorted_files.append(item)
        #Remove the base directory from the directory list, it is not needed
        if base_directory in sorted_directories:
            sorted_directories.remove(base_directory)
        #Sort the two lists case insensitively
        sorted_directories.sort(key=str.lower)
        sorted_files.sort(key=str.lower)
        #Combine the file and directory lists
        sorted_items = sorted_directories + sorted_files
        return sorted_items
    
    def _add_items_to_tree(self, tree_model, directory, items):
        """
        Helper function for adding files to a tree view
        """
        #Check if any files were found
        if items != []:
            def add_items(directory, items, thread):
                #Set the UNIX file format to the directory
                directory = directory.replace("\\", "/")
                """
                Adding the files
                """
                label_brush = data.QBrush(
                    data.QColor(data.theme["fonts"]["singlequotedstring"]["color"])
                )
                label_font = data.QFont(
                    data.current_font_name, data.current_font_size, data.QFont.Weight.Bold
                )
                item_brush = data.QBrush(
                    data.QColor(data.theme["fonts"]["default"]["color"])
                )
                item_font = data.get_current_font()
                #Create the base directory item that will hold all of the found files
                item_base_directory = data.QStandardItem(directory)
                item_base_directory.setEditable(False)
                item_base_directory.setForeground(label_brush)
                item_base_directory.setFont(label_font)
                item_base_directory.setIcon(self.folder_icon)
                #Add an indicating attribute that shows the item is a directory.
                #It's a python object, attributes can be added dynamically!
                item_base_directory.is_base = True
                item_base_directory.full_name = directory
                #Create the base directory object that will hold everything else
                base_directory = self.Directory(item_base_directory)
                #Create the files that will be added last directly to the base directory
                base_files = {}
                #Sort the the item list so that all of the directories are before the files
                sorted_items = self._sort_item_list(items, directory)
                #Loop through the files while creating the directory tree
                for item_with_path in sorted_items:
                    if thread.stop_flag:
                        return None
                    
                    if os.path.isfile(item_with_path):
                        file = item_with_path.replace(directory, "")
                        file_name       = os.path.basename(file)
                        directory_name  = os.path.dirname(file)
                        #Strip the first "/" from the files directory
                        if directory_name.startswith("/"):
                            directory_name = directory_name[1:]
                        #Initialize the file item
                        item_file = data.QStandardItem(file_name)
                        item_file.setEditable(False)
                        item_file.setForeground(item_brush)
                        item_file.setFont(item_font)
                        file_type = functions.get_file_type(file_name)
                        item_file.setIcon(functions.get_language_file_icon(file_type))
                        #Add an atribute that will hold the full file name to the QStandartItem.
                        #It's a python object, attributes can be added dynamically!
                        item_file.full_name = item_with_path
                        #Check if the file is in the base directory
                        if directory_name == "":
                            #Store the file item for adding to the bottom of the tree
                            base_files[file_name] = item_file
                        else:
                            #Check the previous file items directory structure
                            parsed_directory_list = directory_name.split("/")
                            #Create the new directories
                            current_directory = base_directory
                            for dir in parsed_directory_list:
                                #Check if the current loop directory already exists
                                if dir in current_directory.directories:
                                    current_directory = current_directory.directories[dir]
                            #Add the file to the directory
                            current_directory.add_file(file_name, item_file)
                    else:
                        directory_name  = item_with_path.replace(directory, "")
                        #Strip the first "/" from the files directory
                        if directory_name.startswith("/"):
                            directory_name = directory_name[1:]
                        #Check the previous file items directory structure
                        parsed_directory_list = directory_name.split("/")
                        #Create the new directories
                        current_directory = base_directory
                        for dir in parsed_directory_list:
                            #Check if the current loop directory already exists
                            if dir in current_directory.directories:
                                current_directory = current_directory.directories[dir]
                            else:
                                #Create the new directory item
                                item_new_directory = data.QStandardItem(dir)
                                item_new_directory.setEditable(False)
                                item_new_directory.setIcon(self.folder_icon)
                                item_new_directory.setForeground(item_brush)
                                item_new_directory.setFont(item_font)
                                #Add an indicating attribute that shows the item is a directory.
                                #It's a python object, attributes can be added dynamically!
                                item_new_directory.is_dir = True
                                item_new_directory.full_name = item_with_path
                                current_directory = current_directory.add_directory(
                                    dir, 
                                    item_new_directory
                                )
                #Add the base level files from the stored dictionary, first sort them
                for file_key in sorted(base_files, key=str.lower):
                    base_directory.add_file(file_key, base_files[file_key])
                return item_base_directory, base_directory
            
            class ProcessThread(data.QThread):
                finished = data.pyqtSignal(object, object)
                stop_flag = False
                
                def stop(self):
                    self.stop_flag = True
                
                def run(self):
                    result = add_items(directory, items, self)
                    if result == None:
                        return None
                    item_base_directory, base_directory = result
                    self.finished.emit(item_base_directory, base_directory)
            
            @data.pyqtSlot(object, object)
            def completed(directory_base, base_directory):
                tree_model.appendRow(directory_base)
                # Check if the TreeDisplay underlying C++ object is alive
                if self._parent is None:
                    return
                # Expand the base directory item
                self.expand(directory_base.index())
                # Resize the header so the horizontal scrollbar will have the correct width
                self.resize_horizontal_scrollbar()
                # Hide the wait animation
                if self._parent is not None:
                    self._parent._set_wait_animation(self._parent.indexOf(self), False)
            
            if self.worker_thread is not None:
                self.worker_thread.wait()
            self.worker_thread = ProcessThread()
            self.worker_thread.setTerminationEnabled(True)
            self.worker_thread.finished.connect(completed)
            self.worker_thread.start()
        else:
            item_no_files_found = data.QStandardItem("No items found")
            item_no_files_found.setEditable(False)
            item_no_files_found.setIcon(self.get_node_icon("nothing"))
            item_no_files_found.setForeground(label_brush)
            item_no_files_found.setFont(label_font)
            tree_model.appendRow(item_no_files_found)
    
    def _add_items_with_lines_to_tree(self, tree_model, directory, items):
        """ Helper function for adding files to a tree view """
        #Check if any files were found
        if items != {}:
            #Set the UNIX file format to the directory
            directory = directory.replace("\\", "/")
            """Adding the files"""
            label_brush = data.QBrush(
                data.QColor(data.theme["fonts"]["singlequotedstring"]["color"])
            )
            label_font  = data.QFont(
                data.current_font_name, data.current_font_size, data.QFont.Weight.Bold
            )
            item_brush = data.QBrush(
                data.QColor(data.theme["fonts"]["default"]["color"])
            )
            item_font = data.get_current_font()
            #Create the base directory item that will hold all of the found files
            item_base_directory = data.QStandardItem(directory)
            item_base_directory.setEditable(False)
            item_base_directory.setForeground(label_brush)
            item_base_directory.setFont(label_font)
            item_base_directory.setIcon(self.folder_icon)
            #Create the base directory object that will hold everything else
            base_directory = self.Directory(item_base_directory)
            #Create the files that will be added last directly to the base directory
            base_files = {}
            #Sort the the item list so that all of the directories are before the files
            items_list = list(items.keys())
            sorted_items = self._sort_item_list(items_list, directory)
            #Loop through the files while creating the directory tree
            for item_with_path in sorted_items:
                if os.path.isfile(item_with_path):
                    file = item_with_path.replace(directory, "")
                    file_name       = os.path.basename(file)
                    directory_name  = os.path.dirname(file)
                    #Strip the first "/" from the files directory
                    if directory_name.startswith("/"):
                        directory_name = directory_name[1:]
                    #Initialize the file item
                    item_file = data.QStandardItem(file_name)
                    item_file.setEditable(False)
                    file_type = functions.get_file_type(file_name)
                    item_file.setIcon(functions.get_language_file_icon(file_type))
                    item_file.setForeground(item_brush)
                    item_file.setFont(item_font)
                    #Add an atribute that will hold the full file name to the QStandartItem.
                    #It's a python object, attributes can be added dynamically!
                    item_file.full_name = item_with_path
                    for line in items[item_with_path]:
                        #Adjust the line numbering to Ex.Co. (1 to end)
                        line += 1
                        #Create the goto line item
                        item_line = data.QStandardItem("line {:d}".format(line))
                        item_line.setEditable(False)
                        item_line.setIcon(self.goto_icon)
                        item_line.setForeground(item_brush)
                        item_line.setFont(item_font)
                        #Add the file name and line number as attributes
                        item_line.full_name     = item_with_path
                        item_line.line_number   = line
                        item_file.appendRow(item_line)
                    #Check if the file is in the base directory
                    if directory_name == "":
                        #Store the file item for adding to the bottom of the tree
                        base_files[file_name] = item_file
                    else:
                        #Check the previous file items directory structure
                        parsed_directory_list = directory_name.split("/")
                        #Create the new directories
                        current_directory = base_directory
                        for dir in parsed_directory_list:
                            #Check if the current loop directory already exists
                            if dir in current_directory.directories:
                                current_directory = current_directory.directories[dir]
                        #Add the file to the directory
                        current_directory.add_file(file_name, item_file)
                else:
                    directory_name  = item_with_path.replace(directory, "")
                    #Strip the first "/" from the files directory
                    if directory_name.startswith("/"):
                        directory_name = directory_name[1:]
                    #Check the previous file items directory structure
                    parsed_directory_list = directory_name.split("/")
                    #Create the new directories
                    current_directory = base_directory
                    for dir in parsed_directory_list:
                        #Check if the current loop directory already exists
                        if dir in current_directory.directories:
                            current_directory = current_directory.directories[dir]
                        else:
                            #Create the new directory item
                            item_new_directory = data.QStandardItem(dir)
                            item_new_directory.setEditable(False)
                            item_new_directory.setIcon(self.folder_icon)
                            item_new_directory.setForeground(item_brush)
                            item_new_directory.setFont(item_font)
                            #Add an indicating attribute that shows the item is a directory.
                            #It's a python object, attributes can be added dynamically!
                            item_new_directory.is_dir = True
                            current_directory = current_directory.add_directory(
                                                    dir, 
                                                    item_new_directory
                                                )
            #Add the base level files from the stored dictionary, first sort them
            for file_key in sorted(base_files, key=str.lower):
                base_directory.add_file(file_key, base_files[file_key])
            tree_model.appendRow(item_base_directory)
            #Expand the base directory item
            self.expand(item_base_directory.index())
            #Resize the header so the horizontal scrollbar will have the correct width
            self.resize_horizontal_scrollbar()
        else:
            item_no_files_found = data.QStandardItem("No items found")
            item_no_files_found.setEditable(False)
            item_no_files_found.setIcon(self.get_node_icon("nothing"))
            item_no_files_found.setForeground(item_brush)
            item_no_files_found.setFont(item_font)
            tree_model.appendRow(item_no_files_found)
    
    def display_directory_tree(self, directory):
        """
        Display the selected directory in a tree view structure
        """
        #Set the tree display type to FILES
        self.set_display_type(data.TreeDisplayType.FILES)
        #Create the walk generator that returns all files/subdirectories
        try:
            walk_generator = os.walk(directory)
        except:
            self.main_form.display.repl_display_message(
                "Invalid directory!", 
                message_type=data.MessageType.ERROR
            )
            return
        #Initialize and display the search options
        tree_model = self._init_found_files_options(
            None, 
            directory, 
            custom_text="DISPLAYING ALL FILES/SUBDIRECTORIES"
        )
        
        class ProcessThread(data.QThread):
            finished = data.pyqtSignal(list)
            stop_flag = False
                
            def stop(self):
                self.stop_flag = True
            
            def run(self):
                #Initialize the list that will hold both the directories and files
                found_items = []
                for item in walk_generator:
                    if self.stop_flag:
                        return
                    base_directory = item[0]
                    for _dir in item[1]:
                        found_items.append(os.path.join(base_directory, _dir).replace("\\", "/"))
                    for file in item[2]:
                        found_items.append(os.path.join(base_directory, file).replace("\\", "/"))
                self.finished.emit(found_items)
        
        def completed(items):
            #Add the items to the treeview
            self._add_items_to_tree(tree_model, directory, items)
        
        if self.worker_thread is not None:
            self.worker_thread.wait()
        self._parent._set_wait_animation(self._parent.indexOf(self), True)
        self.worker_thread = ProcessThread()
        self.worker_thread.setTerminationEnabled(True)
        self.worker_thread.finished.connect(completed)
        self.worker_thread.start()

    def display_found_files(self, search_text, found_files, directory):
        """
        Display files that were found using the 'functions' module's
        find_files function
        """
        #Check if found files are valid
        if found_files == None:
            self.main_form.display.repl_display_message(
                "Error in finding files!", 
                message_type=data.MessageType.WARNING
            )
            return
        #Set the tree display type to FILES
        self.set_display_type(data.TreeDisplayType.FILES)
        #Initialize and display the search options
        tree_model = self._init_found_files_options(search_text, directory)
        #Sort the found file list
        found_files.sort(key=str.lower)
        #Add the items to the treeview
        self._add_items_to_tree(tree_model, directory, found_files)
    
    def display_found_files_with_lines(self,
                                       search_title,
                                       search_text,
                                       search_dir,
                                       case_sensitive,
                                       search_subdirs,
                                       break_on_find,
                                       file_filter):
        """
        Display files with lines that were found using the 'functions' 
        module's find_in_files function
        """
        # Set the tree display type to NODE
        self.set_display_type(data.TreeDisplayType.FILES_WITH_LINES)
        # Initialize and display the search options
        tree_model = self._init_found_files_options(search_title, search_dir)
        
        class ProcessThread(data.QThread):
            finished = data.pyqtSignal(dict)
            error = data.pyqtSignal(str)
            stop_flag = False
                
            def stop(self):
                self.stop_flag = True
            
            def run(self):
                # Initialize the list that will hold both the directories and files
                found_items = functions.find_files_with_text_enum(
                    search_text,
                    search_dir,
                    case_sensitive,
                    search_subdirs,
                    break_on_find,
                    file_filter,
                )
                if isinstance(found_items, dict):
                    self.finished.emit(found_items)
                else:
                    self.error.emit(found_items)
        
        def reset():
            # Resize the header so the horizontal scrollbar will have the correct width
            self.resize_horizontal_scrollbar()
            # Hide the wait animation
            if self._parent is not None:
                self._parent._set_wait_animation(self._parent.indexOf(self), False)
        
        def completed(found_items):
            # Check if the TreeDisplay underlying C++ object is alive
            if self._parent is None:
                reset()
                return
            # Check of the function return is valid
            if found_items == {}:
                message = "No files found!"
                # Check if any files were found
                self.main_form.display.repl_display_message(
                    message, 
                    message_type=data.MessageType.WARNING
                )
                self.main_form.display.write_to_statusbar(message, 2000)
                # Display error in tree widget
                brush = data.QBrush(
                    data.QColor(data.theme["fonts"]["error"]["color"])
                )
                font = data.QFont(
                    data.current_font_name, data.current_font_size, data.QFont.Weight.Bold
                )
                error_item  = data.QStandardItem(message)
                error_item.setEditable(False)
                error_item.setForeground(brush)
                error_item.setFont(font)
                tree_model.appendRow(error_item)
                reset()
                return
            # Add the items with lines to the treeview
            self._add_items_with_lines_to_tree(tree_model, search_dir, found_items)
            reset()
        
        def error(message):
            # Check if any files were found
            self.main_form.display.repl_display_error(message)
            self.main_form.display.write_to_statusbar(message, 2000)
            # Display error in tree widget
            brush = data.QBrush(
                data.QColor(data.theme["fonts"]["error"]["color"])
            )
            font = data.QFont(
                data.current_font_name, data.current_font_size, data.QFont.Weight.Bold
            )
            error_item  = data.QStandardItem(message)
            error_item.setEditable(False)
            error_item.setForeground(brush)
            error_item.setFont(font)
            tree_model.appendRow(error_item)
            reset()
            return
        
        if self.worker_thread is not None:
            self.worker_thread.stop()
            self.worker_thread.wait()
        self._parent._set_wait_animation(self._parent.indexOf(self), True)
        self.worker_thread = ProcessThread()
        self.worker_thread.setTerminationEnabled(True)
        self.worker_thread.finished.connect(completed)
        self.worker_thread.error.connect(error)
        self.worker_thread.start()
    
    def display_replacements_in_files(self, 
                                      search_text, 
                                      replace_text, 
                                      replaced_files, 
                                      directory):
        """
        Display files with lines that were replaces using the 'functions' 
        module's replace_text_in_files_enum function
        """
        #Check if found files are valid
        if replaced_files == None:
            self.main_form.display.repl_display_message(
                "Error in finding files!", 
                message_type=data.MessageType.WARNING
            )
            return
        #Set the tree display type to NODE
        self.set_display_type(data.TreeDisplayType.FILES_WITH_LINES)
        #Initialize and display the search options
        tree_model = self._init_replace_in_files_options(search_text, replace_text, directory)
        #Add the items with lines to the treeview
        self._add_items_with_lines_to_tree(tree_model, directory, replaced_files)


##
##  Tree display for viewing/editing the filesystem
##

import os
import enum
import types
import shutil
import traceback
import data
import functions
import components
if data.platform == "Windows":
    import win32api, win32con

class TreeDisplayBase(data.QTreeView):
    # Signals
    key_release_signal = data.pyqtSignal(str, dict)
    
    # Class variables
    _parent = None
    main_form = None
    name = ""
    savable = data.CanSave.NO
    tree_menu = None
    icon_manipulator = None
    key_release_lock = None
    
    
    def __del__(self):
        try:
            self.clean_up()
        except Exception as ex:
            print(ex)
    
    def clean_up(self):
        model = self.model()
        if model:
            root = model.invisibleRootItem()
            for item in self.iterate_items(root):
                if item == None:
                    continue
                item.setData(None)
                for row in range(item.rowCount()):
                    item.removeRow(row)
                for col in range(item.columnCount()):
                    item.removeRow(col)
                    
        # Clean up the tree model
        self._clean_model()
        # Disconnect signals
        try:
            self.doubleClicked.disconnect()
        except:
            pass
        try:
            self.expanded.disconnect()
        except:
            pass
        self._parent = None
        self.main_form = None
        self.icon_manipulator = None
        if self.tree_menu is not None:
            self.tree_menu.setParent(None)
            self.tree_menu = None
        # Clean up self
        self.setParent(None)
        self.deleteLater()
    
    
    def __init__(self, parent, main_form, name):
        # Initialize the superclass
        super().__init__(parent)
        # Set default font
        self.setFont(data.get_current_font())
        # Initialize everything else
        self._parent = parent
        self.main_form = main_form
        self.name = name
        self.icon_manipulator = components.IconManipulator()
        self.key_release_lock = False
        # Set the icon size for every node
        self.update_icon_size()
        # Set the nodes to be animated on expand/contract
        self.setAnimated(True)
        # Disable node expansion on double click
        self.setExpandsOnDoubleClick(False)
        # Install event filter
        self.installEventFilter(self)
    
    def eventFilter(self, object, event):
        if not self.key_release_lock:
            # Check for keyboard releases
            if event.type() == data.QEvent.Type.KeyRelease:
                key = data.keys[event.key()]
                modifiers = event.modifiers()
                modifier_shift = (modifiers & data.Qt.KeyboardModifier.ShiftModifier) == data.Qt.KeyboardModifier.ShiftModifier
                modifier_control = (modifiers & data.Qt.KeyboardModifier.ControlModifier) == data.Qt.KeyboardModifier.ControlModifier
                modifier_alt = (modifiers & data.Qt.KeyboardModifier.AltModifier) == data.Qt.KeyboardModifier.AltModifier
                modifier_meta = (modifiers & data.Qt.KeyboardModifier.MetaModifier) == data.Qt.KeyboardModifier.MetaModifier
                modifier_keypad = (modifiers & data.Qt.KeyboardModifier.KeypadModifier) == data.Qt.KeyboardModifier.KeypadModifier
                modifier_dict = {
                    "shift": modifier_shift,
                    "control": modifier_control,
                    "alt": modifier_alt,
                    "meta": modifier_meta,
                    "keypad": modifier_keypad,
                }
                # Emit a signal for a keyrelease
                self.key_release_signal.emit(key, modifier_dict)
        
        return super().eventFilter(object, event)
    
    """
    Private/Internal functions
    """
    def _create_standard_item(self, text, bold=False, icon=None):
        # Font
#        brush = data.QBrush(data.QColor(data.theme["fonts"]["keyword"]["color"]))
        font = data.get_current_font()
        font.setBold(bold)
        # Item initialization
        item = data.QStandardItem(text)
        item.setEditable(False)
#        item.setForeground(brush)
        item.setFont(font)
        # Set icon if needed
        if icon is not None:
            item.setIcon(icon)
        return item
    
    def _create_menu(self):
        self.tree_menu = Menu(self)
        self.default_menu_font = self.tree_menu.font()
        self.customize_context_menu()
        return self.tree_menu
    
    def _clean_model(self):
        if self.model() is not None:
            self.model().setParent(None)
            self.setModel(None)
    
    def _check_contents(self):
        #Update the horizontal scrollbar width
        self._resize_horizontal_scrollbar()
    
    def _resize_horizontal_scrollbar(self):
        """
        Resize the header so the horizontal scrollbar will have the correct width
        """
        for i in range(self.model().rowCount()):
            self.resizeColumnToContents(i)
    
    def _lock_key_release(self):
        self.key_release_lock = True
    
    def _unlock_key_release(self):
        self.key_release_lock = False
    
    """
    Overridden functions
    """
    def setFocus(self):
        """
        Overridden focus event
        """
        # Execute the supeclass focus function
        super().setFocus()
        # Check indication
        self.main_form.view.indication_check()
    
    def mousePressEvent(self, event):
        """Function connected to the clicked signal of the tree display"""
        super().mousePressEvent(event)
        # Clear the selection if the index is invalid
        index = self.indexAt(event.pos())
        if index.isValid() == False:
            self.clearSelection()
        # Set the focus
        self.setFocus()
        # Set the last focused widget to the parent basic widget
        self.main_form.last_focused_widget = self._parent
        # Set Save/SaveAs buttons in the menubar
        self._parent._set_save_status()
        # Reset the click&drag context menu action
        components.ActionFilter.clear_action()
    
    
    """
    Public functions
    """
    def update_styles(self):
        self.update_icon_size()
        self.setFont(data.get_current_font())
    
    def update_icon_size(self):
        self.setIconSize(
            functions.create_size(
                data.tree_display_icon_size, 
                data.tree_display_icon_size
            )
        )

    def _customize_context_menu(self, menu, default_menu_font):
        """
        This needs to be called in a subclass as needed
        """
        if data.custom_menu_scale is not None and data.custom_menu_font is not None:
            components.TheSquid.customize_menu_style(menu)
            font = data.get_current_font()
            if menu is not None:
                menu.setFont(font)
            # Recursively change the fonts of all items
            root = self.model().invisibleRootItem()
            for item in self.iterate_items(root):
                if item == None:
                    continue
                font.setBold(item.font().bold())
                item.setFont(font)
        else:
            if default_menu_font == None:
                return
            components.TheSquid.customize_menu_style(menu)
            if menu is not None:
                menu.setFont(default_menu_font)
            # Recursively change the fonts of all items
            root = self.model().invisibleRootItem()
            for item in self.iterate_items(root):
                if item == None:
                    continue
                default_menu_font.setBold(item.font().bold())
                item.setFont(default_menu_font)
    
    def iterate_items(self, root):
        """
        Iterator that returns all tree items recursively
        """
        if root is not None:
            stack = [root]
            while stack:
                parent = stack.pop(0)
                for row in range(parent.rowCount()):
                    for column in range(parent.columnCount()):
                        child = parent.child(row, column)
                        yield child
                        if child is not None:
                            if child.hasChildren():
                                stack.append(child)

class TreeExplorer(TreeDisplayBase):
    # Item type enumeration
    class ItemType(enum.Enum):
        FILE = 0
        DIRECTORY = 1
        BASE_DIRECTORY = 2
        ONE_UP_DIRECTORY = 3
        DISK = 4
        NEW_FILE = 5
        NEW_DIRECTORY = 6
        RENAME_FILE = 7
        RENAME_DIRECTORY = 8
        COMPUTER = 9
    
    # Signals
    open_file_signal = data.pyqtSignal(str)
    open_file_hex_signal = data.pyqtSignal(str)
    open_directory_signal = data.pyqtSignal()
    
    # Attributes
    current_viewed_directory = None
    default_menu_font = None
    base_item = None
    added_item = None
    renamed_item = None
    cut_items = None
    copy_items = None
    
    def __init__(self, parent, main_form):
        # Initialize the superclass
        super().__init__(parent, main_form, "Tree Explorer")
        self.setAnimated(True)
        self.setObjectName("TreeExplorer")
        self.setSelectionMode(data.QAbstractItemView.SelectionMode.ExtendedSelection)
        # Icons
        self.project_icon = functions.create_icon("tango_icons/sessions.png")
        self.file_icon = functions.create_icon("tango_icons/file.png")
        self.folder_icon = functions.create_icon("tango_icons/document-open.png")
        self.disk_icon = functions.create_icon("tango_icons/harddisk.png")
        self.computer = functions.create_icon("tango_icons/computer.png")
        self.goto_icon = functions.create_icon('tango_icons/edit-goto.png')
        # Connect signals
        self.doubleClicked.connect(self._item_double_click)
        self.key_release_signal.connect(self.__keyrelease_slot)
    
    @data.pyqtSlot(str, dict)
    def __keyrelease_slot(self, key, modifiers):
#        print(key, modifiers)
        # Copy
        if key == "Key_C" and modifiers["control"] == True:
            self.__copy_items()
        
        # Cut
        if key == "Key_X" and modifiers["control"] == True:
            self.__cut_items()
        
        # Paste
        if key == "Key_V" and modifiers["control"] == True:
            self.__paste_items()
        
        # delete
        if key == "Key_Delete":
            self.__delete_items()
    
    def _init_tree_model(self):
        self.horizontalScrollbarAction(1)
        self.setSelectionBehavior(data.QAbstractItemView.SelectionBehavior.SelectRows)
        tree_model = data.QStandardItemModel()
        tree_model.setHorizontalHeaderLabels(["TREE FILE EXPLORER"])
        self.header().hide()
        self._clean_model()
        self.setModel(tree_model)
        self.setUniformRowHeights(True)
        return tree_model
    
    def _create_item_attribute(self, 
                               itype, 
                               path, 
                               hidden=False, 
                               disk=False,
                               hide_menu=False):
        return types.SimpleNamespace(
            itype=itype,
            path=path,
            hidden=hidden,
            disk=disk,
            hide_menu=hide_menu
        )
    
    def _is_hidden_item(self, item):
        try:
            if data.platform == "Windows":
                # Windows
                attribute = win32api.GetFileAttributes(item)
                hidden = (
                    attribute & 
                    (win32con.FILE_ATTRIBUTE_HIDDEN | 
                        win32con.FILE_ATTRIBUTE_SYSTEM)
                )
            else:
                # Linux / OSX
                hidden = os.path.basename(item).startswith('.')
            return hidden
        except:
            return False
    
    def start_editing_item(self, index):
        self._lock_key_release()
        self.edit(index)
    
    def closeEditor(self, *args):
        widget = args[0]
        self.__item_editing_closed(widget)
        return super().closeEditor(*args)
    
    def commitData(self, editor):
        self.__commit_data(editor)
        return super().commitData(editor)
    
    def __commit_data(self, editor):
        searched_item = editor.text()
        root = self.model().invisibleRootItem()
        for it in self.iterate_items(root):
            if it.text() == searched_item and it.attributes.itype == TreeExplorer.ItemType.FILE:
                self.setCurrentIndex(it.index())
                break
            elif it.text() == searched_item and it.attributes.itype == TreeExplorer.ItemType.DIRECTORY:
                self.setCurrentIndex(it.index())
                break
    
    def __item_editing_closed(self, widget):
        """
        Signal that fires when editing was canceled/ended
        """
#        print(widget.text())
#        self.display_directory(self.current_viewed_directory)
        # Check if the directory name is valid
        if self.added_item is not None and self.added_item.text() == "":
            self.base_item.removeRow(self.added_item.row())
            self.added_item = None
        elif self.renamed_item is not None:
#            self.renamed_item.setEditable(False)
            self.renamed_item = None
        self._unlock_key_release()
    
    def _item_changed(self, item):
        """
        Callback connected to the displays 
        QStandardItemModel 'itemChanged' signal
        """
#        print("Changed item:\n    ", str(item))
        if not hasattr(item, "attributes"):
            return
        if (item.attributes.itype == TreeExplorer.ItemType.RENAME_FILE or
            item.attributes.itype == TreeExplorer.ItemType.RENAME_DIRECTORY):
            # Reset the type first
            if item.attributes.itype == TreeExplorer.ItemType.RENAME_DIRECTORY:
                item.attributes.itype = TreeExplorer.ItemType.DIRECTORY
                item_text = "Directory"
            else:
                item.attributes.itype = TreeExplorer.ItemType.FILE
                item_text = "File"
            # Initialize the names
            old_name = item.attributes.path
            new_name = os.path.join(
                os.path.dirname(item.attributes.path),
                item.text()
            )
            # Check if the names are different
            old_name = functions.unixify_path(old_name)
            new_name = functions.unixify_path(new_name)
            if old_name == new_name:
                return
            # Check if an item with the same name as the
            # renamed item already exists
            item.setEditable(False)
            if os.path.exists(new_name):
                self.main_form.display.repl_display_message(
                    "{} '{}' already exits!".format(item_text, new_name),
                    message_type=data.MessageType.ERROR
                )
                self.display_directory(self.current_viewed_directory)
                return
            # Rename the item
            try:
                os.rename(old_name, new_name)
                item.attributes.path = new_name
                self.main_form.display.repl_display_message(
                    "Renamed {}:\n    '{}'\n  to:\n    '{}'!".format(
                        item_text.lower(), old_name, new_name),
                    message_type=data.MessageType.SUCCESS
                )
            except:
                self.main_form.display.repl_display_message(
                    "Error while renaming {}: '{}'!".format(
                        item_text.lower(), item.attributes.path),
                    message_type=data.MessageType.ERROR
                )
                self.display_directory(self.current_viewed_directory)
                return
            # Finish editing and reset the view
            self.renamed_item = None
            self.display_directory(self.current_viewed_directory)
            
        elif (item.attributes.itype == TreeExplorer.ItemType.NEW_DIRECTORY or
              item.attributes.itype == TreeExplorer.ItemType.NEW_FILE):
            path = os.path.join(item.attributes.path, item.text())
            item.attributes.path = functions.unixify_path(path)
            if item.attributes.itype == TreeExplorer.ItemType.NEW_DIRECTORY:
                item.attributes.itype = TreeExplorer.ItemType.DIRECTORY
                item_text = "Directory"
            else:
                item.attributes.itype = TreeExplorer.ItemType.FILE
                item_text = "File"
            if os.path.exists(item.attributes.path):
                self.base_item.removeRow(item.index())
                self.main_form.display.repl_display_message(
                    "{} '{}' already exits!".format(
                        item_text, item.attributes.path),
                    message_type=data.MessageType.ERROR
                )
                return
            # Create the directory
            try:
                if item.attributes.itype == TreeExplorer.ItemType.DIRECTORY:
                    os.mkdir(item.attributes.path)
                else:
                    open(item.attributes.path, 'a').close()
                self.main_form.display.repl_display_message(
                    "Created {}: '{}'!".format(
                        item_text.lower(), item.attributes.path),
                    message_type=data.MessageType.SUCCESS
                )
            except:
                self.base_item.removeRow(item.index())
                self.main_form.display.repl_display_message(
                    "Error while creating {}: '{}'!".format(
                        item_text.lower(), item.attributes.path),
                    message_type=data.MessageType.ERROR
                )
                return
            # Finish editing and reset the view
            item.setEditable(False)
            self.added_item = None
            self.display_directory(self.current_viewed_directory)
    
    def _item_right_click(self, model_index):
        item = self.model().itemFromIndex(model_index)
        cursor = data.QCursor.pos()  
        # Clean up the menu if needed
        if self.tree_menu is not None:
            self.tree_menu.setParent(None)
            self.tree_menu.deleteLater()
        # Initialize the menu
        self.tree_menu = Menu(self)
        self.default_menu_font = self.tree_menu.font()
        self.customize_context_menu()
        
        # First check if the click was in an empty space
        # and create item actions accordingly
        if item is not None:
            # Open the current item
            def open_item():
                self._open_item(item)
            title = "Open directory"
            icon = 'tango_icons/document-open.png'
            if hasattr(item, "attributes") == False:
                return
            elif item.attributes.hide_menu == True:
                return
            if item.attributes.itype == TreeExplorer.ItemType.FILE:
                title = "Open file"
                icon = 'tango_icons/document-open.png'
            open_action = data.QAction(title, self.tree_menu)
            open_action.triggered.connect(open_item)
            icon = functions.create_icon(icon)
            open_action.setIcon(icon)
            if item.attributes.itype in [TreeExplorer.ItemType.FILE, 
                                         TreeExplorer.ItemType.DIRECTORY]:
                self.tree_menu.addAction(open_action)
            # Open with system
            def open_system():
                if data.platform == 'Windows':
                    os.startfile(item.attributes.path)
                else:
                    subprocess.call(["xdg-open", item.attributes.path])
            if item.attributes.itype == TreeExplorer.ItemType.FILE:
                action_open_system = data.QAction("Open with system", self.tree_menu)
                action_open_system.triggered.connect(open_system)
                icon = functions.create_icon('tango_icons/open-with-default-app.png')
                action_open_system.setIcon(icon)
                self.tree_menu.addAction(action_open_system)
                def open_hex():
                    if item.attributes.itype == TreeExplorer.ItemType.FILE:
                        file_path = item.attributes.path
                        self.open_file_hex_signal.emit(file_path)
                    else:
                        self.main_form.display.repl_display_error(
                            "Item of type '{}' cannot be opened in the Hex-View!".format(
                                item.attributes.itype
                            )
                        )
                action_open_hex = data.QAction("Open with Hex-View", self.tree_menu)
                action_open_hex.triggered.connect(open_hex)
                icon = functions.create_icon('various/node_template.png')
                action_open_hex.setIcon(icon)
                self.tree_menu.addAction(action_open_hex)
                # Open path in explorer
                open_in_explorer_action = data.QAction("Open in explorer", self)
                def open_in_explorer():
                    path = item.attributes.path
                    try:
                        result = functions.open_item_in_explorer(path)
                    except:
                        result = False
                    if result == False:
                        main_form.display.repl_display_error(
                            "Error opening path in explorer: {}".format(path)
                        )
                open_in_explorer_action.setIcon(
                    functions.create_icon('tango_icons/document-open.png')
                )
                open_in_explorer_action.triggered.connect(open_in_explorer)
                self.tree_menu.addAction(open_in_explorer_action)
            elif item.attributes.itype == TreeExplorer.ItemType.DIRECTORY:
                action_open_system = data.QAction("Open in explorer", self.tree_menu)
                action_open_system.triggered.connect(open_system)
                icon = functions.create_icon('tango_icons/system-show-cwd-tree.png')
                action_open_system.setIcon(icon)
                self.tree_menu.addAction(action_open_system)
            
            # Copy item name to clipboard
            def copy_item_name_to_clipboard():
                text = os.path.basename(item.attributes.path)
                cb = data.application.clipboard()
                cb.clear(mode=cb.Mode.Clipboard)
                cb.setText(text, mode=cb.Mode.Clipboard)
                self.main_form.display.repl_display_message(
                    "Copied to clipboard: \"{}\"".format(text)
                )
            action_copy_clipboard = data.QAction(
                "Copy item name to clipboard", self.tree_menu
            )
            action_copy_clipboard.triggered.connect(
                copy_item_name_to_clipboard
            )
            icon = functions.create_icon('tango_icons/edit-copy.png')
            action_copy_clipboard.setIcon(icon)
            if item.attributes.itype in [TreeExplorer.ItemType.FILE, 
                                         TreeExplorer.ItemType.DIRECTORY]:
                self.tree_menu.addAction(action_copy_clipboard)
            # Copy item path to clipboard
            def copy_item_path_to_clipboard():
                text = item.attributes.path
                cb = data.application.clipboard()
                cb.clear(mode=cb.Mode.Clipboard)
                cb.setText(text, mode=cb.Mode.Clipboard)
                self.main_form.display.repl_display_message(
                    "Copied to clipboard: \"{}\"".format(text)
                )
            action_copy_clipboard = data.QAction(
                "Copy item path to clipboard", self.tree_menu
            )
            action_copy_clipboard.triggered.connect(
                copy_item_path_to_clipboard
            )
            icon = functions.create_icon('tango_icons/edit-copy.png')
            action_copy_clipboard.setIcon(icon)
            if item.attributes.itype in [TreeExplorer.ItemType.FILE, 
                                         TreeExplorer.ItemType.DIRECTORY]:
                self.tree_menu.addAction(action_copy_clipboard)
            # Update current working directory
            def update_cwd():
                if item.attributes.itype == TreeExplorer.ItemType.FILE:
                    path = os.path.dirname(item.attributes.path)
                else:
                    path = item.attributes.path
                self.main_form.set_cwd(path)
            title = "Update CWD"
            if item.attributes.itype == TreeExplorer.ItemType.FILE:
                title = "Update CWD to parent directory"
            action_update_cwd = data.QAction(title, self.tree_menu)
            action_update_cwd.triggered.connect(update_cwd)
            icon = functions.create_icon('tango_icons/update-cwd.png')
            action_update_cwd.setIcon(icon)
            if item.attributes.itype in [TreeExplorer.ItemType.FILE, 
                                         TreeExplorer.ItemType.DIRECTORY,
                                         TreeExplorer.ItemType.BASE_DIRECTORY]:
                self.tree_menu.addAction(action_update_cwd)
            # Separator
            self.tree_menu.addSeparator()
            # Cut item
            cut_items_action = data.QAction(
                "Cut", self.tree_menu
            )
            cut_items_action.triggered.connect(self.__cut_items)
            icon = functions.create_icon('tango_icons/edit-cut.png')
            cut_items_action.setIcon(icon)
            if item.attributes.itype in [TreeExplorer.ItemType.FILE, 
                                         TreeExplorer.ItemType.DIRECTORY]:
                self.tree_menu.addAction(cut_items_action)
            # Copy item
            copy_item_action = data.QAction(
                "Copy", self.tree_menu
            )
            copy_item_action.triggered.connect(self.__copy_items)
            icon = functions.create_icon('tango_icons/edit-copy.png')
            copy_item_action.setIcon(icon)
            if item.attributes.itype in [TreeExplorer.ItemType.FILE, 
                                         TreeExplorer.ItemType.DIRECTORY]:
                self.tree_menu.addAction(copy_item_action)
            # Paste item
            paste_item_action = data.QAction(
                "Paste", self.tree_menu
            )
            paste_item_action.triggered.connect(self.__paste_items)
            icon = functions.create_icon('tango_icons/edit-paste.png')
            paste_item_action.setIcon(icon)
            if item.attributes.itype in [TreeExplorer.ItemType.FILE,
                                         TreeExplorer.ItemType.DIRECTORY,
                                         TreeExplorer.ItemType.BASE_DIRECTORY]:
                if TreeExplorer.cut_items is not None or TreeExplorer.copy_items is not None:
                    self.tree_menu.addAction(paste_item_action)
            # Separator
            self.tree_menu.addSeparator()
            # Rename item
            def rename_item():
                if len(self.selectedIndexes()) > 1:
                    self.main_form.display.display_warning(
                        "Renaming allows only one item at a time!"
                    )
                    return
                item.setEditable(True)
                if item.attributes.itype == TreeExplorer.ItemType.DIRECTORY:
                    item.attributes.itype = TreeExplorer.ItemType.RENAME_DIRECTORY
                else:
                    item.attributes.itype = TreeExplorer.ItemType.RENAME_FILE
                index = item.index()
                self.scrollTo(index)
                # Start editing the new empty directory name
                self.start_editing_item(index)
                self.renamed_item = item
            rename_item_action = data.QAction(
                "Rename", self.tree_menu
            )
            rename_item_action.triggered.connect(rename_item)
            icon = functions.create_icon('tango_icons/delete-end-line.png')
            rename_item_action.setIcon(icon)
            if item.attributes.itype in [TreeExplorer.ItemType.FILE, 
                                         TreeExplorer.ItemType.DIRECTORY]:
                self.tree_menu.addAction(rename_item_action)
            # Delete item
            delete_item_action = data.QAction(
                "Delete", self.tree_menu
            )
            delete_item_action.triggered.connect(self.__delete_items)
            icon = functions.create_icon('tango_icons/session-remove.png')
            delete_item_action.setIcon(icon)
            if item.attributes.itype in [TreeExplorer.ItemType.FILE, 
                                         TreeExplorer.ItemType.DIRECTORY]:
                self.tree_menu.addAction(delete_item_action)
        else:
            # Paste item
            paste_item_action = data.QAction(
                "Paste", self.tree_menu
            )
            paste_item_action.triggered.connect(self.__paste_items)
            icon = functions.create_icon('tango_icons/edit-paste.png')
            paste_item_action.setIcon(icon)
            if TreeExplorer.cut_items is not None or TreeExplorer.copy_items is not None:
                self.tree_menu.addAction(paste_item_action)
        # Add the actions that are on every menu
        # Separator
        self.tree_menu.addSeparator()
        # New file
        def refresh():
            self.display_directory(self.current_viewed_directory)
        refresh_action = data.QAction(
            "Refresh view", self.tree_menu
        )
        refresh_action.triggered.connect(refresh)
        icon = functions.create_icon('tango_icons/view-refresh.png')
        refresh_action.setIcon(icon)
        self.tree_menu.addAction(refresh_action)
        # New file
        def new_file():
            # Get the path
            path = self.current_viewed_directory
            # Create a new file item for editing
            create_file_item = self._create_standard_item(
                    "", bold=False, icon=self.file_icon
            )
            create_file_item.attributes = self._create_item_attribute(
                TreeExplorer.ItemType.NEW_FILE,
                path
            )
            create_file_item.setEditable(True)
            self.base_item.appendRow(create_file_item)
            self.added_item = create_file_item
            index = create_file_item.index()
            self.scrollTo(index)
            # Start editing the new empty file name
            self.start_editing_item(index)
        new_file_action = data.QAction(
            "New file", self.tree_menu
        )
        new_file_action.triggered.connect(new_file)
        icon = functions.create_icon('tango_icons/document-new.png')
        new_file_action.setIcon(icon)
        self.tree_menu.addAction(new_file_action)
        # New directory
        def new_directory():
            # Get the path
            path = self.current_viewed_directory
            # Create a new directory item for editing
            create_directory_item = self._create_standard_item(
                    "", bold=False, icon=self.folder_icon
            )
            create_directory_item.attributes = self._create_item_attribute(
                TreeExplorer.ItemType.NEW_DIRECTORY,
                path
            )
            create_directory_item.setEditable(True)
            self.base_item.appendRow(create_directory_item)
            self.added_item = create_directory_item
            index = create_directory_item.index()
            self.scrollTo(index)
            # Start editing the new empty directory name
            self.start_editing_item(index)
            
        new_directory_action = data.QAction(
            "New Directory", self.tree_menu
        )
        new_directory_action.triggered.connect(new_directory)
        icon = functions.create_icon('tango_icons/folder-new.png')
        new_directory_action.setIcon(icon)
        self.tree_menu.addAction(new_directory_action)
        # Show the menu
        self.tree_menu.popup(cursor)
    
    def __paste_items(self):
        if TreeExplorer.cut_items is not None:
            items = TreeExplorer.cut_items
        elif TreeExplorer.copy_items is not None:
            items = TreeExplorer.copy_items
        else:
            self.main_form.display.display_error(
                "Copy AND Cut items list is empty!\n" +
                "Cannot perform this action!"
            )
            return
        for it in items:
            path = it.path
            itype = it.itype
            # Setup the directory
            base_name = os.path.basename(path)
            new_path = os.path.join(
                self.current_viewed_directory,
                base_name
            )
            if itype == TreeExplorer.ItemType.DIRECTORY:
                if os.path.exists(new_path):
                    message = "The PASTE directory already exists! "
                    message += "Do you wish to overwrite it?"
                    reply = YesNoDialog.question(message)
                    if reply != data.DialogResult.Yes.value:
                        return
                if os.path.isdir(new_path):
                    shutil.rmtree(new_path)
                    time.sleep(0.1)
                shutil.copytree(path, new_path)
                if TreeExplorer.cut_items is not None:
                    shutil.rmtree(path)
            else:
                if os.path.exists(new_path):
                    message = "The PASTE file already exists! "
                    message += "Do you wish to overwrite it?"
                    reply = YesNoDialog.question(message)
                    if reply != data.DialogResult.Yes.value:
                        return
                shutil.copy(path, new_path)
                if TreeExplorer.cut_items is not None:
                    os.remove(path)
        if TreeExplorer.cut_items is not None:
            TreeExplorer.cut_items = None
            TreeExplorer.copy_items = None
        self.display_directory(self.current_viewed_directory)
    
    def __copy_items(self):
        items = []
        for i in self.selectedIndexes():
            it = self.model().itemFromIndex(i)
            if it.attributes.itype in [TreeExplorer.ItemType.FILE, 
                                        TreeExplorer.ItemType.DIRECTORY]:
                items.append(it.attributes)
        if len(items) == 0:
            self.main_form.display.repl_display_message(
                "Nothing selected to copy!"
            )
            return
        TreeExplorer.cut_items = None
        TreeExplorer.copy_items = items
        self.main_form.display.repl_display_message(
            "Copied items:"
        )
        for i in items:
            self.main_form.display.repl_display_message(
                "  {}: \"{}\"".format(
                    i.itype.name.lower(),
                    i.path
                )
            )
    
    def __cut_items(self):
        items = []
        for i in self.selectedIndexes():
            it = self.model().itemFromIndex(i)
            if it.attributes.itype in [TreeExplorer.ItemType.FILE, 
                                        TreeExplorer.ItemType.DIRECTORY]:
                items.append(it.attributes)
        TreeExplorer.cut_items = items
        TreeExplorer.copy_items = None
        self.main_form.display.repl_display_message(
            "Cut items:"
        )
        for i in items:
            self.main_form.display.repl_display_message(
                "  {}: \"{}\"".format(
                    i.itype.name.lower(),
                    i.path
                )
            ) 
    
    def __delete_items(self):
        items = []
        for i in self.selectedIndexes():
            item = self.model().itemFromIndex(i)
            items.append(item.attributes)
        message = "Are you sure you want to delete the {} selected items?".format(len(items))
        reply = YesNoDialog.question(message)
        if reply != data.DialogResult.Yes.value:
            return
        for it in items:
            path = it.path
            try:
                if os.path.exists(path):
                    if os.path.isdir(path):
                        shutil.rmtree(path)
                    else:
                        os.remove(path)
                    self.display_directory(self.current_viewed_directory)
                else:
                    self.main_form.display.repl_display_message(
                        "Item '{}'\n does not seem to exist!!".format(
                            item.attributes.path),
                        message_type=data.MessageType.WARNING
                    )
            except:
                self.main_form.display.repl_display_message(
                    traceback.format_exc(),
                    message_type=data.MessageType.ERROR
                )

    def __open_items(self, model_index=None):
        try:
            if model_index is not None:
                indexes = (model_index, )
            else:
                indexes = self.selectedIndexes()
            for i in indexes:
                item = self.model().itemFromIndex(i)
                self._open_item(item)
        except:
            self.main_form.display.repl_display_error(
                traceback.format_exc()
            )
    
    def _item_double_click(self, model_index):
        self.__open_items(model_index)
    
    def _open_item(self, item):
        if hasattr(item, "attributes") == False:
            index = item.index()
            if self.isExpanded(index):
                self.collapse(index)
            else:
                self.expand(index)
            return
        if item.attributes.itype in [TreeExplorer.ItemType.DIRECTORY, 
                                     TreeExplorer.ItemType.ONE_UP_DIRECTORY]:
            # Store previous directory
            previous_directory = self.current_viewed_directory
            # Clean and display the new directory
            self._clean_model()
            self.display_directory(
                item.attributes.path, 
                disk=item.attributes.disk
            )
            if item.attributes.itype == TreeExplorer.ItemType.ONE_UP_DIRECTORY:
                try:
                    # Select the ascending sub-directory
                    base_name = os.path.split(previous_directory)[1]
                    root = self.model().invisibleRootItem()
                    for it in self.iterate_items(root):
                        if it.text() == base_name:
                            self.setCurrentIndex(it.index())
                except:
                    traceback.print_exc()
        if item.attributes.itype == TreeExplorer.ItemType.FILE:    
            self.open_file_signal.emit(item.attributes.path)
        if item.attributes.itype == TreeExplorer.ItemType.DISK:    
            if data.platform == "Windows":
                self.display_windows_disks()
    
    def display_windows_disks(self):
        self._clean_model()
        tree_model = self._init_tree_model()
        base_item = self._create_standard_item(
            "Computer", bold=False, icon=self.computer
        )
        base_item.attributes = self._create_item_attribute(
            TreeExplorer.ItemType.COMPUTER,
            None
        )
        tree_model.appendRow(base_item)
        drives = win32api.GetLogicalDriveStrings()
        drives = drives.split('\000')[:-1]
        for d in drives:
            d = functions.unixify_path(d)
            item = self._create_standard_item(
                d, bold=False, icon=self.disk_icon
            )
            item.attributes = self._create_item_attribute(
                TreeExplorer.ItemType.DIRECTORY,
                d,
                disk=True
            )
            base_item.appendRow(item)
        self.base_item = base_item
        # Set the tree model
        self.setModel(tree_model)
        # Connect the signals
        tree_model.itemChanged.connect(self._item_changed)
        # Expand the base item
        self.expand(base_item.index())

    def _create_directory_list(self, directory):
        dir_items = []
        file_items = []
        dir_list = os.listdir(directory)
        for i in dir_list:
            full_path = os.path.join(directory, i)
            full_path = functions.unixify_path(full_path)
            hidden = self._is_hidden_item(full_path)
            if os.path.isdir(full_path):
                icon = self.folder_icon
                if hidden:
                    icon = functions.change_icon_opacity(icon, 0.3)
                item = self._create_standard_item(
                    i, bold=False, icon=icon
                )
                item.attributes = self._create_item_attribute(
                    TreeExplorer.ItemType.DIRECTORY,
                    full_path,
                    hidden
                )
                dir_items.append(item)
            else:
                icon = functions.create_language_document_icon_from_path(
                    full_path, check_content=False
                )
                if hidden:
                    icon = functions.change_icon_opacity(icon, 0.3)
                item = self._create_standard_item(
                    i, bold=False, icon=icon
                )
                item.attributes = self._create_item_attribute(
                    TreeExplorer.ItemType.FILE,
                    full_path,
                    hidden
                )
                file_items.append(item)
        dir_items.sort(key=lambda s: s.text().lower())
        file_items.sort(key=lambda s: s.text().lower())
        item_list = dir_items + file_items
        return item_list
                
    
    """
    Overriden events
    """
    def mousePressEvent(self, event):
        # First execute any special routine ...
        if event.button() == data.Qt.MouseButton.RightButton:
            index = self.indexAt(event.pos())
            self._item_right_click(index)
        # ... then call the super-class event
        super().mousePressEvent(event)
                
    
    """
    Public functions
    """
    def display_directory(self, directory, disk=False):
        # Store the directory
        self.current_viewed_directory = directory
        # Create the directory list
        tree_model = self._init_tree_model()
        sd = os.path.splitdrive(directory)
        if disk == True:
            base_item = self._create_standard_item(
                directory, bold=False, icon=self.disk_icon
            )
            base_item.attributes = self._create_item_attribute(
                TreeExplorer.ItemType.DISK,
                directory
            )
            tree_model.appendRow(base_item)
        elif (sd[1] != "" and sd[1] != "\\"):
            parent_dir = os.path.abspath(
                os.path.join(directory, os.pardir)
            )
            base_item = self._create_standard_item(
                functions.unixify_path(directory), 
                bold=False, 
                icon=self.folder_icon
            )
            base_item.attributes = self._create_item_attribute(
                TreeExplorer.ItemType.BASE_DIRECTORY,
                directory
            )
            up_item = self._create_standard_item(
                "..", bold=False, icon=self.folder_icon
            )
            up_item.attributes = self._create_item_attribute(
                TreeExplorer.ItemType.ONE_UP_DIRECTORY,
                parent_dir,
                hide_menu=True
            )
            base_item.appendRow(up_item)
            tree_model.appendRow(base_item)
        else:
            base_item = self._create_standard_item(
                sd[0], bold=False, icon=self.disk_icon
            )
            base_item.attributes = self._create_item_attribute(
                TreeExplorer.ItemType.DISK,
                directory
            )
            tree_model.appendRow(base_item)
        try:
            lst = self._create_directory_list(directory)
            for i in lst:
                base_item.appendRow(i)
        except:
            self.main_form.display.repl_display_message(
                traceback.format_exc(),
                message_type=data.MessageType.ERROR
            )
            self.main_form.display.repl_display_message(
                "Error while parsing directory:\n  '{}'".format(
                    directory),
                message_type=data.MessageType.ERROR
            )
        self.base_item = base_item
        # Set the tree model
        self.setModel(tree_model)
        # Connect the signals
        tree_model.itemChanged.connect(self._item_changed)
        # Expand the base item
        self.expand(base_item.index())
    
    def customize_context_menu(self):
        self._customize_context_menu(
            self.tree_menu, self.default_menu_font
        )

