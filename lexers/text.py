"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

from __future__ import annotations

from typing import Any

import keyword
import builtins
import re
import qt
import data
import settings
import functions
import time
import lexers


class Text(qt.QsciLexerCustom):
    """Lexer for styling normal text documents"""

    # Class variables
    styles: dict[str, int] = {"Default": 0}

    def __init__(self, parent: Any = None) -> None:
        """Overridden initialization"""
        # Initialize superclass
        super().__init__()
        # Set the font colors
        self.setFont(settings.get_current_font(), 0)
        # Reset autoindentation style
        self.setAutoIndentStyle(0)
        # Set the theme
        self.set_theme(settings.get_theme())

    def set_theme(self, theme: dict[str, Any]) -> None:
        # Papers
        self.setPaper(
            qt.QColor(settings.get_theme()["fonts"]["default"]["background"]),
            self.styles["Default"],
        )
        # Fonts
        lexers.set_font(self, "Default", theme["fonts"]["default"])

    def language(self) -> str:
        return "Plain text"

    def description(self, style: int) -> str:
        if style == 0:
            description = "Text"
        else:
            description = ""
        return description

    def defaultStyle(self) -> int:
        return self.styles["Default"]

    def braceStyle(self) -> int:
        return self.styles["Default"]

    def defaultFont(self, style: int | None = None) -> qt.QFont:
        return qt.QFont(
            settings.get("current_font_name"), settings.get("current_font_size")
        )

    def styleText(self, start: int, end: int) -> None:
        self.startStyling(start)
        self.setStyling(end - start, 0)
