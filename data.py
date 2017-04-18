
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2017 Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

##  FILE DESCRIPTION:
##      Module that holds objects that will be used across modules.

import sys


"""
PyQt4 / PyQt5 selection
"""
# Widgets that were moved from the QtGui module to the QtWidgets module in PyQt5
moved_widgets = [
    "QApplication", "QMainWindow", "QTreeView", "QLineEdit", "QDialog",
    "QGroupBox", "QTabWidget", "QTextEdit", "QTabBar", "QMenu", "QMenuBar",
    "QLabel", "QAction", "QGridLayout", "QStatusBar", "QVBoxLayout",
    "QSplitter", "QToolButton", "QToolBar", "QAbstractItemView", "QMessageBox",
    "QFileDialog", "QTextEdit", "QWidget"
]

try:
    import PyQt5.Qsci
    import PyQt5.QtCore
    import PyQt5.QtGui
    import PyQt5.QtWidgets
    PyQt = PyQt5
    """
    Move the moved widgets into this module so the reference in other modules
    will always be the same regardless of which PyQt version you are using.
    """
    # Get a reference to this (data) module
    thismodule = sys.modules[__name__]
    # Add the references to this module dynamically
    for widget in moved_widgets:
        setattr(thismodule, widget, getattr(PyQt5.QtWidgets, widget))
    # Set the constant for the PyQt version
    PYQT_MODE = 5
except:
    import PyQt4.Qsci
    import PyQt4.QtCore
    import PyQt4.QtGui
    PyQt = PyQt4
    """
    Move the moved widgets into this module so the reference in other modules
    will always be the same regardless of which PyQt version you are using.
    """
    # Get a reference to this (data) module
    thismodule = sys.modules[__name__]
    # Add the references to this module dynamically
    for widget in moved_widgets:
        setattr(thismodule, widget, getattr(PyQt4.QtGui, widget))
    # Set the constant for the PyQt version
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


# Themes need PyQt version defined beforehand, as they also import the data module
import themes

"""
File extension lists
"""
ext_python              = [".py", ".pyw", ".scons"]
ext_cython             = [".pyx", ".pxd", ".pxi"]
ext_c                   = [".c", ".h"]
ext_cpp                 = [".c++", ".h++", ".cc", ".hh", ".cpp", ".hpp", ".cxx", ".hxx"]
ext_pascal              = [".pas", ".pp", ".lpr", ".cyp"]
ext_oberon              = [".mod", ".ob", ".ob2", ".cp"]
ext_ada                 = [".ads", ".adb"]
ext_json                = [".json"]
ext_lua                 = [".lua"]
ext_d                   = [".d"]
ext_nim                 = [".nim"]
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
-------------------------------------------
Various stored settings for global use
-------------------------------------------
"""
application_version = "6.3"
# Global variable that holds state of logging mode
logging_mode = False
# Global referenc to the log display window, so it can be used anywhere
log_window = None
# Global reference to the Qt application
application = None
# Global string with the application directory
application_directory = ""
# User configuration file
config_file = "user_functions.cfg"
# Global string with the resources directory
resources_directory = "resources"
# Application icon image that will be displayed on all Qt widgets
application_icon = "exco-icon.png"
# Ex.Co. information image displayed when "About Ex.Co" 
# action is clicked in the menubar "Help" menu
about_image = "exco-info.png"
# Funcion wheel background image
function_wheel_image = "various/function-wheel.png"
# Maximum limit of highlighting instances
maximum_highlights = 300
# Column at which the edge marker is shown in documents
edge_marker_column = 90
# Global width of tabs
tab_width = 4
# Terminal console program used on GNU/Linux
terminal = "lxterminal"
# Zoom factor when a new editor is created (default is 0)
zoom_factor = 0
# Default tree display font size (file-tree, node-tree, ...)
tree_display_font_size = 10
# Default EOL style in editors (EolWindows-CRLF, EolUnix-LF, EolMac-CR)
default_eol = PyQt.Qsci.QsciScintilla.EolUnix
# Current theme
theme = themes.Air


# Show PyQt/QScintilla version that is being used and if running in 
# QScintilla compatibility mode
LIBRARY_VERSIONS = "PyQt" + PyQt.QtCore.PYQT_VERSION_STR
LIBRARY_VERSIONS += " / QScintilla" + PyQt.Qsci.QSCINTILLA_VERSION_STR
if compatibility_mode == True:
    LIBRARY_VERSIONS += "(Compatibility mode)"


"""
-------------------------------------------
Keyboard shortcuts 
-------------------------------------------

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
THESE BINDINGS ARE THE DEFAULT, DON'T CHANGE THEM HERE!
CUSTOM BINDINGS SHOULD BE OVERRIDDEN IN THE USER CONFIGURATION FILE 'user_functions.cfg'!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""
new_file_keys = 'Ctrl+N'
open_file_keys = 'Ctrl+O'
save_file_keys = 'Ctrl+S'
saveas_file_keys = 'Ctrl+Shift+S'
close_tab_keys = 'Ctrl+W'
find_keys = 'Ctrl+F'
regex_find_keys = 'Alt+F'
find_and_replace_keys = 'Ctrl+Shift+F'
regex_find_and_replace_keys = 'Alt+Shift+F'
highlight_keys = 'Ctrl+G'
regex_highlight_keys = 'Alt+G'
clear_highlights_keys = 'Ctrl+Shift+G'
replace_selection_keys = 'Ctrl+H'
regex_replace_selection_keys = 'Alt+H'
replace_all_keys = 'Ctrl+Shift+H'
regex_replace_all_keys = 'Alt+Shift+H'
toggle_comment_keys = 'Ctrl+Shift+C'
toggle_autocompletion_keys = 'Ctrl+K'
toggle_wrap_keys = 'Ctrl+P'
reload_file_keys = 'F9'
node_tree_keys = 'F8'
goto_line_keys = 'Ctrl+M'
indent_to_cursor_keys = 'Ctrl+I'
to_uppercase_keys = 'Alt+U'
to_lowercase_keys = 'Alt+L'
find_in_documents_keys = 'Ctrl+F4'
find_replace_in_documents_keys = 'Ctrl+F5'
replace_all_in_documents_keys = 'Ctrl+F6'
find_in_files_keys = 'Ctrl+F2'
find_files_keys = 'Ctrl+F1'
replace_in_files_keys = 'Ctrl+F3'
cwd_tree_keys = 'F7'
function_wheel_toggle_keys = 'F1'
maximize_window_keys = 'F12'
main_focus_keys = 'Ctrl+1'
upper_focus_keys = 'Ctrl+2'
lower_focus_keys = 'Ctrl+3'
toggle_log_keys = 'F10'
spin_clockwise_keys = 'Ctrl+PgDown'
spin_counterclockwise_keys = 'Ctrl+PgUp'
toggle_mode_keys = 'F5'
toggle_main_window_side_keys = 'F6'
move_tab_right_keys = 'Ctrl+.'
move_tab_left_keys = 'Ctrl+,'
toggle_edge_keys = 'Ctrl+E'
reset_zoom_keys = "Alt+Z"
bookmark_toggle_keys = "CTRL+B"
bookmark_goto_keys = "Alt"
bookmark_store_keys = "Alt+Shift"
repeat_eval_keys = 'F3'
repl_focus_single_1_keys = 'Ctrl+R'
repl_focus_single_2_keys = 'Ctrl+4'
repl_focus_multi_keys = 'Ctrl+5'
# Custom editor commands
copy_keys = 'Ctrl+C'
cut_keys = 'Ctrl+X'
paste_keys = 'Ctrl+V'
undo_keys = 'Ctrl+Z'
redo_keys = 'Ctrl+Y'
select_all_keys = 'Ctrl+A'
indent_keys = 'Tab'
unindent_keys = 'Shift+Tab'
delete_start_of_word_keys = 'Ctrl+BackSpace'
delete_end_of_word_keys = 'Ctrl+Delete'
delete_start_of_line_keys = 'Ctrl+Shift+BackSpace'
delete_end_of_line_keys = 'Ctrl+Shift+Delete'
go_to_start_keys = 'Ctrl+Home'
go_to_end_keys = 'Ctrl+End'
select_page_up_keys = 'Shift+PageUp'
select_page_down_keys = 'Shift+PageDown'
select_to_start_keys = 'Ctrl+Shift+Home'
select_to_end_keys = 'Ctrl+Shift+End'
scroll_up_keys = 'PageUp'
scroll_down_keys = 'PageDown'
line_cut_keys = 'Ctrl+L'
line_copy_keys = 'Ctrl+Shift+T'
line_delete_keys = 'Ctrl+Shift+L'
line_transpose_keys = 'Ctrl+T'
line_selection_duplicate_keys = 'Ctrl+D'



"""
--------------------------------------
Various global functions and routines
--------------------------------------
"""
def print_log(message):
    """Internal module function that runs the append_message method of the log window"""
    if log_window != None:
        log_window.append_message(message)
