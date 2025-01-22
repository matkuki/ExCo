# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-present Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

##  FILE DESCRIPTION:
##      Module that holds objects that will be used across modules.

import os
import sys
import enum
import inspect
import pathlib
import platform

import qt
from constants import *

# File directory reference
if getattr(sys, "frozen", False):
    # The application is frozen
    file_directory = os.path.dirname(sys.executable)
else:
    # The application is not frozen
    file_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

"""
--------------------------------------------------------
Various stored settings for global use.
These are the DEFAULT values, override them in the user
configuration file!
--------------------------------------------------------
"""
application_version = "7.8"
# Global variables
command_line_options = None
debug_mode = False
logging_mode = False
# Global referenc to the log display window, so it can be used anywhere
log_window = None
# Global reference to the Qt application
application = None
# Global string with the application directory
application_directory = file_directory
# Home directory
try:
    home_directory = os.path.realpath(str(pathlib.Path.home())) \
        .replace('\\', '/')
except:
    home_directory = os.path.expanduser('~')
# Global string with the resources directory
resources_directory = os.path.join(application_directory,  "resources") \
    .replace('\\', '/')
# Global settings directory
settings_directory = os.path.join(home_directory, ".exco") \
    .replace('\\', '/')
# Fonts directory
fonts_directory = os.path.join(resources_directory, "fonts/") \
    .replace('\\', '/')
# Global string variable for the current platform name ("Windows", "Linux", ...),
# and a flag if running on the Raspberry PI
platform = platform.system()
on_windows = (platform == "Windows")
on_linux = (platform == "Linux")
on_rpi = False
if os.name == "posix":
    on_rpi = (os.uname()[1] == "raspberrypi")
# User configuration file
config_file = os.path.join(settings_directory,  "userfunctions.cfg") \
    .replace('\\', '/')
# Global signal dispatcher
signal_dispatcher = None
# Application icon image that will be displayed on all Qt widgets
application_icon = os.path.join(resources_directory, "exco-icon.png") \
    .replace('\\', '/')
# Ex.Co. information image displayed when "About Ex.Co" 
# action is clicked in the menubar "Help" menu
about_image = os.path.join(resources_directory, "exco-info.png") \
    .replace('\\', '/')
# Settings filenames
settings_filename = {
    "mark-0": "exco.ini",
    "mark-1": "exco.mk1.ini",
    "mark-2": "exco.mk2.ini",
}
# Terminal console program used on GNU/Linux
terminal = "x-terminal-emulator"
# Default tree display icon size
tree_display_icon_size = 16
# Default font
current_font_name = "Selawik"
current_font_size = 10
def get_current_font():
    return qt.QFont(current_font_name, int(current_font_size))
current_editor_font_name = "Source Code Pro"
current_editor_font_size = 10
def get_editor_font():
    return qt.QFont(current_editor_font_name, int(current_editor_font_size))

# Scaling
toplevel_menu_scale = 100.0

# Sizes
standard_button_size = 50

# Current theme
# Themes need PyQt version defined beforehand, as they also import the data module
theme = None
# Custom MenuBar scale factor
custom_menu_scale = None
# Custom MenuBar scale font
"""
Windows Vista Default:
    ("Segoe UI", 9, qt.PyQt.QtGui.QFont.Normal)
"""
custom_menu_font = None
# Function information that is used between modules
global_function_information = {}
# REPL messages tab name
repl_messages_tab_name = "REPL MESSAGES"
file_explorer_tab_name = "FILE EXPLORER"

# Show PyQt/QScintilla version that is being used and if running in 
# QScintilla compatibility mode
LIBRARY_VERSIONS = "PyQt{} / QScintilla{}".format(
    qt.PyQt.QtCore.PYQT_VERSION_STR,
    qt.PyQt.Qsci.QSCINTILLA_VERSION_STR
)

# Store all Qt keys as a dictionary
keys = {}
if qt.PYQT_MODE < 6:
    keys_namespace = qt.Qt
else:
    keys_namespace = qt.Qt.Key
 
for k in dir(keys_namespace):
    if k.startswith("Key_"):
        value = getattr(keys_namespace, k)
        keys[value] = k

# Various settings
restore_last_session = True
