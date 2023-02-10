# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2023 Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import os
import itertools
import inspect
import functools
import keyword
import re
import collections
import functions
import settings
import settings.constants
import lexers
import traceback
import gc
import json
import data
import components.actionfilter
import components.communicator
import components.processcontroller
import components.thesquid

from .contextmenu import *
from .custombuttons import *
from .dialogs import *
from .excoinfo import *
from .functionwheel import *
from .messagelogger import *
from .tabwidget import *
from .plaineditor import *
from .customeditor import *
from .repllineedit import *
from .replhelper import *
from .replbox import *
from .sessionguimanipulator import *
from .settingsguimanipulator import *
from .textdiffer import *
from .treedisplays import *
from .menu import *
from .themeindicator import *
from .stylesheets import *
from .dockingoverlay import *
from .thebox import *
from .hexview import *
from .templates import *


"""
-------------------------------------------------
Main window and its supporting objects
-------------------------------------------------
"""
class MainWindow(data.QMainWindow):
    """
    Main form that holds all Qt objects
    """
    # Signals
    data_send = data.pyqtSignal(object)
    
    # Define main form control references
    name                    = "Main Window"
    boxes_groupbox          = None
    main_box                = None
    main_splitter           = None
    main_groupbox           = None  # QGroupBox that will hold the main splitter, needed for overlaying
    main_groupbox_layout    = None  # QVBoxLayout used by the main groupbox
    repl                    = None  # QLineEdit that will be used for the Python REPL
    repl_helper             = None  # QTextEdit helper for inputting more than one line into the REPL
    repl_box                = None  # QGroupBox that the REPL will be in
    repl_messages_tab       = None  # Reference to a tab that displays REPL messages
    node_tree_tab           = None  # Reference to a tab that displays NODE TREE information
    menubar                 = None  # Menubar
    recent_files_menu       = None  # Recent files submenu in the Menubar
    sessions_menu           = None  # Sessions option on the menubar
    toolbar                 = None  # Toolbar
    statusbar               = None  # Statusbar
    statusbar_label_left    = None  # Left side of the statusbar for showing line and column numbers
    docking_overlay         = None  # Left side of the statusbar for showing line and column numbers
    # Flag for locking the main window keypress and release
    key_lock                = False
    # Flag indicating the first time the user config file was imported
    _first_scan             = True
    # Generator for supplying the number when a new document is created
    new_file_count          = itertools.count(0, 1)
    # References for enabling/disabling saving of the current document in the menubar
    save_file_action            = None
    saveas_file_action          = None
    save_ascii_file_action      = None
    save_ansiwin_file_action    = None
    save_in_encoding            = None
    # Attribute for signaling the state of the save buttons in the "File" menubar
    save_state              = False
    # Supported Ex.Co. file extension types
    exco_file_exts =  []
    for k,v in data.supported_file_extentions.items():
        exco_file_exts.extend(['*' + x for x in v])
    # Dictionary for storing the menubar special functions
    menubar_functions       = {}
    # Last focused widget and tab needed by the function wheel overlay
    last_focused_widget     = None
    """Namespace references for grouping functionality"""
    settings                = None
    sessions                = None
    view                    = None
    system                  = None
    editing                 = None
    display                 = None
    bookmarks               = None


    def __init__(self, new_document=False, logging=False, file_arguments=None):
        """Initialization routine for the main form"""
        # Initialize superclass, from which the main form is inherited
        super().__init__()
        # Initialize the namespace references
        self.settings = self.Settings(self)
        self.sessions = self.Sessions(self)
        self.view = self.View(self)
        self.system = self.System(self)
        self.editing = self.Editing(self)
        self.display = self.Display(self)
        self.bookmarks = self.Bookmarks(self)
        # Set the name of the main window
        self.name = "{} - PID:{}".format(
            self.get_default_title(),
            os.getpid()
        )
        self.setObjectName("Form")
        # IPC communicator
#        self.communicator = components.communicator.IpcCommunicator(self.name)
#        self.data_send.connect(self.communicator.send)
#        self.communicator.received.connect(self.__data_received)
        # Filc communicator
        self.communicator = components.communicator.FileCommunicator(self.name)
        self.communicator.received.connect(self.__data_received)
        # Set default font
        self.setFont(data.get_current_font())
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
                *message,
                message_type=data.MessageType.WARNING
            )
        functions.repl_print = repl_print
        # Initialize layout
        self.view.layout_init()
        # Set the initial window size according to the system resolution
        initial_size = self.view.function_wheel_overlay.size()
        initial_width = initial_size.width() * 14/10
        initial_height = initial_size.height() * 11/10
        self.resize(int(initial_width), int(initial_height))
        # Load the settings
        self.settings.restore()
        # Initialize the theme indicator
        self.display.init_theme_indicator()
        # Initialize repl interpreter
        self.init_interpreter()
        # Set the main window icon if it exists
        if os.path.isfile(data.application_icon) == True:
            self.setWindowIcon(data.QIcon(data.application_icon))
        # Set the repl type to a single line
        self.view.set_repl_type(data.ReplType.SINGLE_LINE)
        self.view.reset_entire_style_sheet()
        # Add a custom event filter
        self.installEventFilter(self)
        # Set flag on window to always show tooltips
        self.setAttribute(data.Qt.WidgetAttribute.WA_AlwaysShowToolTips, True)
        # Connect signals
        data.signal_dispatcher.update_title.connect(self.update_title)
        # Open the file passed as an argument to the QMainWindow initialization
        if file_arguments is not None:
            for file in file_arguments:
                self.open_file(file=file, tab_widget=self.get_largest_window())
        else:
            # Create a new document in the main window if the flag was set and
            # the file_arguments is None
            if new_document == True:
                self.create_new()
        # Show the PyQt / QScintilla version in statusbar
        self.statusbar_label_left.setText(data.LIBRARY_VERSIONS)
        self.display.repl_display_message(
            "Using:\n    Python {}\n    {}".format(sys.version, data.LIBRARY_VERSIONS),
        )
        # Show library data
        if lexers.cython_lexers_found:
            self.display.repl_display_message(
                "Cython lexers imported.",
                message_type=data.MessageType.SUCCESS
            )
        if lexers.nim_lexers_found:
            self.display.repl_display_message(
                "Nim lexers imported.",
                message_type=data.MessageType.SUCCESS
            )
    
    def __del__(self) -> None:
        if hasattr(self, "communicator") and self.communicator is not None:
            del self.communicator

    def eventFilter(self, object, event):
        if event.type() == data.QEvent.Type.Enter:
            self.display.docking_overlay_hide()

        if event.type() == data.QEvent.Type.WindowActivate:
            pass
        elif event.type()== data.QEvent.Type.WindowDeactivate:
            self.display.docking_overlay_hide()

        return False
    
    @data.pyqtSlot(object)
    def __data_received(self, _data:object) -> None:
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
                    for arg in arguments:
                        try:
                            self.open_file(file=arg)
                        except:
                            traceback.print_exc()
                    self.showNormal()
                    self.activateWindow()
                
                elif command == "show":
                    self.showNormal()
                    self.activateWindow()

    def get_default_title(self):
        return "Ex.Co. {}".format(data.application_version)

    def reset_title(self):
        self.setWindowTitle(self.get_default_title())

    @data.pyqtSlot()
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
        self.statusbar = data.QStatusBar(self)
        self.statusbar.setFont(data.get_current_font())
        self.display.write_to_statusbar("Status Bar")
        #Add label for showing the cursor position in a basic widget
        self.statusbar_label_left = data.QLabel(self)
        self.statusbar_label_left.setText("")
        self.statusbar.addPermanentWidget(self.statusbar_label_left)
        #Add the statusbar to the MainWindow
        self.setStatusBar(self.statusbar)

    def get_all_boxes(self):
        return self.findChildren(TheBox)

    def get_all_windows(self):
        return self.findChildren(TabWidget)

    def get_all_tree_widgets(self):
        return self.findChildren(data.QTreeView)

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
        surface =  0
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
        surface =  0
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
        surface =  0
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
        return  dict(
            form        = self,
            quit        = self.exit,
            exit        = self.exit,
            new         = self.create_new,
            _open       = self.open_files,
            _open_d     = self.open_file_with_dialog,
            save        = functions.write_to_file,
            version     = data.application_version,
            run         = self.run_process,
            set_cwd         = self.set_cwd,
            get_cwd         = self.get_cwd,
            update_cwd      = self.update_cwd,
            open_cwd        = self.open_cwd,
            close_all       = self.close_all_tabs,
            # Settings functions
            settings        = self.settings.manipulator,
            save_settings   = self.settings.save,
            load_settings   = self.settings.restore,
            # Session functions
            session_add     = self.sessions.add,
            session_restore = self.sessions.restore,
            session_remove  = self.sessions.remove,
            # System function
            find_files       = self.system.find_files,
            find_in_files    = self.system.find_in_files,
            replace_in_files = self.system.replace_in_files,
            # Document editing references
            find                    = self.editing.find,
            regex_find              = self.editing.regex_find,
            find_and_replace        = self.editing.find_and_replace,
            regex_find_and_replace  = self.editing.regex_find_and_replace,
            goto_line               = self.editing.line.goto,
            replace_all             = self.editing.replace_all,
            regex_replace_all       = self.editing.regex_replace_all,
            replace_in_selection    = self.editing.replace_in_selection,
            regex_replace_in_selection  = self.editing.regex_replace_in_selection,
            highlight               = self.editing.highlight,
            regex_highlight         = self.editing.regex_highlight,
            clear_highlights        = self.editing.clear_highlights,
            find_in_open_documents          = self.editing.find_in_open_documents,
            find_replace_in_open_documents  = self.editing.find_replace_in_open_documents,
            replace_all_in_open_documents   = self.editing.replace_all_in_open_documents,
            replace_line            = self.editing.line.replace,
            remove_line             = self.editing.line.remove,
            get_line                = self.editing.line.get,
            set_line                = self.editing.line.set,
            # Display functions
            echo            = self.display.repl_display_message,
            clear_repl_tab  = self.display.repl_clear_tab,
            show_node_tree  = self.display.show_nodes,
            # Other
            get_all_windows  = self.get_all_windows,
            get_all_tree_widgets  = self.get_all_tree_widgets,
            get_all_editors  = self.get_all_editors,
        )

    def get_references_autocompletions(self):
        """Get the form references and autocompletions"""
        new_references  =   dict(
            itertools.chain(
                self.get_form_references().items(),
                self.repl.get_repl_references().items()
            )
        )
        #Create auto completion list for the REPL
        ac_list_prim    = [x for x in new_references]
        #Add Python/custom keywords to the primary level autocompletions
        ac_list_prim.extend(keyword.kwlist)
        ac_list_prim.extend(["range"])
        #Add current working directory items to the primary autocompletions
        ac_list_prim.extend(os.listdir(os.getcwd()))
        #Create the secondary autocompletion list
        #(methods and attributes of the primary list references)
        ac_list_sec     = []
        keywords        = new_references
        #Get all keyword methods and variables
        for key in keywords:
            ac_list_sec.append(key)
            #Add methods to secondary autocompletion list
            for method in inspect.getmembers(keywords[key], predicate=inspect.isroutine):
                if str(method[0])[0] != '_':
                    ac_list_sec.append(str(key) + "." + str(method[0]))
            #Add variables to secondary autocompletion list
            try:
                for variable in keywords[key].__dict__:
                    if str(variable)[0] != '_':
                        ac_list_sec.append(str(key) + "." + str(variable))
            except:
                pass
        #Return the tuple
        return (new_references, ac_list_prim, ac_list_sec)

    def get_cwd(self):
        """
        Display the current working directory
        """
        self.display.repl_display_message(os.getcwd())

    def open_cwd(self):
        """Display the current working directory in the systems explorer"""
        cwd = os.getcwd()
        if data.platform == "Windows":
            self.repl._repl_eval("r: explorer .")
        elif data.platform == "Linux":
            self.repl._repl_eval("r: xdg-open \"{}\"".format(cwd))
        else:
            self.display.repl_display_message(
                "Not implemented on '{}' platform!".format(data.platform)
            )

    def set_cwd(self, directory):
        """Set the current working directory and display it"""
        os.chdir(directory)
        #Store the current REPL text
        repl_text = self.repl.text()
        #Reset the interpreter and update its references
        self.reset_interpreter()
        #Display the selected directory
        self.display.repl_display_message("CWD changed to:")
        self.get_cwd()
        #Restore the previous REPL text
        self.repl.setText(repl_text)

    def update_cwd(self):
        """
        Set the current working directory to the path of the currently
        focused scintilla document in the main basic widget
        """
        #Nested function for displaying multiple messages
        def display(message):
            self.display.repl_display_message(
                message,
                message_type=data.MessageType.WARNING
            )
            self.display.write_to_statusbar(message)
        #Get the document path
        path = os.path.dirname(current_widget.save_name)
        #Check if the path is not an empty string
        if path == "":
            message = "Document path is not valid!"
            display(message)
            return
        #Set the new current working directory
        self.set_cwd(path)

    def closeEvent(self, event):
        """Event that fires when the main window is closed"""
        #Check if there are any modified documents
        if self.check_document_states() == True:
            quit_message = "You have modified documents!\nWhat do you wish to do?"
            reply = QuitDialog.question(quit_message)
            if reply == data.DialogResult.Quit.value:
                pass
            elif reply == data.DialogResult.SaveAllAndQuit.value:
                result = self.file_save_all()
                if result == False:
                    event.ignore()
            else:
                event.ignore()

    def resizeEvent(self, event):
        """Resize QMainWindow event"""
        #Save the size relations between basic widgets
        self.view.save_layout()
        #Hide the function whell if it is displayed
        self.view.hide_all_overlay_widgets()
        #Accept the event
        event.setAccepted(False)

    def keyPressEvent(self, event):
        """QMainWindow keyPressEvent, to catch which key was pressed"""
        #Check if the lock is released
        if self.key_lock == False:
            #Check for active keys
            if self.__window_filter_keypress(event) == True:
                return

    def keyReleaseEvent(self, event):
        """QMainWindow keyReleaseEvent, to catch which key was pressed"""
        #Check if the lock is released
        if self.key_lock == False:
            #Check for active keys
            if self.__window_filter_keyrelease(event) == True:
                return

    def mousePressEvent(self, event):
        """Overridden main window mouse click event"""
        # Execute the superclass mouse press event
        super().mousePressEvent(event)
        # Hide the function wheel if it is shown
        if event.button() != data.Qt.MouseButton.RightButton:
            self.view.hide_all_overlay_widgets()
        # Reset the click&drag context menu action
        components.actionfilter.ActionFilter.clear_action()

    def __window_filter_keypress(self, key_event):
        """Filter keypress for appropriate action"""
        pressed_key = key_event.key()
        accept_keypress = False
        #Check for escape keypress
        if pressed_key == data.Qt.Key.Key_Escape:
            #Check if the function wheel overlay is shown
            if self.view.function_wheel_overlay.isVisible() == True:
                self.view.toggle_function_wheel()
        return accept_keypress

    def __window_filter_keyrelease(self, key_event):
            """Filter keyrelease for appropriate action"""
            #released_key = key_event.key()
            accept_keyrelease = False
            return accept_keyrelease

    def key_events_lock(self):
        """
        Function for disabling/locking the keypress and
        keyrelease events (used by the ReplLineEdit widget)
        """
        #Disable the key events of the QMainWindow
        self.key_lock = True
        #Disable the save/saveas buttons in the menubar
        self.set_save_file_state(False)

    def key_events_unlock(self):
        """
        Function for enabling/unlocking the keypress and
        keyrelease events (used by the ReplLineEdit widget)
        """
        #Reenable the key events of the QMainWindow
        self.key_lock = False

    def get_directory_with_dialog(self):
        """
        Function for using a QFileDialog window for retreiving
        a directory name as a string
        """
        directory = data.QFileDialog.getExistingDirectory(
            self, # QWidget parent = None
            None, # QString caption = ''
            os.getcwd(), # QString directory = ''
            # Options options = QFileDialog.ShowDirsOnly
        )
        return directory

    def run_process(self, command, show_console=True, output_to_repl=False):
        """
        Run a command line process and display the result
        """
        self.display.repl_display_message("Executing CMD command: \"" + command + "\"")
        #Run the command and display the result
        result  = self.repl.interpreter.run_cmd_process(command, show_console, output_to_repl)
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
            if focused_tab is not None and focused_tab.savable == data.CanSave.YES:
                focused_tab.save_document(
                    saveas=False,
                    encoding=encoding,
                    line_ending=line_ending
                )
                if encoding == "cp1250":
                    self.display.repl_display_success("Saved file {} in ANSI encoding.".format(focused_tab.save_name))
                elif encoding == "ascii":
                    self.display.repl_display_success("Saved file {} in ASCII encoding.".format(focused_tab.save_name))
                # Set the icon if it was set by the lexer
                focused_tab.internals.update_icon(focused_tab)
                # Reimport the user configuration file and update the menubar
                if functions.is_config_file(focused_tab.save_name) == True:
                    self.update_menubar()
                    self.import_user_functions()

    def file_saveas(self, encoding="utf-8"):
        """The function name says it all"""
        focused_tab = self.get_tab_by_focus()
        if focused_tab is not None:
            focused_tab.save_document(
                saveas=True,
                encoding=encoding
            )
            #Set the icon if it was set by the lexer
            focused_tab.internals.update_icon(focused_tab)
            #Reimport the user configuration file and update the menubar
            if functions.is_config_file(focused_tab.save_name) == True:
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
                if (tab.savable == data.CanSave.YES and
                    tab.save_status == data.FileStatus.MODIFIED):
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
                message_type=data.MessageType.WARNING
            )
        else:
            self.display.repl_display_message(
                "'Save all' executed successfully",
                message_type=data.MessageType.SUCCESS
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
        """
        Initialize the menubar ("QAction.triggered.connect" signals
        first parameter is always "checked: bool").
        This is a very long function that should be trimmed sometime!
        """
        self.menubar = MenuBar()
        # Click filter for the menubar menus
        click_filter = components.actionfilter.ActionFilter(self)
        # Nested function for creating an action
        def create_action(name, key_combo, status_tip, icon, function, enabled=True):
            action = data.QAction(name, self)
            # Key combination
            keys = None
            if key_combo is not None and key_combo != "":
                if isinstance(key_combo, list):
                    if len(key_combo) == 1:
                        keys = key_combo[0]
                        if keys.startswith("#") == False:
                            action.setShortcut(keys)
                    elif any([isinstance(x, str) for x in key_combo]):
                        keys = []
                        for k in key_combo:
                            if k.startswith("#") == False:
                                keys.append(k)
                        action.setShortcuts(keys)
                    else:
                        raise Exception("Key combination list has to contain only strings!")
                elif isinstance(key_combo, str):
                    keys = key_combo
                    if keys.startswith("#") == False:
                        action.setShortcut(keys)
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
            self.menubar_functions[function.__name__] = function
            data.global_function_information[function.__name__] = (
                name, function, icon, keys, status_tip
            )
            #print(function.__name__)
            # Check if there is a tab character in the function
            # name and remove the part of the string after it
            if '\t' in name:
                name = name[:name.find('\t')]
            # Add the action to the context menu
            # function list in the helper forms module
            ContextMenu.add_function(
                function.__name__, action.pixmap, function, name
            )
            # Enable/disable action according to passed
            # parameter and return the action
            action.setEnabled(enabled)

            if hasattr(self.menubar, "stored_actions") == False:
                self.menubar.stored_actions = []
            self.menubar.stored_actions.append(action)
            return action
        # Nested function for writing text to the REPL
        def repl_text_input(text, cursor_position):
            self.repl.setText(text)
            self.repl.setFocus()
            self.repl.setCursorPosition(cursor_position)
        # File menu
        def construct_file_menu():
#            file_menu = self.menubar.addMenu("&File")
            file_menu = Menu("&File", self.menubar)
            self.menubar.addMenu(file_menu)
            file_menu.installEventFilter(click_filter)
            # New file
            def special_create_new_file():
                self.file_create_new()
            new_file_action = create_action(
                'New',
                settings.keyboard_shortcuts['general']['new_file'],
                'Create new empty file',
                'tango_icons/document-new.png',
                special_create_new_file
            )
            # Open file
            def special_open_file():
                self.file_open()
            open_file_action = create_action(
                'Open',
                settings.keyboard_shortcuts['general']['open_file'],
                'Open file',
                'tango_icons/document-open.png',
                special_open_file
            )
            # Save options need to be saved to a reference for disabling/enabling
            # Save file
            def special_save_file():
                self.file_save()
            self.save_file_action = create_action('Save', settings.keyboard_shortcuts['general']['save_file'], 'Save current file in the UTF-8 encoding', 'tango_icons/document-save.png', special_save_file, enabled=False)
            # Save file as
            def special_saveas_file():
                self.file_saveas()
            self.saveas_file_action = create_action('Save As', settings.keyboard_shortcuts['general']['saveas_file'], 'Save current file as a new file in the UTF-8 encoding', 'tango_icons/document-save-as.png', special_saveas_file, enabled=False)
            # Save all
            def special_save_all():
                self.file_save_all()
            self.save_all_action = create_action('Save All', None, 'Save all modified documents in all windows in the UTF-8 encoding', 'tango_icons/file-save-all.png', special_save_all, enabled=False)
            # Exit
            exit_action = create_action('Exit\tAlt+F4', None, 'Exit application', 'tango_icons/system-log-out.png', self.exit)
            # Additional menu for saving in different encodings
            def add_save_in_different_encoding_submenu():
                # Add the save in encoding menu
                self.save_in_encoding = Menu("Save in encoding...", self.menubar)
                self.save_in_encoding.setEnabled(False)
                temp_icon = functions.create_icon('tango_icons/document-save-as.png')
                self.save_in_encoding.setIcon(temp_icon)
                self.save_in_encoding.installEventFilter(click_filter)
                # Save as ASCII encoding
                temp_string = 'Save current file with the ASCII encoding, '
                temp_string += 'unknown characters will be replaced with "?"'
                def save_ascii_file():
                    self.file_save(encoding="ascii")
                self.save_ascii_file_action = create_action('ASCII', None, temp_string, None, save_ascii_file, enabled=False)
                # Save in ANSI Windows encoding
                temp_string = 'Save current file with the ANSI Windows (CP-1250) encoding with CR+LF line ending, '
                temp_string += 'unknown characters will be replaced with "?"'
                def save_ansi_file():
                    self.file_save(encoding="cp1250", line_ending="\r\n")
                self.save_ansiwin_file_action = create_action('ANSI (Windows)', None, temp_string, None, save_ansi_file, enabled=False)
                # Add the save options to to parent action
                self.save_in_encoding.addAction(self.save_ascii_file_action)
                self.save_in_encoding.addAction(self.save_ansiwin_file_action)
                # Add the parent action to the menu
                file_menu.addMenu(self.save_in_encoding)
            # Add the closing functions
            # Close tab
            def close_tab():
                try:
                    current_window  = self.get_window_by_child_tab()
                    current_index   = current_window.currentIndex()
                    current_window.close_tab(current_index)
                    #Focus the newly displayed tab
                    if current_window.count() > 0:
                        current_window.currentWidget().setFocus()
                except:
                    self.display.repl_display_error(traceback.format_exc())
            close_tab_action = create_action('Close Tab', settings.keyboard_shortcuts['general']['close_tab'], 'Close the current tab', 'tango_icons/close-tab.png', close_tab)
            # Close all
            close_all_action = create_action('Close All Tabs', None, 'Close all tabs in all windows', 'tango_icons/close-all-tabs.png', self.close_all_tabs)
            #Add load/save settings options
            save_settings_action = create_action('Save Settings', None, 'Save current settings', 'tango_icons/file-settings-save.png', self.settings.save)
            load_settings_action = create_action('Load Settings', None, 'Load saved settings', 'tango_icons/file-settings-load.png', self.settings.restore)
            #Add the editing option for the userfunctions file
            def open_user_func_file():
                user_definitions_file = os.path.join(
                    data.application_directory, data.config_file
                )
                #Test if userfunctions file exists
                if os.path.isfile(user_definitions_file) == False:
                    self.display.repl_display_message(
                        "User definitions file does not exist!",
                        message_type=data.MessageType.ERROR
                    )
                    message = "Do you wish to generate the default user definition and function file?"
                    reply = YesNoDialog.question(message)
                    if reply == data.DialogResult.Yes.value:
                        functions.create_default_config_file()
                        self.display.repl_display_message(
                            "Default user definitions file generated!",
                            message_type=data.MessageType.SUCCESS
                        )
                    else:
                        return
                self.open_file(user_definitions_file)
            edit_functions_action = create_action('Edit User Definitions', None, 'Open the {} file for editing in the main window'.format(data.config_file), 'tango_icons/file-user-funcs.png', open_user_func_file)
            #Add the reload option for the userfunctions file
            reload_functions_action = create_action('Reload User Definitions', None, 'Reload the {} file to refresh user defined definitions and functions'.format(data.config_file), 'tango_icons/file-user-funcs-reload.png', self.import_user_functions)
            #Add recent file list in the file menu
            recent_file_list_menu = self.view.create_recent_file_list_menu()
            clear_recent_file_list_action = create_action(
                'Clear recent files',
                None,
                'Clear the recent files list',
                'tango_icons/edit-clear.png',
                self.view.clear_recent_file_list,
            )
            #Add the actions to the File menu
            file_menu.addAction(new_file_action)
            file_menu.addAction(open_file_action)
            file_menu.addAction(self.save_file_action)
            file_menu.addAction(self.saveas_file_action)
            add_save_in_different_encoding_submenu()
            file_menu.addAction(self.save_all_action)
            file_menu.addSeparator()
            file_menu.addAction(close_tab_action)
            file_menu.addAction(close_all_action)
            file_menu.addSeparator()
            file_menu.addAction(save_settings_action)
            file_menu.addAction(load_settings_action)
            file_menu.addSeparator()
            file_menu.addAction(edit_functions_action)
            file_menu.addAction(reload_functions_action)
            file_menu.addSeparator()
            file_menu.addMenu(recent_file_list_menu)
            file_menu.addAction(clear_recent_file_list_action)
            file_menu.addSeparator()
            file_menu.addAction(exit_action)
        #Edit Menus
        #Adding the basic options to the menu
        def construct_edit_basic_menu():
            edit_menu = Menu("&Editing", self.menubar)
            self.menubar.addMenu(edit_menu)
            edit_menu.installEventFilter(click_filter)
            def copy():
                try:
                    self.get_tab_by_focus().copy()
                except:
                    self.display.repl_display_error(traceback.format_exc())
            temp_string = 'Copy any selected text in the currently '
            temp_string += 'selected window to the clipboard'
            copy_action = create_action(
                'Copy\t' + settings.keyboard_shortcuts['editor']['copy'],
                "#" + settings.keyboard_shortcuts['editor']['copy'],
                temp_string,
                'tango_icons/edit-copy.png',
                copy
            )
            def cut():
                try:
                    self.get_tab_by_focus().cut()
                except:
                    self.display.repl_display_error(traceback.format_exc())
            cut_action = create_action(
                'Cut\t' + settings.keyboard_shortcuts['editor']['cut'],
                "#" + settings.keyboard_shortcuts['editor']['cut'],
                'Cut any selected text in the currently selected window to the clipboard',
                'tango_icons/edit-cut.png',
                cut
            )
            def paste():
                try:
                    self.get_tab_by_focus().paste()
                except:
                    pass
            paste_action = create_action(
                'Paste\t' + settings.keyboard_shortcuts['editor']['paste'],
                "#" + settings.keyboard_shortcuts['editor']['paste'],
                'Paste the text in the clipboard to the currenty selected window',
                'tango_icons/edit-paste.png',
                paste
            )
            def undo():
                try:
                    self.get_tab_by_focus().undo()
                except:
                    self.display.repl_display_error(traceback.format_exc())
            undo_action = create_action(
                'Undo\t' + settings.keyboard_shortcuts['editor']['undo'],
                "#" + settings.keyboard_shortcuts['editor']['undo'],
                'Undo last editor action in the currenty selected window',
                'tango_icons/edit-undo.png',
                undo
            )
            def redo():
                try:
                    self.get_tab_by_focus().redo()
                except:
                    self.display.repl_display_error(traceback.format_exc())
            redo_action = create_action(
                'Redo\t' + settings.keyboard_shortcuts['editor']['redo'],
                "#" + settings.keyboard_shortcuts['editor']['redo'],
                'Redo last undone editor action in the currenty selected window',
                'tango_icons/edit-redo.png',
                redo
            )
            def select_all():
                try:
                    self.get_tab_by_focus().selectAll(True)
                except:
                    self.display.repl_display_error(traceback.format_exc())
            select_all_action = create_action(
                'Select All\t' + settings.keyboard_shortcuts['editor']['select_all'],
                "#" + settings.keyboard_shortcuts['editor']['select_all'],
                'Select all of the text in the currenty selected window',
                'tango_icons/edit-select-all.png',
                select_all
            )
            def indent():
                try:
                    self.get_tab_by_focus().custom_indent()
                except:
                    self.display.repl_display_error(traceback.format_exc())
            indent_action = create_action(
                'Indent\t' + settings.keyboard_shortcuts['editor']['indent'],
                "#" + settings.keyboard_shortcuts['editor']['indent'],
                'Indent the selected lines by the default width (4 spaces) in the currenty selected window',
                'tango_icons/format-indent-more.png',
                indent
            )
            def unindent():
                try:
                    self.get_tab_by_focus().custom_unindent()
                except:
                    self.display.repl_display_error(traceback.format_exc())
            unindent_action = create_action(
                'Unindent\t' + settings.keyboard_shortcuts['editor']['unindent'],
                "#" + settings.keyboard_shortcuts['editor']['unindent'],
                'Unindent the selected lines by the default width (4 spaces) in the currenty selected window',
                'tango_icons/format-indent-less.png',
                unindent
            )
            def delete_start_of_word():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.QsciScintillaBase.SCI_DELWORDLEFT)
                except:
                    self.display.repl_display_error(traceback.format_exc())
            del_start_word_action = create_action(
                'Delete start of word\t' + settings.keyboard_shortcuts['editor']['delete_start_of_word'],
                "#" + settings.keyboard_shortcuts['editor']['delete_start_of_word'],
                'Delete the current word from the cursor to the starting index of the word',
                'tango_icons/delete-start-word.png',
                delete_start_of_word
            )
            def delete_end_of_word():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.QsciScintillaBase.SCI_DELWORDRIGHT)
                except:
                    self.display.repl_display_error(traceback.format_exc())
            del_end_word_action = create_action(
                'Delete end of word\t' + settings.keyboard_shortcuts['editor']['delete_end_of_word'],
                "#" + settings.keyboard_shortcuts['editor']['delete_end_of_word'],
                'Delete the current word from the cursor to the ending index of the word',
                'tango_icons/delete-end-word.png',
                delete_end_of_word
            )
            def delete_start_of_line():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.QsciScintillaBase.SCI_DELLINELEFT)
                except:
                    self.display.repl_display_error(traceback.format_exc())
            del_start_line_action = create_action(
                'Delete start of line\t' + settings.keyboard_shortcuts['editor']['delete_start_of_line'],
                "#" + settings.keyboard_shortcuts['editor']['delete_start_of_line'],
                'Delete the current line from the cursor to the starting index of the line',
                'tango_icons/delete-start-line.png',
                delete_start_of_line
            )
            def delete_end_of_line():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.QsciScintillaBase.SCI_DELLINERIGHT)
                except:
                    self.display.repl_display_error(traceback.format_exc())
            del_end_line_action = create_action(
                'Delete end of line\t' + settings.keyboard_shortcuts['editor']['delete_end_of_line'],
                "#" + settings.keyboard_shortcuts['editor']['delete_end_of_line'],
                'Delete the current line from the cursor to the ending index of the line',
                'tango_icons/delete-end-line.png',
                delete_end_of_line
            )
            def goto_to_start():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.QsciScintillaBase.SCI_DOCUMENTSTART)
                except:
                    self.display.repl_display_error(traceback.format_exc())
            go_to_start_action = create_action(
                'Go to start\t' + settings.keyboard_shortcuts['editor']['go_to_start'],
                "#" + settings.keyboard_shortcuts['editor']['go_to_start'],
                'Move cursor up to the start of the currently selected document',
                'tango_icons/goto-start.png',
                goto_to_start
            )
            def goto_to_end():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.QsciScintillaBase.SCI_DOCUMENTEND)
                except:
                    self.display.repl_display_error(traceback.format_exc())
            go_to_end_action = create_action(
                'Go to end\t' + settings.keyboard_shortcuts['editor']['go_to_end'],
                "#" + settings.keyboard_shortcuts['editor']['go_to_end'],
                'Move cursor down to the end of the currently selected document',
                'tango_icons/goto-end.png',
                goto_to_end
            )
            def select_page_up():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.QsciScintillaBase.SCI_PAGEUPEXTEND)
                except:
                    self.display.repl_display_error(traceback.format_exc())
            select_page_up_action = create_action(
                'Select page up\t' + settings.keyboard_shortcuts['editor']['select_page_up'],
                "#" + settings.keyboard_shortcuts['editor']['select_page_up'],
                'Select text up one page of the currently selected document',
                'tango_icons/Input-keyboard.svg',
                select_page_up
            )
            def select_page_down():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.QsciScintillaBase.SCI_PAGEDOWN)
                except:
                    self.display.repl_display_error(traceback.format_exc())
            select_page_down_action = create_action(
                'Select page down\t' + settings.keyboard_shortcuts['editor']['select_page_down'],
                "#" + settings.keyboard_shortcuts['editor']['select_page_down'],
                'Select text down one page of the currently selected document',
                'tango_icons/Input-keyboard.svg',
                select_page_down
            )
            def select_to_start():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.QsciScintillaBase.SCI_DOCUMENTSTARTEXTEND)
                except:
                    self.display.repl_display_error(traceback.format_exc())
            select_to_start_action = create_action(
                'Select to start\t' + settings.keyboard_shortcuts['editor']['select_to_start'],
                "#" + settings.keyboard_shortcuts['editor']['select_to_start'],
                'Select all text up to the start of the currently selected document',
                'tango_icons/Input-keyboard.svg',
                select_to_start
            )
            def select_to_end():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.QsciScintillaBase.SCI_DOCUMENTENDEXTEND)
                except:
                    self.display.repl_display_error(traceback.format_exc())
            select_to_end_action = create_action(
                'Select to end\t' + settings.keyboard_shortcuts['editor']['select_to_end'],
                "#" + settings.keyboard_shortcuts['editor']['select_to_end'],
                'Select all text down to the start of the currently selected document',
                'tango_icons/Input-keyboard.svg',
                select_to_end
            )
            def scroll_up():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.QsciScintillaBase.SCI_PAGEUP)
                except:
                    self.display.repl_display_error(traceback.format_exc())
            scroll_up_action = create_action(
                'Scroll up\t' + settings.keyboard_shortcuts['editor']['scroll_up'],
                "#" + settings.keyboard_shortcuts['editor']['scroll_up'],
                'Scroll up one page of the currently selected document',
                'tango_icons/scroll-up.png',
                scroll_up
            )
            def scroll_down():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.QsciScintillaBase.SCI_PAGEDOWN)
                except:
                    self.display.repl_display_error(traceback.format_exc())
            scroll_down_action = create_action(
                'Scroll down\t' + settings.keyboard_shortcuts['editor']['scroll_down'],
                "#" + settings.keyboard_shortcuts['editor']['scroll_down'],
                'Scroll down one page of the currently selected document',
                'tango_icons/scroll-down.png',
                scroll_down
            )
            def line_cut():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.QsciScintillaBase.SCI_LINECUT)
                except:
                    self.display.repl_display_error(traceback.format_exc())
            line_cut_action = create_action(
                'Line Cut\t' + settings.keyboard_shortcuts['editor']['line_cut'],
                "#" + settings.keyboard_shortcuts['editor']['line_cut'],
                'Cut out the current line/lines of the currently selected document',
                'tango_icons/edit-line-cut.png',
                line_cut
            )
            def line_copy():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.QsciScintillaBase.SCI_LINECOPY)
                except:
                    self.display.repl_display_error(traceback.format_exc())
            line_copy_action = create_action(
                'Line Copy\t' + settings.keyboard_shortcuts['editor']['line_copy'],
                "#" + settings.keyboard_shortcuts['editor']['line_copy'],
                'Copy the current line/lines of the currently selected document',
                'tango_icons/edit-line-copy.png',
                line_copy
            )
            def line_delete():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.QsciScintillaBase.SCI_LINEDELETE)
                except:
                    self.display.repl_display_error(traceback.format_exc())
            line_delete_action = create_action(
                'Line Delete\t' + settings.keyboard_shortcuts['editor']['line_delete'],
                "#" + settings.keyboard_shortcuts['editor']['line_delete'],
                'Delete the current line of the currently selected document',
                'tango_icons/edit-line-delete.png',
                line_delete
            )
            def line_transpose():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.QsciScintillaBase.SCI_LINETRANSPOSE)
                except:
                    self.display.repl_display_error(traceback.format_exc())
            line_transpose_action = create_action(
                'Line Transpose\t' + settings.keyboard_shortcuts['editor']['line_transpose'],
                "#" + settings.keyboard_shortcuts['editor']['line_transpose'],
                'Switch the current line with the line above it of the currently selected document',
                'tango_icons/edit-line-transpose.png',
                line_transpose
            )
            def line_duplicate():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    #send_sci_message(data.QsciScintillaBase.SCI_LINEDUPLICATE)
                    send_sci_message(data.QsciScintillaBase.SCI_SELECTIONDUPLICATE)
                except:
                    self.display.repl_display_error(traceback.format_exc())
            line_duplicate_action = create_action(
                'Line/Selection Duplicate\t' + settings.keyboard_shortcuts['editor']['line_selection_duplicate'],
                "#" + settings.keyboard_shortcuts['editor']['line_selection_duplicate'],
                'Duplicate the current line/selection of the currently selected document',
                'tango_icons/edit-line-duplicate.png',
                line_duplicate
            )
            #Rectangular block selection
            action_text = 'Rectangular block selection\tAlt+Mouse'
            rect_block_action = data.QAction(
                functions.create_icon('tango_icons/Input-keyboard.svg'),
                action_text,
                self
            )
            temp_string = 'Select rectangle using the mouse in the currently selected document'
            rect_block_action.setStatusTip(temp_string)
#            temp_icon = functions.create_icon("")
#            rect_block_action.setIcon(temp_icon)
            edit_menu.addAction(cut_action)
            edit_menu.addAction(copy_action)
            edit_menu.addAction(paste_action)
            edit_menu.addAction(undo_action)
            edit_menu.addAction(redo_action)
            edit_menu.addAction(indent_action)
            edit_menu.addAction(unindent_action)
            edit_menu.addAction(select_all_action)
            edit_menu.addAction(line_cut_action)
            edit_menu.addAction(line_copy_action)
            edit_menu.addAction(line_delete_action)
            edit_menu.addAction(line_transpose_action)
            edit_menu.addAction(line_duplicate_action)
            edit_menu.addAction(scroll_up_action)
            edit_menu.addAction(scroll_down_action)
            edit_menu.addAction(del_start_word_action)
            edit_menu.addAction(del_end_word_action)
            edit_menu.addAction(del_start_line_action)
            edit_menu.addAction(del_end_line_action)
            edit_menu.addAction(go_to_start_action)
            edit_menu.addAction(go_to_end_action)
            edit_menu.addAction(select_page_up_action)
            edit_menu.addAction(select_page_down_action)
            edit_menu.addAction(select_to_start_action)
            edit_menu.addAction(select_to_end_action)
            edit_menu.addAction(rect_block_action)
        def construct_edit_advanced_menu():
            edit_menu = Menu("&Advanced", self.menubar)
            self.menubar.addMenu(edit_menu)
            edit_menu.installEventFilter(click_filter)
            #Nested special function for finding text in the currentlly focused custom editor
            def special_find():
                try:
                    focused_tab = self.get_used_tab()
                    selected_text = focused_tab.selectedText().replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n")
                    temp_string = 'find("{}",'.format(selected_text)
                    temp_string += 'case_sensitive=False,'
                    temp_string += 'search_forward=True,'
                    temp_string += 'window_name="{}")'.format(focused_tab._parent.name)
                    self.repl.setText(temp_string)
                except:
                    self.repl.setText('find("",case_sensitive=False)')
                self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                self.repl.setFocus()
                self.repl.setCursorPosition(self.repl.text().find('",case_sensitive'))
            find_action = create_action(
                'Find',
                settings.keyboard_shortcuts['general']['find'],
                'Find text in the currently selected document',
                'tango_icons/edit-find.png',
                special_find
            )
            #Nested special function for finding text in the currentlly focused
            #custom editor using regular expressions
            def special_regex_find():
                try:
                    focused_tab = self.get_used_tab()
                    selected_text = focused_tab.selectedText().replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n")
                    temp_string = 'regex_find(r"{}",'.format(selected_text)
                    temp_string += 'case_sensitive=False,'
                    temp_string += 'search_forward=True,'
                    temp_string += 'window_name="{}")'.format(focused_tab._parent.name)
                    self.repl.setText(temp_string)
                except:
                    self.repl.setText('regex_find(r"",case_sensitive=False)')
                self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                self.repl.setFocus()
                self.repl.setCursorPosition(self.repl.text().find('",case_sensitive'))
            regex_find_action = create_action(
                'Regex Find',
                settings.keyboard_shortcuts['general']['regex_find'],
                'Find text in currently selected document using Python regular expressions',
                'tango_icons/edit-find-re.png',
                special_regex_find
            )
            #Nested special function for finding and replacing one instance of text in the current main window custom editor
            def special_find_and_replace():
                try:
                    focused_tab = self.get_used_tab()
                    selected_text = focused_tab.selectedText().replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n")
                    temp_string = 'find_and_replace("{}","",'.format(selected_text)
                    temp_string += 'case_sensitive=False,'
                    temp_string += 'search_forward=True,'
                    temp_string += 'window_name="{}")'.format(focused_tab._parent.name)
                    self.repl.setText(temp_string)
                except:
                    self.repl.setText('find_and_replace("","",case_sensitive=False)')
                self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                self.repl.setFocus()
                self.repl.setCursorPosition(self.repl.text().find('",case_sensitive'))
            find_and_replace_action = create_action(
                'Find and Replace',
                settings.keyboard_shortcuts['general']['find_and_replace'],
                'Find and replace one instance of text from cursor in currently selected document',
                'tango_icons/edit-find-replace.png',
                special_find_and_replace
            )
            #Nested special function for finding and replacing one instance of text
            #in the current main window custom editor using regular expressions
            def special_regex_find_and_replace():
                try:
                    focused_tab = self.get_used_tab()
                    selected_text = focused_tab.selectedText().replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n")
                    temp_string = 'regex_find_and_replace(r"{}",r"",'.format(selected_text)
                    temp_string += 'case_sensitive=False,'
                    temp_string += 'search_forward=True,'
                    temp_string += 'window_name="{}")'.format(focused_tab._parent.name)
                    self.repl.setText(temp_string)
                except:
                    self.repl.setText('regex_find_and_replace(r"",r"",case_sensitive=False)')
                self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                self.repl.setFocus()
                self.repl.setCursorPosition(self.repl.text().find('",case_sensitive'))
            regex_find_and_replace_action = create_action(
                'Regex Find and Replace',
                settings.keyboard_shortcuts['general']['regex_find_and_replace'],
                'Find and replace one instance of text from cursor in currently selected document using Python regular expressions',
                'tango_icons/edit-find-replace-re.png',
                special_regex_find_and_replace
            )
            def special_highlight():
                try:
                    focused_tab = self.get_used_tab()
                    selected_text = focused_tab.selectedText().replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n")
                    temp_string = 'highlight("{}",'.format(selected_text)
                    temp_string += 'case_sensitive=False,'
                    temp_string += 'window_name="{}")'.format(focused_tab._parent.name)
                    self.repl.setText(temp_string)
                except:
                    self.repl.setText('highlight("",case_sensitive=False)')
                self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                self.repl.setFocus()
                self.repl.setCursorPosition(self.repl.text().find('",case_sensitive'))
            highlight_action = create_action(
                'Highlight',
                settings.keyboard_shortcuts['general']['highlight'],
                'Highlight all instances of text in currently selected document',
                'tango_icons/edit-highlight.png',
                special_highlight
            )
            def special_regex_highlight():
                try:
                    focused_tab = self.get_used_tab()
                    selected_text = focused_tab.selectedText().replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n")
                    temp_string = 'regex_highlight(r"{}",'.format(selected_text)
                    temp_string += 'case_sensitive=False,'
                    temp_string += 'window_name="{}")'.format(focused_tab._parent.name)
                    self.repl.setText(temp_string)
                except:
                    self.repl.setText('regex_highlight(r"",case_sensitive=False)')
                self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                self.repl.setFocus()
                self.repl.setCursorPosition(self.repl.text().find('",case_sensitive'))
            regex_highlight_action = create_action(
                'Regex Highlight',
                settings.keyboard_shortcuts['general']['regex_highlight'],
                'Highlight all instances of text in currently selected document using Python regular expressions',
                'tango_icons/edit-highlight-re.png',
                special_regex_highlight
            )
            def special_clear_highlights():
                try:
                    focused_tab = self.get_used_tab()
                    self.repl.setText('clear_highlights(window_name="{}")'.format(focused_tab._parent.name))
                except:
                    self.repl.setText('clear_highlights()')
                self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                self.repl.setFocus()
                self.repl.setCursorPosition(len(self.repl.text()))
            clear_highlights_action = create_action(
                'Clear Highlights',
                settings.keyboard_shortcuts['general']['clear_highlights'],
                'Clear all higlights in currently selected document',
                'tango_icons/edit-clear-highlights.png',
                special_clear_highlights
            )
            def special_replace_in_selection():
                try:
                    focused_tab = self.get_used_tab()
                    temp_string = 'replace_in_selection("","",case_sensitive=False,'
                    temp_string += 'window_name="{}")'.format(focused_tab._parent.name)
                    self.repl.setText(temp_string)
                except:
                    self.repl.setText('replace_in_selection("","",case_sensitive=False)')
                self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                self.repl.setFocus()
                self.repl.setCursorPosition(self.repl.text().find('","",case_sensitive'))
            replace_selection_action = create_action(
                'Replace In Selection',
                settings.keyboard_shortcuts['general']['replace_selection'],
                'Replace all instances of text in the selected text of the current selected document',
                'tango_icons/edit-replace-in-selection.png',
                special_replace_in_selection
            )
            def special_regex_replace_in_selection():
                try:
                    focused_tab = self.get_used_tab()
                    temp_string = 'regex_replace_in_selection(r"",r"",case_sensitive=False,'
                    temp_string += 'window_name="{}")'.format(focused_tab._parent.name)
                    self.repl.setText(temp_string)
                except:
                    self.repl.setText('regex_replace_in_selection(r"",r"",case_sensitive=False)')
                self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                self.repl.setFocus()
                self.repl.setCursorPosition(self.repl.text().find('",r"",case_sensitive'))
            temp_string = 'Replace all instances of text in the '
            temp_string += 'selected text of the current selected document'
            temp_string += 'using Python regular expressions'
            regex_replace_selection_action = create_action(
                'Regex Replace In Selection',
                settings.keyboard_shortcuts['general']['regex_replace_selection'],
                temp_string,
                'tango_icons/edit-replace-in-selection-re.png',
                special_regex_replace_in_selection
            )
            #Nested special function for replacing all instances of text in
            #the selected custom editor
            def special_replace_all():
                try:
                    focused_tab = self.get_used_tab()
                    selected_text = focused_tab.selectedText().replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n")
                    temp_string = 'replace_all("{}","",'.format(selected_text)
                    temp_string += 'case_sensitive=False,'
                    temp_string += 'window_name="{}")'.format(focused_tab._parent.name)
                    self.repl.setText(temp_string)
                except:
                    self.repl.setText('replace_all("","",case_sensitive=False)')
                self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                self.repl.setFocus()
                self.repl.setCursorPosition(self.repl.text().find('",case_sensitive'))
            replace_all_action = create_action(
                'Replace All',
                settings.keyboard_shortcuts['general']['replace_all'],
                'Replace all instances of text in currently selected document',
                'tango_icons/edit-replace-all.png',
                special_replace_all
            )
            #Nested special function for replacing all instances of text in
            #the selected custom editor using regular expressions
            def special_regex_replace_all():
                try:
                    focused_tab = self.get_used_tab()
                    selected_text = focused_tab.selectedText().replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n")
                    temp_string = 'regex_replace_all(r"{}",r"",'.format(selected_text)
                    temp_string += 'case_sensitive=False,'
                    temp_string += 'window_name="{}")'.format(focused_tab._parent.name)
                    self.repl.setText(temp_string)
                except:
                    self.repl.setText('regex_replace_all(r"",r"",case_sensitive=False)')
                self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                self.repl.setFocus()
                self.repl.setCursorPosition(self.repl.text().find('",case_sensitive'))
            regex_replace_all_action = create_action(
                'Regex Replace All',
                settings.keyboard_shortcuts['general']['regex_replace_all'],
                'Replace all instances of text in currently selected document using Python regular expressions',
                'tango_icons/edit-replace-all-re.png',
                special_regex_replace_all
            )
            #Nested special function for un/commenting selected lines in the main widget
            def comment_uncomment():
                try:
                    self.get_tab_by_focus().toggle_comment_uncomment()
                except:
                    traceback.print_exc()
            toggle_comment_action = create_action(
                'Comment/Uncomment',
                settings.keyboard_shortcuts['general']['toggle_comment'],
                'Toggle comments for the selected lines or single line in the currently selected document',
                'tango_icons/edit-comment-uncomment.png',
                comment_uncomment
            )
            def toggle_autocompletions():
                try:
                    self.get_tab_by_focus().toggle_autocompletions()
                except:
                    traceback.print_exc()
            toggle_autocompletion_action = create_action(
                'Enable/Disable Autocompletion',
                settings.keyboard_shortcuts['general']['toggle_autocompletion'],
                'Enable/Disable autocompletions for the currently selected document',
                'tango_icons/edit-autocompletion.png',
                toggle_autocompletions
            )
            def toggle_wordwrap():
                try:
                    self.get_tab_by_focus().toggle_wordwrap()
                except:
                    traceback.print_exc()
            toggle_wrap_action = create_action(
                'Enable/Disable Line Wrapping',
                settings.keyboard_shortcuts['general']['toggle_wrap'],
                'Enable/Disable line wrapping for the currently selected document',
                'tango_icons/wordwrap.png',
                toggle_wordwrap
            )
            def reload_file():
                try:
                    self.get_tab_by_focus().reload_file()
                except:
                    traceback.print_exc()
            reload_file_action = create_action(
                'Reload file',
                settings.keyboard_shortcuts['general']['reload_file'],
                'Reload file from disk, will prompt if file contains changes',
                'tango_icons/view-refresh.png',
                reload_file
            )
            def create_node_tree():
                mw = self.get_tab_by_focus()
                if isinstance(mw, CustomEditor):
                    self.display.show_nodes(mw, mw.current_file_type)
                else:
                    message = "No document opened in the selected window or\n"
                    message += "the document is not an editor!"
                    self.display.repl_display_message(
                        message,
                        message_type=data.MessageType.ERROR
                    )
            node_tree_action = create_action(
                'Create/reload node tree (C / Nim / Python3)',
                settings.keyboard_shortcuts['general']['node_tree'],
                'Create a node tree for the code for the currently selected document (C / Nim / Python3)',
                'tango_icons/edit-node-tree.png',
                create_node_tree
            )
            def special_goto_line():
                try:
                    focused_tab = self.get_used_tab()
                    self.repl.setText('goto_line(,window_name="{}")'.format(focused_tab._parent.name))
                    self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                    self.repl.setCursorPosition(self.repl.text().find(',window_name'))
                except:
                    self.repl.setText('goto_line()')
                    self.repl.setCursorPosition(len(self.repl.text())-1)
                self.repl.setFocus()
            goto_line_action = create_action(
                'Goto line',
                settings.keyboard_shortcuts['general']['goto_line'],
                'Go to the specified line in the current main window document',
                'tango_icons/edit-goto.png',
                special_goto_line
            )
            def special_indent_to_cursor():
                try:
                    self.get_tab_by_focus().indent_lines_to_cursor()
                except:
                    self.display.repl_display_error(traceback.format_exc())
            temp_string = 'Indent the selected lines to the current cursor position '
            temp_string += '(SPACE ON THE LEFT SIDE OF LINES IS STRIPPED!)'
            indent_to_cursor_action = create_action(
                'Indent to cursor',
                settings.keyboard_shortcuts['general']['indent_to_cursor'],
                temp_string,
                'tango_icons/edit-indent-to-cursor.png',
                special_indent_to_cursor
            )
            def special_to_uppercase():
                focused_tab = self.get_used_tab()
                self.editing.convert_to_uppercase(focused_tab._parent.name)
            to_uppercase_action = create_action(
                'Selection to UPPERCASE',
                settings.keyboard_shortcuts['general']['to_uppercase'],
                'Convert selected text to UPPERCASE',
                'tango_icons/edit-case-to-upper.png',
                special_to_uppercase
            )
            def special_to_lowercase():
                focused_tab = self.get_used_tab()
                self.editing.convert_to_lowercase(focused_tab._parent.name)
            to_lowercase_action = create_action(
                'Selection to lowercase',
                settings.keyboard_shortcuts['general']['to_lowercase'],
                'Convert selected text to lowercase',
                'tango_icons/edit-case-to-lower.png',
                special_to_lowercase
            )
            #Nested function for finding files in open documents
            def special_find_in_open_documents():
                try:
                    focused_tab = self.get_used_tab()
                    selected_text = focused_tab.selectedText().replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n")
                    repl_text = 'find_in_open_documents("{}"'.format(selected_text)
                    repl_text += ",case_sensitive=False,regular_expression=False"
                    repl_text += ',window_name="{}")'.format(focused_tab._parent.name)
                    self.repl.setText(repl_text)
                except:
                    self.repl.setText('find_in_open_documents("",case_sensitive=False,regular_expression=False)')
                self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                self.repl.setCursorPosition(self.repl.text().find('",case_sensitive'))
                self.repl.setFocus()
            find_in_documents_action = create_action(
                'Find in open documents',
                settings.keyboard_shortcuts['general']['find_in_documents'],
                temp_string,
                'tango_icons/edit-find-in-open-documents.png',
                special_find_in_open_documents
            )
            #Nested function for finding and replacing text in open documents
            def special_find_replace_in_open_documents():
                try:
                    focused_tab = self.get_used_tab()
                    selected_text = focused_tab.selectedText().replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n")
                    repl_text = 'find_replace_in_open_documents("{}",""'.format(selected_text)
                    repl_text += ",case_sensitive=False,regular_expression=False"
                    repl_text += ',window_name="{}")'.format(focused_tab._parent.name)
                    self.repl.setText(repl_text)
                except:
                    self.repl.setText('find_replace_in_open_documents("","",case_sensitive=False,regular_expression=False)')
                self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                self.repl.setCursorPosition(self.repl.text().find('",case_sensitive'))
                self.repl.setFocus()
            find_replace_in_documents_action = create_action(
                'Find and replace in open documents',
                settings.keyboard_shortcuts['general']['find_replace_in_documents'],
                temp_string,
                'tango_icons/edit-replace-in-open-documents.png',
                special_find_replace_in_open_documents
            )
            #Nested function for replacing all string instances in open documents
            def special_replace_all_in_open_documents():
                try:
                    focused_tab = self.get_used_tab()
                    selected_text = focused_tab.selectedText().replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n")
                    repl_text = 'replace_all_in_open_documents("{}",""'.format(selected_text)
                    repl_text += ",case_sensitive=False,regular_expression=False"
                    repl_text += ',window_name="{}")'.format(focused_tab._parent.name)
                    self.repl.setText(repl_text)
                except:
                    self.repl.setText('replace_all_in_open_documents("","",case_sensitive=False,regular_expression=False)')
                self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                self.repl.setCursorPosition(self.repl.text().find('",case_sensitive'))
                self.repl.setFocus()
            replace_all_in_documents_action = create_action(
                'Replace all in open documents',
                settings.keyboard_shortcuts['general']['replace_all_in_documents'],
                'Replace all instances of search text across all open documents in the currently selected window',
                'tango_icons/edit-replace-all-in-open-documents.png',
                special_replace_all_in_open_documents
            )
            reset_context_menu_action = create_action(
                'Reset context menus',
                None,
                'Reset functions of ALL context menus (right-click menus)',
                'tango_icons/reset-context-menu.png',
                ContextMenu.reset_functions
            )
            # Open in browser
            def open_in_browser(*args):
                try:
                    focused_tab = self.get_used_tab()
                    selected_text = focused_tab.selectedText()
                    functions.open_url(selected_text)
                except:
                    message = "Cannot open selected editor text in the system's web-browser!"
                    self.display.repl_display_error(message)
            open_in_browser_action = create_action(
                'Open in browser',
                None,
                'Open selected editor text in the systems web-browser',
                'tango_icons/gnome-web-browser.png',
                open_in_browser,
            )
            #Adding the edit menu and constructing all of the options
            edit_menu.addAction(find_action)
            edit_menu.addAction(regex_find_action)
            edit_menu.addAction(find_and_replace_action)
            edit_menu.addAction(regex_find_and_replace_action)
            edit_menu.addAction(goto_line_action)
            edit_menu.addAction(indent_to_cursor_action)
            edit_menu.addAction(highlight_action)
            edit_menu.addAction(regex_highlight_action)
            edit_menu.addAction(clear_highlights_action)
            edit_menu.addAction(replace_selection_action)
            edit_menu.addAction(regex_replace_selection_action)
            edit_menu.addAction(replace_all_action)
            edit_menu.addAction(regex_replace_all_action)
            edit_menu.addAction(toggle_comment_action)
            edit_menu.addAction(toggle_autocompletion_action)
            edit_menu.addAction(toggle_wrap_action)
            edit_menu.addAction(to_uppercase_action)
            edit_menu.addAction(to_lowercase_action)
            edit_menu.addAction(node_tree_action)
            edit_menu.addAction(reload_file_action)
            edit_menu.addAction(open_in_browser_action)
            edit_menu.addAction(reset_context_menu_action)
            edit_menu.addSeparator()
            edit_menu.addAction(find_in_documents_action)
            edit_menu.addAction(find_replace_in_documents_action)
            edit_menu.addAction(replace_all_in_documents_action)
        #System menu
        def construct_system_menu():
            system_menu = Menu("S&ystem", self.menubar)
            self.menubar.addMenu(system_menu)
            system_menu.installEventFilter(click_filter)
            def special_find_in():
                #The second argument is raw, so that single backslashes work for windows paths
                self.repl.setText('find_in_files("",r"directory",case_sensitive=False,search_subdirs=True,break_on_find=False,file_filter=None)')
                self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                self.repl.setFocus()
                self.repl.setSelection(self.repl.text().index("directory"), len("directory"))
            def special_find_in_with_dialog():
                #The second argument is raw, so that single backslashes work for windows paths
                self.repl.setText('find_in_files("",case_sensitive=False,search_subdirs=True,break_on_find=False,file_filter=None)')
                self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                self.repl.setFocus()
                self.repl.setCursorPosition(self.repl.text().find('",case_sensitive'))
            self.menubar_functions["special_find_in_with_dialog"] = special_find_in_with_dialog
            temp_string = 'Find all the files in a directory/subdirectories '
            temp_string += 'that contain the search string'
            find_in_files_action = create_action(
                'Find in files',
                settings.keyboard_shortcuts['general']['find_in_files'],
                temp_string,
                'tango_icons/system-find-in-files.png',
                special_find_in
            )
            def special_find_file():
                #The second argument is raw, so that single backslashes work for windows paths
                self.repl.setText('find_files("",r"directory",case_sensitive=False,search_subdirs=True)')
                self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                self.repl.setFocus()
                self.repl.setSelection(self.repl.text().index("directory"), len("directory"))
            def special_find_file_with_dialog():
                #The second argument is raw, so that single backslashes work for windows paths
                self.repl.setText('find_files("",case_sensitive=False,search_subdirs=True)')
                self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                self.repl.setFocus()
                self.repl.setCursorPosition(self.repl.text().find('",case_sensitive'))
            self.menubar_functions["special_find_file_with_dialog"] = special_find_file_with_dialog
            temp_string = 'Find all the files in a directory/subdirectories '
            temp_string += 'that have the search string in them'
            find_files_action = create_action(
                'Find files',
                settings.keyboard_shortcuts['general']['find_files'],
                temp_string,
                'tango_icons/system-find-files.png',
                special_find_file
            )
            def special_replace_in_files():
                #The second argument is raw, so that single backslashes work for windows paths
                temp_string = 'replace_in_files("search_text","replace_text",'
                temp_string += 'r"directory",case_sensitive=False,search_subdirs=True,file_filter=None)'
                self.repl.setText(temp_string)
                self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                self.repl.setFocus()
                self.repl.setSelection(self.repl.text().index("directory"), len("directory"))
            def special_replace_in_files_with_dialog():
                #The second argument is raw, so that single backslashes work for windows paths
                temp_string = 'replace_in_files("search_text","replace_text",'
                temp_string += 'case_sensitive=False,search_subdirs=True,file_filter=None)'
                self.repl.setText(temp_string)
                self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                self.repl.setFocus()
                self.repl.setCursorPosition(self.repl.text().find('",case_sensitive'))
            self.menubar_functions["special_replace_in_files_with_dialog"] = special_replace_in_files_with_dialog
            temp_string = 'Find all the files in a directory/subdirectories '
            temp_string += 'that have the search string in them and replace all '
            temp_string += 'instances in the file with the replace string'
            replace_in_files_action = create_action(
                'Replace in files',
                settings.keyboard_shortcuts['general']['replace_in_files'],
                temp_string,
                'tango_icons/system-replace-in-files.png',
                special_replace_in_files
            )
            def special_run_command():
                self.repl.setText('run("",show_console=True)')
                self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                self.repl.setFocus()
                self.repl.setCursorPosition(self.repl.text().find('",show_'))
            run_command_action = create_action(
                'Run command',
                None,
                'Run command as a new process (FULLY TESTED ONLY ON WINDOWS!)',
                'tango_icons/utilities-terminal.png',
                special_run_command
            )
            def create_cwd_tree():
                self.display.show_directory_tree(os.getcwd())
            cwd_tree_action = create_action(
                'Show current working directory tree',
                settings.keyboard_shortcuts['general']['cwd_tree'],
                'Create a node tree for the current working directory (CWD)',
                'tango_icons/system-show-cwd-tree.png',
                create_cwd_tree
            )
            def show_explorer():
                self.system.show_explorer()
            show_explorer_action = create_action(
                'Show current working directory explorer',
                settings.keyboard_shortcuts['general']['cwd_explorer'],
                'Show the current working directory in the systems explorer',
                'tango_icons/system-show-cwd.png',
                show_explorer
            )
            def show_terminal():
                self.repl.interpreter.create_terminal()
            show_terminal_action = create_action(
                'Show Console/Terminal window',
                None,
                'Show a Console(Windows) / Terminal(Linux) ' +
                    'window at the current working directory',
                'tango_icons/utilities-terminal.png',
                show_terminal
            )
            def open_general_explorer():
                file_explorer = self.get_helper_window().tree_add_tab(
                    data.file_explorer_tab_name, TreeExplorer
                )
                file_explorer.display_directory(os.getcwd())
                file_explorer.open_file_signal.connect(self.open_file)
                file_explorer.open_file_hex_signal.connect(self.open_file_hex)
                file_explorer.internals.set_icon(
                    file_explorer,
                    functions.create_icon(
                        'tango_icons/system-show-cwd-tree-blue.png'
                    )
                )
                self.get_helper_window().setCurrentWidget(file_explorer)
            show_new_explorer_tree_action = create_action(
                'Show current working directory in tree explorer',
                settings.keyboard_shortcuts['general']['new_cwd_tree'],
                'Show the current working directory in the tree explorer',
                'tango_icons/system-show-cwd-tree-blue.png',
                open_general_explorer
            )
            # Add the menu items
            system_menu.addAction(find_files_action)
            system_menu.addAction(find_in_files_action)
            system_menu.addAction(replace_in_files_action)
            system_menu.addSeparator()
            system_menu.addAction(cwd_tree_action)
            system_menu.addAction(show_new_explorer_tree_action)
            system_menu.addAction(show_explorer_action)
            system_menu.addSeparator()
            system_menu.addAction(run_command_action)
            system_menu.addAction(show_terminal_action)
        #Lexers menu
        def construct_lexers_menu(parent):
            def set_lexer(lexer, lexer_name):
                try:
                    #Get the focused tab and reset the lexer
                    focused_tab = self.get_tab_by_focus()
                    focused_tab.clear_lexer()
                    #Initialize and set the new lexer
                    lexer_instance = lexer()
                    focused_tab.set_lexer(lexer_instance, lexer_name)
                    #Display the lexer change
                    message = "Lexer changed to: {}".format(lexer_name)
                    self.display.repl_display_message(message)
                except Exception as ex:
                    message = "Error with lexer selection!\n"
                    message += "Select a window widget with an opened document first."
                    self.display.repl_display_message(
                        message,
                        message_type=data.MessageType.ERROR
                    )
                    self.display.write_to_statusbar(message)
            lexers_menu = self.display.create_lexers_menu(
                "Change lexer",
                set_lexer,
                store_menu_to_mainform=False,
                custom_parent=parent
            )
            lexers_menu.installEventFilter(click_filter)
            temp_icon = functions.create_icon('tango_icons/lexers.png')
            lexers_menu.setIcon(temp_icon)
            parent.addMenu(lexers_menu)
        #View menu
        def construct_view_menu():
            view_menu = Menu("&View", self.menubar)
            self.menubar.addMenu(view_menu)
            view_menu.installEventFilter(click_filter)
            #Show/hide the function wheel
            function_wheel_toggle_action = create_action(
                'Show/Hide Function Wheel',
                settings.keyboard_shortcuts['general']['function_wheel_toggle'],
                'Show/hide the Ex.Co. function wheel',
                data.application_icon,
                self.view.toggle_function_wheel
            )
            #Maximize/minimize entire Ex.Co. window
            maximize_window_action = create_action(
                'Maximize/Normalize',
                settings.keyboard_shortcuts['general']['maximize_window'],
                'Maximize/Normalize application window',
                'tango_icons/view-fullscreen.png',
                self.view.toggle_window_size
            )

            def focus_main_window():
                window = self.get_largest_window()
                self.view.set_window_focus(window)
            main_focus_action = create_action(
                'Focus Largest window',
                settings.keyboard_shortcuts['general']['main_focus'],
                'Set focus to the largest window',
                'tango_icons/view-focus-main.png',
                focus_main_window
            )
            def focus_upper_window():
                window = self.get_helper_window()
                self.view.set_window_focus(window)
            upper_focus_action = create_action(
                'Focus helper window',
                settings.keyboard_shortcuts['general']['upper_focus'],
                'Set focus to the helper window',
                'tango_icons/view-focus-upper.png',
                focus_upper_window
            )
            def focus_lower_window():
                window = self.get_repl_window()
                self.view.set_window_focus(window)
            lower_focus_action = create_action(
                'Focus messages window',
                settings.keyboard_shortcuts['general']['lower_focus'],
                'Set focus to the messages window',
                'tango_icons/view-focus-lower.png',
                focus_lower_window
            )

            def toggle_one_window_mode():
                self.view.toggle_one_window_mode()
            toggle_one_window_mode_action = create_action(
                'One window mode toggle',
                settings.keyboard_shortcuts['general']['toggle_mode'],
                'Toggle between one-window and stored layout',
                'tango_icons/view-toggle-window-mode.png',
                toggle_one_window_mode
            )

            def select_tab_right():
                try:
                    self.get_window_by_child_tab().select_tab(data.Direction.RIGHT)
                except:
                    self.display.repl_display_error(traceback.format_exc())
            select_tab_right_action = create_action(
                'Select tab right',
                settings.keyboard_shortcuts['general']['select_tab_right'],
                'Select one tab to the right in the currently selected window',
                'tango_icons/view-select-tab-right.png',
                select_tab_right
            )
            def select_tab_left():
                try:
                    self.get_window_by_child_tab().select_tab(data.Direction.LEFT)
                except:
                    self.display.repl_display_error(traceback.format_exc())
            select_tab_left_action = create_action(
                'Select tab left',
                settings.keyboard_shortcuts['general']['select_tab_left'],
                'Select one tab to the left in the currently selected window',
                'tango_icons/view-select-tab-left.png',
                select_tab_left
            )
            def move_tab_right():
                try:
                    self.get_window_by_child_tab().move_tab(data.Direction.RIGHT)
                except:
                    self.display.repl_display_error(traceback.format_exc())
            move_tab_right_action = create_action(
                'Move tab right',
                settings.keyboard_shortcuts['general']['move_tab_right'],
                'Move the current tab in the currently selected window one position to the right',
                'tango_icons/view-move-tab-right.png',
                move_tab_right
            )
            def move_tab_left():
                try:
                    self.get_window_by_child_tab().move_tab(data.Direction.LEFT)
                except:
                    self.display.repl_display_error(traceback.format_exc())
            move_tab_left_action = create_action(
                'Move tab left',
                settings.keyboard_shortcuts['general']['move_tab_left'],
                'Move the current tab in the currently selected window one position to the left',
                'tango_icons/view-move-tab-left.png',
                move_tab_left
            )
            def show_edge():
                try:
                    self.get_tab_by_focus().edge_marker_toggle()
                except:
                    self.display.repl_display_error(traceback.format_exc())
            toggle_edge_action = create_action(
                'Toggle edge marker',
                settings.keyboard_shortcuts['general']['toggle_edge'],
                'Toggle the display of the edge marker that shows the prefered maximum chars in a line',
                'tango_icons/view-edge-marker.png',
                show_edge
            )
            def reset_zoom():
                try:
                    self.get_tab_by_focus()._parent.zoom_reset()
                except:
                    self.display.repl_display_error(traceback.format_exc())
            reset_zoom_action = create_action(
                'Zoom reset',
                settings.keyboard_shortcuts['general']['reset_zoom'],
                'Reset the zoom level on the currently focused document',
                'tango_icons/view-zoom-reset.png',
                reset_zoom
            )
            #Bookmarks
            def bookmark_goto(number):
                self.bookmarks.goto(number)
            self.menubar_functions["bookmark_goto"] = bookmark_goto
            def bookmark_store(number):
                try:
                    current_tab = self.get_tab_by_focus()
                    current_line = current_tab.getCursorPosition()[0] + 1
                    self.bookmarks.add_mark_by_number(
                        current_tab,
                        current_line,
                        number
                    )
                except:
                    self.display.repl_display_error(traceback.format_exc())
            def bookmark_toggle():
                try:
                    self.get_tab_by_focus().bookmarks.toggle()
                except:
                    self.display.repl_display_error(traceback.format_exc())
            bookmark_menu = Menu("&Bookmarks", self.menubar)
            view_menu.addMenu(bookmark_menu)
            bookmark_menu.installEventFilter(click_filter)
            temp_icon = functions.create_icon('tango_icons/bookmarks.png')
            bookmark_menu.setIcon(temp_icon)
            bookmark_toggle_action = create_action(
                'Toggle Bookmark',
                settings.keyboard_shortcuts['general']['bookmark_toggle'],
                'Toggle a bookmark at the current document line',
                'tango_icons/bookmark.png',
                bookmark_toggle
            )
            bookmark_menu.addAction(bookmark_toggle_action)
            def bookmarks_clear():
                self.bookmarks.clear()
            bookmark_clear_action = create_action(
                'Clear Bookmarks',
                None,
                'Clear Bookmarks',
                'tango_icons/bookmarks-clear.png',
                bookmarks_clear
            )
            bookmark_menu.addAction(bookmark_clear_action)
            bookmark_menu.addSeparator()
            bookmark_goto_menu = Menu("Go To", self.menubar)
            bookmark_menu.addMenu(bookmark_goto_menu)
            bookmark_goto_menu.installEventFilter(click_filter)
            temp_icon = functions.create_icon('tango_icons/bookmarks-goto.png')
            bookmark_goto_menu.setIcon(temp_icon)
            bookmark_store_menu = Menu("Store", self.menubar)
            bookmark_menu.addMenu(bookmark_store_menu)
            bookmark_store_menu.installEventFilter(click_filter)
            temp_icon = functions.create_icon('tango_icons/bookmarks-store.png')
            bookmark_store_menu.setIcon(temp_icon)
            self.bookmark_menu = bookmark_menu
            for i in range(10):
                #Go To
                def create_goto_bookmark():
                    func = functools.partial(bookmark_goto, i)
                    func.__name__ = "bookmark_goto_{}".format(i)
                    return func
                bookmark_goto_action = create_action(
                    'Bookmark Goto {:d}'.format(i),
                    settings.keyboard_shortcuts['general']['bookmark_goto'][i],
                    "Go to bookmark number:{:d}".format(i),
                    'tango_icons/bookmarks-goto.png',
                    create_goto_bookmark()
                )
                bookmark_goto_menu.addAction(bookmark_goto_action)
                #Store
                def create_store_bookmark():
                    func = functools.partial(bookmark_store, i)
#                    func.__name__ = "store_bookmark_{}".format(i)
                    func.__name__ = "bookmark_store_{}".format(i)
                    return func
                bookmark_store_action = create_action(
                    'Bookmark Store {:d}'.format(i),
                    settings.keyboard_shortcuts['general']['bookmark_store'][i],
                    "Store bookmark number:{:d}".format(i),
                    'tango_icons/bookmarks-store.png',
                    create_store_bookmark()
                )
                bookmark_store_menu.addAction(bookmark_store_action)
            def toggle_line_endings():
                try:
                    self.get_tab_by_focus().toggle_line_endings()
                except:
                    self.display.repl_display_error(traceback.format_exc())
            temp_string = 'Toggle the visibility of the End-Of-Line characters '
            temp_string += 'for the currently selected document'
            toggle_lineend_action = create_action(
                'Toggle EOL visibility',
                None,
                temp_string,
                'tango_icons/view-line-end.png',
                toggle_line_endings
            )
            def toggle_cursor_line_highlighting():
                try:
                    self.get_tab_by_focus().toggle_cursor_line_highlighting()
                except:
                    traceback.print_exc()
                    self.display.repl_display_error(traceback.format_exc())
            temp_string = 'Toggle the visibility of the line that the cursor is'
            temp_string += ' on for the currently selected document'
            toggle_cursor_line_action = create_action(
                'Toggle cursor line visibility',
                None,
                temp_string,
                'tango_icons/edit-show-cursor-line.png',
                toggle_cursor_line_highlighting
            )
            #Add all actions and menus
            view_menu.addAction(function_wheel_toggle_action)
            view_menu.addSeparator()
            view_menu.addMenu(bookmark_menu)
            view_menu.addSeparator()
            construct_lexers_menu(view_menu)
            view_menu.addSeparator()
            view_menu.addAction(main_focus_action)
            view_menu.addAction(upper_focus_action)
            view_menu.addAction(lower_focus_action)
            view_menu.addAction(toggle_one_window_mode_action)
            view_menu.addAction(maximize_window_action)
            view_menu.addAction(select_tab_right_action)
            view_menu.addAction(select_tab_left_action)
            view_menu.addAction(move_tab_right_action)
            view_menu.addAction(move_tab_left_action)
            view_menu.addAction(toggle_edge_action)
            view_menu.addAction(reset_zoom_action)
            view_menu.addAction(toggle_lineend_action)
            view_menu.addAction(toggle_cursor_line_action)
        #REPL menu
        def construct_repl_menu():
            repl_menu = Menu("&REPL", self.menubar)
            self.menubar.addMenu(repl_menu)
            repl_menu.installEventFilter(click_filter)
            repeat_eval_action = create_action(
                'REPL Repeat Command',
                settings.keyboard_shortcuts['general']['repeat_eval'],
                'Repeat the last REPL command',
                'tango_icons/repl-repeat-command.png',
                self.repl.repeat_last_repl_eval
            )
            def repl_single_focus():
                self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                self.repl.setFocus()
            repl_focus_action = create_action(
                'Focus REPL(Single)',
                [settings.keyboard_shortcuts['general']['repl_focus_single_1'], settings.keyboard_shortcuts['general']['repl_focus_single_2']],
                'Set focus to the Python REPL(Single Line)',
                'tango_icons/repl-focus-single.png',
                repl_single_focus
            )
            def repl_multi_focus():
                self.view.set_repl_type(data.ReplType.MULTI_LINE)
                self.repl_helper.setFocus()
            repl_focus_multi_action = create_action(
                'Focus REPL(Multi)',
                settings.keyboard_shortcuts['general']['repl_focus_multi'],
                'Set focus to the Python REPL(Multi Line)',
                'tango_icons/repl-focus-multi.png',
                repl_multi_focus
            )
            repl_menu.addAction(repeat_eval_action)
            repl_menu.addAction(repl_focus_action)
            repl_menu.addAction(repl_focus_multi_action)
        #Sessions menu
        def construct_sessions_menu():
            sessions_menu = Menu("Sessions", self.menubar)
            self.menubar.addMenu(sessions_menu)
            sessions_menu.installEventFilter(click_filter)
            def add_session():
                repl_text_input(text='session_add("", session_group=None)', cursor_position=13)
            add_session_action = create_action(
                'Add Session',
                None,
                'Save the currently opened documents to a session',
                'tango_icons/session-add.png',
                add_session
            )
            def remove_session():
                repl_text_input(text='session_remove("", session_group=None)', cursor_position=13)
            remove_session_action = create_action(
                'Remove Session',
                None,
                'Remove the session with matching name and group',
                'tango_icons/session-remove.png',
                remove_session
            )
            session_editor_action = create_action(
                'Graphical Session Editor',
                None,
                'Graphical user friendly session editor',
                'tango_icons/sessions-gui.png',
                self.display.show_session_editor
            )
            #Sessions menu
            self.sessions_menu = Menu("Sessions", self.menubar)
            self.sessions_menu.setIcon(functions.create_icon('tango_icons/sessions.png'))
            sessions_menu.addAction(add_session_action)
            sessions_menu.addAction(remove_session_action)
            sessions_menu.addAction(session_editor_action)
            sessions_menu.addSeparator()
            sessions_menu.addMenu(self.sessions_menu)
        # Settings menu
        def construct_settings_menu():
            settings_menu = Menu("Settings", self.menubar)
            self.menubar.addMenu(settings_menu)
            settings_menu.installEventFilter(click_filter)
            def show_settings():
                self.view.show_settings_gui_manipulator()
            show_gui_action = create_action(
                'Graphical Settings Editor',
                None,
                'Graphical user friendly settings editor',
                'tango_icons/settings-png',
                show_settings
            )
            # Add the items
            settings_menu.addAction(show_gui_action)
        #Help menu
        def construct_help_menu():
            help_menu = Menu("&Help", self.menubar)
            self.menubar.addMenu(help_menu)
            help_menu.installEventFilter(click_filter)
            self.fm = help_menu
            about_action = create_action(
                'About Ex.Co.',
                None,
                'Ex.Co. Information',
                'tango_icons/help-browser.png',
                self.view.show_about
            )
            help_menu.addAction(about_action)
        #Execute the nested construction functions
        construct_file_menu()
        construct_edit_basic_menu()
        construct_edit_advanced_menu()
        construct_system_menu()
        construct_view_menu()
        construct_repl_menu()
        construct_sessions_menu()
#        construct_settings_menu()
        construct_help_menu()
        #Connect the triggered signal for hiding the function wheel on menubar clicks
        def hide_fw(action):
            #Hide the function wheel only when the clicked action is not "Show/Hide Function Wheel"
            if isinstance(action, data.QAction):
                if action.text() != "Show/Hide Function Wheel":
                    #Hide the function wheel if it is shown
                    self.view.hide_function_wheel()
        self.menubar.triggered.connect(hide_fw)
        #Add the menubar to the MainWindow
        self.setMenuBar(self.menubar)

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
        new_references, ac_list_prim, ac_list_sec = self.get_references_autocompletions()
        #Initialize and set auto completer for the REPL
        self.repl.interpreter_update_references(new_references, ac_list_prim, ac_list_sec)
        #Initialize the autocompletions for the REPL helper
        merged_autocompletions = [word for word in new_references]
        merged_autocompletions.extend(ac_list_prim)
        self.repl_helper.update_autocompletions(merged_autocompletions)
        #Import the user functions
        self.import_user_functions()

    def import_user_functions(self):
        """Import the user defined functions form the userfunctions.cfg file"""
        self.repl.skip_next_repl_focus()
        user_file_path = os.path.join(data.application_directory, data.config_file)
        # Test if userfunctions file exists
        if os.path.isfile(user_file_path) == False:
            message = "User functions file does not exist!\n"
            message += "Create an empty file named '{}' ".format(data.config_file)
            message += "in the application directory\n"
            message += "to make this error dissappear."
            self.display.repl_display_message(
                message,
                message_type=data.MessageType.ERROR
            )
            message = "Do you wish to generate the default user definition and function file?"
            reply = YesNoDialog.question(message)
            if reply == data.DialogResult.Yes.value:
                functions.create_default_config_file()
                self.display.repl_display_success(
                    "Default user definitions file generated!"
                )
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
                "if callable(first_scan):\n    first_scan();",
                display_action=False
            )
        try:
            # Update the REPL autocompletions
            import_nodes, class_tree_nodes, function_nodes, global_vars = functions.get_python_node_list(user_code)
            # First get the function names
            user_function_names = [func.name for func in function_nodes]
            # Then get the autocompletions by testing if the function has
            # the "autocompletion" attribute. Because in Python everything is an object,
            # functions can also have attributes! Very nice!
            user_function_autocompletions = []
            for func_name in user_function_names:
                """User functions are stored in the REPL's intepreter 'locals' dictionary"""
                function = self.repl.interpreter.__dict__['locals'][func_name]
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
        new_references, ac_list_prim, ac_list_sec = self.get_references_autocompletions()
        # Initialize and set auto completer
        self.repl.interpreter_reset_references(new_references, ac_list_prim, ac_list_sec)
        # Reimport the user functions
        self.import_user_functions()
        # Display interpreter reset success
        self.display.write_to_statusbar("REPL interpreter references successfully updated", 2000)

    def create_new(self, tab_name=None, tab_widget=None):
        """Creates an empty scintilla document using a generator counter"""
        #Set the new tab name
        if tab_name is None:
            tab_name = "new_" + str(next(self.new_file_count))
        #Create the new scintilla document in the selected basic widget
        return_widget = None
        if tab_widget is None:
            return_widget = self.get_largest_window().editor_add_document(tab_name, type="new")
        else:
            return_widget = tab_widget.editor_add_document(tab_name, type="new")
        #Set focus to the new widget
        return_widget.setFocus()
        #Return the widget reference
        return return_widget

    def open_file_with_dialog(self, tab_widget=None):
        """Open a file for editing using a file dialog"""
        #Create and show a file dialog window, restore last browsed directory and set the file filter
        file_dialog = data.QFileDialog
        files = file_dialog.getOpenFileNames(
            self,
            "Open File",
            os.getcwd(),
            "All Files (*);;Ex.Co. Files({})".format(' '.join(self.exco_file_exts))
        )
        if data.PYQT_MODE == 5:
            # PyQt5's getOpenFileNames returns a tuple (files_list, selected_filter),
            # so pass only the files to the function
            files = files[0]
        # Check and then add the selected file to the main TabWidget if the window parameter is unspecified
        self.open_files(files, tab_widget)

    def open_files(self, files=None, tab_widget=None):
        """Cheach and read valid files to the selected TabWidget"""
        #Check if the files are valid
        if files is None or files == "":
            return
        if isinstance(files,  str):
            #Single file
            self.open_file(files, tab_widget)
        else:
            #List of files
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
                    message_type=data.MessageType.ERROR
                )
                return
            # Check the file size
            file_size = functions.get_file_size_Mb(in_file)
            if file_size  > 50:
                #Create the warning message
                warning =   "The file is larger than 50 MB! ({:d} MB)\n".format(int(file_size))
                warning +=  "A lot of RAM will be needed!\n"
                warning +=  "Files larger than 300 MB can cause the system to hang!\n"
                warning +=  "Are you sure you want to open it?"
                reply = YesNoDialog.warning(warning)
                if reply == data.DialogResult.No.value:
                    return
            # Check if file is already open
            check_tab_widget, check_index = self.check_open_file(in_file)
            if check_index is not None and check_tab_widget is not None:
                check_tab_widget.setCurrentIndex(check_index)
                return

            if tab_widget is None:
                tab_widget = self.get_largest_window()

            # Add new scintilla document tab to the basic widget
            new_tab = tab_widget.editor_add_document(in_file, "file", bypass_check=False)
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
                        message = "CAUTION: NULL ('\\0') characters in file:\n'{}'".format(in_file)
                        self.display.repl_display_message(
                            message, message_type=data.MessageType.WARNING
                        )
                    else:
                        new_tab.setText(file_text)
                    # Save the layout if needed
                    if save_layout == True:
                        self.view.layout_save()
                except MemoryError:
                    message = "Insufficient memory to open the file!"
                    self.display.repl_display_message(message, message_type=data.MessageType.ERROR)
                    self.display.write_to_statusbar(message)
                    tab_widget.widget(tab_widget.currentIndex()).setParent(None)
                    tab_widget.removeTab(tab_widget.currentIndex())
                    return None
                except:
                    message = "Unexpected error occured while opening file!"
                    self.display.repl_display_message(message, message_type=data.MessageType.ERROR)
                    self.display.write_to_statusbar(message)
                    tab_widget.widget(tab_widget.currentIndex()).setParent(None)
                    tab_widget.removeTab(tab_widget.currentIndex())
                    return None
                #Reset the changed status of the current tab,
                #because adding the file content line by line was registered as a text change
                tab_widget.reset_text_changed()
                #Update the settings manipulator with the new file
                self.settings.update_recent_list(in_file)
                #Update the current working directory
                path = os.path.dirname(in_file)
                if path == "":
                    path = data.application_directory
                self.set_cwd(path)
                #Set focus to the newly opened document
                tab_widget.currentWidget().setFocus()
                #Update the Save/SaveAs buttons in the menubar
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
                data.QCoreApplication.processEvents()
                return new_tab
        elif isinstance(file, list) == True:
            tabs = []
            for f in file:
                new_tab = open_file_function(f, tab_widget)
                tabs.append(new_tab)
                self.repaint()
                data.QCoreApplication.processEvents()
            return tabs
        else:
            self.display.repl_display_message(
                "Unknown parameter type to 'open file' function!",
                message_type=data.MessageType.ERROR
            )
            return None

    def open_file_hex(self,
                      file_path,
                      tab_widget=None,
                      save_layout=False):
        # Check if file exists
        if os.path.isfile(file_path) == False:
            self.display.repl_display_message(
                "File: {}\ndoesn't exist!".format(file_path),
                message_type=data.MessageType.ERROR
            )
            return
        # Check the file size
        file_size = functions.get_file_size_Mb(file_path)
        if file_size > 50:
            #Create the warning message
            warning =   "The file is larger than {0:d} MB! ({0:d} MB)\n".format(int(file_size))
            warning +=  "A lot of RAM will be needed!\n"
            warning +=  "Files larger than 300 MB can cause the system to hang!\n"
            warning +=  "Are you sure you want to open it?"
            reply = YesNoDialog.warning(warning)
            if reply == data.DialogResult.No.value:
                return
        # Check if file is already open
        check_tab_widget, check_index = self.check_open_file(
            file_path, _type=data.FileType.Hex
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

    def check_open_file(self, file_with_path, _type=data.FileType.Text):
        """
        Check if a file is already open in one of the windows
        """
        found_tab_widget = None
        found_index = None
        # Change the windows style path to the Unix style
        file_with_path = file_with_path.replace("\\", "/")
        for tab_widget in self.get_all_windows():

            # Loop through all of the documents in the tab widget
            if _type == data.FileType.Text:
                for i in range(tab_widget.count()):
                    # Check the file name and file name with path
                    if (tab_widget.widget(i).name == os.path.basename(file_with_path) and
                        tab_widget.widget(i).save_name == file_with_path):
                        # If the file is already open, get its index in the tab widget
                        found_tab_widget = tab_widget
                        found_index = i
                        break
            elif _type == data.FileType.Hex:
                for i in range(tab_widget.count()):
                    # Check the file name and file name with path
                    tab = tab_widget.widget(i)
                    if isinstance(tab, HexView) and tab.save_name == file_with_path:
                        # If the file is already open, get its index in the tab widget
                        found_tab_widget = tab_widget
                        found_index = i
                        break

        return found_tab_widget, found_index

    def close_all_tabs(self):
        """Clear all documents from the main and upper window"""
        # Check if there are any modified documents
        if self.check_document_states() == True:
            message = "You have modified documents!\nWhat do you wish to do?"
            reply = CloseEditorDialog.question(message)
            if reply == data.DialogResult.SaveAndClose.value:
                self.file_save_all()
            elif reply == data.DialogResult.Cancel.value:
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
            if reply == data.DialogResult.SaveAndClose.value:
                self.file_save_all()
            elif reply == data.DialogResult.Cancel.value:
                return
        #Close all tabs and remove all bookmarks from them
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
        #Set the save state flag accordingly
        self.save_state = enable

    def get_tab_by_name(self, tab_name):
        """Find a tab using its name in the basic widgets"""
        windows = self.get_all_windows()
        #Loop through all the basic widgets/windows and check the tabs
        for window in windows:
            for i in range(0, window.count()):
                if window.tabText(i) == tab_name:
                    return window.widget(i)
        #Tab was not found
        return None

    def get_tab_by_save_name(self, in_save_name):
        """
        Find a tab using its save name (file path) in the tab widgets
        """
        windows = self.get_all_windows()
        #Loop through all the tab widgets/windows and check the tabs
        for window in windows:
            for i in range(0, window.count()):
                if isinstance(window.widget(i), CustomEditor) and \
                   window.widget(i).save_name == in_save_name:
                        return window.widget(i)
        #Tab was not found
        return None

    def get_tab_by_string_in_name(self, string):
        """Find a tab with 'string' in its name in the basic widgets"""
        windows = self.get_all_windows()
        #Loop through all the basic widgets/windows and check the tabs
        for window in windows:
            for i in range(0, window.count()):
                if string in window.tabText(i):
                    return window.widget(i)
        #Tab was not found
        return None

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
        #Check if any tab is focused
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
        #Loop through all the basic widgets/windows and check the tab focus
        for window in windows:
            for i in range(0, window.count()):
                if isinstance(window.widget(i), TextDiffer) == True:
                    if (window.widget(i).editor_1.hasFocus() == True or
                        window.widget(i).editor_2.hasFocus() == True):
                        return window
                else:
                    if window.widget(i).hasFocus() == True:
                        return window
        #No tab in the basic widgets has focus
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
                    if window.widget(i).savable == data.CanSave.YES:
                        if window.widget(i).save_status == data.FileStatus.MODIFIED:
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

    class Settings:
        """
        Functions for manipulating the application settings
        (namespace/nested class to MainWindow)
        """
        # Class varibles
        _parent = None
        # Custom object for manipulating the settings of Ex.Co.
        manipulator = None
        # GUI Settings manipulator
        gui_manipulator = None

        def __init__(self, parent):
            """
            Initialization of the Settings object instance
            """
            # Get the reference to the MainWindow parent object instance
            self._parent = parent
            # Initialize the Ex.Co. settings object with the current working directory
            self.manipulator = settings.SettingsFileManipulator()

        def update_recent_list(self, new_file=None):
            """
            Update the settings manipulator with the new file
            """
            # Nested function for opening the recent file
            def new_file_function(file):
                try:
                    self._parent.open_file(file=file, tab_widget=None)
                    self._parent.get_largest_window().currentWidget().setFocus()
                except:
                    pass
            # Update the file manipulator
            if new_file is not None:
                self.manipulator.add_recent_file(new_file)
            # Refresh the menubar recent list
            recent_files_menu = self._parent.recent_files_menu
            # !!Clear all of the actions from the menu OR YOU'LL HAVE MEMORY LEAKS!!
            for action in recent_files_menu.actions():
                recent_files_menu.removeAction(action)
                action.setParent(None)
                action.deleteLater()
                action = None
            recent_files_menu.clear()
            # Add the new recent files list to the menu
            for recent_file in reversed(self.manipulator.recent_files):
                # Iterate in the reverse order, so that the last file will be displayed
                # on the top of the menubar "Recent Files" menu
                recent_file_name = recent_file
                # Check if the filename has too many characters
                if len(recent_file_name) > 30:
                    # Shorten the name that will appear in the menubar
                    recent_file_name = "...{}".format(os.path.splitdrive(recent_file)[1][-30:])
                new_file_action = data.QAction(recent_file_name, recent_files_menu)
                new_file_action.setStatusTip("Open: {}".format(recent_file))
                # Create a function reference for opening the recent file
                temp_function = functools.partial(new_file_function, recent_file)
                new_file_action.triggered.connect(temp_function)
                recent_files_menu.addAction(new_file_action)

        def clear_recent_list(self):
            self.manipulator.clear_recent_files()

        def restore(self):
            """Restore the previously stored settings"""
            # Load the settings from the initialization file
            result = self.manipulator.load_settings()
            # Update the theme
            data.theme = self.manipulator.theme
            self._parent.view.refresh_theme()
            # Update recent files list in the menubar
            self.update_recent_list()
            # Update sessions list in the menubar
            self._parent.sessions.update_menu()
            # Display message in statusbar
            self._parent.display.write_to_statusbar("Restored settings", 1000)
            # Update custon context menu functions
            for func_type in self.manipulator.context_menu_functions.keys():
                funcs = self.manipulator.context_menu_functions[func_type]
                for func_key in funcs.keys():
                    getattr(ContextMenu, func_type)[func_key] = funcs[func_key]
            # Display the settings load error AFTER the theme has been set
            # Otherwise the error text color will not be styled correctly
            if result == False:
                self._parent.display.repl_display_message(
                    "Error loading the settings file, using the default settings values!\nTHE SETTINGS FILE WILL NOT BE UPDATED!",
                    message_type=data.MessageType.ERROR
                )

        def save(self):
            """Save the current settings"""
            self.manipulator.save_settings(
                data.theme,
                ContextMenu.get_settings()
            )
            #Display message in statusbar
            self._parent.display.write_to_statusbar("Saved settings", 1000)

    class Sessions:
        """
        Functions for manipulating sessions
        (namespace/nested class to MainWindow)
        """
        #Class varibles
        _parent = None

        def __init__(self, parent):
            """Initialization of the Sessions object instance"""
            #Get the reference to the MainWindow parent object instance
            self._parent = parent

        def add(self, session_name, session_group_chain=[]):
            """Add the current opened documents in the main and upper window"""
            # Check if the session name is too short
            if len(session_name) < 3:
                self._parent.display.repl_display_message(
                    "Session name is too short!",
                    message_type=data.MessageType.ERROR
                )
                return
            if session_group_chain is not None:
                if (isinstance(session_group_chain, tuple) == False and
                    isinstance(session_group_chain, list) == False):
                    self._parent.display.repl_display_message(
                        "Group name must be a tuple/list of strings!",
                        message_type=data.MessageType.ERROR
                    )
                    return
            # Create lists of files in each window
            try:
                all_windows = self._parent.get_all_windows()
#                if len(all_windows) > 0 and any([x.count() > 0 for x in all_windows]) > 0:
                if len(all_windows) > 0:
                    # Check if the session is already stored
                    session_found = False
                    group = self._parent.settings.manipulator.stored_sessions["main"]
                    for c in session_group_chain:
                        if c in group["groups"].keys():
                            group = group["groups"][c]
                    else:
                        if session_name in group["sessions"].keys():
                            session_found = True
                    # Store the session
                    self._parent.settings.manipulator.add_session(
                        session_name,
                        session_group_chain,
                        self._parent.view.layout_generate(),
                    )
                    if session_found == True:
                        message = "Session '{}/{}' overwritten!".format(
                            "/".join(session_group_chain), session_name
                        )
                    else:
                        message = "Session '{}/{}' added!".format(
                            "/".join(session_group_chain), session_name
                        )
                    self._parent.display.repl_display_message(
                        message,
                        message_type=data.MessageType.SUCCESS
                    )
                    # Refresh the sessions menu in the menubar
                    self.update_menu()
                    # Return success
                    return True
                else:
                    self._parent.display.repl_display_message(
                        "No documents to store!",
                        message_type=data.MessageType.ERROR
                    )
                    self._parent.display.write_to_statusbar("No documents to store!", 1500)
                    # Return error
                    return False
            except Exception as ex:
                traceback.print_exc()
                message = "Invalid document types in the main or upper window!"
                self._parent.display.repl_display_message(
                    message,
                    message_type=data.MessageType.ERROR
                )
                self._parent.display.write_to_statusbar(message, 1500)
                # Return error
                return False

        def restore(self, session):
            """
            Restore the files as stored in the selected session
            """
            # Check if there are any modified documents
            if self._parent.check_document_states() == True:
                message = (
                    "Restoring session: '{}'\n".format(session["name"]) +
                    "You have modified documents!\n" +
                    "What do you wish to do?"
                )
                reply = RestoreSessionDialog.question(message)
                if reply == data.DialogResult.SaveAndRestore.value:
                    self.file_save_all()
                elif reply == data.DialogResult.Cancel.value:
                    return
            # Check if session was found
            if session is not None:
                # Clear all documents from the main and upper window
                self._parent.close_all_tabs()
                # Add files to windows
                self._parent.view.layout_restore(session["layout"])
            else:
                # Session was not found
                message = "Session '{}' was not found!".format(
                    session["chain"]
                )
                self._parent.display.repl_display_message(
                    message,
                    message_type=data.MessageType.ERROR
                )
                self._parent.display.write_to_statusbar(message, 1500)

        def exco_restore(self):
            """
            Open all the source files for Ex.Co.
            """
            # Check if there are any modified documents
            if self._parent.check_document_states() == True:
                message = (
                    "Restoring Ex.Co. development session\n" +
                    "You have modified documents!\n" +
                    "What do you wish to do?"
                )
                reply = RestoreSessionDialog.question(message)
                if reply == data.DialogResult.SaveAndRestore.value:
                    self.file_save_all()
                elif reply == data.DialogResult.Cancel.value:
                    return
            # Clear all documents from the main and upper window
            self._parent.get_largest_window().clear()
            # Loop through the aplication directory and add the relevant files
            exco_main_files = []
            exco_dir = self._parent.settings.manipulator.directories["application"]
            exco_dirs = [
                exco_dir,
                os.path.join(exco_dir, "themes"),
                os.path.join(exco_dir, "cython"),
            ]
            for directory in exco_dirs:
                if os.path.isdir(directory) == False:
                    continue
                for item in os.listdir(directory):
                    file_extension = os.path.splitext(item)[1].lower()
                    if (file_extension == ".py" or
                        file_extension == ".pyw" or
                        file_extension == ".pyx" or
                        file_extension == ".pxd" or
                        file_extension == ".pxi" or
                        file_extension == ".cfg"):
                        file = os.path.join(directory, item)
                        exco_main_files.append(file)
            # Sort the files by name
            exco_main_files.sort()
            # Add the files to the main window
            for file in exco_main_files:
                self._parent.open_file(file, self._parent.get_largest_window())

        def remove(self, session):
            """
            Delete the session
            """
            result = self._parent.settings.manipulator.remove_session(session)
            if result == False:
                # Session was not found
                message = "Session '{}/{}' was not found!".format(
                    "/".join(session["chain"]), session["name"]
                )
                self._parent.display.repl_display_message(
                    message,
                    message_type=data.MessageType.ERROR
                )
                self._parent.display.write_to_statusbar(message, 1500)
            else:
                # Session was removed successfully
                message = "Session '{}/{}' was removed!".format(
                    "/".join(session["chain"]), session["name"]
                )
                self._parent.display.repl_display_message(
                    message,
                    message_type=data.MessageType.WARNING
                )
            # Refresh the sessions menu in the menubar
            self.update_menu()

        def update_menu(self):
            """Update the displayed items in the Sessions menu in the menubar"""
            # Nested function for retrieving the sessions name attribute case insensitively
            def get_case_insensitive_group_name(item):
                name = item[0]
                return name.lower()
            # Clear the sessions list
            self._parent.sessions_menu.clear()
            # First add the Ex.Co. session (all Ex.Co. source files)
            session_name = "Ex.Co. source files"
            exco_session_action = data.QAction(session_name, self._parent)
            exco_session_action.setStatusTip("Open all Ex.Co. source files")
            exco_session_method = self.exco_restore
            exco_session_action.setIcon(functions.create_icon('exco-icon.png'))
            exco_session_action.triggered.connect(exco_session_method)
            self._parent.sessions_menu.addAction(exco_session_action)
            self._parent.sessions_menu.addSeparator()
            ## Create the Sessions menu
            # Group processing function
            def process_group(in_group, in_menu, create_menu=True):
                # Create the new group and attach it to the parent menu
                if create_menu:
                    folder_name = in_group["name"].replace('&', "&&")
                    new_group_menu = Menu(folder_name, self._parent.menubar)
                    in_menu.addMenu(new_group_menu)
                    new_group_menu.setIcon(functions.create_icon('tango_icons/folder.png'))
                else:
                    new_group_menu = in_menu
                # Add the groups
                for g,v in sorted(in_group["groups"].items(), key=lambda x: x[0].lower()):
                    process_group(v, new_group_menu)
                # Add the sessions
                for s,v in sorted(in_group["sessions"].items(), key=lambda x: x[0].lower()):
                    session_name = s.replace('&', "&&")
                    new_session_action = data.QAction(session_name, new_group_menu)
                    new_session_action.setStatusTip("Restore Session: {}".format(s))
                    new_session_method = functools.partial(self.restore, v)
                    new_session_action.setIcon(functions.create_icon('tango_icons/sessions.png'))
                    new_session_action.triggered.connect(new_session_method)
                    new_group_menu.addAction(new_session_action)
            # Process the groups
            sessions_menu = self._parent.sessions_menu
            main_session_group = self._parent.settings.manipulator.stored_sessions["main"]
            process_group(main_session_group, sessions_menu, create_menu=False)

        def get_window_documents(self):
            """
            Return all the editor document paths in the selected window as a list
            """
            window = self._parent.get_window_by_indication()
            documents = [window.widget(i).save_name
                            for i in range(window.count())
                                if  window.widget(i).savable == data.CanSave.YES and
                                    window.widget(i).save_name != ""]
            return documents

    class View:
        """
        Functions for manipulating the application appearance
        (namespace/nested class to MainWindow)
        """
        # Class varibles
        _parent                     = None
        __stored_layout_standard    = None
        __stored_layout_one_window  = None
        #Default widths and heights of the windows
        vertical_width_1            = 2/3
        vertical_width_2            = 1/3
        horizontal_width_1          = 2/3
        horizontal_width_2          = 1/3
        main_relation               = 55
        #Overlay helper widget that will be displayed on top of the main groupbox
        function_wheel_overlay      = None
        #Last executed functions text on the function wheel
        last_executed_function_text = None
        #Function wheel overlay minimum size
        #Stored REPL single/multi line state
        repl_state                  = None
        #Lock used when spinning widgets, so the layout does not get saved mid-spin
        layout_save_block           = False

        def __init__(self, parent):
            """Initialization of the View object instance"""
            #Get the reference to the MainWindow parent object instance
            self._parent = parent
            #Initialize the REPL state to unknown, so it will force
            #the form layout to refresh it
            self.repl_state = None

        def save_layout(self):
            """Save the widths of the splitters"""
            #Check if the splitters are filled correctly
            if self.layout_save_block == True:
                return

        def layout_init(self, show_overlay=False):
            """
            Create the basic layout
            """
            # Create QSplitters
            main_splitter = data.QSplitter(data.Qt.Orientation.Vertical)
            main_splitter.setObjectName("MainSplitter")
            # Create the boxes
            boxes_groupbox = create_groupbox_with_layout(
                name="MainGroupBox", borderless=True,
            )
            # Main box
            main_box = TheBox(
                "",
                "Main",
                data.Qt.Orientation.Horizontal,
                self._parent,
                self._parent
            )
            boxes_groupbox.layout().addWidget(main_box)

            # Vertically split edit fields with the REPL
            main_splitter.addWidget(boxes_groupbox)
            main_splitter.addWidget(self._parent.repl_box)
            # Set the sizes for the main splitter
            main_splitter.setStretchFactor(0, 1)
            #Initialize the main groupbox
            main_groupbox = data.QGroupBox(self._parent)
            main_groupbox_layout = data.QVBoxLayout(main_groupbox)
            main_groupbox_layout.addWidget(main_splitter)
            main_groupbox_layout.setContentsMargins(2, 2, 2, 2)
            main_groupbox_layout.setSpacing(0)
            main_groupbox.setLayout(main_groupbox_layout)
            main_groupbox.setObjectName("Main_Groupbox")
            #Add the splitters combined in the groupbox to the main form
            self._parent.setCentralWidget(main_groupbox)
            # Save references to the MainWindow
            self._parent.boxes_groupbox = boxes_groupbox
            self._parent.main_box = main_box
            self._parent.main_splitter = main_splitter
            self._parent.main_groupbox = main_groupbox
            self._parent.main_groupbox_layout = main_groupbox_layout
            #Initialize the function wheel overlay over the QMainWindows central widget, if needed
            self.function_wheel_overlay = FunctionWheel(
                parent=self._parent.main_groupbox,
                main_form=self._parent,
            )
            self.function_wheel_overlay.setObjectName("Function_Wheel")
            if show_overlay == True:
                self.function_wheel_overlay.show()
            else:
                self.function_wheel_overlay.hide()
            # Settings GUI Manipulator
            if self._parent.settings.gui_manipulator is not None:
                self._parent.settings.gui_manipulator.__del__()
                self._parent.settings.gui_manipulator = None

            self.layout_restore(settings.constants.default_layout)
            self.check_all_close_buttons()

        def show_about(self):
            """Show ExCo information"""
            about = ExCoInfo(
                self._parent,
                app_dir=self._parent.settings.manipulator.directories["application"]
            )
            #The exec_() function shows the dialog in MODAL mode (the parent is unclickable while the dialog is shown)
            about.exec()

        def set_window_focus(self, window):
            """
            Set focus to one of the editing windows
            """
            try:
                # If the window does not have focus, set focus to it
                window.currentWidget().setFocus()
                # Update the Save/SaveAs buttons in the menubar
                window._set_save_status()
                # Check is the widget is a scintilla custom editor
                if isinstance(window.currentWidget(), CustomEditor):
                    # Update the cursor position
                    cw = window.currentWidget()
                    line = cw.getCursorPosition()[0]
                    column = cw.getCursorPosition()[1]
                    index = cw.positionFromLineIndex(line, column)
                    self._parent.display.update_cursor_position(line, column, index)
                else:
                    # Clear the cursor position
                    self._parent.display.update_cursor_position()
            except:
                window.setFocus()
                self._parent.display.write_to_statusbar("Empty window '" + window.name + "' focused!", 1000)
                # Clear the cursor position
                self._parent.display.update_cursor_position()
            finally:
                # Store the last focused widget
                self._parent.last_focused_widget = window

        def set_repl_type(self, type=data.ReplType.SINGLE_LINE):
            """
            Set REPL input as a one line ReplLineEdit or a multiline ReplHelper
            """
            # Check if the REPL type needs to be updated
            if (type == data.ReplType.SINGLE_LINE and
                self.repl_state == data.ReplType.SINGLE_LINE):
                self._parent.main_splitter.setSizes([10, 1])
                return
            elif (type == data.ReplType.MULTI_LINE and
                self.repl_state == data.ReplType.MULTI_LINE):
                return
            self.repl_state = type
            # Reinitialize the groupbox that holds the REPL
            self._parent.repl_box.set_repl(type)
            self._parent.main_splitter.setSizes([10, 1])

        def toggle_window_size(self):
            """
            Maximize the main application window
            """
            if self._parent.isMaximized() == True:
                self._parent.showNormal()
            else:
                self._parent.showMaximized()

        def toggle_one_window_mode(self):
            """
            Toggle between one-window mode and a stored layout
            """
            windows = self._parent.get_all_windows()
            if len(windows) > 1:
                # Store layout and change to one-window
                self.__stored_layout_standard = self.layout_generate()
                json_layout = json.loads(self.__stored_layout_standard)
                window_size = json_layout["WINDOW-SIZE"]
                
#                print(json.dumps(json_layout, indent=4))
                
                # Remove the widget from current layout
                windows = self._parent.get_all_windows()
                widgets = []
                for w in windows:
                    for i in reversed(range(w.count())):
                        widget = w.widget(i)
                        widgets.append((widget, w.tabText(i)))
                        w.removeTab(i)
                        widget.setParent(None)
                
                # Set one-window layout
                if self.__stored_layout_one_window is not None:
                    one_window_layout = self.__stored_layout_one_window
                else:
                    if isinstance(window_size, tuple) or isinstance(window_size, list):
                        one_window_layout = settings.constants.one_window_layout.format(
                            "[{}, {}]".format(*window_size), window_size[1]
                        )
                    elif window_size == "MAXIMIZED":
                        one_window_layout = settings.constants.one_window_layout.format(
                            '"{}"'.format(window_size), 9999
                        )
                    else:
                        raise Exception("Unknown window size: '{}'".format(window_size))
                self.layout_restore(one_window_layout)
                # Put all widgets back into the one
                largest_window = self._parent.get_largest_window()
                widgets.sort(key=lambda x: isinstance(x, CustomEditor) or isinstance(x, PlainEditor))
                for w in reversed(widgets):
                    widget, tab_text = w
                    if tab_text == "REPL MESSAGES":
                        continue
                    largest_window.addTab(widget, tab_text)
                    if hasattr(widget, "_parent"):
                        widget._parent = largest_window
                    elif hasattr(widget, "parent") and not callable(widget.parent):
                        widget.parent = largest_window
                # Update the icons of the tabs
                for i in range(largest_window.count()):
                    largest_window.update_tab_icon(largest_window.widget(i))
            
            else:                
                # Remove the widget from current layout
                windows = self._parent.get_all_windows()
                widgets = {}
                for w in windows:
                    for i in reversed(range(w.count())):
                        widget = w.widget(i)
                        widgets[widget.internals.get_id()] = {
                            "widget": widget,
                            "tab-text": w.tabText(i),
                        }
                        w.removeTab(i)
                        widget.setParent(None)
                
                # Restore stored layout
                self.layout_restore(self.__stored_layout_standard, pre_stored_widgets=widgets)

        def toggle_function_wheel(self):
            """
            Show/hide the function wheel overlay
            """
            if self.function_wheel_overlay.isVisible() == True:
                self.hide_function_wheel()
            else:
                self.show_function_wheel()

        def hide_all_overlay_widgets(self):
            """
            Hide every overlay widget: function wheel, settings gui manipulator, ...
            """
            self.hide_function_wheel()
            self.hide_settings_gui_manipulator()

        def show_function_wheel(self):
            """Show the function wheel overlay"""
            self.hide_settings_gui_manipulator()
            # Check the windows size before displaying the overlay
            if (self._parent.width() < self.function_wheel_overlay.width() or
                self._parent.height() < self.function_wheel_overlay.height()):
                new_size =  functions.create_size(
                    int(self.function_wheel_overlay.width() + self.function_wheel_overlay.width()/5),
                    int(self.function_wheel_overlay.height() + self.function_wheel_overlay.height()/5)
                )
                self._parent.resize(new_size)
            # Check if the function wheel overlay is initialized
            if self.function_wheel_overlay is not None:
                # Save the currently focused widget
                focused_widget = self._parent.get_window_by_child_tab()
                focused_tab = self._parent.get_tab_by_focus()
                if focused_widget is None:
                    focused_widget = self._parent.get_window_by_focus()
                # Store the last focused widget and tab
                self._parent.last_focused_widget = focused_widget
                # Show the function wheel overlay
                self.function_wheel_overlay.show()

        def hide_function_wheel(self):
            """
            Hide the function wheel overlay
            """
            if self.function_wheel_overlay is not None:
                self.function_wheel_overlay.hide()

        def show_settings_gui_manipulator(self):
            # Initialize the settings GUI manipulator if needed
            if self._parent.settings.gui_manipulator is None:
                compare_size = SettingsGuiManipulator.DEFAULT_SIZE
                if (self._parent.width() < compare_size[0] or
                    self._parent.height() < compare_size[1]):
                        new_size =  functions.create_size(
                            int(compare_size[0] + compare_size[0]/5),
                            int(compare_size[1] + compare_size[1]/5)
                        )
                        self._parent.resize(new_size)
                self._parent.settings.gui_manipulator = SettingsGuiManipulator(
                    parent=self._parent.main_groupbox,
                    main_form=self._parent,
                )
            elif self._parent.settings.gui_manipulator.shown == True:
                return
            # Show the gui manipulator
            self._parent.settings.gui_manipulator.show()

        def hide_settings_gui_manipulator(self):
            if self._parent.settings.gui_manipulator is not None:
                self._parent.settings.gui_manipulator.hide()

        def init_style_sheet(self):
            style_sheet = ("""
#Form {{
    background-color: {};
    border: 0px;
}}
#Main_Groupbox {{
    border: 0px;
}}
QSplitter {{
    margin: 0px;
    padding: 0px;
    width: 4px;
}}
QSplitter::handle {{
    background: {};
}}
{}
{}
{}
{}
{}
{}
            """.format(
                data.theme["form"],
                data.theme["form"],
                StyleSheetScrollbar.full(),
                StyleSheetButton.standard(),
                StyleSheetMenu.standard(),
                StyleSheetMenuBar.standard(),
                StyleSheetTooltip.standard(),
                StyleSheetTable.standard(),
            ))
            return style_sheet

        def reset_window_colors(self, in_sheet):
            style_sheet = in_sheet
            style_sheet += self.generate_window_colors()
            style_sheet = self._style_tree_widgets(style_sheet)
            return style_sheet

        def reset_entire_style_sheet(self):
            style_sheet = self.init_style_sheet()
            style_sheet = self.reset_window_colors(style_sheet)
            self._parent.setStyleSheet(style_sheet)
            self._parent.menubar.update_style()
            Menu.update_styles()
#            self._parent.repl_box.indication_reset()
            self.indication_check()

        def generate_window_colors(self):
            style_sheet = """
TabWidget::pane {{
    border: 2px solid {};
    background-color: {};
    margin: 0px;
    spacing: 0px;
    padding: 0px;
}}
TabWidget[indicated=false]::pane {{
    border: 2px solid {};
    background-color: {};
}}
TabWidget[indicated=true]::pane {{
    border: 2px solid {};
    background-color: {};
}}
TabWidget QToolButton {{
    background: {};
    border: 1px solid {};
    margin-top: 0px;
    margin-bottom: 0px;
    margin-left: 0px;
    margin-right: 1px;
}}
TabWidget QToolButton:hover {{
    background: {};
    border: 1px solid {};
}}
            """.format(
                data.theme["indication"]["passiveborder"],
                data.theme["indication"]["passivebackground"],
                data.theme["indication"]["passiveborder"],
                data.theme["indication"]["passivebackground"],
                data.theme["indication"]["activeborder"],
                data.theme["indication"]["activebackground"],
                data.theme["indication"]["passivebackground"],
                data.theme["indication"]["passiveborder"],
                data.theme["indication"]["activebackground"],
                data.theme["indication"]["activeborder"],
            )
            return style_sheet

        def generate_treedisplay_colors(self, type):
            style_sheet =  type + " {"
            style_sheet += "color: {};".format(
                data.theme["fonts"]["default"]["color"],
            )
            style_sheet += "background-color: {};".format(
                data.theme["fonts"]["default"]["background"],
            )
            style_sheet += "}"
            if data.theme["name"] != "Air":
                shrink_icon = expand_icon = os.path.join(
                    data.resources_directory,
                    "feather/air-light-grey/chevron-down.svg"
                ).replace("\\", "/")
                expand_icon = os.path.join(
                    data.resources_directory,
                    "feather/air-light-grey/chevron-right.svg"
                ).replace("\\", "/")
            else:
                shrink_icon = expand_icon = os.path.join(
                    data.resources_directory,
                    "feather/air-grey/chevron-down.svg"
                ).replace("\\", "/")
                expand_icon = os.path.join(
                    data.resources_directory,
                    "feather/air-grey/chevron-right.svg"
                ).replace("\\", "/")
            style_sheet += (
                type + "::branch:closed:has-children:!has-siblings," +
                type + "::branch:closed:has-children:has-siblings {" +
                "    border-image: none;" +
                "    image: url({0});".format(expand_icon) +
                "}" +
                type + "::branch:open:has-children:!has-siblings," +
                type + "::branch:open:has-children:has-siblings {" +
                "    border-image: none;" +
                "    image: url({0});".format(shrink_icon) +
                "}"
            )

            return style_sheet

        def _style_tree_widgets(self, style_sheet):
            tree_widgets = (
                "QTreeView",
            )
            for t in tree_widgets:
                style_sheet += self.generate_treedisplay_colors(t)
            return style_sheet

        def indicate_window(self):
            style_sheet = self.init_style_sheet()
            # Windows
            windows = self._parent.get_all_windows()
            for w in windows:
                w.style().unpolish(w)
                w.style().polish(w)
                w.repaint()

            data.signal_dispatcher.update_title.emit()


        def indication_check(self):
            if hasattr(self, "indication_timer"):
                self.indication_timer.stop()
            else:
                self.indication_timer = data.QTimer(self._parent)
                self.indication_timer.setInterval(50)
                self.indication_timer.setSingleShot(True)
                self.indication_timer.timeout.connect(self.__indication_check)
            self.indication_timer.start(50)

        __indication_state = None
        def __indication_check(self):
            """
            Check if any of the main windows or the REPL is focused
            and indicate the focused widget if needed
            """
            windows = self._parent.get_all_windows()
            if len(windows) == 0 or self._parent.repl is None:
                self.__indication_state = None
                return
            Menu.update_styles()

            # Check the REPL focus
            if (self._parent.repl.hasFocus() == True or
                self._parent.repl_helper.hasFocus() == True):
#                self.__indication_state = "repl-indicated"
                self._parent.repl_box.indication_set()
                return
            else:
                self._parent.repl_box.indication_reset()

            # Check the focus for all of the windows
            window_indicated_flag = False
            indication_list = {}
            for window in windows:
#                window.setProperty("indicated", False)
                indication_list[window] = False
            for window in windows:
                if window.count() == 0:
                    if window.hasFocus() == True:
                        indication_list[window] = True
                        window_indicated_flag = True
                    else:
                        indication_list[window] = False
                else:
                    window.indicated = False
                    for i in range(window.count()):
                        if isinstance(window.widget(i), TextDiffer) == True:
                            if (window.widget(i).hasFocus() == True or
                                window.widget(i).editor_1.hasFocus() == True or
                                window.widget(i).editor_2.hasFocus() == True):
                                indication_list[window] = True
                                window_indicated_flag = True
                        else:
                            w = window.widget(i)
                            if w.hasFocus() == True:
                                indication_list[window] = True
                                window_indicated_flag = True

            if window_indicated_flag:
                for k,v in indication_list.items():
                    k.setProperty("indicated", v)
                self.indicate_window()
                self.__indication_state = "window-indicated"
                return

        def refresh_theme(self):
            windows = self._parent.get_all_windows()
            for window in windows:
                window.customize_tab_bar()
                for i in range(window.count()):
                    if hasattr(window.widget(i), "refresh_lexer") == True:
                        window.widget(i).refresh_lexer()
                    elif hasattr(window.widget(i), "set_theme") == True:
                        window.widget(i).set_theme(data.theme)
            self._parent.repl_helper.refresh_lexer()
            self.reset_entire_style_sheet()
            self._parent.statusbar.setStyleSheet(
                "color: {};".format(data.theme["indication"]["font"])
            )
            # Update the taskbar menu
            self._parent.display.update_theme_taskbar_icon()

            # Update the function wheel
            self.function_wheel_overlay.update_style()

            # Reset the button styled images
            CustomButton.stored_hex = None

        def create_recent_file_list_menu(self):
            self._parent.recent_files_menu = Menu("Recent Files", self._parent.menubar)
            temp_icon = functions.create_icon('tango_icons/file-recent-files.png')
            self._parent.recent_files_menu.setIcon(temp_icon)
            return self._parent.recent_files_menu

        def delete_recent_file_list_menu(self):
            self._parent.recent_files_menu.setParent(None)
            self._parent.recent_files_menu = None

        def clear_recent_file_list(self):
            warning = (
                "Are you sure you wish to delete\n" +
                "the recent files list?"
            )
            reply = YesNoDialog.warning(warning)
            if reply == data.DialogResult.No.value:
                return
            self._parent.settings.clear_recent_list()
            self._parent.settings.update_recent_list()
            self._parent.display.repl_display_success("Recent file list cleared.")


        """
        Layout
        """
        def check_all_close_buttons(self):
            for w in self._parent.get_all_windows():
                w.check_close_button()

        def get_layout_classes(self):
            # Class name storage
            classes = {
                'CustomEditor': CustomEditor,
                'PlainEditor': PlainEditor,
                data.repl_messages_tab_name: PlainEditor,
                'TreeDisplay': TreeDisplay,
                'TreeExplorer': TreeExplorer,
                'HexView': HexView,
            }
            inverted_classes = {v: k for k, v in classes.items()}
            return classes, inverted_classes

        def reindex_all_windows(self):
            # Adjust indexes if needed
            for box in self._parent.get_all_boxes():
                index = 0
                box.update_orientations()
                for i in range(box.count()):
                    tab_widget = box.widget(i)
                    if isinstance(tab_widget, TabWidget):
                        name = tab_widget.objectName()
                        base_name = functions.remove_tabs_from_name(name)
                        box_name = box.objectName()
                        if base_name != box_name:
                            name = box_name + ".Tabs0"
                        new_name = "{}{}".format(
                            functions.remove_tab_number_from_name(name),
                            index
                        )
                        tab_widget.setObjectName(new_name)
                        index += 1
            # Adjust unnecessary box duplications in names and
            # more than one box at one position
            boxes = self._parent.get_all_boxes()
            for b in boxes:
                if b.count() == 1 and \
                   isinstance(b.widget(0), TheBox) and \
                   b.objectName() != "Main":
                        # Remove the unnecessary box (OLD)
#                        b.parent().addWidget(b.widget(0))
                        # Remove the unnecessary box
#                        print("parent:", b.parent().objectName(), "count:", b.parent().count())
#                        print("current:", b.objectName())
                        index = b.parent().indexOf(b)
#                        print("index:", index)
                        b.parent().insertWidget(index, b.widget(0))

                        b.setParent(None)
                        b.deleteLater()
                elif b.count() == 0:
                    pass

            def rename(box):
                for i in range(box.count()):
                    widget = box.widget(i)
                    if isinstance(widget, TheBox):
                        if widget.orientation() == data.Qt.Orientation.Vertical:
                            widget.setObjectName(box.objectName() + f".V{i}")
                        else:
                            widget.setObjectName(box.objectName() + f".H{i}")
                        rename(widget)
                    else:
                        tabs_name = widget.objectName().split('.')[-1]
                        widget.setObjectName(widget.parent().objectName() + f".{tabs_name}")

            main_box = self._parent.findChild(TheBox, "Main")
            rename(main_box)

            # Check close buttons
            self.check_all_close_buttons()

            # Save the layout
            data.QTimer.singleShot(
                10, self._parent.view.layout_save
            )

        def layout_generate(self):
            main = self._parent.findChild(TheBox, "Main")
            children = main.get_child_boxes()
            window_size = self._parent.size()
            window_size = (window_size.width(), window_size.height())
            if self._parent.isMaximized():
                window_size = "MAXIMIZED"
            layout = {
                "WINDOW-SIZE": window_size,
                "BOXES": children
            }

            json_layout = json.dumps(layout, ensure_ascii=False)
            return json_layout

        def layout_restore(self, json_layout, pre_stored_widgets=None):
            main_form = self._parent
            main_groupbox = self._parent.main_groupbox
            main_form.display.repl_suppress()
            # Class name storage
            classes, inverted_classes = self.get_layout_classes()

            # First load the JSON layout, to see if it's valid
            if isinstance(json_layout, str):
                layout = json.loads(json_layout)
            else:
                layout = json_layout

            # Restore size
            window_size = layout["WINDOW-SIZE"]
            screen_size = functions.get_screen_size()
            if window_size == "MAXIMIZED":
                self._parent.showMaximized()
            elif isinstance(window_size, tuple) or \
                 isinstance(window_size, list):
                w, h = window_size
                if w > screen_size[0] or h > screen_size[1]:
                    self._parent.showMaximized()
                else:
                    self._parent.resize(data.QSize(int(w), int(h)))
                    functions.center_to_current_screen(self._parent)

            main_box = self._parent.main_box
            main_box.clear_all()
#            self._parent._print_all_boxes_and_windows()
            
            def create_box(parent, box):
                for k,v in sorted(box.items()):
                    if k.startswith("BOX"):
                        orientation = data.Qt.Orientation.Horizontal
                        if k[-1] == 'V':
                            orientation = data.Qt.Orientation.Vertical
                        new_box = parent.add_box(orientation, add_tabs=False)
                        new_box.show()
                        for _k, _v in v.items():
                            create_box(new_box, _v)
                    elif k == "SIZES":
                        new_box.setSizes(v)
                    elif k.startswith("TABS"):
                        new_tabs = parent.add_tabs()
                        new_tabs.check_close_button()
                        
                        if pre_stored_widgets:
                            for key, class_string in v.items():
                                if isinstance(class_string, tuple) or isinstance(class_string, list):
                                    cls, tab_index, widget_data = class_string
                                    number = widget_data[-1]
                                    if number in pre_stored_widgets.keys():
                                        wd = pre_stored_widgets[number]
                                        w = wd["widget"]
                                        new_tabs.addTab(w, wd["tab-text"])
                                        w.internals.update_tab_widget(new_tabs)
                                        w.internals.update_icon(w)
                            continue
                        
                        current_index = None
                        tab_index = None
                        widget_data = None
                        for key, class_string in v.items():
                            if key == "CURRENT-INDEX":
                                current_index = class_string
                                continue
                            elif isinstance(class_string, str):
                                cls = class_string
                            elif isinstance(class_string, tuple) or isinstance(class_string, list):
                                cls, tab_index, widget_data = class_string
                            else:
                                self._parent.display.display_error(
                                    f"[LAYOUT] Unknown item 'class_string': {class_string.__class__}"
                                )
                                continue

                            if cls in classes.keys():

                                if cls == "CustomEditor":
                                    file = key
                                    if isinstance(class_string, tuple) or isinstance(class_string, list):
                                        line, index, first_visible_line = widget_data[:3]
                                    widget = self._parent.open_file(file, new_tabs, False)
                                    if tab_index is not None:
                                        widget = new_tabs.widget(tab_index)
                                        if widget is not None:
                                            widget.setCursorPosition(line, index)
                                            widget.setFirstVisibleLine(first_visible_line)

#                                elif cls == "Console":
#                                    new_tabs.console_add(key)

                                elif cls == "TreeExplorer":
                                    directory_path = widget_data[0]
                                    if os.path.isdir(directory_path):
                                        file_explorer = new_tabs.tree_add_tab(
                                            data.file_explorer_tab_name, TreeExplorer
                                        )
                                        file_explorer.display_directory(directory_path)
                                        file_explorer.open_file_signal.connect(self._parent.open_file)
                                        file_explorer.open_file_hex_signal.connect(self._parent.open_file_hex)
                                        file_explorer.internals.update_icon(file_explorer)

                                elif cls == "HexView":
                                    file_path = widget_data[0]
                                    if os.path.isfile(file_path):
                                        new_hexview = new_tabs.hexview_add(file_path)

                                elif cls == data.repl_messages_tab_name:
                                    self._parent.repl_messages_tab = new_tabs.plain_add_document(
                                        data.repl_messages_tab_name
                                    )
                                    rmt = self._parent.repl_messages_tab
                                    rmt.internals.set_icon(rmt, self._parent.display.repl_messages_icon)
                            else:
                                self._parent.display.repl_display_error(f"Unknown tab type: {v}")
                        if current_index is not None:
                            new_tabs.setCurrentIndex(current_index)
                    else:
                        self._parent.display.display_error("Unknown box child type: {}".format(k))
            # Open the permanent items
            for k, v in sorted(layout["BOXES"].items()):
                create_box(main_box, v)

            main_form.display.repl_unsuppress()

        def layout_save(self, *args, _async=True):
            def save(*args, **kwargs):
                try:
                    if _async:
                        self.layout_save_timer.stop()
                    layout = self.layout_generate()
#                    file_path = "unknown"
#                    functions.write_to_file(layout, file_path)
                except:
                    traceback.print_exc()
            if _async:
                if not hasattr(self, "layout_save_timer"):
                    # Create the layout save timer if it doesn't exist yet
                    self.layout_save_timer = data.QTimer(self._parent)
                    self.layout_save_timer.setInterval(500)
                    self.layout_save_timer.setSingleShot(True)
                    self.layout_save_timer.timeout.connect(save)
                timer = self.layout_save_timer
                if timer.isActive():
                    timer.stop()
                timer.start()
            else:
                save()

        def check_layout_timer(self):
            if hasattr(self, "layout_save_timer"):
                timer = self.layout_save_timer
                return timer.isActive()
            else:
                return False


    class System:
        """
        Functions that interact with the system
        (namespace/nested class to MainWindow)
        """
        #Class varibles
        _parent = None

        def __init__(self, parent):
            """Initialization of the System object instance"""
            #Get the reference to the MainWindow parent object instance
            self._parent = parent

        def find_files(self,
                       file_name,
                       search_dir=None,
                       case_sensitive=False,
                       search_subdirs=True):
            """Return a list of files that match file_name as a list and display it"""
            #Check if the search directory is none, then use a dialog window
            #to select the real search directory
            if search_dir is None:
                search_dir = self._parent.get_directory_with_dialog()
                #Update the current working directory
                if os.path.isdir(search_dir):
                    self._parent.set_cwd(search_dir)
            #Execute the find function
            found_files = functions.find_files_by_name(
                              file_name,
                              search_dir,
                              case_sensitive,
                              search_subdirs
                          )
            #Check of the function return is valid
            if found_files is None:
                #Check if directory is valid
                self._parent.display.repl_display_message(
                    "Invalid search directory!",
                    message_type=data.MessageType.ERROR
                )
                self._parent.display.write_to_statusbar("Invalid search directory!", 2000)
                return
            elif found_files == []:
                #Check if any files were found
                self._parent.display.repl_display_message(
                    "No files found!",
                    message_type=data.MessageType.WARNING
                )
                self._parent.display.write_to_statusbar("No files found!", 2000)
                return
            #Display the found files
            self._parent.display.show_found_files(
                "'{}' in its name".format(file_name),
                found_files,
                search_dir
            )

        def find_in_files(self,
                          search_text,
                          search_dir=None,
                          case_sensitive=False,
                          search_subdirs=True,
                          break_on_find=False,
                          file_filter=None):
            """Return a list of files that contain the searched text as a list and display it"""
            #Check if the search directory is none, then use a dialog window
            #to select the real search directory
            if search_dir is None:
                search_dir = self._parent.get_directory_with_dialog()
                #Update the current working directory
                if os.path.isdir(search_dir):
                    self._parent.set_cwd(search_dir)
            try:
                # Display the found files
                self._parent.display.show_found_files_with_lines_in_tree(
                    "'{}' in its content".format(search_text),
                    search_text,
                    search_dir,
                    case_sensitive,
                    search_subdirs,
                    break_on_find,
                    file_filter,
                )
            except Exception as ex:
                self._parent.display.repl_display_message(
                    str(ex),
                    message_type=data.MessageType.ERROR
                )

        def replace_in_files(self,
                             search_text,
                             replace_text,
                             search_dir=None,
                             case_sensitive=False,
                             search_subdirs=True,
                             file_filter=None):
            """
            Same as the function in the 'functions' module.
            Replaces all instances of search_string with the replace_string in the files,
            that contain the search string in the search_dir.
            """
            #Close the log window if it is displayed
            warning = "The replaced content will be saved back into the files!\n"
            warning += "You better have a backup of the files if you are unsure,\n"
            warning += "because this action CANNOT be undone!\n"
            warning += "Do you want to continue?"
            reply = YesNoDialog.warning(warning)
            if reply == data.DialogResult.No.value:
                return
            #Check if the search directory is none, then use a dialog window
            #to select the real search directory
            if search_dir is None:
                search_dir = self._parent.get_directory_with_dialog()
                #Update the current working directory
                if os.path.isdir(search_dir):
                    self._parent.set_cwd(search_dir)
            #Replace the text in files
            result = functions.replace_text_in_files_enum(
                search_text,
                replace_text,
                search_dir,
                case_sensitive,
                search_subdirs,
                file_filter
            )
            if result == -1:
                self._parent.display.repl_display_message(
                    "Invalid search&replace in files directory!",
                    message_type=data.MessageType.ERROR
                )
                self._parent.display.write_to_statusbar("Invalid search directory!", 2000)
                return
            elif result == -2:
                self._parent.display.repl_display_message(
                    "Cannot search&replace in files over multiple lines!",
                    message_type=data.MessageType.ERROR
                )
                self._parent.display.write_to_statusbar("Invalid search directory!", 2000)
                return
            #Check the return type
            if len(result) == 0:
                self._parent.display.repl_display_message(
                    "No files with '{}' in its text were found!".format(search_text),
                    message_type=data.MessageType.WARNING
                )
            elif isinstance(result, dict):
                self._parent.display.show_replaced_text_in_files_in_tree(
                    search_text,
                    replace_text,
                    result,
                    search_dir
                )
            else:
                self._parent.display.repl_display_message(
                    "Unknown error!",
                    message_type=data.MessageType.ERROR
                )

        def show_explorer(self):
            if data.platform == "Windows":
                command = "explorer ."
            else:
                self._parent.display.display_warning("Unimplemented yet!")
                return
            self._parent.repl.interpreter.run_cmd_process(command, show_console=False)

    class Editing:
        """
        Document editing functions
        (namespace/nested class to MainWindow)
        """
        #Class varibles
        _parent = None

        def __init__(self, parent):
            """Initialization of the Editing object instance"""
            #Get the reference to the MainWindow parent object instance
            self._parent = parent
            #Initialize the namespace classes
            self.line   = self.Line(self)

        def find_in_open_documents(self,
                                   search_text,
                                   case_sensitive=False,
                                   regular_expression=False,
                                   window_name=None):
            """
            Find instances of search text accross all open documents
            in the selected window
            """
            # Get the current widget
            tab_widget = self._parent.get_window_by_indication()
            if window_name is None:
                window_name = "Main"
            # Check if there are any documents in the basic widget
            if tab_widget.count() == 0:
                message = "No documents in " + tab_widget.name.lower()
                message += " editing window"
                self._parent.display.repl_display_message(
                    message,
                    message_type=data.MessageType.WARNING
                )
                return
            # Save the current index to reset focus to it if no
            # instances of search string are found
            saved_index = tab_widget.currentIndex()
            # Create a deque of the tab index order and start with the current
            # index, deque is used, because it can be rotated by default
            in_deque = collections.deque(range(tab_widget.count()))
            # Rotate the deque until the first element is the current index
            while in_deque[0] != tab_widget.currentIndex():
                in_deque.rotate(1)
            # Set a flag for the first document
            first_document = True
            for i in in_deque:
                # Skip the current widget if it's not an editor
                if isinstance(tab_widget.widget(i), CustomEditor) == False:
                    continue
                # Place the cursor to the top of the document
                # if it is not the current document
                if first_document == True:
                    first_document = False
                else:
                    tab_widget.widget(i).setCursorPosition(0, 0)
                # Find the text
                result = tab_widget.widget(i).find_text(
                    search_text,
                    case_sensitive,
                    True, # search_forward
                    regular_expression
                )
                # If a replace was done, return success
# I can't remember why CYCLED was added here???
#                if (result == data.SearchResult.FOUND or
#                    result == data.SearchResult.CYCLED):
                if result == data.SearchResult.FOUND:
                    return True
            # Nothing found
            tab_widget.setCurrentIndex(saved_index)
            message = "No instances of '" + search_text + "' found in "
            message += tab_widget.name.lower() + " editing window"
            self._parent.display.repl_display_message(
                message,
                message_type=data.MessageType.WARNING
            )
            return False

        def find_replace_in_open_documents(self,
                                           search_text,
                                           replace_text,
                                           case_sensitive=False,
                                           regular_expression=False,
                                           window_name=None):
            """
            Find and replace instaces of search string with replace string
            across all of the open documents in the selected window, one
            instance at a time, starting from the currently selected widget.
            """
            #Get the current widget
            tab_widget = self._parent.get_window_by_indication()
            if window_name is None:
                window_name = "Main"
            #Check if there are any documents in the basic widget
            if tab_widget.count() == 0:
                message = "No documents in the " + tab_widget.name.lower()
                message += " editing window"
                self._parent.display.repl_display_message(
                    message,
                    message_type=data.MessageType.WARNING
                )
                return
            #Save the current index to reset focus to it if no instances of search string are found
            saved_index = tab_widget.currentIndex()
            #Create a deque of the tab index order and start with the current index,
            #deque is used, because it can be rotated by default
            in_deque= collections.deque(range(tab_widget.count()))
            #Rotate the deque until the first element is the current index
            while in_deque[0] != tab_widget.currentIndex():
                in_deque.rotate(1)
            #Find the next instance
            for i in in_deque:
                result = tab_widget.widget(i).find_and_replace(
                    search_text,
                    replace_text,
                    case_sensitive,
                    regular_expression
                )
                #If a replace was done, return success
                if result == True:
                    message = "Found and replaced in " + tab_widget.name.lower()
                    message += " editing window"
                    self._parent.display.write_to_statusbar(message)
                    return True
            #Nothing found
            tab_widget.setCurrentIndex(saved_index)
            message = "No instances of '" + search_text + "' found in the "
            message += tab_widget.name.lower() + " editing window"
            self._parent.display.repl_display_message(
                message,
                message_type=data.MessageType.WARNING
            )
            return False

        def replace_all_in_open_documents(self,
                                          search_text,
                                          replace_text,
                                          case_sensitive=False,
                                          regular_expression=False,
                                          window_name=None):
            """
            Replace all instaces of search string with replace string across
            all of the open documents in the selected window
            """
            #Get the current widget
            tab_widget = self._parent.get_window_by_indication()
            if window_name is None:
                window_name = "Main"
            #Loop over each widget and replace all instances of the search text
            for i in range(tab_widget.count()):
                tab_widget.widget(i).replace_all(
                    search_text,
                    replace_text,
                    case_sensitive,
                    regular_expression
                )
            message = "Replacing all in open documents completed"
            self._parent.display.repl_display_message(
                message,
                message_type=data.MessageType.SUCCESS
            )

        """
        Special wraper functions that take a existing function and
        execute it for the currently focused CustomEditor.
        """
        def run_focused_widget_method(self,
                                      method_name,
                                      argument_list,
                                      window_name=None):
            """Execute a focused widget method"""
            # Get the current widget
#            widget = self._parent.get_tab_by_focus()
            widget = self._parent.get_tab_by_indication()
            # None-check the current widget in the selected window
            if widget is not None:
                method = getattr(widget, method_name)
                # Argument list has to be preceded by the '*' character
                method(*argument_list)
            else:
                message = "No document in focused window!"
                self._parent.display.repl_display_message(
                    message,
                    message_type=data.MessageType.WARNING
                )

        def find(self, search_text, case_sensitive=False, search_forward=True, window_name=None):
            """Find text in the currently focused window"""
            argument_list = [search_text, case_sensitive, search_forward]
            self.run_focused_widget_method("find_text", argument_list, window_name)

        def regex_find(self, search_text, case_sensitive=False, search_forward=True, window_name=None):
            """Find text in the currently focused window"""
            argument_list = [search_text, case_sensitive, search_forward, True]
            self.run_focused_widget_method("find_text", argument_list, window_name)

        def find_and_replace(self, search_text, replace_text, case_sensitive=False, search_forward=True, window_name=None):
            """Find and replace text in the currently focused window"""
            argument_list = [search_text, replace_text, case_sensitive, search_forward]
            self.run_focused_widget_method("find_and_replace", argument_list, window_name)

        def regex_find_and_replace(self, search_text, replace_text, case_sensitive=False, search_forward=True, window_name=None):
            """
            Find and replace text in the currently focused window
            using the regular expressions module
            """
            argument_list = [search_text, replace_text, case_sensitive, search_forward, True]
            self.run_focused_widget_method("find_and_replace", argument_list, window_name)

        def replace_all(self, search_text, replace_text, case_sensitive=False, window_name=None):
            """Replace all occurences of a string in the currently focused window"""
            argument_list = [search_text, replace_text, case_sensitive]
            self.run_focused_widget_method("replace_all", argument_list, window_name)

        def regex_replace_all(self, search_text, replace_text, case_sensitive=False, window_name=None):
            """
            Replace all occurences of a string in the currently focused window
            using the regular expressions module
            """
            argument_list = [search_text, replace_text, case_sensitive, True]
            self.run_focused_widget_method("replace_all", argument_list, window_name)

        def replace_in_selection(self, search_text, replace_text, case_sensitive=False, window_name=None):
            """Replace all occurences of a string in the current selection in the currently focused window"""
            argument_list = [search_text, replace_text, case_sensitive]
            self.run_focused_widget_method("replace_in_selection", argument_list, window_name)

        def regex_replace_in_selection(self, search_text, replace_text, case_sensitive=False, window_name=None):
            """
            Replace all occurences of a string in the current selection in the
            currently focused window using regular expressions module
            """
            argument_list = [search_text, replace_text, case_sensitive, True]
            self.run_focused_widget_method("replace_in_selection", argument_list, window_name)

        def highlight(self, highlight_text, case_sensitive=False, window_name=None):
            """Highlight all occurences of text in the currently focused window"""
            argument_list = [highlight_text, case_sensitive]
            self.run_focused_widget_method("highlight_text", argument_list, window_name)

        def regex_highlight(self, highlight_text, case_sensitive=False, window_name=None):
            """
            Highlight all occurences of text in the currently focused window
            using regular expressions
            """
            argument_list = [highlight_text, case_sensitive, True]
            self.run_focused_widget_method("highlight_text", argument_list, window_name)

        def clear_highlights(self, window_name=None):
            """Clear all highlights in the currently focused window"""
            argument_list = []
            self.run_focused_widget_method("clear_highlights", argument_list, window_name)

        def convert_to_uppercase(self, window_name=None):
            """Change the case of the selected text in the currently focused window"""
            argument_list = [True]
            self.run_focused_widget_method("convert_case", argument_list, window_name)

        def convert_to_lowercase(self, window_name=None):
            """Change the case of the selected text in the currently focused window"""
            argument_list = [False]
            self.run_focused_widget_method("convert_case", argument_list, window_name)

        class Line():
            #Class varibles
            parent = None

            def __init__(self, parent):
                """Initialization of the Editing object instance"""
                #Get the reference to the MainWindow parent object instance
                self._parent = parent

            def goto(self, line_number, window_name=None):
                """Set focus and cursor to the selected line in the currently focused window"""
                argument_list = [line_number]
                self._parent.run_focused_widget_method("goto_line", argument_list, window_name)

            def replace(self, replace_text, line_number, window_name=None):
                """Replace the selected line in the currently focused window"""
                argument_list = [replace_text, line_number]
                self._parent.run_focused_widget_method("replace_line", argument_list, window_name)

            def remove(self, line_number, window_name=None):
                """Remove the selected line in the currently focused window"""
                argument_list = [line_number]
                self._parent.run_focused_widget_method("remove_line", argument_list, window_name)

            def get(self, line_number, window_name=None):
                """Replace the selected line in the currently focused window"""
                argument_list = [line_number]
                self._parent.run_focused_widget_method("get_line", argument_list, window_name)

            def set(self, line_text, line_number, window_name=None):
                """Replace the selected line in the currently focused window"""
                argument_list = [line_text, line_number]
                self._parent.run_focused_widget_method("set_line", argument_list, window_name)

    class Display:
        """
        Functions for displaying of various functions such as:
        show_nodes, find_in_open_documents, ...
        (namespace/nested class to MainWindow)
        """
        # Class varibles
        _parent             = None
        # Attribute for storing which type of tab is used for dispaying node trees
        node_view_type      = data.NodeDisplayType.TREE
        # Theme indicator label
        theme_indicatore    = None
        # Theme actions
        action_air          = None
        action_earth        = None
        action_water        = None
        action_mc           = None
        # References to the dynamically created menus
        stored_menus        = []
        # Icons used for the special widgets
        node_tree_icon              = None
        repl_messages_icon          = None
        system_found_files_icon     = None
        system_found_in_files_icon  = None
        system_replace_in_files_icon= None
        system_show_cwd_tree_icon   = None

        def __init__(self, parent):
            """
            Initialization of the Display object instance
            """
            # Get the reference to the MainWindow parent object instance
            self._parent = parent
            # Initialize the stored icons
            self.node_tree_icon = functions.create_icon('tango_icons/edit-node-tree.png')
            self.repl_messages_icon = functions.create_icon('tango_icons/repl-messages.png')
            self.system_found_files_icon = functions.create_icon('tango_icons/system-find-files.png')
            self.system_found_in_files_icon = functions.create_icon('tango_icons/system-find-in-files.png')
            self.system_replace_in_files_icon = functions.create_icon('tango_icons/system-replace-in-files.png')
            self.system_show_cwd_tree_icon = functions.create_icon('tango_icons/system-show-cwd-tree.png')

        def init_theme_indicator(self):
            """
            Initialization of the theme indicator in the statusbar
            """
            self.theme_indicatore = ThemeIndicator(self._parent.statusbar, self._parent)
            self.theme_indicatore.set_image(data.theme["image-file"])
            self.theme_indicatore.setToolTip(data.theme["tooltip"])
            self.theme_indicatore.restyle()
            self._parent.statusbar.addPermanentWidget(self.theme_indicatore)

        def update_theme_taskbar_icon(self):
            # Check if the indicator is initialized
            if self.theme_indicatore is None:
                return
            # Set the theme icon and tooltip
            self.theme_indicatore.set_image(data.theme["image-file"])
            self.theme_indicatore.setToolTip(data.theme["tooltip"])
            self.theme_indicatore.restyle()

        def write_to_statusbar(self, message, msec=0):
            """Write a message to the statusbar"""
            self._parent.statusbar.setStyleSheet(
                "color: {};".format(data.theme["indication"]["font"])
            )
            self._parent.statusbar.showMessage(message, msec)

        def update_cursor_position(self, cursor_line=None, cursor_column=None, index=None):
            """
            Update the position of the cursor in the current widget
            to the statusbar.
            """
            if cursor_line is None and cursor_column is None:
                self._parent.statusbar_label_left.setText("")
            else:
                statusbar_text = "LINE: {} COLUMN: {} / INDEX: {}".format(
                    cursor_line+1,
                    cursor_column+1,
                    index
                )
                self._parent.statusbar_label_left.setText(statusbar_text)

        def repl_display_success(self, *message):
            self.repl_display_message(
                *message,
                message_type=data.MessageType.SUCCESS
            )

        def repl_display_error(self, *message):
            self.repl_display_message(
                *message,
                message_type=data.MessageType.ERROR
            )

        def repl_display_warning(self, *message):
            self.repl_display_message(
                *message,
                message_type=data.MessageType.WARNING
            )

        __repl_suppressed = False
        __repl_cache = []
        def repl_suppress(self):
            self.__repl_suppressed = True

        def repl_unsuppress(self):
            self.__repl_suppressed = False
            for items in self.__repl_cache:
                self.repl_display_message(
                    *items[0],
                    scroll_to_end=items[1],
                    focus_repl_messages=items[2],
                    message_type=items[3],
                )
            self.__repl_cache = []

        def repl_display_message(self,
                                 *message,
                                 scroll_to_end=True,
                                 focus_repl_messages=True,
                                 message_type=None):
            """
            Display the REPL return message in a scintilla tab
            named "REPL Messages" in one of the basic widgets
            """

            if self.__repl_suppressed:
                self.__repl_cache.append(
                    (
                        message,
                        scroll_to_end,
                        focus_repl_messages,
                        message_type
                    )
                )
                return

            #Nested function for styling REPL MESSAGES text
            def style_repl_text(start, end, color, lexer_number):
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
                    data.QsciScintillaBase.SCI_STYLESETFONT,
                    lexer_number,
                    data.current_editor_font_name.encode("utf-8")
                )
                parent.repl_messages_tab.SendScintilla(
                    data.QsciScintillaBase.SCI_STYLESETSIZE,
                    lexer_number,
                    data.current_editor_font_size
                )
                parent.repl_messages_tab.SendScintilla(
                    data.QsciScintillaBase.SCI_STYLESETBOLD,
                    lexer_number,
                    True
                )
                parent.repl_messages_tab.SendScintilla(
                    data.QsciScintillaBase.SCI_STYLESETUNDERLINE,
                    lexer_number,
                    False
                )
                parent.repl_messages_tab.SendScintilla(
                    data.QsciScintillaBase.SCI_STYLESETFORE,
                    lexer_number,
                    data.QColor(color)
                )
                parent.repl_messages_tab.SendScintilla(
                    data.QsciScintillaBase.SCI_STYLESETBACK,
                    lexer_number,
                    data.QColor(data.theme["fonts"]["default"]["background"])
                )
                parent.repl_messages_tab.SendScintilla(
                    data.QsciScintillaBase.SCI_STARTSTYLING,
                    start,
                    lexer_number
                )
                parent.repl_messages_tab.SendScintilla(
                    data.QsciScintillaBase.SCI_SETSTYLING,
                    end - start,
                    lexer_number
                )
            #Define references directly to the parent and mainform for performance and clarity
            parent = self._parent
            #Find the "REPL Message" tab in the basic widgets
            parent.repl_messages_tab = self.find_repl_messages_tab()
            # Create a new REPL tab in the lower basic widget if it doesn't exist
            if parent.repl_messages_tab is None:
                parent.repl_messages_tab = parent.get_repl_window().plain_add_document(
                    data.repl_messages_tab_name
                )
                rmt = parent.repl_messages_tab
                rmt.internals.set_icon(rmt, self.repl_messages_icon)
            # Parse the message arguments
            if len(message) > 1:
                message = " ".join(message)
            else:
                message = message[0]
            #Check if message is a string class, if not then make it a string
            if message is None:
                return
#            elif isinstance(message, bytes) == True:
#                # Convert a byte string to utf-8 string
#                message = message.decode("utf-8")
            elif isinstance(message, str) == False:
                message = str(message)
            #Check if the message should be error colored
            if message_type is not None:
                #Convert the text to a byte array to get the correct length of the text
                #if it contains non-ASCII characters
                start_bytes = parent.repl_messages_tab.text().encode("utf-8")
                #Get the point from which the text will be highlighted
                start = len(start_bytes) - 1
                if start < 0:
                    start = 0
                #Add the error message
                parent.repl_messages_tab.append("{}\n".format(message))
                #Convert the text to a byte array to get the correct length of the text
                #if it contains non-ASCII characters
                end_bytes = parent.repl_messages_tab.text().encode("utf-8")
                #Get the end point to which the text will be highlighted
                end = len(end_bytes) - 1
                if end < 0:
                    end = 0
                elif end < start:
                    end = start
                #THE MESSAGE COLORS ARE: 0xBBGGRR (BB-blue,GG-green,RR-red)
                if message_type == data.MessageType.ERROR:
                    style_repl_text(start, end, data.theme["fonts"]["error"]["color"], 1)
                elif message_type == data.MessageType.WARNING:
                    style_repl_text(start, end, data.theme["fonts"]["warning"]["color"], 2)
                elif message_type == data.MessageType.SUCCESS:
                    style_repl_text(start, end, data.theme["fonts"]["success"]["color"], 3)
                elif message_type == data.MessageType.DIFF_UNIQUE_1:
                    style_repl_text(start, end, data.theme["fonts"]["diff-unique-1"]["color"], 4)
                elif message_type == data.MessageType.DIFF_UNIQUE_2:
                    style_repl_text(start, end, data.theme["fonts"]["diff-unique-2"]["color"], 5)
                elif message_type == data.MessageType.DIFF_SIMILAR:
                    style_repl_text(start, end, data.theme["fonts"]["diff-similar"]["color"], 6)
            else:
                #Add REPL message to the REPL message tab
                parent.repl_messages_tab.append("{}\n".format(message))
            #Bring the REPL tab to the front
            if focus_repl_messages == True:
                parent.repl_messages_tab._parent.setCurrentWidget(
                    parent.repl_messages_tab
                )
            #Bring cursor to the current message
            if scroll_to_end == True:
                parent.repl_messages_tab.setCursorPosition(
                    parent.repl_messages_tab.lines(), 0
                )
                parent.repl_messages_tab.setFirstVisibleLine(
                    parent.repl_messages_tab.lines()
                )

        def repl_scroll_to_bottom(self):
            """Scroll the REPL MESSAGES tab to the bottom"""
            #Find the "REPL Message" tab in the basic widgets
            self._parent.repl_messages_tab = self.find_repl_messages_tab()
            if self._parent.repl_messages_tab is not None:
                self._parent.repl_messages_tab.goto_line(
                    self._parent.repl_messages_tab.lines()
                )

        def repl_clear_tab(self):
            """Clear text from the REPL messages tab"""
            #Find the "REPL Message" tab in the basic widgets
            self._parent.repl_messages_tab = self.find_repl_messages_tab()
            #Check if REPL messages tab exists
            if self._parent.repl_messages_tab is not None:
                self._parent.repl_messages_tab.setText("")
                self._parent.repl_messages_tab.SendScintilla(
                    data.QsciScintillaBase.SCI_STYLECLEARALL
                )
                self._parent.repl_messages_tab.set_theme(data.theme)
                #Bring the REPL tab to the front
                self._parent.repl_messages_tab._parent.setCurrentWidget(
                    self._parent.repl_messages_tab
                )

        def find_repl_messages_tab(self):
            """Find the "REPL Message" tab in the basic widgets of the MainForm"""
            #Call the MainForm function to find the repl tab by name
            self._parent.repl_messages_tab = self._parent.get_tab_by_name(data.repl_messages_tab_name)
            return self._parent.repl_messages_tab

        def show_nodes(self, custom_editor, parser):
            """
            Function for selecting which type of node tree will be displayed
            """
            if self.node_view_type == data.NodeDisplayType.DOCUMENT:
                self.show_nodes_in_document(custom_editor, parser)
            elif self.node_view_type == data.NodeDisplayType.TREE:
                self.show_nodes_in_tree(custom_editor, parser)

        def show_nodes_in_tree(self, custom_editor, parser):
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
                        message_type=data.MessageType.ERROR
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
            if not(parser in valid_parsers):
                parsers = ", ".join((x.title() for x in valid_parsers))
                message = "Document type is not in ({}),\nbut is of type '{}'!".format(parsers, parser)
                parent.display.repl_display_message(
                        message,
                        message_type=data.MessageType.ERROR
                )
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
            node_tree_tab._parent.setTabIcon(
                node_tree_tab_index,
                self.node_tree_icon
            )
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
                    custom_editor,
                    python_node_tree,
                    parser_error
                )
                new_keywords = [x.name for x in python_node_tree if x.type == "import"]
                new_keywords.extend([x.name for x in python_node_tree if x.type == "class"])
                new_keywords.extend([x.name for x in python_node_tree if x.type == "function"])
                new_keywords.extend([x.name for x in python_node_tree if x.type == "global_variable"])
                custom_editor.set_lexer(
                    lexers.CustomPython(
                        custom_editor, additional_keywords=new_keywords
                    ),
                    "PYTHON"
                )
            elif parser == "NIM":
                # Get all the file information
                nim_nodes = functions.get_nim_node_tree(custom_editor.text())
                # Display the information in the tree tab
                parent.node_tree_tab.display_nim_nodes(
                    custom_editor,
                    nim_nodes
                )
            elif parser in ("C",
                            "C++",
                            "D",
                            "PASCAL",
                            "PHP",
                            "JAVASCRIPT",
                            "MAKEFILE",
                            "HTML",):
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
                except Exception as ex:
                    parent.display.repl_display_error(traceback.format_exc())
                    return
                # Display the information in the tree tab
                parent.node_tree_tab.display_nodes(
                    custom_editor,
                    result,
                    icons[parser],
                )

        def show_nodes_in_document(self, custom_editor, parser):
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
                        message_type=data.MessageType.ERROR
                )
                parent.display.write_to_statusbar("No document selected for node tree creation!", 5000)
                return
            # Check if the document type is Python or C
            if parser != "PYTHON" and parser != "C":
                parent.display.repl_display_message(
                        "Document is not Python or C!",
                        message_type=data.MessageType.ERROR
                )
                parent.display.write_to_statusbar("Document is not Python or C", 5000)
                return
            # Nested hotspot function
            def create_hotspot(node_tab):
                #Create the hotspot boundaries
                hotspot_line        = node_tab.lines()-2
                hotspot_first_ch    = node_tab.text(hotspot_line).index("-")
                hotspot_line_length = node_tab.lineLength(hotspot_line)
                hotspot_start       = node_tab.positionFromLineIndex(hotspot_line, hotspot_first_ch)
                hotspot_end         = node_tab.positionFromLineIndex(hotspot_line, hotspot_line_length)
                hotspot_length      = hotspot_end - hotspot_start
                #Style the hotspot on the node tab
                node_tab.hotspots.style(
                    node_tab, hotspot_start, hotspot_length, color=0xff0000
                )
            # Create the function and connect the hotspot release signal to it
            def hotspot_release(position, modifiers):
                # Get the line and index at where the hotspot was clicked
                line, index = parent.node_tree_tab.lineIndexFromPosition(position)
                # Get the document name and focus on the tab with the document
                document_name       = re.search("DOCUMENT\:\s*(.*)\n", parent.node_tree_tab.text(0)).group(1)
                goto_line_number    = int(re.search(".*\(line\:(\d+)\).*", parent.node_tree_tab.text(line)).group(1))
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
            #Define a name for the NODE tab
            node_tree_tab_name = "NODE TREE/LIST"
            #Find the "NODE" tab in the basic widgets
            parent.node_tree_tab = parent.get_tab_by_name(node_tree_tab_name)
            if parent.node_tree_tab:
                parent.node_tree_tab._parent.close_tab(node_tree_tab_name)
            #Create a new NODE tab in the upper basic widget
            parent.node_tree_tab = parent.get_helper_window().plain_add_document(node_tree_tab_name)
            parent.node_tree_tab.current_icon = self.node_tree_icon
            #Set the NODE document to be ReadOnly
            parent.node_tree_tab.setReadOnly(True)
            parent.node_tree_tab.setText("")
            parent.node_tree_tab.SendScintilla(data.QsciScintillaBase.SCI_STYLECLEARALL)
            parent.node_tree_tab.parentWidget().setCurrentWidget(parent.node_tree_tab)
            #Check if the custom editor is valid
            if isinstance(custom_editor, CustomEditor) == False:
                message = "The editor is not valid!"
                parent.display.repl_display_message(
                        message,
                        message_type=data.MessageType.ERROR
                )
                parent.display.write_to_statusbar(message,  2000)
                return
            else:
                #Check the type of document in the custom editor
                parser = custom_editor.current_file_type
            #Get the node tree for the current widget in the custom editor
            if parser == "PYTHON":
                import_nodes, class_tree_nodes, function_nodes, global_vars = functions.get_python_node_list(custom_editor.text())
                init_space  = "    -"
                extra_space = "     "
                #Display document name, used for finding the tab when clicking the hotspot
                document_name = os.path.basename(custom_editor.save_name)
                document_text = "DOCUMENT: {}\n".format(document_name)
                parent.node_tree_tab.append(document_text)
                parent.node_tree_tab.append("TYPE: {}\n\n".format(parser))
                #Display class nodes
                parent.node_tree_tab.append("CLASS/METHOD TREE:\n")
                for node in class_tree_nodes:
                    node_text = init_space + str(node[0].name) + "(line:"
                    node_text += str(node[0].lineno) + ")\n"
                    parent.node_tree_tab.append(node_text)
                    create_hotspot(parent.node_tree_tab)
                    for child in node[1]:
                        child_text = (child[0]+1)*extra_space + init_space
                        child_text += str(child[1].name) + "(line:"
                        child_text += str(child[1].lineno) + ")\n"
                        parent.node_tree_tab.append(child_text)
                        create_hotspot(parent.node_tree_tab)
                    parent.node_tree_tab.append("\n")
                #Check if there were any nodes found
                if class_tree_nodes == []:
                    parent.node_tree_tab.append("No classes found\n\n")
                #Display function nodes
                parent.node_tree_tab.append("FUNCTIONS:\n")
                for func in function_nodes:
                    func_text = init_space + func.name + "(line:"
                    func_text += str(func.lineno) + ")\n"
                    parent.node_tree_tab.append(func_text)
                    create_hotspot(parent.node_tree_tab)
                #Check if there were any nodes found
                if function_nodes == []:
                    parent.node_tree_tab.append("No functions found\n\n")
                #Connect the hotspot mouserelease signal
                parent.node_tree_tab.SCN_HOTSPOTRELEASECLICK.connect(hotspot_release)
            elif parser == "C":
                function_nodes = functions.get_c_function_list(custom_editor.text())
                init_space          = "    -"
                extra_space     = "     "
                #Display document name, used for finding the tab when clicking the hotspot
                document_name = os.path.basename(custom_editor.save_name)
                document_text = "DOCUMENT: {}\n".format(document_name)
                parent.node_tree_tab.append(document_text)
                parent.node_tree_tab.append("TYPE: {}\n\n".format(parser))
                #Display functions
                parent.node_tree_tab.append("FUNCTION LIST:\n")
                for func in function_nodes:
                    node_text = init_space + func[0] + extra_space
                    node_text += "(line:" + str(func[1]) + ")\n"
                    parent.node_tree_tab.append(node_text)
                    create_hotspot(parent.node_tree_tab)
                #Check if there were any nodes found
                if function_nodes == []:
                    parent.node_tree_tab.append("No functions found\n\n")
                #Connect the hotspot mouserelease signal
                parent.node_tree_tab.SCN_HOTSPOTRELEASECLICK.connect(hotspot_release)

        def show_found_files(self, search_text, file_list, directory):
            """
            Function for selecting which type of node tree will be displayed
            """
            if self.node_view_type == data.NodeDisplayType.DOCUMENT:
                self.show_found_files_in_document(file_list, directory)
            elif self.node_view_type == data.NodeDisplayType.TREE:
                self.show_found_files_in_tree(search_text, file_list, directory)

        def show_found_files_in_document(self, file_list, directory):
            """
            Display the found files returned from the find_files system function
            in the REPL MESSAGES tab
            """
            #Create lines that will be displayed in the REPL messages window
            display_file_info = []
            for file in file_list:
                display_file_info.append("{} ({})".format(os.path.basename(file), file))
            #Display all found files
            self._parent.display.repl_display_message("Found {:d} files:".format(len(file_list)))
            #Use scintilla HOTSPOTS to create clickable file links
            #Create the function and connect the hotspot release signal to it
            def hotspot_release(position, modifiers):
                #Get the line and index at where the hotspot was clicked
                line, index = self._parent.repl_messages_tab.lineIndexFromPosition(position)
                file =  re.search(
                    ".*\((.*)\)",
                    self._parent.repl_messages_tab.text(line)
                ).group(1).replace("\n", "")
                #Open the files
                self._parent.open_file(file, self._parent.get_largest_window())
                #Because open_file updates the new CWD in the REPL MESSAGES,
                #it is needed to set the cursor back to where the hotspot was clicked
                self._parent.repl_messages_tab.setCursorPosition(line, index)
            self._parent.repl_messages_tab.SCN_HOTSPOTRELEASECLICK.connect(hotspot_release)
            #Get the start position
            pos           = self._parent.repl_messages_tab.getCursorPosition()
            hotspot_start = self._parent.repl_messages_tab.positionFromLineIndex(pos[0], pos[1])
            #self.display.repl_display_message("\n".join(found_files))
            self._parent.display.repl_display_message("\n".join(display_file_info))
            #Get the end position
            pos         = self._parent.repl_messages_tab.getCursorPosition()
            hotspot_end = self._parent.repl_messages_tab.positionFromLineIndex(pos[0], pos[1])
            #Style the hotspot on the node tab
            self._parent.repl_messages_tab.hotspots.style(
                self._parent.repl_messages_tab,
                hotspot_start,
                hotspot_end,
                color=0xff0000
            )

        def show_directory_tree(self, directory):
            """
            Display the directory information in a TreeDisplay widget
            """
            #Define references directly to the parent and mainform for performance and clarity
            parent = self._parent
            #Define a name for the FOUND FILES tab
            found_files_tab_name = "FILE/DIRECTORY TREE"
            #Find the "FILE/DIRECTORY TREE" tab in the basic widgets
            parent.found_files_tab = parent.get_tab_by_name(found_files_tab_name)
            if parent.found_files_tab:
                parent.found_files_tab._parent.close_tab(found_files_tab_name)
            #Create a new FOUND FILES tab in the upper basic widget
            found_files_tab = parent.get_helper_window().tree_add_tab(found_files_tab_name)
            found_files_tab.internals.set_icon(
                found_files_tab, self.system_show_cwd_tree_icon
            )
            #Focus the node tree tab
            found_files_tab._parent.setCurrentWidget(found_files_tab)
            #Display the directory information in the tree tab
            found_files_tab.display_directory_tree(directory)

        def show_found_files_in_tree(self, search_text, file_list, directory):
            """
            Display the found files returned from the find_files system function
            in a TreeDisplay widget
            """
            #Define references directly to the parent and mainform for performance and clarity
            parent = self._parent
            #Define a name for the FOUND FILES tab
            found_files_tab_name = "FOUND FILES"
            #Find the "FOUND FILES" tab in the basic widgets
            parent.found_files_tab = parent.get_tab_by_name(found_files_tab_name)
            if parent.found_files_tab:
                parent.found_files_tab._parent.close_tab(found_files_tab_name)
            found_files_tab = parent.found_files_tab
            #Create a new FOUND FILES tab in the upper basic widget
            found_files_tab = parent.get_helper_window().tree_add_tab(found_files_tab_name)
            found_files_tab.internals.set_icon(
                found_files_tab, self.system_found_files_icon
            )
            #Focus the node tree tab
            found_files_tab._parent.setCurrentWidget(found_files_tab)
            #Display the found files information in the tree tab
            found_files_tab.display_found_files(
                search_text,
                file_list,
                directory
            )

        def show_found_files_with_lines_in_tree(self,
                                                search_title,
                                                search_text,
                                                search_dir,
                                                case_sensitive,
                                                search_subdirs,
                                                break_on_find,
                                                file_filter):
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
            found_files_tab.internals.set_icon(
                found_files_tab, self.system_found_files_icon
            )
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
                file_filter
            )

        def show_replaced_text_in_files_in_tree(self,
                                                search_text,
                                                replace_text,
                                                file_list,
                                                directory):
            """
            Display the found files with line information returned from the
            find_in_files and replace_in_files system function in a TreeDisplay
            """
            #Define references directly to the parent and mainform for performance and clarity
            parent = self._parent
            #Define a name for the FOUND FILES tab
            found_files_tab_name = "REPLACEMENTS IN FILES"
            #Find the FOUND FILES tab in the basic widgets
            parent.found_files_tab = parent.get_tab_by_name(found_files_tab_name)
            if parent.found_files_tab:
                parent.found_files_tab._parent.close_tab(found_files_tab_name)
            #Create a new FOUND FILES tab in the upper basic widget
            parent.found_files_tab = parent.get_helper_window().tree_add_tab(found_files_tab_name)
            parent.found_files_tab.internals.set_icon(
                parent.found_files_tab, self.system_replace_in_files_icon
            )
            #Focus the node tree tab
            parent.found_files_tab._parent.setCurrentWidget(parent.found_files_tab)
            #Display the found files information in the tree tab
            parent.found_files_tab.display_replacements_in_files(
                search_text,
                replace_text,
                file_list,
                directory
            )

        def show_text_difference(self,
                                 text_1,
                                 text_2,
                                 text_name_1=None,
                                 text_name_2=None):
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
                text_name_2
            )
            # Find the "DIFF(...)" tab in the basic widgets and close it
            diff_tab_string = "DIFF("
            diff_tab = parent.get_tab_by_string_in_name(diff_tab_string)
            if diff_tab:
                diff_tab_index = diff_tab._parent.indexOf(diff_tab)
                diff_tab._parent.close_tab(diff_tab_index)
            # Add the created text differ to the main window
            diff_index = largest_window.addTab(
                text_differ,
                "DIFF({} / {})".format(text_name_1, text_name_2)
            )
            #Set focus to the text differ tab
            largest_window.setCurrentIndex(diff_index)

        def show_session_editor(self):
            """Display a window for editing sessions"""
            #Create the SessionGuiManipulator
            settings_manipulator = self._parent.settings.manipulator
            sessions_manipulator = SessionGuiManipulator(
                settings_manipulator,
                self._parent.get_helper_window(),
                self._parent
            )
            #Find the old "SESSIONS" tab in the basic widgets and close it
            sessions_tab_name = "SESSIONS"
            sessions_tab = self._parent.get_tab_by_name(sessions_tab_name)
            if sessions_tab:
                sessions_tab._parent.close_tab(sessions_tab_name)
            #Show the sessions in the manipulator
            sessions_manipulator.show_sessions()
            #Add the created session manipulator to the upper window
            sm_index = self._parent.get_helper_window().addTab(
                sessions_manipulator,
                "SESSIONS"
            )
            #Set focus to the text differ tab
            self._parent.get_helper_window().setCurrentIndex(sm_index)

        def create_lexers_menu(self,
                               menu_name,
                               set_lexer_func,
                               store_menu_to_mainform=True,
                               custom_parent=None):
            """
            Create a lexer menu. Currently used in the View menu and
            the CustomEditor tab menu.
            Parameter set_lexer_func has to have:
                - parameter lexer: a lexers.Lexer object
                - parameter lexer_name: a string
            """
            set_lexer = set_lexer_func
            # Nested function for creating an action
            def create_action(name,
                              key_combo,
                              status_tip,
                              icon,
                              function,
                              menu_parent):
                action = data.QAction(name, menu_parent)
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
                if '\t' in name:
                    name = name[:name.find('\t')]
                # Add the action to the context menu
                # function list in the helper forms module
                ContextMenu.add_function(
                    function.__name__, action.pixmap, function, name
                )
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
            def create_lexer(lexer, description):
                func = functools.partial(set_lexer, lexer, description)
                func.__name__ = "set_lexer_{}".format(lexer.__name__)
                return func
            NONE_action = create_action(
                'No lexer',
                None,
                'Disable document lexer',
                'tango_icons/file.png',
                create_lexer(lexers.Text, 'Plain text'),
                lexers_menu
            )
            ADA_action = create_action(
                'Ada',
                None,
                'Change document lexer to: Ada',
                'language_icons/logo_ada.png',
                create_lexer(lexers.Ada, 'Ada'),
                lexers_menu
            )
            AWK_action = create_action(
                'AWK',
                None,
                'Change document lexer to: AWK',
                'language_icons/logo_awk.png',
                create_lexer(lexers.AWK, 'AWK'),
                lexers_menu
            )
            BASH_action = create_action(
                'Bash',
                None,
                'Change document lexer to: Bash',
                'language_icons/logo_bash.png',
                create_lexer(lexers.Bash, 'Bash'),
                lexers_menu
            )
            BATCH_action = create_action(
                'Batch',
                None,
                'Change document lexer to: Batch',
                'language_icons/logo_batch.png',
                create_lexer(lexers.Batch, 'Batch'),
                lexers_menu
            )
            CMAKE_action = create_action(
                'CMake',
                None,
                'Change document lexer to: CMake',
                'language_icons/logo_cmake.png',
                create_lexer(lexers.CMake, 'CMake'),
                lexers_menu
            )
            C_CPP_action = create_action(
                'C / C++',
                None,
                'Change document lexer to: C / C++',
                'language_icons/logo_c_cpp.png',
                create_lexer(lexers.CPP, 'C / C++'),
                lexers_menu
            )
            CSS_action = create_action(
                'CSS',
                None,
                'Change document lexer to: CSS',
                'language_icons/logo_css.png',
                create_lexer(lexers.CSS, 'CSS'),
                lexers_menu
            )
            D_action = create_action(
                'D',
                None,
                'Change document lexer to: D',
                'language_icons/logo_d.png',
                create_lexer(lexers.D, 'D'),
                lexers_menu
            )
            FORTRAN_action = create_action(
                'Fortran',
                None,
                'Change document lexer to: Fortran',
                'language_icons/logo_fortran.png',
                create_lexer(lexers.Fortran, 'Fortran'),
                lexers_menu
            )
            HTML_action = create_action(
                'HTML',
                None,
                'Change document lexer to: HTML',
                'language_icons/logo_html.png',
                create_lexer(lexers.HTML, 'HTML'),
                lexers_menu
            )
            LUA_action = create_action(
                'Lua',
                None,
                'Change document lexer to: Lua',
                'language_icons/logo_lua.png',
                create_lexer(lexers.Lua, 'Lua'),
                lexers_menu
            )
            MAKEFILE_action = create_action(
                'MakeFile',
                None,
                'Change document lexer to: MakeFile',
                'language_icons/logo_makefile.png',
                create_lexer(lexers.Makefile, 'MakeFile'),
                lexers_menu
            )
            MATLAB_action = create_action(
                'Matlab',
                None,
                'Change document lexer to: Matlab',
                'language_icons/logo_matlab.png',
                create_lexer(lexers.Matlab, 'Matlab'),
                lexers_menu
            )
#            NIM_action = create_action(
#                'Nim',
#                None,
#                'Change document lexer to: Nim',
#                'language_icons/logo_nim.png',
#                create_lexer(lexers.Nim, 'Nim'),
#                lexers_menu
#            )
            OBERON_action = create_action(
                'Oberon / Modula',
                None,
                'Change document lexer to: Oberon / Modula',
                'language_icons/logo_oberon.png',
                create_lexer(lexers.Oberon, 'Oberon / Modula'),
                lexers_menu
            )
            PASCAL_action = create_action(
                'Pascal',
                None,
                'Change document lexer to: Pascal',
                'language_icons/logo_pascal.png',
                create_lexer(lexers.Pascal, 'Pascal'),
                lexers_menu
            )
            PERL_action = create_action(
                'Perl',
                None,
                'Change document lexer to: Perl',
                'language_icons/logo_perl.png',
                create_lexer(lexers.Perl, 'Perl'),
                lexers_menu
            )
            PYTHON_action = create_action(
                'Python',
                None,
                'Change document lexer to: Python',
                'language_icons/logo_python.png',
                create_lexer(lexers.Python, 'Python'),
                lexers_menu
            )
            RUBY_action = create_action(
                'Ruby',
                None,
                'Change document lexer to: Ruby',
                'language_icons/logo_ruby.png',
                create_lexer(lexers.Ruby, 'Ruby'),
                lexers_menu
            )
            ROUTEROS_action = create_action(
                'RouterOS',
                None,
                'Change document lexer to: RouterOS',
                'language_icons/logo_routeros.png',
                create_lexer(lexers.RouterOS, 'RouterOS'),
                lexers_menu
            )
            SQL_action = create_action(
                'SQL',
                None,
                'Change document lexer to: SQL',
                'language_icons/logo_sql.png',
                create_lexer(lexers.SQL, 'SQL'),
                lexers_menu
            )
            TCL_action = data.QAction('TCL', lexers_menu)
            TCL_action.setIcon(functions.create_icon('language_icons/logo_tcl.png'))
            TCL_action.triggered.connect(
                functools.partial(set_lexer, lexers.TCL, 'TCL')
            )
            TCL_action = create_action(
                'TCL',
                None,
                'Change document lexer to: TCL',
                'language_icons/logo_tcl.png',
                create_lexer(lexers.TCL, 'TCL'),
                lexers_menu
            )
            TEX_action = create_action(
                'TeX',
                None,
                'Change document lexer to: TeX',
                'language_icons/logo_tex.png',
                create_lexer(lexers.TeX, 'TeX'),
                lexers_menu
            )
            VERILOG_action = create_action(
                'Verilog',
                None,
                'Change document lexer to: Verilog',
                'language_icons/logo_verilog.png',
                create_lexer(lexers.Verilog, 'Verilog'),
                lexers_menu
            )
            VHDL_action = create_action(
                'VHDL',
                None,
                'Change document lexer to: VHDL',
                'language_icons/logo_vhdl.png',
                create_lexer(lexers.VHDL, 'VHDL'),
                lexers_menu
            )
            XML_action = create_action(
                'XML',
                None,
                'Change document lexer to: XML',
                'language_icons/logo_xml.png',
                create_lexer(lexers.XML, 'XML'),
                lexers_menu
            )
            YAML_action = create_action(
                'YAML',
                None,
                'Change document lexer to: YAML',
                'language_icons/logo_yaml.png',
                create_lexer(lexers.YAML, 'YAML'),
                lexers_menu
            )
            CSharp_action = create_action(
                'C#',
                None,
                'Change document lexer to: C#',
                'language_icons/logo_csharp.png',
                create_lexer(lexers.CPP, 'C#'),
                lexers_menu
            )
            Java_action = create_action(
                'Java',
                None,
                'Change document lexer to: Java',
                'language_icons/logo_java.png',
                create_lexer(lexers.Java, 'Java'),
                lexers_menu
            )
            JavaScript_action = create_action(
                'JavaScript',
                None,
                'Change document lexer to: JavaScript',
                'language_icons/logo_javascript.png',
                create_lexer(lexers.JavaScript, 'JavaScript'),
                lexers_menu
            )
            Octave_action = create_action(
                'Octave',
                None,
                'Change document lexer to: Octave',
                'language_icons/logo_octave.png',
                create_lexer(lexers.Octave, 'Octave'),
                lexers_menu
            )
            PostScript_action = create_action(
                'PostScript',
                None,
                'Change document lexer to: PostScript',
                'language_icons/logo_postscript.png',
                create_lexer(lexers.PostScript, 'PostScript'),
                lexers_menu
            )
            Fortran77_action = create_action(
                'Fortran77',
                None,
                'Change document lexer to: Fortran77',
                'language_icons/logo_fortran77.png',
                create_lexer(lexers.Fortran77, 'Fortran77'),
                lexers_menu
            )
            IDL_action = create_action(
                'IDL',
                None,
                'Change document lexer to: IDL',
                'language_icons/logo_idl.png',
                create_lexer(lexers.IDL, 'IDL'),
                lexers_menu
            )
            cicode_action = create_action(
                'CiCode',
                None,
                'Change document lexer to: CiCode',
                'language_icons/logo_cicode.png',
                create_lexer(lexers.CiCode, 'CiCode'),
                lexers_menu
            )
            json_action = create_action(
                'JSON',
                None,
                'Change document lexer to: JSON',
                'language_icons/logo_json.png',
                create_lexer(lexers.JSON, 'JSON'),
                lexers_menu
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
#            lexers_menu.addAction(NIM_action)
            lexers_menu.addAction(OBERON_action)
            lexers_menu.addAction(Octave_action)
            lexers_menu.addAction(PASCAL_action)
            lexers_menu.addAction(PERL_action)
            lexers_menu.addAction(PostScript_action)
            lexers_menu.addAction(PYTHON_action)
            lexers_menu.addAction(RUBY_action)
            lexers_menu.addAction(ROUTEROS_action)
            lexers_menu.addAction(SQL_action)
            lexers_menu.addAction(TCL_action)
            lexers_menu.addAction(TEX_action)
            lexers_menu.addAction(VERILOG_action)
            lexers_menu.addAction(VHDL_action)
            lexers_menu.addAction(XML_action)
            lexers_menu.addAction(YAML_action)
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
        def docking_overlay_show(self):
            parent = self._parent
            docking_overlay = parent.docking_overlay
            if docking_overlay is not None:
                window_list = parent.get_all_windows()
                docking_overlay.show_on_parent(window_list)

        def docking_overlay_hide(self):
            parent = self._parent
            if parent.docking_overlay is not None:
                parent.docking_overlay.hide()

    class Bookmarks:
        """
        All bookmark functionality
        """
        # Class varibles
        parent = None
        # List of all the bookmarks
        marks = None

        def __init__(self, parent):
            """Initialization of the Bookmarks object instance"""
            # Get the reference to the MainWindow parent object instance
            self._parent = parent
            # Initialize all the bookmarks
            self.init()

        def init(self):
            self.marks = {}
            for i in range(10):
                self.marks[i] = {
                    "editor": None,
                    "line": None,
                    "marker-handle": None,
                }

        def add(self, editor, line):
            # Bookmarks should only work in editors
            if (isinstance(editor, CustomEditor) == False or editor.embedded == True):
                return
            for i in range(10):
                if self.marks[i]["editor"] is None and self.marks[i]["line"] is None:
                    self.marks[i]["editor"] = editor
                    self.marks[i]["line"] = line
                    self.marks[i]["handle"] = None
                    self._parent.display.repl_display_success(
                        "Bookmark '{:d}' was added!".format(i),
                    )
                    return i
            else:
                self._parent.display.repl_display_error("All ten bookmarks are occupied!")
                return None

        def add_mark_by_number(self, editor, line, mark_number):
            # Bookmarks should only work in editors
            if (isinstance(editor, CustomEditor) == False or editor.embedded == True):
                return
            # Clear the selected marker if it is not empty
            if self.marks[mark_number]["editor"] is not None and self.marks[mark_number]["line"] is not None:
                self.marks[mark_number]["editor"].bookmarks.toggle_at_line(self.marks[mark_number]["line"])
                self.marks[mark_number]["editor"] = None
                self.marks[mark_number]["line"] = None
                self.marks[mark_number]["handle"] = None
            # Check if there is a bookmark already at the selected editor line
            for i in range(10):
                if self.marks[i]["editor"] == editor and self.marks[i]["line"] == line:
                    self.marks[i]["editor"].bookmarks.toggle_at_line(self.marks[i]["line"])
                    break
            # Set and store the marker on the editor
            handle = editor.bookmarks.add_marker_at_line(line)
            self.marks[mark_number]["editor"] = editor
            self.marks[mark_number]["line"] = line
            self.marks[mark_number]["handle"] = handle
            self._parent.display.repl_display_success(
                "Bookmark '{:d}' was added!".format(mark_number)
            )

        def clear(self):
            cleared_any = False
            for i in range(10):
                if self.marks[i]["editor"] is not None and self.marks[i]["line"] is not None:
                    self.marks[i]["editor"].bookmarks.toggle_at_line(self.marks[i]["line"])
                    self.marks[i]["editor"] = None
                    self.marks[i]["line"] = None
                    self.marks[i]["handle"] = None
                    cleared_any = True
            if cleared_any == False:
                self._parent.display.repl_display_warning(
                    "Bookmarks are clear."
                )
                return

        def remove_by_number(self, mark_number):
            if self.bounds_check(mark_number) == False:
                return
            self.marks[mark_number]["editor"] = None
            self.marks[mark_number]["line"] = None
            self.marks[mark_number]["handle"] = None

        def remove_by_reference(self, editor, line):
            for i in range(10):
                if self.marks[i]["editor"] == editor and self.marks[i]["line"] == line:
                    self.marks[i]["editor"] = None
                    self.marks[i]["line"] = None
                    self.marks[i]["handle"] = None
                    self._parent.display.repl_display_success(
                        "Bookmark '{:d}' was removed!".format(i)
                    )
                    break
            else:
                self._parent.display.repl_display_error("Bookmark not found!")

        def get_editor_all(self, editor):
            """
            Get all bookmarks for a specific editor
            """
            editor_bookmarks = []
            for number, mark in self.marks.items():
                if mark["editor"] == editor:
                    editor_bookmarks.append(mark)
            return editor_bookmarks

        def remove_editor_all(self, editor):
            """
            Remove all bookmarks of an editor
            """
            removed_bookmarks = []
            for i in range(10):
                if self.marks[i]["editor"] == editor:
                    self.marks[i]["editor"] = None
                    self.marks[i]["line"] = None
                    self.marks[i]["handle"] = None
                    removed_bookmarks.append(i)
            if removed_bookmarks != []:
                close_message = "Bookmarks: "
                close_message += ", ".join(str(mark) for mark in removed_bookmarks)
                close_message += "\nwere removed."
                self._parent.display.repl_display_success(close_message)

        def check(self, editor, line):
            for i in range(10):
                if self.marks[i]["editor"] == editor and self.marks[i]["line"] == line:
                    return i
            else:
                return None

        def bounds_check(self, mark_number):
            if mark_number < 0 or mark_number > 9:
                self._parent.display.repl_display_error("Bookmarks only go from 0 to 9!")
                return False
            else:
                return True

        def goto(self, mark_number):
            if self.bounds_check(mark_number) == False:
                return
            if self.marks[mark_number]["editor"] is None and self.marks[mark_number]["line"] is None:
                self._parent.display.repl_display_warning(
                    "Bookmark '{:d}' is empty!".format(mark_number)
                )
            else:
                editor = self.marks[mark_number]["editor"]
                line = self.marks[mark_number]["line"]
                # Focus the stored editor and it's parent tab widget
                editor._parent.setCurrentWidget(editor)
                # Go to the stored line
                editor.goto_line(line)
