"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

from __future__ import annotations

import qt
import data
import settings
import functions
import lexers
from typing import Any


class BaseLexer(qt.QsciLexerCustom):
    """
    Lexer for styling normal text documents
    """

    # Constants
    name: str = "Unknown"

    # Class variables
    styles: dict[str, int] = {"default": 0}

    def __init__(self, parent: Any = None) -> None:
        """
        Overridden initialization
        """
        # Initialize superclass
        super().__init__(parent)
        # Set the default style values
        self.setDefaultColor(
            qt.QColor(settings.get_theme()["fonts"]["default"]["color"])
        )
        self.setDefaultPaper(
            qt.QColor(settings.get_theme()["fonts"]["default"]["background"])
        )
        self.setDefaultFont(settings.get_editor_font())
        # Set the font colors
        self.setFont(settings.get_current_font(), 0)
        # Reset autoindentation style
        self.setAutoIndentStyle(0)
        # Set the theme
        self.set_theme()

    def set_font(self, style_name: str, style_options: dict[str, Any]) -> None:
        style_index = self.styles[style_name]
        self.setColor(qt.QColor(style_options["color"]), style_index)
        weight = qt.QFont.Weight.Normal
        if style_options["bold"]:
            weight = qt.QFont.Weight.Bold
        self.setFont(
            qt.QFont(
                settings.get("current_editor_font_name"),
                settings.get("current_editor_font_size"),
                weight=weight,
            ),
            style_index,
        )

    def set_theme(self, *args: Any, **kwargs: Any) -> None:
        for style in self.styles:
            # Papers
            self.setPaper(
                qt.QColor(settings.get_theme()["fonts"][style]["background"]),
                self.styles[style],
            )
            # Fonts
            self.set_font(style, settings.get_theme()["fonts"][style])

    def language(self) -> str:
        return self.name

    def description(self, style: int) -> str:
        if style <= len(self.styles.keys()):
            description = self.name
        else:
            description = ""
        return description

    def defaultStyle(self) -> int:
        return self.styles["default"]

    def braceStyle(self) -> int:
        return self.styles["default"]

    def defaultFont(self, style: int | None = None) -> qt.QFont:
        return qt.QFont(
            settings.get("current_font_name"), settings.get("current_font_size")
        )

    def styleText(self, start: int, end: int) -> None:
        raise Exception("[BaseLexer] Styling function needs to be overriden!")
