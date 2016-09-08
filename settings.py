
# -*- coding: utf-8 -*-

"""
    Ex.Co. LICENSE :
        This file is part of Ex.Co..

        Ex.Co. is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        Ex.Co. is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with Ex.Co..  If not, see <http://www.gnu.org/licenses/>.


    PYTHON LICENSE :
        "Python" and the Python logos are trademarks or registered trademarks of the Python Software Foundation,
        used by Ex.Co. with permission from the Foundation


    Cython LICENSE:
        Cython is freely available under the open source Apache License


    PyQt4 LICENSE :
        PyQt4 is licensed under the GNU General Public License version 3
    PyQt Alternative Logo LICENSE:
        The PyQt Alternative Logo is licensed under Creative Commons CC0 1.0 Universal Public Domain Dedication


    Qt Logo LICENSE:
        The Qt logo is copyright of Digia Plc and/or its subsidiaries.
        Digia, Qt and their respective logos are trademarks of Digia Corporation in Finland and/or other countries worldwide.


    Tango Icons LICENSE:
        The Tango base icon theme is released to the Public Domain.
        The Tango base icon theme is made possible by the Tango Desktop Project.

    My Tango Style Icons LICENSE:
        The Tango Icons I created are released under the GNU General Public License version 3.
    
    
    Eric6 LICENSE:
        Eric6 IDE is licensed under the GNU General Public License version 3


    Nuitka LICENSE:
        Nuitka is a Python compiler compatible with Ex.Co..
        Nuitka is licensed under the Apache license.
"""


##  FILE DESCRIPTION:
##      Module used to save, load, ... settings of Ex.Co.

import os
import os.path
import platform
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
    settings_filename               = "exco_init.ini"
    settings_filename_with_path     = ""
    application_directory           = ""
    resources_directory             = "resources/"
    level_spacing                   = "    "
    recent_files                    = []
    stored_sessions                 = []
    main_window_side                = data.MainWindowSide.RIGHT
    theme                           = themes.Air
    
    empty_settings_list         =   [   
                                        "[General Settings]", 
                                        "    Main_Window_Side    Left", 
                                        "    Theme    Air",
                                        "",  
                                        "[Recent Files]", 
                                        "", 
                                        "[Sessions]", 
                                    ]
    
    def __init__(self,  app_dir, res_dir):
        #Assign the application directory
        self.application_directory  = app_dir
        self.resources_directory    = res_dir
        #Join the application directory with the settings filename
        self.settings_filename_with_path    = os.path.join(self.application_directory, self.settings_filename)
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
        settings_lines = ["[General Settings]"]
        #Save the main window side
        self.main_window_side = main_window_side
        if main_window_side == data.MainWindowSide.RIGHT:
            settings_lines.append("{:s}Main_Window_Side{:s}Right".format(
                    self.level_spacing, self.level_spacing
                )
            )
        else:
            settings_lines.append("{:s}Main_Window_Side{:s}Left".format(
                    self.level_spacing, self.level_spacing
                )
            )
        #Save the theme
        self.theme = theme
        settings_lines.append("{0}Theme{1}{2}".format(
                self.level_spacing, 
                self.level_spacing, 
                theme.__name__.split(".")[1]
            )
        )
        settings_lines.append("")
        #Save the recent files to list
        settings_lines.append("[Recent Files]")
        for file in self.recent_files:
            settings_lines.append("{:s}{:s}".format(self.level_spacing, file))
        settings_lines.append("")
        #Save the sessions to list
        settings_lines.append("[Sessions]")
        for session in self.stored_sessions:
            settings_lines.append("{:s}[{:s}]".format(self.level_spacing, session.name))
            #Store the group name if specified
            if session.group != None:
                settings_lines.append("{:s}{:s}".format(2*self.level_spacing, "[Group]"))
                settings_lines.append("{:s}{:s}".format(3*self.level_spacing, session.group))
            #Check if there are any main window files
            if session.main_files != []:
                #Add main window tag
                settings_lines.append("{:s}{:s}".format(2*self.level_spacing, "[Main]"))
                for file in session.main_files:
                    settings_lines.append("{:s}{:s}".format(3*self.level_spacing, file))
            #Check if there are any upper window files
            if session.upper_files != []:
                #Add upper window tag
                settings_lines.append("{:s}{:s}".format(2*self.level_spacing, "[Upper]"))
                for file in session.upper_files:
                    settings_lines.append("{:s}{:s}".format(3*self.level_spacing, file))
            #Check if there are any lower window files
            if session.lower_files != []:
                #Add lower window tag
                settings_lines.append("{:s}{:s}".format(2*self.level_spacing, "[Lower]"))
                for file in session.lower_files:
                    settings_lines.append("{:s}{:s}".format(3*self.level_spacing, file))
        #Save the file to disk
        self.create_settings_file(settings_lines)
    
    def load_settings(self):
        """Load all setting from the settings file"""
        settings_file_lines = functions.read_file_to_list(
            self.settings_filename_with_path
        )
        recent_files_start_line = 0
        sessions_start_line     = 0
        for i, line in enumerate(settings_file_lines):
            split_line = line.split()
            if "Main_Window_Side" in line:
                #Load main window side
                if split_line[1].lower() == "right":
                    self.main_window_side = data.MainWindowSide.RIGHT
                else:
                    self.main_window_side = data.MainWindowSide.LEFT
            elif  "Theme" in line:
                #Set the theme
                theme_string = split_line[1].lower()
                if theme_string == "air":
                    self.theme = themes.Air
                elif theme_string == "earth":
                    self.theme = themes.Earth
                elif theme_string == "water":
                    self.theme = themes.Water
            #Test if the first recent files line has been reached
            elif "[Recent Files]" in line:
                #Store the line that is the beggining of the recent file list
                recent_files_start_line = i + 1
                #Reset the recent file list
                self.recent_files = []
                #Loop to the line that doesn't have a indentation
                for j in range(recent_files_start_line, len(settings_file_lines)):
                    #Test if the last element was reached
                    if settings_file_lines[j].startswith(self.level_spacing) == False:
                        #Break from the loop
                        break
                    #Save the recent file
                    file = settings_file_lines[j]
                    file = file.lstrip()
                    file = file.replace("\n", "")
                    self.recent_files.append(file)
                    #Test if end of the file reached
                    if j == len(settings_file_lines)-1:
                        #Break from the loop
                        break
            #Test if the sessions line has been reached
            elif  "[Sessions]" in line:
                #Reset the stored sessions list
                self.stored_sessions = []
                #Store the line that is the beggining of the stored sessions list
                sessions_start_line     = i + 1
                current_session         = None
                #Read all of the stored sessions
                for j in range(sessions_start_line, len(settings_file_lines)):
                    ln = settings_file_lines[j]
                    #Test is the line contains a session name
                    if ln.startswith(self.level_spacing + "[") and "]" in ln:
                        #Save session name
                        current_session = Session(ln.strip().replace("[", "").replace("]", ""))
                        #Loop through the current session element, break if you reach the end of the file
                        loop_start = j + 1
                        group                   = False
                        current_window_name     = None
                        current_window_files    = None
                        for k in range(loop_start, len(settings_file_lines)):
                            ln_2 = settings_file_lines[k]
                            #Test if there is a 2-level indent and a window name
                            if ln_2.startswith(2*self.level_spacing + "[") and "]" in ln_2:
                                #Save the current window name to a reference
                                current_window_name = ln_2.strip().replace("[", "").replace("]", "")
                                if current_window_name.lower() == "main":
                                    current_window_files = current_session.main_files
                                    group = False
                                elif current_window_name.lower() == "upper":
                                    current_window_files = current_session.upper_files
                                    group = False
                                elif current_window_name.lower() == "lower":
                                    current_window_files = current_session.lower_files
                                    group = False
                                elif current_window_name.lower() == "group":
                                    group = True 
                                else:
                                    #Found an invalid window name, skip to the next session
                                    break
                            #Test if group name is active
                            elif group == True:
                                #Test if there is a 3-level indent
                                if 3*self.level_spacing in ln_2:
                                    current_session.group = ln_2.strip()
                            elif group == False:
                                #Test if there is a 3-level indent
                                if 3*self.level_spacing in ln_2:
                                    current_window_files.append(ln_2.strip())
                            #Test if we reached a new session or end of the file
                            if (ln_2.startswith(2*self.level_spacing) == False or
                                k == len(settings_file_lines)-1):
                                #Store the session to the list
                                self.stored_sessions.append(current_session)
                                #Break from the loop
                                break
                    #Test if we reached the last element or end of the file
                    if (ln.startswith(self.level_spacing) == False or
                        j == len(settings_file_lines)-1):
                        for s in self.stored_sessions:
                            data.print_log("Session: " + s.name)
                            data.print_log("    Window: Main")
                            for f in s.main_files:
                                data.print_log("        File: " + f)
                            data.print_log("    Window: Upper")
                            for f in s.upper_files:
                                data.print_log("        File: " + f)
                            data.print_log("    Window: Lower")
                            for f in s.lower_files:
                                data.print_log("        File: " + f)
                        #Break from the loop
                        break
        #Show the recent files in the log window
        data.print_log("Found recent files:")
        for file in self.recent_files:
            data.print_log("{:s}{:s}".format(self.level_spacing, file))

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
                self.save_settings(self.main_window_side)
                session_found = True
        #Check if the session was already found
        if session_found == False:
            #Add the session to the list
            self.stored_sessions.append(session)
            #Save the new settings
            self.save_settings(self.main_window_side)

    def remove_session(self, session_name, session_group=None):
        """Remove a session from the stored session list"""
        #Loop through the stored sessions
        for session in self.stored_sessions:
            #Check if the session names and groups match 
            if session.name == session_name and session_group == session.group:
                #Remove the session from the stored session list
                self.stored_sessions.remove(session)
                #Save the new settings
                self.save_settings(self.main_window_side)
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


