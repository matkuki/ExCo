"""
Ex.Co. main editor window.

Central QMainWindow subclass managing editors, REPL, docking,
sessions, bookmarks, and the menubar. Most domain logic lives in
namespace sub-modules (settings, sessions, view, system, editing,
display, bookmarks, tools) instantiated during __init__.

Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import collections
import functools
import gc
import inspect
import itertools
import json
import keyword
import os
import re
import sys
import traceback
from typing import *

import components.actionfilter
import components.communicator
import components.processcontroller
import components.thesquid
import constants
import data
import functions
import lexers
import qt
import settings
import settings.constants

from gui.custombuttons import CustomButton
from gui.customeditor import CustomEditor
from gui.dialogs import (
    CloseEditorDialog,
    QuitDialog,
    RestoreSessionDialog,
    YesNoDialog,
)
from gui.dockingoverlay import DockingOverlay
from gui.excoinfo import ExCoInfo
from gui.externalprogram import ExternalWidget
from gui.functionwheel import FunctionWheel
from gui.hexview import HexView
from gui.plaineditor import PlainEditor
from gui.replbox import ReplBox
from gui.replindicator import ReplIndicator
from gui.sessionguimanipulator import SessionGuiManipulator
from gui.settingsguimanipulator import SettingsGuiManipulator
from gui.stylesheets import (
    StyleSheetButton,
    StyleSheetMenu,
    StyleSheetMenuBar,
    StyleSheetScrollbar,
    StyleSheetTable,
    StyleSheetTabWidget,
    StyleSheetTooltip,
    StyleSheetTreeWidget,
)
from gui.tabwidget import TabWidget
from gui.templates import (
    create_groupbox_with_layout,
)

from .bookmarks import Bookmarks
from .menubar import init_menubar as _init_menubar
from .tools import Tools
from gui.textdiffer import TextDiffer
from gui.thebox import TheBox
from gui.themeindicator import ThemeIndicator
from gui.treedisplays import (
    TreeDisplay,
    TreeExplorer,
)

from .display import Display
from .editing import Editing
from .sessions import Sessions
from .settings import Settings
from .system import System
from .view import View


class MainWindow(qt.QMainWindow):
    """
    Main form that holds all Qt objects
    """

    # Signals
    data_send = qt.pyqtSignal(object)

    # Define main form control references
    name = "Main Window"
    boxes_groupbox = None
    main_box = None
    main_splitter = None
    main_groupbox = (
        None  # QGroupBox that will hold the main splitter, needed for overlaying
    )
    main_groupbox_layout = None  # QVBoxLayout used by the main groupbox
    repl = None  # QLineEdit that will be used for the Python REPL
    repl_helper = (
        None  # QTextEdit helper for inputting more than one line into the REPL
    )
    repl_box = None  # QGroupBox that the REPL will be in
    repl_messages_tab = None  # Reference to a tab that displays REPL messages
    node_tree_tab = None  # Reference to a tab that displays NODE TREE information
    menubar = None  # Menubar
    recent_files_menu = None  # Recent files submenu in the Menubar
    sessions_menu = None  # Sessions option on the menubar
    toolbar = None  # Toolbar
    statusbar = None  # Statusbar
    statusbar_label_left = (
        None  # Left side of the statusbar for showing line and column numbers
    )
    docking_overlay = (
        None  # Left side of the statusbar for showing line and column numbers
    )
    # Flag for locking the main window keypress and release
    key_lock = False
    # Flag indicating the first time the user config file was imported
    _first_scan = True
    # Generator for supplying the number when a new document is created
    new_file_count = itertools.count(0, 1)
    # References for enabling/disabling saving of the current document in the menubar
    save_file_action = None
    saveas_file_action = None
    save_ascii_file_action = None
    save_ansiwin_file_action = None
    save_in_encoding = None
    # Attribute for signaling the state of the save buttons in the "File" menubar
    save_state = False
    # Supported Ex.Co. file extension types
    exco_file_exts = []
    for k, v in constants.supported_file_extentions.items():
        exco_file_exts.extend(["*" + x for x in v])
    # Dictionary for storing the menubar special functions
    menubar_functions = {}
    # Last focused widget and tab needed by the function wheel overlay
    last_focused_widget = None

    # Namespace references for grouping functionality
    settings = None
    sessions = None
    view = None
    system = None
    editing = None
    display = None
    bookmarks = None

    # External program reference
    external_program = None

    def __init__(self, new_document=False, logging=False, file_arguments=None):
        """
        Initialization routine for the main form
        """
        # Initialize superclass, from which the main form is inherited
        super().__init__()
        # Initialize the namespace references
        self.settings = Settings(self)
        self.sessions = Sessions(self)
        self.view = View(self)
        self.system = System(self)
        self.editing = Editing(self)
        self.display = Display(self)
        self.bookmarks = Bookmarks(self)
        self.tools = Tools(self)
        # Set the name of the main window
        self.name = "{} - PID:{}".format(self.get_default_title(), os.getpid())
        self.setObjectName("Form")
        # IPC communicator
        # self.communicator = components.communicator.IpcCommunicator(self.name)
        # self.data_send.connect(self.communicator.send)
        # self.communicator.received.connect(self.__data_received)
        # Filc communicator
        self.communicator = components.communicator.FileCommunicator(self.name)
        self.communicator.received.connect(self.__data_received)
        # Set default font
        self.setFont(settings.get_current_font())
        # Initialize the main window title
        self.reset_title()
        # Initialize statusbar
        self.init_statusbar()
        # Initialize the REPL
        self.init_repl()
        # Initialize the menubar
        self.init_menubar()
        # Initialize the docking overlay
        self.docking_overlay = DockingOverlay(self)

        # Initialize the debug print function
        def repl_print(*message):
            if len(message) == 1 and isinstance(message, str):
                message = ["REPL PRINT:\n", message[0]]
            else:
                message = ["REPL PRINT:\n"] + [str(x) for x in message]
            self.display.repl_display_message(
                *message, message_type=constants.MessageType.WARNING
            )

        functions.repl_print = repl_print
        # Initialize layout
        self.view.layout_init()
        # Set the initial window size according to the system resolution
        initial_size = self.view.function_wheel_overlay.size()
        initial_width = initial_size.width() * 14 / 10
        initial_height = initial_size.height() * 11 / 10
        self.resize(int(initial_width), int(initial_height))
        # Load the settings
        self.settings.restore()
        # Initialize REPL type indicator
        self.display.init_repl_indicator()
        self.display.repl_indicator.set_language(constants.ReplLanguage.Python)
        # Initialize the theme indicator
        self.display.init_theme_indicator()
        # Initialize repl interpreter
        self.init_interpreter()
        # Set the main window icon if it exists
        if os.path.isfile(data.application_icon) == True:
            self.setWindowIcon(qt.QIcon(data.application_icon))
        # Set the repl type to a single line
        self.view.set_repl_type(constants.ReplType.SINGLE_LINE)
        self.view.reset_entire_style_sheet()
        # Add a custom event filter
        self.installEventFilter(self)
        # Set flag on window to always show tooltips
        self.setAttribute(qt.Qt.WidgetAttribute.WA_AlwaysShowToolTips, True)
        # Connect signals
        data.signal_dispatcher.update_title.connect(self.update_title)
        # Store file arguments for opening after layout restoration
        self._startup_file_arguments = file_arguments
        # Always restore layout if enabled
        if settings.get("restore_last_session"):
            qt.QTimer.singleShot(0, self.__restore_last_session)
        else:
            # Only create new document if no layout restore AND no files
            if file_arguments is None and new_document == True:
                self.create_new()
        # Show the PyQt / QScintilla version in statusbar
        self.statusbar_label_left.setText(data.LIBRARY_VERSIONS)
        self.display.repl_display_message(
            "Using:\n    Python {}\n    {}".format(sys.version, data.LIBRARY_VERSIONS),
        )
        # Show library data
        if lexers.cython_lexers_found:
            self.display.repl_display_message(
                "Cython lexers imported.", message_type=constants.MessageType.SUCCESS
            )
        if lexers.nim_lexers_found:
            self.display.repl_display_message(
                "Nim lexers imported.", message_type=constants.MessageType.SUCCESS
            )

    def __restore_last_session(self) -> None:
        last_layout_filepath = functions.unixify_join(
            data.settings_directory, settings.get("last-layout-filename")
        )
        last_layout = functions.load_json_file(last_layout_filepath)
        self.view.layout_restore(last_layout)

        # Open startup files AFTER layout restore completes
        if (
            hasattr(self, "_startup_file_arguments")
            and self._startup_file_arguments is not None
        ):
            for file in self._startup_file_arguments:
                self.open_file(file=file, tab_widget=self.get_largest_window())

    def __del__(self) -> None:
        if hasattr(self, "communicator") and self.communicator is not None:
            del self.communicator

    def eventFilter(self, object, event):
        if event.type() == qt.QEvent.Type.Enter:
            self.display.docking_overlay_hide()

        if event.type() == qt.QEvent.Type.WindowActivate:
            pass
        elif event.type() == qt.QEvent.Type.WindowDeactivate:
            self.display.docking_overlay_hide()

        if event.type() in (
            qt.QEvent.Type.Enter,
            qt.QEvent.Type.MouseButtonPress,
            qt.QEvent.Type.KeyPress,
        ):
            if data.platform == "Windows":
                import win32gui

                try:
                    win32gui.SetFocus(self.winId())
                except:
                    pass
        elif event.type() == qt.QEvent.Type.Leave:
            if data.platform == "Windows":

                def set_external_focus():
                    import win32gui

                    try:
                        handle = win32gui.WindowFromPoint(win32gui.GetCursorPos())
                        if handle in ExternalWidget.handle_cache:
                            win32gui.SetFocus(handle)
                    except:
                        traceback.print_exc()

                qt.QTimer.singleShot(50, set_external_focus)

        return False

    @qt.pyqtSlot(object)
    def bring_to_foreground(self) -> None:
        if self.isMinimized():
            self.showNormal()
        if not self.isActiveWindow():
            flags = self.windowFlags()
            self.setWindowFlags(flags | qt.Qt.WindowType.WindowStaysOnTopHint)
            self.show()
            self.raise_()
            self.activateWindow()
            self.setWindowFlags(flags)
            self.show()

    def __data_received(self, _data: object) -> None:
        _from, message = _data

        def send(*args):
            self.data_send.emit(*args)

        if message == "ping":
            send("pong")

        elif isinstance(message, dict):
            if "command" in message.keys() and "arguments" in message.keys():
                command = message["command"]
                arguments = message["arguments"]
                if command == "open":
                    line = message.get("line")
                    for arg in arguments:
                        try:
                            tab = self.open_file(file=arg)
                            if line is not None and tab is not None:
                                tab.goto_line(line)
                        except:
                            self.display.repl_display_error(traceback.format_exc())
                    self.bring_to_foreground()

                elif command == "show":
                    self.bring_to_foreground()

    def get_default_title(self):
        return "Ex.Co. {}".format(data.application_version)

    def reset_title(self):
        self.setWindowTitle(self.get_default_title())

    @qt.pyqtSlot()
    def update_title(self):
        window = self.get_window_by_indication()
        if window is None:
            self.reset_title()
            return

        current_widget = window.currentWidget()
        current_index = window.currentIndex()
        if current_widget:
            if window.tabText(current_index).strip() != "":
                self.setWindowTitle(
                    "{} ({})".format(
                        window.tabText(current_index).strip(),
                        self.get_default_title(),
                    )
                )
            else:
                self.reset_title()

        else:
            self.reset_title()

    def init_statusbar(self):
        self.statusbar = qt.QStatusBar(self)
        self.statusbar.setFont(settings.get_current_font())
        self.display.write_to_statusbar("Status Bar")
        # Add label for showing the cursor position in a basic widget
        self.statusbar_label_left = qt.QLabel(self)
        self.statusbar_label_left.setText("")
        self.statusbar.addPermanentWidget(self.statusbar_label_left)
        # Add the statusbar to the MainWindow
        self.setStatusBar(self.statusbar)

    def get_all_boxes(self):
        return self.findChildren(TheBox)

    def get_all_windows(self):
        return self.findChildren(TabWidget)

    def get_all_tree_widgets(self):
        return self.findChildren(qt.QTreeView)

    def get_all_editors(self):
        windows = self.get_all_windows()
        editors = []
        for w in windows:
            for i in range(w.count()):
                widget = w.widget(i)
                if isinstance(widget, CustomEditor):
                    editors.append(widget)
        return editors

    def get_largest_window(self):
        largest_window = None
        surface = 0
        all_windows = self.get_all_windows()
        for tw in all_windows:
            compare_surface = tw.size().width() * tw.size().height()
            if compare_surface > surface:
                surface = compare_surface
                largest_window = tw
        if (largest_window is None) and (len(all_windows) > 0):
            largest_window = all_windows[-1]
        return largest_window

    def get_helper_window(self):
        helper_window = None
        windows = {}
        for tw in self.get_all_windows():
            compare_surface = tw.size().width() * tw.size().height()
            windows[compare_surface] = tw
        keys = list(windows.keys())
        keys.sort()
        if len(windows.keys()) > 1:
            helper_window = windows[keys[-2]]
        else:
            helper_window = windows[keys[-1]]
        return helper_window

    def get_repl_window(self):
        repl_window = None
        windows = {}
        for tw in self.get_all_windows():
            compare_surface = tw.size().width() * tw.size().height()
            while compare_surface in windows.keys():
                compare_surface += 1
            windows[compare_surface] = tw
        keys = list(windows.keys())
        keys.sort()
        if len(windows.keys()) > 2:
            repl_window = windows[keys[-3]]
        elif len(windows.keys()) > 1:
            repl_window = windows[keys[-2]]
        else:
            repl_window = windows[keys[-1]]
        return repl_window

    def get_form_references(self):
        """
        Create and return a dictionary that holds all the main form references
        that will be used by the REPL interpreter
        """
        return dict(
            form=self,
            quit=self.exit,
            exit=self.exit,
            new=self.create_new,
            _open=self.open_files,
            _open_d=self.open_file_with_dialog,
            save=functions.write_to_file,
            version=data.application_version,
            run=self.run_process,
            set_cwd=self.set_cwd,
            get_cwd=self.get_cwd,
            update_cwd=self.update_cwd,
            open_cwd=self.open_cwd,
            close_all=self.close_all_tabs,
            # Settings functions
            settings=settings,
            load_settings=self.settings.restore,
            # Session functions
            session_add=self.sessions.add,
            session_restore=self.sessions.restore,
            session_remove=self.sessions.remove,
            # System function
            find_files=self.system.find_files,
            find_in_files=self.system.find_in_files,
            replace_in_files=self.system.replace_in_files,
            # Document editing references
            find=self.editing.find,
            regex_find=lambda *a, **kw: self.editing.find(
                *a, regular_expression=True, **kw
            ),
            find_and_replace=self.editing.find_and_replace,
            regex_find_and_replace=lambda *a, **kw: self.editing.find_and_replace(
                *a, regular_expression=True, **kw
            ),
            goto_line=self.editing.line.goto,
            replace_all=self.editing.replace_all,
            regex_replace_all=lambda *a, **kw: self.editing.replace_all(
                *a, regular_expression=True, **kw
            ),
            replace_in_selection=self.editing.replace_in_selection,
            regex_replace_in_selection=lambda *a, **kw: (
                self.editing.replace_in_selection(*a, regular_expression=True, **kw)
            ),
            highlight=self.editing.highlight,
            regex_highlight=lambda *a, **kw: self.editing.highlight(
                *a, regular_expression=True, **kw
            ),
            clear_highlights=self.editing.clear_highlights,
            find_in_open_documents=self.editing.find_in_open_documents,
            find_replace_in_open_documents=self.editing.find_replace_in_open_documents,
            replace_all_in_open_documents=self.editing.replace_all_in_open_documents,
            replace_line=self.editing.line.replace,
            remove_line=self.editing.line.remove,
            get_line=self.editing.line.get,
            set_line=self.editing.line.set,
            # Display functions
            echo=self.display.repl_display_message,
            clear_repl_tab=self.display.repl_clear_tab,
            show_node_tree=self.display.show_nodes,
            # Other
            get_all_windows=self.get_all_windows,
            get_all_tree_widgets=self.get_all_tree_widgets,
            get_all_editors=self.get_all_editors,
        )

    def get_references_autocompletions(self):
        """Get the form references and autocompletions"""
        new_references = dict(
            itertools.chain(
                self.get_form_references().items(),
                self.repl.get_repl_references().items(),
            )
        )
        # Create auto completion list for the REPL
        ac_list_prim = [x for x in new_references]
        # Add Python/custom keywords to the primary level autocompletions
        ac_list_prim.extend(keyword.kwlist)
        ac_list_prim.extend(["range"])
        # Add current working directory items to the primary autocompletions
        ac_list_prim.extend(os.listdir(os.getcwd()))
        # Create the secondary autocompletion list
        # (methods and attributes of the primary list references)
        ac_list_sec = []
        keywords = new_references
        # Get all keyword methods and variables
        for key in keywords:
            ac_list_sec.append(key)
            # Add methods to secondary autocompletion list
            for method in inspect.getmembers(
                keywords[key], predicate=inspect.isroutine
            ):
                if str(method[0])[0] != "_":
                    ac_list_sec.append(str(key) + "." + str(method[0]))
            # Add variables to secondary autocompletion list
            try:
                for variable in keywords[key].__dict__:
                    if str(variable)[0] != "_":
                        ac_list_sec.append(str(key) + "." + str(variable))
            except:
                pass
        # Return the tuple
        return (new_references, ac_list_prim, ac_list_sec)

    def get_cwd(self):
        """
        Display the current working directory
        """
        self.display.repl_display_message(os.getcwd())

    def open_cwd(self):
        """Display the current working directory in the systems explorer"""
        self.system.show_explorer()

    def set_cwd(self, directory):
        """Set the current working directory and display it"""
        os.chdir(directory)
        # Store the current REPL text
        repl_text = self.repl.text()
        # Reset the interpreter and update its references
        self.reset_interpreter()
        # Display the selected directory
        self.display.repl_display_message("CWD changed to:")
        self.get_cwd()
        # Restore the previous REPL text
        self.repl.setText(repl_text)

    def update_cwd(self):
        """
        Set the current working directory to the path of the currently
        focused scintilla document in the main basic widget
        """

        # Nested function for displaying multiple messages
        def display(message):
            self.display.repl_display_message(
                message, message_type=constants.MessageType.WARNING
            )
            self.display.write_to_statusbar(message)

        # Get the document path
        window = self.get_window_by_indication()
        if window is None:
            return
        current_widget = window.currentWidget()
        path = os.path.dirname(current_widget.save_path)
        # Check if the path is not an empty string
        if path == "":
            message = "Document path is not valid!"
            display(message)
            return
        # Set the new current working directory
        self.set_cwd(path)

    def closeEvent(self, event):
        """
        Event that fires when the main window is closed
        """
        # Check if there are any modified documents
        if self.check_document_states() == True:
            quit_message = "You have modified documents!\nWhat do you wish to do?"
            reply = QuitDialog.question(quit_message)
            if reply == constants.DialogResult.Quit.value:
                pass
            elif reply == constants.DialogResult.SaveAllAndQuit.value:
                result = self.file_save_all()
                if result == False:
                    event.ignore()
            else:
                event.ignore()
        # Store current session if needed
        if settings.get("restore_last_session"):
            layout = self.view.layout_generate()
            settings.save_last_layout(layout)

    def resizeEvent(self, event):
        """
        Resize QMainWindow event
        """
        # Hide the function whell if it is displayed
        self.view.hide_all_overlay_widgets()
        # Accept the event
        event.setAccepted(False)

    def keyPressEvent(self, event):
        """
        QMainWindow keyPressEvent, to catch which key was pressed
        """
        # Check if the lock is released
        if self.key_lock == False:
            # Check for active keys
            if self.__window_filter_keypress(event) == True:
                return

    def keyReleaseEvent(self, event):
        """QMainWindow keyReleaseEvent, to catch which key was pressed"""
        # Check if the lock is released
        if self.key_lock == False:
            # Check for active keys
            if self.__window_filter_keyrelease(event) == True:
                return

    def mousePressEvent(self, event):
        """Overridden main window mouse click event"""
        # Execute the superclass mouse press event
        super().mousePressEvent(event)
        # Hide the function wheel if it is shown
        if event.button() != qt.Qt.MouseButton.RightButton:
            self.view.hide_all_overlay_widgets()
        # Reset the click&drag context menu action
        components.actionfilter.ActionFilter.clear_action()

    def __window_filter_keypress(self, key_event):
        """Filter keypress for appropriate action"""
        pressed_key = key_event.key()
        accept_keypress = False
        # Check for escape keypress
        if pressed_key == qt.Qt.Key.Key_Escape:
            # Check if the function wheel overlay is shown
            if self.view.function_wheel_overlay is not None:
                if self.view.function_wheel_overlay.isVisible():
                    self.view.hide_function_wheel()
            if self.settings.gui_manipulator is not None:
                if self.settings.gui_manipulator.isVisible():
                    self.view.hide_settings_manipulator()
        return accept_keypress

    def __window_filter_keyrelease(self, key_event):
        """Filter keyrelease for appropriate action"""
        # released_key = key_event.key()
        accept_keyrelease = False
        return accept_keyrelease

    def key_events_lock(self):
        """
        Function for disabling/locking the keypress and
        keyrelease events (used by the ReplLineEdit widget)
        """
        # Disable the key events of the QMainWindow
        self.key_lock = True
        # Disable the save/saveas buttons in the menubar
        self.set_save_file_state(False)

    def key_events_unlock(self):
        """
        Function for enabling/unlocking the keypress and
        keyrelease events (used by the ReplLineEdit widget)
        """
        # Reenable the key events of the QMainWindow
        self.key_lock = False

    def get_directory_with_dialog(self):
        """
        Function for using a QFileDialog window for retreiving
        a directory name as a string
        """
        directory = qt.QFileDialog.getExistingDirectory(
            self,  # QWidget parent = None
            None,  # QString caption = ''
            os.getcwd(),  # QString directory = ''
            # Options options = QFileDialog.ShowDirsOnly
        )
        return directory

    def run_process(self, command, show_console=True, output_to_repl=False):
        """
        Run a command line process and display the result
        """
        self.display.repl_display_message('Executing CMD command: "' + command + '"')
        # Run the command and display the result
        result = self.repl.get_interpreter().run_cmd_process(
            command, show_console, output_to_repl
        )
        self.display.repl_display_message(result)

    def file_create_new(self):
        """The function name says it all"""
        self.create_new(tab_name=None, tab_widget=self.last_focused_widget)

    def file_open(self):
        """The function name says it all"""
        self.open_file_with_dialog(tab_widget=self.last_focused_widget)

    def file_save(self, encoding="utf-8", line_ending=None):
        """The function name says it all"""
        focused_tab = self.get_tab_by_focus()
        if isinstance(focused_tab, CustomEditor) == True:
            if focused_tab is not None and focused_tab.savable == constants.CanSave.YES:
                focused_tab.save_document(
                    saveas=False, encoding=encoding, line_ending=line_ending
                )
                if encoding == "cp1250":
                    self.display.repl_display_success(
                        "Saved file {} in ANSI encoding.".format(focused_tab.save_path)
                    )
                elif encoding == "ascii":
                    self.display.repl_display_success(
                        "Saved file {} in ASCII encoding.".format(focused_tab.save_path)
                    )
                # Set the icon if it was set by the lexer
                focused_tab.internals.update_icon(focused_tab)
                # Reimport the user configuration file and update the menubar
                if functions.is_config_file(focused_tab.save_path) == True:
                    self.update_menubar()
                    self.import_user_functions()

    def file_saveas(self, encoding="utf-8"):
        """The function name says it all"""
        focused_tab = self.get_tab_by_focus()
        if focused_tab is not None:
            focused_tab.save_document(saveas=True, encoding=encoding)
            # Set the icon if it was set by the lexer
            focused_tab.internals.update_icon(focused_tab)
            # Reimport the user configuration file and update the menubar
            if functions.is_config_file(focused_tab.save_path) == True:
                self.update_menubar()
                self.import_user_functions()

    def file_save_all(self, encoding="utf-8"):
        """
        Save all open modified files
        """
        # Create a list of the windows
        windows = self.get_all_windows()
        # Loop through all the basic widgets/windows and check the tabs
        saved_something = False
        for window in windows:
            for i in range(0, window.count()):
                tab = window.widget(i)
                # Skip to next tab if it is not a CustomEditor
                if isinstance(tab, CustomEditor) == False:
                    continue
                # Test if the tab is modified and savable
                if (
                    tab.savable == constants.CanSave.YES
                    and tab.save_status == constants.FileStatus.MODIFIED
                ):
                    # Save the file
                    result = tab.save_document(saveas=False, encoding=encoding)
                    # Set the icon if it was set by the lexer
                    tab.internals.update_icon(tab)
                    # Set the saved something flag
                    saved_something = True
                    if result == False:
                        return False
        # Display the successful save
        if saved_something == False:
            self.display.repl_display_message(
                "No modified documents to save",
                message_type=constants.MessageType.WARNING,
            )
        else:
            self.display.repl_display_message(
                "'Save all' executed successfully",
                message_type=constants.MessageType.SUCCESS,
            )
        return True

    def update_menubar(self):
        """
        Update the Menubar in case any keyboard shortcuts
        were changed in the configuration file
        """
        self.init_menubar()
        self.settings.update_recent_list()
        self.sessions.update_menu()

    def init_menubar(self):
        _init_menubar(self)

    def init_repl(self):
        """
        Initialize everything that concerns the REPL
        """
        # Initialize the groupbox that the REPL will be in, and place the REPL widget into it
        self.repl_box = ReplBox(self, self.get_form_references())
        # Initialize the Python REPL widget
        self.repl = self.repl_box.repl
        self.repl_helper = self.repl_box.repl_helper

    def init_interpreter(self):
        """
        Initialize the python interactive interpreter that will
        be used with the python REPL QLineEdit
        """
        new_references, ac_list_prim, ac_list_sec = (
            self.get_references_autocompletions()
        )
        # Initialize and set auto completer for the REPL
        self.repl.interpreter_update_references(
            new_references, ac_list_prim, ac_list_sec
        )
        # Initialize the autocompletions for the REPL helper
        merged_autocompletions = [word for word in new_references]
        merged_autocompletions.extend(ac_list_prim)
        self.repl_helper.update_autocompletions(merged_autocompletions)
        # Import the user functions
        self.import_user_functions()

    def import_user_functions(self):
        """Import the user defined functions form the userfunctions.cfg file"""
        self.repl.skip_next_repl_focus()
        user_file_path = os.path.join(data.application_directory, data.config_file)
        # Test if userfunctions file exists
        if os.path.isfile(user_file_path) == False:
            #            message = "User functions file does not exist!\n"
            #            message += "Create an empty file named '{}' ".format(data.config_file)
            #            message += "in the application directory\n"
            #            message += "to make this error dissappear."
            #            self.display.repl_display_message(
            #                message,
            #                message_type=constants.MessageType.ERROR
            #            )
            # Ask to create the user definitions
            #            message = "Do you wish to generate the default user definition and function file?"
            #            reply = YesNoDialog.question(message)
            #            if reply == constants.DialogResult.Yes.value:
            #                functions.create_default_config_file()
            #                self.display.repl_display_success(
            #                    "Default user definitions file generated!"
            #                )
            # Just create the user definitions
            functions.create_default_config_file()
            message = "User functions file does not exist, creating the default one."
            self.display.repl_display_warning(message)
            return
        user_file = open(user_file_path, "r", encoding="utf-8")
        user_code = user_file.read()
        user_file.close()
        result = self.repl._repl_eval(user_code, display_action=False)
        if result is not None:
            self.display.repl_display_error(
                "ERROR IN USER CONFIGURATION FILE:\n" + result
            )
            return
        # Execute the data module's first_scan function once
        if self._first_scan == True:
            self._first_scan = False
            self.repl._repl_eval(
                "if callable(first_scan):\n    first_scan();", display_action=False
            )
        try:
            # Update the REPL autocompletions
            import_nodes, class_tree_nodes, function_nodes, global_vars = (
                functions.get_python_node_list(user_code)
            )
            # First get the function names
            user_function_names = [func.name for func in function_nodes]
            # Then get the autocompletions by testing if the function has
            # the "autocompletion" attribute. Because in Python everything is an object,
            # functions can also have attributes! Very nice!
            user_function_autocompletions = []
            for func_name in user_function_names:
                """User functions are stored in the REPL's intepreter 'locals' dictionary"""
                function = self.repl.get_interpreter().__dict__["locals"][func_name]
                # Check for the "autocompletions" attribute
                if hasattr(function, "autocompletion"):
                    user_function_autocompletions.append(function.autocompletion)
                else:
                    user_function_autocompletions.append(func_name)
            self.repl.interpreter_add_references(user_function_autocompletions)

            # Update the styles of all objects
            components.thesquid.TheSquid.update_styles()

            # Display the successful import
            self.display.write_to_statusbar("User functions imported successfully!")
        except:
            message = "!! Error importing user functions !!"
            self.display.repl_display_error(
                "{}\n{}".format(traceback.format_exc(), message)
            )
            self.display.write_to_statusbar(message)

    def reset_interpreter(self):
        new_references, ac_list_prim, ac_list_sec = (
            self.get_references_autocompletions()
        )
        # Initialize and set auto completer
        self.repl.interpreter_reset_references(
            new_references, ac_list_prim, ac_list_sec
        )
        # Reimport the user functions
        self.import_user_functions()
        # Display interpreter reset success
        self.display.write_to_statusbar(
            "REPL interpreter references successfully updated", 2000
        )

    def create_new(self, tab_name=None, tab_widget=None):
        """Creates an empty scintilla document using a generator counter"""
        # Set the new tab name
        if tab_name is None:
            tab_name = "new_" + str(next(self.new_file_count))
        # Create the new scintilla document in the selected basic widget
        return_widget = None
        if tab_widget is None:
            return_widget = self.get_largest_window().editor_add_document(
                tab_name, type="new"
            )
        else:
            return_widget = tab_widget.editor_add_document(tab_name, type="new")
        # Set focus to the new widget
        return_widget.setFocus()
        # Return the widget reference
        return return_widget

    def open_file_with_dialog(self, tab_widget=None):
        """Open a file for editing using a file dialog"""
        # Create and show a file dialog window, restore last browsed directory and set the file filter
        file_dialog = qt.QFileDialog
        files = file_dialog.getOpenFileNames(
            self,
            "Open File",
            os.getcwd(),
            "All Files (*);;Ex.Co. Files({})".format(" ".join(self.exco_file_exts)),
        )
        # Check and then add the selected file to the main TabWidget if the window parameter is unspecified
        self.open_files(files, tab_widget)

    def open_files(self, files=None, tab_widget=None):
        """Cheach and read valid files to the selected TabWidget"""
        # Check if the files are valid
        if files is None or files == "":
            return
        if isinstance(files, str):
            # Single file
            self.open_file(files, tab_widget)
        else:
            # List of files
            for file in files:
                self.open_file(file, tab_widget)

    def open_file(self, file=None, tab_widget=None, save_layout=False):
        """
        Read file contents into a TabWidget
        """

        def open_file_function(in_file, tab_widget):
            # Check if file exists
            if os.path.isfile(in_file) == False:
                self.display.repl_display_message(
                    "File: {}\ndoesn't exist!".format(in_file),
                    message_type=constants.MessageType.ERROR,
                )
                return
            # Check the file size
            file_size = functions.get_file_size_Mb(in_file)
            if file_size > 50:
                # Create the warning message
                warning = "The file is larger than 50 MB! ({:d} MB)\n".format(
                    int(file_size)
                )
                warning += "A lot of RAM will be needed!\n"
                warning += "Files larger than 300 MB can cause the system to hang!\n"
                warning += "Are you sure you want to open it?"
                reply = YesNoDialog.warning(warning)
                if reply == constants.DialogResult.No.value:
                    return
            # Check if file is already open
            check_tab_widget, check_index = self.check_open_file(in_file)
            if check_index is not None and check_tab_widget is not None:
                check_tab_widget.setCurrentIndex(check_index)
                return

            if tab_widget is None:
                tab_widget = self.get_largest_window()

            # Add new scintilla document tab to the basic widget
            new_tab = tab_widget.editor_add_document(
                in_file, "file", bypass_check=False
            )
            # Set the icon if it was set by the lexer
            new_tab.internals.update_icon(new_tab)

            if new_tab is not None:
                try:
                    # Read the whole file and display the text
                    file_text = functions.read_file_to_string(in_file)
                    # Remove the NULL characters
                    if "\0" in file_text:
                        # Use append, it does not remove the NULL characters
                        new_tab.append(file_text)
                        # Display a warning that the text has NULL characters
                        message = (
                            "CAUTION: NULL ('\\0') characters in file:\n'{}'".format(
                                in_file
                            )
                        )
                        self.display.repl_display_message(
                            message, message_type=constants.MessageType.WARNING
                        )
                    else:
                        new_tab.setText(file_text)
                    # Save the layout if needed
                    if save_layout == True:
                        self.view.layout_save()
                except MemoryError:
                    message = "Insufficient memory to open the file!"
                    self.display.repl_display_message(
                        message, message_type=constants.MessageType.ERROR
                    )
                    self.display.write_to_statusbar(message)
                    tab_widget.widget(tab_widget.currentIndex()).setParent(None)
                    tab_widget.removeTab(tab_widget.currentIndex())
                    return None
                except:
                    message = "Unexpected error occured while opening file!"
                    self.display.repl_display_message(
                        message, message_type=constants.MessageType.ERROR
                    )
                    self.display.write_to_statusbar(message)
                    tab_widget.widget(tab_widget.currentIndex()).setParent(None)
                    tab_widget.removeTab(tab_widget.currentIndex())
                    return None
                # Reset the changed status of the current tab,
                # because adding the file content line by line was registered as a text change
                tab_widget.reset_text_changed()
                # Update the settings manipulator with the new file
                self.settings.update_recent_list(in_file)
                # Update the current working directory
                path = os.path.dirname(in_file)
                if path == "":
                    path = data.application_directory
                self.set_cwd(path)
                # Set focus to the newly opened document
                tab_widget.currentWidget().setFocus()
                # Update the Save/SaveAs buttons in the menubar
                self.set_save_file_state(True)
                return new_tab
            else:
                message = "File cannot be read!\n"
                message += "It's probably not a text file!"
                self.display.repl_display_error(message)
                self.display.write_to_statusbar("File cannot be read!", 3000)
            return None

        if isinstance(file, str) == True:
            if file != "":
                new_tab = open_file_function(file, tab_widget)
                self.repaint()
                functions.process_events()
                return new_tab
        elif isinstance(file, list) == True:
            tabs = []
            for f in file:
                new_tab = open_file_function(f, tab_widget)
                tabs.append(new_tab)
                self.repaint()
                # Needed for every file opened to be visually updated clearly
                functions.process_events()
            return tabs
        else:
            self.display.repl_display_message(
                "Unknown parameter type to 'open file' function!",
                message_type=constants.MessageType.ERROR,
            )
            return None

    def open_file_hex(self, file_path, tab_widget=None, save_layout=False):
        # Check if file exists
        if os.path.isfile(file_path) == False:
            self.display.repl_display_message(
                "File: {}\ndoesn't exist!".format(file_path),
                message_type=constants.MessageType.ERROR,
            )
            return
        # Check the file size
        file_size = functions.get_file_size_Mb(file_path)
        if file_size > 50:
            # Create the warning message
            warning = "The file is larger than {0:d} MB! ({0:d} MB)\n".format(
                int(file_size)
            )
            warning += "A lot of RAM will be needed!\n"
            warning += "Files larger than 300 MB can cause the system to hang!\n"
            warning += "Are you sure you want to open it?"
            reply = YesNoDialog.warning(warning)
            if reply == constants.DialogResult.No.value:
                return
        # Check if file is already open
        check_tab_widget, check_index = self.check_open_file(
            file_path, _type=constants.FileType.Hex
        )
        if check_index is not None and check_tab_widget is not None:
            check_tab_widget.setCurrentIndex(check_index)
            return

        if tab_widget is None:
            tab_widget = self.get_largest_window()

        # Add new hexview document
        new_tab = tab_widget.hexview_add(file_path)
        # Update the icon
        new_tab.internals.update_icon(new_tab)

        if new_tab is not None:
            # Update the settings manipulator with the new file
            self.settings.update_recent_list(file_path)
            # Update the current working directory
            path = os.path.dirname(file_path)
            if path == "":
                path = data.application_directory
            self.set_cwd(path)
            # Set focus to the newly opened document
            tab_widget.currentWidget().setFocus()
            return new_tab
        else:
            message = "File cannot be read!"
            self.display.repl_display_error(message)
            self.display.write_to_statusbar("File cannot be read!", 3000)

    def check_open_file(self, file_with_path, _type=constants.FileType.Text):
        """
        Check if a file is already open in one of the windows
        """
        found_tab_widget = None
        found_index = None
        # Change the windows style path to the Unix style
        file_with_path = file_with_path.replace("\\", "/")
        for tab_widget in self.get_all_windows():
            # Loop through all of the documents in the tab widget
            if _type == constants.FileType.Text:
                for i in range(tab_widget.count()):
                    # Check the file name and file name with path
                    if (
                        tab_widget.widget(i).name == os.path.basename(file_with_path)
                        and tab_widget.widget(i).save_path == file_with_path
                    ):
                        # If the file is already open, get its index in the tab widget
                        found_tab_widget = tab_widget
                        found_index = i
                        break
            elif _type == constants.FileType.Hex:
                for i in range(tab_widget.count()):
                    # Check the file name and file name with path
                    tab = tab_widget.widget(i)
                    if isinstance(tab, HexView) and tab.save_path == file_with_path:
                        # If the file is already open, get its index in the tab widget
                        found_tab_widget = tab_widget
                        found_index = i
                        break

        return found_tab_widget, found_index

    def close_all_tabs(self):
        """
        Clear all documents from the main and upper window
        """
        # Check if there are any modified documents
        if self.check_document_states() == True:
            message = "You have modified documents!\nWhat do you wish to do?"
            reply = CloseEditorDialog.question(message)
            if reply == constants.DialogResult.SaveAndClose.value:
                self.file_save_all()
            elif reply == constants.DialogResult.Cancel.value:
                return
        # Close all tabs and remove all bookmarks from them
        for window in self.get_all_windows():
            for i in range(window.count()):
                if isinstance(window.widget(0), CustomEditor):
                    self.bookmarks.remove_editor_all(window.widget(0))
                window.close_tab(0, force=True)
        # Force a garbage collection cycle
        gc.collect()

    def close_window_tabs(self, tab_widget, widget):
        """
        Clear all other documents except the selected one
        in a specified basic widget
        """
        # Check if there are any modified documents
        if self.check_document_states(tab_widget) == True:
            message = "You have modified documents!\nWhat do you wish to do?"
            reply = CloseEditorDialog.question(message)
            if reply == constants.DialogResult.SaveAndClose.value:
                self.file_save_all()
            elif reply == constants.DialogResult.Cancel.value:
                return
        # Close all tabs and remove all bookmarks from them
        clear_index = 0
        for i in range(tab_widget.count()):
            if tab_widget.widget(clear_index) == widget:
                clear_index += 1
                continue
            if isinstance(tab_widget.widget(clear_index), CustomEditor):
                self.bookmarks.remove_editor_all(tab_widget.widget(clear_index))
            tab_widget.close_tab(clear_index, force=True)
        # Force a garbage collection cycle
        gc.collect()

    def set_save_file_state(self, enable):
        """Enable or disable the save functionality and save options under "File" in the menubar"""
        self.save_file_action.setEnabled(enable)
        self.saveas_file_action.setEnabled(enable)
        self.save_ascii_file_action.setEnabled(enable)
        self.save_ansiwin_file_action.setEnabled(enable)
        self.save_in_encoding.setEnabled(enable)
        self.save_all_action.setEnabled(enable)
        # Set the save state flag accordingly
        self.save_state = enable

    def _find_tab(self, predicate):
        """Find a tab matching a predicate across all windows."""
        windows = self.get_all_windows()
        for window in windows:
            for i in range(window.count()):
                widget = window.widget(i)
                if predicate(widget, window, i):
                    return widget
        return None

    def get_tab_by_name(self, tab_name):
        """Find a tab using its name in the basic widgets"""
        return self._find_tab(lambda w, win, i: win.tabText(i) == tab_name)

    def get_tab_by_save_path(self, in_save_path):
        """
        Find a tab using its save name (file path) in the tab widgets
        """
        return self._find_tab(
            lambda w, win, i: (
                isinstance(w, CustomEditor) and w.save_path == in_save_path
            )
        )

    def get_tab_by_string_in_name(self, string):
        """Find a tab with 'string' in its name in the basic widgets"""
        return self._find_tab(lambda w, win, i: string in win.tabText(i))

    def get_tab_by_focus(self):
        """
        Find the focused tab
        """
        windows = self.get_all_windows()
        # Loop through all the basic widgets/windows and check the tab focus
        for window in windows:
            for i in range(0, window.count()):
                if isinstance(window.widget(i), TextDiffer) == True:
                    if window.widget(i).editor_1.hasFocus() == True:
                        return window.widget(i).editor_1
                    elif window.widget(i).editor_2.hasFocus() == True:
                        return window.widget(i).editor_2
                else:
                    if window.widget(i).hasFocus() == True:
                        return window.widget(i)
            if self.repl_helper.hasFocus() == True:
                return self.repl_helper
        # No tab in the basic widgets has focus
        return None

    def get_tab_by_indication(self):
        windows = self.get_all_windows()
        for window in windows:
            for i in range(0, window.count()):
                if window.property("indicated") == True:
                    return window.currentWidget()
        return None

    def get_current_tab_by_parent_name(self, window_name):
        """
        Find the current tab by the parent TabWidget name property
        """
        widget = self.get_largest_window()
        return widget

    def get_used_tab(self):
        """
        Get the tab that was last used (if none return the main tab)
        """
        focused_tab = self.get_tab_by_focus()
        # Check if any tab is focused
        if focused_tab is None:
            focused_tab = self.get_largest_window()
        return focused_tab

    def get_window_by_focus(self):
        """
        Get the basic widget by focus
        """
        windows = self.get_all_windows()
        # Loop through all the basic widgets/windows and check their focus
        for window in windows:
            if window.hasFocus() == True:
                return window
        # No tab in the basic widgets has focus
        return None

    def get_window_by_child_tab(self):
        """
        Find the focused window by it's currently focused child tab
        (Same as get_tab_by_focus but returns the window instead of the tab)
        """
        windows = self.get_all_windows()
        # Loop through all the basic widgets/windows and check the tab focus
        for window in windows:
            for i in range(0, window.count()):
                if isinstance(window.widget(i), TextDiffer) == True:
                    if (
                        window.widget(i).editor_1.hasFocus() == True
                        or window.widget(i).editor_2.hasFocus() == True
                    ):
                        return window
                else:
                    if window.widget(i).hasFocus() == True:
                        return window
        # No tab in the basic widgets has focus
        return None

    def get_window_by_indication(self):
        windows = self.get_all_windows()
        for window in windows:
            for i in range(0, window.count()):
                if window.property("indicated") == True:
                    return window
        return None

    def get_window_by_name(self, window_name=None):
        """
        Get the tab widget by name
        """
        windows = self.get_all_windows()
        for w in windows:
            if window_name == w.objectName():
                return w
        return None

    def check_document_states(self, tab_widget=None):
        """
        Check if there are any modified documents in the editor windows
        """

        # Nested function for checking modified documents in a single basic widget
        # (just to play with nested functions)
        def check_documents_in_window(window):
            if window.count() > 0:
                for i in range(0, window.count()):
                    if window.widget(i).savable == constants.CanSave.YES:
                        if (
                            window.widget(i).save_status
                            == constants.FileStatus.MODIFIED
                        ):
                            return True
            return False

        if tab_widget is None:
            # Check all widget in all three windows for changes
            if any([check_documents_in_window(x) for x in self.get_all_windows()]):
                # Modified document found
                return True
            else:
                # No changes found
                return False
        else:
            return check_documents_in_window(tab_widget)

    def exit(self, event=None):
        """
        Exit application
        """
        # Close the MainWindow
        self.close()
