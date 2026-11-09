"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import os
import sys
import data


def check_shortcut_combination(combination_string: str) -> list[str] | None:
    keys: list[str] = []
    current_key: list[str] = []
    for c in combination_string:
        if c == "+" and not (len(current_key) == 0):
            if len(current_key) > 0:
                keys.append("".join(current_key))
                current_key = []
        else:
            current_key.append(c)
    else:
        if len(current_key) > 0:
            keys.append("".join(current_key))
        else:
            keys = []
    valid_modifiers: tuple[str, ...] = ("ctrl", "shift", "alt")
    valid_key_names: dict[str, str] = {
        "add": "+",
        "plus": "+",
        "minus": "-",
        "subtract": "-",
        "divide": "/",
        "multiply": "*",
        "asterisk": "*",
        "down": "down",
        "tab": "\t",
        "backspace": "backspace",
        "escape": "escape",
        "up": "up",
        "left": "left",
        "right": "right",
        "home": "home",
        "end": "end",
        "pageup": "pageup",
        "pagedown": "pagedown",
        "delete": "delete",
        "insert": "insert",
        "escape": "escape",
    }
    out_keys: list[str] = []
    valid: bool = True
    for k in keys:
        key = k.lower()
        if len(key) > 1 and key in valid_modifiers:
            out_keys.append(k)
        elif len(key) > 1 and key in valid_key_names.keys():
            out_keys.append(valid_key_names[key])
        elif len(key) == 1:
            out_keys.append(k)
        else:
            valid = False
            break
    return out_keys if valid else None
