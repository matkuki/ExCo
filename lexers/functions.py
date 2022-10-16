
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2018 Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""


##  FILE DESCRIPTION:
##      Functions used by lexers

import keyword
import builtins
import re
import functions
import data
import time
import lexers

def set_font(lexer, style_name, style_options):
    style_index = lexer.styles[style_name]
    lexer.setColor(
        data.QColor(style_options["color"]),
        style_index
    )
    weight = data.QFont.Weight.Normal
    if style_options["bold"]:
        weight = data.QFont.Weight.Bold
#    elif bold == 2:
#        weight = data.QFont.Weight.Black
    lexer.setFont(
        data.QFont(
            data.current_editor_font_name,
            data.current_editor_font_size,
            weight=weight
        ),
        style_index
    )

def get_lexer_from_file_type(file_type):
    current_file_type = file_type
    lexer = None
    if file_type == "python":
        if lexers.nim_lexers_found == True:
            lexer = lexers.CustomPython()
        else:
            lexer = lexers.Python()
    elif file_type == "cython":
        lexer = lexers.Cython()
    elif file_type == "c":
        lexer = lexers.CPP()
    elif file_type == "c++":
        lexer = lexers.CPP()
    elif file_type == "cmake":
        lexer = lexers.CMake()
    elif file_type == "pascal":
        lexer = lexers.Pascal()
    elif file_type == "oberon/modula":
        lexer = lexers.Oberon()
    elif file_type == "ada":
        lexer = lexers.Ada()
    elif file_type == "d":
        lexer = lexers.D()
    elif file_type == "nim":
        lexer = lexers.Nim()
    elif file_type == "makefile":
        lexer = lexers.Makefile()
    elif file_type == "xml":
        lexer = lexers.XML()
    elif file_type == "batch":
        lexer = lexers.Batch()
    elif file_type == "bash":
        lexer = lexers.Bash()
    elif file_type == "lua":
        lexer = lexers.Lua()
    elif file_type == "coffeescript":
        if data.compatibility_mode == False:
            lexer = lexers.CoffeeScript()
        else:
            lexer = lexers.Text()
    elif file_type == "c#":
        lexer = lexers.CPP()
    elif file_type == "java":
        lexer = lexers.Java()
    elif file_type == "javascript":
        lexer = lexers.JavaScript()
    elif file_type == "octave":
        lexer = lexers.Octave()
    elif file_type == "routeros":
        lexer = lexers.RouterOS()
    elif file_type == "sql":
        lexer = lexers.SQL()
    elif file_type == "postscript":
        lexer = lexers.PostScript()
    elif file_type == "php":
        lexer = lexers.Php()
    elif file_type == "fortran":
        lexer = lexers.Fortran()
    elif file_type == "fortran77":
        lexer = lexers.Fortran77()
    elif file_type == "idl":
        lexer = lexers.IDL()
    elif file_type == "ruby":
        lexer = lexers.Ruby()
    elif file_type == "html":
        lexer = lexers.HTML()
    elif file_type == "css":
        lexer = lexers.CSS()
    elif file_type == "awk":
        lexer = lexers.AWK()
    elif file_type == "cicode":
        lexer = lexers.CiCode()
    else:
        #No lexer was chosen, set file type to text and lexer to plain text
        current_file_type = "TEXT"
        lexer = lexers.Text()
    return (current_file_type, lexer)

def get_comment_style_for_lexer(lexer):
    open_close_comment_style = False
    comment_string = None
    end_comment_string = None
    if isinstance(lexer, lexers.CustomPython):
        comment_string = "#"
    elif isinstance(lexer, lexers.Python):
        comment_string = "#"
    elif isinstance(lexer, lexers.Cython):
        comment_string = "#"
    elif isinstance(lexer, lexers.AWK):
        comment_string = "#"
    elif isinstance(lexer, lexers.CPP):
        comment_string = "//"
    elif isinstance(lexer, lexers.CiCode):
        comment_string = "//"
    elif isinstance(lexer, lexers.Pascal):
        comment_string = "//"
    elif isinstance(lexer, lexers.Oberon):
        open_close_comment_style = True
        comment_string = "(*"
        end_comment_string = "*)"
    elif isinstance(lexer, lexers.Ada):
        comment_string = "--"
    elif isinstance(lexer, lexers.D):
        comment_string = "//"
    elif isinstance(lexer, lexers.Nim):
        comment_string = "#"
    elif isinstance(lexer, lexers.Makefile):
        comment_string = "#"
    elif isinstance(lexer, lexers.XML):
        comment_string = None
    elif isinstance(lexer, lexers.Batch):
        comment_string = "::"
    elif isinstance(lexer, lexers.Bash):
        comment_string = "#"
    elif isinstance(lexer, lexers.Lua):
        comment_string = "--"
    elif data.compatibility_mode == False and isinstance(lexer, lexers.CoffeeScript):
        comment_string = "#"
    elif isinstance(lexer, lexers.Java):
        comment_string = "//"
    elif isinstance(lexer, lexers.JavaScript):
        comment_string = "//"
    elif isinstance(lexer, lexers.Octave):
        comment_string = "#"
    elif isinstance(lexer, lexers.RouterOS):
        comment_string = "#"
    elif isinstance(lexer, lexers.SQL):
        comment_string = "#"
    elif isinstance(lexer, lexers.PostScript):
        comment_string = "%"
    elif isinstance(lexer, lexers.Fortran):
        comment_string = "c "
    elif isinstance(lexer, lexers.Fortran77):
        comment_string = "c "
    elif isinstance(lexer, lexers.IDL):
        comment_string = "//"
    elif isinstance(lexer, lexers.Ruby):
        comment_string = "#"
    elif isinstance(lexer, lexers.HTML):
        open_close_comment_style = True
        comment_string = "<!--"
        end_comment_string = "-->"
    elif isinstance(lexer, lexers.CSS):
        open_close_comment_style = True
        comment_string = "/*"
        end_comment_string = "*/"
    # Save the comment options to the lexer
    return (open_close_comment_style, comment_string, end_comment_string)




