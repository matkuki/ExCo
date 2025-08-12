"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import functools
import os
import traceback

import constants
import data
import functions
import qt

from gui import (
    customeditor,
    hexview,
    plaineditor,
    stylesheets,
    tabwidget,
    terminal,
    treedisplays,
)


class TheBox(qt.QSplitter):
    name = None
    parent_name = None
    generated_name = None
    main_form = None

    def __init__(self, name, parent_name, orientation, parent, main_form):
        super().__init__(orientation, parent)
        self.main_form = main_form
        self._generate_name(name, parent_name)
        # Disable collapsing of children
        self.setChildrenCollapsible(False)
        # Connect the signals
        self.splitterMoved.connect(self.splitterMoveEvent)
        # Update style
        self.update_style()

    def _generate_name(self, name, parent_name):
        self.name = name
        self.parent_name = parent_name
        if self.name == "":
            self.generated_name = parent_name
        else:
            self.generated_name = ".".join([parent_name, name])
        self.setObjectName(self.generated_name)

    def _get_number_of_tabs(self):
        count = 0
        for t in self.main_form.get_all_windows():
            if self.generated_name in t.objectName():
                count += 1
        return count

    def is_empty(self):
        return self.count() == 0

    def get_orientation_letter(self):
        if self.orientation() == qt.Qt.Orientation.Vertical:
            return "V"
        else:
            return "H"

    def update_orientations(self):
        if self.orientation() == qt.Qt.Orientation.Vertical:
            name = functions.right_replace(self.objectName(), "H", "V", 1)
        else:
            name = functions.right_replace(self.objectName(), "V", "H", 1)
        self.setObjectName(name)
        self.generated_name = name
        parent = self.parent()
        if isinstance(parent, TheBox) and parent.objectName() != "Main":
            parent.update_orientations()

    def add_box(self, orientation, index=None, add_tabs=True):
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
        box = TheBox(name, self.generated_name, orientation, self, self.main_form)
        if index is not None:
            self.insertWidget(index, box)
        else:
            self.addWidget(box)
        if add_tabs == True:
            tabs_number = self._get_number_of_tabs()
            tab_widget = tabwidget.TabWidget(self, self.main_form, self)
            tab_widget.setObjectName(box.generated_name + f".Tabs{tabs_number}")
            box.addWidget(tab_widget)
        return box

    def add_tabs(self, index=None):
        tabs_number = self._get_number_of_tabs()
        tab_widget = tabwidget.TabWidget(self, self.main_form, self)
        tab_widget.setObjectName(self.generated_name + f".Tabs{tabs_number}")
        if index is not None:
            self.insertWidget(index, tab_widget)
        else:
            self.addWidget(tab_widget)
        return tab_widget

    def rename(self, new_name):
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

    def clear_all(self):
        for i in reversed(range(self.count())):
            self.widget(i).setParent(None)
        for box in self.findChildren(TheBox):
            box.setParent(None)

    def get_child_boxes(self):
        classes, inverted_classes = self.main_form.view.get_layout_classes()
        children = {}
        for i in range(self.count()):
            child = self.widget(i)
            if isinstance(child, TheBox):
                orientation = child.get_orientation_letter()
                children[i] = {
                    f"BOX-{orientation}": child.get_child_boxes(),
                    "SIZES": child.sizes(),
                }
            else:
                tabs = {}
                for j in range(child.count()):
                    w = child.widget(j)
                    tab_text = child.tabText(j)
                    name = w.name
                    # Custom editor
                    if isinstance(w, customeditor.CustomEditor):
                        name = w.save_path
                        if name.strip() == "":
                            name = tab_text
                        line, index = w.getCursorPosition()
                        first_visible_line = w.firstVisibleLine()
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
                        tabs[hexview_name] = (
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
                        tabs[terminal_name] = (
                            inverted_classes[w.__class__],
                            j,
                            (
                                w.current_working_directory,
                                w.internals.get_id(),
                            ),
                        )
                    else:
                        # tabs[name] = inverted_classes[w.__class__]
                        pass
                tabs["CURRENT-INDEX"] = child.currentIndex()
                children[i] = {"TABS": tabs}
        return children

    def update_style(self):
        #        self.setStyleSheet(stylesheets.splitter.get_transparent_stylesheet())
        pass

    """
    Overridden functions
    """

    def resizeEvent(self, e):
        super().resizeEvent(e)
        mouse_buttons = data.application.mouseButtons()
        if mouse_buttons == qt.Qt.MouseButton.LeftButton:
            self.main_form.view.layout_save()

    def splitterMoveEvent(self, index, pos):
        mouse_buttons = data.application.mouseButtons()
        if mouse_buttons == qt.Qt.MouseButton.LeftButton:
            self.main_form.view.layout_save()
