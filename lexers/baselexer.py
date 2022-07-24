
# -*- coding: utf-8 -*-

"""
Copyright (c) 2022 Matic Kukovec. 
"""

import data
import functions
import lexers


class BaseLexer(data.QsciLexerCustom):
    """
    Lexer for styling normal text documents
    """
    # Constants
    name = "Unknown"
    
    # Class variables
    styles = {
        "default" : 0
    }
    
    def __init__(self, parent=None):
        """
        Overridden initialization
        """
        # Initialize superclass
        super().__init__(parent)
        # Set the default style values
        self.setDefaultColor(data.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(data.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
        # Set the font colors
        self.setFont(data.get_current_font(), 0)
        # Reset autoindentation style
        self.setAutoIndentStyle(0)
        # Set the theme
        self.set_theme()
    
    def set_font(self, style_name, style_options):
        style_index = self.styles[style_name]
        self.setColor(
            data.QColor(style_options["color"]),
            style_index
        )
        weight = data.QFont.Normal
        if style_options["bold"]:
            weight = data.QFont.Bold
    #    elif bold == 2:
    #        weight = data.QFont.Black
        self.setFont(
            data.QFont(
                data.current_editor_font_name,
                data.current_editor_font_size,
                weight=weight
            ),
            style_index
        )
    
    def set_theme(self, *args, **kwargs):
        for style in self.styles:
            # Papers
            self.setPaper(
                data.QColor(data.theme["fonts"][style]["background"]), 
                self.styles[style]
            )
            # Fonts
            self.set_font(style, data.theme["fonts"][style])
    
    def language(self):
        return self.name
    
    def description(self, style):
        if style <= len(self.styles.keys()):
            description = self.name
        else:
            description = ""
        return description
    
    def defaultStyle(self):
        return self.styles["default"]
    
    def braceStyle(self):
        return self.styles["default"]
    
    def defaultFont(self, style):
        return data.QFont(data.current_font_name, data.current_font_size)
    
    def styleText(self, start, end):
        raise Exception("[BaseLexer] Styling function needs to be overriden!")
