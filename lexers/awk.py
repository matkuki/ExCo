# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-present Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import keyword
import builtins
import re
import functions
import qt
import data
import time
import lexers


class AWK(qt.QsciLexerCustom):
    """
    Custom lexer for the AWK programming languages
    """
    styles = {
        "Default" : 0,
        "Comment" : 1,
        "Keyword" : 2,
        "BuiltInVariable" : 3,
        "BuiltInFunction" : 4,
        "String" : 5,
        "Number" : 6,
        "Operator" : 7,
    }
    # Class variables
    keyword_list = [
        "BEGIN", "delete", "for", "in", "printf", "END", 
        "do", "function", "next", "return", "break", 
        "else", "getline", "print", "while", "continue", 
        "exit", "if", 
    ]
    builtin_variable_list = [
        "ARGC", "ARGV", "CONVFMT", "ENVIRON", "FILENAME", "FNR",
        "FS", "NF", "NR", "OFMT", "OFS", "ORS", "RLENGTH",
        "RS", "RSTART", "SUBSEP",
    ]
    builtin_function_list = [
        "atan2", "index", "match", "sprintf", "substr", "close", 
        "int", "rand", "sqrt", "system", "cos", "length", 
        "sin", "srand", "tolower", "exp", "log", "split", 
        "sub", "toupper", "gsub", 
    ]
    operator_list = [
        "=", "+", "-", "*", "/", "<", ">", "@", "$", ".",
        "~", "&", "%", "|", "!", "?", "^", ".", ":", "\"",
    ]
    splitter = re.compile(r"(\{\.|\.\}|\#|\'|\"\"\"|\n|\s+|\w+|\W)")
    # Characters that autoindent one level on pressing Return/Enter
    autoindent_characters = ["{"]

    def __init__(self, parent=None):
        """
        Overridden initialization
        """
        # Initialize superclass
        super().__init__()
        # Set the default style values
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
        # Reset autoindentation style
        self.setAutoIndentStyle(0)
        # Set the theme
        self.set_theme(data.theme)
    
    def language(self):
        return "AWK"
    
    def description(self, style):
        if style < len(self.styles):
            description = "Custom lexer for the AWK programming languages"
        else:
            description = ""
        return description
    
    def defaultStyle(self):
        return self.styles["Default"]
    
    def braceStyle(self):
        return self.styles["Default"]
    
    def defaultFont(self, style):
        return qt.QFont(data.current_font_name, data.current_font_size)
    
    def set_theme(self, theme):
        for style in self.styles:
            # Papers
            self.setPaper(
                qt.QColor(data.theme["fonts"][style.lower()]["background"]), 
                self.styles[style]
            )
            # Fonts
            lexers.set_font(self, style, theme["fonts"][style.lower()])
    
    def styleText(self, start, end):
        """
        Overloaded method for styling text.
        """
        # Style in pure Python, VERY SLOW!
        editor = self.editor()
        if editor is None:
            return
        # Initialize the styling
        self.startStyling(start)
        # Scintilla works with bytes, so we have to adjust
        # the start and end boundaries
        text = bytearray(editor.text(), "utf-8")[start:end].decode("utf-8")
        # Loop optimizations
        setStyling      = self.setStyling
        operator_list   = self.operator_list
        builtin_variable_list = self.builtin_variable_list
        builtin_function_list = self.builtin_function_list
        keyword_list    = self.keyword_list
        DEFAULT         = self.styles["Default"]
        COMMENT         = self.styles["Comment"]
        KEYWORD         = self.styles["Keyword"]
        BUILTINVARIABLE = self.styles["BuiltInVariable"]
        BUILTINFUNCTION = self.styles["BuiltInFunction"]
        STRING          = self.styles["String"]
        NUMBER          = self.styles["Number"]
        OPERATOR        = self.styles["Operator"]
        # Initialize various states and split the text into tokens
        stringing = False
        commenting = False
        tokens = [
            (token, len(bytearray(token, "utf-8"))) 
                for token in self.splitter.findall(text)
        ]
        # Style the tokens accordingly
        for i, token in enumerate(tokens):
            if commenting == True:
                # Continuation of comment
                setStyling(token[1], COMMENT)
                # Check if comment ends
                if "\n" in token[0]:
                    commenting = False
            elif stringing == True:
                # Continuation of a string
                setStyling(token[1], STRING)
                # Check if string ends
                if (token[0] == "\"" and (tokens[i-1][0] != "\\") 
                    or "\n" in token[0]):
                        stringing = False
            elif token[0] == "#":
                setStyling(token[1], COMMENT)
                commenting = True
            elif token[0] == "\"":
                # Start of a string
                setStyling(token[1], STRING)
                stringing = True
            elif token[0] in operator_list:
                setStyling(token[1], OPERATOR)
            elif token[0] in keyword_list:
                setStyling(token[1], KEYWORD)
            elif token[0] in builtin_variable_list:
                setStyling(token[1], BUILTINVARIABLE)
            elif token[0] in builtin_function_list:
                setStyling(token[1], BUILTINFUNCTION)
            else:
                setStyling(token[1], DEFAULT)
