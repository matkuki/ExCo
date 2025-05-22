"""
Copyright (c) 2013-present Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""


##  FILE DESCRIPTION:
##      Module used to save, load, ... settings of Ex.Co.

import os
import os.path
import json
import traceback
import data
import themes
import settings.constants
import settings.functions
try:
    import settings.old.settings as oldsettings
    OLD_SETTINGS_IMPORTED = True
except:
    OLD_SETTINGS_IMPORTED = False
import functions


# Editor settings
editor = settings.constants.editor["default"].copy()
# Keyboard shortcuts
keyboard_shortcuts = settings.constants.keyboard_shortcuts["default"].copy()
# Variables
variables = {
    "open-new-files-in-open-instance": False,
    "max-number-of-recent-files": 100,
}

"""
-------------------------------------------
Object for manipulating settings/sessions
-------------------------------------------
"""
class SettingsFileManipulator:
    """
    Object that will be used for saving, loading, ... all of the Ex.Co. settings
    """
    LAST_LAYOUT_FILENAME = "last_layout.json"
    
    settings_filename_with_path = None
    directories = {
        "application": None,
        "resources": None,
    }
    recent_files = []
    stored_sessions = {}
    context_menu_functions = {}
    error_lock = False
    # General settings
    theme = None
    data_variables = (
        "terminal",
        "tree_display_icon_size",
        "current_font_name",
        "current_font_size",
        "current_editor_font_name",
        "current_editor_font_size",
        "toplevel_menu_scale",
        "restore_last_session",
    )
    
    def __init__(self):
        # Assign the application directory
        self.directories["application"] = data.application_directory
        self.directories["resources"] = data.resources_directory
        # Create the settings file path
        functions.create_directory(data.settings_directory)
        self.settings_filename_with_path = functions.unixify_join(
            data.settings_directory,
            data.settings_filename["mark-2"]
        )
        # Initialize an empty sessions list
        self.stored_sessions = {
            "main": self.create_empty_session_group()
        }
        # Check if the settings file exists
        if self.check_settings_file() == None:
            old_files = {}
            for k,v in data.settings_filename.items():
                old_files[k] = settings_filename_with_path = functions.unixify_join(
                    data.settings_directory,
                    v
                )
            if os.path.isfile(old_files["mark-1"]):
                # Convert MK-I setting file to to MK-II
                self.settings_filename_with_path = old_files["mark-1"]
                self.load_settings()
                def recurse_groups(item):
                    # Sessions
                    if "sessions" in item.keys():
                        for k,v in item["sessions"].items():
                            new_session = {
                                "name": v["name"],
                                "chain": v["chain"],
                                "layout": None,
                            }
                            layout = json.loads(settings.constants.default_layout)
                            windows = {
                                "main-window-files": layout["BOXES"]["0"]["BOX-H"]["0"]["BOX-V"]["0"]["TABS"],
                                "upper-window-files": layout["BOXES"]["0"]["BOX-H"]["1"]["BOX-V"]["0"]["BOX-H"]["0"]["TABS"],
                                "lower-window-files": layout["BOXES"]["0"]["BOX-H"]["1"]["BOX-V"]["1"]["BOX-H"]["0"]["TABS"],
                            }
                            for kk,vv in windows.items():
                                files = v[kk]["files"]
                                for f in files:
                                    if isinstance(f, dict):
                                        vv[f["path"]] = [
                                            "CustomEditor",
                                            0,
                                            [
                                                f["line"],
                                                f["index"],
                                                f["first-visible-line"],
                                            ]
                                        ]
                                    else:
                                        vv[f] = [
                                            "CustomEditor",
                                            0,
                                            [
                                                0,
                                                0,
                                                0
                                            ]
                                        ]
                            new_session["layout"] = layout
                            for kk,vv in windows.items():
                                v.pop(kk)
                            v["layout"] = layout
                    # Groups
                    if "groups" in item.keys():
                        for k,v in item["groups"].items():
                            recurse_groups(v)
                recurse_groups(self.stored_sessions["main"])
                self.settings_filename_with_path = old_files["mark-2"]
                self.write_settings_file(
                    self.theme,
                    self.recent_files,
                    self.stored_sessions,
                    self.context_menu_functions
                )
            elif OLD_SETTINGS_IMPORTED == True and os.path.isfile(old_files["mark-0"]):
                # Convert MK-0 setting file to to MK-1
                old_data = oldsettings.parse_settings_file(old_files["mark-0"])
                for k,v in old_data["sessions"].items():
                    v["Name"] = k
                self.write_settings_file(
                    old_data["theme"],
                    old_data["recent_files"],
                    old_data["sessions"],
                    old_data["context_menu_functions"],
                )
            else:
                self.theme = themes.get("Air")
                self.write_settings_file(
                    self.theme,
                    self.recent_files,
                    self.stored_sessions,
                    self.context_menu_functions
                )
        # Load the settings from the settings file
        self.load_settings()
    
    def check_settings_file(self):
        """
        Check if the settings file exists
        """
        return functions.test_text_file(self.settings_filename_with_path)
    
    def get_settings_file(self):
        return self.settings_filename_with_path
    
    def create_settings_file(self, settings_data):
        """
        Create the settings file
        """
        functions.write_json_file(
            self.settings_filename_with_path,
            settings_data
        )
    
    def write_settings_file(self,
                            theme,
                            recent_files,
                            stored_sessions,
                            context_menu_functions):
        try:
            theme_name = theme["name"]
        except:
            theme_name = theme.name
        settings_data = {
            "theme": theme_name,
            "recent_files": recent_files,
            "stored_sessions": stored_sessions,
            "context_menu_functions": context_menu_functions,
            "editor": editor,
            "keyboard_shortcuts": keyboard_shortcuts,
            "variables": variables
        }
        for dv in self.data_variables:
            settings_data[dv] = getattr(data, dv)
        
        # Save settings data to disk
        self.create_settings_file(settings_data)
    
    def save_settings(self,
                      theme,
                      context_menu_functions=None):
        """
        Save all settings to the settings file
        """
        if self.error_lock == True:
            return
        if context_menu_functions == None:
            context_menu_functions = self.context_menu_functions
        else:
            self.context_menu_functions = context_menu_functions
        self.write_settings_file(
            theme,
            self.recent_files,
            self.stored_sessions,
            context_menu_functions
        )
    
    def update_recent_files(self):
        """
        Update only the recent file list in settings file
        """
        if self.error_lock == True:
            return
        settings_data = functions.load_json_file(
            self.settings_filename_with_path
        )
        # Update only the recent file list
        stored_sessions = settings_data["stored_sessions"]
        # Save the updated settings
        self.write_settings_file(
            data.theme,
            self.recent_files,
            stored_sessions,
            self.context_menu_functions
        )
    
    def clear_recent_files(self):
        if self.error_lock == True:
            return
        settings_data = functions.load_json_file(
            self.settings_filename_with_path
        )
        # Clear the recent file list
        self.recent_files = []
        # Load the sessions
        stored_sessions = settings_data["stored_sessions"]
        # Save the updated settings
        self.write_settings_file(
            data.theme,
            self.recent_files,
            stored_sessions,
            self.context_menu_functions
        )
    
    def load_settings(self):
        """
        Load all setting from the settings file
        """
        global variables
        try:
            settings_data = functions.load_json_file(
                self.settings_filename_with_path
            )
            # Theme
            self.theme = themes.get(settings_data["theme"])
            data.theme = self.theme
            # Recent files
            self.recent_files = settings_data["recent_files"]
            # Sessions
            self.stored_sessions = settings_data["stored_sessions"]
            # Load custom context menu functions
            if "context_menu_functions" in settings_data.keys():
                self.context_menu_functions = settings_data["context_menu_functions"]
            else:
                self.context_menu_functions = {}
            # Variables
            if "variables" in settings_data.keys():
                variables = settings_data["variables"]
            # Check if old-style session file
            if self.check_old_style_sessions():
                self.write_settings_file(
                    data.theme,
                    self.recent_files,
                    self.stored_sessions,
                    self.context_menu_functions
                )
            # Return success
            return True
        except:
            traceback.print_exc()
            # Set the default settings values
            self.theme = themes.get("Air")
            data.theme = self.theme
            self.recent_files = []
            self.stored_sessions = {}
            self.context_menu_functions = {}
            # Set the error flag
            self.error_lock = True
            # Return error
            return False
    
    def check_old_style_sessions(self):
        if "main" not in self.stored_sessions.keys():
            new_sessions = {
                "main": {
                    "name": "main",
                    "chain": [],
                    "groups": {},
                    "sessions": {},
                }
            }
            for k,v in sorted(self.stored_sessions.items(), key=lambda x: x[0].lower()):
                group = new_sessions["main"]
                for g in v["Group"]:
                    if g not in group["groups"].keys():
                        group["groups"][g] = {
                            "name": g,
                            "chain": [],
                            "groups": {},
                            "sessions": {},
                        }
                        if group["chain"] is not None:
                            for x in group["chain"]:
                                group["groups"][g]["chain"].append(x)
                        group["groups"][g]["chain"].append(g)
                    group = group["groups"][g]
                if k not in group["sessions"].keys():
                    group["sessions"][k] = {
                        "name": k,
                        "chain": [],
                        "main-window-files": v["Main window files"],
                        "upper-window-files": v["Upper window files"],
                        "lower-window-files": v["Lower window files"],
                    }
                    if group["chain"] is not None:
                        for x in group["chain"]:
                            group["sessions"][k]["chain"].append(x)
            self.stored_sessions = new_sessions
            return True
        return False
    
    def create_empty_session(self,
                             name="",
                             chain=[],
                             layout=""):
        return {
            "name": name,
            "chain": chain,
            "layout": layout,
        }
    
    def create_empty_session_group(self,
                                   name="",
                                   chain=[],
                                   groups={},
                                   sessions={}):
        return {
            "name": name,
            "chain": chain,
            "groups": groups,
            "sessions": sessions
        }
    
    def add_session(self, 
                    session_name, 
                    session_group_chain, 
                    layout,):
        """
        Add a new session to the stored session list
        """
        # Update sessions
        self.load_settings()
        
        # Create the new session object
        new_session = self.create_empty_session(
            name=session_name,
            chain=session_group_chain,
            layout=layout,
        )
        # Add/replace the session in the dictionary
        group = self.stored_sessions["main"]
        for c in new_session["chain"]:
            group = group["groups"][c]
        group["sessions"][session_name] = new_session
        # Save the new settings
        self.save_settings(self.theme)
    
    def add_group(self, group_name, group_chain):
        """
        Add a new group to the stored session list
        """
        # Update sessions
        self.load_settings()
        
        # Create the new group object
        new_group = self.create_empty_session_group(
            name=group_name,
            chain=group_chain,
            groups={},
            sessions={}
        )
        # Add/replace the session in the dictionary
        group = self.stored_sessions["main"]
        for c in group_chain:
            group = group["groups"][c]
        group["groups"][group_name] = new_group
        # Save the new settings
        self.save_settings(self.theme)

    def remove_session(self, session_to_remove):
        """
        Remove a session from the stored session list
        """
        # Update sessions
        self.load_settings()
        
        group = self.stored_sessions["main"]
        for c in session_to_remove["chain"]:
            group = group["groups"][c]
        if session_to_remove["name"] in group["sessions"].keys():
            # Remove the session from the stored session list
            group["sessions"].pop(session_to_remove["name"])
            # Save the new settings
            self.save_settings(self.theme)
            return True
        # Signal that the session was not removed
        return False
    
    def remove_group(self, remove_group):
        """
        Remove an entire group from the stored session list
        """
        # Update sessions
        self.load_settings()
        
        group = self.stored_sessions["main"]
        if len(remove_group["chain"]) > 0:
            for c in remove_group["chain"]:
                group = group["groups"][c]
        if remove_group["name"] in group["groups"].keys():
            # Remove the session from the stored session list
            group["groups"].pop(remove_group["name"])
            # Save the new settings
            self.save_settings(self.theme)
            return True
        # Signal that the group was not removed
        return False
    
    def sort_sessions(self):
        """
        Sort the stored sessions alphabetically by name
        """
        # Update sessions
        self.load_settings()
        
        # Create a new empty dict
        sorted_sessions = {}
        # Add sorted keys
        for k in sorted(self.stored_sessions.keys(), key=lambda x: x.lower()):
            sorted_sessions[k] = self.stored_sessions[k]
        # Sort the stored sessions
        self.stored_sessions = sorted_sessions
    
    def get_session(self, name, chain):
        # Update sessions
        self.load_settings()
        
        session = None
        group = self.stored_sessions["main"]
        for c in chain:
            group = group["groups"][c]
        if name in group["sessions"].keys():
            session = group["sessions"][name]
        return session
    
    def get_group(self, chain):
        # Update sessions
        self.load_settings()
        
        group = self.stored_sessions["main"]
        for c in chain:
            group = group["groups"][c]
        return group
    
    def rename_group(self, group, new_group_name):
        # Update sessions
        self.load_settings()
        
        def rename_first_group(grp, new_name, in_level):
            grp["chain"][in_level] = new_name
            for k,v in grp["groups"].items():
                rename_first_group(v, new_name, in_level)
            for k,v in grp["sessions"].items():
                v["chain"][in_level] = new_name
        level = len(group["chain"]) - 1
        rename_first_group(group, new_group_name, level)
        group["name"] = new_group_name

    def add_recent_file(self, new_file):
        """Add a new file to the recent file list"""
        # Replace back-slashes to forward-slashes on Windows
        if data.platform == "Windows":
            new_file = new_file.replace("\\", "/")
        # Check recent files list length
        while len(self.recent_files) > variables["max-number-of-recent-files"]:
            # The recent files list is to long
            self.recent_files.pop(0)
        # Check if he new file is already in the list
        if new_file in self.recent_files:
            # Check if the file is already at the top
            if self.recent_files.index(new_file) == (variables["max-number-of-recent-files"]-1):
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
    
    def save_last_layout(self, layout):
        filepath = os.path.join(data.settings_directory, self.LAST_LAYOUT_FILENAME)
        with open(filepath, "w+", encoding="utf-8") as f:
            f.write(json.dumps(layout, indent=2, ensure_ascii=False))
    