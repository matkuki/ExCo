"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

from typing import Any, Dict

import qt
import themes

from settings.settings import SettingsManipulator

__settings_manipulator: SettingsManipulator = SettingsManipulator()
__theme_cache: Dict[str, Dict[str, Any]] = {}


def get(name: str) -> Any:
    return __settings_manipulator.get(name)


def get_theme() -> dict:
    theme_name = __settings_manipulator.get("theme")
    if theme_name not in __theme_cache.keys():
        __theme_cache[theme_name] = themes.get(theme_name)
    return __theme_cache[theme_name]


def get_sessions() -> dict:
    return __settings_manipulator.sessions


def set(name: str, value: Any) -> None:
    __settings_manipulator.set(name, value)


def get_current_font():
    return qt.QFont(
        __settings_manipulator.get("current_font_name"),
        int(__settings_manipulator.get("current_font_size")),
    )


def get_editor_font():
    return qt.QFont(
        __settings_manipulator.get("current_editor_font_name"),
        int(__settings_manipulator.get("current_editor_font_size")),
    )


# --- API Definition ---
# This list specifies the names under which the functionality will be
# exposed as global functions in the current module's namespace.
# These names form the 'exposed API'.
exposed_api_names = ["load", "save", "save_last_layout", "add_recent_file"]

# This list maps the desired exposed API names to the actual method names
# on the internal object (which is assumed to be __settings_manipulator).
# 'method' is the name of the function inside the class/module.
# 'exposed_function' is the name it will be given in the current global scope.
exposed_api_map = [
    {"method": "load_settings", "exposed_function": "load"},
    {"method": "save_settings", "exposed_function": "save"},
    {"method": "save_last_layout", "exposed_function": "save_last_layout"},
    {"method": "add_recent_file", "exposed_function": "add_recent_file"},
]

# --- Dynamic Function Definition ---

# It is assumed that an instance of a settings handler class,
# which contains the actual logic (e.g., load_settings, save_settings),
# has been instantiated and assigned to a private/internal variable like:
# __settings_manipulator = SettingsManipulatorClass(...)

# Dynamically define global functions (proxies) for the exposed API names.
for mapping in exposed_api_map:
    method_name = mapping["method"]
    exposed_name = mapping["exposed_function"]

    # 1. Define a function factory (maker_proxy) that creates the actual proxy function.
    # This is a critical step to ensure that 'method_name' is captured correctly
    # for each proxy function (a standard Python closure-in-a-loop fix).
    def make_proxy(method_name):
        # 2. This inner function (proxy) is the one that will be exposed.
        # It takes any arguments/keyword arguments passed to it.
        def proxy(*args, **kwargs):
            # 3. Call the actual method on the internal settings object.
            # 'getattr' is used to look up the method by its string name.
            return getattr(__settings_manipulator, method_name)(*args, **kwargs)

        # 4. Return the proxy function, which forms a closure over 'method_name'.
        return proxy

    # Assign the newly created proxy function to a global variable
    # with the 'exposed_name' (e.g., globals()["load"] = proxy_function).
    # This effectively creates a new, accessible, top-level function.
    globals()[exposed_name] = make_proxy(method_name)

# --- Final State ---
# After the loop, the current module will have global functions like:
# load(*args, **kwargs) -> calls __settings_manipulator.load_settings(*args, **kwargs)
# save_last_layout(*args, **kwargs) -> calls __settings_manipulator.save_last_layout(*args, **kwargs)
