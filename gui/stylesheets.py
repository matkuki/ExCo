
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


def stylesheet_scrollbar():
    down_arrow_image = functions.get_resource_file("feather/air-grey/chevron-down.svg")
    down_arrow_hover_image = functions.get_resource_file("feather/air-blue/chevron-down.svg")
    up_arrow_image = functions.get_resource_file("feather/air-grey/chevron-up.svg")
    up_arrow_hover_image = functions.get_resource_file("feather/air-blue/chevron-up.svg")
    width = 10
    height = 10
    color_background = data.theme.ScrollBar.background
    color_handle = data.theme.ScrollBar.handle
    color_handle_hover = data.theme.ScrollBar.handle_hover
    style_sheet = (f"""
        /*
            Horizontal
        */
        QScrollBar:horizontal {{
            border: none;
            background: {color_background};
            height: {height}px;
            margin: 0px 0px 0px 0px;
        }}
        QScrollBar::handle:horizontal {{
            background: {color_handle};
            min-width: 20px;
        }}
        QScrollBar::handle:hover {{
            background: {color_handle_hover};
        }}
        QScrollBar::handle:horizontal:pressed {{
            background: {color_handle_hover};
        }}
        
        QScrollBar::sub-line:horizontal, QScrollBar::add-line:horizontal,
        QScrollBar::left-arrow:horizontal, QScrollBar::right-arrow:horizontal,
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
            background: none;
            width: 0px;
            height: 0px;
        }}
        
        /*
            Vertical
        */
        QScrollBar:vertical {{
            border: none;
            background: {color_background};
            width: {width}px;
            margin: 0px 0px 0px 0px;
        }}
        QScrollBar::handle:vertical {{
            background: {color_handle};
            min-height: 20px;
        }}
        QScrollBar::handle:hover {{
            background: {color_handle_hover};
        }}
        QScrollBar::handle:vertical:pressed {{
            background: {color_handle_hover};
        }}
        
        QScrollBar::sub-line:vertical, QScrollBar::add-line:vertical,
        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical,
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
            background: none;
            width: 0px;
            height: 0px;
        }}
    """)
    return style_sheet