# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-present Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import re

import qt
import data
import functions
import lexers


class CustomSpice(qt.QsciLexerCustom):
    """
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    !! This lexer is not needed as there is a built-in !!
    !! one for the Spice programming language          !!
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    Custom lexer for the Spice programming languages
    """
    styles = {
        "Default": 0,
        "Comment": 1,
        "Instruction0": 2,
        "Instruction1": 3,
        "Type": 4,
        "String": 5,
        "Number": 6,
        "Operator": 7,
    }
    # Class variables
    keyword_dictionary = {
        "Instruction0": ("ac", "alias", "alter", "alterparam", "append", "askvalues", "assertvalid", "autoscale", "break", "compose", "copy", "copytodoc", "dc", "delete", "destroy", "destroyvec", "diff", "display", "disto", "dowhile", "echo", "else", "end", "errorstop", "fftinit", "filter", "foreach", "fourier", "freqtotime", "function", "functionundef", "goto", "homecursors", "if", "isdisplayed", "label", "let", "linearize", "listing", "load", "loadaccumulator", "makelabel", "movelabel", "makesmithplot", "movecursorleft", "movecursorright", "msgbox", "nameplot", "newplot", "nextparam", "noise", "nopoints", "op", "plot", "plotf", "plotref", "poly", "print", "printcursors", "printevent", "printname", "printplot", "printstatus", "printtext", "printtol", "printunits", "printval", "printvector", "pwl", "pz", "quit", "removesmithplot", "rename", "repeat", "resume", "rotate", "runs", "rusage", "save", "sendplot", "sendscript", "sens", "set", "setcursor", "setdoc", "setlabel", "setlabeltype", "setmargins", "setnthtrigger", "setunits", "setvec", "setparam", "setplot", "setquery", "setscaletype", "settracecolor", "settracestyle", "setsource", "settrigger", "setvec", "setxlimits", "setylimits", "show", "showmod", "sort", "status", "step", "stop", "switch", "tf", "timetofreq", "timetowave", "tran", "unalias", "unlet", "unset", "unalterparam", "update", "version", "view", "wavefilter", "wavetotime", "where", "while", "write"),
        "Instruction1": ("abs", "askvalue", "atan", "average", "ceil", "cos", "db", "differentiate", "differentiatex", "exp", "finalvalue", "floor", "getcursorx", "getcursory", "getcursory0", "getcursory1", "getparam", "im", "ln", "initialvalue", "integrate", "integratex", "interpolate", "isdef", "isdisplayed", "j", "log", "length", "mag,", "max", "maxscale", "mean", "meanpts", "min", "minscale", "nextplot", "nextvector", "norm", "operatingpoint", "ph", "phase", "phaseextend", "pk_pk", "pos", "pulse", "re", "rms", "rmspts", "rnd", "sameplot", "sin", "sqrt", "stddev", "stddevpts", "tan", "tfall", "tolerance", "trise", "unitvec", "vector"),
        "Type": ("param", "nodeset", "include", "options", "dcconv", "subckt", "ends", "model"),
    }
    operator_list = [
        "=", "+", "-", "/", "<", ">", "@", "$", ".",
        "~", "&", "%", "|", "!", "?", "^", ".", ":", "\"",
    ]
    splitter = re.compile(r"(\{\.|\.\}|\#|\'|\"\"\"|\n|\s+|\w+|\W)")
    # Characters that autoindent one level on pressing Return/Enter
    autoindent_characters = []
    # String start/end tokens
    tokens_string = ("\"", )
    # Comment tokens
    tokens_comment = []

    def __init__(self, parent=None):
        """
        Overridden initialization
        """
        # Initialize superclass
        super().__init__()
        print("INIT")
        # Set the default style values
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
        # Reset autoindentation style
        self.setAutoIndentStyle(0)
        # Set the theme
        self.set_theme(data.theme)
    
    def language(self):
        return "Spice"
    
    def description(self, style):
        if style < len(self.styles):
            description = "Custom lexer for the Spice circuit languages"
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
        setStyling         = self.setStyling
        operator_list      = self.operator_list
        keyword_dictionary = self.keyword_dictionary
        DEFAULT            = self.styles["Default"]
        COMMENT            = self.styles["Comment"]
        INSTRUCTION0       = self.styles["Instruction0"]
        INSTRUCTION1       = self.styles["Instruction1"]
        TYPE               = self.styles["Type"]
        STRING             = self.styles["String"]
        NUMBER             = self.styles["Number"]
        OPERATOR           = self.styles["Operator"]
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
                if (token[0] == "\"" and (tokens[i-1][0] != "\\") or "\n" in token[0]):
                    stringing = False
            elif token[0] in self.tokens_comment:
                setStyling(token[1], COMMENT)
                commenting = True
            elif token[0] in self.tokens_string:
                # Start of a string
                setStyling(token[1], STRING)
                stringing = True
            elif token[0] in operator_list:
                print("TU0")
                setStyling(token[1], OPERATOR)
            elif token[0] in keyword_dictionary["Instruction0"]:
                print("TU1")
                setStyling(token[1], INSTRUCTION0)
            elif token[0] in keyword_dictionary["Instruction1"]:
                print("TU2")
                setStyling(token[1], INSTRUCTION1)
            elif token[0] in keyword_dictionary["Type"]:
                print("TU3")
                setStyling(token[1], TYPE)
            else:
                setStyling(token[1], DEFAULT)
