"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import functools
import os
import traceback
from typing import Any, cast

import constants
import data
import functions
import qt

from gui import (
    customeditor,
    hexview,
    markdownviewer,
    plaineditor,
    stylesheets,
    tabwidget,
    treedisplays,
)


class TheBoxSplitterHandle(qt.QSplitterHandle):
    """Splitter handle that re-balances the box on a double-click."""

    doubleClicked = qt.pyqtSignal()

    def __init__(self, orientation: qt.Qt.Orientation, parent: qt.QSplitter) -> None:
        super().__init__(orientation, parent)

    def mouseDoubleClickEvent(self, event: qt.QMouseEvent | None) -> None:
        self.doubleClicked.emit()
        super().mouseDoubleClickEvent(event)


class TheBox(qt.QSplitter):
    name: str | None = None
    parent_name: str | None = None
    generated_name: str | None = None
    main_form: Any = None

    def __init__(
        self,
        name: str,
        parent_name: str,
        orientation: qt.Qt.Orientation,
        parent: Any,
        main_form: Any,
    ) -> None:
        super().__init__(orientation, parent)
        self.main_form = main_form
        self._generate_name(name, parent_name)
        # Disable collapsing of children
        self.setChildrenCollapsible(False)
        # Connect the signals
        self.splitterMoved.connect(self.splitterMoveEvent)
        # Update style
        self.update_style()

    def createHandle(self) -> qt.QSplitterHandle:
        handle = TheBoxSplitterHandle(self.orientation(), self)
        handle.doubleClicked.connect(self.handle_double_clicked)
        return handle

    def _generate_name(self, name: str, parent_name: str) -> None:
        self.name = name
        self.parent_name = parent_name
        if self.name == "":
            self.generated_name = parent_name
        else:
            self.generated_name = ".".join([parent_name, name])
        self.setObjectName(self.generated_name)

    def _get_number_of_tabs(self) -> int:
        count = 0
        for t in self.main_form.get_all_windows():
            if self.generated_name in t.objectName():
                count += 1
        return count

    def is_empty(self) -> bool:
        return self.count() == 0

    def get_orientation_letter(self) -> str:
        if self.orientation() == qt.Qt.Orientation.Vertical:
            return "V"
        else:
            return "H"

    def update_orientations(self) -> None:
        if self.orientation() == qt.Qt.Orientation.Vertical:
            name = functions.right_replace(self.objectName(), "H", "V", 1)
        else:
            name = functions.right_replace(self.objectName(), "V", "H", 1)
        self.setObjectName(name)
        self.generated_name = name
        parent = self.parent()
        if isinstance(parent, TheBox) and parent.objectName() != "Main":
            parent.update_orientations()

    def add_box(
        self,
        orientation: qt.Qt.Orientation,
        index: int | None = None,
        add_tabs: bool = True,
    ) -> "TheBox":
        if orientation == qt.Qt.Orientation.Vertical:
            name_symbol = "V"
        else:
            name_symbol = "H"
        if index is not None:
            name = f"{name_symbol}{index}"
        else:
            # Count needed indexes
            new_index = self.count()
            name = f"{name_symbol}{new_index}"
        assert self.generated_name is not None
        box = TheBox(name, self.generated_name, orientation, self, self.main_form)
        if index is not None:
            self.insertWidget(index, box)
        else:
            self.addWidget(box)
        if add_tabs == True:
            tabs_number = self._get_number_of_tabs()
            tab_widget = tabwidget.TabWidget(self, self.main_form, self)
            assert box.generated_name is not None
            tab_widget.setObjectName(box.generated_name + f".Tabs{tabs_number}")
            box.addWidget(tab_widget)
        functions.process_events()
        return box

    def add_tabs(self, index: int | None = None) -> tabwidget.TabWidget:
        tabs_number = self._get_number_of_tabs()
        tab_widget = tabwidget.TabWidget(self, self.main_form, self)
        assert self.generated_name is not None
        tab_widget.setObjectName(self.generated_name + f".Tabs{tabs_number}")
        if index is not None:
            self.insertWidget(index, tab_widget)
        else:
            self.addWidget(tab_widget)
        functions.process_events()
        return tab_widget

    def rename(self, new_name: str) -> None:
        current_name = self.objectName()
        self.setObjectName(new_name)
        self.generated_name = new_name
        for b in self.main_form.findChildren(TheBox):
            on = b.objectName()
            if current_name in on:
                b.setObjectName(on.replace(current_name, new_name))
        for t in self.main_form.findChildren(tabwidget.TabWidget):
            on = t.objectName()
            if current_name in on:
                t.setObjectName(on.replace(current_name, new_name))

    def clear_all(self) -> None:
        for i in reversed(range(self.count())):
            widget = self.widget(i)
            if widget is not None:
                widget.setParent(None)
        for box in self.findChildren(TheBox):
            box.setParent(None)
        functions.process_events()

    def get_child_boxes(self) -> dict[Any, Any]:
        import gui.terminal as terminal

        classes, inverted_classes = self.main_form.view.get_layout_classes()
        children: dict[Any, Any] = {}
        for i in range(self.count()):
            child = self.widget(i)
            if child is None:
                continue
            if isinstance(child, TheBox):
                orientation = child.get_orientation_letter()
                sizes = child.sizes()
                total = sum(sizes)
                # Persist pane ratios instead of raw pixels so the layout
                # stays proportional across window sizes, screens and DPI
                # (legacy pixel lists are still recognized on restore).
                children[i] = {
                    f"BOX-{orientation}": child.get_child_boxes(),
                    "SIZES": [round(s / total, 6) for s in sizes]
                    if total > 0
                    else sizes,
                }
            else:
                tabs_widget = cast(tabwidget.TabWidget, child)
                tabs: dict[str, Any] = {}
                for j in range(tabs_widget.count()):
                    w = tabs_widget.widget(j)
                    if w is None:
                        continue
                    tab_text = tabs_widget.tabText(j)
                    name: Any = getattr(w, "name", None)
                    # Custom editor
                    if isinstance(w, customeditor.CustomEditor):
                        name = w.save_path
                        if name.strip() == "":
                            name = tab_text
                        line, index = w.getCursorPosition()
                        first_visible_line = w.firstVisibleLine()
                        assert w.internals is not None
                        tabs[name] = (
                            inverted_classes[w.__class__],
                            j,
                            (
                                line,
                                index,
                                first_visible_line,
                                w.internals.get_id(),
                            ),
                        )
                    elif isinstance(w, plaineditor.PlainEditor):
                        # REPL messages
                        if tab_text == constants.SpecialTabNames.Messages.value:
                            tabs[name] = (
                                constants.SpecialTabNames.Messages.value,
                                j,
                                (w.internals.get_id(),),
                            )
                    elif isinstance(w, treedisplays.TreeExplorer):
                        # Tree explorer
                        tree_name = "{}-{}".format(name, j)
                        assert w.internals is not None
                        tabs[tree_name] = (
                            inverted_classes[w.__class__],
                            j,
                            (
                                w.current_viewed_directory,
                                w.internals.get_id(),
                            ),
                        )

                    elif isinstance(w, hexview.HexView):
                        # Hex-view
                        hexview_name = "{}-{}".format(name, j)
                        assert w.internals is not None
                        tabs[hexview_name] = (
                            inverted_classes[w.__class__],
                            j,
                            (
                                w.save_path,
                                w.internals.get_id(),
                            ),
                        )
                    elif isinstance(w, markdownviewer.MarkdownViewer):
                        # Markdown viewer
                        markdownviewer_name = "{}-{}".format(name, j)
                        assert w.internals is not None
                        tabs[markdownviewer_name] = (
                            inverted_classes[w.__class__],
                            j,
                            (
                                w.save_path,
                                w.internals.get_id(),
                            ),
                        )
                    elif isinstance(w, terminal.Terminal):
                        # Terminal
                        terminal_name = "{}-{}".format(name, j)
                        assert w.internals is not None
                        tabs[terminal_name] = (
                            inverted_classes[w.__class__],
                            j,
                            (
                                w.current_working_directory,
                                getattr(w.backend, "shell", None),
                                w.internals.get_id(),
                            ),
                        )
                    else:
                        # tabs[name] = inverted_classes[w.__class__]
                        pass
                tabs["CURRENT-INDEX"] = tabs_widget.currentIndex()
                children[i] = {"TABS": tabs}
        return children

    def update_style(self) -> None:
        functions.process_events()

    """
    Overridden functions
    """

    def resizeEvent(self, e: qt.QResizeEvent | None) -> None:
        super().resizeEvent(e)
        mouse_buttons = data.application.mouseButtons()
        if mouse_buttons == qt.Qt.MouseButton.LeftButton:
            self.main_form.view.layout_save()

    def splitterMoveEvent(self, index: int, pos: int) -> None:
        mouse_buttons = data.application.mouseButtons()
        if mouse_buttons == qt.Qt.MouseButton.LeftButton:
            self.main_form.view.layout_save()

    def handle_double_clicked(self) -> None:
        """Equalize the box children when a splitter handle is double-clicked."""
        sizes = self.sizes()
        if len(sizes) > 1:
            self.setSizes(functions.integer_split(sum(sizes), len(sizes)))
