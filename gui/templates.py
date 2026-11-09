"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

from typing import Any

import enum

import qt
import data
import functions


class LayoutType(enum.Enum):
    Horizontal = 0
    Vertical = 1
    Grid = 2
    Stack = 3


def create_layout(
    layout: LayoutType = LayoutType.Horizontal,
    spacing: int = 0,
    margins: tuple[int, int, int, int] = (0, 0, 0, 0),
    parent: qt.QWidget | None = None,
) -> qt.QLayout:
    new_layout: qt.QLayout
    if layout == LayoutType.Horizontal:
        new_layout = qt.QHBoxLayout(parent)

    elif layout == LayoutType.Vertical:
        new_layout = qt.QVBoxLayout(parent)

    elif layout == LayoutType.Grid:
        new_layout = qt.QGridLayout(parent)

    elif layout == LayoutType.Stack:
        new_layout = qt.QStackedLayout(parent)

    else:
        raise Exception("Unknown layout type: '{}'".format(layout))

    new_layout.setSpacing(spacing)
    new_layout.setContentsMargins(*margins)
    return new_layout


def create_groupbox_borderless(
    name: str | None = None,
    parent: qt.QWidget | None = None,
) -> qt.QGroupBox:
    group_box = qt.QGroupBox(parent)
    if parent:
        group_box.setParent(parent)
    if name:
        group_box.setObjectName(name)

    def update_style() -> None:
        group_box.setStyleSheet(
            f"""
QGroupBox {{
    background: transparent;
    border: none;
}}
        """
        )

    setattr(group_box, "update_style", update_style)
    group_box.update_style()  # type: ignore[attr-defined]
    return group_box


def create_groupbox_with_layout(
    name: str | None = None,
    text: str | None = None,
    layout: LayoutType = LayoutType.Horizontal,
    borderless: bool = True,
    background_color: str | None = None,
    spacing: int | None = None,
    margins: tuple[int, int, int, int] | None = None,
    h_size_policy: qt.QSizePolicy.Policy = qt.QSizePolicy.Policy.Expanding,
    v_size_policy: qt.QSizePolicy.Policy = qt.QSizePolicy.Policy.Minimum,
    adjust_margins_to_text: bool = False,
    parent: qt.QWidget | None = None,
    override_margin_top: int | None = None,
) -> qt.QGroupBox:
    groupbox = None
    if borderless:
        groupbox = create_groupbox_borderless(name, parent=parent)
    else:
        raise Exception("UNIMPLEMENTED!")

    groupbox.setLayout(create_layout(layout=layout))
    if background_color is not None:
        groupbox.setStyleSheet(
            f"""
            background: {background_color};
        """
        )
    groupbox.setSizePolicy(qt.QSizePolicy(h_size_policy, v_size_policy))
    group_layout = groupbox.layout()
    assert group_layout is not None
    if spacing is not None:
        group_layout.setSpacing(spacing)
    if margins is not None:
        group_layout.setContentsMargins(*margins)
    if adjust_margins_to_text != False:
        fm = qt.QFontMetrics(qt.QApplication.font())
        font_height = fm.height() // 2
        current_margins = group_layout.contentsMargins()
        group_layout.setContentsMargins(
            current_margins.left(),
            current_margins.top() + font_height,
            current_margins.right(),
            current_margins.bottom(),
        )
    return groupbox


def create_frame(
    parent: qt.QWidget | None = None,
    layout: LayoutType = LayoutType.Horizontal,
    spacing: int = 0,
    margins: tuple[int, int, int, int] = (0, 0, 0, 0),
) -> qt.QFrame:
    frame = qt.QFrame(parent)
    frame_layout = create_layout(
        layout=layout, spacing=spacing, margins=margins, parent=frame
    )
    frame.setLayout(frame_layout)
    return frame


def create_scroll_area() -> qt.QScrollArea:
    scroll_area = qt.QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setHorizontalScrollBarPolicy(qt.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    vertical_bar = scroll_area.verticalScrollBar()
    horizontal_bar = scroll_area.horizontalScrollBar()
    assert vertical_bar is not None and horizontal_bar is not None
    vertical_bar.setContextMenuPolicy(qt.Qt.ContextMenuPolicy.NoContextMenu)
    horizontal_bar.setContextMenuPolicy(qt.Qt.ContextMenuPolicy.NoContextMenu)
    scroll_area.setFrameShape(qt.QFrame.Shape.NoFrame)
    return scroll_area
