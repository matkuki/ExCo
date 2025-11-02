"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import os
import sys
import keyword
import inspect
import textwrap
import traceback

import qt
import data
import settings
import functions


class DockingOverlay:
    INFO_POINT_SIZE = (30, 30)
    parent = None
    overlay_label = None
    storage = []

    class BaseDockLabel(qt.QLabel):
        name = None
        widget = None
        initial_position = None
        expanded_position = None
        initial_size = None
        expanded_size = None

        def __init__(
            self,
            name,
            parent,
            widget,
            initial_position,
            expanded_position,
            initial_size,
            expanded_size,
            image_path,
        ):
            super().__init__(parent)
            self.name = name
            self.widget = widget
            self.setAcceptDrops(True)
            self.setScaledContents(False)
            self.setAlignment(
                qt.Qt.AlignmentFlag.AlignHCenter | qt.Qt.AlignmentFlag.AlignVCenter
            )
            self.setStyleSheet(
                f"""
QLabel {{
    border-color: {settings.get_theme()["indication"]["passiveborder"]};
    border-width: 1px;
    border-style: solid;
    padding: 0px;
    background: {settings.get_theme()["dock_point_color_passive"]};
    margin: 0px 0px 0px 0px;
}}
QLabel:hover {{
    border-color: {settings.get_theme()["indication"]["passiveborder"]};
    border-width: 1px;
    border-style: solid;
    padding: 0px;
    background: {settings.get_theme()["dock_point_color_active"]};
    margin: 0px 0px 0px 0px;
}}
            """
            )
            icon_scale = 0.8
            self.setPixmap(
                functions.create_pixmap_with_size(
                    image_path,
                    initial_size[0] * icon_scale,
                    initial_size[1] * icon_scale,
                )
            )

            self.setGeometry(
                int(initial_position[0]),
                int(initial_position[1]),
                int(initial_size[0]),
                int(initial_size[1]),
            )
            self.initial_position = initial_position
            self.expanded_position = expanded_position
            self.initial_size = initial_size
            self.expanded_size = expanded_size

        def dragEnterEvent(self, event):
            event.accept()
            self.setGeometry(
                int(self.expanded_position[0]),
                int(self.expanded_position[1]),
                int(self.expanded_size[0]),
                int(self.expanded_size[1]),
            )
            self.stored_drag_enter_event = event.clone()
            self.widget.dragEnterEvent(event)
            return super().dragEnterEvent(event)

        def dragLeaveEvent(self, event):
            self.setGeometry(
                int(self.initial_position[0]),
                int(self.initial_position[1]),
                int(self.initial_size[0]),
                int(self.initial_size[1]),
            )
            return super().dragLeaveEvent(event)

    class CentralDockLabel(BaseDockLabel):
        def dropEvent(self, event):
            main_form = self.parent()
            main_form.display.docking_overlay_hide()
            self.widget.dropEvent(event)
            main_form.view.reindex_all_windows()
            main_form.view.layout_save()
            return super().dropEvent(event)

    class SideDockLabel(BaseDockLabel):
        def dropEvent(self, event):
            main_form = self.parent()
            main_form.display.docking_overlay_hide()
            box = self.widget.parent()
            if self.name == "top" or self.name == "bottom":
                if box.orientation() == qt.Qt.Orientation.Vertical:
                    tabs_index = box.indexOf(self.widget)
                    if self.name == "bottom":
                        insert_index = tabs_index + 1
                    else:
                        insert_index = tabs_index
                    tabs = box.add_tabs(index=insert_index)
                    tabs.dragEnterEvent(self.stored_drag_enter_event)
                    tabs.dropEvent(event)
                else:
                    if box.count() == 1:
                        box.setOrientation(qt.Qt.Orientation.Vertical)
                        box.update_orientations()
                        if self.name == "top":
                            box.rename(box.objectName())
                            tabs = box.add_tabs(index=0)
                        else:
                            tabs = box.add_tabs()
                        tabs.dragEnterEvent(self.stored_drag_enter_event)
                        tabs.dropEvent(event)
                    else:
                        tabs_index = box.indexOf(self.widget)
                        old_tabs = box.widget(tabs_index)
                        old_tabs.hide()
                        new_box = box.add_box(
                            qt.Qt.Orientation.Vertical, index=tabs_index, add_tabs=False
                        )
                        new_box.addWidget(old_tabs)
                        old_tabs.show()
                        old_tabs.box = new_box
                        if self.name == "top":
                            new_box.add_tabs(index=0)
                            new_tabs = new_box.widget(0)
                        else:
                            new_tabs = new_box.add_tabs()
                        new_tabs.dragEnterEvent(self.stored_drag_enter_event)
                        new_tabs.dropEvent(event)
                        split_size = int(box.height() / box.count())
                        new_box.setSizes([split_size] * new_box.count())

            elif self.name == "right" or self.name == "left":
                if box.orientation() == qt.Qt.Orientation.Horizontal:
                    tabs_index = box.indexOf(self.widget)
                    if self.name == "right":
                        insert_index = tabs_index + 1
                    else:
                        insert_index = tabs_index
                    tabs = box.add_tabs(index=insert_index)
                    tabs.dragEnterEvent(self.stored_drag_enter_event)
                    tabs.dropEvent(event)
                else:
                    if box.count() == 1:
                        box.setOrientation(qt.Qt.Orientation.Horizontal)
                        box.update_orientations()
                        if self.name == "right":
                            tabs = box.add_tabs()
                        else:
                            tabs = box.add_tabs(index=0)
                        tabs.dragEnterEvent(self.stored_drag_enter_event)
                        tabs.dropEvent(event)
                    else:
                        tabs_index = box.indexOf(self.widget)
                        old_tabs = box.widget(tabs_index)
                        old_tabs.hide()
                        new_box = box.add_box(
                            qt.Qt.Orientation.Horizontal,
                            index=tabs_index,
                            add_tabs=False,
                        )
                        new_box.addWidget(old_tabs)
                        old_tabs.show()
                        old_tabs.box = new_box
                        new_tabs = new_box.add_tabs()
                        new_tabs.dragEnterEvent(self.stored_drag_enter_event)
                        new_tabs.dropEvent(event)
                        split_size = int(box.width() / box.count())
                        new_box.setSizes([split_size] * new_box.count())

            # Reindex the tabs in the box
            main_form.view.reindex_all_windows()

            # Split windows equally
            if box.orientation() == qt.Qt.Orientation.Horizontal:
                split_size = int(box.width() / box.count())
            else:
                split_size = int(box.height() / box.count())
            box.setSizes([split_size] * box.count())
            # Save layout
            main_form.view.layout_save()
            
            return super().dropEvent(event)

    @staticmethod
    def get_scaled_point_size():
        return (
            DockingOverlay.INFO_POINT_SIZE[0] * settings.get("toplevel_menu_scale") / 100.0,
            DockingOverlay.INFO_POINT_SIZE[1] * settings.get("toplevel_menu_scale") / 100.0,
        )

    @staticmethod
    def get_scaled_font_size():
        return 10 * settings.get("toplevel_menu_scale") / 100.0

    @staticmethod
    def create_dock_point(
        name,
        parent,
        widget,
        _type,
        initial_position,
        expanded_position,
        initial_size,
        expanded_size,
        image_path,
        store=True,
    ):
        dock_label = _type(
            name,
            parent,
            widget,
            initial_position,
            expanded_position,
            initial_size,
            expanded_size,
            image_path,
        )
        if store == True:
            DockingOverlay.storage.append(dock_label)
        return dock_label

    def __init__(self, parent):
        self.parent = parent

    def show_on_parent(self, docking_widgets):
        for widget in docking_widgets:
            point_size = DockingOverlay.get_scaled_point_size()
            center, left, right, top, bottom = functions.get_edges_to_widget(
                widget, self.parent, point_size
            )
            # Center point
            center_point_width = widget.geometry().width() / 2
            center_point_height = widget.geometry().height() / 2
            dock_point_center = self.create_dock_point(
                "center",
                self.parent,
                widget,
                DockingOverlay.CentralDockLabel,
                center,
                (
                    center[0] - (center_point_width / 2),
                    center[1] - (center_point_height / 2),
                ),
                point_size,
                (
                    point_size[0] + center_point_width,
                    point_size[1] + center_point_height,
                ),
                "various/window_insert.png",
            )
            dock_point_center.show()
            # Rest
            rest = (left, right, top, bottom)
            for i, p in enumerate(rest):
                exp_pos = None
                exp_size = None
                name = None
                if i == 0:
                    exp_pos = (left[0], top[1])
                    exp_size = (
                        widget.geometry().width() * 1 / 3,
                        widget.geometry().height(),
                    )
                    name = "left"
                elif i == 1:
                    exp_pos = (
                        (
                            right[0]
                            - (widget.geometry().width() * 1 / 3)
                            + point_size[0]
                        ),
                        top[1],
                    )
                    exp_size = (
                        widget.geometry().width() * 1 / 3,
                        widget.geometry().height(),
                    )
                    name = "right"
                elif i == 2:
                    exp_pos = (left[0], top[1])
                    exp_size = (
                        widget.geometry().width(),
                        widget.geometry().height() * 1 / 3,
                    )
                    name = "top"
                elif i == 3:
                    exp_pos = (
                        left[0],
                        (
                            bottom[1]
                            - (widget.geometry().height() * 1 / 3)
                            + point_size[1]
                        ),
                    )
                    exp_size = (
                        widget.geometry().width(),
                        widget.geometry().height() * 1 / 3,
                    )
                    name = "bottom"
                dock_point = self.create_dock_point(
                    name,
                    self.parent,
                    widget,
                    DockingOverlay.SideDockLabel,
                    p,
                    exp_pos,
                    point_size,
                    exp_size,
                    "various/plus.png",
                )
                dock_point.show()
                
        qt.QCoreApplication.processEvents()

    def hide(self):
        if self.overlay_label != None:
            self.overlay_label.hide()
        
        for w in DockingOverlay.storage:
            if hasattr(w, "description"):
                d = w.description
                d.setParent(None)
                d.deleteLater()
                w.description = None
            w.setParent(None)
        DockingOverlay.storage = []
