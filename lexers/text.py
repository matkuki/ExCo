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
import qt
import data
import functions
import time
import lexers


class Text(qt.QsciLexerCustom):
    """Lexer for styling normal text documents"""
    # Class variables
    styles = {
        "Default" : 0
    }
    
    def __init__(self, parent=None):
        """Overridden initialization"""
        #Initialize superclass
        super().__init__()
        #Set the font colors
        self.setFont(data.get_current_font(), 0)
        #Reset autoindentation style
        self.setAutoIndentStyle(0)
        #Set the theme
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        # Papers
        self.setPaper(
            qt.QColor(data.theme["fonts"]["default"]["background"]), 
            self.styles["Default"]
        )
        # Fonts
        lexers.set_font(self, "Default", theme["fonts"]["default"])
    
    def language(self):
        return "Plain text"
    
    def description(self, style):
        if style == 0:
            description = "Text"
        else:
            description = ""
        return description
    
    def defaultStyle(self):
        return self.styles["Default"]
    
    def braceStyle(self):
        return self.styles["Default"]
    
    def defaultFont(self, style):
        return qt.QFont(data.current_font_name, data.current_font_size)
    
    def styleText(self, start, end):
        self.startStyling(start)
        self.setStyling(end - start, 0)


