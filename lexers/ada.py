"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import builtins
import keyword
import re
import time

import data
import qt

import functions
import lexers


class Ada(qt.QsciLexerCustom):
    """Custom lexer for the Ada programming languages"""

    styles = {
        "Default": 0,
        "Comment": 1,
        "Keyword": 2,
        "String": 3,
        "Procedure": 4,
        "Number": 5,
        "Type": 6,
        "Package": 7,
    }

    # Class variables
    keyword_list = [
        "abort",
        "else",
        "new",
        "return",
        "abs",
        "elsif",
        "not",
        "reverse",
        "abstract",
        "end",
        "null",
        "accept",
        "entry",
        "select",
        "access",
        "exception",
        "of",
        "separate",
        "aliased",
        "exit",
        "or",
        "some",
        "all",
        "others",
        "subtype",
        "and",
        "for",
        "out",
        "synchronized",
        "array",
        "function",
        "overriding",
        "at",
        "tagged",
        "generic",
        "package",
        "task",
        "begin",
        "goto",
        "pragma",
        "terminate",
        "body",
        "private",
        "then",
        "if",
        "procedure",
        "type",
        "case",
        "in",
        "protected",
        "constant",
        "interface",
        "until",
        "is",
        "raise",
        "use",
        "declare",
        "range",
        "delay",
        "limited",
        "record",
        "when",
        "delta",
        "loop",
        "rem",
        "while",
        "digits",
        "renames",
        "with",
        "do",
        "mod",
        "requeue",
        "xor",
    ]
    splitter = re.compile(r"(\-\-|\s+|\w+|\W)")

    def __init__(self, parent=None):
        """Overridden initialization"""
        # Initialize superclass
        super().__init__()
        # Set the default style values
        self.setDefaultColor(qt.QColor(settings.get_theme()["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(settings.get_theme()["fonts"]["default"]["background"]))
        self.setDefaultFont(settings.get_editor_font())
        # Reset autoindentation style
        self.setAutoIndentStyle(0)
        # Set the theme
        self.set_theme(settings.get_theme())

    def language(self):
        return "Ada"

    def description(self, style):
        if style <= 7:
            description = "Custom lexer for the Ada programming languages"
        else:
            description = ""
        return description

    def set_theme(self, theme):
        for style in self.styles:
            # Papers
            self.setPaper(
                qt.QColor(settings.get_theme()["fonts"][style.lower()]["background"]),
                self.styles[style],
            )
            # Fonts
            lexers.set_font(self, style, theme["fonts"][style.lower()])

    def styleText(self, start, end):
        """
        Overloaded method for styling text.
        NOTE:
            Very slow if done in Python!
            Using the Cython version is better.
            The fastest would probably be adding the lexer directly into
            the QScintilla source. Maybe never :-)
        """
        # Get the global cython flag
        if lexers.cython_lexers_found == True:
            # Cython module found
            lexers.cython_lexers.style_ada(start, end, self, self.editor())
        else:
            # Style in pure Python, VERY SLOW!
            editor = self.editor()
            if editor is None:
                return
            # Initialize the procedure/package counter
            pp_counter = []
            # Initialize the styling
            self.startStyling(0)
            # Scintilla works with bytes, so we have to adjust the start and end boundaries
            text = bytearray(editor.text().lower(), "utf-8").decode("utf-8")
            # Loop optimizations
            setStyling = self.setStyling
            kw_list = self.keyword_list
            DEF = self.styles["Default"]
            KWD = self.styles["Keyword"]
            COM = self.styles["Comment"]
            STR = self.styles["String"]
            PRO = self.styles["Procedure"]
            NUM = self.styles["Number"]
            PAC = self.styles["Package"]
            #            TYP = self.styles["Type"]
            # Initialize comment state and split the text into tokens
            commenting = False
            stringing = False
            tokens = [
                (token, len(bytearray(token, "utf-8")))
                for token in self.splitter.findall(text)
            ]
            # Style the tokens accordingly
            for i, token in enumerate(tokens):
                if commenting == True:
                    # Continuation of comment
                    setStyling(token[1], COM)
                    # Check if comment ends
                    if "\n" in token[0]:
                        commenting = False
                elif stringing == True:
                    # Continuation of a string
                    setStyling(token[1], STR)
                    # Check if string ends
                    if token[0] == '"' or "\n" in token[0]:
                        stringing = False
                elif token[0] == '"':
                    # Start of a string
                    setStyling(token[1], STR)
                    stringing = True
                elif token[0] in kw_list:
                    # Keyword
                    setStyling(token[1], KWD)
                elif token[0] == "--":
                    # Start of a comment
                    setStyling(token[1], COM)
                    commenting = True
                elif i > 1 and tokens[i - 2][0] == "procedure":
                    # Procedure name
                    setStyling(token[1], PRO)
                    # Mark the procedure
                    if tokens[i + 1][0] != ";":
                        pp_counter.append("PROCEDURE")
                elif i > 1 and (
                    tokens[i - 2][0] == "package" or tokens[i - 2][0] == "body"
                ):
                    # Package name
                    setStyling(token[1], PAC)
                    # Mark the package
                    pp_counter.append("PACKAGE")
                elif (i > 1 and tokens[i - 2][0] == "end") and (
                    len(tokens) - 1 >= i + 1
                ):
                    # Package or procedure name end
                    if len(pp_counter) > 0:
                        if pp_counter.pop() == "PACKAGE":
                            setStyling(token[1], PAC)
                        else:
                            setStyling(token[1], PRO)
                    else:
                        setStyling(token[1], DEF)
                elif functions.is_number(token[0]):
                    # Number
                    setStyling(token[1], NUM)
                else:
                    setStyling(token[1], DEF)
