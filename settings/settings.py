"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

##  FILE DESCRIPTION:
##      Module used to save, load, ... settings of Ex.Co.

import json
import os
import os.path
import shutil
import threading
import traceback
from collections import UserDict
from typing import Any, Callable, Dict, Union

import data
import filefunctions
import functions
import settings.constants
import settings.functions

try:
    import settings.old.settings as oldsettings

    OLD_SETTINGS_IMPORTED = True
except:
    OLD_SETTINGS_IMPORTED = False


class SettingsManipulator:
    """
    Object that will be used for saving, loading, ... all of the Ex.Co. settings
    """

    __error_lock: bool = False

    def __error_check(self) -> None:
        if self.__error_lock:
            raise Exception("[Settings] An error occurred during loading of settings!")

        return self.__error_lock

    def __init__(self):
        # Set the current active settings file path
        self.active_settings_file = functions.unixify_join(
            data.settings_directory, settings.constants.settings_filename["mark-3"]
        )
        active_settings_file_exists = self.check_settings_file(
            self.active_settings_file
        )

        # Create storage
        self.storage = SettingsStorage(
            file_path=self.active_settings_file,
            default_settings=settings.constants.default_settings,
        )

        # Create the session manipulator
        self.sessions = Sessions(self)

        # Create the settings file path
        functions.create_directory(data.settings_directory)
        self.set("settings_filename_with_path", self.active_settings_file)

        # Check if the settings file exists
        if active_settings_file_exists is None:
            old_files = {}
            for k, v in settings.constants.settings_filename.items():
                old_files[k] = functions.unixify_join(data.settings_directory, v)
            if os.path.isfile(old_files["mark-2"]):
                # Convert MK-II setting file to to MK-III
                self.__load_mk2(old_files["mark-2"])
            elif os.path.isfile(old_files["mark-1"]):
                # Convert MK-I setting file to to MK-II
                self.__load_mk1(old_files["mark-2"])
            elif OLD_SETTINGS_IMPORTED == True and os.path.isfile(old_files["mark-0"]):
                # Convert MK-0 setting file to to MK-1
                self.__load_mk0(old_files["mark-0"])
            else:
                self.set("theme-name", "Air")
                self.sessions.set_sessions(self.sessions.get_sessions())
        # Load the settings from the settings file
        self.load_settings()

    def __load_mk0(self, old_file_path: str) -> None:
        old_data = oldsettings.parse_settings_file(old_file_path)
        for k, v in old_data["sessions"].items():
            v["Name"] = k
        self.set("theme", old_data["theme"])
        self.set("recent_files", old_data["recent_files"])
        self.set("stored_sessions", old_data["sessions"])
        self.set("context_menu_functions", old_data["context_menu_functions"])

    def __load_mk1(self, old_file_path: str) -> None:
        # Load data from file
        settings_data = functions.load_json_file(old_file_path)
        # Update storage
        self.storage.update_without_saving(settings_data)
        # Overwrite settings with the active settings file
        self.set("settings_filename_with_path", self.active_settings_file)

        def recurse_groups(item):
            # Sessions
            if "sessions" in item.keys():
                for k, v in item["sessions"].items():
                    new_session = {
                        "name": v["name"],
                        "chain": v["chain"],
                        "layout": None,
                    }
                    layout = json.loads(settings.constants.default_layout)
                    windows = {
                        "main-window-files": layout["BOXES"]["0"]["BOX-H"]["0"][
                            "BOX-V"
                        ]["0"]["TABS"],
                        "upper-window-files": layout["BOXES"]["0"]["BOX-H"]["1"][
                            "BOX-V"
                        ]["0"]["BOX-H"]["0"]["TABS"],
                        "lower-window-files": layout["BOXES"]["0"]["BOX-H"]["1"][
                            "BOX-V"
                        ]["1"]["BOX-H"]["0"]["TABS"],
                    }
                    for kk, vv in windows.items():
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
                                    ],
                                ]
                            else:
                                vv[f] = ["CustomEditor", 0, [0, 0, 0]]
                    new_session["layout"] = layout
                    for kk, vv in windows.items():
                        v.pop(kk)
                    v["layout"] = layout
            # Groups
            if "groups" in item.keys():
                for k, v in item["groups"].items():
                    recurse_groups(v)

        sessions = settings_data["stored_sessions"]
        recurse_groups(sessions["main"])
        self.set("settings_filename_with_path", active_settings_file)
        self.sessions.set_sessions(sessions)

    def __load_mk2(self, old_file_path: str) -> None:
        # Load data from file
        settings_data = functions.load_json_file(old_file_path)
        # Update storage
        self.storage.update_without_saving(settings_data)
        # Overwrite settings with the active settings file
        self.set("settings_filename_with_path", self.active_settings_file)
        # Update the settings to the new file
        self.sessions.set_sessions(settings_data["stored_sessions"])

    def get(self, name: str) -> Any:
        return self.storage[name]

    def set(self, name: str, value: Any) -> None:
        if self.__error_check():
            return

        self.storage[name] = value

    def check_settings_file(self, settings_file_path: str):
        """
        Check if the settings file exists
        """
        return functions.test_text_file(settings_file_path)

    def get_settings_file(self):
        return self.get("settings_filename_with_path")

    def update_recent_files(self):
        """
        Update only the recent file list in settings file
        """
        if self.__error_check():
            return

        settings_data = functions.load_json_file(
            self.get("settings_filename_with_path")
        )
        # Load the session data from the file to have it up-to-date
        stored_sessions = settings_data["stored_sessions"]
        self.sessions.set_sessions(stored_sessions)

    def clear_recent_files(self):
        if self.__error_check():
            return

        settings_data = functions.load_json_file(
            self.get("settings_filename_with_path")
        )
        # Clear the recent file list
        self.get("recent_files", [])
        # Load the session data from the file to have it up-to-date
        stored_sessions = settings_data["stored_sessions"]
        self.sessions.set_sessions(stored_sessions)

    def load_settings(self):
        """
        Load all setting from the settings file
        """
        try:
            # Load data from file
            settings_data = functions.load_json_file(
                self.get("settings_filename_with_path")
            )

            # Update storage
            self.storage.update_without_saving(settings_data)

            # Sessions
            self.sessions.set_sessions(settings_data["stored_sessions"])

            # Check if old-style session file
            if self.sessions.check_old_style_sessions():
                self.sessions.set_sessions(self.sessions.get_sessions())
            # Return success
            return True
        except:
            traceback.print_exc()
            # Set the error flag
            self.__error_lock = True
            # Return error
            return False

    def add_recent_file(self, new_file):
        """
        Add a new file to the recent file list
        """
        if self.__error_check():
            return

        # Replace back-slashes to forward-slashes on Windows
        if data.platform == "Windows":
            new_file = new_file.replace("\\", "/")
        # Check recent files list length
        while len(self.get("recent_files")) > self.get("max-number-of-recent-files"):
            # The recent files list is to long
            self.get("recent_files").pop(0)
        # Check if he new file is already in the list
        if new_file in self.get("recent_files"):
            # Check if the file is already at the top
            if self.get("recent_files").index(new_file) == (
                self.get("max-number-of-recent-files") - 1
            ):
                return
            # Remove the old file with the same name as the new file from the list
            self.get("recent_files").pop(self.get("recent_files").index(new_file))
            # Add the new file to the end of the list
            self.get("recent_files").append(new_file)
        else:
            # The new file is not in the list, append it to the end of the list
            self.get("recent_files").append(new_file)
        # Save the new settings
        self.update_recent_files()

    def save_last_layout(self, layout):
        if self.__error_check():
            return

        filepath = os.path.join(
            data.settings_directory, self.get("last-layout-filename")
        )
        with open(filepath, "w+", encoding="utf-8") as f:
            f.write(json.dumps(layout, indent=2, ensure_ascii=False))


class Sessions:
    def __init__(self, parent: SettingsManipulator):
        # Store the parent reference
        self.__parent = parent

        # Initialize an empty sessions list
        self.__sessions: dict = {"main": self.create_empty_session_group()}

    def check_old_style_sessions(self):
        if "main" not in self.__sessions.keys():
            new_sessions = {
                "main": {
                    "name": "main",
                    "chain": [],
                    "groups": {},
                    "sessions": {},
                }
            }
            for k, v in sorted(self.__sessions.items(), key=lambda x: x[0].lower()):
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
            self.__sessions = new_sessions
            return True
        return False

    def set_sessions(self, new_sessions) -> None:
        self.__sessions = new_sessions
        self.store_sessions()

    def store_sessions(self) -> None:
        self.__parent.set("stored_sessions", self.__sessions)

    def get_sessions(self) -> dict:
        return self.__sessions

    def create_empty_session(self, name="", chain=[], layout=""):
        return {
            "name": name,
            "chain": chain,
            "layout": layout,
        }

    def create_empty_session_group(self, name="", chain=[], groups={}, sessions={}):
        return {"name": name, "chain": chain, "groups": groups, "sessions": sessions}

    def add_session(
        self,
        session_name,
        session_group_chain,
        layout,
    ):
        """
        Add a new session to the stored session list
        """
        # Update sessions
        self.__parent.load_settings()

        # Create the new session object
        new_session = self.create_empty_session(
            name=session_name,
            chain=session_group_chain,
            layout=layout,
        )
        # Add/replace the session in the dictionary
        group = self.__sessions["main"]
        for c in new_session["chain"]:
            group = group["groups"][c]
        group["sessions"][session_name] = new_session
        # Save the new settings
        self.store_sessions()

    def add_group(self, group_name, group_chain):
        """
        Add a new group to the stored session list
        """
        # Update sessions
        self.__parent.load_settings()

        # Create the new group object
        new_group = self.create_empty_session_group(
            name=group_name, chain=group_chain, groups={}, sessions={}
        )
        # Add/replace the session in the dictionary
        group = self.__sessions["main"]
        for c in group_chain:
            group = group["groups"][c]
        group["groups"][group_name] = new_group
        # Save the new settings
        self.store_sessions()

    def remove_session(self, session_to_remove):
        """
        Remove a session from the stored session list
        """
        # Update sessions
        self.__parent.load_settings()

        group = self.__sessions["main"]
        for c in session_to_remove["chain"]:
            group = group["groups"][c]
        if session_to_remove["name"] in group["sessions"].keys():
            # Remove the session from the stored session list
            group["sessions"].pop(session_to_remove["name"])
            # Save the new settings
            self.store_sessions()
            return True
        # Signal that the session was not removed
        return False

    def remove_group(self, remove_group):
        """
        Remove an entire group from the stored session list
        """
        # Update sessions
        self.__parent.load_settings()

        group = self.__sessions["main"]
        if len(remove_group["chain"]) > 0:
            for c in remove_group["chain"]:
                group = group["groups"][c]
        if remove_group["name"] in group["groups"].keys():
            # Remove the session from the stored session list
            group["groups"].pop(remove_group["name"])
            # Save the new settings
            self.store_sessions()
            return True
        # Signal that the group was not removed
        return False

    def sort_sessions(self):
        """
        Sort the stored sessions alphabetically by name
        """
        # Update sessions
        self.__parent.load_settings()

        # Create a new empty dict
        sorted_sessions = {}
        # Add sorted keys
        for k in sorted(self.__sessions.keys(), key=lambda x: x.lower()):
            sorted_sessions[k] = self.__sessions[k]
        # Sort the stored sessions
        self.__sessions = sorted_sessions

    def get_session(self, name, chain):
        # Update sessions
        self.__parent.load_settings()

        session = None
        group = self.__sessions["main"]
        for c in chain:
            group = group["groups"][c]
        if name in group["sessions"].keys():
            session = group["sessions"][name]
        return session

    def get_group(self, chain):
        # Update sessions
        self.__parent.load_settings()

        group = self.__sessions["main"]
        for c in chain:
            group = group["groups"][c]
        return group

    def rename_group(self, group, new_group_name):
        def rename_first_group(grp, new_name, in_level):
            if in_level < len(grp["chain"]):
                return
            grp["chain"][in_level] = new_name
            for k, v in grp["groups"].items():
                rename_first_group(v, new_name, in_level)
            for k, v in grp["sessions"].items():
                v["chain"][in_level] = new_name

        level = len(group["chain"]) - 1
        rename_first_group(group, new_group_name, level)
        group["name"] = new_group_name


class SettingsStorage(UserDict):
    """
    A simple settings manager that loads/saves settings from a JSON file.
    Settings are saved to the file only when a value genuinely changes,
    or on initial load if the file doesn't exist/is corrupted.

    When setting or updating, if a value is a dictionary and the existing
    value for that key is also a dictionary, they are recursively merged.
    """

    def __init__(
        self,
        file_path: str,
        default_settings: Dict[str, Any],
        print_func: Callable[[str], None] = print,
    ):
        """
        Initializes the Settings manager.

        Args:
            file_path (str): The absolute path to the JSON file where settings
                             will be stored.
            default_settings (Dict[str, Any]): A dictionary of default settings.
                                               These will be used if the settings file
                                               doesn't exist or is empty.
                                               Must not be None.
            print_func (Callable[[str], None], optional): A custom function to use
                                                           for printing messages.
                                                           Defaults to the built-in print().
        """
        super().__init__()
        self.file_path = file_path
        if default_settings is None:
            raise Exception("Default settings are needed here!")
        self.__default_settings = default_settings
        self.__print = print_func

        self.__load()

    def echo(self, message: str) -> None:
        """
        Custom print method for the Settings class, using the provided print_func.

        Args:
            message (str): The message string to print.
        """
        self.__print(message)

    def __backup_file(self) -> None:
        # Create a copy of the settings file
        settings_file = self.file_path
        settings_copy = (
            f"{settings_file}.{functions.get_default_datetime_formatted_string()}.bak"
        )
        shutil.copy(settings_file, settings_copy)

    def __load(self) -> None:
        """
        Loads settings from the JSON file. If the file doesn't exist or is invalid,
        it uses the default settings and saves them to the file immediately.
        """
        if not os.path.exists(self.file_path):
            self.echo(
                f"Settings file not found at '{self.file_path}'.\n"
                "Using default settings.\n"
            )
            # Use the intelligent update to set defaults, enabling recursive merging
            # if default_settings contains nested dicts
            self.data.clear()  # Ensure data is empty before applying defaults
            self.update(
                self.__default_settings, _initial_load=True
            )  # Pass a flag to prevent saving here
            # The initial load ensures default settings are applied and saved if needed
            if (
                self.data != self.__default_settings
            ):  # Only save if something was actually changed/merged
                self.__save()
            elif not os.path.exists(
                self.file_path
            ):  # Ensure a file is written if it truly didn't exist
                self.__save()
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                loaded_data = json.load(f)
                # First, apply defaults. Then, apply loaded data on top, merging recursively.
                self.data.clear()  # Clear existing data to ensure defaults are the base
                self.update(self.__default_settings, _initial_load=True)
                self.update(loaded_data, _initial_load=True)  # Merge loaded data
                if (
                    self.data != loaded_data
                ):  # If merging changed something from purely loaded
                    self.__save()  # Save if the merge process modified something
        except json.JSONDecodeError:
            self.echo(
                f"Error decoding JSON from '{self.file_path}'.\n"
                "File might be corrupted.\n"
                f"Using default settings and overwriting the file.\n"
                f"A backup copy will be created of the invalid file!\n"
            )

            # Create a copy of the invalid settings file
            self.__backup_file()

            self.data.clear()
            self.update(self.__default_settings, _initial_load=True)
            self.__save()
        except Exception as e:
            self.echo(
                f"An unexpected error occurred while loading settings from '{self.file_path}':\n  -> {e}.\n"
                f"Using default settings.\n"
            )

            # Create a copy of the invalid settings file
            self.__backup_file()

            self.data.clear()
            self.update(self.__default_settings, _initial_load=True)
            self.__save()

    def __save(self) -> None:
        """
        Immediately writes the current settings to the JSON file.
        """
        try:
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            filefunctions.write_json_file(self.file_path, self.data)
            self.echo(f"Settings saved to '{self.file_path}'.")
        except Exception as e:
            self.echo(f"Error saving settings to '{self.file_path}': {e}'")

    def __setitem__(self, key: str, value: Any) -> None:
        """
        Overrides the dictionary's __setitem__ method to save settings
        only if the value truly changes or it's a new key.
        If the value is a dictionary and the existing item is also a dictionary,
        it performs a recursive update with deep change detection.
        """
        changed = False

        if (
            key in self.data
            and isinstance(self.data[key], dict)
            and isinstance(value, dict)
        ):
            # --- Deep Change Detection for Nested Dictionary ---

            # 1. Capture the initial state of the nested dict
            initial_nested_snapshot = json.dumps(self.data[key], sort_keys=True)

            # 2. Perform the recursive update (modifies self.data[key] in-place)
            self.data[key].update(value)

            # 3. Capture the final state of the nested dict
            final_nested_snapshot = json.dumps(self.data[key], sort_keys=True)

            # 4. Compare snapshots to check for change
            if final_nested_snapshot != initial_nested_snapshot:
                self.echo(f"Setting '{key}' (nested dict) updated.")
                changed = True
            else:
                # If the nested update did not result in a change, we exit the method
                # early to prevent unnecessary saving.
                return

        else:
            # Standard set item, with simple change detection for non-dict values
            if key in self.data:
                if self.data[key] == value:
                    return  # No change, no save
                else:
                    self.echo(f"Setting '{key}' changed.")
                    changed = True
            else:
                self.echo(f"Setting '{key}' added.")
                changed = True

            # Perform the actual set operation
            super().__setitem__(key, value)

        if changed:
            self.__save()

    def __delitem__(self, key: str) -> None:
        """
        Overrides the dictionary's __delitem__ method to save settings
        only if the key-value pair was actually deleted.
        """
        if key in self.data:
            self.echo(f"Setting '{key}' deleted.")  # Message updated
            super().__delitem__(key)
            self.__save()
        else:
            self.echo(
                f"Attempted to delete non-existent setting '{key}'. No action, no save."
            )
            raise KeyError(f"'{key}' not found in settings.")

    def update(self, other=None, _initial_load=False, **kwargs) -> None:
        """
        Overrides the update method to save settings only if the data truly changes.
        If a value is a dictionary and the existing item is also a dictionary,
        it performs a recursive update.

        The final JSON snapshot check ensures all changes, including those from
        recursive dictionary updates, are accurately detected before saving.
        """

        # 1. Capture the initial state for the final deep comparison (to catch ALL changes)
        initial_data_snapshot = json.dumps(self.data, sort_keys=True)

        # --- Helper function for setting key/value and tracking changes ---
        # NOTE: This helper is only for non-recursive assignments. It relies on
        # the final JSON snapshot check for recursive changes.
        def _set_item_and_check_change(key, value):
            # Check if the key exists AND the value is different
            if key in self.data and self.data[key] == value:
                return  # Value is the same, do nothing

            # Value is new or different, set it.
            # We explicitly pass the class name 'SettingsStorage' to super()
            # to resolve the nested function scope issue.
            super(SettingsStorage, self).__setitem__(key, value)

            # Since the value changed, we don't need a separate _changed flag
            # here anymore, as the final JSON snapshot will capture this change too.
            # The JSON comparison is the single source of truth for change detection.

        # Process 'other' if it's a dict or iterable of key-value pairs
        if other:
            if hasattr(other, "keys"):  # It's a dict-like object
                for key, value in other.items():
                    if (
                        key in self.data
                        and isinstance(self.data[key], dict)
                        and isinstance(value, dict)
                    ):
                        # Recursive update for nested dictionaries.
                        # This update modifies self.data[key] in-place.
                        self.data[key].update(value)
                        # NO _changed = True HERE! Rely on JSON comparison.
                    else:
                        _set_item_and_check_change(key, value)
            else:  # Assume iterable of (key, value) pairs
                for key, value in other:
                    if (
                        key in self.data
                        and isinstance(self.data[key], dict)
                        and isinstance(value, dict)
                    ):
                        self.data[key].update(value)
                        # NO _changed = True HERE! Rely on JSON comparison.
                    else:
                        _set_item_and_check_change(key, value)

        # Process kwargs
        for key, value in kwargs.items():
            if (
                key in self.data
                and isinstance(self.data[key], dict)
                and isinstance(value, dict)
            ):
                # Recursive update for nested dictionaries
                self.data[key].update(value)
                # NO _changed = True HERE! Rely on JSON comparison.
            else:
                _set_item_and_check_change(key, value)

        # 2. Capture the final state for the final deep comparison
        final_data_snapshot = json.dumps(self.data, sort_keys=True)

        # 3. Final Check and Save
        # The JSON comparison is now the ONLY check for any change (simple or deep).
        if final_data_snapshot != initial_data_snapshot:
            if not _initial_load:  # Only save if not called from __load
                self.__save()

    def update_without_saving(self, other=None, **kwargs) -> None:
        """
        Updates the settings without triggering a save operation.
        Useful for batch updates where you'll manually call save() later.
        This method will *not* perform recursive dictionary merging.
        It will overwrite entire dictionaries if present in 'other' or 'kwargs'.
        """
        super().update(other, **kwargs)
        self.echo("Settings updated without saving to disk.")

    def clear(self) -> None:
        """
        Overries the clear method to save settings only if there were items to clear.
        """
        if self.data:  # Only save if data was cleared
            self.echo("All settings cleared.")
            super().clear()
            self.__save()
        else:
            self.echo("Settings were already empty. No clear action, no save.")

    def set_default(self, key: str, value: Any) -> None:
        """
        Sets a default value for a setting if it doesn't already exist.
        If the default value is a dictionary and the existing item is also
        a dictionary, it performs a recursive update.
        This will save if the key is new or a nested dict is merged.
        """
        if key not in self:
            self.echo(f"Setting default '{key}' applied.")
            self[key] = (
                value  # Use self[key] to trigger __setitem__ (which handles recursion)
            )
        elif isinstance(self.data.get(key), dict) and isinstance(value, dict):
            # If default is a dict and existing is a dict, attempt to merge
            initial_snapshot = json.dumps(self.data[key], sort_keys=True)
            self.data[key].update(value)  # This performs the merge
            if json.dumps(self.data[key], sort_keys=True) != initial_snapshot:
                self.echo(f"Setting default '{key}' (nested dict) merged.")
                self.__save()
            else:
                self.echo(
                    f"Setting '{key}' already exists and merge resulted in no changes, default not applied."
                )
        else:
            self.echo(f"Setting '{key}' already exists, default not applied.")
