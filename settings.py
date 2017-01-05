
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2017 Matic Kukovec. 
Release under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""


##  FILE DESCRIPTION:
##      Module used to save, load, ... settings of Ex.Co.

import os
import os.path
import platform
import imp
import data
import themes
import functions


"""
-------------------------------------------
Structure for storing session information
-------------------------------------------
"""
class Session():
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


"""
-------------------------------------------
Object for manipulating settings/sessions
-------------------------------------------
"""
class SettingsFileManipulator():
    """Object that will be used for saving, loading, ... all of the Ex.Co. settings """
    #Class variables
    settings_filename               = "exco.ini"
    settings_filename_with_path     = ""
    application_directory           = ""
    resources_directory             = "resources/"
    level_spacing                   = "    "
    recent_files                    = []
    stored_sessions                 = []
    main_window_side                = data.MainWindowSide.RIGHT
    theme                           = themes.Air
    
    empty_settings_list = [   
        "# Needed imports", 
        "import themes", 
        "",
        "# General Settings",  
        "main_window_side = 0", 
        "theme = themes.Air", 
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
    
    def save_settings(self, main_window_side, theme):
        """Save all settings to the settings file"""
        settings_lines = []
        settings_lines.append("# Needed imports")
        settings_lines.append("import themes")
        settings_lines.append("")
        settings_lines.append("# General Settings")
        settings_lines.append("main_window_side = {}".format(main_window_side))
        settings_lines.append("theme = themes.{}".format(data.theme.__name__))
        settings_lines.append("")
        settings_lines.append("# Recent files")
        settings_lines.append("recent_files = [")
        for file in self.recent_files:
            settings_lines.append("    '{}',".format(file))
        settings_lines.append("]")
        settings_lines.append("")
        settings_lines.append("# Sessions")
        settings_lines.append("sessions = {")
        for session in self.stored_sessions:
            settings_lines.append("    '{}': {{".format(session.name))
            settings_lines.append("        'Group': {},".format(repr(session.group)))
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
    
    def load_settings(self):
        """Load all setting from the settings file"""
        # Import the init file as a python module
        init_module = imp.load_source(
            self.settings_filename, 
            self.settings_filename_with_path
        )
        # Main window side
        self.main_window_side = init_module.main_window_side
        # Theme
        self.theme = init_module.theme
        # Recent files
        self.recent_files = init_module.recent_files
        # Sessions
        self.stored_sessions = []
        for session in init_module.sessions:
            current_session = Session(session)
            current_session.group = init_module.sessions[session]['Group']
            current_session.main_files = init_module.sessions[session]['Main window files']
            current_session.upper_files = init_module.sessions[session]['Upper window files']
            current_session.lower_files = init_module.sessions[session]['Lower window files']
            self.stored_sessions.append(current_session)

    def add_session(self, session_name, session_group, main_files, upper_files, lower_files):
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
                self.save_settings(self.main_window_side, self.theme)
                session_found = True
        #Check if the session was already found
        if session_found == False:
            #Add the session to the list
            self.stored_sessions.append(session)
            #Save the new settings
            self.save_settings(self.main_window_side, self.theme)

    def remove_session(self, session_name, session_group=None):
        """Remove a session from the stored session list"""
        #Loop through the stored sessions
        for session in self.stored_sessions:
            #Check if the session names and groups match 
            if session.name == session_name and session_group == session.group:
                #Remove the session from the stored session list
                self.stored_sessions.remove(session)
                #Save the new settings
                self.save_settings(self.main_window_side, self.theme)
                return True
        #Signal that the session was not removed
        return False

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
        #Replace back-slashes to forward-slashes on Windows
        if platform.system() == "Windows":
            new_file    = new_file.replace("\\", "/")
        #Check recent files list length
        while len(self.recent_files) > 10:
            #The recent files list is to long
            self.recent_files.pop(0)
        #Check if he new file is already in the list
        if new_file in self.recent_files:
            #Remove the old file with the same name as the new file from the list
            self.recent_files.pop(self.recent_files.index(new_file))
            #Add the new file to the end of the list
            self.recent_files.append(new_file)
        else:
            #The new file is not in the list, append it to the end of the list
            self.recent_files.append(new_file)
        #Save the new settings
        self.save_settings(self.main_window_side, data.theme)


