# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2023 Matic Kukovec.
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
QPushButton[focused=true] {{
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

class StyleSheetMenu:
    @staticmethod
    def standard():
        style_sheet = """
QMenu {{
    background-color: {};
    border: 1px solid {};
    color: {};
    menu-scrollable: 1;
}}
QMenu::item {{
    background-color: transparent;
    border: none;
    padding-top: 2px;
    padding-bottom: 2px;
    padding-right: 20px;
    spacing: 12px;
    margin: 1px;
}}
QMenu::item:selected  {{
    background-color: {};
}}
QMenu::right-arrow  {{
    image: url({});
    width: 14px;
    height: 14px;
}}
QMenu::right-arrow:disabled  {{
    image: url({});
    width: 14px;
    height: 14px;
}}
        """.format(
            data.theme["indication"]["passivebackground"],
            data.theme["indication"]["passiveborder"],
            data.theme["fonts"]["default"]["color"],
            data.theme["indication"]["hover"],
            functions.get_resource_file(data.theme["right-arrow-menu-image"]),
            functions.get_resource_file(data.theme["right-arrow-menu-disabled-image"]),
        )
        return style_sheet

class StyleSheetMenuBar:
    @staticmethod
    def standard():
        style_sheet = """
QMenuBar {{
    background-color: {};
    color: {};
}}
QMenuBar::item {{
    background-color: transparent;
}}
QMenuBar::item:selected {{
    background-color: {};
}}
        """.format(
                data.theme["indication"]["passivebackground"],
                data.theme["fonts"]["default"]["color"],
                data.theme["indication"]["hover"],
        )
        return style_sheet

class StyleSheetTooltip:
    @staticmethod
    def standard():
        style_sheet = f"""
QToolTip {{
    font-family: {data.current_font_name};
    font-size: {data.current_font_size};
    background-color: {data.theme["indication"]["passivebackground"]}; 
    color: {data.theme["indication"]["font"]}; 
    border: {data.theme["indication"]["passiveborder"]} solid 1px;
}}
        """
        return style_sheet

class StyleSheetFrame:
    @staticmethod
    def standard(background_transparent=False,
                 no_border=True):
        background_color = data.theme["fonts"]["default"]["background"]
        if background_transparent:
            background_color = "transparent"
        border = f'1px solid {data.theme["indication"]["passiveborder"]}'
        if no_border:
            border = "none"
        style_sheet = (f"""
QFrame {{
    background-color: {background_color};
    border: {border};
}}
        """)
        return style_sheet

class StyleSheetTable:
    @staticmethod
    def standard():
        border_width = 1
        padding = 0
        spacing = 0
        return f"""
QTableView {{
    background-color: {data.theme["fonts"]["default"]["background"]};
    color: {data.theme["fonts"]["default"]["color"]};
    selection-background-color: {data.theme["indication"]["activebackground"]};
    selection-color: {data.theme["fonts"]["default"]["color"]};
    border: {border_width}px solid {data.theme["indication"]["passiveborder"]};
    gridline-color: {data.theme["indication"]["passiveborder"]};
    padding: {padding}px;
    spacing: {padding}px;
    font-family: {data.current_editor_font_name};
    font-size: {data.current_editor_font_size}pt;
}}
QTableView QTableCornerButton::section {{
    background: {data.theme["fonts"]["default"]["background"]};
    border: none;
}}

/*
QTableView::item {{
    border: {border_width}px solid {data.theme["indication"]["passiveborder"]};
}}
*/
QTableView::item::selected {{
    background-color: {data.theme["indication"]["activebackground"]};
}}

QHeaderView {{
    background-color: {data.theme["table-header"]};
    color: {data.theme["fonts"]["default"]["color"]};
}}
QHeaderView::section {{
    border-style: none;
    border-right: 1px solid {data.theme["indication"]["passiveborder"]};
    border-bottom: 1px solid {data.theme["indication"]["passiveborder"]};
    background-color: {data.theme["table-header"]};
    color: {data.theme["fonts"]["default"]["color"]};
    font-family: {data.current_editor_font_name};
    font-size: {data.current_editor_font_size}pt;
}}
        """