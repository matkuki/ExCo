"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import importlib
import math
import re
import typing

import data
import settings
import qt


class TheSquid:
    """
    The static object for executing functions that encompass multiple objects.
    """

    main_form = None
    repl = None
    repl_helper = None

    @staticmethod
    def init_objects(main_form):
        TheSquid.main_form = main_form
        TheSquid.repl = main_form.repl
        TheSquid.repl_helper = main_form.repl_helper

        TheSquid.__module_customeditor = importlib.import_module("gui.treedisplays")

    @staticmethod
    def update_objects():
        TheSquid.repl = TheSquid.main_form.repl
        TheSquid.repl_helper = TheSquid.main_form.repl_helper

    @staticmethod
    def update_styles():
        if TheSquid.main_form == None:
            # Do not update if the main form is not initialized
            return
        TheSquid.update_objects()

        if settings.get("custom_menu_font") != None:
            for action in TheSquid.main_form.menubar.stored_actions:
                action.setFont(qt.QFont(*settings.get("custom_menu_font")))

        windows = TheSquid.main_form.get_all_windows()

        for window in windows:
            window.customize_tab_bar()

            for i in range(window.count()):
                if hasattr(window.widget(i), "corner_widget"):
                    if settings.get("custom_menu_scale") != None:
                        window.widget(i).corner_widget.setIconSize(
                            qt.QSize(settings.get("custom_menu_scale"), settings.get("custom_menu_scale"))
                        )
                    else:
                        window.widget(i).corner_widget.setIconSize(qt.QSize(16, 16))
                if hasattr(window.widget(i), "internals"):
                    window.widget(i).internals.restyle_corner_button_icons()
                if isinstance(
                    window.widget(i), TheSquid.__module_customeditor.TreeDisplayBase
                ):
                    window.widget(i).update_styles()
