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
from typing import Any

import qt
import data
import settings
import functions


class DockingOverlay:
    INFO_POINT_SIZE: tuple[int, int] = (30, 30)
    parent: Any = None
    overlay_label: Any = None
    storage: list["DockingOverlay.BaseDockLabel"] = []

    class BaseDockLabel(qt.QLabel):
        name: str | None = None
        widget: Any = None
        initial_position: tuple[float, float] | None = None
        expanded_position: tuple[float, float] | None = None
        initial_size: tuple[float, float] | None = None
        expanded_size: tuple[float, float] | None = None
        stored_drag_enter_event: Any = None

        def __init__(
            self,
            name: str,
            parent: Any,
            widget: Any,
            initial_position: tuple[float, float],
            expanded_position: tuple[float, float],
            initial_size: tuple[float, float],
            expanded_size: tuple[float, float],
            image_path: str,
        ) -> None:
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

        def dragEnterEvent(self, event: qt.QDragEnterEvent | None) -> None:
            if event is None:
                return
            event.accept()
            assert self.expanded_position is not None and self.expanded_size is not None
            self.setGeometry(
                int(self.expanded_position[0]),
                int(self.expanded_position[1]),
                int(self.expanded_size[0]),
                int(self.expanded_size[1]),
            )
            self.stored_drag_enter_event = event.clone()
            self.widget.dragEnterEvent(event)
            return super().dragEnterEvent(event)

        def dragLeaveEvent(self, event: qt.QDragLeaveEvent | None) -> None:
            assert self.initial_position is not None and self.initial_size is not None
            self.setGeometry(
                int(self.initial_position[0]),
                int(self.initial_position[1]),
                int(self.initial_size[0]),
                int(self.initial_size[1]),
            )
            return super().dragLeaveEvent(event)

    class CentralDockLabel(BaseDockLabel):
        def dropEvent(self, event: qt.QDropEvent | None) -> None:
            main_form: Any = self.parent()
            main_form.display.docking_overlay_hide()
            self.widget.dropEvent(event)
            main_form.view.reindex_all_windows()
            return super().dropEvent(event)

    class SideDockLabel(BaseDockLabel):
        """
        Dock point that splits the hovered pane to make room for the dropped
        tab(s). The dropped pane receives `default_drop_ratio` (percent) of the
        original pane's extent; sibling panes are left untouched.
        """

        def dropEvent(self, event: qt.QDropEvent | None) -> None:
            main_form: Any = self.parent()
            main_form.display.docking_overlay_hide()
            box = self.widget.parent()
            # Normalized share (0..1) granted to the dropped pane
            ratio = functions.clamp(
                settings.get("default_drop_ratio") / 100.0, 0.05, 0.95
            )
            vertical_drop = self.name in ("top", "bottom")
            new_first = self.name in ("top", "left")
            new_second = self.name in ("bottom", "right")
            if vertical_drop:
                along_axis = box.orientation() == qt.Qt.Orientation.Vertical
            else:
                along_axis = box.orientation() == qt.Qt.Orientation.Horizontal

            if along_axis:
                # The drop runs along the box's current split axis: insert an
                # adjacent tab and shrink only the hovered pane's region.
                tabs_index = box.indexOf(self.widget)
                insert_index = tabs_index + (1 if new_second else 0)
                old_sizes = box.sizes()
                new_share, old_share = functions.ratio_split_sizes(
                    old_sizes[tabs_index], ratio
                )
                tabs = box.add_tabs(index=insert_index)
                tabs.dragEnterEvent(self.stored_drag_enter_event)
                tabs.dropEvent(event)
                new_sizes = []
                for i, size in enumerate(old_sizes):
                    if i == tabs_index:
                        if new_first:
                            new_sizes.append(new_share)
                            new_sizes.append(old_share)
                        else:
                            new_sizes.append(old_share)
                            new_sizes.append(new_share)
                    else:
                        new_sizes.append(size)
                box.setSizes(new_sizes)
            elif box.count() == 1:
                # Flip the whole box onto the drop axis and split its only pane.
                if vertical_drop:
                    orientation = qt.Qt.Orientation.Vertical
                    old_extent = box.size().height()
                else:
                    orientation = qt.Qt.Orientation.Horizontal
                    old_extent = box.size().width()
                new_share, old_share = functions.ratio_split_sizes(old_extent, ratio)
                box.setOrientation(orientation)
                box.update_orientations()
                if new_first:
                    tabs = box.add_tabs(index=0)
                else:
                    tabs = box.add_tabs()
                tabs.dragEnterEvent(self.stored_drag_enter_event)
                tabs.dropEvent(event)
                if new_first:
                    box.setSizes([new_share, old_share])
                else:
                    box.setSizes([old_share, new_share])
            else:
                # Wrap the hovered pane into a nested box on the drop axis and
                # split that pane's region, leaving sibling panes untouched.
                tabs_index = box.indexOf(self.widget)
                old_sizes = box.sizes()
                new_share, old_share = functions.ratio_split_sizes(
                    old_sizes[tabs_index], ratio
                )
                old_tabs = box.widget(tabs_index)
                old_tabs.hide()
                if vertical_drop:
                    orientation = qt.Qt.Orientation.Vertical
                else:
                    orientation = qt.Qt.Orientation.Horizontal
                new_box = box.add_box(orientation, index=tabs_index, add_tabs=False)
                new_box.addWidget(old_tabs)
                old_tabs.show()
                old_tabs.box = new_box
                if new_first:
                    new_tabs = new_box.add_tabs(index=0)
                else:
                    new_tabs = new_box.add_tabs()
                new_tabs.dragEnterEvent(self.stored_drag_enter_event)
                new_tabs.dropEvent(event)
                if new_first:
                    new_box.setSizes([new_share, old_share])
                else:
                    new_box.setSizes([old_share, new_share])
                box.setSizes(old_sizes)

            # Reindex the tabs in the box (also schedules the layout save)
            main_form.view.reindex_all_windows()

            return super().dropEvent(event)

    @staticmethod
    def get_scaled_point_size() -> tuple[float, float]:
        return (
            DockingOverlay.INFO_POINT_SIZE[0]
            * settings.get("toplevel_menu_scale")
            / 100.0,
            DockingOverlay.INFO_POINT_SIZE[1]
            * settings.get("toplevel_menu_scale")
            / 100.0,
        )

    @staticmethod
    def get_scaled_font_size() -> float:
        return 10 * settings.get("toplevel_menu_scale") / 100.0

    @staticmethod
    def create_dock_point(
        name: str,
        parent: Any,
        widget: Any,
        _type: type["DockingOverlay.BaseDockLabel"],
        initial_position: tuple[float, float],
        expanded_position: tuple[float, float],
        initial_size: tuple[float, float],
        expanded_size: tuple[float, float],
        image_path: str,
        store: bool = True,
    ) -> "DockingOverlay.BaseDockLabel":
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

    def __init__(self, parent: Any) -> None:
        self.parent = parent

    def show_on_parent(self, docking_widgets: list[Any]) -> None:
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
            # The side previews expand to the split share granted to the
            # dropped pane, so what you see matches the resulting split
            ratio = functions.clamp(
                settings.get("default_drop_ratio") / 100.0, 0.05, 0.95
            )
            pane_width = widget.geometry().width() * ratio
            pane_height = widget.geometry().height() * ratio
            for i, p in enumerate(rest):
                exp_pos = None
                exp_size = None
                name = None
                if i == 0:
                    exp_pos = (left[0], top[1])
                    exp_size = (pane_width, widget.geometry().height())
                    name = "left"
                elif i == 1:
                    exp_pos = (
                        (right[0] - pane_width + point_size[0]),
                        top[1],
                    )
                    exp_size = (pane_width, widget.geometry().height())
                    name = "right"
                elif i == 2:
                    exp_pos = (left[0], top[1])
                    exp_size = (widget.geometry().width(), pane_height)
                    name = "top"
                elif i == 3:
                    exp_pos = (
                        left[0],
                        (bottom[1] - pane_height + point_size[1]),
                    )
                    exp_size = (widget.geometry().width(), pane_height)
                    name = "bottom"
                assert name is not None
                assert exp_pos is not None
                assert exp_size is not None
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

    def hide(self) -> None:
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
