"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

from typing import Any, Dict

import qt
import themes

from .settings import SettingsManipulator

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


# Exposed API
exposed_api_names = ["load", "save", "save_last_layout", "add_recent_file"]
exposed_api_map = [
    {"method": "load_settings", "exposed_function": "load"},
    {"method": "save_settings", "exposed_function": "save"},
    {"method": "save_last_layout", "exposed_function": "save_last_layout"},
    {"method": "add_recent_file", "exposed_function": "add_recent_file"},
]
# Dynamically define global functions
for mapping in exposed_api_map:
    method_name = mapping["method"]
    exposed_name = mapping["exposed_function"]

    def make_proxy(method_name):
        def proxy(*args, **kwargs):
            return getattr(__settings_manipulator, method_name)(*args, **kwargs)

        return proxy

    globals()[exposed_name] = make_proxy(method_name)
