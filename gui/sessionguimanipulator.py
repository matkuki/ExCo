"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import enum
from typing import Any, Callable

import components.actionfilter
import components.internals
import components.treefilter
import constants
import settings
import functions
import qt

from gui.dialogs import *
import gui.menu

"""
-------------------------------------------------
GUI Session manipulation object
-------------------------------------------------
"""


class ItemType(enum.Enum):
    SESSION = enum.auto()
    GROUP = enum.auto()
    EMPTY_SESSION = enum.auto()
    EMPTY_GROUP = enum.auto()


class SessionTree(qt.QTreeView):
    """
    The sessions tree, filtered through a proxy model.

    The manipulator's code works on the items of its own model, while the tree
    itself shows the filtered view of it, so every index that comes out of the
    view has to be taken back to the model first. Doing that here, once, keeps
    the mapping out of the handlers below - and keeps the model's own rows,
    which the sessions store is rebuilt from, out of the reach of the filter.

    setModel() therefore points the proxy at the model instead of handing it to
    the view: the view is permanently attached to the proxy, which is what
    makes an emptied and refilled tree come back still filtered.
    """

    def __init__(self, parent: qt.QWidget | None = None) -> None:
        super().__init__(parent)
        # A row that is still being typed in has to survive the filter,
        # otherwise "add session" would appear to do nothing while a filter is
        # active. Qt keeps an accepted row's parents visible as well, so the
        # group it is being added to stays reachable too.
        self.filter_proxy: components.treefilter.SubstringFilterProxy = (
            components.treefilter.SubstringFilterProxy(
                self,
                always_visible=lambda item: (
                    getattr(item, "type", None)
                    in (ItemType.EMPTY_SESSION, ItemType.EMPTY_GROUP)
                ),
            )
        )
        super().setModel(self.filter_proxy)

    def setModel(self, model: qt.QAbstractItemModel | None) -> None:
        """Filter *model* from now on (or nothing, when it is None)."""
        self.filter_proxy.setSourceModel(model)

    def set_filter_text(self, text: str) -> None:
        """Filter the shown rows; an empty text shows them all again."""
        self.filter_proxy.set_filter_text(text)

    def filter_text(self) -> str:
        return self.filter_proxy.filter_text()

    def source_index(self, view_index: qt.QModelIndex) -> qt.QModelIndex:
        """Translate an index of the view into an index of the model."""
        return self.filter_proxy.mapToSource(view_index)

    def view_index(self, source_index: qt.QModelIndex) -> qt.QModelIndex:
        """Translate an index of the model into an index of the view."""
        return self.filter_proxy.mapFromSource(source_index)


class SessionGuiManipulator(qt.QWidget):
    """
    GUI object for easier user editing of sessions

    The tab widget itself is a plain container holding a filter bar, a
    QTreeView and a footer bar, because the bars cannot live inside the tree: a
    QAbstractScrollArea keeps owning its own viewport even after a QLayout is
    installed on it, so a child laid out in that layout is centred over the
    scrollable area rather than reserved a strip at the bottom. The container's
    QVBoxLayout gives the tree the remaining height and pins the two bars
    flush above and below it.
    """

    class SessionItem(qt.QStandardItem):
        """QStandarItem with overridden methods"""

        # The session that the standard item will store
        my_parent = None
        name = None
        type = None

    # Class variables
    main_form: Any = None
    current_icon = None
    internals = None
    name = ""
    savable = constants.CanSave.NO
    last_clicked_session = None
    tree_model: Any = None
    tree_menu: Any = None
    edit_flag = False
    # Icons, all set in __init__ before the tree model or the footer needs
    # them, hence no None default here.
    node_icon_group: qt.QIcon
    node_icon_session: qt.QIcon
    icon_session_add: qt.QIcon
    icon_session_remove: qt.QIcon
    icon_session_overwrite: qt.QIcon
    icon_group_add: qt.QIcon
    icon_session_edit: qt.QIcon

    def __del__(self):
        try:
            # Disconnect signals
            self.tree.doubleClicked.disconnect()
            # Clean up main references
            self._parent = None
            self.main_form = None
            self.internals = None
            # Clean up self
            self.setParent(None)
            self.deleteLater()
        except:
            pass

    def __init__(self, parent, main_form):
        """Initialization"""
        # Initialize the superclass
        super().__init__(parent)
        # Initialize components
        # Nothing in this module calls into Internals any more, but the tab
        # still has to own one: the generic tab machinery reaches for
        # `tab.internals` without checking (thebox.get_id, mainwindow
        # update_icon, view.update_tab_widget, tabwidget.update_corner_widget,
        # thesquid.restyle_corner_button_icons). Only add_corner_button was
        # used from here, and that moved to the footer bar.
        self.internals = components.internals.Internals(parent=self, tab_widget=parent)
        # Store the reference to the parent TabWidget from the "forms" module
        self._parent = parent
        # Store the reference to the MainWindow form from the "forms" module
        self.main_form = main_form
        # Set default font
        self.setFont(settings.get_current_font())
        # Set the icon
        self.current_icon = functions.create_icon("tango_icons/sessions.png")
        # Store name of self
        self.name = "Session editing tree display"
        # Create the tree display that holds the sessions. It is a child of
        # this container so that the filter and footer bars can sit around it.
        self.tree: SessionTree = SessionTree(self)
        self.tree.setFont(settings.get_current_font())
        # Enable node expansion on double click
        self.tree.setExpandsOnDoubleClick(True)
        # Mouse presses are delivered to the viewport of a scroll area, while
        # focus events go to the tree itself, so both are watched. Bookkeeping
        # that used to live in mousePressEvent moves into this filter: the
        # container never sees either event.
        self.tree.installEventFilter(self)
        self.tree.viewport().installEventFilter(self)
        # Filter bar, above the tree
        self.filter_bar = components.treefilter.TreeFilterBar(self, "Filter sessions")
        self.filter_bar.filter_changed.connect(self.tree.set_filter_text)
        self.filter_bar.focus_in.connect(self.__filter_bar_focus_in)
        # Set the node icons
        self.node_icon_group = functions.create_icon("tango_icons/folder.png")
        self.node_icon_session = functions.create_icon("tango_icons/sessions.png")
        self.icon_session_add = functions.create_icon("tango_icons/session-add.png")
        self.icon_session_remove = functions.create_icon(
            "tango_icons/session-remove.png"
        )
        self.icon_session_overwrite = functions.create_icon(
            "tango_icons/session-overwrite.png"
        )
        self.icon_group_add = functions.create_icon("tango_icons/folder-add.png")
        self.icon_session_edit = functions.create_icon("tango_icons/session-edit.png")
        # Connect the signals
        self.tree.doubleClicked.connect(self.__item_double_clicked)
        self.tree.itemDelegate().closeEditor.connect(self.__item_editing_closed)
        # Right click context menu, carrying the same actions as the footer
        self.tree.setContextMenuPolicy(qt.Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.__show_context_menu)
        # Initialize the currently edited item reference
        self.__edit_item = None
        # Whether a deferred refresh is already queued (see __schedule_refresh)
        self._refresh_pending = False
        # Assemble the container: filter bar on top, then the tree, then the
        # footer bar underneath
        self.main_layout: qt.QVBoxLayout = qt.QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.filter_bar)
        self.main_layout.addWidget(self.tree)
        self._create_footer()
        # Set the theme
        self.set_theme(settings.get_theme())

    def eventFilter(self, object: qt.QObject, event: qt.QEvent) -> bool:  # type: ignore[override]
        """
        Track the interaction the container never sees itself.

        A press inside the tree reaches the viewport of the scroll area and a
        focus change reaches the view, so neither mousePressEvent nor FocusIn
        on the container would ever be called. Each event type is handled for
        exactly one of the two objects: a scroll area propagates viewport
        presses to itself as well, and accepting both would run the
        bookkeeping twice.
        """
        event_type = event.type()
        if (
            event_type == qt.QEvent.Type.MouseButtonPress
            and object is self.tree.viewport()
        ):
            # Set the focus on the tree
            self.tree.setFocus()
            # Set the last focused widget to the parent basic widget
            self.main_form.last_focused_widget = self._parent
            # Set Save/SaveAs buttons in the menubar
            self._parent._set_save_status()
            # Reset the click&drag context menu action
            components.actionfilter.ActionFilter.clear_action()
        elif event_type == qt.QEvent.Type.FocusIn and object is self.tree:
            # Check indication
            self.main_form.view.indication_check()
        return super().eventFilter(object, event)

    def __filter_bar_focus_in(self) -> None:
        """A click on the filter field is focus, so check the indication."""
        self.main_form.view.indication_check()

    def clean_model(self) -> None:
        # The view is permanently attached to the proxy, so it is the proxy
        # that has to let go of the model - and the model that has to be
        # released is the source one, not the proxy.
        model: Any = self.tree.filter_proxy.sourceModel()
        if model is not None:
            model.setParent(None)
            self.tree.setModel(None)

    def setFocus(
        self, reason: qt.Qt.FocusReason = qt.Qt.FocusReason.OtherFocusReason
    ) -> None:
        """Forward the focus request, and its reason, to the inner tree"""
        self.tree.setFocus(reason)

    def __item_double_clicked(self, model_index):
        """Callback connected to the treeview's 'clicked' signal"""
        session_item = self.tree_model.itemFromIndex(
            self.tree.source_index(model_index)
        )
        if session_item.type == ItemType.SESSION:
            # Open the session
            session_chain = self.__get_node_chain(session_item)
            session = settings.get_sessions().get_session(
                session_item.text(), session_chain
            )
            if session is None:
                self.__report_unresolved(session_chain, session_item.text())
                return
            self.main_form.sessions.restore(session)
        elif session_item.type == ItemType.GROUP:
            pass

    def __item_changed(self, item):
        """
        Callback connected to the displays QStandardItemModel 'itemChanged' signal
        """
        # Get the clicked item
        changed_item = item
        # Check for editing
        if self.edit_flag == True:
            if changed_item.type == ItemType.SESSION:
                self.reset_locks()
                # Item is a session
                old_item_name = item.name
                new_item_name = item.text()
                item_chain = self.__get_node_chain(item)
                # Rename
                group = settings.get_sessions().get_group(item_chain)
                if group is None or old_item_name not in group["sessions"]:
                    self.__report_unresolved(item_chain, old_item_name)
                    self.__schedule_refresh()
                    return
                session = group["sessions"].pop(old_item_name)
                item.name = new_item_name
                item.setEditable(False)
                session["name"] = new_item_name
                group["sessions"][new_item_name] = session
                # Save the the new session list by saving the settings
                settings.get_sessions().store_sessions()
                group_name = "/".join(item_chain)
                self.main_form.display.repl_display_message(
                    "Session '{}/{}' was renamed to '{}/{}'!".format(
                        group_name, old_item_name, group_name, new_item_name
                    ),
                    message_type=constants.MessageType.SUCCESS,
                )
                # Refresh the session tree
                self.__schedule_refresh()
            elif changed_item.type == ItemType.GROUP:
                self.reset_locks()
                # Update sessions
                settings.load()
                # Item is a group
                old_group_name = item.name
                new_group_name = item.text()
                item_chain = self.__get_node_chain(item)
                # Rename the group
                parent_group = settings.get_sessions().get_group(item_chain)
                if parent_group is None or old_group_name not in parent_group["groups"]:
                    self.__report_unresolved(item_chain, old_group_name)
                    self.__schedule_refresh()
                    return
                group = parent_group["groups"].pop(old_group_name)
                item.name = new_group_name
                item.setEditable(False)
                settings.get_sessions().rename_group(group, new_group_name)
                parent_group["groups"][new_group_name] = group
                # Save the the new session list by saving the settings
                settings.get_sessions().store_sessions()
                # Display successful group deletion
                self.main_form.display.repl_display_message(
                    "Group '{}' was renamed to '{}'!".format(
                        old_group_name, new_group_name
                    ),
                    message_type=constants.MessageType.SUCCESS,
                )
                # Refresh the session tree
                self.__schedule_refresh()
        else:
            if changed_item.type == ItemType.SESSION:
                pass
            elif changed_item.type == ItemType.GROUP:
                pass
            elif changed_item.type == ItemType.EMPTY_SESSION:
                if len(changed_item.text()) < 3:
                    # Clear the editing reference so __item_editing_closed becomes a no-op
                    self.__edit_item = None
                    # Remove the item from the tree
                    if changed_item.parent() is not None:
                        changed_item.parent().removeRow(changed_item.row())
                    else:
                        self.tree_model.removeRow(changed_item.row())
                    # Display message
                    message = "Session must have at least 3 characters in it's name!"
                    self.main_form.display.repl_display_message(
                        message, message_type=constants.MessageType.WARNING
                    )
                else:
                    # Update item
                    changed_item.type = ItemType.SESSION
                    changed_item.setEditable(False)
                    # Adjust the name to the new one, by getting the standard item text
                    session_name = item.text()
                    session_chain = self.__get_node_chain(item)
                    # Add session through the main window and check the result
                    if not self.main_form.sessions.add(session_name, session_chain):
                        ## Error occured, remove session item from tree widget
                        # Clear the editing reference so __item_editing_closed becomes a no-op
                        self.__edit_item = None
                        # Remove the item from the tree
                        if changed_item.parent() is not None:
                            changed_item.parent().removeRow(changed_item.row())
                        else:
                            self.tree_model.removeRow(changed_item.row())
                    # Refresh the session tree
                    self.__schedule_refresh()
            elif changed_item.type == ItemType.EMPTY_GROUP:
                if len(changed_item.text()) < 3:
                    # Clear the editing reference so __item_editing_closed becomes a no-op
                    self.__edit_item = None
                    # Remove the item from the tree
                    if changed_item.parent() is not None:
                        changed_item.parent().removeRow(changed_item.row())
                    else:
                        self.tree_model.removeRow(changed_item.row())
                    # Display message
                    message = "Group must have at least 3 characters in it's name!"
                    self.main_form.display.repl_display_message(
                        message, message_type=constants.MessageType.WARNING
                    )
                # When the item's name is changed it refires the itemChanged signal,
                # so a check of one of the properties is necessary to not repeat the operation
                elif item.name == "":
                    # Adjust the name to the new one, by getting the standard item text
                    group_name = item.text()
                    group_chain = self.__get_node_chain(item)
                    # Set the item attributes
                    item.name = group_name
                    item.setEditable(False)
                    # Add group to sessions
                    settings.get_sessions().add_group(group_name, group_chain)
                    # Save the sessions
                    settings.get_sessions().store_sessions()
                    # Refresh the session tree
                    self.__schedule_refresh()
                # Update the type
                changed_item.type = ItemType.GROUP

    def __item_editing_closed(self, editor, hint):
        """
        Signal that fires when editing was canceled/ended in an empty session or empty group
        """
        item = self.__edit_item
        self.__edit_item = None
        # Check if the item was already handled/removed by __item_changed
        if item is None:
            return
        # Check change
        if item.type == ItemType.EMPTY_GROUP:
            if len(item.text()) < 3:
                # Remove the item from the tree
                if item.parent() is not None:
                    item.parent().removeRow(item.row())
                else:
                    self.tree_model.removeRow(item.row())
        elif item.type == ItemType.EMPTY_SESSION:
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

    def __schedule_refresh(self) -> None:
        """
        Rebuild the tree once the item change that asked for it has unwound.

        This handler runs from inside QStandardItem.setText(), so removing the
        rows here destroys the very item Qt is still writing into - a
        use-after-free that shows up as a hard access violation rather than a
        Python exception. Queueing the rebuild for the event loop lets setText
        finish first, and the store write that led here has already happened,
        so nothing observable is lost. Repeated requests collapse into the one
        rebuild that is already pending.
        """
        if self._refresh_pending:
            return
        self._refresh_pending = True
        qt.QTimer.singleShot(0, self._flush_refresh)

    def _flush_refresh(self) -> None:
        """Run the rebuild that __schedule_refresh deferred"""
        self._refresh_pending = False
        self.refresh_display()

    def refresh_display(self):
        """
        Refresh the displayed session while keeping the expanded groups
        """
        # Reset the all locks/flags
        self.reset_locks()
        # Remember which groups are currently expanded
        expanded_chains = self.__expanded_group_chains()
        # Rebuild the tree from the stored sessions
        if self.tree_model is not None:
            self.__populate_model()
        # Re-expand the groups that were expanded before the refresh
        for chain in expanded_chains:
            node = self.__find_group_node(chain)
            if node is not None:
                # A group that the filter is hiding has no index in the view,
                # and expand() ignores those, which is what is wanted here.
                self.tree.expand(self.tree.view_index(node.index()))
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

    def __report_unresolved(
        self, item_chain: list[str], item_name: str | None = None
    ) -> None:
        """
        Report a session or group that could not be resolved in the store
        """
        target = list(item_chain)
        if item_name is not None:
            target.append(item_name)
        message = "Could not find '{}'!".format("/".join(target))
        self.main_form.display.repl_display_message(
            message, message_type=constants.MessageType.ERROR
        )

    def __get_current_group(self):
        if self.tree.selectedIndexes() != []:
            selected_item = self.tree_model.itemFromIndex(
                self.tree.source_index(self.tree.selectedIndexes()[0])
            )
            if selected_item.type == ItemType.SESSION:
                chain = self.__get_node_chain(selected_item)
                if len(chain) > 0:
                    return selected_item.parent()
                else:
                    return None
            elif (
                selected_item.type == ItemType.GROUP
                or selected_item.type == ItemType.EMPTY_GROUP
            ):
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
        empty_group_node.type = ItemType.EMPTY_GROUP
        empty_group_node.setEditable(True)
        empty_group_node.setIcon(self.node_icon_group)
        parent_group = self.__get_current_group()
        if parent_group is not None:
            empty_group_node.parent_group = parent_group.name
            parent_group.appendRow(empty_group_node)
        else:
            self.tree_model.appendRow(empty_group_node)
        self.tree.scrollTo(self.tree.view_index(empty_group_node.index()))
        # Start editing the new empty group
        self.__start_editing_item(empty_group_node)

    def add_empty_session(self):
        # Check for various flags
        if self.edit_flag == True:
            return
        # Initialize the session
        empty_session_node = self.SessionItem("")
        empty_session_node._parent = self
        empty_session_node.name = ""
        empty_session_node.type = ItemType.EMPTY_SESSION
        empty_session_node.setEditable(True)
        empty_session_node.setIcon(self.node_icon_session)
        parent_group = self.__get_current_group()
        if parent_group is not None:
            parent_group.appendRow(empty_session_node)
            self.tree.expand(self.tree.view_index(parent_group.index()))
        else:
            self.tree_model.appendRow(empty_session_node)
        self.tree.scrollTo(self.tree.view_index(empty_session_node.index()))
        # Start editing the new empty session
        self.__start_editing_item(empty_session_node)

    def remove_item(self):
        # Check for various flags
        if self.edit_flag == True:
            return
        # Check if an item is selected
        if self.tree.selectedIndexes() == []:
            return
        selected_item = self.tree_model.itemFromIndex(
            self.tree.source_index(self.tree.selectedIndexes()[0])
        )
        # Check the selected item type
        if selected_item.type == ItemType.GROUP:
            group_chain = self.__get_node_chain(selected_item) + [selected_item.text()]
            remove_group = settings.get_sessions().get_group(group_chain)
            if remove_group is None:
                self.__report_unresolved(group_chain)
                return
            # Check if the group has subgroups
            group_name_with_chain = "{}/{}".format(
                "/".join(remove_group["chain"]), remove_group["name"]
            )
            if len(remove_group["sessions"]) > 0 or len(remove_group["groups"]) > 0:
                message = "Cannot delete group\n'{}'\n".format(group_name_with_chain)
                message += "because it contains subgroups!"
                reply = OkDialog.error(message)
                return

            message = "Are you sure you want to delete group:\n"
            message += "'{}' ?".format(group_name_with_chain)
            reply = YesNoDialog.warning(message)
            if reply == constants.DialogResult.No.value:
                return
            # Delete the group
            result = settings.get_sessions().remove_group(remove_group)
            # Display the deletion result
            if result == True:
                self.main_form.display.repl_display_message(
                    "Group '{}' was deleted!".format(group_name_with_chain),
                    message_type=constants.MessageType.SUCCESS,
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
                    message, message_type=constants.MessageType.ERROR
                )
        elif selected_item.type == ItemType.SESSION:
            session_chain = self.__get_node_chain(selected_item)
            remove_session = settings.get_sessions().get_session(
                selected_item.text(), session_chain
            )
            if remove_session is None:
                self.__report_unresolved(session_chain, selected_item.text())
                return
            session_name_with_chain = "{}/{}".format(
                "/".join(remove_session["chain"]), remove_session["name"]
            )
            message = "Are you sure you want to delete session:\n"
            message += "'{}' ?".format(session_name_with_chain)
            reply = YesNoDialog.warning(message)
            if reply == constants.DialogResult.No.value:
                return
            # Delete the session
            settings.get_sessions().remove_session(remove_session)
            # Remove the item from the tree
            if selected_item.parent() is not None:
                selected_item.parent().removeRow(selected_item.row())
            else:
                self.tree_model.removeRow(selected_item.row())
            # Refresh the session tree
            self.refresh_display()
        elif selected_item.type == ItemType.EMPTY_SESSION:
            # Display successful group deletion
            self.main_form.display.repl_display_message(
                "Empty session was deleted!", message_type=constants.MessageType.SUCCESS
            )
            # Refresh the tree
            self.refresh_display()
        elif selected_item.type == ItemType.EMPTY_GROUP:
            # Display successful group deletion
            self.main_form.display.repl_display_message(
                "Empty group was deleted!", message_type=constants.MessageType.SUCCESS
            )
            # Refresh the tree
            self.refresh_display()

    def overwrite_session(self):
        """
        Overwrite the selected session
        """
        # Check for various flags
        if self.edit_flag == True:
            return
        # Check if a session is selected
        if self.tree.selectedIndexes() == []:
            return
        selected_item = self.tree_model.itemFromIndex(
            self.tree.source_index(self.tree.selectedIndexes()[0])
        )
        # Check the selected item type
        if selected_item.type == ItemType.GROUP:
            # Show message that groups cannot be overwritten
            self.main_form.display.repl_display_message(
                "Groups cannot be overwritten!",
                message_type=constants.MessageType.ERROR,
            )
            return
        elif selected_item.type == ItemType.SESSION:
            session_chain = self.__get_node_chain(selected_item)
            selected_session = settings.get_sessions().get_session(
                selected_item.text(), session_chain
            )
            if selected_session is None:
                self.__report_unresolved(session_chain, selected_item.text())
                return
            # Adding a session that is already stored will overwrite it
            self.main_form.sessions.add(
                selected_session["name"], selected_session["chain"]
            )
            # Refresh the tree
            self.refresh_display()

    def __start_editing_item(self, item):
        self.tree.edit(self.tree.view_index(item.index()))
        self.__edit_item = item

    def edit_item(self) -> None:
        """
        Edit the selected session or group name
        """
        if self.edit_flag == True:
            return
        # Check if an item is selected
        if self.tree.selectedIndexes() == []:
            return
        selected_item = self.tree_model.itemFromIndex(
            self.tree.source_index(self.tree.selectedIndexes()[0])
        )

        # Check the selected item type
        if (
            selected_item.type == ItemType.GROUP
            or selected_item.type == ItemType.SESSION
        ):
            selected_item.setEditable(True)
            selected_item.name = selected_item.text()
            self.__start_editing_item(selected_item)
            # Lock the footer buttons for the duration of the edit. This has to
            # stay inside the branch above: a row that no editor is opened for
            # would otherwise never get a closeEditor to clear the lock.
            self.edit_flag = True

    def show_sessions(self):
        """
        Show the current session in a tree structure
        """
        if self.tree_model is not None:
            self.tree_model.itemChanged.disconnect()
        # Initialize the display
        self.tree_model = qt.QStandardItemModel()
        self.tree_model.setHorizontalHeaderLabels(["SESSIONS"])
        self.tree.header().hide()
        #        self.clean_model()
        self.tree.setModel(self.tree_model)
        self.tree.setUniformRowHeights(True)
        # Connect the tree model signals
        self.tree_model.itemChanged.connect(self.__item_changed)
        # Populate the model from the stored sessions
        self.__populate_model()

    def __populate_model(self):
        """
        (Re)build the tree contents from the stored sessions
        """
        # Clear the existing rows (if any)
        self.tree_model.removeRows(0, self.tree_model.rowCount())
        # font = qt.QFont(settings.get("current_font_name"), settings.get("current_font_size"), qt.QFont.Bold)
        font = qt.QFont(
            settings.get("current_font_name"), settings.get("current_font_size")
        )

        ## Create the Sessions menu
        # Group processing function
        def process_group(in_group, in_menu, create_menu=True):
            # Create the new group and attach it to the parent menu
            if create_menu:
                item_group_node = self.SessionItem(in_group["name"])
                item_group_node.setFont(font)
                item_group_node.my_parent = self
                item_group_node.name = (
                    in_group["chain"][-1] if len(in_group["chain"]) > 0 else ""
                )
                item_group_node.type = ItemType.GROUP
                item_group_node.setEditable(False)
                item_group_node.setIcon(self.node_icon_group)
                in_menu.appendRow(item_group_node)
            else:
                item_group_node = in_menu
            # Add the groups
            for g, v in sorted(in_group["groups"].items(), key=lambda x: x[0].lower()):
                process_group(v, item_group_node)
            # Add the sessions
            for s, v in sorted(
                in_group["sessions"].items(), key=lambda x: x[0].lower()
            ):
                item_session_node = self.SessionItem(s)
                item_session_node.my_parent = self
                item_session_node.name = s
                item_session_node.type = ItemType.SESSION
                item_session_node.setEditable(False)
                item_session_node.setIcon(self.node_icon_session)
                item_group_node.appendRow(item_session_node)

        # Process the groups
        main_session_group = settings.get("stored_sessions")["main"]
        process_group(main_session_group, self.tree_model, create_menu=False)

    def __expanded_group_chains(self):
        """
        Return the list of group name-chains of the currently expanded groups
        """
        chains = []
        if self.tree_model is not None:
            self.__collect_expanded_chains(
                self.tree_model.invisibleRootItem(), [], chains
            )
        return chains

    def __collect_expanded_chains(self, node, prefix, chains):
        for i in range(node.rowCount()):
            child = node.child(i)
            if child is None:
                continue
            if child.type == ItemType.GROUP:
                chain = prefix + [child.text()]
                if self.tree.isExpanded(self.tree.view_index(child.index())):
                    chains.append(chain)
                self.__collect_expanded_chains(child, chain, chains)

    def __find_group_node(self, chain):
        """
        Find the group item matching the given group name-chain, or None
        """
        if self.tree_model is None:
            return None
        node = self.tree_model.invisibleRootItem()
        for name in chain:
            found = None
            for i in range(node.rowCount()):
                child = node.child(i)
                if (
                    child is not None
                    and child.type == ItemType.GROUP
                    and child.text() == name
                ):
                    found = child
                    break
            if found is None:
                return None
            node = found
        return node

    def _create_footer(self) -> None:
        """
        Create the footer bar that carries the session actions.

        Laid out and styled to match the text differ's footer exactly: the
        same 28px height, the same margins and spacing, the same flat
        action buttons and the same thin separators between button groups.
        """
        self.footer: qt.QWidget = qt.QWidget(self)
        self.footer.setObjectName("session_editor_footer")
        self.footer.setFixedHeight(28)
        self.footer_layout: qt.QHBoxLayout = qt.QHBoxLayout()
        self.footer_layout.setContentsMargins(8, 2, 8, 2)
        self.footer_layout.setSpacing(8)
        self.footer.setLayout(self.footer_layout)
        # The differ keeps its badges and stats on the left, so the actions
        # are pushed to the right here with a stretch
        self.footer_layout.addStretch()
        self._footer_buttons: list[qt.QPushButton] = []
        # Edit session
        self._add_footer_button(
            self.icon_session_edit, "Edit the selected item", self.edit_item
        )
        # Overwrite session
        self._add_footer_button(
            self.icon_session_overwrite,
            "Overwrite the selected session",
            self.overwrite_session,
        )
        self._make_vline()
        # Add group
        self._add_footer_button(
            self.icon_group_add, "Add a new group", self.add_empty_group
        )
        # Add session
        self._add_footer_button(
            self.icon_session_add, "Add a new session", self.add_empty_session
        )
        self._make_vline()
        # Remove session/group
        self._add_footer_button(
            self.icon_session_remove,
            "Remove the selected session/group",
            self.remove_item,
        )
        self.main_layout.addWidget(self.footer)

    def _add_footer_button(
        self, icon: qt.QIcon, tooltip: str, function: Callable[[], Any]
    ) -> None:
        """Add a flat, icon-only action button to the footer bar."""
        button = qt.QPushButton(self.footer)
        button.setObjectName("session_editor_action_button")
        button.setIcon(icon)
        button.setToolTip(tooltip)
        button.setFlat(True)
        button.clicked.connect(function)
        self.footer_layout.addWidget(button)
        self._footer_buttons.append(button)

    def _make_vline(self) -> None:
        """Add a thin vertical separator to the footer bar."""
        line = qt.QWidget(self.footer)
        line.setObjectName("session_editor_vline")
        line.setFixedWidth(1)
        self.footer_layout.addWidget(line)

    def _apply_footer_theme(self, theme: dict[str, Any]) -> None:
        """
        Style the footer bar with the colours of the active theme.

        The differ derives its three badges from the diff accent colours;
        the sessions have no equivalent, so only the neutral bar, the button
        border and the hover state are themed here.
        """
        background = theme["linemargin"]["background"]
        border = theme["scrollbar"]["handle"]
        button_border = theme["indication"]["passiveborder"]
        hover = theme["indication"]["hover"]
        self.footer.setStyleSheet(
            """
#session_editor_footer {{
    background-color: {};
    border-top: 1px solid {};
}}
QPushButton#session_editor_action_button {{
    background: transparent;
    border: none;
    padding: 1px 3px;
}}
QPushButton#session_editor_action_button {{
    border: 1px solid {};
}}
QPushButton#session_editor_action_button:hover {{
    background: {};
}}
QWidget#session_editor_vline {{
    background-color: {};
    min-width: 1px;
    max-width: 1px;
}}
""".format(
                background,
                border,
                button_border,
                hover,
                border,
            )
        )

    def set_theme(self, theme: dict[str, Any]) -> None:
        self.filter_bar.apply_theme(theme)
        self._apply_footer_theme(theme)

    def _context_action(
        self, menu: qt.QMenu, text: str, icon: qt.QIcon, function: Callable[[], Any]
    ) -> None:
        """Add an action to the context menu."""
        action = qt.QAction(text, menu)
        action.setIcon(icon)
        action.triggered.connect(function)
        menu.addAction(action)

    def _build_context_menu(self, index: qt.QModelIndex | None) -> qt.QMenu:
        """
        Build the context menu for a right click at *index*.

        This mirrors the footer bar, restricted to what makes sense where
        the click landed: the background of the tree offers the two creation
        actions, an item offers the actions that apply to it, and a group
        also offers the creation actions, which fill that group. Overwrite is
        meaningless for a group, so it is left out there instead of failing
        once it is triggered. A half-created row (an empty group or session
        that is being typed) can only sensibly be dropped.
        """
        menu = gui.menu.Menu(self)
        item = None
        if index is not None and index.isValid() and self.tree_model is not None:
            item = self.tree_model.itemFromIndex(self.tree.source_index(index))
        # The background of the tree
        if item is None:
            self._context_action(
                menu, "Add group", self.icon_group_add, self.add_empty_group
            )
            self._context_action(
                menu, "Add session", self.icon_session_add, self.add_empty_session
            )
            return menu
        # A row that is still being typed in
        if item.type in (ItemType.EMPTY_SESSION, ItemType.EMPTY_GROUP):
            self._context_action(
                menu, "Remove", self.icon_session_remove, self.remove_item
            )
            return menu
        # A stored group or session
        self._context_action(menu, "Edit name", self.icon_session_edit, self.edit_item)
        if item.type == ItemType.SESSION:
            self._context_action(
                menu, "Overwrite", self.icon_session_overwrite, self.overwrite_session
            )
        else:
            # A group can hold more, and the right click has already selected
            # it, so these land inside the group that was clicked.
            menu.addSeparator()
            self._context_action(
                menu, "Add group", self.icon_group_add, self.add_empty_group
            )
            self._context_action(
                menu, "Add session", self.icon_session_add, self.add_empty_session
            )
        menu.addSeparator()
        self._context_action(menu, "Remove", self.icon_session_remove, self.remove_item)
        return menu

    def _select_for_context_menu(self, index: qt.QModelIndex) -> None:
        """
        Move the selection onto the item that was right clicked.

        The context menu triggers the very same handlers the footer bar
        does, and those act on the current selection, so without this a
        right click would edit or remove whatever happened to be selected
        before. A click on the background clears the selection instead, so
        that the two creation actions add at the top level rather than
        inside a group that merely was selected.
        """
        if index.isValid():
            selection_model: Any = self.tree.selectionModel()
            selection_model.select(
                index,
                qt.QItemSelectionModel.SelectionFlag.ClearAndSelect
                | qt.QItemSelectionModel.SelectionFlag.Rows,
            )
            self.tree.setCurrentIndex(index)
        else:
            self.tree.clearSelection()
            self.tree.setCurrentIndex(qt.QModelIndex())

    def __show_context_menu(self, position: qt.QPoint) -> None:
        """Show the context menu for a right click at *position*."""
        index = self.tree.indexAt(position)
        self._select_for_context_menu(index)
        if self.tree_menu is not None:
            self.tree_menu.setParent(None)
            self.tree_menu = None
        self.tree_menu = self._build_context_menu(index)
        viewport: Any = self.tree.viewport()
        self.tree_menu.popup(viewport.mapToGlobal(position))
