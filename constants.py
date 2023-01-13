# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2023 Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import enum

# File extension lists
supported_file_extentions = {
    #"assembly": [".s", ".S", ".Asm"],
    "ada": [".ads", ".adb"],
    "awk": [".awk"],
    "bash": [".sh"],
    "batch": [".bat",  ".batch"],
    "c": [".c", ".h"],
    "c++": [".c++", ".h++", ".cc", ".hh", ".cpp", ".hpp", ".cxx", ".hxx"],
    "cicode": [".ci"],
    "coffeescript": [".coffee"],
    "csharp": [".cs"],
    "css": [".css"],
    "cython": [".pyx", ".pxd", ".pxi"],
    "d": [".d"],
    "fortran": [".f90", ".f95", ".f03"],
    "fortran77": [".f", ".for"],
    "html": [".html", ".htm", ".svelte"],
    "idl": [".idl"],
    "ini": [".ini"],
    "java": [".java"],
    "javascript": [".js", ".jsx", ".ts", ".tsx"],
    "json": [".json"],
    "lua": [".lua"],
    "nim": [".nim", ".nims"],
    "oberon/modula": [".mod", ".ob", ".ob2", ".cp"],
    "octave": [".m"],
    "pascal": [".pas", ".pp", ".lpr", ".cyp"],
    "perl": [".pl", ".pm"],
    "php": [".php"],
    "postscript": [".ps",],
    "python": [".py", ".pyw", ".pyi", ".scons"],
    "routeros": [".rsc"],
    "ruby": [".rb", ".rbw"],
    "sql": [".sql"],
    "text": [".txt", ".text"],
    "xml": [".xml", ".tpy"],
}

# Global enumerations
class FileStatus(enum.Enum):
    OK       = 0
    MODIFIED = 1

class FileType(enum.Enum):
    Text = 0
    Hex  = 1

class CanSave:
    YES = 0
    NO  = 1

class SearchResult(enum.Enum):
    NOT_FOUND = None
    FOUND     = 1
    CYCLED    = 2

class WindowMode(enum.Enum):
    THREE = 0
    ONE   = 1

class MainWindowSide(enum.Enum):
    LEFT  = 0
    RIGHT = 1

class ReplType(enum.Enum):
    SINGLE_LINE = 0
    MULTI_LINE  = 1

class Direction(enum.Enum):
    LEFT  = 0
    RIGHT = 1

class SpinDirection(enum.Enum):
    CLOCKWISE         = 0
    COUNTER_CLOCKWISE = 1

class MessageType(enum.Enum):
    ERROR         = 0
    WARNING       = 1
    SUCCESS       = 2
    DIFF_UNIQUE_1 = 3
    DIFF_UNIQUE_2 = 4
    DIFF_SIMILAR  = 5

class HexButtonFocus(enum.Enum):
    NONE   = 0
    TAB    = 1
    WINDOW = 2

class NodeDisplayType(enum.Enum):
    DOCUMENT = 0
    TREE     = 1

class TreeDisplayType(enum.Enum):
    NODES            = 0
    FILES            = 1
    FILES_WITH_LINES = 2

class DialogResult(enum.Enum):
    Ok = 0
    Cancel = 1
    Yes = 2
    No = 3
    Quit = 4
    Close = 5
    Restore = 6
    SaveAllAndQuit = 7
    SaveAndClose = 8
    SaveAndRestore = 9