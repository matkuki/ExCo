
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


class IconManipulator:
    """
    Icon manipulator for a widget inside a basic widget
    """
    _parent = None
    _tab_widget = None
    corner_groupbox = None
    
    def __init__(self, parent=None, tab_widget=None):
        self._parent = parent
        self._tab_widget = tab_widget
    
    def __del__(self):
        self.remove_corner_groupbox()
    
    def set_icon(self, obj, icon):
        """
        Set the current icon and update it by sending the signal to the 
        parent basic widget
        """
        obj.current_icon = icon
        self.update_icon(obj)
    
    def update_tab_widget(self, new_tab_widget):
        self._tab_widget = new_tab_widget
    
    def update_icon(self, obj):
        """
        Update the current icon and update it by sending the signal to the 
        parent basic widget
        """
        tab_widget = self._tab_widget
        if isinstance(obj, gui.CustomEditor):
            if isinstance(tab_widget, gui.TabWidget):
                tab_widget.update_tab_icon(obj)
                self.update_corner_widget(obj)
            elif isinstance(tab_widget, gui.TextDiffer):
                tab_widget._parent.update_tab_icon(obj)
        elif isinstance(obj, gui.PlainEditor):
            if isinstance(tab_widget, gui.TabWidget):
                tab_widget.update_tab_icon(obj)
        elif hasattr(obj, "_parent") and obj.current_icon is not None:
            obj._parent.update_tab_icon(obj)
    
    def update_corner_widget(self, obj):
        if self.corner_groupbox is not None:
            tab_widget = self._tab_widget
            self.show_corner_groupbox(tab_widget)
            return True
        else:
            return False
    
    def remove_corner_groupbox(self):
        if self.corner_groupbox is None:
            return
        self.corner_groupbox = None
    
    def create_corner_button(self, icon, tooltip, function):
        button = data.QToolButton()
        if isinstance(icon, data.QIcon):
            button.setIcon(icon)
        else:
            button.setIcon(functions.create_icon(icon))
        button.setPopupMode(data.QToolButton.ToolButtonPopupMode.InstantPopup)
        button.setToolTip(tooltip)
        button.clicked.connect(function)
        return button
    
    def add_corner_button(self, icon, tooltip, function):
        # Create the group box for buttons if needed
        if self.corner_groupbox is None:
            self.corner_groupbox = data.QGroupBox(self._tab_widget)
            corner_layout = data.QHBoxLayout()
            corner_layout.setSpacing(0)
            corner_layout.setContentsMargins(0, 0, 0, 0)
            self.corner_groupbox.setLayout(corner_layout)
            self.corner_groupbox.setStyleSheet("QGroupBox{border: 0px;}")
            self.corner_groupbox.show()
        # Add the button
        button = self.create_corner_button(icon, tooltip, function)
        layout = self.corner_groupbox.layout()
        layout.addWidget(button)
        for i in range(layout.count()):
            if data.custom_menu_scale is not None:
                layout.itemAt(i).widget().setIconSize(
                    data.QSize(
                        data.custom_menu_scale, 
                        data.custom_menu_scale
                    )
                )
    
    def restyle_corner_button_icons(self):
        if self.corner_groupbox is None:
            return
        layout = self.corner_groupbox.layout()
        for i in range(layout.count()):
            if data.custom_menu_scale is not None:
                layout.itemAt(i).widget().setIconSize(
                    data.QSize(
                        data.custom_menu_scale, 
                        data.custom_menu_scale
                    )
                )
    
    def update_corner_button_icon(self, icon, index=0):
        if self.corner_groupbox is None:
            return
        layout = self.corner_groupbox.layout()
        if isinstance(icon, data.QIcon):
            layout.itemAt(index).widget().setIcon(icon)
        else:
            layout.itemAt(index).widget().setIcon(
                functions.create_icon(icon)
            )
    
    def show_corner_groupbox(self, tab_widget):
        if self.corner_groupbox is None:
            return
        tab_widget.setCornerWidget(self.corner_groupbox)
        self.corner_groupbox.show()
        self.corner_groupbox.setStyleSheet(
            "QGroupBox {border: 0px;}"
        )