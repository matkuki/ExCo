# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2022 Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import data
import functions


def create_layout(vertical=False,
                  spacing=0,
                  margins=(0,0,0,0),
                  parent=None,
                  ):
    if isinstance(vertical, bool) and vertical:
        assert vertical == True
        new_layout = data.QVBoxLayout(parent)

    elif vertical == 'grid':
        new_layout = data.QGridLayout(parent)

    elif vertical == 'stack':
        new_layout = data.QStackedLayout(parent)

    else:
        assert vertical == False
        new_layout = data.QHBoxLayout(parent)

    new_layout.setSpacing(spacing)
    new_layout.setContentsMargins(*margins)
    return new_layout

def create_groupbox_borderless(name=None,
                               parent=None,
                               ):
    group_box = data.QGroupBox(parent)
    if parent:
        group_box.setParent(parent)
    if name:
        group_box.setObjectName(name)
    def update_style():
        group_box.setStyleSheet(f"""
QGroupBox {{
    background: transparent;
    border: none;
}}
        """)
    group_box.update_style = update_style
    group_box.update_style()
    return group_box

def create_groupbox_with_layout(name=None,
                                text=None,
                                vertical=True,
                                borderless=False,
                                background_color=None,
                                spacing=None,
                                margins=None,
                                h_size_policy=data.QSizePolicy.Policy.Expanding,
                                v_size_policy=data.QSizePolicy.Policy.Minimum,
                                adjust_margins_to_text=False,
                                parent=None,
                                override_margin_top=None,
                                ):
    groupbox = None
    if borderless:
        groupbox = create_groupbox_borderless(
            name, parent=parent
        )
    else:
        groupbox = create_groupbox(
            name,
            text,
            parent=parent,
            override_margin_top=override_margin_top
        )
    groupbox.setLayout(
        create_layout(
            vertical=vertical
        )
    )
    if background_color is not None:
        groupbox.setStyleSheet(f"""
            background: {background_color};
        """)
    groupbox.setSizePolicy(
        data.QSizePolicy(h_size_policy, v_size_policy)
    )
    if spacing is not None:
        groupbox.layout().setSpacing(spacing)
    if margins is not None:
        groupbox.layout().setContentsMargins(*margins)
    if adjust_margins_to_text != False:
        fm = data.QFontMetrics(data.get_general_font())
        font_height = fm.height() / 2
        margins = groupbox.layout().contentsMargins()
        groupbox.layout().setContentsMargins(
            margins.left(),
            margins.top() + font_height,
            margins.right(),
            margins.bottom()
        )
    return groupbox