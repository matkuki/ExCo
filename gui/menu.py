# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2023 Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""


import uuid
import data

from .stylesheets import *


class Menu(data.QMenu):
    menu_cache = {}

    @staticmethod
    def update_styles():
        delete_list = []
        for k,v in Menu.menu_cache.items():
            try:
                v.update_style()
            except:
                delete_list.append(v)
        for d in delete_list:
            Menu.menu_cache.pop(d, None)

    def __del__(self):
        self.menu_cache.pop(self._id, None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._id = uuid.uuid4()
        Menu.menu_cache[self._id] = self
        # Set options
        self.setToolTipsVisible(True)
        # Set default font
        self.setFont(data.get_current_font())
        # Update style
        self.update_style()

    def setStyle(self, *args, **kwargs):
        super().setStyle(*args, **kwargs)
        self.update_style()

    def update_style(self):
        pass


class MenuBar(data.QMenuBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the default font
        self.setFont(data.get_current_font())
        # Restyle
        self.update_style()

    def update_style(self):
        pass








