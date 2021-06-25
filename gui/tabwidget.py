
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2021 Matic Kukovec.
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

from .customeditor import *
from .dialogs import *
from .plaineditor import *
from .treedisplays import *
from .menu import *


"""
-----------------------------
Subclassed QTabWidget that can hold all custom editor and other widgets
-----------------------------
"""
class TabWidget(data.QTabWidget):          
    """Basic widget used for holding QScintilla/QTextEdit objects"""
    class CustomTabBar(data.QTabBar):
        """Custom tab bar used to capture tab clicks, ..."""
        # Reference to the parent widget
        _parent      = None
        # Reference to the main form
        main_form   = None
        # Reference to the tab menu
        tab_menu    = None
        
        def __init__(self, parent):
            """Initialize the tab bar object"""
            # Initialize superclass
            super().__init__(parent)
            # Store the parent reference
            self._parent = parent
            # Store the main form reference
            self.main_form = self._parent._parent
            # Set style
            self.set_style()
            # Set default font
            self.setFont(data.get_current_font())
        
        def set_style(self):
            close_image = functions.get_resource_file("feather/air-grey/x.svg")
            close_hover_image = functions.get_resource_file("feather/air-blue/x.svg")
            right_arrow_image = functions.get_resource_file("feather/air-grey/chevron-right.svg")
            right_arrow_hover_image = functions.get_resource_file("feather/air-blue/chevron-right.svg")
            left_arrow_image = functions.get_resource_file("feather/air-grey/chevron-left.svg")
            left_arrow_hover_image = functions.get_resource_file("feather/air-blue/chevron-left.svg")
            style = f"""
                QTabBar::close-button {{
                    image: url({close_image})
                }}
                QTabBar::close-button:hover {{
                    image: url({close_hover_image})
                }}
                
                QTabBar QToolButton {{
                    margin-bottom: 1px;
                    margin-left: 1px;
                }}
                
                QTabBar QToolButton::right-arrow {{
                    image: url({right_arrow_image});
                }}
                QTabBar QToolButton::right-arrow:hover {{
                    image: url({right_arrow_hover_image});
                }}
                
                QTabBar QToolButton::left-arrow {{
                    image: url({left_arrow_image});
                }}
                QTabBar QToolButton::left-arrow:hover {{
                    image: url({left_arrow_hover_image});
                }}
                
                QTabBar::tab {{
                    background: {data.theme.Indication.PassiveBackGround};
                    border: 1px solid {data.theme.Indication.PassiveBorder};
                    border-bottom-color: {data.theme.Indication.PassiveBackGround};
                    padding-top: 2px;
                    padding-bottom: 2px;
                    padding-left: 4px;
                    padding-right: 4px;
                    color: {data.theme.Font.DefaultHtml};
                }}
                QTabBar::tab:hover {{
                    background: {data.theme.Indication.Hover};
                    border-bottom-color: {data.theme.Indication.Hover};
                }}
                QTabBar::tab:selected {{
                    background: {data.theme.Indication.ActiveBackGround};
                    border: 1px solid {data.theme.Indication.ActiveBorder};
                    border-bottom-color: {data.theme.Indication.PassiveBackGround};
                }}
            """
            self.setStyleSheet(style)
        
        def mousePressEvent(self, event):
            #Execute the superclass event method
            super().mousePressEvent(event)
            event_button    = event.button()
            key_modifiers   = data.QApplication.keyboardModifiers()
            #Tab Drag&Drop functionality
            if event_button == data.Qt.LeftButton:
                if (key_modifiers == data.Qt.ControlModifier or
                    key_modifiers == data.Qt.ShiftModifier):
                    tab_number = self._parent.tabBar().tabAt(event.pos())
                    if tab_number != -1:
                        mime_data = data.QMimeData()
                        mime_data.setText("{} {:d}".format(self._parent.name, tab_number))
                        drag = data.QDrag(self._parent)
                        drag.setMimeData(mime_data)
                        drag.setHotSpot(event.pos())
                        drag.exec_(data.Qt.CopyAction | data.Qt.MoveAction)
        
        def mouseReleaseEvent(self, event):
            # Execute the superclass event method
            super().mouseReleaseEvent(event)
            event_button = event.button()
            # Check for a right click
            if event_button == data.Qt.RightButton:
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
                    event.pos()
                )
                self.tab_menu = menu
                # Show the tab context menu
                cursor = data.QCursor.pos()
                menu.popup(cursor)
                # Accept the event
                event.accept()
    
    class TabMenu(Menu):
        """Custom menu that appears when right clicking a tab"""
        def __init__(self, parent, main_form, tab_widget, editor_widget, cursor_position):
            #Nested function for creating a move or copy action
            def create_move_copy_action(action_name, 
                                        window_name, 
                                        move=True, 
                                        focus_name=None):
                window = main_form.get_window_by_name(window_name)
                action = data.QAction(action_name, self)
                if move == True:
                    func = window.move_editor_in
                    action_func = functools.partial(
                        func, 
                        tab_widget, 
                        parent.tabAt(cursor_position), 
                    )
                    icon = functions.create_icon('tango_icons/window-tab-move.png')
                else:
                    func = window.copy_editor_in
                    action_func = functools.partial(
                        func, 
                        tab_widget, 
                        parent.tabAt(cursor_position), 
                        focus_name
                    )
                    icon = functions.create_icon('tango_icons/window-tab-copy.png')
                action.setIcon(icon)
                action.triggered.connect(action_func)
                return action
            #Nested function for creating text difference actions
            def create_diff_action(action_name,
                                   main_form, 
                                   compare_tab_1, 
                                   compare_tab_2):
                def difference_function(main_form, 
                                        compare_tab_1, 
                                        compare_tab_2):
                    #Check for text documents in both tabs
                    if (isinstance(compare_tab_1, CustomEditor) == False and
                         isinstance(compare_tab_1, PlainEditor) == False):
                        main_form.display.repl_display_message(
                            "First tab is not a text document!", 
                            message_type=data.MessageType.ERROR
                        )
                        return
                    elif (isinstance(compare_tab_2, CustomEditor) == False and
                         isinstance(compare_tab_2, PlainEditor) == False):
                        main_form.display.repl_display_message(
                            "Second tab is not a text document!", 
                            message_type=data.MessageType.ERROR
                        )
                        return
                    #Initialize the compare parameters
                    text_1      = compare_tab_1.text()
                    text_1_name = compare_tab_1.name
                    text_2      = compare_tab_2.text()
                    text_2_name = compare_tab_2.name
                    #Display the text difference
                    main_form.display.show_text_difference(
                        text_1, 
                        text_2,
                        text_1_name, 
                        text_2_name
                    )
                diff_action = data.QAction(action_name, self)
                if "main" in action_name.lower():
                    diff_action.setIcon(functions.create_icon('tango_icons/compare-text-main.png'))
                elif "upper" in action_name.lower():
                    diff_action.setIcon(functions.create_icon('tango_icons/compare-text-upper.png'))
                else:
                    diff_action.setIcon(functions.create_icon('tango_icons/compare-text-lower.png'))
                function =  functools.partial(
                                difference_function, 
                                main_form, 
                                compare_tab_1, 
                                compare_tab_2
                            )
                diff_action.triggered.connect(function)
                return diff_action
            #Nested function for checking is the basic widgets current tab is an editor
            def check_for_editor(tab_widget):
                current_tab = tab_widget.currentWidget()
                if (isinstance(current_tab, CustomEditor) == True or
                    isinstance(current_tab, PlainEditor) == True):
                    return True
                else:
                    return False
            #Nested function for updating the current working directory
            def update_cwd():
                #Get the document path
                path = os.path.dirname(editor_widget.save_name)
                #Check if the path is not an empty string
                if path == "":
                    message = "Document path is not valid!"
                    main_form.display.repl_display_message(
                        message, 
                        message_type=data.MessageType.WARNING
                    )
                    return
                main_form.set_cwd(path)
            #Initialize the superclass
            super().__init__(parent)
            #Change the basic widget name to lowercase
            tab_widget_name = tab_widget.name.lower()
            #Add actions according to the parent TabWidget
            #Move actions
            move_to_main  = create_move_copy_action("Move to main window", "main")
            move_to_upper = create_move_copy_action("Move to upper window", "upper")
            move_to_lower = create_move_copy_action("Move to lower window", "lower")
            #Copy action
            copy_to_main = create_move_copy_action(
                "Copy to main window", 
                "main", 
                move=False, 
                focus_name="main"
            )
            copy_to_upper = create_move_copy_action(
                "Copy to upper window", 
                "upper", 
                move=False, 
                focus_name="upper"
            )
            copy_to_lower = create_move_copy_action(
                "Copy to lower window", 
                "lower", 
                move=False, 
                focus_name="lower"
            )
            #Clear REPL MESSAGES tab action
            clear_repl_action = data.QAction("Clear messages", self)
            clear_repl_action.setIcon(functions.create_icon('tango_icons/edit-clear.png'))
            clear_repl_action.triggered.connect(main_form.display.repl_clear_tab)
            #Text difference actions
            diff_main_action = create_diff_action(
                "Text diff to main window", 
                main_form, 
                main_form.main_window.currentWidget(), 
                editor_widget
            )
            diff_upper_action = create_diff_action(
                "Text diff to upper window", 
                main_form, 
                main_form.upper_window.currentWidget(), 
                editor_widget
            )
            diff_lower_action = create_diff_action(
                "Text diff to lower window", 
                main_form, 
                main_form.lower_window.currentWidget(), 
                editor_widget
            )
            #Update current working directory action
            if hasattr(editor_widget, "save_name") == True:
                update_cwd_action = data.QAction("Update CWD", self)
                update_cwd_action.setIcon(functions.create_icon('tango_icons/update-cwd.png'))
                update_cwd_action.triggered.connect(update_cwd)
                self.addAction(update_cwd_action)
                self.addSeparator()
            # Add the 'copy file name to clipboard' action
            clipboard_copy_action = data.QAction("Copy document name to clipboard", self)
            def clipboard_copy():
                cb = data.application.clipboard()
                cb.clear(mode=cb.Clipboard)
                cb.setText(editor_widget.name, mode=cb.Clipboard)
            clipboard_copy_action.setIcon(
                functions.create_icon('tango_icons/edit-copy.png')
            )
            clipboard_copy_action.triggered.connect(clipboard_copy)
            self.addAction(clipboard_copy_action)
            self.addSeparator()
            #Nested function for adding diff actions
            def add_diff_actions():
                #Diff to main window
                if (check_for_editor(main_form.main_window) == True and
                    editor_widget != main_form.main_window.currentWidget()):
                    self.addAction(diff_main_action)
                #Diff to upper window
                if (check_for_editor(main_form.upper_window) == True and
                    editor_widget != main_form.upper_window.currentWidget()):
                    self.addAction(diff_upper_action)
                #Diff to lower window
                if (check_for_editor(main_form.lower_window) == True and
                    editor_widget != main_form.lower_window.currentWidget()):
                    self.addAction(diff_lower_action)
            #Check which basic widget is the parent to the clicked tab
            if "main" in tab_widget_name:
                #Add the actions to the menu
                self.addAction(move_to_upper)
                self.addAction(move_to_lower)
                self.addSeparator()
                #Check the tab widget type
                if isinstance(editor_widget, CustomEditor) == True:
                    #Copy functions are only available to custom editors
                    self.addAction(copy_to_upper)
                    self.addAction(copy_to_lower)
                elif (isinstance(editor_widget, PlainEditor) == True and
                      editor_widget.name == "REPL MESSAGES"):
                    #REPL MESSAGES tab clear option
                    self.addAction(clear_repl_action)
                if (isinstance(editor_widget, CustomEditor) == True or
                    isinstance(editor_widget, PlainEditor) == True):
                    #Diff functions for plain and custom editors
                    self.addSeparator()
                    add_diff_actions()
            elif "upper" in tab_widget_name:
                #Add the actions to the menu
                self.addAction(move_to_main)
                self.addAction(move_to_lower)
                self.addSeparator()
                #Check the tab widget type
                if isinstance(editor_widget, CustomEditor) == True:
                    #Copy functions are only available to custom editors
                    self.addAction(copy_to_main)
                    self.addAction(copy_to_lower)
                elif (isinstance(editor_widget, PlainEditor) == True and
                      editor_widget.name == "REPL MESSAGES"):
                    #REPL MESSAGES tab clear option
                    self.addAction(clear_repl_action)
                if (isinstance(editor_widget, CustomEditor) == True or
                    isinstance(editor_widget, PlainEditor) == True):
                    #Diff functions for plain and custom editors
                    self.addSeparator()
                    add_diff_actions()
            elif "lower" in tab_widget_name:
                #Add the actions to the menu
                self.addAction(move_to_main)
                self.addAction(move_to_upper)
                self.addSeparator()
                #Check the tab widget type
                if isinstance(editor_widget, CustomEditor) == True:
                    #Copy functions are only available to custom editors
                    self.addAction(copy_to_main)
                    self.addAction(copy_to_upper)
                elif (isinstance(editor_widget, PlainEditor) == True and
                      editor_widget.name == "REPL MESSAGES"):
                    #REPL MESSAGES tab clear option
                    self.addAction(clear_repl_action)
                if (isinstance(editor_widget, CustomEditor) == True or
                    isinstance(editor_widget, PlainEditor) == True):
                    #Diff functions for plain and custom editors
                    self.addSeparator()
                    add_diff_actions()
            # Closing
            self.addSeparator()
            close_other_action = data.QAction(
                "Close all other tabs in this window", self
            )
            close_other_action.setIcon(
                functions.create_icon('tango_icons/close-all-tabs.png')
            )
            close_other_action.triggered.connect(
                functools.partial(
                    main_form.close_window_tabs,
                    tab_widget,
                    editor_widget
                )
            )
            self.addAction(close_other_action)
    
    
    # Class variables
    # Name of the basic widget                       
    name                    = ""
    # Reference to the last file that was drag&dropped onto the main  form
    drag_dropped_file       = None
    # Drag&Dropped text data
    drag_text               = None
    # The source widgets of the drag&drop event
    drag_source             = None
    # QMainWindow
    _parent                 = None
    # Custom tab bar
    custom_tab_bar          = None
    # Default font for textboxes
    default_editor_font     = data.QFont(data.current_font_name, data.current_font_size)
    # Default font and icon size for the tab bar
    default_tab_font        = None
    default_icon_size       = None
    # Attribute for indicating if the REPL is indicated
    indicated               = False
    
    
    def __init__(self, parent):
        """Initialization"""
        # Initialize superclass, from which the current class is inherited,
        # THIS MUST BE DONE SO THAT THE SUPERCLASS EXECUTES ITS __init__ !!!!!!
        super().__init__(parent)
        # Set various events and attributes
        # Save parent as a reference
        self._parent = parent
        # Set default font
        self.setFont(data.get_current_font())
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
        self.currentChanged.connect(self._signal_editor_tabindex_change)
        # Store the default settings
        self.default_tab_font = self.tabBar().font()
        self.default_icon_size = self.tabBar().iconSize()
    
    def customize_tab_bar(self):
        if data.custom_menu_scale != None and data.custom_menu_font != None:
            components.TheSquid.customize_menu_style(self.tabBar())
            self.tabBar().setFont(data.QFont(*data.custom_menu_font))
            new_icon_size = data.QSize(
                data.custom_menu_scale,
                data.custom_menu_scale
            )
            self.setIconSize(new_icon_size)
        else:
            components.TheSquid.customize_menu_style(self.tabBar())
            self.tabBar().setFont(data.get_current_font())
            self.setIconSize(self.default_icon_size)
        self.tabBar().set_style()

    def _drag_filter(self, event):
        self.drag_dropped_file  = None
        self.drag_text          = None
        self.drag_source        = None
        if event.mimeData().hasUrls():
            url=event.mimeData().urls()[0]
            if url.isValid():
                # Filter out non file items
                if url.scheme()=="file":
                    # "toLocalFile" returns path to file
                    self.drag_dropped_file=url.toLocalFile()
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
    
    def event(self, event):
        # Execute the superclass event method
        super().event(event)
        # Only check indication if the current widget is not indicated
        if self.indicated == False:
            if (event.type() == data.QEvent.KeyPress or
                event.type() == data.QEvent.KeyRelease):
                # Check indication
                self._parent.view.indication_check()
        # Indicate that the event was processed by returning True
        return True

    def dragEnterEvent(self, event):
        """Qt Drag event that fires when you click and drag something onto the basic widget"""
        self._drag_filter(event)
    
    def dropEvent(self, event):
        """Qt Drop event"""
        if self.drag_dropped_file != None:
            #Displays the file name with path
            data.print_log("Drag&Dropped: " + str(self.drag_dropped_file))
            #Open file in a new scintilla tab
            self._parent.open_file(self.drag_dropped_file,  self)
            event.accept()
        elif self.drag_text != None:
            #Drag&drop widget event occured
            try:
                name, str_index = self.drag_text.split()
                index = int(str_index)
                key_modifiers = data.QApplication.keyboardModifiers() 
                if (key_modifiers == data.Qt.ControlModifier or
                    key_modifiers == data.Qt.AltModifier):
                    self.copy_editor_in(self.drag_source, index)
                    data.print_log("Drag&Drop copied tab {:d} from the {} widget".format(index, name))
                else:
                    self.move_editor_in(self.drag_source, index)
                    data.print_log("Drag&Drop moved tab {:d} from the {} widget".format(index, name))
                event.accept()
            except:
                self._parent.display.repl_display_message(
                    traceback.format_exc(), 
                    message_type=data.MessageType.ERROR
                )
        #Reset the drag&drop data attributes
        self.drag_dropped_file  = None
        self.drag_text          = None

    def enterEvent(self, enter_event):
        """Event that fires when the focus shifts to the TabWidget"""
        cw = self.currentWidget() 
        if cw != None:
            #Check if the current widget is a custom editor or a QTextEdit widget
            if isinstance(cw, CustomEditor):
                #Get currently selected tab in the basic widget and display its name and lexer
                self._parent.display.write_to_statusbar(cw.name)
            else:
                #Display only the QTextEdit name
                self._parent.display.write_to_statusbar(cw.name)
        data.print_log("Entered TabWidget: " + str(self.name))

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        # Set focus to the clicked basic widget
        self.setFocus()
        # Set Save/SaveAs buttons in the menubar
        self._set_save_status()
        # Store the last focused widget to the parent
        self._parent.last_focused_widget = self
        data.print_log("Stored \"{}\" as last focused widget".format(self.name))
        # Hide the function wheel if it is shown
        self._parent.view.hide_all_overlay_widgets()
        if (event.button() == data.Qt.RightButton and
            self.count() == 0):
            # Show the function wheel if right clicked
            self._parent.view.show_function_wheel()
        # Display the tab name in the log window
        if self.currentWidget() != None:
            tab_name = self.currentWidget().name
            data.print_log("Mouse click in: \"" + str(tab_name) + "\"")
        else:
            # Clear the cursor positions in the statusbar
            self._parent.display.update_cursor_position()
            data.print_log("Mouse click in: \"" + self.name + "\"")
        # Reset the click&drag context menu action
        components.ActionFilter.clear_action()

    def wheelEvent(self, wheel_event):
        """QScintilla mouse wheel rotate event"""
        key_modifiers = data.QApplication.keyboardModifiers()
        if data.PYQT_MODE == 4:
            delta = wheel_event.delta()
        else:
            delta = wheel_event.angleDelta().y()
        if delta < 0:
            data.print_log("Mouse rotate down event")
            if key_modifiers == data.Qt.ControlModifier:
                #Zoom out the scintilla tab view
                self.zoom_out()
        else:
            data.print_log("Mouse rotate up event")
            if key_modifiers == data.Qt.ControlModifier:
                #Zoom in the scintilla tab view
                self.zoom_in()
        #Handle the event
        if key_modifiers == data.Qt.ControlModifier:
            #Accept the event, the event will not be propageted(sent forward) to the parent
            wheel_event.accept()
        else:
            #Propagate(send forward) the wheel event to the parent
            wheel_event.ignore()
    
    def resizeEvent(self, event):
        """Resize basic widget event"""
        #First execute the superclass resize event function
        super().resizeEvent(event)
        #Save the size relations between basic widgets
        self._parent.view.save_layout()
        event.setAccepted(False)
    
    def setFocus(self):
        """Overridden focus event"""
        #Execute the supeclass focus function
        super().setFocus()
        #Check indication
        self._parent.view.indication_check()

    def _signal_editor_tabindex_change(self, change_event):
        """Signal when the tab index changes"""
        # Set Save/SaveAs buttons in the menubar
        self._set_save_status()
        # Check if there is a tab in the tab widget
        current_tab = self.currentWidget()
        if current_tab:
            data.print_log("Selected tab: " + str(self.currentWidget().name))
        # Update the icons of the tabs
        for i in range(self.count()):
            self.update_tab_icon(self.widget(i))
        # Update the corner widgets
        if current_tab != None and hasattr(current_tab, "icon_manipulator"):
            if current_tab.icon_manipulator.update_corner_widget(current_tab) == False:
                # Remove the corner widget if the current widget is of an unknown type
                self.setCornerWidget(None)
        else:
            # Remove the corner widget if there is no current tab active
            self.setCornerWidget(None)

    def _signal_editor_tabclose(self, emmited_tab_number, force=False):
        """Event that fires when a tab close"""
        #Nested function for clearing all bookmarks in the document
        def clear_document_bookmarks():
            #Check if bookmarks need to be cleared
            if isinstance(self.widget(emmited_tab_number), CustomEditor):
                self._parent.bookmarks.remove_editor_all(self.widget(emmited_tab_number))
        data.print_log("Closing tab: " + str(self.tabText(emmited_tab_number)))
        # Store the tab reference
        tab = self.widget(emmited_tab_number)
        #Check if the document is modified
        if tab.savable == data.CanSave.YES:
            if tab.save_status == data.FileStatus.MODIFIED and force == False:
                #Close the log window if it is displayed
                self._parent.view.set_log_window(False)
                #Display the close notification
                close_message = "Document '" + self.tabText(emmited_tab_number)
                close_message += "' has been modified!\nClose it anyway?"
                reply = YesNoDialog.question(close_message)
                if reply == data.QMessageBox.Yes:
                    clear_document_bookmarks()
                    #Close tab anyway
                    self.removeTab(emmited_tab_number)
                else:
                    #Cancel tab closing
                    return
            else:
                clear_document_bookmarks()
                #The document is unmodified
                self.removeTab(emmited_tab_number)
        else:
            clear_document_bookmarks()
            #The document cannot be saved, close it
            self.removeTab(emmited_tab_number)
        # Delete the tab from memory
        if hasattr(tab, "clean_up"):
            tab.clean_up()
        # Just in case, decrement the refcount of the tab (that's what del does)
        del tab

    def _signal_editor_cursor_change(self, cursor_line=None, cursor_column=None):
        """Signal that fires when cursor position changes"""
        self._parent.display.update_cursor_position(cursor_line, cursor_column)
    
    def _set_save_status(self):
        """Enable/disable save/saveas buttons in the menubar"""
        cw = self.currentWidget()
        if cw != None:
            #Check if the current widget is a custom editor or a QTextEdit widget
            if isinstance(cw, CustomEditor):
                #Get currently selected tab in the basic widget and display its name and lexer
                self._parent.display.write_to_statusbar(cw.name)
            else:
                #Display only the QTextEdit name
                self._parent.display.write_to_statusbar(cw.name)
            #Set the Save/SaveAs status of the menubar
            if cw.savable == data.CanSave.YES:
                self._parent.set_save_file_state(True)
            else:
                self._parent.set_save_file_state(False)
        if self.count() == 0:
            self._parent.set_save_file_state(False)
    
    def _signal_text_changed(self):
        """Signal that is emmited when the document text changes"""
        #Check if the current widget is valid
        if self.currentWidget() == None:
            return
        #Update the save status of the current widget
        if self.currentWidget().savable == data.CanSave.YES:
            #Set document as modified
            self.currentWidget().save_status = data.FileStatus.MODIFIED
            #Check if special character is already in the name of the tab
            self.set_text_changed(self.currentIndex())
        #Update margin width
        self.editor_update_margin()
    
    def set_text_changed(self, index):
        if not "*" in self.tabText(index):
            self.setTabText(index, "*" + self.tabText(index) + "*")
    
    def reset_text_changed(self, index=None):
        """Reset the changed status of the current widget (remove the * symbols from the tab name)"""
        # Update the save status of the current widget
        if index is None:
            index = self.currentIndex()
        if self.widget(index).savable == data.CanSave.YES:
            self.widget(index).save_status = data.FileStatus.OK
            self.setTabText(index, self.tabText(index).strip("*"))
    
    def _set_wait_animation(self, index, show):
        tabBar = self.tabBar()
        if show:
            lbl = data.QLabel(self)
            movie = data.QMovie(
                os.path.join(
                    data.resources_directory, 
                    "animations/wait.gif"
                ),
                parent=lbl
            )
            movie.setCacheMode(data.QMovie.CacheAll)
            if data.custom_menu_scale != None:
                size = tuple([(x * data.custom_menu_scale / 16) for x in (16, 16)])
            else:
                size = (16, 16)
            movie.setScaledSize(data.QSize(*size))
            lbl.setMovie(movie)
            movie.start()
            tabBar.setTabButton(index, data.QTabBar.LeftSide, lbl)
        else:
            tabBar.setTabButton(index, data.QTabBar.LeftSide, None)

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
        #Zoom in
        try:
            self.currentWidget().zoomIn()
        except:
            pass
        #Update the margin width
        self.editor_update_margin()
    
    def zoom_out(self):
        """Zoom out view function (it is the same for the CustomEditor and QTextEdit)"""
        #Zoom out
        try:
            self.currentWidget().zoomOut()
        except:
            pass
        #Update the margin width
        self.editor_update_margin()

    def zoom_reset(self):
        """Reset the zoom to default"""
        #Check is the widget is a scintilla custom editor
        if isinstance(self.currentWidget(), CustomEditor):
            #Reset zoom
            self.currentWidget().zoomTo(0)
            #Update the margin width
            self.editor_update_margin()
        elif isinstance(self.currentWidget(), data.QTextEdit):
            #Reset zoom
            self.currentWidget().setFont(self.default_editor_font)
    
    def plain_create_document(self, name):
        """Create a plain vanilla scintilla document"""
        #Initialize the custom editor
        new_scintilla_tab = PlainEditor(self, self._parent)
        #Add attributes for status of the document (!!you can add attributes to objects that have the __dict__ attribute!!)
        new_scintilla_tab.name = name
        #Initialize the scrollbars
        new_scintilla_tab.SendScintilla(data.QsciScintillaBase.SCI_SETVSCROLLBAR, True)
        new_scintilla_tab.SendScintilla(data.QsciScintillaBase.SCI_SETHSCROLLBAR, True)
        #Hide the margin
        new_scintilla_tab.setMarginWidth(1, 0)
        #Disable drops
        new_scintilla_tab.setAcceptDrops(False)
        #Add needed signals
        new_scintilla_tab.cursorPositionChanged.connect(self._signal_editor_cursor_change)
        #Customize the mouse click event for the plain document with a decorator
        def custom_mouse_click(function_to_decorate):
            def decorated_function(*args, **kwargs):
                function_to_decorate(*args, **kwargs)
                #Set Save/SaveAs buttons in the menubar
                self._set_save_status()
            return decorated_function
        #Add the custom click decorator to the mouse click function
        new_scintilla_tab.mousePressEvent = custom_mouse_click(new_scintilla_tab.mousePressEvent)
        #Return the scintilla reference
        return new_scintilla_tab
    
    def plain_add_document(self, document_name):
        """Add a plain scintilla document to self(QTabWidget)"""
        #Create new scintilla object
        new_editor_tab = self.plain_create_document(document_name)
        #Add the scintilla document to the tab widget   
        new_editor_tab_index = self.addTab(new_editor_tab, document_name)
        #Make new tab visible
        self.setCurrentIndex(new_editor_tab_index)
        data.print_log("Added new empty tab: " + document_name)
        #Return the reference to the new added scintilla tab widget
        return self.widget(new_editor_tab_index)
    
    def editor_create_document(self, file_with_path=None):
        """Create and initialize a custom scintilla document"""
        #Initialize the custom editor
        new_scintilla_tab = CustomEditor(self, self._parent, file_with_path)
        #Connect the signals
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
                    self._parent.display.repl_display_message(
                        "Testing for TEXT file failed!", 
                        message_type=data.MessageType.ERROR
                    )
                    # File cannot be read
                    return None
                # Create new scintilla document
                new_editor_tab = self.editor_create_document(document_name)
                # Set the lexer that colour codes the document
                new_editor_tab.choose_lexer(file_type)
                # Add the scintilla document to the tab widget
                new_editor_tab_index = self.addTab(new_editor_tab, os.path.basename(document_name))
                # Make the new tab visible
                self.setCurrentIndex(new_editor_tab_index)              
                data.print_log("Added file: " + document_name)
                # Return the reference to the new added scintilla tab widget
                return self.widget(new_editor_tab_index)
            else:
                data.print_log("!! Document is not a text file or has an unsupported format")
                self._parent.display.write_to_statusbar("Document is not a text file, doesn't exist or has an unsupported format!", 1500)
                return None
        else:
            ## New tab is an empty tab
            # Create new scintilla object
            new_editor_tab = self.editor_create_document(document_name)
            # Add the scintilla document to the tab widget   
            new_editor_tab_index = self.addTab(new_editor_tab, document_name)
            # Make new tab visible
            self.setCurrentIndex(new_editor_tab_index)
            data.print_log("Added new empty tab: " + document_name)
            # Return the reference to the new added scintilla tab widget
            return self.widget(new_editor_tab_index)
    
    def tree_create_tab(self, tree_tab_name, tree_type=None):
        """Create and initialize a tree display widget"""
        # Initialize the custom editor
        if tree_type != None:
            new_tree_tab = tree_type(self, self._parent)
        else:
            new_tree_tab = TreeDisplay(self, self._parent)
        # Add attributes for status of the document
        new_tree_tab.name = tree_tab_name
        new_tree_tab.savable = data.CanSave.NO
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

    def editor_update_margin(self):
        """Update margin width according to the number of lines in the current document"""
        #Check is the widget is a scintilla custom editor
        if isinstance(self.currentWidget(), CustomEditor):
            self.currentWidget().update_margin()

    def set_tab_name(self, tab, new_text):
        """Set the name of a tab by passing a reference to it"""
        #Cycle through all of the tabs
        for i in range(self.count()):
            if self.widget(i) == tab:
                #Set the new text of the tab
                self.setTabText(i, new_text)
                break
    
    def select_tab(self, direction=data.Direction.RIGHT):
        """
        Select tab left/right of the currently selected tab
        """
        current_index = self.currentIndex()
        if direction == data.Direction.RIGHT:
            # Check if the widget is already at the far right
            if current_index < self.tabBar().count()-1:
                new_index = current_index + 1
                self.setCurrentIndex(new_index)
        else:
            # Check if the widget is already at the far left
            if current_index > 0:
                new_index = current_index - 1
                self.setCurrentIndex(new_index)
    
    def move_tab(self, direction=data.Direction.RIGHT):
        """
        Change the position of the current tab in the basic widget,
        according to the selected direction
        """
        #Store the current index and widget
        current_index = self.currentIndex()
        #Check the move direction
        if direction == data.Direction.RIGHT:
            #Check if the widget is already at the far right
            if current_index < self.tabBar().count()-1:
                new_index = current_index + 1
                self.tabBar().moveTab(current_index, new_index)
                #This hack is needed to correctly focus the moved tab
                self.setCurrentIndex(current_index)
                self.setCurrentIndex(new_index)
        else:
            #Check if the widget is already at the far left
            if current_index > 0:
                new_index = current_index - 1
                self.tabBar().moveTab(current_index, new_index)
                #This hack is needed to correctly focus the moved tab
                self.setCurrentIndex(current_index)
                self.setCurrentIndex(new_index)
    
    def update_tab_icon(self, tab):
        if (hasattr(tab, "current_icon") == True) and (tab.current_icon != None):
            self.setTabIcon(self.indexOf(tab), tab.current_icon)

    def copy_editor_in(self, source_tab_widget, source_index, focus_name=None):
        """Copy another CustomEditor widget into self"""
        #Create a new reference to the source custom editor
        source_widget = source_tab_widget.widget(source_index)
        #Check if the source tab is valid
        if source_widget == None:
            return
        #PlainEditor tabs should not be copied
        if isinstance(source_widget, CustomEditor) == False:
            self._parent.display.repl_display_message(
                "Only custom editor tabs can be copied!", 
                message_type=data.MessageType.ERROR
            )
            return
        #Check if the source file already exists in the target basic widget
        check_index = self._parent.check_open_file(source_widget.save_name, self)
        if check_index != None:
            #File is already open, focus it
            self.setCurrentIndex(check_index)
            return
        #Create a new editor document
        new_widget = self.editor_create_document(source_widget.save_name)
        #Add the copied custom editor to the target basic widget
        new_index = self.addTab(
            new_widget, 
            source_tab_widget.tabIcon(source_index), 
            source_tab_widget.tabText(source_index)
        )
        #Set focus to the copied widget
        self.setCurrentIndex(new_index)
        #Copy the source editor text and set the lexer accordigly
        source_widget.copy_self(new_widget)
        #Also reset the text change
        self.reset_text_changed(new_index)
        #Set Focus to the copied widget parent
        if focus_name == None:
            self._parent.view.set_window_focus(self.drag_source.name)
        else:
            self._parent.view.set_window_focus(focus_name) 
        #Update the margin in the copied widget
        self.editor_update_margin()

    def move_editor_in(self, source_tab_widget, source_index):
        """Move another CustomEditor widget into self without copying it"""
        moved_widget        = source_tab_widget.widget(source_index)
        moved_widget_icon   = source_tab_widget.tabIcon(source_index)
        moved_widget_text   = source_tab_widget.tabText(source_index)
        # Check if the source tab is valid
        if moved_widget == None:
            return
        # PlainEditor tabs should not evaluate its name
        if isinstance(moved_widget, CustomEditor) == True:
            # Check if the source file already exists in the target basic widget
            check_index = self._parent.check_open_file(moved_widget.save_name, self)
            if check_index != None:
                # File is already open, focus it
                self.setCurrentIndex(check_index)
                return
        # Move the custom editor widget from source to target
        new_index = self.addTab(moved_widget, moved_widget_icon, moved_widget_text)
        # Set focus to the copied widget
        self.setCurrentIndex(new_index)
        # Change the custom editor parent
        self.widget(new_index)._parent = self
        self.widget(new_index).icon_manipulator.update_tab_widget(self)
        # Set Focus to the copied widget parent
        self._parent.view.set_window_focus(source_tab_widget.name)
        # Update corner widget
        """
        This has to be done multiple times! 
        Don't know why yet, maybe the PyQt parent transfer happens in the background???
        """
        for i in range(2):
            self._signal_editor_tabindex_change(None)
            source_tab_widget._signal_editor_tabindex_change(None)



