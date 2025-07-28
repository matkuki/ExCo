"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import functools
import os
import traceback

import components.actionfilter
import components.thesquid
import constants
import data
import settings
import functions
import qt

from .custombuttons import *
from .customeditor import *
from .dialogs import *
from .externalprogram import *
from .hexview import *
from .menu import *
from .plaineditor import *
from .templates import *
from .terminal import *
from .treedisplays import *

"""
-----------------------------
Subclassed QTabWidget that can hold all custom editor and other widgets
-----------------------------
"""


class TabWidget(qt.QTabWidget):
    """
    Basic widget used for holding QScintilla/QTextEdit objects
    """

    class CustomTabBar(qt.QTabBar):
        """
        Custom tab bar used to capture tab clicks, ...
        """

        # Reference to the parent widget
        _parent = None
        # Reference to the main form
        main_form = None
        # Reference to the tab menu
        tab_menu = None

        def __init__(self, parent):
            """
            Initialize the tab bar object
            """
            # Initialize superclass
            super().__init__(parent)
            # Store the parent reference
            self._parent = parent
            # Store the main form reference
            self.main_form = self._parent.main_form
            # Set style
            self.set_style()
            # Set default font
            self.setFont(settings.get_current_font())
            # Don't draw the background, only the tabs
            self.setDrawBase(False)

        def set_style(self):
            close_image = functions.get_resource_file(settings.get_theme()["close-image"])
            close_hover_image = functions.get_resource_file(
                settings.get_theme()["close-hover-image"]
            )
            right_arrow_image = functions.get_resource_file(
                settings.get_theme()["right-arrow-image"]
            )
            right_arrow_hover_image = functions.get_resource_file(
                settings.get_theme()["right-arrow-hover-image"]
            )
            left_arrow_image = functions.get_resource_file(
                settings.get_theme()["left-arrow-image"]
            )
            left_arrow_hover_image = functions.get_resource_file(
                settings.get_theme()["left-arrow-hover-image"]
            )
            style = """
QTabBar::close-button {{
    image: url({})
}}
QTabBar::close-button:hover {{
    image: url({})
}}

QTabBar QToolButton {{
    margin-bottom: 1px;
    margin-left: 1px;
}}

QTabBar QToolButton::right-arrow {{
    image: url({});
}}
QTabBar QToolButton::right-arrow:hover {{
    image: url({});
}}

QTabBar QToolButton::left-arrow {{
    image: url({});
}}
QTabBar QToolButton::left-arrow:hover {{
    image: url({});
}}

QTabBar::tab {{
    background: {};
    border: 1px solid {};
    border-bottom-color: {};
    padding-top: 2px;
    padding-bottom: 2px;
    padding-left: 4px;
    padding-right: 4px;
    color: {};
}}
QTabBar::tab:hover {{
    background: {};
    border-bottom-color: {};
}}
QTabBar::tab:selected {{
    background: {};
    border: 1px solid {};
    border-bottom-color: {};
}}
            """.format(
                close_image,
                close_hover_image,
                right_arrow_image,
                right_arrow_hover_image,
                left_arrow_image,
                left_arrow_hover_image,
                settings.get_theme()["indication"]["passivebackground"],
                settings.get_theme()["indication"]["passiveborder"],
                settings.get_theme()["indication"]["passivebackground"],
                settings.get_theme()["fonts"]["default"]["color"],
                settings.get_theme()["indication"]["hover"],
                settings.get_theme()["indication"]["hover"],
                settings.get_theme()["indication"]["activebackground"],
                settings.get_theme()["indication"]["activeborder"],
                settings.get_theme()["indication"]["passivebackground"],
            )
            self.setStyleSheet(style)

        def mousePressEvent(self, event):
            # Execute the superclass event method
            super().mousePressEvent(event)
            event_button = event.button()
            key_modifiers = qt.QApplication.keyboardModifiers()

            self._parent.store_drag_data()

        def contextMenuEvent(self, event):
            # Clean up the old menu
            if self.tab_menu != None:
                self.tab_menu.setParent(None)
                self.tab_menu = None
            # Create the popup tab context menu
            menu = self._parent.TabMenu(
                self,
                self.main_form,
                self._parent,
                self._parent.widget(self.tabAt(event.pos())),
                event.pos(),
            )
            self.tab_menu = menu
            # Show the tab context menu
            cursor = qt.QCursor.pos()
            menu.popup(cursor)
            event.accept()

    class TabMenu(Menu):
        """
        Custom menu that appears when right clicking a tab
        """

        def __init__(self, parent, main_form, tab_widget, widget, cursor_position):
            # Nested function for updating the current working directory
            def update_cwd():
                # Get the document path
                path = os.path.dirname(widget.save_name)
                # Check if the path is not an empty string
                if path == "":
                    message = "Document path is not valid!"
                    main_form.display.repl_display_message(
                        message, message_type=constants.MessageType.WARNING
                    )
                    return
                main_form.set_cwd(path)

            # Initialize the superclass
            super().__init__(parent)
            # Change the basic widget name to lowercase
            tab_widget_name = tab_widget.name.lower()
            # Clear REPL MESSAGES tab action
            clear_repl_action = qt.QAction("Clear messages", self)
            clear_repl_action.setIcon(
                functions.create_icon("tango_icons/edit-clear.png")
            )
            clear_repl_action.triggered.connect(main_form.display.repl_clear_tab)

            if hasattr(widget, "save_name") == True:
                update_cwd_action = qt.QAction("Update CWD", self)
                update_cwd_action.setIcon(
                    functions.create_icon("tango_icons/update-cwd.png")
                )
                update_cwd_action.triggered.connect(update_cwd)
                self.addAction(update_cwd_action)
                self.addSeparator()
            # Add the 'copy file name to clipboard' action
            clipboard_copy_action = qt.QAction("Copy tab name to clipboard", self)

            def clipboard_copy():
                cb = data.application.clipboard()
                cb.clear(mode=cb.Mode.Clipboard)
                cb.setText(widget.name, mode=cb.Mode.Clipboard)

            clipboard_copy_action.setIcon(
                functions.create_icon("tango_icons/edit-copy.png")
            )
            clipboard_copy_action.triggered.connect(clipboard_copy)
            self.addAction(clipboard_copy_action)
            # Copy path
            if self.__check_for_editor(tab_widget):
                clipboard_copy_path_action = qt.QAction(
                    "Copy document path to clipboard", self
                )

                def clipboard_path_copy():
                    cb = data.application.clipboard()
                    cb.clear(mode=cb.Mode.Clipboard)
                    cb.setText(widget.save_name, mode=cb.Mode.Clipboard)

                clipboard_copy_path_action.setIcon(
                    functions.create_icon("tango_icons/edit-copy.png")
                )
                clipboard_copy_path_action.triggered.connect(clipboard_path_copy)
                self.addAction(clipboard_copy_path_action)
            # Text diff to focused editor
            if self.__check_for_editor(tab_widget):
                # Check if a editor is focused
                indicated_widget = main_form.get_tab_by_indication()
                if (
                    indicated_widget is not None
                    and isinstance(indicated_widget, CustomEditor)
                    and indicated_widget is not widget
                ):
                    # Text difference actions
                    diff_action = self.__create_diff_action(
                        "Text diff to focused window",
                        main_form,
                        indicated_widget,
                        widget,
                    )
                    self.addAction(diff_action)
            # Open path in explorer and hex-view
            if self.__check_for_editor(tab_widget):
                # Open in Hex-View
                def open_hex():
                    file_path = widget.save_name
                    main_form.open_file_hex(file_path)

                action_open_hex = qt.QAction("Open with Hex-View", self)
                action_open_hex.triggered.connect(open_hex)
                icon = functions.create_icon("various/node_template.png")
                action_open_hex.setIcon(icon)
                self.addAction(action_open_hex)

                open_in_explorer_action = qt.QAction("Open document in explorer", self)

                def open_in_explorer():
                    path = widget.save_name
                    try:
                        result = functions.open_item_in_explorer(path)
                    except:
                        result = False
                    if result == False:
                        main_form.display.repl_display_error(
                            "Error opening path in explorer: '{}'".format(path)
                        )

                open_in_explorer_action.setIcon(
                    functions.create_icon("tango_icons/document-open.png")
                )
                open_in_explorer_action.triggered.connect(open_in_explorer)
                self.addAction(open_in_explorer_action)

            # Closing
            self.addSeparator()
            close_other_action = qt.QAction("Close all other tabs in this window", self)
            close_other_action.setIcon(
                functions.create_icon("tango_icons/close-all-tabs.png")
            )
            close_other_action.triggered.connect(
                functools.partial(main_form.close_window_tabs, tab_widget, widget)
            )
            self.addAction(close_other_action)

        def __check_for_editor(self, tab_widget):
            """
            Function for checking is the basic widgets current tab is an editor
            """
            current_tab = tab_widget.currentWidget()
            if isinstance(current_tab, CustomEditor) == True:
                return True
            else:
                return False

        def __create_diff_action(
            self, action_name, main_form, compare_tab_1, compare_tab_2
        ):
            def difference_function(main_form, compare_tab_1, compare_tab_2):
                # Check for text documents in both tabs
                if (
                    isinstance(compare_tab_1, CustomEditor) == False
                    and isinstance(compare_tab_1, PlainEditor) == False
                ):
                    main_form.display.repl_display_message(
                        "First tab is not a text document!",
                        message_type=constants.MessageType.ERROR,
                    )
                    return
                elif (
                    isinstance(compare_tab_2, CustomEditor) == False
                    and isinstance(compare_tab_2, PlainEditor) == False
                ):
                    main_form.display.repl_display_message(
                        "Second tab is not a text document!",
                        message_type=constants.MessageType.ERROR,
                    )
                    return
                # Initialize the compare parameters
                text_1 = compare_tab_1.text()
                text_1_name = compare_tab_1.name
                text_2 = compare_tab_2.text()
                text_2_name = compare_tab_2.name
                # Display the text difference
                main_form.display.show_text_difference(
                    text_1, text_2, text_1_name, text_2_name
                )

            diff_action = qt.QAction(action_name, self)
            diff_action.setIcon(
                functions.create_icon("tango_icons/compare-text-main.png")
            )
            function = functools.partial(
                difference_function, main_form, compare_tab_1, compare_tab_2
            )
            diff_action.triggered.connect(function)
            return diff_action

    # Class variables
    # Name of the basic widget
    name = ""
    # Reference to the last file that was drag&dropped onto the main  form
    drag_dropped_file = None
    # Drag&Dropped text data
    drag_text = None
    # The source widgets of the drag&drop event
    drag_source = None
    # QMainWindow
    _parent = None
    main_form = None
    # Custom tab bar
    custom_tab_bar = None
    # Default font for textboxes
    default_editor_font = qt.QFont(settings.get("current_font_name"), settings.get("current_font_size"))
    # Default font and icon size for the tab bar
    default_tab_font = None
    default_icon_size = None

    # Tab-bar stuff
    move_range = None
    drag_lock = None
    drag_event_data = None

    def __init__(self, parent, main_form, box):
        """Initialization"""
        # Initialize superclass, from which the current class is inherited,
        # THIS MUST BE DONE SO THAT THE SUPERCLASS EXECUTES ITS __init__ !!!!!!
        super().__init__(parent)
        self.setProperty("indicated", False)
        # Set various events and attributes
        # Save parent as a reference
        self._parent = parent
        self.main_form = main_form
        self.box = box
        # Set default font
        self.setFont(settings.get_current_font())
        # Initialize the custom tab bar
        self.custom_tab_bar = self.CustomTabBar(self)
        self.setTabBar(self.custom_tab_bar)
        # Enable drag&drop events
        self.setAcceptDrops(True)
        # Add close buttons to tabs
        self.setTabsClosable(True)
        # Set tabs as movable, so that you can move tabs with the mouse
        self.setMovable(True)
        # Add signal for coling a tab to the EVT_tabCloseRequested function
        self.tabCloseRequested.connect(self._signal_editor_tabclose)
        # Connect signal that fires when the tab index changes
        self.currentChanged.connect(self.__signal_editor_tabindex_change)
        # Store the default settings
        self.default_tab_font = self.tabBar().font()
        self.default_icon_size = self.tabBar().iconSize()
        # Install tab-bar's event filter
        self.tabBar().installEventFilter(self)

    def customize_tab_bar(self):
        if settings.get("custom_menu_scale") != None and settings.get("custom_menu_font") != None:
            self.tabBar().setFont(qt.QFont(*settings.get("custom_menu_font")))
            new_icon_size = functions.create_size(
                settings.get("custom_menu_scale"), settings.get("custom_menu_scale")
            )
            self.setIconSize(new_icon_size)
        else:
            self.tabBar().setFont(settings.get_current_font())
            self.setIconSize(self.default_icon_size)
        self.tabBar().set_style()

    def __drag_filter(self, event):
        self.drag_dropped_file = None
        self.drag_text = None
        self.drag_source = None
        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0]
            if url.isValid():
                # Filter out non file items
                if url.scheme() == "file":
                    # "toLocalFile" returns path to file
                    self.drag_dropped_file = url.toLocalFile()
                    event.accept()
        elif event.mimeData().text() != None:
            try:
                name, index = event.mimeData().text().split()
                # Don't accept drags into self
                if name != self.name:
                    self.drag_source = event.source()
                    self.drag_text = event.mimeData().text()
                    event.accept()
            except:
                return

    def __init_drag_data(self, e):
        self.indexTab = self.currentIndex()
        self.tabRect = self.tabBar().tabRect(self.indexTab)
        self.pixmap = qt.QPixmap(self.tabRect.size())
        self.tabBar().render(self.pixmap, qt.QPoint(), qt.QRegion(self.tabRect))
        painter = qt.QPainter(self.pixmap)
        painter.setCompositionMode(
            painter.CompositionMode.CompositionMode_DestinationIn
        )
        painter.fillRect(self.pixmap.rect(), qt.QColor(0, 0, 0, 64))
        painter.end()

    def __start_tab_drag(self):
        index = self.currentIndex()
        if index != -1:
            mime_data = qt.QMimeData()
            #            mime_data.setText("{:s} {:d}".format(
            #                    self.name, index
            #                )
            #            )
            drag = qt.QDrag(self)
            drag.setMimeData(mime_data)
            drag.setPixmap(self.pixmap)
            drag.setHotSpot(
                qt.QPoint(int(self.tabRect.width() / 2), int(self.tabRect.height() / 2))
            )
            drag.exec(qt.Qt.DropAction.CopyAction | qt.Qt.DropAction.MoveAction)
            drag.destroyed.connect(self.__drag_destroyed)

    def store_drag_data(self):
        # Store drag information
        TabWidget.drag_event_data = {
            "name": self.tabText(self.currentIndex()),
            "index": self.currentIndex(),
        }

    def __drag_destroyed(self, *args):
        for i in (10, 0):
            mouse_event = qt.QMouseEvent(
                qt.QEvent.Type.MouseButtonRelease,
                qt.QPointF(i, i),
                qt.QPointF(i, i),
                qt.QPointF(i, i),
                qt.Qt.MouseButton.LeftButton,
                qt.Qt.MouseButton.LeftButton,
                qt.Qt.KeyboardModifier.NoModifier,
            )
            data.application.sendEvent(self.tabBar(), mouse_event)

    def _setmove_range(self):
        tabRect = self.tabBar().tabRect(self.currentIndex())
        pos = self.tabBar().mapFromGlobal(qt.QCursor.pos())
        self.move_range = pos.x() - tabRect.left(), tabRect.right() - pos.x()

    def eventFilter(self, source, event):
        if (
            event.type() == qt.QEvent.Type.KeyPress
            or event.type() == qt.QEvent.Type.KeyRelease
        ):
            # Check indication
            self.main_form.view.indication_check()

        if source == self.tabBar():
            if (
                event.type() == qt.QEvent.Type.MouseButtonPress
                and event.buttons() == qt.Qt.MouseButton.LeftButton
            ):
                qt.QTimer.singleShot(0, self._setmove_range)
            elif event.type() == qt.QEvent.Type.MouseButtonRelease:
                self.move_range = None
            elif (
                event.type() == qt.QEvent.Type.MouseMove and self.move_range is not None
            ):
                pos = event.pos()
                if self.tabBar().rect().contains(pos):
                    self.drag_lock = False
                else:
                    buttons = data.application.mouseButtons()
                    if buttons == qt.Qt.MouseButton.LeftButton:
                        if self.drag_lock == False:
                            if hasattr(self.main_form.display, "docking_overlay_show"):
                                self.drag_lock = True
                                self.main_form.display.docking_overlay_show()
                                self.__init_drag_data(event)
                                self.__start_tab_drag()
                    else:
                        self.drag_lock = False

                if (self.move_range is not None) and (pos.x() < self.move_range[0]):
                    return True
                elif (self.move_range is not None) and (
                    pos.x() > self.tabBar().width() - self.move_range[1]
                ):
                    return True
        return qt.QTabWidget.eventFilter(self, source, event)

    def dragEnterEvent(self, event):
        """
        Qt Drag event that fires when you click and drag something onto the basic widget
        """
        self.__drag_filter(event)

        if TabWidget.drag_event_data is not None:
            name = TabWidget.drag_event_data["name"]
            index = TabWidget.drag_event_data["index"]
            TabWidget.drag_event_data["source"] = event.source()

    def dropEvent(self, event):
        """
        Qt Drop event
        """
        try:
            if self.drag_dropped_file != None:
                # Open file in a new scintilla tab
                self.main_form.open_file(self.drag_dropped_file, self)
                event.accept()
            elif TabWidget.drag_event_data is not None:
                # Drag&drop widget event occured
                name = TabWidget.drag_event_data["name"]
                index = TabWidget.drag_event_data["index"]
                source = TabWidget.drag_event_data["source"]
                self.drag_tab_in(source, index)
                event.accept()
                TabWidget.drag_event_data = None
            else:
                event.ignore()
            # Reset the drag&drop data attributes
            self.drag_dropped_file = None
            self.drag_text = None
        except Exception as ex:
            self.main_form.display.repl_display_error(traceback.format_exc())
            traceback.print_exc()
            event.ignore()

        # Hide the docking overlay
        if hasattr(self.main_form.display, "docking_overlay_hide"):
            self.main_form.display.docking_overlay_hide()

    def enterEvent(self, enter_event):
        """Event that fires when the focus shifts to the TabWidget"""
        cw = self.currentWidget()
        if cw != None:
            # Check if the current widget is a custom editor or a QTextEdit widget
            if isinstance(cw, CustomEditor):
                # Get currently selected tab in the basic widget and display its name and lexer
                self.main_form.display.write_to_statusbar(cw.name)
            else:
                # Display only the QTextEdit name
                self.main_form.display.write_to_statusbar(cw.name)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        # Set focus to the clicked basic widget
        self.setFocus()
        # Set Save/SaveAs buttons in the menubar
        self._set_save_status()
        # Store the last focused widget to the parent
        self.main_form.last_focused_widget = self
        # Hide the function wheel if it is shown
        self.main_form.view.hide_all_overlay_widgets()
        if event.button() == qt.Qt.MouseButton.RightButton and self.count() == 0:
            # Show the function wheel if right clicked
            self.main_form.view.show_function_wheel()
        # Display the tab name in the log window
        if self.currentWidget() != None:
            tab_name = self.currentWidget().name
        else:
            # Clear the cursor positions in the statusbar
            self.main_form.display.update_cursor_position()
        # Reset the click&drag context menu action
        components.actionfilter.ActionFilter.clear_action()

        widget = self.currentWidget()
        if widget and isinstance(widget, ExternalWidget):
            widget.window_reference.raise_()

    def wheelEvent(self, wheel_event):
        """
        QScintilla mouse wheel rotate event
        """
        key_modifiers = qt.QApplication.keyboardModifiers()
        delta = wheel_event.angleDelta().y()
        if delta < 0:
            if key_modifiers == qt.Qt.KeyboardModifier.ControlModifier:
                # Zoom out the scintilla tab view
                self.zoom_out()
        else:
            if key_modifiers == qt.Qt.KeyboardModifier.ControlModifier:
                # Zoom in the scintilla tab view
                self.zoom_in()
        # Handle the event
        if key_modifiers == qt.Qt.KeyboardModifier.ControlModifier:
            # Accept the event, the event will not be propageted(sent forward) to the parent
            wheel_event.accept()
        else:
            # Propagate(send forward) the wheel event to the parent
            wheel_event.ignore()

    def resizeEvent(self, event):
        """Resize basic widget event"""
        # First execute the superclass resize event function
        super().resizeEvent(event)
        event.setAccepted(False)
        # Reposition the close button if needed
        self.close_button_reposition()

    def showEvent(self, event):
        super().showEvent(event)
        # Reposition the close button if needed
        self.close_button_reposition()

    def setFocus(self):
        """
        Overridden focus event
        """
        # Execute the supeclass focus function
        super().setFocus()
        # Check indication
        self.main_form.view.indication_check()

    def setTabText(self, *args, **kwargs):
        super().setTabText(*args, **kwargs)
        # Update window title
        data.signal_dispatcher.update_title.emit()

    def __signal_editor_tabindex_change(self, change_event):
        """Signal when the tab index changes"""
        # Set Save/SaveAs buttons in the menubar
        self._set_save_status()
        # Check if there is a tab in the tab widget
        current_tab = self.currentWidget()
        # Update the icons of the tabs
        for i in range(self.count()):
            self.update_tab_icon(self.widget(i))
        # Check close button
        self.check_close_button()
        # Update the corner widgets
        if current_tab is not None and hasattr(current_tab, "internals"):
            current_tab.internals.update_tab_widget(self)
            if current_tab.internals.update_corner_widget(current_tab) == False:
                # Remove the corner widget if the current widget is of an unknown type
                self.setCornerWidget(None)
        else:
            # Remove the corner widget if there is no current tab active
            self.setCornerWidget(None)

        self.store_drag_data()

        # Update window title
        data.signal_dispatcher.update_title.emit()

    def _signal_editor_tabclose(self, emmited_tab_number, force=False):
        """
        Event that fires when a tab close
        """

        # Nested function for clearing all bookmarks in the document
        def clear_document_bookmarks():
            # Check if bookmarks need to be cleared
            if isinstance(self.widget(emmited_tab_number), CustomEditor):
                self.main_form.bookmarks.remove_editor_all(
                    self.widget(emmited_tab_number)
                )

        # Store the tab reference
        tab = self.widget(emmited_tab_number)
        # Check if the document is modified
        if tab.savable == constants.CanSave.YES:
            if tab.save_status == constants.FileStatus.MODIFIED and force == False:
                # Display the close notification
                close_message = "Document '" + self.tabText(emmited_tab_number)
                close_message += "' has been modified!\nWhat do you wish to do?"
                reply = CloseEditorDialog.question(close_message)
                if reply == constants.DialogResult.SaveAndClose.value:
                    result = tab.save_document()
                    if result == False:
                        return
                    clear_document_bookmarks()
                    # Close tab anyway
                    self.removeTab(emmited_tab_number)
                elif reply == constants.DialogResult.Close.value:
                    clear_document_bookmarks()
                    # Close tab anyway
                    self.removeTab(emmited_tab_number)
                else:
                    # Cancel tab closing
                    return
            else:
                clear_document_bookmarks()
                # The document is unmodified
                self.removeTab(emmited_tab_number)
        else:
            clear_document_bookmarks()
            # The document cannot be saved, close it
            self.removeTab(emmited_tab_number)
        # Delete the tab from memory
        if hasattr(tab, "__del__"):
            tab.__del__()
        # Just in case, decrement the refcount of the tab (that's what del does)
        del tab

    def _signal_editor_cursor_change(self, cursor_line=None, cursor_column=None):
        """
        Signal that fires when cursor position changes
        """
        sender = self.sender()
        index = sender.positionFromLineIndex(cursor_line, cursor_column)
        self.main_form.display.update_cursor_position(cursor_line, cursor_column, index)

    def _set_save_status(self):
        """Enable/disable save/saveas buttons in the menubar"""
        cw = self.currentWidget()
        if cw != None:
            # Check if the current widget is a custom editor or a QTextEdit widget
            if isinstance(cw, CustomEditor):
                # Get currently selected tab in the basic widget and display its name and lexer
                self.main_form.display.write_to_statusbar(cw.name)
            else:
                # Display only the QTextEdit name
                self.main_form.display.write_to_statusbar(cw.name)
            # Set the Save/SaveAs status of the menubar
            if cw.savable == constants.CanSave.YES:
                self.main_form.set_save_file_state(True)
            else:
                self.main_form.set_save_file_state(False)
        if self.count() == 0:
            self.main_form.set_save_file_state(False)

    def _signal_text_changed(self):
        """Signal that is emmited when the document text changes"""
        # Check if the current widget is valid
        if self.currentWidget() == None:
            return
        # Update the save status of the current widget
        if self.currentWidget().savable == constants.CanSave.YES:
            # Set document as modified
            self.currentWidget().save_status = constants.FileStatus.MODIFIED
            # Check if special character is already in the name of the tab
            self.set_text_changed(self.currentIndex())
        # Update margin width
        self.editor_update_margin()

    def set_text_changed(self, index):
        if not "*" in self.tabText(index):
            self.setTabText(index, "*" + self.tabText(index) + "*")

    def reset_text_changed(self, index=None):
        """Reset the changed status of the current widget (remove the * symbols from the tab name)"""
        # Update the save status of the current widget
        if index is None:
            index = self.currentIndex()
        if self.widget(index).savable == constants.CanSave.YES:
            self.widget(index).save_status = constants.FileStatus.OK
            self.setTabText(index, self.tabText(index).strip("*"))

    def _set_wait_animation(self, index, show):
        tabBar = self.tabBar()
        if show:
            lbl = qt.QLabel(self)
            movie = qt.QMovie(
                os.path.join(data.resources_directory, "animations/wait.gif"),
                parent=lbl,
            )
            movie.setCacheMode(qt.QMovie.CacheMode.CacheAll)
            if settings.get("custom_menu_scale") != None:
                size = tuple([(x * settings.get("custom_menu_scale") / 16) for x in (16, 16)])
            else:
                size = (16, 16)
            movie.setScaledSize(functions.create_size(*size))
            lbl.setMovie(movie)
            movie.start()
            tabBar.setTabButton(index, qt.QTabBar.ButtonPosition.LeftSide, lbl)
        else:
            tabBar.setTabButton(index, qt.QTabBar.ButtonPosition.LeftSide, None)

    def close_tab(self, tab=None, force=False):
        """Close a tab in the basic widget"""
        # Return if there are no tabs open
        if self.count == 0:
            return
        # First check if a tab name was given
        if isinstance(tab, str):
            for i in range(0, self.count()):
                if self.tabText(i) == tab:
                    # Tab found, close it
                    self._signal_editor_tabclose(i, force)
                    break
        elif isinstance(tab, int):
            # Close the tab
            self._signal_editor_tabclose(tab, force)
        elif tab == None:
            # No tab number given, select the current tab for closing
            self._signal_editor_tabclose(self.currentIndex(), force)
        else:
            for i in range(0, self.count()):
                # Close tab by reference
                if self.widget(i) == tab:
                    # Tab found, close it
                    self._signal_editor_tabclose(i, force)
                    break

    def zoom_in(self):
        """Zoom in view function (it is the same for the CustomEditor and QTextEdit)"""
        # Zoom in
        try:
            self.currentWidget().zoomIn()
        except:
            pass
        # Update the margin width
        self.editor_update_margin()

    def zoom_out(self):
        """Zoom out view function (it is the same for the CustomEditor and QTextEdit)"""
        # Zoom out
        try:
            self.currentWidget().zoomOut()
        except:
            pass
        # Update the margin width
        self.editor_update_margin()

    def zoom_reset(self):
        """Reset the zoom to default"""
        # Check is the widget is a scintilla custom editor
        if isinstance(self.currentWidget(), CustomEditor):
            # Reset zoom
            self.currentWidget().zoomTo(0)
            # Update the margin width
            self.editor_update_margin()
        elif isinstance(self.currentWidget(), qt.QTextEdit):
            # Reset zoom
            self.currentWidget().setFont(self.default_editor_font)

    def plain_create_document(self, name):
        """Create a plain vanilla scintilla document"""
        # Initialize the custom editor
        new_scintilla_tab = PlainEditor(self, self.main_form)
        # Add attributes for status of the document (!!you can add attributes to objects that have the __dict__ attribute!!)
        new_scintilla_tab.name = name
        # Initialize the scrollbars
        new_scintilla_tab.SendScintilla(qt.QsciScintillaBase.SCI_SETVSCROLLBAR, True)
        new_scintilla_tab.SendScintilla(qt.QsciScintillaBase.SCI_SETHSCROLLBAR, True)
        # Hide the margin
        new_scintilla_tab.setMarginWidth(1, 0)
        # Disable drops
        new_scintilla_tab.setAcceptDrops(False)
        # Add needed signals
        new_scintilla_tab.cursorPositionChanged.connect(
            self._signal_editor_cursor_change
        )

        # Customize the mouse click event for the plain document with a decorator
        def custom_mouse_click(function_to_decorate):
            def decorated_function(*args, **kwargs):
                function_to_decorate(*args, **kwargs)
                # Set Save/SaveAs buttons in the menubar
                self._set_save_status()

            return decorated_function

        # Add the custom click decorator to the mouse click function
        new_scintilla_tab.mousePressEvent = custom_mouse_click(
            new_scintilla_tab.mousePressEvent
        )
        # Return the scintilla reference
        return new_scintilla_tab

    def plain_add_document(self, document_name):
        """Add a plain scintilla document to self(QTabWidget)"""
        # Create new scintilla object
        new_editor_tab = self.plain_create_document(document_name)
        # Add the scintilla document to the tab widget
        new_editor_tab_index = self.addTab(new_editor_tab, document_name)
        # Make new tab visible
        self.setCurrentIndex(new_editor_tab_index)
        # Return the reference to the new added scintilla tab widget
        return self.widget(new_editor_tab_index)

    def editor_create_document(self, file_with_path=None):
        """Create and initialize a custom scintilla document"""
        # Initialize the custom editor
        new_scintilla_tab = CustomEditor(self, self.main_form, file_with_path)
        # Connect the signals
        new_scintilla_tab.textChanged.connect(new_scintilla_tab.text_changed)
        return new_scintilla_tab

    def editor_add_document(self, document_name, type=None, bypass_check=False):
        """Check tab type and add a document to self(QTabWidget)"""
        if type == "file":
            ## New tab is a file on disk
            file_type = "unknown"
            if bypass_check == False:
                file_type = functions.get_file_type(document_name)
            if file_type != "unknown" or bypass_check == True:
                # Test if file can be read
                if functions.test_text_file(document_name) == None:
                    self.main_form.display.repl_display_message(
                        "Testing for TEXT file failed!",
                        message_type=constants.MessageType.ERROR,
                    )
                    # File cannot be read
                    return None
                # Create new scintilla document
                new_editor_tab = self.editor_create_document(document_name)
                # Set the lexer that colour codes the document
                new_editor_tab.choose_lexer(file_type)
                # Add the scintilla document to the tab widget
                new_editor_tab_index = self.addTab(
                    new_editor_tab, os.path.basename(document_name)
                )
                # Make the new tab visible
                self.setCurrentIndex(new_editor_tab_index)
                # Return the reference to the new added scintilla tab widget
                return self.widget(new_editor_tab_index)
            else:
                self.main_form.display.write_to_statusbar(
                    "Document is not a text file, doesn't exist or has an unsupported format!",
                    1500,
                )
                return None
        else:
            ## New tab is an empty tab
            # Create new scintilla object
            new_editor_tab = self.editor_create_document(document_name)
            # Add the scintilla document to the tab widget
            new_editor_tab_index = self.addTab(new_editor_tab, document_name)
            # Make new tab visible
            self.setCurrentIndex(new_editor_tab_index)
            # Return the reference to the new added scintilla tab widget
            return self.widget(new_editor_tab_index)

    def hexview_add(self, file_path):
        # Initialize the hex-view
        new_hexview = HexView(file_path, self, self.main_form)
        tab_text = "{} (Hex)".format(new_hexview.name)
        new_hexview_tab_index = self.addTab(new_hexview, tab_text)
        # Make new tab visible
        self.setCurrentIndex(new_hexview_tab_index)
        return self.widget(new_hexview_tab_index)

    terminal_count = 0

    def terminal_add(self):
        name = "TERMINAL-{}".format(self.terminal_count)
        self.terminal_count += 1
        # Initialize the hex-view
        new_terminal = Terminal(self, self.main_form, name)
        tab_text = name
        new_terminal_tab_index = self.addTab(new_terminal, tab_text)
        # Make new tab visible
        self.setCurrentIndex(new_terminal_tab_index)
        return self.widget(new_terminal_tab_index)

    def tree_create_tab(self, tree_tab_name, tree_type=None):
        """Create and initialize a tree display widget"""
        # Initialize the custom editor
        if tree_type != None:
            new_tree_tab = tree_type(self, self.main_form)
        else:
            new_tree_tab = TreeDisplay(self, self.main_form)
        # Add attributes for status of the document
        new_tree_tab.name = tree_tab_name
        new_tree_tab.savable = constants.CanSave.NO
        # Return the reference to the new added tree tab widget
        return new_tree_tab

    def tree_add_tab(self, tree_tab_name, tree_type=None):
        """Create and initialize a tree display widget"""
        # Initialize the custom editor
        new_tree_tab = self.tree_create_tab(tree_tab_name, tree_type)
        # Add the tree tab to the tab widget
        new_tree_tab_index = self.addTab(new_tree_tab, tree_tab_name)
        # Return the reference to the new added tree tab widget
        return self.widget(new_tree_tab_index)

    def terminal_emulator_add(self, tab_name, program):
        new_external_tab = create_external_widget(self, self.main_form, program)
        # Add the tree tab to the tab widget
        new_tree_tab_index = self.addTab(new_external_tab, tab_name)

    def editor_update_margin(self):
        """
        Update margin width according to the number of lines in the current document
        """
        # Check is the widget is a scintilla custom editor
        if isinstance(self.currentWidget(), CustomEditor):
            self.currentWidget().update_margin()

    def set_tab_name(self, tab, new_text):
        """
        Set the name of a tab by passing a reference to it
        """
        # Cycle through all of the tabs
        for i in range(self.count()):
            if self.widget(i) == tab:
                # Set the new text of the tab
                self.setTabText(i, new_text)
                break

    def select_tab(self, direction=constants.Direction.RIGHT):
        """
        Select tab left/right of the currently selected tab
        """
        current_index = self.currentIndex()
        if direction == constants.Direction.RIGHT:
            # Check if the widget is already at the far right
            if current_index < self.tabBar().count() - 1:
                new_index = current_index + 1
                self.setCurrentIndex(new_index)
        else:
            # Check if the widget is already at the far left
            if current_index > 0:
                new_index = current_index - 1
                self.setCurrentIndex(new_index)

    def move_tab(self, direction=constants.Direction.RIGHT):
        """
        Change the position of the current tab in the basic widget,
        according to the selected direction
        """
        # Store the current index and widget
        current_index = self.currentIndex()
        # Check the move direction
        if direction == constants.Direction.RIGHT:
            # Check if the widget is already at the far right
            if current_index < self.tabBar().count() - 1:
                new_index = current_index + 1
                self.tabBar().moveTab(current_index, new_index)
                # This hack is needed to correctly focus the moved tab
                self.setCurrentIndex(current_index)
                self.setCurrentIndex(new_index)
        else:
            # Check if the widget is already at the far left
            if current_index > 0:
                new_index = current_index - 1
                self.tabBar().moveTab(current_index, new_index)
                # This hack is needed to correctly focus the moved tab
                self.setCurrentIndex(current_index)
                self.setCurrentIndex(new_index)

    def update_tab_icon(self, tab):
        if (hasattr(tab, "current_icon") == True) and (tab.current_icon != None):
            self.setTabIcon(self.indexOf(tab), tab.current_icon)

    def copy_editor_in(self, source_tab_widget, source_index, focus_name):
        """Copy another CustomEditor widget into self"""
        # Create a new reference to the source custom editor
        source_widget = source_tab_widget.widget(source_index)
        # Check if the source tab is valid
        if source_widget == None:
            return
        # PlainEditor tabs should not be copied
        if isinstance(source_widget, CustomEditor) == False:
            self.main_form.display.repl_display_message(
                "Only custom editor tabs can be copied!",
                message_type=constants.MessageType.ERROR,
            )
            return
        # Check if the source file already exists in the target basic widget
        check_tab_widget, check_index = self.main_form.check_open_file(
            source_widget.save_name
        )
        if check_index is not None and check_tab_widget is self:
            # File is already open, focus it
            self.setCurrentIndex(check_index)
            return
        # Create a new editor document
        new_widget = self.editor_create_document(source_widget.save_name)
        # Add the copied custom editor to the target basic widget
        new_index = self.addTab(
            new_widget,
            source_tab_widget.tabIcon(source_index),
            source_tab_widget.tabText(source_index),
        )
        # Set focus to the copied widget
        self.setCurrentIndex(new_index)
        # Copy the source editor text and set the lexer accordigly
        source_widget.copy_self(new_widget)
        # Also reset the text change
        self.reset_text_changed(new_index)
        # Set Focus to the copied widget parent
        self.main_form.view.set_window_focus(focus_name)
        # Update the margin in the copied widget
        self.editor_update_margin()

    def move_editor_in(self, source_tab_widget, source_index):
        """Move another CustomEditor widget into self without copying it"""
        moved_widget = source_tab_widget.widget(source_index)
        moved_widget_icon = source_tab_widget.tabIcon(source_index)
        moved_widget_text = source_tab_widget.tabText(source_index)
        # Check if the source tab is valid
        if moved_widget == None:
            return
        # PlainEditor tabs should not evaluate its name
        if isinstance(moved_widget, CustomEditor) == True:
            # Check if the source file already exists in the target basic widget
            check_tab_widget, check_index = self.main_form.check_open_file(
                moved_widget.save_name
            )
            if check_index is not None and check_tab_widget is self:
                # File is already open, focus it
                self.setCurrentIndex(check_index)
                return
        # Move the custom editor widget from source to target
        new_index = self.addTab(moved_widget, moved_widget_icon, moved_widget_text)
        # Set focus to the copied widget
        self.setCurrentIndex(new_index)
        # Change the custom editor parent
        self.widget(new_index)._parent = self
        self.widget(new_index).internals.update_tab_widget(self)
        # Set Focus to the copied widget parent
        self.main_form.view.set_window_focus(source_tab_widget)
        # Update corner widget
        """
        This has to be done multiple times!
        Don't know why yet, maybe the PyQt parent transfer happens in the background???
        """
        for i in range(2):
            self.__signal_editor_tabindex_change(None)
            source_tab_widget.__signal_editor_tabindex_change(None)

    def drag_tab_in(self, source_tab_widget, source_index):
        """
        Drag another gui.forms.customeditor.CustomEditor widget into self without copying it
        """
        dragged_widget = source_tab_widget.widget(source_index)
        dragged_widget_icon = source_tab_widget.tabIcon(source_index)
        dragged_widget_text = source_tab_widget.tabText(source_index)
        # Check if the source tab is valid
        if dragged_widget is None:
            return
        # gui.forms.plaineditor.PlainEditor tabs should not evaluate its name
        if isinstance(dragged_widget, CustomEditor) == True:
            # Check if the source file already exists
            # in the target basic widget
            check_tab_widget, check_index = self.main_form.check_open_file(
                dragged_widget.save_name
            )
            if check_index is not None and check_tab_widget is self:
                # File is already open, focus it
                self.setCurrentIndex(check_index)
                return
        # Move the custom editor widget from source to target
        source_tab_widget.removeTab(source_tab_widget.indexOf(dragged_widget))
        new_index = self.addTab(
            dragged_widget, dragged_widget_icon, dragged_widget_text
        )

        # Update source tab corner buttons
        def update_source(*args):
            source_tab = source_tab_widget.currentWidget()
            if hasattr(source_tab, "add_corner_buttons"):
                source_tab.internals.update_corner_widget(source_tab)
                source_tab.internals.remove_corner_groupbox()
                source_tab.add_corner_buttons()

        qt.QTimer.singleShot(5, update_source)
        # Set focus to the copied widget
        self.setCurrentIndex(new_index)
        # Change the custom editor parent
        tab = self.widget(new_index)
        tab._parent = self

        def update_new(*args):
            tab.internals.update_tab_widget(self)
            if hasattr(tab, "add_corner_buttons"):
                tab.internals.update_corner_widget(tab)
                tab.internals.remove_corner_groupbox()
                tab.add_corner_buttons()

        qt.QTimer.singleShot(10, update_new)

    def tabs(self):
        for i in range(self.count()):
            yield self.widget(i)

    def close_all(self):
        for t in self.tabs():
            self.close_tab(t)

    def remove_from_box(self):
        main_form = self.main_form
        self.hide()
        self.setParent(None)
        # Repeat deletion for removal of newly emptied boxed
        for b in main_form.get_all_boxes():
            if b.is_empty() and b.objectName() != "Main":
                b.hide()
                b.setParent(None)
        # Reindex all tab widgets
        main_form.view.reindex_all_windows()

    def close_button_show(self):
        if not hasattr(self, "close_overlay"):
            close_button = StandardButton(
                self,
                self.main_form,
            )
            close_button.setIcon(functions.create_icon("various/close.png"))
            close_button.setIconSize(
                qt.QSize(
                    int(settings.get("tree_display_icon_size") * 2),
                    int(settings.get("tree_display_icon_size") * 2),
                )
            )
            tooltip = "Close this box"
            close_button.setToolTip(tooltip)
            close_button.setStatusTip(tooltip)
            close_button.set_click_function(self.remove_from_box)

            self.close_overlay = create_groupbox_borderless(self)
            self.close_overlay.setAlignment(
                qt.Qt.AlignmentFlag.AlignRight | qt.Qt.AlignmentFlag.AlignVCenter
            )
            self.close_overlay.setLayout(qt.QHBoxLayout())
            self.close_overlay.layout().addWidget(close_button)
            self.close_overlay.layout().setAlignment(
                qt.Qt.AlignmentFlag.AlignRight | qt.Qt.AlignmentFlag.AlignTop
            )
            self.close_overlay.setParent(self)
        self.close_overlay.show()
        self.close_button_reposition()

    def close_button_hide(self):
        if hasattr(self, "close_overlay"):
            self.close_overlay.hide()

    def close_button_reposition(self):
        if hasattr(self, "close_overlay"):
            if self.close_overlay.isVisible():
                self.close_overlay.resize(self.size())

    def check_close_button(self):
        # Show the close button
        if self.count() == 0 and len(self.main_form.get_all_windows()) > 1:
            self.close_button_show()
            self.close_button_reposition()
        else:
            self.close_button_hide()
