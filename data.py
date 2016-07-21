
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

"""
-------------------------------------------
Various stored settings for global use
-------------------------------------------
"""
APPLICATION_VERSION     = "4.3"
#Global variable that holds state of logging mode
logging_mode            = False
#Global referenc to the log display window, so it can be used anywhere
log_window              = None
#Global reference to the Qt application
application             = None
#Global string with the application directory
application_directory   = ""
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


"""
File extension lists
"""
ext_python              = [".py", ".pyw"]
ext_cpython             = [".pyx", ".pxd"]
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
-----------------------------
Various global functions and routines
-----------------------------
"""
def print_log(message):
    """Internal module function that runs the append_message method of the log window"""
    try:
        log_window.append_message(message)
    except:
        return
