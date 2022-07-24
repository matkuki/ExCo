
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2021 Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import os
import sys
import data
import functions


class StyleSheetScrollbar:
    @staticmethod
    def horizontal():
        width = 10
        height = 10
        color_background = data.theme["scrollbar"]["background"]
        color_handle = data.theme["scrollbar"]["handle"]
        color_handle_hover = data.theme["scrollbar"]["handle-hover"]
        style_sheet = """
            QScrollBar:horizontal {{
                border: none;
                background: {};
                height: {}px;
                margin: 0px 0px 0px 0px;
            }}
            QScrollBar::handle:horizontal {{
                background: {};
                min-width: 20px;
            }}
            QScrollBar::handle:hover {{
                background: {};
            }}
            QScrollBar::handle:horizontal:pressed {{
                background: {};
            }}
            
            QScrollBar::sub-line:horizontal, QScrollBar::add-line:horizontal,
            QScrollBar::left-arrow:horizontal, QScrollBar::right-arrow:horizontal,
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
                background: none;
                width: 0px;
                height: 0px;
            }}
        """.format(
            color_background,
            height,
            color_handle,
            color_handle_hover,
            color_handle_hover,
        )
        return style_sheet
    
    @staticmethod
    def vertical():
        width = 10
        height = 10
        color_background = data.theme["scrollbar"]["background"]
        color_handle = data.theme["scrollbar"]["handle"]
        color_handle_hover = data.theme["scrollbar"]["handle-hover"]
        style_sheet = """
            QScrollBar:vertical {{
                border: none;
                background: {};
                width: {}px;
                margin: 0px 0px 0px 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {};
                min-height: 20px;
            }}
            QScrollBar::handle:hover {{
                background: {};
            }}
            QScrollBar::handle:vertical:pressed {{
                background: {};
            }}
            
            QScrollBar::sub-line:vertical, QScrollBar::add-line:vertical,
            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical,
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
                width: 0px;
                height: 0px;
            }}
        """.format(
            color_background,
            width,
            color_handle,
            color_handle_hover,
            color_handle_hover,
            
        )
        return style_sheet
    
    @staticmethod
    def full():
        style_sheet = (
            StyleSheetScrollbar.horizontal() +
            StyleSheetScrollbar.vertical()
        )
        return style_sheet

class StyleSheetButton:
    @staticmethod
    def standard():
        style_sheet = f"""
            QPushButton {{
                background-color: {data.theme["indication"]["passivebackground"]};
                color: {data.theme["indication"]["font"]};
                border: 1px solid {data.theme["indication"]["passiveborder"]};
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {data.theme["indication"]["hover"]};
                color: {data.theme["indication"]["font"]};
                border: 1px solid {data.theme["indication"]["activeborder"]};
            }}
            QPushButton:pressed {{
                background-color: {data.theme["indication"]["activebackground"]};
                color: {data.theme["indication"]["font"]};
                border: 1px solid {data.theme["indication"]["activeborder"]};
            }}
        """
        return style_sheet