# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2023 Matic Kukovec. 
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

if getattr(sys, "frozen", False):
    # The application is frozen
    file_directory = os.path.dirname(sys.executable)
else:
    # The application is not frozen
    file_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


"""
PyQt4 / PyQt5 / PyQt6 selection

NOTE:
    Objects are imported so that they can be used either directly with data.QSize,
    or by specifiying the full namespace with data.PyQt.QtCore.QSize!
"""
try:
    import PyQt6.Qsci
    import PyQt6.QtCore
    import PyQt6.QtGui
    import PyQt6.QtWidgets
    PyQt = PyQt6
    from PyQt6.Qsci import *
    from PyQt6.QtCore import *
    from PyQt6.QtGui import *
    from PyQt6.QtWidgets import *
    PYQT_MODE = 6
except:
    try:
        import PyQt5.Qsci
        import PyQt5.QtCore
        import PyQt5.QtGui
        import PyQt5.QtWidgets
        PyQt = PyQt5
        from PyQt5.Qsci import *
        from PyQt5.QtCore import *
        from PyQt5.QtGui import *
        from PyQt5.QtWidgets import *
        PYQT_MODE = 5
    except:
        import PyQt4.Qsci
        import PyQt4.QtCore
        import PyQt4.QtGui
        PyQt = PyQt4
        from PyQt4.Qsci import *
        from PyQt4.QtCore import *
        from PyQt4.QtGui import *
        PYQT_MODE = 4

from constants import *


"""
--------------------------------------------------------
Various stored settings for global use.
These are the DEFAULT values, override them in the user
configuration file!
--------------------------------------------------------
"""
application_version = "7.2"
# Global variable that holds state of logging mode
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
# Global string variable for the current platform name ("Windows", "Linux", ...),
# and a flag if running on the Raspberry PI
platform = platform.system()
on_rpi = False
if os.name == "posix":
    on_rpi = (os.uname()[1] == "raspberrypi")
# User configuration file
config_file = os.path.join(settings_directory,  "userfunctions.cfg") \
    .replace('\\', '/')
# Default user configuration file content
default_config_file_content = '''# -*- coding: utf-8 -*-

##  FILE DESCRIPTION:
##      Normal module with a special name that holds custom user functions/variables.
##      To manipulate the editors/windows, take a look at the QScintilla details at:
##      http://pyqt.sourceforge.net/Docs/QScintilla2
##
##  NOTES:
##      Built-in special function escape sequence: "lit#"
##          (prepend it to escape built-ins like: cmain, set_all_text, lines, ...)

\'\'\'
# These imports are optional as they are already imported 
# by the REPL, I added them here for clarity.
import data
import functions
import settings

# Imported for less typing
from gui import *


# Initialization function that gets executed only ONCE at startup
def first_scan():
    pass

# Example of got to customize the menu font and menu font scaling
#data.custom_menu_scale = 25
#data.custom_menu_font = ("Segoe UI", 10, data.QFont.Weight.Bold)
#data.custom_menu_scale = None
#data.custom_menu_font = None

def trim_whitespace():
    """
    Remove whitespace from back of every line in the main document
    """
    ll = []
    tab = form.get_tab_by_indication()
    for line in tab.line_list:
        ll.append(line.rstrip())
    tab.line_list = ll
trim_whitespace.autocompletion = "trim_whitespace()"

def align_assignments():
    """
    Align any assignments in the selected lines
    """
    tab = form.get_tab_by_indication()
    new_lines = []
    selected_text = tab.selectedText()
    max_left_size = 0
    for line in selected_text.split('\n'):
        if '=' in line and line.count('=') == 1:
            split_line = line.split('=')
            left_size = len(split_line[0].rstrip())
            if left_size > max_left_size:
                max_left_size = left_size
            new_lines.append(split_line)
        else:
            new_lines.append(line)
    for i in range(len(new_lines)):
        if isinstance(new_lines[i], list):
            new_lines[i] = "{} = {}".format(
                new_lines[i][0].rstrip().ljust(max_left_size, ' '),
                new_lines[i][1].strip()
            )
    tab.replaceSelectedText('\n'.join(new_lines))
align_assignments.autocompletion = "align_assignments()"

# Example function definition with defined autocompletion string
def delete_files_in_dir(extension=None, directory=None):
    # Delete all files with the selected file extension from the directory
    if isinstance(extension, str) == False:
        print("File extension argument must be a string!")
        return
    if directory == None:
        directory = os.getcwd()
    elif os.path.isdir(directory) == False:
        return
    print("Deleting '{:s}' files in:".format(extension))
    print(directory)
    for file in os.listdir(directory):
        file_extension = os.path.splitext(file)[1].lower()
        if file_extension == extension or file_extension == "." + extension:
            os.remove(os.path.join(directory, file))
            print(" - deleted file: {:s}".format(file))
    print("DONE")
delete_files_in_dir.autocompletion = "delete_files_in_dir(extension=\"\", directory=None)"
\'\'\'
'''
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
    return QFont(current_font_name, int(current_font_size))
current_editor_font_name = "Source Code Pro"
current_editor_font_size = 10
def get_editor_font():
    return QFont(current_editor_font_name, int(current_editor_font_size))

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
    ("Segoe UI", 9, PyQt.QtGui.QFont.Normal)
"""
custom_menu_font = None
# Function information that is used between modules
global_function_information = {}

# Global signal dispatcher
signal_dispatcher = None

# REPL messages tab name
repl_messages_tab_name = "REPL MESSAGES"
file_explorer_tab_name = "FILE EXPLORER"

# Show PyQt/QScintilla version that is being used and if running in 
# QScintilla compatibility mode
LIBRARY_VERSIONS = "PyQt{} / QScintilla{}".format(
    PyQt.QtCore.PYQT_VERSION_STR,
    PyQt.Qsci.QSCINTILLA_VERSION_STR
)

# Store all Qt keys as a dictionary
keys = {}
if PYQT_MODE < 6:
    keys_namespace = Qt
else:
    keys_namespace = Qt.Key
 
for k in dir(keys_namespace):
    if k.startswith("Key_"):
        value = getattr(keys_namespace, k)
        keys[value] = k
