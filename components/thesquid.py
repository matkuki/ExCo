
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2019 Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import data
import functions
import gui
import re
import math
import typing

from .customstyle import *


class TheSquid:
    """
    The static object for executing functions that encompass multiple objects.
    """
    main_form = None
    main_window = None
    upper_window = None
    lower_window = None
    repl = None
    repl_helper = None
    
    @staticmethod
    def init_objects(main_form):
        TheSquid.main_form = main_form
        TheSquid.main_window = main_form.main_window
        TheSquid.upper_window = main_form.upper_window
        TheSquid.lower_window = main_form.lower_window
        TheSquid.repl = main_form.repl
        TheSquid.repl_helper = main_form.repl_helper
    
    @staticmethod
    def update_objects():
        TheSquid.main_window = TheSquid.main_form.main_window
        TheSquid.upper_window = TheSquid.main_form.upper_window
        TheSquid.lower_window = TheSquid.main_form.lower_window
        TheSquid.repl = TheSquid.main_form.repl
        TheSquid.repl_helper = TheSquid.main_form.repl_helper
    
    @staticmethod
    def update_styles():
        if TheSquid.main_form == None:
            # Do not update if the main form is not initialized
            return
        TheSquid.update_objects()
        
        TheSquid.customize_menu_style(TheSquid.main_form.menubar)
        if data.custom_menu_font != None:
            for action in TheSquid.main_form.menubar.stored_actions:
                action.setFont(data.QFont(*data.custom_menu_font))
        TheSquid.customize_menu_style(TheSquid.main_form.sessions_menu)
        TheSquid.customize_menu_style(TheSquid.main_form.recent_files_menu)
        TheSquid.customize_menu_style(TheSquid.main_form.save_in_encoding)
        TheSquid.customize_menu_style(TheSquid.main_form.bookmark_menu)
        
        def set_style(menu):
            if hasattr(menu, "actions"):
                TheSquid.customize_menu_style(menu)
                for item in menu.actions():
                    if item.menu() != None:
                        TheSquid.customize_menu_style(item.menu())
                        set_style(item)
        set_style(TheSquid.main_form.sessions_menu)
        
        windows = [
            TheSquid.main_window,
            TheSquid.upper_window,
            TheSquid.lower_window
        ]
        
        for window in windows:
            window.customize_tab_bar()
        
            for i in range(window.count()):
                if hasattr(window.widget(i), "corner_widget"):
                    TheSquid.customize_menu_style(
                        window.widget(i).corner_widget
                    )
                    if data.custom_menu_scale != None:
                        window.widget(i).corner_widget.setIconSize(
                            data.QSize(
                                data.custom_menu_scale, data.custom_menu_scale
                            )
                        )
                    else:
                        window.widget(i).corner_widget.setIconSize(
                            data.QSize(16, 16)
                        )
                if hasattr(window.widget(i), "icon_manipulator"):
                    window.widget(i).icon_manipulator.restyle_corner_button_icons()
                if isinstance(window.widget(i), gui.TreeDisplayBase):
                    window.widget(i).update_styles()
    
    @staticmethod
    def customize_menu_style(menu):
        if data.custom_menu_scale != None and data.custom_menu_font != None:
            # Customize the style
            try:
                default_style_name = data.QApplication.style().objectName()
                custom_style = CustomStyle(default_style_name)
                menu.setStyle(custom_style)
            except:
                if data.platform == "Windows":
                    custom_style = CustomStyle("Windows")
                    menu.setStyle(custom_style)
                else:
                    custom_style = CustomStyle("GTK")
                    menu.setStyle(custom_style)
        else:
            # Reset the style
            menu.setStyle(data.QApplication.style())