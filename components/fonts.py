
"""
Copyright (c) 2021 embeetle.
"""


import os
import os.path
import sys
import traceback
import functools
import textwrap

import qt
import data
import functions

def __get_fonts_from_resources():
    directory = data.fonts_directory
    font_file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            item = functions.unixify_join(root, file)
            if item.lower().endswith('.ttf') or item.lower().endswith('.otf'):
                font_file_list.append(
                    functions.unixify_join(directory, item)
                )
    return font_file_list

def set_application_font(name, size):
    name = data.current_font_name
    # Load the fonts from 'resources/fonts'
    font_file_list = __get_fonts_from_resources()
    for file in font_file_list:
        qt.QFontDatabase.addApplicationFont(file)

    # Check if font is properly loaded
    search_font_name = name.lower()
    font_found = False
    if qt.PYQT_MODE < 6:
        for fontname in qt.QFontDatabase().families(): # noqa
            if search_font_name in fontname.lower():
                font_found = True
                break
    else:
        # The QFontDatabase class has now only static member functions. The constructor has been
        # deprecated.
        for fontname in qt.QFontDatabase.families():
            if search_font_name in fontname.lower():
                font_found = True
                break
    if not font_found:
        raise Exception("[Fonts] Could not find correct font!")

    # Apply the font for the whole application
    font = data.get_current_font()
    data.application.setFont(font)