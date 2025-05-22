"""
Copyright (c) 2013-present Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import qt
import data
import functions
import lexers


class BaseLexer(qt.QsciLexerCustom):
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
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
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
            qt.QColor(style_options["color"]),
            style_index
        )
        weight = qt.QFont.Weight.Normal
        if style_options["bold"]:
            weight = qt.QFont.Weight.Bold
        self.setFont(
            qt.QFont(
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
                qt.QColor(data.theme["fonts"][style]["background"]), 
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
        return qt.QFont(data.current_font_name, data.current_font_size)
    
    def styleText(self, start, end):
        raise Exception("[BaseLexer] Styling function needs to be overriden!")
