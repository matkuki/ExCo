
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2018 Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""


##  FILE DESCRIPTION:
##      Module used to save, load, ... settings of Ex.Co.

import os
import os.path
import runpy
import data
import themes
import functions


"""
----------------------------------------------------------------
Static Object for storing default editor settings that are used
when a new editor is created
----------------------------------------------------------------
"""
class Editor:
    """
    These are the built-in defaults, attributes should be changed
    in other modules!
    """
    # Default EOL style in editors (EolWindows-CRLF, EolUnix-LF, EolMac-CR)
    end_of_line_mode = data.QsciScintilla.EolUnix
    # Font colors and styles
    font = data.QFont('Courier', 10)
    brace_color = data.QColor(255, 153, 0)
    comment_font = b'Courier'
    # Edge marker
    edge_marker_color = data.QColor(180, 180, 180, alpha=255)
    edge_marker_column = 90
    # Various
    cursor_line_visible = False
    # Maximum limit of highlighting instances
    maximum_highlights = 300
    # Global width of tabs
    tab_width = 4
    # Zoom factor when a new editor is created (default is 0)
    zoom_factor = 0
    """
    -------------------------------------------
    Keyboard shortcuts
    -------------------------------------------
    """
    class Keys:
        # Custom editor commands
        copy = 'Ctrl+C'
        cut = 'Ctrl+X'
        paste = 'Ctrl+V'
        undo = 'Ctrl+Z'
        redo = 'Ctrl+Y'
        select_all = 'Ctrl+A'
        indent = 'Tab'
        unindent = 'Shift+Tab'
        delete_start_of_word = 'Ctrl+BackSpace'
        delete_end_of_word = 'Ctrl+Delete'
        delete_start_of_line = 'Ctrl+Shift+BackSpace'
        delete_end_of_line = 'Ctrl+Shift+Delete'
        go_to_start = 'Ctrl+Home'
        go_to_end = 'Ctrl+End'
        select_page_up = 'Shift+PageUp'
        select_page_down = 'Shift+PageDown'
        select_to_start = 'Ctrl+Shift+Home'
        select_to_end = 'Ctrl+Shift+End'
        scroll_up = 'PageUp'
        scroll_down = 'PageDown'
        line_cut = 'Ctrl+L'
        line_copy = 'Ctrl+Shift+T'
        line_delete = 'Ctrl+Shift+L'
        line_transpose = 'Ctrl+T'
        line_selection_duplicate = 'Ctrl+D'
        
        @staticmethod
        def check_function(function_name):
            check_list = [x for x in dir(Editor.Keys) if not x.startswith('__')]
            return function_name in check_list
        
        @staticmethod
        def check_combination(combination):
            if combination.startswith("#"):
               combination = combination[1:] 
            check_list = [
                (x, getattr(Editor.Keys, x)) 
                    for x in dir(Editor.Keys) 
                        if not x.startswith('__')
            ]
            for name, keys in check_list:
                if not(isinstance(keys, str)) and not(isinstance(keys, list)):
                    continue
                if isinstance(combination, list):
                    if isinstance(keys, list):
                        for k in keys:
                            for c in combination:
                                if k.strip().lower() == c.strip().lower():
                                    return True
                    else:
                        for c in combination:
                            if keys.strip().lower() == c.strip().lower():
                                return True
                elif isinstance(keys, str):
                    if keys.strip().lower() == combination.strip().lower():
                        return True
            return False


"""
-------------------------------------------
General keyboard shortcuts
-------------------------------------------
"""
class Keys:
    bookmark_goto = [
        "Alt+0", "Alt+1", "Alt+2", "Alt+3", "Alt+4", 
        "Alt+5", "Alt+6", "Alt+7", "Alt+8", "Alt+9",
    ]
    bookmark_store = [
        "Alt+Shift+0", "Alt+Shift+1", "Alt+Shift+2", "Alt+Shift+3", 
        "Alt+Shift+4", "Alt+Shift+5", "Alt+Shift+6", "Alt+Shift+7", 
        "Alt+Shift+8", "Alt+Shift+9",
    ]
    bookmark_toggle = "Ctrl+B"
    clear_highlights = 'Ctrl+Shift+G'
    close_tab = 'Ctrl+W'
    cwd_tree = 'F7'
    new_cwd_tree = 'Ctrl+F7'
    cwd_explorer = 'Alt+F7'
    find = 'Ctrl+F'
    find_and_replace = 'Ctrl+Shift+F'
    find_files = 'Ctrl+F1'
    find_in_documents = 'Ctrl+F4'
    find_in_files = 'Ctrl+F2'
    find_replace_in_documents = 'Ctrl+F5'
    function_wheel_toggle = 'F1'
    goto_line = 'Ctrl+M'
    highlight = 'Ctrl+G'
    indent_to_cursor = 'Ctrl+I'
    lower_focus = 'Ctrl+3'
    main_focus = 'Ctrl+1'
    maximize_window = 'F12'
    move_tab_left = 'Ctrl+,'
    move_tab_right = 'Ctrl+.'
    new_file = 'Ctrl+N'
    node_tree = 'F8'
    open_file = 'Ctrl+O'
    regex_find = 'Alt+F'
    regex_find_and_replace = 'Alt+Shift+F'
    regex_highlight = 'Alt+G'
    regex_replace_all = 'Alt+Shift+H'
    regex_replace_selection = 'Alt+H'
    reload_file = 'F9'
    repeat_eval = 'F3'
    repl_focus_multi = 'Ctrl+5'
    repl_focus_single_1 = 'Ctrl+R'
    repl_focus_single_2 = 'Ctrl+4'
    replace_all = 'Ctrl+Shift+H'
    replace_all_in_documents = 'Ctrl+F6'
    replace_in_files = 'Ctrl+F3'
    replace_selection = 'Ctrl+H'
    reset_zoom = "Alt+Z"
    save_file = 'Ctrl+S'
    saveas_file = 'Ctrl+Shift+S'
    spin_clockwise = 'Ctrl+PgDown'
    spin_counterclockwise = 'Ctrl+PgUp'
    to_lowercase = 'Alt+L'
    to_uppercase = 'Alt+U'
    toggle_autocompletion = 'Ctrl+K'
    toggle_comment = 'Ctrl+Shift+C'
    toggle_edge = 'Ctrl+E'
    toggle_log = 'F10'
    toggle_main_window_side = 'F6'
    toggle_mode = 'F5'
    toggle_wrap = 'Ctrl+P'
    upper_focus = 'Ctrl+2'
    
    @staticmethod
    def check_function(function_name):
        check_list = [
            x for x in dir(Keys) 
                if not x.startswith('__')
        ]
        return function_name in check_list
    
    @staticmethod
    def check_combination(combination):
        check_list = [
            (x, getattr(Keys, x)) 
                for x in dir(Keys) 
                    if not x.startswith('__')
        ]
        for name, keys in check_list:
            if not(isinstance(keys, str)) and not(isinstance(keys, list)):
                continue
            if isinstance(combination, list):
                if isinstance(keys, list):
                    for k in keys:
                        for c in combination:
                            if k.strip().lower() == c.strip().lower():
                                return True
                else:
                    for c in combination:
                        if keys.strip().lower() == c.strip().lower():
                            return True
            elif isinstance(keys, str):
                if keys.strip().lower() == combination.strip().lower():
                    return True
        return False


"""
-------------------------------------------
Structure for storing session information
-------------------------------------------
"""
class Session:
    """Structure for storing single session information"""
    name        = ""
    group       = None
    main_files  = []
    upper_files = []
    lower_files = []
    def __init__(self, name):
        """Session initialization"""
        #Initialization of class variables turns them into instance variables
        self.name           = name
        self.group          = None
        self.main_files     = []
        self.upper_files    = []
        self.lower_files    = []
    
    @staticmethod
    def parse(session_dict):
        """
        Parse a session dictionary into a session object.
        Example dictionary:
            
            'application': {
                'Group': ('embedoffice',),
                'Main window files': [
                    'D:/embedoffice_stuff/embedoffice/data.py',
                    'D:/embedoffice_stuff/embedoffice/embedoffice.py',
                    'D:/embedoffice_stuff/embedoffice/gui/forms/mainwindow.py',
                    'D:/embedoffice_stuff/embedoffice/gui/forms/basicwidget.py',
                    'D:/embedoffice_stuff/embedoffice/gui/helpers/projectdisplay.py',
                    'D:/embedoffice_stuff/embedoffice/project/project.py',
                    'D:/embedoffice_stuff/embedoffice/gui/helpers/projectwizard.py',
                    'D:/embedoffice_stuff/embedoffice/gui/helpers/buttons.py',
                    'D:/embedoffice_stuff/embedoffice/components/hexbuilding.py',
                    'D:/embedoffice_stuff/embedoffice/components/hexpainting.py',
                ],
                'Upper window files': [
                ],
                'Lower window files': [
                ],
            },
        """
        session = Session(session)
        session.group = in_sessions[session]['Group']
        session.main_files = in_sessions[session]['Main window files']
        session.upper_files = in_sessions[session]['Upper window files']
        session.lower_files = in_sessions[session]['Lower window files']


"""
-------------------------------------------
Object for manipulating settings/sessions
-------------------------------------------
"""
class SettingsFileManipulator:
    """
    Object that will be used for saving, loading, ... all of the Ex.Co. settings
    """
    #Class variables
    settings_filename               = "exco.ini"
    settings_filename_with_path     = ""
    application_directory           = ""
    resources_directory             = "resources/"
    level_spacing                   = "    "
    max_number_of_recent_files      = 10
    recent_files                    = []
    stored_sessions                 = []
    context_menu_functions          = {}
    error_lock                      = False
    # General settings
    main_window_side                = data.MainWindowSide.RIGHT
    theme                           = themes.Air
    
    empty_settings_list = [
        "# General Settings",  
        "main_window_side = 0", 
        "theme = themes.Air",
        "",
        "# Custom context menu functions", 
        "context_menu_functions = {}",
        "",
        "# Recent files", 
        "recent_files = []", 
        "", 
        "# Sessions", 
        "sessions = {}", 
    ]
    
    def __init__(self, app_dir, res_dir):
        #Assign the application directory
        self.application_directory  = app_dir
        self.resources_directory    = res_dir
        #Join the application directory with the settings filename
        self.settings_filename_with_path = os.path.join(
            self.application_directory, 
            self.settings_filename
        )
        #Check if the settings file exists
        if self.check_settings_file() == None:
            #Create the settings file
            self.create_settings_file(self.empty_settings_list)
        #Load the settings from the settings file
        self.load_settings()
    
    def check_settings_file(self):
        """Check if the settings file exists"""
        return functions.test_text_file(self.settings_filename_with_path)
    
    def create_settings_file(self, list_of_lines):
        """Create the settings file"""
        #Create/truncate settings file
        file = open(self.settings_filename_with_path, "w", encoding="utf-8")
        #Write the default settings string into the empty settings file
        for line in list_of_lines:
            file.write(line + "\n")
        #Close the file handle
        file.close()
    
    def _parse_sessions(self, in_sessions):
        parsed_sessions = []
        for session in in_sessions:
            current_session = Session(session)
            current_session.group = in_sessions[session]['Group']
            current_session.main_files = in_sessions[session]['Main window files']
            current_session.upper_files = in_sessions[session]['Upper window files']
            current_session.lower_files = in_sessions[session]['Lower window files']
            parsed_sessions.append(current_session)
        return parsed_sessions
    
    def write_settings_file(self,
                            main_window_side,
                            theme,
                            recent_files,
                            stored_sessions,
                            context_menu_functions):
        settings_lines = []
        settings_lines.append("# General Settings")
        settings_lines.append("main_window_side = {}".format(main_window_side))
        settings_lines.append("theme = {}".format(theme.__name__))
        settings_lines.append("")
        # Recent file list
        settings_lines.append("# Recent files")
        settings_lines.append("recent_files = [")
        for file in recent_files:
            settings_lines.append("    '{}',".format(file))
        settings_lines.append("]")
        settings_lines.append("")
        # Custom context menu functions
        settings_lines.append("# Custom context menu functions")
        settings_lines.append("context_menu_functions = {")
        for func_type in context_menu_functions:
            settings_lines.append("    '{}': {{".format(func_type))
            for func in context_menu_functions[func_type]:
                settings_lines.append("        {}: '{}',".format(
                    func, context_menu_functions[func_type][func])
                )
            settings_lines.append("    },")
        settings_lines.append("}")
        settings_lines.append("")
        # Sessions
        settings_lines.append("# Sessions")
        settings_lines.append("sessions = {")
        for session in stored_sessions:
            settings_lines.append("    '{}': {{".format(session.name))
            if isinstance(session.group, str) or (session.group == None):
                settings_lines.append("        'Group': {},".format(repr(session.group)))
            elif isinstance(session.group, tuple) and all([isinstance(x, str) for x in session.group]):
                settings_lines.append("        'Group': {},".format(str(session.group)))
            else:
                print("'{}'".format(repr(session.name)))
                raise Exception("[SETTINGS] Unknown session group type!")
            settings_lines.append("        'Main window files': [")
            for file in session.main_files:
                settings_lines.append("            '{}',".format(file))
            settings_lines.append("        ],")
            settings_lines.append("        'Upper window files': [")
            for file in session.upper_files:
                settings_lines.append("            '{}',".format(file))
            settings_lines.append("        ],")
            settings_lines.append("        'Lower window files': [")
            for file in session.lower_files:
                settings_lines.append("            '{}',".format(file))
            settings_lines.append("        ],")
            settings_lines.append("    },")
        settings_lines.append("}")
        #Save the file to disk
        self.create_settings_file(settings_lines)
    
    def save_settings(self, 
                      main_window_side, 
                      theme,
                      context_menu_functions=None):
        """Save all settings to the settings file"""
        if self.error_lock == True:
            return
        if context_menu_functions == None:
            context_menu_functions = self.context_menu_functions
        else:
            self.context_menu_functions = context_menu_functions
        self.write_settings_file(
            main_window_side,
            theme,
            self.recent_files,
            self.stored_sessions,
            context_menu_functions
        )
    
    def update_recent_files(self):
        """Update only the recent file list in settings file"""
        if self.error_lock == True:
            return
        # Import the init file as a python module
        init_module = runpy.run_path(
            self.settings_filename_with_path,
            init_globals = {"themes": themes, "data": data}
        )
        # Update only the recent file list
        stored_sessions = self._parse_sessions(init_module["sessions"])
        # Save the updated settings
        self.write_settings_file(
            init_module["main_window_side"],
            init_module["theme"],
            self.recent_files,
            stored_sessions,
            self.context_menu_functions
        )
    
    def load_settings(self):
        """Load all setting from the settings file"""
        try:
            # Import the init file as a python module
            init_module = runpy.run_path(
                self.settings_filename_with_path,
                init_globals = {"themes": themes, "data": data}
            )
            # Main window side
            self.main_window_side = init_module["main_window_side"]
            # Theme
            self.theme = init_module["theme"]
            # Recent files
            self.recent_files = init_module["recent_files"]
            # Sessions
            self.stored_sessions = self._parse_sessions(init_module["sessions"])
            # Load custom context menu functions
            if "context_menu_functions" in init_module.keys():
                self.context_menu_functions = init_module["context_menu_functions"]
            else:
                self.context_menu_functions = {}
            # Return success
            return True
        except:
            # Set the default settings values
            self.main_window_side = data.MainWindowSide.LEFT
            self.theme = themes.Air
            self.recent_files = []
            self.stored_sessions = []
            self.context_menu_functions = {}
            # Set the error flag
            self.error_lock = True
            # Return error
            return False
        

    def add_session(self, 
                    session_name, 
                    session_group, 
                    main_files, 
                    upper_files, 
                    lower_files):
        """Add a new session to the stored session list"""
        #Create the new session object
        session = Session(session_name)
        #Store the group name
        session.group = session_group
        #Add the files to the session
        session.main_files.extend(main_files)
        session.upper_files.extend(upper_files)
        session.lower_files.extend(lower_files)
        #Check if a session with the same name is already in the stored sessions list
        session_found = False
        for i, s in enumerate(self.stored_sessions):
            #Check if the session names and groups match 
            if s.name == session_name and s.group == session_group:
                #Replace the session
                self.stored_sessions[i] = session
                #Save the new settings
                self.save_settings(
                    self.main_window_side, self.theme
                )
                session_found = True
        #Check if the session was already found
        if session_found == False:
            #Add the session to the list
            self.stored_sessions.append(session)
            #Save the new settings
            self.save_settings(self.main_window_side, self.theme)

    def remove_session(self, session_name, session_group=None):
        """
        Remove a session from the stored session list
        """
        # Loop through the stored sessions
        for session in self.stored_sessions:
            # Check if the session names and groups match 
            if session.name == session_name and session_group == session.group:
                # Remove the session from the stored session list
                self.stored_sessions.remove(session)
                # Save the new settings
                self.save_settings(self.main_window_side, self.theme)
                return True
        # Signal that the session was not removed
        return False
    
    def remove_group(self, remove_group):
        """
        Remove an entire group from the stored session list
        """
        found_group = False
        filtered_sessions = []
        for i, session in enumerate(self.stored_sessions):
            if session.group != remove_group:
                filtered_sessions.append(session)
            else:
                found_group = True
        if found_group == True:
            # Overwrite the old session list
            self.stored_sessions = filtered_sessions
            # Save the new settings
            self.save_settings(self.main_window_side, self.theme)
            # Signal that the session was not removed
        return found_group

    def get_session(self, session_name, session_group=None):
        """Return the session from the stored sessions list if it exists"""
        for session in self.stored_sessions:
            #Check if the session names match 
            if session.name == session_name and session.group == session_group:
                #Return the session
                return session
        #Return None if session was not found
        return None
    
    def sort_sessions(self):
        """Sort the stored sessions alphabetically by name"""
        #Nested function for retrieving the sessions name attribute case insensitively
        def get_case_insensitive_name(item):
            name = item.name
            return name.lower()
        #Sort the stored sessions
        self.stored_sessions.sort(key=get_case_insensitive_name)

    def add_recent_file(self, new_file):
        """Add a new file to the recent file list"""
        # Replace back-slashes to forward-slashes on Windows
        if data.platform == "Windows":
            new_file = new_file.replace("\\", "/")
        # Check recent files list length
        while len(self.recent_files) > self.max_number_of_recent_files:
            # The recent files list is to long
            self.recent_files.pop(0)
        # Check if he new file is already in the list
        if new_file in self.recent_files:
            # Check if the file is already at the top
            if self.recent_files.index(new_file) == (self.max_number_of_recent_files-1):
                return
            # Remove the old file with the same name as the new file from the list
            self.recent_files.pop(self.recent_files.index(new_file))
            # Add the new file to the end of the list
            self.recent_files.append(new_file)
        else:
            # The new file is not in the list, append it to the end of the list
            self.recent_files.append(new_file)
        # Save the new settings
        self.update_recent_files()
    
    """
    Session group functionality
    """
    class Group:
        def __init__(self, name, parent=None, reference=None):
            self.name = name
            self.reference = reference
            self.parent = parent
            self.items = {}
            self.subgroups = {}
        
        def subgroup_get(self, name):
            if name in self.subgroups.keys():
                return self.subgroups[name]
            else:
                return None
        
        def subgroup_get_recursive(self, group_list):
            name = group_list[0]
            if name in self.subgroups.keys():
                if len(group_list) > 1:
                    return self.subgroups[name].subgroup_get_recursive(group_list[1:])
                else:
                    return self.subgroups[name]
            else:
                return None
        
        def subgroup_create(self, name, reference):
            if not(name in self.subgroups.keys()):
                # Create an instance of the same class as self
                self.subgroups[name] = self.__class__(name, self, reference)
            return self.subgroups[name]
    
    def get_sorted_groups(self):
        groups = []
        # Sort the sessions
        self.sort_sessions()
        # Add the groups to the menu first
        for session in self.stored_sessions:
            if session.group != None:
                if isinstance(session.group, str):
                    session.group = (session.group, )
                group_found = False
                for group in groups:
                    if session.group == group:
                        # Group found, it's already in the list
                        group_found = True
                        break
                if group_found == False:
                    # Group is not in the list, add it as a tuple (name, reference)
                    groups.append(session.group)
        # Sort the group list and add the groups to the session menu
        def sort_groups_func(arg=None):
            if isinstance(arg, tuple) and all([isinstance(x, str) for x in arg]):
                lowercase_group_tree = [x.lower() for x in arg]
                return " ".join(lowercase_group_tree)
            else:
                return arg.lower()
        groups.sort(key=sort_groups_func)
        return groups


