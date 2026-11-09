"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

from typing import Any

import uuid
import qt
import data
import settings

from gui.stylesheets import *


class Menu(qt.QMenu):
    menu_cache: dict[uuid.UUID, "Menu"] = {}
    _id: uuid.UUID

    @staticmethod
    def update_styles() -> None:
        delete_list: list[uuid.UUID] = []
        for k, v in Menu.menu_cache.items():
            try:
                v.update_style()
            except:
                delete_list.append(k)
        for d in delete_list:
            Menu.menu_cache.pop(d, None)

    def __del__(self) -> None:
        self.menu_cache.pop(self._id, None)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._id = uuid.uuid4()
        Menu.menu_cache[self._id] = self
        # Set options
        self.setToolTipsVisible(True)
        # Update style
        self.update_style()

    def setStyle(self, *args: Any, **kwargs: Any) -> None:
        super().setStyle(*args, **kwargs)
        self.update_style()

    def update_style(self) -> None:
        # Set the default font
        self.setFont(settings.get_menu_font())


class MenuBar(qt.QMenuBar):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        # Restyle
        self.update_style()

    def update_style(self) -> None:
        # Set the font from the menu font setting
        self.setFont(settings.get_menu_font())
