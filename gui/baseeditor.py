# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2023 Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""


import data

from .stylesheets import *

"""
-----------------------------
Subclassed QScintilla widget used for displaying REPL messages, Python/C node trees, ...
-----------------------------
"""
class BaseEditor(data.QsciScintilla):

    def set_theme(self, theme):
        if theme["name"] == "Air":
            self.resetFoldMarginColors()
        else:
            self.setFoldMarginColors(
                data.QColor(theme["foldmargin"]["foreground"]),
                data.QColor(theme["foldmargin"]["background"])
            )
        self.setMarginsForegroundColor(data.QColor(theme["linemargin"]["foreground"]))
        self.setMarginsBackgroundColor(data.QColor(theme["linemargin"]["background"]))
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
                data.QColor(theme["fonts"]["default"]["background"])
            )
        self.SendScintilla(
            data.QsciScintillaBase.SCI_STYLESETBACK,
            data.QsciScintillaBase.STYLE_LINENUMBER,
            data.QColor(theme["linemargin"]["background"])
        )
        self.SendScintilla(
            data.QsciScintillaBase.SCI_SETCARETFORE,
            data.QColor(theme["cursor"])
        )
        self.setCaretLineBackgroundColor(
            data.QColor(theme["cursor-line-background"])
        )
        self.setStyleSheet("""
BaseEditor {{
    border: 0px;
    background-color: {};
    padding: 0px;
    spacing: 0px;
    margin: 0px;
}}
QListView {{
    background-color: {};
    color: {};
}}
QListView::item:selected {{
    background-color: {};
    color: {};
}}
QListView::item:selected {{
    background-color: {};
    color: {};
}}
{}
        """.format(
            theme["indication"]["passivebackground"],
            theme["indication"]["passivebackground"],
            theme["fonts"]["default"]["color"],
            theme["indication"]["passivebackground"],
            theme["fonts"]["default"]["color"],
            theme["indication"]["activebackground"],
            theme["fonts"]["default"]["color"],
            StyleSheetScrollbar.full(),
        ))

    def delete_context_menu(self):
        # Clean up the context menu
        if self.context_menu is not None:
            self.context_menu.hide()
            self.context_menu.clear_items()
            self.context_menu.deleteLater()
            self.context_menu.setParent(None)
        self.context_menu = None
