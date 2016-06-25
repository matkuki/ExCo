
# -*- coding: utf-8 -*-

"""
    Ex.Co. LICENSE :
        This file is part of Ex.Co..

        Ex.Co. is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        Ex.Co. is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with Ex.Co..  If not, see <http://www.gnu.org/licenses/>.


    PYTHON LICENSE :
        "Python" and the Python logos are trademarks or registered trademarks of the Python Software Foundation,
        used by Ex.Co. with permission from the Foundation


    Cython LICENSE:
        Cython is freely available under the open source Apache License


    PyQt4 LICENSE :
        PyQt4 is licensed under the GNU General Public License version 3
    PyQt Alternative Logo LICENSE:
        The PyQt Alternative Logo is licensed under Creative Commons CC0 1.0 Universal Public Domain Dedication


    Qt Logo LICENSE:
        The Qt logo is copyright of Digia Plc and/or its subsidiaries.
        Digia, Qt and their respective logos are trademarks of Digia Corporation in Finland and/or other countries worldwide.


    Tango Icons LICENSE:
        The Tango base icon theme is released to the Public Domain.
        The Tango base icon theme is made possible by the Tango Desktop Project.

    My Tango Style Icons LICENSE:
        The Tango Icons I created are released under the GNU General Public License version 3.
    
    
    Eric6 LICENSE:
        Eric6 IDE is licensed under the GNU General Public License version 3


    Nuitka LICENSE:
        Nuitka is a Python compiler compatible with Ex.Co..
        Nuitka is freely available under the open source Apache License.
"""

##  FILE DESCRIPTION:
##      Various helper PyQt forms used by the forms module

import os
import os.path
import collections
import ast
import inspect
import functools
import difflib
import PyQt4.QtCore
import PyQt4.QtGui
import settings
import functions
import forms
import data


"""
-------------------------------------------------
Module helper functions
-------------------------------------------------
"""
def set_icon(icon_name):
    """
    Module function for initializing and returning an QIcon object
    """
    return   PyQt4.QtGui.QIcon(
                os.path.join(
                    data.resources_directory, 
                    icon_name
                )
            )

def set_pixmap(pixmap_name):
    """
    Module function for initializing and returning an QPixmap object
    """
    return   PyQt4.QtGui.QPixmap(
                os.path.join(
                    data.resources_directory, 
                    pixmap_name
                )
            )

def get_language_file_icon(language_name):
    """
    Module function for getting the programming language icon from the language name
    """
    language_name = language_name.lower()
    if language_name    == "python":
        return set_icon('language_icons/logo_python.png')
    elif language_name  == "cython":
        return set_icon('language_icons/logo_cython.png')
    elif language_name  == "c":
        return set_icon('language_icons/logo_c.png')
    elif language_name  == "c++":
        return set_icon('language_icons/logo_cpp.png')
    elif language_name  == "oberon/modula":
        return set_icon('language_icons/logo_oberon.png')
    elif language_name  == "d":
        return set_icon('language_icons/logo_d.png')
    elif language_name  == "nim":
        return set_icon('language_icons/logo_nim.png')
    elif language_name  == "ada":
        return set_icon('language_icons/logo_ada.png')
    elif language_name  == "cmake":
        return set_icon('language_icons/logo_cmake.png')
    elif language_name  == "css":
        return set_icon('language_icons/logo_css.png')
    elif language_name  == "html":
        return set_icon('language_icons/logo_html.png')
    elif language_name  == "json":
        return set_icon('language_icons/logo_json.png')
    elif language_name  == "lua":
        return set_icon('language_icons/logo_lua.png')
    elif language_name  == "matlab":
        return set_icon('language_icons/logo_matlab.png')
    elif language_name  == "perl":
        return set_icon('language_icons/logo_perl.png')
    elif language_name  == "ruby":
        return set_icon('language_icons/logo_ruby.png')
    elif language_name  == "tcl":
        return set_icon('language_icons/logo_tcl.png')
    elif language_name  == "tex":
        return set_icon('language_icons/logo_tex.png')
    elif language_name  == "ini" or language_name  == "makefile":
        return set_icon('tango_icons/document-properties.png')
    elif language_name  == "coffeescript":
        return set_icon('language_icons/logo_coffeescript.png')
    elif language_name  == "c#":
        return set_icon('language_icons/logo_csharp.png')
    elif language_name  == "java":
        return set_icon('language_icons/logo_java.png')
    elif language_name  == "javascript":
        return set_icon('language_icons/logo_javascript.png')
    elif language_name  == "octave":
        return set_icon('language_icons/logo_octave.png')
    elif language_name  == "sql":
        return set_icon('language_icons/logo_sql.png')
    elif language_name  == "xml":
        return set_icon('language_icons/logo_xml.png')
    elif language_name  == "text":
        return set_icon('tango_icons/text-x-generic.png')
    else:
        return set_icon("tango_icons/file.png")


"""
Module structures
"""
class SessionGuiManipulator(PyQt4.QtGui.QTreeView):
    """
    GUI object for easier user editing of sessions
    """
    class SessionItem(PyQt4.QtGui.QStandardItem):
        """QStandarItem with overridden methods"""
        #The session that the standard item will store
        my_parent   = None
        name        = None
        type        = None
        session     = None
    
    #Class constants
    class ItemType:
        SESSION         = 0
        GROUP           = 1
        EMPTY_SESSION   = 2
        EMPTY_GROUP     = 3
    
    #Class variables
    parent                  = None
    main_form               = None
    settings_manipulator    = None
    name                    = ""
    savable                 = data.CanSave.NO
    last_clicked_session    = None
    tree_model              = None
    session_nodes           = None
    refresh_lock            = False
    edit_flag               = False
    last_created_item       = None
    #Icons
    node_icon_group         = None
    node_icon_session       = None
    icon_session_add        = None
    icon_session_remove     = None
    icon_session_overwrite  = None
    icon_group_add          = None
    icon_session_edit       = None
    
    def __init__(self, settings_manipulator, parent, main_form):
        """Initialization"""
        #Initialize the superclass
        super().__init__(parent)
        #Store the reference to the parent BasicWidget from the "forms" module
        self.parent = parent
        #Store the reference to the MainWindow form from the "forms" module
        self.main_form = main_form
        #Store the reference to the active SettingsManipulator
        self.settings_manipulator = settings_manipulator
        #Store name of self
        self.name = "Session editing tree display"
        #Enable node expansion on double click
        self.setExpandsOnDoubleClick(True)
        #Set the node icons
        self.node_icon_group    = set_icon("tango_icons/folder.png")
        self.node_icon_session  = set_icon("tango_icons/sessions.png")
        self.icon_session_add       = set_icon("tango_icons/session-add.png")
        self.icon_session_remove    = set_icon("tango_icons/session-remove.png")
        self.icon_session_overwrite = set_icon("tango_icons/session-overwrite.png")
        self.icon_group_add         = set_icon("tango_icons/folder-add.png")
        self.icon_session_edit      = set_icon("tango_icons/session-edit.png")
        #Connect the signals
        self.doubleClicked.connect(self._item_double_clicked)
    
    def mousePressEvent(self, event):
        """Function connected to the clicked signal of the tree display"""
        super().mousePressEvent(event)
        #Set the focus
        self.setFocus()
        #Set Save/SaveAs buttons in the menubar
        self.parent._set_save_status()
    
    def setFocus(self):
        """Overridden focus event"""
        #Execute the supeclass focus function
        super().setFocus()
        #Check indication
        self.main_form.view.indication_check()
    
    def _item_double_clicked(self, model_index):
        """Callback connected to the treeview's 'clicked' signal"""
        session_item = self.tree_model.itemFromIndex(model_index)
        if session_item.type == self.ItemType.SESSION:
            #Open the session
            session = session_item.session
            #This is a call to the MainWindow class in the forms module
            self.main_form.sessions.restore(session.name, session.group)
        elif session_item.type == self.ItemType.GROUP:
            pass
    
    def _item_changed(self, item):
        """Callback connected to the displays QStandardItemModel 'itemChanged' signal"""
        #Get the clicked item
        changed_item = item
        #Check for editing
        if self.edit_flag == True:
            if changed_item.type == self.ItemType.SESSION:
                #Item is a session
                old_item_name = item.session.name
                new_item_name = self.indexWidget(item.index()).text()
                #Rename all of the sessions with the group name and store them in a new list
                new_session_list = []
                for session in self.settings_manipulator.stored_sessions:
                    if session.name == old_item_name and session.group == item.session.group:
                        session.name = new_item_name
                    new_session_list.append(session)
                #Replace the old list with the new
                self.settings_manipulator.stored_sessions = new_session_list
                #Save the the new session list by saving the settings
                self.settings_manipulator.save_settings(
                    self.settings_manipulator.main_window_side
                )
                #Update the main forms session menu
                self.main_form.sessions.update_menu()
                #Display successful group deletion
                group_name = item.session.group
                if group_name == None:
                    group_name = ""
                else:
                    group_name += " / "
                self.main_form.display.repl_display_message(
                    "Session '{:s}{:s}' was renamed to '{:s}{:s}'!".format(
                                                                group_name, 
                                                                old_item_name, 
                                                                group_name, 
                                                                new_item_name
                                                            ), 
                    message_type=data.MessageType.SUCCESS
                )
                #Refresh the session tree
                self.refresh_display()
                #Refresh the session tree
                self.refresh_display()
            elif changed_item.type == self.ItemType.GROUP:
                #Item is a group
                old_group_name = item.name
                new_group_name = self.indexWidget(item.index()).text()
                #Rename all of the session with the group name and store them in a new list
                new_session_list = []
                for session in self.settings_manipulator.stored_sessions:
                    if session.group == old_group_name:
                        session.group = new_group_name
                    new_session_list.append(session)
                #Replace the old list with the new
                self.settings_manipulator.stored_sessions = new_session_list
                #Save the the new session list by saving the settings
                self.settings_manipulator.save_settings(
                    self.settings_manipulator.main_window_side
                )
                #Update the main forms session menu
                self.main_form.sessions.update_menu()
                #Display successful group deletion
                self.main_form.display.repl_display_message(
                    "Group '{:s}' was renamed to '{:s}'!".format(
                                                                old_group_name, 
                                                                new_group_name
                                                            ), 
                    message_type=data.MessageType.SUCCESS
                )
                #Refresh the session tree
                self.refresh_display()
        else:
            if changed_item.type == self.ItemType.SESSION:
                #Item is a session
    #            session = changed_item.session
                pass
            elif changed_item.type == self.ItemType.GROUP:
                #Item is a group
    #            group_name = changed_item.name
                pass
            elif changed_item.type == self.ItemType.EMPTY_SESSION:
                #Store the session
                session = changed_item.session
                #Adjust the name to the new one, by getting the QLineEdit at the model index
                session.name = self.indexWidget(item.index()).text()
                #This is a call to the MainWindow class in the forms module
                self.main_form.sessions.add(session.name, session.group)
                #Refresh the session tree
                self.refresh_display()
                self.last_created_item = self.ItemType.EMPTY_SESSION
            elif changed_item.type == self.ItemType.EMPTY_GROUP:
                #Adjust the name to the new one, by getting the QLineEdit at the model index
                group_name = self.indexWidget(item.index()).text()
                #When the item's name is change it refires the itemChanged signal,
                #so a check of one of the properties is necessary to not repeat the operation
                if item.name == "":
                    item.name = group_name
                    item.setEditable(False)
                    #Display the warning
                    message = "An empty group was created.\n"
                    message += "A session must be added to it or the empty group will \n"
                    message += "be deleted on the next refresh!"
                    self.main_form.display.repl_display_message(
                        message, 
                        message_type=data.MessageType.WARNING
                    )
                    #Set the refresh lock, so it won't delete the empty group node
                    self.refresh_lock = True
                    self.last_created_item = self.ItemType.EMPTY_GROUP
    
    def _item_editing_closed(self, widget):
        """Signal that fires when editing was canceled/ended in an empty session or empty group"""
        if (self.refresh_lock == True and 
            self.last_created_item == self.ItemType.EMPTY_GROUP):
            return
        self.refresh_display()
    
    def refresh_display(self):
        """Refresh the displayed session while keeping the expanded groups"""
        #Reset the all locks/flags
        self.refresh_lock   = False
        self.edit_flag      = False
        #Store which groups are expanded
        expanded_groups = []
        for group in self.groups.items():
            if self.isExpanded(group[1].index()):
                expanded_groups.append(group[0])
        #Remove the empty node by refreshing the session tree
        self.show_sessions()
        #Expand the groups that were expanded before
        for exp_group in expanded_groups:
            for group in self.groups.items():
                if group[0] == exp_group:
                    self.expand(group[1].index())
    
    def add_empty_group(self):
        #Check for various flags
        if self.edit_flag == True:
            return
        #Check if an empty group is already present
        for session_node in self.session_nodes:
            if session_node.type == self.ItemType.EMPTY_GROUP:
                return
        empty_group_node = self.SessionItem("")
        empty_group_node.parent    = self
        empty_group_node.name      = ""
        empty_group_node.session   = None
        empty_group_node.type      = self.ItemType.EMPTY_GROUP
        empty_group_node.setEditable(True)
        empty_group_node.setIcon(self.node_icon_group)
        self.tree_model.appendRow(empty_group_node)
        #Start editing the new empty group
        self.session_nodes.append(empty_group_node)
        self.edit(empty_group_node.index())
        #Add the session signal when editing is canceled
        delegate = self.itemDelegate(empty_group_node.index())
        delegate.closeEditor.connect(self._item_editing_closed)
        #Store last created node type
        self.last_created_item = self.ItemType.EMPTY_GROUP
    
    def add_empty_session(self):
        #Check for various flags
        if self.edit_flag == True:
            return
        #Check if an empty session is already present
        for session_node in self.session_nodes:
            if session_node.type == self.ItemType.EMPTY_SESSION:
                return
        #Check where the session will be added
        attachment_item = self.tree_model
        has_group = False
        if self.selectedIndexes() != []:
            selected_item = self.tree_model.itemFromIndex(self.selectedIndexes()[0])
            if selected_item.type == self.ItemType.SESSION:
                if selected_item.session.group != None:
                    attachment_item = selected_item.parent()
                    self.expand(attachment_item.index())
                    has_group = True
            elif (selected_item.type == self.ItemType.GROUP or 
                  selected_item.type == self.ItemType.EMPTY_GROUP):
                has_group = True
                attachment_item = selected_item
                self.expand(attachment_item.index())
        #Initialize the session
        empty_session = settings.Session("")
        if has_group == True:
            empty_session.group = attachment_item.name
        empty_session_node = self.SessionItem("")
        empty_session_node.parent    = self
        empty_session_node.name      = ""
        empty_session_node.session   = empty_session
        empty_session_node.type      = self.ItemType.EMPTY_SESSION
        empty_session_node.setEditable(True)
        empty_session_node.setIcon(self.node_icon_session)
        attachment_item.appendRow(empty_session_node)
        #Start editing the new empty session
        self.session_nodes.append(empty_session_node)
        self.edit(empty_session_node.index())
        #Add the session signal when editing is canceled
        delegate = self.itemDelegate(empty_session_node.index())
        delegate.closeEditor.connect(self._item_editing_closed)
        #Store last created node type
        self.last_created_item = self.ItemType.EMPTY_SESSION
    
    def remove_session(self):
        #Check for various flags
        if self.edit_flag == True:
            return
        #Check if an item is selected
        if self.selectedIndexes() == []:
            return
        selected_item = self.tree_model.itemFromIndex(self.selectedIndexes()[0])
        #Check the selected item type
        if selected_item.type == self.ItemType.GROUP:
            remove_group_name = selected_item.name
            message =  "Are you sure you want to delete group:\n"
            message += "'{:s}' ?".format(remove_group_name)
            reply = PyQt4.QtGui.QMessageBox.question(
                        self.parent, 
                        'Delete Session Group', 
                        message,
                        PyQt4.QtGui.QMessageBox.Yes,
                        PyQt4.QtGui.QMessageBox.No
                    )
            if reply == PyQt4.QtGui.QMessageBox.No:
                return
            #Delete all of the session with the group name
            for session in self.settings_manipulator.stored_sessions:
                if session.group == remove_group_name:
                    self.main_form.sessions.remove(session.name, session.group)
            #Display successful group deletion
            self.main_form.display.repl_display_message(
                "Group '{:s}' was deleted!".format(remove_group_name), 
                message_type=data.MessageType.SUCCESS
            )
            #Refresh the tree
            self.refresh_display()
        elif selected_item.type == self.ItemType.SESSION:
            remove_session = selected_item.session
            group_name = remove_session.group
            if group_name == None:
                group_name = ""
            else:
                group_name += " / "
            message =  "Are you sure you want to delete session:\n"
            message += "'{:s}{:s}' ?".format(group_name, remove_session.name)
            reply = PyQt4.QtGui.QMessageBox.question(
                        self.parent, 
                        'Delete Session Group', 
                        message,
                        PyQt4.QtGui.QMessageBox.Yes,
                        PyQt4.QtGui.QMessageBox.No
                    )
            if reply == PyQt4.QtGui.QMessageBox.No:
                return
            #Delete the session
            #Delete all of the session with the group name
            for session in self.settings_manipulator.stored_sessions:
                if (session.name == remove_session.name and
                    session.group == remove_session.group):
                    self.main_form.sessions.remove(session.name, session.group)
                    break
            #Refresh the tree
            self.refresh_display()
        elif selected_item.type == self.ItemType.EMPTY_SESSION:
            #Display successful group deletion
            self.main_form.display.repl_display_message(
                "Empty session was deleted!", 
                message_type=data.MessageType.SUCCESS
            )
            #Refresh the tree
            self.refresh_display()
        elif selected_item.type == self.ItemType.EMPTY_GROUP:
            #Display successful group deletion
            self.main_form.display.repl_display_message(
                "Empty group was deleted!", 
                message_type=data.MessageType.SUCCESS
            )
            #Refresh the tree
            self.refresh_display()
    
    def overwrite_session(self):
        """Overwrite the selected session"""
        #Check for various flags
        if self.edit_flag == True:
            return
        #Check if a session is selected
        if self.selectedIndexes() == []:
            return
        selected_item = self.tree_model.itemFromIndex(self.selectedIndexes()[0])
        #Check the selected item type
        if selected_item.type == self.ItemType.GROUP:
            #Show message that groups cannot be overwritten
            self.main_form.display.repl_display_message(
                "Groups cannot be overwritten!", 
                message_type=data.MessageType.ERROR
            )
            return
        elif selected_item.type == self.ItemType.SESSION:
            selected_session = selected_item.session
            #Adding a session that is already stored will overwrite it
            self.main_form.sessions.add(selected_session.name, selected_session.group)
            #Refresh the tree
            self.refresh_display()
    
    def edit_item(self):
        """Edit the selected session or group name"""
        if self.edit_flag == True:
            return
        #Check if an item is selected
        if self.selectedIndexes() == []:
            return
        selected_item = self.tree_model.itemFromIndex(self.selectedIndexes()[0])
        #Check the selected item type
        if selected_item.type == self.ItemType.GROUP or selected_item.type == self.ItemType.SESSION:
            selected_item.setEditable(True)
            self.edit(selected_item.index())
        #Add the session signal when editing is canceled
        delegate = self.itemDelegate(selected_item.index())
        delegate.closeEditor.connect(self._item_editing_closed)
        #Set the editing flag
        self.edit_flag = True
    
    def show_sessions(self):
        """Show the current session in a tree structure"""
        #Initialize the display
        self.tree_model = PyQt4.QtGui.QStandardItemModel()
        self.tree_model.setHorizontalHeaderLabels(["SESSIONS"])
        self.header().hide()
        self.setModel(self.tree_model)
        self.setUniformRowHeights(True)
        #Connect the tree model signals
        self.tree_model.itemChanged.connect(self._item_changed)
        font    = PyQt4.QtGui.QFont("Courier", 10, PyQt4.QtGui.QFont.Bold)
        #First add all of the groups, if any
        self.groups = {}
        for session in self.settings_manipulator.stored_sessions:
            if session.group != None:
                if not(session.group in self.groups):
                    item_group_node = self.SessionItem(session.group)
                    item_group_node.setFont(font)
                    item_group_node.my_parent   = self
                    item_group_node.name        = session.group
                    item_group_node.session     = None
                    item_group_node.type        = self.ItemType.GROUP
                    item_group_node.setEditable(False)
                    item_group_node.setIcon(self.node_icon_group)
                    self.groups[session.group] = item_group_node
        #Add the groups to the display
        for self.group in collections.OrderedDict(sorted(self.groups.items())).items():
            self.tree_model.appendRow(self.group[1])
        #Initialize the list of session nodes
        self.session_nodes = []
        #Loop through the manipulators sessions and add them to the display
        for session in self.settings_manipulator.stored_sessions:
            item_session_node = self.SessionItem(session.name)
            item_session_node.my_parent = self
            item_session_node.name      = session.name
            item_session_node.session   = session
            item_session_node.type      = self.ItemType.SESSION
            item_session_node.setEditable(False)
            item_session_node.setIcon(self.node_icon_session)
            #Check if the item is in a group
            if session.group != None:
                self.groups[session.group].appendRow(item_session_node)
            else:
                self.tree_model.appendRow(item_session_node)
            #Append the session to the stored node list
            self.session_nodes.append(item_session_node)
    
    def show_session_buttons(self, parent):
        """
        Create and display buttons for manipulating sessions
        on the parent basic widget
        """
        #Create the find toolbar and buttons
        session_toolbar = PyQt4.QtGui.QToolBar(parent)
        session_toolbar.setIconSize(PyQt4.QtCore.QSize(16,16))
        session_add_action = PyQt4.QtGui.QAction(
                                    self.icon_session_add, 
                                    "session_add",
                                    parent
                                )
        session_add_action.setToolTip(
            "Add a new session"
        )
        session_add_action.triggered.connect(self.add_empty_session)
        session_remove_action = PyQt4.QtGui.QAction(
                                    self.icon_session_remove, 
                                    "session_remove",
                                    parent
                                )
        session_remove_action.setToolTip(
            "Remove the selected session"
        )
        session_remove_action.triggered.connect(self.remove_session)
        session_overwrite_action = PyQt4.QtGui.QAction(
                                        self.icon_session_overwrite, 
                                        "session_overwrite",
                                        parent
                                    )
        session_overwrite_action.setToolTip(
            "Overwrite the selected session"
        )
        session_overwrite_action.triggered.connect(self.overwrite_session)
        session_add_group_action = PyQt4.QtGui.QAction(
                                        self.icon_group_add, 
                                        "session_add_group",
                                        parent
                                    )
        session_add_group_action.setToolTip(
            "Add a new group"
        )
        session_add_group_action.triggered.connect(self.add_empty_group)
        session_edit_action = PyQt4.QtGui.QAction(
                                        self.icon_session_edit, 
                                        "session_edit",
                                        parent
                                    )
        session_edit_action.setToolTip(
            "Edit the selected item"
        )
        session_edit_action.triggered.connect(self.edit_item)
        session_toolbar.addAction(session_edit_action)
        session_toolbar.addAction(session_overwrite_action)
        session_toolbar.addAction(session_add_group_action)
        session_toolbar.addAction(session_add_action)
        session_toolbar.addAction(session_remove_action)
        session_toolbar.show()
        #Set the corner widget of the parent
        parent.setCornerWidget(session_toolbar)



"""
----------------------------------------------------------------------------
Object for displaying various results in a tree structure
----------------------------------------------------------------------------
"""
class TreeDisplay(PyQt4.QtGui.QTreeView):
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
            #Create a new instance of Directory class using the __class__ dunder method
            new_directory = self.__class__(dir_item)
            #Add the new directory to the dictionary
            self.directories[dir_name] = new_directory
            #Add the new directory item to the parent(self)
            self.item.appendRow(dir_item)
            #Return the directory object reference
            return new_directory
        
        def add_file(self, file_name, file_item):
            self.files[file_name] = file_item
            #Add the new file item to the parent(self)
            self.item.appendRow(file_item)
    
    #Class variables
    parent                  = None
    main_form               = None
    name                    = ""
    savable                 = data.CanSave.NO
    tree_display_type       = None
    #Attributes specific to the display data
    bound_node_tab          = None
    #Node icons
    node_icon_import        = None
    node_icon_type          = None
    node_icon_const         = None
    node_icon_function      = None
    node_icon_procedure     = None
    node_icon_converter     = None
    node_icon_iterator      = None
    node_icon_class         = None
    node_icon_method        = None
    node_icon_property      = None
    node_icon_macro         = None
    node_icon_template      = None
    node_icon_variable      = None
    node_icon_namespace     = None
    node_icon_nothing       = None
    folder_icon             = None
    goto_icon               = None
    python_icon             = None
    nim_icon                = None
    c_icon                  = None
    
    def __init__(self, parent=None, main_form=None):
        """Initialization"""
        #Initialize the superclass
        super().__init__(parent)
        #Store the reference to the parent
        self.parent = parent
        #Store the reference to the main form
        self.main_form = main_form
        #Store name of self
        self.name = "Tree display"
        #Disable node expansion on double click
        self.setExpandsOnDoubleClick(False)
        #Connect the doubleclick signal
        self.doubleClicked.connect(self._item_double_click)
        #Connect the doubleclick signal
        self.expanded.connect(self._check_contents)
        #Initialize the icons
        #Node icons
        self.node_icon_import   = set_icon("various/node_module.png")
        self.node_icon_type     = set_icon("various/node_type.png")
        self.node_icon_variable = set_icon("various/node_variable.png")
        self.node_icon_const    = set_icon("various/node_const.png")
        self.node_icon_function = set_icon("various/node_function.png")
        self.node_icon_procedure= set_icon("various/node_procedure.png")
        self.node_icon_converter= set_icon("various/node_converter.png")
        self.node_icon_iterator = set_icon("various/node_iterator.png")
        self.node_icon_class    = set_icon("various/node_class.png")
        self.node_icon_method   = set_icon("various/node_method.png")
        self.node_icon_macro    = set_icon("various/node_macro.png")
        self.node_icon_template = set_icon("various/node_template.png")
        self.node_icon_namespace= set_icon("various/node_namespace.png")
        self.node_icon_nothing  = set_icon("tango_icons/dialog-warning.png")
        self.python_icon        = set_icon("language_icons/logo_python.png")
        self.nim_icon           = set_icon("language_icons/logo_nim.png")
        self.c_icon             = set_icon("language_icons/logo_c.png")
        #File searching icons
        self.file_icon      = set_icon("tango_icons/file.png")
        self.folder_icon    = set_icon("tango_icons/folder.png")
        self.goto_icon      = set_icon('tango_icons/edit-goto.png')
    
    def setFocus(self):
        """Overridden focus event"""
        #Execute the supeclass focus function
        super().setFocus()
        #Check indication
        self.main_form.view.indication_check()
    
    def mousePressEvent(self, event):
        """Function connected to the clicked signal of the tree display"""
        super().mousePressEvent(event)
        #Set the focus
        self.setFocus()
        #Set Save/SaveAs buttons in the menubar
        self.parent._set_save_status()
    
    def _item_double_click(self, model_index):
        """Function connected to the doubleClicked signal of the tree display"""
        #Use the item text according to the tree display type
        if self.tree_display_type == data.TreeDisplayType.NODES:
            #Get the text of the double clicked item
            item = self.model().itemFromIndex(model_index)
            self._node_item_parse(item)
        elif self.tree_display_type == data.TreeDisplayType.FILES:
            #Get the double clicked item
            item = self.model().itemFromIndex(model_index)
            #Test if the item has the 'full_name' attribute
            if hasattr(item, "is_dir") == True:
                #Expand/collapse the directory node
                if self.isExpanded(item.index()) == True:
                    self.collapse(item.index())
                else:
                    self.expand(item.index())
                return
            elif hasattr(item, "full_name") == True:
                #Open the file
                self.main_form.open_file(file=item.full_name)
        elif self.tree_display_type == data.TreeDisplayType.FILES_WITH_LINES:
            #Get the double clicked item
            item = self.model().itemFromIndex(model_index)
            #Test if the item has the 'full_name' attribute
            if hasattr(item, "full_name") == False:
                return
            #Open the file
            self.main_form.open_file(file=item.full_name)
            #Check if a line item was clicked
            if hasattr(item, "line_number") == True:
                #Goto the stored line number
                document = self.main_form.main_window.currentWidget()
                document.goto_line(item.line_number)
    
    def _node_item_parse(self, item):
        #Check the item text
        item_text = item.text()
        if hasattr(item, "line_number") == True:
            #Goto the stored line number
            self.bound_tab.parent.setCurrentWidget(self.bound_tab)
            self.bound_tab.goto_line(item.line_number)
        elif "line:" in item_text:
            #Parse the line number out of the item text
            line = item_text.split()[-1]
            start_index = line.index(":") + 1
            end_index   = -1
            line_number = int(line[start_index:end_index])
            #Focus the bound tab in its parent window
            self.bound_tab.parent.setCurrentWidget(self.bound_tab)
            #Go to the item line number
            self.bound_tab.goto_line(line_number)
        elif "DOCUMENT" in item_text:
            #Focus the bound tab in its parent window
            self.bound_tab.parent.setCurrentWidget(self.bound_tab)
    
    def _check_contents(self):
        #Update the horizontal scrollbar width
        self.resize_horizontal_scrollbar()
    
    def set_font_size(self, size_in_points):
        """Set the font size for the tree display items"""
        #Initialize the font with the new size
        new_font = PyQt4.QtGui.QFont('Courier', size_in_points)
        #Set the new font
        self.setFont(new_font)
    
    def set_display_type(self, tree_type):
        """Set the tree display type attribute"""
        self.tree_display_type = tree_type
    
    def resize_horizontal_scrollbar(self):
        """
        Resize the header so the horizontal scrollbar will have the correct width
        """
        for i in range(self.model().rowCount()):
            self.resizeColumnToContents(i)
    
    def display_python_nodes(self, 
                             custom_editor,
                             import_nodes, 
                             class_nodes,
                             function_nodes,
                             global_vars):
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
        self.setSelectionBehavior(PyQt4.QtGui.QAbstractItemView.SelectRows)
        tree_model = PyQt4.QtGui.QStandardItemModel()
        tree_model.setHorizontalHeaderLabels([document_name])
        self.setModel(tree_model)
        self.setUniformRowHeights(True)
        self.set_font_size(10)
        #Add the file attributes to the tree display
        description_brush   = PyQt4.QtGui.QBrush(PyQt4.QtGui.QColor(0, 0, 128))
        description_font    = PyQt4.QtGui.QFont("Courier", 10, PyQt4.QtGui.QFont.Bold)
        item_document_name  = PyQt4.QtGui.QStandardItem(document_name_text)
        item_document_name.setEditable(False)
        item_document_name.setForeground(description_brush)
        item_document_name.setFont(description_font)
        item_document_type  = PyQt4.QtGui.QStandardItem(document_type_text)
        item_document_type.setEditable(False)
        item_document_type.setForeground(description_brush)
        item_document_type.setFont(description_font)
        item_document_type.setIcon(self.python_icon)
        tree_model.appendRow(item_document_name)
        tree_model.appendRow(item_document_type)
        #Set the label properties
        label_brush = PyQt4.QtGui.QBrush(PyQt4.QtGui.QColor(128, 0, 128))
        label_font  = PyQt4.QtGui.QFont("Courier", 10, PyQt4.QtGui.QFont.Bold)
        """Imported module filtering"""
        item_imports = PyQt4.QtGui.QStandardItem(import_text)
        item_imports.setEditable(False)
        item_imports.setForeground(label_brush)
        item_imports.setFont(label_font)
        for node in import_nodes:
            node_text = str(node[0]) + " (line:"
            node_text += str(node[1]) + ")"
            item_import_node = PyQt4.QtGui.QStandardItem(node_text)
            item_import_node.setEditable(False)
            item_import_node.setIcon(self.node_icon_import)
            item_imports.appendRow(item_import_node)
        #Append the import node to the model
        tree_model.appendRow(item_imports)
        """Class nodes filtering"""
        item_classes = PyQt4.QtGui.QStandardItem(class_text)
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
            parent_tree_node = PyQt4.QtGui.QStandardItem(node_text)
            parent_tree_node.setEditable(False)
            parent_tree_node.setIcon(self.node_icon_class)
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
                child_tree_node = PyQt4.QtGui.QStandardItem(child_text)
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
                        child_tree_node.setIcon(self.node_icon_class)
                    else:
                        #Set method/function icon according to the previous base node type
                        if base_node_type[child_level-1] == 0:
                            child_tree_node.setIcon(self.node_icon_method)
                        elif base_node_type[child_level-1] == 1:
                            child_tree_node.setIcon(self.node_icon_procedure)
                    #Determine the parent node level
                    level_retraction    = 1
                    parent_level        = child_level - level_retraction
                    parent_node         = None
                    while parent_node == None and parent_level >= 0:
                        parent_node = base_node_items[parent_level]
                        level_retraction += 1
                        parent_level        = child_level - level_retraction
                    #Add the child node to the parent node
                    parent_node.appendRow(child_tree_node)
                    #Sort the base node children
                    parent_node.sortChildren(0)
                else:
                    #Set the icon for the 
                    if isinstance(child_object, ast.ClassDef) == True:
                        child_tree_node.setIcon(self.node_icon_class)
                    elif isinstance(child_object, ast.FunctionDef) == True:
                        child_tree_node.setIcon(self.node_icon_method)
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
            item_no_classes = PyQt4.QtGui.QStandardItem("No classes found")
            item_no_classes.setEditable(False)
            item_no_classes.setIcon(self.node_icon_nothing)
            item_classes.appendRow(item_no_classes)
        """Function nodes filtering"""
        item_functions = PyQt4.QtGui.QStandardItem(function_text)
        item_functions.setEditable(False)
        item_functions.setForeground(label_brush)
        item_functions.setFont(label_font)
        #Create function nodes as tree items
        for func in function_nodes:
            #Set the function node text
            func_text = func.name + " (line:"
            func_text += str(func.lineno) + ")"
            #Construct the node and add it to the tree
            function_node = PyQt4.QtGui.QStandardItem(func_text)
            function_node.setEditable(False)
            function_node.setIcon(self.node_icon_procedure)
            item_functions.appendRow(function_node)
        item_functions.sortChildren(0)
        #Check if there were any nodes found
        if function_nodes == []:
            item_no_functions = PyQt4.QtGui.QStandardItem("No functions found")
            item_no_functions.setEditable(False)
            item_no_functions.setIcon(self.node_icon_nothing)
            item_functions.appendRow(item_no_functions)
        #Append the function nodes to the model
        tree_model.appendRow(item_functions)
        #Expand the base nodes
        self.expand(item_classes.index())
        self.expand(item_functions.index())
        #Resize the header so the horizontal scrollbar will have the correct width
        self.resize_horizontal_scrollbar()
    
    def display_c_nodes(self, custom_editor, function_nodes):
        """Display the input C data in a tree structure"""
        #Store the custom editor tab that for quicker navigation
        self.bound_tab = custom_editor
        #Set the tree display type to NODE
        self.set_display_type(data.TreeDisplayType.NODES)
        #Define the document name, type
        document_name       = os.path.basename(custom_editor.save_name)
        document_name_text  = "DOCUMENT: {:s}".format(document_name)
        document_type_text  = "TYPE: {:s}".format(custom_editor.current_file_type)
        #Define the display structure texts
        function_text       = "FUNCTIONS:"
        #Initialize the tree display
        self.setSelectionBehavior(PyQt4.QtGui.QAbstractItemView.SelectRows)
        tree_model = PyQt4.QtGui.QStandardItemModel()
        tree_model.setHorizontalHeaderLabels([document_name])
        self.setModel(tree_model)
        self.setUniformRowHeights(True)
        self.set_font_size(10)
        #Add the file attributes to the tree display
        description_brush   = PyQt4.QtGui.QBrush(PyQt4.QtGui.QColor(0, 0, 128))
        description_font    = PyQt4.QtGui.QFont("Courier", 10, PyQt4.QtGui.QFont.Bold)
        item_document_name  = PyQt4.QtGui.QStandardItem(document_name_text)
        item_document_name.setEditable(False)
        item_document_name.setForeground(description_brush)
        item_document_name.setFont(description_font)
        item_document_type  = PyQt4.QtGui.QStandardItem(document_type_text)
        item_document_type.setEditable(False)
        item_document_type.setForeground(description_brush)
        item_document_type.setFont(description_font)
        item_document_type.setIcon(self.c_icon)
        tree_model.appendRow(item_document_name)
        tree_model.appendRow(item_document_type)
        #Set the label properties
        label_brush = PyQt4.QtGui.QBrush(PyQt4.QtGui.QColor(128, 0, 128))
        label_font  = PyQt4.QtGui.QFont("Courier", 10, PyQt4.QtGui.QFont.Bold)
        """Function nodes filtering"""
        item_functions = PyQt4.QtGui.QStandardItem(function_text)
        item_functions.setEditable(False)
        item_functions.setForeground(label_brush)
        item_functions.setFont(label_font)
        #Create function nodes as tree items
        for func in function_nodes:
            #Set the function node text
            func_text = func[0] + " (line:"
            func_text += str(func[1]) + ")"
            #Construct the node and add it to the tree
            function_node = PyQt4.QtGui.QStandardItem(func_text)
            function_node.setEditable(False)
            function_node.setIcon(self.node_icon_procedure)
            item_functions.appendRow(function_node)
        #Check if there were any nodes found
        if function_nodes == []:
            item_no_functions = PyQt4.QtGui.QStandardItem("No functions found")
            item_no_functions.setEditable(False)
            item_functions.appendRow(item_no_functions)
        #Append the function nodes to the model
        tree_model.appendRow(item_functions)
        #Expand the base node
        self.expand(item_functions.index())
        #Resize the header so the horizontal scrollbar will have the correct width
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
        self.setSelectionBehavior(PyQt4.QtGui.QAbstractItemView.SelectRows)
        tree_model = PyQt4.QtGui.QStandardItemModel()
        tree_model.setHorizontalHeaderLabels([document_name])
        self.setModel(tree_model)
        self.setUniformRowHeights(True)
        self.set_font_size(10)
        #Add the file attributes to the tree display
        description_brush   = PyQt4.QtGui.QBrush(PyQt4.QtGui.QColor(0, 0, 128))
        description_font    = PyQt4.QtGui.QFont("Courier", 10, PyQt4.QtGui.QFont.Bold)
        item_document_name  = PyQt4.QtGui.QStandardItem(document_name_text)
        item_document_name.setEditable(False)
        item_document_name.setForeground(description_brush)
        item_document_name.setFont(description_font)
        item_document_type  = PyQt4.QtGui.QStandardItem(document_type_text)
        item_document_type.setEditable(False)
        item_document_type.setForeground(description_brush)
        item_document_type.setFont(description_font)
        item_document_type.setIcon(self.nim_icon)
        tree_model.appendRow(item_document_name)
        tree_model.appendRow(item_document_type)
        """Add the nodes"""
        label_brush = PyQt4.QtGui.QBrush(PyQt4.QtGui.QColor(128, 0, 128))
        label_font  = PyQt4.QtGui.QFont("Courier", 10, PyQt4.QtGui.QFont.Bold)
        #Nested function for creating a tree node
        def create_tree_node(node_text, 
                             node_text_brush, 
                             node_text_font, 
                             node_icon, 
                             node_line_number):
            tree_node = PyQt4.QtGui.QStandardItem(node_text)
            tree_node.setEditable(False)
            if node_text_brush != None:
                tree_node.setForeground(node_text_brush)
            if node_text_font != None:
                tree_node.setFont(node_text_font)
            if node_icon != None:
                tree_node.setIcon(node_icon)
            if node_line_number != None:
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
                                            self.node_icon_import, 
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
                                            self.node_icon_type, 
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
                                            self.node_icon_const, 
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
                                            self.node_icon_const, 
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
                                        self.node_icon_variable, 
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
                                        self.node_icon_procedure, 
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
                                        self.node_icon_procedure, 
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
                                                self.node_icon_converter,  
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
                                                self.node_icon_iterator,  
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
                                        self.node_icon_method, 
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
                                            self.node_icon_method, 
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
                                        self.node_icon_macro, 
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
                                        self.node_icon_template, 
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
                                        self.node_icon_class, 
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
                                        self.node_icon_namespace, 
                                        namespace.line + 1
                                    )
                    item_namespaces_node.appendRow(item_namespace_node)
                    show_nim_node(None, item_namespace_node, namespace)
        show_nim_node(tree_model, None, nim_nodes)
    
    def _init_found_files_options(self, search_text, directory, custom_text=None):
        #Initialize the tree display to the found files type
        self.horizontalScrollbarAction(1)
        self.setSelectionBehavior(PyQt4.QtGui.QAbstractItemView.SelectRows)
        tree_model = PyQt4.QtGui.QStandardItemModel()
        tree_model.setHorizontalHeaderLabels(["FOUND FILES TREE"])
        self.header().hide()
        self.setModel(tree_model)
        self.setUniformRowHeights(True)
        self.set_font_size(10)
        """Define the description details"""
        #Font
        description_brush   = PyQt4.QtGui.QBrush(PyQt4.QtGui.QColor(0, 0, 128))
        description_font    = PyQt4.QtGui.QFont("Courier", 10, PyQt4.QtGui.QFont.Bold)
        #Directory item
        item_directory  = PyQt4.QtGui.QStandardItem(
                            "BASE DIRECTORY: {:s}".format(directory.replace("\\", "/"))
                          )
        item_directory.setEditable(False)
        item_directory.setForeground(description_brush)
        item_directory.setFont(description_font)
        #Search item, display according to the custom text parameter
        if custom_text == None:
            item_search_text = PyQt4.QtGui.QStandardItem(
                                "FILE HAS: {:s}".format(search_text)
                               )
        else:
            item_search_text = PyQt4.QtGui.QStandardItem(custom_text)
        item_search_text.setEditable(False)
        item_search_text.setForeground(description_brush)
        item_search_text.setFont(description_font)
        tree_model.appendRow(item_directory)
        tree_model.appendRow(item_search_text)
        return tree_model
    
    def _init_replace_in_files_options(self, search_text, replace_text, directory):
        #Initialize the tree display to the found files type
        self.horizontalScrollbarAction(1)
        self.setSelectionBehavior(PyQt4.QtGui.QAbstractItemView.SelectRows)
        tree_model = PyQt4.QtGui.QStandardItemModel()
        tree_model.setHorizontalHeaderLabels(["REPLACED IN FILES TREE"])
        self.header().hide()
        self.setModel(tree_model)
        self.setUniformRowHeights(True)
        self.set_font_size(10)
        """Define the description details"""
        #Font
        description_brush   = PyQt4.QtGui.QBrush(PyQt4.QtGui.QColor(0, 0, 128))
        description_font    = PyQt4.QtGui.QFont("Courier", 10, PyQt4.QtGui.QFont.Bold)
        #Directory item
        item_directory  = PyQt4.QtGui.QStandardItem(
                            "BASE DIRECTORY: {:s}".format(directory.replace("\\", "/"))
                          )
        item_directory.setEditable(False)
        item_directory.setForeground(description_brush)
        item_directory.setFont(description_font)
        #Search item
        item_search_text = PyQt4.QtGui.QStandardItem(
                            "SEARCH TEXT: {:s}".format(search_text)
                           )
        item_search_text.setEditable(False)
        item_search_text.setForeground(description_brush)
        item_search_text.setFont(description_font)
        #Replace item
        item_replace_text = PyQt4.QtGui.QStandardItem(
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
            dir = os.path.dirname(item)
            if (not dir in sorted_directories):
                sorted_directories.append(dir)
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
        """ Helper function for adding files to a tree view """
        #Check if any files were found
        if items != []:
            #Set the UNIX file format to the directory
            directory = directory.replace("\\", "/")
            """Adding the files"""
            label_brush = PyQt4.QtGui.QBrush(PyQt4.QtGui.QColor(128, 0, 128))
            label_font  = PyQt4.QtGui.QFont("Courier", 10, PyQt4.QtGui.QFont.Bold)
            #Create the base directory item that will hold all of the found files
            item_base_directory = PyQt4.QtGui.QStandardItem(directory)
            item_base_directory.setEditable(False)
            item_base_directory.setForeground(label_brush)
            item_base_directory.setFont(label_font)
            item_base_directory.setIcon(self.folder_icon)
            #Create the base directory object that will hold everything else
            base_directory = self.Directory(item_base_directory)
            #Create the files that will be added last directly to the base directory
            base_files = {}
            #Sort the the item list so that all of the directories are before the files
            sorted_items = self._sort_item_list(items, directory)
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
                    item_file = PyQt4.QtGui.QStandardItem(file_name)
                    item_file.setEditable(False)
                    file_type = functions.get_file_type(file_name)
                    item_file.setIcon(get_language_file_icon(file_type))
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
                            item_new_directory = PyQt4.QtGui.QStandardItem(dir)
                            item_new_directory.setEditable(False)
                            item_new_directory.setIcon(self.folder_icon)
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
            item_no_files_found = PyQt4.QtGui.QStandardItem("No items found")
            item_no_files_found.setEditable(False)
            item_no_files_found.setIcon(self.node_icon_nothing)
            tree_model.appendRow(item_no_files_found)
    
    def _add_items_with_lines_to_tree(self, tree_model, directory, items):
        """ Helper function for adding files to a tree view """
        #Check if any files were found
        if items != {}:
            #Set the UNIX file format to the directory
            directory = directory.replace("\\", "/")
            """Adding the files"""
            label_brush = PyQt4.QtGui.QBrush(PyQt4.QtGui.QColor(128, 0, 128))
            label_font  = PyQt4.QtGui.QFont("Courier", 10, PyQt4.QtGui.QFont.Bold)
            #Create the base directory item that will hold all of the found files
            item_base_directory = PyQt4.QtGui.QStandardItem(directory)
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
                    item_file = PyQt4.QtGui.QStandardItem(file_name)
                    item_file.setEditable(False)
                    file_type = functions.get_file_type(file_name)
                    item_file.setIcon(get_language_file_icon(file_type))
                    #Add an atribute that will hold the full file name to the QStandartItem.
                    #It's a python object, attributes can be added dynamically!
                    item_file.full_name = item_with_path
                    for line in items[item_with_path]:
                        #Adjust the line numbering to Ex.Co. (1 to end)
                        line += 1
                        #Create the goto line item
                        item_line = PyQt4.QtGui.QStandardItem("line {:d}".format(line))
                        item_line.setEditable(False)
                        item_line.setIcon(self.goto_icon)
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
                            item_new_directory = PyQt4.QtGui.QStandardItem(dir)
                            item_new_directory.setEditable(False)
                            item_new_directory.setIcon(self.folder_icon)
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
            item_no_files_found = PyQt4.QtGui.QStandardItem("No items found")
            item_no_files_found.setEditable(False)
            item_no_files_found.setIcon(self.node_icon_nothing)
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
        #Initialize the list that will hold both the directories and files
        found_items = []
        for item in walk_generator:
            base_directory = item[0]
            for dir in item[1]:
                found_items.append(os.path.join(base_directory, dir).replace("\\", "/"))
            for file in item[2]:
                found_items.append(os.path.join(base_directory, file).replace("\\", "/"))
        #Add the items to the treeview
        self._add_items_to_tree(tree_model, directory, found_items)
    
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
    
    def display_found_files_with_lines(self, search_text, found_files, directory):
        """
        Display files with lines that were found using the 'functions' 
        module's find_in_files function
        """
        #Check if found files are valid
        if found_files == None:
            self.main_form.display.repl_display_message(
                "Error in finding files!", 
                message_type=data.MessageType.WARNING
            )
            return
        #Set the tree display type to NODE
        self.set_display_type(data.TreeDisplayType.FILES_WITH_LINES)
        #Initialize and display the search options
        tree_model = self._init_found_files_options(search_text, directory)
        #Add the items with lines to the treeview
        self._add_items_with_lines_to_tree(tree_model, directory, found_files)
    
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




"""
----------------------------------------------------------------------------
Object for displaying text difference between two files
----------------------------------------------------------------------------
"""
class TextDiffer(PyQt4.QtGui.QWidget):
    """A widget that holds two PlainEditors for displaying text difference"""
    #Class variables
    parent                  = None
    main_form               = None
    name                    = ""
    savable                 = data.CanSave.NO
    focused_editor          = None
    text_1                  = None
    text_2                  = None
    text_1_name             = None
    text_2_name             = None
    diff_text               = None
    #Class constants
    DEFAULT_FONT            = PyQt4.QtGui.QFont('Courier', 10)
    DEFAULT_FONT_BACK_COLOR = PyQt4.QtGui.QColor(0xd7, 0xd3, 0xcf, 255)
    MARGIN_BACK_COLOR       = PyQt4.QtGui.QColor(0xd7, 0xd3, 0xcf, 255)
    MARGIN_FORE_COLOR       = PyQt4.QtGui.QColor(0x2e, 0x34, 0x36, 255)
    MARGIN_STYLE            = PyQt4.Qsci.QsciScintilla.STYLE_LINENUMBER
    INDICATOR_UNIQUE_1          = 1
    INDICATOR_UNIQUE_1_COLOR    = PyQt4.QtGui.QColor(0x72, 0x9f, 0xcf, 80)
    INDICATOR_UNIQUE_2          = 2
    INDICATOR_UNIQUE_2_COLOR    = PyQt4.QtGui.QColor(0xad, 0x7f, 0xa8, 80)
    INDICATOR_SIMILAR           = 3
    INDICATOR_SIMILAR_COLOR     = PyQt4.QtGui.QColor(0x8a, 0xe2, 0x34, 80)
    GET_X_OFFSET    = PyQt4.Qsci.QsciScintillaBase.SCI_GETXOFFSET
    SET_X_OFFSET    = PyQt4.Qsci.QsciScintillaBase.SCI_SETXOFFSET
    UPDATE_H_SCROLL = PyQt4.Qsci.QsciScintillaBase.SC_UPDATE_H_SCROLL
    UPDATE_V_SCROLL = PyQt4.Qsci.QsciScintillaBase.SC_UPDATE_V_SCROLL
    #Diff icons
    icon_unique_1   = None
    icon_unique_2   = None
    icon_similar    = None
    #Marker references
    marker_unique_1         = None
    marker_unique_2         = None
    marker_unique_symbol_1  = None
    marker_unique_symbol_2  = None
    marker_similar_1        = None
    marker_similar_2        = None
    marker_similar_symbol_1 = None
    marker_similar_symbol_2 = None
    #Child widgets
    splitter    = None
    editor_1    = None
    editor_2    = None
    layout      = None
    
    def __init__(self, 
                 parent, 
                 main_form, 
                 text_1=None, 
                 text_2=None, 
                 text_1_name="", 
                 text_2_name=""):
        """Initialization"""
        #Initialize the superclass
        super().__init__(parent)
        #Store the reference to the parent
        self.parent = parent
        #Store the reference to the main form
        self.main_form = main_form
        #Set the name of the differ widget
        if text_1_name != None and text_2_name != None:
            self.name = "Text difference: {:s} / {:s}".format(text_1_name, text_2_name)
            self.text_1_name = text_1_name
            self.text_2_name = text_2_name
        else:
            self.name = "Text difference"
            self.text_1_name = "TEXT 1"
            self.text_2_name = "TEXT 2"
        #Initialize diff icons
        self.icon_unique_1  = set_icon("tango_icons/diff-unique-1.png")
        self.icon_unique_2  = set_icon("tango_icons/diff-unique-2.png")
        self.icon_similar   = set_icon("tango_icons/diff-similar.png")
        #Create the horizontal splitter and two editor widgets
        self.splitter = PyQt4.QtGui.QSplitter(PyQt4.QtCore.Qt.Horizontal, self)
        self.editor_1 = forms.CustomEditor(self, main_form)
        self.init_editor(self.editor_1)
        self.editor_2 = forms.CustomEditor(self, main_form)
        self.init_editor(self.editor_2)
        self.splitter.addWidget(self.editor_1)
        self.splitter.addWidget(self.editor_2)
        self.layout = PyQt4.QtGui.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.splitter)
        #Set the layout
        self.setLayout(self.layout)
        #Connect the necessary signals
        self.editor_1.SCN_UPDATEUI.connect(self._scn_updateui_1)
        self.editor_2.SCN_UPDATEUI.connect(self._scn_updateui_2)
        self.editor_1.cursorPositionChanged.connect(self._cursor_change_1)
        self.editor_2.cursorPositionChanged.connect(self._cursor_change_2)
        #Overwrite the CustomEditor parent widgets to point to the TextDiffers' PARENT
        self.editor_1.parent = self.parent
        self.editor_2.parent = self.parent
        #Add a new attribute to the CustomEditor that will hold the TextDiffer reference
        self.editor_1.actual_parent = self
        self.editor_2.actual_parent = self
        #Set the embedded flag
        self.editor_1.embedded = True
        self.editor_2.embedded = True
        #Add decorators to each editors mouse clicks and mouse wheel scrolls
        def focus_decorator(function_to_decorate, focused_editor):
            def decorated_function(*args, **kwargs):
                self.focused_editor = focused_editor
                function_to_decorate(*args, **kwargs)
            return decorated_function
        self.editor_1.mousePressEvent = focus_decorator(
                                            self.editor_1.mousePressEvent,
                                            self.editor_1
                                        )
        self.editor_1.wheelEvent =  focus_decorator(
                                        self.editor_1.wheelEvent,
                                        self.editor_1
                                    )
        self.editor_2.mousePressEvent = focus_decorator(
                                            self.editor_2.mousePressEvent,
                                            self.editor_2
                                        )
        self.editor_2.wheelEvent =  focus_decorator(
                                        self.editor_2.wheelEvent,
                                        self.editor_2
                                    )
        #Focus the first editor on initialization
        self.focused_editor = self.editor_1
        self.focused_editor.setFocus()
        #Initialize markers
        self.init_markers()
        #Set editor functions that have to be propagated from the TextDiffer
        #to the child editor
        self._init_editor_functions()
        #Check the text validity
        if text_1 == None or text_2 == None:
            #One of the texts is unspecified
            return
        #Create the diff
        self.compare(text_1, text_2)
    
    def _scn_updateui_1(self, sc_update):
        """Function connected to the SCN_UPDATEUI signal for scroll detection"""
        if self.focused_editor == self.editor_1:
            #Scroll the opposite editor
            if sc_update == self.UPDATE_H_SCROLL:
                current_x_offset = self.editor_1.SendScintilla(self.GET_X_OFFSET)
                self.editor_2.SendScintilla(self.SET_X_OFFSET, current_x_offset)
            elif sc_update == self.UPDATE_V_SCROLL:
                current_top_line = self.editor_1.firstVisibleLine()
                self.editor_2.setFirstVisibleLine(current_top_line)
    
    def _scn_updateui_2(self, sc_update):
        """Function connected to the SCN_UPDATEUI signal for scroll detection"""
        if self.focused_editor == self.editor_2:
            #Scroll the opposite editor
            if sc_update == self.UPDATE_H_SCROLL:
                current_x_offset = self.editor_2.SendScintilla(self.GET_X_OFFSET)
                self.editor_1.SendScintilla(self.SET_X_OFFSET, current_x_offset)
            elif sc_update == self.UPDATE_V_SCROLL:
                current_top_line = self.editor_2.firstVisibleLine()
                self.editor_1.setFirstVisibleLine(current_top_line)
    
    def _cursor_change_1(self, line, index):
        """
        Function connected to the cursorPositionChanged signal for
        cursor position change detection
        """
        if self.focused_editor == self.editor_1:
            #Update the cursor position on the opposite editor
            cursor_line, cursor_index = self.editor_1.getCursorPosition()
            #Check if the opposite editor line is long enough
            if self.editor_2.lineLength(cursor_line) > cursor_index:
                self.editor_2.setCursorPosition(cursor_line, cursor_index)
            else:
                self.editor_2.setCursorPosition(cursor_line, 0)
            #Update the first visible line, so that the views in both differs match
            current_top_line = self.editor_1.firstVisibleLine()
            self.editor_2.setFirstVisibleLine(current_top_line)
    
    def _cursor_change_2(self, line, index):
        """
        Function connected to the cursorPositionChanged signal for
        cursor position change detection
        """
        if self.focused_editor == self.editor_2:
            #Update the cursor position on the opposite editor
            cursor_line, cursor_index = self.editor_2.getCursorPosition()
            #Check if the opposite editor line is long enough
            if self.editor_1.lineLength(cursor_line) > cursor_index:
                self.editor_1.setCursorPosition(cursor_line, cursor_index)
            else:
                self.editor_1.setCursorPosition(cursor_line, 0)
            #Update the first visible line, so that the views in both differs match
            current_top_line = self.editor_2.firstVisibleLine()
            self.editor_1.setFirstVisibleLine(current_top_line)
    
    def _update_margins(self):
        """Update the text margin width"""
        self.editor_1.setMarginWidth(0, "0" * len(str(self.editor_1.lines())))
        self.editor_2.setMarginWidth(0, "0" * len(str(self.editor_2.lines())))
    
    def _signal_editor_cursor_change(self, cursor_line=None, cursor_column=None):
        """Signal that fires when cursor position changes in one of the editors"""
        self.main_form.display.update_cursor_position(cursor_line, cursor_column)
    
    def _init_editor_functions(self):
        """
        Initialize the editor functions that are called on the TextDiffer widget,
        but need to be executed on one of the editors
        """
        #Find text function propagated to the focused editor
        def enabled_function(*args, **kwargs):
            #Get the function
            function = getattr(self.focused_editor, args[0])
            #Call the function˘, leaving out the "function name" argument
            function(*args[1:], **kwargs)
        #Unimplemented functions
        def uniplemented_function(*args, **kwargs):
            self.main_form.display.repl_display_message(
                "Function '{:s}' is not implemented by the TextDiffer!".format(args[0]), 
                message_type=data.MessageType.ERROR
            )
        all_editor_functions  = inspect.getmembers(
                                    forms.CustomEditor, 
                                    predicate=inspect.isfunction
                                )
        enabled_functions = [
                                "find_text", 
                            ]
        disabled_functions =  [
                                "__init__",
                                "__setattr__",
                                "_filter_keypress",
                                "_filter_keyrelease",
                                "_init_special_functions",
                                "_set_indicator",
                                "find_text",
                                "keyPressEvent",
                                "keyReleaseEvent",
                                "mousePressEvent",
                                "setFocus",
                                "wheelEvent",
                            ]
        #Check methods
        for function in all_editor_functions:
            if function[0] in enabled_functions:
                #Find text is enabled
                setattr(
                    self, 
                    function[0], 
                    functools.partial(enabled_function, function[0])
                )
            elif function[0] in disabled_functions:
                #Disabled functions should be skipped, they are probably already
                #implemented by the TextDiffer
                continue
            else:
                #Unimplemented functions should display an error message
                setattr(
                    self, 
                    function[0], 
                    functools.partial(uniplemented_function, function[0])
                )
        
    def mousePressEvent(self, event):
        """Overloaded mouse click event"""
        #Execute the superclass mouse click event
        super().mousePressEvent(event)
        #Set focus to the clicked editor
        self.setFocus()
        #Set the last focused widget to the parent basic widget
        self.main_form.last_focused_widget = self.parent
        data.print_log("Stored \"{:s}\" as last focused widget".format(self.parent.name))
        #Hide the function wheel if it is shown
        if self.main_form.view.function_wheel_overlay != None:
            self.main_form.view.hide_function_wheel()
    
    def setFocus(self):
        """Overridden focus event"""
        #Execute the superclass focus function
        super().setFocus()
        #Check indication
        self.main_form.view.indication_check()
        #Focus the last focused editor
        self.focused_editor.setFocus()
    
    def init_margin(self, 
                    editor, 
                    marker_unique, 
                    marker_unique_symbol, 
                    marker_similar, 
                    marker_similar_symbol):
        """Initialize margin for coloring lines showing diff symbols"""
        editor.setMarginWidth(0, "0")
        #Setting the margin width to 0 makes the marker colour the entire line
        #to the marker background color
        editor.setMarginWidth(1, "00")
        editor.setMarginWidth(2, 0)        
        editor.setMarginType(0, PyQt4.Qsci.QsciScintilla.TextMargin)
        editor.setMarginType(1, PyQt4.Qsci.QsciScintilla.SymbolMargin)
        editor.setMarginType(2, PyQt4.Qsci.QsciScintilla.SymbolMargin)
        #I DON'T KNOW THE ENTIRE LOGIC BEHIND MARKERS AND MARGINS! If you set 
        #something wrong in the margin mask, the markers on a different margin don't appear!
        #http://www.scintilla.org/ScintillaDoc.html#SCI_SETMARGINMASKN
        editor.setMarginMarkerMask(
            1,
            ~PyQt4.Qsci.QsciScintillaBase.SC_MASK_FOLDERS 
        )
        editor.setMarginMarkerMask(
            2, 
            0x0
        )
    
    def init_markers(self):
        """Initialize all markers for showing diff symbols"""
        #Set the images
        image_scale_size = PyQt4.QtCore.QSize(16, 16)
        image_unique_1  = set_pixmap('tango_icons/diff-unique-1.png')
        image_unique_2  = set_pixmap('tango_icons/diff-unique-2.png')
        image_similar   = set_pixmap('tango_icons/diff-similar.png')
        #Scale the images to a smaller size
        image_unique_1  = image_unique_1.scaled(image_scale_size)
        image_unique_2  = image_unique_2.scaled(image_scale_size)
        image_similar   = image_similar.scaled(image_scale_size)
        #Markers for editor 1
        self.marker_unique_1            = self.editor_1.markerDefine(PyQt4.Qsci.QsciScintillaBase.SC_MARK_BACKGROUND, 0)
        self.marker_unique_symbol_1     = self.editor_1.markerDefine(image_unique_1, 1)
        self.marker_similar_1           = self.editor_1.markerDefine(PyQt4.Qsci.QsciScintillaBase.SC_MARK_BACKGROUND, 2)
        self.marker_similar_symbol_1    = self.editor_1.markerDefine(image_similar, 3)
        #Set background colors only for the background markers
        self.editor_1.setMarkerBackgroundColor(self.INDICATOR_UNIQUE_1_COLOR, self.marker_unique_1)
        self.editor_1.setMarkerBackgroundColor(self.INDICATOR_SIMILAR_COLOR, self.marker_similar_1)
        #Margins for editor 1
        self.init_margin(
            self.editor_1, 
            self.marker_unique_1, 
            self.marker_unique_symbol_1, 
            self.marker_similar_1, 
            self.marker_similar_symbol_1
        )
        #Markers for editor 2
        self.marker_unique_2            = self.editor_2.markerDefine(PyQt4.Qsci.QsciScintillaBase.SC_MARK_BACKGROUND, 0)
        self.marker_unique_symbol_2     = self.editor_2.markerDefine(image_unique_2, 1)
        self.marker_similar_2           = self.editor_2.markerDefine(PyQt4.Qsci.QsciScintillaBase.SC_MARK_BACKGROUND, 2)
        self.marker_similar_symbol_2    = self.editor_2.markerDefine(image_similar, 3)
        #Set background colors only for the background markers
        self.editor_2.setMarkerBackgroundColor(self.INDICATOR_UNIQUE_2_COLOR, self.marker_unique_2)
        self.editor_2.setMarkerBackgroundColor(self.INDICATOR_SIMILAR_COLOR, self.marker_similar_2)
        #Margins for editor 2
        self.init_margin(
            self.editor_2, 
            self.marker_unique_2, 
            self.marker_unique_symbol_2, 
            self.marker_similar_2, 
            self.marker_similar_symbol_2
        )
    
    def init_indicator(self,
                       editor, 
                       indicator, 
                       color):
        """Set the indicator settings"""
        editor.indicatorDefine(
            PyQt4.Qsci.QsciScintillaBase.INDIC_ROUNDBOX,
            indicator
        )
        editor.setIndicatorForegroundColor(
            color, 
            indicator
        )
        editor.SendScintilla(
            PyQt4.Qsci.QsciScintillaBase.SCI_SETINDICATORCURRENT, 
            indicator
        )
    
    def init_editor(self, editor):
        """Initialize all of the PlainEditor settings for difference displaying"""
        editor.setLexer(None)
        editor.setUtf8(True)
        editor.setIndentationsUseTabs(False)
        editor.setFont(self.DEFAULT_FONT)
        editor.setBraceMatching(PyQt4.Qsci.QsciScintilla.SloppyBraceMatch)
        editor.setMatchedBraceBackgroundColor(PyQt4.QtGui.QColor(255, 153, 0))
        editor.setAcceptDrops(False)
        editor.setEolMode(PyQt4.Qsci.QsciScintilla.EolUnix)
        editor.setReadOnly(True)
        editor.savable = data.CanSave.NO
    
    def set_margin_text(self, editor, line, text):
        """Set the editor's margin text at the selected line"""
        editor.setMarginText(line, text, self.MARGIN_STYLE)
    
    def set_line_indicator(self, editor, line, indicator_index):
        """Set the editor's selected line color"""
        #Set the indicator
        if indicator_index == self.INDICATOR_UNIQUE_1:
            self.init_indicator(
                editor, 
                self.INDICATOR_UNIQUE_1, 
                self.INDICATOR_UNIQUE_1_COLOR
            )
        elif indicator_index == self.INDICATOR_UNIQUE_2:
            self.init_indicator(
                editor, 
                self.INDICATOR_UNIQUE_2, 
                self.INDICATOR_UNIQUE_2_COLOR
            )
        elif indicator_index == self.INDICATOR_SIMILAR:
            self.init_indicator(
                editor, 
                self.INDICATOR_SIMILAR, 
                self.INDICATOR_SIMILAR_COLOR
            )
        #Color the line background
        scintilla_command = PyQt4.Qsci.QsciScintillaBase.SCI_INDICATORFILLRANGE
        start   = editor.positionFromLineIndex(line, 0)
        length  = editor.lineLength(line)
        editor.SendScintilla(
            scintilla_command, 
            start, 
            length
        )
    
    def compare(self, text_1, text_2):
        """
        Compare two text strings and display the difference
        !! This function uses Python's difflib which is not 100% accurate !!
        """
        #Store the original text
        self.text_1 = text_1
        self.text_2 = text_2
        text_1_list = text_1.split("\n")
        text_2_list = text_2.split("\n")
        #Create the difference
        differer = difflib.Differ()
        list_sum = list(differer.compare(text_1_list, text_2_list))
        #Assemble the two lists of strings that will be displayed in each editor
        list_1              = []
        line_counter_1      = 1
        line_numbering_1    = []
        line_styling_1      = []
        list_2              = []
        line_counter_2      = 1
        line_numbering_2    = []
        line_styling_2      = []
        #Flow control flags
        skip_next     = False
        store_next    = False
        for i, line in enumerate(list_sum):
            if store_next == True:
                store_next = False
                list_2.append(line[2:])
                line_numbering_2.append(str(line_counter_2))
                line_counter_2 += 1
                line_styling_2.append(self.INDICATOR_SIMILAR)
            elif skip_next == False:
                if line.startswith("  "):
                    #The line is the same in both texts
                    list_1.append(line[2:])
                    line_numbering_1.append(str(line_counter_1))
                    line_counter_1 += 1
                    line_styling_1.append(None)
                    list_2.append(line[2:])
                    line_numbering_2.append(str(line_counter_2))
                    line_counter_2 += 1
                    line_styling_2.append(None)
                elif line.startswith("- "):
                    #The line is unique to text 1
                    list_1.append(line[2:])
                    line_numbering_1.append(str(line_counter_1))
                    line_counter_1 += 1
                    line_styling_1.append(self.INDICATOR_UNIQUE_1)
                    list_2.append("")
                    line_numbering_2.append("")
                    line_styling_2.append(None)
                elif line.startswith("+ "):
                    #The line is unique to text 2
                    list_1.append("")
                    line_numbering_1.append("")
                    line_styling_1.append(None)
                    list_2.append(line[2:])
                    line_numbering_2.append(str(line_counter_2))
                    line_counter_2 += 1
                    line_styling_2.append(self.INDICATOR_UNIQUE_2)
                elif line.startswith("? "):
                    #The line is similar
                    if (list_sum[i-1].startswith("- ") and
                        list_sum[i+1].startswith("+ ") and
                        list_sum[i+2].startswith("? ")):
                        """
                        Line order:
                            - ...
                            ? ...
                            + ...
                            ? ...
                        """
                        #Lines have only a few character difference, skip the 
                        #first '?' and handle the next '?' as a "'- '/'+ '/'? '" sequence
                        pass
                    elif list_sum[i-1].startswith("- "):
                        #Line in text 1 has something added
                        """
                        Line order:
                            - ...
                            ? ...
                            + ...
                        """
                        line_styling_1[len(line_numbering_1) - 1] = self.INDICATOR_SIMILAR
                        
                        list_2.pop()
                        line_numbering_2.pop()
                        line_styling_2.pop()
                        store_next = True
                    elif list_sum[i-1].startswith("+ "):
                        #Line in text 2 has something added
                        """
                        Line order:
                            - ...
                            + ...
                            ? ...
                        """
                        list_1.pop()
                        line_numbering_1.pop()
                        line_styling_1.pop()
                        line_styling_1[len(line_numbering_1) - 1] = self.INDICATOR_SIMILAR
                        
                        pop_index_2 = (len(line_numbering_2) - 1) - 1
                        list_2.pop(pop_index_2)
                        line_numbering_2.pop(pop_index_2)
                        line_styling_2.pop()
                        line_styling_2.pop()
                        line_styling_2.append(self.INDICATOR_SIMILAR)
            else:
                skip_next = False
        #Display the results
        self.editor_1.setText("\n".join(list_1))
        self.editor_2.setText("\n".join(list_2))
        #Set margins and style for both editors
        for i, line in enumerate(line_numbering_1):
            self.set_margin_text(self.editor_1, i, line)
            line_styling = line_styling_1[i]
            if line_styling != None:
                if line_styling == self.INDICATOR_SIMILAR:
                    self.editor_1.markerAdd(i, self.marker_similar_1)
                    self.editor_1.markerAdd(i, self.marker_similar_symbol_1)
                else:
                    self.editor_1.markerAdd(i, self.marker_unique_1)
                    self.editor_1.markerAdd(i, self.marker_unique_symbol_1)
        for i, line in enumerate(line_numbering_2):
            self.set_margin_text(self.editor_2, i, line)
            line_styling = line_styling_2[i]
            if line_styling != None:
                if line_styling == self.INDICATOR_SIMILAR:
                    self.editor_2.markerAdd(i, self.marker_similar_2)
                    self.editor_2.markerAdd(i, self.marker_similar_symbol_2)
                else:
                    self.editor_2.markerAdd(i, self.marker_unique_2)
                    self.editor_2.markerAdd(i, self.marker_unique_symbol_2)
        #Check if there were any differences
        if (any(line_styling_1) == False and any(line_styling_2) == False):
            self.main_form.display.repl_display_message(
                "No differences between texts.", 
                message_type=data.MessageType.SUCCESS
            )
        else:
            #Count the number of differences
            difference_counter_1 = 0
            #Similar line count is the same in both editor line stylings
            similarity_counter = 0
            for diff in line_styling_1:
                if diff != None:
                    if diff == self.INDICATOR_SIMILAR:
                        similarity_counter += 1
                    else:
                        difference_counter_1 += 1
            difference_counter_2 = 0
            for diff in line_styling_2:
                if diff != None:
                    if diff == self.INDICATOR_SIMILAR:
                        #Skip the similar line, which were already counter above
                        continue
                    else:
                        difference_counter_2 += 1
            #Display the differences/similarities messages
            self.main_form.display.repl_display_message(
                "{:d} differences found in '{:s}'!".format(difference_counter_1, self.text_1_name), 
                message_type=data.MessageType.DIFF_UNIQUE_1
            )
            self.main_form.display.repl_display_message(
                "{:d} differences found in '{:s}'!".format(difference_counter_2, self.text_2_name), 
                message_type=data.MessageType.DIFF_UNIQUE_2
            )
            self.main_form.display.repl_display_message(
                "{:d} similarities found between documents!".format(similarity_counter, self.text_2_name), 
                message_type=data.MessageType.DIFF_SIMILAR
            )
        self._update_margins()
    
    def find_next_unique_1(self):
        """Find and scroll to the first unique 1 difference"""
        self.focused_editor         = self.editor_1
        cursor_line, cursor_index   = self.editor_1.getCursorPosition()
        next_unique_diff_line = self.editor_1.markerFindNext(cursor_line+1, 0b0011)
        #Correct the line numbering to the 1..line_count display
        next_unique_diff_line += 1
        self.editor_1.goto_line(next_unique_diff_line)
        self.editor_2.goto_line(next_unique_diff_line)
        #Check if we are back at the start of the document
        if next_unique_diff_line == 0:
            self.main_form.display.repl_display_message(
                "Scrolled back to the start of the document!", 
                message_type=data.MessageType.DIFF_UNIQUE_1
            )
            self.main_form.display.write_to_statusbar(
                "Scrolled back to the start of the document!"
            )
    
    def find_next_unique_2(self):
        """Find and scroll to the first unique 2 difference"""
        self.focused_editor         = self.editor_2
        cursor_line, cursor_index   = self.editor_2.getCursorPosition()
        next_unique_diff_line = self.editor_2.markerFindNext(cursor_line+1, 0b0011)
        #Correct the line numbering to the 1..line_count display
        next_unique_diff_line += 1
        self.editor_1.goto_line(next_unique_diff_line)
        self.editor_2.goto_line(next_unique_diff_line)
        #Check if we are back at the start of the document
        if next_unique_diff_line == 0:
            self.main_form.display.repl_display_message(
                "Scrolled back to the start of the document!", 
                message_type=data.MessageType.DIFF_UNIQUE_2
            )
            self.main_form.display.write_to_statusbar(
                "Scrolled back to the start of the document!"
            )
    
    def find_next_similar(self):
        """Find and scroll to the first similar line"""
        self.focused_editor         = self.editor_1
        cursor_line, cursor_index   = self.editor_1.getCursorPosition()
        next_unique_diff_line = self.editor_1.markerFindNext(cursor_line+1, 0b1100)
        #Correct the line numbering to the 1..line_count display
        next_unique_diff_line += 1
        self.editor_1.goto_line(next_unique_diff_line)
        self.editor_2.goto_line(next_unique_diff_line)
        #Check if we are back at the start of the document
        if next_unique_diff_line == 0:
            self.main_form.display.repl_display_message(
                "Scrolled back to the start of the document!", 
                message_type=data.MessageType.DIFF_SIMILAR
            )
            self.main_form.display.write_to_statusbar(
                "Scrolled back to the start of the document!"
            )
    
    def show_find_buttons(self, parent):
        """
        Create and display buttons for finding unique/similar differences
        on the parent basic widget
        """
        #Check if the parent is a basic widget
        if isinstance(parent, forms.BasicWidget) == False:
            return
        #Create the find toolbar and buttons
        find_toolbar = PyQt4.QtGui.QToolBar(parent)
        find_toolbar.setIconSize(PyQt4.QtCore.QSize(16,16))
        unique_1_action =   PyQt4.QtGui.QAction(
                                set_icon("tango_icons/diff-unique-1.png"), 
                                "unique_1_button",
                                parent
                            )
        unique_1_action.setToolTip(
            "Scroll to next unique line\nin document: '{:s}'".format(self.text_1_name)
        )
        unique_1_action.triggered.connect(self.find_next_unique_1)
        unique_2_action =   PyQt4.QtGui.QAction(
                                set_icon("tango_icons/diff-unique-2.png"), 
                                "unique_2_button",
                                parent
                            )
        unique_2_action.setToolTip(
            "Scroll to next unique line\nin document: '{:s}'".format(self.text_2_name)
        )
        unique_2_action.triggered.connect(self.find_next_unique_2)
        similar_action =   PyQt4.QtGui.QAction(
                                set_icon("tango_icons/diff-similar.png"), 
                                "unique_2_button",
                                parent
                            )
        similar_action.setToolTip(
            "Scroll to next similar line\nin both documents"
        )
        similar_action.triggered.connect(self.find_next_similar)
        find_toolbar.addAction(unique_1_action)
        find_toolbar.addAction(unique_2_action)
        find_toolbar.addAction(similar_action)
        find_toolbar.show()
        #Set the corner widget of the parent
        parent.setCornerWidget(find_toolbar)



"""
----------------------------------------------------------------------------
Object for showing log messages across all widgets, mostly for debug purposes
----------------------------------------------------------------------------
"""
class MessageLogger(PyQt4.QtGui.QWidget):
    """Simple subclass for displaying log messages"""
    #Controls and variables of the log window  (class variables >> this means that these variables are shared accross instances of this class)
    displaybox  = None      #QTextEdit that will display log messages
    layout      = None      #The layout of the log window
    parent      = None
    
    def __init__(self, parent):
        """Initialization routine"""
        #Initialize superclass, from which the current class is inherited, THIS MUST BE DONE SO THAT THE SUPERCLASS EXECUTES ITS __init__ !!!!!!
        super().__init__()
        
        #Initialize the log window
        self.setWindowTitle("LOGGING WINDOW")
        self.resize(500, 300)
        self.setWindowFlags(PyQt4.QtCore.Qt.WindowStaysOnTopHint)
        
        #Initialize the display box
        self.displaybox = PyQt4.QtGui.QTextEdit(self)
        self.displaybox.setReadOnly(True)
        #Make displaybox click/doubleclick event also fire the log window click/doubleclick method
        self.displaybox.mousePressEvent         = self._event_mousepress
        self.displaybox.mouseDoubleClickEvent   = self._event_mouse_doubleclick
        self.keyPressEvent                      = self._keypress
        
        #Initialize layout
        self.layout = PyQt4.QtGui.QGridLayout()
        self.layout.addWidget(self.displaybox)
        self.setLayout(self.layout)
        
        self.append_message("Ex.Co. debug log window loaded")
        self.append_message("LOGGING Mode is enabled")
        self.parent = parent
        
        #Set the log window icon
        if os.path.isfile(data.application_icon) == True:
            self.setWindowIcon(PyQt4.QtGui.QIcon(data.application_icon))
    
    def _event_mouse_doubleclick(self, mouse_event):
        """Rereferenced/overloaded displaybox doubleclick event"""
        self.clear_log()
    
    def _event_mousepress(self, mouse_event):
        """Rereferenced/overloaded displaybox click event"""
        pass
    
    def _keypress(self, key_event):
        """Rereferenced/overloaded MessageLogger keypress event"""
        pressed_key = key_event.key()
        if pressed_key == PyQt4.QtCore.Qt.Key_Escape:
            self.close()
    
    def clear_log(self):
        """Clear all messages from the log display"""
        self.displaybox.clear()
        
    def append_message(self,  message):
        """Adds a message as a string to the log display if logging mode is enabled"""
        #Check if message is a string class, if not then make it a string
        if isinstance(message, str) == False:
            message = str(message)
        #Check if logging mode is enabled
        if data.logging_mode == True:
            self.displaybox.append(message)
        #Bring cursor to the current message (this is in a QTextEdit not QScintilla)
        cursor = self.displaybox.textCursor()
        cursor.movePosition(PyQt4.QtGui.QTextCursor.End)
        cursor.movePosition(PyQt4.QtGui.QTextCursor.StartOfLine)
        self.displaybox.setTextCursor(cursor)



"""
-----------------------------------------------------------------------------------
ExCo Information Widget for displaying the license, used languages and libraries, ...
-----------------------------------------------------------------------------------
"""
class ExCoInfo(PyQt4.QtGui.QDialog):
    #Class variables
    name    = "Ex.Co. Info"
    savable = data.CanSave.NO
    
    #Class functions(methods)
    def __init__(self, parent, app_dir=""):
        """Initialization routine"""
        #Initialize superclass, from which the current class is inherited,
        #THIS MUST BE DONE SO THAT THE SUPERCLASS EXECUTES ITS __init__ !!!!!!
        super().__init__()
        #Setup the window
        self.setWindowTitle("About Ex.Co.")
        self.setWindowFlags(PyQt4.QtCore.Qt.WindowStaysOnTopHint)
        #Setup the picture
        exco_picture    = PyQt4.QtGui.QPixmap(data.about_image)
        self.picture    = PyQt4.QtGui.QLabel(self)
        self.picture.setPixmap(exco_picture)
        self.picture.setGeometry(self.frameGeometry())
        self.picture.setScaledContents(True)
        #Assign events
        self.picture.mousePressEvent        = self._close
        self.picture.mouseDoubleClickEvent  = self._close
        #Initialize layout
        self.layout = PyQt4.QtGui.QGridLayout()
        self.layout.addWidget(self.picture)
        self.layout.setSpacing(0)
        self.layout.setMargin(0)
        self.setLayout(self.layout)
        #Set the log window icon
        if os.path.isfile(data.application_icon) == True:
            self.setWindowIcon(PyQt4.QtGui.QIcon(data.application_icon))
        #Save the info window geometry, the values were gotten by showing a dialog with the label containing
        #the Exco_Info.png image with the size set to (50, 50), so it would automatically resize to the label image size
        my_width    = 610
        my_height   = 620
        #Set the info window position
        parent_left     = parent.geometry().left()
        parent_top      = parent.geometry().top()
        parent_width    = parent.geometry().width()
        parent_height   = parent.geometry().height()
        my_left = parent_left + (parent_width/2) - (my_width/2)
        my_top = parent_top + (parent_height/2) - (my_height/2)
        self.setGeometry(PyQt4.QtCore.QRect(my_left, my_top, my_width, my_height))
        self.setFixedSize(my_width, my_height)
#        self.setStyleSheet("background-color:transparent;")
#        self.setWindowFlags(PyQt4.QtCore.Qt.WindowStaysOnTopHint | PyQt4.QtCore.Qt.Dialog | PyQt4.QtCore.Qt.FramelessWindowHint)
#        self.setAttribute(PyQt4.QtCore.Qt.WA_TranslucentBackground)

    def _close(self, event):
        """Close the widget"""
        self.close()
