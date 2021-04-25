
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2019 Matic Kukovec.
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
import pprint

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


"""
-------------------------------------------------
Main window and its supporting objects
-------------------------------------------------
"""
class MainWindow(data.QMainWindow):
    """Main form that holds all Qt objects"""
    # Define main form control references
    name                    = "Main Window"
    main_window             = None  # Main window
    upper_window            = None  # Upper sidebar
    lower_window            = None  # Lower sidebar
    vertical_splitter       = None  # QSplitter that will split the main form vertically
    horizontal_splitter     = None  # QSplitter that will split the main form horizontally
    main_splitter           = None  # QSplitter that will split the main form and REPL vertically
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
    exco_file_exts =  (
        ['*' + x for x in data.ext_python] +
        ['*' + x for x in data.ext_cython] +
        ['*' + x for x in data.ext_c] +
        ['*' + x for x in data.ext_cpp] +
        ['*' + x for x in data.ext_pascal] +
        ['*' + x for x in data.ext_oberon] +
        ['*' + x for x in data.ext_ada] +
        ['*' + x for x in data.ext_json] +
        ['*' + x for x in data.ext_d] +
        ['*' + x for x in data.ext_nim] +
        ['*' + x for x in data.ext_perl] +
        ['*' + x for x in data.ext_xml] +
        ['*' + x for x in data.ext_text] +
        ['*' + x for x in data.ext_ini]
    )
    # Dictionary for storing the menubar special functions
    menubar_functions       = {}
    # Last focused widget and tab needed by the function wheel overlay
    last_focused_widget     = None
    last_focused_tab        = None
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
        self.settings   = self.Settings(self)
        self.sessions   = self.Sessions(self)
        self.view       = self.View(self)
        self.system     = self.System(self)
        self.editing    = self.Editing(self)
        self.display    = self.Display(self)
        self.bookmarks  = self.Bookmarks(self)
        # Set the name of the main window
        self.name = "Main Window"
        self.setObjectName("Form")
        # Set default font
        self.setFont(data.get_current_font())
        # Initialize the main window 
        self.setWindowTitle("Ex.Co. " + data.application_version)
        # Initialize the log dialog window
        data.log_window = MessageLogger(self)
        # Initialize basic window widgets(main, side_up, side_down)
        self._init_basic_widgets()
        # Initialize statusbar
        self._init_statusbar()
        # Initialize the REPL
        self._init_repl()
        # Initialize the menubar
        self._init_menubar()
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
        # Set the three basic widgets inside the splitters
        self.view.set_basic_widgets(
            main_widget     = self.main_window,
            upper_widget    = self.upper_window,
            lower_widget    = self.lower_window
        )
        # Set the initial window size according to the system resolution
        initial_size    = self.view.function_wheel_overlay.background_image.size()
        initial_width   = initial_size.width() * 14/10
        initial_height  = initial_size.height() * 11/10
        self.resize(initial_width, initial_height)
        # Show log window if logging mode is enabled
        if logging == True:
            # Show log dialog window
            self.view.set_log_window(True)
        data.print_log("Main window displayed successfully")
        # Load the settings
        self.settings.restore()
        # Initialize the theme indicator
        self.display.init_theme_indicator()
        # Initialize repl interpreter
        self._init_interpreter()
        # Set the main window icon if it exists
        if os.path.isfile(data.application_icon) == True:
            self.setWindowIcon(data.QIcon(data.application_icon))
        # Set the repl type to a single line
        self.view.set_repl_type(data.ReplType.SINGLE_LINE)
        self.view.indication_check()
        # Open the file passed as an argument to the QMainWindow initialization
        if file_arguments != None:
            for file in file_arguments:
                self.open_file(file=file, basic_widget=self.main_window)
        else:
            # Create a new document in the main window if the flag was set and
            # the file_arguments is None
            if new_document == True:
                self.create_new()
        # Show the PyQt / QScintilla version in statusbar
        self.statusbar_label_left.setText(data.LIBRARY_VERSIONS)
        self.display.repl_display_message(
            "Using: {}".format(data.LIBRARY_VERSIONS),
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
    
    def _init_statusbar(self):
        self.statusbar = data.QStatusBar(self)
        self.statusbar.setFont(data.get_current_font())
        self.display.write_to_statusbar("Status Bar")
        #Add label for showing the cursor position in a basic widget
        self.statusbar_label_left = data.QLabel(self)
        self.statusbar_label_left.setText("")
        self.statusbar.addPermanentWidget(self.statusbar_label_left)
        #Add the statusbar to the MainWindow
        self.setStatusBar(self.statusbar)
    
    def get_form_references(self):
        """
        Create and return a dictionary that holds all the main form references
        that will be used by the REPL interpreter
        """
        return  dict(
            form        = self,                 
            main        = self.main_window, 
            upper       = self.upper_window, 
            lower       = self.lower_window,
            print_log   = data.print_log, 
            quit        = self.exit, 
            exit        = self.exit, 
            new         = self.create_new, 
            _open       = self.open_files,
            _open_d     = self.open_file_with_dialog, 
            save        = functions.write_to_file, 
            log         = data.log_window, 
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
            # View functions
            spin                    = self.view.spin_basic_widgets, 
            toggle_main_window_side = self.view.toggle_main_window_side, 
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
        """Display the current working directory"""
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
        self._reset_interpreter()
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
        #Check if there is a document in the main basic widget
        current_widget = self.main_window.currentWidget()
        if current_widget == None:
            message = "No document in the main window!"
            display(message)
            return
        #Get the document path
        path = os.path.dirname(current_widget.save_name)
        #Check if the path is not an empty string
        if path == "":
            message = "Document path is not valid!"
            display(message)
            return
        #Set the new current working directory
        self.set_cwd(path)
    
    def leaveEvent(self,  event):
        """Event that fires when you leave the main form"""
        data.print_log("Left Main form")
        
    def closeEvent(self, event):
        """Event that fires when the main window is closed"""
        #Close the log window if it is displayed
        self.view.set_log_window(False)
        #Check if there are any modified documents
        if self.check_document_states() == True:
            quit_message = "You have modified documents!\nQuit anyway?"
            reply = YesNoDialog.question(quit_message)
            if reply != data.QMessageBox.Yes:
                event.ignore()

    def resizeEvent(self, event):
        """Resize QMainWindow event"""
        #Save the size relations between basic widgets
        self.view.save_layout()
        #Refresh the size relation between the basic widgets and the REPL,
        #so that the REPL height is always the same
        self.view.refresh_main_splitter()
        #Hide the function whell if it is displayed
        self.view.hide_all_overlay_widgets()
        #Accept the event
        event.setAccepted(False)

    def keyPressEvent(self, event):
        """QMainWindow keyPressEvent, to catch which key was pressed"""
        #Check if the lock is released
        if self.key_lock == False:
            #Check for active keys
            if self._window_filter_keypress(event) == True:
                return
    
    def keyReleaseEvent(self, event):
        """QMainWindow keyReleaseEvent, to catch which key was pressed"""
        #Check if the lock is released
        if self.key_lock == False:
            #Check for active keys
            if self._window_filter_keyrelease(event) == True:
                return
    
    def mousePressEvent(self, event):
        """Overridden main window mouse click event"""
        # Execute the superclass mouse press event
        super().mousePressEvent(event)
        # Hide the function wheel if it is shown
        if event.button() != data.Qt.RightButton:
            self.view.hide_all_overlay_widgets()
        # Reset the click&drag context menu action
        components.ActionFilter.clear_action()
    
    def _window_filter_keypress(self, key_event):
        """Filter keypress for appropriate action"""
        pressed_key = key_event.key()
        accept_keypress = False
        #Check for escape keypress
        if pressed_key == data.Qt.Key_Escape:
            #Check if the function wheel overlay is shown
            if self.view.function_wheel_overlay.isVisible() == True:
                self.view.toggle_function_wheel()
        return accept_keypress
    
    def _window_filter_keyrelease(self, key_event):
            """Filter keyrelease for appropriate action"""
            #released_key = key_event.key()
            accept_keyrelease = False
            return accept_keyrelease

    def _key_events_lock(self):
        """
        Function for disabling/locking the keypress and 
        keyrelease events (used by the ReplLineEdit widget)
        """
        #Disable the key events of the QMainWindow
        self.key_lock = True
        #Disable the save/saveas buttons in the menubar
        self.set_save_file_state(False)

    def _key_events_unlock(self):
        """
        Function for enabling/unlocking the keypress and
        keyrelease events (used by the ReplLineEdit widget)
        """
        #Reenable the key events of the QMainWindow
        self.key_lock = False
    
    def _get_directory_with_dialog(self):
        """
        Function for using a QFileDialog window for retreiving
        a directory name as a string
        """
        dir_dialog = data.QFileDialog
        directory = dir_dialog.getExistingDirectory()
        return directory
    
    def run_process(self, command, show_console=True, output_to_repl=False):
        """Run a command line process and display the result"""
        self.display.repl_display_message("Executing CMD command: \"" + command + "\"")
        #Run the command and display the result
        result  = self.repl.interpreter.run_cmd_process(command, show_console, output_to_repl)
        self.display.repl_display_message(result)
    
    def file_create_new(self):
        """The function name says it all"""
        self.create_new(tab_name=None, basic_widget=self.last_focused_widget)
    
    def file_open(self):
        """The function name says it all"""
        self.open_file_with_dialog(basic_widget=self.last_focused_widget)
    
    def file_save(self, encoding="utf-8", line_ending=None):
        """The function name says it all"""
        focused_tab = self.get_tab_by_focus()
        if isinstance(focused_tab, CustomEditor) == True:
            if focused_tab != None and focused_tab.savable == data.CanSave.YES:
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
                focused_tab.icon_manipulator.update_icon(focused_tab)
                # Reimport the user configuration file and update the menubar
                if functions.is_config_file(focused_tab.save_name) == True:
                    self.update_menubar()
                    self.import_user_functions()
    
    def file_saveas(self, encoding="utf-8"):
        """The function name says it all"""
        focused_tab = self.get_tab_by_focus()
        if focused_tab != None:
            focused_tab.save_document(
                saveas=True,
                encoding=encoding
            )
            #Set the icon if it was set by the lexer
            focused_tab.icon_manipulator.update_icon(focused_tab)
            #Reimport the user configuration file and update the menubar
            if functions.is_config_file(focused_tab.save_name) == True:
                self.update_menubar()
                self.import_user_functions()
    
    def file_save_all(self, encoding="utf-8"):
        """Save all open modified files"""
        #Create a list of the windows
        windows = [self.main_window, self.upper_window, self.lower_window]
        #Loop through all the basic widgets/windows and check the tabs
        saved_something = False
        for window in windows:
            for i in range(0, window.count()):
                tab = window.widget(i)
                #Skip to next tab if it is not a CustomEditor
                if isinstance(tab, CustomEditor) == False:
                    continue
                #Test if the tab is modified and savable
                if (tab.savable == data.CanSave.YES and 
                    tab.save_status == data.FileStatus.MODIFIED):
                    #Save the file
                    tab.save_document(saveas=False, encoding=encoding)
                    #Set the icon if it was set by the lexer
                    tab.icon_manipulator.update_icon(tab)
                    #Set the saved something flag
                    saved_something = True
        #Display the successful save
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
    
    def update_menubar(self):
        """
        Update the Menubar in case any keyboard shortcuts
        were changed in the configuration file
        """
        self._init_menubar()
        self.settings.update_recent_list()
        self.sessions.update_menu()

    def _init_menubar(self):
        """
        Initialize the menubar ("QAction.triggered.connect" signals 
        first parameter is always "checked: bool").
        This is a very long function that should be trimmed sometime!
        """
        self.menubar = data.QMenuBar()
        self.menubar.setFont(data.get_current_font())
        # Click filter for the menubar menus
        click_filter = components.ActionFilter(self)
        # Nested function for creating an action
        def create_action(name, key_combo, status_tip, icon, function, enabled=True):
            action = data.QAction(name, self)
            # Key combination
            keys = None
            if key_combo != None and key_combo != "":
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
            if icon != None:
                action.setIcon(functions.create_icon(icon))
                action.pixmap = functions.create_pixmap_with_size(icon, 32, 32)
            # Function
            if function != None:
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
            file_menu = Menu("&File")
            self.menubar.addMenu(file_menu)
            file_menu.installEventFilter(click_filter)
            # New file
            def special_create_new_file():
                self.file_create_new()
            new_file_action = create_action('New', settings.Keys.new_file, 'Create new empty file', 'tango_icons/document-new.png', special_create_new_file)
            # Open file
            def special_open_file():
                self.file_open()
            open_file_action = create_action('Open', settings.Keys.open_file, 'Open file', 'tango_icons/document-open.png', special_open_file)
            # Save options need to be saved to a reference for disabling/enabling
            # Save file
            def special_save_file():
                self.file_save()
            self.save_file_action = create_action('Save', settings.Keys.save_file, 'Save current file in the UTF-8 encoding', 'tango_icons/document-save.png', special_save_file, enabled=False)
            # Save file as
            def special_saveas_file():
                self.file_saveas()
            self.saveas_file_action = create_action('Save As', settings.Keys.saveas_file, 'Save current file as a new file in the UTF-8 encoding', 'tango_icons/document-save-as.png', special_saveas_file, enabled=False)
            # Save all
            def special_save_all():
                self.file_save_all()
            self.save_all_action = create_action('Save All', None, 'Save all modified documents in all windows in the UTF-8 encoding', 'tango_icons/file-save-all.png', special_save_all, enabled=False)
            # Exit
            exit_action = create_action('Exit\tAlt+F4', None, 'Exit application', 'tango_icons/system-log-out.png', self.exit)
            # Additional menu for saving in different encodings
            def add_save_in_different_encoding_submenu():
                # Add the save in encoding menu
                self.save_in_encoding = Menu("Save in encoding...")
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
                    current_window.currentWidget().setFocus()
                except:
                    pass
            close_tab_action = create_action('Close Tab', settings.Keys.close_tab, 'Close the current tab', 'tango_icons/close-tab.png', close_tab)
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
                    if reply == data.QMessageBox.Yes:
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
            #Add reload themes function
            themes_reload_action = create_action('Reload Themes', None, 'Reload themes from modules to update any changes made in the theme files', 'tango_icons/themes-reload.png', self.view.reload_themes)
            #Add recent file list in the file menu
            recent_file_list_menu = self.view.create_recent_file_list_menu()
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
            file_menu.addAction(themes_reload_action)
            file_menu.addSeparator()
            file_menu.addMenu(recent_file_list_menu)
            file_menu.addSeparator()
            file_menu.addAction(exit_action)
        #Edit Menus
        #Adding the basic options to the menu
        def construct_edit_basic_menu():
            edit_menu = Menu("&Editing")
            self.menubar.addMenu(edit_menu)
            edit_menu.installEventFilter(click_filter)
            def copy():
                try:
                    self.get_tab_by_focus().copy()
                except:
                    pass
            temp_string = 'Copy any selected text in the currently '
            temp_string += 'selected window to the clipboard'
            copy_action = create_action(
                'Copy\t' + settings.Editor.Keys.copy, 
                "#" + settings.Editor.Keys.copy,
                temp_string, 
                'tango_icons/edit-copy.png', 
                copy
            )
            def cut():
                try:
                    self.get_tab_by_focus().cut()
                except:
                    pass
            cut_action = create_action(
                'Cut\t' + settings.Editor.Keys.cut, 
                "#" + settings.Editor.Keys.cut,  
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
                'Paste\t' + settings.Editor.Keys.paste, 
                "#" + settings.Editor.Keys.paste,  
                'Paste the text in the clipboard to the currenty selected window', 
                'tango_icons/edit-paste.png', 
                paste
            )
            def undo():
                try:
                    self.get_tab_by_focus().undo()
                except:
                    pass
            undo_action = create_action(
                'Undo\t' + settings.Editor.Keys.undo, 
                "#" + settings.Editor.Keys.undo, 
                'Undo last editor action in the currenty selected window', 
                'tango_icons/edit-undo.png', 
                undo
            )
            def redo():
                try:
                    self.get_tab_by_focus().redo()
                except:
                    pass
            redo_action = create_action(
                'Redo\t' + settings.Editor.Keys.redo, 
                "#" + settings.Editor.Keys.redo, 
                'Redo last undone editor action in the currenty selected window', 
                'tango_icons/edit-redo.png', 
                redo
            )
            def select_all():
                try:
                    self.get_tab_by_focus().selectAll(True)
                except:
                    pass
            select_all_action = create_action(
                'Select All\t' + settings.Editor.Keys.select_all, 
                "#" + settings.Editor.Keys.select_all, 
                'Select all of the text in the currenty selected window', 
                'tango_icons/edit-select-all.png', 
                select_all
            )
            def indent():
                try:
                    self.get_tab_by_focus().custom_indent()
                except:
                    pass
            indent_action = create_action(
                'Indent\t' + settings.Editor.Keys.indent, 
                "#" + settings.Editor.Keys.indent, 
                'Indent the selected lines by the default width (4 spaces) in the currenty selected window', 
                'tango_icons/format-indent-more.png', 
                indent
            )
            def unindent():
                try:
                    self.get_tab_by_focus().custom_unindent()
                except:
                    pass
            unindent_action = create_action(
                'Unindent\t' + settings.Editor.Keys.unindent, 
                "#" + settings.Editor.Keys.unindent,
                'Unindent the selected lines by the default width (4 spaces) in the currenty selected window', 
                'tango_icons/format-indent-less.png', 
                unindent
            )
            def delete_start_of_word():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.QsciScintillaBase.SCI_DELWORDLEFT)
                except:
                    pass
            del_start_word_action = create_action(
                'Delete start of word\t' + settings.Editor.Keys.delete_start_of_word, 
                "#" + settings.Editor.Keys.delete_start_of_word, 
                'Delete the current word from the cursor to the starting index of the word', 
                'tango_icons/delete-start-word.png', 
                delete_start_of_word
            )
            def delete_end_of_word():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.QsciScintillaBase.SCI_DELWORDRIGHT)
                except:
                    pass
            del_end_word_action = create_action(
                'Delete end of word\t' + settings.Editor.Keys.delete_end_of_word,
                "#" + settings.Editor.Keys.delete_end_of_word, 
                'Delete the current word from the cursor to the ending index of the word', 
                'tango_icons/delete-end-word.png', 
                delete_end_of_word
            )
            def delete_start_of_line():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.QsciScintillaBase.SCI_DELLINELEFT)
                except:
                    pass
            del_start_line_action = create_action(
                'Delete start of line\t' + settings.Editor.Keys.delete_start_of_line,
                "#" + settings.Editor.Keys.delete_start_of_line, 
                'Delete the current line from the cursor to the starting index of the line', 
                'tango_icons/delete-start-line.png', 
                delete_start_of_line
            )
            def delete_end_of_line():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.QsciScintillaBase.SCI_DELLINERIGHT)
                except:
                    pass
            del_end_line_action = create_action(
                'Delete end of line\t' + settings.Editor.Keys.delete_end_of_line,
                "#" + settings.Editor.Keys.delete_end_of_line, 
                'Delete the current line from the cursor to the ending index of the line', 
                'tango_icons/delete-end-line.png', 
                delete_end_of_line
            )
            def goto_to_start():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.QsciScintillaBase.SCI_DOCUMENTSTART)
                except:
                    pass
            go_to_start_action = create_action(
                'Go to start\t' + settings.Editor.Keys.go_to_start,
                "#" + settings.Editor.Keys.go_to_start, 
                'Move cursor up to the start of the currently selected document', 
                'tango_icons/goto-start.png', 
                goto_to_start
            )
            def goto_to_end():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.QsciScintillaBase.SCI_DOCUMENTEND)
                except:
                    pass
            go_to_end_action = create_action(
                'Go to end\t' + settings.Editor.Keys.go_to_end,
                "#" + settings.Editor.Keys.go_to_end, 
                'Move cursor down to the end of the currently selected document', 
                'tango_icons/goto-end.png', 
                goto_to_end
            )
            def select_page_up():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.QsciScintillaBase.SCI_PAGEUPEXTEND)
                except:
                    pass
            select_page_up_action = create_action(
                'Select page up\t' + settings.Editor.Keys.select_page_up,
                "#" + settings.Editor.Keys.select_page_up, 
                'Select text up one page of the currently selected document', 
                None, 
                select_page_up
            )
            def select_page_down():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.QsciScintillaBase.SCI_PAGEDOWN)
                except:
                    pass
            select_page_down_action = create_action(
                'Select page down\t' + settings.Editor.Keys.select_page_down,
                "#" + settings.Editor.Keys.select_page_down, 
                'Select text down one page of the currently selected document', 
                None, 
                select_page_down
            )
            def select_to_start():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.QsciScintillaBase.SCI_DOCUMENTSTARTEXTEND)
                except:
                    pass
            select_to_start_action = create_action(
                'Select to start\t' + settings.Editor.Keys.select_to_start,
                "#" + settings.Editor.Keys.select_to_start, 
                'Select all text up to the start of the currently selected document', 
                None, 
                select_to_start
            )
            def select_to_end():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.QsciScintillaBase.SCI_DOCUMENTENDEXTEND)
                except:
                    pass
            select_to_end_action = create_action(
                'Select to end\t' + settings.Editor.Keys.select_to_end,
                "#" + settings.Editor.Keys.select_to_end, 
                'Select all text down to the start of the currently selected document', 
                None, 
                select_to_end
            )
            def scroll_up():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.QsciScintillaBase.SCI_PAGEUP)
                except:
                    pass
            scroll_up_action = create_action(
                'Scroll up\t' + settings.Editor.Keys.scroll_up,
                "#" + settings.Editor.Keys.scroll_up, 
                'Scroll up one page of the currently selected document', 
                'tango_icons/scroll-up.png', 
                scroll_up
            )
            def scroll_down():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.QsciScintillaBase.SCI_PAGEDOWN)
                except:
                    pass
            scroll_down_action = create_action(
                'Scroll down\t' + settings.Editor.Keys.scroll_down,
                "#" + settings.Editor.Keys.scroll_down, 
                'Scroll down one page of the currently selected document', 
                'tango_icons/scroll-down.png', 
                scroll_down
            )
            def line_cut():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.QsciScintillaBase.SCI_LINECUT)
                except:
                    pass
            line_cut_action = create_action(
                'Line Cut\t' + settings.Editor.Keys.line_cut,
                "#" + settings.Editor.Keys.line_cut, 
                'Cut out the current line/lines of the currently selected document', 
                'tango_icons/edit-line-cut.png', 
                line_cut
            )
            def line_copy():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.QsciScintillaBase.SCI_LINECOPY)
                except:
                    pass
            line_copy_action = create_action(
                'Line Copy\t' + settings.Editor.Keys.line_copy,
                "#" + settings.Editor.Keys.line_copy, 
                'Copy the current line/lines of the currently selected document', 
                'tango_icons/edit-line-copy.png', 
                line_copy
            )
            def line_delete():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.QsciScintillaBase.SCI_LINEDELETE)
                except:
                    pass
            line_delete_action = create_action(
                'Line Delete\t' + settings.Editor.Keys.line_delete,
                "#" + settings.Editor.Keys.line_delete, 
                'Delete the current line of the currently selected document', 
                'tango_icons/edit-line-delete.png', 
                line_delete
            )
            def line_transpose():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.QsciScintillaBase.SCI_LINETRANSPOSE)
                except:
                    pass
            line_transpose_action = create_action(
                'Line Transpose\t' + settings.Editor.Keys.line_transpose,
                "#" + settings.Editor.Keys.line_transpose, 
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
                    pass
            line_duplicate_action = create_action(
                'Line/Selection Duplicate\t' + settings.Editor.Keys.line_selection_duplicate,
                "#" + settings.Editor.Keys.line_selection_duplicate, 
                'Duplicate the current line/selection of the currently selected document', 
                'tango_icons/edit-line-duplicate.png', 
                line_duplicate
            )
            #Rectangular block selection
            action_text = 'Rectangular block selection\tAlt+Mouse'
            rect_block_action    = data.QAction(action_text, self)
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
            edit_menu = Menu("&Advanced")
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
                settings.Keys.find, 
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
                settings.Keys.regex_find, 
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
                settings.Keys.find_and_replace, 
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
                settings.Keys.regex_find_and_replace, 
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
                settings.Keys.highlight, 
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
                settings.Keys.regex_highlight, 
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
                settings.Keys.clear_highlights, 
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
                settings.Keys.replace_selection, 
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
                settings.Keys.regex_replace_selection, 
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
                settings.Keys.replace_all, 
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
                settings.Keys.regex_replace_all, 
                'Replace all instances of text in currently selected document using Python regular expressions', 
                'tango_icons/edit-replace-all-re.png', 
                special_regex_replace_all
            )
            #Nested special function for un/commenting selected lines in the main widget
            def comment_uncomment():
                try:
                    self.get_tab_by_focus().toggle_comment_uncomment()
                except Exception as ex:
                    print(ex)
            toggle_comment_action = create_action(
                'Comment/Uncomment',
                settings.Keys.toggle_comment, 
                'Toggle comments for the selected lines or single line in the currently selected document', 
                'tango_icons/edit-comment-uncomment.png', 
                comment_uncomment
            )
            def toggle_autocompletions():
                try:
                    self.get_tab_by_focus().toggle_autocompletions()
                except:
                    pass
            toggle_autocompletion_action = create_action(
                'Enable/Disable Autocompletion',
                settings.Keys.toggle_autocompletion, 
                'Enable/Disable autocompletions for the currently selected document', 
                'tango_icons/edit-autocompletion.png', 
                toggle_autocompletions
            )
            def toggle_wordwrap():
                try:
                    self.get_tab_by_focus().toggle_wordwrap()
                except:
                    pass
            toggle_wrap_action = create_action(
                'Enable/Disable Line Wrapping',
                settings.Keys.toggle_wrap, 
                'Enable/Disable line wrapping for the currently selected document', 
                'tango_icons/wordwrap.png', 
                toggle_wordwrap
            )
            def reload_file():
                try:
                    self.get_tab_by_focus().reload_file()
                except:
                    pass
            reload_file_action = create_action(
                'Reload file',
                settings.Keys.reload_file, 
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
                settings.Keys.node_tree, 
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
                settings.Keys.goto_line, 
                'Go to the specified line in the current main window document', 
                'tango_icons/edit-goto.png', 
                special_goto_line
            )
            def special_indent_to_cursor():
                try:
                    self.get_tab_by_focus().indent_lines_to_cursor()
                except:
                    pass
            temp_string = 'Indent the selected lines to the current cursor position '
            temp_string += '(SPACE ON THE LEFT SIDE OF LINES IS STRIPPED!)'
            indent_to_cursor_action = create_action(
                'Indent to cursor',
                settings.Keys.indent_to_cursor, 
                temp_string, 
                'tango_icons/edit-indent-to-cursor.png', 
                special_indent_to_cursor
            )
            def special_to_uppercase():
                focused_tab = self.get_used_tab()
                self.editing.convert_to_uppercase(focused_tab._parent.name)
            to_uppercase_action = create_action(
                'Selection to UPPERCASE',
                settings.Keys.to_uppercase, 
                'Convert selected text to UPPERCASE', 
                'tango_icons/edit-case-to-upper.png', 
                special_to_uppercase
            )
            def special_to_lowercase():
                focused_tab = self.get_used_tab()
                self.editing.convert_to_lowercase(focused_tab._parent.name)
            to_lowercase_action = create_action(
                'Selection to lowercase',
                settings.Keys.to_lowercase, 
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
                settings.Keys.find_in_documents, 
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
                settings.Keys.find_replace_in_documents, 
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
                settings.Keys.replace_all_in_documents, 
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
            edit_menu.addAction(reset_context_menu_action)
            edit_menu.addSeparator()
            edit_menu.addAction(find_in_documents_action)
            edit_menu.addAction(find_replace_in_documents_action)
            edit_menu.addAction(replace_all_in_documents_action)
        #System menu
        def construct_system_menu():
            system_menu = Menu("S&ystem")
            self.menubar.addMenu(system_menu)
            system_menu.installEventFilter(click_filter)
            def special_find_in():
                #The second argument is raw, so that single backslashes work for windows paths
                self.repl.setText('find_in_files("",r"directory",case_sensitive=False,search_subdirs=True,break_on_find=False)')
                self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                self.repl.setFocus()
                self.repl.setSelection(self.repl.text().index("directory"), len("directory"))
            def special_find_in_with_dialog():
                #The second argument is raw, so that single backslashes work for windows paths
                self.repl.setText('find_in_files("",case_sensitive=False,search_subdirs=True,break_on_find=False)')
                self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                self.repl.setFocus()
                self.repl.setCursorPosition(self.repl.text().find('",case_sensitive'))
            self.menubar_functions["special_find_in_with_dialog"] = special_find_in_with_dialog
            temp_string = 'Find all the files in a directory/subdirectories '
            temp_string += 'that contain the search string'
            find_in_files_action = create_action(
                'Find in files',
                settings.Keys.find_in_files, 
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
                settings.Keys.find_files, 
                temp_string, 
                'tango_icons/system-find-files.png', 
                special_find_file
            )
            def special_replace_in_files():
                #The second argument is raw, so that single backslashes work for windows paths
                temp_string = 'replace_in_files("search_text","replace_text",'
                temp_string += 'r"directory",case_sensitive=False,search_subdirs=True)'
                self.repl.setText(temp_string)
                self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                self.repl.setFocus()
                self.repl.setSelection(self.repl.text().index("directory"), len("directory"))
            def special_replace_in_files_with_dialog():
                #The second argument is raw, so that single backslashes work for windows paths
                temp_string = 'replace_in_files("search_text","replace_text",'
                temp_string += 'case_sensitive=False,search_subdirs=True)'
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
                settings.Keys.replace_in_files, 
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
                settings.Keys.cwd_tree, 
                'Create a node tree for the current working directory (CWD)', 
                'tango_icons/system-show-cwd-tree.png', 
                create_cwd_tree
            )
            def show_explorer():
                self.system.show_explorer()
            show_explorer_action = create_action(
                'Show current working directory explorer',
                settings.Keys.cwd_explorer, 
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
                file_explorer = self.upper_window.tree_add_tab(
                    "FILE EXPLORER", TreeExplorer
                )
                file_explorer.display_directory(os.getcwd())
                file_explorer.open_file_signal.connect(self.open_file)
                file_explorer.icon_manipulator.set_icon(
                    file_explorer,
                    functions.create_icon(
                        'tango_icons/system-show-cwd-tree-blue.png'
                    )
                )
                self.upper_window.setCurrentWidget(file_explorer)
            show_new_explorer_tree_action = create_action(
                'Show current working directory in tree explorer',
                settings.Keys.new_cwd_tree, 
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
            view_menu = Menu("&View")
            self.menubar.addMenu(view_menu)
            view_menu.installEventFilter(click_filter)
            #Show/hide the function wheel
            function_wheel_toggle_action = create_action(
                'Show/Hide Function Wheel',
                settings.Keys.function_wheel_toggle, 
                'Show/hide the Ex.Co. function wheel', 
                data.application_icon, 
                self.view.toggle_function_wheel
            )
            #Maximize/minimize entire Ex.Co. window
            maximize_window_action = create_action(
                'Maximize/Normalize',
                settings.Keys.maximize_window, 
                'Maximize/Normalize application window', 
                'tango_icons/view-fullscreen.png', 
                self.view.toggle_window_size
            )
            def focus_main_window():
                self.view.set_window_focus("main")
            main_focus_action = create_action(
                'Focus Main window',
                settings.Keys.main_focus, 
                'Set focus to the Main editing window', 
                'tango_icons/view-focus-main.png', 
                focus_main_window
            )
            def focus_upper_window():
                self.view.set_window_focus("upper")
            upper_focus_action = create_action(
                'Focus Upper window',
                settings.Keys.upper_focus, 
                'Set focus to the Upper editing window', 
                'tango_icons/view-focus-upper.png', 
                focus_upper_window
            )
            def focus_lower_window():
                self.view.set_window_focus("lower")
            lower_focus_action = create_action(
                'Focus Lower window',
                settings.Keys.lower_focus, 
                'Set focus to the Lower editing window', 
                'tango_icons/view-focus-lower.png', 
                focus_lower_window
            )
            toggle_log_action = create_action(
                'Show/Hide Log Window',
                settings.Keys.toggle_log, 
                'Toggle the display of the log window', 
                'tango_icons/view-log.png', 
                self.view.toggle_log_window
            )
            spin_clockwise_action = create_action(
                'Spin view clockwise',
                settings.Keys.spin_clockwise, 
                'Spin the editor windows clockwise', 
                'tango_icons/view-spin-clock.png', 
                self.view.spin_widgets_clockwise
            )
            spin_counterclockwise_action = create_action(
                'Spin view counter-clockwise',
                settings.Keys.spin_counterclockwise, 
                'Spin the editor windows counter-clockwise', 
                'tango_icons/view-spin-counter.png', 
                self.view.spin_widgets_counterclockwise
            )
            toggle_mode_action = create_action(
                'Toggle window mode',
                settings.Keys.toggle_mode, 
                'Toggle between one and three window display', 
                'tango_icons/view-toggle-window-mode.png', 
                self.view.toggle_window_mode
            )
            toggle_main_window_side_action = create_action(
                'Toggle main window side',
                settings.Keys.toggle_main_window_side, 
                'Toggle which side the main window is on', 
                'tango_icons/view-toggle-window-side.png', 
                self.view.toggle_main_window_side
            )
            def select_tab_right():
                try:
                    self.get_window_by_child_tab().select_tab(data.Direction.RIGHT)
                except:
                    pass
            select_tab_right_action = create_action(
                'Select tab right',
                settings.Keys.select_tab_right, 
                'Select one tab to the right in the currently selected window', 
                'tango_icons/view-select-tab-right.png', 
                select_tab_right
            )
            def select_tab_left():
                try:
                    self.get_window_by_child_tab().select_tab(data.Direction.LEFT)
                except:
                    pass
            select_tab_left_action = create_action(
                'Select tab left',
                settings.Keys.select_tab_left, 
                'Select one tab to the left in the currently selected window', 
                'tango_icons/view-select-tab-left.png', 
                select_tab_left
            )
            def move_tab_right():
                try:
                    self.get_window_by_child_tab().move_tab(data.Direction.RIGHT)
                except:
                    pass
            move_tab_right_action = create_action(
                'Move tab right',
                settings.Keys.move_tab_right, 
                'Move the current tab in the currently selected window one position to the right', 
                'tango_icons/view-move-tab-right.png', 
                move_tab_right
            )
            def move_tab_left():
                try:
                    self.get_window_by_child_tab().move_tab(data.Direction.LEFT)
                except:
                    pass
            move_tab_left_action = create_action(
                'Move tab left',
                settings.Keys.move_tab_left, 
                'Move the current tab in the currently selected window one position to the left', 
                'tango_icons/view-move-tab-left.png', 
                move_tab_left
            )
            def show_edge():
                try:
                    self.get_tab_by_focus().edge_marker_toggle()
                except:
                    pass
            toggle_edge_action = create_action(
                'Toggle edge marker',
                settings.Keys.toggle_edge, 
                'Toggle the display of the edge marker that shows the prefered maximum chars in a line', 
                'tango_icons/view-edge-marker.png', 
                show_edge
            )
            def reset_zoom():
                try:
                    self.get_tab_by_focus()._parent.zoom_reset()
                except:
                    pass
            reset_zoom_action = create_action(
                'Zoom reset',
                settings.Keys.reset_zoom, 
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
                    pass
            def bookmark_toggle():
                try:
                    self.get_tab_by_focus().bookmarks.toggle()
                except:
                    pass
            bookmark_menu = Menu("&Bookmarks")
            view_menu.addMenu(bookmark_menu)
            bookmark_menu.installEventFilter(click_filter)
            temp_icon = functions.create_icon('tango_icons/bookmarks.png')
            bookmark_menu.setIcon(temp_icon)
            bookmark_toggle_action = create_action(
                'Toggle Bookmark',
                settings.Keys.bookmark_toggle, 
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
            bookmark_goto_menu = Menu("Go To")
            bookmark_menu.addMenu(bookmark_goto_menu)
            bookmark_goto_menu.installEventFilter(click_filter)
            temp_icon = functions.create_icon('tango_icons/bookmarks-goto.png')
            bookmark_goto_menu.setIcon(temp_icon)
            bookmark_store_menu = Menu("Store")
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
#                    getattr(settings.Keys, "bookmark_goto_{}".format(i)),
                    settings.Keys.bookmark_goto[i],
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
#                    getattr(settings.Keys, "bookmark_store_{}".format(i)),
                    settings.Keys.bookmark_store[i],
                    "Store bookmark number:{:d}".format(i), 
                    'tango_icons/bookmarks-store.png', 
                    create_store_bookmark()
                )
                bookmark_store_menu.addAction(bookmark_store_action)
            def toggle_line_endings():
                try:
                    self.get_tab_by_focus().toggle_line_endings()
                except:
                    pass
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
                    pass
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
            view_menu.addAction(maximize_window_action)
            view_menu.addAction(main_focus_action)
            view_menu.addAction(upper_focus_action)
            view_menu.addAction(lower_focus_action)
            view_menu.addAction(toggle_log_action)
            view_menu.addAction(spin_clockwise_action)
            view_menu.addAction(spin_counterclockwise_action)
            view_menu.addAction(toggle_mode_action)
            view_menu.addAction(toggle_main_window_side_action)
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
            repl_menu = Menu("&REPL")
            self.menubar.addMenu(repl_menu)
            repl_menu.installEventFilter(click_filter)
            repeat_eval_action = create_action(
                'REPL Repeat Command',
                settings.Keys.repeat_eval, 
                'Repeat the last REPL command', 
                'tango_icons/repl-repeat-command.png', 
                self.repl.repeat_last_repl_eval
            )
            def repl_single_focus():
                self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                self.repl.setFocus()
            repl_focus_action = create_action(
                'Focus REPL(Single)',
                [settings.Keys.repl_focus_single_1, settings.Keys.repl_focus_single_2], 
                'Set focus to the Python REPL(Single Line)', 
                'tango_icons/repl-focus-single.png', 
                repl_single_focus
            )
            def repl_multi_focus():
                self.view.set_repl_type(data.ReplType.MULTI_LINE)
                self.repl_helper.setFocus()
            repl_focus_multi_action = create_action(
                'Focus REPL(Multi)',
                settings.Keys.repl_focus_multi, 
                'Set focus to the Python REPL(Multi Line)', 
                'tango_icons/repl-focus-multi.png', 
                repl_multi_focus
            )
            repl_menu.addAction(repeat_eval_action)
            repl_menu.addAction(repl_focus_action)  
            repl_menu.addAction(repl_focus_multi_action)
        #Sessions menu
        def construct_sessions_menu():
            sessions_menu = Menu("Sessions")
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
            self.sessions_menu = Menu("Sessions")
            self.sessions_menu.setIcon(functions.create_icon('tango_icons/sessions.png'))
            sessions_menu.addAction(add_session_action)
            sessions_menu.addAction(remove_session_action)
            sessions_menu.addAction(session_editor_action)
            sessions_menu.addSeparator()
            sessions_menu.addMenu(self.sessions_menu)
        # Settings menu
        def construct_settings_menu():
            settings_menu = Menu("Settings")
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
            help_menu = Menu("&Help")
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
    
    def _init_basic_widgets(self):
        """Initialize the three widgets that are used for displaying data"""
        #Initialize and add child controls to main_window(QTabControl)
        self.main_window = BasicWidget(self)
        self.main_window.setTabShape(data.QTabWidget.Rounded)
        #Initialize and add child controls to lower_window(QTabControl)
        self.upper_window = BasicWidget(self)
        #Initialise and add child controls to lower_window(QTabControl)
        self.lower_window = BasicWidget(self)
    
    def _init_repl(self):
        """Initialize everything that concerns the REPL"""
        # Initialize the groupbox that the REPL will be in, and place the REPL widget into it
        self.repl_box = ReplBox(self, self.get_form_references())
        # Initialize the Python REPL widget
        self.repl = self.repl_box.repl
        self.repl_helper = self.repl_box.repl_helper
    
    def _init_interpreter(self):
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
            if reply == data.QMessageBox.Yes:
                functions.create_default_config_file()
                self.display.repl_display_message(
                    "Default user definitions file generated!", 
                    message_type=data.MessageType.SUCCESS
                )
            return
        user_file = open(user_file_path, "r", encoding="utf-8")
        user_code = user_file.read()
        user_file.close()
        result = self.repl._repl_eval(user_code, display_action=False)
        if result != None:
            self.display.repl_display_message(
                "ERROR IN USER CONFIGURATION FILE:\n" + result, 
                message_type=data.MessageType.ERROR
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
            components.TheSquid.update_styles()
            
            # Display the successful import
            self.display.write_to_statusbar("User functions imported successfully!")
        except:
            message = "!! Error importing user functions !!"
            self.display.repl_display_error(
                "{}\n{}".format(traceback.format_exc(), message)
            )
            self.display.write_to_statusbar(message)
    
    def _reset_interpreter(self):
        new_references, ac_list_prim, ac_list_sec = self.get_references_autocompletions()
        # Initialize and set auto completer
        self.repl.interpreter_reset_references(new_references, ac_list_prim, ac_list_sec)
        # Reimport the user functions
        self.import_user_functions()
        # Display interpreter reset success
        self.display.write_to_statusbar("REPL interpreter references successfully updated", 2000)

    def create_new(self, tab_name=None, basic_widget=None):
        """Creates an empty scintilla document using a generator counter"""
        #Set the new tab name
        if tab_name == None:
            tab_name = "new_" + str(next(self.new_file_count))
        #Create the new scintilla document in the selected basic widget 
        return_widget = None
        if basic_widget == None:
            return_widget = self.main_window.editor_add_document(tab_name, type="new")
        else:
            return_widget = basic_widget.editor_add_document(tab_name, type="new")
        #Set focus to the new widget
        return_widget.setFocus()
        #Return the widget reference
        return return_widget

    def open_file_with_dialog(self, basic_widget=None):
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
        # Check and then add the selected file to the main BasicWidget if the window parameter is unspecified
        self.open_files(files, basic_widget)
    
    def open_files(self, files=None, basic_widget=None):
        """Cheach and read valid files to the selected BasicWidget"""
        #Check if the files are valid
        if files == None or files == "":
            return
        if isinstance(files,  str):
            #Single file
            self.open_file(files, basic_widget)
        else:
            #List of files
            for file in files:
                self.open_file(file, basic_widget)

    def open_file(self, file=None, basic_widget=None):
        """
        Read file contents into a BasicWidget
        """
        def open_file_function(in_file, basic_widget):
            #Check if file exists
            if os.path.isfile(in_file) == False:
                self.display.repl_display_message(
                    "File: {}\ndoesn't exist!".format(in_file), 
                    message_type=data.MessageType.ERROR
                )
                return
            #Check the file size
            file_size = functions.get_file_size_Mb(in_file)
            if file_size  > 50:
                #Close the log window if it is displayed
                self.view.set_log_window(False)
                #Create the warning message
                warning =   "The file is larger than 50 MB! ({:d} MB)\n".format(int(file_size))
                warning +=  "A lot of RAM will be needed!\n"
                warning +=  "Files larger than 300 MB can cause the system to hang!\n"
                warning +=  "Are you sure you want to open it?"
                reply = YesNoDialog.warning(warning)
                if reply == data.QMessageBox.No:
                    return
            #Check selected window
            if basic_widget == None:
                basic_widget = self.main_window
            #Check if file is already open
            index = self.check_open_file(in_file, basic_widget)
            if index != None:
                basic_widget.setCurrentIndex(index)
                return
            #Add new scintilla document tab to the basic widget
            new_tab = basic_widget.editor_add_document(in_file, "file", bypass_check=False)
            #Set the icon if it was set by the lexer
            new_tab.icon_manipulator.update_icon(new_tab)
                
            if new_tab != None:
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
                except MemoryError:
                    message = "Insufficient memory to open the file!"
                    self.display.repl_display_message(message, message_type=data.MessageType.ERROR)
                    self.display.write_to_statusbar(message)
                    basic_widget.widget(basic_widget.currentIndex()).setParent(None)
                    basic_widget.removeTab(basic_widget.currentIndex())
                    return None
                except:
                    message = "Unexpected error occured while opening file!"
                    self.display.repl_display_message(message, message_type=data.MessageType.ERROR)
                    self.display.write_to_statusbar(message)
                    basic_widget.widget(basic_widget.currentIndex()).setParent(None)
                    basic_widget.removeTab(basic_widget.currentIndex())
                    return None
                #Reset the changed status of the current tab, 
                #because adding the file content line by line was registered as a text change
                basic_widget.reset_text_changed()
                #Update the settings manipulator with the new file
                self.settings.update_recent_list(in_file)
                #Update the current working directory
                path = os.path.dirname(in_file)
                if path == "":
                    path = data.application_directory
                self.set_cwd(path)
                data.print_log("Opened file: " + str(in_file))
                #Set focus to the newly opened document
                basic_widget.currentWidget().setFocus()
                #Update the Save/SaveAs buttons in the menubar
                self.set_save_file_state(True)
                return new_tab
            else:
                message = "File cannot be read!\n"
                message += "It's probably not a text file!"
                self.display.repl_display_message(
                    message, message_type=data.MessageType.ERROR
                )
                self.display.write_to_statusbar("File cannot be read!", 3000)
            return None
        if isinstance(file, str) == True:
            if file != "":
                new_tab = open_file_function(file, basic_widget)
                self.repaint()
                data.QCoreApplication.processEvents()
                return new_tab
        elif isinstance(file, list) == True:
            tabs = []
            for f in file:
                new_tab = open_file_function(f, basic_widget)
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
            
    
    def check_open_file(self, file_with_path, basic_widget):
        """Check if a file is already open in one of the windows"""
        found_index = None
        #Change the Windows style path to the Unix style
        file_with_path = file_with_path.replace("\\", "/")
        #Loop through all of the documents in the basic widget
        for i in range(basic_widget.count()):
            #Check the file name and file name with path
            if (basic_widget.widget(i).name == os.path.basename(file_with_path) and 
                basic_widget.widget(i).save_name == file_with_path):
                #If the file is already open, get its index in the tab widget
                found_index = i
                break
        return found_index
    
    def close_all_tabs(self):
        """Clear all documents from the main and upper window"""
        #Check if there are any modified documents
        if self.check_document_states() == True:
            #Close the log window if it is displayed
            self.view.set_log_window(False)
            message = "You have modified documents!\nClose all tabs?"
            reply = YesNoDialog.question(message)
            if reply == data.QMessageBox.No:
                return
        #Close all tabs and remove all bookmarks from them
        for i in range(self.main_window.count()):
            if isinstance(self.main_window.widget(0), CustomEditor):
                self.bookmarks.remove_editor_all(self.main_window.widget(0))
            self.main_window.close_tab(0, force=True)
        for i in range(self.upper_window.count()):
            if isinstance(self.upper_window.widget(0), CustomEditor):
                self.bookmarks.remove_editor_all(self.upper_window.widget(0))
            self.upper_window.close_tab(0, force=True)
        for i in range(self.lower_window.count()):
            if isinstance(self.lower_window.widget(0), CustomEditor):
                self.bookmarks.remove_editor_all(self.lower_window.widget(0))
            self.lower_window.close_tab(0, force=True)
        # Force a garbage collection cycle
        gc.collect()
    
    def close_window_tabs(self, basic_widget, widget):
        """
        Clear all other documents except the selected one
        in a specified basic widget
        """
        #Check if there are any modified documents
        if self.check_document_states(basic_widget) == True:
            #Close the log window if it is displayed
            self.view.set_log_window(False)
            message = "You have modified documents!\nClose all tabs?"
            reply = YesNoDialog.question(message)
            if reply == data.QMessageBox.No:
                return
        #Close all tabs and remove all bookmarks from them
        clear_index = 0
        for i in range(basic_widget.count()):
            if basic_widget.widget(clear_index) == widget:
                clear_index += 1
                continue
            if isinstance(basic_widget.widget(clear_index), CustomEditor):
                self.bookmarks.remove_editor_all(basic_widget.widget(clear_index))
            basic_widget.close_tab(clear_index, force=True)
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
        windows =[self.main_window, self.upper_window, self.lower_window]
        #Loop through all the basic widgets/windows and check the tabs
        for window in windows:
            for i in range(0, window.count()):
                if window.tabText(i) == tab_name:
                    return window.widget(i)
        #Tab was not found
        return None
    
    def get_tab_by_string_in_name(self, string):
        """Find a tab with 'string' in its name in the basic widgets"""
        windows =[self.main_window, self.upper_window, self.lower_window]
        #Loop through all the basic widgets/windows and check the tabs
        for window in windows:
            for i in range(0, window.count()):
                if string in window.tabText(i):
                    return window.widget(i)
        #Tab was not found
        return None
    
    def get_tab_by_focus(self):
        """Find the focused tab"""
        windows =[self.main_window, self.upper_window, self.lower_window]
        #Loop through all the basic widgets/windows and check the tab focus
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
        #No tab in the basic widgets has focus
        return None
    
    def get_current_tab_by_parent_name(self, window_name):
        """Find the current tab by the parent BasicWidget name property"""
        widget = None
        if window_name == None:
            widget  = self.main_window.currentWidget()
        elif window_name == "Main":
            widget  = self.main_window.currentWidget()
        elif window_name == "Upper":
            widget = self.upper_window.currentWidget()
        elif window_name == "Lower":
            widget = self.lower_window.currentWidget()
        return widget
    
    def get_used_tab(self):
        """Get the tab that was last used (if none return the main tab)"""
        focused_tab = self.get_tab_by_focus()
        #Check if any tab is focused
        if focused_tab == None:
            focused_tab = self.main_window.currentWidget()
        return focused_tab
    
    def get_window_by_focus(self):
        """Get the basic widget by focus"""
        windows =[self.main_window, self.upper_window, self.lower_window]
        #Loop through all the basic widgets/windows and check their focus
        for window in windows:
            if window.hasFocus() == True:
                return window
        #No tab in the basic widgets has focus
        return None
    
    def get_window_by_name(self, window_name=None):
        """Get the basic widget by name"""
        window = None
        if window_name == None:
            window = self.main_window
        elif window_name.lower() == "main":
            window = self.main_window
        elif window_name.lower() == "upper":
            window = self.upper_window
        elif window_name.lower() == "lower":
            window = self.lower_window
        return window
    
    def get_window_by_child_tab(self):
        """
        Find the focused window by it's currently focused child tab
        (Same as get_tab_by_focus but returns the window instead of the tab)
        """
        windows =[self.main_window, self.upper_window, self.lower_window]
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
    
    def check_document_states(self, basic_widget=None):
        """Check if there are any modified documents in the editor windows"""
        # Nested function for checking modified documents in a single basic widget
        # (just to play with nested functions)
        def check_documents_in_window(window):
            if window.count() > 0:
                for i in range(0, window.count()):
                    if window.widget(i).savable == data.CanSave.YES:
                        if window.widget(i).save_status == data.FileStatus.MODIFIED:
                            return True
            return False
        if basic_widget is None:
            # Check all widget in all three windows for changes
            if (check_documents_in_window(self.main_window) == True or
                check_documents_in_window(self.upper_window) == True or
                check_documents_in_window(self.lower_window) == True):
                # Modified document found
                return True
            else:
                # No changes found
                return False
        else:
            return check_documents_in_window(basic_widget)

    def exit(self, event=None):
        """Exit application"""
        #Close the MainWindow
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
            """Initialization of the Settings object instance"""
            # Get the reference to the MainWindow parent object instance
            self._parent = parent
            # Initialize the Ex.Co. settings object with the current working directory
            self.manipulator = settings.SettingsFileManipulator()
        
        def update_recent_list(self, new_file=None):
            """Update the settings manipulator with the new file"""
            # Nested function for opening the recent file
            def new_file_function(file):
                try:
                    self._parent.open_file(file=file, basic_widget=None)
                    self._parent.main_window.currentWidget().setFocus()
                except:
                    pass
            # Update the file manipulator
            if new_file != None:
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
    
        def restore(self):
            """Restore the previously stored settings"""
            # Load the settings from the initialization file
            result = self.manipulator.load_settings()
            # Set main window side
            self._parent.view.set_main_window_side(
                self.manipulator.main_window_side
            )
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
                self._parent.view.main_window_side, 
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

        def add(self, session_name, session_group=None):
            """Add the current opened documents in the main and upper window"""
            # Check if the session name is too short
            if len(session_name) < 3:
                self._parent.display.repl_display_message(
                    "Session name is too short!", 
                    message_type=data.MessageType.ERROR
                )
                return
            if session_group != None:
                if (isinstance(session_group, str) == False and
                    isinstance(session_group, tuple) == False and
                    isinstance(session_group, list) == False):
                    self._parent.display.repl_display_message(
                        "Group name must be a string or a tuple/list of strings!", 
                        message_type=data.MessageType.ERROR
                    )
                    return
            # Create lists of files in each window
            try:
                main = self.get_window_data("main")
                upper = self.get_window_data("upper")
                lower = self.get_window_data("lower")
                if (main["files"] != [] or upper["files"] != []):
                    # Check if the session is already stored
                    session_found = False
                    for ssn in self._parent.settings.manipulator.stored_sessions:
                        if ssn.name == session_name and ssn.group == session_group:
                            session_found = True
                            break
                    # Store the session
                    self._parent.settings.manipulator.add_session(
                        session_name,
                        session_group,
                        main,
                        upper,
                        lower
                    )
                    # Session added successfully
                    if session_group == None:
                        session_group = ""
                    group_string = ""
                    if session_group != "":
                        group_string = "/".join(session_group) + "/"
                    if session_found == True:
                        message = "Session '{}{}' overwritten!".format(
                            group_string, session_name
                        )
                    else:
                        message = "Session '{}{}' added!".format(
                            group_string, session_name
                        )
                    self._parent.display.repl_display_message(
                        message, 
                        message_type=data.MessageType.SUCCESS
                    )
                else:
                    self._parent.display.repl_display_message(
                        "No documents to store!", 
                        message_type=data.MessageType.ERROR
                    )
                    self._parent.display.write_to_statusbar("No documents to store!", 1500)
                # Refresh the sessions menu in the menubar
                self.update_menu()
            except Exception as ex:
                traceback.print_exc()
                message = "Invalid document types in the main or upper window!"
                self._parent.display.repl_display_message(
                    message, 
                    message_type=data.MessageType.ERROR
                )
                self._parent.display.write_to_statusbar(message, 1500)

        def restore(self, session_name, session_group=None):
            """Restore the files as stored in the selected session"""
            #Check if there are any modified documents
            if self._parent.check_document_states() == True:
                #Close the log window if it is displayed
                self._parent.view.set_log_window(False)
                message =  "You have modified documents!\n"
                message += "Restore session '{}' anyway?".format(session_name)
                reply = YesNoDialog.question(message)
                if reply == data.QMessageBox.No:
                    return
            #Find the session
            session = self._parent.settings.manipulator.get_session(
                session_name,
                session_group
            )
            #Check if session was found
            if session != None:
                #Clear all documents from the main and upper window
                self._parent.close_all_tabs()
                # Add files to windows
                restore_data = (
                    ("Upper window files", self._parent.upper_window),
                    ("Lower window files", self._parent.lower_window),
                    ("Main window files", self._parent.main_window),
                )
                for name,window in restore_data:
                    for item in session.storage[name]["files"]:
                        try:
                            if isinstance(item, str):
                                file = item
                                self._parent.open_file(file, window)
                                
                            elif isinstance(item, dict):
                                file = item["path"]
                                line = item["line"]
                                index = item["index"]
                                first_visible_line = item["first-visible-line"]
                                tab = self._parent.open_file(file, window)
                                tab.setCursorPosition(line, index)
                                tab.setFirstVisibleLine(first_visible_line)
                            else:
                                raise Exception(
                                    "Unknown type of session item: ".format(
                                        item.__class__
                                    )
                                )
                        except:
                            traceback.print_exc()
                            self._parent.display.repl_display_message(
                                "Could not find upper session item:\n{}".format(
                                    pprint.pformat(item)
                                ),
                                message_type=data.MessageType.ERROR
                            )
                    if window.count() > 0:
                        window.setCurrentIndex(session.storage[name]["current-index"])
            else:
                #Session was not found
                if session_group == None:
                    session_group = ""
                group_string = ""
                if session_group != "":
                    group_string = "/".join(session_group) + "/"
                message = "Session '{}{}' was not found!".format(
                    group_string, session_name
                )
                self._parent.display.repl_display_message(
                    message, 
                    message_type=data.MessageType.ERROR
                )
                self._parent.display.write_to_statusbar(message, 1500)
        
        def exco_restore(self):
            """Open all the source files for Ex.Co."""
            #Check if there are any modified documents
            if self._parent.check_document_states() == True:
                #Close the log window if it is displayed
                self._parent.view.set_log_window(False)
                message =  "You have modified documents!\n"
                message += "Restore Ex.Co development session anyway?"
                reply = YesNoDialog.question(message)
                if reply == data.QMessageBox.No:
                    return
            #Clear all documents from the main and upper window
            self._parent.main_window.clear()
            self._parent.upper_window.clear()
            #Loop through the aplication directory and add the relevant files
            exco_main_files = []
            exco_dir = self._parent.settings.manipulator.application_directory
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
            #Sort the files by name
            exco_main_files.sort()
            #Add the files to the main window
            for file in exco_main_files:
                self._parent.open_file(file, self._parent.main_window)

        def remove(self, session_name, session_group=None):
            """Delete the session"""
            result = self._parent.settings.manipulator.remove_session(
                session_name, 
                session_group
            )
            #Adjust the group name string
            if session_group == None:
                session_group = ""
            group_string = ""
            if session_group != "":
                group_string = "/".join(session_group) + "/"
            if result == False:
                #Session was not found
                message = "Session '{}{}' was not found!".format(
                    group_string, session_name
                )
                self._parent.display.repl_display_message(
                    message, 
                    message_type=data.MessageType.ERROR
                )
                self._parent.display.write_to_statusbar(message, 1500)
            else:
                #Session was removed successfully
                message = "Session '{}{}' was removed!".format(
                    group_string, session_name
                )
                self._parent.display.repl_display_message(
                    message, 
                    message_type=data.MessageType.WARNING
                )
            #Refresh the sessions menu in the menubar
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
            # Create a list of groups that will be stored for reuse
            groups = self._parent.settings.manipulator.get_sorted_groups()
            # Create the Sessions menu
            main_group = self._parent.settings.manipulator.Group(
                "BASE", parent=None, reference=self._parent.sessions_menu
            )
            for group in groups:
                current_node = main_group
                for folder in group:
                    new_group = current_node.subgroup_get(folder)
                    if new_group == None:
                        new_group = Menu(folder)
                        current_node.reference.addMenu(new_group)
                        new_group.setIcon(functions.create_icon('tango_icons/folder.png'))
                    current_node = current_node.subgroup_create(folder, new_group)
            # Loop through all of the stored sessions and add them
            for session in self._parent.settings.manipulator.stored_sessions:
                # Add the session
                new_session_action = data.QAction(session.name, self._parent)
                new_session_action.setStatusTip("Restore Session: {}".format(session.name))
                new_session_method = functools.partial(
                    self.restore,
                    session_name=session.name,
                    session_group=session.group
                )
                new_session_action.setIcon(functions.create_icon('tango_icons/sessions.png'))
                new_session_action.triggered.connect(new_session_method)
                # Check if the session is in a group
                if session.group != None:
                    group = main_group.subgroup_get_recursive(session.group)
                    group.reference.addAction(new_session_action)
                else:
                    main_group.reference.addAction(new_session_action)
        
        def get_window_documents(self, window_name):
            """Return all the editor document paths in the selected window as a list"""
            window = self._parent.get_window_by_name(window_name)
            documents = [window.widget(i).save_name 
                            for i in range(window.count()) 
                                if  window.widget(i).savable == data.CanSave.YES and
                                    window.widget(i).save_name != ""]
            return documents
        
        def get_window_data(self, window_name):
            """Return all the editor document paths in the selected window as a list"""
            window = self._parent.get_window_by_name(window_name)
            window_data = {
                "current-index": window.currentIndex(),
                "files": [],
            }
            for i in range(window.count()):
                if window.widget(i).savable == data.CanSave.YES and \
                   window.widget(i).save_name != "":
                    w = window.widget(i)
                    line, index = w.getCursorPosition()
                    new_data = {
                        "path": w.save_name,
                        "line": line,
                        "index": index,
                        "first-visible-line": w.firstVisibleLine(),
                    }
                    window_data["files"].append(new_data)
            return window_data
    
    
    class View:
        """
        Functions for manipulating the application appearance
        (namespace/nested class to MainWindow)
        """
        #Class varibles
        _parent                  = None
        #Default widths and heights of the windows
        vertical_width_1        = 2/3
        vertical_width_2        = 1/3
        horizontal_width_1      = 2/3
        horizontal_width_2      = 1/3
        main_relation           = 55
        #Window mode: ONE or THREE
        window_mode             = data.WindowMode.THREE
        #Attribute that stores which side the main window is on
        main_window_side        = data.MainWindowSide.LEFT
        #Overlay helper widget that will be displayed on top of the main groupbox
        function_wheel_overlay  = None
        #Last executed functions text on the function wheel
        last_executed_function_text  = None
        #Function wheel overlay minimum size
        FUNCTION_WHEEL_BOUNDS   = (0, 0)
        #Stored REPL single/multi line state
        repl_state              = None
        #Lock used when spinning widgets, so the layout does not get saved mid-spin
        layout_save_block       = False
        
        def __init__(self, parent):
            """Initialization of the View object instance"""
            #Get the reference to the MainWindow parent object instance
            self._parent = parent
            #Get the function wheel overlay image size
            function_wheel_size = data.QPixmap(
                FunctionWheel.create_background_image()
            ).size()
            self.FUNCTION_WHEEL_BOUNDS = (
                function_wheel_size.width(), 
                function_wheel_size.height()
            )
            #Initialize the REPL state to unknown, so it will force
            #the form layout to refresh it
            self.repl_state = None
        
        def refresh_layout(self, window_mode, main_window_side):
            """Refresh all widgets to the initial dimensions"""
            #Check which window mode is active
            if window_mode == data.WindowMode.THREE:
                #Set vertical and horizontal splitter heights
                if main_window_side == data.MainWindowSide.LEFT:
                    self._parent.vertical_splitter.setSizes(
                        [self._parent.vertical_splitter.width()*self.vertical_width_1, 
                         self._parent.vertical_splitter.width()*self.vertical_width_2]
                    )
                    self._parent.horizontal_splitter.setSizes(
                        [self._parent.horizontal_splitter.width()*self.horizontal_width_1, 
                         self._parent.horizontal_splitter.width()*self.horizontal_width_2]
                    )
                elif main_window_side   == data.MainWindowSide.RIGHT:
                    self._parent.vertical_splitter.setSizes(
                        [self._parent.vertical_splitter.width()*self.vertical_width_1, 
                         self._parent.vertical_splitter.width()*self.vertical_width_2]
                    )
                    self._parent.horizontal_splitter.setSizes(
                        [self._parent.horizontal_splitter.width()*self.horizontal_width_2, 
                         self._parent.horizontal_splitter.width()*self.horizontal_width_1]
                    )
            #Set the REPL font
            self._parent.repl.setFont(data.QFont("Arial", 12, data.QFont.Bold))
            #Refresh the size relation between the basic widgets and the REPL,
            #so that the REPL height is always the same
            self.refresh_main_splitter()
        
        def save_layout(self):
            """Save the widths of the splitters"""
            #Check if the splitters are filled correctly
            if self.layout_save_block == True:
                return
            if self._parent.vertical_splitter.count() < 2 or self._parent.horizontal_splitter.count() < 2:
                return
            #Check which window mode is active
            if (self._parent.window_mode == data.WindowMode.THREE and
                self._parent.vertical_splitter.height() > 0 and
                self._parent.horizontal_splitter.width() > 0):
                self.vertical_width_1   = (self._parent.vertical_splitter.sizes()[0] / 
                                           self._parent.vertical_splitter.height())
                self.vertical_width_2   = (self._parent.vertical_splitter.sizes()[1] / 
                                           self._parent.vertical_splitter.height())
                #Save the horizontal positions according to the main window side
                if self.main_window_side    == data.MainWindowSide.LEFT:
                    self.horizontal_width_1     = (self._parent.horizontal_splitter.sizes()[0] / 
                                                   self._parent.horizontal_splitter.width())
                    self.horizontal_width_2     = (self._parent.horizontal_splitter.sizes()[1] / 
                                                   self._parent.horizontal_splitter.width())
                elif self.main_window_side  == data.MainWindowSide.RIGHT:
                    self.horizontal_width_1     = (self._parent.horizontal_splitter.sizes()[1] / 
                                                   self._parent.horizontal_splitter.width())
                    self.horizontal_width_2     = (self._parent.horizontal_splitter.sizes()[0] / 
                                                   self._parent.horizontal_splitter.width())
        
        def set_basic_widgets(self, 
                              main_widget, 
                              upper_widget, 
                              lower_widget, 
                              show_overlay=False):
            """
            Create new QSplitters, add basic widgets to these splitters and
            put the QSplitters on the main form
            """
            #Save the currently focused widget
            focused_widget  = self._parent.get_window_by_child_tab()
            focused_tab     = self._parent.get_tab_by_focus()
            if focused_widget == None:
                focused_widget = self._parent.get_window_by_focus()
            #Store the last focused tab
            self._parent.last_focused_tab = focused_tab
            #Create QSplitters to split main window into three parts: 
            #editing(QScintilla), upper_window(QTabControl), lower_window(QTabControl)
            vertical_splitter      = data.QSplitter(data.Qt.Vertical)
            vertical_splitter.setObjectName("Vertical_Splitter")
            horizontal_splitter    = data.QSplitter(data.Qt.Horizontal)
            horizontal_splitter.setObjectName("Horizontal_Splitter")
            main_splitter          = data.QSplitter(data.Qt.Vertical)
            main_splitter.setObjectName("Main_Splitter")
            #Set new widget order to class attributes
            main_widget.name    = "Main"
            upper_widget.name   = "Upper"
            lower_widget.name   = "Lower"
            main_widget.setObjectName("Main")
            upper_widget.setObjectName("Upper")
            lower_widget.setObjectName("Lower")
            main_window    = main_widget
            upper_window   = upper_widget
            lower_window   = lower_widget
            #Vertically split upper_window and lower_window
            vertical_splitter.addWidget(upper_widget)
            vertical_splitter.addWidget(lower_widget)
            #Horizontally split editing and vertical splitter according to main window side attribute
            if self.main_window_side == data.MainWindowSide.LEFT:
                horizontal_splitter.addWidget(main_widget)
                horizontal_splitter.addWidget(vertical_splitter)
            elif self.main_window_side == data.MainWindowSide.RIGHT:
                horizontal_splitter.addWidget(vertical_splitter)
                horizontal_splitter.addWidget(main_widget)
            #Vertically split edit fields with the REPL
            main_splitter.addWidget(horizontal_splitter)
            main_splitter.addWidget(self._parent.repl_box)
            #Set the window mode attribute to one
            self._parent.window_mode = data.WindowMode.THREE
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
            #Save references to the MainWindow
            self._parent.main_window    = main_window
            self._parent.upper_window   = upper_window
            self._parent.lower_window   = lower_window
            self._parent.vertical_splitter       = vertical_splitter
            self._parent.horizontal_splitter     = horizontal_splitter
            self._parent.main_splitter           = main_splitter
            self._parent.main_groupbox           = main_groupbox
            self._parent.main_groupbox_layout    = main_groupbox_layout
            #Resize the splitters as needed
            self.refresh_layout(self._parent.window_mode, self.main_window_side)
            #Set focus back to the last focused widget
            if focused_widget != None:
                #Store the last focused widget
                self._parent.last_focused_widget = focused_widget
                data.print_log(
                    "Stored \"{}\" as last focused widget".format(focused_widget.name)
                )
                #Set focus to the last focused widget
                if focused_tab != None:
                    focused_tab.setFocus()
                else:
                    focused_widget.setFocus()
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
            if self._parent.settings.gui_manipulator != None:
                self._parent.settings.gui_manipulator.clean_up()
                self._parent.settings.gui_manipulator = None
    
        def set_log_window(self, show=True):
            """Show or hide the log window"""
            if show == True:
                data.logging_mode = True
                data.log_window.show()
            else:
                data.log_window.hide()
            self._parent.activateWindow()
                
        def toggle_log_window(self):
            """Toggle the display of the log window"""
            if data.log_window.isVisible():
                self.set_log_window(False)
            else:
                self.set_log_window(True)
        
        def show_about(self):
            """Show ExCo information"""
            about = ExCoInfo(self._parent, app_dir=self._parent.settings.manipulator.application_directory)
            #The exec_() function shows the dialog in MODAL mode (the parent is unclickable while the dialog is shown)
            about.exec_()
        
        def set_main_window_side(self, main_window_side):
            """Set main window side"""
            #Set the new main window side
            self.main_window_side = main_window_side
            #Refresh the layout
            self.set_basic_widgets(
                main_widget=self._parent.main_window,
                upper_widget=self._parent.upper_window,
                lower_widget=self._parent.lower_window
            )
        
        def spin_basic_widgets(self, direction=data.SpinDirection.CLOCKWISE):
            """
            Spin the three basic widgets clockwise or counter-clockwise using the splitters.
            
            Parameters:
                direction:  0 - clockwise,  1 - counter-clockwise
            """
            self.layout_save_block = True
            #Only spin the widgets if in THREE window mode
            if self.window_mode != data.WindowMode.THREE:
                return
            #Check which side the main window is on and adjust the direction accordigly
            if self.main_window_side == data.MainWindowSide.RIGHT:
                #The main window is on the right side, reverse the spin direction
                if direction == data.SpinDirection.CLOCKWISE:
                    direction = data.SpinDirection.COUNTER_CLOCKWISE
                else:
                    direction = data.SpinDirection.CLOCKWISE
                #Save current positioning
                temp_widget_main    = self._parent.horizontal_splitter.widget(1)
                temp_widget_upper   = self._parent.vertical_splitter.widget(0)
                temp_widget_lower   = self._parent.vertical_splitter.widget(1)
            else:
                #Save current positioning
                temp_widget_main    = self._parent.horizontal_splitter.widget(0)
                temp_widget_upper   = self._parent.vertical_splitter.widget(0)
                temp_widget_lower   = self._parent.vertical_splitter.widget(1)
            #Spin according to direction
            if direction == data.SpinDirection.CLOCKWISE:
                self.set_basic_widgets(
                    main_widget=temp_widget_lower,
                    upper_widget=temp_widget_main,
                    lower_widget=temp_widget_upper
                )
            else:
                self.set_basic_widgets(
                    main_widget=temp_widget_upper,
                    upper_widget=temp_widget_lower,
                    lower_widget=temp_widget_main
                )
            #Update the basic widget references with the new layout
            self._parent.repl.interpreter_update_windows(
                self._parent.main_window, 
                self._parent.upper_window, 
                self._parent.lower_window
            )
            self.layout_save_block = False
            if direction == data.SpinDirection.CLOCKWISE:
                data.print_log("Span view clockwise")
            else:
                data.print_log("Span view counter-clockwise")
        
        def spin_widgets_clockwise(self):
            """Convenience function for use with the menubar and REPL"""
            self.spin_basic_widgets(data.SpinDirection.CLOCKWISE)

        def spin_widgets_counterclockwise(self):
            """Convenience function for use with the menubar and REPL"""
            self.spin_basic_widgets(data.SpinDirection.COUNTER_CLOCKWISE)
        
        def toggle_window_mode(self):
            """Toggle one/three window mode"""
            if self.window_mode     == data.WindowMode.THREE:
                self._parent.upper_window.hide()
                self._parent.lower_window.hide()
                self.window_mode = data.WindowMode.ONE
                #Focus on the main window as the other two windows are hidden
                self.set_window_focus("main")
                self._parent.display.write_to_statusbar("Window mode changed to: ONE", 1000)
            elif self.window_mode   == data.WindowMode.ONE:
                self._parent.upper_window.show()
                self._parent.lower_window.show()
                self.window_mode = data.WindowMode.THREE
                self._parent.display.write_to_statusbar("Window mode changed to: THREE", 1000)
        
        def toggle_main_window_side(self):
            """Toggle main window side"""
            if self.window_mode == data.WindowMode.THREE:
                if self.main_window_side == data.MainWindowSide.LEFT:
                    self.set_main_window_side(data.MainWindowSide.RIGHT)
                elif self.main_window_side == data.MainWindowSide.RIGHT:
                    self.set_main_window_side(data.MainWindowSide.LEFT)
        
        def set_window_focus(self, window):
            """Set focus to one of the editing windows"""
            window = window.lower()
            #Choose a window based on the string argument
            if window == "main" or self.window_mode == data.WindowMode.ONE:
                window  = self._parent.main_window
            elif window == "upper":
                window  = self._parent.upper_window
            elif window == "lower":
                window  = self._parent.lower_window
            try:
                #If the window does not have focus, set focus to it
                window.currentWidget().setFocus()
                #Update the Save/SaveAs buttons in the menubar
                window._set_save_status()
                #Check is the widget is a scintilla custom editor
                if isinstance(window.currentWidget(), CustomEditor):
                    #Update the cursor position
                    line    = window.currentWidget().getCursorPosition()[0]
                    column  = window.currentWidget().getCursorPosition()[1]
                    self._parent.display.update_cursor_position(line, column)
                else:
                    #Clear the cursor position
                    self._parent.display.update_cursor_position()
            except:
                window.setFocus()
                self._parent.display.write_to_statusbar("Empty window '" + window.name + "' focused!", 1000)
                #Clear the cursor position
                self._parent.display.update_cursor_position()
            finally:
                #Store the last focused widget
                self._parent.last_focused_widget = window
        
        def set_repl_type(self, type=data.ReplType.SINGLE_LINE):
            """Set REPL input as a one line ReplLineEdit or a multiline ReplHelper"""
            #Check if the REPL type needs to be updated
            if (type == data.ReplType.SINGLE_LINE and 
                self.repl_state == data.ReplType.SINGLE_LINE):
                return
            elif (type == data.ReplType.MULTI_LINE and 
                self.repl_state == data.ReplType.MULTI_LINE):
                return
            # Reinitialize the groupbox that holds the REPL
            self._parent.repl_box.set_repl(type)
            #Refresh the layout
            self._parent.view.set_basic_widgets(
                main_widget=self._parent.main_window,
                upper_widget=self._parent.upper_window,
                lower_widget=self._parent.lower_window
            )
        
        def toggle_window_size(self):
            """Maximize the main application window"""
            if self._parent.isMaximized() == True:
                self._parent.showNormal()
            else:
                self._parent.showMaximized()
            self.refresh_layout(self.window_mode, self.main_window_side)
        
        def toggle_function_wheel(self):
            """Show/hide the function wheel overlay"""
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
            if (self._parent.width() < self.FUNCTION_WHEEL_BOUNDS[0] or 
                self._parent.height() < self.FUNCTION_WHEEL_BOUNDS[1]):
                new_size =  data.QSize(
                    self.FUNCTION_WHEEL_BOUNDS[0] + self.FUNCTION_WHEEL_BOUNDS[0]/5,
                    self.FUNCTION_WHEEL_BOUNDS[1] + self.FUNCTION_WHEEL_BOUNDS[1]/5
                )
                self._parent.resize(new_size)
            # Check if the function wheel overlay is initialized
            if self.function_wheel_overlay != None:
                # Save the currently focused widget
                focused_widget  = self._parent.get_window_by_child_tab()
                focused_tab     = self._parent.get_tab_by_focus()
                if focused_widget == None:
                    focused_widget = self._parent.get_window_by_focus()
                # Store the last focused widget and tab
                self._parent.last_focused_widget = focused_widget
                self._parent.last_focused_tab    = focused_tab
                # Show the function wheel overlay
                self.function_wheel_overlay.show()
        
        def hide_function_wheel(self):
            """Hide the function wheel overlay"""
            if self.function_wheel_overlay != None:
                self.function_wheel_overlay.hide()
        
        def show_settings_gui_manipulator(self):
            # Initialize the settings GUI manipulator if needed
            if self._parent.settings.gui_manipulator == None:
                compare_size = SettingsGuiManipulator.DEFAULT_SIZE
                if (self._parent.width() < compare_size[0] or 
                    self._parent.height() < compare_size[1]):
                        new_size =  data.QSize(
                            compare_size[0] + compare_size[0]/5,
                            compare_size[1] + compare_size[1]/5
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
            if self._parent.settings.gui_manipulator != None:
                self._parent.settings.gui_manipulator.hide()
        
        def __generate_scrollbar_style(self):
            down_arrow_image = functions.get_resource_file("feather/air-grey/chevron-down.svg")
            down_arrow_hover_image = functions.get_resource_file("feather/air-blue/chevron-down.svg")
            up_arrow_image = functions.get_resource_file("feather/air-grey/chevron-up.svg")
            up_arrow_hover_image = functions.get_resource_file("feather/air-blue/chevron-up.svg")
            width = 10
            height = 10
            color_background = data.theme.ScrollBar.background
            color_handle = data.theme.ScrollBar.handle
            color_handle_hover = data.theme.ScrollBar.handle_hover
            style_sheet = (f"""
                /*
                    Horizontal
                */
                QScrollBar:horizontal {{
                    border: none;
                    background: {color_background};
                    height: {height}px;
                    margin: 0px 0px 0px 0px;
                }}
                QScrollBar::handle:horizontal {{
                    background: {color_handle};
                    min-width: 20px;
                }}
                QScrollBar::handle:hover {{
                    background: {color_handle_hover};
                }}
                QScrollBar::handle:horizontal:pressed {{
                    background: {color_handle_hover};
                }}
                
                QScrollBar::sub-line:horizontal, QScrollBar::add-line:horizontal,
                QScrollBar::left-arrow:horizontal, QScrollBar::right-arrow:horizontal,
                QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
                    background: none;
                    width: 0px;
                    height: 0px;
                }}
                
                /*
                    Vertical
                */
                QScrollBar:vertical {{
                    border: none;
                    background: {color_background};
                    width: {width}px;
                    margin: 0px 0px 0px 0px;
                }}
                QScrollBar::handle:vertical {{
                    background: {color_handle};
                    min-height: 20px;
                }}
                QScrollBar::handle:hover {{
                    background: {color_handle_hover};
                }}
                QScrollBar::handle:vertical:pressed {{
                    background: {color_handle_hover};
                }}
                
                QScrollBar::sub-line:vertical, QScrollBar::add-line:vertical,
                QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical,
                QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                    background: none;
                    width: 0px;
                    height: 0px;
                }}
            """)
            return style_sheet
            
        
        def init_style_sheet(self):
            style_sheet = (f"""
                #Form {{
                    background-color: {data.theme.Form};
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
                    background: {data.theme.Form};
                }}
                QMenuBar {{
                    background-color: {data.theme.Indication.PassiveBackGround};
                    color: {data.theme.Font.DefaultHtml};
                }}
                QMenuBar::item {{
                    background-color: transparent;
                }}
                QMenuBar::item:selected {{
                    background-color: {data.theme.Indication.Hover};
                }}
                {self.__generate_scrollbar_style()}
            """)
            return style_sheet
        
        def reset_window_colors(self, in_sheet):
            windows = ["Main", "Upper", "Lower"]
            style_sheet = in_sheet
            for window in windows:
                style_sheet += self.generate_window_colors(
                    window, 
                    data.theme.Indication.PassiveBorder, 
                    data.theme.Indication.PassiveBackGround
                )
            style_sheet = self._style_tree_widgets(style_sheet)
            return style_sheet
        
        def reset_entire_style_sheet(self):
            style_sheet = self.init_style_sheet()
            style_sheet = self.reset_window_colors(style_sheet)
            self._parent.setStyleSheet(style_sheet)
            Menu.update_styles()
            self._parent.repl_box.indication_reset()
        
        def generate_window_colors(self, window_name, border, background):
            style_sheet = (f"""
                #{window_name}::pane {{
                    border: 2px solid {border};
                    background-color: {background};
                }}
                #{window_name} QToolButton {{
                    background: {data.theme.Indication.PassiveBackGround};
                    border: 1px solid {data.theme.Indication.PassiveBorder};
                    margin-top: 0px;
                    margin-bottom: 0px;
                    margin-left: 0px;
                    margin-right: 1px;
                }}
                #{window_name} QToolButton:hover {{
                    background: {data.theme.Indication.ActiveBackGround};
                    border: 1px solid {data.theme.Indication.ActiveBorder};
                }}
            """)
            return style_sheet
        
        def generate_treedisplay_colors(self, type):
            style_sheet =  type + " {"
            style_sheet += "color: rgb({0},{1},{2});".format(
                data.theme.Font.Default.red(), 
                data.theme.Font.Default.green(), 
                data.theme.Font.Default.blue() 
            )
            style_sheet += "background-color: rgb({0},{1},{2});".format(
                data.theme.Paper.Default.red(), 
                data.theme.Paper.Default.green(), 
                data.theme.Paper.Default.blue() 
            )
            style_sheet += "}"
            if data.theme != themes.Air:
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
#                "TreeDisplay",
#                "TreeDisplayBase",
#                "TreeExplorer",
#                "SessionGuiManipulator",
            )
            for t in tree_widgets:
                style_sheet += self.generate_treedisplay_colors(t)
            return style_sheet
        
        def indicate_window(self, window_name=None, repl=False):
            style_sheet = self.init_style_sheet()
            # REPL
            if repl:
                self._parent.repl_box.indication_set()
            else:
                self._parent.repl_box.indication_reset()
            # Windows
            windows = ["Main", "Upper", "Lower"]
            if window_name:
                style_sheet += self.generate_window_colors(
                    window_name, 
                    data.theme.Indication.ActiveBorder, 
                    data.theme.Indication.ActiveBackGround
                )
                windows.remove(window_name)
            for window in windows:
                style_sheet += self.generate_window_colors(
                    window, 
                    data.theme.Indication.PassiveBorder, 
                    data.theme.Indication.PassiveBackGround
                )
            # Tree widgets
            style_sheet = self._style_tree_widgets(style_sheet)
            
            # Apply style sheet
            self._parent.setStyleSheet(style_sheet)

        def indication_check(self):
            if hasattr(self, "indication_timer"):
                self.indication_timer.stop()
            else:
                self.indication_timer = data.QTimer(self._parent)
                self.indication_timer.setInterval(50)
                self.indication_timer.setSingleShot(True)
                self.indication_timer.timeout.connect(self.__indication_check)
            self.indication_timer.start(50)
        
        def __indication_check(self):
            """
            Check if any of the main windows or the REPL is focused
            and indicate the focused widget if needed
            """
            if (self._parent.main_window == None or 
                self._parent.upper_window == None or 
                self._parent.lower_window == None or 
                self._parent.repl == None):
                return
            Menu.update_styles()
            #Check the focus for all of the windows
            windows = [self._parent.main_window, 
                       self._parent.upper_window, 
                       self._parent.lower_window]
            for window in windows:
                if window.count() == 0:
                    if window.hasFocus() == True:
                        window.indicated = True
                        self.indicate_window(window.name)
                        return
                    else:
                        window.indicated = False
                else:
                    window.indicated = False
                    for i in range(window.count()):
                        if isinstance(window.widget(i), TextDiffer) == True:
                            if (window.widget(i).hasFocus() == True or
                                window.widget(i).editor_1.hasFocus() == True or
                                window.widget(i).editor_2.hasFocus() == True):
                                window.indicated = True
                                self.indicate_window(window.name)
                                return
                        else:
                            if window.widget(i).hasFocus() == True:
                                window.indicated = True
                                self.indicate_window(window.name)
                                return
            #Check the REPL focus
            if (self._parent.repl.hasFocus() == True or
                self._parent.repl_helper.hasFocus() == True):
                self._parent.repl.indicated = True
                self.indicate_window(repl=True)
                return
            #If no widget has focus, reset the QMainWindows stylesheet
            self.reset_entire_style_sheet()
        
        def refresh_main_splitter(self):
            # Refresh the size relation between the basic widgets and the REPL,
            # so that the REPL height is always the same
            self._parent.main_splitter.setSizes(
                [
                    self._parent.height() - self.main_relation,
                    self.main_relation - (self.main_relation * 0.1)
                ]
            )
            self.reset_entire_style_sheet()
        
        def refresh_theme(self):
            windows = [
                self._parent.main_window, 
                self._parent.upper_window, 
                self._parent.lower_window
            ]
            for window in windows:
                window.customize_tab_bar()
                for i in range(window.count()):
                    if hasattr(window.widget(i), "refresh_lexer") == True:
                        window.widget(i).refresh_lexer()
                    elif hasattr(window.widget(i), "set_theme") == True:
                        window.widget(i).set_theme(data.theme)
            self._parent.repl_helper.refresh_lexer()
            self.indication_check()
            self._parent.statusbar.setStyleSheet(
                "color: {0};".format(data.theme.Indication.Font)
            )
            # Update the taskbar menu
            self._parent.display.update_theme_taskbar_icon()
            
            # Reset the function wheel
            if FunctionWheel.check_theme_state():
                if self.function_wheel_overlay != None:
                    self.function_wheel_overlay.clean_up()
                self.function_wheel_overlay = FunctionWheel(
                    parent=self._parent.main_groupbox, 
                    main_form=self._parent, 
                )
                FunctionWheel.reset_background_image()
            
            # Reset the settings gui manipulator so it will update
            if SettingsGuiManipulator.check_theme_state():
                if self._parent.settings.gui_manipulator != None:
                    self._parent.settings.gui_manipulator.clean_up()
                self._parent.settings.gui_manipulator = None
                SettingsGuiManipulator.reset_background_image()
        
        def reload_themes(self):
            global lexers, themes
            
            """
            !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            THIS ROUTINE EATS MEMORY LIKE CRAZY BUT IS NEEDED
            FOR NUITKA AND CX_FREEZE TO WORK CORRECTLY
            !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            (If you don't want to consume memory reload the themes by restarting Ex.Co.!)
            -----------------------------------------------------------------------------
            """
            current_theme_name = data.theme.__name__.split(".")[1]
            import themes
            import lexers
            for theme in themes.theme_list:
                importlib.reload(theme)
            importlib.reload(lexers)
            # Set the theme again
            data.theme = getattr(themes, current_theme_name)
            self.refresh_theme()
            """
            -----------------------------------------------------------------------------
            """
    
        def create_recent_file_list_menu(self):
            self._parent.recent_files_menu = Menu("Recent Files")
            self._parent.recent_files_menu.setStyleSheet("QMenu { menu-scrollable: 1; }")
            temp_icon = functions.create_icon('tango_icons/file-recent-files.png')
            self._parent.recent_files_menu.setIcon(temp_icon)
            return self._parent.recent_files_menu
        
        def delete_recent_file_list_menu(self):
            self._parent.recent_files_menu.setParent(None)
            self._parent.recent_files_menu = None

    
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
            if search_dir == None:
                search_dir = self._parent._get_directory_with_dialog()
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
            if found_files == None:
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
                          break_on_find=False):
            """Return a list of files that contain the searched text as a list and display it"""
            #Check if the search directory is none, then use a dialog window
            #to select the real search directory
            if search_dir == None:
                search_dir = self._parent._get_directory_with_dialog()
                #Update the current working directory
                if os.path.isdir(search_dir):
                    self._parent.set_cwd(search_dir)
            try:
                #Execute the find function
                result = functions.find_files_with_text_enum(
                    search_text, 
                    search_dir, 
                    case_sensitive, 
                    search_subdirs, 
                    break_on_find
                )
                # Check of the function return is valid
                if result == -1:
                    self._parent.display.repl_display_message(
                        "Invalid search directory!", 
                        message_type=data.MessageType.ERROR
                    )
                    self._parent.display.write_to_statusbar("Invalid search directory!", 2000)
                    return
                elif result == -2:
                    self._parent.display.repl_display_message(
                        "Cannot search over multiple lines!", 
                        message_type=data.MessageType.ERROR
                    )
                    self._parent.display.write_to_statusbar("Invalid search directory!", 2000)
                    return
                elif result == {}:
                    #Check if any files were found
                    self._parent.display.repl_display_message(
                        "No files found!", 
                        message_type=data.MessageType.WARNING
                    )
                    self._parent.display.write_to_statusbar("No files found!", 2000)
                    return
                #Display the found files
                self._parent.display.show_found_files_with_lines_in_tree(
                    "'{}' in its content".format(search_text), 
                    result, 
                    search_dir
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
                             search_subdirs=True):
            """
            Same as the function in the 'functions' module.
            Replaces all instances of search_string with the replace_string in the files,
            that contain the search string in the search_dir.
            """
            #Close the log window if it is displayed
            self._parent.view.set_log_window(False)
            warning = "The replaced content will be saved back into the files!\n"
            warning += "You better have a backup of the files if you are unsure,\n"
            warning += "because this action CANNOT be undone!\n"
            warning += "Do you want to continue?"
            reply = YesNoDialog.warning(warning)
            if reply == data.QMessageBox.No:
                return
            #Check if the search directory is none, then use a dialog window
            #to select the real search directory
            if search_dir == None:
                search_dir = self._parent._get_directory_with_dialog()
                #Update the current working directory
                if os.path.isdir(search_dir):
                    self._parent.set_cwd(search_dir)
            #Replace the text in files
            result = functions.replace_text_in_files_enum(
                search_text, 
                replace_text, 
                search_dir, 
                case_sensitive, 
                search_subdirs
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
            basic_widget = self._parent.get_window_by_name(window_name)
            if window_name == None:
                window_name = "Main"
            # Check if there are any documents in the basic widget
            if basic_widget.count() == 0:
                message = "No documents in " + basic_widget.name.lower()
                message += " editing window"
                self._parent.display.repl_display_message(
                    message, 
                    message_type=data.MessageType.WARNING
                )
                return
            # Save the current index to reset focus to it if no
            # instances of search string are found
            saved_index = basic_widget.currentIndex()
            # Create a deque of the tab index order and start with the current
            # index, deque is used, because it can be rotated by default
            in_deque = collections.deque(range(basic_widget.count()))
            # Rotate the deque until the first element is the current index
            while in_deque[0] != basic_widget.currentIndex():
                in_deque.rotate(1)
            # Set a flag for the first document
            first_document = True
            for i in in_deque:
                # Skip the current widget if it's not an editor
                if isinstance(basic_widget.widget(i), CustomEditor) == False:
                    continue
                # Place the cursor to the top of the document
                # if it is not the current document
                if first_document == True:
                    first_document = False
                else:
                    basic_widget.widget(i).setCursorPosition(0, 0)
                # Find the text
                result = basic_widget.widget(i).find_text(
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
            basic_widget.setCurrentIndex(saved_index)
            message = "No instances of '" + search_text + "' found in "
            message += basic_widget.name.lower() + " editing window"
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
            basic_widget = self._parent.get_window_by_name(window_name)
            if window_name == None:
                window_name = "Main"
            #Check if there are any documents in the basic widget
            if basic_widget.count() == 0:
                message = "No documents in the " + basic_widget.name.lower()
                message += " editing window"
                self._parent.display.repl_display_message(
                    message, 
                    message_type=data.MessageType.WARNING
                )
                return
            #Save the current index to reset focus to it if no instances of search string are found
            saved_index = basic_widget.currentIndex()
            #Create a deque of the tab index order and start with the current index,
            #deque is used, because it can be rotated by default
            in_deque= collections.deque(range(basic_widget.count()))
            #Rotate the deque until the first element is the current index
            while in_deque[0] != basic_widget.currentIndex():
                in_deque.rotate(1)
            #Find the next instance
            for i in in_deque:
                result = basic_widget.widget(i).find_and_replace(
                    search_text, 
                    replace_text, 
                    case_sensitive, 
                    regular_expression
                )
                #If a replace was done, return success
                if result == True:
                    message = "Found and replaced in " + basic_widget.name.lower()
                    message += " editing window"
                    self._parent.display.write_to_statusbar(message)
                    return True
            #Nothing found
            basic_widget.setCurrentIndex(saved_index)
            message = "No instances of '" + search_text + "' found in the "
            message += basic_widget.name.lower() + " editing window"
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
            basic_widget = self._parent.get_window_by_name(window_name)
            if window_name == None:
                window_name = "Main"
            #Loop over each widget and replace all instances of the search text
            for i in range(basic_widget.count()):
                basic_widget.widget(i).replace_all(
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
        def _run_focused_widget_method(self,
                                       method_name,
                                       argument_list, 
                                       window_name=None):
            """Execute a focused widget method"""
            #Get the current widget
            widget = self._parent.get_current_tab_by_parent_name(window_name)
            if window_name == None:
                window_name = "Main"
            #None-check the current widget in the selected window
            if widget != None:
                method = getattr(widget, method_name)
                #Argument list has to be preceded by the '*' character
                method(*argument_list)
            else:
                message = "No document in {} window!".format(window_name)
                self._parent.display.repl_display_message(
                    message, 
                    message_type=data.MessageType.WARNING
                )
        
        def find(self, search_text, case_sensitive=False, search_forward=True, window_name=None):
            """Find text in the currently focused window"""
            argument_list = [search_text, case_sensitive, search_forward]
            self._run_focused_widget_method("find_text", argument_list, window_name)
        
        def regex_find(self, search_text, case_sensitive=False, search_forward=True, window_name=None):
            """Find text in the currently focused window"""
            argument_list = [search_text, case_sensitive, search_forward, True]
            self._run_focused_widget_method("find_text", argument_list, window_name)
        
        def find_and_replace(self, search_text, replace_text, case_sensitive=False, search_forward=True, window_name=None):
            """Find and replace text in the currently focused window"""
            argument_list = [search_text, replace_text, case_sensitive, search_forward]
            self._run_focused_widget_method("find_and_replace", argument_list, window_name)
        
        def regex_find_and_replace(self, search_text, replace_text, case_sensitive=False, search_forward=True, window_name=None):
            """
            Find and replace text in the currently focused window
            using the regular expressions module
            """
            argument_list = [search_text, replace_text, case_sensitive, search_forward, True]
            self._run_focused_widget_method("find_and_replace", argument_list, window_name)
        
        def replace_all(self, search_text, replace_text, case_sensitive=False, window_name=None):
            """Replace all occurences of a string in the currently focused window"""
            argument_list = [search_text, replace_text, case_sensitive]
            self._run_focused_widget_method("replace_all", argument_list, window_name)
        
        def regex_replace_all(self, search_text, replace_text, case_sensitive=False, window_name=None):
            """
            Replace all occurences of a string in the currently focused window
            using the regular expressions module
            """
            argument_list = [search_text, replace_text, case_sensitive, True]
            self._run_focused_widget_method("replace_all", argument_list, window_name)
        
        def replace_in_selection(self, search_text, replace_text, case_sensitive=False, window_name=None):
            """Replace all occurences of a string in the current selection in the currently focused window"""
            argument_list = [search_text, replace_text, case_sensitive]
            self._run_focused_widget_method("replace_in_selection", argument_list, window_name)
        
        def regex_replace_in_selection(self, search_text, replace_text, case_sensitive=False, window_name=None):
            """
            Replace all occurences of a string in the current selection in the
            currently focused window using regular expressions module
            """
            argument_list = [search_text, replace_text, case_sensitive, True]
            self._run_focused_widget_method("replace_in_selection", argument_list, window_name)
        
        def highlight(self, highlight_text, case_sensitive=False, window_name=None):
            """Highlight all occurences of text in the currently focused window"""
            argument_list = [highlight_text, case_sensitive]
            self._run_focused_widget_method("highlight_text", argument_list, window_name)
        
        def regex_highlight(self, highlight_text, case_sensitive=False, window_name=None):
            """
            Highlight all occurences of text in the currently focused window
            using regular expressions
            """
            argument_list = [highlight_text, case_sensitive, True]
            self._run_focused_widget_method("highlight_text", argument_list, window_name)
        
        def clear_highlights(self, window_name=None):
            """Clear all highlights in the currently focused window"""
            argument_list = []
            self._run_focused_widget_method("clear_highlights", argument_list, window_name)
        
        def convert_to_uppercase(self, window_name=None):
            """Change the case of the selected text in the currently focused window"""
            argument_list = [True]
            self._run_focused_widget_method("convert_case", argument_list, window_name)
        
        def convert_to_lowercase(self, window_name=None):
            """Change the case of the selected text in the currently focused window"""
            argument_list = [False]
            self._run_focused_widget_method("convert_case", argument_list, window_name)
        
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
                self._parent._run_focused_widget_method("goto_line", argument_list, window_name)
            
            def replace(self, replace_text, line_number, window_name=None):
                """Replace the selected line in the currently focused window"""
                argument_list = [replace_text, line_number]
                self._parent._run_focused_widget_method("replace_line", argument_list, window_name)
            
            def remove(self, line_number, window_name=None):
                """Remove the selected line in the currently focused window"""
                argument_list = [line_number]
                self._parent._run_focused_widget_method("remove_line", argument_list, window_name)
            
            def get(self, line_number, window_name=None):
                """Replace the selected line in the currently focused window"""
                argument_list = [line_number]
                self._parent._run_focused_widget_method("get_line", argument_list, window_name)
            
            def set(self, line_text, line_number, window_name=None):
                """Replace the selected line in the currently focused window"""
                argument_list = [line_text, line_number]
                self._parent._run_focused_widget_method("set_line", argument_list, window_name)
    
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
        # Theme menu
        theme_menu          = None
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
            """ Initialization of the Display object instance """
            # Get the reference to the MainWindow parent object instance
            self._parent = parent
            # Initialize the stored icons
            self.node_tree_icon = functions.create_icon('tango_icons/edit-node-tree.png')
            self.repl_messages_icon = functions.create_icon('tango_icons/repl-messages.png')
            self.system_found_files_icon = functions.create_icon('tango_icons/system-find-files.png')
            self.system_found_in_files_icon = functions.create_icon('tango_icons/system-find-in-files.png')
            self.system_replace_in_files_icon = functions.create_icon('tango_icons/system-replace-in-files.png')
            self.system_show_cwd_tree_icon = functions.create_icon('tango_icons/system-show-cwd-tree.png')
            # Initialize the theme menu
            self.init_theme_menu()
        
        def init_theme_indicator(self):
            """ Initialization of the theme indicator in the statusbar """
            self.theme_indicatore = ThemeIndicator(self)
            self.theme_indicatore.set_image(data.theme.image_file)
            self.theme_indicatore.setToolTip(data.theme.tooltip)
            self.theme_indicatore.restyle()
            self._parent.statusbar.addPermanentWidget(self.theme_indicatore)
        
        def update_theme_taskbar_icon(self):
            # Check if the indicator is initialized
            if self.theme_indicatore == None:
                return
            # Set the theme icon and tooltip
            self.theme_indicatore.set_image(data.theme.image_file)
            self.theme_indicatore.setToolTip(data.theme.tooltip)
            self.theme_indicatore.restyle()
        
        def init_theme_menu(self):
            """ Initialization of the theme menu used by the theme indicator """
            def choose_theme(theme):
                data.theme = theme
                self._parent.view.refresh_theme()
                self.update_theme_taskbar_icon()
                current_theme = data.theme.tooltip
                self.repl_display_message(
                    "Changed theme to: {}".format(current_theme), 
                    message_type=data.MessageType.SUCCESS
                )
            
            if self.theme_menu != None:
                # Clear the menu actions from memory
                self.theme_menu.clear()
                for action in self.theme_menu.actions():
                    self.theme_menu.removeAction(action)
                    action.setParent(None)
                    action.deleteLater()
                    action = None
            self.theme_menu = Menu()
            # Add the theme actions
            for theme in themes.theme_list:
                action_theme = data.QAction(theme.name, self.theme_menu)
                action_theme.triggered.connect(
                    functools.partial(choose_theme, theme)
                )
                icon = functions.create_icon(theme.image_file)
                action_theme.setIcon(icon)
                self.theme_menu.addAction(action_theme)
        
        def write_to_statusbar(self, message, msec=0):
            """Write a message to the statusbar"""
            self._parent.statusbar.setStyleSheet(
                "color: {0};".format(data.theme.Indication.Font)
            )
            self._parent.statusbar.showMessage(message, msec)
        
        def update_cursor_position(self, cursor_line=None, cursor_column=None):
            """Update the position of the cursor in the current widget to the statusbar"""
            if cursor_line == None and cursor_column == None:
                self._parent.statusbar_label_left.setText("")
            else:
                statusbar_text = "LINE: " + str(cursor_line+1)
                statusbar_text += " COLUMN: " + str(cursor_column+1)
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
        
        def repl_display_message(self, 
                                 *message, 
                                 scroll_to_end=True, 
                                 focus_repl_messages=True, 
                                 message_type=None):
            """
            Display the REPL return message in a scintilla tab
            named "REPL Messages" in one of the basic widgets
            """
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
#                    data.theme.Font.Python.Default[0].encode("utf-8")
                    b"Arial"
                )
                parent.repl_messages_tab.SendScintilla(
                    data.QsciScintillaBase.SCI_STYLESETSIZE,
                    lexer_number,
                    10
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
                    color
                )
                parent.repl_messages_tab.SendScintilla(
                    data.QsciScintillaBase.SCI_STYLESETBACK,
                    lexer_number,
                    data.theme.Paper.Default
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
            #Set the tab name for displaying REPL messages
            repl_messages_tab_name = "REPL MESSAGES"
            #Find the "REPL Message" tab in the basic widgets
            parent.repl_messages_tab = self.find_repl_messages_tab()
            #Create a new REPL tab in the lower basic widget if it doesn't exist
            if parent.repl_messages_tab == None:
                parent.repl_messages_tab = parent.lower_window.plain_add_document(
                    repl_messages_tab_name
                )
                rmt = parent.repl_messages_tab
                rmt.icon_manipulator.set_icon(rmt, self.repl_messages_icon)
            # Parse the message arguments
            if len(message) > 1:
                message = " ".join(message)
            else:
                message = message[0]
            #Check if message is a string class, if not then make it a string
            if message == None:
                return
#            elif isinstance(message, bytes) == True:
#                # Convert a byte string to utf-8 string
#                message = message.decode("utf-8")
            elif isinstance(message, str) == False:
                message = str(message)
            #Check if the message should be error colored
            if message_type != None:
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
                    style_repl_text(start, end, data.theme.Font.Repl.Error, 1)
                elif message_type == data.MessageType.WARNING:
                    style_repl_text(start, end, data.theme.Font.Repl.Warning, 2)
                elif message_type == data.MessageType.SUCCESS:
                    style_repl_text(start, end, data.theme.Font.Repl.Success, 3)
                elif message_type == data.MessageType.DIFF_UNIQUE_1:
                    style_repl_text(start, end, data.theme.Font.Repl.Diff_Unique_1, 4)
                elif message_type == data.MessageType.DIFF_UNIQUE_2:
                    style_repl_text(start, end, data.theme.Font.Repl.Diff_Unique_2, 5)
                elif message_type == data.MessageType.DIFF_SIMILAR:
                    style_repl_text(start, end, data.theme.Font.Repl.Diff_Similar, 6)
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
            if self._parent.repl_messages_tab != None:
                self._parent.repl_messages_tab.goto_line(
                    self._parent.repl_messages_tab.lines()
                )
        
        def repl_clear_tab(self):
            """Clear text from the REPL messages tab"""
            #Find the "REPL Message" tab in the basic widgets
            self._parent.repl_messages_tab = self.find_repl_messages_tab()
            #Check if REPL messages tab exists
            if self._parent.repl_messages_tab != None:
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
            #Set the tab name for displaying REPL messages
            repl_messages_tab_name = "REPL MESSAGES"
            #Call the MainForm function to find the repl tab by name
            self._parent.repl_messages_tab = self._parent.get_tab_by_name(repl_messages_tab_name)
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
            if custom_editor == None:
                parent.display.repl_display_message(
                        "No document selected for node tree creation!", 
                        message_type=data.MessageType.ERROR
                )
                parent.display.write_to_statusbar("No document selected for node tree creation!", 5000)
                return
            # Check if the document type is Python or C
            valid_parsers = ["PYTHON", "C", "NIM"]
            if not(parser in valid_parsers):
                parsers = ", ".join([x[0] + x[1:].lower() for x in valid_parsers[:-1]])
                message = "Document is not of type: {}!".format(parsers)
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
            parent.node_tree_tab = parent.upper_window.tree_add_tab(node_tree_tab_name)
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
            elif parser == "C":
                # Get all the file information
                try:
                    result = functions.get_c_node_tree_with_ctags(custom_editor.text())
                except Exception as ex:
                    parent.display.repl_display_message(
                        str(ex), 
                        message_type=data.MessageType.ERROR
                    )
                    return
                c_nodes = result
                # Display the information in the tree tab
                parent.node_tree_tab.display_c_nodes(
                    custom_editor, 
                    c_nodes 
                )
            elif parser == "NIM":
                # Get all the file information
                nim_nodes = functions.get_nim_node_tree(custom_editor.text())
                # Display the information in the tree tab
                parent.node_tree_tab.display_nim_nodes(
                    custom_editor, 
                    nim_nodes 
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
            if custom_editor == None:
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
                if document_tab == None:
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
            parent.node_tree_tab = parent.upper_window.plain_add_document(node_tree_tab_name)
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
                self._parent.open_file(file, self._parent.main_window)
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
            found_files_tab = parent.upper_window.tree_add_tab(found_files_tab_name)
            found_files_tab.icon_manipulator.set_icon(
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
            found_files_tab = parent.upper_window.tree_add_tab(found_files_tab_name)
            found_files_tab.icon_manipulator.set_icon(
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
        
        def show_found_files_with_lines_in_tree(self, search_text, file_list, directory):
            """
            Display the found files with line information returned from the 
            find_in_files and replace_in_files system function in a TreeDisplay
            """
            #Define references directly to the parent and mainform for performance and clarity
            parent = self._parent
            #Define a name for the FOUND FILES tab
            found_files_tab_name = "FOUND FILES"
            #Find the FOUND FILES tab in the basic widgets
            parent.found_files_tab = parent.get_tab_by_name(found_files_tab_name)
            if parent.found_files_tab:
                parent.found_files_tab._parent.close_tab(found_files_tab_name)
            found_files_tab = parent.found_files_tab
            #Create a new FOUND FILES tab in the upper basic widget
            found_files_tab = parent.upper_window.tree_add_tab(found_files_tab_name)
            found_files_tab.icon_manipulator.set_icon(
                found_files_tab, self.system_found_files_icon
            )
            #Focus the node tree tab
            found_files_tab._parent.setCurrentWidget(found_files_tab)
            #Display the found files information in the tree tab
            found_files_tab.display_found_files_with_lines(
                search_text, 
                file_list, 
                directory
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
            parent.found_files_tab = parent.upper_window.tree_add_tab(found_files_tab_name)
            parent.found_files_tab.icon_manipulator.set_icon(
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
        
        def show_text_difference(self, text_1, text_2, text_name_1=None, text_name_2=None):
            """Display the difference between two texts in a TextDiffer"""
            #Check if text names are valid
            if text_name_1 == None:
                text_name_1 = "TEXT 1"
            if text_name_2 == None:
                text_name_2 = "TEXT 2"
            #Create a reference to the main form for less typing
            parent = self._parent
            #Create and initialize a text differ
            text_differ = TextDiffer(
                parent.main_window,
                parent,
                text_1,
                text_2,
                text_name_1,
                text_name_2
            )
            #Find the "DIFF(...)" tab in the basic widgets and close it
            diff_tab_string = "DIFF("
            diff_tab = parent.get_tab_by_string_in_name(diff_tab_string)
            if diff_tab:
                diff_tab_index = diff_tab._parent.indexOf(diff_tab)
                diff_tab._parent.close_tab(diff_tab_index)
            #Add the created text differ to the main window
            diff_index = parent.main_window.addTab(
                text_differ, 
                "DIFF({} / {})".format(text_name_1, text_name_2)
            )
            #Set focus to the text differ tab
            parent.main_window.setCurrentIndex(diff_index)
        
        def show_session_editor(self):
            """Display a window for editing sessions"""
            #Create the SessionGuiManipulator
            settings_manipulator = self._parent.settings.manipulator
            sessions_manipulator = SessionGuiManipulator(
                settings_manipulator, 
                self._parent.upper_window, 
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
            sm_index = self._parent.upper_window.addTab(
                sessions_manipulator,
                "SESSIONS"
            )
            #Set focus to the text differ tab
            self._parent.upper_window.setCurrentIndex(sm_index)
        
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
                if key_combo != None and key_combo != "" and key_combo != []:
                    if isinstance(key_combo, list):
                        action.setShortcuts(key_combo)
                    else:
                        action.setShortcut(key_combo)
                action.setStatusTip(status_tip)
                # Icon and pixmap
                action.pixmap = None
                if icon != None:
                    action.setIcon(functions.create_icon(icon))
                    action.pixmap = functions.create_pixmap_with_size(icon, 32, 32)
                # Function
                if function != None:
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
            if custom_parent != None:
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
            NIM_action = create_action(
                'Nim',
                None, 
                'Change document lexer to: Nim', 
                'language_icons/logo_nim.png', 
                create_lexer(lexers.Nim, 'Nim'),
                lexers_menu
            )
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
            if data.compatibility_mode == False:
                CoffeeScript_action = create_action(
                    'CoffeeScript',
                    None, 
                    'Change document lexer to: CoffeeScript', 
                    'language_icons/logo_coffeescript.png', 
                    create_lexer(lexers.CoffeeScript, 'CoffeeScript'),
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
            lexers_menu.addAction(NONE_action)
            lexers_menu.addSeparator()
            lexers_menu.addAction(ADA_action)
            lexers_menu.addAction(AWK_action)
            lexers_menu.addAction(BASH_action)
            lexers_menu.addAction(BATCH_action)
            lexers_menu.addAction(CMAKE_action)
            lexers_menu.addAction(C_CPP_action)
            lexers_menu.addAction(cicode_action)
            if data.compatibility_mode == False:
                lexers_menu.addAction(CoffeeScript_action)
            lexers_menu.addAction(CSharp_action)
            lexers_menu.addAction(CSS_action)
            lexers_menu.addAction(D_action)
            lexers_menu.addAction(Fortran77_action)
            lexers_menu.addAction(FORTRAN_action)
            lexers_menu.addAction(HTML_action)
            lexers_menu.addAction(IDL_action)
            lexers_menu.addAction(Java_action)
            lexers_menu.addAction(JavaScript_action)
            lexers_menu.addAction(LUA_action)
            lexers_menu.addAction(MAKEFILE_action)
            lexers_menu.addAction(MATLAB_action)
            lexers_menu.addAction(NIM_action)
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
    
    class Bookmarks:
        """
        All bookmark functionality
        """
        #Class varibles
        _parent = None
        #List of all the bookmarks
        marks = None
        
        def __init__(self, parent):
            """Initialization of the Bookmarks object instance"""
            #Get the reference to the MainWindow parent object instance
            self._parent = parent
            #Initialize all the bookmarks
            self.init()
        
        def init(self):
            self.marks = {}
            for i in range(10):
                self.marks[i] = (None, None)
        
        def add(self, editor, line):
            #Bookmarks should only work in editors
            if (isinstance(editor, CustomEditor) == False or editor.embedded == True):
                return
            for i in range(10):
                if self.marks[i] == (None, None):
                    self.marks[i] = (editor, line)
                    self._parent.display.repl_display_message(
                        "Bookmark '{:d}' was added!".format(i), 
                        message_type=data.MessageType.SUCCESS
                    )
                    return i
            else:
                self._parent.display.repl_display_message(
                    "All ten bookmarks are occupied!", 
                    message_type=data.MessageType.ERROR
                )
                return None
        
        def add_mark_by_number(self, editor, line, mark_number):
            #Bookmarks should only work in editors
            if (isinstance(editor, CustomEditor) == False or editor.embedded == True):
                return
            #Clear the selected marker if it is not empty
            if self.marks[mark_number] != (None, None):
                self.marks[mark_number][0].bookmarks.toggle_at_line(self.marks[mark_number][1])
                self.marks[mark_number] = (None, None)
            #Check if there is a bookmark already at the selected editor line
            for i in range(10):
                if self.marks[i] == (editor, line):
                    self.marks[i][0].bookmarks.toggle_at_line(self.marks[i][1])
                    break
            #Set and store the marker on the editor
            self.marks[mark_number] = (editor, line)
            editor.bookmarks.add_marker_at_line(line)
            self._parent.display.repl_display_message(
                "Bookmark '{:d}' was added!".format(mark_number), 
                message_type=data.MessageType.SUCCESS
            )
        
        def clear(self):
            cleared_any = False
            for i in range(10):
                if self.marks[i] != (None, None):
                    self.marks[i][0].bookmarks.toggle_at_line(self.marks[i][1])
                    self.marks[i] = (None, None)
                    cleared_any = True
            if cleared_any == False:
                self._parent.display.repl_display_message(
                    "Bookmarks are clear.", 
                    message_type=data.MessageType.WARNING
                )
                return
        
        def remove_by_number(self, mark_number):
            if self.bounds_check(mark_number) == False:
                return
            self.marks[mark_number] = (None, None)
        
        def remove_by_reference(self, editor, line):
            for i in range(10):
                if self.marks[i][0] == editor and self.marks[i][1] == line:
                    self.marks[i] = (None, None)
                    self._parent.display.repl_display_message(
                        "Bookmark '{:d}' was removed!".format(i), 
                        message_type=data.MessageType.SUCCESS
                    )
                    break
            else:
                self._parent.display.repl_display_message(
                    "Bookmark not found!", 
                    message_type=data.MessageType.ERROR
                )
        
        def remove_editor_all(self, editor):
            """Remove all bookmarks of an editor"""
            removed_bookmarks = []
            for i in range(10):
                if self.marks[i][0] == editor:
                    self.marks[i] = (None, None)
                    removed_bookmarks.append(i)
            if removed_bookmarks != []:
                close_message = "Bookmarks: "
                close_message += ", ".join(str(mark) for mark in removed_bookmarks)
                close_message += "\nwere removed."
                self._parent.display.repl_display_message(
                    close_message, 
                    message_type=data.MessageType.SUCCESS
                )
        
        def check(self, editor, line):
            for i in range(10):
                if self.marks[i][0] == editor and self.marks[i][1] == line:
                    return i
            else:
                return None
        
        def bounds_check(self, mark_number):
            if mark_number < 0 or mark_number > 9:
                self._parent.display.repl_display_message(
                    "Bookmarks only go from 0 to 9!", 
                    message_type=data.MessageType.ERROR
                )
                return False
            else:
                return True
        
        def goto(self, mark_number):
            if self.bounds_check(mark_number) == False:
                return
            if self.marks[mark_number] == (None, None):
                self._parent.display.repl_display_message(
                    "Bookmark '{:d}' is empty!".format(mark_number), 
                    message_type=data.MessageType.WARNING
                )
            else:
                editor = self.marks[mark_number][0]
                line = self.marks[mark_number][1]
                #Focus the stored editor and it's parent basic widget
                editor._parent.setCurrentWidget(editor)
                self._parent.view.set_window_focus(editor._parent.name)
                #Go to the stored line
                editor.goto_line(line)



