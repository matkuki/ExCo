"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import os
import sys
import data
import settings
import functions


class StyleSheetStatusbar:
    @staticmethod
    def standard():
        style_sheet = """
QStatusBar {{
    background-color: {};
    color: {};
    font-family: {};
    font-size: {}pt;
}}
QStatusBar::item {{
    border: none;
}}
QLabel {{
    background-color: transparent;
    color: {};
    font-family: {};
    font-size: {}pt;
}}
        """.format(
            settings.get_theme()["form"],
            settings.get_theme()["indication"]["font"],
            settings.get("current_font_name"),
            settings.get("current_font_size"),
            settings.get_theme()["indication"]["font"],
            settings.get("current_font_name"),
            settings.get("current_font_size"),
        )
        return style_sheet


class StyleSheetScrollbar:
    @staticmethod
    def horizontal():
        width = 10
        height = 10
        color_background = settings.get_theme()["scrollbar"]["background"]
        color_handle = settings.get_theme()["scrollbar"]["handle"]
        color_handle_hover = settings.get_theme()["scrollbar"]["handle-hover"]
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
        color_background = settings.get_theme()["scrollbar"]["background"]
        color_handle = settings.get_theme()["scrollbar"]["handle"]
        color_handle_hover = settings.get_theme()["scrollbar"]["handle-hover"]
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
        style_sheet = StyleSheetScrollbar.horizontal() + StyleSheetScrollbar.vertical()
        return style_sheet


class StyleSheetButton:
    @staticmethod
    def standard():
        style_sheet = f"""
QPushButton {{
    background-color: {settings.get_theme()["indication"]["passivebackground"]};
    color: {settings.get_theme()["indication"]["font"]};
    border: 1px solid {settings.get_theme()["indication"]["passiveborder"]};
    border-radius: 4px;
}}
QPushButton:hover {{
    background-color: {settings.get_theme()["indication"]["hover"]};
    color: {settings.get_theme()["indication"]["font"]};
    border: 1px solid {settings.get_theme()["indication"]["activeborder"]};
}}
QPushButton[focused=true] {{
    background-color: {settings.get_theme()["indication"]["hover"]};
    color: {settings.get_theme()["indication"]["font"]};
    border: 1px solid {settings.get_theme()["indication"]["activeborder"]};
}}
QPushButton:pressed {{
    background-color: {settings.get_theme()["indication"]["activebackground"]};
    color: {settings.get_theme()["indication"]["font"]};
    border: 1px solid {settings.get_theme()["indication"]["activeborder"]};
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
            settings.get_theme()["indication"]["passivebackground"],
            settings.get_theme()["indication"]["passiveborder"],
            settings.get_theme()["fonts"]["default"]["color"],
            settings.get_theme()["indication"]["hover"],
            functions.get_resource_file(settings.get_theme()["right-arrow-menu-image"]),
            functions.get_resource_file(settings.get_theme()["right-arrow-menu-disabled-image"]),
        )
        return style_sheet


class StyleSheetMenuBar:
    @staticmethod
    def standard():
        style_sheet = """
QMenuBar {{
    background-color: {};
    color: {};
    spacing: 4px;
}}
QMenuBar::item {{
    background-color: transparent;
    padding-top: 2px;
    padding-bottom: 2px;
    padding-left: 4px;
    padding-right: 4px;
}}
QMenuBar::item:selected {{
    background-color: {};
}}
        """.format(
            settings.get_theme()["indication"]["passivebackground"],
            settings.get_theme()["fonts"]["default"]["color"],
            settings.get_theme()["indication"]["hover"],
        )
        return style_sheet


class StyleSheetTooltip:
    @staticmethod
    def standard():
        style_sheet = f"""
QToolTip {{
    font-family: {settings.get("current_font_name")};
    font-size: {settings.get("current_font_size")};
    background-color: {settings.get_theme()["indication"]["passivebackground"]}; 
    color: {settings.get_theme()["indication"]["font"]}; 
    border: {settings.get_theme()["indication"]["passiveborder"]} solid 1px;
}}
        """
        return style_sheet


class StyleSheetFrame:
    @staticmethod
    def standard(background_transparent=False, no_border=True):
        background_color = settings.get_theme()["fonts"]["default"]["background"]
        if background_transparent:
            background_color = "transparent"
        border = f'1px solid {settings.get_theme()["indication"]["passiveborder"]}'
        if no_border:
            border = "none"
        style_sheet = f"""
QFrame {{
    background-color: {background_color};
    border: {border};
    spacing: 0px;
}}
        """
        return style_sheet


class StyleSheetTable:
    @staticmethod
    def standard():
        border_width = 1
        padding = 0
        spacing = 0
        return f"""
QTableView {{
    background-color: {settings.get_theme()["fonts"]["default"]["background"]};
    color: {settings.get_theme()["fonts"]["default"]["color"]};
    selection-background-color: {settings.get_theme()["indication"]["activebackground"]};
    selection-color: {settings.get_theme()["fonts"]["default"]["color"]};
    border: {border_width}px solid {settings.get_theme()["indication"]["passiveborder"]};
    gridline-color: {settings.get_theme()["indication"]["passiveborder"]};
    padding: {padding}px;
    spacing: {padding}px;
    font-family: {settings.get("current_editor_font_name")};
    font-size: {settings.get("current_editor_font_size")}pt;
}}
QTableView QTableCornerButton::section {{
    background: {settings.get_theme()["fonts"]["default"]["background"]};
    border: none;
}}

/*
QTableView::item {{
    border: {border_width}px solid {settings.get_theme()["indication"]["passiveborder"]};
}}
*/
QTableView::item::selected {{
    background-color: {settings.get_theme()["indication"]["activebackground"]};
}}

QHeaderView {{
    background-color: {settings.get_theme()["table-header"]};
    color: {settings.get_theme()["fonts"]["default"]["color"]};
}}
QHeaderView::section {{
    border-style: none;
    border-right: 1px solid {settings.get_theme()["indication"]["passiveborder"]};
    border-bottom: 1px solid {settings.get_theme()["indication"]["passiveborder"]};
    background-color: {settings.get_theme()["table-header"]};
    color: {settings.get_theme()["fonts"]["default"]["color"]};
    font-family: {settings.get("current_editor_font_name")};
    font-size: {settings.get("current_editor_font_size")}pt;
}}
        """


class StyleSheetTabWidget:
    @staticmethod
    def standard():
        style_sheet = """
TabWidget::pane {{
    border: 2px solid {};
    background-color: {};
    margin: 0px;
    spacing: 0px;
    padding: 0px;
}}
TabWidget[indicated=false]::pane {{
    border: 2px solid {};
    background-color: {};
}}
TabWidget[indicated=true]::pane {{
    border: 2px solid {};
    background-color: {};
}}
TabWidget QToolButton {{
    background: {};
    border: 1px solid {};
    margin-top: 0px;
    margin-bottom: 0px;
    margin-left: 0px;
    margin-right: 1px;
}}
TabWidget QToolButton:hover {{
    background: {};
    border: 1px solid {};
}}
        """.format(
            settings.get_theme()["indication"]["passiveborder"],
            settings.get_theme()["indication"]["passivebackground"],
            settings.get_theme()["indication"]["passiveborder"],
            settings.get_theme()["indication"]["passivebackground"],
            settings.get_theme()["indication"]["activeborder"],
            settings.get_theme()["indication"]["activebackground"],
            settings.get_theme()["indication"]["passivebackground"],
            settings.get_theme()["indication"]["passiveborder"],
            settings.get_theme()["indication"]["activebackground"],
            settings.get_theme()["indication"]["activeborder"],
        )
        return style_sheet


class StyleSheetTreeWidget:
    @staticmethod
    def standard():
        if settings.get_theme()["name"] != "Air":
            shrink_icon = os.path.join(
                data.resources_directory, "feather/air-light-grey/chevron-down.svg"
            ).replace("\\", "/")
            expand_icon = os.path.join(
                data.resources_directory, "feather/air-light-grey/chevron-right.svg"
            ).replace("\\", "/")
        else:
            shrink_icon = os.path.join(
                data.resources_directory, "feather/air-grey/chevron-down.svg"
            ).replace("\\", "/")
            expand_icon = os.path.join(
                data.resources_directory, "feather/air-grey/chevron-right.svg"
            ).replace("\\", "/")
        style_sheet = f"""
QTreeView {{
    color: {settings.get_theme()["fonts"]["default"]["color"]};
    background-color: {settings.get_theme()["fonts"]["default"]["background"]};
}}
QTreeView::branch {{
    background-color: {settings.get_theme()["fonts"]["default"]["background"]};
}}
QTreeView::branch:closed:has-children:!has-siblings,
QTreeView::branch:closed:has-children:has-siblings {{
    border-image: none;
    image: url({expand_icon});
}}
QTreeView::branch:open:has-children:!has-siblings,
QTreeView::branch:open:has-children:has-siblings {{
    border-image: none;
    image: url({shrink_icon});
}}

QTreeView::item:hover {{
    color: {settings.get_theme()["fonts"]["default"]["color"]};
    background-color: {settings.get_theme()["indication"]["hover"]};
}}
QTreeView::item:selected {{
    color: {settings.get_theme()["fonts"]["default"]["color"]};
    background-color: {settings.get_theme()["indication"]["selection"]};
}}
"""
        return style_sheet


class StyleSheetLineEdit:
    @staticmethod
    def standard():
        style_sheet = f"""
QLineEdit {{
    text-align: left;
    background: {settings.get_theme()["indication"]["passivebackground"]};
    color: {settings.get_theme()["fonts"]["default"]["color"]};
    border: 1px solid {settings.get_theme()["indication"]["passiveborder"]};
    font-family: {settings.get("current_font_name")};
    font-size: {settings.get("current_font_size")}pt;
    padding: 0px 5px 0px 5px;
}}
    """
        return style_sheet
