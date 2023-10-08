# -*- coding: utf-8 -*-

"""
Copyright (c) 2018 Matic Kukovec. 
"""

import keyword
import builtins
import re
import functions
import qt
import data
import time
import lexers


class Php(qt.QsciLexerCustom):
    """Lexer for styling Php documents"""
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
        for style in self.styles:
            # Papers
            self.setPaper(
                qt.QColor(data.theme["fonts"][style.lower()]["background"]), 
                self.styles[style]
            )
            # Fonts
            lexers.set_font(self, style, theme["fonts"][style.lower()])
    
    def language(self):
        return "Php"
    
    def description(self, style):
        if style == 0:
            description = "Php"
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


