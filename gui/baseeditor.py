
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2021 Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import os
import sys
import itertools
import inspect
import functools
import keyword
import re
import collections
import textwrap
import importlib
import data
import components
import themes
import functions
import interpreter
import settings
import lexers
import traceback
import gc

from .contextmenu import *
from .stylesheets import *

"""
-----------------------------
Subclassed QScintilla widget used for displaying REPL messages, Python/C node trees, ...
-----------------------------
""" 
class BaseEditor(data.QsciScintilla):
    
    def set_theme(self, theme):
        if theme == themes.Air:
            self.resetFoldMarginColors()
        else:
            self.setFoldMarginColors(
                theme.FoldMargin.ForeGround, 
                theme.FoldMargin.BackGround
            )
        self.setMarginsForegroundColor(theme.LineMargin.ForeGround)
        self.setMarginsBackgroundColor(theme.LineMargin.BackGround)
        if self.lexer() is not None and hasattr(self.lexer(), "get_default_background_color"):
            self.SendScintilla(
                data.QsciScintillaBase.SCI_STYLESETBACK, 
                data.QsciScintillaBase.STYLE_DEFAULT, 
                self.lexer().get_default_background_color()
            )
        else:
            self.SendScintilla(
                data.QsciScintillaBase.SCI_STYLESETBACK, 
                data.QsciScintillaBase.STYLE_DEFAULT, 
                theme.Paper.Default
            )
        self.SendScintilla(
            data.QsciScintillaBase.SCI_STYLESETBACK, 
            data.QsciScintillaBase.STYLE_LINENUMBER, 
            theme.LineMargin.BackGround
        )
        self.SendScintilla(
            data.QsciScintillaBase.SCI_SETCARETFORE, 
            theme.Cursor
        )
        self.setCaretLineBackgroundColor(
            theme.Cursor_Line_Background
        )
        self.setStyleSheet("""
            BaseEditor {{
                border: 0px;
                background-color: {};
                padding: 0px;
                spacing: 0px;
                margin: 0px;
            }}
            {}
        """.format(
            data.theme.Indication.PassiveBackGround,
            StyleSheetScrollbar.full(),
        ))