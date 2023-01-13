
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2023 Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import os
import os.path
import time
import difflib
import inspect
import textwrap
import functools
import traceback
import collections

import data
import settings
import functions
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
        my_parent = None
        name      = None
        type      = None
    
    #Class constants
    class ItemType:
        SESSION       = 0
        GROUP         = 1
        EMPTY_SESSION = 2
        EMPTY_GROUP   = 3
    
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
    edit_flag               = False
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
        # Initialize the superclass
        super().__init__(parent)
        # Initialize components
        self.icon_manipulator = components.IconManipulator(
            parent=self, tab_widget=parent
        )
        self.add_corner_buttons()
        # Store the reference to the parent TabWidget from the "forms" module
        self._parent = parent
        # Store the reference to the MainWindow form from the "forms" module
        self.main_form = main_form
        # Set default font
        self.setFont(data.get_current_font())
        # Store the reference to the active SettingsManipulator
        self.settings_manipulator = settings_manipulator
        # Set the icon
        self.current_icon = functions.create_icon("tango_icons/sessions.png")
        # Store name of self
        self.name = "Session editing tree display"
        # Enable node expansion on double click
        self.setExpandsOnDoubleClick(True)
        # Set the node icons
        self.node_icon_group        = functions.create_icon("tango_icons/folder.png")
        self.node_icon_session      = functions.create_icon("tango_icons/sessions.png")
        self.icon_session_add       = functions.create_icon("tango_icons/session-add.png")
        self.icon_session_remove    = functions.create_icon("tango_icons/session-remove.png")
        self.icon_session_overwrite = functions.create_icon("tango_icons/session-overwrite.png")
        self.icon_group_add         = functions.create_icon("tango_icons/folder-add.png")
        self.icon_session_edit      = functions.create_icon("tango_icons/session-edit.png")
        # Connect the signals
        self.doubleClicked.connect(self.__item_double_clicked)
        self.itemDelegate().closeEditor.connect(self.__item_editing_closed)
    
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
    
    def __item_double_clicked(self, model_index):
        """Callback connected to the treeview's 'clicked' signal"""
        session_item = self.tree_model.itemFromIndex(model_index)
        if session_item.type == self.ItemType.SESSION:
            # Open the session
            session = self.settings_manipulator.get_session(
                session_item.text(),
                self.__get_node_chain(session_item)
            )
            self.main_form.sessions.restore(session)
        elif session_item.type == self.ItemType.GROUP:
            pass
    
    def __item_changed(self, item):
        """
        Callback connected to the displays QStandardItemModel 'itemChanged' signal
        """
        # Get the clicked item
        changed_item = item
        # Check for editing
        if self.edit_flag == True:
            if changed_item.type == self.ItemType.SESSION:
                self.reset_locks()
                # Item is a session
                old_item_name = item.name
                new_item_name = self.indexWidget(item.index()).text()
                item_chain = self.__get_node_chain(item)
                # Rename 
                group = self.settings_manipulator.get_group(item_chain)
                session = group["sessions"].pop(old_item_name)
                item.name = new_item_name
                item.setEditable(False)
                session["name"] = new_item_name
                group["sessions"][new_item_name] = session
                # Save the the new session list by saving the settings
                self.settings_manipulator.save_settings(
                    data.theme
                )
                group_name = "/".join(item_chain)
                self.main_form.display.repl_display_message(
                    "Session '{}/{}' was renamed to '{}/{}'!".format(
                       group_name, 
                       old_item_name,  
                       group_name, 
                       new_item_name 
                    ), 
                    message_type=data.MessageType.SUCCESS
                )
                # Refresh the session tree
                self.refresh_display()
            elif changed_item.type == self.ItemType.GROUP:
                self.reset_locks()
                # Item is a group
                old_group_name = item.name
                new_group_name = self.indexWidget(item.index()).text()
                item_chain = self.__get_node_chain(item)
                # Rename the group
                parent_group = self.settings_manipulator.get_group(item_chain)
                group = parent_group["groups"].pop(old_group_name)
                item.name = new_group_name
                item.setEditable(False)
                parent_group["groups"][new_group_name] = group
                self.settings_manipulator.rename_group(group, new_group_name)
                # Save the the new session list by saving the settings
                self.settings_manipulator.save_settings(
                    data.theme
                )
                # Display successful group deletion
                self.main_form.display.repl_display_message(
                    "Group '{}' was renamed to '{}'!".format(
                        old_group_name, 
                        new_group_name
                    ), 
                    message_type=data.MessageType.SUCCESS
                )
                # Refresh the session tree
                self.refresh_display()
        else:
            if changed_item.type == self.ItemType.SESSION:
                pass
            elif changed_item.type == self.ItemType.GROUP:
                pass
            elif changed_item.type == self.ItemType.EMPTY_SESSION:
                if len(changed_item.text()) < 3:
                    # Disconnect the signal
                    delegate = self.itemDelegate(changed_item.index())
                    delegate.closeEditor.disconnect()
                    # Remove the item from the tree
                    if changed_item.parent() is not None:
                        changed_item.parent().removeRow(changed_item.row())
                    else:
                        self.tree_model.removeRow(changed_item.row())
                    # Display message
                    message = "Session must have at least 3 characters in it's name!"
                    self.main_form.display.repl_display_message(
                        message, 
                        message_type=data.MessageType.WARNING
                    )
                else:
                    # Update item
                    changed_item.type = self.ItemType.SESSION
                    changed_item.setEditable(False)
                    # Adjust the name to the new one, by getting the QLineEdit at the model index
                    session_name = self.indexWidget(item.index()).text()
                    session_chain = self.__get_node_chain(item)
                    # Add session through the main window and check the result
                    if not self.main_form.sessions.add(session_name, session_chain):
                        ## Error occured, remove session item from tree widget
                        # Disconnect the signal
                        delegate = self.itemDelegate(changed_item.index())
                        delegate.closeEditor.disconnect()
                        # Remove the item from the tree
                        if changed_item.parent() is not None:
                            changed_item.parent().removeRow(changed_item.row())
                        else:
                            self.tree_model.removeRow(changed_item.row())
                    # Refresh the session tree
                    self.refresh_display()
            elif changed_item.type == self.ItemType.EMPTY_GROUP:
                # When the item's name is changed it refires the itemChanged signal,
                # so a check of one of the properties is necessary to not repeat the operation
                if item.name == "":
                    # Adjust the name to the new one, by getting the QLineEdit at the model index
                    group_name = self.indexWidget(item.index()).text()
                    group_chain = self.__get_node_chain(item)
                    # Set the item attributes
                    item.name = group_name
                    item.setEditable(False)
                    # Add group to sessions
                    self.settings_manipulator.add_group(group_name, group_chain)
                    # Save the sessions
                    self.settings_manipulator.save_settings(
                        data.theme
                    )
                # Update the type
                changed_item.type = self.ItemType.GROUP
    
    def __item_editing_closed(self, editor, hint):
        """
        Signal that fires when editing was canceled/ended in an empty session or empty group
        """
        item = self.__edit_item
        self.__edit_item = None
        # Check change
        if item.type == self.ItemType.EMPTY_GROUP:
            if len(item.text()) < 3:
                # Remove the item from the tree
                if item.parent() is not None:
                    item.parent().removeRow(item.row())
                else:
                    self.tree_model.removeRow(item.row())
        elif item.type == self.ItemType.EMPTY_SESSION:
            if len(item.text()) < 3:
                # Remove the item from the tree
                if item.parent() is not None:
                    item.parent().removeRow(item.row())
                else:
                    self.tree_model.removeRow(item.row())
        # Refresh all options
        self.refresh_display()
    
    def reset_locks(self):
        # Reset the all locks/flags
        self.edit_flag = False
    
    def refresh_display(self):
        """
        Refresh the displayed session while keeping the expanded groups
        """
        # Reset the all locks/flags
        self.reset_locks()
        # Update the main window menu
        self.main_form.sessions.update_menu()
    
    def __get_node_chain(self, node):
        parent = node.parent()
        chain = []
        while parent is not None:
            chain.append(parent.text())
            parent = parent.parent()
        chain.reverse()
        return chain
    
    def __get_current_group(self):
        if self.selectedIndexes() != []:
            selected_item = self.tree_model.itemFromIndex(self.selectedIndexes()[0])
            if selected_item.type == self.ItemType.SESSION:
                chain = self.__get_node_chain(selected_item)
                if len(chain) > 0:
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
        # Check for various flags
        if self.edit_flag == True:
            return
        empty_group_node = self.SessionItem("")
        empty_group_node._parent = self
        empty_group_node.name = ""
        empty_group_node.type = self.ItemType.EMPTY_GROUP
        empty_group_node.setEditable(True)
        empty_group_node.setIcon(self.node_icon_group)
        parent_group = self.__get_current_group()
        if parent_group is not None:
            empty_group_node.parent_group = parent_group.name
            parent_group.appendRow(empty_group_node)
        else:
            self.tree_model.appendRow(empty_group_node)
        self.scrollTo(empty_group_node.index())
        # Start editing the new empty group
        self.__start_editing_item(empty_group_node)
        # Add the session signal when editing is canceled
#        delegate = self.itemDelegate(empty_group_node.index())
#        delegate.closeEditor.connect(
#            functools.partial(self.__item_editing_closed, empty_group_node)
#        )
    
    def add_empty_session(self):
        # Check for various flags
        if self.edit_flag == True:
            return
        # Initialize the session
        empty_session_node = self.SessionItem("")
        empty_session_node._parent = self
        empty_session_node.name = ""
        empty_session_node.type = self.ItemType.EMPTY_SESSION
        empty_session_node.setEditable(True)
        empty_session_node.setIcon(self.node_icon_session)
        parent_group = self.__get_current_group()
        if parent_group is not None:
            parent_group.appendRow(empty_session_node)
            self.expand(parent_group.index())
        else:
            self.tree_model.appendRow(empty_session_node)
        self.scrollTo(empty_session_node.index())
        # Start editing the new empty session
        self.__start_editing_item(empty_session_node)
        # Add the session signal when editing is canceled
#        delegate = self.itemDelegate(empty_session_node.index())
#        delegate.closeEditor.connect(
#            functools.partial(self.__item_editing_closed, empty_session_node)
#        )
    
    def remove_item(self):
        # Check for various flags
        if self.edit_flag == True:
            return
        # Check if an item is selected
        if self.selectedIndexes() == []:
            return
        selected_item = self.tree_model.itemFromIndex(self.selectedIndexes()[0])
        # Check the selected item type
        if selected_item.type == self.ItemType.GROUP:
            remove_group = self.settings_manipulator.get_group(
                self.__get_node_chain(selected_item) + [selected_item.text()]
            )
            # Check if the group has subgroups
            group_name_with_chain = "{}/{}".format(
                "/".join(remove_group["chain"]), remove_group["name"]
            )
            if len(remove_group["sessions"]) > 0 or len(remove_group["groups"]) > 0:
                message =  "Cannot delete group\n'{}'\n".format(group_name_with_chain)
                message += "because it contains subgroups!"
                reply = OkDialog.error(message)
                return
            
            message =  "Are you sure you want to delete group:\n"
            message += "'{}' ?".format(group_name_with_chain)
            reply = YesNoDialog.warning(message)
            if reply == data.DialogResult.No.value:
                return
            # Delete the group
            result = self.settings_manipulator.remove_group(remove_group)
            # Display the deletion result
            if result == True:
                self.main_form.display.repl_display_message(
                    "Group '{}' was deleted!".format(group_name_with_chain), 
                    message_type=data.MessageType.SUCCESS
                )
                # Remove the item from the tree
                if selected_item.parent() is not None:
                    selected_item.parent().removeRow(selected_item.row())
                else:
                    self.tree_model.removeRow(selected_item.row())
                # Refresh the session tree
                self.refresh_display()
            else:
                message = "An error occured while deleting session "
                message += "group '{}'!".format(group_name_with_chain)
                self.main_form.display.repl_display_message(
                    message, 
                    message_type=data.MessageType.ERROR
                )
        elif selected_item.type == self.ItemType.SESSION:
            remove_session = self.settings_manipulator.get_session(
                selected_item.text(),
                self.__get_node_chain(selected_item)
            )
            session_name_with_chain = "{}/{}".format(
                "/".join(remove_session["chain"]), remove_session["name"]
            )
            message =  "Are you sure you want to delete session:\n"
            message += "'{}' ?".format(session_name_with_chain)
            reply = YesNoDialog.warning(message)
            if reply == data.DialogResult.No.value:
                return
            # Delete the session
            self.settings_manipulator.remove_session(remove_session)
            # Remove the item from the tree
            if selected_item.parent() is not None:
                selected_item.parent().removeRow(selected_item.row())
            else:
                self.tree_model.removeRow(selected_item.row())
            # Refresh the session tree
            self.refresh_display()
        elif selected_item.type == self.ItemType.EMPTY_SESSION:
            #Display successful group deletion
            self.main_form.display.repl_display_message(
                "Empty session was deleted!", 
                message_type=data.MessageType.SUCCESS
            )
            # Refresh the tree
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
        """
        Overwrite the selected session
        """
        # Check for various flags
        if self.edit_flag == True:
            return
        # Check if a session is selected
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
            selected_session = self.settings_manipulator.get_session(
                selected_item.text(),
                self.__get_node_chain(selected_item)
            )
            # Adding a session that is already stored will overwrite it
            self.main_form.sessions.add(
                selected_session["name"],
                selected_session["chain"]
            )
            # Refresh the tree
            self.refresh_display()
    
    def __start_editing_item(self, item):
        self.edit(item.index())
        self.__edit_item = item
    
    def edit_item(self):
        """
        Edit the selected session or group name
        """
        if self.edit_flag == True:
            return
        # Check if an item is selected
        if self.selectedIndexes() == []:
            return
        selected_item = self.tree_model.itemFromIndex(self.selectedIndexes()[0])
        
        # Check the selected item type
        if (selected_item.type == self.ItemType.GROUP or
            selected_item.type == self.ItemType.SESSION):
                selected_item.setEditable(True)
                selected_item.name = selected_item.text()
                self.__start_editing_item(selected_item)
        # Set the editing flag
        self.edit_flag = True
    
    def show_sessions(self):
        """
        Show the current session in a tree structure
        """
        if self.tree_model is not None:
            self.tree_model.itemChanged.disconnect()
        # Initialize the display
        self.tree_model = data.QStandardItemModel()
        self.tree_model.setHorizontalHeaderLabels(["SESSIONS"])
        self.header().hide()
#        self.clean_model()
        self.setModel(self.tree_model)
        self.setUniformRowHeights(True)
        # Connect the tree model signals
        self.tree_model.itemChanged.connect(self.__item_changed)
#        font = data.QFont(data.current_font_name, data.current_font_size, data.QFont.Bold)
        font = data.QFont(data.current_font_name, data.current_font_size)
        ## Create the Sessions menu
        # Group processing function
        def process_group(in_group, in_menu, create_menu=True):
            # Create the new group and attach it to the parent menu
            if create_menu:
                item_group_node = self.SessionItem(in_group["name"])
                item_group_node.setFont(font)
                item_group_node.my_parent = self
                item_group_node.name = in_group["chain"][-1] if len(in_group["chain"]) > 0 else ""
                item_group_node.type = self.ItemType.GROUP
                item_group_node.setEditable(False)
                item_group_node.setIcon(self.node_icon_group)
                in_menu.appendRow(item_group_node)
            else:
                item_group_node = in_menu
            # Add the groups
            for g,v in sorted(in_group["groups"].items(), key=lambda x: x[0].lower()):
                process_group(v, item_group_node)
            # Add the sessions
            for s,v in sorted(in_group["sessions"].items(), key=lambda x: x[0].lower()):
                item_session_node = self.SessionItem(s)
                item_session_node.my_parent = self
                item_session_node.name = s
                item_session_node.type = self.ItemType.SESSION
                item_session_node.setEditable(False)
                item_session_node.setIcon(self.node_icon_session)
                item_group_node.appendRow(item_session_node)
        # Process the groups
        main_session_group = self.settings_manipulator.stored_sessions["main"]
        process_group(main_session_group, self.tree_model, create_menu=False)
    
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
        # Remove session/group
        self.icon_manipulator.add_corner_button(
            "tango_icons/session-remove.png",
            "Remove the selected session/group",
            self.remove_item
        )



