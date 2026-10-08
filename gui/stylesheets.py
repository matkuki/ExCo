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
            functions.get_resource_file(
                settings.get_theme()["right-arrow-menu-disabled-image"]
            ),
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
    def standard(background_transparent=False, no_border=False):
        background_color = settings.get_theme()["fonts"]["default"]["background"]
        if background_transparent:
            background_color = "transparent"
        border = f"1px solid {settings.get_theme()['indication']['passiveborder']}"
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

    @staticmethod
    def container(background_transparent=False):
        """Container frame with border collapse support.
        Outer containers get border, inner containers inherit via QSS descendant rules.
        """
        background_color = settings.get_theme()["fonts"]["default"]["background"]
        if background_transparent:
            background_color = "transparent"
        border = f"1px solid {settings.get_theme()['indication']['passiveborder']}"
        style_sheet = f"""
QFrame {{
    background-color: {background_color};
    border: {border};
    spacing: 0px;
}}
/* Border collapse: inner frames inherit outer border */
QFrame > QFrame {{
    border: none;
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
    border: 1px solid {};
    background-color: {};
    margin: 0px;
    spacing: 0px;
    padding: 0px;
}}
TabWidget[indicated=false]::pane {{
    border: 1px solid {};
    background-color: {};
}}
TabWidget[indicated=true]::pane {{
    border: 1px solid {};
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


class StyleSheetContainer:
    """Global container border collapse rules.

    All container widgets (QFrame, QScrollArea, QGroupBox, QScrollBar, etc.)
    should have single-line borders with collapse behavior when adjacent.
    """

    @staticmethod
    def global_rules():
        passive = settings.get_theme()["indication"]["passiveborder"]
        return f"""
/* ===== CONTAINER BORDER COLLAPSE ===== */
/* All container widgets get single-line borders */
QFrame#Container, QScrollArea, QGroupBox, QScrollBar {{
    border: 1px solid {passive};
}}

/* Border collapse: inner containers inherit outer border */
QFrame#Container > QFrame, QScrollArea > QWidget, QGroupBox > QFrame {{
    border: none;
}}

/* Top bars / filter bars: fixed height (28px), border-bottom only,
   no side margins so border runs edge-to-edge and aligns with vertical border */
QWidget#TopBar, QWidget#FilterBar {{
    border-bottom: 1px solid {passive};
    border-left: none;
    border-right: none;
    border-top: none;
}}

/* Action footers: fixed height, border-top only */
QWidget#ActionFooter {{
    border-top: 1px solid {passive};
    border-left: none;
    border-right: none;
    border-bottom: none;
}}

/* Scroll areas: border on scroll area itself, viewport has no frame */
QScrollArea {{ border: 1px solid {passive}; }}
QScrollArea > QWidget {{ border: none; }}
QScrollArea QWidget {{ border: none; }}
QAbstractScrollArea {{ border: 1px solid {passive}; }}
QAbstractScrollArea > QWidget {{ border: none; }}

/* QSplitter handles - single line between panes */
QSplitter::handle {{
    background: {passive};
    width: 1px;
    height: 1px;
}}
QSplitter::handle:horizontal {{ width: 1px; }}
QSplitter::handle:vertical {{ height: 1px; }}

/* TabWidget pane: 1px border, collapse with adjacent containers */
TabWidget::pane {{ border: 1px solid {passive}; }}
TabWidget QWidget {{ border: none; }}

/* QGroupBox: title area gets no extra border, content area inherits */
QGroupBox {{ border: 1px solid {passive}; margin-top: 0.5em; }}
QGroupBox::title {{ subcontrol-origin: margin; left: 10px; padding: 0 3px; }}
QGroupBox > QWidget {{ border: none; }}

/* QScrollBar: no border, handled by scroll area border */
QScrollBar {{ border: none; }}
"""

    @staticmethod
    def top_bar():
        """Top bar / filter bar: fixed height 28px, border-bottom only."""
        passive = settings.get_theme()["indication"]["passiveborder"]
        return f"""
QWidget#TopBar, QWidget#FilterBar {{
    border-bottom: 1px solid {passive};
    border-left: none;
    border-right: none;
    border-top: none;
}}
"""

    @staticmethod
    def action_footer():
        """Action footer: fixed height, border-top only."""
        passive = settings.get_theme()["indication"]["passiveborder"]
        return f"""
QWidget#ActionFooter {{
    border-top: 1px solid {passive};
    border-left: none;
    border-right: none;
    border-bottom: none;
}}
"""

    @staticmethod
    def scroll_area():
        """Scroll area with collapsed borders."""
        passive = settings.get_theme()["indication"]["passiveborder"]
        return f"""
QScrollArea {{ border: 1px solid {passive}; }}
QScrollArea > QWidget {{ border: none; }}
QScrollArea QWidget {{ border: none; }}
QAbstractScrollArea {{ border: 1px solid {passive}; }}
QAbstractScrollArea > QWidget {{ border: none; }}
"""

    @staticmethod
    def group_box():
        """QGroupBox with collapsed borders."""
        passive = settings.get_theme()["indication"]["passiveborder"]
        return f"""
QGroupBox {{ border: 1px solid {passive}; margin-top: 0.5em; }}
QGroupBox::title {{ subcontrol-origin: margin; left: 10px; padding: 0 3px; }}
QGroupBox > QWidget {{ border: none; }}
"""
