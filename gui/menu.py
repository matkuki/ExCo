
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
import themes


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
        self.update_style()
        Menu.menu_cache[self._id] = self
        # Set default font
        self.setFont(data.get_current_font())
    
    def update_style(self):
        self.setStyleSheet("""
            QMenu {{
                background-color: {};
                border: 1px solid {};
                color: {}
            }}
            QMenu::item {{
                background-color: transparent;
            }}
            QMenu::item:selected  {{
                background-color: {};
            }}
        """.format(
                data.theme.Indication.PassiveBackGround,
                data.theme.Indication.PassiveBorder,
                data.theme.Font.DefaultHtml,
                data.theme.Indication.Hover,
        ))


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
                data.theme.Indication.PassiveBackGround,
                data.theme.Font.DefaultHtml,
                data.theme.Indication.Hover,
        ))








