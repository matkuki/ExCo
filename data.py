
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2018 Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

##  FILE DESCRIPTION:
##      Module that holds objects that will be used across modules.

import os
import sys
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
PyQt4 / PyQt5 selection

NOTE:
    Objects are imported so that they can be used either directly with data.QSize,
    or by specifiying the full namespace with data.PyQt.QtCore.QSize!
"""
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
# Safety check for PyQt mode selection
if PYQT_MODE != 4 and PYQT_MODE != 5:
    raise Exception("PyQt mode has to be either 4 or 5!")


"""
-----------------------------------------------------------
Compatibility mode test for PyQt versions lower than 4.11
-----------------------------------------------------------
"""
try:
    PyQt.Qsci.QsciLexerCoffeeScript
    compatibility_mode = False
except:
    compatibility_mode = True


"""
File extension lists
"""
ext_python              = [".py", ".pyw", ".pyi", ".scons"]
ext_cython              = [".pyx", ".pxd", ".pxi"]
ext_c                   = [".c", ".h"]
ext_cpp                 = [".c++", ".h++", ".cc", ".hh", ".cpp", ".hpp", ".cxx", ".hxx"]
ext_pascal              = [".pas", ".pp", ".lpr", ".cyp"]
ext_oberon              = [".mod", ".ob", ".ob2", ".cp"]
ext_ada                 = [".ads", ".adb"]
ext_json                = [".json"]
ext_lua                 = [".lua"]
ext_d                   = [".d"]
ext_nim                 = [".nim", ".nims"]
ext_perl                = [".pl", ".pm"]
ext_xml                 = [".xml", ".tpy"]
ext_batch               = [".bat",  ".batch"]
ext_bash                = [".sh"]
ext_ini                 = [".ini"]
ext_text                = [".txt", ".text"]
ext_coffeescript        = [".coffee"]
ext_csharp              = [".cs"]
ext_java                = [".java"]
ext_javascript          = [".js"]
ext_octave              = [".m"]
ext_routeros            = [".rsc"]
ext_sql                 = [".sql"]
ext_postscript          = [".ps",]
ext_fortran             = [".f90", ".f95", ".f03"]
ext_fortran77           = [".f", ".for"]
ext_idl                 = [".idl"]
ext_ruby                = [".rb", ".rbw"]
ext_html                = [".html", ".htm"]
ext_css                 = [".css"]
ext_awk                 = [".awk"]
ext_cicode              = [".ci"]


"""
-------------------------------------------------
Global enumerations
-------------------------------------------------
"""
class FileStatus:
    OK          = 0
    MODIFIED    = 1

class CanSave:
    YES = 0
    NO  = 1

class SearchResult:
    NOT_FOUND   = None
    FOUND       = 1
    CYCLED      = 2

class WindowMode:
    THREE   = 0
    ONE     = 1

class MainWindowSide:
    LEFT    = 0
    RIGHT   = 1

class ReplType:
    SINGLE_LINE = 0
    MULTI_LINE  = 1

class Direction:
    LEFT    = 0
    RIGHT   = 1 

class SpinDirection:
    CLOCKWISE           = 0
    COUNTER_CLOCKWISE   = 1

class MessageType:
    ERROR           = 0
    WARNING         = 1
    SUCCESS         = 2
    DIFF_UNIQUE_1   = 3
    DIFF_UNIQUE_2   = 4
    DIFF_SIMILAR    = 5

class HexButtonFocus:
    NONE        = 0
    TAB         = 1
    WINDOW      = 2

class NodeDisplayType:
    DOCUMENT    = 0
    TREE        = 1

class TreeDisplayType:
    NODES               = 0
    FILES               = 1
    FILES_WITH_LINES    = 2


"""
--------------------------------------------------------
Various stored settings for global use.
These are the DEFAULT values, override them in the user
configuration file!
--------------------------------------------------------
"""
application_version = "6.16"
# Global variable that holds state of logging mode
logging_mode = False
# Global referenc to the log display window, so it can be used anywhere
log_window = None
# Global reference to the Qt application
application = None
# Global string with the application directory
application_directory = file_directory
# Home directory
home_directory = os.path.realpath(str(pathlib.Path.home())) \
    .replace('\\', '/')
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
default_config_file_content = '''
# -*- coding: utf-8 -*-

##  FILE DESCRIPTION:
##      Normal module with a special name that holds custom user functions/variables.
##      To manipulate the editors/windows, take a look at the QScintilla details at:
##      http://pyqt.sourceforge.net/Docs/QScintilla2
##
##  NOTES:
##      Built-in special function escape sequence: "lit#"
##          (prepend it to escape built-ins like: cmain, set_all_text, lines, ...)

"""
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

data.tab_width = 4
data.terminal = "xterm"
data.edge_marker_column = 80
data.zoom_factor = 0
data.tree_display_font_size = 10
data.tree_display_icon_size = 16
form.repl_helper.zoomTo(data.zoom_factor)

# Custom keyboard shortcuts
data.copy_keys = 'Ctrl+C'

# Example of got to customize the menu font and menu font scaling
#data.custom_menu_scale = 25
#data.custom_menu_font = ("Segoe UI", 10, data.QFont.Bold)
#data.custom_menu_scale = None
#data.custom_menu_font = None

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
"""

'''
# Application icon image that will be displayed on all Qt widgets
application_icon = os.path.join(resources_directory,  "exco-icon.png") \
    .replace('\\', '/')
# Ex.Co. information image displayed when "About Ex.Co" 
# action is clicked in the menubar "Help" menu
about_image = os.path.join(resources_directory,  "exco-info.png") \
    .replace('\\', '/')
# Terminal console program used on GNU/Linux
terminal = "x-terminal-emulator"
# Default tree display font size (file-tree, node-tree, ...)
tree_display_font_size = 10
tree_display_icon_size = 16
# Default font
current_font_name = "Source Code Pro"
current_font_size = 9
# Current theme
# Themes need PyQt version defined beforehand, as they also import the data module
import themes
theme = themes.Air
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

# Show PyQt/QScintilla version that is being used and if running in 
# QScintilla compatibility mode
LIBRARY_VERSIONS = "PyQt" + PyQt.QtCore.PYQT_VERSION_STR
LIBRARY_VERSIONS += " / QScintilla" + PyQt.Qsci.QSCINTILLA_VERSION_STR
if compatibility_mode == True:
    LIBRARY_VERSIONS += "(Compatibility mode)"




"""
--------------------------------------
Various global functions and routines
--------------------------------------
"""
def print_log(*args, **kwargs):
    """Internal module function that runs the append_message method of the log window"""
    if log_window != None:
        log_window.append_message(*args)
