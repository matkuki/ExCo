
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2019 Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import os
import sip
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

from .dialogs import *


"""
-------------------------------------------------
GUI Session manipulation object
-------------------------------------------------
"""
class SessionGuiManipulator(data.QTreeView):
    """
    GUI object for easier user editing of sessions
    """
    class SessionItem(data.QStandardItem):
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
    current_icon            = None
    icon_manipulator        = None
    name                    = ""
    savable                 = data.CanSave.NO
    last_clicked_session    = None
    tree_model              = None
    session_nodes           = None
    refresh_lock            = False
    edit_flag               = False
    last_created_item       = None
    session_groupbox        = None
    #Icons
    node_icon_group         = None
    node_icon_session       = None
    icon_session_add        = None
    icon_session_remove     = None
    icon_session_overwrite  = None
    icon_group_add          = None
    icon_session_edit       = None
    
    
    def clean_up(self):
        # Disconnect signals
        self.doubleClicked.disconnect()
        # Clean up main references
        self._parent = None
        self.main_form = None
        self.settings_manipulator = None
        self.icon_manipulator = None
        if self.session_groupbox != None:
            self.session_groupbox.setParent(None)
            self.session_groupbox.deleteLater()
            self.session_groupbox = None
        # Clean up self
        self.setParent(None)
        self.deleteLater()
    
    def __init__(self, settings_manipulator, parent, main_form):
        """Initialization"""
        #Initialize the superclass
        super().__init__(parent)
        # Initialize components
        self.icon_manipulator = components.IconManipulator(
            parent=self, basic_widget=parent
        )
        self.add_corner_buttons()
        #Store the reference to the parent BasicWidget from the "forms" module
        self._parent = parent
        #Store the reference to the MainWindow form from the "forms" module
        self.main_form = main_form
        # Set default font
        self.setFont(data.get_current_font())
        #Store the reference to the active SettingsManipulator
        self.settings_manipulator = settings_manipulator
        #Set the icon
        self.current_icon = functions.create_icon("tango_icons/sessions.png")
        #Store name of self
        self.name = "Session editing tree display"
        #Enable node expansion on double click
        self.setExpandsOnDoubleClick(True)
        #Set the node icons
        self.node_icon_group        = functions.create_icon("tango_icons/folder.png")
        self.node_icon_session      = functions.create_icon("tango_icons/sessions.png")
        self.icon_session_add       = functions.create_icon("tango_icons/session-add.png")
        self.icon_session_remove    = functions.create_icon("tango_icons/session-remove.png")
        self.icon_session_overwrite = functions.create_icon("tango_icons/session-overwrite.png")
        self.icon_group_add         = functions.create_icon("tango_icons/folder-add.png")
        self.icon_session_edit      = functions.create_icon("tango_icons/session-edit.png")
        #Connect the signals
        self.doubleClicked.connect(self._item_double_clicked)
    
    def clean_model(self):
        if self.model() != None:
            self.model().setParent(None)
            self.setModel(None)
    
    def mousePressEvent(self, event):
        """Function connected to the clicked signal of the tree display"""
        super().mousePressEvent(event)
        #Set the focus
        self.setFocus()
        #Set the last focused widget to the parent basic widget
        self.main_form.last_focused_widget = self._parent
        data.print_log("Stored \"{:s}\" as last focused widget".format(self._parent.name))
        #Set Save/SaveAs buttons in the menubar
        self._parent._set_save_status()
        # Reset the click&drag context menu action
        components.ActionFilter.clear_action()
    
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
                    self.settings_manipulator.main_window_side, 
                    data.theme
                )
                #Update the main forms session menu
                self.main_form.sessions.update_menu()
                #Display successful group deletion
                group_name = item.session.group
                if group_name == None:
                    group_name = ""
                else:
                    group_name = " / ".join(group_name) + " / "
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
                    self.settings_manipulator.main_window_side, 
                    data.theme
                )
                #Update the main forms session menu
                self.main_form.sessions.update_menu()
                #Display successful group deletion
                self.main_form.display.repl_display_message(
                    "Group '{}' was renamed to '{}'!".format(
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
                if item.name == None:
                    item.name = group_name
                    if hasattr(item, "parent_group") == True:
                        item.name = (group_name, )
                        if item.parent_group != None:
                            item.name = item.parent_group + (group_name, )
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
        for group in self.groups:
            if self.isExpanded(group.index()):
                expanded_groups.append(group)
        #Remove the empty node by refreshing the session tree
        self.show_sessions()
        #Expand the groups that were expanded before
        for exp_group in expanded_groups:
            for group in self.groups:
                if group.name == exp_group.name:
                    self.expand(group.index())
    
    def _get_current_group(self):
        if self.selectedIndexes() != []:
            selected_item = self.tree_model.itemFromIndex(self.selectedIndexes()[0])
            if selected_item.type == self.ItemType.SESSION:
                if selected_item.session.group != None:
                    return selected_item.parent()
                else:
                    return None
            elif (selected_item.type == self.ItemType.GROUP or 
                  selected_item.type == self.ItemType.EMPTY_GROUP):
                return selected_item
            else:
                return None
        else:
            return None
    
    def add_empty_group(self):
        #Check for various flags
        if self.edit_flag == True:
            return
        #Check if an empty group is already present
#        for session_node in self.session_nodes:
#            if session_node.type == self.ItemType.EMPTY_GROUP:
#                return
        empty_group_node = self.SessionItem("")
        empty_group_node.parent    = self
        empty_group_node.name      = None
        empty_group_node.parent_group   = None
        empty_group_node.session   = None
        empty_group_node.type      = self.ItemType.EMPTY_GROUP
        empty_group_node.setEditable(True)
        empty_group_node.setIcon(self.node_icon_group)
        parent_group = self._get_current_group()
        if parent_group != None:
            empty_group_node.parent_group = parent_group.name
            parent_group.appendRow(empty_group_node)
        else:
            self.tree_model.appendRow(empty_group_node)
        self.scrollTo(empty_group_node.index())
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
        #Initialize the session
        empty_session = settings.Session("")
        empty_session_node = self.SessionItem("")
        empty_session_node.parent    = self
        empty_session_node.name      = ""
        empty_session_node.session   = empty_session
        empty_session_node.type      = self.ItemType.EMPTY_SESSION
        empty_session_node.setEditable(True)
        empty_session_node.setIcon(self.node_icon_session)
        parent_group = self._get_current_group()
        if parent_group != None:
            empty_session.group = parent_group.name
            parent_group.appendRow(empty_session_node)
            self.expand(parent_group.index())
        else:
            self.tree_model.appendRow(empty_session_node)
        self.scrollTo(empty_session_node.index())
        #Start editing the new empty session
        self.session_nodes.append(empty_session_node)
        self.edit(empty_session_node.index())
        #Add the session signal when editing is canceled
        delegate = self.itemDelegate(empty_session_node.index())
        delegate.closeEditor.connect(self._item_editing_closed)
        #Store last created node type
        self.last_created_item = self.ItemType.EMPTY_SESSION
    
    def remove_session(self):
        # Check for various flags
        if self.edit_flag == True:
            return
        # Check if an item is selected
        if self.selectedIndexes() == []:
            return
        selected_item = self.tree_model.itemFromIndex(self.selectedIndexes()[0])
        # Check the selected item type
        if selected_item.type == self.ItemType.GROUP:
            remove_group = selected_item.name
            # Adjust the group name string
            if remove_group == None:
                selected_item.name = ""
            remove_group_name = ""
            if remove_group != "":
                remove_group_name = "/".join(remove_group) + "/"
            
            # First add all of the groups, if any
            groups = self.settings_manipulator.get_sorted_groups()
            # Check if the group has subgroups
            main_group = self.settings_manipulator.Group(
                "BASE", parent=None, reference=self.tree_model
            )
            current_group = selected_item.name
            for group in groups:
                if (len(group) > len(remove_group)) and (set(remove_group).issubset(group)):
                    message =  "Cannot delete group\n'{:s}'\n".format(remove_group_name)
                    message += "because it contains subgroups!"
                    reply = OkDialog.error(message)
                    return
            
            message =  "Are you sure you want to delete group:\n"
            message += "'{:s}' ?".format(remove_group_name)
            reply = YesNoDialog.warning(message)
            if reply == data.QMessageBox.No:
                return
            # Delete the group
            result = self.settings_manipulator.remove_group(remove_group)
            # Display the deletion result
            if result == True:
                self.main_form.display.repl_display_message(
                    "Group '{:s}' was deleted!".format(remove_group_name), 
                    message_type=data.MessageType.SUCCESS
                )
            else:
                message = "An error occured while deleting session "
                message += "group '{:s}'!".format(remove_group_name)
                self.main_form.display.repl_display_message(
                    message, 
                    message_type=data.MessageType.ERROR
                )
            # Refresh the tree
            self.refresh_display()
        elif selected_item.type == self.ItemType.SESSION:
            remove_session = selected_item.session
            # Adjust the group name string
            if remove_session.group == None:
                remove_session.group = ""
            group_name = ""
            if remove_session.group != "":
                group_name = "/".join(remove_session.group) + "/"
            message =  "Are you sure you want to delete session:\n"
            message += "'{:s}{:s}' ?".format(group_name, remove_session.name)
            reply = YesNoDialog.warning(message)
            if reply == data.QMessageBox.No:
                return
            # Delete the session
            # Delete all of the session with the group name
            for session in self.settings_manipulator.stored_sessions:
                if (session.name == remove_session.name and
                    session.group == remove_session.group):
                    self.main_form.sessions.remove(session.name, session.group)
                    break
            # Refresh the tree
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
        self.tree_model = data.QStandardItemModel()
        self.tree_model.setHorizontalHeaderLabels(["SESSIONS"])
        self.header().hide()
#        self.clean_model()
        self.setModel(self.tree_model)
        self.setUniformRowHeights(True)
        #Connect the tree model signals
        self.tree_model.itemChanged.connect(self._item_changed)
        font = data.QFont(data.current_font_name, data.current_font_size, data.QFont.Bold)
        #First add all of the groups, if any
        groups = self.settings_manipulator.get_sorted_groups()
        self.groups = []
        # Create the Sessions menu
        main_group = self.settings_manipulator.Group(
            "BASE", parent=None, reference=self.tree_model
        )
        for group in groups:
            current_node = main_group
            level_counter = 1
            for folder in group:
                new_group = current_node.subgroup_get(folder)
                if new_group == None:
                    item_group_node = self.SessionItem(folder)
                    item_group_node.setFont(font)
                    item_group_node.my_parent   = self
                    item_group_node.name        = group[:level_counter]
                    item_group_node.session     = None
                    item_group_node.type        = self.ItemType.GROUP
                    item_group_node.setEditable(False)
                    item_group_node.setIcon(self.node_icon_group)
                    current_node.reference.appendRow(item_group_node)
                current_node = current_node.subgroup_create(folder, item_group_node)
                self.groups.append(item_group_node)
                level_counter += 1
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
                group = main_group.subgroup_get_recursive(session.group)
                group.reference.appendRow(item_session_node)
            else:
                main_group.reference.appendRow(item_session_node)
            #Append the session to the stored node list
            self.session_nodes.append(item_session_node)
    
    def add_corner_buttons(self):
        # Edit session
        self.icon_manipulator.add_corner_button(
            "tango_icons/session-edit.png",
            "Edit the selected item",
            self.edit_item
        )
        # Overwrite session
        self.icon_manipulator.add_corner_button(
            "tango_icons/session-overwrite.png",
            "Overwrite the selected session",
            self.overwrite_session
        )
        # Add group
        self.icon_manipulator.add_corner_button(
            "tango_icons/folder-add.png",
            "Add a new group",
            self.add_empty_group
        )
        # Add session
        self.icon_manipulator.add_corner_button(
            "tango_icons/session-add.png",
            "Add a new session",
            self.add_empty_session
        )
        # Remove session
        self.icon_manipulator.add_corner_button(
            "tango_icons/session-remove.png",
            "Remove the selected session",
            self.remove_session
        )



