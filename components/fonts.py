
"""
Copyright (c) 2021 embeetle.
"""


import os
import os.path
import sys
import traceback
import functools
import textwrap
import functions
import data

def get_fonts_from_resources():
    directory = functions.unixify_path_join(data.resources_directory, "fonts/")
    font_file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            item = functions.unixify_path_join(root, file)
            if item.lower().endswith('.ttf') or item.lower().endswith('.otf'):
                font_file_list.append(
                    functions.unixify_path_join(directory, item)
                )
    return font_file_list

def set_application_font(name, size):
    # Load the fonts
    font_file_list = get_fonts_from_resources()
    for file in font_file_list:
        data.QFontDatabase.addApplicationFont(file)
    # Check if the font is available
    fdb = data.QFontDatabase()
    font_found = False
    for f in fdb.families():
        if name.lower() in f.lower():
            font_found = True
            name = f
            break
    if not font_found:
        raise ValueError(
            "Font '{}' is not installed on the system!".format(name)
        )
    # Apply the font for the whole application
    font = data.QFont(name, size)
    data.current_font_name = name
    data.current_font_size = size
    data.application.setFont(font)