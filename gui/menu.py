
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2021 Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import os
import sip
import os.path
import collections
import traceback
import ast
import inspect
import math
import functools
import textwrap
import difflib
import re
import uuid
import time
import settings
import functions
import data
import components


class Menu(data.QMenu):
    menu_cache = {}
    
    @staticmethod
    def update_styles():
        delete_list = []
        for k,v in Menu.menu_cache.items():
            if not sip.isdeleted(v):
                v.update_style()
            else:
                delete_list.append(v)
        for d in delete_list:
            Menu.menu_cache.pop(d, None)
    
    def __del__(self):
        self.menu_cache.pop(self._id, None)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._id = uuid.uuid4()
        Menu.menu_cache[self._id] = self
        # Set default font
        self.setFont(data.get_current_font())
        # Update style
        self.update_style()
    
    def setStyle(self, *args, **kwargs):
        super().setStyle(*args, **kwargs)
        self.update_style()
    
    def update_style(self):
        style_sheet = """
            QMenu {{
                background-color: {};
                border: 1px solid {};
                color: {};
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
        self.setStyleSheet(style_sheet)


class MenuBar(data.QMenuBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the default font
        self.setFont(data.get_current_font())
        # Restyle
        self.update_style()
    
    def update_style(self):
        self.setStyleSheet("""
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
        ))








