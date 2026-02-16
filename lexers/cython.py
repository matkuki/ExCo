"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

from __future__ import annotations

from typing import Any

import builtins
import keyword
import re
import time

import data
import qt
import settings

import functions
import lexers
from lexers.python import Python


class Cython(Python):
    """Cython - basically Python with added keywords"""

    # Class variables
    _kwrds: Any = None
    styles: dict[str, int] = {
        "Default": 0,
        "Comment": 1,
        "Number": 2,
        "DoubleQuotedString": 3,
        "SingleQuotedString": 4,
        "Keyword": 5,
        "TripleSingleQuotedString": 6,
        "TripleDoubleQuotedString": 7,
        "ClassName": 8,
        "FunctionMethodName": 9,
        "Operator": 10,
        "Identifier": 11,
        "CommentBlock": 12,
        "UnclosedString": 13,
        "HighlightedIdentifier": 14,
        "Decorator": 15,
    }
    _c_kwrds = [
        "void",
        "char",
        "int",
        "long",
        "short",
        "double",
        "float",
        "const",
        "unsigned",
        "inline",
    ]
    _cython_kwrds = [
        "by",
        "cdef",
        "cimport",
        "cpdef",
        "ctypedef",
        "enum",
        "except?",
        "extern",
        "gil",
        "include",
        "nogil",
        "property",
        "public",
        "readonly",
        "struct",
        "union",
        "DEF",
        "IF",
        "ELIF",
        "ELSE",
    ]

    def __init__(self, parent: Any = None) -> None:
        """Overridden initialization"""
        # Initialize superclass
        super().__init__()
        # Set default colors
        self.setDefaultColor(
            qt.QColor(settings.get_theme()["fonts"]["default"]["color"])
        )
        self.setDefaultPaper(
            qt.QColor(settings.get_theme()["fonts"]["default"]["background"])
        )
        self.setDefaultFont(
            qt.QFont(
                settings.get("current_font_name"), settings.get("current_font_size")
            )
        )
        # Initialize the keyword list
        self.init_kwrds()
        # Set the theme
        self.set_theme(settings.get_theme())

    def set_theme(self, theme: dict[str, Any]) -> None:
        for style in self.styles:
            # Papers
            self.setPaper(
                qt.QColor(settings.get_theme()["fonts"][style.lower()]["background"]),
                self.styles[style],
            )
            # Fonts
            lexers.set_font(self, style, theme["fonts"][style.lower()])

    def keywords(self, state):
        """
        Overridden method for determining keywords,
        read the QScintilla QsciLexer class documentation on the Riverbank website.
        """
        keywrds = None
        # Only state 1 returns keywords, don't know why? Check the C++ Scintilla lexer source files.
        if state == 1:
            keywrds = self._kwrds
        return keywrds
