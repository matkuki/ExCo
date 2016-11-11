
# -*- coding: utf-8 -*-

"""
    Ex.Co. LICENSE :
        This file is part of Ex.Co..

        Ex.Co. is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        Ex.Co. is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with Ex.Co..  If not, see <http://www.gnu.org/licenses/>.


    PYTHON LICENSE :
        "Python" and the Python logos are trademarks or registered trademarks of the Python Software Foundation,
        used by Ex.Co. with permission from the Foundation


    Cython LICENSE:
        Cython is freely available under the open source Apache License


    PyQt4 LICENSE :
        PyQt4 is licensed under the GNU General Public License version 3
    PyQt Alternative Logo LICENSE:
        The PyQt Alternative Logo is licensed under Creative Commons CC0 1.0 Universal Public Domain Dedication


    Qt Logo LICENSE:
        The Qt logo is copyright of Digia Plc and/or its subsidiaries.
        Digia, Qt and their respective logos are trademarks of Digia Corporation in Finland and/or other countries worldwide.


    Tango Icons LICENSE:
        The Tango base icon theme is released to the Public Domain.
        The Tango base icon theme is made possible by the Tango Desktop Project.

    My Tango Style Icons LICENSE:
        The Tango Icons I created are released under the GNU General Public License version 3.


    Eric6 LICENSE:
        Eric6 IDE is licensed under the GNU General Public License version 3


    Nuitka LICENSE:
        Nuitka is a Python compiler compatible with Ex.Co..
        Nuitka is licensed under the Apache license.
"""


##  FILE DESCRIPTION:
##      Module that holds objects that will be used across modules.

import PyQt4.Qsci
import themes


"""
File extension lists
"""
ext_python              = [".py", ".pyw"]
ext_cpython             = [".pyx", ".pxd", ".pxi"]
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
APPLICATION_VERSION     = "5.4"
#Global variable that holds state of logging mode
logging_mode            = False
#Global referenc to the log display window, so it can be used anywhere
log_window              = None
#Global reference to the Qt application
application             = None
#Global string with the application directory
application_directory   = ""
#User configuration file
config_file = "user_functions.cfg"
#Global string with the resources directory
resources_directory     = "resources"
#Application icon image that will be displayed on all Qt widgets
application_icon        = "Exco_Icon.png"
#Ex.Co. information image displayed when "About Ex.Co" action is clicked in the menubar "Help" menu
about_image             = "ExCo_Info.png"
#Funcion wheel background image
function_wheel_image    = "various/function-wheel.png"
#Maximum limit of highlighting instances
MAXIMUM_HIGHLIGHTS      = 300
#Column at which the edge marker is shown in documents
EDGE_MARKER_COLUMN      = 90
#Global width of tabs
tab_width = 4
#Terminal console program used on GNU/Linux
terminal = "lxterminal"
#Zoom factor when a new editor is created (default is 0)
zoom_factor = 0
#Default tree display(file-tree, node-tree, ...)
tree_display_font_size = 10
#Default EOL style (EolWindows-CRLF, EolUnix-LF, EolMac-CR)
default_eol = PyQt4.Qsci.QsciScintilla.EolUnix
#Current theme
theme = themes.Air


"""
-------------------------------------------
Keyboard shortcuts 
-------------------------------------------

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
THESE BINDINGS ARE THE DEFAULT, DON'T CHANGE THEM HERE!
CUSTOM BINDINGS SHOULD BE OVERIDDEN IN THE USER CONFIGURATION FILE 'user_functions.cfg'!
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
spin_clockwise_keys = 'Ctrl+*'
spin_counterclockwise_keys = 'Ctrl+/'
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
#Custom editor commands
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
-----------------------------------------------------------
Compatibility mode test for PyQt versions lower than 4.11
-----------------------------------------------------------
"""
try:
    PyQt4.Qsci.QsciLexerCoffeeScript
    compatibility_mode = False
except:
    compatibility_mode = True


"""
--------------------------------------
Various global functions and routines
--------------------------------------
"""
def print_log(message):
    """Internal module function that runs the append_message method of the log window"""
    try:
        log_window.append_message(message)
    except:
        return
