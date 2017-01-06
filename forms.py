
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2017 Matic Kukovec. 
Release under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

##  FILE DESCRIPTION:
##      - Definitions of the Main form and its controls, more or less everything
##        involving PyQt4
##
##      - The file is very big because I wanted all of the widget definition in a single file.
##        To navigate the file use either Ex.Co.(Show Node Tree function - F5) itself or 
##        in the Eric6 IDE
##
##      - Every import is explicitly defined e.g.: PyQt4.Qt...  
##        I did this for learning purposes, to familiarize myself with the PyQt4 libraries
##
##      - The code tries to follow PEP 8 for naming conventions
##          - since version 0.7 the standard Qt method nameing(camelCase)
##            had to be used, which does not conform with PEP 8
##
##      - Function is sometimes used instead of method
##
##      - Basic widget is sometimes simply called "window" or "editor window", 
##        they all mean the same thing: an instance of a BasicWidget class

import os
import sys
import platform
import itertools
import inspect
import functools
import keyword
import re
import collections
import textwrap
import importlib
import data
import themes
import helper_forms
import functions
import interpreter
import settings
import lexers
import traceback



"""
-------------------------------------------------
Main window and its supporting objects
-------------------------------------------------
"""
class MainWindow(data.QMainWindow):
    """Main form that holds all Qt objects"""
    # Define main form control references
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
    # Last directory browsed by the "Open File" and other dialogs
    last_browsed_dir        = ""
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
        ['*' + x for x in data.ext_cpython] +
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
        self.setObjectName("Form")
        # Initialize the main window 
        self.setWindowTitle("Ex.Co. " + data.APPLICATION_VERSION)
        # Initialize the log dialog window
        data.log_window = helper_forms.MessageLogger(self)
        # Initialize basic window widgets(main, side_up, side_down)
        self._init_basic_widgets()
        # Initialize statusbar
        self._init_statusbar()
        # Initialize the REPL
        self._init_repl()
        # Initialize the menubar
        self._init_menubar()
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
        self.settings.restore()
        # Initialize the theme indicator
        self.display.init_theme_indicator()
        # Initialize repl interpreter
        self._init_interpreter()
        # Set the main window icon if it exists
        if os.path.isfile(data.application_icon) == True:
            self.setWindowIcon(data.PyQt.QtGui.QIcon(data.application_icon))
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
    
    def _init_statusbar(self):
        self.statusbar  = data.QStatusBar(self)
        self.display.write_to_statusbar("Status Bar")
        #Add label for showing the cursor position in a basic widget
        self.statusbar_label_left = data.QLabel()
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
            open        = self.open_files,
            open_d      = self.open_file_with_dialog, 
            save        = functions.write_to_file, 
            log         = data.log_window, 
            version     = data.APPLICATION_VERSION,
            run         = self.run_process, 
            set_cwd         = self.set_cwd, 
            get_cwd         = self.get_cwd, 
            update_cwd      = self.update_cwd, 
            close_all       = self.close_all_tabs, 
            #Settings functions
            settings        = self.settings.manipulator,
            save_settings   = self.settings.save, 
            load_settings   = self.settings.restore, 
            #Session functions
            session_add     = self.sessions.add, 
            session_restore = self.sessions.restore, 
            session_remove  = self.sessions.remove, 
            #View functions
            spin                    = self.view.spin_basic_widgets, 
            toggle_main_window_side = self.view.toggle_main_window_side, 
            #System function
            find_files       = self.system.find_files, 
            find_in_files    = self.system.find_in_files, 
            replace_in_files = self.system.replace_in_files, 
            #Document editing references
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
            #Display functions
            print           = self.display.repl_display_message,
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

    def set_cwd(self, dir):
        """Set the current working directory and display it"""
        os.chdir(dir)
        #Store the current REPL text
        repl_text = self.repl.text()
        #Reset the interpreter and update its references
        self._reset_interpreter()
        #Update the last browsed directory to the class/instance variable
        self.last_browsed_dir = dir
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
            reply = data.QMessageBox.question(
                self, 
                'Quit', 
                quit_message,
                data.QMessageBox.Yes,
                data.QMessageBox.No
            )
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
        if self.view.function_wheel_overlay != None:
            self.view.function_wheel_overlay.hide()
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
        #Execute the superclass mouse press event
        super().mousePressEvent(event)
        #Hide the function wheel if it is shown
        if self.view.function_wheel_overlay != None:
            self.view.hide_function_wheel()
    
    def _window_filter_keypress(self, key_event):
        """Filter keypress for appropriate action"""
        pressed_key = key_event.key()
        accept_keypress = False
        #Check for escape keypress
        if pressed_key == data.PyQt.QtCore.Qt.Key_Escape:
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
                    last_dir=self.last_browsed_dir, 
                    encoding=encoding, 
                    line_ending=line_ending
                )
                #Set the icon if it was set by the lexer
                if focused_tab.current_icon != None:
                    parent = focused_tab.parent
                    parent.setTabIcon(parent.indexOf(focused_tab), focused_tab.current_icon)
                #Save the last browsed directory from the editor widget to the main form
                self.last_browsed_dir = focused_tab.last_browsed_dir
                #Reimport the user configuration file and update the menubar
                if functions.is_config_file(focused_tab.save_name) == True:
                    self.import_user_functions()
                    self.update_menubar()
    
    def file_saveas(self, encoding="utf-8"):
        """The function name says it all"""
        focused_tab = self.get_tab_by_focus()
        if focused_tab != None:
            focused_tab.save_document(
                saveas=True, 
                last_dir=self.last_browsed_dir, 
                encoding=encoding
            )
            #Set the icon if it was set by the lexer
            if focused_tab.current_icon != None:
                parent = focused_tab.parent
                parent.setTabIcon(parent.indexOf(focused_tab), focused_tab.current_icon)
            #Save the last browsed directory from the editor widget to the main form
            self.last_browsed_dir = focused_tab.last_browsed_dir
            #Reimport the user configuration file and update the menubar
            if functions.is_config_file(focused_tab.save_name) == True:
                self.import_user_functions()
                self.update_menubar()
    
    def file_save_all(self, encoding="utf-8"):
        """Save all open modified files"""
        #Create a list of the windows
        windows =[self.main_window, self.upper_window, self.lower_window]
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
                    tab.save_document(saveas=False, last_dir=None, encoding=encoding)
                    #Set the icon if it was set by the lexer
                    if tab.current_icon != None:
                        tab.parent.setTabIcon(tab.parent.indexOf(tab), tab.current_icon)
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
        self.menubar = data.QMenuBar(self)
        #Nested function for writing text to the REPL
        def repl_text_input(text,  cursor_position):
            self.repl.setText(text)
            self.repl.setFocus()
            self.repl.setCursorPosition(cursor_position)
        #File menu
        def construct_file_menu():
            file_menu = self.menubar.addMenu("&File")
            def special_create_new_file():
                self.file_create_new()
            new_file_action     = data.QAction('New', self)
            new_file_action.setShortcut(data.new_file_keys)
            new_file_action.setStatusTip('Create new empty file')
            temp_icon = helper_forms.set_icon('tango_icons/document-new.png')
            new_file_action.setIcon(temp_icon)
            new_file_action.triggered.connect(special_create_new_file)
            #Open file
            def special_open_file():
                self.file_open()
            open_file_action = data.QAction('Open', self)
            open_file_action.setShortcut(data.open_file_keys)  
            open_file_action.setStatusTip('Open File')
            temp_icon = helper_forms.set_icon('tango_icons/document-open.png')
            open_file_action.setIcon(temp_icon)
            open_file_action.triggered.connect(special_open_file)
            #Save options need to be saved to a reference for disabling/enabling
            #Save
            def special_save_file():
                self.file_save()
            self.save_file_action = data.QAction('Save', self)
            self.save_file_action.setShortcut(data.save_file_keys)
            self.save_file_action.setStatusTip('Save current file in the UTF-8 encoding')
            self.save_file_action.setEnabled(False)
            temp_icon = helper_forms.set_icon('tango_icons/document-save.png')
            self.save_file_action.setIcon(temp_icon)
            self.save_file_action.triggered.connect(special_save_file)
            #Save as
            def special_saveas_file():
                self.file_saveas()
            self.saveas_file_action = data.QAction('Save As', self)
            self.saveas_file_action.setShortcut(data.saveas_file_keys)
            self.saveas_file_action.setStatusTip('Save current file as a new file in the UTF-8 encoding')
            self.saveas_file_action.setEnabled(False)
            temp_icon = helper_forms.set_icon('tango_icons/document-save-as.png')
            self.saveas_file_action.setIcon(temp_icon)
            self.saveas_file_action.triggered.connect(special_saveas_file)
            #Save all
            def special_save_all():
                self.file_save_all()
            self.save_all_action = data.QAction('Save All', self)
            self.save_all_action.setStatusTip('Save all modified documents in all windows in the UTF-8 encoding')
            self.save_all_action.setEnabled(False)
            temp_icon = helper_forms.set_icon('tango_icons/file-save-all.png')
            self.save_all_action.setIcon(temp_icon)
            self.save_all_action.triggered.connect(special_save_all)
            #Exit
            action_text = 'Exit\tAlt+F4'
            exit_action = data.QAction(action_text, self)     
            exit_action.setStatusTip('Exit application')
            temp_icon = helper_forms.set_icon('tango_icons/system-log-out.png')
            exit_action.setIcon(temp_icon)
            exit_action.triggered.connect(self.exit)
            #Additional menu for saving in different encodings
            def add_save_in_different_encoding_submenu():
                self.save_in_encoding = data.QMenu("Save in encoding...")
                #Save as ASCII encoding
                self.save_ascii_file_action = data.QAction('ASCII', self)
                temp_string = 'Save current file with the ASCII encoding, '
                temp_string += 'unknown characters will be replaced with "?"'
                self.save_ascii_file_action.setStatusTip(temp_string)
                self.save_ascii_file_action.setEnabled(False)
                self.save_ascii_file_action.triggered.connect(
                    functools.partial(self.file_save, encoding="ascii")
                )
                #Save in ANSI Windows encoding
                self.save_ansiwin_file_action = data.QAction('ANSI (Windows)', self)
                temp_string = 'Save current file with the ANSI Windows (CP-1250) encoding with CR+LF line ending, '
                temp_string += 'unknown characters will be replaced with "?"'
                self.save_ansiwin_file_action.setStatusTip(temp_string)
                self.save_ansiwin_file_action.setEnabled(False)
                self.save_ansiwin_file_action.triggered.connect(
                    functools.partial(self.file_save, encoding="cp1250", line_ending="\r\n")
                )
                self.save_in_encoding.addAction(self.save_ascii_file_action)
                self.save_in_encoding.addAction(self.save_ansiwin_file_action)
                self.save_in_encoding.setEnabled(False)
                temp_icon = helper_forms.set_icon('tango_icons/document-save-as.png')
                self.save_in_encoding.setIcon(temp_icon)
                file_menu.addMenu(self.save_in_encoding)
            #Add the closing functions
            def close_tab():
                try:
                    current_window  = self.get_window_by_child_tab()
                    current_index   = current_window.currentIndex()
                    current_window.close_tab(current_index)
                    #Focus the newly displayed tab
                    current_window.currentWidget().setFocus()
                except:
                    pass
            self.menubar_functions["close_tab"] = close_tab
            close_tab_action    = data.QAction('Close Tab', self)
            close_tab_action.setShortcut(data.close_tab_keys)
            close_tab_action.setStatusTip('Close the current tab')
            close_tab_action.triggered.connect(close_tab)
            temp_icon = helper_forms.set_icon('tango_icons/close-tab.png')
            close_tab_action.setIcon(temp_icon)
            close_all_action    = data.QAction('Close All Tabs', self)
            close_all_action.setStatusTip('Close all tabs in the main and upper window')
            close_all_action.triggered.connect(self.close_all_tabs)
            temp_icon = helper_forms.set_icon('tango_icons/close-all-tabs.png')
            close_all_action.setIcon(temp_icon)
            #Add load/save settings options
            save_settings_action    = data.QAction('Save Settings', self)
            save_settings_action.setStatusTip('Save current settings: main window side')
            temp_icon = helper_forms.set_icon('tango_icons/file-settings-save.png')
            save_settings_action.setIcon(temp_icon)
            save_settings_action.triggered.connect(self.settings.save)
            load_settings_action    = data.QAction('Load Settings', self)
            load_settings_action.setStatusTip('Load saved settings: main window side')
            temp_icon = helper_forms.set_icon('tango_icons/file-settings-load.png')
            load_settings_action.setIcon(temp_icon)
            load_settings_action.triggered.connect(self.settings.restore)
            #Add the editing option for the user_functions file
            def open_user_func_file():
                user_definitions_file = os.path.join(data.application_directory, data.config_file)
                #Test if user_functions file exists
                if os.path.isfile(user_definitions_file) == False:
                    self.display.repl_display_message(
                        "User functions file does not exist!", 
                        message_type=data.MessageType.ERROR
                    )
                    return
                self.open_file(user_definitions_file)
            self.menubar_functions["open_user_func_file"] = open_user_func_file
            edit_functions_action   = data.QAction('Edit User Functions', self)
            temp_string = 'Open the {} file for '.format(data.config_file)
            temp_string += 'editing in the main window'
            edit_functions_action.setStatusTip(temp_string)
            temp_icon = helper_forms.set_icon('tango_icons/file-user-funcs.png')
            edit_functions_action.setIcon(temp_icon)
            edit_functions_action.triggered.connect(open_user_func_file)
            #Add the reload option for the user_functions file
            self.menubar_functions["reload_user_func_file"] = self.import_user_functions
            reload_functions_action = data.QAction('Reload User Functions', self)
            temp_string = 'Reload the {} file to '.format(data.config_file)
            temp_string += 'refresh user defined functions'
            reload_functions_action.setStatusTip(temp_string)
            temp_icon = helper_forms.set_icon('tango_icons/file-user-funcs-reload.png')
            reload_functions_action.setIcon(temp_icon)
            reload_functions_action.triggered.connect(self.import_user_functions)
            #Add reload themes function
            self.menubar_functions["themes_reload"] = self.view.reload_themes
            themes_reload_action = data.QAction('Reload Themes', self)
            temp_string = 'Reload themes from modules to update '
            temp_string += 'any changes made in the theme files'
            themes_reload_action.setStatusTip(temp_string)
            temp_icon = helper_forms.set_icon('tango_icons/themes-reload.png')
            themes_reload_action.setIcon(temp_icon)
            themes_reload_action.triggered.connect(self.view.reload_themes)
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
            edit_menu   = self.menubar.addMenu("&Editing")
            def copy():
                try:
                    self.get_tab_by_focus().copy()
                except:
                    pass
            self.menubar_functions["copy"] = copy
            action_text = 'Copy\t' + data.copy_keys
            copy_action = data.QAction(action_text , self)
            temp_string = 'Copy any selected text in the currently '
            temp_string += 'selected window to the clipboard'
            copy_action.setStatusTip(temp_string)
            temp_icon = helper_forms.set_icon('tango_icons/edit-copy.png')
            copy_action.setIcon(temp_icon)
            copy_action.triggered.connect(copy)
            def cut():
                try:
                    self.get_tab_by_focus().cut()
                except:
                    pass
            self.menubar_functions["cut"] = cut
            action_text = 'Cut\t' + data.cut_keys
            cut_action  = data.QAction(action_text, self)
            cut_action.setStatusTip('Cut any selected text in the currently selected window to the clipboard')
            temp_icon = helper_forms.set_icon('tango_icons/edit-cut.png')
            cut_action.setIcon(temp_icon)
            cut_action.triggered.connect(cut)
            def paste():
                try:
                    self.get_tab_by_focus().paste()
                except:
                    pass
            self.menubar_functions["paste"] = paste
            action_text = 'Paste\t' + data.paste_keys
            paste_action    = data.QAction(action_text, self)
            paste_action.setStatusTip('Paste the text in the clipboard to the currenty selected window')
            temp_icon = helper_forms.set_icon('tango_icons/edit-paste.png')
            paste_action.setIcon(temp_icon)
            paste_action.triggered.connect(paste)
            def undo():
                try:
                    self.get_tab_by_focus().undo()
                except:
                    pass
            self.menubar_functions["undo"] = undo
            action_text = 'Undo\t' + data.undo_keys
            undo_action    = data.QAction(action_text, self)
            undo_action.setStatusTip('Undo last editor action in the currenty selected window')
            temp_icon = helper_forms.set_icon('tango_icons/edit-undo.png')
            undo_action.setIcon(temp_icon)
            undo_action.triggered.connect(undo)
            def redo():
                try:
                    self.get_tab_by_focus().redo()
                except:
                    pass
            self.menubar_functions["redo"] = redo
            action_text = 'Redo\t' + data.redo_keys
            redo_action    = data.QAction(action_text, self)
            redo_action.setStatusTip('Redo last undone editor action in the currenty selected window')
            temp_icon = helper_forms.set_icon('tango_icons/edit-redo.png')
            redo_action.setIcon(temp_icon)
            redo_action.triggered.connect(redo)
            def select_all():
                try:
                    self.get_tab_by_focus().selectAll(True)
                except:
                    pass
            self.menubar_functions["select_all"] = select_all
            action_text = 'Select All\t' + data.select_all_keys
            select_all_action = data.QAction(action_text, self)
            select_all_action.setStatusTip('Select all of the text in the currenty selected window')
            temp_icon = helper_forms.set_icon('tango_icons/edit-select-all.png')
            select_all_action.setIcon(temp_icon)
            select_all_action.triggered.connect(select_all)
            def indent():
                try:
                    tab = self.get_tab_by_focus()
                    tab.custom_indent()
                except:
                    pass
            self.menubar_functions["indent"] = indent
            action_text = 'Indent\t' + data.indent_keys
            indent_action = data.QAction(action_text, self)
            indent_action.setStatusTip('Indent the selected lines by the default width (4 spaces) in the currenty selected window')
            temp_icon = helper_forms.set_icon('tango_icons/format-indent-more.png')
            indent_action.setIcon(temp_icon)
            indent_action.triggered.connect(indent)
            def unindent():
                try:
                    tab = self.get_tab_by_focus()
                    tab.custom_unindent()
                except:
                    pass
            self.menubar_functions["unindent"] = unindent
            action_text = 'Unindent\t' + data.unindent_keys
            unindent_action    = data.QAction(action_text, self)
            unindent_action.setStatusTip('Unindent the selected lines by the default width (4 spaces) in the currenty selected window')
            temp_icon = helper_forms.set_icon('tango_icons/format-indent-less.png')
            unindent_action.setIcon(temp_icon)
            unindent_action.triggered.connect(unindent)
            def delete_start_of_word():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.PyQt.Qsci.QsciScintillaBase.SCI_DELWORDLEFT)
                except:
                    pass
            self.menubar_functions["delete_start_of_word"] = delete_start_of_word
            action_text = 'Delete start of word\t' + data.delete_start_of_word_keys
            del_start_word_action    = data.QAction(action_text, self)
            temp_string = 'Delete the current word from the cursor to the starting index of the word'
            del_start_word_action.setStatusTip(temp_string)
            temp_icon = helper_forms.set_icon('tango_icons/delete-end-word.png')
            del_start_word_action.setIcon(temp_icon)
            del_start_word_action.triggered.connect(delete_start_of_word)
            def delete_end_of_word():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.PyQt.Qsci.QsciScintillaBase.SCI_DELWORDRIGHT)
                except:
                    pass
            self.menubar_functions["delete_end_of_word"] = delete_end_of_word
            action_text = 'Delete end of word\t' + data.delete_end_of_word_keys
            del_end_word_action    = data.QAction(action_text, self)
            temp_string = 'Delete the current word from the cursor to the ending index of the word'
            del_end_word_action.setStatusTip(temp_string)
            temp_icon = helper_forms.set_icon('tango_icons/delete-start-word.png')
            del_end_word_action.setIcon(temp_icon)
            del_end_word_action.triggered.connect(delete_end_of_word)
            def delete_start_of_line():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.PyQt.Qsci.QsciScintillaBase.SCI_DELLINELEFT)
                except:
                    pass
            self.menubar_functions["delete_start_of_line"] = delete_start_of_line
            action_text = 'Delete start of line\t' + data.delete_start_of_line_keys
            del_start_line_action    = data.QAction(action_text, self)
            temp_string = 'Delete the current line from the cursor to the starting index of the line'
            del_start_line_action.setStatusTip(temp_string)
            temp_icon = helper_forms.set_icon('tango_icons/delete-start-line.png')
            del_start_line_action.setIcon(temp_icon)
            del_start_line_action.triggered.connect(delete_start_of_line)
            def delete_end_of_line():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.PyQt.Qsci.QsciScintillaBase.SCI_DELLINERIGHT)
                except:
                    pass
            self.menubar_functions["delete_end_of_line"] = delete_end_of_line
            action_text = 'Delete end of line\t' + data.delete_end_of_line_keys
            del_end_line_action    = data.QAction(action_text, self)
            temp_string = 'Delete the current line from the cursor to the ending index of the line'
            del_end_line_action.setStatusTip(temp_string)
            temp_icon = helper_forms.set_icon('tango_icons/delete-end-line.png')
            del_end_line_action.setIcon(temp_icon)
            del_end_line_action.triggered.connect(delete_end_of_line)
            def goto_to_start():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.PyQt.Qsci.QsciScintillaBase.SCI_DOCUMENTSTART)
                except:
                    pass
            self.menubar_functions["goto_to_start"] = goto_to_start
            action_text = 'Go to start\t' + data.go_to_start_keys
            go_to_start_action    = data.QAction(action_text, self)
            temp_string = 'Move cursor up to the start of the currently selected document'
            go_to_start_action.setStatusTip(temp_string)
            temp_icon = helper_forms.set_icon('tango_icons/goto-start.png')
            go_to_start_action.setIcon(temp_icon)
            go_to_start_action.triggered.connect(goto_to_start)
            def goto_to_end():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.PyQt.Qsci.QsciScintillaBase.SCI_DOCUMENTEND)
                except:
                    pass
            self.menubar_functions["goto_to_end"] = goto_to_end
            action_text = 'Go to end\t' + data.go_to_end_keys
            go_to_end_action    = data.QAction(action_text, self)
            temp_string = 'Move cursor down to the end of the currently selected document'
            go_to_end_action.setStatusTip(temp_string)
            temp_icon = helper_forms.set_icon('tango_icons/goto-end.png')
            go_to_end_action.setIcon(temp_icon)
            go_to_end_action.triggered.connect(goto_to_end)
            def select_page_up():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.PyQt.Qsci.QsciScintillaBase.SCI_PAGEUPEXTEND)
                except:
                    pass
            self.menubar_functions["select_page_up"] = select_page_up
            action_text = 'Select page up\t' + data.select_page_up_keys
            select_page_up_action    = data.QAction(action_text, self)
            temp_string = 'Select text up one page of the currently selected document'
            select_page_up_action.setStatusTip(temp_string)
            temp_icon = helper_forms.set_icon("")
            select_page_up_action.setIcon(temp_icon)
            select_page_up_action.triggered.connect(select_page_up)
            def select_page_down():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.PyQt.Qsci.QsciScintillaBase.SCI_PAGEDOWN)
                except:
                    pass
            self.menubar_functions["select_page_down"] = select_page_down
            action_text = 'Select page down\t' + data.select_page_down_keys
            select_page_down_action    = data.QAction(action_text, self)
            temp_string = 'Select text down one page of the currently selected document'
            select_page_down_action.setStatusTip(temp_string)
            temp_icon = helper_forms.set_icon("")
            select_page_down_action.setIcon(temp_icon)
            select_page_down_action.triggered.connect(select_page_down)
            def select_to_start():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.PyQt.Qsci.QsciScintillaBase.SCI_DOCUMENTSTARTEXTEND)
                except:
                    pass
            self.menubar_functions["select_to_start"] = select_to_start
            action_text = 'Select to start\t' + data.select_to_start_keys
            select_to_start_action    = data.QAction(action_text, self)
            temp_string = 'Select all text up to the start of the currently selected document'
            select_to_start_action.setStatusTip(temp_string)
            temp_icon = helper_forms.set_icon("")
            select_to_start_action.setIcon(temp_icon)
            select_to_start_action.triggered.connect(select_to_start)
            def select_to_end():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.PyQt.Qsci.QsciScintillaBase.SCI_DOCUMENTENDEXTEND)
                except:
                    pass
            self.menubar_functions["select_to_end"] = select_to_end
            action_text = 'Select to end\t' + data.select_to_end_keys
            select_to_end_action    = data.QAction(action_text, self)
            temp_string = 'Select all text down to the start of the currently selected document'
            select_to_end_action.setStatusTip(temp_string)
            temp_icon = helper_forms.set_icon("")
            select_to_end_action.setIcon(temp_icon)
            select_to_end_action.triggered.connect(select_to_end)
            def scroll_up():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.PyQt.Qsci.QsciScintillaBase.SCI_PAGEUP)
                except:
                    pass
            self.menubar_functions["scroll_up"] = scroll_up
            action_text = 'Scroll up\t' + data.scroll_up_keys
            scroll_up_action    = data.QAction(action_text, self)
            temp_string = 'Scroll up one page of the currently selected document'
            scroll_up_action.setStatusTip(temp_string)
            temp_icon = helper_forms.set_icon('tango_icons/scroll-up.png')
            scroll_up_action.setIcon(temp_icon)
            scroll_up_action.triggered.connect(scroll_up)
            def scroll_down():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.PyQt.Qsci.QsciScintillaBase.SCI_PAGEDOWN)
                except:
                    pass
            self.menubar_functions["scroll_down"] = scroll_down
            action_text = 'Scroll down\t' + data.scroll_down_keys
            scroll_down_action    = data.QAction(action_text, self)
            temp_string = 'Scroll down one page of the currently selected document'
            scroll_down_action.setStatusTip(temp_string)
            temp_icon = helper_forms.set_icon('tango_icons/scroll-down.png')
            scroll_down_action.setIcon(temp_icon)
            scroll_down_action.triggered.connect(scroll_down)
            def line_cut():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.PyQt.Qsci.QsciScintillaBase.SCI_LINECUT)
                except:
                    pass
            self.menubar_functions["line_cut"] = line_cut
            action_text = 'Line Cut\t' + data.line_cut_keys
            line_cut_action    = data.QAction(action_text, self)
            temp_string = 'Cut out the current line/lines of the currently selected document'
            line_cut_action.setStatusTip(temp_string)
            temp_icon = helper_forms.set_icon('tango_icons/edit-line-cut.png')
            line_cut_action.setIcon(temp_icon)
            line_cut_action.triggered.connect(line_cut)
            def line_copy():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.PyQt.Qsci.QsciScintillaBase.SCI_LINECOPY)
                except:
                    pass
            self.menubar_functions["line_copy"] = line_copy
            action_text = 'Line Copy\t' + data.line_copy_keys
            line_copy_action    = data.QAction(action_text, self)
            temp_string = 'Copy the current line/lines of the currently selected document'
            line_copy_action.setStatusTip(temp_string)
            temp_icon = helper_forms.set_icon('tango_icons/edit-line-copy.png')
            line_copy_action.setIcon(temp_icon)
            line_copy_action.triggered.connect(line_copy)
            def line_delete():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.PyQt.Qsci.QsciScintillaBase.SCI_LINEDELETE)
                except:
                    pass
            self.menubar_functions["line_delete"] = line_delete
            action_text = 'Line Delete\t' + data.line_delete_keys
            line_delete_action    = data.QAction(action_text, self)
            temp_string = 'Delete the current line of the currently selected document'
            line_delete_action.setStatusTip(temp_string)
            temp_icon = helper_forms.set_icon('tango_icons/edit-line-delete.png')
            line_delete_action.setIcon(temp_icon)
            line_delete_action.triggered.connect(line_delete)
            def line_transpose():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.PyQt.Qsci.QsciScintillaBase.SCI_LINETRANSPOSE)
                except:
                    pass
            self.menubar_functions["line_transpose"] = line_transpose
            action_text = 'Line Transpose\t' + data.line_transpose_keys
            line_transpose_action    = data.QAction(action_text, self)
            temp_string = 'Switch the current line with the line above it of the currently selected document'
            line_transpose_action.setStatusTip(temp_string)
            temp_icon = helper_forms.set_icon('tango_icons/edit-line-transpose.png')
            line_transpose_action.setIcon(temp_icon)
            line_transpose_action.triggered.connect(line_transpose)
            def line_duplicate():
                try:
                    send_sci_message = self.get_tab_by_focus().SendScintilla
                    send_sci_message(data.PyQt.Qsci.QsciScintillaBase.SCI_LINEDUPLICATE)
                except:
                    pass
            self.menubar_functions["line_duplicate"] = line_duplicate
            action_text = 'Line/Selection Duplicate\t' + data.line_selection_duplicate_keys
            line_duplicate_action    = data.QAction(action_text, self)
            temp_string = 'Duplicate the current line/selection of the currently selected document'
            line_duplicate_action.setStatusTip(temp_string)
            temp_icon = helper_forms.set_icon('tango_icons/edit-line-duplicate.png')
            line_duplicate_action.setIcon(temp_icon)
            line_duplicate_action.triggered.connect(line_duplicate)
            #Rectangular block selection
            action_text = 'Rectangular block selection\tAlt+Mouse'
            rect_block_action    = data.QAction(action_text, self)
            temp_string = 'Select rectangle using the mouse in the currently selected document'
            rect_block_action.setStatusTip(temp_string)
            temp_icon = helper_forms.set_icon("")
            rect_block_action.setIcon(temp_icon)
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
            edit_menu   = self.menubar.addMenu("&Advanced")
            #Nested special function for finding text in the currentlly focused custom editor
            def special_find():
                try:
                    focused_tab = self.get_used_tab()
                    selected_text = focused_tab.selectedText().replace("\\", "\\\\").replace("\"", "\\\"")
                    temp_string = 'find("{:s}",'.format(selected_text)
                    temp_string += 'case_sensitive=False,'
                    temp_string += 'search_forward=True,'
                    temp_string += 'window_name="{:s}")'.format(focused_tab.parent.name)
                    self.repl.setText(temp_string)
                except:
                    self.repl.setText('find("",case_sensitive=False)')
                self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                self.repl.setFocus()
                self.repl.setCursorPosition(self.repl.text().find('",case_sensitive'))
            self.menubar_functions["special_find"] = special_find
            find_action = data.QAction('Find', self)
            find_action.setShortcut(data.find_keys)
            find_action.setStatusTip('Find text in the currently selected document')
            temp_icon = helper_forms.set_icon('tango_icons/edit-find.png')
            find_action.setIcon(temp_icon)
            find_action.triggered.connect(special_find)
            #Nested special function for finding text in the currentlly focused 
            #custom editor using regular expressions
            def special_regex_find():
                try:
                    focused_tab = self.get_used_tab()
                    selected_text = focused_tab.selectedText().replace("\\", "\\\\").replace("\"", "\\\"")
                    temp_string = 'regex_find(r"{:s}",'.format(selected_text)
                    temp_string += 'case_sensitive=False,'
                    temp_string += 'search_forward=True,'
                    temp_string += 'window_name="{:s}")'.format(focused_tab.parent.name)
                    self.repl.setText(temp_string)
                except:
                    self.repl.setText('regex_find(r"",case_sensitive=False)')
                self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                self.repl.setFocus()
                self.repl.setCursorPosition(self.repl.text().find('",case_sensitive'))
            self.menubar_functions["special_regex_find"] = special_regex_find
            regex_find_action = data.QAction('Regex Find', self)
            regex_find_action.setShortcut(data.regex_find_keys)
            regex_find_action.setStatusTip(
                'Find text in currently selected document using Python regular expressions'
            )
            temp_icon = helper_forms.set_icon('tango_icons/edit-find-re.png')
            regex_find_action.setIcon(temp_icon)
            regex_find_action.triggered.connect(special_regex_find)
            #Nested special function for finding and replacing one instance of text in the current main window custom editor
            def special_find_and_replace():
                try:
                    focused_tab = self.get_used_tab()
                    selected_text = focused_tab.selectedText().replace("\\", "\\\\").replace("\"", "\\\"")
                    temp_string = 'find_and_replace("{:s}","",'.format(selected_text)
                    temp_string += 'case_sensitive=False,'
                    temp_string += 'search_forward=True,'
                    temp_string += 'window_name="{:s}")'.format(focused_tab.parent.name)
                    self.repl.setText(temp_string)
                except:
                    self.repl.setText('find_and_replace("","",case_sensitive=False)')
                self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                self.repl.setFocus()
                self.repl.setCursorPosition(self.repl.text().find('",case_sensitive'))
            self.menubar_functions["special_find_and_replace"] = special_find_and_replace
            find_and_replace_action = data.QAction('Find and Replace', self)
            find_and_replace_action.setShortcut(data.find_and_replace_keys)
            temp_string = 'Find and replace one instance of text '
            temp_string += 'from cursor in currently selected document'
            find_and_replace_action.setStatusTip(temp_string)
            temp_icon = helper_forms.set_icon('tango_icons/edit-find-replace.png')
            find_and_replace_action.setIcon(temp_icon)
            find_and_replace_action.triggered.connect(special_find_and_replace)
            #Nested special function for finding and replacing one instance of text
            #in the current main window custom editor using regular expressions
            def special_regex_find_and_replace():
                try:
                    focused_tab = self.get_used_tab()
                    selected_text = focused_tab.selectedText().replace("\\", "\\\\").replace("\"", "\\\"")
                    temp_string = 'regex_find_and_replace(r"{:s}",r"",'.format(selected_text)
                    temp_string += 'case_sensitive=False,'
                    temp_string += 'search_forward=True,'
                    temp_string += 'window_name="{:s}")'.format(focused_tab.parent.name)
                    self.repl.setText(temp_string)
                except:
                    self.repl.setText('regex_find_and_replace(r"",r"",case_sensitive=False)')
                self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                self.repl.setFocus()
                self.repl.setCursorPosition(self.repl.text().find('",case_sensitive'))
            self.menubar_functions["special_regex_find_and_replace"] = special_regex_find_and_replace
            regex_find_and_replace_action = data.QAction('Regex Find and Replace', self)
            regex_find_and_replace_action.setShortcut(data.regex_find_and_replace_keys)
            temp_string = 'Find and replace one instance of text '
            temp_string += 'from cursor in currently selected document '
            temp_string += 'using Python regular expressions'
            regex_find_and_replace_action.setStatusTip(temp_string)
            temp_icon = helper_forms.set_icon('tango_icons/edit-find-replace-re.png')
            regex_find_and_replace_action.setIcon(temp_icon)
            regex_find_and_replace_action.triggered.connect(special_regex_find_and_replace)
            def special_highlight():
                try:
                    focused_tab = self.get_used_tab()
                    selected_text = focused_tab.selectedText().replace("\\", "\\\\").replace("\"", "\\\"")
                    temp_string = 'highlight("{:s}",'.format(selected_text)
                    temp_string += 'case_sensitive=False,'
                    temp_string += 'window_name="{:s}")'.format(focused_tab.parent.name)
                    self.repl.setText(temp_string)
                except:
                    self.repl.setText('highlight("",case_sensitive=False)')
                self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                self.repl.setFocus()
                self.repl.setCursorPosition(self.repl.text().find('",case_sensitive'))
            self.menubar_functions["special_highlight"] = special_highlight
            highlight_action = data.QAction('Highlight', self)
            highlight_action.setShortcut(data.highlight_keys)
            highlight_action.setStatusTip('Highlight all instances of text in currently selected document')
            temp_icon = helper_forms.set_icon('tango_icons/edit-highlight.png')
            highlight_action.setIcon(temp_icon)
            highlight_action.triggered.connect(special_highlight)
            def special_regex_highlight():
                try:
                    focused_tab = self.get_used_tab()
                    selected_text = focused_tab.selectedText().replace("\\", "\\\\").replace("\"", "\\\"")
                    temp_string = 'regex_highlight(r"{:s}",'.format(selected_text)
                    temp_string += 'case_sensitive=False,'
                    temp_string += 'window_name="{:s}")'.format(focused_tab.parent.name)
                    self.repl.setText(temp_string)
                except:
                    self.repl.setText('regex_highlight(r"",case_sensitive=False)')
                self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                self.repl.setFocus()
                self.repl.setCursorPosition(self.repl.text().find('",case_sensitive'))
            self.menubar_functions["special_regex_highlight"] = special_regex_highlight
            regex_highlight_action = data.QAction('Regex Highlight', self)
            regex_highlight_action.setShortcut(data.regex_highlight_keys)
            temp_string = "Highlight all instances of text in currently "
            temp_string += "selected document using Python regular expressions"
            regex_highlight_action.setStatusTip(temp_string)
            temp_icon = helper_forms.set_icon('tango_icons/edit-highlight-re.png')
            regex_highlight_action.setIcon(temp_icon)
            regex_highlight_action.triggered.connect(special_regex_highlight)
            def special_clear_highlights():
                try:
                    focused_tab = self.get_used_tab()
                    self.repl.setText('clear_highlights(window_name="{:s}")'.format(focused_tab.parent.name))
                except:
                    self.repl.setText('clear_highlights()')
                self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                self.repl.setFocus()
                self.repl.setCursorPosition(len(self.repl.text()))
            self.menubar_functions["special_clear_highlights"] = special_clear_highlights
            clear_highlights_action = data.QAction('Clear Highlights', self)
            clear_highlights_action.setShortcut(data.clear_highlights_keys)
            clear_highlights_action.setStatusTip('Clear all in currently selected document')
            temp_icon = helper_forms.set_icon('tango_icons/edit-clear-highlights.png')
            clear_highlights_action.setIcon(temp_icon)
            clear_highlights_action.triggered.connect(special_clear_highlights)
            def special_replace_in_selection():
                try:
                    focused_tab = self.get_used_tab()
                    temp_string = 'replace_in_selection("","",case_sensitive=False,'
                    temp_string += 'window_name="{:s}")'.format(focused_tab.parent.name)                                  
                    self.repl.setText(temp_string)
                except:
                    self.repl.setText('replace_in_selection("","",case_sensitive=False)')
                self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                self.repl.setFocus()
                self.repl.setCursorPosition(self.repl.text().find('","",case_sensitive'))
            self.menubar_functions["special_replace_in_selection"] = special_replace_in_selection
            replace_selection_action = data.QAction('Replace In Selection', self)
            replace_selection_action.setShortcut(data.replace_selection_keys)
            temp_string = 'Replace all instances of text in the '
            temp_string += 'selected text of the current selected document'
            replace_selection_action.setStatusTip(temp_string)
            temp_icon = helper_forms.set_icon('tango_icons/edit-replace-in-selection.png')
            replace_selection_action.setIcon(temp_icon)
            replace_selection_action.triggered.connect(special_replace_in_selection)
            def special_regex_replace_in_selection():
                try:
                    focused_tab = self.get_used_tab()
                    temp_string = 'regex_replace_in_selection(r"",r"",case_sensitive=False,'
                    temp_string += 'window_name="{:s}")'.format(focused_tab.parent.name)                                  
                    self.repl.setText(temp_string)
                except:
                    self.repl.setText('regex_replace_in_selection(r"",r"",case_sensitive=False)')
                self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                self.repl.setFocus()
                self.repl.setCursorPosition(self.repl.text().find('",r"",case_sensitive'))
            self.menubar_functions["special_regex_replace_in_selection"] = special_regex_replace_in_selection
            regex_replace_selection_action = data.QAction('Regex Replace In Selection', self)
            regex_replace_selection_action.setShortcut(data.regex_replace_selection_keys)
            temp_string = 'Replace all instances of text in the '
            temp_string += 'selected text of the current selected document'
            temp_string += 'using Python regular expressions'
            regex_replace_selection_action.setStatusTip(temp_string)
            temp_icon = helper_forms.set_icon('tango_icons/edit-replace-in-selection-re.png')
            regex_replace_selection_action.setIcon(temp_icon)
            regex_replace_selection_action.triggered.connect(special_regex_replace_in_selection)
            #Nested special function for replacing all instances of text in
            #the selected custom editor
            def special_replace_all():
                try:
                    focused_tab = self.get_used_tab()
                    selected_text = focused_tab.selectedText().replace("\\", "\\\\").replace("\"", "\\\"")
                    temp_string = 'replace_all("{:s}","",'.format(selected_text)
                    temp_string += 'case_sensitive=False,'
                    temp_string += 'window_name="{:s}")'.format(focused_tab.parent.name)
                    self.repl.setText(temp_string)
                except:
                    self.repl.setText('replace_all("","",case_sensitive=False)')
                self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                self.repl.setFocus()
                self.repl.setCursorPosition(self.repl.text().find('",case_sensitive'))
            self.menubar_functions["special_replace_all"] = special_replace_all
            replace_all_action = data.QAction('Replace All', self)
            replace_all_action.setShortcut(data.replace_all_keys)
            replace_all_action.setStatusTip('Replace all instances of text in currently selected document')
            temp_icon = helper_forms.set_icon('tango_icons/edit-replace-all.png')
            replace_all_action.setIcon(temp_icon)
            replace_all_action.triggered.connect(special_replace_all)
            #Nested special function for replacing all instances of text in
            #the selected custom editor using regular expressions
            def special_regex_replace_all():
                try:
                    focused_tab = self.get_used_tab()
                    selected_text = focused_tab.selectedText().replace("\\", "\\\\").replace("\"", "\\\"")
                    temp_string = 'regex_replace_all(r"{:s}",r"",'.format(selected_text)
                    temp_string += 'case_sensitive=False,'
                    temp_string += 'window_name="{:s}")'.format(focused_tab.parent.name)
                    self.repl.setText(temp_string)
                except:
                    self.repl.setText('regex_replace_all(r"",r"",case_sensitive=False)')
                self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                self.repl.setFocus()
                self.repl.setCursorPosition(self.repl.text().find('",case_sensitive'))
            self.menubar_functions["special_regex_replace_all"] = special_regex_replace_all
            regex_replace_all_action    = data.QAction('Regex Replace All', self)
            regex_replace_all_action.setShortcut(data.regex_replace_all_keys)
            regex_replace_all_action.setStatusTip('Replace all instances of text in currently selected document using Python regular expressions')
            temp_icon = helper_forms.set_icon('tango_icons/edit-replace-all-re.png')
            regex_replace_all_action.setIcon(temp_icon)
            regex_replace_all_action.triggered.connect(special_regex_replace_all)
            #Nested special function for un/commenting selected lines in the main widget
            def comment_uncomment():
                try:
                    self.get_tab_by_focus().toggle_comment_uncomment()
                except:
                    pass
            self.menubar_functions["comment_uncomment"] = comment_uncomment
            toggle_comment_action   = data.QAction('Comment/Uncomment', self)
            toggle_comment_action.setShortcut(data.toggle_comment_keys)
            temp_string = 'Toggle comments for the selected lines or single line'
            temp_string += " in the currently selected document"
            toggle_comment_action.setStatusTip(temp_string)
            temp_icon = helper_forms.set_icon('tango_icons/edit-comment-uncomment.png')
            toggle_comment_action.setIcon(temp_icon)
            toggle_comment_action.triggered.connect(comment_uncomment)
            def toggle_autocompletions():
                try:
                    self.get_tab_by_focus().toggle_autocompletions()
                except:
                    pass
            self.menubar_functions["toggle_autocompletions"] = toggle_autocompletions
            toggle_autocompletion_action = data.QAction('Enable/Disable Autocompletion', self)
            toggle_autocompletion_action.setShortcut(data.toggle_autocompletion_keys)
            temp_string = 'Enable/Disable autocompletions '
            temp_string += 'for the currently selected document'
            toggle_autocompletion_action.setStatusTip(temp_string)
            temp_icon = helper_forms.set_icon('tango_icons/edit-autocompletion.png')
            toggle_autocompletion_action.setIcon(temp_icon)
            toggle_autocompletion_action.triggered.connect(toggle_autocompletions)
            def toggle_wordwrap():
                try:
                    self.get_tab_by_focus().toggle_wordwrap()
                except:
                    pass
            self.menubar_functions["toggle_wordwrap"] = toggle_wordwrap
            toggle_wrap_action = data.QAction('Enable/Disable Line Wrapping', self)
            toggle_wrap_action.setShortcut(data.toggle_wrap_keys)
            temp_string = 'Enable/Disable line wrapping '
            temp_string += 'for the currently selected document'
            toggle_wrap_action.setStatusTip(temp_string)
            temp_icon = helper_forms.set_icon('tango_icons/wordwrap.png')
            toggle_wrap_action.setIcon(temp_icon)
            toggle_wrap_action.triggered.connect(toggle_wordwrap)
            def reload_file():
                try:
                    self.get_tab_by_focus().reload_file()
                except:
                    pass
            self.menubar_functions["reload_file"] = reload_file
            reload_file_action = data.QAction('Reload file', self)
            reload_file_action.setShortcut(data.reload_file_keys)
            reload_file_action.setStatusTip('Reload file from disk, will prompt if file contains changes')
            temp_icon = helper_forms.set_icon('tango_icons/view-refresh.png')
            reload_file_action.setIcon(temp_icon)
            reload_file_action.triggered.connect(reload_file)
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
            self.menubar_functions["create_node_tree"] = create_node_tree
            node_tree_action = data.QAction('Create/reload node tree (C / Nim / Python3)', self)
            node_tree_action.setShortcut(data.node_tree_keys)
            temp_string = 'Create a node tree for the code for the '
            temp_string += 'currently selected document (C / Nim / Python3)'
            node_tree_action.setStatusTip(temp_string)
            temp_icon = helper_forms.set_icon('tango_icons/edit-node-tree.png')
            node_tree_action.setIcon(temp_icon)
            node_tree_action.triggered.connect(create_node_tree)
            def special_goto_line():
                try:
                    focused_tab = self.get_used_tab()
                    self.repl.setText('goto_line(,window_name="{:s}")'.format(focused_tab.parent.name))
                    self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                    self.repl.setCursorPosition(self.repl.text().find(',window_name'))
                except:
                    self.repl.setText('goto_line()')
                    self.repl.setCursorPosition(len(self.repl.text())-1)
                self.repl.setFocus()
            self.menubar_functions["special_goto_line"] = special_goto_line
            goto_line_action = data.QAction('Goto line', self)
            goto_line_action.setShortcut(data.goto_line_keys)
            goto_line_action.setStatusTip('Go to the specified line in the current main window document')
            temp_icon = helper_forms.set_icon('tango_icons/edit-goto.png')
            goto_line_action.setIcon(temp_icon)
            goto_line_action.triggered.connect(special_goto_line)
            def special_indent_to_cursor():
                try:
                    self.get_tab_by_focus().indent_lines_to_cursor()
                except:
                    pass
            self.menubar_functions["special_indent_to_cursor"] = special_indent_to_cursor
            indent_to_cursor_action = data.QAction('Indent to cursor', self)
            indent_to_cursor_action.setShortcut(data.indent_to_cursor_keys)
            temp_string = 'Indent the selected lines to the current cursor position '
            temp_string += '(SPACE ON THE LEFT SIDE OF LINES IS STRIPPED!)'
            indent_to_cursor_action.setStatusTip(temp_string)
            temp_icon = helper_forms.set_icon('tango_icons/edit-indent-to-cursor.png')
            indent_to_cursor_action.setIcon(temp_icon)
            indent_to_cursor_action.triggered.connect(special_indent_to_cursor)
            def special_to_uppercase():
                focused_tab = self.get_used_tab()
                self.editing.convert_to_uppercase(focused_tab.parent.name)
            self.menubar_functions["special_to_uppercase"] = special_to_uppercase
            to_uppercase_action = data.QAction('Selection to UPPERCASE', self)
            to_uppercase_action.setShortcut(data.to_uppercase_keys)
            to_uppercase_action.setStatusTip('Convert selected text to UPPERCASE')
            temp_icon = helper_forms.set_icon('tango_icons/edit-case-to-upper.png')
            to_uppercase_action.setIcon(temp_icon)
            to_uppercase_action.triggered.connect(special_to_uppercase)
            def special_to_lowercase():
                focused_tab = self.get_used_tab()
                self.editing.convert_to_lowercase(focused_tab.parent.name)
            self.menubar_functions["special_to_lowercase"] = special_to_lowercase
            to_lowercase_action = data.QAction('Selection to lowercase', self)
            to_lowercase_action.setShortcut(data.to_lowercase_keys)
            to_lowercase_action.setStatusTip('Convert selected text to lowercase')
            temp_icon = helper_forms.set_icon('tango_icons/edit-case-to-lower.png')
            to_lowercase_action.setIcon(temp_icon)
            to_lowercase_action.triggered.connect(special_to_lowercase)
            #Nested function for finding files in open documents
            def special_find_in_open_documents():
                try:
                    focused_tab = self.get_used_tab()
                    selected_text = focused_tab.selectedText().replace("\\", "\\\\").replace("\"", "\\\"")
                    repl_text = 'find_in_open_documents("{:s}"'.format(selected_text)
                    repl_text += ",case_sensitive=False,regular_expression=False"
                    repl_text += ',window_name="{:s}")'.format(focused_tab.parent.name)
                    self.repl.setText(repl_text)
                except:
                    self.repl.setText('find_in_open_documents("",case_sensitive=False,regular_expression=False)')
                self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                self.repl.setCursorPosition(self.repl.text().find('",case_sensitive'))
                self.repl.setFocus()
            self.menubar_functions["special_find_in_open_documents"] = special_find_in_open_documents
            find_in_documents_action = data.QAction('Find in open documents', self)
            find_in_documents_action.setShortcut(data.find_in_documents_keys)
            temp_string = 'Find string/regular expression across all open documents'
            temp_string += ' in the currently selected window'
            find_in_documents_action.setStatusTip(temp_string)
            temp_icon = helper_forms.set_icon('tango_icons/edit-find-in-open-documents.png')
            find_in_documents_action.setIcon(temp_icon)
            find_in_documents_action.triggered.connect(
                special_find_in_open_documents
            )
            #Nested function for finding and replacing text in open documents
            def special_find_replace_in_open_documents():
                try:
                    focused_tab = self.get_used_tab()
                    selected_text = focused_tab.selectedText().replace("\\", "\\\\").replace("\"", "\\\"")
                    repl_text = 'find_replace_in_open_documents("{:s}",""'.format(selected_text)
                    repl_text += ",case_sensitive=False,regular_expression=False"
                    repl_text += ',window_name="{:s}")'.format(focused_tab.parent.name)
                    self.repl.setText(repl_text)
                except:
                    self.repl.setText('find_replace_in_open_documents("","",case_sensitive=False,regular_expression=False)')
                self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                self.repl.setCursorPosition(self.repl.text().find('",case_sensitive'))
                self.repl.setFocus()
            self.menubar_functions["special_find_replace_in_open_documents"] = special_find_replace_in_open_documents
            find_replace_in_documents_action = data.QAction('Find and replace in open documents', self)
            find_replace_in_documents_action.setShortcut(data.find_replace_in_documents_keys)
            temp_string = 'Find and replace across all open documents in'
            temp_string += ' the currently selected window'
            find_replace_in_documents_action.setStatusTip(temp_string)
            temp_icon = helper_forms.set_icon('tango_icons/edit-replace-in-open-documents.png')
            find_replace_in_documents_action.setIcon(temp_icon)
            find_replace_in_documents_action.triggered.connect(
                special_find_replace_in_open_documents
            )
            #Nested function for replacing all string instances in open documents
            def special_replace_all_in_open_documents():
                try:
                    focused_tab = self.get_used_tab()
                    selected_text = focused_tab.selectedText().replace("\\", "\\\\").replace("\"", "\\\"")
                    repl_text = 'replace_all_in_open_documents("{:s}",""'.format(selected_text)
                    repl_text += ",case_sensitive=False,regular_expression=False"
                    repl_text += ',window_name="{:s}")'.format(focused_tab.parent.name)
                    self.repl.setText(repl_text)
                except:
                    self.repl.setText('replace_all_in_open_documents("","",case_sensitive=False,regular_expression=False)')
                self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                self.repl.setCursorPosition(self.repl.text().find('",case_sensitive'))
                self.repl.setFocus()
            self.menubar_functions["special_replace_all_in_open_documents"] = special_replace_all_in_open_documents
            replace_all_in_documents_action = data.QAction('Replace all in open documents', self)
            replace_all_in_documents_action.setShortcut(data.replace_all_in_documents_keys)
            replace_all_in_documents_action.setStatusTip('Replace all instances of search text across all open documents in the currently selected window')
            temp_icon = helper_forms.set_icon('tango_icons/edit-replace-all-in-open-documents.png')
            replace_all_in_documents_action.setIcon(temp_icon)
            replace_all_in_documents_action.triggered.connect(
                special_replace_all_in_open_documents
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
            edit_menu.addSeparator()
            edit_menu.addAction(find_in_documents_action)
            edit_menu.addAction(find_replace_in_documents_action)
            edit_menu.addAction(replace_all_in_documents_action)
        #System menu
        def construct_system_menu():
            system_menu    = self.menubar.addMenu("S&ystem")
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
            self.menubar_functions["special_find_in"]               = special_find_in
            self.menubar_functions["special_find_in_with_dialog"]   = special_find_in_with_dialog
            find_in_files_action    = data.QAction('Find in files', self)
            find_in_files_action.setShortcut(data.find_in_files_keys)
            temp_string = 'Find all the files in a directory/subdirectories '
            temp_string += 'that contain the search string'
            find_in_files_action.setStatusTip(temp_string)
            temp_icon = helper_forms.set_icon('tango_icons/system-find-in-files.png')
            find_in_files_action.setIcon(temp_icon)
            find_in_files_action.triggered.connect(special_find_in)
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
            self.menubar_functions["special_find_file"]             = special_find_file
            self.menubar_functions["special_find_file_with_dialog"] = special_find_file_with_dialog
            find_files_action   = data.QAction('Find files', self)
            find_files_action.setShortcut(data.find_files_keys)
            temp_string = 'Find all the files in a directory/subdirectories '
            temp_string += 'that have the search string in them'
            find_files_action.setStatusTip(temp_string)
            temp_icon = helper_forms.set_icon('tango_icons/system-find-files.png')
            find_files_action.setIcon(temp_icon)
            find_files_action.triggered.connect(special_find_file)
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
            self.menubar_functions["special_replace_in_files"]              = special_replace_in_files
            self.menubar_functions["special_replace_in_files_with_dialog"]  = special_replace_in_files_with_dialog
            replace_in_files_action = data.QAction('Replace in files', self)
            replace_in_files_action.setShortcut(data.replace_in_files_keys)
            temp_string = 'Find all the files in a directory/subdirectories '
            temp_string += 'that have the search string in them and replace all '
            temp_string += 'instances in the file with the replace string'
            replace_in_files_action.setStatusTip(temp_string)
            temp_icon = helper_forms.set_icon('tango_icons/system-replace-in-files.png')
            replace_in_files_action.setIcon(temp_icon)
            replace_in_files_action.triggered.connect(special_replace_in_files)
            def special_run_command():
                self.repl.setText('run("",show_console=True)')
                self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                self.repl.setFocus()
                self.repl.setCursorPosition(self.repl.text().find('",show_'))
            self.menubar_functions["special_run_command"] = special_run_command
            run_command_action  = data.QAction('Run command', self)
            run_command_action.setStatusTip('Run command as a new process (FULLY TESTED ONLY ON WINDOWS!)')
            temp_icon = helper_forms.set_icon('tango_icons/utilities-terminal.png')
            run_command_action.setIcon(temp_icon)
            run_command_action.triggered.connect(special_run_command)
            def create_cwd_tree():
                self.display.show_directory_tree(os.getcwd())
            self.menubar_functions["create_cwd_tree"] = create_cwd_tree
            cwd_tree_action = data.QAction('Show current working directory tree', self)
            cwd_tree_action.setShortcut(data.cwd_tree_keys)
            temp_string = 'Create a node tree for the current working directory (CWD)'
            cwd_tree_action.setStatusTip(temp_string)
            temp_icon = helper_forms.set_icon('tango_icons/system-show-cwd-tree.png')
            cwd_tree_action.setIcon(temp_icon)
            cwd_tree_action.triggered.connect(create_cwd_tree)
            system_menu.addAction(find_files_action)
            system_menu.addAction(find_in_files_action)
            system_menu.addAction(replace_in_files_action)
            system_menu.addAction(cwd_tree_action)
            system_menu.addAction(run_command_action)
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
                    message = "Lexer changed to: {:s}".format(lexer_name)
                    self.display.repl_display_message(message)
                except Exception as ex:
                    print(ex)
                    message = "Error with lexer selection!\n"
                    message += "Select a window widget with an opened document first."
                    self.display.repl_display_message(
                        message, 
                        message_type=data.MessageType.ERROR
                    )
                    self.display.write_to_statusbar(message)
            lexers_menu = self.display.create_lexers_menu(
                "Change lexer", 
                parent,
                set_lexer
            )
            temp_icon = helper_forms.set_icon('tango_icons/lexers.png')
            lexers_menu.setIcon(temp_icon)
            parent.addMenu(lexers_menu)
        #View menu
        def construct_view_menu():
            view_menu = self.menubar.addMenu("&View")
            #Show/hide the function wheel
            function_wheel_toggle_action = data.QAction('Show/Hide Function Wheel', self)
            function_wheel_toggle_action.setShortcut(data.function_wheel_toggle_keys)
            function_wheel_toggle_action.setStatusTip('Show/hide the Ex.Co. function wheel')
            temp_icon = helper_forms.set_icon('Exco_Icon.png')
            function_wheel_toggle_action.setIcon(temp_icon)
            function_wheel_toggle_action.triggered.connect(self.view.toggle_function_wheel)
            #Maximize/minimize entire Ex.Co. window
            maximize_window_action  = data.QAction('Maximize/Normalize', self)
            maximize_window_action.setShortcut(data.maximize_window_keys)
            maximize_window_action.setStatusTip('Maximize/Normalize application window')
            temp_icon = helper_forms.set_icon('tango_icons/view-fullscreen.png')
            maximize_window_action.setIcon(temp_icon)
            maximize_window_action.triggered.connect(self.view.toggle_window_size)
            main_focus_action = data.QAction('Focus Main window', self)  
            main_focus_action.setShortcut(data.main_focus_keys)
            main_focus_action.setStatusTip('Set focus to the Main editing window')
            temp_icon = helper_forms.set_icon('tango_icons/view-focus-main.png')
            main_focus_action.setIcon(temp_icon)
            main_focus_action.triggered.connect(
                functools.partial(self.view.set_window_focus, "main")
            )
            upper_focus_action = data.QAction('Focus Upper window', self) 
            upper_focus_action.setShortcut(data.upper_focus_keys)
            upper_focus_action.setStatusTip('Set focus to the Upper editing window')
            temp_icon = helper_forms.set_icon('tango_icons/view-focus-upper.png')
            upper_focus_action.setIcon(temp_icon)
            upper_focus_action.triggered.connect(
                functools.partial(self.view.set_window_focus, "upper")
            )
            lower_focus_action = data.QAction('Focus Lower window', self) 
            lower_focus_action.setShortcut(data.lower_focus_keys)
            lower_focus_action.setStatusTip('Set focus to the Lower editing window')
            temp_icon = helper_forms.set_icon('tango_icons/view-focus-lower.png')
            lower_focus_action.setIcon(temp_icon)
            lower_focus_action.triggered.connect(
                functools.partial(self.view.set_window_focus, "lower")
            )
            toggle_log_action = data.QAction('Show/Hide Log Window', self) 
            toggle_log_action.setShortcut(data.toggle_log_keys)
            toggle_log_action.setStatusTip('Toggle the display of the log window')
            temp_icon = helper_forms.set_icon('tango_icons/view-log.png')
            toggle_log_action.setIcon(temp_icon)
            toggle_log_action.triggered.connect(self.view.toggle_log_window)
            spin_clockwise_action = data.QAction('Spin view clockwise', self)  
            spin_clockwise_action.setShortcut(data.spin_clockwise_keys)
            spin_clockwise_action.setStatusTip('Spin the editor windows clockwise')
            temp_icon = helper_forms.set_icon('tango_icons/view-spin-clock.png')
            spin_clockwise_action.setIcon(temp_icon)
            spin_clockwise_action.triggered.connect(self.view.spin_widgets_clockwise)
            spin_counterclockwise_action = data.QAction('Spin view counter-clockwise', self)
            spin_counterclockwise_action.setShortcut(data.spin_counterclockwise_keys)
            spin_counterclockwise_action.setStatusTip('Spin the editor windows counter-clockwise')
            temp_icon = helper_forms.set_icon('tango_icons/view-spin-counter.png')
            spin_counterclockwise_action.setIcon(temp_icon)
            spin_counterclockwise_action.triggered.connect(self.view.spin_widgets_counterclockwise)
            toggle_mode_action = data.QAction('Toggle window mode', self)
            toggle_mode_action.setShortcut(data.toggle_mode_keys)
            toggle_mode_action.setStatusTip('Toggle between one and three window display')
            temp_icon = helper_forms.set_icon('tango_icons/view-toggle-window-mode.png')
            toggle_mode_action.setIcon(temp_icon)
            toggle_mode_action.triggered.connect(self.view.toggle_window_mode)
            toggle_main_window_side_action = data.QAction('Toggle main window side', self)
            toggle_main_window_side_action.setShortcut(data.toggle_main_window_side_keys)
            toggle_main_window_side_action.setStatusTip('Toggle which side the main window is on')
            temp_icon = helper_forms.set_icon('tango_icons/view-toggle-window-side.png')
            toggle_main_window_side_action.setIcon(temp_icon)
            toggle_main_window_side_action.triggered.connect(self.view.toggle_main_window_side)
            def move_tab(direction):
                try:
                    self.get_window_by_child_tab().move_tab(direction)
                except:
                    pass
            self.menubar_functions["move_tab_right"] = functools.partial(move_tab, direction=data.Direction.RIGHT)
            self.menubar_functions["move_tab_left"] = functools.partial(move_tab, direction=data.Direction.LEFT)
            move_tab_right_action = data.QAction('Move tab right', self)
            move_tab_right_action.setShortcut(data.move_tab_right_keys)
            move_tab_right_action.setStatusTip('Move the current tab in the currently selected window one position to the right')
            temp_icon = helper_forms.set_icon('tango_icons/view-move-tab-right.png')
            move_tab_right_action.setIcon(temp_icon)
            move_tab_right_action.triggered.connect(
                functools.partial(move_tab, direction=data.Direction.RIGHT)
            )
            move_tab_left_action = data.QAction('Move tab left', self)
            move_tab_left_action.setShortcut(data.move_tab_left_keys)
            move_tab_left_action.setStatusTip('Move the current tab in the currently selected window one position to the left')
            temp_icon = helper_forms.set_icon('tango_icons/view-move-tab-left.png')
            move_tab_left_action.setIcon(temp_icon)
            move_tab_left_action.triggered.connect(
                functools.partial(move_tab, direction=data.Direction.LEFT)
            )
            def show_edge():
                try:
                    self.get_tab_by_focus().edge_marker_toggle()
                except:
                    pass
            self.menubar_functions["show_edge"] = show_edge
            toggle_edge_action = data.QAction('Toggle edge marker', self)
            toggle_edge_action.setShortcut(data.toggle_edge_keys)
            toggle_edge_action.setStatusTip('Toggle the display of the edge marker that shows the prefered maximum chars in a line')
            temp_icon = helper_forms.set_icon('tango_icons/view-edge-marker.png')
            toggle_edge_action.setIcon(temp_icon)
            toggle_edge_action.triggered.connect(show_edge)
            def reset_zoom():
                try:
                    self.get_tab_by_focus().parent.zoom_reset()
                except:
                    pass
            self.menubar_functions["reset_zoom"] = reset_zoom
            reset_zoom_action = data.QAction('Zoom reset', self)
            reset_zoom_action.setShortcut(data.reset_zoom_keys)
            reset_zoom_action.setStatusTip('Reset the zoom level on the currently focused document!')
            temp_icon = helper_forms.set_icon('tango_icons/view-zoom-reset.png')
            reset_zoom_action.setIcon(temp_icon)
            reset_zoom_action.triggered.connect(reset_zoom)
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
            def bookmarks_clear():
                self.bookmarks.clear()
            self.menubar_functions["bookmarks_clear"] = bookmarks_clear
            def bookmark_toggle():
                try:
                    self.get_tab_by_focus().bookmarks.toggle()
                except:
                    pass
            self.menubar_functions["bookmark_toggle"] = bookmark_toggle
            bookmark_menu = view_menu.addMenu("&Bookmarks")
            temp_icon = helper_forms.set_icon('tango_icons/bookmarks.png')
            bookmark_menu.setIcon(temp_icon)
            bookmark_toggle_action = data.QAction('Toggle Bookmark', self)
            bookmark_toggle_action.setShortcut(data.bookmark_toggle_keys)
            bookmark_toggle_action.setStatusTip("Toggle a bookmark at the current document line")
            temp_icon = helper_forms.set_icon('tango_icons/bookmark.png')
            bookmark_toggle_action.setIcon(temp_icon)
            bookmark_toggle_action.triggered.connect(bookmark_toggle)
            bookmark_menu.addAction(bookmark_toggle_action)
            bookmark_clear_action = data.QAction('Clear Bookmarks', self)
            bookmark_clear_action.setStatusTip("Clear all bookmarks")
            temp_icon = helper_forms.set_icon('tango_icons/bookmarks-clear.png')
            bookmark_clear_action.setIcon(temp_icon)
            bookmark_clear_action.triggered.connect(bookmarks_clear)
            bookmark_menu.addAction(bookmark_clear_action)
            bookmark_menu.addSeparator()
            bookmark_goto_menu = bookmark_menu.addMenu("Go To")
            temp_icon = helper_forms.set_icon('tango_icons/bookmarks-goto.png')
            bookmark_goto_menu.setIcon(temp_icon)
            bookmark_store_menu = bookmark_menu.addMenu("Store")
            temp_icon = helper_forms.set_icon('tango_icons/bookmarks-store.png')
            bookmark_store_menu.setIcon(temp_icon)
            for i in range(10):
                #Go To
                bookmark_goto_action = data.QAction('Bookmark {:d}'.format(i), self)
                bookmark_goto_action.setShortcut("{}+{}".format(data.bookmark_goto_keys, i))
                bookmark_goto_action.setStatusTip("Go to bookmark number:{:d}".format(i))
                temp_icon = helper_forms.set_icon('tango_icons/bookmarks-goto.png')
                bookmark_goto_action.setIcon(temp_icon)
                bookmark_goto_action.triggered.connect(functools.partial(bookmark_goto, i))
                bookmark_goto_menu.addAction(bookmark_goto_action)
                #Store
                bookmark_store_action = data.QAction('Bookmark {:d}'.format(i), self)
                bookmark_store_action.setShortcut("{}+{}".format(data.bookmark_store_keys, i))
                bookmark_store_action.setStatusTip("Store bookmark number:{:d}".format(i))
                temp_icon = helper_forms.set_icon('tango_icons/bookmarks-store.png')
                bookmark_store_action.setIcon(temp_icon)
                bookmark_store_action.triggered.connect(functools.partial(bookmark_store, i))
                bookmark_store_menu.addAction(bookmark_store_action)
            def toggle_line_endings():
                try:
                    self.get_tab_by_focus().toggle_line_endings()
                except:
                    pass
            self.menubar_functions["toggle_line_endings"] = toggle_line_endings
            toggle_lineend_action = data.QAction('Toggle EOL visibility', self)
#            toggle_lineend_action.setShortcut('Ctrl+')
            temp_string = 'Toggle the visibility of the End-Of-Line characters '
            temp_string += 'for the currently selected document'
            toggle_lineend_action.setStatusTip(temp_string)
            temp_icon = helper_forms.set_icon('tango_icons/view-line-end.png')
            toggle_lineend_action.setIcon(temp_icon)
            toggle_lineend_action.triggered.connect(toggle_line_endings)
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
            view_menu.addAction(move_tab_right_action)
            view_menu.addAction(move_tab_left_action)
            view_menu.addAction(toggle_edge_action)
            view_menu.addAction(reset_zoom_action)
            view_menu.addAction(toggle_lineend_action)
        #REPL menu
        def construct_repl_menu():
            repl_menu = self.menubar.addMenu("&REPL")
            repeat_eval_action = data.QAction('REPL Repeat Command', self)
            repeat_eval_action.setShortcut(data.repeat_eval_keys)
            repeat_eval_action.setStatusTip('Repeat the last REPL command')
            repeat_eval_action.triggered.connect(self.repl.repeat_last_repl_eval)
            temp_icon = helper_forms.set_icon('tango_icons/repl-repeat-command.png')
            repeat_eval_action.setIcon(temp_icon)
            def repl_single_focus():
                self.view.set_repl_type(data.ReplType.SINGLE_LINE)
                self.repl.setFocus()
            self.menubar_functions["repl_single_focus"] = repl_single_focus
            repl_focus_action = data.QAction('Focus REPL(Single)', self)   
            repl_focus_action.setShortcuts(
                [data.repl_focus_single_1_keys, data.repl_focus_single_2_keys]
            )
            repl_focus_action.setStatusTip('Set focus to the Python REPL(Single Line)')
            repl_focus_action.triggered.connect(repl_single_focus)
            temp_icon = helper_forms.set_icon('tango_icons/repl-focus-single.png')
            repl_focus_action.setIcon(temp_icon)
            def repl_multi_focus():
                self.view.set_repl_type(data.ReplType.MULTI_LINE)
                self.repl_helper.setFocus()
            self.menubar_functions["repl_multi_focus"] = repl_multi_focus
            repl_focus_multi_action = data.QAction('Focus REPL(Multi)', self)
            repl_focus_multi_action.setShortcut(data.repl_focus_multi_keys)
            repl_focus_multi_action.setStatusTip('Set focus to the Python REPL(Multi Line)')
            repl_focus_multi_action.triggered.connect(repl_multi_focus)
            temp_icon = helper_forms.set_icon('tango_icons/repl-focus-multi.png')
            repl_focus_multi_action.setIcon(temp_icon)
            repl_menu.addAction(repeat_eval_action)
            repl_menu.addAction(repl_focus_action)  
            repl_menu.addAction(repl_focus_multi_action)
        #Sessions menu
        def construct_sessions_menu():
            sessions_menu       = self.menubar.addMenu("&Sessions")
            add_session_action  = data.QAction('Add Session', self)
            add_session_action.setStatusTip('Save the currently opened documents to a session')
            add_session_action.setIcon(helper_forms.set_icon('tango_icons/session-add.png'))
            add_session_action.triggered.connect(
                functools.partial(repl_text_input, text='session_add("", session_group=None)', cursor_position=13)
            )
            remove_session_action = data.QAction('Remove Session', self)
            remove_session_action.setStatusTip('Remove the session with matching name and group')
            remove_session_action.setIcon(helper_forms.set_icon('tango_icons/session-remove.png'))
            remove_session_action.triggered.connect(
                functools.partial(repl_text_input, text='session_remove("", session_group=None)', cursor_position=16)
            )
            session_editor_action = data.QAction('Graphical Session Editor', self)
            session_editor_action.setStatusTip('Graphical user friendly session editor')
            session_editor_action.setIcon(helper_forms.set_icon('tango_icons/sessions-gui.png'))
            session_editor_action.triggered.connect(self.display.show_session_editor)
            self.menubar_functions["show_session_editor"] = self.display.show_session_editor
            #Sessions menu
            self.sessions_menu = data.QMenu("Sessions")
            self.sessions_menu.setIcon(helper_forms.set_icon('tango_icons/sessions.png'))
            sessions_menu.addAction(add_session_action)
            sessions_menu.addAction(remove_session_action)
            sessions_menu.addAction(session_editor_action)
            sessions_menu.addSeparator()
            sessions_menu.addMenu(self.sessions_menu)
        #Help menu
        def construct_help_menu():
            help_menu = self.menubar.addMenu("&Help")
            self.fm = help_menu
            about_action = data.QAction('About Ex.Co.', self)
            about_action.setStatusTip('Ex.Co. Information')
            temp_icon = helper_forms.set_icon('tango_icons/help-browser.png')
            about_action.setIcon(temp_icon)
            about_action.triggered.connect(self.view.show_about)
            help_menu.addAction(about_action)
        #Execute the nested construction functions
        construct_file_menu()
        construct_edit_basic_menu()
        construct_edit_advanced_menu()
        construct_system_menu()
        construct_view_menu()
        construct_repl_menu()
        construct_sessions_menu()
        construct_help_menu()
        #Connect the triggered signal for hiding the function wheel on menubar clicks
        def hide_fw(action):
            #Hide the function wheel only when the clicked action is not "Show/Hide Function Wheel"
            if isinstance(action, data.QAction):
                if action.text() != "Show/Hide Function Wheel":
                    #Hide the function wheel if it is shown
                    if self.view.function_wheel_overlay != None:
                        self.view.hide_function_wheel()
        self.menubar.triggered.connect(hide_fw)
        #Add the menubar to the MainWindow
        self.setMenuBar(self.menubar)
    
    def _init_basic_widgets(self):
        """Initialize the three widgets that are used for displaying data"""
        #Initialize and add child controls to main_window(QTabControl)
        self.main_window    = BasicWidget(self)
        self.main_window.setTabShape(data.QTabWidget.Rounded)
        #Initialize and add child controls to lower_window(QTabControl)
        self.upper_window   = BasicWidget(self)
        #Initialise and add child controls to lower_window(QTabControl)
        self.lower_window   = BasicWidget(self)
    
    def _init_repl(self):
        """Initialize everything that concerns the REPL"""
        #Initialize the Python REPL widget
        self.repl           = ReplLineEdit(self, interpreter_references=self.get_form_references())
        self.repl.setObjectName("REPL_line")
        self.repl_helper    = ReplHelper(self, self.repl)
        self.repl_helper.setObjectName("REPL_multiline")
        #Initialize the groupbox that the REPL will be in, and place the REPL widget into it
        self.repl_box       = data.QGroupBox("Python Interactive Interpreter (REPL)")
        repl_layout         = data.QVBoxLayout()
        repl_layout.addWidget(self.repl)
        repl_layout.addWidget(self.repl_helper)
        self.repl_box.setLayout(repl_layout)
    
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
        """Import the user defined functions form the user_functions.cfg file"""
        self.repl.skip_next_repl_focus()
        user_file_path = os.path.join(data.application_directory, data.config_file)
        #Test if user_functions file exists
        if os.path.isfile(user_file_path) == False:
            message = "User functions file does not exist!\n"
            message += "Create an empty file named '{}' ".format(data.config_file)
            message += "in the application directory\n"
            message += "to make this error dissappear."
            self.display.repl_display_message(
                message, 
                message_type=data.MessageType.ERROR
            )
            return
        user_file = open(user_file_path)
        user_code = user_file.read()
        user_file.close()
        result = self.repl._repl_eval(user_code, display_action=False)
        if result != None:
            self.display.repl_display_message(
                "ERROR IN USER FUNCTIONS FILE:\n" + result, 
                message_type=data.MessageType.ERROR
            )
            return
        if self._first_scan == True:
            self._first_scan = False
            self.repl._repl_eval(
                "if callable(first_scan):\n    first_scan()", 
                display_action=False
            )
        #Update the REPL autocompletions
        import_nodes, class_tree_nodes, function_nodes, global_vars = functions.get_python_node_list(user_code)
        #First get the function names
        user_function_names = [func.name for func in function_nodes]
        #Then get the autocompletions by testing if the function has
        #the "autocompletion" attribute. Because in Python everything is an object,
        #functions can also have attributes! Very nice!
        user_function_autocompletions = []
        for func_name in user_function_names:
            """User functions are stored in the REPL's intepreter 'locals' dictionary"""""
            function = self.repl.interpreter.__dict__['locals'][func_name]
            #Check for the "autocompletions" attribute
            if hasattr(function, "autocompletion"):
                user_function_autocompletions.append(function.autocompletion)
            else:
                user_function_autocompletions.append(func_name)
        self.repl.interpreter_add_references(user_function_autocompletions)
        #Display the successful import
        self.display.write_to_statusbar("User functions imported successfully!")
    
    def _reset_interpreter(self):
        new_references, ac_list_prim, ac_list_sec = self.get_references_autocompletions()
        #Initialize and set auto completer
        self.repl.interpreter_reset_references(new_references, ac_list_prim, ac_list_sec)
        #Reimport the user functions
        self.import_user_functions()
        #Display interpreter reset success
        self.display.write_to_statusbar("REPL interpreter references successfully updated", 2000)

    def create_new(self, tab_name=None, basic_widget=None):
        """Creates an empty scintilla document using a generator counter"""
        #Set the new tab name
        if tab_name == None:
            tab_name = "new_" + str(next(self.new_file_count))
        #Create the new scintilla document in the selected basic widget 
        return_widget = None
        if basic_widget == None:
            return_widget   = self.main_window.editor_add_document(tab_name, type="new")
        else:
            return_widget   = basic_widget.editor_add_document(tab_name, type="new")
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
            self.last_browsed_dir, 
            "All Files (*);;Ex.Co. Files({:s})".format(' '.join(self.exco_file_exts))
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
                    "File: {:s}\ndoesn't exist!".format(in_file), 
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
                reply = data.QMessageBox.question(
                    self, 
                    'OPENING HUGE FILE', 
                    warning,
                    data.QMessageBox.Yes,
                    data.QMessageBox.No
                )
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
            if new_tab.current_icon != None:
                basic_widget.setTabIcon(basic_widget.indexOf(new_tab), new_tab.current_icon)
            if new_tab != None:
                try:
                    #Read the whole file and display the text
                    file_text = functions.read_file_to_string(in_file)
                    new_tab.setText(file_text)
                except MemoryError:
                    message = "Insufficient memory to open the file!"
                    self.display.repl_display_message(message, message_type=data.MessageType.ERROR)
                    self.display.write_to_statusbar(message)
                    basic_widget.removeTab(basic_widget.currentIndex())
                    return
                except:
                    message = "Unexpected error occured while opening file!"
                    self.display.repl_display_message(message, message_type=data.MessageType.ERROR)
                    self.display.write_to_statusbar(message)
                    basic_widget.removeTab(basic_widget.currentIndex())
                    return
                #Reset the changed status of the current tab, 
                #because adding the file content line by line was registered as a text change
                basic_widget.reset_text_changed()
                #Update the settings manipulator with the new file
                self.settings.update_recent_list(in_file)
                #Update the current working directory
                path = os.path.dirname(in_file)
                self.set_cwd(path)
                data.print_log("Opened file: " + str(in_file))
                #Set focus to the newly opened document
                basic_widget.currentWidget().setFocus()
                #Update the Save/SaveAs buttons in the menubar
                self.set_save_file_state(True)
            else:
                message = "File cannot be read!\n"
                message += "It's probably not a text file!"
                self.display.repl_display_message(
                    message, message_type=data.MessageType.ERROR
                )
                self.display.write_to_statusbar("File cannot be read!", 3000)
        if isinstance(file, str) == True:
            if file != None and file != "":
                open_file_function(file, basic_widget)
        elif isinstance(file, list) == True:
            for f in file:
                open_file_function(f, basic_widget)
        else:
            self.display.repl_display_message(
                "Unknown parameter type to 'open file' function!", 
                message_type=data.MessageType.ERROR
            )
            
    
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
            reply = data.QMessageBox.question(
                self, 
                'Close all tabs', 
                message,
                data.QMessageBox.Yes,
                data.QMessageBox.No
            )
            if reply == data.QMessageBox.No:
                return
        #Close all tabs and remove all bookmarks from them
        for i in range(self.main_window.count()):
            if isinstance(self.main_window.widget(0), CustomEditor):
                self.bookmarks.remove_editor_all(self.main_window.widget(0))
            self.main_window.removeTab(0)
        for i in range(self.upper_window.count()):
            if isinstance(self.upper_window.widget(0), CustomEditor):
                self.bookmarks.remove_editor_all(self.upper_window.widget(0))
            self.upper_window.removeTab(0)
        for i in range(self.lower_window.count()):
            if isinstance(self.lower_window.widget(0), CustomEditor):
                self.bookmarks.remove_editor_all(self.lower_window.widget(0))
            self.lower_window.removeTab(0)
    
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
                if isinstance(window.widget(i), helper_forms.TextDiffer) == True:
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
                if isinstance(window.widget(i), helper_forms.TextDiffer) == True:
                    if (window.widget(i).editor_1.hasFocus() == True or
                        window.widget(i).editor_2.hasFocus() == True):
                        return window
                else:
                    if window.widget(i).hasFocus() == True:
                        return window
        #No tab in the basic widgets has focus
        return None
    
    def check_document_states(self):
        """Check if there are any modified documents in the editor windows"""
        #Nested function for checking modified documents in a single basic widget
        #(just to play with nested functions)
        def check_documents_in_window(window):
            if window.count() > 0:
                for i in range(0, window.count()):
                    if window.widget(i).savable == data.CanSave.YES:
                        if window.widget(i).save_status == data.FileStatus.MODIFIED:
                            return True
            return False
        #Check all widget in all three windows for changes
        if (check_documents_in_window(self.main_window)     == True or
            check_documents_in_window(self.upper_window)    == True or
            check_documents_in_window(self.lower_window)    == True):
            #Modified document found
            return True
        else:
            #No changes found
            return False

    def exit(self, event=None):
        """Exit application"""
        #Close the MainWindow
        self.close()
    
    class Settings:
        """
        Functions for manipulating the application settings
        (namespace/nested class to MainWindow)
        """
        #Class varibles
        parent = None
        #Custom object for manipulating the settings of Ex.Co.
        manipulator = None
        
        def __init__(self, parent):
            """Initialization of the Settings object instance"""
            #Get the reference to the MainWindow parent object instance
            self.parent = parent
            #Initialize the Ex.Co. settings object with the current working directory
            self.manipulator = settings.SettingsFileManipulator(
                data.application_directory, 
                data.resources_directory
            )
        
        def update_recent_list(self, new_file=None):
            """Update the settings manipulator with the new file"""
            #Nested function for opening the recent file
            def new_file_function(file):
                self.parent.open_file(file=file, basic_widget=None)
                self.parent.main_window.currentWidget().setFocus()
            #Update the file manipulator
            if new_file != None:
                self.manipulator.add_recent_file(new_file)
            #Refresh the menubar recent list
            recent_files_menu = self.parent.recent_files_menu
            # !!Clear all of the actions from the menu OR YOU'LL HAVE MEMORY LEAKS!!
            for action in recent_files_menu.actions():
                recent_files_menu.removeAction(action)
                action.setParent(None)
                action.deleteLater()
                action = None
            recent_files_menu.clear()
            # Add the new recent files list to the menu
            for recent_file in reversed(self.manipulator.recent_files):
                #Iterate in the reverse order, so that the last file will be displayed
                #on the top of the menubar "Recent Files" menu
                recent_file_name = recent_file
                #Check if the filename has too many characters
                if len(recent_file_name) > 30:
                    #Shorten the name that will appear in the menubar
                    recent_file_name = "...{:s}".format(os.path.splitdrive(recent_file)[1][-30:])
                new_file_action = data.QAction(recent_file_name, recent_files_menu) #self.parent)
                new_file_action.setStatusTip("Open: {:s}".format(recent_file))
                #Create a function reference for opening the recent file
                temp_function = functools.partial(new_file_function, recent_file)
                new_file_action.triggered.connect(temp_function)
                recent_files_menu.addAction(new_file_action)
    
        def restore(self):
            """Restore the previously stored settings"""
            #Load the settings from the initialization file
            self.manipulator.load_settings()
            #Set main window side
            self.parent.view.set_main_window_side(
                self.manipulator.main_window_side
            )
            #Update the theme
            data.theme = self.manipulator.theme
            self.parent.view.refresh_theme()
            #Update recent files list in the menubar
            self.update_recent_list()
            #Update sessions list in the menubar
            self.parent.sessions.update_menu()
            #Display message in statusbar
            self.parent.display.write_to_statusbar("Restored settings", 1000)
        
        def save(self):
            """Save the current settings"""
            self.manipulator.save_settings(
                self.parent.view.main_window_side, 
                data.theme
            )
            #Display message in statusbar
            self.parent.display.write_to_statusbar("Saved settings", 1000)
    
    class Sessions:
        """
        Functions for manipulating sessions
        (namespace/nested class to MainWindow)
        """
        #Class varibles
        parent = None
    
        def __init__(self, parent):
            """Initialization of the Sessions object instance"""
            #Get the reference to the MainWindow parent object instance
            self.parent = parent

        def add(self, session_name, session_group=None):
            """Add the current opened documents in the main and upper window"""
            #Check if the session name is too short
            if len(session_name) < 3:
                self.parent.display.repl_display_message(
                    "Session name is too short!", 
                    message_type=data.MessageType.ERROR
                )
                return
            if session_group != None:
                if isinstance(session_group, str) == False:
                    self.parent.display.repl_display_message(
                        "Group name must be a string!", 
                        message_type=data.MessageType.ERROR
                    )
                    return
            #Create lists of files in each window
            try:
                main_files = self.get_window_documents("main")
                upper_files = self.get_window_documents("upper")
                lower_files = self.get_window_documents("lower")
                if (main_files != [] or upper_files != []):
                    #Check if the session is already stored
                    session_found = False
                    for ssn in self.parent.settings.manipulator.stored_sessions:
                        if ssn.name == session_name and ssn.group == session_group:
                            session_found = True
                            break
                    #Store the session
                    self.parent.settings.manipulator.add_session(
                        session_name,
                        session_group,
                        main_files,
                        upper_files,
                        lower_files
                    )
                    #Session added successfully
                    if session_group == None or session_group == "":
                        session_group = ""
                    else:
                        session_group = session_group + "/"
                    if session_found == True:
                        message = "Session '{:s}{:s}' overwritten!".format(session_group, session_name)
                    else:
                        message = "Session '{:s}{:s}' added!".format(session_group, session_name)
                    self.parent.display.repl_display_message(
                        message, 
                        message_type=data.MessageType.SUCCESS
                    )
                else:
                    self.parent.display.repl_display_message(
                        "No documents to store!", 
                        message_type=data.MessageType.ERROR
                    )
                    self.parent.display.write_to_statusbar("No documents to store!", 1500)
                #Refresh the sessions menu in the menubar
                self.update_menu()
            except Exception as ex:
                print(ex)
                message = "Invalid document types in the main or upper window!"
                self.parent.display.repl_display_message(
                    message, 
                    message_type=data.MessageType.ERROR
                )
                self.parent.display.write_to_statusbar(message, 1500)

        def restore(self, session_name, session_group=None):
            """Restore the files as stored in the selected session"""
            #Check if there are any modified documents
            if self.parent.check_document_states() == True:
                #Close the log window if it is displayed
                self.parent.view.set_log_window(False)
                message =  "You have modified documents!\n"
                message += "Restore session '{:s}' anyway?".format(session_name)
                reply = data.QMessageBox.question(
                    self.parent, 
                    'Restore Session', 
                    message,
                    data.QMessageBox.Yes,
                    data.QMessageBox.No
                )
                if reply == data.QMessageBox.No:
                    return
            #Find the session
            session = self.parent.settings.manipulator.get_session(
                          session_name,
                          session_group
                      )
            #Check if session was found
            if session != None:
                #Clear all documents from the main and upper window
                self.parent.close_all_tabs()
                #Add files to upper window
                for file in session.upper_files:
                    try:
                        self.parent.open_file(file, self.parent.upper_window)
                    except:
                        self.parent.display.repl_display_message("Could not find session file:\n" + file, message_type=data.MessageType.ERROR)
                #Add files to lower window
                for file in session.lower_files:
                    try:
                        self.parent.open_file(file, self.parent.lower_window)
                    except:
                        self.parent.display.repl_display_message("Could not find session file:\n" + file, message_type=data.MessageType.ERROR)
                #Add files to main window
                for file in session.main_files:
                    try:
                        self.parent.open_file(file, self.parent.main_window)
                    except:
                        self.parent.display.repl_display_message("Could not find session file:\n" + file, message_type=data.MessageType.ERROR)
            else:
                #Session was not found
                if session_group == None or session_group == "":
                    session_group = ""
                else:
                    session_group = session_group + "/"
                message = "Session '{:s}{:s}' was not found!".format(session_group, session_name)
                self.parent.display.repl_display_message(
                    message, 
                    message_type=data.MessageType.ERROR
                )
                self.parent.display.write_to_statusbar(message, 1500)
        
        def exco_restore(self):
            """Open all the source files for Ex.Co."""
            #Check if there are any modified documents
            if self.parent.check_document_states() == True:
                #Close the log window if it is displayed
                self.parent.view.set_log_window(False)
                message =  "You have modified documents!\n"
                message += "Restore Ex.Co development session anyway?"
                reply = data.QMessageBox.question(
                    self.parent, 'Restore Session', 
                    message,
                    data.QMessageBox.Yes,
                    data.QMessageBox.No
                )
                if reply == data.QMessageBox.No:
                    return
            #Clear all documents from the main and upper window
            self.parent.main_window.clear()
            self.parent.upper_window.clear()
            #Loop through the aplication directory and add the relevant files
            exco_main_files = []
            exco_dir = self.parent.settings.manipulator.application_directory
            exco_dirs = [
                exco_dir,
                os.path.join(exco_dir, "themes"),
                os.path.join(exco_dir, "cython"),
            ]
            for directory in exco_dirs:
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
                self.parent.open_file(file, self.parent.main_window)

        def remove(self, session_name, session_group=None):
            """Delete the session"""
            result = self.parent.settings.manipulator.remove_session(
                         session_name, 
                         session_group
                     )
            #Adjust the group name string
            if session_group == None or session_group == "":
                session_group = ""
            else:
                session_group = session_group + "/"
            if result == False:
                #Session was not found
                message = "Session '{:s}{:s}' was not found!".format(session_group, session_name)
                self.parent.display.repl_display_message(
                    message, 
                    message_type=data.MessageType.ERROR
                )
                self.parent.display.write_to_statusbar(message, 1500)
            else:
                #Session was removed successfully
                message = "Session '{:s}{:s}' was removed!".format(session_group, session_name)
                self.parent.display.repl_display_message(
                    message, 
                    message_type=data.MessageType.WARNING
                )
            #Refresh the sessions menu in the menubar
            self.update_menu()

        def update_menu(self):
            """Update the displayed items in the Sessions menu in the menubar"""
            #Nested function for retrieving the sessions name attribute case insensitively
            def get_case_insensitive_group_name(item):
                name = item[0]
                return name.lower()
            #Clear the sessions list
            self.parent.sessions_menu.clear()
            #First add the Ex.Co. session (all Ex.Co. source files)
            session_name = "Ex.Co. source files"
            exco_session_action = data.QAction(session_name, self.parent)
            exco_session_action.setStatusTip("Open all Ex.Co. source files")
            exco_session_method = self.exco_restore
            exco_session_action.setIcon(helper_forms.set_icon('Exco_Icon.png'))
            exco_session_action.triggered.connect(exco_session_method)
            self.parent.sessions_menu.addAction(exco_session_action)
            self.parent.sessions_menu.addSeparator()
            #Create a list of groups that will be stored for reuse
            groups = []
            #Sort the sessions
            self.parent.settings.manipulator.sort_sessions()
            #Add the groups to the menu first
            for session in self.parent.settings.manipulator.stored_sessions:
                if session.group != None:
                    group_found = False
                    for group in groups:
                        if session.group == group:
                            #Group found, it's already in the list
                            group_found = True
                            break
                    if group_found == False:
                        #Group is not in the list, add it as a tuple (name, reference)
                        groups.append(session.group)
            #Sort the group list and add the groups to the session menu
            groups.sort()
            sorted_groups = []
            for group in groups:
                new_group = self.parent.sessions_menu.addMenu(group)
                new_group.setIcon(helper_forms.set_icon('tango_icons/folder.png'))
                sorted_groups.append((group, new_group))
            #Loop through all of the stored sessions and add them
            for session in self.parent.settings.manipulator.stored_sessions:
                #Add the session
                new_session_action = data.QAction(session.name, self.parent)
                new_session_action.setStatusTip("Restore Session: {:s}".format(session.name))
                new_session_method = functools.partial(
                                         self.restore,
                                         session_name=session.name,
                                         session_group=session.group
                                     )
                new_session_action.setIcon(helper_forms.set_icon('tango_icons/sessions.png'))
                new_session_action.triggered.connect(new_session_method)
                #Check if the session is in a group
                if session.group != None:
                    #Loop througt the groups and add the action to the correct one
                    for group in sorted_groups:
                        if group[0] == session.group:
                           group[1].addAction(new_session_action)
                           break
                else:
                    self.parent.sessions_menu.addAction(new_session_action)
        
        def get_window_documents(self, window_name):
            """Return all the editor document paths in the selected window as a list"""
            window = self.parent.get_window_by_name(window_name)
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
        #Class varibles
        parent                  = None
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
            self.parent = parent
            #Get the function wheel overlay image size
            function_wheel_size = data.PyQt.QtGui.QPixmap(
                os.path.join(
                    data.resources_directory, 
                    data.function_wheel_image
                )
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
                    self.parent.vertical_splitter.setSizes(
                        [self.parent.vertical_splitter.width()*self.vertical_width_1, 
                         self.parent.vertical_splitter.width()*self.vertical_width_2]
                    )
                    self.parent.horizontal_splitter.setSizes(
                        [self.parent.horizontal_splitter.width()*self.horizontal_width_1, 
                         self.parent.horizontal_splitter.width()*self.horizontal_width_2]
                    )
                elif main_window_side   == data.MainWindowSide.RIGHT:
                    self.parent.vertical_splitter.setSizes(
                        [self.parent.vertical_splitter.width()*self.vertical_width_1, 
                         self.parent.vertical_splitter.width()*self.vertical_width_2]
                    )
                    self.parent.horizontal_splitter.setSizes(
                        [self.parent.horizontal_splitter.width()*self.horizontal_width_2, 
                         self.parent.horizontal_splitter.width()*self.horizontal_width_1]
                    )
            #Set the REPL font
            self.parent.repl.setFont(data.PyQt.QtGui.QFont("Arial", 12, data.PyQt.QtGui.QFont.Bold))
            #Refresh the size relation between the basic widgets and the REPL,
            #so that the REPL height is always the same
            self.refresh_main_splitter()
        
        def save_layout(self):
            """Save the widths of the splitters"""
            #Check if the splitters are filled correctly
            if self.layout_save_block == True:
                return
            if self.parent.vertical_splitter.count() < 2 or self.parent.horizontal_splitter.count() < 2:
                return
            #Check which window mode is active
            if (self.parent.window_mode == data.WindowMode.THREE and
                self.parent.vertical_splitter.height() > 0 and
                self.parent.horizontal_splitter.width() > 0):
                self.vertical_width_1   = (self.parent.vertical_splitter.sizes()[0] / 
                                           self.parent.vertical_splitter.height())
                self.vertical_width_2   = (self.parent.vertical_splitter.sizes()[1] / 
                                           self.parent.vertical_splitter.height())
                #Save the horizontal positions according to the main window side
                if self.main_window_side    == data.MainWindowSide.LEFT:
                    self.horizontal_width_1     = (self.parent.horizontal_splitter.sizes()[0] / 
                                                   self.parent.horizontal_splitter.width())
                    self.horizontal_width_2     = (self.parent.horizontal_splitter.sizes()[1] / 
                                                   self.parent.horizontal_splitter.width())
                elif self.main_window_side  == data.MainWindowSide.RIGHT:
                    self.horizontal_width_1     = (self.parent.horizontal_splitter.sizes()[1] / 
                                                   self.parent.horizontal_splitter.width())
                    self.horizontal_width_2     = (self.parent.horizontal_splitter.sizes()[0] / 
                                                   self.parent.horizontal_splitter.width())
        
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
            focused_widget  = self.parent.get_window_by_child_tab()
            focused_tab     = self.parent.get_tab_by_focus()
            if focused_widget == None:
                focused_widget = self.parent.get_window_by_focus()
            #Store the last focused tab
            self.parent.last_focused_tab = focused_tab
            #Create QSplitters to split main window into three parts: 
            #editing(QScintilla), upper_window(QTabControl), lower_window(QTabControl)
            vertical_splitter      = data.QSplitter(data.PyQt.QtCore.Qt.Vertical)
            vertical_splitter.setObjectName("Vertical_Splitter")
            horizontal_splitter    = data.QSplitter(data.PyQt.QtCore.Qt.Horizontal)
            horizontal_splitter.setObjectName("Horizontal_Splitter")
            main_splitter          = data.QSplitter(data.PyQt.QtCore.Qt.Vertical)
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
            main_splitter.addWidget(self.parent.repl_box)
            #Set the window mode attribute to one
            self.parent.window_mode = data.WindowMode.THREE
            #Initialize the main groupbox
            main_groupbox = data.QGroupBox(self.parent)
            main_groupbox_layout = data.QVBoxLayout(main_groupbox)
            main_groupbox_layout.addWidget(main_splitter)
            main_groupbox.setLayout(main_groupbox_layout)
            main_groupbox.setObjectName("Main_Groupbox")
            #Add the splitters combined in the groupbox to the main form
            self.parent.setCentralWidget(main_groupbox)
            #Save references to the MainWindow
            self.parent.main_window    = main_window
            self.parent.upper_window   = upper_window
            self.parent.lower_window   = lower_window
            self.parent.vertical_splitter       = vertical_splitter
            self.parent.horizontal_splitter     = horizontal_splitter
            self.parent.main_splitter           = main_splitter
            self.parent.main_groupbox           = main_groupbox
            self.parent.main_groupbox_layout    = main_groupbox_layout
            #Resize the splitters as needed
            self.refresh_layout(self.parent.window_mode, self.main_window_side)
            #Set focus back to the last focused widget
            if focused_widget != None:
                #Store the last focused widget
                self.parent.last_focused_widget = focused_widget
                data.print_log(
                    "Stored \"{:s}\" as last focused widget".format(focused_widget.name)
                )
                #Set focus to the last focused widget
                if focused_tab != None:
                    focused_tab.setFocus()
                else:
                    focused_widget.setFocus()
            #Initialize the function wheel overlay over the QMainWindows central widget, if needed
            self.function_wheel_overlay = FunctionWheelOverlay(
                parent=self.parent.main_groupbox, 
                main_form=self.parent, 
            )
            self.function_wheel_overlay.setObjectName("Function_Wheel")
            if show_overlay == True:
                self.function_wheel_overlay.show()
            else:
                self.function_wheel_overlay.hide()
    
        def set_log_window(self, show=True):
            """Show or hide the log window"""
            if show == True:
                data.logging_mode = True
                data.log_window.show()
            else:
                data.log_window.hide()
            self.parent.activateWindow()
                
        def toggle_log_window(self):
            """Toggle the display of the log window"""
            if data.log_window.isVisible():
                self.set_log_window(False)
            else:
                self.set_log_window(True)
        
        def show_about(self):
            """Show ExCo information"""
            about = helper_forms.ExCoInfo(self.parent, app_dir=self.parent.settings.manipulator.application_directory)
            #The exec_() function shows the dialog in MODAL mode (the parent is unclickable while the dialog is shown)
            about.exec_()
        
        def set_main_window_side(self, main_window_side):
            """Set main window side"""
            #Set the new main window side
            self.main_window_side = main_window_side
            #Refresh the layout
            self.set_basic_widgets(
                main_widget=self.parent.main_window,
                upper_widget=self.parent.upper_window,
                lower_widget=self.parent.lower_window
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
                temp_widget_main    = self.parent.horizontal_splitter.widget(1)
                temp_widget_upper   = self.parent.vertical_splitter.widget(0)
                temp_widget_lower   = self.parent.vertical_splitter.widget(1)
            else:
                #Save current positioning
                temp_widget_main    = self.parent.horizontal_splitter.widget(0)
                temp_widget_upper   = self.parent.vertical_splitter.widget(0)
                temp_widget_lower   = self.parent.vertical_splitter.widget(1)
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
            self.parent.repl.interpreter_update_windows(
                self.parent.main_window, 
                self.parent.upper_window, 
                self.parent.lower_window
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
                self.parent.upper_window.hide()
                self.parent.lower_window.hide()
                self.window_mode = data.WindowMode.ONE
                #Focus on the main window as the other two windows are hidden
                self.set_window_focus("main")
                self.parent.display.write_to_statusbar("Window mode changed to: ONE", 1000)
            elif self.window_mode   == data.WindowMode.ONE:
                self.parent.upper_window.show()
                self.parent.lower_window.show()
                self.window_mode = data.WindowMode.THREE
                self.parent.display.write_to_statusbar("Window mode changed to: THREE", 1000)
        
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
                window  = self.parent.main_window
            elif window == "upper":
                window  = self.parent.upper_window
            elif window == "lower":
                window  = self.parent.lower_window
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
                    self.parent.display.update_cursor_position(line, column)
                else:
                    #Clear the cursor position
                    self.parent.display.update_cursor_position()
            except:
                window.setFocus()
                self.parent.display.write_to_statusbar("Empty window '" + window.name + "' focused!", 1000)
                #Clear the cursor position
                self.parent.display.update_cursor_position()
            finally:
                #Store the last focused widget
                self.parent.last_focused_widget = window
        
        def set_repl_type(self, type=data.ReplType.SINGLE_LINE):
            """Set REPL input as a one line ReplLineEdit or a multiline ReplHelper"""
            #Check if the REPL type needs to be updated
            if (type == data.ReplType.SINGLE_LINE and 
                self.repl_state == data.ReplType.SINGLE_LINE):
                return
            elif (type == data.ReplType.MULTI_LINE and 
                self.repl_state == data.ReplType.MULTI_LINE):
                return
            #Initialize the groupbox that the REPL will be in, and place the REPL widget into it
            self.parent.repl_box = data.QGroupBox("Python Interactive Interpreter (REPL)")
            self.parent.repl_box.setObjectName("REPL_Box")
            repl_layout = data.QVBoxLayout()
            repl_layout.addWidget(self.parent.repl)
            repl_layout.addWidget(self.parent.repl_helper)
            #Set which REPL widget will be displayed
            if type == data.ReplType.SINGLE_LINE:
                self.parent.repl.setVisible(True)
                self.parent.repl_helper.setVisible(False)
                self.repl_state = data.ReplType.SINGLE_LINE
                self.main_relation = 55
            else:
                self.parent.repl.setVisible(False)
                self.parent.repl_helper.setVisible(True)
                self.repl_state = data.ReplType.MULTI_LINE
                self.main_relation = 100
            self.parent.repl_box.setLayout(repl_layout)
            #Refresh the layout
            self.parent.view.set_basic_widgets(
                main_widget=self.parent.main_window,
                upper_widget=self.parent.upper_window,
                lower_widget=self.parent.lower_window
            )
        
        def toggle_window_size(self):
            """Maximize the main application window"""
            if self.parent.isMaximized() == True:
                self.parent.showNormal()
            else:
                self.parent.showMaximized()
            self.refresh_layout(self.window_mode, self.main_window_side)
        
        def toggle_function_wheel(self):
            """Show/hide the function wheel overlay"""
            if self.function_wheel_overlay.isVisible() == True:
                self.hide_function_wheel()
            else:
                self.show_function_wheel()
        
        def show_function_wheel(self):
            """Show the function wheel overlay"""
            #Check the windows size before displaying the overlay
            if (self.parent.width() < self.FUNCTION_WHEEL_BOUNDS[0] or 
                self.parent.height() < self.FUNCTION_WHEEL_BOUNDS[1]):
                new_size =  data.PyQt.QtCore.QSize(
                                self.FUNCTION_WHEEL_BOUNDS[0] + self.FUNCTION_WHEEL_BOUNDS[0]/5,
                                self.FUNCTION_WHEEL_BOUNDS[1] + self.FUNCTION_WHEEL_BOUNDS[1]/5
                            )
                self.parent.resize(new_size)
            #Check if the function wheel overlay is initialized
            if self.function_wheel_overlay != None:
                #Save the currently focused widget
                focused_widget  = self.parent.get_window_by_child_tab()
                focused_tab     = self.parent.get_tab_by_focus()
                if focused_widget == None:
                    focused_widget = self.parent.get_window_by_focus()
                #Store the last focused widget and tab
                self.parent.last_focused_widget = focused_widget
                self.parent.last_focused_tab    = focused_tab
                #Show the function wheel overlay
                self.function_wheel_overlay.show()
        
        def hide_function_wheel(self):
            """Hide the function wheel overlay"""
            if self.function_wheel_overlay != None:
                self.function_wheel_overlay.hide()
        
        def init_style_sheet(self):            
            style_sheet = (
                "#Form {" +
                "   background-color: {0};".format(data.theme.Form) +
                "}" + 
                "QSplitter::handle {" +
                "   background: {0};".format(data.theme.Form) +
                "}"
            )
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
            style_sheet += self.generate_treedisplay_colors("TreeDisplay")
            style_sheet += self.generate_treedisplay_colors("SessionGuiManipulator")
            return style_sheet
        
        def reset_repl_colors(self, in_sheet):
            style_sheet = in_sheet
            style_sheet += self.generate_repl_colors(
                data.theme.Indication.PassiveBorder, 
                data.theme.Indication.PassiveBackGround
            )
            return style_sheet
        
        def reset_entire_style_sheet(self):
            style_sheet = self.init_style_sheet()
            style_sheet = self.reset_window_colors(style_sheet)
            style_sheet = self.reset_repl_colors(style_sheet)
            self.parent.setStyleSheet(style_sheet)
        
        def generate_window_colors(self, window_name, border, background):
            style_sheet = (
                "#" + window_name + "::pane {" + 
                    "border: 2px solid {0};".format(border) +
                    "background-color: {0};".format(background)  +
                "}"
            )
            return style_sheet
        
        def generate_repl_colors(self, border, background):
            style_sheet = (
                "#REPL_Box {" + 
                    "font-size: 8pt; font-weight: bold;" +
                    "color: {0};".format(border) +
                    "background-color: {0};".format(data.theme.Indication.PassiveBackGround) +
                    "border: 2px solid {0};".format(border) +
                    "border-radius: 5px;" +
                    "margin-top: 5px;" +
                    "margin-bottom: 0px;" +
                    "margin-left: 0px;" +
                    "margin-right: 0px;" +
                    "padding-top: 0px;" +
                    "padding-bottom: 0px;" +
                    "padding-left: 0px;" +
                    "padding-right: 0px;" +
                "}" + 
                "#REPL_Box::title {" +
                    "color: {0};".format(data.theme.Indication.ActiveBorder) +
                    "subcontrol-position: top left;" +
                    "padding: 0px;" + 
                    "left: 8px;" +
                    "top: -6px;" +
                "}"
            )
            # REPL and REPL helper have to be set directly
            self.parent.repl.setStyleSheet(
                "color: rgb({0}, {1}, {2});".format(
                    data.theme.Font.Default.red(), 
                    data.theme.Font.Default.green(), 
                    data.theme.Font.Default.blue()
                ) +
                "background-color: {0};".format(background)
            )
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
                    "tango_icons/shrink-negative.png"
                ).replace("\\", "/")
                expand_icon = os.path.join(
                    data.resources_directory, 
                    "tango_icons/expand-negative.png"
                ).replace("\\", "/")
            else:
                shrink_icon = expand_icon = os.path.join(
                    data.resources_directory, 
                    "tango_icons/shrink-positive.png"
                ).replace("\\", "/")
                expand_icon = os.path.join(
                    data.resources_directory, 
                    "tango_icons/expand-positive.png"
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
        
        def indicate_repl(self):
            """Indicate that the REPL is focused by coloring the border"""
            style_sheet = self.init_style_sheet()
            style_sheet += self.generate_repl_colors(
                data.theme.Indication.ActiveBorder, 
                data.theme.Indication.ActiveBackGround
            )
            windows = ["Main", "Upper", "Lower"]
            for window in windows:
                style_sheet += self.generate_window_colors(
                    window, 
                    data.theme.Indication.PassiveBorder, 
                    data.theme.Indication.PassiveBackGround
                )
            style_sheet += self.generate_treedisplay_colors("TreeDisplay")
            style_sheet += self.generate_treedisplay_colors("SessionGuiManipulator")
            self.parent.setStyleSheet(style_sheet)
        
        def indicate_window(self, window_name):
            if (window_name != "Main" and 
                window_name != "Upper" and 
                window_name != "Lower"):
                return
            style_sheet = self.init_style_sheet()
            style_sheet += self.generate_window_colors(
                window_name, 
                data.theme.Indication.ActiveBorder, 
                data.theme.Indication.ActiveBackGround
            )
            self.parent.setStyleSheet(style_sheet)
            windows = ["Main", "Upper", "Lower"]
            windows.remove(window_name)
            for window in windows:
                style_sheet += self.generate_window_colors(
                    window, 
                    data.theme.Indication.PassiveBorder, 
                    data.theme.Indication.PassiveBackGround
                )
                self.parent.setStyleSheet(style_sheet)
            style_sheet += self.generate_repl_colors(
                data.theme.Indication.PassiveBorder, 
                data.theme.Indication.PassiveBackGround
            )
            self.parent.setStyleSheet(style_sheet)
            style_sheet += self.generate_treedisplay_colors("TreeDisplay")
            style_sheet += self.generate_treedisplay_colors("SessionGuiManipulator")
            self.parent.setStyleSheet(style_sheet)
        
        def indication_check(self):
            """
            Check if any of the main windows or the REPL is focused
            and indicate the focused widget if needed
            """
            if (self.parent.main_window == None or 
                self.parent.upper_window == None or 
                self.parent.lower_window == None or 
                self.parent.repl == None):
                return
            #Check the focus for all of the windows
            windows = [self.parent.main_window, 
                       self.parent.upper_window, 
                       self.parent.lower_window]
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
                        if isinstance(window.widget(i), helper_forms.TextDiffer) == True:
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
            if (self.parent.repl.hasFocus() == True or
                self.parent.repl_helper.hasFocus() == True):
                self.parent.repl.indicated = True
                self.indicate_repl()
                return
            #If no widget has focus, reset the QMainWindows stylesheet
            self.reset_entire_style_sheet()
        
        def refresh_main_splitter(self):
            #Refresh the size relation between the basic widgets and the REPL,
            #so that the REPL height is always the same
            self.parent.main_splitter.setSizes(
                [self.parent.height() - self.main_relation, self.main_relation]
            )
        
        def refresh_theme(self):
            windows = [
                self.parent.main_window, 
                self.parent.upper_window, 
                self.parent.lower_window
            ]
            for window in windows:
                for i in range(window.count()):
                    if hasattr(window.widget(i), "refresh_lexer") == True:
                        window.widget(i).refresh_lexer()
                    elif hasattr(window.widget(i), "set_theme") == True:
                        window.widget(i).set_theme(data.theme)
            self.parent.repl_helper.refresh_lexer()
            self.indication_check()
            self.parent.statusbar.setStyleSheet(
                "color: {0};".format(data.theme.Indication.Font)
            )
        
        def reload_themes(self):
            global lexers, themes
            
            """
            !!!! THE OLD ROUTINE EATS MEMORY LIKE CRAZY !!!!
            (If you don't want to consume memory reload the themes by restarting Ex.Co.!)
            -----------------------------------------------------------------------------
            """
#            current_theme_name = data.theme.__name__.split(".")[1]
#            import themes
#            import lexers
#            importlib.reload(themes.air)
#            importlib.reload(themes.earth)
#            importlib.reload(themes.water)
#            importlib.reload(themes.mc)
#            importlib.reload(lexers)
            """
            -----------------------------------------------------------------------------
            """
            
            # Store the name of the current theme
            current_theme_name = data.theme.__name__
            # Remove the themes and lexers modules
            del themes
            del lexers
            del sys.modules["themes"]
            del sys.modules["lexers"]
            # Reimport the modules
            import themes
            import lexers
            # Set the theme again
            data.theme = getattr(themes, current_theme_name)
            self.refresh_theme()
    
        def create_recent_file_list_menu(self):
            self.parent.recent_files_menu = data.QMenu("Recent Files")
            temp_icon = helper_forms.set_icon('tango_icons/file-recent-files.png')
            self.parent.recent_files_menu.setIcon(temp_icon)
            return self.parent.recent_files_menu
        
        def delete_recent_file_list_menu(self):
            self.parent.recent_files_menu.setParent(None)
            self.parent.recent_files_menu = None

    
    class System:
        """
        Functions that interact with the system
        (namespace/nested class to MainWindow)
        """
        #Class varibles
        parent = None
        
        def __init__(self, parent):
            """Initialization of the System object instance"""
            #Get the reference to the MainWindow parent object instance
            self.parent = parent
        
        def find_files(self, 
                       file_name, 
                       search_dir=None,
                       case_sensitive=False, 
                       search_subdirs=True):
            """Return a list of files that match file_name as a list and display it"""
            #Check if the search directory is none, then use a dialog window
            #to select the real search directory
            if search_dir == None:
                search_dir = self.parent._get_directory_with_dialog()
                #Update the current working directory
                if os.path.isdir(search_dir):
                    self.parent.set_cwd(search_dir)
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
                self.parent.display.repl_display_message(
                    "Invalid search directory!", 
                    message_type=data.MessageType.ERROR
                )
                self.parent.display.write_to_statusbar("Invalid search directory!", 2000)
                return
            elif found_files == []:
                #Check if any files were found
                self.parent.display.repl_display_message(
                    "No files found!", 
                    message_type=data.MessageType.WARNING
                )
                self.parent.display.write_to_statusbar("No files found!", 2000)
                return
            #Display the found files
            self.parent.display.show_found_files(
                "'{:s}' in its name".format(file_name), 
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
                search_dir = self.parent._get_directory_with_dialog()
                #Update the current working directory
                if os.path.isdir(search_dir):
                    self.parent.set_cwd(search_dir)
            try:
                #Execute the find function
                found_files = functions.find_files_with_text_enum(
                    search_text, 
                    search_dir, 
                    case_sensitive, 
                    search_subdirs, 
                    break_on_find
                )
                #Check of the function return is valid
                if found_files == None:
                    #Check if directory is valid
                    self.parent.display.repl_display_message(
                        "Invalid search directory!", 
                        message_type=data.MessageType.ERROR
                    )
                    self.parent.display.write_to_statusbar("Invalid search directory!", 2000)
                    return
                elif found_files == {}:
                    #Check if any files were found
                    self.parent.display.repl_display_message(
                        "No files found!", 
                        message_type=data.MessageType.WARNING
                    )
                    self.parent.display.write_to_statusbar("No files found!", 2000)
                    return
                #Display the found files
                self.parent.display.show_found_files_with_lines_in_tree(
                    "'{:s}' in its content".format(search_text), 
                    found_files, 
                    search_dir
                )
            except Exception as ex:
                self.parent.display.repl_display_message(
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
            self.parent.view.set_log_window(False)
            warning = "The replaced content will be saved back into the files!\n"
            warning += "You better have a backup of the files if you are unsure,\n"
            warning += "because this action CANNOT be undone!\n"
            warning += "Do you want to continue?"
            reply = data.QMessageBoxwarning(
                        self.parent,
                        'REPLACING IN FILES', 
                        warning,
                        data.QMessageBox.Yes,
                        data.QMessageBox.No
                    )
            if reply == data.QMessageBox.No:
                return
            #Check if the search directory is none, then use a dialog window
            #to select the real search directory
            if search_dir == None:
                search_dir = self.parent._get_directory_with_dialog()
                #Update the current working directory
                if os.path.isdir(search_dir):
                    self.parent.set_cwd(search_dir)
            #Replace the text in files
            result = functions.replace_text_in_files_enum(
                         search_text, 
                         replace_text, 
                         search_dir, 
                         case_sensitive, 
                         search_subdirs
                     )
            #Check the return type
            if len(result) == 0:
                self.parent.display.repl_display_message(
                    "No files with '{:s}' in its text were found!".format(search_text), 
                    message_type=data.MessageType.WARNING
                )
            elif isinstance(result, dict):
                self.parent.display.show_replaced_text_in_files_in_tree(
                    search_text, 
                    replace_text, 
                    result, 
                    search_dir
                )
            else:
                self.parent.display.repl_display_message(
                    "Unknown error!", 
                    message_type=data.MessageType.ERROR
                )
    
    class Editing:
        """
        Document editing functions
        (namespace/nested class to MainWindow)
        """
        #Class varibles
        parent = None
        
        def __init__(self, parent):
            """Initialization of the Editing object instance"""
            #Get the reference to the MainWindow parent object instance
            self.parent = parent
            #Initialize the namespace classes
            self.line   = self.Line(self)
        
        def find_in_open_documents(self, 
                                   search_text, 
                                   case_sensitive=False, 
                                   regular_expression=False, 
                                   window_name=None):
            """
            Find instances of search text accross all open document in the selected window
            """
            #Get the current widget
            basic_widget = self.parent.get_window_by_name(window_name)
            if window_name == None:
                window_name = "Main"
            #Check if there are any documents in the basic widget
            if basic_widget.count() == 0:
                message = "No documents in " + basic_widget.name.lower()
                message += " editing window"
                self.parent.display.repl_display_message(
                    message, 
                    message_type=data.MessageType.WARNING
                )
                return
            #Save the current index to reset focus to it if no instances of search string are found
            saved_index = basic_widget.currentIndex()
            #Create a deque of the tab index order and start with the current index,
            #deque is used, because it can be rotated by default
            in_deque = collections.deque(range(basic_widget.count()))
            #Rotate the deque until the first element is the current index
            while in_deque[0] != basic_widget.currentIndex():
                in_deque.rotate(1)
            #Set a flag for the first document
            first_document = True
            for i in in_deque:
                #Skip the current widget if it's not an editor
                if isinstance(basic_widget.widget(i), CustomEditor) == False:
                    continue
                #Place the cursor to the top of the document if it is not the current document
                if first_document == True:
                    first_document = False
                else:
                    basic_widget.widget(i).setCursorPosition(0, 0)
                #Find the text
                result = basic_widget.widget(i).find_text(
                             search_text,
                             case_sensitive, 
                             True, # search_forward
                             regular_expression  
                         )
                #If a replace was done, return success
                if result == data.SearchResult.FOUND:
                    return True
            #Nothing found
            basic_widget.setCurrentIndex(saved_index)
            message = "No instances of '" + search_text + "' found in "
            message += basic_widget.name.lower() + " editing window"
            self.parent.display.repl_display_message(
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
            Find and replace instaces of search string with replace string across
            all of the open documents in the selected window, one instance at a time,
            starting from the currently selected widget.
            """
            #Get the current widget
            basic_widget = self.parent.get_window_by_name(window_name)
            if window_name == None:
                window_name = "Main"
            #Check if there are any documents in the basic widget
            if basic_widget.count() == 0:
                message = "No documents in the " + basic_widget.name.lower()
                message += " editing window"
                self.parent.display.repl_display_message(
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
                    self.parent.display.write_to_statusbar(message)
                    return True
            #Nothing found
            basic_widget.setCurrentIndex(saved_index)
            message = "No instances of '" + search_text + "' found in the "
            message += basic_widget.name.lower() + " editing window"
            self.parent.display.repl_display_message(
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
            basic_widget = self.parent.get_window_by_name(window_name)
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
            self.parent.display.repl_display_message(
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
            widget = self.parent.get_current_tab_by_parent_name(window_name)
            if window_name == None:
                window_name = "Main"
            #None-check the current widget in the selected window
            if widget != None:
                method = getattr(widget, method_name)
                #Argument list has to be preceded by the '*' character
                method(*argument_list)
            else:
                message = "No document in {:s} window!".format(window_name)
                self.parent.display.repl_display_message(
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
                self.parent = parent
                
            def goto(self, line_number, window_name=None):
                """Set focus and cursor to the selected line in the currently focused window"""
                argument_list = [line_number]
                self.parent._run_focused_widget_method("goto_line", argument_list, window_name)
            
            def replace(self, replace_text, line_number, window_name=None):
                """Replace the selected line in the currently focused window"""
                argument_list = [replace_text, line_number]
                self.parent._run_focused_widget_method("replace_line", argument_list, window_name)
            
            def remove(self, line_number, window_name=None):
                """Remove the selected line in the currently focused window"""
                argument_list = [line_number]
                self.parent._run_focused_widget_method("remove_line", argument_list, window_name)
            
            def get(self, line_number, window_name=None):
                """Replace the selected line in the currently focused window"""
                argument_list = [line_number]
                self.parent._run_focused_widget_method("get_line", argument_list, window_name)
            
            def set(self, line_text, line_number, window_name=None):
                """Replace the selected line in the currently focused window"""
                argument_list = [line_text, line_number]
                self.parent._run_focused_widget_method("set_line", argument_list, window_name)
    
    class Display:
        """
        Functions for displaying of various functions such as:
        show_nodes, find_in_open_documents, ...
        (namespace/nested class to MainWindow)
        """
        # Class varibles
        parent              = None
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
        
        def __init__(self, parent):
            """ Initialization of the Display object instance """
            # Get the reference to the MainWindow parent object instance
            self.parent = parent
            # Initialize the theme menu
            self.init_theme_menu()
        
        def init_theme_indicator(self):
            """ Initialization of the theme indicator in the statusbar """
            class ThemeIndicator(data.QLabel):
                def __init__(self, parent):
                    # Initialize superclass
                    super().__init__()
                    # Store the reference to the parent
                    self.parent = parent
                
                def mouseReleaseEvent(self, event):
                    # Execute the superclass event method
                    super().mouseReleaseEvent(event)
                    cursor = data.PyQt.QtGui.QCursor.pos()
                    self.parent.theme_menu.popup(cursor)
            
            if data.theme == themes.Air:
                tooltip = "Air"
                image = "tango_icons/theme-air.png"
            elif data.theme == themes.Earth:
                tooltip = "Earth"
                image = "tango_icons/theme-earth.png"
            elif data.theme == themes.Water:
                tooltip = "Water"
                image = "tango_icons/theme-water.png"
            elif data.theme == themes.MC:
                tooltip = "MC"
                image = "tango_icons/theme-mc.png"
            raw_picture = data.PyQt.QtGui.QPixmap(
                os.path.join(
                    data.resources_directory, image
                )
            )
            picture = raw_picture.scaled(16, 16, data.PyQt.QtCore.Qt.KeepAspectRatio)
            self.theme_indicatore = ThemeIndicator(self)
            self.theme_indicatore.setPixmap(picture)
            self.theme_indicatore.setToolTip(tooltip)
            self.theme_indicatore.setStyleSheet(
                    "ThemeIndicator {" + 
                    "    color: black;" + 
                    "    padding-top: 0px;" +
                    "    padding-bottom: 0px;" +
                    "    padding-left: 0px;" +
                    "    padding-right: 4px;" +
                    "}" +
                    "QToolTip {" + 
                    "    color: black;" + 
                    "    padding-top: 0px;" +
                    "    padding-bottom: 0px;" +
                    "    padding-left: 0px;" +
                    "    padding-right: 0px;" + 
                    "}"
            )
            self.parent.statusbar.addPermanentWidget(self.theme_indicatore)
        
        def init_theme_menu(self):
            """ Initialization of the theme menu used by the theme indicator """
            def choose_theme(theme):
                data.theme = theme
                self.parent.view.refresh_theme()
                if data.theme == themes.Air:
                    tooltip = "Air"
                    image = "tango_icons/theme-air.png"
                elif data.theme == themes.Earth:
                    tooltip = "Earth"
                    image = "tango_icons/theme-earth.png"
                elif data.theme == themes.Water:
                    tooltip = "Water"
                    image = "tango_icons/theme-water.png"
                elif data.theme == themes.MC:
                    tooltip = "Midnight Commander"
                    image = "tango_icons/theme-mc.png"
                raw_picture = data.PyQt.QtGui.QPixmap(
                    os.path.join(
                        data.resources_directory, image
                    )
                )
                picture = raw_picture.scaled(16, 16, data.PyQt.QtCore.Qt.KeepAspectRatio)
                self.theme_indicatore.setPixmap(picture)
                self.theme_indicatore.setToolTip(tooltip)
                self.theme_indicatore.setStyleSheet(
                    "ThemeIndicator {" + 
                    "    color: black;" + 
                    "    padding-top: 0px;" +
                    "    padding-bottom: 0px;" +
                    "    padding-left: 0px;" +
                    "    padding-right: 4px;" +
                    "}" +
                    "QToolTip {" + 
                    "    color: black;" + 
                    "    padding-top: 0px;" +
                    "    padding-bottom: 0px;" +
                    "    padding-left: 0px;" +
                    "    padding-right: 0px;" + 
                    "}"
                )
                self.repl_display_message(
                    "Changed theme to: {}".format(tooltip), 
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
            self.theme_menu = data.QMenu()
            # Air
            action_air = data.QAction("Air", self.theme_menu)
            action_air.triggered.connect(
                functools.partial(choose_theme, themes.Air)
            )
            icon = helper_forms.set_icon('tango_icons/theme-air.png')
            action_air.setIcon(icon)
            self.theme_menu.addAction(action_air)
            # Earth
            action_earth = data.QAction("Earth", self.theme_menu)
            action_earth.triggered.connect(
                functools.partial(choose_theme, themes.Earth)
            )
            icon = helper_forms.set_icon('tango_icons/theme-earth.png')
            action_earth.setIcon(icon)
            self.theme_menu.addAction(action_earth)
            # Water
            action_water = data.QAction("Water", self.theme_menu)
            action_water.triggered.connect(
                functools.partial(choose_theme, themes.Water)
            )
            icon = helper_forms.set_icon('tango_icons/theme-water.png')
            action_water.setIcon(icon)
            self.theme_menu.addAction(action_water)
            # Midnight Commander
            action_mc = data.QAction("MC", self.theme_menu)
            action_mc.triggered.connect(
                functools.partial(choose_theme, themes.MC)
            )
            icon = helper_forms.set_icon('tango_icons/theme-mc.png')
            action_mc.setIcon(icon)
            self.theme_menu.addAction(action_mc)
        
        def write_to_statusbar(self, message, msec=0):
            """Write a message to the statusbar"""
            self.parent.statusbar.setStyleSheet(
                "color: {0};".format(data.theme.Indication.Font)
            )
            self.parent.statusbar.showMessage(message, msec)
        
        def update_cursor_position(self, cursor_line=None, cursor_column=None):
            """Update the position of the cursor in the current widget to the statusbar"""
            if cursor_line == None and cursor_column == None:
                self.parent.statusbar_label_left.setText("")
            else:
                statusbar_text = "LINE: " + str(cursor_line+1)
                statusbar_text += " COLUMN: " + str(cursor_column+1)
                self.parent.statusbar_label_left.setText(statusbar_text)
        
        def repl_display_message(self, 
                                 message, 
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
                    data.PyQt.Qsci.QsciScintillaBase.SCI_STYLESETFONT,
                    lexer_number,
                    b'Ariel'
                )
                parent.repl_messages_tab.SendScintilla(
                    data.PyQt.Qsci.QsciScintillaBase.SCI_STYLESETSIZE,
                    lexer_number,
                    10
                )
                parent.repl_messages_tab.SendScintilla(
                    data.PyQt.Qsci.QsciScintillaBase.SCI_STYLESETBOLD,
                    lexer_number,
                    True
                )
                parent.repl_messages_tab.SendScintilla(
                    data.PyQt.Qsci.QsciScintillaBase.SCI_STYLESETUNDERLINE,
                    lexer_number,
                    False
                )
                parent.repl_messages_tab.SendScintilla(
                    data.PyQt.Qsci.QsciScintillaBase.SCI_STYLESETFORE,
                    lexer_number,
                    color
                )
                parent.repl_messages_tab.SendScintilla(
                    data.PyQt.Qsci.QsciScintillaBase.SCI_STYLESETBACK,
                    lexer_number,
                    data.theme.Paper.Default
                )
                parent.repl_messages_tab.SendScintilla(
                    data.PyQt.Qsci.QsciScintillaBase.SCI_STARTSTYLING,
                    start,
                    lexer_number
                )
                parent.repl_messages_tab.SendScintilla(
                    data.PyQt.Qsci.QsciScintillaBase.SCI_SETSTYLING,
                    end - start,
                    lexer_number
                )
            #Define references directly to the parent and mainform for performance and clarity
            parent = self.parent
            #Set the tab name for displaying REPL messages
            repl_messages_tab_name = "REPL MESSAGES"
            #Find the "REPL Message" tab in the basic widgets
            parent.repl_messages_tab = self.find_repl_messages_tab()
            #Create a new REPL tab in the lower basic widget if it doesn't exist
            if parent.repl_messages_tab == None:
                parent.repl_messages_tab = parent.lower_window.plain_add_document(repl_messages_tab_name)
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
                start       = len(start_bytes) - 1
                if start < 0:
                    start = 0
                #Add the error message
                parent.repl_messages_tab.append("{:s}\n".format(message))
                #Convert the text to a byte array to get the correct length of the text
                #if it contains non-ASCII characters
                end_bytes   = parent.repl_messages_tab.text().encode("utf-8")
                #Get the end point to which the text will be highlighted
                end         = len(end_bytes) - 1
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
                parent.repl_messages_tab.append("{:s}\n".format(message))
            #Bring the REPL tab to the front
            if focus_repl_messages == True:
                parent.repl_messages_tab.parent.setCurrentWidget(parent.repl_messages_tab)
            #Bring cursor to the current message 
            if scroll_to_end == True:
                parent.repl_messages_tab.setCursorPosition(parent.repl_messages_tab.lines(), 0)
                parent.repl_messages_tab.setFirstVisibleLine(parent.repl_messages_tab.lines())
        
        def repl_scroll_to_bottom(self):
            """Scroll the REPL MESSAGES tab to the bottom"""
            #Find the "REPL Message" tab in the basic widgets
            self.parent.repl_messages_tab = self.find_repl_messages_tab()
            if self.parent.repl_messages_tab != None:
                self.parent.repl_messages_tab.goto_line(self.parent.repl_messages_tab.lines())
        
        def repl_clear_tab(self):
            """Clear text from the REPL messages tab"""
            #Find the "REPL Message" tab in the basic widgets
            self.parent.repl_messages_tab = self.find_repl_messages_tab()
            #Check if REPL messages tab exists
            if self.parent.repl_messages_tab != None:
                self.parent.repl_messages_tab.setText("")
                self.parent.repl_messages_tab.SendScintilla(data.PyQt.Qsci.QsciScintillaBase.SCI_STYLECLEARALL)
                self.parent.repl_messages_tab.set_theme(data.theme)
                #Bring the REPL tab to the front
                self.parent.repl_messages_tab.parent.setCurrentWidget(self.parent.repl_messages_tab)
        
        def find_repl_messages_tab(self):
            """Find the "REPL Message" tab in the basic widgets of the MainForm"""
            #Set the tab name for displaying REPL messages
            repl_messages_tab_name = "REPL MESSAGES"
            #Call the MainForm function to find the repl tab by name
            self.parent.repl_messages_tab = self.parent.get_tab_by_name(repl_messages_tab_name)
            return self.parent.repl_messages_tab
        
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
            #Define references directly to the parent and mainform for performance and clarity
            parent = self.parent
            #Check if the custom editor is valid
            if custom_editor == None:
                parent.display.repl_display_message(
                        "No document selected for node tree creation!", 
                        message_type=data.MessageType.ERROR
                )
                parent.display.write_to_statusbar("No document selected for node tree creation!", 5000)
                return
            #Check if the document type is Python or C
            if parser != "PYTHON" and parser != "C" and parser != "NIM":
                message = "Document is not C, Nim or Python 3!"
                parent.display.repl_display_message(
                        message, 
                        message_type=data.MessageType.ERROR
                )
                parent.display.write_to_statusbar(message, 5000)
                return
            #Define a name for the NODE tab
            node_tree_tab_name = "NODE TREE/LIST"
            #Find the "NODE TREE/LIST" tab in the basic widgets
            parent.node_tree_tab = parent.get_tab_by_name(node_tree_tab_name)
            if parent.node_tree_tab:
                parent.node_tree_tab.parent.close_tab(node_tree_tab_name)
            #Create a new NODE tab in the upper basic widget and set its icon
            parent.node_tree_tab    = parent.upper_window.tree_add_tab(node_tree_tab_name)
            node_tree_tab           = parent.node_tree_tab
            node_tree_tab_index     = node_tree_tab.parent.indexOf(node_tree_tab)
            node_tree_tab.parent.setTabIcon(
                node_tree_tab_index, 
                node_tree_tab.parent.node_tree_icon
            )
            #Focus the node tree tab
            parent.node_tree_tab.parent.setCurrentWidget(parent.node_tree_tab)
            #Display the nodes according to file type
            if parser == "PYTHON":
                #Get all the file information
                try:
                    python_node_tree = functions.get_python_node_tree(custom_editor.text())
                    parser_error = False
                except Exception as ex:
                    # Exception, probably an error in the file's syntax
                    python_node_tree = []
                    parser_error = ex
                #Display the information in the tree tab
                parent.node_tree_tab.display_python_nodes_in_tree(
                    custom_editor,
                    python_node_tree, 
                    parser_error
                )
            elif parser == "C":
                #Get all the file information
                function_nodes = functions.get_c_function_list(custom_editor.text())
                #Display the information in the tree tab
                parent.node_tree_tab.display_c_nodes(
                    custom_editor, 
                    function_nodes 
                )
            elif parser == "NIM":
                #Get all the file information
                nim_nodes = functions.get_nim_node_tree(custom_editor.text())
                #Display the information in the tree tab
                parent.node_tree_tab.display_nim_nodes(
                    custom_editor, 
                    nim_nodes 
                )
        
        def show_nodes_in_document(self, custom_editor, parser):
            """
            Show the node tree of a parsed file in a "NODE TREE" Scintilla
            document in the upper window
            """
            #Define references directly to the parent and mainform for performance and clarity
            parent = self.parent
            #Check if the custom editor is valid
            if custom_editor == None:
                parent.display.repl_display_message(
                        "No document selected for node tree creation!", 
                        message_type=data.MessageType.ERROR
                )
                parent.display.write_to_statusbar("No document selected for node tree creation!", 5000)
                return
            #Check if the document type is Python or C
            if parser != "PYTHON" and parser != "C":
                parent.display.repl_display_message(
                        "Document is not Python or C!", 
                        message_type=data.MessageType.ERROR
                )
                parent.display.write_to_statusbar("Document is not Python or C", 5000)
                return
            #Nested hotspot function
            def create_hotspot(node_tab):
                #Create the hotspot boundaries
                hotspot_line        = node_tab.lines()-2
                hotspot_first_ch    = node_tab.text(hotspot_line).index("-")
                hotspot_line_length = node_tab.lineLength(hotspot_line)
                hotspot_start       = node_tab.positionFromLineIndex(hotspot_line, hotspot_first_ch)
                hotspot_end         = node_tab.positionFromLineIndex(hotspot_line, hotspot_line_length)
                hotspot_length      = hotspot_end - hotspot_start
                #Style the hotspot on the node tab
                node_tab.hotspots.style(hotspot_start, hotspot_length, color=0xff0000)
            #Create the function and connect the hotspot release signal to it
            def hotspot_release(position, modifiers):
                #Get the line and index at where the hotspot was clicked
                line, index = parent.node_tree_tab.lineIndexFromPosition(position)
                #Get the document name and focus on the tab with the document
                document_name       = re.search("DOCUMENT\:\s*(.*)\n", parent.node_tree_tab.text(0)).group(1)
                goto_line_number    = int(re.search(".*\(line\:(\d+)\).*", parent.node_tree_tab.text(line)).group(1))
                #Find the document, set focus to it and go to the line the hotspot points to
                document_tab = parent.get_tab_by_name(document_name)
                #Check if the document was modified
                if document_tab == None:
                    #Then it has stars(*) in the name
                    document_tab = parent.get_tab_by_name("*{:s}*".format(document_name))
                try:
                    document_tab.parent.setCurrentWidget(document_tab)
                    document_tab.goto_line(goto_line_number)
                except:
                    return
            #Define a name for the NODE tab
            node_tree_tab_name = "NODE TREE/LIST"
            #Find the "NODE" tab in the basic widgets
            parent.node_tree_tab = parent.get_tab_by_name(node_tree_tab_name)
            if parent.node_tree_tab:
                parent.node_tree_tab.parent.close_tab(node_tree_tab_name)
            #Create a new NODE tab in the upper basic widget
            parent.node_tree_tab = parent.upper_window.plain_add_document(node_tree_tab_name)
            #Set the NODE document to be ReadOnly
            parent.node_tree_tab.setReadOnly(True)
            parent.node_tree_tab.setText("")
            parent.node_tree_tab.SendScintilla(data.PyQt.Qsci.QsciScintillaBase.SCI_STYLECLEARALL)
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
                document_text = "DOCUMENT: {:s}\n".format(document_name)
                parent.node_tree_tab.append(document_text)
                parent.node_tree_tab.append("TYPE: {:s}\n\n".format(parser))
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
                document_text = "DOCUMENT: {:s}\n".format(document_name)
                parent.node_tree_tab.append(document_text)
                parent.node_tree_tab.append("TYPE: {:s}\n\n".format(parser))
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
                display_file_info.append("{:s} ({:s})".format(os.path.basename(file), file))
            #Display all found files
            self.parent.display.repl_display_message("Found {:d} files:".format(len(file_list)))
            #Use scintilla HOTSPOTS to create clickable file links
            #Create the function and connect the hotspot release signal to it
            def hotspot_release(position, modifiers):
                #Get the line and index at where the hotspot was clicked
                line, index = self.parent.repl_messages_tab.lineIndexFromPosition(position)
                file =  re.search(
                            ".*\((.*)\)", 
                            self.parent.repl_messages_tab.text(line)
                        ).group(1).replace("\n", "")
                #Open the files
                self.parent.open_file(file, self.parent.main_window)
                #Because open_file updates the new CWD in the REPL MESSAGES,
                #it is needed to set the cursor back to where the hotspot was clicked
                self.parent.repl_messages_tab.setCursorPosition(line, index)
            self.parent.repl_messages_tab.SCN_HOTSPOTRELEASECLICK.connect(hotspot_release)
            #Get the start position
            pos           = self.parent.repl_messages_tab.getCursorPosition()
            hotspot_start = self.parent.repl_messages_tab.positionFromLineIndex(pos[0], pos[1])
            #self.display.repl_display_message("\n".join(found_files))
            self.parent.display.repl_display_message("\n".join(display_file_info))
            #Get the end position
            pos         = self.parent.repl_messages_tab.getCursorPosition()
            hotspot_end = self.parent.repl_messages_tab.positionFromLineIndex(pos[0], pos[1])
            #Style the hotspot on the node tab
            self.parent.repl_messages_tab.hotspots.style(hotspot_start, hotspot_end, color=0xff0000)
        
        def show_directory_tree(self, directory):
            """
            Display the directory information in a TreeDisplay widget
            """
            #Define references directly to the parent and mainform for performance and clarity
            parent = self.parent
            #Define a name for the FOUND FILES tab
            found_files_tab_name = "FILE/DIRECTORY TREE"
            #Find the "FILE/DIRECTORY TREE" tab in the basic widgets
            parent.found_files_tab = parent.get_tab_by_name(found_files_tab_name)
            if parent.found_files_tab:
                parent.found_files_tab.parent.close_tab(found_files_tab_name)
            #Create a new FOUND FILES tab in the upper basic widget
            parent.found_files_tab = parent.upper_window.tree_add_tab(found_files_tab_name)
            #Focus the node tree tab
            parent.found_files_tab.parent.setCurrentWidget(parent.found_files_tab)
            #Display the directory information in the tree tab
            parent.found_files_tab.display_directory_tree(directory)
        
        def show_found_files_in_tree(self, search_text, file_list, directory):
            """
            Display the found files returned from the find_files system function
            in a TreeDisplay widget
            """
            #Define references directly to the parent and mainform for performance and clarity
            parent = self.parent
            #Define a name for the FOUND FILES tab
            found_files_tab_name = "FOUND FILES"
            #Find the "FOUND FILES" tab in the basic widgets
            parent.found_files_tab = parent.get_tab_by_name(found_files_tab_name)
            if parent.found_files_tab:
                parent.found_files_tab.parent.close_tab(found_files_tab_name)
            #Create a new FOUND FILES tab in the upper basic widget
            parent.found_files_tab = parent.upper_window.tree_add_tab(found_files_tab_name)
            #Focus the node tree tab
            parent.found_files_tab.parent.setCurrentWidget(parent.found_files_tab)
            #Display the found files information in the tree tab
            parent.found_files_tab.display_found_files(
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
            parent = self.parent
            #Define a name for the FOUND FILES tab
            found_files_tab_name = "FOUND FILES"
            #Find the FOUND FILES tab in the basic widgets
            parent.found_files_tab = parent.get_tab_by_name(found_files_tab_name)
            if parent.found_files_tab:
                parent.found_files_tab.parent.close_tab(found_files_tab_name)
            #Create a new FOUND FILES tab in the upper basic widget
            parent.found_files_tab = parent.upper_window.tree_add_tab(found_files_tab_name)
            #Focus the node tree tab
            parent.found_files_tab.parent.setCurrentWidget(parent.found_files_tab)
            #Display the found files information in the tree tab
            parent.found_files_tab.display_found_files_with_lines(
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
            parent = self.parent
            #Define a name for the FOUND FILES tab
            found_files_tab_name = "REPLACEMENTS IN FILES"
            #Find the FOUND FILES tab in the basic widgets
            parent.found_files_tab = parent.get_tab_by_name(found_files_tab_name)
            if parent.found_files_tab:
                parent.found_files_tab.parent.close_tab(found_files_tab_name)
            #Create a new FOUND FILES tab in the upper basic widget
            parent.found_files_tab = parent.upper_window.tree_add_tab(found_files_tab_name)
            #Focus the node tree tab
            parent.found_files_tab.parent.setCurrentWidget(parent.found_files_tab)
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
            parent = self.parent
            #Create and initialize a text differ
            text_differ =   helper_forms.TextDiffer(
                                parent.main_window,
                                parent,
                                text_1,
                                text_2,
                                text_name_1,
                                text_name_2)
            #Find the "DIFF(...)" tab in the basic widgets and close it
            diff_tab_string = "DIFF("
            diff_tab = parent.get_tab_by_string_in_name(diff_tab_string)
            if diff_tab:
                diff_tab_index = diff_tab.parent.indexOf(diff_tab)
                diff_tab.parent.close_tab(diff_tab_index)
            #Add the created text differ to the main window
            diff_index = parent.main_window.addTab(
                text_differ, 
                "DIFF({:s} / {:s})".format(text_name_1, text_name_2)
            )
            #Set focus to the text differ tab
            parent.main_window.setCurrentIndex(diff_index)
        
        def show_session_editor(self):
            """Display a window for editing sessions"""
            #Create the SessionGuiManipulator
            settings_manipulator = self.parent.settings.manipulator
            sessions_manipulator = helper_forms.SessionGuiManipulator(
                                        settings_manipulator, 
                                        self.parent.upper_window, 
                                        self.parent
                                    )
            #Find the old "SESSIONS" tab in the basic widgets and close it
            sessions_tab_name = "SESSIONS"
            sessions_tab = self.parent.get_tab_by_name(sessions_tab_name)
            if sessions_tab:
                sessions_tab.parent.close_tab(sessions_tab_name)
            #Show the sessions in the manipulator
            sessions_manipulator.show_sessions()
            #Add the created session manipulator to the upper window
            sm_index = self.parent.upper_window.addTab(
                sessions_manipulator,
                "SESSIONS"
            )
            #Set focus to the text differ tab
            self.parent.upper_window.setCurrentIndex(sm_index)
        
        def create_lexers_menu(self, menu_name, menu_owner, set_lexer_func):
            """
            Create a lexer menu. Currently used in the View menu and
            the CustomEditor tab menu.
            Parameter set_lexer_func has to have:
                - parameter lexer: a lexers.Lexer object
                - parameter lexer_name: a string
            """
            set_lexer = set_lexer_func
            lexers_menu = data.QMenu(menu_name, menu_owner)
            NONE_action = data.QAction('No lexer', lexers_menu)
            NONE_action.setIcon(helper_forms.set_icon('tango_icons/file.png'))
            NONE_action.triggered.connect(
                functools.partial(set_lexer, lexers.Text, 'Plain text')
            )
            ADA_action = data.QAction('Ada', lexers_menu)
            ADA_action.setIcon(helper_forms.set_icon('language_icons/logo_ada.png'))
            ADA_action.triggered.connect(
                functools.partial(set_lexer, lexers.Ada, 'Ada')
            )
            BASH_action = data.QAction('Bash', lexers_menu)
            BASH_action.setIcon(helper_forms.set_icon('language_icons/logo_bash.png'))
            BASH_action.triggered.connect(
                functools.partial(set_lexer, lexers.Bash, 'Bash')
            )
            BATCH_action = data.QAction('Batch', lexers_menu)
            BATCH_action.setIcon(helper_forms.set_icon('language_icons/logo_batch.png'))
            BATCH_action.triggered.connect(
                functools.partial(set_lexer, lexers.Batch, 'Batch')
            )
            CMAKE_action = data.QAction('CMake', lexers_menu)
            CMAKE_action.setIcon(helper_forms.set_icon('language_icons/logo_cmake.png'))
            CMAKE_action.triggered.connect(
                functools.partial(set_lexer, lexers.CMake, 'CMake')
            )
            C_CPP_action = data.QAction('C / C++', lexers_menu)
            C_CPP_action.setIcon(helper_forms.set_icon('language_icons/logo_c_cpp.png'))
            C_CPP_action.triggered.connect(
                functools.partial(set_lexer, lexers.CPP, 'C / C++')
            )
            CSS_action = data.QAction('CSS', lexers_menu)
            CSS_action.setIcon(helper_forms.set_icon('language_icons/logo_css.png'))
            CSS_action.triggered.connect(
                functools.partial(set_lexer, lexers.CSS, 'CSS')
            )
            D_action = data.QAction('D', lexers_menu)
            D_action.setIcon(helper_forms.set_icon('language_icons/logo_d.png'))
            D_action.triggered.connect(
                functools.partial(set_lexer, lexers.D, 'D')
            )
            FORTRAN_action = data.QAction('Fortran', lexers_menu)
            FORTRAN_action.setIcon(helper_forms.set_icon('language_icons/logo_fortran.png'))
            FORTRAN_action.triggered.connect(
                functools.partial(set_lexer, lexers.Fortran, 'Fortran')
            )
            HTML_action = data.QAction('HTML', lexers_menu)
            HTML_action.setIcon(helper_forms.set_icon('language_icons/logo_html.png'))
            HTML_action.triggered.connect(
                functools.partial(set_lexer, lexers.HTML, 'HTML')
            )
            LUA_action = data.QAction('Lua', lexers_menu)
            LUA_action.setIcon(helper_forms.set_icon('language_icons/logo_lua.png'))
            LUA_action.triggered.connect(
                functools.partial(set_lexer, lexers.Lua, 'Lua')
            )
            MAKEFILE_action = data.QAction('MakeFile', lexers_menu)
            MAKEFILE_action.setIcon(helper_forms.set_icon('language_icons/logo_makefile.png'))
            MAKEFILE_action.triggered.connect(
                functools.partial(set_lexer, lexers.Makefile, 'MakeFile')
            )
            MATLAB_action = data.QAction('Matlab', lexers_menu)
            MATLAB_action.setIcon(helper_forms.set_icon('language_icons/logo_matlab.png'))
            MATLAB_action.triggered.connect(
                functools.partial(set_lexer, lexers.Matlab, 'Matlab')
            )
            NIM_action = data.QAction('Nim', lexers_menu)
            NIM_action.setIcon(helper_forms.set_icon('language_icons/logo_nim.png'))
            NIM_action.triggered.connect(
                functools.partial(set_lexer, lexers.Nim, 'Nim')
            )
            OBERON_action = data.QAction('Oberon / Modula', lexers_menu)
            OBERON_action.setIcon(helper_forms.set_icon('language_icons/logo_oberon.png'))
            OBERON_action.triggered.connect(
                functools.partial(set_lexer, lexers.Oberon, 'Oberon / Modula')
            )
            PASCAL_action = data.QAction('Pascal', lexers_menu)
            PASCAL_action.setIcon(helper_forms.set_icon('language_icons/logo_pascal.png'))
            PASCAL_action.triggered.connect(
                functools.partial(set_lexer, lexers.Pascal, 'Pascal')
            )
            PERL_action = data.QAction('Perl', lexers_menu)
            PERL_action.setIcon(helper_forms.set_icon('language_icons/logo_perl.png'))
            PERL_action.triggered.connect(
                functools.partial(set_lexer, lexers.Perl, 'Perl')
            )
            PYTHON_action = data.QAction('Python', lexers_menu)
            PYTHON_action.setIcon(helper_forms.set_icon('language_icons/logo_python.png'))
            PYTHON_action.triggered.connect(
                functools.partial(set_lexer, lexers.Python, 'Python')
            )
            RUBY_action = data.QAction('Ruby', lexers_menu)
            RUBY_action.setIcon(helper_forms.set_icon('language_icons/logo_ruby.png'))
            RUBY_action.triggered.connect(
                functools.partial(set_lexer, lexers.Ruby, 'Ruby')
            )
            ROUTEROS_action = data.QAction('RouterOS', lexers_menu)
            ROUTEROS_action.setIcon(helper_forms.set_icon('language_icons/logo_routeros.png'))
            ROUTEROS_action.triggered.connect(
                functools.partial(set_lexer, lexers.RouterOS, 'RouterOS')
            )
            SQL_action = data.QAction('SQL', lexers_menu)
            SQL_action.setIcon(helper_forms.set_icon('language_icons/logo_sql.png'))
            SQL_action.triggered.connect(
                functools.partial(set_lexer, lexers.SQL, 'SQL')
            )
            TCL_action = data.QAction('TCL', lexers_menu)
            TCL_action.setIcon(helper_forms.set_icon('language_icons/logo_tcl.png'))
            TCL_action.triggered.connect(
                functools.partial(set_lexer, lexers.TCL, 'TCL')
            )
            TEX_action = data.QAction('TeX', lexers_menu)
            TEX_action.setIcon(helper_forms.set_icon('language_icons/logo_tex.png'))
            TEX_action.triggered.connect(
                functools.partial(set_lexer, lexers.TeX, 'TeX')
            )
            VERILOG_action = data.QAction('Verilog', lexers_menu)
            VERILOG_action.setIcon(helper_forms.set_icon('language_icons/logo_verilog.png'))
            VERILOG_action.triggered.connect(
                functools.partial(set_lexer, lexers.Verilog, 'Verilog')
            )
            VHDL_action = data.QAction('VHDL', lexers_menu)
            VHDL_action.setIcon(helper_forms.set_icon('language_icons/logo_vhdl.png'))
            VHDL_action.triggered.connect(
                functools.partial(set_lexer, lexers.VHDL, 'VHDL')
            )
            XML_action = data.QAction('XML', lexers_menu)
            XML_action.setIcon(helper_forms.set_icon('language_icons/logo_xml.png'))
            XML_action.triggered.connect(
                functools.partial(set_lexer, lexers.XML, 'XML')
            )
            YAML_action = data.QAction('YAML', lexers_menu)
            YAML_action.setIcon(helper_forms.set_icon('language_icons/logo_yaml.png'))
            YAML_action.triggered.connect(
                functools.partial(set_lexer, lexers.YAML, 'YAML')
            )
            if data.compatibility_mode == False:
                CoffeeScript_action = data.QAction('CoffeeScript', lexers_menu)
                CoffeeScript_action.setIcon(helper_forms.set_icon('language_icons/logo_coffeescript.png'))
                CoffeeScript_action.triggered.connect(
                    functools.partial(set_lexer, lexers.CoffeeScript, 'CoffeeScript')
                )
            CSharp_action = data.QAction('C#', lexers_menu)
            CSharp_action.setIcon(helper_forms.set_icon('language_icons/logo_csharp.png'))
            CSharp_action.triggered.connect(
                functools.partial(set_lexer, lexers.CPP, 'C#')
            )
            Java_action = data.QAction('Java', lexers_menu)
            Java_action.setIcon(helper_forms.set_icon('language_icons/logo_java.png'))
            Java_action.triggered.connect(
                functools.partial(set_lexer, lexers.Java, 'Java')
            )
            JavaScript_action = data.QAction('JavaScript', lexers_menu)
            JavaScript_action.setIcon(helper_forms.set_icon('language_icons/logo_javascript.png'))
            JavaScript_action.triggered.connect(
                functools.partial(set_lexer, lexers.JavaScript, 'JavaScript')
            )
            Octave_action = data.QAction('Octave', lexers_menu)
            Octave_action.setIcon(helper_forms.set_icon('language_icons/logo_octave.png'))
            Octave_action.triggered.connect(
                functools.partial(set_lexer, lexers.Octave, 'Octave')
            )
            PostScript_action = data.QAction('PostScript', lexers_menu)
            PostScript_action.setIcon(helper_forms.set_icon('language_icons/logo_postscript.png'))
            PostScript_action.triggered.connect(
                functools.partial(set_lexer, lexers.PostScript, 'PostScript')
            )
            Fortran77_action = data.QAction('Fortran77', lexers_menu)
            Fortran77_action.setIcon(helper_forms.set_icon('language_icons/logo_fortran77.png'))
            Fortran77_action.triggered.connect(
                functools.partial(set_lexer, lexers.Fortran77, 'Fortran77')
            )
            IDL_action = data.QAction('IDL', lexers_menu)
            IDL_action.setIcon(helper_forms.set_icon('language_icons/logo_idl.png'))
            IDL_action.triggered.connect(
                functools.partial(set_lexer, lexers.IDL, 'IDL')
            )
            lexers_menu.addAction(NONE_action)
            lexers_menu.addSeparator()
            lexers_menu.addAction(ADA_action)
            lexers_menu.addAction(BASH_action)
            lexers_menu.addAction(BATCH_action)
            lexers_menu.addAction(CMAKE_action)
            lexers_menu.addAction(C_CPP_action)
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
                # Delete the QObject by setting it's parent to None
                self.stored_menus[i].setParent(None)
            self.stored_menus = []
            # Add the newly created menu to the internal list for future cleaning
            self.stored_menus.append(lexers_menu)
            # Return the created menu
            return lexers_menu
    
    class Bookmarks:
        """
        All bookmark functionality
        """
        #Class varibles
        parent = None
        #List of all the bookmarks
        marks = None
        
        def __init__(self, parent):
            """Initialization of the Bookmarks object instance"""
            #Get the reference to the MainWindow parent object instance
            self.parent = parent
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
                    self.parent.display.repl_display_message(
                        "Bookmark '{:d}' was added!".format(i), 
                        message_type=data.MessageType.SUCCESS
                    )
                    return i
            else:
                self.parent.display.repl_display_message(
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
            self.parent.display.repl_display_message(
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
                self.parent.display.repl_display_message(
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
                    self.parent.display.repl_display_message(
                        "Bookmark '{:d}' was removed!".format(i), 
                        message_type=data.MessageType.SUCCESS
                    )
                    break
            else:
                self.parent.display.repl_display_message(
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
                self.parent.display.repl_display_message(
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
                self.parent.display.repl_display_message(
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
                self.parent.display.repl_display_message(
                    "Bookmark '{:d}' is empty!".format(mark_number), 
                    message_type=data.MessageType.WARNING
                )
            else:
                editor = self.marks[mark_number][0]
                line = self.marks[mark_number][1]
                #Focus the stored editor and it's parent basic widget
                editor.parent.setCurrentWidget(editor)
                self.parent.view.set_window_focus(editor.parent.name)
                #Go to the stored line
                editor.goto_line(line)



"""
-----------------------------
Subclassed QTabWidget that can hold all custom editor and other widgets
-----------------------------
"""
class BasicWidget(data.QTabWidget):          
    """Basic widget used for holding QScintilla/QTextEdit objects"""
    class CustomTabBar(data.QTabBar):
        """Custom tab bar used to capture tab clicks, ..."""
        #Reference to the parent widget
        parent      = None
        #Reference to the main form
        main_form   = None
        
        def __init__(self, parent):
            """Initialize the tab bar object"""
            #Initialize superclass
            super().__init__(parent)
            #Store the parent reference
            self.parent = parent
            #Store the main form reference
            self.main_form = self.parent.parent
        
        def mousePressEvent(self, event):
            #Execute the superclass event method
            super().mousePressEvent(event)
            event_button    = event.button()
            key_modifiers   = data.QApplication.keyboardModifiers()
            #Tab Drag&Drop functionality
            if event_button == data.PyQt.QtCore.Qt.LeftButton:
                if (key_modifiers == data.PyQt.QtCore.Qt.ControlModifier or
                    key_modifiers == data.PyQt.QtCore.Qt.ShiftModifier):
                    tab_number = self.parent.tabBar().tabAt(event.pos())
                    if tab_number != -1:
                        mime_data = data.PyQt.QtCore.QMimeData()
                        mime_data.setText("{:s} {:d}".format(self.parent.name, tab_number))
                        drag = data.PyQt.QtGui.QDrag(self.parent)
                        drag.setMimeData(mime_data)
                        drag.setHotSpot(event.pos())
                        drag.exec_(data.PyQt.QtCore.Qt.CopyAction | data.PyQt.QtCore.Qt.MoveAction)
        
        def mouseReleaseEvent(self, event):
            #Execute the superclass event method
            super().mouseReleaseEvent(event)
            event_button = event.button()
            #Check for a right click
            if event_button == data.PyQt.QtCore.Qt.RightButton:
                #Create the popup tab context menu
                menu = self.parent.TabMenu(
                            self, 
                            self.main_form, 
                            self.parent, 
                            self.parent.widget(self.tabAt(event.pos())), 
                            event.pos()
                        )
                #Show the tab context menu
                cursor = data.PyQt.QtGui.QCursor.pos()
                menu.popup(cursor)
                #Accept the event
                event.accept()
    
    class TabMenu(data.QMenu):
        """Custom menu that appears when right clicking a tab"""
        def __init__(self, parent, main_form, basic_widget, editor_widget, cursor_position):
            #Nested function for creating a move or copy action
            def create_move_copy_action(action_name, 
                                        window_name, 
                                        move=True, 
                                        focus_name=None):
                window = main_form.get_window_by_name(window_name)
                action = data.QAction(action_name, self)
                if move == True:
                    func = window.move_editor_in
                    action_func =   functools.partial(
                                        func, 
                                        basic_widget, 
                                        parent.tabAt(cursor_position), 
                                    )
                    icon = helper_forms.set_icon('tango_icons/window-tab-move.png')
                else:
                    func = window.copy_editor_in
                    action_func =   functools.partial(
                                        func, 
                                        basic_widget, 
                                        parent.tabAt(cursor_position), 
                                        focus_name
                                    )
                    icon = helper_forms.set_icon('tango_icons/window-tab-copy.png')
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
                    diff_action.setIcon(helper_forms.set_icon('tango_icons/compare-text-main.png'))
                elif "upper" in action_name.lower():
                    diff_action.setIcon(helper_forms.set_icon('tango_icons/compare-text-upper.png'))
                else:
                    diff_action.setIcon(helper_forms.set_icon('tango_icons/compare-text-lower.png'))
                function =  functools.partial(
                                difference_function, 
                                main_form, 
                                compare_tab_1, 
                                compare_tab_2
                            )
                diff_action.triggered.connect(function)
                return diff_action
            #Nested function for checking is the basic widgets current tab is an editor
            def check_for_editor(basic_widget):
                current_tab = basic_widget.currentWidget()
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
            basic_widget_name = basic_widget.name.lower()
            #Add actions according to the parent BasicWidget
            #Move actions
            move_to_main  = create_move_copy_action("Move to main window", "main")
            move_to_upper = create_move_copy_action("Move to upper window", "upper")
            move_to_lower = create_move_copy_action("Move to lower window", "lower")
            #Copy action
            copy_to_main =  create_move_copy_action(
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
            clear_repl_action.setIcon(helper_forms.set_icon('tango_icons/edit-clear.png'))
            clear_repl_action.triggered.connect(main_form.display.repl_clear_tab)
            #Text difference actions
            diff_main_action =  create_diff_action(
                                    "Text diff to main window", 
                                    main_form, 
                                    main_form.main_window.currentWidget(), 
                                    editor_widget
                                )
            diff_upper_action =  create_diff_action(
                                    "Text diff to upper window", 
                                    main_form, 
                                    main_form.upper_window.currentWidget(), 
                                    editor_widget
                                )
            diff_lower_action =  create_diff_action(
                                    "Text diff to lower window", 
                                    main_form, 
                                    main_form.lower_window.currentWidget(), 
                                    editor_widget
                                )
            #Update current working directory action
            if hasattr(editor_widget, "save_name") == True:
                update_cwd_action = data.QAction("Update CWD", self)
                update_cwd_action.setIcon(helper_forms.set_icon('tango_icons/update-cwd.png'))
                update_cwd_action.triggered.connect(update_cwd)
                self.addAction(update_cwd_action)
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
            if "main" in basic_widget_name:
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
            elif "upper" in basic_widget_name:
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
            elif "lower" in basic_widget_name:
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
    
    #Class variables
    #Name of the basic widget                       
    name                    = ""
    #Reference to the last file that was drag&dropped onto the main  form
    drag_dropped_file       = None
    #Drag&Dropped text data
    drag_text               = None
    #The source widgets of the drag&drop event
    drag_source             = None
    #QMainWindow
    parent                  = None
    #Custom tab bar
    custom_tab_bar          = None
    #Default font for textboxes
    default_editor_font     = data.PyQt.QtGui.QFont('Courier', 10)
    #Stored icon for the node tree tab
    node_tree_icon          = None
    #Stored icon for the repl messages tab
    repl_messages_icon      = None
    #Attribute for indicating if the REPL is indicated
    indicated               = False
    
    
    def __init__(self, parent):
        """Initialization"""
        #Initialize superclass, from which the current class is inherited,
        #THIS MUST BE DONE SO THAT THE SUPERCLASS EXECUTES ITS __init__ !!!!!!
        super().__init__(parent)
        #Set various events and attributes
        #Save parent as a reference
        self.parent = parent
        #Initialize the custom tab bar
        self.custom_tab_bar = self.CustomTabBar(self)
        self.setTabBar(self.custom_tab_bar)
        #Enable drag&drop events
        self.setAcceptDrops(True)           
        #Add close buttons to tabs
        self.setTabsClosable(True)
        #Set tabs as movable, so that you can move tabs with the mouse
        self.setMovable(True)
        #Add signal for coling a tab to the EVT_tabCloseRequested function
        self.tabCloseRequested.connect(self._signal_editor_tabclose)
        #Vonnect signal that fires when the tab index changes
        self.currentChanged.connect(self._signal_editor_tabindex_change)
        #Set the stored node tree tab icon
        self.node_tree_icon = helper_forms.set_icon('tango_icons/edit-node-tree.png')
        #Set the stored node tree tab icon
        self.repl_messages_icon = helper_forms.set_icon('tango_icons/repl-messages.png')
        #Set the stored system icons
        self.system_found_files_icon        = helper_forms.set_icon('tango_icons/system-find-files.png')
        self.system_found_in_files_icon     = helper_forms.set_icon('tango_icons/system-find-in-files.png')
        self.system_replace_in_files_icon   = helper_forms.set_icon('tango_icons/system-replace-in-files.png')

    def _drag_filter(self, event):
        self.drag_dropped_file  = None
        self.drag_text          = None
        self.drag_source        = None
        if event.mimeData().hasUrls():
            url=event.mimeData().urls()[0]
            if url.isValid():
                #filter out non file items
                if url.scheme()=="file":
                    #"toLocalFile" returns path to file
                    self.drag_dropped_file=url.toLocalFile()
                    event.accept()
        elif event.mimeData().text() != None:
            try:
                name, index = event.mimeData().text().split()
                #Don't accept drags into self
                if name != self.name:
                    self.drag_source = event.source()
                    self.drag_text = event.mimeData().text()
                    event.accept()
            except:
                return
    
    def event(self, event):
        #Execute the superclass event method
        super().event(event)
        #Only check indication if the current widget is not indicated
        if self.indicated == False:
            if (event.type() == data.PyQt.QtCore.QEvent.KeyPress or
                event.type() == data.PyQt.QtCore.QEvent.KeyRelease):
                #Check indication
                self.parent.view.indication_check()
        #Indicate that the event was processed by returning True
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
            self.parent.open_file(self.drag_dropped_file,  self)
            event.accept()
        elif self.drag_text != None:
            #Drag&drop widget event occured
            name, str_index = self.drag_text.split()
            index = int(str_index)
            key_modifiers = data.QApplication.keyboardModifiers() 
            if (key_modifiers == data.PyQt.QtCore.Qt.ControlModifier or
                key_modifiers == data.PyQt.QtCore.Qt.AltModifier):
                self.copy_editor_in(self.drag_source, index)
                data.print_log("Drag&Drop copied tab {:d} from the {:s} widget".format(index, name))
            else:
                self.move_editor_in(self.drag_source, index)
                data.print_log("Drag&Drop moved tab {:d} from the {:s} widget".format(index, name))
            event.accept()
        #Reset the drag&drop data attributes
        self.drag_dropped_file  = None
        self.drag_text          = None

    def enterEvent(self, enter_event):
        """Event that fires when the focus shifts to the BasicWidget"""
        cw = self.currentWidget() 
        if cw != None:
            #Check if the current widget is a custom editor or a QTextEdit widget
            if isinstance(cw, CustomEditor):
                #Get currently selected tab in the basic widget and display its name and lexer
                self.parent.display.write_to_statusbar(cw.name)
            else:
                #Display only the QTextEdit name
                self.parent.display.write_to_statusbar(cw.name)
        data.print_log("Entered BasicWidget: " + str(self.name))

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        #Set focus to the clicked basic widget
        self.setFocus()
        #Set Save/SaveAs buttons in the menubar
        self._set_save_status()
        #Store the last focused widget to the parent
        self.parent.last_focused_widget = self
        data.print_log("Stored \"{:s}\" as last focused widget".format(self.name))
        #Hide the function wheel if it is shown
        if self.parent.view.function_wheel_overlay != None:
            self.parent.view.hide_function_wheel()
        #Display the tab name in the log window
        if self.currentWidget() != None:
            tab_name = self.currentWidget().name
            data.print_log("Mouse click in: \"" + str(tab_name) + "\"")
        else:
            #Clear the cursor positions in the statusbar
            self.parent.display.update_cursor_position()
            data.print_log("Mouse click in: \"" + self.name + "\"")

    def wheelEvent(self, wheel_event):
        """QScintilla mouse wheel rotate event"""
        key_modifiers = data.QApplication.keyboardModifiers()
        if data.PYQT_MODE == 4:
            delta = wheel_event.delta()
        else:
            delta = wheel_event.angleDelta().y()
        if delta < 0:
            data.print_log("Mouse rotate down event")
            if key_modifiers == data.PyQt.QtCore.Qt.ControlModifier:
                #Zoom out the scintilla tab view
                self.zoom_out()
        else:
            data.print_log("Mouse rotate up event")
            if key_modifiers == data.PyQt.QtCore.Qt.ControlModifier:
                #Zoom in the scintilla tab view
                self.zoom_in()
        #Handle the event
        if key_modifiers == data.PyQt.QtCore.Qt.ControlModifier:
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
        self.parent.view.save_layout()
        event.setAccepted(False)
    
    def setFocus(self):
        """Overridden focus event"""
        #Execute the supeclass focus function
        super().setFocus()
        #Check indication
        self.parent.view.indication_check()

    def _signal_editor_tabindex_change(self, change_event):
        """Signal when the tab index changes"""
        #Set Save/SaveAs buttons in the menubar
        self._set_save_status()
        #Check if there is a tab in the tab widget
        current_tab = self.currentWidget()
        if current_tab:
            data.print_log("Selected tab: " + str(self.currentWidget().name))
        #Update the icons of the tabs
        for i in range(self.count()):
            if self.tabText(i) == "NODE TREE/LIST":
                self.setTabIcon(i, self.node_tree_icon)
            elif self.tabText(i) == "REPL MESSAGES":
                self.setTabIcon(i, self.repl_messages_icon)
            elif self.tabText(i) == "FOUND FILES":
                self.setTabIcon(i, self.system_found_files_icon)
            elif self.tabText(i) == "FOUND IN FILES":
                self.setTabIcon(i, self.system_found_in_files_icon)
            elif self.tabText(i) == "REPLACED IN FILES":
                self.setTabIcon(i, self.system_replace_in_files_icon)
            else:
                document = self.widget(i)
                if isinstance(document, CustomEditor) == True:
                    if document.current_icon != None:
                        self.setTabIcon(i, document.current_icon)
        #Display special find buttons if the current tab is text differ
        if isinstance(current_tab, CustomEditor) == True:
            def show_lexer_menu():
                def set_lexer(lexer, lexer_name):
                    try:
                        current_tab.clear_lexer()
                        # Initialize and set the new lexer
                        lexer_instance = lexer()
                        current_tab.set_lexer(lexer_instance, lexer_name)
                        # Change the corner widget (button) icon
                        self.cornerWidget().setIcon(current_tab.current_icon)
                        # Display the lexer change
                        message = "Lexer changed to: {:s}".format(lexer_name)
                        self.parent.display.repl_display_message(message)
                    except Exception as ex:
                        print(ex)
                        message = "Error with lexer selection!\n"
                        message += "Select a window widget with an opened document first."
                        self.parent.display.repl_display_message(
                            message, 
                            message_type=data.MessageType.ERROR
                        )
                        self.parent.display.write_to_statusbar(message)
                lexers_menu = self.parent.display.create_lexers_menu(
                    "Change lexer", self, set_lexer
                )
                cursor = data.PyQt.QtGui.QCursor.pos()
                lexers_menu.popup(cursor)
            button_show_lexers = data.QToolButton(self)
            button_show_lexers.setIcon(current_tab.current_icon)
            button_show_lexers.setPopupMode(data.QToolButton.InstantPopup)
            button_show_lexers.setToolTip("Change the current lexer")
            button_show_lexers.clicked.connect(show_lexer_menu)
            button_show_lexers.show()
            self.setCornerWidget(button_show_lexers)
        elif isinstance(current_tab, helper_forms.TextDiffer) == True:
            current_tab.show_find_buttons(self)
        elif isinstance(current_tab, helper_forms.SessionGuiManipulator) == True:
            current_tab.show_session_buttons(self)
        elif isinstance(current_tab, PlainEditor) == True:
            if current_tab.name == "REPL MESSAGES":
                def clear():
                    self.parent.display.repl_clear_tab()
                button_clear_repl_messages = data.QToolButton(self)
                button_clear_repl_messages.setIcon(helper_forms.set_icon('tango_icons/edit-clear.png'))
                button_clear_repl_messages.setPopupMode(data.QToolButton.InstantPopup)
                button_clear_repl_messages.setToolTip("Clear messages")
                button_clear_repl_messages.clicked.connect(clear)
                button_clear_repl_messages.show()
                self.setCornerWidget(button_clear_repl_messages)
        else:
            #Remove the corner widget
            self.setCornerWidget(None)
        
    def _signal_editor_tabclose(self, emmited_tab_number):
        """Event that fires when a tab close"""
        #Nested function for clearing all bookmarks in the document
        def clear_document_bookmarks():
            #Check if bookmarks need to be cleared
            if isinstance(self.widget(emmited_tab_number), CustomEditor):
                self.parent.bookmarks.remove_editor_all(self.widget(emmited_tab_number))
        data.print_log("Closing tab: " + str(self.tabText(emmited_tab_number)))
        # Store the tab reference
        tab = self.widget(emmited_tab_number)
        #Check if the document is modified
        if self.widget(emmited_tab_number).savable == data.CanSave.YES:
            if self.widget(emmited_tab_number).save_status == data.FileStatus.MODIFIED:
                #Close the log window if it is displayed
                self.parent.view.set_log_window(False)
                #Display the close notification
                close_message = "Document '" + self.tabText(emmited_tab_number)
                close_message += "' has been modified!\nClose it anyway?"
                reply = data.QMessageBox.question(
                    self, 
                    'Closing Tab', 
                    close_message,
                    data.QMessageBox.Yes,
                    data.QMessageBox.No
                )
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
        tab.setParent(None)
        del tab

    def _signal_editor_cursor_change(self, cursor_line=None, cursor_column=None):
        """Signal that fires when cursor position changes"""
        self.parent.display.update_cursor_position(cursor_line, cursor_column)
    
    def _set_save_status(self):
        """Enable/disable save/saveas buttons in the menubar"""
        cw = self.currentWidget()
        if cw != None:
            #Check if the current widget is a custom editor or a QTextEdit widget
            if isinstance(cw, CustomEditor):
                #Get currently selected tab in the basic widget and display its name and lexer
                self.parent.display.write_to_statusbar(cw.name)
            else:
                #Display only the QTextEdit name
                self.parent.display.write_to_statusbar(cw.name)
            #Set the Save/SaveAs status of the menubar
            if cw.savable == data.CanSave.YES:
                self.parent.set_save_file_state(True)
            else:
                self.parent.set_save_file_state(False)
        if self.count() == 0:
            self.parent.set_save_file_state(False)
    
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
            if not "*" in self.tabText(self.currentIndex()):
                #Add the special character to the tab name
                self.setTabText(self.currentIndex(), "*" + self.tabText(self.currentIndex()) + "*")
        #Update margin width
        self.editor_update_margin()

    def reset_text_changed(self, index=None):
        """Reset the changed status of the current widget (remove the * symbols from the tab name)"""
        #Update the save status of the current widget
        if index == None:
            if self.currentWidget().savable == data.CanSave.YES:
                self.currentWidget().save_status = data.FileStatus.OK
                self.setTabText(self.currentIndex(), self.tabText(self.currentIndex()).strip("*"))
        else:
            if self.widget(index).savable == data.CanSave.YES:
                self.widget(index).save_status = data.FileStatus.OK
                self.setTabText(index, self.tabText(index).strip("*"))

    def close_tab(self, tab=None):
        """Close a tab in the basic widget"""
        #Return if there are no tabs open
        if self.count == 0:
            return
        #First check if a tab name was given
        if isinstance(tab, str):
            for i in range(0, self.count()):
                if self.tabText(i) == tab:
                    #Tab found, close it
                    self._signal_editor_tabclose(i)
        elif isinstance(tab, int):
            #Close the tab
            self._signal_editor_tabclose(tab)
        elif tab == None:
            #No tab number given, select the current tab for closing
            self._signal_editor_tabclose(self.currentIndex())

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
        new_scintilla_tab = PlainEditor(self, self.parent)
        new_scintilla_tab.setFont(self.default_editor_font)
        #Add attributes for status of the document (!!you can add attributes to objects that have the __dict__ attribute!!)
        new_scintilla_tab.parent    = self
        new_scintilla_tab.name      = name
        #Initialize the scrollbars
        new_scintilla_tab.SendScintilla(data.PyQt.Qsci.QsciScintillaBase.SCI_SETVSCROLLBAR, True)
        new_scintilla_tab.SendScintilla(data.PyQt.Qsci.QsciScintillaBase.SCI_SETHSCROLLBAR, True)
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
        new_scintilla_tab = CustomEditor(self, self.parent, file_with_path)
        #Connect the signals
        new_scintilla_tab.textChanged.connect(new_scintilla_tab.text_changed)
        return new_scintilla_tab
    
    def editor_add_document(self, document_name, type=None, bypass_check=False):
        """Check tab type and add a document to self(QTabWidget)"""
        if type == "file":      #New tab is a file on disk
            file_type = "unknown"
            if bypass_check == False:
                file_type = functions.get_file_type(document_name)
            if file_type != "unknown" or bypass_check == True:
                #Test if file can be read
                if functions.test_text_file(document_name) == None:
                    self.parent.display.repl_display_message(
                        "Testing for TEXT file failed!", 
                        message_type=data.MessageType.ERROR
                    )
                    #File cannot be read
                    return None
                #Create new scintilla document
                new_editor_tab = self.editor_create_document(document_name)    
                #Set the lexer that colour codes the document
                new_editor_tab.choose_lexer(file_type)
                #Add the scintilla document to the tab widget
                new_editor_tab_index = self.addTab(new_editor_tab, os.path.basename(document_name))
                #Make the new tab visible
                self.setCurrentIndex(new_editor_tab_index)              
                data.print_log("Added file: " + document_name)
                #Return the reference to the new added scintilla tab widget
                return self.widget(new_editor_tab_index)
            else:
                data.print_log("!! Document is not a text file or has an unsupported format")
                self.parent.display.write_to_statusbar("Document is not a text file, doesn't exist or has an unsupported format!", 1500)
                return None
        else:           #New tab is an empty tab
            #Create new scintilla object
            new_editor_tab = self.editor_create_document(document_name)
            #Add the scintilla document to the tab widget   
            new_editor_tab_index = self.addTab(new_editor_tab, document_name)
            #Make new tab visible
            self.setCurrentIndex(new_editor_tab_index)
            data.print_log("Added new empty tab: " + document_name)
            #Return the reference to the new added scintilla tab widget
            return self.widget(new_editor_tab_index)
    
    def tree_create_tab(self, tree_tab_name):
        """Create and initialize a tree display widget"""
        #Initialize the custom editor
        new_tree_tab = helper_forms.TreeDisplay(self, self.parent)
        #Add attributes for status of the document (!!you can add attributes to objects that have the __dict__ attribute!!)
        new_tree_tab.parent    = self
        new_tree_tab.name      = tree_tab_name
        new_tree_tab.savable   = data.CanSave.NO
        #Return the reference to the new added tree tab widget
        return new_tree_tab
    
    def tree_add_tab(self, tree_tab_name):
        """Create and initialize a tree display widget"""
        #Initialize the custom editor
        new_tree_tab = self.tree_create_tab(tree_tab_name)
        #Add the tree tab to the tab widget
        new_tree_tab_index = self.addTab(new_tree_tab, tree_tab_name)
        #Return the reference to the new added tree tab widget
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

    def move_tab(self, direction=data.Direction.RIGHT):
        """
        Change the position of the current tab in the basic widget,
        according to the selected direction
        """
        #Store the current index and widget
        current_index   = self.currentIndex()
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

    def copy_editor_in(self, source_basic_widget, source_index, focus_name=None):
        """Copy another CustomEditor widget into self"""
        #Create a new reference to the source custom editor
        source_widget = source_basic_widget.widget(source_index)
        #Check if the source tab is valid
        if source_widget == None:
            return
        #PlainEditor tabs should not be copied
        if isinstance(source_widget, CustomEditor) == False:
            self.parent.display.repl_display_message(
                "Only custom editor tabs can be copied!", 
                message_type=data.MessageType.ERROR
            )
            return
        #Check if the source file already exists in the target basic widget
        check_index = self.parent.check_open_file(source_widget.save_name, self)
        if check_index != None:
            #File is already open, focus it
            self.setCurrentIndex(check_index)
            return
        #Create a new editor document
        new_widget = self.editor_create_document(source_widget.save_name)
        #Add the copied custom editor to the target basic widget
        new_index = self.addTab(
                        new_widget, 
                        source_basic_widget.tabIcon(source_index), 
                        source_basic_widget.tabText(source_index)
                    )
        #Set focus to the copied widget
        self.setCurrentIndex(new_index)
        #Copy the source editor text and set the lexer accordigly
        source_widget.copy_self(new_widget)
        #Also reset the text change
        self.reset_text_changed(new_index)
        #Set Focus to the copied widget parent
        if focus_name == None:
            self.parent.view.set_window_focus(self.drag_source.name)
        else:
           self.parent.view.set_window_focus(focus_name) 
        #Update the margin in the copied widget
        self.editor_update_margin()

    def move_editor_in(self, source_basic_widget, source_index):
        """Move another CustomEditor widget into self without copying it"""
        moved_widget        = source_basic_widget.widget(source_index)
        moved_widget_icon   = source_basic_widget.tabIcon(source_index)
        moved_widget_text   = source_basic_widget.tabText(source_index)
        #Check if the source tab is valid
        if moved_widget == None:
            return
        #PlainEditor tabs should not evaluate its name
        if isinstance(moved_widget, CustomEditor) == True:
            #Check if the source file already exists in the target basic widget
            check_index = self.parent.check_open_file(moved_widget.save_name, self)
            if check_index != None:
                #File is already open, focus it
                self.setCurrentIndex(check_index)
                return
        #Move the custom editor widget from source to target
        new_index = self.addTab(moved_widget, moved_widget_icon, moved_widget_text)
        #Set focus to the copied widget
        self.setCurrentIndex(new_index)
        #Change the custom editor parent
        self.widget(new_index).parent = self
        #Set Focus to the copied widget parent
        self.parent.view.set_window_focus(source_basic_widget.name)


"""
-----------------------------
Subclassed QScintilla widget used for displaying REPL messages, Python/C node trees, ...
-----------------------------
""" 
class PlainEditor(data.PyQt.Qsci.QsciScintilla):
    #Class variables
    name            = None
    parent          = None
    main_form       = None
    savable         = data.CanSave.NO
    default_font    = data.PyQt.QtGui.QFont('Courier', 10)
    """Namespace references for grouping functionality"""
    hotspots    = None
    
    
    def __init__(self, parent, main_form):
        #Initialize the superclass
        super().__init__()
        #Store the main form and parent widget references
        self.parent     = parent
        self.main_form  = main_form
        #Set encoding format to UTF-8 (Unicode)
        self.setUtf8(True)
        #Tabs are spaces by default
        self.setIndentationsUseTabs(False)
        #Set line endings to be Unix style ("\n")
        self.setEolMode(data.default_eol)
        #Initialize the namespace references
        self.hotspots = self.Hotspots(self)
        #Set the initial zoom factor
        self.zoomTo(data.zoom_factor)
        #Set the theme
        self.set_theme(data.theme)
    
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
        #Execute the supeclass focus function
        super().setFocus()
        #Check indication
        self.main_form.view.indication_check()
    
    def goto_line(self, line_number):
        """Set focus and cursor to the selected line"""
        #Move the cursor to the start of the selected line
        self.setCursorPosition(line_number, 0)
        #Move the first displayed line to the top of the viewving area
        self.SendScintilla(
            data.PyQt.Qsci.QsciScintillaBase.SCI_GOTOLINE, 
            line_number
        )
    
    def set_theme(self, theme):
        #Set the lexer
        self.setLexer(lexers.Text(self))
        #Now the theme
        if theme == themes.Air:
            self.resetFoldMarginColors()
        else:
            self.setFoldMarginColors(
                theme.FoldMargin.ForeGround, 
                theme.FoldMargin.BackGround
            )
        self.setMarginsForegroundColor(theme.LineMargin.ForeGround)
        self.setMarginsBackgroundColor(theme.LineMargin.BackGround)
        self.SendScintilla(
            data.PyQt.Qsci.QsciScintillaBase.SCI_STYLESETBACK, 
            data.PyQt.Qsci.QsciScintillaBase.STYLE_DEFAULT, 
            theme.Paper.Default
        )
        self.SendScintilla(
            data.PyQt.Qsci.QsciScintillaBase.SCI_STYLESETBACK, 
            data.PyQt.Qsci.QsciScintillaBase.STYLE_LINENUMBER, 
            theme.LineMargin.BackGround
        )
        self.SendScintilla(
            data.PyQt.Qsci.QsciScintillaBase.SCI_SETCARETFORE, 
            theme.Cursor
        )
    
    class Hotspots():
        """
        Functions for styling text with hotspots
        (namespace/nested class to PlainEditor)
        """
        #Class varibles
        parent = None
        
        def __init__(self, parent):
            """Initialization of the Editing object instance"""
            #Get the reference to the MainWindow parent object instance
            self.parent = parent
        
        def style(self, index_from, length, color=0xff0000):
            """Style the text from/to with a hotspot"""
            send_scintilla = self.parent.SendScintilla
            #Use the scintilla low level messaging system to set the hotspot
            send_scintilla(data.PyQt.Qsci.QsciScintillaBase.SCI_STYLESETHOTSPOT, 2, True)
            send_scintilla(data.PyQt.Qsci.QsciScintillaBase.SCI_SETHOTSPOTACTIVEFORE, True, color)
            send_scintilla(data.PyQt.Qsci.QsciScintillaBase.SCI_SETHOTSPOTACTIVEUNDERLINE, True)
            send_scintilla(data.PyQt.Qsci.QsciScintillaBase.SCI_STARTSTYLING, index_from, 2)
            send_scintilla(data.PyQt.Qsci.QsciScintillaBase.SCI_SETSTYLING, length, 2)


"""
-----------------------------
Subclassed QScintilla widget used for editing
-----------------------------
""" 
class CustomEditor(data.PyQt.Qsci.QsciScintilla):
    """
    QScintilla widget with added custom functions
    COMMENT:    Functions treat items as if the starting with index is 1 instead of 0!
                It's a little confusing at first, but you will get the hang of it.
                This is done because scintilla displays line numbers from index 1.
    """
    #Class variables
    parent                  = None
    main_form               = None
    name                    = ""
    save_name               = ""
    save_status             = data.FileStatus.OK
    savable                 = data.CanSave.NO
    embedded                = False
    last_browsed_dir        = ""
    #Default fonts
    default_font            = data.PyQt.QtGui.QFont('Courier', 10)
    default_comment_font    = b'Courier'
    #Brace matching color
    brace_color             = data.PyQt.QtGui.QColor(255, 153, 0)
    #Current document type, initialized to text
    current_file_type       = "TEXT"
    #Current tab icon
    current_icon            = None
    #Comment character/s that will be used in comment/uncomment functions
    comment_string          = None
    #Oberon/Modula-2/CP have the begin('(*')/end('*)') commenting style,
    #set the attribute to signal this commenting style and the beginning
    #and end commenting string
    oberon_comment_style    = False
    end_comment_string      = None
    #Indicator enumerations
    HIGHLIGHT_INDICATOR     = 0
    FIND_INDICATOR          = 2
    REPLACE_INDICATOR       = 3
    #Status of the edge markes
    edge_marker_state       = False
    #Line strings in a list, gets updated on every text change,
    #can be used like any other python list(append, extend, reverse, ...)
    line_list               = None
    #List that holds the line numbers, gets updated on every text change
    line_count              = None
    """Namespace references for grouping functionality"""
    hotspots                = None
    bookmarks               = None
    
    """
    Subclassed list object for easier text manipulation
    in the scintilla document
    """
    class LineList(list):
        """List object that will hold the lines of the CustomEditor"""
        #Class variables
        parent = None
        
        """
        Class functions/methods
        """
        def __init__(self, parent, initial_text):
            """Overridden init function"""
            #Initialize superclass
            super().__init__()
            #Set the reference to the parent object
            self.parent = parent
            #Check if initial text is valid
            if initial_text:
                #Update the list of lines
                self.update_text_to_list(initial_text)

        def __getitem__(self, key):
            """Overridden list method that returns the specified line(item)"""
            #Check if the value is an int or a slice
            if isinstance(key, int):
                #Create a new key variable, because key is ReadOnly
                actual_key = key
                #Check if the key is lower than 1
                if actual_key == 0:
                    actual_key = 1
                #Check if the key is greater than 0
                if actual_key > 0:
                    actual_key -= 1
                #Return the line string
                return super().__getitem__(actual_key)
            elif isinstance(key, slice):
                #Create new key variables, because key is ReadOnly
                key_min     = key.start
                key_max     = key.stop
                #Check the lower bound of the slice is 0
                if key_min == None:
                    key_min = 0
                #Check if the key is greater than 0
                if key_min > 0:
                    key_min -= 1
                key_slice = slice(key_min, key_max)
                return super().__getitem__(key_slice)
            #The key is an invalid type
            return None

        def __setitem__(self, key, value):
            """Overridden list method that sets the specified line(item) to a value"""
            #Check if the value is a string or a list
            if isinstance(value, str) == False and isinstance(value, list) == False:
                raise Exception("Value has to be a list or a string!")
            #Check if the value is a string or a list
            if isinstance(value, str):
                #Try to set the line
                try:
                    #Create a new key variable, because key is ReadOnly
                    actual_key = key
                    #Check if the key is 0
                    if actual_key == 0:
                        actual_key = 1
                    #Check if the key is greater than 0
                    if actual_key > 0:
                        actual_key -= 1
                    #Set the line
                    super().__setitem__(actual_key, value)
                except:
                    self.append(value, update_parent=False)
                #Update the custom editor document text
                self.parent.set_line(value, key)
            else:
                #The value is a list
                #Create new key variables, because key is ReadOnly
                key_min     = key.start
                key_max     = key.stop
                #Check if the lower boundary of the slice is 0
                if key_min == 0:
                    key_min = 1
                #Check boundary order
                if key_max < key_min:
                    raise Exception("First index has to be higher than the second!")
                #Check the boundaries
                if len(value) != (key_max-key_min+1):
                    raise Exception("Ranges of assignment don't match!")
                #Insert the range into the custom list object
                super().__setitem__(slice(key_min-1, key_max), value)
                #Adjust the line numbers to standard(0..lines()-1) numbering
                line_from   = key_min - 1
                line_to     = key_max - 1
                #Set the new lines in the custom editor document
                self.parent.set_lines(line_from, line_to, value)
        
        def __iadd__(self, value):
            """Overloaded '+=' operator"""
            raise Exception("'+=' operator not implemented yet!")
        
        def __isub__(self, value):
            """Overloaded '-=' operator"""
            raise Exception("'-=' operator not implemented yet!")
        
        def __imul__(self, value):
            """Overloaded '*=' operator"""
            raise Exception("'*=' operator not implemented yet!")

        def _setitem(self, key, value):
            """Set the item at position-key, without updating the scintilla document"""
            #Check if the value is a string
            if isinstance(value, str) == False:
                return
            #Try to set the line
            try:
                #Create a new key variable, because key is ReadOnly
                actual_key = key
                #Check if the key is 0
                if actual_key == 0:
                    actual_key = 1
                #Check if the key is greater than 0
                if actual_key > 0:
                    actual_key -= 1
                #Set the line
                super().__setitem__(actual_key, value)
            except:
                self.append(value, update_parent=False)
        
        def _update_list_to_text(self, scroll_to_line=None):
            """Update the list of lines to the parent CustomEditor document"""
            #Merge the list into a single string with the
            #newline character as the delimiter
            text = "\n".join(self)
            #Update the text of the document
            self.parent.set_all_text(text)
            #Check if a line to which to scroll to was specified
            if scroll_to_line == None:
                scroll_to_line = self.parent.lines()
            #Scroll to the desired line of the document
            self.parent.setCursorPosition(scroll_to_line, 0)
        
        def append(self, value, update_parent=True):
            """
            Overloaded list append method
            Special arguments:
                update_parent   - False: append to list internally without updating
                                         the parent CustomEditor document.
                                  True:  append to list and update the parent
                                         CustomEditor document.
            """
            #Check the update_parent parameter type
            if isinstance(update_parent, bool) == False:
                raise Exception("'update_parent' parameter must be of type boolean!")
            #Check the append value type
            if isinstance(value, str):
                #Execute the superclass append method
                super().append(value)
            elif isinstance(value, list):
                exception_text = "Use 'extend' to add multiple lines!"
                raise Exception(exception_text)
            else:
                exception_text = "'append' parameter must be a string!"
                raise Exception(exception_text)
            #Check if updating the parent document is needed
            if update_parent == True:
                self._update_list_to_text()
        
        def extend(self, value, update_parent=True):
            """
            Overloaded list extend method
            Special arguments:
                update_parent   - False: append to list internally without updating
                                         the parent CustomEditor document.
                                  True:  append to list and update the parent
                                         CustomEditor document.
            """
            #Check the update_parent parameter type
            if isinstance(update_parent, bool) == False:
                raise Exception("'update_parent' parameter must be of type boolean!")
            #Check the extend value type
            if isinstance(value, list) == False:
                raise Exception("Extend parameter must be a list!")
            elif all(isinstance(item, str) for item in value) == False:
                raise Exception("All extend list items must be strings!")
            #Extend the list
            super().extend(value)
            #Check if updating the parent document is needed
            if update_parent == True:
                self._update_list_to_text()
        
        def insert(self, index, value, update_parent=True):
            """Overloaded insert method"""
            #Check the insert index type
            if isinstance(index, int) == False:
                raise Exception("Insert index parameter must be an integer!")
            #Check the insert value type
            if isinstance(value, str) == False:
                raise Exception("Insert parameter must be a string!")
            #Correct and check the index
            index -= 1
            if index < 0:
                index = 0
            #Insert the item
            super().insert(index, value)
            #Check if updating the parent document is needed
            if update_parent == True:
                self._update_list_to_text(index)
        
        def pop(self, index=None, update_parent=True):
            """Overloaded pop method"""
            #Check the insert index type
            if isinstance(index, int) == False:
                raise Exception("Pop index parameter must be an integer!")
            #Correct and check the index
            index -= 1
            if index < 0:
                index = 0
            #Pop out the item
            return_item = super().pop(index)
            #Check if updating the parent document is needed
            if update_parent == True:
                self._update_list_to_text(index)
            #Return the poped line
            return return_item
        
        def remove(self, item, update_parent=True):
            """Overloaded remove method"""
            #Check the insert index type
            if isinstance(item, str) == False:
                raise Exception("Remove item parameter must be a string!")
            #Check if item exists
            if not(item in self):
                raise Exception("Cannot remove item! Item is not in the list!")
            else:
                index = self.index(item) - 1
                #Check the index
                if index < 0:
                    index = 0    
            #Remove the item
            super().remove(item)
            #Check if updating the parent document is needed
            if update_parent == True:
                self._update_list_to_text(index)
        
        def reverse(self, update_parent=True):
            """Overloaded reverse method"""
            #Reverse the list
            super().reverse()
            #Check if updating the parent document is needed
            if update_parent == True:
                self._update_list_to_text()
            
        def sort(self, update_parent=True):
            """Overloaded sort method"""
            pass
            #Reverse the list
            super().sort()
            #Check if updating the parent document is needed
            if update_parent == True:
                self._update_list_to_text()
        
        def update_text_to_list(self, update_text):
            """Update the list from a string"""
            #Check if the value is a string
            if isinstance(update_text, str) == False:
                return
            #Empty the list
            del self[:]
            #Set the new content
            self.extend(re.split("\n", update_text), update_parent=False)
        
        def get_absolute_cursor_position(self):
            """Get the absolute cursor position"""
            line, index = self.parent.getCursorPosition()
            absolute_position = 0
            for i in range(line):
                absolute_position += len(self[i])
            absolute_position += index + 1
            return absolute_position
    
#    """
#    LineList property functions (decorators)
#    NOTE:  This isn't needed because a safety is implemented in the __setattr__
#           function that prevets reassignment of the line_list attribute.
#           Just left it in if anyone is interested in decorators.
#    """
#    @property
#    def line_list(self):
#        """Getter function for the _line_list attribute"""
#        return self._line_list
#    
#    @line_list.setter
#    def line_list(self, value):
#        """Setter function for the _line_list attribute"""
#        self.main_form.display.repl_display_message("Cannot reassign the LineList attribute!")
#    
#    @line_list.deleter
#    def line_list(self):
#        self.main_form.display.repl_display_message("Cannot delete the LineList attribute!")

    """
    Built-in and private functions
    """
    def __init__(self, parent, main_form, file_with_path=None):
        """Initialize the scintilla widget"""
        #Initialize superclass, from which the current class is inherited,
        #THIS MUST BE DONE SO THAT THE SUPERCLASS EXECUTES ITS __init__ !!!!!!
        super().__init__()
        #Set encoding format to UTF-8 (Unicode)
        self.setUtf8(True)
        #Set font family and size
        self.setFont(self.default_font)
        #Set the margin type (0 is by default line numbers, 1 is for non code folding symbols and 2 is for code folding)
        self.setMarginType(0, data.PyQt.Qsci.QsciScintilla.NumberMargin)
        #Set margin width and font
        self.setMarginWidth(0, "00")
        self.setMarginsFont(self.default_font)
        #Reset the modified status of the document
        self.setModified(False)
        #Set brace matching
        self.setBraceMatching(data.PyQt.Qsci.QsciScintilla.SloppyBraceMatch)
        self.setMatchedBraceBackgroundColor(self.brace_color)
        #Autoindentation enabled when using "Enter" to indent to the same level as the previous line
        self.setAutoIndent(True)
        #Tabs are spaces by default
        self.setIndentationsUseTabs(False)
        #Set tab space indentation width
        self.setTabWidth(data.tab_width)
        #Set backspace to delete by tab widths
        self.setBackspaceUnindents(True)
        #Scintilla widget must not accept drag/drop events, the cursor freezes if it does!!!
        self.setAcceptDrops(False)
        #Set line endings to be Unix style ("\n")
        self.setEolMode(data.default_eol)
        #Set the initial zoom factor
        self.zoomTo(data.zoom_factor)
        #Correct the file name if it is unspecified
        if file_with_path == None:
            file_with_path = ""
        #Add attributes for status of the document (!!you can add attributes to objects that have the __dict__ attribute!!)
        self.parent     = parent
        self.main_form  = main_form
        self.name       = os.path.basename(file_with_path)
        #Set save name with path
        if os.path.dirname(file_with_path) != "":
            self.save_name  = file_with_path
        else:
            self.save_name  = ""
        #Replace back-slashes to forward-slashes on Windows
        if platform.system() == "Windows":
            self.save_name  = self.save_name.replace("\\", "/")
        #Last directory browsed by the "Open File" and other dialogs
        if self.save_name != "":
            #If save_name was valid, extract the directory of the save file
            self.last_browsed_dir = os.path.dirname(self.save_name)
        else:
            self.last_browsed_dir = self.save_name
        #Reset the file save status 
        self.save_status = data.FileStatus.OK
        #Enable saving of the scintilla document
        self.savable = data.CanSave.YES
        #Initialize instance variables
        self._init_special_functions()
        #Make second margin (the one to the right of the line number margin),
        #sensitive to mouseclicks
        self.setMarginSensitivity(1, True)
        #Add needed signals
        self.cursorPositionChanged.connect(self.parent._signal_editor_cursor_change)
        self.marginClicked.connect(self._margin_clicked)
        self.linesChanged.connect(self._lines_changed)
        #Set the lexer to the default Plain Text
        self.choose_lexer("text")
        #Setup autocompletion
        self.init_autocompletions()
        #Setup the LineList object that will hold the custom editor text as a list of lines
        self.line_list = self.LineList(self, self.text())
        self.line_list = [""]
        #Bookmark initialization
        self._init_bookmark_marker()
        #Initialize the namespace references
        self.hotspots   = self.Hotspots(self)
        self.bookmarks  = self.Bookmarks(self)
        self.keyboard   = self.Keyboard(self)
    
    def __setattr__(self, name, value):
        """
        Special/magic method that is called everytime an attribute of
        the CustomEditor class is set.
        """
        #Filter out the line_list attribute
        if name == "line_list":
            #Check if the assigned object is NOT a LineList object
            if isinstance(value, self.LineList) == False:
                #Check the extend value type
                if isinstance(value, list) == False:
                    raise Exception("Reassignment value of line_list must be a list!")
                elif all(isinstance(item, str) for item in value) == False:
                    raise Exception("All value list items must be strings!")
                text = self.list_to_text(value)
                self.set_all_text(text)
                self.line_list.update_text_to_list(text)
                #Cancel the assignment
                return
        #Call the superclasses/original __setattr__() special method
        super().__setattr__(name, value)
        
    def _init_special_functions(self):
        """Initialize the methods for document manipulation"""
        #Set references to the special functions
        self.find           = self.find_text
        self.save           = self.save_document
        self.clear          = self.clear_editor
        self.highlight      = self.highlight_text

    def _filter_keypress(self, key_event):
        """Filter keypress for appropriate action"""
        #pressed_key = key_event.key()
        accept_keypress = False
        return accept_keypress

    def _filter_keyrelease(self, key_event):
        """Filter keyrelease for appropriate action"""
        #released_key = key_event.key()
        accept_keyrelease = False
        return accept_keyrelease
    
    def _init_bookmark_marker(self):
        """Initialize the marker for the bookmarks"""
        image_scale_size = data.PyQt.QtCore.QSize(16, 16)
        bookmark_image  = helper_forms.set_pixmap('tango_icons/bookmark.png')
        bookmark_image  = bookmark_image.scaled(image_scale_size)
        self.bookmark_marker = self.markerDefine(bookmark_image, 1)
    
    def _margin_clicked(self, margin, line, state):
        """Signal for a mouseclick on the margin"""
        #Adjust line index to the line list indexing (1..lines)
        adjusted_line = line + 1
        #Add/remove bookmark
        self.bookmarks.toggle_at_line(adjusted_line)
    
    def _lines_changed(self):
        """Signal that fires when the number of lines changes"""
        self.markerDeleteAll(self.bookmark_marker)
        bookmarks = self.main_form.bookmarks.marks
        for i in bookmarks:
            if bookmarks[i][0] == self:
                self.bookmarks.add_marker_at_line(bookmarks[i][1])
    
    def _skip_next_repl_focus(self):
        #Disable REPL focus after the REPL evaluation
        self.main_form.repl.skip_next_repl_focus()
        #Set focus to the basic widget that holds this document
        self.main_form.view.set_window_focus(self.parent.name.lower())


    """
    Qt QSciScintilla functions
    """
    def keyPressEvent(self, event):
        """QScintila keyPressEvent, to catch which key was pressed"""
        #Filter out TAB and SHIFT+TAB key combinations to override
        #the default indent/unindent functionality
        key = event.key()
#        char = event.text()
#        key_modifiers = data.QApplication.keyboardModifiers()
        if key == data.PyQt.QtCore.Qt.Key_Tab:
            self.custom_indent()
        elif key == data.PyQt.QtCore.Qt.Key_Backtab:
            self.custom_unindent()
        elif (key == data.PyQt.QtCore.Qt.Key_Enter or
              key == data.PyQt.QtCore.Qt.Key_Return):
            super(data.PyQt.Qsci.QsciScintilla, self).keyPressEvent(event)
            #Check for autoindent character list
            if hasattr(self.lexer(), "autoindent_characters"):
                line_number = self.get_line_number()
                #Check that the last line is valid
                if len(self.line_list[line_number-1]) == 0:
                    return
                elif len(self.line_list[line_number-1].rstrip()) == 0:
                    return
                last_character = self.line_list[line_number-1].rstrip()[-1]
                if last_character in self.lexer().autoindent_characters:
                    line = self.line_list[line_number]
                    stripped_line = self.line_list[line_number].strip()
                    if stripped_line == "":
                        self.line_list[line_number] = (self.line_list[line_number] +
                                                       " " * data.tab_width)
                        self.setCursorPosition(
                            line_number-1, 
                            len(self.line_list[line_number])
                        )
                    else:
                        whitespace = len(line) - len(line.lstrip())
                        self.line_list[line_number] = (" " * whitespace + 
                                                       " " * data.tab_width + 
                                                       stripped_line)
                        #The line is not empty, move the cursor to the first
                        #non-whitespace character
                        self.setCursorPosition(
                            line_number-1, 
                            whitespace + data.tab_width
                        )
        else:
            #Execute the superclass method first, the same trick as in __init__ !
            super(data.PyQt.Qsci.QsciScintilla, self).keyPressEvent(event)
            #Filter the event
            self._filter_keypress(event)

    def keyReleaseEvent(self, event):
        """QScintila KeyReleaseEvent, to catch which key was released"""
        #Execute the superclass method first, the same trick as in __init__ !
        super(data.PyQt.Qsci.QsciScintilla, self).keyReleaseEvent(event)
        #Filter the event
        self._filter_keyrelease(event)

    def mousePressEvent(self, event):
        """Overloaded mouse click event"""
        #Execute the superclass method first, the same trick as in __init__ !
        super(data.PyQt.Qsci.QsciScintilla, self).mousePressEvent(event)
        #Set focus to the clicked editor
        self.setFocus()
        #Set Save/SaveAs buttons in the menubar
        self.parent._set_save_status()
        #Update the cursor positions in the statusbar
        self.main_form.display.update_cursor_position(self.getCursorPosition()[0], self.getCursorPosition()[1])
        #Set the last focused widget to the parent basic widget
        self.main_form.last_focused_widget = self.parent
        data.print_log("Stored \"{:s}\" as last focused widget".format(self.parent.name))
        #Hide the function wheel if it is shown
        if self.main_form.view.function_wheel_overlay != None:
            self.main_form.view.hide_function_wheel()

    def wheelEvent(self, event):
        """Mouse scroll event of the custom editor"""
        key_modifiers = data.QApplication.keyboardModifiers()
        if key_modifiers != data.PyQt.QtCore.Qt.ControlModifier:
            #Execute the superclass method
            super(data.PyQt.Qsci.QsciScintilla, self).wheelEvent(event)
        else:
            #Ignore the event, it will be propageted up to the parent objects
            event.ignore()

    def text_changed(self):
        """Event that fires when the scintilla document text changes"""
        #Update the line list
        self.line_list.update_text_to_list(self.text())
        #Update the line count list with a list comprehention
        self.line_count = [line for line in range(1, self.lines()+1)]
        #Execute the parent basic widget signal
        self.parent._signal_text_changed()
    
    def setFocus(self):
        """Overridden focus event"""
        #Execute the supeclass focus function
        super().setFocus()
        #Check the save button status of the menubar
        self.parent._set_save_status()
        #Check indication
        self.main_form.view.indication_check()

    """
    Line manipulation functions
    """
    def goto_line(self, line_number):
        """Set focus and cursor to the selected line"""
        #Check if the selected line is within the line boundaries of the current document
        line_number = self.check_line_numbering(line_number)
        #Move the cursor to the start of the selected line
        self.setCursorPosition(line_number, 0)
        #Move the first displayed line to the top of the viewing area minus an offset
        self.set_first_visible_line(line_number - 10)
        #Disable REPL focus after the REPL evaluation
        self._skip_next_repl_focus()
    
    def set_first_visible_line(self, line_number):
        """Move the top of the viewing area to the selected line"""
        self.SendScintilla(
            data.PyQt.Qsci.QsciScintillaBase.SCI_SETFIRSTVISIBLELINE, 
            line_number
        )

    def remove_line(self, line_number):
        """Remove a line from the custom editor"""
        #Check if the selected line is within the line boundaries of the current document
        line_number = self.check_line_numbering(line_number)
        #Select the whole line text, "tab.lineLength(line_number)" doesn't work because a single UTF-8 character has the length of 2
        self.setSelection(line_number, 0, line_number+1, 0)
        #Replace the line with an empty string
        self.replaceSelectedText("")
    
    def replace_line(self, replace_text, line_number):
        """
        Replace an entire line in a scintilla document
            - line_number has to be as displayed in a QScintilla widget, which is ""from 1 to number_of_lines""
        """
        #Check if the selected line is within the line boundaries of the current document
        line_number = self.check_line_numbering(line_number)
        #Select the whole line text, "tab.lineLength(line_number)" doesn't work because a single UTF-8 character has the length of 2
        self.setSelection(line_number, 0, line_number+1, 0)
        #Replace the selected text with the new
        if "\n" in self.selectedText() or "\r\n" in self.selectedText():
            self.replaceSelectedText(replace_text + "\n")
        else:
            #The last line, do not add the newline character
            self.replaceSelectedText(replace_text)

    def set_line(self, line_text, line_number):
        """Set the text of a line"""
        self.replace_line(line_text, line_number)
    
    def set_lines(self, line_from, line_to, list_of_strings):
        """
        Set the text of multiple lines in one operation.
        This function is almost the same as "prepend_to_lines" and "append_to_lines",
        they may be merged in the future.
        """
        #Check the boundaries
        if line_from < 0:
            line_from = 0
        if line_to < 0:
            line_to = 0
        #Select the text from the lines and test if line_to is the last line in the document
        if line_to == self.lines()-1:
            self.setSelection(line_from, 0, line_to, len(self.text(line_to)))
        else:
            self.setSelection(line_from, 0, line_to, len(self.text(line_to))-1)
        #Split get the selected lines and add them to a list
        selected_lines = []
        for i in range(line_from, line_to+1):
            selected_lines.append(self.text(i))
        #Loop through the list and replace the line text
        for i in range(len(selected_lines)):
            selected_lines[i] = list_of_strings[i]
        #Replace the selected text with the prepended list merged into one string
        self.replaceSelectedText(self.list_to_text(selected_lines))
        #Set the cursor to the beginning of the last set line
        self.setCursorPosition(line_to, 0)

    def set_all_text(self, text):
        """
        Set the entire scintilla document text with a single select/replace routine.
        This function was added, because "setText()" function from Qscintilla
        cannot be undone!
        """
        #Check if the text is a list of lines
        if isinstance(text, list):
            #Join the list items into one string with newline as the delimiter
            text = "\n".join(text)
        #Select all the text in the document
        self.setSelection(0,0,self.lines(),0)
        #Replace it with the new text
        self.replaceSelectedText(text)
    
    def set_theme(self, theme):
        if theme == themes.Air:
            self.resetFoldMarginColors()
        else:
            self.setFoldMarginColors(
                theme.FoldMargin.ForeGround, 
                theme.FoldMargin.BackGround
            )
        self.setMarginsForegroundColor(theme.LineMargin.ForeGround)
        self.setMarginsBackgroundColor(theme.LineMargin.BackGround)
        self.SendScintilla(
            data.PyQt.Qsci.QsciScintillaBase.SCI_STYLESETBACK, 
            data.PyQt.Qsci.QsciScintillaBase.STYLE_DEFAULT, 
            theme.Paper.Default
        )
        self.SendScintilla(
            data.PyQt.Qsci.QsciScintillaBase.SCI_STYLESETBACK, 
            data.PyQt.Qsci.QsciScintillaBase.STYLE_LINENUMBER, 
            theme.LineMargin.BackGround
        )
        self.SendScintilla(
            data.PyQt.Qsci.QsciScintillaBase.SCI_SETCARETFORE, 
            theme.Cursor
        )
    
    def get_line_number(self):
        """return the line on which the cursor is"""
        return self.getCursorPosition()[0] + 1

    def get_line(self, line_number):
        """Return the text of the selected line in the scintilla document"""
        line_text = self.text(line_number - 1)
        return line_text.replace("\n", "")

    def get_lines(self, line_from=None, line_to=None):
        """Return the text of the entire scintilla document as a list of lines"""
        #Check if boundaries are valid
        if line_from == None or line_to == None:
            return self.line_list
        else:
            #Slice up the line_list list according to the boundaries
            return self.line_list[line_from:line_to]
    
    def get_absolute_cursor_position(self):
        """
        Get the absolute cursor position using the line list
        NOTE:
            This function returns the actual length of characters,
            NOT the length of bytes!
        """
        return self.line_list.get_absolute_cursor_position()
    
    def append_to_line(self, append_text,  line_number):
        """Add text to the back of the line"""
        #Check if the appending text is valid
        if append_text != "" and append_text != None:
            #Append the text, stripping the newline characters from the current line text
            self.replace_line(self.get_line(line_number).rstrip() + append_text, line_number)
    
    def append_to_lines(self, *args, **kwds):
        """Add text to the back of the line range"""
        #Check the arguments and keyword arguments
        appending_text = ""
        sel_line_from, sel_index_from, sel_line_to, sel_index_to = self.getSelection()
        if len(args) == 1 and isinstance(args[0], str) and (sel_line_from == sel_line_to):
            #Append text to all lines
            appending_text = args[0]
            line_from = 1
            line_to = self.lines()
        elif (len(args) == 3 and
              isinstance(args[0], str) and
              isinstance(args[1], int) and
              isinstance(args[2], int)):
            #Append text to specified lines
            appending_text  = args[0]
            line_from       = args[1]
            line_to         = args[2]
        elif sel_line_from != sel_line_to:
            #Append text to selected lines
            appending_text  = args[0]
            line_from       = sel_line_from + 1
            line_to         = sel_line_to + 1
        else:
            self.main_form.display.write_to_statusbar("Wrong arguments to 'append' function!", 1000)
            return
        #Check if the appending text is valid
        if appending_text != "" and appending_text != None:
            #Adjust the line numbers to standard(0..lines()) numbering
            line_from -= 1
            line_to  -= 1
            #Check the boundaries
            if line_from < 0:
                line_from = 0
            if line_to < 0:
                line_to = 0
            #Select the text from the lines
            self.setSelection(line_from, 0, line_to,  len(self.text(line_to).replace("\n", "")))
            #Split the line text into a list
            selected_lines = self.text_to_list(self.selectedText())
            #Loop through the list and prepend the prepend text
            for i in range(len(selected_lines)):
                selected_lines[i] = selected_lines[i] + appending_text
            #Replace the selected text with the prepended list merged into one string
            self.replaceSelectedText(self.list_to_text(selected_lines))
    
    def prepend_to_line(self, append_text, line_number):
        """Add text to the front of the line"""
        #Check if the appending text is valid
        if append_text != "" and append_text != None:
            #Prepend the text, stripping the newline characters from the current line text
            self.replace_line(
                append_text + self.get_line(line_number).rstrip(),
                line_number
            )

    def prepend_to_lines(self, *args, **kwds):
        """Add text to the front of the line range"""
        #Check the arguments and keyword arguments
        prepending_text = ""
        sel_line_from, sel_index_from, sel_line_to, sel_index_to = self.getSelection()
        if len(args) == 1 and isinstance(args[0], str) and (sel_line_from == sel_line_to):
            #Prepend text to all lines
            prepending_text = args[0]
            line_from = 1
            line_to = self.lines()
        elif (len(args) == 3 and 
              isinstance(args[0], str) and
              isinstance(args[1], int) and
              isinstance(args[2], int)):
            #Prepend text to specified lines
            prepending_text = args[0]
            line_from       = args[1]
            line_to         = args[2]
        elif sel_line_from != sel_line_to:
            #Prepend text to selected lines
            prepending_text  = args[0]
            line_from       = sel_line_from + 1
            line_to         = sel_line_to + 1
        else:
            self.main_form.display.write_to_statusbar("Wrong arguments to 'prepend' function!", 1000)
            return
        #Check if the appending text is valid
        if prepending_text != "" and prepending_text != None:
            #Adjust the line numbers to standard(0..lines()) numbering
            line_from   -= 1
            line_to     -= 1
            #Check the boundaries
            if line_from < 0:
                line_from = 0
            if line_to < 0:
                line_to = 0
            #Select the text from the lines
            self.setSelection(line_from, 0, line_to, len(self.text(line_to))-1)
            #Split the line text into a list
            selected_lines = self.text_to_list(self.selectedText())
            #Loop through the list and prepend the prepend text
            for i in range(len(selected_lines)):
                selected_lines[i] = prepending_text + selected_lines[i]
            #Replace the selected text with the prepended list merged into one string
            self.replaceSelectedText(self.list_to_text(selected_lines))
            #Set the cursor to the beginning of the last prepended line
            self.setCursorPosition(line_to, 0)

    def comment_line(self, line_number=None):
        """Comment a single line according to the currently set lexer"""
        if line_number == None:
            line_number = self.getCursorPosition()[0] + 1
        #Check commenting style
        if self.oberon_comment_style == True:
            self.prepend_to_line(self.comment_string, line_number)
            self.append_to_line(self.end_comment_string, line_number)
        else:
            self.prepend_to_line(self.comment_string, line_number)
        #Return the cursor to the commented line
        self.setCursorPosition(line_number-1, 0)

    def comment_lines(self, line_from=0, line_to=0):
        """Comment lines according to the currently set lexer"""
        if line_from == line_to:
            return
        else:
            #Check commenting style
            if self.oberon_comment_style == True:
                self.prepend_to_lines(self.comment_string, line_from, line_to)
                self.append_to_lines(self.end_comment_string, line_from, line_to)
            else:
                self.prepend_to_lines(self.comment_string, line_from, line_to)
            #Select the commented lines again, reverse the boundaries,
            #so that the cursor will be at the beggining of the selection
            self.setSelection(line_to-1, self.lineLength(line_to-1)-1, line_from-1, 0)

    def uncomment_line(self, line_number=None):
        """Uncomment a single line according to the currently set lexer"""
        if line_number == None:
            line_number = self.getCursorPosition()[0] + 1
        line_text       = self.get_line(line_number)
        #Check the commenting style
        if self.oberon_comment_style == True:
            if line_text.lstrip().startswith(self.comment_string):
                new_line = line_text.replace(self.comment_string, "", 1)
                new_line = functions.right_replace(new_line, self.end_comment_string, "", 1)
                self.replace_line(new_line, line_number)
                #Return the cursor to the uncommented line
                self.setCursorPosition(line_number-1, 0)
        else:
            if line_text.lstrip().startswith(self.comment_string):
                self.replace_line(line_text.replace(self.comment_string, "", 1), line_number)
                #Return the cursor to the uncommented line
                self.setCursorPosition(line_number-1, 0)

    def uncomment_lines(self, line_from, line_to):
        """Uncomment lines according to the currently set lexer"""
        if line_from == line_to:
            return
        else:
            #Adjust the line numbers to standard(0..lines()-1) numbering
            line_from   -= 1
            line_to     -= 1
            #Select the text from the lines
            self.setSelection(line_from, 0, line_to, self.lineLength(line_to)-1)
            #Split the line text into a list
            selected_lines = self.text_to_list(self.selectedText())
            #Loop through the list and remove the comment string if it's in front of the line
            for i in range(len(selected_lines)):
                #Check the commenting style
                if self.oberon_comment_style == True:
                    if selected_lines[i].lstrip().startswith(self.comment_string):
                        selected_lines[i] = selected_lines[i].replace(
                                                self.comment_string, 
                                                "", 
                                                1
                                            )
                        selected_lines[i] = functions.right_replace(
                                                selected_lines[i], 
                                                self.end_comment_string, 
                                                "", 
                                                1
                                            )
                else:
                    if selected_lines[i].lstrip().startswith(self.comment_string):
                        selected_lines[i] = selected_lines[i].replace(self.comment_string, "", 1)
            #Replace the selected text with the prepended list merged into one string
            self.replaceSelectedText(self.list_to_text(selected_lines))
            #Select the uncommented lines again, reverse the boundaries,
            #so that the cursor will be at the beggining of the selection
            self.setSelection(line_to, self.lineLength(line_to)-1, line_from, 0)
    
    def indent_lines_to_cursor(self):
        """
        Indent selected lines to the current cursor position in the document.
        P.S.:   Ex.Co. uses spaces as tabs by default, so if you copy text that
                contains tabs, the indent will not be correct unless you run the
                tabs_to_spaces function first!
        """
        #Test if there is no selected text
        if self.getSelection() == (-1, -1, -1, -1):
            return
        #Get the cursor index in the current line and selected lines
        cursor_position     = self.getCursorPosition()
        indent_space        = cursor_position[1] * " "
        start_line_number   = self.getSelection()[0] + 1
        end_line_number     = self.getSelection()[2] + 1
        #Get the lines text as a list
        indented_lines = []
        line_list = self.get_lines(start_line_number, end_line_number)
        for i in range(len(line_list)):
            line = line_list[i].lstrip()
            indented_lines.append(indent_space + line)
        #Adjust the line numbers to standard(0..lines()) numbering
        start_line_number   -= 1
        end_line_number     -= 1
        #Select the text from the lines
        if end_line_number == (self.lines()-1):
            #The last selected line is at the end of the document,
            #select every character to the end.
            self.setSelection(start_line_number, 0, end_line_number, self.lineLength(end_line_number))
        else:
            self.setSelection(start_line_number, 0, end_line_number, self.lineLength(end_line_number)-1)
        #Replace the selected text with the prepended list merged into one string
        self.replaceSelectedText(self.list_to_text(indented_lines))
        #Move the cursor to the beggining of the restore line
        #to reset the document view to the beginning of the line
        self.setCursorPosition(cursor_position[0], 0)
        #Restore cursor back to the original position
        self.setCursorPosition(cursor_position[0], cursor_position[1])
    
    def custom_indent(self):
        """
        Scintila indents line-by-line, which is very slow for a large amount of lines. Try indenting 20000 lines.
        This is a custom indentation function that indents all lines in one operation.
        """
        #Check QScintilla's tab width
        if self.tabWidth() != data.tab_width:
            self.setTabWidth(data.tab_width)
        #Indent according to selection
        selection = self.getSelection()
        if selection == (-1, -1, -1, -1):
            line_number, position = self.getCursorPosition()
            #Adjust index to the line list indexing
            line_number += 1
            line_text = self.line_list[line_number]
            #Check if there is no text before the cursor position in the current line
            if line_text[:position].strip() == "":
                for i, ch in enumerate(line_text):
                    #Find the first none space character
                    if ch != " ":
                        diff = (data.tab_width - (i % data.tab_width))
                        adding_text = diff * " "
                        new_line = adding_text + line_text
                        self.line_list[line_number] = new_line
                        self.setCursorPosition(line_number-1, i+diff)
                        break
                else:
                    #No text in the current line
                    diff = (data.tab_width - (position % data.tab_width))
                    adding_text = diff * " "
                    new_line = line_text[:position] + adding_text + line_text[position:]
                    self.line_list[line_number] = new_line
                    self.setCursorPosition(line_number-1, len(new_line))
            else:
                #There is text before the cursor
                diff = (data.tab_width - (position % data.tab_width))
                adding_text = diff * " "
                new_line = line_text[:position] + adding_text + line_text[position:]
                self.line_list[line_number] = new_line
                self.setCursorPosition(line_number-1, position+diff)
        else:
            #MULTILINE INDENT
            selected_line = self.getCursorPosition()[0]
            #Adjust the 'from' and 'to' indexes to the line list indexing
            line_from = selection[0]+1
            line_to = selection[2]+1
            #This part is to mimic the default indent functionality of Scintilla
            if selection[3] == 0:
                line_to = selection[2]
            #Get the selected line list
            lines = self.line_list[line_from:line_to]
            #Set the indentation width
            indentation_string = data.tab_width * " "
            #Select the indentation function
            if sys.version_info.minor <= 2:
                def nested_indent(line, indent_string):
                    if line.strip() != " ":
                        line = indent_string + line
                    return line
                indent_func = nested_indent
            else:
                indent_func = textwrap.indent
            #Indent the line list in place
            for i, line in enumerate(lines):
                lines[i] = indent_func(line, indentation_string)
            #Set the new line list in one operation
            self.line_list[line_from:line_to] = lines
            #Set the selection again according to which line was selected before the indent
            if selected_line == selection[0]:
                #This part is also to mimic the default indent functionality of Scintilla
                if selection[3] == 0:
                    select_from = selection[2]
                else:
                    select_from = selection[2] + 1
                select_from_length = 0
                select_to = selection[0]
                select_to_length = 0
            else:
                select_from = selection[0]
                select_from_length = 0
                select_to = selection[2]
                #This part is also to mimic the default indent functionality of Scintilla
                if selection[3] == 0:
                    select_to = selection[2]
                else:
                    select_to = selection[2] + 1
                select_to_length = 0
            self.setSelection(
                select_from, 
                select_from_length, 
                select_to, 
                select_to_length
            )
    
    def custom_unindent(self):
        """
        Scintila unindents line-by-line, which is very slow for a large amount of lines. Try unindenting 20000 lines.
        This is a custom unindentation function that unindents all lines in one operation.
        """
        #Check QScintilla's tab width
        if self.tabWidth() != data.tab_width:
            self.setTabWidth(data.tab_width)
        #Unindent according to selection
        selection = self.getSelection()
        if selection == (-1, -1, -1, -1):
            line_number, position = self.getCursorPosition()
            #Adjust index to the line list indexing
            line_number += 1
            line_text = self.line_list[line_number]
            if line_text == "":
                return
            elif line_text.strip() == "":
                #The line contains only spaces
                diff = len(line_text) % data.tab_width
                if diff == 0:
                    diff = data.tab_width
                new_length = len(line_text) - diff
                self.line_list[line_number] = self.line_list[line_number][:new_length]
                self.setCursorPosition(line_number-1, new_length)
            else:
                if line_text[0] != " ":
                    #Do not indent, just move the cursor back
                    if position == 0:
                        return
                    diff = position % data.tab_width
                    if diff == 0:
                        diff = data.tab_width
                    self.setCursorPosition(line_number-1, position-diff)
                elif line_text[:position].strip() == "":
                    #The line has spaces in the beginning
                    for i, ch in enumerate(line_text):
                        if ch != " ":
                            diff = i % data.tab_width
                            if diff == 0:
                                diff = data.tab_width
                            self.line_list[line_number] = self.line_list[line_number][diff:]
                            self.setCursorPosition(line_number-1, i-diff)
                            break
                else:
                    #Move the cursor to the first none space character then repeat above code
                    diff = position % data.tab_width
                    if diff == 0:
                        diff = data.tab_width
                    self.setCursorPosition(line_number-1, position-diff)
        else:
            #MULTILINE UNINDENT
            selected_line = self.getCursorPosition()[0]
            #Adjust the 'from' and 'to' indexes to the line list indexing
            line_from = selection[0]+1
            line_to = selection[2]+1
            #This part is to mimic the default indent functionality of Scintilla
            if selection[3] == 0:
                line_to = selection[2]
            #Get the selected line list
            lines = self.line_list[line_from:line_to]
            #Unindent the line list in place
            for i in range(0, len(lines)):
                for j in range(0, data.tab_width):
                    if lines[i].startswith(" "):
                        lines[i] = lines[i].replace(" ", "", 1)
            #Set the new line list in one operation
            self.line_list[line_from:line_to] = lines
            #Set the selection again according to which line was selected before the indent
            if selected_line == selection[0]:
                #This part is also to mimic the default indent functionality of Scintilla
                if selection[3] == 0:
                    select_from = selection[2]
                else:
                    select_from = selection[2] + 1
                select_from_length = 0
                select_to = selection[0]
                select_to_length = 0
            else:
                select_from = selection[0]
                select_to = selection[2]
                select_from_length = 0
                #This part is also to mimic the default indent functionality of Scintilla
                if selection[3] == 0:
                    select_to = selection[2]
                else:
                    select_to = selection[2] + 1
                select_to_length = 0
            self.setSelection(
                select_from, 
                select_from_length, 
                select_to, 
                select_to_length
            )
    
    def text_to_list(self, input_text):
        """Split the input text into a list of lines according to the document EOL delimiter"""
        out_list = []
        if self.eolMode() == data.PyQt.Qsci.QsciScintilla.EolUnix:
            out_list = input_text.split("\n")
        elif self.eolMode() == data.PyQt.Qsci.QsciScintilla.EolWindows:
            out_list = input_text.split("\r\n")
        elif self.eolMode() == data.PyQt.Qsci.QsciScintilla.EolMac:
            out_list = input_text.split("\r")
        return out_list
    
    def list_to_text(self, line_list):
        """Convert a list of lines to one string according to the document EOL delimiter"""
        out_text = ""
        if self.eolMode() == data.PyQt.Qsci.QsciScintilla.EolUnix:
            out_text = "\n".join(line_list)
        elif self.eolMode() == data.PyQt.Qsci.QsciScintilla.EolWindows:
            out_text = "\r\n".join(line_list)
        elif self.eolMode() == data.PyQt.Qsci.QsciScintilla.EolMac:
            out_text = "\r".join(line_list)
        return out_text

    def toggle_comment_uncomment(self):
        """Toggle commenting for the selected lines"""
        #Check if the document is a valid programming language
        if self.current_file_type == "TEXT" or self.current_file_type == None:
            return
        #Test if there is no selected text
        if (self.getSelection() == (-1, -1, -1, -1) or
            self.getSelection()[0] == self.getSelection()[2]):
            #No selected text
            line_number = self.getCursorPosition()[0] + 1
            line_text   = self.get_line(line_number)
            #Un/comment only the current line (no arguments un/comments current line)
            if line_text.lstrip().startswith(self.comment_string):
                self.uncomment_line()
            else:
                self.comment_line()
        else:
            #Text is selected 
            start_line_number   = self.getSelection()[0] + 1
            first_selected_chars = self.selectedText()[0:len(self.comment_string)]
            end_line_number     = self.getSelection()[2] + 1
            #Choose un/commenting according to the first line in selection
            if first_selected_chars == self.comment_string:
                self.uncomment_lines(start_line_number, end_line_number)
            else:
                self.comment_lines(start_line_number, end_line_number)
    
    def for_each_line(self, in_func):
        """Apply function 'in_func' to lines"""
        #Check that in_func is really a function
        if callable(in_func) == False:
            self.main_form.display.repl_display_message(
                "'for_each_line' argument has to be a function!", 
                message_type=data.MessageType.ERROR
            )
            return
        #Check there is only one argument
        arguments = inspect.getargspec(in_func).args
        if len(arguments) != 1:
            self.main_form.display.repl_display_message(
                "'for_each_line' function has to have only one argument!", 
                message_type=data.MessageType.ERROR
            )
            return
        #
        if (self.getSelection() == (-1, -1, -1, -1) or
            self.getSelection()[0] == self.getSelection()[2]):
            #No selected text, apply function to the every line
            try:
                new_line_list = []
                for line in self.line_list:
                    new_line = in_func(line)
                    new_line_list.append(new_line)
                #Assign the new list over the old one
                self.line_list = new_line_list
            except Exception as ex:
                self.main_form.display.repl_display_message(
                    "'for_each_line' has an error:\n" + str(ex), 
                    message_type=data.MessageType.ERROR
                )
                return
        else:
            #Selected text, apply function to the selected lines only
            try:
                #Get the starting and end line
                start_line_number   = self.getSelection()[0] + 1
                end_line_number     = self.getSelection()[2] + 1
                #Apply the function to the lines
                new_line_list = []
                for line in self.line_list[start_line_number:end_line_number]:
                    new_line = in_func(line)
                    new_line_list.append(new_line)
                #Assign the new list over the old one
                self.line_list[start_line_number:end_line_number] = new_line_list
            except Exception as ex:
                self.main_form.display.repl_display_message(
                    "'for_each_line' has an error:\n" + str(ex), 
                    message_type=data.MessageType.ERROR
                )
                return
    
    def remove_empty_lines(self):
        new_line_list = []
        for line in self.line_list:
            if line.strip() != "":
                new_line_list.append(line)
        #Assign the new list over the old one
        self.line_list = new_line_list

    """
    Search and replace functions
    """
    def find_text(self, 
                  search_text, 
                  case_sensitive=False, 
                  search_forward=True, 
                  regular_expression=False):
        """
        (SAME AS THE QSciScintilla.find, BUT THIS RETURNS A RESULT)
        Function to find an occurance of text in the current tab of a basic widget:
            - Python reguler expressions are used, not the Scintilla built in ones
            - function executes cyclically over the scintilla document, when it reaches the end of the document
            ! THERE IS A BUG WHEN SEARCHING FOR UNICODE STRINGS, THESE ARE ALWAYS CASE SENSITIVE
        """
        def focus_entire_found_text():
            """
            Nested function for selection the entire found text
            """
            # Save the currently found text selection attributes
            position = self.getSelection()
            # Set the cursor to the beginning of the line, so that in case the
            # found string index is behind the previous cursor index, the whole
            # found text is shown!
            self.setCursorPosition(position[0], 0)
            self.setSelection(position[0], position[1], position[2], position[3])
        # Set focus to the tab that will be searched
        self.parent.setCurrentWidget(self)
        if regular_expression == True:
            # Get the absolute cursor index from line/index position
            line, index = self.getCursorPosition()
            absolute_position = self.positionFromLineIndex(line, index)
            # Compile the search expression according to the case sensitivity
            if case_sensitive == True:
                compiled_search_re = re.compile(search_text)
            else:
                compiled_search_re = re.compile(search_text, re.IGNORECASE)
            # Search based on the search direction
            if search_forward == True:
                # Regex search from the absolute position to the end for the search expression
                search_result = re.search(compiled_search_re, self.text()[absolute_position:])
                if search_result != None:
                    #Select the found expression
                    result_start    = absolute_position + search_result.start()
                    result_end      = result_start + len(search_result.group(0))
                    self.setCursorPosition(0, result_start)
                    self.setSelection(0, result_start, 0, result_end)
                    # Return successful find
                    return data.SearchResult.FOUND
                else:
                    # Begin a new search from the top of the document
                    search_result = re.search(compiled_search_re, self.text())
                    if search_result != None:
                        # Select the found expression
                        result_start    = search_result.start()
                        result_end      = result_start + len(search_result.group(0))
                        self.setCursorPosition(0, result_start)
                        self.setSelection(0, result_start, 0, result_end)
                        self.main_form.display.write_to_statusbar("Reached end of document, started from the top again!")
                        # Return cycled find
                        return data.SearchResult.CYCLED
                    else:
                        self.main_form.display.write_to_statusbar("Text was not found!")
                        return data.SearchResult.NOT_FOUND
            else:
                # Move the cursor one character back when searching backard
                # to not catch the same search result again
                cursor_position = self.get_absolute_cursor_position()
                search_text = self.text()[:cursor_position]
                # Regex search from the absolute position to the end for the search expression
                search_result = [m for m in re.finditer(compiled_search_re, search_text)]
                if search_result != []:
                    #Select the found expression
                    result_start    = search_result[-1].start()
                    result_end      = search_result[-1].end()
                    self.setCursorPosition(0, result_start)
                    self.setSelection(0, result_start, 0, result_end)
                    # Return successful find
                    return data.SearchResult.FOUND
                else:
                    # Begin a new search from the top of the document
                    search_result = [m for m in re.finditer(compiled_search_re, self.text())]
                    if search_result != []:
                        # Select the found expression
                        result_start    = search_result[-1].start()
                        result_end      = search_result[-1].end()
                        self.setCursorPosition(0, result_start)
                        self.setSelection(0, result_start, 0, result_end)
                        self.main_form.display.write_to_statusbar("Reached end of document, started from the top again!")
                        # Return cycled find
                        return data.SearchResult.CYCLED
                    else:
                        self.main_form.display.write_to_statusbar("Text was not found!")
                        return data.SearchResult.NOT_FOUND
        else:
            # Move the cursor one character back when searching backard
            # to not catch the same search result again
            if search_forward == False:
                line, index = self.getCursorPosition()
                self.setCursorPosition(line, index-1)
            # "findFirst" is the QScintilla function for finding text in a document
            search_result = self.findFirst(search_text, 
                False, 
                case_sensitive, 
                False, 
                False, 
                forward=search_forward
            )
            if search_result == False:
                # Try to find text again from the top or at the bottom of 
                # the scintilla document, depending on the search direction
                if search_forward == True:
                    s_line = 0
                    s_index = 0
                else:
                    s_line = len(self.line_list)-1
                    s_index = len(self.text())
                inner_result = self.findFirst(
                    search_text, 
                    False, 
                    case_sensitive, 
                    False, 
                    False, 
                    forward=search_forward, 
                    line=s_line, 
                    index=s_index
                )
                if inner_result == False:
                    self.main_form.display.write_to_statusbar("Text was not found!")
                    return data.SearchResult.NOT_FOUND
                else:
                    self.main_form.display.write_to_statusbar("Reached end of document, started from the other end again!")
                    focus_entire_found_text()
                    # Return cycled find
                    return data.SearchResult.CYCLED
            else:
                # Found text
                self.main_form.display.write_to_statusbar("Found text: \"" + search_text + "\"")
                focus_entire_found_text()
                # Return successful find
                return data.SearchResult.FOUND
    
    def find_all(self,
                 search_text, 
                 case_sensitive=False, 
                 regular_expression=False, 
                 text_to_bytes=False):
        """Find all instances of a string and return a list of (line, index_start, index_end)"""
        #Find all instances of the search string and return the list
        matches = functions.index_strings_in_text(
            search_text, 
            self.text(), 
            case_sensitive, 
            regular_expression, 
            text_to_bytes
        )
        return matches
    
    def find_and_replace(self, 
                         search_text, 
                         replace_text, 
                         case_sensitive=False, 
                         search_forward=True, 
                         regular_expression=False):
        """Find next instance of the search string and replace it with the replace string"""
        if regular_expression == True:
            #Check if expression exists in the document
            search_result = self.find_text(
                search_text, case_sensitive, search_forward, regular_expression
            )
            if search_result != data.SearchResult.NOT_FOUND:
                if case_sensitive == True:
                    compiled_search_re = re.compile(search_text)
                else:
                    compiled_search_re = re.compile(search_text, re.IGNORECASE)
                #The search expression is already selected from the find_text function
                found_expression = self.selectedText()
                #Save the found selected text line/index information
                saved_selection = self.getSelection()
                #Replace the search expression with the replace expression
                replacement = re.sub(compiled_search_re, replace_text, found_expression)
                #Replace selected text with replace text
                self.replaceSelectedText(replacement)
                #Select the newly replaced text
                self.main_form.display.repl_display_message(replacement)
                self.setSelection(
                    saved_selection[0], 
                    saved_selection[1], 
                    saved_selection[2], 
                    saved_selection[1]+len(replacement)
                )
                return True
            else:
                #Search text not found
                self.main_form.display.write_to_statusbar("Text was not found!")
                return False
        else:
            #Check if string exists in the document
            search_result = self.find_text(search_text, case_sensitive)
            if search_result != data.SearchResult.NOT_FOUND:
                #Save the found selected text line/index information
                saved_selection = self.getSelection()
                #Replace selected text with replace text
                self.replaceSelectedText(replace_text)
                #Select the newly replaced text
                self.setSelection(
                    saved_selection[0], 
                    saved_selection[1], 
                    saved_selection[2], 
                    saved_selection[1]+len(replace_text)
                )
                return True
            else:
                #Search text not found
                self.main_form.display.write_to_statusbar("Text was not found!")
                return False
    
    def replace_all(self,
                    search_text, 
                    replace_text, 
                    case_sensitive=False,
                    regular_expression=False):
        """Replace all occurences of a string in a scintilla document"""
        #Store the current cursor position
        current_position = self.getCursorPosition()
        #Move cursor to the top of the document, so all the search string instances will be found
        self.setCursorPosition(0, 0)
        #Clear all previous highlights
        self.clear_highlights()
        #Setup the indicator style, the replace indicator is 1
        self.set_indicator_replace()
        #Correct the displayed file name
        if self.save_name == None or self.save_name == "":
            file_name = self.parent.tabText(self.parent.currentIndex())
        else:
            file_name = os.path.basename(self.save_name)
        #Check if there are any instances of the search text in the document
        #based on the regular expression flag
        search_result = None
        if regular_expression == True:
            #Check case sensitivity for regular expression
            if case_sensitive == True:
                compiled_search_re = re.compile(search_text)
            else:
                compiled_search_re = re.compile(search_text, re.IGNORECASE)
            search_result = re.search(compiled_search_re, self.text())
        else:
            search_result = self.find_text(search_text, case_sensitive)
        if search_result == data.SearchResult.NOT_FOUND:
            message = "No matches were found in '{:s}'!".format(file_name)
            self.main_form.display.repl_display_message(
                message, 
                message_type=data.MessageType.WARNING
            )
            return
        #Use the re module to replace the text
        text = self.text()
        matches, replaced_text  =   functions.replace_and_index(
                                        text, 
                                        search_text, 
                                        replace_text, 
                                        case_sensitive, 
                                        regular_expression, 
                                    )
        #Check if there were any matches or
        #if the search and replace text were equivalent!
        if matches != None:
            #Replace the text
            self.replace_entire_text(replaced_text)
            #Matches can only be displayed for non-regex functionality
            if regular_expression == True:
                #Build the list of matches used by the highlight_raw function
                corrected_matches = []
                for i in matches:
                    index = self.positionFromLineIndex(i, 0)
                    corrected_matches.append(
                        (
                            0, 
                            index, 
                            0, 
                            index+len(self.text(i)), 
                        )
                    )
                #Display the replacements in the REPL tab
                if len(corrected_matches) < data.MAXIMUM_HIGHLIGHTS:
                    message = "{:s} replacements:".format(file_name)
                    self.main_form.display.repl_display_message(
                        message, 
                        message_type=data.MessageType.SUCCESS
                    )
                    for match in corrected_matches:
                        line    = self.lineIndexFromPosition(match[1])[0] + 1
                        index   = self.lineIndexFromPosition(match[1])[1]
                        message = "    replacement made in line:{:d}".format(line)
                        self.main_form.display.repl_display_message(
                            message, 
                            message_type=data.MessageType.SUCCESS
                        )
                else:
                    message = "{:d} replacements made in {:s}!\n".format(
                                                                    len(corrected_matches), 
                                                                    file_name
                                                                )
                    message += "Too many to list individually!"
                    self.main_form.display.repl_display_message(
                        message, 
                        message_type=data.MessageType.WARNING
                    )
                #Highlight and display the line difference between the old and new texts
                self.highlight_raw(corrected_matches)
            else:
                #Display the replacements in the REPL tab
                if len(matches) < data.MAXIMUM_HIGHLIGHTS:
                    message = "{:s} replacements:".format(file_name)
                    self.main_form.display.repl_display_message(
                        message, 
                        message_type=data.MessageType.SUCCESS
                    )
                    for match in matches:
                        line    = self.lineIndexFromPosition(match[1])[0] + 1
                        index   = self.lineIndexFromPosition(match[1])[1]
                        message = "    replaced \"{:s}\" in line:{:d} column:{:d}".format(
                                                                                search_text, 
                                                                                line, 
                                                                                index
                                                                            )
                        self.main_form.display.repl_display_message(
                            message, 
                            message_type=data.MessageType.SUCCESS
                        )
                else:
                    message = "{:d} replacements made in {:s}!\n".format(
                                                                    len(matches), 
                                                                    file_name
                                                                )
                    message += "Too many to list individually!"
                    self.main_form.display.repl_display_message(
                        message, 
                        message_type=data.MessageType.WARNING
                    )
                #Highlight and display the replaced text
                self.highlight_raw(matches)
            #Restore the previous cursor position
            self.setCursorPosition(current_position[0], current_position[1])
        else:
            message = "The search string and replace string are equivalent!\n"
            message += "Change the search/replace string or change the case sensitivity!"
            self.main_form.display.repl_display_message(
                message,
                message_type=data.MessageType.ERROR
            )
    
    def replace_in_selection(self, 
                             search_text, 
                             replace_text, 
                             case_sensitive=False, 
                             regular_expression=False):
        """Replace all occurences of a string in the current selection in the scintilla document"""
        #Get the start and end point of the selected text
        start_line, start_index,  end_line, end_index = self.getSelection()
        #Get the currently selected text and use the re module to replace the text
        selected_text   = self.selectedText()
        replaced_text   = functions.regex_replace_text(
                              selected_text, 
                              search_text, 
                              replace_text, 
                              case_sensitive, 
                              regular_expression
                        )
        #Check if any replacements were made
        if replaced_text != selected_text:
            #Put the text back into the selection space and select it again
            self.replaceSelectedText(replaced_text)
            new_end_line = start_line
            new_end_index = start_index + len(bytearray(replaced_text, "utf-8"))
            self.setSelection(start_line, start_index, new_end_line, new_end_index)
        else:
            message = "No replacements were made!"
            self.main_form.display.repl_display_message(
                message,
                message_type=data.MessageType.WARNING
            )    
    
    def replace_entire_text(self, new_text):
        """Replace the entire text of the document"""
        #Select the entire text
        self.selectAll(True)
        #Replace the text with the new
        self.replaceSelectedText(new_text)
    
    def convert_case(self, uppercase=False):
        """Convert selected text in the scintilla document into the selected case letters"""
        #Get the start and end point of the selected text
        start_line, start_index,  end_line, end_index = self.getSelection()
        #Get the currently selected text
        selected_text   = self.selectedText()
        #Convert it to the selected case
        if uppercase == False:
            selected_text   = selected_text.lower()
        else:
            selected_text   = selected_text.upper()
        #Replace the selection with the new upercase text
        self.replaceSelectedText(selected_text)
        #Reselect the previously selected text
        self.setSelection(start_line, start_index,  end_line, end_index)
    
    
    """
    Highligting functions
    """
    def highlight_text(self, 
                       highlight_text, 
                       case_sensitive=False, 
                       regular_expression=False):
        """
        Highlight all instances of the selected text with a selected colour
        """
        #Setup the indicator style, the highlight indicator will be 0
        self.set_indicator_highlight()
        #Get all instances of the text using list comprehension and the re module
        matches = self.find_all(
                      highlight_text, 
                      case_sensitive, 
                      regular_expression, 
                      text_to_bytes=True
                  )
        #Check if the match list is empty
        if matches:
            #Use the raw highlight function to set the highlight indicators
            self.highlight_raw(matches)
            self.main_form.display.repl_display_message(
                "{:d} matches highlighted".format(len(matches)) 
            )
            #Set the cursor to the first highlight
            self.find_text(highlight_text, case_sensitive, True, regular_expression)
        else:
            self.main_form.display.repl_display_message(
                "No matches found!",
                message_type=data.MessageType.WARNING
            )
    
    def highlight_raw(self, highlight_list):
        """
        Core highlight function that uses Scintilla messages to style indicators.
        QScintilla's fillIndicatorRange function is to slow for large numbers of
        highlights!
        INFO:   This is done using the scintilla "INDICATORS" described in the official
                scintilla API (http://www.scintilla.org/ScintillaDoc.html#Indicators)
        """
        scintilla_command = data.PyQt.Qsci.QsciScintillaBase.SCI_INDICATORFILLRANGE
        for highlight in highlight_list:
            start   = highlight[1]
            length  = highlight[3] - highlight[1]
            self.SendScintilla(
                scintilla_command, 
                start, 
                length
            )
    
    def clear_highlights(self):
        """Clear all highlighted text"""
        #Clear the highlight indicators
        self.clearIndicatorRange(
            0, 
            0, 
            self.lines(), 
            self.lineLength(self.lines()-1), 
            self.HIGHLIGHT_INDICATOR
        )
        #Clear the replace indicators
        self.clearIndicatorRange(
            0, 
            0, 
            self.lines(), 
            self.lineLength(self.lines()-1), 
            self.REPLACE_INDICATOR
        )
        #Clear the find indicators
        self.clearIndicatorRange(
            0, 
            0, 
            self.lines(), 
            self.lineLength(self.lines()-1), 
            self.FIND_INDICATOR
        )
    
    def _set_indicator(self,
                       indicator, 
                       fore_color):
        """Set the indicator settings"""
        self.indicatorDefine(
            data.PyQt.Qsci.QsciScintillaBase.INDIC_ROUNDBOX,
            indicator
        )
        self.setIndicatorForegroundColor(
            fore_color, 
            indicator
        )
        self.SendScintilla(
            data.PyQt.Qsci.QsciScintillaBase.SCI_SETINDICATORCURRENT, 
            indicator
        )

    def set_indicator_highlight(self):
        """Set the appearance of the highlight indicator (the default indicator is 0)"""
        self._set_indicator(
            self.HIGHLIGHT_INDICATOR, 
            data.PyQt.QtGui.QColor(0, 255, 0, 80)
        )

    def set_indicator_replace(self):
        """Set the appearance of the highlight indicator"""
        self._set_indicator(
            self.REPLACE_INDICATOR, 
            data.PyQt.QtGui.QColor(50, 180, 255, 80)
        )

    def set_indicator_find(self):
        """Set the appearance of the highlight indicator"""
        self._set_indicator(
            self.FIND_INDICATOR, 
            data.PyQt.QtGui.QColor(255, 180, 50, 100)
        )


    """
    Various CustomEditor functions
    """
    def check_line_numbering(self, line_number):
        """
        Check if the line number is in the bounds of the current document
        and return the filtered line number
        """
        #Convert the line numbering from the displayed 1-to-n to the array numbering of python 0-to-n
        line_number -= 1
        #Check if the line number is below the index 0
        if line_number < 0:
            line_number = 0
        elif line_number > self.lines()-1:
            line_number = self.lines()-1
        return line_number
    
    def save_document(self, saveas=False, last_dir=None, encoding="utf-8", line_ending=None):
        """Save a document to a file"""
        if self.save_name == "" or saveas != False:
            #Tab has an empty directory attribute or "SaveAs" was invoked, select file using the QfileDialog
            file_dialog = data.QFileDialog
            #Check if the custom editors last browsed dir was previously set
            if self.last_browsed_dir == "" and last_dir != None:
                self.last_browsed_dir = last_dir
            #Get the filename from the QfileDialog window
            temp_save_name = file_dialog.getSaveFileName(
                self, 
                "Save File", 
                self.last_browsed_dir + self.save_name, 
                "All Files(*)"
            )
            if data.PYQT_MODE == 5:
                # PyQt5's getOpenFileNames returns a tuple (files_list, selected_filter),
                # so pass only the files to the function
                temp_save_name = temp_save_name[0]
            #Check if the user has selected a file
            if temp_save_name == "":
                return
            #Replace back-slashes to forward-slashes on Windows
            if platform.system() == "Windows":
                temp_save_name = temp_save_name.replace("\\", "/")
            #Save the chosen file name to the document "save_name" attribute
            self.save_name = temp_save_name
        #Update the last browsed directory to the class/instance variable
        self.last_browsed_dir = os.path.dirname(self.save_name)
        #Set the tab name by filtering it out from the QFileDialog result
        self.name = os.path.basename(self.save_name)
        #Change the displayed name of the tab in the basic widget
        self.parent.set_tab_name(self, self.name)
        #Check if a line ending was specified
        if line_ending == None:
            #Write contents of the tab into the specified file
            save_result = functions.write_to_file(self.text(), self.save_name, encoding)
        else:
            #The line ending has to be a string
            if isinstance(line_ending, str) == False:
                self.main_form.display.repl_display_message(
                    "Line ending has to be a string!", 
                    message_type=data.MessageType.ERROR
                )
                return
            else:
                #Convert the text into a list and join it together with the specified line ending
                text_list = self.line_list
                converted_text = line_ending.join(text_list)
                save_result = functions.write_to_file(converted_text, self.save_name, encoding)
        #Check result of the functions.write_to_file function
        if save_result == True:
            #Saving has succeded
            self.parent.reset_text_changed(self.parent.indexOf(self))
            #Update the lexer for the document
            file_type = functions.get_file_type(self.save_name)
            self.choose_lexer(file_type)
            #Update the settings manipulator with the new file
            self.main_form.settings.update_recent_list(self.save_name)
        else:
            #Saving has failed
            error_message = "Error while trying to write file to disk:\n"
            error_message += str(save_result)
            self.main_form.display.repl_display_message(
                error_message, 
                message_type=data.MessageType.ERROR
            )
            self.main_form.display.write_to_statusbar(
                "Saving to file failed, check path and disk space!"
            )
    
    def refresh_lexer(self):
        """ Refresh the current lexer (used by themes) """
        self.set_theme(data.theme)
        self.lexer().set_theme(data.theme)
    
    def choose_lexer(self, file_type):
        """Choose the lexer from the file type parameter for the scintilla document"""
        #Set the lexer for syntax highlighting according to file type
        lexer = None
        if file_type    == "python":
            lexer   = lexers.Python()
            self.comment_string = "#"
        elif file_type  == "cython":
            lexer   = lexers.Cython()
            self.comment_string = "#"
        elif file_type  == "c":
            lexer   = lexers.CPP()
            self.comment_string = "//"
        elif file_type  == "c++":
            lexer   = lexers.CPP()
            self.comment_string = "//"
        elif file_type  == "pascal":
            lexer   = lexers.Pascal()
            self.comment_string = "//"
        elif file_type  == "oberon/modula":
            lexer   = lexers.Oberon()
            self.oberon_comment_style = True
            self.comment_string     = "(*"
            self.end_comment_string = "*)"
        elif file_type  == "ada":
            lexer   = lexers.Ada()
            self.comment_string = "--"
        elif file_type  == "d":
            lexer   = lexers.D()
            self.comment_string = "//"
        elif file_type  == "nim":
            lexer   = lexers.Nim()
            self.comment_string = "#"
        elif file_type  == "makefile":
            lexer   = lexers.Makefile()
            self.comment_string = "#"
        elif file_type  == "xml":
            lexer   = lexers.XML()
            self.comment_string = None
        elif file_type  == "batch":
            lexer   = lexers.Batch()
            self.comment_string = "::"
        elif file_type  == "bash":
            lexer   = lexers.Bash()
            self.comment_string = "#"
        elif file_type  == "lua":
            lexer   = lexers.Lua()
            self.comment_string = "--"
        elif file_type  == "coffeescript":
            if data.compatibility_mode == False:
                lexer = lexers.CoffeeScript()
                self.comment_string = "#"
            else:
                lexer = lexers.Text()
                self.comment_string = None
        elif file_type  == "c#":
            lexer   = lexers.CPP()
            self.comment_string = "//"
        elif file_type  == "java":
            lexer   = lexers.Java()
            self.comment_string = "//"
        elif file_type  == "javascript":
            lexer   = lexers.JavaScript()
            self.comment_string = "//"
        elif file_type  == "octave":
            lexer   = lexers.Octave()
            self.comment_string = "#"
        elif file_type  == "routeros":
            lexer   = lexers.RouterOS()
            self.comment_string = "#"
        elif file_type  == "sql":
            lexer   = lexers.SQL()
            self.comment_string = "#"
        elif file_type  == "postscript":
            lexer   = lexers.PostScript()
            self.comment_string = "%"
        elif file_type  == "fortran":
            lexer   = lexers.Fortran()
            self.comment_string = "c "
        elif file_type  == "fortran77":
            lexer   = lexers.Fortran77()
            self.comment_string = "c "
        elif file_type  == "idl":
            lexer   = lexers.IDL()
            self.comment_string = "//"
        elif file_type  == "ruby":
            lexer   = lexers.Ruby()
            self.comment_string = "#"
        elif file_type  == "html":
            lexer   = lexers.HTML()
            self.oberon_comment_style = True
            self.comment_string     = "<!--"
            self.end_comment_string = "-->"
        elif file_type  == "css":
            lexer   = lexers.CSS()
            self.oberon_comment_style = True
            self.comment_string     = "/*"
            self.end_comment_string = "*/"
        else:
            #No lexer was chosen, set file type to text and lexer to plain text
            self.current_file_type = "TEXT"
            lexer = lexers.Text()
            self.comment_string = None
        #Check if a lexer was chosen
        if lexer != None:
            self.set_lexer(lexer, file_type)
        else:
            self.main_form.display.repl_display_message(
                "Error while setting the lexer!",
                message_type=data.MessageType.ERROR
            )
    
    def clear_lexer(self):
        """Remove the lexer from the editor"""
        if self.lexer() != None:
            self.lexer().deleteLater()
            self.lexer().setParent(None)
            self.setLexer(None)
    
    def set_lexer(self, lexer, file_type):
        """Function that actually sets the lexer"""
        # First clear the lexer
        self.clear_lexer()
        #Save the current file type to a string
        self.current_file_type = file_type.upper()
        #Set the lexer default font family
        lexer.setDefaultFont(self.default_font)
        #Set the lexer for the current scintilla document
        lexer.setParent(self)
        self.setLexer(lexer)
        #Reset the brace matching color
        self.setMatchedBraceBackgroundColor(self.brace_color)
        #Change the font style of comments so that they are the same as the default scintilla text
        #This is done using the low-level API function "SendScintilla" that is documented here: http://pyqt.sourceforge.net/Docs/QScintilla2/classQsciScintillaBase.html
        #With it you can invoke C functions documented here: http://www.scintilla.org/ScintillaDoc.html
        self.SendScintilla(data.PyQt.Qsci.QsciScintillaBase.SCI_STYLESETFONT, 1, self.default_comment_font)
        #Enable code folding for the file type
        self.setFolding(data.PyQt.Qsci.QsciScintilla.PlainFoldStyle)
        #Set all fonts in the current lexer to the default style
        #and set the keyword styles to bold
        if (isinstance(lexer, lexers.Ada) or
            isinstance(lexer, lexers.Oberon) or
            isinstance(lexer, lexers.Nim)):
            #Set the margin font for the lexers in the lexers.py module
            self.setMarginsFont(lexer.default_font)
        #Get the icon according to the file type
        self.current_icon = helper_forms.get_language_file_icon(file_type)
        #Set the theme
        self.set_theme(data.theme)

    def clear_editor(self):
        """Clear the text from the scintilla document"""
        self.SendScintilla(data.PyQt.Qsci.QsciScintillaBase.SCI_CLEARALL)
    
    def tabs_to_spaces(self):
        """Convert all tab(\t) characters to spaces"""
        spaces = " " * data.tab_width
        self.setText(self.text().replace("\t", spaces))

    def undo_all(self):
        """Repeat undo until there is something to undo"""
        while self.isUndoAvailable() == True:
            self.undo()

    def redo_all(self):
        """Repeat redo until there is something to redo"""
        while self.isRedoAvailable() == True:
            self.redo()
    
    def update_margin(self):
        """Update margin width according to the number of lines in the document"""
        line_count  = self.lines()
        #Set margin width
        self.setMarginWidth(0, str(line_count) + "0")

    def edge_marker_show(self):
        """Show the marker at the specified column number"""
        #Set the marker color to blue
        marker_color = data.PyQt.QtGui.QColor(180, 180, 180, alpha=255)
        #Set the column number where the marker will be shown
        marker_column = data.EDGE_MARKER_COLUMN 
        #Set the marker options
        self.setEdgeColor(marker_color)
        self.setEdgeColumn(marker_column)
        self.setEdgeMode(data.PyQt.Qsci.QsciScintilla.EdgeLine)

    def edge_marker_hide(self):
        """Hide the column marker"""
        self.setEdgeMode(data.PyQt.Qsci.QsciScintilla.EdgeNone)
    
    def edge_marker_toggle(self):
        """Toggle edge marker display"""
        if self.edge_marker_state == False:
            self.edge_marker_show()
            self.edge_marker_state =True
        else:
            self.edge_marker_hide()
            self.edge_marker_state =False
    
    def reload_file(self):
        """Reload current document from disk"""
        #Check if file was loaded from or saved to disk
        if self.save_name == "":
            self.main_form.display.write_to_statusbar("Document has no file on disk!", 3000)
            return
        #Check the file status
        if self.save_status == data.FileStatus.MODIFIED:
            #Close the log window if it is displayed
            self.main_form.view.set_log_window(False)
            #Display the close notification
            reload_message = "Document '" + self.name+ "' has been modified!\nReload it from disk anyway?"
            reply = data.QMessageBox.question(
                self, 
                'Reloding Tab', 
                reload_message,
                data.QMessageBox.Yes,
                data.QMessageBox.No
            )
            if reply == data.QMessageBox.No:
                #Cancel tab file reloading
                return
        #Check if the name of the document is valid
        if self.name == "" or self.name == None:
            return
        #Open the file and read the contents
        try:
            disk_file_text = functions.read_file_to_string(self.save_name)
        except:
            self.main_form.display.write_to_statusbar("Error reloading file!", 3000)
            return
        #Save the current cursor position
        temp_position = self.getCursorPosition()
        #Reload the file
        self.replace_entire_text(disk_file_text)
        #Restore saved cursor position
        self.setCursorPosition(temp_position[0], temp_position[1])
    
    def copy_self(self, new_editor):
        """Copy everything needed from self to the destination editor"""
        if new_editor == None:
            return
        new_editor.setLexer(self.lexer())
        new_editor.setText(self.text())
    
    def toggle_wordwrap(self):
        """ 
        Toggle word wrap on/off.
        Wrap modes:
            data.PyQt.Qsci.QsciScintilla.WrapNone - Lines are not wrapped.
            data.PyQt.Qsci.QsciScintilla.WrapWord - Lines are wrapped at word boundaries.
            data.PyQt.Qsci.QsciScintilla.WrapCharacter - Lines are wrapped at character boundaries.
            data.PyQt.Qsci.QsciScintilla.WrapWhitespace - Lines are wrapped at whitespace boundaries. 
        Wrap visual flags:
            data.PyQt.Qsci.QsciScintilla.WrapFlagNone - No wrap flag is displayed.
            data.PyQt.Qsci.QsciScintilla.WrapFlagByText - A wrap flag is displayed by the text.
            data.PyQt.Qsci.QsciScintilla.WrapFlagByBorder - A wrap flag is displayed by the border.
            data.PyQt.Qsci.QsciScintilla.WrapFlagInMargin - A wrap flag is displayed in the line number margin. 
        Wrap indentation:
            data.PyQt.Qsci.QsciScintilla.WrapIndentFixed - Wrapped sub-lines are indented by the amount set by setWrapVisualFlags().
            data.PyQt.Qsci.QsciScintilla.WrapIndentSame - Wrapped sub-lines are indented by the same amount as the first sub-line.
            data.PyQt.Qsci.QsciScintilla.WrapIndentIndented - Wrapped sub-lines are indented by the same amount as the first sub-line plus one more level of indentation. 
        """
        if self.wrapMode() == data.PyQt.Qsci.QsciScintilla.WrapNone:
            self.setWrapMode(data.PyQt.Qsci.QsciScintilla.WrapWord)
            self.setWrapVisualFlags(data.PyQt.Qsci.QsciScintilla.WrapFlagByText)
            self.setWrapIndentMode(data.PyQt.Qsci.QsciScintilla.WrapIndentSame)
            self.main_form.display.repl_display_message(
                "Line wrapping ON", 
                message_type=data.MessageType.WARNING
            )
        else:
            self.setWrapMode(data.PyQt.Qsci.QsciScintilla.WrapNone)
            self.setWrapVisualFlags(data.PyQt.Qsci.QsciScintilla.WrapFlagNone)
            self.main_form.display.repl_display_message(
                "Line wrapping OFF", 
                message_type=data.MessageType.WARNING
            )
    
    def toggle_line_endings(self):
        """Set the visibility of the End-Of-Line character"""
        if self.eolVisibility() == True:
            self.setEolVisibility(False)
            self.main_form.display.repl_display_message(
                "EOL characters hidden", 
                message_type=data.MessageType.WARNING
            )
        else:
            self.setEolVisibility(True)
            self.main_form.display.repl_display_message(
                "EOL characters shown", 
                message_type=data.MessageType.WARNING
            )
    

    """
    CustomEditor autocompletion functions
    """
    def init_autocompletions(self, new_autocompletions=[]):
        """Set the initial autocompletion functionality for the document"""
        self.disable_autocompletions()
    
    def enable_autocompletions(self, new_autocompletions=[]):
        """Function for enabling the CustomEditor autocompletions"""
        #Set how many characters must be typed for the autocompletion popup to appear
        self.setAutoCompletionThreshold(1)
        #Set the source from where the autocompletions will be fetched
        self.setAutoCompletionSource(data.PyQt.Qsci.QsciScintilla.AcsDocument)
        #Set autocompletion case sensitivity
        self.setAutoCompletionCaseSensitivity(False)
    
    def disable_autocompletions(self):
        """Disable the CustomEditor autocompletions"""
        self.setAutoCompletionSource(data.PyQt.Qsci.QsciScintilla.AcsNone)
    
    def toggle_autocompletions(self):
        """Enable/disable autocompletions for the CustomEditor"""
        #Initilize the document name for displaying
        if self.save_name == None or self.save_name == "":
            document_name = self.parent.tabText(self.parent.currentIndex())
        else:
            document_name = os.path.basename(self.save_name)
        #Check the autocompletion source
        if self.autoCompletionSource() == data.PyQt.Qsci.QsciScintilla.AcsDocument:
            self.disable_autocompletions()
            message = "Autocompletions DISABLED in {:s}".format(document_name)
            self.main_form.display.repl_display_message(
                message, 
                message_type=data.MessageType.WARNING
            )
            self.main_form.display.write_to_statusbar("Autocompletions DISABLED")
        else:
            self.enable_autocompletions()
            message = "Autocompletions ENABLED in {:s}".format(document_name)
            self.main_form.display.repl_display_message(
                message, 
                message_type=data.MessageType.SUCCESS
            )
            self.main_form.display.write_to_statusbar("Autocompletions ENABLED")
    
    class Hotspots:
        """
        Functions for styling text with hotspots
        (namespace/nested class to CustomEditor)
        """
        #Class varibles
        parent = None
        
        def __init__(self, parent):
            """Initialization of the Editing object instance"""
            #Get the reference to the MainWindow parent object instance
            self.parent = parent
        
        def style(self, index_from, length, color=0xff0000):
            """Style the text from/to with a hotspot"""
            send_scintilla = self.parent.SendScintilla
            #Use the scintilla low level messaging system to set the hotspot
            send_scintilla(data.PyQt.Qsci.QsciScintillaBase.SCI_STYLESETHOTSPOT, 2, True)
            send_scintilla(data.PyQt.Qsci.QsciScintillaBase.SCI_SETHOTSPOTACTIVEFORE, True, color)
            send_scintilla(data.PyQt.Qsci.QsciScintillaBase.SCI_SETHOTSPOTACTIVEUNDERLINE, True)
            send_scintilla(data.PyQt.Qsci.QsciScintillaBase.SCI_STARTSTYLING, index_from, 2)
            send_scintilla(data.PyQt.Qsci.QsciScintillaBase.SCI_SETSTYLING, length, 2)
    
    class Bookmarks:
        """
        Bookmark functionality
        """
        def __init__(self, parent):
            """Initialization of the Editing object instance"""
            #Get the reference to the MainWindow parent object instance
            self.parent = parent
        
        def toggle(self):
            """Add/Remove a bookmark at the current line"""
            #Get the cursor line position
            current_line = self.parent.getCursorPosition()[0] + 1
            #Toggle the bookmark
            self.toggle_at_line(current_line)
        
        def toggle_at_line(self, line):
            """
            Toggle a bookmarks at the specified line
            (Line indexing has to be 1..lines)
            """
            #MarkerAdd function needs the standard line indexing
            scintilla_line = line - 1
            #Check if the line is already bookmarked
            if self.parent.main_form.bookmarks.check(self.parent, line) == None:
                if self.parent.main_form.bookmarks.add(self.parent, line) != None:
                    self.parent.markerAdd(scintilla_line, self.parent.bookmark_marker)
            else:
                self.parent.main_form.bookmarks.remove_by_reference(self.parent, line)
                self.parent.markerDelete(scintilla_line, self.parent.bookmark_marker)
        
        def add_marker_at_line(self, line):
            #MarkerAdd function needs the standard line indexing
            scintilla_line = line - 1
            self.parent.markerAdd(scintilla_line, self.parent.bookmark_marker)
        
        def remove_marker_at_line(self, line):
            #MarkerAdd function needs the standard line indexing
            scintilla_line = line - 1
            self.parent.markerDelete(scintilla_line, self.parent.bookmark_marker)
    
    class Keyboard:
        """
        Keyboard command assignment, ...
        Relevant Scintilla items:
            SCI_ASSIGNCMDKEY(int keyDefinition, int sciCommand)
            SCI_CLEARCMDKEY(int keyDefinition)
            SCI_CLEARALLCMDKEYS
            SCI_NULL
        """
        parent = None
        #GNU/Linux and Windows bindings copied from Scintila source 'KeyMap.cxx'
        bindings = {
            "Down" : data.PyQt.Qsci.QsciScintillaBase.SCI_LINEDOWN,
            "Down+Shift" : data.PyQt.Qsci.QsciScintillaBase.SCI_LINEDOWNEXTEND,
            "Down+Ctrl" : data.PyQt.Qsci.QsciScintillaBase.SCI_LINESCROLLDOWN,
            "Down+Alt+Shift" : data.PyQt.Qsci.QsciScintillaBase.SCI_LINEDOWNRECTEXTEND,
            "Up" : data.PyQt.Qsci.QsciScintillaBase.SCI_LINEUP,
            "Up+Shift" : data.PyQt.Qsci.QsciScintillaBase.SCI_LINEUPEXTEND,
            "Up+Ctrl" : data.PyQt.Qsci.QsciScintillaBase.SCI_LINESCROLLUP,
            "Up+Alt+Shift" : data.PyQt.Qsci.QsciScintillaBase.SCI_LINEUPRECTEXTEND,
            "[+Ctrl" : data.PyQt.Qsci.QsciScintillaBase.SCI_PARAUP,
            "[+Ctrl+Shift" : data.PyQt.Qsci.QsciScintillaBase.SCI_PARAUPEXTEND,
            "]+Ctrl" : data.PyQt.Qsci.QsciScintillaBase.SCI_PARADOWN,
            "]+Ctrl+Shift" : data.PyQt.Qsci.QsciScintillaBase.SCI_PARADOWNEXTEND,
            "Left" : data.PyQt.Qsci.QsciScintillaBase.SCI_CHARLEFT,
            "Left+Shift" : data.PyQt.Qsci.QsciScintillaBase.SCI_CHARLEFTEXTEND,
            "Left+Ctrl" : data.PyQt.Qsci.QsciScintillaBase.SCI_WORDLEFT,
            "Left+Shift+Ctrl" : data.PyQt.Qsci.QsciScintillaBase.SCI_WORDLEFTEXTEND,
            "Left+Alt+Shift" : data.PyQt.Qsci.QsciScintillaBase.SCI_CHARLEFTRECTEXTEND,
            "Right" : data.PyQt.Qsci.QsciScintillaBase.SCI_CHARRIGHT,
            "Right+Shift" : data.PyQt.Qsci.QsciScintillaBase.SCI_CHARRIGHTEXTEND,
            "Right+Ctrl" : data.PyQt.Qsci.QsciScintillaBase.SCI_WORDRIGHT,
            "Right+Shift+Ctrl" : data.PyQt.Qsci.QsciScintillaBase.SCI_WORDRIGHTEXTEND,
            "Right+Alt+Shift" : data.PyQt.Qsci.QsciScintillaBase.SCI_CHARRIGHTRECTEXTEND,
            "/+Ctrl" : data.PyQt.Qsci.QsciScintillaBase.SCI_WORDPARTLEFT,
            "/+Ctrl+Shift" : data.PyQt.Qsci.QsciScintillaBase.SCI_WORDPARTLEFTEXTEND,
            "\\+Ctrl" : data.PyQt.Qsci.QsciScintillaBase.SCI_WORDPARTRIGHT,
            "\\+Ctrl+Shift" : data.PyQt.Qsci.QsciScintillaBase.SCI_WORDPARTRIGHTEXTEND,
            "Home" : data.PyQt.Qsci.QsciScintillaBase.SCI_VCHOME,
            "Home+Shift" : data.PyQt.Qsci.QsciScintillaBase.SCI_VCHOMEEXTEND,
            data.go_to_start_keys : data.PyQt.Qsci.QsciScintillaBase.SCI_DOCUMENTSTART,
            data.select_to_start_keys : data.PyQt.Qsci.QsciScintillaBase.SCI_DOCUMENTSTARTEXTEND,
            "Home+Alt" : data.PyQt.Qsci.QsciScintillaBase.SCI_HOMEDISPLAY,
            "Home+Alt+Shift" : data.PyQt.Qsci.QsciScintillaBase.SCI_VCHOMERECTEXTEND,
            "End" : data.PyQt.Qsci.QsciScintillaBase.SCI_LINEEND,
            "End+Shift" : data.PyQt.Qsci.QsciScintillaBase.SCI_LINEENDEXTEND,
            data.go_to_end_keys : data.PyQt.Qsci.QsciScintillaBase.SCI_DOCUMENTEND,
            data.select_to_end_keys : data.PyQt.Qsci.QsciScintillaBase.SCI_DOCUMENTENDEXTEND,
            "End+Alt" : data.PyQt.Qsci.QsciScintillaBase.SCI_LINEENDDISPLAY,
            "End+Alt+Shift" : data.PyQt.Qsci.QsciScintillaBase.SCI_LINEENDRECTEXTEND,
            data.scroll_up_keys : data.PyQt.Qsci.QsciScintillaBase.SCI_PAGEUP,
            data.select_page_up_keys : data.PyQt.Qsci.QsciScintillaBase.SCI_PAGEUPEXTEND,
            "PageUp+Alt+Shift" : data.PyQt.Qsci.QsciScintillaBase.SCI_PAGEUPRECTEXTEND,
            data.scroll_down_keys : data.PyQt.Qsci.QsciScintillaBase.SCI_PAGEDOWN,
            data.select_page_down_keys : data.PyQt.Qsci.QsciScintillaBase.SCI_PAGEDOWNEXTEND,
            "PageDown+Alt+Shift" : data.PyQt.Qsci.QsciScintillaBase.SCI_PAGEDOWNRECTEXTEND,
            "Delete" : data.PyQt.Qsci.QsciScintillaBase.SCI_CLEAR,
            "Delete+Shift" : data.PyQt.Qsci.QsciScintillaBase.SCI_CUT,
            data.delete_end_of_word_keys: data.PyQt.Qsci.QsciScintillaBase.SCI_DELWORDRIGHT,
            data.delete_end_of_line_keys : data.PyQt.Qsci.QsciScintillaBase.SCI_DELLINERIGHT,
            "Insert" : data.PyQt.Qsci.QsciScintillaBase.SCI_EDITTOGGLEOVERTYPE,
            "Insert+Shift" : data.PyQt.Qsci.QsciScintillaBase.SCI_PASTE,
            "Insert+Ctrl" : data.PyQt.Qsci.QsciScintillaBase.SCI_COPY,
            "Escape" : data.PyQt.Qsci.QsciScintillaBase.SCI_CANCEL,
            "Backspace" : data.PyQt.Qsci.QsciScintillaBase.SCI_DELETEBACK,
            "Backspace+Shift" : data.PyQt.Qsci.QsciScintillaBase.SCI_DELETEBACK,
            data.delete_start_of_word_keys : data.PyQt.Qsci.QsciScintillaBase.SCI_DELWORDLEFT,
            "Backspace+Alt" : data.PyQt.Qsci.QsciScintillaBase.SCI_UNDO,
            data.delete_start_of_line_keys : data.PyQt.Qsci.QsciScintillaBase.SCI_DELLINELEFT,
            data.undo_keys : data.PyQt.Qsci.QsciScintillaBase.SCI_UNDO,
            data.redo_keys : data.PyQt.Qsci.QsciScintillaBase.SCI_REDO,
            data.cut_keys : data.PyQt.Qsci.QsciScintillaBase.SCI_CUT,
            data.copy_keys : data.PyQt.Qsci.QsciScintillaBase.SCI_COPY,
            data.paste_keys : data.PyQt.Qsci.QsciScintillaBase.SCI_PASTE,
            data.select_all_keys : data.PyQt.Qsci.QsciScintillaBase.SCI_SELECTALL,
            data.indent_keys : data.PyQt.Qsci.QsciScintillaBase.SCI_TAB,
            data.unindent_keys : data.PyQt.Qsci.QsciScintillaBase.SCI_BACKTAB,
            "Return" : data.PyQt.Qsci.QsciScintillaBase.SCI_NEWLINE,
            "Return+Shift" : data.PyQt.Qsci.QsciScintillaBase.SCI_NEWLINE,
            "Add+Ctrl" : data.PyQt.Qsci.QsciScintillaBase.SCI_ZOOMIN,
            "Subtract+Ctrl" : data.PyQt.Qsci.QsciScintillaBase.SCI_ZOOMOUT,
            "Divide+Ctrl" : data.PyQt.Qsci.QsciScintillaBase.SCI_SETZOOM,
            data.line_cut_keys : data.PyQt.Qsci.QsciScintillaBase.SCI_LINECUT,
            data.line_delete_keys : data.PyQt.Qsci.QsciScintillaBase.SCI_LINEDELETE,
            data.line_copy_keys : data.PyQt.Qsci.QsciScintillaBase.SCI_LINECOPY,
            data.line_transpose_keys : data.PyQt.Qsci.QsciScintillaBase.SCI_LINETRANSPOSE,
            data.line_selection_duplicate_keys : data.PyQt.Qsci.QsciScintillaBase.SCI_SELECTIONDUPLICATE,
            "U+Ctrl" : data.PyQt.Qsci.QsciScintillaBase.SCI_LOWERCASE,
            "U+Ctrl+Shift" : data.PyQt.Qsci.QsciScintillaBase.SCI_UPPERCASE,
        }
        scintilla_keys = {
            "down" : data.PyQt.Qsci.QsciScintillaBase.SCK_DOWN,
            "up" : data.PyQt.Qsci.QsciScintillaBase.SCK_UP,
            "left" : data.PyQt.Qsci.QsciScintillaBase.SCK_LEFT,
            "right" : data.PyQt.Qsci.QsciScintillaBase.SCK_RIGHT,
            "home" : data.PyQt.Qsci.QsciScintillaBase.SCK_HOME,
            "end" : data.PyQt.Qsci.QsciScintillaBase.SCK_END,
            "pageup" : data.PyQt.Qsci.QsciScintillaBase.SCK_PRIOR,
            "pagedown" : data.PyQt.Qsci.QsciScintillaBase.SCK_NEXT,
            "delete" : data.PyQt.Qsci.QsciScintillaBase.SCK_DELETE,
            "insert" : data.PyQt.Qsci.QsciScintillaBase.SCK_INSERT,
            "escape" : data.PyQt.Qsci.QsciScintillaBase.SCK_ESCAPE,
            "backspace" : data.PyQt.Qsci.QsciScintillaBase.SCK_BACK,
            "tab" : data.PyQt.Qsci.QsciScintillaBase.SCK_TAB,
            "return" : data.PyQt.Qsci.QsciScintillaBase.SCK_RETURN,
            "add" : data.PyQt.Qsci.QsciScintillaBase.SCK_ADD,
            "subtract" : data.PyQt.Qsci.QsciScintillaBase.SCK_SUBTRACT,
            "divide" : data.PyQt.Qsci.QsciScintillaBase.SCK_DIVIDE,
            "win" : data.PyQt.Qsci.QsciScintillaBase.SCK_WIN,
            "rwin" : data.PyQt.Qsci.QsciScintillaBase.SCK_RWIN,
            "menu" : data.PyQt.Qsci.QsciScintillaBase.SCK_MENU,
        }
        valid_modifiers = [
            data.PyQt.Qsci.QsciScintillaBase.SCMOD_NORM, 
            data.PyQt.Qsci.QsciScintillaBase.SCMOD_SHIFT, 
            data.PyQt.Qsci.QsciScintillaBase.SCMOD_CTRL, 
            data.PyQt.Qsci.QsciScintillaBase.SCMOD_ALT, 
            data.PyQt.Qsci.QsciScintillaBase.SCMOD_SUPER, 
            data.PyQt.Qsci.QsciScintillaBase.SCMOD_META
        ]
        
        def __init__(self, parent):
            """Initialization of the Keyboard object instance"""
            #Get the reference to the MainWindow parent object instance
            self.parent = parent
            #Assign keyboard commands
            self.clear_all_keys()
            bindings = self.bindings
            set_key_combination = self.set_key_combination
            for keys in bindings:
                set_key_combination(
                    keys, bindings[keys]
                )
        
        def _parse_key_string(self, key_string):
            """ Parse a '+' delimited string for a key combination """
            split_keys = key_string.replace(" ", "").lower().split("+")
            #Check for to many keys in binding
            if len(split_keys) > 4:
                raise ValueError("Too many items in key string!")
            #Parse the items
            modifiers = []
            key_combination = 0
            if "ctrl" in split_keys:
                modifiers.append(data.PyQt.Qsci.QsciScintillaBase.SCMOD_CTRL)
                split_keys.remove("ctrl")
            if "alt" in split_keys:
                modifiers.append(data.PyQt.Qsci.QsciScintillaBase.SCMOD_ALT)
                split_keys.remove("alt")
            if "shift" in split_keys:
                modifiers.append(data.PyQt.Qsci.QsciScintillaBase.SCMOD_SHIFT)
                split_keys.remove("shift")
            if "meta" in split_keys:
                modifiers.append(data.PyQt.Qsci.QsciScintillaBase.SCMOD_META)
                split_keys.remove("meta")
            base_key = split_keys[0]
            if len(split_keys) == 0:
                raise ValueError("Key string has to have a base character!")
            if len(base_key) != 1:
                if base_key in self.scintilla_keys:
                    key_combination = self.scintilla_keys[base_key]
                else:
                    raise ValueError("Unknown base key!")
            else:
                key_combination = ord(base_key.upper())
            if modifiers != []:
                for m in modifiers:
                    key_combination += (m << 16)
            return key_combination
        
        def _check_keys(self, key, modifier=None):
            """ Check the validity of the key and modifier """
            if isinstance(key, str) == True:
                if len(key) != 1:
                    if modifier != None:
                        raise ValueError("modifier argument has to be 'None' with a key string!")
                    #key argument is going to be parsed as a combination
                    key = self._parse_key_string(key)
                else:
                    if key in self.scintilla_keys:
                        key = self.scintilla_keys[key]
                    else:
                        key = ord(key)
            if modifier == None:
                key_combination = key
            else:
                if not(modifier in self.valid_modifiers):
                    raise ValueError("The keyboard modifier is not valid: {}".format(modifier))
                key_combination = key + (modifier << 16)
            return key_combination
        
        def clear_all_keys(self):
            """
            Clear all mappings from the internal Scintilla mapping table
            """
            self.parent.SendScintilla(
                data.PyQt.Qsci.QsciScintillaBase.SCI_CLEARALLCMDKEYS
            )
        
        def clear_key_combination(self, key, modifier=None):
            """
            Clear the key combination from the internal Scintilla Mapping
            Raw example of clearing the CTRL+X (Cut text function) combination:
                cmain.SendScintilla(
                    data.PyQt.Qsci.QsciScintillaBase.SCI_CLEARCMDKEY, 
                    ord('X') + (data.PyQt.Qsci.QsciScintillaBase.SCMOD_CTRL << 16)
                )
            """
            try:
                key_combination = self._check_keys(key, modifier)
            except Exception as ex:
                self.parent.main_form.display.repl_display_message(
                    str(ex), 
                    message_type=data.MessageType.ERROR
                )
                return
            self.parent.SendScintilla(
                data.PyQt.Qsci.QsciScintillaBase.SCI_CLEARCMDKEY, 
                key_combination
            )
        
        def set_key_combination(self, key, command, modifier=None):
            """
            Assign a key combination to a command.
            Parameters:
                key - character or key string combination
                command - Scintilla command that will execute on the key combination
                modifier - Ctrl, Alt, ...
            Raw example of assigning CTRL+D to the Cut function:
                cmain.SendScintilla(
                    data.PyQt.Qsci.QsciScintillaBase.SCI_ASSIGNCMDKEY, 
                    ord('D') + (data.PyQt.Qsci.QsciScintillaBase.SCMOD_CTRL << 16),
                    data.PyQt.Qsci.QsciScintillaBase.SCI_CUT
                )
            """
            try:
                key_combination = self._check_keys(key, modifier)
            except Exception as ex:
                self.parent.main_form.display.repl_display_message(
                    str(ex), 
                    message_type=data.MessageType.ERROR
                )
                return
            self.parent.SendScintilla(
                data.PyQt.Qsci.QsciScintillaBase.SCI_ASSIGNCMDKEY, 
                key_combination,
                command
            )
        


"""
-----------------------------
Python REPL widget
-----------------------------
"""
class ReplLineEdit(data.QLineEdit):
    """Custom QLineEdit used for the REPL functionality"""
    #Class variables  (class variables >> this means that these variables are shared accross instances of this class, until you assign a new value to them, then they become instance variables)
    parent                          = None          #Main window reference
    interpreter                     = None          #Custom interpreter used with the REPL
    #Attribute for indicating if the REPL is indicated
    indicated                       = False
    #List of characters to use for splitting the compare string for sequences. Minus (-) was taken out because it can appear in path names 
    _comparison_list                = [".", "(", " ", "+", "-", "*", "%", ",", "\"", "'"]
    _reduced_comparison_list        = ["(", " ", "+", "-", "*", "%", ",", "\"", "'"]
    #Lists of autocompletions grouped by levels
    _list_first_level_completions   = None
    _list_second_level_completions  = None
    #Generator used to cycle through autocompletions
    _ac_cycler                      = None
    #Dictionary that holds the current buffer position, the whole buffer list and the currently typed input
    _input_buffer                   = {"count": 0,  "list": [], "current_input": ""}
    #Flag that when set, make the next REPL evaluation not focus back on the REPL
    _repl_focus_flag                = False
    
    """
    Built-in and private functions
    """
    def __init__(self, parent, interpreter_references=None):
        """Initialization"""
        #Initialize superclass class, from which the current class is inherited, THIS MUST BE DONE SO THAT THE SUPERCLASS EXECUTES ITS __init__ !!!!!!
        super().__init__()
        #Initialize the parent references and update the autocompletion lists
        self.parent = parent
        #Initialize the interpreter
        self.interpreter = interpreter.CustomInterpreter(
            interpreter_references, 
            parent.display.repl_display_message
        )
        #Initialize interpreter reference list that will be used for autocompletions
        self._list_repl_references  = [str_ref for str_ref in interpreter_references]

    def _get_path_list(self, path_string):
        """Return a list of all directories and files if the path string is valid"""
        path_list   = []
        #Strip the path to the last forwardslash character
        base_path   = path_string[:path_string.rfind("/")+1]
        #Check if the base path string is a valid path
        if os.path.isdir(base_path) == False:
            return path_list
        #Add items of directory to list
        for item in os.listdir(base_path):
            path_list.append(os.path.join(base_path, item))
        #Return the path item list
        return path_list

    def _filter_keypress(self, key_event):
        """Filter keypress for appropriate action"""
        pressed_key = key_event.key()
        #Reset the autocompletion cycler
        self._ac_cycler                 = None
        #Get valid sequances used for autocompletion
        current_sequences_list = self._get_valid_sequence_list(self.text())
        #Check and display autocompletions if any are valid
        autocompletion_list = self._find_autocompletions(current_sequences_list)
        if (pressed_key >= 48 and pressed_key <= 57 or
            pressed_key >= 65 and pressed_key <= 90 or
            pressed_key == 95):
            #Return if there are no characters in the current sequence
            if len(current_sequences_list[0]) == 0:
                return
            #A letter or number has been pressed
            self._display_autocompletion(autocompletion_list)
            #Create the cycler that will cycle through the autocompletions
            self._create_ac_cycler(autocompletion_list)
            #A new character has been type, reset the input buffer counter
            self._input_buffer["count"] = 0
        elif pressed_key == 16777235:
            #Cycle input buffer up
            self._input_buffer_cycle(1)
        elif pressed_key == 16777237:
            #Cycle input buffer down
            self._input_buffer_cycle(0)
        elif pressed_key == 16777219:
            #A new character has been typed, reset the input buffer counter
            self._input_buffer["count"] = 0
        elif (pressed_key == data.PyQt.QtCore.Qt.Key_Enter or
                pressed_key == data.PyQt.QtCore.Qt.Key_Return):
            if self.selectedText() != "":
                self.setCursorPosition(len(self.text()))
            else:
                #Detected ENTER key press, evaluate REPL text
                self._repl_eval()

    def _repl_eval(self, external_string=None, display_action=True):
        """Evaluate string entered into the REPL widget"""
        data.print_log("REPL evaluated")
        #Check if an external evaluation string was specified
        if external_string == None:
            #No external evaluation string, evaluate the REPL text
            current_command = self.text()
        else:
            current_command = external_string
        #Display evaluated command if specified
        current_rm_index = None
        if display_action == True:
            repl_messages = self.parent.display.find_repl_messages_tab()
            if repl_messages != None:
                if repl_messages.parent.count() > 1:
                    current_rm_index = repl_messages.parent.currentIndex()
            #Display the evaluated command (this sets the focus to the REPL messages tab)
            split_command = current_command.split("\n")
            for i, command in enumerate(split_command):
                if i != 0:
                    self.parent.display.repl_display_message("... " + command)
                else:
                    self.parent.display.repl_display_message(">>> " + command)
            if current_rm_index != None:
                #Revert the focus of the BasicWidget that hold the REPL messages tab to
                #whichever widget was focused before
                repl_messages.parent.setCurrentIndex(current_rm_index)
        #Evaluate the REPL text and store the result
        eval_return = self.interpreter.eval_command(current_command, display_action)
        #Save text into the input buffer
        self._input_buffer_add(self.text())
        #Clear the REPL text
        self.setText("")
        #Check if the REPL focus flag is set
        if self._repl_focus_flag == True:
            #Skip setting focus back to the REPL and reset the skip focus flag
            self._repl_focus_flag = False
        else:
            #Set focus back to the REPL
            self.setFocus()
        #Check evaluation return message and display it in the "REPL Messages" tab
        if eval_return != None:
            data.print_log(eval_return)
            if display_action == True:
                self.parent.display.repl_display_message(
                    eval_return,
                    message_type=data.MessageType.ERROR
                )
            else:
                return eval_return
        else:
            data.print_log("EVALUATION/EXECUTION SUCCESS")
        return None


    """
    REPL autocompletion functions
    """
    def _display_autocompletion(self, ac_list):
        """Show the autocompletion in the REPL"""
        #Check if there are no autocompletions and that there is no text after the cursor position
        if len(ac_list) > 0 and self.cursorPosition() == len(self.text()):
            start_pos   = self.cursorPosition()
            self.setText(self.text() + ac_list[0])
            end_pos     = self.cursorPosition()
            #Select the added autocompletion text
            self.setSelection(start_pos, end_pos)
    
    def _create_ac_cycler(self,  autocompletion_list):
        """Create a autocompletion cycler to cycle through all of the autocompletions"""
        if len(autocompletion_list) > 0:
            self._ac_cycler = itertools.cycle(autocompletion_list)
            #Cycle one autocompletion forward, because the first autocompletion is already shown
            next(self._ac_cycler)
        else:
            self._ac_cycler = None
    
    def _cycle_autocompletion(self):
        """Cycle through autocompletion list"""
        #Return if there are no autocompletions
        if self._ac_cycler == None:
            return
        if self.selectedText() == "":
            #Current autocompletion is already shown without a selection area
            ac_start        = len(self.text())
            self.setText(self.text() + next(self._ac_cycler))
            end_pos     = self.cursorPosition()
            self.setSelection(ac_start, end_pos)
        else:
            #Current autocompletion has a selection area
            ac_start        = self.selectionStart()
            self.setText(self.text()[:ac_start] + next(self._ac_cycler))
            end_pos     = self.cursorPosition()
            self.setSelection(ac_start, end_pos)

    def _input_buffer_cycle(self, direction=0):
        """Cycle the input buffer into the selected direction"""
        #Check if the input buffer is empty
        if len(self._input_buffer["list"]) == 0:
            return
        #Save currently typed text
        if self._input_buffer["count"] == 0:
            self._input_buffer["current_input"] = self.text()
        #Check what is the current buffer position, change it and put it into the REPL
        if direction == 1:
            if self._input_buffer["count"] > -(len(self._input_buffer["list"])):
                self._input_buffer["count"] -= 1
            self.setText(self._input_buffer["list"][self._input_buffer["count"]])
        else:
            if self._input_buffer["count"] < -1:
                self._input_buffer["count"] += 1
                self.setText(self._input_buffer["list"][self._input_buffer["count"]])
            else:
                #Show currently saved input text (the text that the user typed before pressing up)
                self._input_buffer["count"] = 0
                self.setText(self._input_buffer["current_input"])
    
    def _input_buffer_add(self,  entry):
        """Add a single value to the input buffer"""
        #Check if there is any input text
        if self.text() == "":
            return
        #Check if the last saved input is the same as the current input, otherwise add it to the input buffer
        if len(self._input_buffer["list"]) > 0:
            if self.text() != self._input_buffer["list"][-1]:
                self._input_buffer["list"].append(self.text())
        else:
            #Add the text into the buffer withoit checking if the input buffer is empty
            self._input_buffer["list"].append(self.text())
        #Reset the item counter
        self._input_buffer["count"] = 0
        #Reset the stored current input text
        self._input_buffer["current_input"] = ""

    def input_buffer_clear(self):
        """Clear the input buffer, counter and current saved input"""
        self._input_buffer  = {"count": 0,  "list": [], "current_input": ""}

    def _get_valid_sequence_list(self, string):
        """
        Get the last one or two valid sequence, which will be compared to autocompletion list
        E.G. 1: "print(main.se" returns >> first = "se", second = "main"
        E.G. 2: "print_log(nek" returns >> first = "nek", second = ""
        """
        raw_text                = string
        current_sequence    = ""
        previous_sequence   = ""
        #List the separators as they appear in the raw string
        separator_list = []
        for ch in raw_text:
            if ch in self._comparison_list:
                separator_list.append(ch)
        #Do the standard autocompletion parse
        for i, ch_1 in reversed(list(enumerate(raw_text))):
            #Get the last valid separation character
            if ch_1 in self._comparison_list:
                current_sequence = raw_text[(i+1):]
                #If the character is a dot, return the previous sequence also
                if ch_1 == ".":
                    #The separator is a dot, get the previous sequence in case it's a class
                    for j, ch_2 in reversed(list(enumerate(raw_text[:i]))):
                        if ch_2 in self._reduced_comparison_list:
                            #Found a character from the reduced comparison list
                            previous_sequence = raw_text[(j+1):i]
                            break
                        elif j == 0:
                            #Did not find a character from the reduced comparison list and reached the beggining of text
                            previous_sequence = raw_text[j:i]
                            break
                break
        if not [x for x in raw_text if x in self._comparison_list]:
            #None of the separator characters were found in current text
            current_sequence = self.text()
        data.print_log(previous_sequence + "  " + current_sequence)
        return [current_sequence, previous_sequence]
    
    def _find_autocompletions(self, current_sequences_list):
        """Check and display the current autocompletions, if there are any"""
        current_sequence    = current_sequences_list[0]
        previous_sequence   = current_sequences_list[1]
        found_list              = []
        if previous_sequence != "":
            for ref in self._list_second_level_completions:
                if ref.startswith(previous_sequence + "." + current_sequence):
                    #Autocompletion found, delete the part of the autocompletion that is already written
                    found_list.append(ref.replace(previous_sequence + "." + current_sequence, ""))
        else:
            #Test if autocompletion is a path or an object
            if "/" in current_sequence or "\\" in current_sequence:
                #Replace the windows path backslashes to forwardslashes
                if "\\" in current_sequence:
                    current_sequence = current_sequence.replace("\\", "/")
                #Path (all path searches are done case sensetively)
                path_items = self._get_path_list(current_sequence)
                for item in path_items:
                    if item.startswith(current_sequence):
                        diff_index = re.search(current_sequence, item).end()
                        #Autocompletion found, delete the part of the autocompletion that is already written
                        found_list.append(item[diff_index:])
            else:
                #Object
                for ref in self._list_first_level_completions:
                    if ref.startswith(current_sequence):
                        #Autocompletion found, delete the part of the autocompletion that is already written.
                        #ONLY THE FIRST INSTANCE OF THE ALREADY WRITTEN PART HAS TO BE REPLACED,
                        #ELSE YOU GET:
                        #   "line_list" autocompletion, input_text = "li" >>> output of "ref.replace(current_sequence, "")"
                        #   is "ne_st" instead of "ne_list"
                        found_list.append(ref.replace(current_sequence, "", 1))
        return found_list


    """
    Qt QLineEdit functions
    """
    def event(self, event):
        """Rereferenced/overloaded main QWidget event, that is executed before all other events of the widget"""
        if (event.type() == data.PyQt.QtCore.QEvent.KeyPress) and (event.key() == data.PyQt.QtCore.Qt.Key_Tab):
            self._cycle_autocompletion()
            return True
        return data.QLineEdit.event(self, event)

    def _keypress_decorator(func):
        """A decorator for the QScintila KeypressEvent, to catch which key was pressed"""
        def key_press(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self._filter_keypress(args[0])
        return key_press

    @_keypress_decorator    #Add decorator to the keypress event
    def keyPressEvent(self,  event):
        """QScintila keyPressEvent, to catch which key was pressed"""
        #Return the key event
        return data.QLineEdit.keyPressEvent(self, event)

    def focusInEvent(self, event):
        """Event that fires when the REPL gets focus"""
        self.parent._key_events_lock()
        #Set the focus to the REPL
        self.setFocus()
        #Clear the cursor position from the statusbar
        self.parent.display.update_cursor_position()
        data.print_log("Entered REPL")
        #Reset the main forms last focused widget
        self.parent.last_focused_widget = None
        data.print_log("Reset last focused widget attribute")
        #Hide the function wheel if it is shown
        if self.parent.view.function_wheel_overlay != None:
            self.parent.view.hide_function_wheel()
        #Ignore the event
        event.ignore()
        #Return the focus event
        return data.QLineEdit.focusInEvent(self, event)
    
    def setFocus(self):
        """Overridden focus event"""
        #Execute the supeclass focus function
        super().setFocus()
        #Check indication
        self.parent.view.indication_check()

    def focusOutEvent(self, event):
        """Event that fires when the REPL loses focus"""
        self.parent._key_events_unlock()
        data.print_log("Left REPL")
        #Ignore the event
        event.ignore()
        #Return the focus event
        return data.QLineEdit.focusOutEvent(self, event)
    
    def wheelEvent(self, wheel_event):
        """Overridden mouse wheel rotate event"""
        key_modifiers = data.QApplication.keyboardModifiers()
        if data.PYQT_MODE == 4:
            delta = wheel_event.delta()
        else:
            delta = wheel_event.angleDelta().y()
        if delta < 0:
            data.print_log("REPL helper mouse rotate down event")
            if key_modifiers == data.PyQt.QtCore.Qt.ControlModifier:
                #Zoom out the scintilla tab view
                self.decrease_text_size()
        else:
            data.print_log("REPL helper mouse rotate up event")
            if key_modifiers == data.PyQt.QtCore.Qt.ControlModifier:
                #Zoom in the scintilla tab view
                self.increase_text_size()
        #Handle the event
        if key_modifiers == data.PyQt.QtCore.Qt.ControlModifier:
            #Accept the event, the event will not be propageted(sent forward) to the parent
            wheel_event.accept()
        else:
            #Propagate(send forward) the wheel event to the parent
            wheel_event.ignore()
    
    def increase_text_size(self):
        """Increase size of the REPL text"""
        new_font = self.font()
        if new_font.pointSize() > 32:
            return
        new_font.setPointSize(new_font.pointSize() + 1)
        self.setFont(new_font)
        new_font_metric = data.PyQt.QtGui.QFontMetrics(new_font)
        self.parent.view.main_relation = new_font_metric.height() + 48
        self.parent.view.refresh_main_splitter()
    
    def decrease_text_size(self):
        """Decrease size of the REPL text"""
        new_font = self.font()
        if new_font.pointSize() < 12:
            return
        new_font.setPointSize(new_font.pointSize() - 1)
        self.setFont(new_font)
        new_font_metric = data.PyQt.QtGui.QFontMetrics(new_font)
        self.parent.view.main_relation = new_font_metric.height() + 48
        self.parent.view.refresh_main_splitter()
    

    """
    REPL interactive interpreter functions
    """
    def interpreter_update_references(self, new_references, first_level_list, second_level_list):
        """Update the references that can be accessed by the interactive interpreter"""
        #Update the interpreter with the new locals
        self.interpreter.update_locals(new_references)
        self._list_first_level_completions = first_level_list
        self._list_second_level_completions = second_level_list
        #Extend the primary autocompletion with the useful custom interpreter methods
        self._list_first_level_completions.extend(self.interpreter.get_default_references())
        #Extend the primary autocompletion with the regular expression dictionary of the REPL CustomInterpreter
        self._list_first_level_completions.extend(self.interpreter.dict_re_references)
        #The keyword dictionary is different from the references, look in the interpreter module
        ext_first_level = [self.interpreter.dict_keywords[keyword][0] for keyword in self.interpreter.dict_keywords]
        self._list_first_level_completions.extend(ext_first_level)
        #Convert lists to sets and back to remove duplicates
        self._list_first_level_completions  = list(set(self._list_first_level_completions))
        self._list_second_level_completions = list(set(self._list_second_level_completions))
        #Sort the new lists alphabetically
        self._list_first_level_completions.sort()
        self._list_second_level_completions.sort()
    
    def interpreter_add_references(self, new_references):
        """Append new references to the existing REPL interpreter references"""
        self._list_first_level_completions = list(self._list_first_level_completions)
        #Extend the primary autocompletions
        self._list_first_level_completions.extend(new_references)
        #Convert list to set and back to remove duplicates
        self._list_first_level_completions = list(set(self._list_first_level_completions))
        #Sort the new lists alphabetically
        self._list_first_level_completions.sort()
    
    def interpreter_reset_references(self, new_references, first_level_list, second_level_list):
        """Clear all of the interpreter references and update them with the new ones"""
        #Clear the references
        self.interpreter.reset_locals
        #Update the references
        self.interpreter_update_references(new_references, first_level_list, second_level_list)
    
    def interpreter_update_windows(self, main, upper, lower):
        """Update the Main, Upper and Lower window references of the interpreter"""
        self.interpreter.locals["main"]     = main
        self.interpreter.locals["upper"]    = upper
        self.interpreter.locals["lower"]    = lower


    """
    Various ReplLineEdit functions
    """
    def skip_next_repl_focus(self):
        """
        Function that sets the flag that makes the next REPL evaluation
        skip setting focus back to the ReplLineEdit
        """
        #Set the skip focus flag
        self._repl_focus_flag = True
    
    def get_repl_references(self):
        """Create and return a dictionary that holds all the REPL references that will be used in the interpreter module"""
        return  dict(
                    repl        = self,
                    interpreter = self.interpreter, 
                )   
    
    def repeat_last_repl_eval(self):
        """Repeat the last command that was evaluated by the REPL if any"""
        #Check the input buffer
        if len(self._input_buffer["list"]) > 0:
            #Set REPL text to the last item in REPL input list by cycling the buffer list up
            self._input_buffer_cycle(1)
            #Evaluate REPL text
            self._repl_eval()
        else:
            self.parent.display.write_to_statusbar("No commands in REPL input buffer!", 1000)

    def external_eval_request(self, eval_string, calling_widget):
        """An external evaluation request from the ReplHelper or another widget"""
        #Evaluate the external string
        self._repl_eval(eval_string)
        #Set focus back to the calling widget
        calling_widget.setFocus()

"""
-----------------------------------------------------
Scintilla class for inputting more than one line into the REPL
-----------------------------------------------------
"""
class ReplHelper(data.PyQt.Qsci.QsciScintilla):

    """
    REPL scintilla box for inputting multiple lines into the REPL.
    MUST BE PAIRED WITH A ReplLineEdit OBJECT!
    """
    #Class variables
    parent          = None
    repl_master     = None
    #The scintilla api object(data.PyQt.Qsci.QsciAPIs) must be an instace variable, or the underlying c++
    #mechanism deletes the object and the autocompletions compiled with api.prepare() are lost
    api             = None
    #Attribute for indicating if the REPL helper is indicated
    indicated       = False
    #Default font
    default_font    = data.PyQt.QtGui.QFont('Courier', 10)
    #LineList object copied from the CustomEditor object
    line_list       = None
    
    """
    Built-in and private functions
    """
    def __init__(self, parent, repl_master):
        #Initialize superclass, from which the current class is inherited, THIS MUST BE DONE SO THAT THE SUPERCLASS EXECUTES ITS __init__ !!!!!!
        super().__init__()
        #Save the reference to the parent(main window)
        self.parent = parent
        #Save the reference to the REPL object
        self.repl_master = repl_master
        #Hide the horizontal and show the vertical scrollbar
        self.SendScintilla(data.PyQt.Qsci.QsciScintillaBase.SCI_SETVSCROLLBAR, True)
        self.SendScintilla(data.PyQt.Qsci.QsciScintillaBase.SCI_SETHSCROLLBAR, False)
        #Hide the margin
        self.setMarginWidth(1, 0)
        #Autoindentation enabled when using "Enter" to indent to the same level as the previous line
        self.setAutoIndent(True)
        #Tabs are spaces by default
        self.setIndentationsUseTabs(False)
        #Set tab space indentation width
        self.setTabWidth(data.tab_width)
        #Set encoding format to UTF-8 (Unicode)
        self.setUtf8(True)
        #Set brace matching
        self.setBraceMatching(data.PyQt.Qsci.QsciScintilla.SloppyBraceMatch)
        self.setMatchedBraceBackgroundColor(data.PyQt.QtGui.QColor(255, 153, 0))
        #Tabs are spaces by default
        self.setIndentationsUseTabs(False)
        #Set backspace to delete by tab widths
        self.setBackspaceUnindents(True)
        #Disable drops
        self.setAcceptDrops(False)
        #Set line endings to be Unix style ("\n")
        self.setEolMode(data.default_eol)
        #Set the initial zoom factor
        self.zoomTo(data.zoom_factor)
        """
        Functionality copied from the CustomEditor to copy some of 
        the neede editing functionality like commenting, ...
        """
        # Add the attributes needed to imple
        self.line_list = CustomEditor.LineList(self, self.text())
        self.line_list = [""]
        self.current_file_type = "PYTHON"
        self.comment_string = "#"
        self.oberon_comment_style = False
        # Add the needed functions assigned from the CustomEditor
        self.set_theme = functools.partial(CustomEditor.set_theme, self)
        self.toggle_comment_uncomment = functools.partial(CustomEditor.toggle_comment_uncomment, self)
        self.comment_line = functools.partial(CustomEditor.comment_line, self)
        self.comment_lines = functools.partial(CustomEditor.comment_lines, self)
        self.uncomment_line = functools.partial(CustomEditor.uncomment_line, self)
        self.uncomment_lines = functools.partial(CustomEditor.uncomment_lines, self)
        self.prepend_to_line = functools.partial(CustomEditor.prepend_to_line, self)
        self.prepend_to_lines = functools.partial(CustomEditor.prepend_to_lines, self)
        self.replace_line = functools.partial(CustomEditor.replace_line, self)
        self.get_line = functools.partial(CustomEditor.get_line, self)
        self.check_line_numbering = functools.partial(CustomEditor.check_line_numbering, self)
        self.text_to_list = functools.partial(CustomEditor.text_to_list, self)
        self.list_to_text = functools.partial(CustomEditor.list_to_text, self)
        # Add the function and connect the signal to update the line/column positions
        self._signal_editor_cursor_change = functools.partial(BasicWidget._signal_editor_cursor_change, self)
        self.cursorPositionChanged.connect(self._signal_editor_cursor_change)
        #Set the lexer to python
        self.set_lexer()
        #Set the initial autocompletions
        self.update_autocompletions()

    def _filter_keypress(self, key_event):
        """Filter keypress for appropriate action"""
        pressed_key = key_event.key()
        accept_keypress = False
        #Get key modifiers and check if the Ctrl+Enter was pressed
        key_modifiers = data.QApplication.keyboardModifiers()
        if ((key_modifiers == data.PyQt.QtCore.Qt.ControlModifier and pressed_key == data.PyQt.QtCore.Qt.Key_Return) or
            pressed_key == data.PyQt.QtCore.Qt.Key_Enter):
                #ON MY KEYBOARD Ctrl+Enter CANNOT BE DETECTED!
                #Qt.ControlModifier  MODIFIER SHOWS FALSE WHEN USING data.QApplication.keyboardModifiers() + Enter
                self.repl_master.external_eval_request(self.text(), self)
                accept_keypress = True
        return accept_keypress
    
    def _filter_keyrelease(self, key_event):
        """Filter keyrelease for appropriate action"""
        #Only check indication if the current widget is not indicated
        if self.indicated == False:
            #Check indication
            self.parent.view.indication_check()
        return False

    """
    Qt QSciScintilla functions
    """
    def keyPressEvent(self, event):
        """QScintila keyPressEvent, to catch which key was pressed"""       
        #Filter the event
        if self._filter_keypress(event) == False:
            #Execute the superclass method, if the filter ignored the event
            super(data.PyQt.Qsci.QsciScintilla, self).keyPressEvent(event)
    
    def keyReleaseEvent(self, event):
        """QScintila KeyReleaseEvent, to catch which key was released"""
        #Execute the superclass method first, the same trick as in __init__ !
        super(data.PyQt.Qsci.QsciScintilla, self).keyReleaseEvent(event)
        #Filter the event
        self._filter_keyrelease(event)
    
    def mousePressEvent(self, event):
        # Execute the superclass mouse click event
        super().mousePressEvent(event)
        # Reset the main forms last focused widget
        self.parent.last_focused_widget = None
        data.print_log("Reset last focused widget attribute")
        # Set focus to the clicked helper
        self.setFocus()
        # Hide the function wheel if it is shown
        if self.parent.view.function_wheel_overlay != None:
            self.parent.view.hide_function_wheel()
            # Need to set focus to self or the repl helper doesn't get focused,
            # don't know why?
            self.setFocus()
    
    def setFocus(self):
        """Overridden focus event"""
        # Execute the supeclass focus function
        super().setFocus()
        # Check indication
        self.parent.view.indication_check()
    
    def wheelEvent(self, wheel_event):
        """Overridden mouse wheel rotate event"""
        key_modifiers = data.QApplication.keyboardModifiers()
        if data.PYQT_MODE == 4:
            delta = wheel_event.delta()
        else:
            delta = wheel_event.angleDelta().y()
        if delta < 0:
            data.print_log("REPL helper mouse rotate down event")
            if key_modifiers == data.PyQt.QtCore.Qt.ControlModifier:
                #Zoom out the scintilla tab view
                self.zoomOut()
        else:
            data.print_log("REPL helper mouse rotate up event")
            if key_modifiers == data.PyQt.QtCore.Qt.ControlModifier:
                #Zoom in the scintilla tab view
                self.zoomIn()
        #Handle the event
        if key_modifiers != data.PyQt.QtCore.Qt.ControlModifier:
            #Execute the superclass method
            super(data.PyQt.Qsci.QsciScintilla, self).wheelEvent(wheel_event)
        else:
            #Propagate(send forward) the wheel event to the parent
            wheel_event.ignore()
    
    def set_lexer(self):
        if self.lexer() != None:
            self.lexer().setParent(None)
            self.setLexer(None)
        # Create the new lexer
        lexer = lexers.Python()
        lexer.setParent(self)
        #Set the lexers default font
        lexer.setDefaultFont(self.default_font)
        #Set the lexer with the initial autocompletions
        self.setLexer(lexer)
        #Set the theme
        self.set_theme(data.theme)
        self.lexer().set_theme(data.theme)
    
    def refresh_lexer(self):
        #Set the theme
        self.set_theme(data.theme)
        self.lexer().set_theme(data.theme)
        

    """
    ReplHelper autocompletion functions
    """
    def update_autocompletions(self, new_autocompletions=[]):
        """Function for updating the ReplHelper autocompletions"""
        #Set the lexer
        self.refresh_lexer()
        #Set the scintilla api for the autocompletions (MUST BE AN INSTANCE VARIABLE)
        self.api = data.PyQt.Qsci.QsciAPIs(self.lexer())
        #Populate the api with all of the python keywords
        for kw in keyword.kwlist:
            self.api.add(kw)
        for word in new_autocompletions:
            self.api.add(word)
        self.api.prepare()
        #Set how many characters must be typed for the autocompletion popup to appear
        self.setAutoCompletionThreshold(1)
        #Set the source from where the autocompletions will be fetched
        self.setAutoCompletionSource(data.PyQt.Qsci.QsciScintilla.AcsAll)
        #Set autocompletion case sensitivity
        self.setAutoCompletionCaseSensitivity(False)


"""
----------------------------------------------------------------
Overlay helper widget for visually selecting an Ex.Co. function
----------------------------------------------------------------
"""
class FunctionWheelOverlay(data.QGroupBox):
    #Class custom objects/types
    class ButtonInfo:
        """
        Simple object used as a structure for the custom button information
        """
        #Class variables
        name                = None
        geometry            = None
        pixmap              = None
        function            = None
        function_text       = None
        font                = None
        focus_last_widget   = None
        no_tab_focus_disable        = None
        no_document_focus_disable   = None
        check_last_tab_type = None
        extra_button        = None
        check_text_differ   = None
        tool_tip            = None
        
        def __init__(self, 
                     input_name, 
                     input_geometry, 
                     input_pixmap, 
                     input_function, 
                     input_function_text, 
                     input_font=data.PyQt.QtGui.QFont(
                                    'Courier', 14, weight=data.PyQt.QtGui.QFont.Bold
                                ), 
                     input_focus_last_widget=data.HexButtonFocus.NONE, 
                     input_no_tab_focus_disable=False, 
                     input_no_document_focus_disable=True, 
                     input_check_last_tab_type=False, 
                     input_extra_button=None, 
                     input_check_text_differ=False, 
                     input_tool_tip=None):
            #Initialize the attributes
            self.name               = input_name
            self.geometry           = input_geometry
            self.pixmap             = input_pixmap
            self.function           = input_function
            self.function_text      = input_function_text
            self.font               = input_font
            self.focus_last_widget  = input_focus_last_widget
            self.no_tab_focus_disable   = input_no_tab_focus_disable
            self.no_document_focus_disable   = input_no_document_focus_disable
            self.check_last_tab_type    = input_check_last_tab_type
            self.extra_button       = input_extra_button
            self.check_text_differ  = input_check_text_differ
            self.tool_tip           = input_tool_tip
    
    class CustomButton(data.QLabel):
        """
        Custom button used for displaying and executing Ex.Co. functions
        """
        #Class variables
        parent              = None
        group_box_parent    = None
        main_form           = None
        stored_pixmap       = None
        stored_font         = None
        stored_hex          = None
        function            = None
        function_text       = None
        stored_opacity      = 0.0
        focus_last_widget   = True
        no_tab_focus_disable       = False
        no_document_focus_disable  = True
        check_last_tab_type = False
        check_text_differ   = None
        tool_tip            = None
        #Class constants
        OPACITY_LOW         = 0.5
        OPACITY_HIGH        = 1.0
        
        
        def __init__(self, 
                     parent, 
                     main_form,
                     input_pixmap, 
                     input_function=None, 
                     input_function_text="", 
                     input_font=data.PyQt.QtGui.QFont(
                                    'Courier', 14, weight=data.PyQt.QtGui.QFont.Bold
                                ), 
                     input_focus_last_widget=data.HexButtonFocus.NONE, 
                     input_no_tab_focus_disable=False, 
                     input_no_document_focus_disable=True, 
                     input_check_last_tab_type=False, 
                     input_check_text_differ=False, 
                     input_tool_tip=None):
            #Initialize superclass
            super().__init__(parent)
            #Store the reference to the parent
            self.parent = parent
            #Store the reference to the main form
            self.main_form = main_form
            #Store the reference to the group box that holds the parent
            #(the parent of the parent)
            self.group_box_parent = parent.parent
            #Store the main function image
            self.stored_pixmap = input_pixmap
            #Store the hex edge image
            self.stored_hex = data.PyQt.QtGui.QPixmap(
                os.path.join(
                    data.resources_directory, 
                    "various/hex-button-edge.png"
                )
            )
            #Store the function that will be executed on the click event
            self.function = input_function
            #Store the function text
            self.function_text = input_function_text
            #Set the attribute that will be check if focus update is needed
            #when the custom button executes its function
            self.focus_last_widget = input_focus_last_widget
            #Set the attribute that checks if any tab is focused
            self.no_tab_focus_disable = input_no_tab_focus_disable
            #Set the attribute that will be check if button will be disabled
            #if there is no focused document tab
            self.no_document_focus_disable = input_no_document_focus_disable
            #Set checking the save state stored in the main form
            self.check_last_tab_type = input_check_last_tab_type
            #Set checking for if the focused tab is a text differer
            self.check_text_differ  = input_check_text_differ
            #Set the font that will be used with the button
            self.stored_font = input_font
            #Enable mouse move events
            self.setMouseTracking(True)
            #Set the image for displaying
            self.setPixmap(input_pixmap)
            #Image should scale to the button size
            self.setScaledContents(True)
            #Set the initial opacity to low
            self._set_opacity(self.OPACITY_LOW)
            #Set the tooltip if it was set
            if input_tool_tip != None:
                self.setToolTip(input_tool_tip)

        def _set_opacity(self, input_opacity):
            """Set the opacity of the stored QPixmap image and display it"""
            #Store the opacity
            self.stored_opacity = input_opacity
            #Create and initialize the QImage from the stored QPixmap
            button_image = self.stored_pixmap
            hex_image = self.stored_hex
            image = data.PyQt.QtGui.QImage(
                hex_image.size(), 
                data.PyQt.QtGui.QImage.Format_ARGB32_Premultiplied
            )
            image.fill(data.PyQt.QtCore.Qt.transparent)
            #Create and initialize the QPainter that will manipulate the QImage
            button_painter = data.PyQt.QtGui.QPainter(image)
            button_painter.setOpacity(input_opacity)
            button_painter.drawPixmap(18, 13, button_image)
            button_painter.end()
            #Display the manipulated image
            self.setPixmap(data.PyQt.QtGui.QPixmap.fromImage(image))
        
        def _set_opacity_with_hex_edge(self, input_opacity):
            """Set the opacity of the stored QPixmap image and display it"""
            #Store the opacity
            self.stored_opacity = input_opacity
            #Create and initialize the QImage from the stored QPixmap
            button_image = self.stored_pixmap
            hex_image = self.stored_hex
            image = data.PyQt.QtGui.QImage(
                hex_image.size(), 
                data.PyQt.QtGui.QImage.Format_ARGB32_Premultiplied
            )
            image.fill(data.PyQt.QtCore.Qt.transparent)
            #Create and initialize the QPainter that will manipulate the QImage
            button_painter = data.PyQt.QtGui.QPainter(image)
            button_painter.setCompositionMode(data.PyQt.QtGui.QPainter.CompositionMode_Source)
            button_painter.setOpacity(input_opacity)
            button_painter.drawPixmap(0, 0, hex_image)
            button_painter.drawPixmap(18, 13, button_image)
            button_painter.end()
            #Display the manipulated image
            self.setPixmap(data.PyQt.QtGui.QPixmap.fromImage(image))
        
        def mousePressEvent(self, event):
            """Overloaded widget click event"""
            #Execute the superclass mouse click event first
            super().mousePressEvent(event)
            #Execute the function if it was initialized
            if self.function != None:
                try:
                    #Set focus to the last focused widget stored on the main form
                    if self.focus_last_widget == data.HexButtonFocus.TAB:
                        self.main_form.last_focused_widget.currentWidget().setFocus()
                    elif self.focus_last_widget == data.HexButtonFocus.WINDOW:
                        self.main_form.last_focused_widget.setFocus()
                    #Store the executed function for next cursor placement
                    self.main_form.view.last_executed_function_text = self.function_text
                    #Execute the buttons stored function
                    self.function()
                except:
                    traceback.print_exc()
                    message = "You need to focus one of the editor windows first!"
                    self.main_form.display.repl_display_message(
                        message, 
                        message_type=data.MessageType.ERROR
                    )
                #Close the function wheel
                self.parent.hide()
        
        def mouseMoveEvent(self, event):
            """Overloaded mouse move event"""
            super().mouseMoveEvent(event)
            if self.isEnabled() == True:
                self.highlight()
        
        def enterEvent(self, event):
            """Overloaded widget enter event"""
            super().enterEvent(event)
            #Bring the widget to the front of the Z-axis stack
            self.raise_()
            #Highlight the widget only if it's enabled
            if self.isEnabled() == True:
                self.highlight()
        
        def leaveEvent(self, event):
            """Overloaded widget leave event"""
            super().leaveEvent(event)
            #Dim the widget only if it's enabled
            if self.isEnabled() == True:
                self.dim()
        
        def dim(self, clear_hex_edge=False):
            """Set the buttons opacity to low and clear the function text"""
            #Set the opacity to low
            if clear_hex_edge == True:
                self._set_opacity(self.OPACITY_LOW)
            else:
                self._set_opacity_with_hex_edge(self.OPACITY_LOW)
            #Clear the text in the parent display label
            self.parent.display("", self.stored_font)
        
        def highlight(self):
            """Set the buttons opacity to high and display the buttons function text"""
            #Set the opacity to full
            self._set_opacity_with_hex_edge(self.OPACITY_HIGH)
            #Display the stored function text
            self.parent.display(self.function_text, self.stored_font)
    
    class DoubleButton(CustomButton):
        """
        A CustomButton with an extra button added to itself,
        used for when double functionality is needed, for example when
        a function has a version with or without a dialog window.
        """
        #The extra button reference
        parent                      = None
        main_form                   = None
        extra_button                = None
        extra_button_size_factor    = 1/3
        extra_button_position       = data.PyQt.QtCore.QPoint(0, 0)
        extra_button_stored_opacity = None
        extra_button_stored_pixmap  = None
        extra_button_function       = None
        extra_button_function_text  = None
        #Class constants
        OPACITY_LOW                 = 0.5
        OPACITY_HIGH                = 1.0
        
        def init_extra_button(self, 
                              parent, 
                              main_form, 
                              input_extra_pixmap, 
                              input_extra_function=None, 
                              input_extra_function_text=""):   
            #Store the parent and main form references
            self.parent     = parent
            self.main_form  = main_form
            #Initialize the extra button
            self.extra_button = data.QLabel(self)
            width   = int(self.geometry().width() * self.extra_button_size_factor)
            height  = int(self.geometry().height() * self.extra_button_size_factor)
            self.extra_button_position = data.PyQt.QtCore.QPoint(
                                            self.geometry().width()*2/3-width, 
                                            self.geometry().height()*1/4
                                         )
            rectangle   = data.PyQt.QtCore.QRect(self.extra_button_position, data.PyQt.QtCore.QSize(width, height))
            self.extra_button.setGeometry(rectangle)
            self.extra_button_stored_pixmap = input_extra_pixmap
            self.extra_button.setPixmap(input_extra_pixmap)
            self.extra_button.setScaledContents(True)
            #Store the function options
            self.extra_button_function      = input_extra_function
            self.extra_button_function_text = input_extra_function_text
            #Set the extra button opacity to low
            self._set_extra_button_opacity(self.OPACITY_LOW)
            #Overridden the extra buttons events
            self.extra_button.mousePressEvent   = self.extra_button_click
            self.extra_button.enterEvent        = self.extra_button_enter_event
            self.extra_button.leaveEvent        = self.extra_button_leave_event
        
        def extra_button_click(self, event):
            """mousePressEvent for the extra button"""
            #Execute the function if it was initialized
            if self.extra_button_function != None:
                try:
                    #Set focus to the last focused widget stored on the main form
                    if self.focus_last_widget == data.HexButtonFocus.TAB:
                        self.main_form.last_focused_widget.currentWidget().setFocus()
                    elif self.focus_last_widget == data.HexButtonFocus.WINDOW:
                        self.main_form.last_focused_widget.setFocus()
                    #Store the executed function for next cursor placement
                    self.main_form.view.last_executed_function_text = self.function_text
                    #Execute the buttons stored function
                    self.extra_button_function()
                except Exception as ex:
                    print(ex)
                    message = "You need to focus one of the editor windows first!"
                    self.main_form.display.repl_display_message(
                        message, 
                        message_type=data.MessageType.ERROR
                    )
                #Close the function wheel
                self.parent.hide()
        
        def extra_button_enter_event(self, event):
            """Overloaded widget enter event"""
            #Check if the button is enabled
            if self.isEnabled() == True:
                self._set_extra_button_opacity(self.OPACITY_HIGH)
                #Display the stored extra buttons function text
                extra_button_font = data.PyQt.QtGui.QFont(
                    'Courier', 
                    self.stored_font.pointSize()-2, 
                    weight=data.PyQt.QtGui.QFont.Bold
                )
                self.parent.display(
                    self.extra_button_function_text, 
                    extra_button_font
                )
        
        def extra_button_leave_event(self, event):
            """Overloaded widget enter event"""
            #Check if the button is enabled
            if self.isEnabled() == True:
                self._set_extra_button_opacity(self.OPACITY_LOW)
                #Clear the function text
                extra_button_font = data.PyQt.QtGui.QFont(
                    'Courier', 
                    self.stored_font.pointSize()-2, 
                    weight=data.PyQt.QtGui.QFont.Bold
                )
                self.parent.display(
                    "", 
                    extra_button_font
                )
        
        def extra_button_enable(self):
            """Hide and disable the extra button"""
            self.extra_button.setVisible(True)
            self.extra_button.setEnabled(True)
        
        def extra_button_disable(self):
            """Hide and disable the extra button"""
            self.extra_button.setVisible(False)
            self.extra_button.setEnabled(False)
            self._set_extra_button_opacity(self.OPACITY_LOW)
        
        def resizeEvent(self, event):
            """Overridden resize event"""
            #Execute the superclass resize function
            super().resizeEvent(event)
            #Update the extra button geometry
            width = int(self.geometry().width() * self.extra_button_size_factor)
            height = int(self.geometry().height() * self.extra_button_size_factor)
            rectangle   = data.PyQt.QtCore.QRect(
                            self.extra_button_position, 
                            data.PyQt.QtCore.QSize(width, height)
                          )
            self.extra_button.setGeometry(rectangle)
        
        def _set_extra_button_opacity(self, input_opacity):
            """Set the opacity of the extra button"""
            #Store the opacity
            self.extra_button_stored_opacity = input_opacity
            #Create and initialize the QImage from the stored QPixmap
            button_image = self.extra_button_stored_pixmap
            image = data.PyQt.QtGui.QImage(
                button_image.size(), 
                data.PyQt.QtGui.QImage.Format_ARGB32_Premultiplied
            )
            image.fill(data.PyQt.QtCore.Qt.transparent)
            #Create and initialize the QPainter that will manipulate the QImage
            button_painter = data.PyQt.QtGui.QPainter(image)
            button_painter.setOpacity(input_opacity)
            button_painter.drawPixmap(0, 0, button_image)
            button_painter.end()
            #Display the manipulated image
            self.extra_button.setPixmap(data.PyQt.QtGui.QPixmap.fromImage(image))

    #Class variables
    parent                  = None
    main_form               = None
    background_image        = None
    display_label           = None
    cursor_show_position    = None
    
    def __init__(self, parent=None, main_form=None):
        #Initialize the superclass
        super().__init__(parent)
        #Store the reference to the parent
        self.parent = parent
        #Store the reference to the main form
        self.main_form = main_form
        #Store the background image for sizing details
        self.background_image = data.PyQt.QtGui.QPixmap(
            os.path.join(
                data.resources_directory, 
                data.function_wheel_image
            )
        )
        #Set the background color
        self.setStyleSheet(
            "QGroupBox {" +
                "background-color: rgb(238, 238, 236);" +
                "border-image: url(" + data.resources_directory.replace("\\", "/") +
                "/various/function-wheel.png);" +
            "}"
        )
        self.setStyleSheet("background-color:transparent;")
        self.setStyleSheet("border:0;")
        #Setup the picture
        exco_picture    = data.PyQt.QtGui.QPixmap(
            os.path.join(
                data.resources_directory, 
                data.function_wheel_image
            )
        )
        self.picture    = data.QLabel(self)
        self.picture.setPixmap(exco_picture)
        self.picture.setGeometry(self.frameGeometry())
        self.picture.setScaledContents(True)
        self.layout = data.QGridLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(
            data.PyQt.QtCore.QMargins(0,0,0,0)
        )
        self.layout.addWidget(self.picture)
        self.setLayout(self.layout)
        
        #Initialize the display label that will display the function names
        #when the mouse cursor is over a function button
        self.display_label = data.QLabel(self)
        self.display_label.setGeometry(36, 448, 120, 50)
        font = data.PyQt.QtGui.QFont('Courier', 14)
        font.setBold(True)
        self.display_label.setFont(font)
        self.display_label.setAlignment(
            data.PyQt.QtCore.Qt.AlignHCenter | data.PyQt.QtCore.Qt.AlignVCenter
        )
        #Initialize all of the hex function buttons
        self._init_all_buttons()
        #Position the overlay to the center of the screen
        self.center(self.background_image.size())
        #Scale the function wheel size if needed
        self.scale(1, 1)
    
    def _init_all_buttons(self):
        """Function for calling all button initialization subroutines"""
        self._init_file_buttons()
        self._init_basic_buttons()
        self._init_advanced_buttons()
        self._init_system_view_buttons()
        self._init_repl_buttons()
        #Check the states of the hex function buttons
        self._check_hex_button_states()
    
    def _init_basic_buttons(self):
        #Alias the class references to shorten the names
        form    = self.main_form
        #Create the list from which the hex buttons will be constructed
        hex_button_list = [ 
            self.ButtonInfo(
                "button_line_cut", 
                (244, 0, 68, 60), 
                "tango_icons/edit-line-cut.png", 
                form.menubar_functions["line_cut"], 
                "Line Cut", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ), 
            self.ButtonInfo(
                "button_1", 
                (244, 52, 68, 60), 
                "tango_icons/edit-line-copy.png", 
                form.menubar_functions["line_copy"], 
                "Line Copy", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ), 
            self.ButtonInfo(
                "button_2", 
                (199, 26, 68, 60), 
                "tango_icons/edit-line-delete.png", 
                form.menubar_functions["line_delete"], 
                "Line Delete", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_3", 
                (199, 79, 68, 60), 
                "tango_icons/edit-line-transpose.png", 
                form.menubar_functions["line_transpose"], 
                "Line\nTranspose", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_4", 
                (154, 53, 68, 60), 
                "tango_icons/edit-line-duplicate.png", 
                form.menubar_functions["line_duplicate"], 
                "Line\nDuplicate", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_5", 
                (154, 106, 68, 60), 
                "tango_icons/edit-redo.png", 
                form.menubar_functions["redo"], 
                "Redo", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ), 
            self.ButtonInfo(
                "button_6", 
                (109, 79, 68, 60), 
                "tango_icons/edit-undo.png", 
                form.menubar_functions["undo"], 
                "Undo", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ), 
            self.ButtonInfo(
                "button_7", 
                (109, 26, 68, 60), 
                "tango_icons/delete-end-line_32x32.png", 
                form.menubar_functions["delete_end_of_line"], 
                "Delete line\nending", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ), 
            self.ButtonInfo(
                "button_8", 
                (63, 0, 68, 60), 
                "tango_icons/delete-start-line_32x32.png", 
                form.menubar_functions["delete_start_of_line"], 
                "Delete line\nbeginning", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ), 
            self.ButtonInfo(
                "button_goto_start", 
                (19, 26, 68, 60), 
                "tango_icons/goto-start.png", 
                form.menubar_functions["goto_to_start"], 
                "Goto Start", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ), 
            self.ButtonInfo(
                "button_goto_end", 
                (64, 54, 68, 60), 
                "tango_icons/goto-end.png", 
                form.menubar_functions["goto_to_end"], 
                "Goto End", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ), 
            self.ButtonInfo(
                "button_select_all", 
                (153, 0, 68, 60), 
                "tango_icons/edit-select-all.png", 
                form.menubar_functions["select_all"], 
                "Select All", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ), 
        ]
        self._create_hex_buttons_from_list(hex_button_list)
    
    def _init_advanced_buttons(self):
        #Alias the class references to shorten the names
        form    = self.main_form
        #Create the list from which the hex buttons will be constructed
        hex_button_list = [ 
            self.ButtonInfo(
                "button_find", 
                (514, 0, 68, 60), 
                "tango_icons/edit-find.png", 
                form.menubar_functions["special_find"], 
                "Find", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
                input_check_text_differ=True, 
            ), 
            self.ButtonInfo(
                "button_find_regex", 
                (514, 53, 68, 60), 
                "tango_icons/edit-find-re.png", 
                form.menubar_functions["special_regex_find"], 
                "Regex Find", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
                input_check_text_differ=True, 
            ),
            self.ButtonInfo(
                "button_13", 
                (469, 26, 68, 60), 
                "tango_icons/edit-find-replace.png", 
                form.menubar_functions["special_find_and_replace"], 
                "Find and\nReplace", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_14", 
                (469, 79, 68, 60), 
                "tango_icons/edit-find-replace-re.png", 
                form.menubar_functions["special_regex_find_and_replace"], 
                "Regex Find\nand Replace", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_goto_line", 
                (514, 104, 68, 60), 
                "tango_icons/edit-goto.png", 
                form.menubar_functions["special_goto_line"], 
                "Goto Line", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
                input_check_text_differ=True, 
            ),
            self.ButtonInfo(
                "button_16", 
                (469, 130, 68, 60), 
                "tango_icons/edit-indent-to-cursor.png", 
                form.menubar_functions["special_indent_to_cursor"], 
                "Indent to\ncursor", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_17", 
                (424, 53, 68, 60), 
                "tango_icons/edit-highlight.png", 
                form.menubar_functions["special_highlight"], 
                "Highlight", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_18", 
                (424, 104, 68, 60), 
                "tango_icons/edit-highlight-re.png", 
                form.menubar_functions["special_regex_highlight"], 
                "Regex\nHighlight", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_19", 
                (424, 155, 68, 60), 
                "tango_icons/edit-clear-highlights.png", 
                form.menubar_functions["special_clear_highlights"], 
                "Clear\nHighlights", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_20", 
                (379, 79, 68, 60), 
                "tango_icons/edit-replace-in-selection.png", 
                form.menubar_functions["special_replace_in_selection"], 
                "Replace in\nselection", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_21", 
                (379, 130, 68, 60), 
                "tango_icons/edit-replace-in-selection-re.png", 
                form.menubar_functions["special_regex_replace_in_selection"], 
                "Regex Replace\nin selection", 
                input_font=data.PyQt.QtGui.QFont(
                                    'Courier', 11, weight=data.PyQt.QtGui.QFont.Bold
                                ), 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_22", 
                (379, 182, 68, 60), 
                "tango_icons/edit-comment-uncomment.png", 
                form.menubar_functions["comment_uncomment"], 
                "Comment\nUncomment", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_23", 
                (334, 105, 68, 60), 
                "tango_icons/edit-replace-all.png", 
                form.menubar_functions["special_replace_all"], 
                "Replace All", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_24", 
                (334, 157, 68, 60), 
                "tango_icons/edit-replace-all-re.png", 
                form.menubar_functions["special_regex_replace_all"], 
                "Regex\nReplace All", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_25", 
                (334, 208, 68, 60), 
                "tango_icons/edit-autocompletion.png", 
                form.menubar_functions["toggle_autocompletions"], 
                "Toggle\nAutocompletions", 
                input_font=data.PyQt.QtGui.QFont(
                                    'Courier', 10, weight=data.PyQt.QtGui.QFont.Bold
                                ), 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_26", 
                (288, 131, 68, 60), 
                "tango_icons/edit-case-to-upper.png", 
                form.menubar_functions["special_to_uppercase"], 
                "Selection to\nUPPERCASE", 
                input_font=data.PyQt.QtGui.QFont(
                                    'Courier', 12, weight=data.PyQt.QtGui.QFont.Bold
                                ), 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_27", 
                (289, 183, 68, 60), 
                "tango_icons/edit-case-to-lower.png", 
                form.menubar_functions["special_to_lowercase"], 
                "Selection to\nlowercase", 
                input_font=data.PyQt.QtGui.QFont(
                                    'Courier', 12, weight=data.PyQt.QtGui.QFont.Bold
                                ), 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_node_tree", 
                (287, 234, 68, 60), 
                "tango_icons/edit-node-tree.png", 
                form.menubar_functions["create_node_tree"], 
                "Create/Reload\n Node Tree", 
                input_font=data.PyQt.QtGui.QFont(
                                    'Courier', 11, weight=data.PyQt.QtGui.QFont.Bold
                                ), 
                input_focus_last_widget=data.HexButtonFocus.TAB,  
                input_tool_tip=("Create a node tree from the currently\n" +
                                "selected document and display it in the\n" +
                                "upper window.\nSupported programming languages:\n" +
                                "- C\n- Nim\n- Python 3"), 
            ),
            self.ButtonInfo(
                "button_29", 
                (244, 156, 68, 60), 
                "tango_icons/view-refresh.png", 
                form.menubar_functions["reload_file"], 
                "Reload File", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_30", 
                (244, 208, 68, 60), 
                "tango_icons/edit-find-in-open-documents.png", 
                form.menubar_functions["special_find_in_open_documents"], 
                "Find in open\ndocuments", 
                input_font=data.PyQt.QtGui.QFont(
                                    'Courier', 12, weight=data.PyQt.QtGui.QFont.Bold
                                ), 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_31", 
                (244, 261, 68, 60), 
                "tango_icons/edit-replace-in-open-documents.png", 
                form.menubar_functions["special_find_replace_in_open_documents"], 
                "Find and Replace\nin open documents", 
                input_font=data.PyQt.QtGui.QFont(
                                    'Courier', 9, weight=data.PyQt.QtGui.QFont.Bold
                                ), 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_replace_all_in_open_documents", 
                (198, 234, 68, 60), 
                "tango_icons/edit-replace-all-in-open-documents.png", 
                form.menubar_functions["special_replace_all_in_open_documents"], 
                "Replace all in\nopen documents", 
                input_font=data.PyQt.QtGui.QFont(
                                    'Courier', 10, weight=data.PyQt.QtGui.QFont.Bold
                                ), 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_bookmark_toggle", 
                (198, 183, 68, 60), 
                "tango_icons/bookmark.png", 
                form.menubar_functions["bookmark_toggle"], 
                "Toggle\nBookmark", 
                input_font=data.PyQt.QtGui.QFont(
                                    'Courier', 14, weight=data.PyQt.QtGui.QFont.Bold
                                ), 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_toggle_wordwrap", 
                (424, 0, 68, 60), 
                "tango_icons/wordwrap.png", 
                form.menubar_functions["toggle_wordwrap"], 
                "Toggle\nWord Wrap", 
                input_font=data.PyQt.QtGui.QFont(
                                    'Courier', 14, weight=data.PyQt.QtGui.QFont.Bold
                                ), 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_toggle_lineendings", 
                (378, 26, 68, 60), 
                "tango_icons/view-line-end.png", 
                form.menubar_functions["toggle_line_endings"], 
                "Toggle\nLine Ending\nVisibility", 
                input_font=data.PyQt.QtGui.QFont(
                                    'Courier', 12, weight=data.PyQt.QtGui.QFont.Bold
                                ), 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
        ]
        self._create_hex_buttons_from_list(hex_button_list)
    
    def _init_file_buttons(self):
        #Alias the class references to shorten the names
        form    = self.main_form
        #Create the list from which the hex buttons will be constructed
        hex_button_list = [ 
            self.ButtonInfo(
                "button_new", 
                (19, 131, 68, 60), 
                "tango_icons/document-new.png", 
                form.file_create_new, 
                "Create new\ndocument", 
                input_focus_last_widget=data.HexButtonFocus.WINDOW, 
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_open", 
                (109, 182, 68, 60), 
                "tango_icons/document-open.png", 
                form.file_open, 
                "Open\ndocument", 
                input_focus_last_widget=data.HexButtonFocus.WINDOW, 
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_user_funcs_open", 
                (19, 182, 68, 60), 
                "tango_icons/file-user-funcs.png", 
                form.menubar_functions["open_user_func_file"], 
                "Edit User\nFunctions", 
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_user_funcs_reload", 
                (64, 154, 68, 60), 
                "tango_icons/file-user-funcs-reload.png", 
                form.menubar_functions["reload_user_func_file"], 
                "Reload User\nFunctions", 
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_save", 
                (19, 234, 68, 60), 
                "tango_icons/document-save.png", 
                form.file_save, 
                "Save", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
                input_no_document_focus_disable=True, 
                input_check_last_tab_type=True, 
            ),
            self.ButtonInfo(
                "button_save_as", 
                (64, 208, 68, 60), 
                "tango_icons/document-save-as.png", 
                form.file_saveas, 
                "Save As", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
                input_no_document_focus_disable=True, 
                input_check_last_tab_type=True, 
            ),
            self.ButtonInfo(
                "button_save_all", 
                (109, 234, 68, 60),
                "tango_icons/file-save-all.png", 
                form.file_save_all, 
                "Save All", 
                input_focus_last_widget=data.HexButtonFocus.WINDOW, 
                input_no_document_focus_disable=True, 
                input_check_last_tab_type=True, 
            ),
            
            self.ButtonInfo(
                "button_34", 
                (109, 285, 68, 60), 
                "tango_icons/close-all-tabs.png", 
                form.close_all_tabs, 
                "Close\nAll Tabs", 
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_35", 
                (64, 259, 68, 60), 
                "tango_icons/file-settings-save.png", 
                form.settings.save, 
                "Save\nsettings", 
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_36", 
                (19, 285, 68, 60), 
                "tango_icons/file-settings-load.png", 
                form.settings.restore, 
                "Load\nsettings", 
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_38", 
                (64, 311, 68, 60), 
                "tango_icons/help-browser.png", 
                form.view.show_about, 
                "Show Ex.Co.\nInformation", 
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_39", 
                (514, 468, 68, 60), 
                "tango_icons/system-log-out.png", 
                form.exit, 
                "Exit Ex.Co.", 
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_40", 
                (19, 338, 68, 60), 
                "tango_icons/themes-reload.png", 
                form.view.reload_themes, 
                "Reload\nThemes", 
                input_no_document_focus_disable=False, 
            ),
        ]
        self._create_hex_buttons_from_list(hex_button_list)
    
    def _init_system_view_buttons(self):
        #Alias the class references to shorten the names
        form    = self.main_form
        f_p     = functools.partial
        #Create the list from which the hex buttons will be constructed
        hex_button_list = [ 
            self.ButtonInfo(
                "button_43", 
                (469, 233, 68, 60), 
                "tango_icons/utilities-terminal.png", 
                form.menubar_functions["special_run_command"], 
                "Run Console\nCommand", 
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_44", 
                (469, 286, 68, 60), 
                "tango_icons/view-fullscreen.png", 
                form.view.toggle_window_size, 
                "Maximize/\nNormalize", 
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_45", 
                (424, 260, 68, 60), 
                "tango_icons/view-focus-main.png", 
                f_p(form.view.set_window_focus, "main"), 
                "Focus Main\nWindow", 
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_46", 
                (424, 312, 68, 60), 
                "tango_icons/view-focus-upper.png", 
                f_p(form.view.set_window_focus, "upper"), 
                "Focus Upper\nWindow", 
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_47", 
                (424, 364, 68, 60), 
                "tango_icons/view-focus-lower.png", 
                f_p(form.view.set_window_focus, "lower"), 
                "Focus Lower\nWindow", 
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_48", 
                (469, 338, 68, 60), 
                "tango_icons/view-log.png", 
                form.view.toggle_log_window, 
                "Show/Hide\nLog Window", 
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_49", 
                (379, 286, 68, 60), 
                "tango_icons/view-spin-clock.png", 
                form.view.spin_widgets_clockwise, 
                "Spin Windows\nClockwise", 
                input_focus_last_widget=False, 
                input_font=data.PyQt.QtGui.QFont(
                                'Courier', 12, weight=data.PyQt.QtGui.QFont.Bold
                            ), 
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_50", 
                (379, 338, 68, 60), 
                "tango_icons/view-spin-counter.png", 
                form.view.spin_widgets_counterclockwise, 
                "Spin Windows\nCounter\nClockwise",  
                input_focus_last_widget=False, 
                input_font=data.PyQt.QtGui.QFont(
                                'Courier', 10, weight=data.PyQt.QtGui.QFont.Bold
                            ), 
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_51", 
                (334, 363, 68, 60), 
                "tango_icons/view-toggle-window-mode.png", 
                form.view.toggle_window_mode, 
                "Toggle\nWindow Mode",  
                input_focus_last_widget=False, 
                input_font=data.PyQt.QtGui.QFont(
                                'Courier', 13, weight=data.PyQt.QtGui.QFont.Bold
                            ), 
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_52", 
                (334, 311, 68, 60), 
                "tango_icons/view-toggle-window-side.png", 
                form.view.toggle_main_window_side, 
                "Toggle\nWindow Side",  
                input_focus_last_widget=False, 
                input_font=data.PyQt.QtGui.QFont(
                                'Courier', 13, weight=data.PyQt.QtGui.QFont.Bold
                            ), 
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_move_tab_left", 
                (334, 415, 68, 60), 
                "tango_icons/view-move-tab-left.png", 
                form.menubar_functions["move_tab_left"], 
                "Move Tab\nLeft",
                input_focus_last_widget=data.HexButtonFocus.TAB, 
                input_no_tab_focus_disable=True,
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_move_tab_right", 
                (379, 389, 68, 60), 
                "tango_icons/view-move-tab-right.png", 
                form.menubar_functions["move_tab_right"], 
                "Move Tab\nRight", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
                input_no_tab_focus_disable=True,
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_close_tab", 
                (289, 441, 68, 60),
                "tango_icons/close-tab.png", 
                form.menubar_functions["close_tab"], 
                "Close Current\nTab", 
                input_font=data.PyQt.QtGui.QFont(
                                    'Courier', 11, weight=data.PyQt.QtGui.QFont.Bold
                                ), 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
                input_no_tab_focus_disable=True,
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_55", 
                (289, 389, 68, 60), 
                "tango_icons/view-edge-marker.png", 
                form.menubar_functions["show_edge"], 
                "Show/Hide\nEdge Marker", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_zoom_reset", 
                (289, 338, 68, 60), 
                "tango_icons/view-zoom-reset.png", 
                form.menubar_functions["reset_zoom"], 
                "Zoom Reset", 
                input_focus_last_widget=data.HexButtonFocus.TAB, 
            ),
            self.ButtonInfo(
                "button_find_files", 
                (514, 207, 68, 60), 
                "tango_icons/system-find-files.png", 
                form.menubar_functions["special_find_file"], 
                "Find Files",  
                input_no_document_focus_disable=False, 
                input_extra_button=["various/hex-button-dir-dialog.png", 
                                    form.menubar_functions["special_find_file_with_dialog"], 
                                    "Find Files\nwith dialog", 
                                    ],
            ),
            self.ButtonInfo(
                "button_find_in_files", 
                (514, 259, 68, 60), 
                "tango_icons/system-find-in-files.png", 
                form.menubar_functions["special_find_in"], 
                "Find in\nFiles", 
                input_no_document_focus_disable=False, 
                input_extra_button=["various/hex-button-dir-dialog.png", 
                                    form.menubar_functions["special_find_in_with_dialog"], 
                                    "Find in\nFiles with\ndialog", 
                                    ], 
            ),
            self.ButtonInfo(
                "button_replace_in_files", 
                (514, 311, 68, 60), 
                "tango_icons/system-replace-in-files.png", 
                form.menubar_functions["special_replace_in_files"], 
                "Replace all\nin Files", 
                input_no_document_focus_disable=False, 
                input_extra_button=["various/hex-button-dir-dialog.png", 
                                    form.menubar_functions["special_replace_in_files_with_dialog"], 
                                    "Replace all\nin Files\nwith dialog", 
                                    ],  
            ),
            self.ButtonInfo(
                "button_show_session_editor", 
                (514, 364, 68, 60), 
                "tango_icons/sessions-gui.png", 
                form.menubar_functions["show_session_editor"], 
                "Show Session\nEditor", 
                input_no_document_focus_disable=False,
                input_font=data.PyQt.QtGui.QFont(
                                    'Courier', 12, weight=data.PyQt.QtGui.QFont.Bold
                                ), 
            ),
            self.ButtonInfo(
                "button_cwd_tree", 
                (468, 390, 68, 60), 
                "tango_icons/system-show-cwd-tree.png", 
                form.menubar_functions["create_cwd_tree"], 
                "Show CWD\nFile/Directory\nTree", 
                input_font=data.PyQt.QtGui.QFont(
                                    'Courier', 10, weight=data.PyQt.QtGui.QFont.Bold
                                ), 
                input_focus_last_widget=data.HexButtonFocus.NONE, 
                input_tool_tip=("Create a file/directory tree for the " + 
                                "current working directory (CWD)"), 
                input_no_document_focus_disable=False,
            ),
            self.ButtonInfo(
                "button_bookmarks_clear", 
                (424, 415, 68, 60), 
                "tango_icons/bookmarks-clear.png", 
                form.menubar_functions["bookmarks_clear"], 
                "Clear All\nBookmarks", 
                input_font=data.PyQt.QtGui.QFont(
                                    'Courier', 14, weight=data.PyQt.QtGui.QFont.Bold
                                ), 
                input_focus_last_widget=data.HexButtonFocus.NONE, 
                input_no_document_focus_disable=False,
            ),
        ]
        self._create_hex_buttons_from_list(hex_button_list)
    
    def _init_repl_buttons(self):
        #Alias the class references to shorten the names
        form    = self.main_form
        #Create the list from which the hex buttons will be constructed
        hex_button_list = [ 
            self.ButtonInfo(
                "button_57", 
                (199, 338, 68, 60), 
                "tango_icons/repl-focus-single.png", 
                form.menubar_functions["repl_single_focus"], 
                "REPL Focus\n(Single Line)",  
                input_focus_last_widget=False, 
                input_font=data.PyQt.QtGui.QFont(
                                'Courier', 13, weight=data.PyQt.QtGui.QFont.Bold
                            ), 
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_58", 
                (199, 390, 68, 60), 
                "tango_icons/repl-focus-multi.png", 
                form.menubar_functions["repl_multi_focus"], 
                "REPL Focus\n(Multi Line)",  
                input_focus_last_widget=False, 
                input_font=data.PyQt.QtGui.QFont(
                                'Courier', 13, weight=data.PyQt.QtGui.QFont.Bold
                            ), 
                input_no_document_focus_disable=False, 
            ),
            self.ButtonInfo(
                "button_59", 
                (154, 364, 68, 60), 
                "tango_icons/repl-repeat-command.png", 
                form.repl.repeat_last_repl_eval, 
                "Repeat Last\nREPL Command",  
                input_focus_last_widget=False, 
                input_font=data.PyQt.QtGui.QFont(
                                'Courier', 13, weight=data.PyQt.QtGui.QFont.Bold
                            ), 
                input_no_document_focus_disable=False, 
            ),
        ]
        self._create_hex_buttons_from_list(hex_button_list)
    
    def _create_hex_buttons_from_list(self, hex_button_list):
        #Create all of the buttons from the list
        for button in hex_button_list:
            #Initialize the custom hex buttom
            if button.extra_button != None:
                init_button = self.DoubleButton(
                                self, 
                                self.main_form, 
                                input_pixmap=helper_forms.set_pixmap(button.pixmap), 
                                input_function=button.function, 
                                input_function_text=button.function_text, 
                                input_font=button.font, 
                                input_focus_last_widget=button.focus_last_widget, 
                                input_no_tab_focus_disable=button.no_tab_focus_disable, 
                                input_no_document_focus_disable=button.no_document_focus_disable, 
                                input_check_last_tab_type=button.check_last_tab_type, 
                                input_check_text_differ=button.check_text_differ, 
                                input_tool_tip=button.tool_tip, 
                            )
                init_button.init_extra_button(
                    self, 
                    self.main_form, 
                    helper_forms.set_pixmap(button.extra_button[0]), 
                    input_extra_function=button.extra_button[1],
                    input_extra_function_text=button.extra_button[2], 
                )
            else:
                init_button = self.CustomButton(
                                self, 
                                self.main_form, 
                                input_pixmap=helper_forms.set_pixmap(button.pixmap), 
                                input_function=button.function, 
                                input_function_text=button.function_text, 
                                input_font=button.font, 
                                input_focus_last_widget=button.focus_last_widget, 
                                input_no_tab_focus_disable=button.no_tab_focus_disable, 
                                input_no_document_focus_disable=button.no_document_focus_disable, 
                                input_check_last_tab_type=button.check_last_tab_type, 
                                input_check_text_differ=button.check_text_differ, 
                                input_tool_tip=button.tool_tip, 
                            )
            #Set the button size and location
            init_button.setGeometry(
                button.geometry[0], 
                button.geometry[1], 
                button.geometry[2], 
                button.geometry[3]
            )
    
    def _check_hex_button_states(self):
        """Check the hex function button states when displaying the function wheel"""
        for child_widget in self.children():
            #Skip the child widget if it is not a hex or double button
            if (isinstance(child_widget, self.CustomButton) == False and
                isinstance(child_widget, self.DoubleButton) == False):
                continue
            #First display and enable the hex button
            child_widget.setVisible(True)
            child_widget.setEnabled(True)
            if isinstance(child_widget, self.DoubleButton) == True:
                child_widget.extra_button_enable()
            #If the button needs to focus on the last focused widget,
            #check if the last focused widget is valid
            last_widget = self.main_form.last_focused_widget
            last_tab    = self.main_form.last_focused_tab
            result = False
            if last_widget != None and last_widget.count() != 0:
                result = True
            if result == False and child_widget.no_tab_focus_disable == True:
                #Disable if no tab is focused
                child_widget.setEnabled(False)
            elif result == False and child_widget.no_document_focus_disable == True:
                #If document focus is needed by the button, check if a tab is a focused document
                child_widget.setEnabled(False)
            elif (child_widget.no_document_focus_disable == True and
                 (isinstance(last_tab, CustomEditor) == False and
                  isinstance(last_tab, PlainEditor) == False)):
                #If focus is needed by the button, check the tab is an editing widget
                child_widget.setEnabled(False)
            elif (child_widget.check_last_tab_type == True and
                  isinstance(last_tab, CustomEditor) == False):
                #Check tab type for save/save_as/save_all buttons, it must be a CustomEditor
                child_widget.setEnabled(False)
            elif (child_widget.no_document_focus_disable == True and
                  hasattr(last_tab, "actual_parent") == True and
                  isinstance(last_tab.actual_parent, helper_forms.TextDiffer) == True):
                #Check if tab is a TextDiffer, enable only the supported functions
                if (child_widget.function_text != "Find" and
                    child_widget.function_text != "Regex Find" and
                    child_widget.function_text != "Goto Line" and
                    child_widget.function_text != "Move Tab\nLeft" and
                    child_widget.function_text != "Move Tab\nRight" and
                    child_widget.function_text != "Close Current\nTab"):
                    child_widget.setEnabled(False)
            #Call the dim method to draw the hex edge if the button is enabled
            if child_widget.isEnabled() == True:
                child_widget.dim()
            else:
                #Otherwise completley dim the button along with the hex edge
                child_widget.dim(clear_hex_edge=True)
    
    def hideEvent(self, event):
        """Overridden widget hide event"""
        #Set focus to the last focused widget stored on the main form
        last_widget = self.main_form.last_focused_widget
        if last_widget != None:
            if last_widget.currentWidget() != None:
                last_widget.currentWidget().setFocus()
    
    def display(self, string, font):
        """Display string in the display label"""
        #Setup additional font settings
        font.setBold(True)
        self.display_label.setFont(font)
        self.display_label.setAlignment(
            data.PyQt.QtCore.Qt.AlignHCenter | data.PyQt.QtCore.Qt.AlignVCenter
        )
        #Display the string
        self.display_label.setText(string)
    
    def hide(self):
        """Hide the function wheel overlay"""
        #First clear the hex edge from all of the buttons
        for child_widget in self.children():
            #Skip the child widget if it is not a hex or double button
            if (isinstance(child_widget, self.CustomButton) == False and
                isinstance(child_widget, self.DoubleButton) == False):
                continue
            #Dim the button and clear the hex edge
            child_widget.dim(clear_hex_edge=True)
            #Hide the button, fixes a leaveEvent issue with the "Open File" function.
            child_widget.setVisible(False)
            if isinstance(child_widget, self.DoubleButton) == True:
                child_widget.extra_button_disable()
        #Disable the function wheel
        self.setVisible(False)
        self.setEnabled(False)
    
    def show(self):
        """Show the function wheel overlay"""
        self.setVisible(True)
        self.setEnabled(True)
        #Refresh the states of the hex function buttons
        self._check_hex_button_states()
        #Center to main form
        self.center(self.size())
        #Set the cursor to the center of the last executed function, if any
        self.highlight_last_clicked_button()
        self.setFocus()
    
    def scale(self, width_scale_factor=1, height_scale_factor=1):
        """Scale the size of the function wheel and all of its child widgets"""
        #Scale the function wheel form
        geo = self.geometry()
        new_width = int(geo.width() * width_scale_factor)
        new_height = int(geo.height() * height_scale_factor)
        rectangle   = data.PyQt.QtCore.QRect(geo.topLeft(), data.PyQt.QtCore.QSize(new_width, new_height))
        self.setGeometry(rectangle)
        #Scale all of the function wheel child widgets
        for button in self.children():
            geo = button.geometry()
            new_topLeft = data.PyQt.QtCore.QPoint(
                            int(geo.topLeft().x() * width_scale_factor),
                            int(geo.topLeft().y() * height_scale_factor)
                          )
            new_width = int(geo.width() * width_scale_factor)
            new_height = int(geo.height() * height_scale_factor)
            new_size = data.PyQt.QtCore.QSize(new_width, new_height)
            rectangle   = data.PyQt.QtCore.QRect(new_topLeft, new_size)
            button.setGeometry(rectangle)
        #Center to main form
        self.center(self.size())
    
    def center(self, size):
        """
        Center the function wheel to the main form,
        according to the size parameter
        """
        x_offset = int((self.main_form.size().width() - size.width()) / 2)
        y_offset = int((self.main_form.size().height()*93/100 - size.height()) / 2)
        rectangle_top_left  = data.PyQt.QtCore.QPoint(x_offset, y_offset)
        rectangle_size      = size
        rectangle   = data.PyQt.QtCore.QRect(rectangle_top_left, rectangle_size)
        self.setGeometry(rectangle)
    
    def highlight_last_clicked_button(self):
        """Name says it all"""
        #Check if there is a stored button function
        last_function_text = self.main_form.view.last_executed_function_text
        if last_function_text == None:
            return
        #Loop through the buttons and check its function
        for button in self.children():
            if isinstance(button, self.CustomButton):
                #Compare the stored function text with the buttons function text
                if button.function_text == last_function_text:
                    #Only higlight the button if it is enabled
                    if button.isEnabled() == True:
                        button.highlight()
                    button_position = self.mapToGlobal(button.geometry().topLeft())
                    cursor = data.PyQt.QtGui.QCursor()
                    cursor.setPos(
                        button_position.x() + int(button.geometry().width()/2), 
                        button_position.y() + int(button.geometry().height()/2)
                    )
                    break



