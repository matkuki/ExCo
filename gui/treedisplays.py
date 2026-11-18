"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import ast
import base64
import enum
import html
import os
import os.path
import re
import shutil
import stat
import subprocess
import threading
import time
import traceback
import types
from functools import cmp_to_key
from pathlib import Path
from send2trash import send2trash
from typing import *

import components.actionfilter
import components.internals
import components.osclipboard
import components.thesquid
import components.treefilter
import components.vcsstatus
import constants
import data
import functions
import qt
import settings

from gui.dialogs import *
from gui.menu import *
from gui.stylesheets import *

# For type checking only (avoids circular imports)
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from gui.customeditor import CustomEditor


_collator: qt.QCollator = qt.QCollator()
_collator.setCaseSensitivity(qt.Qt.CaseSensitivity.CaseInsensitive)


def _component_category(component: str) -> int:
    if component.startswith("."):
        return 0
    if component.startswith("_"):
        return 1
    return 2


def _compare_names(first: str, second: str) -> int:
    first_components: list[str] = first.replace("\\", "/").split("/")
    second_components: list[str] = second.replace("\\", "/").split("/")
    for first_component, second_component in zip(first_components, second_components):
        first_category = _component_category(first_component)
        second_category = _component_category(second_component)
        if first_category != second_category:
            return -1 if first_category < second_category else 1
        comparison = _collator.compare(first_component, second_component)
        if comparison != 0:
            return -1 if comparison < 0 else 1
    if len(first_components) == len(second_components):
        return 0
    return -1 if len(first_components) < len(second_components) else 1


_sort_key = cmp_to_key(_compare_names)


def _format_size(size_bytes: int) -> str:
    """
    A human readable size with dot thousands separators, e.g. '55.55 kB'.

    Byte counts below 1 kB stay exact with grouped thousands; anything larger
    is shown in kB/MB/GB/TB with a decimal point - '1.234.567 B' becomes
    '1.18 MB' - and grows up to the next unit at 1024.
    """
    size: float = float(size_bytes)
    for unit in ("B", "kB", "MB", "GB", "TB"):
        if size < 1024.0:
            if unit == "B":
                return "{} B".format(f"{int(size):,}".replace(",", "."))
            return "{:.2f} {}".format(size, unit)
        size /= 1024.0
    return "{:.2f} PB".format(size)


def _tooltip_lines(path: str, info: os.stat_result, size_text: str | None) -> str:
    """
    The metadata tooltip lines for a stat'ed *path*, size line from *size_text*.

    A file gets its own stat-based size when none is given; a directory is
    expected to pass its recursive total, because walking that tree is the
    expensive part and happens lazily on hover instead.
    """
    if size_text is None and stat.S_ISREG(info.st_mode):
        size_text = _format_size(int(info.st_size))

    def _when(stamp: float) -> str:
        return time.strftime("%Y-%m-%d %H:%M", time.localtime(stamp))

    lines: list[str] = [path]
    if size_text is not None:
        lines.append("Size: " + size_text)
    lines.append("Created: {}".format(_when(float(info.st_ctime))))
    lines.append("Modified: {}".format(_when(float(info.st_mtime))))
    lines.append("Accessed: {}".format(_when(float(info.st_atime))))
    return "\n".join(lines)


def _tooltip_text(path: str, size_text: str | None) -> str | None:
    """The metadata tooltip for *path* with the already-computed *size_text*."""
    try:
        info: os.stat_result = os.stat(path)
    except OSError:
        return None
    return _tooltip_lines(path, info, size_text)


# A directory tooltip shows the total of everything under it, which usually
# means walking a whole tree. That walk now happens only once, on the first
# hover over the directory, and it is bounded, so a single huge subdirectory
# cannot stall the listing or the tooltip. A truncated result is shown with
# a '>' prefix rather than as if it were exact.
_MAX_DIR_SIZE_ENTRIES: int = 50_000


def _scan_directory_size(path: str) -> tuple[int, bool] | None:
    """
    Total regular-file size under *path*, or None when the tree is unreadable.

    Returns (total_bytes, truncated); a truncated scan stopped at
    _MAX_DIR_SIZE_ENTRIES files and so is only a lower bound.
    """
    total: int = 0
    scanned: int = 0
    try:
        for root, _dirs, files in os.walk(path, followlinks=False):
            for name in files:
                if scanned >= _MAX_DIR_SIZE_ENTRIES:
                    return total, True
                scanned += 1
                try:
                    total += os.path.getsize(os.path.join(root, name))
                except OSError:
                    pass
    except OSError:
        return None
    return total, False


def remove_readonly(func: Any, path: str, excinfo: Any) -> None:
    os.chmod(path, stat.S_IWRITE)
    func(path)


class TreeTabBase(qt.QWidget):
    """
    Container shared by the tree tabs: a filter bar on top, the tree below.

    The trees used to *be* the tab, which left nowhere to put a filter. A
    QTreeView cannot host a sibling widget - anything added to its layout is
    drawn inside the scroll area, so a bar lands centred over the rows instead
    of above them - so the tab is an ordinary widget holding the bar and the
    view.

    The view keeps everything Qt delivers to the tree (delegate, key release,
    mouse presses), because that is what has to happen on the widget that
    receives the events. The forwarding block below re-implements the view calls
    the handlers already make, so they keep reading the model directly: a filter
    on a QStandardItemModel hides rows in place, so a model index and a view
    index are the same index and there is nothing to translate.

    `findChildren(qt.QTreeView)` therefore finds the view, not the tab.
    """

    # Class variables
    main_form: Any = None
    _parent: qt.QWidget = None  # type: ignore[assignment]
    name: str = ""
    savable: constants.CanSave = constants.CanSave.NO  # type: ignore[assignment]
    tree_menu: Any = None
    internals: components.internals.Internals | None = None
    # Relayed from the view, which is where the events arrive. Kept here
    # because these signals used to live on the tree tab itself.
    key_release_signal = qt.pyqtSignal(str, dict)
    doubleClicked = qt.pyqtSignal(qt.QModelIndex)
    expanded = qt.pyqtSignal(qt.QModelIndex)
    # Set by _assemble()
    tree: qt.QTreeView = None  # type: ignore[assignment]
    filter_bar: Any = None
    row_filter: Any = None
    # Set by a subclass that offers a show/hide button for the filter bar
    filter_toggle: qt.QPushButton | None = None

    def __init__(self, parent: qt.QWidget | None, main_form: Any, name: str) -> None:
        """Initialization"""
        super().__init__(parent)
        self._parent = parent  # type: ignore[assignment]
        self.main_form = main_form
        self.name = name
        self.setFont(settings.get_current_font())

    def _assemble(self, placeholder: str) -> None:
        """Put the filter bar above the tree, in the tab's own layout"""
        self.main_layout: qt.QVBoxLayout = qt.QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.setLayout(self.main_layout)
        self.filter_bar = components.treefilter.TreeFilterBar(self, placeholder)
        self.filter_bar.filter_changed.connect(self.set_filter_text)
        self.filter_bar.focus_in.connect(self.__filter_bar_focus_in)
        self.main_layout.addWidget(self.filter_bar)
        self.main_layout.addWidget(self.tree)
        # Relay the view's own signals, so code that connects to the tab keeps
        # working now that the tree lives inside it.
        self.tree.doubleClicked.connect(self.doubleClicked)
        self.tree.expanded.connect(self.expanded)

    def set_filter_text(self, text: str) -> None:
        """Filter the tree with *text*"""
        self.row_filter.set_filter_text(text)

    def __filter_bar_focus_in(self) -> None:
        """A click on the filter field is focus, so check the indication."""
        self.main_form.view.indication_check()

    def filter_text(self) -> str:
        """The active query, trimmed"""
        return self.row_filter.filter_text()

    def focus_filter(self) -> None:
        """Put the keyboard focus in the filter field, showing the bar first"""
        self.set_filter_bar_visible(True)
        self.filter_bar.focus_filter()

    def clear_filter(self) -> None:
        """Empty the filter field"""
        self.filter_bar.clear_filter()

    def is_filter_bar_visible(self) -> bool:
        """Whether the filter bar is shown"""
        return not self.filter_bar.isHidden()

    def set_filter_bar_visible(self, visible: bool) -> None:
        """Show or hide the filter bar, clearing the query when it is hidden"""
        if visible == self.is_filter_bar_visible():
            return
        field_had_focus = self.filter_bar.filter_edit.hasFocus()
        self.filter_bar.setVisible(visible)
        if not visible:
            # A hidden bar must not keep files out of sight: the query would be
            # invisible and impossible to edit.
            self.clear_filter()
            if field_had_focus:
                self.tree.setFocus()
        self.__sync_filter_toggle(visible)
        self.__update_filter_toggle_tooltip(visible)

    def toggle_filter_bar(self) -> None:
        """Show the filter bar if it is hidden, hide it otherwise"""
        self.set_filter_bar_visible(not self.is_filter_bar_visible())

    def __sync_filter_toggle(self, visible: bool) -> None:
        """Keep a subclass's footer toggle on the same state as the bar"""
        toggle = self.filter_toggle
        if toggle is None or toggle.isChecked() == visible:
            return
        toggle.blockSignals(True)
        try:
            toggle.setChecked(visible)
        finally:
            toggle.blockSignals(False)

    def __update_filter_toggle_tooltip(self, visible: bool) -> None:
        """Make a subclass's footer toggle say what it will do next"""
        toggle = self.filter_toggle
        if toggle is not None:
            toggle.setToolTip(
                "Hide the filter field (Ctrl+Alt+F focuses it)"
                if visible
                else "Show the filter field (Ctrl+Alt+F focuses it)"
            )

    def update_filter_styles(self) -> None:
        """Re-apply the theme to the bar after a theme change"""
        self.filter_bar.apply_theme(settings.get_theme())

    def _model_changed(self, model: qt.QStandardItemModel | None) -> None:
        """Hand the new model to the row filter"""
        self.row_filter.attach(model, self.tree)

    """
    View forwarding
    """

    def setModel(self, model: qt.QAbstractItemModel | None) -> None:
        """Point the view at *model* and let the row filter follow it.

        The filter lives on the tab, so this is the one place that hands a new
        model over: a rebuilt node tree or file listing comes back filtered.
        """
        self.tree.setModel(model)
        if isinstance(model, qt.QStandardItemModel):
            self.row_filter.attach(model, self.tree)
        else:
            # clean_model() hands over None. Letting go here stops the filter
            # from holding model signals on a model nothing shows any more.
            self.row_filter.detach()

    def model(self) -> qt.QAbstractItemModel | None:
        return self.tree.model()

    def header(self) -> qt.QHeaderView:
        return self.tree.header()  # type: ignore[return-value]

    def expand(self, index: qt.QModelIndex) -> None:
        self.tree.expand(index)

    def collapse(self, index: qt.QModelIndex) -> None:
        self.tree.collapse(index)

    def isExpanded(self, index: qt.QModelIndex) -> bool:
        return self.tree.isExpanded(index)

    def expandAll(self) -> None:
        self.tree.expandAll()

    def collapseAll(self) -> None:
        self.tree.collapseAll()

    def scrollTo(
        self,
        index: qt.QModelIndex,
        hint: qt.QAbstractItemView.ScrollHint = qt.QAbstractItemView.ScrollHint.EnsureVisible,
    ) -> None:
        self.tree.scrollTo(index, hint)

    def selectedIndexes(self) -> list[qt.QModelIndex]:
        return self.tree.selectedIndexes()

    def currentIndex(self) -> qt.QModelIndex:
        return self.tree.currentIndex()

    def selectionModel(self) -> qt.QItemSelectionModel | None:
        return self.tree.selectionModel()

    def setCurrentIndex(self, index: qt.QModelIndex) -> None:
        self.tree.setCurrentIndex(index)

    def setSelectionMode(self, mode: qt.QAbstractItemView.SelectionMode) -> None:
        self.tree.setSelectionMode(mode)

    def setSelectionBehavior(
        self, behavior: qt.QAbstractItemView.SelectionBehavior
    ) -> None:
        self.tree.setSelectionBehavior(behavior)

    def setUniformRowHeights(self, uniform: bool) -> None:
        self.tree.setUniformRowHeights(uniform)

    def setAnimated(self, enable: bool) -> None:
        self.tree.setAnimated(enable)

    def setExpandsOnDoubleClick(self, enable: bool) -> None:
        self.tree.setExpandsOnDoubleClick(enable)

    def setObjectName(self, name: str) -> None:  # type: ignore[override]
        # Both halves carry the name: the sheet's rules are written against the
        # tree, and the container is what the tab holds.
        super().setObjectName(name)
        self.tree.setObjectName(name)

    def setIconSize(self, size: qt.QSize) -> None:
        self.tree.setIconSize(size)

    def setEditTriggers(self, triggers: qt.QAbstractItemView.EditTrigger) -> None:
        self.tree.setEditTriggers(triggers)

    def setItemDelegate(self, delegate: qt.QAbstractItemDelegate) -> None:
        self.tree.setItemDelegate(delegate)

    def setItemDelegateForColumn(
        self, column: int, delegate: qt.QAbstractItemDelegate
    ) -> None:
        self.tree.setItemDelegateForColumn(column, delegate)

    def itemDelegate(self) -> qt.QAbstractItemDelegate | None:
        return self.tree.itemDelegate()

    def resizeColumnToContents(self, column: int) -> None:
        self.tree.resizeColumnToContents(column)

    def indexAt(self, position: qt.QPoint) -> qt.QModelIndex:
        return self.tree.indexAt(position)

    def visualRect(self, index: qt.QModelIndex) -> qt.QRect:
        return self.tree.visualRect(index)

    def visualItemRect(self, item: qt.QTreeWidgetItem) -> qt.QRect:
        return self.tree.visualItemRect(item)  # type: ignore[attr-defined]

    def setSelection(
        self,
        selection: qt.QItemSelection,
        command: qt.QItemSelectionModel.SelectionFlag,
    ) -> None:
        self.tree.setSelection(selection, command)  # type: ignore[arg-type]

    def edit(self, index: qt.QModelIndex) -> None:
        self.tree.edit(index)

    def clearSelection(self) -> None:
        self.tree.clearSelection()

    def setFocus(
        self, reason: qt.Qt.FocusReason = qt.Qt.FocusReason.OtherFocusReason
    ) -> None:
        self.tree.setFocus(reason)

    def setFocusPolicy(self, policy: qt.Qt.FocusPolicy) -> None:
        self.tree.setFocusPolicy(policy)

    def setStyleSheet(self, style: str) -> None:  # type: ignore[override]
        super().setStyleSheet(style)
        self.tree.setStyleSheet(style)

    def setEnabled(self, enabled: bool) -> None:
        super().setEnabled(enabled)
        self.tree.setEnabled(enabled)

    def setFont(self, font: qt.QFont) -> None:
        super().setFont(font)
        if self.tree is not None:
            self.tree.setFont(font)

    def viewport(self) -> qt.QWidget:
        return self.tree.viewport()  # type: ignore[return-value]

    def horizontalScrollBar(self) -> qt.QScrollBar:
        return self.tree.horizontalScrollBar()  # type: ignore[return-value]

    def verticalScrollBar(self) -> qt.QScrollBar:
        return self.tree.verticalScrollBar()  # type: ignore[return-value]

    def scrollPosition(self) -> qt.QPoint:
        return self.tree.scrollPosition()  # type: ignore[attr-defined]

    def setScrollPosition(self, position: qt.QPoint) -> None:
        self.tree.setScrollPosition(position)  # type: ignore[attr-defined]

    def horizontalScrollbarAction(self, action: int) -> None:
        self.tree.horizontalScrollbarAction(action)


class TreeViewBase(qt.QTreeView):
    """
    The view half of a tree tab: the behaviour Qt delivers to the tree itself.

    A plain widget has no rows, so the scroll area, the delegate, the key
    release bookkeeping and the mouse presses all belong here. The container
    forwards the rest.
    """

    # Custom item delegate
    class CustomItemDelegate(qt.QStyledItemDelegate):
        def helpEvent(
            self,
            event: qt.QHelpEvent | None,
            view: qt.QAbstractItemView | None,
            option: qt.QStyleOptionViewItem,
            index: qt.QModelIndex,
        ) -> bool:
            # The explorer tooltips are resolved lazily per row (the recursive
            # directory size lives on a worker thread), so the container tab
            # answers the tooltip request instead of the item having one set.
            # Tabs without a resolver (the node tree, the sessions tree) keep
            # the default QStyledItemDelegate behaviour.
            if event is not None and view is not None and view.parent() is not None:
                if event.type() == qt.QEvent.Type.ToolTip:
                    resolve = getattr(view.parent(), "_resolve_item_tooltip", None)
                    if resolve is not None:
                        model: qt.QAbstractItemModel | None = index.model()
                        item: qt.QStandardItem | None = (
                            model.itemFromIndex(index)
                            if isinstance(model, qt.QStandardItemModel)
                            else None
                        )
                        if item is not None:
                            text: str | None = resolve(item, event.globalPos())
                            if text is not None:
                                qt.QToolTip.showText(event.globalPos(), text, view)
                                return True
            return super().helpEvent(event, view, option, index)

        def initStyleOption(  # type: ignore[override]
            self,
            option: qt.QStyleOptionViewItem,
            index: qt.QModelIndex,
        ) -> None:
            super().initStyleOption(option, index)
            # A tab that offers `_vcs_decoration` (the explorer) tints a row
            # and suffixes its state letter. This is done here, on the option,
            # and never in the model: a model write raises itemChanged, which
            # the explorer reads as a rename. sizeHint() goes through this
            # too, so the painted width and the scroll range agree.
            view: qt.QWidget | None = option.widget  # type: ignore[assignment]
            tab: Any = view.parent() if view is not None else None
            decorate: Any = getattr(tab, "_vcs_decoration", None)
            model: qt.QAbstractItemModel | None = index.model()
            if decorate is None or not isinstance(model, qt.QStandardItemModel):
                return
            item: qt.QStandardItem | None = model.itemFromIndex(index)
            if item is None:
                return
            decoration: tuple[str, qt.QColor] | None = decorate(item)
            if decoration is None:
                return
            letter, color = decoration
            if letter:
                option.text = f"{option.text}  {letter}"
            palette: qt.QPalette = option.palette
            palette.setColor(qt.QPalette.ColorRole.Text, color)
            palette.setColor(qt.QPalette.ColorRole.HighlightedText, color)
            option.palette = palette

        def createEditor(
            self,
            parent: qt.QWidget,  # type: ignore[override]
            option: qt.QStyleOptionViewItem,
            index: qt.QModelIndex,
        ) -> qt.QWidget:
            editor = qt.QLineEdit(parent)
            editor.setStyleSheet(StyleSheetLineEdit.standard())
            return editor

        def setEditorData(self, editor: qt.QWidget, index: qt.QModelIndex) -> None:  # type: ignore[override]
            editor.setText(index.data())  # type: ignore[attr-defined]

        def setModelData(
            self,
            editor: qt.QWidget,  # type: ignore[override]
            model: qt.QAbstractItemModel,  # type: ignore[override]
            index: qt.QModelIndex,
        ) -> None:
            model.setData(index, editor.text())  # type: ignore[attr-defined]

    # Signals
    key_release_signal = qt.pyqtSignal(str, dict)

    # Class variables
    main_form: Any = None
    _parent: qt.QWidget = None  # type: ignore[assignment]
    name: str = ""
    key_release_lock: bool = False
    default_menu_font: qt.QFont | None = None
    # Set by the container: what to do about a press and a key release.
    pressed_handler: Any = None
    key_release_handler: Any = None
    # Set by the container: what to do when an editor commits or closes.
    # These are the view's own virtual slots -- the tab is an ordinary widget
    # holding the view, so overriding them there would never be called.
    commit_handler: Any = None
    editor_closed_handler: Any = None

    def mousePressEvent(self, event: qt.QMouseEvent) -> None:  # type: ignore[override]
        """Forwarded to the tab, which owns the focus and save bookkeeping"""
        super().mousePressEvent(event)
        if self.pressed_handler is not None:
            self.pressed_handler(event)

    def commitData(self, editor: qt.QWidget) -> None:  # type: ignore[override]
        """Forwarded to the tab before the delegate writes the model."""
        if self.commit_handler is not None:
            self.commit_handler(editor)
        return super().commitData(editor)

    def closeEditor(self, *args: Any) -> None:
        """Forwarded to the tab before Qt reverts or destroys the editor."""
        if self.editor_closed_handler is not None:
            self.editor_closed_handler(args[0])
        return super().closeEditor(*args)

    def eventFilter(self, object: qt.QObject, event: qt.QEvent) -> bool:  # type: ignore[override]
        if not self.key_release_lock:
            # Check for keyboard releases
            if event.type() == qt.QEvent.Type.KeyRelease:
                key = data.keys[event.key()]  # type: ignore[attr-defined]
                modifiers = event.modifiers()  # type: ignore[attr-defined]
                modifier_shift = (
                    modifiers & qt.Qt.KeyboardModifier.ShiftModifier
                ) == qt.Qt.KeyboardModifier.ShiftModifier
                modifier_control = (
                    modifiers & qt.Qt.KeyboardModifier.ControlModifier
                ) == qt.Qt.KeyboardModifier.ControlModifier
                modifier_alt = (
                    modifiers & qt.Qt.KeyboardModifier.AltModifier
                ) == qt.Qt.KeyboardModifier.AltModifier
                modifier_meta = (
                    modifiers & qt.Qt.KeyboardModifier.MetaModifier
                ) == qt.Qt.KeyboardModifier.MetaModifier
                modifier_keypad = (
                    modifiers & qt.Qt.KeyboardModifier.KeypadModifier
                ) == qt.Qt.KeyboardModifier.KeypadModifier
                modifier_dict = {
                    "shift": modifier_shift,
                    "control": modifier_control,
                    "alt": modifier_alt,
                    "meta": modifier_meta,
                    "keypad": modifier_keypad,
                }
                # Emit a signal for a keyrelease
                self.key_release_signal.emit(key, modifier_dict)
                if self.key_release_handler is not None:
                    self.key_release_handler(key, modifier_dict)

        return super().eventFilter(object, event)

    def lock_key_release(self) -> None:
        """Stop emitting key releases while a modal child is up"""
        self.key_release_lock = True

    def unlock_key_release(self) -> None:
        """Resume emitting key releases"""
        self.key_release_lock = False


class Directory:
    """
    Object for holding directory/file information when building directory trees
    """

    item: qt.QStandardItem
    directories: dict[str, "Directory"]
    files: dict[str, qt.QStandardItem]

    def __init__(self, input_item: qt.QStandardItem) -> None:
        """Initialization"""
        self.item = input_item
        self.directories = {}
        self.files = {}

    def add_directory(self, dir_name: str, dir_item: qt.QStandardItem) -> "Directory":
        # Create a new instance of Directory class using the __class__ dunder method
        new_directory = self.__class__(dir_item)
        # Add the new directory to the dictionary
        self.directories[dir_name] = new_directory
        # Add the new directory item to the parent(self)
        self.item.appendRow(dir_item)
        # Return the directory object reference
        return new_directory

    def add_file(self, file_name: str, file_item: qt.QStandardItem) -> None:
        self.files[file_name] = file_item
        # Add the new file item to the parent(self)
        self.item.appendRow(file_item)


class TreeDisplay(TreeTabBase):
    # Class variables
    parent: qt.QWidget = None  # type: ignore[assignment]
    main_form: Any = None
    name: str = ""
    savable: constants.CanSave = constants.CanSave.NO  # type: ignore[assignment]
    current_icon: qt.QIcon | None = None
    internals: components.internals.Internals | None = None
    tree_display_type: constants.TreeDisplayType | None = None
    tree_menu: Any = None
    bound_tab: Any = None
    worker_thread: qt.QThread | None = None
    open_in_explorer_text: str = "Open in explorer"
    # Attributes specific to the display data
    bound_node_tab: Any = None
    # Node icons
    node_icons: dict[str, qt.QIcon]
    folder_icon: qt.QIcon
    goto_icon: qt.QIcon
    python_icon: qt.QIcon
    nim_icon: qt.QIcon
    c_icon: qt.QIcon
    cpp_icon: qt.QIcon

    def __del__(self) -> None:
        try:
            # Clean up the tree model
            try:
                self.clean_model()
            except:
                pass
            # Disconnect signals
            try:
                self.doubleClicked.disconnect()
                self.expanded.disconnect()
            except:
                pass
            # Let go of the rows the filter hid
            try:
                self.row_filter.detach()
            except Exception:
                pass
            # Clean up the file watcher
            try:
                self.__file_watcher.directoryChanged.disconnect()
                watched = self.__file_watcher.directories()
                if watched:
                    self.__file_watcher.removePaths(watched)
            except:
                pass
            # Clean up main references
            self.main_form.node_tree_tab = None
            self._parent = None  # type: ignore[assignment]
            self.main_form = None
            self.internals = None
            self.bound_tab = None
            if self.tree_menu is not None:
                self.tree_menu.setParent(None)
                self.tree_menu = None
            if self.worker_thread is not None:
                self.worker_thread.stop()  # type: ignore[attr-defined]
                self.worker_thread.wait()
                self.worker_thread.quit()
                self.worker_thread = None
            # Clean up self
            self.setParent(None)
            self.deleteLater()
        except:
            pass

    def parent_destroyed(self, event: qt.QEvent) -> None:
        # Connect the bound tab 'destroy' signal to this function
        # for automatic closing of this tree widget
        if self._parent is not None:
            self._parent.close_tab(self)  # type: ignore[attr-defined]

    def __init__(self, parent: qt.QWidget | None = None, main_form: Any = None) -> None:
        """Initialization"""
        # Initialize the superclass: the filter bar and the tree it filters
        super().__init__(parent, main_form, "Tree display")
        # Initialize components
        self.internals = components.internals.Internals(
            parent=parent, tab_widget=parent
        )
        # The tree, and the filter bar above it
        self.tree = TreeViewBase(self)
        self.tree.main_form = main_form
        self.tree._parent = parent  # type: ignore[assignment]
        self.tree.name = self.name
        self.tree.key_release_lock = False
        self._assemble("Filter nodes")
        # The rows are hidden in place, so a model index is a view index
        self.row_filter = components.treefilter.HiddenRowFilter(self, None)
        # Disable node expansion on double click
        self.setExpandsOnDoubleClick(False)
        # Connect the click and doubleclick signal
        self.doubleClicked.connect(self.__item_double_click)
        #        self.clicked.connect(self._item_click)
        # Connect the doubleclick signal
        self.expanded.connect(self._check_contents)
        # Initialize the icons
        # Node icons
        self.node_icons = {
            "module": functions.create_icon("various/node_module.png"),
            "import": functions.create_icon("various/node_module.png"),
            "function": functions.create_icon("various/node_procedure.png"),
            "procedure": functions.create_icon("various/node_procedure.png"),
            "proc": functions.create_icon("various/node_procedure.png"),
            "func": functions.create_icon("various/node_procedure.png"),
            "method": functions.create_icon("various/node_method.png"),
            "getter": functions.create_icon("various/node_method.png"),
            "property": functions.create_icon("various/node_method.png"),
            "var": functions.create_icon("various/node_variable.png"),
            "let": functions.create_icon("various/node_variable.png"),
            "variable": functions.create_icon("various/node_variable.png"),
            "alias": functions.create_icon("various/node_alias.png"),
            "externvar": functions.create_icon("various/node_variable.png"),
            "prototype": functions.create_icon("various/node_function.png"),
            "typedef": functions.create_icon("various/node_type.png"),
            "struct": functions.create_icon("various/node_type.png"),
            "enum": functions.create_icon("various/node_type.png"),
            "union": functions.create_icon("various/node_type.png"),
            "type": functions.create_icon("various/node_type.png"),
            "constant": functions.create_icon("various/node_const.png"),
            "const": functions.create_icon("various/node_const.png"),
            "enumerator": functions.create_icon("various/node_const.png"),
            "include": functions.create_icon("various/node_module.png"),
            "define": functions.create_icon("various/node_macro.png"),
            "pragma": functions.create_icon("various/node_pragma.png"),
            "undef": functions.create_icon("various/node_macro.png"),
            "error": functions.create_icon("various/node_macro.png"),
            "macro": functions.create_icon("various/node_macro.png"),
            "member": functions.create_icon("various/node_method.png"),
            "converter": functions.create_icon("various/node_converter.png"),
            "namespace": functions.create_icon("various/node_namespace.png"),
            "template": functions.create_icon("various/node_template.png"),
            "class": functions.create_icon("various/node_class.png"),
            "iterator": functions.create_icon("various/node_iterator.png"),
            "nothing": functions.create_icon("various/node_unknown.png"),
            "unknown": functions.create_icon("various/node_unknown.png"),
        }
        self.python_icon = functions.create_icon("language_icons/logo_python.png")
        self.nim_icon = functions.create_icon("language_icons/logo_nim.png")
        self.c_icon = functions.create_icon("language_icons/logo_c.png")
        self.cpp_icon = functions.create_icon("language_icons/logo_cpp.png")
        # File searching icons
        self.file_icon = functions.create_icon("tango_icons/file.png")
        self.folder_icon = functions.create_icon("tango_icons/folder.png")
        self.goto_icon = functions.create_icon("tango_icons/edit-goto.png")

        # Install event filter. The key releases arrive at the view, so the
        # filter is installed on the view as well.
        self.tree.installEventFilter(self.tree)
        # Set the item delegate
        self.tree.setItemDelegate(TreeViewBase.CustomItemDelegate())
        # Presses are delivered to the view, and the handler needs the tab's
        # references.
        self.tree.pressed_handler = self._on_mouse_pressed

        # Set the icon size for every node
        self.update_icon_size()

        # File system watcher for auto-refresh
        self._current_directory = None
        self._dir_watch_timer = None
        self._refresh_in_progress = False
        self.__file_watcher = qt.QFileSystemWatcher(self)
        self.__file_watcher.directoryChanged.connect(self.__directory_changed)

    def update_icon_size(self) -> None:
        self.setIconSize(
            functions.create_size(
                settings.get("tree_display_icon_size"),
                settings.get("tree_display_icon_size"),
            )
        )

    def __directory_changed(self, path: str) -> None:
        """Trigger a debounced refresh when the watched directory changes."""
        if self._current_directory is None:
            return
        if self._refresh_in_progress:
            return
        if self._dir_watch_timer is not None:
            self._dir_watch_timer.stop()
        else:
            self._dir_watch_timer = qt.QTimer(self)
            self._dir_watch_timer.setSingleShot(True)
            self._dir_watch_timer.timeout.connect(self.__refresh_directory)
        self._dir_watch_timer.start(100)

    def __refresh_directory(self) -> None:
        """Re-display the current directory after a filesystem change."""
        if self._current_directory is not None:
            self.display_directory_tree(self._current_directory)

    def get_node_icon(self, icon_name: str) -> qt.QIcon:
        if icon_name in self.node_icons.keys():
            return self.node_icons[icon_name]
        else:
            return self.node_icons["unknown"]

    def setFocus(
        self, reason: qt.Qt.FocusReason = qt.Qt.FocusReason.OtherFocusReason
    ) -> None:
        """Overridden focus event"""
        # Execute the supeclass focus function
        super().setFocus(reason)
        # Check indication
        self.main_form.view.indication_check()

    def _on_mouse_pressed(self, event: qt.QMouseEvent) -> None:
        """Bookkeeping for a press on the tree, called from the view.

        The view calls super() on itself first, so this must not: it would go
        to the tab, which is a plain widget and never sees the press.
        """
        # Set the focus
        self.setFocus()
        # Set the last focused widget to the parent basic widget
        self.main_form.last_focused_widget = self._parent
        # Set Save/SaveAs buttons in the menubar
        self._parent._set_save_status()  # type: ignore[attr-defined]
        # Get the index of the clicked item and execute the item's procedure
        if event.button() == qt.Qt.MouseButton.RightButton:
            index = self.indexAt(event.pos())
            self._item_click(index)
        # Reset the click&drag context menu action
        components.actionfilter.ActionFilter.clear_action()

    def _item_click(self, model_index: qt.QModelIndex) -> None:
        if self.tree_display_type == constants.TreeDisplayType.FILES:
            item = self.model().itemFromIndex(model_index)  # type: ignore[union-attr]
            if hasattr(item, "is_dir") == True or hasattr(item, "is_base") == True:

                def update_cwd() -> None:
                    self.main_form.set_cwd(item.full_name)

                cursor = qt.QCursor.pos()

                if self.tree_menu is not None:
                    self.tree_menu.setParent(None)
                    self.tree_menu = None

                self.tree_menu = Menu(self)

                # Open path in explorer
                open_in_explorer_action = qt.QAction(self.open_in_explorer_text, self)

                def open_in_explorer() -> None:
                    path = item.full_name
                    try:
                        result = functions.open_item_in_explorer(path)
                    except:
                        result = False
                    if result == False:
                        self.main_form.display.repl_display_error(
                            "Error opening path in explorer: {}".format(path)
                        )

                open_in_explorer_action.setIcon(
                    functions.create_icon("tango_icons/document-open.png")
                )
                open_in_explorer_action.triggered.connect(open_in_explorer)
                self.tree_menu.addAction(open_in_explorer_action)

                # Open in terminal
                item_full_name = getattr(item, "full_name", None)
                if item_full_name is not None:
                    terminal_path = functions.resolve_terminal_directory(
                        item_full_name, True
                    )

                    def open_in_terminal() -> None:
                        self.main_form.open_terminal_in_directory(
                            terminal_path, self._parent
                        )

                    open_in_terminal_action = qt.QAction("Open in Terminal", self)
                    open_in_terminal_action.setIcon(
                        functions.create_icon("tango_icons/utilities-terminal.png")
                    )
                    open_in_terminal_action.triggered.connect(open_in_terminal)
                    self.tree_menu.addAction(open_in_terminal_action)

                    # Open in external terminal
                    def open_in_external_terminal() -> None:
                        self.main_form.open_external_terminal(terminal_path)

                    open_in_external_terminal_action = qt.QAction(
                        "Open in External Terminal", self
                    )
                    open_in_external_terminal_action.setIcon(
                        functions.create_icon("tango_icons/utilities-terminal.png")
                    )
                    open_in_external_terminal_action.triggered.connect(
                        open_in_external_terminal
                    )
                    self.tree_menu.addAction(open_in_external_terminal_action)
                    self.tree_menu.addSeparator()

                # Clipboard copy name
                clipboard_copy_action = qt.QAction(
                    "Copy directory name to clipboard", self
                )

                def clipboard_copy() -> None:
                    cb = data.application.clipboard()
                    cb.clear(mode=cb.Mode.Clipboard)
                    cb.setText(item.text(), mode=cb.Mode.Clipboard)

                clipboard_copy_action.setIcon(
                    functions.create_icon("tango_icons/edit-copy.png")
                )
                clipboard_copy_action.triggered.connect(clipboard_copy)
                self.tree_menu.addAction(clipboard_copy_action)
                # Clipboard copy path
                clipboard_copy_path_action = qt.QAction(
                    "Copy directory path to clipboard", self
                )

                def clipboard_copy() -> None:
                    cb = data.application.clipboard()
                    cb.clear(mode=cb.Mode.Clipboard)
                    cb.setText(item.full_name, mode=cb.Mode.Clipboard)

                clipboard_copy_path_action.setIcon(
                    functions.create_icon("tango_icons/edit-copy.png")
                )
                clipboard_copy_path_action.triggered.connect(clipboard_copy)
                self.tree_menu.addAction(clipboard_copy_path_action)
                self.tree_menu.addSeparator()

                # Update CWD
                action_update_cwd = qt.QAction("Update CWD", self.tree_menu)
                action_update_cwd.triggered.connect(update_cwd)
                icon = functions.create_icon("tango_icons/update-cwd.png")
                action_update_cwd.setIcon(icon)
                self.tree_menu.addAction(action_update_cwd)

                if hasattr(item, "is_base") == True:

                    def update_to_parent() -> None:
                        parent_directory = os.path.abspath(
                            os.path.join(item.full_name, os.pardir)
                        )
                        self.main_form.set_cwd(parent_directory)

                    action_update_to_parent = qt.QAction(
                        "Update CWD to parent", self.tree_menu
                    )
                    action_update_to_parent.triggered.connect(update_to_parent)
                    icon = functions.create_icon("tango_icons/update-cwd.png")
                    action_update_to_parent.setIcon(icon)
                    self.tree_menu.addAction(action_update_to_parent)
                    self.tree_menu.addSeparator()

                    def one_dir_up() -> None:
                        def func() -> None:
                            parent_directory = os.path.abspath(
                                os.path.join(item.full_name, os.pardir)
                            )
                            self.main_form.display.show_directory_tree(parent_directory)

                        qt.QTimer.singleShot(250, func)

                    action_one_dir_up = qt.QAction(
                        "One directory up ..", self.tree_menu
                    )
                    action_one_dir_up.triggered.connect(one_dir_up)
                    icon = functions.create_icon("tango_icons/one-dir-up.png")
                    action_one_dir_up.setIcon(icon)
                    self.tree_menu.addAction(action_one_dir_up)
                self.tree_menu.popup(cursor)
            elif hasattr(item, "full_name") == True:

                def open_file() -> None:
                    self.main_form.open_file(item.full_name)

                cursor = qt.QCursor.pos()

                if self.tree_menu is not None:
                    self.tree_menu.setParent(None)
                    self.tree_menu = None

                self.tree_menu = Menu(self)
                # Open in Ex.Co.
                action_open_file = qt.QAction("Open", self.tree_menu)
                action_open_file.triggered.connect(open_file)
                icon = functions.create_icon("tango_icons/document-open.png")
                action_open_file.setIcon(icon)
                self.tree_menu.addAction(action_open_file)

                # Open with system
                def open_system() -> None:
                    try:
                        if data.platform == "Windows":
                            os.startfile(item.full_name)
                        else:
                            subprocess.call(["xdg-open", item.full_name])
                    except:
                        self.main_form.display.repl_display_error(
                            traceback.format_exc()
                        )

                action_open = qt.QAction("Open with system", self.tree_menu)
                action_open.triggered.connect(open_system)
                icon = functions.create_icon("tango_icons/open-with-default-app.png")
                action_open.setIcon(icon)
                self.tree_menu.addAction(action_open)

                # Open in Hex-View
                def open_hex() -> None:
                    if item.attributes.itype == TreeExplorer.ItemType.FILE:
                        file_path = item.attributes.path
                        self.open_file_hex_signal.emit(file_path)  # type: ignore[attr-defined]
                    else:
                        self.main_form.display.repl_display_error(
                            "Item of type '{}' cannot be opened in the Hex-View!".format(
                                item.attributes.itype
                            )
                        )

                action_open_hex = qt.QAction("Open with Hex-View", self.tree_menu)
                action_open_hex.triggered.connect(open_hex)
                icon = functions.create_icon("various/node_template.png")
                action_open_hex.setIcon(icon)
                self.tree_menu.addAction(action_open_hex)

                # Open with Markdown Viewer (only for markdown documents)
                if functions.get_file_type(item.full_name) == "markdown":

                    def open_markdown() -> None:
                        if hasattr(item.attributes, "itype"):
                            if item.attributes.itype == TreeExplorer.ItemType.FILE:
                                file_path = item.attributes.path
                                self.open_file_markdown_signal.emit(file_path)  # type: ignore[attr-defined]
                            else:
                                self.main_form.display.repl_display_error(
                                    "Item of type '{}' cannot be opened in the Markdown Viewer!".format(
                                        item.attributes.itype
                                    )
                                )
                        else:
                            self.open_file_markdown_signal.emit(item.full_name)  # type: ignore[attr-defined]

                    action_open_markdown = qt.QAction(
                        "Open with Markdown Viewer", self.tree_menu
                    )
                    action_open_markdown.triggered.connect(open_markdown)
                    icon = functions.create_icon("tango_icons/markdown.png")
                    action_open_markdown.setIcon(icon)
                    self.tree_menu.addAction(action_open_markdown)

                # Open path in explorer
                open_in_explorer_action = qt.QAction(self.open_in_explorer_text, self)

                def open_in_explorer() -> None:
                    path = item.full_name
                    try:
                        result = functions.open_item_in_explorer(path)
                    except:
                        result = False
                    if result == False:
                        self.main_form.display.repl_display_error(
                            "Error opening path in explorer: {}".format(path)
                        )

                open_in_explorer_action.setIcon(
                    functions.create_icon("tango_icons/document-open.png")
                )
                open_in_explorer_action.triggered.connect(open_in_explorer)
                self.tree_menu.addAction(open_in_explorer_action)

                # Open in terminal
                terminal_path = functions.resolve_terminal_directory(
                    item.full_name, False
                )

                def open_in_terminal() -> None:
                    self.main_form.open_terminal_in_directory(
                        terminal_path, self._parent
                    )

                open_in_terminal_action = qt.QAction("Open in Terminal", self)
                open_in_terminal_action.setIcon(
                    functions.create_icon("tango_icons/utilities-terminal.png")
                )
                open_in_terminal_action.triggered.connect(open_in_terminal)
                self.tree_menu.addAction(open_in_terminal_action)

                # Open in external terminal
                def open_in_external_terminal() -> None:
                    self.main_form.open_external_terminal(terminal_path)

                open_in_external_terminal_action = qt.QAction(
                    "Open in External Terminal", self
                )
                open_in_external_terminal_action.setIcon(
                    functions.create_icon("tango_icons/utilities-terminal.png")
                )
                open_in_external_terminal_action.triggered.connect(
                    open_in_external_terminal
                )
                self.tree_menu.addAction(open_in_external_terminal_action)
                self.tree_menu.addSeparator()

                # Copy name to clipboard
                clipboard_copy_action = qt.QAction("Copy file name to clipboard", self)

                def clipboard_copy() -> None:
                    cb = data.application.clipboard()
                    cb.clear(mode=cb.Mode.Clipboard)
                    cb.setText(item.text(), mode=cb.Mode.Clipboard)

                clipboard_copy_action.setIcon(
                    functions.create_icon("tango_icons/edit-copy.png")
                )
                clipboard_copy_action.triggered.connect(clipboard_copy)
                self.tree_menu.addAction(clipboard_copy_action)
                # Clipboard copy path
                clipboard_copy_path_action = qt.QAction(
                    "Copy file path to clipboard", self
                )

                def clipboard_copy() -> None:
                    cb = data.application.clipboard()
                    cb.clear(mode=cb.Mode.Clipboard)
                    cb.setText(item.full_name, mode=cb.Mode.Clipboard)

                clipboard_copy_path_action.setIcon(
                    functions.create_icon("tango_icons/edit-copy.png")
                )
                clipboard_copy_path_action.triggered.connect(clipboard_copy)
                self.tree_menu.addAction(clipboard_copy_path_action)
                self.tree_menu.addSeparator()

                def update_to_parent() -> None:
                    directory = os.path.dirname(item.full_name)
                    self.main_form.set_cwd(directory)

                action_update_to_parent = qt.QAction("Update CWD", self.tree_menu)
                action_update_to_parent.triggered.connect(update_to_parent)
                icon = functions.create_icon("tango_icons/update-cwd.png")
                action_update_to_parent.setIcon(icon)
                self.tree_menu.addAction(action_update_to_parent)
                self.tree_menu.popup(cursor)

        elif self.tree_display_type == constants.TreeDisplayType.NODES:

            def goto_item() -> None:
                # Parse the node
                self._node_item_parse(item)

            def copy_node_to_clipboard() -> None:
                try:
                    cb = data.application.clipboard()
                    cb.clear(mode=cb.Mode.Clipboard)
                    cb.setText(item_text.split()[0], mode=cb.Mode.Clipboard)
                except:
                    pass

            def open_document() -> None:
                # Focus the bound tab in its parent window
                self.bound_tab._parent.setCurrentWidget(self.bound_tab)

            item = self.model().itemFromIndex(model_index)  # type: ignore[union-attr]
            if item == None:
                return
            item_text = item.text()
            cursor = qt.QCursor.pos()

            if self.tree_menu is not None:
                self.tree_menu.setParent(None)
                self.tree_menu = None

            self.tree_menu = Menu(self)

            show_menu = True
            if hasattr(item, "line_number") == True or "line:" in item_text:
                action_goto_line = qt.QAction("Goto node item", self.tree_menu)
                action_goto_line.triggered.connect(goto_item)
                icon = functions.create_icon("tango_icons/edit-goto.png")
                action_goto_line.setIcon(icon)
                self.tree_menu.addAction(action_goto_line)
                action_copy = qt.QAction("Copy name", self.tree_menu)
                action_copy.triggered.connect(copy_node_to_clipboard)
                icon = functions.create_icon("tango_icons/edit-copy.png")
                action_copy.setIcon(icon)
                self.tree_menu.addAction(action_copy)
            elif "DOCUMENT" in item_text:
                action_open = qt.QAction("Focus document", self.tree_menu)
                action_open.triggered.connect(open_document)
                icon = functions.create_icon("tango_icons/document-open.png")
                action_open.setIcon(icon)
                self.tree_menu.addAction(action_open)
            else:
                show_menu = False

            if show_menu:
                self.tree_menu.popup(cursor)

    def __item_double_click(self, model_index: qt.QModelIndex) -> None:
        """
        Function connected to the doubleClicked signal of the tree display
        """
        # Use the item text according to the tree display type
        if self.tree_display_type == constants.TreeDisplayType.NODES:
            # Get the text of the double clicked item
            item = self.model().itemFromIndex(model_index)  # type: ignore[union-attr]
            self._node_item_parse(item)
        elif self.tree_display_type == constants.TreeDisplayType.FILES:
            # Get the double clicked item
            item = self.model().itemFromIndex(model_index)  # type: ignore[union-attr]
            # Test if the item has the 'full_name' attribute
            if hasattr(item, "is_dir") == True:
                # Expand/collapse the directory node
                if self.isExpanded(item.index()) == True:
                    self.collapse(item.index())
                else:
                    self.expand(item.index())
                return
            elif hasattr(item, "full_name") == True:
                # Open the file
                self.main_form.open_file(file=item.full_name)
        elif self.tree_display_type == constants.TreeDisplayType.FILES_WITH_LINES:
            # Get the double clicked item
            item = self.model().itemFromIndex(model_index)  # type: ignore[union-attr]
            # Test if the item has the 'full_name' attribute
            if hasattr(item, "full_name") == False:
                return
            # Open the file
            self.main_form.open_file(file=item.full_name)
            # Check if a line item was clicked
            if hasattr(item, "line_number") == True:
                # Goto the stored line number
                document = self.main_form.get_tab_by_save_path(item.full_name)
                document.goto_line(item.line_number)

    def _node_item_parse(self, item: qt.QStandardItem) -> None:
        # Check if the bound tab has been cleaned up and has no parent
        if self.bound_tab == None or self.bound_tab._parent == None:
            self.main_form.display.repl_display_message(
                "The bound tab has been closed! Reload the tree display.",
                message_type=constants.MessageType.ERROR,
            )
            return
        # Check the item text
        item_text = item.text()
        if hasattr(item, "line_number") == True:
            # Goto the stored line number
            self.bound_tab._parent.setCurrentWidget(self.bound_tab)
            self.bound_tab.goto_line(item.line_number)  # type: ignore[attr-defined]
        elif "line:" in item_text:
            # Parse the line number out of the item text
            line = item_text.split()[-1]
            start_index = line.index(":") + 1
            end_index = -1
            line_number = int(line[start_index:end_index])
            # Focus the bound tab in its parent window
            self.bound_tab._parent.setCurrentWidget(self.bound_tab)
            # Go to the item line number
            self.bound_tab.goto_line(line_number)
        elif "DOCUMENT" in item_text:
            # Focus the bound tab in its parent window
            self.bound_tab._parent.setCurrentWidget(self.bound_tab)

    def _check_contents(self) -> None:
        # Update the horizontal scrollbar width
        self.resize_horizontal_scrollbar()

    def set_display_type(self, tree_type: constants.TreeDisplayType) -> None:
        """Set the tree display type attribute"""
        self.tree_display_type = tree_type

    def resize_horizontal_scrollbar(self) -> None:
        """
        Resize the header so the horizontal scrollbar will have the correct width
        """
        for i in range(self.model().rowCount()):  # type: ignore[union-attr]
            self.resizeColumnToContents(i)

    def display_python_nodes_in_list(
        self,
        custom_editor: Any,
        import_nodes: list,
        class_nodes: list,
        function_nodes: list,
        global_vars: list,
        parse_error: bool = False,
    ) -> None:
        """Display the input python data in the tree display"""
        # Store the custom editor tab that for quicker navigation
        self.bound_tab = custom_editor
        # Set the tree display type to NODE
        self.set_display_type(constants.TreeDisplayType.NODES)
        # Define the document name, type
        document_name = os.path.basename(custom_editor.save_path)
        document_name_text = "DOCUMENT: {:s}".format(document_name)
        document_type_text = "TYPE: {:s}".format(custom_editor.current_file_type)
        # Define the display structure texts
        import_text = "IMPORTS:"
        class_text = "CLASS/METHOD TREE:"
        function_text = "FUNCTIONS:"
        # Initialize the tree display to Python file type
        self.setSelectionBehavior(qt.QAbstractItemView.SelectionBehavior.SelectRows)
        tree_model = qt.QStandardItemModel()
        tree_model.setHorizontalHeaderLabels([document_name])
        self.clean_model()
        self.setModel(tree_model)
        self.setUniformRowHeights(True)
        # Add the file attributes to the tree display
        description_brush = qt.QBrush(
            qt.QColor(settings.get_theme()["fonts"]["keyword"]["color"])
        )
        description_font = qt.QFont(
            settings.get("current_font_name"),
            settings.get("current_font_size"),
            qt.QFont.Weight.Bold,
        )
        item_document_name = qt.QStandardItem(document_name_text)
        item_document_name.setEditable(False)
        item_document_name.setForeground(description_brush)
        item_document_name.setFont(description_font)
        item_document_type = qt.QStandardItem(document_type_text)
        item_document_type.setEditable(False)
        item_document_type.setForeground(description_brush)
        item_document_type.setFont(description_font)
        item_document_type.setIcon(self.python_icon)
        tree_model.appendRow(item_document_name)
        tree_model.appendRow(item_document_type)
        # Set the label properties
        label_brush = qt.QBrush(
            qt.QColor(settings.get_theme()["fonts"]["singlequotedstring"]["color"])
        )
        label_font = qt.QFont(
            settings.get("current_font_name"),
            settings.get("current_font_size"),
            qt.QFont.Weight.Bold,
        )
        # Check if there was a parsing error
        if parse_error != False:
            error_brush = qt.QBrush(qt.QColor(180, 0, 0))
            error_font = qt.QFont(
                settings.get("current_font_name"),
                settings.get("current_font_size"),
                qt.QFont.Weight.Bold,
            )
            item_error = qt.QStandardItem("ERROR PARSING FILE!")
            item_error.setEditable(False)
            item_error.setForeground(error_brush)
            item_error.setFont(error_font)
            item_error.setIcon(self.get_node_icon("nothing"))
            tree_model.appendRow(item_error)
            # Show the error message
            error_font = settings.get_current_font()
            item_error_msg = qt.QStandardItem(str(parse_error))
            item_error_msg.setEditable(False)
            item_error_msg.setForeground(error_brush)
            item_error_msg.setFont(error_font)
            line_number = int(re.search(r"line (\d+)", str(parse_error)).group(1))  # type: ignore[union-attr]
            item_error_msg.line_number = line_number  # type: ignore[attr-defined]
            tree_model.appendRow(item_error_msg)
            return
        """Imported module filtering"""
        item_imports = qt.QStandardItem(import_text)
        item_imports.setEditable(False)
        item_imports.setForeground(label_brush)
        item_imports.setFont(label_font)
        for node in import_nodes:
            node_text = str(node[0]) + " (line:"
            node_text += str(node[1]) + ")"
            item_import_node = qt.QStandardItem(node_text)
            item_import_node.setEditable(False)
            item_import_node.setIcon(self.get_node_icon("import"))
            item_imports.appendRow(item_import_node)
        if import_nodes == []:
            item_no_imports = qt.QStandardItem("No imports found")
            item_no_imports.setEditable(False)
            item_no_imports.setIcon(self.get_node_icon("nothing"))
            item_imports.appendRow(item_no_imports)
        # Append the import node to the model
        tree_model.appendRow(item_imports)
        if import_nodes == []:
            self.expand(item_imports.index())
        """Class nodes filtering"""
        item_classes = qt.QStandardItem(class_text)
        item_classes.setEditable(False)
        item_classes.setForeground(label_brush)
        item_classes.setFont(label_font)
        # Check deepest nest level and store it
        max_level = 0
        for node in class_nodes:
            for child in node[1]:
                child_level = child[0] + 1
                if child_level > max_level:
                    max_level = child_level
        # Initialize the base level references to the size of the deepest nest level
        base_node_items: list[Optional[qt.QStandardItem]] = [None] * max_level
        base_node_type: list[Optional[int]] = [None] * max_level
        # Create class nodes as tree items
        for node in class_nodes:
            # Construct the parent node
            node_text = str(node[0].name) + " (line:"
            node_text += str(node[0].lineno) + ")"
            parent_tree_node = qt.QStandardItem(node_text)
            parent_tree_node.setEditable(False)
            parent_tree_node.setIcon(self.get_node_icon("class"))
            # Create a list that will hold the child nodes
            child_nodes = []
            # Create base nodes
            # Create the child nodes and add them to list
            for i, child in enumerate(node[1]):
                """!! child_level IS THE INDENTATION LEVEL !!"""
                child_level = child[0]
                child_object = child[1]
                child_text = str(child_object.name) + " (line:"
                child_text += str(child_object.lineno) + ")"
                child_tree_node = qt.QStandardItem(child_text)
                child_tree_node.setEditable(False)
                # Save the base node, its type for adding children to it
                base_node_items[child_level] = child_tree_node
                if isinstance(child_object, ast.ClassDef) == True:
                    base_node_type[child_level] = 0
                elif isinstance(child_object, ast.FunctionDef) == True:
                    base_node_type[child_level] = 1
                # Check if the child is a child of a child.
                if child_level != 0:
                    # Set the child icon
                    if isinstance(child_object, ast.ClassDef) == True:
                        child_tree_node.setIcon(self.get_node_icon("class"))
                    else:
                        # Set method/function icon according to the previous base node type
                        if base_node_type[child_level - 1] == 0:
                            child_tree_node.setIcon(self.get_node_icon("method"))
                        elif base_node_type[child_level - 1] == 1:
                            child_tree_node.setIcon(self.get_node_icon("procedure"))
                    # Determine the parent node level
                    level_retraction = 1
                    parent_level = child_level - level_retraction
                    parent_node = None
                    while parent_node == None and parent_level >= 0:
                        parent_node = base_node_items[parent_level]
                        level_retraction += 1
                        parent_level = child_level - level_retraction
                    # Add the child node to the parent node
                    parent_node.appendRow(child_tree_node)  # type: ignore[union-attr]
                    # Sort the base node children
                    parent_node.sortChildren(0)  # type: ignore[union-attr]
                else:
                    # Set the icon for the
                    if isinstance(child_object, ast.ClassDef) == True:
                        child_tree_node.setIcon(self.get_node_icon("class"))
                    elif isinstance(child_object, ast.FunctionDef) == True:
                        child_tree_node.setIcon(self.get_node_icon("method"))
                    child_nodes.append(child_tree_node)
            # Append the child nodes to the parent and sort them
            for cn in child_nodes:
                parent_tree_node.appendRow(cn)
            parent_tree_node.sortChildren(0)
            # Append the parent to the model and sort them
            item_classes.appendRow(parent_tree_node)
            item_classes.sortChildren(0)
        # Append the class nodes to the model
        tree_model.appendRow(item_classes)
        # Check if there were any nodes found
        if class_nodes == []:
            item_no_classes = qt.QStandardItem("No classes found")
            item_no_classes.setEditable(False)
            item_no_classes.setIcon(self.get_node_icon("nothing"))
            item_classes.appendRow(item_no_classes)
        """Function nodes filtering"""
        item_functions = qt.QStandardItem(function_text)
        item_functions.setEditable(False)
        item_functions.setForeground(label_brush)
        item_functions.setFont(label_font)
        # Create function nodes as tree items
        for func in function_nodes:
            # Set the function node text
            func_text = func.name + " (line:"
            func_text += str(func.lineno) + ")"
            # Construct the node and add it to the tree
            function_node = qt.QStandardItem(func_text)
            function_node.setEditable(False)
            function_node.setIcon(self.get_node_icon("procedure"))
            item_functions.appendRow(function_node)
        item_functions.sortChildren(0)
        # Check if there were any nodes found
        if function_nodes == []:
            item_no_functions = qt.QStandardItem("No functions found")
            item_no_functions.setEditable(False)
            item_no_functions.setIcon(self.get_node_icon("nothing"))
            item_functions.appendRow(item_no_functions)
        # Append the function nodes to the model
        tree_model.appendRow(item_functions)
        # Expand the base nodes
        self.expand(item_classes.index())
        self.expand(item_functions.index())
        # Resize the header so the horizontal scrollbar will have the correct width
        self.resize_horizontal_scrollbar()

    def construct_node(
        self, node: Any, parent_is_class: bool = False
    ) -> qt.QStandardItem:
        # Construct the node text
        node_text = str(node.name) + " (line:"
        node_text += str(node.line_number) + ")"
        tree_node = qt.QStandardItem(node_text)
        tree_node.setEditable(False)
        if node.type == "class":
            tree_node.setIcon(self.get_node_icon("class"))
        elif node.type == "function":
            if parent_is_class == False:
                tree_node.setIcon(self.get_node_icon("procedure"))
            else:
                tree_node.setIcon(self.get_node_icon("method"))
        elif node.type == "global_variable":
            tree_node.setIcon(self.get_node_icon("variable"))
        # Append the children
        node_is_class = False
        if node.type == "class":
            node_is_class = True
        for child_node in node.children:
            tree_node.appendRow(self.construct_node(child_node, node_is_class))
        # Sort the child node alphabetically
        tree_node.sortChildren(0)
        # Return the node
        return tree_node

    def display_python_nodes_in_tree(
        self, custom_editor: Any, python_node_tree: Any, parse_error: bool = False
    ) -> None:
        """Display the input python data in the tree display"""
        # Store the custom editor tab that for quicker navigation
        self.bound_tab = custom_editor
        # Set the tree display type to NODE
        self.set_display_type(constants.TreeDisplayType.NODES)
        # Define the document name, type
        document_name = os.path.basename(custom_editor.save_path)
        document_name_text = "DOCUMENT: {:s}".format(document_name)
        document_type_text = "TYPE: {:s}".format(custom_editor.current_file_type)
        # Define the display structure texts
        import_text = "IMPORTS:"
        global_vars_text = "GLOBALS:"
        class_text = "CLASS/METHOD TREE:"
        function_text = "FUNCTIONS:"
        # Initialize the tree display to Python file type
        self.setSelectionBehavior(qt.QAbstractItemView.SelectionBehavior.SelectRows)
        tree_model = qt.QStandardItemModel()
        #        tree_model.setHorizontalHeaderLabels([document_name])
        self.header().hide()
        self.clean_model()
        self.setModel(tree_model)
        self.setUniformRowHeights(True)
        # Add the file attributes to the tree display
        description_brush = qt.QBrush(
            qt.QColor(settings.get_theme()["fonts"]["keyword"]["color"])
        )
        description_font = qt.QFont(
            settings.get("current_font_name"),
            settings.get("current_font_size"),
            qt.QFont.Weight.Bold,
        )
        item_document_name = qt.QStandardItem(document_name_text)
        item_document_name.setEditable(False)
        item_document_name.setForeground(description_brush)
        item_document_name.setFont(description_font)
        item_document_type = qt.QStandardItem(document_type_text)
        item_document_type.setEditable(False)
        item_document_type.setForeground(description_brush)
        item_document_type.setFont(description_font)
        item_document_type.setIcon(self.python_icon)
        tree_model.appendRow(item_document_name)
        tree_model.appendRow(item_document_type)
        # Set the label properties
        label_brush = qt.QBrush(
            qt.QColor(settings.get_theme()["fonts"]["singlequotedstring"]["color"])
        )
        label_font = qt.QFont(
            settings.get("current_font_name"),
            settings.get("current_font_size"),
            qt.QFont.Weight.Bold,
        )
        # Check if there was a parsing error
        if parse_error != False:
            error_brush = qt.QBrush(qt.QColor(180, 0, 0))
            error_font = qt.QFont(
                settings.get("current_font_name"),
                settings.get("current_font_size"),
                qt.QFont.Weight.Bold,
            )
            item_error = qt.QStandardItem("ERROR PARSING FILE!")
            item_error.setEditable(False)
            item_error.setForeground(error_brush)
            item_error.setFont(error_font)
            item_error.setIcon(self.get_node_icon("nothing"))
            tree_model.appendRow(item_error)
            # Show the error message
            error_font = settings.get_current_font()
            item_error_msg = qt.QStandardItem(str(parse_error))
            item_error_msg.setEditable(False)
            item_error_msg.setForeground(error_brush)
            item_error_msg.setFont(error_font)
            try:
                line_number = int(re.search(r"line (\d+)", str(parse_error)).group(1))  # type: ignore[union-attr]
                item_error_msg.line_number = line_number  # type: ignore[attr-defined]
            except:
                pass
            tree_model.appendRow(item_error_msg)
            return
        # Create the filtered node lists
        import_nodes = [x for x in python_node_tree if x.type == "import"]
        class_nodes = [x for x in python_node_tree if x.type == "class"]
        function_nodes = [x for x in python_node_tree if x.type == "function"]
        globals_nodes = [x for x in python_node_tree if x.type == "global_variable"]
        """Imported module filtering"""
        item_imports = qt.QStandardItem(import_text)
        item_imports.setEditable(False)
        item_imports.setForeground(label_brush)
        item_imports.setFont(label_font)
        for node in import_nodes:
            node_text = str(node.name) + " (line:"
            node_text += str(node.line_number) + ")"
            item_import_node = qt.QStandardItem(node_text)
            item_import_node.setEditable(False)
            item_import_node.setIcon(self.get_node_icon("import"))
            item_imports.appendRow(item_import_node)
        if import_nodes == []:
            item_no_imports = qt.QStandardItem("No imports found")
            item_no_imports.setEditable(False)
            item_no_imports.setIcon(self.get_node_icon("nothing"))
            item_imports.appendRow(item_no_imports)
        # Append the import node to the model
        tree_model.appendRow(item_imports)
        if import_nodes == []:
            self.expand(item_imports.index())
        """Global variable nodes filtering"""
        item_globals = qt.QStandardItem(global_vars_text)
        item_globals.setEditable(False)
        item_globals.setForeground(label_brush)
        item_globals.setFont(label_font)
        # Check if there were any nodes found
        if globals_nodes == []:
            item_no_globals = qt.QStandardItem("No global variables found")
            item_no_globals.setEditable(False)
            item_no_globals.setIcon(self.get_node_icon("nothing"))
            item_globals.appendRow(item_no_globals)
        else:
            # Create the function nodes and add them to the tree
            for node in globals_nodes:
                item_globals.appendRow(self.construct_node(node))
        # Append the function nodes to the model
        tree_model.appendRow(item_globals)
        if globals_nodes == []:
            self.expand(item_globals.index())
        """Class nodes filtering"""
        item_classes = qt.QStandardItem(class_text)
        item_classes.setEditable(False)
        item_classes.setForeground(label_brush)
        item_classes.setFont(label_font)
        # Check if there were any nodes found
        if class_nodes == []:
            item_no_classes = qt.QStandardItem("No classes found")
            item_no_classes.setEditable(False)
            item_no_classes.setIcon(self.get_node_icon("nothing"))
            item_classes.appendRow(item_no_classes)
        else:
            # Create the class nodes and add them to the tree
            for node in class_nodes:
                item_classes.appendRow(self.construct_node(node, True))
        # Append the class nodes to the model
        tree_model.appendRow(item_classes)
        """Function nodes filtering"""
        item_functions = qt.QStandardItem(function_text)
        item_functions.setEditable(False)
        item_functions.setForeground(label_brush)
        item_functions.setFont(label_font)
        # Check if there were any nodes found
        if function_nodes == []:
            item_no_functions = qt.QStandardItem("No functions found")
            item_no_functions.setEditable(False)
            item_no_functions.setIcon(self.get_node_icon("nothing"))
            item_functions.appendRow(item_no_functions)
        else:
            # Create the function nodes and add them to the tree
            for node in function_nodes:
                item_functions.appendRow(self.construct_node(node))
        # Append the function nodes to the model
        tree_model.appendRow(item_functions)
        """Finalization"""
        # Expand the base nodes
        self.expand(item_classes.index())
        self.expand(item_functions.index())
        # Resize the header so the horizontal scrollbar will have the correct width
        self.resize_horizontal_scrollbar()

    def display_nodes(
        self, custom_editor: Any, module: Any, parser_icon: qt.QIcon
    ) -> None:
        """
        Display the input general (Ctags) data in a tree structure
        """
        # Store the custom editor tab that for quicker navigation
        self.bound_tab = custom_editor
        # Set the tree display type to NODE
        self.set_display_type(constants.TreeDisplayType.NODES)
        # Set the label properties
        label_brush = qt.QBrush(
            qt.QColor(settings.get_theme()["fonts"]["singlequotedstring"]["color"])
        )
        label_font = qt.QFont(
            settings.get("current_font_name"),
            settings.get("current_font_size"),
            qt.QFont.Weight.Bold,
        )

        # Filter the nodes
        def display_node(
            tree_node: qt.QStandardItem | qt.QStandardItemModel, c_node: Any
        ) -> None:
            node_group: dict[str, list] = {}
            for v in c_node.children:
                if v.type in node_group.keys():
                    node_group[v.type].append(v)
                else:
                    node_group[v.type] = [v]
            # Initialize a list of struct references for later addition of their members
            item_cache: dict = {}
            node_cache: dict = {}
            # Add The nodes to the tree using the parent tree node
            for k in sorted(node_group.keys()):
                if k == "member":
                    continue
                group_name = k.upper()
                item = qt.QStandardItem("{}:".format(group_name))
                current_list = node_group[k]
                if k in self.node_icons.keys():
                    icon = self.get_node_icon(k)
                else:
                    icon = self.get_node_icon("unknown")
                    self.main_form.display.repl_display_warning(
                        "[TreeDisplay] Unknown node: {}".format(k)
                    )

                item.setEditable(False)
                item.setForeground(label_brush)
                item.setFont(label_font)
                # Create nodes as tree items
                current_list = sorted(current_list, key=lambda x: x.name)
                for n in current_list:
                    node_string = "{}:{}".format(n.type, n.name)
                    if node_string not in node_cache.keys() and n.parent is None:
                        # Set the function node text
                        node_text = n.name + " (line:"
                        node_text += str(n.line_number) + ")"
                        # Construct the node and add it to the tree
                        node = qt.QStandardItem(node_text)
                        node.setEditable(False)
                        node.setIcon(icon)

                        if n.children != []:
                            display_node(node, n)

                        item.appendRow(node)

                        node_cache[node_string] = node

                # Check if there were any nodes found
                #                if current_list == []:
                #                    item_no_nodes = qt.QStandardItem("No items found")
                #                    item_no_nodes.setEditable(False)
                #                    item.appendRow(item_no_nodes)
                # Append the nodes to the parent node
                tree_node.appendRow(item)
                item_cache[k] = item

            # Add the struct members directly to the structs
            for k, v in node_group.items():
                for n in v:
                    if n.parent is None:
                        continue
                    # Set the function node text
                    node_text = n.name + " (line:"
                    node_text += str(n.line_number) + ")"
                    # Construct the node and add it to the tree
                    node = qt.QStandardItem(node_text)
                    node.setEditable(False)
                    node.setIcon(self.get_node_icon(n.type))
                    parent_string = "{}:{}".format(n.parent_type, n.parent)
                    if parent_string not in node_cache.keys():
                        parent_node_text = "{} (undefined)".format(n.parent)
                        parent_node = qt.QStandardItem(parent_node_text)
                        parent_node.setEditable(False)
                        parent_node.setIcon(self.get_node_icon(n.parent_type))
                        node_cache[parent_string] = parent_node
                        parent_type_string = n.parent_type
                        if parent_type_string not in item_cache.keys():
                            item = qt.QStandardItem(
                                "{}:".format(parent_type_string.upper())
                            )
                            item.setEditable(False)
                            item.setForeground(label_brush)
                            item.setFont(label_font)
                            tree_node.appendRow(item)
                            item_cache[parent_type_string] = item
                        item_cache[parent_type_string].appendRow(parent_node)
                    node_cache[parent_string].appendRow(node)

        # Define the document name, type
        document_name = os.path.basename(custom_editor.save_path)
        document_name_text = "DOCUMENT: {:s}".format(document_name)
        document_type_text = "TYPE: {:s}".format(custom_editor.current_file_type)
        document_type_icon = parser_icon
        # Initialize the tree display
        self.setSelectionBehavior(qt.QAbstractItemView.SelectionBehavior.SelectRows)
        tree_model = qt.QStandardItemModel()
        #        tree_model.setHorizontalHeaderLabels([document_name])
        self.header().hide()
        self.clean_model()
        self.setModel(tree_model)
        self.setUniformRowHeights(True)
        # Add the file attributes to the tree display
        description_brush = qt.QBrush(
            qt.QColor(settings.get_theme()["fonts"]["keyword"]["color"])
        )
        description_font = qt.QFont(
            settings.get("current_font_name"),
            settings.get("current_font_size"),
            qt.QFont.Weight.Bold,
        )
        item_document_name = qt.QStandardItem(document_name_text)
        item_document_name.setEditable(False)
        item_document_name.setForeground(description_brush)
        item_document_name.setFont(description_font)
        item_document_type = qt.QStandardItem(document_type_text)
        item_document_type.setEditable(False)
        item_document_type.setForeground(description_brush)
        item_document_type.setFont(description_font)
        item_document_type.setIcon(document_type_icon)
        tree_model.appendRow(item_document_name)
        tree_model.appendRow(item_document_type)
        # Add the items recursively
        display_node(tree_model, module[0])
        # Clean the empty base items
        empty_nodes = [
            i
            for i in range(self.model().rowCount())  # type: ignore[union-attr]
            if not self.model().item(i, 0).hasChildren() and i > 1  # type: ignore[union-attr]
        ]
        empty_nodes.reverse()
        for en in empty_nodes:
            self.model().removeRow(en)  # type: ignore[union-attr]
        # Resize the header so the horizontal scrollbar will have the correct width
        self.resize_horizontal_scrollbar()

    def display_nim_nodes_new(
        self, custom_editor: "CustomEditor", nim_nodes: Dict[str, List[Dict[str, Any]]]
    ) -> None:
        """Display the Nim nodes in a tree structure."""
        # Store the custom editor tab for quicker navigation
        self.bound_tab: "CustomEditor" = custom_editor
        self.set_display_type(constants.TreeDisplayType.NODES)

        # Initialize UI settings
        self.setSelectionBehavior(qt.QAbstractItemView.SelectionBehavior.SelectRows)
        self.setUniformRowHeights(True)
        self.header().hide()

        # Create model and clear previous content
        tree_model: qt.QStandardItemModel = qt.QStandardItemModel()
        self.clean_model()
        self.setModel(tree_model)

        # Cache theme and font settings
        theme: Dict[str, Any] = settings.get_theme()
        font_name: str = settings.get("current_font_name")
        font_size: int = settings.get("current_font_size")

        # Create description styling (reused for header items)
        description_brush: qt.QBrush = qt.QBrush(
            qt.QColor(theme["fonts"]["keyword"]["color"])
        )
        description_font: qt.QFont = qt.QFont(
            font_name, font_size, qt.QFont.Weight.Bold
        )

        # Add document header
        document_name: str = os.path.basename(custom_editor.save_path)
        document_name_text: str = f"DOCUMENT: {document_name}"
        document_type_text: str = f"TYPE: {custom_editor.current_file_type}"

        item_document_name: qt.QStandardItem = qt.QStandardItem(document_name_text)
        item_document_name.setEditable(False)
        item_document_name.setForeground(description_brush)
        item_document_name.setFont(description_font)
        item_document_name.setIcon(self.file_icon)

        item_document_type: qt.QStandardItem = qt.QStandardItem(document_type_text)
        item_document_type.setEditable(False)
        item_document_type.setForeground(description_brush)
        item_document_type.setFont(description_font)
        item_document_type.setIcon(self.nim_icon)

        tree_model.appendRow(item_document_name)
        tree_model.appendRow(item_document_type)

        # Add nodes section if there are any nodes
        if nim_nodes:
            # Create label styling for node categories
            label_brush: qt.QBrush = qt.QBrush(
                qt.QColor(theme["fonts"]["singlequotedstring"]["color"])
            )
            label_font: qt.QFont = qt.QFont(font_name, font_size, qt.QFont.Weight.Bold)

            # Sort node types alphabetically for consistent display
            sorted_node_types: List[str] = sorted(nim_nodes.keys())

            for node_type in sorted_node_types:
                type_nodes: List[Dict[str, Any]] = nim_nodes[node_type]
                if not type_nodes:
                    continue

                # Create parent item for this node type
                parent_item: qt.QStandardItem = qt.QStandardItem(f"{node_type}:")
                parent_item.setEditable(False)
                parent_item.setForeground(label_brush)
                parent_item.setFont(label_font)
                tree_model.appendRow(parent_item)

                # Sort nodes by name (case-insensitive) and add as children
                sorted_nodes: List[Dict[str, Any]] = sorted(
                    type_nodes, key=lambda x: x["name"].lower()
                )

                for node in sorted_nodes:
                    child_item: qt.QStandardItem = qt.QStandardItem(node["name"])
                    child_item.setEditable(False)

                    # Add line number as custom attribute
                    if "line" in node:
                        child_item.line_number = node["line"]  # type: ignore[attr-defined]

                    # Set icon based on node type
                    icon: Optional[qt.QIcon] = self.get_node_icon(node_type)
                    if icon:
                        child_item.setIcon(icon)

                    parent_item.appendRow(child_item)

        # Expand all nodes for better visibility
        self.expandAll()

    def display_nim_nodes(self, custom_editor: Any, nim_nodes: Any) -> None:
        """Display the Nim nodes in a tree structure"""
        # Store the custom editor tab that for quicker navigation
        self.bound_tab = custom_editor
        # Set the tree display type to NODE
        self.set_display_type(constants.TreeDisplayType.NODES)
        # Define the document name, type
        document_name = os.path.basename(custom_editor.save_path)
        document_name_text = "DOCUMENT: {:s}".format(document_name)
        document_type_text = "TYPE: {:s}".format(custom_editor.current_file_type)
        # Initialize the tree display
        self.setSelectionBehavior(qt.QAbstractItemView.SelectionBehavior.SelectRows)
        tree_model = qt.QStandardItemModel()
        self.header().hide()
        self.clean_model()
        self.setModel(tree_model)
        self.setUniformRowHeights(True)
        # Add the file attributes to the tree display
        description_brush = qt.QBrush(
            qt.QColor(settings.get_theme()["fonts"]["keyword"]["color"])
        )
        description_font = qt.QFont(
            settings.get("current_font_name"),
            settings.get("current_font_size"),
            qt.QFont.Weight.Bold,
        )
        item_document_name = qt.QStandardItem(document_name_text)
        item_document_name.setEditable(False)
        item_document_name.setForeground(description_brush)
        item_document_name.setFont(description_font)
        item_document_type = qt.QStandardItem(document_type_text)
        item_document_type.setEditable(False)
        item_document_type.setForeground(description_brush)
        item_document_type.setFont(description_font)
        item_document_type.setIcon(self.nim_icon)
        tree_model.appendRow(item_document_name)
        tree_model.appendRow(item_document_type)
        """Add the nodes"""
        label_brush = qt.QBrush(
            qt.QColor(settings.get_theme()["fonts"]["singlequotedstring"]["color"])
        )
        label_font = qt.QFont(
            settings.get("current_font_name"),
            settings.get("current_font_size"),
            qt.QFont.Weight.Bold,
        )

        # Nested function for creating a tree node
        def create_tree_node(
            node_text: str,
            node_text_brush: qt.QBrush | None,
            node_text_font: qt.QFont | None,
            node_icon: qt.QIcon | None,
            node_line_number: int | None,
        ) -> qt.QStandardItem:
            tree_node = qt.QStandardItem(node_text)
            tree_node.setEditable(False)
            if node_text_brush is not None:
                tree_node.setForeground(node_text_brush)
            if node_text_font is not None:
                tree_node.setFont(node_text_font)
            if node_icon is not None:
                tree_node.setIcon(node_icon)
            if node_line_number is not None:
                tree_node.line_number = node_line_number  # type: ignore[attr-defined]
            return tree_node

        # Nested recursive function for displaying nodes
        def show_nim_node(
            tree: qt.QStandardItem, parent_node: qt.QStandardItem | None, new_node: Any
        ) -> None:
            # Nested function for retrieving the nodes name attribute case insensitively
            def get_case_insensitive_name(item: Any) -> str:
                name = item.name
                return name.lower()

            # Check if parent node is set, else append to the main tree model
            appending_node = parent_node
            if parent_node == None:
                appending_node = tree
            if new_node.imports != []:
                item_imports_node = create_tree_node(
                    "IMPORTS:", label_brush, label_font, None, None
                )
                appending_node.appendRow(item_imports_node)  # type: ignore[union-attr]
                # Sort the list by the name attribute
                new_node.imports.sort(key=get_case_insensitive_name)
                # new_node.imports.sort(key=operator.attrgetter('name'))
                for module in new_node.imports:
                    item_module_node = create_tree_node(
                        module.name,
                        None,
                        None,
                        self.get_node_icon("import"),
                        module.line + 1,
                    )
                    item_imports_node.appendRow(item_module_node)
            if new_node.types != []:
                item_types_node = create_tree_node(
                    "TYPES:", label_brush, label_font, None, None
                )
                appending_node.appendRow(item_types_node)  # type: ignore[union-attr]
                # Sort the list by the name attribute
                new_node.types.sort(key=get_case_insensitive_name)
                for type in new_node.types:
                    item_type_node = create_tree_node(
                        type.name, None, None, self.get_node_icon("type"), type.line + 1
                    )
                    item_types_node.appendRow(item_type_node)
            if new_node.consts != []:
                item_consts_node = create_tree_node(
                    "CONSTANTS:", label_brush, label_font, None, None
                )
                appending_node.appendRow(item_consts_node)  # type: ignore[union-attr]
                # Sort the list by the name attribute
                new_node.consts.sort(key=get_case_insensitive_name)
                for const in new_node.consts:
                    item_const_node = create_tree_node(
                        const.name,
                        None,
                        None,
                        self.get_node_icon("const"),
                        const.line + 1,
                    )
                    item_consts_node.appendRow(item_const_node)
            if new_node.lets != []:
                item_lets_node = create_tree_node(
                    "SINGLE ASSIGNMENT VARIABLES:", label_brush, label_font, None, None
                )
                appending_node.appendRow(item_lets_node)  # type: ignore[union-attr]
                # Sort the list by the name attribute
                new_node.consts.sort(key=get_case_insensitive_name)
                for let in new_node.lets:
                    item_let_node = create_tree_node(
                        let.name, None, None, self.get_node_icon("const"), let.line + 1
                    )
                    item_lets_node.appendRow(item_let_node)
            if new_node.vars != []:
                item_vars_node = create_tree_node(
                    "VARIABLES:", label_brush, label_font, None, None
                )
                appending_node.appendRow(item_vars_node)  # type: ignore[union-attr]
                # Sort the list by the name attribute
                new_node.vars.sort(key=get_case_insensitive_name)
                for var in new_node.vars:
                    item_var_node = create_tree_node(
                        var.name,
                        None,
                        None,
                        self.get_node_icon("variable"),
                        var.line + 1,
                    )
                    item_vars_node.appendRow(item_var_node)
            if new_node.procedures != []:
                item_procs_node = create_tree_node(
                    "PROCEDURES:", label_brush, label_font, None, None
                )
                appending_node.appendRow(item_procs_node)  # type: ignore[union-attr]
                # Sort the list by the name attribute
                new_node.procedures.sort(key=get_case_insensitive_name)
                for proc in new_node.procedures:
                    item_proc_node = create_tree_node(
                        proc.name,
                        None,
                        None,
                        self.get_node_icon("procedure"),
                        proc.line + 1,
                    )
                    item_procs_node.appendRow(item_proc_node)
                    show_nim_node(None, item_proc_node, proc)  # type: ignore[arg-type]
            if new_node.forward_declarations != []:
                item_fds_node = create_tree_node(
                    "FORWARD DECLARATIONS:", label_brush, label_font, None, None
                )
                appending_node.appendRow(item_fds_node)  # type: ignore[union-attr]
                # Sort the list by the name attribute
                new_node.forward_declarations.sort(key=get_case_insensitive_name)
                for proc in new_node.forward_declarations:
                    item_fd_node = create_tree_node(
                        proc.name,
                        None,
                        None,
                        self.get_node_icon("procedure"),
                        proc.line + 1,
                    )
                    item_fds_node.appendRow(item_fd_node)
                    show_nim_node(None, item_fd_node, proc)  # type: ignore[arg-type]
            if new_node.converters != []:
                item_converters_node = create_tree_node(
                    "CONVERTERS:", label_brush, label_font, None, None
                )
                appending_node.appendRow(item_converters_node)  # type: ignore[union-attr]
                # Sort the list by the name attribute
                new_node.converters.sort(key=get_case_insensitive_name)
                for converter in new_node.converters:
                    item_converter_node = create_tree_node(
                        converter.name,
                        None,
                        None,
                        self.get_node_icon("converter"),
                        converter.line + 1,
                    )
                    item_converters_node.appendRow(item_converter_node)
                    show_nim_node(None, item_converter_node, converter)  # type: ignore[arg-type]
            if new_node.iterators != []:
                item_iterators_node = create_tree_node(
                    "ITERATORS:", label_brush, label_font, None, None
                )
                appending_node.appendRow(item_iterators_node)  # type: ignore[union-attr]
                # Sort the list by the name attribute
                new_node.iterators.sort(key=get_case_insensitive_name)
                for iterator in new_node.iterators:
                    item_iterator_node = create_tree_node(
                        iterator.name,
                        None,
                        None,
                        self.get_node_icon("iterator"),
                        iterator.line + 1,
                    )
                    item_iterators_node.appendRow(item_iterator_node)
                    show_nim_node(None, item_iterator_node, iterator)  # type: ignore[arg-type]
            if new_node.methods != []:
                item_methods_node = create_tree_node(
                    "METHODS:", label_brush, label_font, None, None
                )
                appending_node.appendRow(item_methods_node)  # type: ignore[union-attr]
                # Sort the list by the name attribute
                new_node.methods.sort(key=get_case_insensitive_name)
                for method in new_node.methods:
                    item_method_node = create_tree_node(
                        method.name,
                        None,
                        None,
                        self.get_node_icon("method"),
                        method.line + 1,
                    )
                    item_methods_node.appendRow(item_method_node)
                    show_nim_node(None, item_method_node, method)  # type: ignore[arg-type]
            if new_node.properties != []:
                item_properties_node = create_tree_node(
                    "PROPERTIES:", label_brush, label_font, None, None
                )
                appending_node.appendRow(item_properties_node)  # type: ignore[union-attr]
                # Sort the list by the name attribute
                new_node.properties.sort(key=get_case_insensitive_name)
                for property in new_node.properties:
                    item_property_node = create_tree_node(
                        property.name,
                        None,
                        None,
                        self.get_node_icon("method"),
                        property.line + 1,
                    )
                    item_properties_node.appendRow(item_property_node)
                    show_nim_node(None, item_property_node, property)  # type: ignore[arg-type]
            if new_node.macros != []:
                item_macros_node = create_tree_node(
                    "MACROS:", label_brush, label_font, None, None
                )
                appending_node.appendRow(item_macros_node)  # type: ignore[union-attr]
                # Sort the list by the name attribute
                new_node.macros.sort(key=get_case_insensitive_name)
                for macro in new_node.macros:
                    item_macro_node = create_tree_node(
                        macro.name,
                        None,
                        None,
                        self.get_node_icon("macro"),
                        macro.line + 1,
                    )
                    item_macros_node.appendRow(item_macro_node)
                    show_nim_node(None, item_macro_node, macro)  # type: ignore[arg-type]
            if new_node.templates != []:
                item_templates_node = create_tree_node(
                    "TEMPLATES:", label_brush, label_font, None, None
                )
                appending_node.appendRow(item_templates_node)  # type: ignore[union-attr]
                # Sort the list by the name attribute
                new_node.templates.sort(key=get_case_insensitive_name)
                for template in new_node.templates:
                    item_template_node = create_tree_node(
                        template.name,
                        None,
                        None,
                        self.get_node_icon("template"),
                        template.line + 1,
                    )
                    item_templates_node.appendRow(item_template_node)
                    show_nim_node(None, item_template_node, template)  # type: ignore[arg-type]
            if new_node.objects != []:
                item_classes_node = create_tree_node(
                    "OBJECTS:", label_brush, label_font, None, None
                )
                appending_node.appendRow(item_classes_node)  # type: ignore[union-attr]
                # Sort the list by the name attribute
                new_node.objects.sort(key=get_case_insensitive_name)
                for obj in new_node.objects:
                    item_class_node = create_tree_node(
                        obj.name, None, None, self.get_node_icon("class"), obj.line + 1
                    )
                    item_classes_node.appendRow(item_class_node)
                    show_nim_node(None, item_class_node, obj)  # type: ignore[arg-type]
            if new_node.namespaces != []:
                item_namespaces_node = create_tree_node(
                    "NAMESPACES:", label_brush, label_font, None, None
                )
                appending_node.appendRow(item_namespaces_node)  # type: ignore[union-attr]
                # Sort the list by the name attribute
                new_node.namespaces.sort(key=get_case_insensitive_name)
                for namespace in new_node.namespaces:
                    item_namespace_node = create_tree_node(
                        namespace.name,
                        None,
                        None,
                        self.get_node_icon("namespace"),
                        namespace.line + 1,
                    )
                    item_namespaces_node.appendRow(item_namespace_node)
                    show_nim_node(None, item_namespace_node, namespace)  # type: ignore[arg-type]

        show_nim_node(tree_model, None, nim_nodes)  # type: ignore[arg-type]

    def clean_model(self) -> None:
        if self.model() is not None:
            self.model().setParent(None)  # type: ignore[union-attr]
            self.setModel(None)

    def _init_found_files_options(
        self, search_text: str | None, directory: str, custom_text: str | None = None
    ) -> qt.QStandardItemModel:
        # Initialize the tree display to the found files type
        self.horizontalScrollbarAction(1)
        self.setSelectionBehavior(qt.QAbstractItemView.SelectionBehavior.SelectRows)
        tree_model = qt.QStandardItemModel()
        tree_model.setHorizontalHeaderLabels(["FOUND FILES TREE"])
        self.header().hide()
        self.clean_model()
        self.setModel(tree_model)
        self.setUniformRowHeights(True)
        """Define the description details"""
        # Font
        description_brush = qt.QBrush(
            qt.QColor(settings.get_theme()["fonts"]["keyword"]["color"])
        )
        description_font = qt.QFont(
            settings.get("current_font_name"),
            settings.get("current_font_size"),
            qt.QFont.Weight.Bold,
        )
        # Directory item
        item_directory = qt.QStandardItem(
            "BASE DIRECTORY: {:s}".format(directory.replace("\\", "/"))
        )
        item_directory.setEditable(False)
        item_directory.setForeground(description_brush)
        item_directory.setFont(description_font)
        # Search item, display according to the custom text parameter
        if custom_text == None:
            item_search_text = qt.QStandardItem("FILE HAS: {:s}".format(search_text))
        else:
            item_search_text = qt.QStandardItem(custom_text)
        item_search_text.setEditable(False)
        item_search_text.setForeground(description_brush)
        item_search_text.setFont(description_font)
        tree_model.appendRow(item_directory)
        tree_model.appendRow(item_search_text)
        return tree_model

    def _init_replace_in_files_options(
        self, search_text: str, replace_text: str, directory: str
    ) -> qt.QStandardItemModel:
        # Initialize the tree display to the found files type
        self.horizontalScrollbarAction(1)
        self.setSelectionBehavior(qt.QAbstractItemView.SelectionBehavior.SelectRows)
        tree_model = qt.QStandardItemModel()
        tree_model.setHorizontalHeaderLabels(["REPLACED IN FILES TREE"])
        self.header().hide()
        self.clean_model()
        self.setModel(tree_model)
        self.setUniformRowHeights(True)
        """Define the description details"""
        # Font
        description_brush = qt.QBrush(
            qt.QColor(settings.get_theme()["fonts"]["default"]["color"])
        )
        description_font = qt.QFont(
            settings.get("current_font_name"),
            settings.get("current_font_size"),
            qt.QFont.Weight.Bold,
        )
        # Directory item
        item_directory = qt.QStandardItem(
            "BASE DIRECTORY: {:s}".format(directory.replace("\\", "/"))
        )
        item_directory.setEditable(False)
        item_directory.setForeground(description_brush)
        item_directory.setFont(description_font)
        # Search item
        item_search_text = qt.QStandardItem("SEARCH TEXT: {:s}".format(search_text))
        item_search_text.setEditable(False)
        item_search_text.setForeground(description_brush)
        item_search_text.setFont(description_font)
        # Replace item
        item_replace_text = qt.QStandardItem("REPLACE TEXT: {:s}".format(replace_text))
        item_replace_text.setEditable(False)
        item_replace_text.setForeground(description_brush)
        item_replace_text.setFont(description_font)
        tree_model.appendRow(item_directory)
        tree_model.appendRow(item_search_text)
        tree_model.appendRow(item_replace_text)
        return tree_model

    def _sort_item_list(self, items: list, base_directory: str) -> list:
        """
        Helper function for sorting a file/directory list so that
        all of the directories are before any files in the list
        """
        sorted_directories = []
        sorted_files = []
        for item in items:
            _dir = None
            if os.path.isdir(item):
                _dir = item
            else:
                _dir = os.path.dirname(item)
            if not _dir in sorted_directories:
                sorted_directories.append(_dir)
            if os.path.isfile(item):
                sorted_files.append(item)
        # Remove the base directory from the directory list, it is not needed
        if base_directory in sorted_directories:
            sorted_directories.remove(base_directory)
        # Sort the two lists case insensitively
        sorted_directories.sort(key=_sort_key)
        sorted_files.sort(key=_sort_key)
        # Combine the file and directory lists
        sorted_items = sorted_directories + sorted_files
        return sorted_items

    def _add_items_to_tree(
        self, tree_model: qt.QStandardItemModel, directory: str, items: list
    ) -> None:
        """
        Helper function for adding files to a tree view
        """
        label_brush = qt.QBrush(
            qt.QColor(settings.get_theme()["fonts"]["singlequotedstring"]["color"])
        )
        label_font = qt.QFont(
            settings.get("current_font_name"),
            settings.get("current_font_size"),
            qt.QFont.Weight.Bold,
        )
        # Check if any files were found
        if items != []:

            def add_items(
                directory: str,
                items: list,
                cancel_flag: Callable[[], bool] = lambda: False,
            ) -> Optional[tuple[qt.QStandardItem, Directory]]:
                # Set the UNIX file format to the directory
                directory = directory.replace("\\", "/")
                """
                Adding the files
                """
                item_brush = qt.QBrush(
                    qt.QColor(settings.get_theme()["fonts"]["default"]["color"])
                )
                item_font = settings.get_current_font()
                # Create the base directory item that will hold all of the found files
                item_base_directory = qt.QStandardItem(directory)
                item_base_directory.setEditable(False)
                item_base_directory.setForeground(label_brush)
                item_base_directory.setFont(label_font)
                item_base_directory.setIcon(self.folder_icon)
                # Add an indicating attribute that shows the item is a directory.
                # It's a python object, attributes can be added dynamically!
                item_base_directory.is_base = True  # type: ignore[attr-defined]
                item_base_directory.full_name = directory  # type: ignore[attr-defined]
                # Create the base directory object that will hold everything else
                base_directory = Directory(item_base_directory)
                # Create the files that will be added last directly to the base directory
                base_files = {}
                # Sort the the item list so that all of the directories are before the files
                sorted_items = self._sort_item_list(items, directory)
                # Loop through the files while creating the directory tree
                for item_with_path in sorted_items:
                    if cancel_flag():
                        return None

                    if os.path.isfile(item_with_path):
                        file = item_with_path.replace(directory, "")
                        file_name = os.path.basename(file)
                        directory_name = os.path.dirname(file)
                        # Strip the first "/" from the files directory
                        if directory_name.startswith("/"):
                            directory_name = directory_name[1:]
                        # Initialize the file item
                        item_file = qt.QStandardItem(file_name)
                        item_file.setEditable(False)
                        item_file.setForeground(item_brush)
                        item_file.setFont(item_font)
                        file_type = functions.get_file_type(file_name)
                        item_file.setIcon(functions.get_language_file_icon(file_type))  # type: ignore[arg-type]
                        # Add an atribute that will hold the full file name to the QStandartItem.
                        # It's a python object, attributes can be added dynamically!
                        item_file.full_name = item_with_path  # type: ignore[attr-defined]
                        # Check if the file is in the base directory
                        if directory_name == "":
                            # Store the file item for adding to the bottom of the tree
                            base_files[file_name] = item_file
                        else:
                            # Check the previous file items directory structure
                            parsed_directory_list = directory_name.split("/")
                            # Create the new directories
                            current_directory = base_directory
                            for dir in parsed_directory_list:
                                # Check if the current loop directory already exists
                                if dir in current_directory.directories:
                                    current_directory = current_directory.directories[
                                        dir
                                    ]
                            # Add the file to the directory
                            current_directory.add_file(file_name, item_file)
                    else:
                        directory_name = item_with_path.replace(directory, "")
                        # Strip the first "/" from the files directory
                        if directory_name.startswith("/"):
                            directory_name = directory_name[1:]
                        # Check the previous file items directory structure
                        parsed_directory_list = directory_name.split("/")
                        # Create the new directories
                        current_directory = base_directory
                        for dir in parsed_directory_list:
                            if cancel_flag():
                                return None

                            # Check if the current loop directory already exists
                            if dir in current_directory.directories:
                                current_directory = current_directory.directories[dir]
                            else:
                                # Create the new directory item
                                item_new_directory = qt.QStandardItem(dir)
                                item_new_directory.setEditable(False)
                                item_new_directory.setIcon(self.folder_icon)
                                item_new_directory.setForeground(item_brush)
                                item_new_directory.setFont(item_font)
                                # Add an indicating attribute that shows the item is a directory.
                                # It's a python object, attributes can be added dynamically!
                                item_new_directory.is_dir = True  # type: ignore[attr-defined]
                                item_new_directory.full_name = item_with_path  # type: ignore[attr-defined]
                                current_directory = current_directory.add_directory(
                                    dir, item_new_directory
                                )
                # Add the base level files from the stored dictionary, first sort them
                for file_key in sorted(base_files, key=_sort_key):
                    base_directory.add_file(file_key, base_files[file_key])
                return item_base_directory, base_directory

            class ProcessThread(qt.QThread):
                finished = qt.pyqtSignal(object, object)
                stop_flag = False

                def stop(self) -> None:
                    self.stop_flag = True

                def stopped(self) -> bool:
                    return self.stop_flag

                def run(self) -> None:
                    result = add_items(directory, items, self.stopped)
                    if result == None:
                        return None
                    item_base_directory, base_directory = result
                    self.finished.emit(item_base_directory, base_directory)

            @qt.pyqtSlot(object, object)
            def completed(directory_base: Any, base_directory: Any) -> None:
                tree_model.appendRow(directory_base)
                # Check if the TreeDisplay underlying C++ object is alive
                if self._parent is None:
                    return
                # Expand the base directory item
                self.expand(directory_base.index())
                # Resize the header so the horizontal scrollbar will have the correct width
                self.resize_horizontal_scrollbar()
                # Hide the wait animation
                if self._parent is not None:
                    self._parent._set_wait_animation(self._parent.indexOf(self), False)  # type: ignore[attr-defined]

            if self.worker_thread is not None:
                self.worker_thread.wait()
            self.worker_thread = ProcessThread()
            self.worker_thread.setTerminationEnabled(True)
            self.worker_thread.finished.connect(completed)
            self.worker_thread.start()
        else:
            item_no_files_found = qt.QStandardItem("No items found")
            item_no_files_found.setEditable(False)
            item_no_files_found.setIcon(self.get_node_icon("nothing"))
            item_no_files_found.setForeground(label_brush)
            item_no_files_found.setFont(label_font)
            tree_model.appendRow(item_no_files_found)

    def _add_items_with_lines_to_tree(
        self, tree_model: qt.QStandardItemModel, directory: str, items: dict
    ) -> None:
        """Helper function for adding files to a tree view"""
        item_brush = qt.QBrush(
            qt.QColor(settings.get_theme()["fonts"]["default"]["color"])
        )
        item_font = settings.get_current_font()
        # Check if any files were found
        if items != {}:
            # Set the UNIX file format to the directory
            directory = directory.replace("\\", "/")
            """Adding the files"""
            label_brush = qt.QBrush(
                qt.QColor(settings.get_theme()["fonts"]["singlequotedstring"]["color"])
            )
            label_font = qt.QFont(
                settings.get("current_font_name"),
                settings.get("current_font_size"),
                qt.QFont.Weight.Bold,
            )
            # Create the base directory item that will hold all of the found files
            item_base_directory = qt.QStandardItem(directory)
            item_base_directory.setEditable(False)
            item_base_directory.setForeground(label_brush)
            item_base_directory.setFont(label_font)
            item_base_directory.setIcon(self.folder_icon)
            # Create the base directory object that will hold everything else
            base_directory = Directory(item_base_directory)
            # Create the files that will be added last directly to the base directory
            base_files = {}
            # Sort the the item list so that all of the directories are before the files
            items_list = list(items.keys())
            sorted_items = self._sort_item_list(items_list, directory)
            # Loop through the files while creating the directory tree
            for item_with_path in sorted_items:
                if os.path.isfile(item_with_path):
                    file = item_with_path.replace(directory, "")
                    file_name = os.path.basename(file)
                    directory_name = os.path.dirname(file)
                    # Strip the first "/" from the files directory
                    if directory_name.startswith("/"):
                        directory_name = directory_name[1:]
                    # Initialize the file item
                    item_file = qt.QStandardItem(file_name)
                    item_file.setEditable(False)
                    file_type = functions.get_file_type(file_name)
                    item_file.setIcon(functions.get_language_file_icon(file_type))  # type: ignore[arg-type]
                    item_file.setForeground(item_brush)
                    item_file.setFont(item_font)
                    # Add an atribute that will hold the full file name to the QStandartItem.
                    # It's a python object, attributes can be added dynamically!
                    item_file.full_name = item_with_path  # type: ignore[attr-defined]
                    for line in items[item_with_path]:
                        # Adjust the line numbering to Ex.Co. (1 to end)
                        line += 1
                        # Create the goto line item
                        item_line = qt.QStandardItem("line {:d}".format(line))
                        item_line.setEditable(False)
                        item_line.setIcon(self.goto_icon)
                        item_line.setForeground(item_brush)
                        item_line.setFont(item_font)
                        # Add the file name and line number as attributes
                        item_line.full_name = item_with_path  # type: ignore[attr-defined]
                        item_line.line_number = line  # type: ignore[attr-defined]
                        item_file.appendRow(item_line)
                    # Check if the file is in the base directory
                    if directory_name == "":
                        # Store the file item for adding to the bottom of the tree
                        base_files[file_name] = item_file
                    else:
                        # Check the previous file items directory structure
                        parsed_directory_list = directory_name.split("/")
                        # Create the new directories
                        current_directory = base_directory
                        for dir in parsed_directory_list:
                            # Check if the current loop directory already exists
                            if dir in current_directory.directories:
                                current_directory = current_directory.directories[dir]
                        # Add the file to the directory
                        current_directory.add_file(file_name, item_file)
                else:
                    directory_name = item_with_path.replace(directory, "")
                    # Strip the first "/" from the files directory
                    if directory_name.startswith("/"):
                        directory_name = directory_name[1:]
                    # Check the previous file items directory structure
                    parsed_directory_list = directory_name.split("/")
                    # Create the new directories
                    current_directory = base_directory
                    for dir in parsed_directory_list:
                        # Check if the current loop directory already exists
                        if dir in current_directory.directories:
                            current_directory = current_directory.directories[dir]
                        else:
                            # Create the new directory item
                            item_new_directory = qt.QStandardItem(dir)
                            item_new_directory.setEditable(False)
                            item_new_directory.setIcon(self.folder_icon)
                            item_new_directory.setForeground(item_brush)
                            item_new_directory.setFont(item_font)
                            # Add an indicating attribute that shows the item is a directory.
                            # It's a python object, attributes can be added dynamically!
                            item_new_directory.is_dir = True  # type: ignore[attr-defined]
                            current_directory = current_directory.add_directory(
                                dir, item_new_directory
                            )
            # Add the base level files from the stored dictionary, first sort them
            for file_key in sorted(base_files, key=_sort_key):
                base_directory.add_file(file_key, base_files[file_key])
            tree_model.appendRow(item_base_directory)
            # Expand the base directory item
            self.expand(item_base_directory.index())
            # Resize the header so the horizontal scrollbar will have the correct width
            self.resize_horizontal_scrollbar()
        else:
            item_no_files_found = qt.QStandardItem("No items found")
            item_no_files_found.setEditable(False)
            item_no_files_found.setIcon(self.get_node_icon("nothing"))
            item_no_files_found.setForeground(item_brush)
            item_no_files_found.setFont(item_font)
            tree_model.appendRow(item_no_files_found)

    def display_directory_tree(self, directory: str) -> None:
        """
        Display the selected directory in a tree view structure
        """
        # Store the current directory for auto-refresh
        self._current_directory = directory  # type: ignore[assignment]
        # Update the file watcher to watch this directory
        self._refresh_in_progress = True
        watched = self.__file_watcher.directories()
        if watched:
            self.__file_watcher.removePaths(watched)
        if os.path.isdir(directory):
            self.__file_watcher.addPath(directory)
        self._refresh_in_progress = False
        # Set the tree display type to FILES
        self.set_display_type(constants.TreeDisplayType.FILES)
        # Create the walk generator that returns all files/subdirectories
        try:
            walk_generator = os.walk(directory)
        except:
            self.main_form.display.repl_display_message(
                "Invalid directory!", message_type=constants.MessageType.ERROR
            )
            return
        # Initialize and display the search options
        tree_model = self._init_found_files_options(
            None, directory, custom_text="DISPLAYING ALL FILES/SUBDIRECTORIES"
        )

        class ProcessThread(qt.QThread):
            finished = qt.pyqtSignal(list)
            stop_flag = False

            def stop(self) -> None:
                self.stop_flag = True

            def run(self) -> None:
                # Initialize the list that will hold both the directories and files
                found_items = []
                for item in walk_generator:
                    if self.stop_flag:
                        return

                    base_directory = item[0]
                    for _dir in item[1]:
                        found_items.append(
                            os.path.join(base_directory, _dir).replace("\\", "/")
                        )
                    for file in item[2]:
                        found_items.append(
                            os.path.join(base_directory, file).replace("\\", "/")
                        )
                self.finished.emit(found_items)

        def completed(items: list) -> None:
            # Add the items to the treeview
            self._add_items_to_tree(tree_model, directory, items)

        if self.worker_thread is not None:
            self.worker_thread.wait()
        self._parent._set_wait_animation(self._parent.indexOf(self), True)  # type: ignore[attr-defined]
        self.worker_thread = ProcessThread()
        self.worker_thread.setTerminationEnabled(True)
        self.worker_thread.finished.connect(completed)
        self.worker_thread.start()

    def display_found_files(
        self, search_text: str, found_files: list, directory: str
    ) -> None:
        """
        Display files that were found using the 'functions' module's
        find_files function
        """
        # Check if found files are valid
        if found_files == None:
            self.main_form.display.repl_display_message(
                "Error in finding files!", message_type=constants.MessageType.WARNING
            )
            return
        # Set the tree display type to FILES
        self.set_display_type(constants.TreeDisplayType.FILES)
        # Initialize and display the search options
        tree_model = self._init_found_files_options(search_text, directory)
        # Sort the found file list
        found_files.sort(key=_sort_key)
        # Add the items to the treeview
        self._add_items_to_tree(tree_model, directory, found_files)

    def display_found_files_with_lines(
        self,
        search_title: str,
        search_text: str,
        search_dir: str,
        case_sensitive: bool,
        search_subdirs: bool,
        break_on_find: bool,
        file_filter: str,
    ) -> None:
        """
        Display files with lines that were found using the 'functions'
        module's find_in_files function
        """
        # Set the tree display type to NODE
        self.set_display_type(constants.TreeDisplayType.FILES_WITH_LINES)
        # Initialize and display the search options
        tree_model = self._init_found_files_options(search_title, search_dir)

        class ProcessThread(qt.QThread):
            finished = qt.pyqtSignal(dict)
            error = qt.pyqtSignal(str)
            stop_flag = False

            def stop(self) -> None:
                self.stop_flag = True

            def stopped(self) -> bool:
                return self.stop_flag

            def run(self) -> None:
                # Initialize the list that will hold both the directories and files
                found_items = functions.find_files_with_text_enum(
                    search_text,
                    search_dir,
                    case_sensitive,
                    search_subdirs,
                    break_on_find,
                    file_filter,
                    self.stopped,
                )
                if isinstance(found_items, dict):
                    self.finished.emit(found_items)
                else:
                    self.error.emit(found_items)

        def reset() -> None:
            # Resize the header so the horizontal scrollbar will have the correct width
            self.resize_horizontal_scrollbar()
            # Hide the wait animation
            if self._parent is not None:
                self._parent._set_wait_animation(self._parent.indexOf(self), False)  # type: ignore[attr-defined]

        def completed(found_items: dict) -> None:
            # Check if the TreeDisplay underlying C++ object is alive
            if self._parent is None:
                reset()
                return
            # Check of the function return is valid
            if found_items == {}:
                message = "No files found!"
                # Check if any files were found
                self.main_form.display.repl_display_message(
                    message, message_type=constants.MessageType.WARNING
                )
                self.main_form.display.write_to_statusbar(message, 2000)
                # Display error in tree widget
                brush = qt.QBrush(
                    qt.QColor(settings.get_theme()["fonts"]["error"]["color"])
                )
                font = qt.QFont(
                    settings.get("current_font_name"),
                    settings.get("current_font_size"),
                    qt.QFont.Weight.Bold,
                )
                error_item = qt.QStandardItem(message)
                error_item.setEditable(False)
                error_item.setForeground(brush)
                error_item.setFont(font)
                tree_model.appendRow(error_item)
                reset()
                return
            # Add the items with lines to the treeview
            self._add_items_with_lines_to_tree(tree_model, search_dir, found_items)
            reset()

        def error(message: str) -> None:
            try:
                # Check if any files were found
                self.main_form.display.repl_display_error(message)
                self.main_form.display.write_to_statusbar(message, 2000)
                # Display error in tree widget
                brush = qt.QBrush(
                    qt.QColor(settings.get_theme()["fonts"]["error"]["color"])
                )
                font = qt.QFont(
                    settings.get("current_font_name"),
                    settings.get("current_font_size"),
                    qt.QFont.Weight.Bold,
                )
                error_item = qt.QStandardItem(message)
                error_item.setEditable(False)
                error_item.setForeground(brush)
                error_item.setFont(font)
                tree_model.appendRow(error_item)
                reset()
            except:
                pass

        if self.worker_thread is not None:
            self.worker_thread.stop()  # type: ignore[attr-defined]
            self.worker_thread.wait()
        self._parent._set_wait_animation(self._parent.indexOf(self), True)  # type: ignore[attr-defined]
        self.worker_thread = ProcessThread()
        self.worker_thread.setTerminationEnabled(True)
        self.worker_thread.finished.connect(completed)
        self.worker_thread.error.connect(error)
        self.worker_thread.start()

    def display_replacements_in_files(
        self, search_text: str, replace_text: str, replaced_files: dict, directory: str
    ) -> None:
        """
        Display files with lines that were replaces using the 'functions'
        module's replace_text_in_files_enum function
        """
        # Check if found files are valid
        if replaced_files == None:
            self.main_form.display.repl_display_message(
                "Error in finding files!", message_type=constants.MessageType.WARNING
            )
            return
        # Set the tree display type to NODE
        self.set_display_type(constants.TreeDisplayType.FILES_WITH_LINES)
        # Initialize and display the search options
        tree_model = self._init_replace_in_files_options(
            search_text, replace_text, directory
        )
        # Add the items with lines to the treeview
        self._add_items_with_lines_to_tree(tree_model, directory, replaced_files)


if data.platform == "Windows":
    import win32api
    import win32con


class TreeDisplayBase(TreeTabBase):
    """
    Container for a file-explorer style tree tab.

    The tree itself is a TreeViewBase child: it is what receives the key
    releases, the mouse presses and the delegate callbacks, so the event filter
    and the press handler live on the view and reach the tab through the
    references below.
    """

    # Class variables
    _parent: qt.QWidget = None  # type: ignore[assignment]
    main_form: Any = None
    name: str = ""
    savable: constants.CanSave = constants.CanSave.NO  # type: ignore[assignment]
    tree_menu: Any = None
    internals: components.internals.Internals | None = None
    default_menu_font: qt.QFont | None = None

    def __del__(self) -> None:
        try:
            try:
                model = self.model()
                if model:
                    root = model.invisibleRootItem()  # type: ignore[attr-defined]
                    for item in self.iterate_items(root):
                        if item == None:
                            continue
                        item.setData(None)
                        for row in range(item.rowCount()):
                            item.removeRow(row)
                        for col in range(item.columnCount()):
                            item.removeRow(col)
            except:
                pass
            # Clean up the tree model
            try:
                self._clean_model()
            except:
                pass
            # Disconnect signals
            try:
                self.tree.doubleClicked.disconnect()
                self.tree.expanded.disconnect()
            except:
                pass
            self._parent = None  # type: ignore[assignment]
            self.main_form = None
            self.internals = None
            if self.tree_menu is not None:
                self.tree_menu.setParent(None)
                self.tree_menu = None
            # The rows were hidden by the filter, not deleted: un-hide them
            # before the view goes, so a re-attached tab is not blank.
            try:
                self.row_filter.detach()
            except Exception:
                pass
            # Clean up self
            self.setParent(None)
            self.deleteLater()
        except Exception:
            pass

    def __init__(self, parent: qt.QWidget, main_form: Any, name: str) -> None:
        # Initialize the superclass
        super().__init__(parent, main_form, name)
        # Initialize everything else
        self.internals = components.internals.Internals(
            parent=parent, tab_widget=parent
        )
        # Set default font
        self.setFont(settings.get_current_font())
        # The tree, and the filter bar above it
        self.tree = TreeViewBase(self)
        self.tree.main_form = main_form
        self.tree._parent = parent  # type: ignore[assignment]
        self.tree.name = name
        self.tree.key_release_lock = False
        self._assemble("Filter files")
        # The rows are hidden in place, so a model index is a view index
        self.row_filter = components.treefilter.HiddenRowFilter(
            self, self._always_visible_row
        )
        # Set the icon size for every node
        self.update_icon_size()
        # Set the nodes to be animated on expand/contract
        self.tree.setAnimated(True)
        # Disable node expansion on double click
        self.tree.setExpandsOnDoubleClick(False)
        # Install event filter. The key releases arrive at the view, so the
        # filter is installed on the view as well.
        self.tree.installEventFilter(self.tree)
        # Set the item delegate
        self.tree.setItemDelegate(TreeViewBase.CustomItemDelegate())
        # Relay the view's key releases to the tab's own signal
        self.tree.key_release_signal.connect(self.key_release_signal)
        # Presses and key releases are delivered to the view, and both handlers
        # need the tab's references.
        self.tree.key_release_handler = self._on_key_release
        self.tree.pressed_handler = self._on_mouse_pressed
        self.tree.commit_handler = self._on_commit_data
        self.tree.editor_closed_handler = self._on_editor_closed

    def _always_visible_row(self, item: qt.QStandardItem) -> bool:
        """Whether *item* bypasses the filter. Overridden per tree."""
        return False

    def _on_commit_data(self, editor: qt.QWidget) -> None:
        """The view is about to write an editor's text into the model."""
        return None

    def _on_editor_closed(self, editor: qt.QWidget) -> None:
        """The view's editor closed, whether it committed or was reverted."""
        return None

    @qt.pyqtSlot(str, dict)
    def _on_key_release(self, key: str, modifiers: dict[str, bool]) -> None:
        """The view saw a key release. Subclasses act on it."""
        return None

    def _on_mouse_pressed(self, event: qt.QMouseEvent) -> None:
        """The view saw a press. Clear a selection that hit nothing."""
        index = self.tree.indexAt(event.pos())
        if index.isValid() == False:
            self.tree.clearSelection()
        # Set the focus
        self.setFocus()
        # Set the last focused widget to the parent basic widget
        self.main_form.last_focused_widget = self._parent
        # Set Save/SaveAs buttons in the menubar
        self._parent._set_save_status()  # type: ignore[attr-defined]
        # Reset the click&drag context menu action
        components.actionfilter.ActionFilter.clear_action()

    def _lock_key_release(self) -> None:
        self.tree.lock_key_release()  # type: ignore[attr-defined]

    def _unlock_key_release(self) -> None:
        self.tree.unlock_key_release()  # type: ignore[attr-defined]

    """
    Private/Internal functions
    """

    def create_standard_item(
        self,
        text: str,
        bold: bool = False,
        icon: qt.QIcon = None,  # type: ignore[assignment]
    ) -> qt.QStandardItem:
        # Font
        #        brush = qt.QBrush(qt.QColor(settings.get_theme()["fonts"]["keyword"]["color"]))
        font = settings.get_current_font()
        font.setBold(bold)
        # Item initialization
        item = qt.QStandardItem(text)
        item.setEditable(False)
        #        item.setForeground(brush)
        item.setFont(font)
        # Set icon if needed
        if icon is not None:
            item.setIcon(icon)
        return item

    def _create_menu(self) -> Menu:
        self.tree_menu = Menu(self)
        self.default_menu_font = self.tree_menu.font()
        return self.tree_menu

    def _clean_model(self) -> None:
        if self.model() is not None:
            self.model().setParent(None)  # type: ignore[union-attr]
            self.setModel(None)

    def _check_contents(self) -> None:
        # Update the horizontal scrollbar width
        self._resize_horizontal_scrollbar()

    def _resize_horizontal_scrollbar(self) -> None:
        """
        Resize the header so the horizontal scrollbar will have the correct width
        """
        for i in range(self.model().rowCount()):  # type: ignore[union-attr]
            self.resizeColumnToContents(i)

    """
    Overridden functions
    """

    def setFocus(
        self, reason: qt.Qt.FocusReason = qt.Qt.FocusReason.OtherFocusReason
    ) -> None:
        """
        Overridden focus event
        """
        # Execute the supeclass focus function
        super().setFocus(reason)
        # Check indication
        self.main_form.view.indication_check()

    """
    Public functions
    """

    def update_styles(self) -> None:
        self.update_icon_size()
        self.setFont(settings.get_current_font())
        self.update_filter_styles()

    def update_icon_size(self) -> None:
        self.setIconSize(
            functions.create_size(
                settings.get("tree_display_icon_size"),
                settings.get("tree_display_icon_size"),
            )
        )

    def iterate_items(self, root: qt.QStandardItem) -> Iterator[qt.QStandardItem]:
        """
        Iterator that returns all tree items recursively
        """
        if root is not None:
            stack = [root]
            while stack:
                parent = stack.pop(0)
                for row in range(parent.rowCount()):
                    for column in range(parent.columnCount()):
                        child = parent.child(row, column)
                        if child is not None:
                            yield child
                            if child.hasChildren():
                                stack.append(child)


# How many locations the explorer's back and forward stacks remember.
NAV_HISTORY_LIMIT: int = 100


# --- image preview in the tooltip -----------------------------------------
# Hovering an image file shows a thumbnail under the usual metadata. The
# thumbnail is decoded on a worker thread, straight to its target size.
IMAGE_PREVIEW_WIDTH: int = 320
IMAGE_PREVIEW_HEIGHT: int = 240
# Files above this size, and images with more pixels than the second limit
# (a decompression bomb decodes into gigabytes), are not decoded at all.
IMAGE_PREVIEW_MAX_BYTES: int = 64 * 1024 * 1024
IMAGE_PREVIEW_MAX_PIXELS: int = 100_000_000
# Formats worth a preview. The intersection with what Qt can read is used: the
# reader list also holds 'pdf' (it renders a page, which is not a thumbnail of
# the file) and a few formats that are not pictures to anyone.
IMAGE_PREVIEW_SUFFIXES: frozenset[str] = frozenset(
    {
        "png",
        "jpg",
        "jpeg",
        "jfif",
        "gif",
        "bmp",
        "webp",
        "ico",
        "svg",
        "svgz",
        "tif",
        "tiff",
        "tga",
        "icns",
    }
)
_previewable_suffixes: frozenset[str] | None = None


class ImagePreview(NamedTuple):
    """What the tooltip shows of an image.

    *width* and *height* are the image's own size. *png* is the thumbnail, or
    empty when the image is too large to decode (the size is still known).
    """

    width: int
    height: int
    png: bytes


def _is_previewable_image(path: str) -> bool:
    """Whether *path* has the suffix of an image Qt can read and we preview."""
    global _previewable_suffixes
    if _previewable_suffixes is None:
        readable: set[str] = {
            bytes(fmt).decode("ascii", "ignore").lower()
            for fmt in qt.QImageReader.supportedImageFormats()
        }
        _previewable_suffixes = IMAGE_PREVIEW_SUFFIXES & readable
    return os.path.splitext(path)[1].lstrip(".").lower() in _previewable_suffixes


def _build_image_preview(path: str) -> ImagePreview | None:
    """The thumbnail of the image at *path*, or None when it cannot be read.

    Runs on a worker thread, so it deals in QImage and bytes only (a QPixmap
    belongs to the GUI thread). The header gives the size without decoding;
    a larger image is decoded *directly* to the thumbnail size, a smaller one
    is never enlarged, and an EXIF rotation is applied.
    """
    reader: qt.QImageReader = qt.QImageReader(path)
    reader.setAutoTransform(True)
    size: qt.QSize = reader.size()
    if not size.isValid() or size.width() <= 0 or size.height() <= 0:
        return None
    width: int = size.width()
    height: int = size.height()
    transformation: Any = reader.transformation()
    if transformation & qt.QImageIOHandler.Transformation.TransformationRotate90:
        width, height = height, width
    if width * height > IMAGE_PREVIEW_MAX_PIXELS:
        return ImagePreview(width, height, b"")
    if size.width() > IMAGE_PREVIEW_WIDTH or size.height() > IMAGE_PREVIEW_HEIGHT:
        reader.setScaledSize(
            size.scaled(
                IMAGE_PREVIEW_WIDTH,
                IMAGE_PREVIEW_HEIGHT,
                qt.Qt.AspectRatioMode.KeepAspectRatio,
            )
        )
    image: qt.QImage = reader.read()
    if image.isNull():
        return None
    buffer: qt.QBuffer = qt.QBuffer()
    buffer.open(qt.QIODevice.OpenModeFlag.WriteOnly)
    if not image.save(buffer, "PNG"):
        return None
    return ImagePreview(width, height, bytes(buffer.data()))


def _rich_preview_tooltip(text: str, preview: ImagePreview) -> str:
    """The metadata *text* as a rich-text tooltip with the preview under it.

    The text is escaped (a file name may hold '&'), kept on one line per entry
    as the plain tooltip is, and the thumbnail is embedded as a data: URI so
    nothing is read from disk again.
    """
    body: str = html.escape(text).replace("\n", "<br>")
    body += "<br>Dimensions: {} x {}".format(preview.width, preview.height)
    if preview.png:
        body += '<br><img src="data:image/png;base64,{}">'.format(
            base64.b64encode(preview.png).decode("ascii")
        )
    return '<html><div style="white-space: nowrap">{}</div></html>'.format(body)


# Height of the repository line above the footer buttons.
VCS_ROW_HEIGHT: int = 20
# Horizontal padding of the repository label, both sides together (the
# footer stylesheet uses half of it on each side).
VCS_LABEL_PADDING: int = 8


class NavLocation(NamedTuple):
    """Somewhere the explorer can be: a directory, or the drive list.

    ``path`` is None for the Computer (drives) view. ``disk`` is what
    ``display_directory`` needs to rebuild a drive's own listing.
    """

    path: str | None
    disk: bool = False


# Feather glyph per repository-menu entry, keyed by the label prefix that
# StatusSnapshot.copy_entries emits. Separators (None) and any label that does
# not start with a known prefix simply carry no icon.
_VCS_MENU_ICONS: tuple[tuple[str, str], ...] = (
    ("Copy branch name", "git-branch"),
    ("Copy bookmark", "bookmark"),
    ("Copy upstream", "upload-cloud"),
    ("Copy full commit hash", "hash"),
    ("Copy short commit hash", "git-commit"),
    ("Copy tag", "tag"),
    ("Copy repository path", "folder"),
)


def _feather_icon(name: str) -> qt.QIcon:
    """A feather glyph that stays visible on this theme's panel backgrounds

    The chrome (footer bar, menus) is light on the Air theme and dark on every
    other bundled theme, the same split StyleSheetTreeWidget uses for its
    branch chevrons, so Air takes the mid-grey set and the rest the light-grey
    one; the black set would disappear on the dark backgrounds.
    """
    variant: str = (
        "air-grey" if settings.get_theme()["name"] == "Air" else "air-light-grey"
    )
    return functions.create_icon("feather/{}/{}.svg".format(variant, name))


class TreeExplorer(TreeDisplayBase):
    # Item type enumeration
    class ItemType(enum.Enum):
        FILE = enum.auto()
        DIRECTORY = enum.auto()
        BASE_DIRECTORY = enum.auto()
        DISK = enum.auto()
        NEW_FILE = enum.auto()
        NEW_DIRECTORY = enum.auto()
        RENAME_FILE = enum.auto()
        RENAME_DIRECTORY = enum.auto()
        COMPUTER = enum.auto()

    # Signals
    open_file_signal = qt.pyqtSignal(str)
    open_file_hex_signal = qt.pyqtSignal(str)
    open_file_markdown_signal = qt.pyqtSignal(str)
    # A worker-thread directory-size scan finished (path, full tooltip text).
    __tooltip_ready = qt.pyqtSignal(str, object)
    # A worker-thread image thumbnail is ready (path, file signature, preview).
    __preview_ready = qt.pyqtSignal(str, object, object)
    # Instance variables (set in __init__)
    __tooltip_cache: dict[str, str]
    __tooltip_inflight: set[str]
    __tooltip_complete: set[str]
    __tooltip_current: tuple[str, qt.QPoint] | None
    __preview_cache: dict[str, tuple[tuple[int, int], ImagePreview | None]]
    __preview_inflight: set[str]

    # Attributes
    current_viewed_directory: str | None = None
    default_menu_font: qt.QFont | None = None
    base_item: qt.QStandardItem | None = None
    added_item: qt.QStandardItem | None = None
    renamed_item: qt.QStandardItem | None = None
    # The root row doubles as the path of the listing: a press on it opens an
    # editor holding the full path, and a confirmed, readable path points the
    # whole view at that directory. While it is open these fields hold the
    # row, its original label and path and the live editor, so that Escape or
    # a press anywhere else can put everything back exactly as it was.
    editing_root_item: qt.QStandardItem | None = None
    __root_edit_text: str = ""
    __root_edit_path: str = ""
    __root_edit_editor: qt.QLineEdit | None = None
    __root_edit_cancelled: bool = False
    __pending_root_path: str | None = None
    # The cut/copy clipboard is deliberately shared by every explorer tab, so
    # an item cut in one tab can be pasted into another. Only a cut that
    # actually moved something releases it -- the sources are gone by then --
    # while a copy keeps it, so the same selection can be pasted into as many
    # directories as wanted. The same items are published on the system
    # clipboard (see components.osclipboard), which is what lets the OS file
    # manager paste them, and its own copies and cuts are pasted from here.
    cut_items: list[types.SimpleNamespace] | None = None
    copy_items: list[types.SimpleNamespace] | None = None
    open_in_explorer_text: str = "Open in explorer"
    _refresh_in_progress: bool = False
    __last_changed_path: str | None = None
    # Instance variables (set in __init__)
    project_icon: qt.QIcon
    file_icon: qt.QIcon
    folder_icon: qt.QIcon
    disk_icon: qt.QIcon
    computer: qt.QIcon
    goto_icon: qt.QIcon
    directory_changed_timer: qt.QTimer
    vcs_label: qt.QLabel
    vcs_row: qt.QWidget
    vcs_row_layout: qt.QHBoxLayout
    footer_buttons: qt.QWidget
    action_button: qt.QPushButton
    __action_menu: Menu | None = None
    __vcs_menu: Menu | None = None
    nav_back_button: qt.QPushButton
    nav_forward_button: qt.QPushButton
    nav_up_button: qt.QPushButton
    __nav_back: list[NavLocation]
    __nav_forward: list[NavLocation]
    __nav_current: NavLocation | None
    __nav_traversing: bool
    __vcs_repo: components.vcsstatus.RepoInfo | None
    __vcs_key: str | None
    __vcs_snapshot: components.vcsstatus.StatusSnapshot | None
    __vcs_fingerprint: int

    def __init__(self, parent: qt.QWidget, main_form: Any) -> None:
        # Initialize the superclass
        super().__init__(parent, main_form, "Tree Explorer")
        self.setAnimated(True)
        self.setObjectName("TreeExplorer")
        self.setSelectionMode(qt.QAbstractItemView.SelectionMode.ExtendedSelection)
        # Icons
        self.project_icon = functions.create_icon("tango_icons/sessions.png")
        self.file_icon = functions.create_icon("tango_icons/file.png")
        self.folder_icon = functions.create_icon("tango_icons/document-open.png")
        self.disk_icon = functions.create_icon("tango_icons/harddisk.png")
        self.computer = functions.create_icon("tango_icons/computer.png")
        self.goto_icon = functions.create_icon("tango_icons/edit-goto.png")
        # Connect signals
        self.tree.doubleClicked.connect(self.__item_double_click)
        self.key_release_signal.connect(self.__keyrelease_slot)
        # Internals
        self.internals.set_icon(  # type: ignore[union-attr]
            self, functions.create_icon("tango_icons/system-show-cwd-tree-blue.png")
        )
        # File watcher: to watch for displayed directory modifications
        self.__file_watcher = qt.QFileSystemWatcher(self)
        self.__file_watcher.directoryChanged.connect(self.__directory_changed)
        self.directory_changed_timer = qt.QTimer(self)
        self.directory_changed_timer.setInterval(50)
        self.directory_changed_timer.setSingleShot(True)
        self.directory_changed_timer.timeout.connect(self.__directory_process)
        # Tooltips resolve lazily on first hover: the stat is cheap, the
        # recursive directory size runs on a worker thread. The caches are
        # cleared on every listing, so a stale size never survives a refresh.
        self.__tooltip_cache = {}
        self.__tooltip_inflight = set()
        self.__tooltip_complete = set()
        self.__tooltip_current = None
        self.__tooltip_ready.connect(self.on_tooltip_ready)
        # Image thumbnails for the tooltip: decoded on a worker thread, cached
        # per file version, cleared with the tooltips on every listing.
        self.__preview_cache = {}
        self.__preview_inflight = set()
        self.__preview_ready.connect(self.on_preview_ready)
        # Version-control state (git / Mercurial). The shared provider runs
        # the status command off the GUI thread; the rows are decorated by the
        # view's delegate through `_vcs_decoration`, never through the model.
        self.__vcs_repo = None
        self.__vcs_key = None
        self.__vcs_snapshot = None
        self.__vcs_fingerprint = 0
        vcs_provider = components.vcsstatus.provider()
        vcs_provider.status_ready.connect(self.__on_vcs_status)
        vcs_provider.metadata_changed.connect(self.__on_vcs_metadata)
        if data.signal_dispatcher is not None:
            data.signal_dispatcher.editor_file_saved.connect(self.__on_editor_saved)
        # An edit by another program changes nothing a watcher sees, so a
        # visible explorer compares a cheap fingerprint of its directory.
        self.__vcs_poll_timer = qt.QTimer(self)
        self.__vcs_poll_timer.setInterval(components.vcsstatus.POLL_INTERVAL_MS)
        self.__vcs_poll_timer.timeout.connect(self.__vcs_poll)
        self.__vcs_poll_timer.start()
        # Navigation history: where the view has been, and where Back/Forward go
        self.__nav_back = []
        self.__nav_forward = []
        self.__nav_current = None
        self.__nav_traversing = False
        # Create footer toolbar with action buttons (like session editor)
        self._create_footer_toolbar()
        self.__update_nav_buttons()
        # The filter is an on-demand tool: start with the bar hidden.
        self.set_filter_bar_visible(False)

    def _create_footer_toolbar(self) -> None:
        """Create the footer toolbar with action buttons (like session editor)."""
        # The footer is one container (one border-top) holding two rows: the
        # repository line when there is one, and the 28 px row of buttons.
        self.footer = qt.QWidget(self)
        self.footer.setObjectName("TreeExplorerFooter")
        footer_rows = qt.QVBoxLayout(self.footer)
        footer_rows.setContentsMargins(0, 0, 0, 0)
        footer_rows.setSpacing(0)

        # The repository line ('git: main · 7b05e612 · 2M 1A'). On a wide tab it
        # sits at the right end of the button row; on a narrow one it is moved
        # into this row above the buttons (`__place_vcs_label`), so it never
        # takes width from them. The row is hidden whenever the label is not
        # in it, and outside a repository.
        self.vcs_row = qt.QWidget(self.footer)
        self.vcs_row.setObjectName("tree_explorer_vcs_row")
        self.vcs_row.setFixedHeight(VCS_ROW_HEIGHT)
        self.vcs_row.hide()
        self.vcs_row_layout = qt.QHBoxLayout(self.vcs_row)
        self.vcs_row_layout.setContentsMargins(8, 2, 8, 0)
        self.vcs_row_layout.setSpacing(0)
        self.vcs_label = qt.QLabel("", self.vcs_row)
        self.vcs_label.setObjectName("tree_explorer_vcs_label")
        self.vcs_label.hide()
        # Ignored, not Preferred, in *both* places: a QLabel asks for its whole
        # text as a minimum width, which would keep the explorer wide -- and,
        # inline, would stop it from ever getting narrow enough to move the
        # label up. It takes the room that is left and clips (the tooltip and
        # the menu have the full values).
        self.vcs_label.setSizePolicy(
            qt.QSizePolicy.Policy.Ignored, qt.QSizePolicy.Policy.Preferred
        )
        # The tool name is a link that opens the copy menu
        self.vcs_label.setTextInteractionFlags(
            qt.Qt.TextInteractionFlag.LinksAccessibleByMouse
        )
        self.vcs_label.setOpenExternalLinks(False)
        self.vcs_label.linkActivated.connect(self.__on_vcs_link)
        self.vcs_row_layout.addWidget(self.vcs_label)
        footer_rows.addWidget(self.vcs_row)

        # The row of buttons, with a horizontal layout
        self.footer_buttons = qt.QWidget(self.footer)
        self.footer_buttons.setFixedHeight(28)
        footer_rows.addWidget(self.footer_buttons)
        self.footer_layout = qt.QHBoxLayout(self.footer_buttons)
        self.footer_layout.setContentsMargins(8, 2, 8, 2)
        self.footer_layout.setSpacing(components.treefilter.BAR_SPACING)
        # No setAlignment() on this layout, deliberately: a layout with an
        # alignment shrinks to its own size hint, and the repository label (when
        # it is in this row) asks for no width at all (Ignored policy), so it
        # was laid out 0 px wide and the text was missing. The buttons are
        # fixed-size and fill the 24 px row exactly, so there is nothing to
        # align vertically anyway.

        # Navigation: back, forward, up
        self.nav_back_button = self._add_footer_button(
            functions.create_icon("tango_icons/go-previous.png"),
            "Back (Alt+Left)",
            self.navigate_back,
        )
        self.nav_forward_button = self._add_footer_button(
            functions.create_icon("tango_icons/go-next.png"),
            "Forward (Alt+Right)",
            self.navigate_forward,
        )
        self.nav_up_button = self._add_footer_button(
            functions.create_icon("tango_icons/go-up.png"),
            "Up (Alt+Up)",
            self.navigate_up,
        )
        # Separator
        self._make_vline()
        # Actions (new file / new directory) behind one popup button
        self.action_button = self._add_footer_action_button(
            _feather_icon("more-horizontal"),
            "Action",
        )
        # Separator
        self._make_vline()
        # Refresh button
        self._add_footer_button(
            functions.create_icon("tango_icons/view-refresh.png"),
            "Refresh",
            self.refresh,
        )
        # Separator
        self._make_vline()
        # Show/hide the filter bar
        self.filter_toggle = self._add_footer_button(
            functions.create_icon("tango_icons/system-search.png"),
            "Hide the filter field (Ctrl+Alt+F focuses it)",
            self.set_filter_bar_visible,
            checkable=True,
        )

        # The buttons stay packed to the left: this spacer takes the spare width
        # whenever the repository label is not in this row (it is on the line
        # above, or hidden). Inline, the label is added with stretch 1 and so
        # takes it instead -- with no stretch anywhere, a layout of fixed-size
        # widgets spreads them over the whole width.
        self.footer_layout.addStretch(0)

        # Apply theme-aware styling (border-top only, no side margins)
        self._apply_footer_theme(settings.get_theme())

        # Add footer to main layout (after the tree)
        self.main_layout.addWidget(self.footer)

    def _create_footer_button(
        self, icon: qt.QIcon, tooltip: str, checkable: bool = False
    ) -> qt.QPushButton:
        """Build a flat, icon-only button and put it in the footer bar."""
        button = qt.QPushButton(self.footer)
        button.setObjectName("tree_explorer_footer_button")
        button.setIcon(icon)
        button.setToolTip(tooltip)
        button.setFlat(True)
        button.setCheckable(checkable)
        button.setFixedSize(24, 24)
        button.setIconSize(qt.QSize(16, 16))
        self.footer_layout.addWidget(button)
        return button

    def _add_footer_button(
        self,
        icon: qt.QIcon,
        tooltip: str,
        function: Callable[..., Any],
        checkable: bool = False,
    ) -> qt.QPushButton:
        """Add a flat, icon-only action button to the footer bar."""
        button = self._create_footer_button(icon, tooltip, checkable)
        if checkable:
            button.toggled.connect(function)
        else:
            button.clicked.connect(function)
        return button

    def _add_footer_action_button(self, icon: qt.QIcon, tooltip: str) -> qt.QPushButton:
        """Add the footer's Action button: one button that pops up its menu

        The footer sits at the bottom of the tab, so the menu opens upward
        (the same as the repository label's copy menu).
        """
        button = self._create_footer_button(icon, tooltip)
        button.clicked.connect(lambda checked=False: self.__show_action_menu(button))
        return button

    def __displayed_directory(self) -> str | None:
        """The directory the view is listing, or None when it lists none

        Answer it from the model's root row rather than from
        ``current_viewed_directory``: the Computer (drives) view has a root row
        without a path, and that variable still holds the folder the drive
        list was opened from, which is no longer what the view shows.
        """
        attributes: Any = getattr(self.base_item, "attributes", None)
        path: Any = getattr(attributes, "path", None)
        return path if isinstance(path, str) else None

    def __show_action_menu(self, button: qt.QPushButton) -> None:
        """The footer's Action menu: the displayed directory's own actions

        It carries the generic options the directory offers in the tree's
        right-click menu, so they are reachable without right-clicking the
        root row: create a file or a directory, paste, refresh, open the
        folder (file explorer / terminal), copy its path and update the CWD.
        Row-only entries (rename, delete, cut/copy of an item) stay in that
        item's own menu.
        """
        if self.__action_menu is not None:
            self.__action_menu.setParent(None)  # type: ignore[call-overload]
            self.__action_menu.deleteLater()
        menu: Menu = Menu(self)
        self.__action_menu = menu
        new_file_action: qt.QAction = qt.QAction("New file", menu)
        new_file_action.setIcon(functions.create_icon("tango_icons/document-new.png"))
        new_file_action.triggered.connect(self.new_file)
        menu.addAction(new_file_action)
        new_directory_action: qt.QAction = qt.QAction("New directory", menu)
        new_directory_action.setIcon(
            functions.create_icon("tango_icons/folder-new.png")
        )
        new_directory_action.triggered.connect(self.new_directory)
        menu.addAction(new_directory_action)

        directory: str | None = self.__displayed_directory()
        if directory is not None:
            # Paste, only when the clipboard has something to paste into it
            if self.__has_pasteable_items():
                menu.addSeparator()
                paste_action: qt.QAction = qt.QAction("Paste", menu)
                paste_action.setIcon(
                    functions.create_icon("tango_icons/edit-paste.png")
                )
                paste_action.triggered.connect(self.__paste_items)
                menu.addAction(paste_action)

            menu.addSeparator()
            refresh_action: qt.QAction = qt.QAction("Refresh view", menu)
            refresh_action.setIcon(
                functions.create_icon("tango_icons/view-refresh.png")
            )
            refresh_action.triggered.connect(self.refresh)
            menu.addAction(refresh_action)

            def open_in_explorer() -> None:
                try:
                    if data.platform == "Windows":
                        os.startfile(directory)
                    else:
                        subprocess.call(["xdg-open", directory])
                except Exception:
                    self.main_form.display.repl_display_error(traceback.format_exc())

            explorer_action: qt.QAction = qt.QAction(self.open_in_explorer_text, menu)
            explorer_action.setIcon(
                functions.create_icon("tango_icons/document-open.png")
            )
            explorer_action.triggered.connect(open_in_explorer)
            menu.addAction(explorer_action)

            def open_in_terminal() -> None:
                self.main_form.open_terminal_in_directory(directory, self._parent)

            terminal_action: qt.QAction = qt.QAction("Open in Terminal", menu)
            terminal_action.setIcon(
                functions.create_icon("tango_icons/utilities-terminal.png")
            )
            terminal_action.triggered.connect(open_in_terminal)
            menu.addAction(terminal_action)

            def open_in_external_terminal() -> None:
                self.main_form.open_external_terminal(directory)

            external_terminal_action: qt.QAction = qt.QAction(
                "Open in External Terminal", menu
            )
            external_terminal_action.setIcon(
                functions.create_icon("tango_icons/utilities-terminal.png")
            )
            external_terminal_action.triggered.connect(open_in_external_terminal)
            menu.addAction(external_terminal_action)

            menu.addSeparator()

            def copy_path() -> None:
                clipboard = data.application.clipboard()
                clipboard.clear(mode=clipboard.Mode.Clipboard)
                clipboard.setText(directory, mode=clipboard.Mode.Clipboard)
                self.main_form.display.repl_display_message(
                    'Copied to clipboard: "{}"'.format(directory)
                )

            copy_path_action: qt.QAction = qt.QAction(
                "Copy directory path to clipboard", menu
            )
            copy_path_action.setIcon(functions.create_icon("tango_icons/edit-copy.png"))
            copy_path_action.triggered.connect(copy_path)
            menu.addAction(copy_path_action)

            def update_cwd() -> None:
                self.main_form.set_cwd(directory)

            cwd_action: qt.QAction = qt.QAction("Update CWD", menu)
            cwd_action.setIcon(functions.create_icon("tango_icons/update-cwd.png"))
            cwd_action.triggered.connect(update_cwd)
            menu.addAction(cwd_action)

            # The root row's editor: only a listing has one (not the drive list)
            if self.base_item is not None:
                root_item: qt.QStandardItem = self.base_item
                change_directory_action: qt.QAction = qt.QAction(
                    "Change directory", menu
                )
                change_directory_action.setIcon(self.goto_icon)
                change_directory_action.triggered.connect(
                    lambda checked=False: self.__start_root_edit(root_item)
                )
                menu.addAction(change_directory_action)

        origin: qt.QPoint = button.mapToGlobal(qt.QPoint(0, 0))
        origin.setY(origin.y() - menu.sizeHint().height())
        menu.popup(origin)

    def _make_vline(self) -> None:
        """Add a thin vertical separator to the footer bar."""
        line = qt.QWidget(self.footer)
        line.setObjectName("tree_explorer_vline")
        line.setFixedWidth(1)
        self.footer_layout.addWidget(line)

    def _apply_footer_theme(self, theme: dict[str, Any]) -> None:
        """Style the footer bar with the colours of the active theme."""
        background = theme["linemargin"]["background"]
        border = theme["scrollbar"]["handle"]
        button_border = theme["indication"]["passiveborder"]
        hover = theme["indication"]["hover"]
        self.footer.setStyleSheet(
            f"""
#TreeExplorerFooter {{
    background-color: {background};
    border-top: 1px solid {border};
}}
QPushButton#tree_explorer_footer_button {{
    background: transparent;
    border: none;
    padding: 1px 3px;
}}
QPushButton#tree_explorer_footer_button {{
    border: 1px solid {theme["indication"]["passiveborder"]};
}}
QPushButton#tree_explorer_footer_button:disabled {{
    border: 1px solid {theme["scrollbar"]["handle"]};
}}
QPushButton#tree_explorer_footer_button:hover {{
    background: {hover};
}}
QPushButton#tree_explorer_footer_button:checked {{
    background: {hover};
    border: 1px solid {theme["indication"]["activeborder"]};
}}
QWidget#tree_explorer_vline {{
    background-color: {theme["scrollbar"]["handle"]};
    min-width: 1px;
    max-width: 1px;
}}
QLabel#tree_explorer_vcs_label {{
    background: transparent;
    border: none;
    color: {theme["linemargin"]["foreground"]};
    padding: 0px {VCS_LABEL_PADDING // 2}px;
}}
"""
        )
        # A QSS rule cannot colour the anchors of a rich-text label: that is
        # the palette's Link role.
        link_palette: qt.QPalette = self.vcs_label.palette()
        link_palette.setColor(
            qt.QPalette.ColorRole.Link, qt.QColor(theme["indication"]["activeborder"])
        )
        self.vcs_label.setPalette(link_palette)
        # An explicit font, because re-parenting a widget under a stylesheet
        # drops the one it inherited: moved between the rows (`__place_vcs_label`)
        # the label came out as the application default, 9 pt Sans Serif, next to
        # a 10 pt Selawik tab. An explicit font survives the move, and it also
        # keeps `__vcs_label_width` independent of where the label is. This runs
        # on every style update, so a font change is followed.
        self.vcs_label.setFont(self.font())

    def update_styles(self) -> None:
        """Re-apply the theme to the tree and the footer bar."""
        super().update_styles()
        self._apply_footer_theme(settings.get_theme())

    def new_file(self) -> None:
        """Create a new file in the current directory."""
        if not self.base_item:
            return
        create_file_item = self.create_standard_item(
            "", bold=False, icon=self.file_icon
        )
        create_file_item.attributes = self.__create_item_attribute(  # type: ignore[attr-defined]
            TreeExplorer.ItemType.NEW_FILE,
            self.current_viewed_directory,  # type: ignore[arg-type]
        )
        create_file_item.setEditable(True)
        self.base_item.appendRow(create_file_item)
        self.added_item = create_file_item
        index = create_file_item.index()
        self.scrollTo(index)
        self.start_editing_item(index)

    def new_directory(self) -> None:
        """Create a new directory in the current directory."""
        if not self.base_item:
            return
        create_directory_item = self.create_standard_item(
            "", bold=False, icon=self.folder_icon
        )
        create_directory_item.attributes = self.__create_item_attribute(  # type: ignore[attr-defined]
            TreeExplorer.ItemType.NEW_DIRECTORY,
            self.current_viewed_directory,  # type: ignore[arg-type]
        )
        create_directory_item.setEditable(True)
        self.base_item.appendRow(create_directory_item)
        self.added_item = create_directory_item
        index = create_directory_item.index()
        self.scrollTo(index)
        self.start_editing_item(index)

    def _always_visible_row(self, item: qt.QStandardItem) -> bool:
        """
        The rows the filter must never hide.

        The drive rows on the Windows view are the only way into a disk, and a
        filter that hid them would strand the user. The rows being created or
        renamed are on screen for the user to type into, so they stay too.
        (There is no '..' row to protect any more: leaving a directory is the
        footer's Up button, which no filter can touch.)

        The base directory row is deliberately *not* in the list. It is the one
        top-level row of a listing rather than a row among siblings, and an
        exempt row takes its whole subtree with it - exempting it would leave
        the filter with nothing to do. It stays by the ordinary rule: while a
        descendant matches.
        """
        if not hasattr(item, "attributes"):
            return False
        itype = getattr(item.attributes, "itype", None)
        if itype is None:
            return False
        return itype in (
            TreeExplorer.ItemType.DISK,
            TreeExplorer.ItemType.COMPUTER,
            TreeExplorer.ItemType.NEW_FILE,
            TreeExplorer.ItemType.NEW_DIRECTORY,
            TreeExplorer.ItemType.RENAME_FILE,
            TreeExplorer.ItemType.RENAME_DIRECTORY,
        )

    @qt.pyqtSlot(str)
    def __directory_changed(self, path: str) -> None:
        if self._refresh_in_progress:
            return
        self.__last_changed_path = path
        self.directory_changed_timer.start(100)

    def __directory_process(self) -> None:
        if self.__last_changed_path is not None:
            self.display_directory(self.__last_changed_path, scroll_restore=True)

    @qt.pyqtSlot(str, dict)
    def __keyrelease_slot(self, key: str, modifiers: dict[str, bool]) -> None:
        # Copy
        if key == "Key_C" and modifiers["control"] == True:
            self.__copy_items()

        # Cut
        if key == "Key_X" and modifiers["control"] == True:
            self.__cut_items()

        # Paste
        if key == "Key_V" and modifiers["control"] == True:
            self.__paste_items()

        # delete
        if key == "Key_Delete":
            self.__delete_items()

        # Navigation history
        if modifiers["alt"] == True:
            if key == "Key_Left":
                self.navigate_back()
            elif key == "Key_Right":
                self.navigate_forward()
            elif key == "Key_Up":
                self.navigate_up()

    def __init_tree_model(self) -> qt.QStandardItemModel:
        self.horizontalScrollbarAction(1)
        self.setSelectionBehavior(qt.QAbstractItemView.SelectionBehavior.SelectRows)
        tree_model: qt.QStandardItemModel = qt.QStandardItemModel()
        tree_model.setHorizontalHeaderLabels(["TREE FILE EXPLORER"])
        self.header().hide()
        self._clean_model()
        self.setModel(tree_model)
        self.setUniformRowHeights(True)
        return tree_model

    def __create_item_attribute(
        self,
        itype: "TreeExplorer.ItemType",
        path: str,
        hidden: bool = False,
        disk: bool = False,
        hide_menu: bool = False,
    ) -> types.SimpleNamespace:
        return types.SimpleNamespace(
            itype=itype, path=path, hidden=hidden, disk=disk, hide_menu=hide_menu
        )

    def __is_hidden_item(self, path: str) -> bool:
        try:
            if data.platform == "Windows":
                attribute: int = win32api.GetFileAttributes(path)
                hidden: bool = bool(
                    attribute
                    & (win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM)
                )
            else:
                hidden = os.path.basename(path).startswith(".")
            return hidden
        except:
            return False

    def start_editing_item(self, index: qt.QModelIndex) -> None:
        self._lock_key_release()
        self.edit(index)

    def _on_commit_data(self, editor: qt.QWidget) -> None:
        self.__commit_data(editor)

    def _on_editor_closed(self, editor: qt.QWidget) -> None:
        self.__item_editing_closed(editor)

    def __commit_data(self, editor: qt.QWidget) -> None:
        searched_item: str = editor.text()  # type: ignore[attr-defined]
        root: qt.QStandardItem = self.model().invisibleRootItem()  # type: ignore[union-attr]
        for it in self.iterate_items(root):
            if it is None or not hasattr(it, "attributes"):
                continue
            if (
                it.text() == searched_item
                and it.attributes.itype == TreeExplorer.ItemType.FILE
            ):
                self.setCurrentIndex(it.index())
                break
            elif (
                it.text() == searched_item
                and it.attributes.itype == TreeExplorer.ItemType.DIRECTORY
            ):
                self.setCurrentIndex(it.index())
                break

    def __item_editing_closed(self, widget: qt.QWidget) -> None:
        """
        Signal that fires when editing was canceled/ended
        """
        # Check if the directory name is valid
        if self.added_item is not None and self.added_item.text() == "":
            self.base_item.removeRow(self.added_item.row())  # type: ignore[union-attr]
            self.added_item = None
        elif self.renamed_item is not None:
            # Reset item type back to original when cancelling rename
            if (
                self.renamed_item.attributes.itype  # type: ignore[attr-defined]
                == TreeExplorer.ItemType.RENAME_DIRECTORY
            ):
                self.renamed_item.attributes.itype = TreeExplorer.ItemType.DIRECTORY  # type: ignore[attr-defined]
            else:
                self.renamed_item.attributes.itype = TreeExplorer.ItemType.FILE  # type: ignore[attr-defined]
            self.renamed_item = None
        if self.editing_root_item is not None:
            self.__reset_root_edit()
        self._unlock_key_release()

    """
    Root row editing

    The root row is the path of the listing, so it is the one editable row
    that is not renamed on disk: a confirmed path points the whole view at
    another directory. Only Enter confirms; Escape, or a press anywhere off
    the editor, restores the row and leaves the listing alone.
    """

    def __is_root_item(self, item: qt.QStandardItem | None) -> bool:
        """Whether *item* is the top row built for the viewed directory."""
        if item is None or self.base_item is None:
            return False
        attributes = getattr(item, "attributes", None)
        if attributes is None:
            return False
        if attributes.itype not in (
            TreeExplorer.ItemType.BASE_DIRECTORY,
            TreeExplorer.ItemType.DISK,
        ):
            return False
        if item is self.base_item:
            return True
        try:
            return item.index() == self.base_item.index()
        except RuntimeError:
            return False

    def __path_key(self, path: str) -> str:
        """A comparable form of *path*, so 'D:' and 'D:/' are the same root."""
        normalised: str = os.path.normcase(os.path.normpath(path))
        if os.name == "nt" and normalised.endswith(":"):
            normalised += "\\"
        return normalised

    def __resolve_root_path(self, entered: str) -> str:
        """Turn what the user typed into a display path, or '' when empty."""
        text_value: str = entered.strip()
        if (
            len(text_value) >= 2
            and text_value[0] == text_value[-1]
            and text_value[0] in ('"', "'")
        ):
            text_value = text_value[1:-1].strip()
        if text_value == "":
            return ""
        text_value = os.path.expandvars(os.path.expanduser(text_value))
        if not os.path.isabs(text_value):
            base: str = self.current_viewed_directory or os.getcwd()
            text_value = os.path.join(base, text_value)
        display: str = functions.unixify_path(os.path.normpath(text_value))
        if os.name == "nt" and display.endswith(":"):
            display += "/"
        return display

    def __restore_root_text(self) -> None:
        """Put the original label back without treating it as a new path."""
        item: qt.QStandardItem | None = self.editing_root_item
        if item is None:
            return
        cancelled: bool = self.__root_edit_cancelled
        self.__root_edit_cancelled = True
        try:
            item.setText(self.__root_edit_text)
        except RuntimeError:
            pass
        finally:
            self.__root_edit_cancelled = cancelled

    def __reset_root_edit(self) -> None:
        """End the root edit and release everything it installed."""
        item: qt.QStandardItem | None = self.editing_root_item
        self.editing_root_item = None
        self.__root_edit_editor = None
        self.__root_edit_cancelled = False
        if item is not None:
            try:
                item.setEditable(False)
            except RuntimeError:
                pass
        self._unlock_key_release()
        application: qt.QCoreApplication | None = qt.QApplication.instance()
        if application is not None:
            application.removeEventFilter(self)

    def __active_editor(self) -> qt.QLineEdit | None:
        """
        The editor the view is using right now.

        A closed editor is cached rather than destroyed, so a plain child
        lookup can hand back a hidden editor from the previous edit; the live
        one is the child that was not hidden.
        """
        viewport: qt.QWidget | None = self.tree.viewport()
        if viewport is None:
            return None
        for candidate in viewport.findChildren(qt.QLineEdit):
            if not candidate.isHidden():
                return candidate
        return None

    def __start_root_edit(self, item: qt.QStandardItem) -> None:
        """Make the root row editable, pre-filled with the viewed path."""
        if self.editing_root_item is not None or self.added_item is not None:
            return
        attributes = getattr(item, "attributes", None)
        path = getattr(attributes, "path", None)
        if not isinstance(path, str):
            return
        self.__root_edit_text = item.text()
        self.__root_edit_path = path
        self.__root_edit_cancelled = False
        item.setEditable(True)
        self.editing_root_item = item
        self.start_editing_item(item.index())
        editor: qt.QLineEdit | None = self.__active_editor()
        if editor is None:
            self.__reset_root_edit()
            return
        self.__root_edit_editor = editor
        editor.selectAll()
        application: qt.QCoreApplication | None = qt.QApplication.instance()
        if application is not None:
            application.installEventFilter(self)

    def __cancel_root_edit(self) -> None:
        """Close the root editor without committing anything."""
        if self.editing_root_item is None:
            return
        self.__root_edit_cancelled = True
        editor: qt.QLineEdit | None = self.__root_edit_editor
        if editor is None:
            self.__reset_root_edit()
            return
        self.tree.closeEditor(
            editor, qt.QAbstractItemDelegate.EndEditHint.RevertModelCache
        )

    def __commit_root_edit(self, item: qt.QStandardItem) -> None:
        """Act on the path typed into the root row."""
        entered: str = item.text()
        resolved: str = self.__resolve_root_path(entered)
        if resolved == "":
            self.__report_root_error(entered)
            self.__restore_root_text()
            return
        if self.__path_key(resolved) == self.__path_key(self.__root_edit_path):
            self.__restore_root_text()
            return
        readable: bool = False
        try:
            readable = os.path.isdir(resolved)
        except OSError:
            readable = False
        if not readable:
            self.__report_root_error(entered)
            self.__restore_root_text()
            return
        # The listing is rebuilt by the event loop: rebuilding it here would
        # free the model item Qt is still writing into (see AGENTS.md).
        self.__restore_root_text()
        self.__pending_root_path = resolved
        qt.QTimer.singleShot(0, self.__apply_pending_root)

    def __report_root_error(self, entered: str) -> None:
        """Report a path the view cannot show."""
        self.main_form.display.repl_display_error(
            "Cannot change root directory: '{}' is not a readable directory!".format(
                entered
            )
        )
        self.main_form.display.write_to_statusbar("Cannot change root directory!", 3000)

    def __apply_pending_root(self) -> None:
        path: str | None = self.__pending_root_path
        self.__pending_root_path = None
        if path is None:
            return
        self.display_directory(path)

    def __root_item_pressed(self, event: qt.QMouseEvent) -> None:
        """A left press on the root row opens the path editor."""
        if self.editing_root_item is not None:
            return
        index: qt.QModelIndex = self.indexAt(event.pos())
        if not index.isValid():
            return
        model: qt.QAbstractItemModel | None = self.model()
        if model is None or not isinstance(model, qt.QStandardItemModel):
            return
        item: qt.QStandardItem | None = model.itemFromIndex(index)
        if item is None or not self.__is_root_item(item):
            return
        # The branch indicator sits in the indentation band left of the row's
        # own rect: a press there belongs to the expander, not the editor.
        rect: qt.QRect = self.visualRect(index)
        if event.pos().x() < rect.left():
            return
        self.__start_root_edit(item)

    def eventFilter(self, object: qt.QObject, event: qt.QEvent) -> bool:  # type: ignore[override]
        """
        Cancels the root edit on any press that is not on its editor.

        A click elsewhere takes the focus from the editor, and the view would
        then commit the typed text; cancelling first is what keeps "click
        outside" from navigating anywhere.
        """
        if (
            self.editing_root_item is not None
            and event.type() == qt.QEvent.Type.MouseButtonPress
        ):
            editor: qt.QLineEdit | None = self.__root_edit_editor
            target: qt.QWidget | None = (
                object if isinstance(object, qt.QWidget) else None
            )
            try:
                off_editor: bool = (
                    target is None
                    or editor is None
                    or (target is not editor and not editor.isAncestorOf(target))
                )
            except RuntimeError:
                off_editor = True
            if off_editor:
                self.__cancel_root_edit()
        return False

    def _safely_remove_row(self, item: qt.QStandardItem) -> bool:
        parent: qt.QStandardItem | None = item.parent()
        if parent is None:
            return False
        row: int = item.row()
        if row < 0 or row >= parent.rowCount():
            return False
        parent.removeRow(row)
        return True

    def __item_changed(self, item: qt.QStandardItem, role: int = -1) -> None:
        """
        Callback connected to the displays
        QStandardItemModel 'itemChanged' signal
        """
        # Hiding a row is a filter decision, not an edit. This handler is
        # connected to the source model, so it sees every write the filter
        # makes. It cannot recognise them from the role argument - PyQt6 hands
        # an itemChanged slot a role of -1 whatever changed - so it asks the
        # filter whether it is inside its own write.
        if self.row_filter.is_applying:
            return
        if not hasattr(item, "attributes"):
            return
        if self.editing_root_item is not None and self.__is_root_item(item):
            # A root edit is confirmed by Enter (the text is already the new
            # path); anything that merely restores the old label is ignored.
            if not self.__root_edit_cancelled:
                self.__commit_root_edit(item)
            return
        if (
            item.attributes.itype == TreeExplorer.ItemType.RENAME_FILE
            or item.attributes.itype == TreeExplorer.ItemType.RENAME_DIRECTORY
        ):
            # Reset the type first
            if item.attributes.itype == TreeExplorer.ItemType.RENAME_DIRECTORY:
                item.attributes.itype = TreeExplorer.ItemType.DIRECTORY
                item_text: str = "Directory"
            else:
                item.attributes.itype = TreeExplorer.ItemType.FILE
                item_text = "File"
            # Initialize the names
            old_name: str = item.attributes.path
            new_name: str = os.path.join(
                os.path.dirname(item.attributes.path), item.text()
            )
            # Check if the names are different
            old_name = functions.unixify_path_keep_symlink(old_name)
            new_name = functions.unixify_path_keep_symlink(new_name)
            if old_name == new_name:
                return
            # Check if an item with the same name as the
            # renamed item already exists
            item.setEditable(False)
            if os.path.exists(new_name):
                self.main_form.display.repl_display_message(
                    "{} '{}' already exits!".format(item_text, new_name),
                    message_type=constants.MessageType.ERROR,
                )
                self.display_directory(
                    self.current_viewed_directory,  # type: ignore[arg-type]
                    scroll_restore=False,
                )
                return
            # Rename the item
            try:
                os.rename(old_name, new_name)
                item.attributes.path = new_name
                self.main_form.display.repl_display_success(
                    "Renamed {}:\n    '{}'\n  to:\n    '{}'!".format(
                        item_text.lower(), old_name, new_name
                    )
                )
            except:
                self.main_form.display.repl_display_error(traceback.format_exc())
                self.main_form.display.repl_display_error(
                    "Error while renaming {}: '{}'!".format(
                        item_text.lower(), item.attributes.path
                    )
                )
                self.display_directory(
                    self.current_viewed_directory,  # type: ignore[arg-type]
                    scroll_restore=False,
                )
                return
            # Finish editing and reset the view
            self.renamed_item = None

        elif (
            item.attributes.itype == TreeExplorer.ItemType.NEW_DIRECTORY
            or item.attributes.itype == TreeExplorer.ItemType.NEW_FILE
        ):
            path: str = os.path.join(item.attributes.path, item.text())
            item.attributes.path = functions.unixify_path_keep_symlink(path)
            if item.attributes.itype == TreeExplorer.ItemType.NEW_DIRECTORY:
                item.attributes.itype = TreeExplorer.ItemType.DIRECTORY
                item_text = "Directory"
            else:
                item.attributes.itype = TreeExplorer.ItemType.FILE
                item_text = "File"
            if os.path.exists(item.attributes.path):
                self._safely_remove_row(item)
                self.main_form.display.repl_display_message(
                    "{} '{}' already exits!".format(item_text, item.attributes.path),
                    message_type=constants.MessageType.ERROR,
                )
                return
            # Create the directory
            try:
                if item.attributes.itype == TreeExplorer.ItemType.DIRECTORY:
                    os.mkdir(item.attributes.path)
                else:
                    open(item.attributes.path, "a").close()
                self.main_form.display.repl_display_message(
                    "Created {}: '{}'!".format(item_text.lower(), item.attributes.path),
                    message_type=constants.MessageType.SUCCESS,
                )
            except:
                self._safely_remove_row(item)
                self.main_form.display.repl_display_message(
                    "Error while creating {}: '{}'!".format(
                        item_text.lower(), item.attributes.path
                    ),
                    message_type=constants.MessageType.ERROR,
                )
                return
            # Finish editing and reset the view
            item.setEditable(False)
            self.added_item = None

    def refresh(self) -> bool:
        return self.display_directory(
            self.current_viewed_directory,  # type: ignore[arg-type]
            scroll_restore=False,
        )

    def __item_right_click(self, model_index: qt.QModelIndex) -> None:
        item: qt.QStandardItem | None = self.model().itemFromIndex(model_index)  # type: ignore[union-attr]
        cursor: qt.QPoint = qt.QCursor.pos()
        # Clean up the menu if needed
        if self.tree_menu is not None:
            self.tree_menu.setParent(None)
            self.tree_menu.deleteLater()
        # Initialize the menu
        self.tree_menu = Menu(self)
        self.default_menu_font = self.tree_menu.font()

        # First check if the click was in an empty space
        # and create item actions accordingly
        if item is not None:
            if hasattr(item, "attributes") == False:
                return
            elif item.attributes.hide_menu == True:  # type: ignore[attr-defined]
                return

            # Open the current item
            def open_item() -> None:
                self.open_item(item)

            title: str = "Open directory"
            icon: qt.QIcon = "tango_icons/document-open.png"  # type: ignore[assignment]
            if item.attributes.itype == TreeExplorer.ItemType.FILE:  # type: ignore[attr-defined]
                title = "Open file"
            open_action: qt.QAction = qt.QAction(title, self.tree_menu)
            open_action.triggered.connect(open_item)
            icon = functions.create_icon(icon)  # type: ignore[arg-type]
            open_action.setIcon(icon)
            if item.attributes.itype in [  # type: ignore[attr-defined]
                TreeExplorer.ItemType.FILE,
                TreeExplorer.ItemType.DIRECTORY,
                TreeExplorer.ItemType.BASE_DIRECTORY,
                TreeExplorer.ItemType.DISK,
            ]:
                self.tree_menu.addAction(open_action)

            # The root row is also the path of the listing: offer the same
            # path editor a left press opens, right below "Open directory".
            if self.__is_root_item(item):

                def change_directory() -> None:
                    self.__start_root_edit(item)

                change_directory_action = qt.QAction("Change directory", self.tree_menu)
                change_directory_action.setIcon(self.goto_icon)
                change_directory_action.triggered.connect(change_directory)
                self.tree_menu.addAction(change_directory_action)

            # Open with system
            def open_system() -> None:
                try:
                    if data.platform == "Windows":
                        os.startfile(item.attributes.path)  # type: ignore[attr-defined]
                    else:
                        subprocess.call(["xdg-open", item.attributes.path])  # type: ignore[attr-defined]
                except:
                    self.main_form.display.repl_display_error(traceback.format_exc())

            # Open with system
            if item.attributes.itype == TreeExplorer.ItemType.FILE:  # type: ignore[attr-defined]
                action_open_system = qt.QAction("Open with system", self.tree_menu)
                action_open_system.triggered.connect(open_system)
                icon = functions.create_icon("tango_icons/open-with-default-app.png")
                action_open_system.setIcon(icon)
                self.tree_menu.addAction(action_open_system)

                # Open with Hex-View
                def open_hex() -> None:
                    if item.attributes.itype == TreeExplorer.ItemType.FILE:  # type: ignore[attr-defined]
                        file_path = item.attributes.path  # type: ignore[attr-defined]
                        self.open_file_hex_signal.emit(file_path)
                    else:
                        self.main_form.display.repl_display_error(
                            "Item of type '{}' cannot be opened in the Hex-View!".format(
                                item.attributes.itype  # type: ignore[attr-defined]
                            )
                        )

                action_open_hex = qt.QAction("Open with Hex-View", self.tree_menu)
                action_open_hex.triggered.connect(open_hex)
                icon = functions.create_icon("various/node_template.png")
                action_open_hex.setIcon(icon)
                self.tree_menu.addAction(action_open_hex)

                # Open with Markdown Viewer (only for markdown documents)
                if functions.get_file_type(item.attributes.path) == "markdown":  # type: ignore[attr-defined]

                    def open_markdown() -> None:
                        file_path = item.attributes.path  # type: ignore[attr-defined]
                        self.open_file_markdown_signal.emit(file_path)

                    action_open_markdown = qt.QAction(
                        "Open with Markdown Viewer", self.tree_menu
                    )
                    action_open_markdown.triggered.connect(open_markdown)
                    icon = functions.create_icon("tango_icons/markdown.png")
                    action_open_markdown.setIcon(icon)
                    self.tree_menu.addAction(action_open_markdown)

            # Open path in explorer
            open_in_explorer_action = qt.QAction(self.open_in_explorer_text, self)

            def open_in_explorer() -> None:
                path = item.attributes.path  # type: ignore[attr-defined]
                if item.attributes.itype == TreeExplorer.ItemType.FILE:  # type: ignore[attr-defined]
                    try:
                        result = functions.open_item_in_explorer(path)
                    except:
                        result = False
                    if result == False:
                        self.main_form.display.repl_display_error(
                            "Error opening path in explorer: {}".format(path)
                        )
                else:
                    try:
                        if data.platform == "Windows":
                            os.startfile(path)
                        else:
                            subprocess.call(["xdg-open", path])
                    except:
                        self.main_form.display.repl_display_error(
                            traceback.format_exc()
                        )

            open_in_explorer_action.setIcon(
                functions.create_icon("tango_icons/document-open.png")
            )
            open_in_explorer_action.triggered.connect(open_in_explorer)
            if item.attributes.itype in [  # type: ignore[attr-defined]
                TreeExplorer.ItemType.FILE,
                TreeExplorer.ItemType.DIRECTORY,
                TreeExplorer.ItemType.BASE_DIRECTORY,
                TreeExplorer.ItemType.DISK,
            ]:
                self.tree_menu.addAction(open_in_explorer_action)

                # Open in terminal
                terminal_path = functions.resolve_terminal_directory(
                    item.attributes.path,  # type: ignore[attr-defined]
                    item.attributes.itype  # type: ignore[attr-defined]
                    in [
                        TreeExplorer.ItemType.DIRECTORY,
                        TreeExplorer.ItemType.BASE_DIRECTORY,
                        TreeExplorer.ItemType.DISK,
                    ],
                )

                def open_in_terminal() -> None:
                    self.main_form.open_terminal_in_directory(
                        terminal_path, self._parent
                    )

                open_in_terminal_action = qt.QAction("Open in Terminal", self.tree_menu)
                open_in_terminal_action.setIcon(
                    functions.create_icon("tango_icons/utilities-terminal.png")
                )
                open_in_terminal_action.triggered.connect(open_in_terminal)
                self.tree_menu.addAction(open_in_terminal_action)

                # Open in external terminal
                def open_in_external_terminal() -> None:
                    self.main_form.open_external_terminal(terminal_path)

                open_in_external_terminal_action = qt.QAction(
                    "Open in External Terminal", self.tree_menu
                )
                open_in_external_terminal_action.setIcon(
                    functions.create_icon("tango_icons/utilities-terminal.png")
                )
                open_in_external_terminal_action.triggered.connect(
                    open_in_external_terminal
                )
                self.tree_menu.addAction(open_in_external_terminal_action)

            # Copy item name to clipboard
            def copy_item_name_to_clipboard() -> None:
                text = os.path.basename(item.attributes.path)  # type: ignore[attr-defined]
                cb = data.application.clipboard()
                cb.clear(mode=cb.Mode.Clipboard)
                cb.setText(text, mode=cb.Mode.Clipboard)
                self.main_form.display.repl_display_message(
                    'Copied to clipboard: "{}"'.format(text)
                )

            action_copy_clipboard = qt.QAction(
                "Copy item name to clipboard", self.tree_menu
            )
            action_copy_clipboard.triggered.connect(copy_item_name_to_clipboard)
            icon = functions.create_icon("tango_icons/edit-copy.png")
            action_copy_clipboard.setIcon(icon)
            if item.attributes.itype in [  # type: ignore[attr-defined]
                TreeExplorer.ItemType.FILE,
                TreeExplorer.ItemType.DIRECTORY,
                TreeExplorer.ItemType.BASE_DIRECTORY,
            ]:
                self.tree_menu.addAction(action_copy_clipboard)

            # Copy item path to clipboard
            def copy_item_path_to_clipboard() -> None:
                text = item.attributes.path  # type: ignore[attr-defined]
                cb = data.application.clipboard()
                cb.clear(mode=cb.Mode.Clipboard)
                cb.setText(text, mode=cb.Mode.Clipboard)
                self.main_form.display.repl_display_message(
                    'Copied to clipboard: "{}"'.format(text)
                )

            action_copy_clipboard = qt.QAction(
                "Copy item path to clipboard", self.tree_menu
            )
            action_copy_clipboard.triggered.connect(copy_item_path_to_clipboard)
            icon = functions.create_icon("tango_icons/edit-copy.png")
            action_copy_clipboard.setIcon(icon)
            if item.attributes.itype in [  # type: ignore[attr-defined]
                TreeExplorer.ItemType.FILE,
                TreeExplorer.ItemType.DIRECTORY,
                TreeExplorer.ItemType.BASE_DIRECTORY,
                TreeExplorer.ItemType.DISK,
            ]:
                self.tree_menu.addAction(action_copy_clipboard)

            # Update current working directory
            def update_cwd() -> None:
                if item.attributes.itype == TreeExplorer.ItemType.FILE:  # type: ignore[attr-defined]
                    path = os.path.dirname(item.attributes.path)  # type: ignore[attr-defined]
                else:
                    path = item.attributes.path  # type: ignore[attr-defined]
                self.main_form.set_cwd(path)

            title = "Update CWD"
            if item.attributes.itype == TreeExplorer.ItemType.FILE:  # type: ignore[attr-defined]
                title = "Update CWD to parent directory"
            action_update_cwd = qt.QAction(title, self.tree_menu)
            action_update_cwd.triggered.connect(update_cwd)
            icon = functions.create_icon("tango_icons/update-cwd.png")
            action_update_cwd.setIcon(icon)
            if item.attributes.itype in [  # type: ignore[attr-defined]
                TreeExplorer.ItemType.FILE,
                TreeExplorer.ItemType.DIRECTORY,
                TreeExplorer.ItemType.BASE_DIRECTORY,
            ]:
                self.tree_menu.addAction(action_update_cwd)

            # Separator
            if not self.tree_menu.isEmpty() and (
                item.attributes.itype  # type: ignore[attr-defined]
                in [
                    TreeExplorer.ItemType.FILE,
                    TreeExplorer.ItemType.DIRECTORY,
                    TreeExplorer.ItemType.BASE_DIRECTORY,
                ]
                or self.__has_pasteable_items()
            ):
                self.tree_menu.addSeparator()
            # Cut item
            cut_items_action = qt.QAction("Cut", self.tree_menu)
            cut_items_action.triggered.connect(self.__cut_items)
            icon = functions.create_icon("tango_icons/edit-cut.png")
            cut_items_action.setIcon(icon)
            if item.attributes.itype in [  # type: ignore[attr-defined]
                TreeExplorer.ItemType.FILE,
                TreeExplorer.ItemType.DIRECTORY,
            ]:
                self.tree_menu.addAction(cut_items_action)
            # Copy item
            copy_item_action = qt.QAction("Copy", self.tree_menu)
            copy_item_action.triggered.connect(self.__copy_items)
            icon = functions.create_icon("tango_icons/edit-copy.png")
            copy_item_action.setIcon(icon)
            if item.attributes.itype in [  # type: ignore[attr-defined]
                TreeExplorer.ItemType.FILE,
                TreeExplorer.ItemType.DIRECTORY,
                TreeExplorer.ItemType.BASE_DIRECTORY,
            ]:
                self.tree_menu.addAction(copy_item_action)
            # Paste item
            paste_item_action = qt.QAction("Paste", self.tree_menu)
            paste_item_action.triggered.connect(self.__paste_items)
            icon = functions.create_icon("tango_icons/edit-paste.png")
            paste_item_action.setIcon(icon)
            if self.__has_pasteable_items():
                self.tree_menu.addAction(paste_item_action)

            # Rename item
            if item.attributes.itype in [  # type: ignore[attr-defined]
                TreeExplorer.ItemType.FILE,
                TreeExplorer.ItemType.DIRECTORY,
            ]:
                # Separator
                self.tree_menu.addSeparator()

                def rename_item() -> None:
                    if len(self.selectedIndexes()) > 1:
                        self.main_form.display.repl_display_warning(
                            "Renaming allows only one item at a time!"
                        )
                        return
                    item.setEditable(True)
                    if item.attributes.itype == TreeExplorer.ItemType.DIRECTORY:  # type: ignore[attr-defined]
                        item.attributes.itype = TreeExplorer.ItemType.RENAME_DIRECTORY  # type: ignore[attr-defined]
                    else:
                        item.attributes.itype = TreeExplorer.ItemType.RENAME_FILE  # type: ignore[attr-defined]
                    index = item.index()
                    self.scrollTo(index)
                    # Start editing the new empty directory name
                    self.start_editing_item(index)
                    self.renamed_item = item

                rename_item_action = qt.QAction("Rename", self.tree_menu)
                rename_item_action.triggered.connect(rename_item)
                icon = functions.create_icon("tango_icons/delete-end-line.png")
                rename_item_action.setIcon(icon)
                self.tree_menu.addAction(rename_item_action)

                # Delete item
                delete_item_action = qt.QAction("Delete", self.tree_menu)
                delete_item_action.triggered.connect(self.__delete_items)
                icon = functions.create_icon("tango_icons/session-remove.png")
                delete_item_action.setIcon(icon)
                self.tree_menu.addAction(delete_item_action)
        else:
            # Paste item
            paste_item_action = qt.QAction("Paste", self.tree_menu)
            paste_item_action.triggered.connect(self.__paste_items)
            icon = functions.create_icon("tango_icons/edit-paste.png")
            paste_item_action.setIcon(icon)
            if self.__has_pasteable_items():
                self.tree_menu.addAction(paste_item_action)
        # Add the actions that are on every menu
        # Separator
        if not self.tree_menu.isEmpty():
            self.tree_menu.addSeparator()
        # New file
        refresh_action = qt.QAction("Refresh view", self.tree_menu)
        refresh_action.triggered.connect(self.refresh)
        icon = functions.create_icon("tango_icons/view-refresh.png")
        refresh_action.setIcon(icon)
        self.tree_menu.addAction(refresh_action)

        # New file
        def new_file() -> None:
            # Get the path
            path = self.current_viewed_directory
            # Create a new file item for editing
            create_file_item = self.create_standard_item(
                "", bold=False, icon=self.file_icon
            )
            create_file_item.attributes = self.__create_item_attribute(  # type: ignore[attr-defined]
                TreeExplorer.ItemType.NEW_FILE,
                path,  # type: ignore[arg-type]
            )
            create_file_item.setEditable(True)
            self.base_item.appendRow(create_file_item)  # type: ignore[union-attr]
            self.added_item = create_file_item
            index = create_file_item.index()
            self.scrollTo(index)
            # Start editing the new empty file name
            self.start_editing_item(index)

        new_file_action = qt.QAction("New file", self.tree_menu)
        new_file_action.triggered.connect(new_file)
        icon = functions.create_icon("tango_icons/document-new.png")
        new_file_action.setIcon(icon)
        self.tree_menu.addAction(new_file_action)

        # New directory
        def new_directory() -> None:
            # Get the path
            path = self.current_viewed_directory
            # Create a new directory item for editing
            create_directory_item = self.create_standard_item(
                "", bold=False, icon=self.folder_icon
            )
            create_directory_item.attributes = self.__create_item_attribute(  # type: ignore[attr-defined]
                TreeExplorer.ItemType.NEW_DIRECTORY,
                path,  # type: ignore[arg-type]
            )
            create_directory_item.setEditable(True)
            self.base_item.appendRow(create_directory_item)  # type: ignore[union-attr]
            self.added_item = create_directory_item
            index = create_directory_item.index()
            self.scrollTo(index)
            # Start editing the new empty directory name
            self.start_editing_item(index)

        new_directory_action = qt.QAction("New Directory", self.tree_menu)
        new_directory_action.triggered.connect(new_directory)
        icon = functions.create_icon("tango_icons/folder-new.png")
        new_directory_action.setIcon(icon)
        self.tree_menu.addAction(new_directory_action)
        # Show the menu
        self.tree_menu.popup(cursor)

    def __paste_copy_path(self, new_path: str, itype: "TreeExplorer.ItemType") -> str:
        """
        Build a '-copy' destination for an existing item, auto-incrementing
        with a trailing number until the name is free.
        For files the '-copy' is inserted before the extension.
        """
        directory = os.path.dirname(new_path)
        base_name = os.path.basename(new_path)
        counter = 1
        if itype in [
            TreeExplorer.ItemType.DIRECTORY,
            TreeExplorer.ItemType.BASE_DIRECTORY,
        ]:
            new_name = f"{base_name}-copy"
        else:
            stem, extension = os.path.splitext(base_name)
            new_name = f"{stem}-copy{extension}"
        candidate = os.path.join(directory, new_name)
        while os.path.lexists(candidate):
            if itype in [
                TreeExplorer.ItemType.DIRECTORY,
                TreeExplorer.ItemType.BASE_DIRECTORY,
            ]:
                new_name = f"{base_name}-copy{counter}"
            else:
                new_name = f"{stem}-copy{counter}{extension}"
            candidate = os.path.join(directory, new_name)
            counter += 1
        return candidate

    def __paste_temp_path(self, new_path: str) -> str:
        """
        Build a unique sibling '.exco-tmp' staging path for 'new_path',
        auto-incrementing with a trailing number until the name is free.
        """
        directory = os.path.dirname(new_path)
        base_name = os.path.basename(new_path)
        counter = 1
        candidate = os.path.join(directory, f"{base_name}.exco-tmp")
        while os.path.lexists(candidate):
            candidate = os.path.join(directory, f"{base_name}.exco-tmp{counter}")
            counter += 1
        return candidate

    def __resolve_paste_target(
        self,
        path: str,
        itype: "TreeExplorer.ItemType",
        base_name: str,
        new_path: str,
    ) -> tuple[str | None, constants.DialogResult | None]:
        """
        Resolve the destination of a single paste item.
        Free targets are used directly; on a collision the user chooses
        between overwrite, overwrite-all, a '-copy' rename, rename-all,
        skip, or skip-all.

        Returns (destination, response); response identifies the 'all'
        choices so the caller can apply them to the remaining items.
        """
        if not os.path.lexists(new_path):
            return (new_path, None)
        message: str = (
            f'The item "{base_name}" already exists!\n'
            "Do you want to overwrite it, paste it as a renamed copy, or skip it?"
        )
        reply: int = OverwriteDialog.question(message)
        if reply == constants.DialogResult.Yes.value:
            return (new_path, constants.DialogResult.Yes)
        if reply == constants.DialogResult.OverwriteAll.value:
            return (new_path, constants.DialogResult.OverwriteAll)
        if reply == constants.DialogResult.Rename.value:
            return (
                self.__paste_copy_path(new_path, itype),
                constants.DialogResult.Rename,
            )
        if reply == constants.DialogResult.RenameAll.value:
            return (
                self.__paste_copy_path(new_path, itype),
                constants.DialogResult.RenameAll,
            )
        if reply == constants.DialogResult.SkipAll.value:
            return (None, constants.DialogResult.SkipAll)
        return (None, constants.DialogResult.No)

    def __clipboard_key(self, path: str) -> str:
        return os.path.normcase(os.path.abspath(path))

    def __item_from_path(self, path: str) -> types.SimpleNamespace:
        return self.__create_item_attribute(
            TreeExplorer.ItemType.DIRECTORY
            if os.path.isdir(path)
            else TreeExplorer.ItemType.FILE,
            path,
        )

    def __in_app_clipboard(self) -> tuple[list[types.SimpleNamespace], bool]:
        """The items of the in-app clipboard and whether they are to be
        moved."""
        if TreeExplorer.cut_items is not None:
            return (TreeExplorer.cut_items, True)
        return (TreeExplorer.copy_items or [], False)

    def __has_pasteable_items(self) -> bool:
        """Whether a paste would have anything to paste.

        The system clipboard counts too, since the OS file manager's own
        copies and cuts land there."""
        if TreeExplorer.cut_items is not None or TreeExplorer.copy_items is not None:
            return True
        try:
            return components.osclipboard.get_files() is not None
        except Exception:
            return False

    def __collect_paste_items(self) -> tuple[list[types.SimpleNamespace], bool] | None:
        """Resolve what a paste should work on: the items and whether they
        are to be moved, or None when there is nothing at all.

        The system clipboard is asked first, so items copied or cut in the
        OS file manager paste here as well. When it holds exactly the items
        of the in-app clipboard that list wins, since it also knows what
        each item is, which the paths alone cannot tell."""
        try:
            system: tuple[list[str], bool] | None = components.osclipboard.get_files()
        except Exception:
            system = None
        in_app: list[types.SimpleNamespace]
        is_cut: bool
        in_app, is_cut = self.__in_app_clipboard()
        if system is None:
            return (in_app, is_cut) if in_app else None
        paths: list[str]
        move: bool
        paths, move = system
        if in_app and {self.__clipboard_key(p) for p in paths} == {
            self.__clipboard_key(i.path) for i in in_app
        }:
            return (in_app, is_cut)
        return ([self.__item_from_path(path) for path in paths], move)

    def __publish_to_system_clipboard(
        self, items: list[types.SimpleNamespace], move: bool
    ) -> None:
        """Hand the items to the system clipboard, so that the OS file
        manager can paste them.

        Best effort: the in-app clipboard remains the source of truth, so a
        clipboard that cannot be written only costs the OS interop."""
        try:
            components.osclipboard.set_files([i.path for i in items], move)
        except Exception:
            self.main_form.display.repl_display_error(traceback.format_exc())

    def __release_system_clipboard(self) -> None:
        """Empty the system clipboard once a cut consumed its sources."""
        try:
            components.osclipboard.clear_files()
        except Exception:
            self.main_form.display.repl_display_error(traceback.format_exc())

    def __paste_items(self) -> None:
        if self.current_viewed_directory is None:
            self.main_form.display.repl_display_message(
                "Cannot paste: no directory is currently viewed!"
            )
            return
        try:
            collected: tuple[list[types.SimpleNamespace], bool] | None
            collected = self.__collect_paste_items()
            if collected is None:
                self.main_form.display.repl_display_error(
                    "Copy AND Cut items list is empty!\n"
                    + "Cannot perform this action!"
                )
                return
            items: list[types.SimpleNamespace]
            is_cut: bool
            items, is_cut = collected
            force_overwrite: bool = False
            force_copy: bool = False
            force_skip: bool = False
            pasted_count: int = 0
            skipped_count: int = 0
            for it in items:
                path: str = it.path
                itype: "TreeExplorer.ItemType" = it.itype
                base_name: str = os.path.basename(path)
                new_path: str = os.path.join(self.current_viewed_directory, base_name)
                if functions.are_paths_same(path, new_path):
                    self.main_form.display.repl_display_warning(
                        "Skipped '{}': it is already in this directory!".format(
                            base_name
                        )
                    )
                    skipped_count += 1
                    continue
                is_symlink = os.path.islink(path)
                if os.path.lexists(new_path):
                    if force_overwrite:
                        destination = new_path
                    elif force_copy:
                        destination = self.__paste_copy_path(new_path, itype)
                    elif force_skip:
                        destination = None
                    else:
                        destination, response = self.__resolve_paste_target(
                            path, itype, base_name, new_path
                        )
                        if response is constants.DialogResult.OverwriteAll:
                            force_overwrite = True
                        elif response is constants.DialogResult.RenameAll:
                            force_copy = True
                        elif response is constants.DialogResult.SkipAll:
                            force_skip = True
                else:
                    destination = new_path
                if destination is None:
                    skipped_count += 1
                    continue
                if itype in [
                    TreeExplorer.ItemType.DIRECTORY,
                    TreeExplorer.ItemType.BASE_DIRECTORY,
                ]:
                    if is_symlink:
                        if os.path.isdir(destination):
                            shutil.rmtree(destination, onerror=remove_readonly)
                            time.sleep(0.1)
                        target = os.readlink(path)
                        os.symlink(target, destination)
                    elif os.path.isdir(destination):
                        temporary = self.__paste_temp_path(destination)
                        try:
                            shutil.copytree(path, temporary)
                        except BaseException:
                            shutil.rmtree(temporary, onerror=remove_readonly)
                            raise
                        shutil.rmtree(destination, onerror=remove_readonly)
                        time.sleep(0.1)
                        os.rename(temporary, destination)
                    else:
                        shutil.copytree(path, destination)
                    if is_cut:
                        if is_symlink:
                            os.remove(path)
                        else:
                            shutil.rmtree(path, onerror=remove_readonly)
                else:
                    if is_symlink:
                        target = os.readlink(path)
                        os.symlink(target, destination)
                    else:
                        shutil.copy(path, destination)
                    if is_cut:
                        os.remove(path)
                pasted_count += 1
        except:
            self.main_form.display.repl_display_error(traceback.format_exc())
            # The clipboard is kept on failure, so the paste can be retried.
            return
        if is_cut and pasted_count > 0:
            # A cut consumed the sources, so it has to release the clipboard;
            # a copy keeps it, so the same selection can be pasted into
            # another directory. A paste that landed nothing keeps it either
            # way, so it can be retried somewhere the paths make sense.
            TreeExplorer.cut_items = None
            TreeExplorer.copy_items = None
            self.__release_system_clipboard()
        summary: str = "{} {} of {} item{}".format(
            "Moved" if is_cut else "Pasted",
            pasted_count,
            len(items),
            "" if len(items) == 1 else "s",
        )
        if skipped_count:
            summary += ", skipped {}".format(skipped_count)
        self.main_form.display.repl_display_message(summary + ".")

    def __copy_items(self) -> None:
        items: list[types.SimpleNamespace] = []
        for i in self.selectedIndexes():
            it: qt.QStandardItem = self.model().itemFromIndex(i)  # type: ignore[union-attr]
            if it is None or not hasattr(it, "attributes"):
                continue
            if it.attributes.disk:
                continue
            if it.attributes.itype in [
                TreeExplorer.ItemType.FILE,
                TreeExplorer.ItemType.DIRECTORY,
                TreeExplorer.ItemType.BASE_DIRECTORY,
            ]:
                items.append(it.attributes)
        if len(items) == 0:
            self.main_form.display.repl_display_message("Nothing selected to copy!")
            return
        TreeExplorer.cut_items = None
        TreeExplorer.copy_items = items
        self.__publish_to_system_clipboard(items, move=False)
        self.main_form.display.repl_display_message("Copied items:")
        for i in items:  # type: ignore[assignment]
            self.main_form.display.repl_display_message(
                '  {}: "{}"'.format(i.itype.name.lower(), i.path)  # type: ignore[attr-defined]
            )

    def __cut_items(self) -> None:
        items: list[types.SimpleNamespace] = []
        for i in self.selectedIndexes():
            it: qt.QStandardItem = self.model().itemFromIndex(i)  # type: ignore[union-attr]
            if it is None or not hasattr(it, "attributes"):
                continue
            if it.attributes.disk:
                continue
            if it.attributes.itype in [
                TreeExplorer.ItemType.FILE,
                TreeExplorer.ItemType.DIRECTORY,
            ]:
                items.append(it.attributes)
        if len(items) == 0:
            self.main_form.display.repl_display_message("Nothing selected to cut!")
            return
        TreeExplorer.cut_items = items
        TreeExplorer.copy_items = None
        self.__publish_to_system_clipboard(items, move=True)
        self.main_form.display.repl_display_message("Cut items:")
        for i in items:  # type: ignore[assignment]
            self.main_form.display.repl_display_message(
                '  {}: "{}"'.format(i.itype.name.lower(), i.path)  # type: ignore[attr-defined]
            )

    def __delete_items(self) -> None:
        items: list[types.SimpleNamespace] = []
        selected: list[types.SimpleNamespace] = []
        for i in self.selectedIndexes():
            item: qt.QStandardItem = self.model().itemFromIndex(i)  # type: ignore[union-attr]
            if item is None or not hasattr(item, "attributes"):
                continue
            selected.append(item.attributes)
            if item.attributes.disk:
                continue
            if item.attributes.itype in [
                TreeExplorer.ItemType.FILE,
                TreeExplorer.ItemType.DIRECTORY,
            ]:
                items.append(item.attributes)
        if len(items) == 0:
            if len(selected) == 0:
                self.main_form.display.repl_display_warning(
                    "Nothing selected to delete!"
                )
            else:
                self.main_form.display.repl_display_warning(
                    "The viewed directory and the drives cannot be deleted!"
                )
            return
        message: str = "What would you like to do with the {} selected items?".format(
            len(items)
        )
        reply: int = DeleteDialog.warning(message)
        if reply == constants.DialogResult.Cancel.value:
            return
        elif reply == constants.DialogResult.RecycleBin.value:
            use_recycle_bin: bool = True
        elif reply == constants.DialogResult.PermanentDelete.value:
            use_recycle_bin = False
        else:
            return
        for it in items:
            path: str = it.path

            if functions.are_paths_same(path, self.current_viewed_directory):
                self.main_form.display.repl_display_warning(
                    "Cannot delete the path that you are currently viewing!\n"
                    + f"  {path}"
                )
                continue
            elif functions.is_parent_directory(
                base_path=path,
                tested_path=self.current_viewed_directory,  # type: ignore[arg-type]
            ):
                self.main_form.display.repl_display_warning(
                    "Cannot delete a path above the path that you are "
                    + f"currently viewing!\n"
                    + f"  {path}"
                )
                continue

            try:
                is_file = it.itype == TreeExplorer.ItemType.FILE
                is_symlink = os.path.islink(path)
                if os.path.lexists(path):
                    if use_recycle_bin:
                        try:
                            # send2trash's SHCreateItemFromParsingName fails with
                            # E_INVALIDARG on forward-slash paths on Windows
                            send2trash(path.replace("/", os.sep))
                        except OSError:
                            # send2trash may fail on symlinks (e.g., to system files on Windows)
                            # Fall back to permanent deletion of the symlink itself
                            if is_symlink:
                                os.remove(path)
                            else:
                                raise
                    else:
                        if is_symlink:
                            os.remove(path)
                        elif os.path.isdir(path):
                            shutil.rmtree(path, onerror=remove_readonly)
                        else:
                            os.remove(path)
                    # Remove from PathWatcher if it was being monitored
                    if is_file:
                        self.main_form.tools.pathwatcher_remove(path)
                else:
                    self.main_form.display.repl_display_message(
                        "Item '{}'\n does not seem to exist!!".format(
                            item.attributes.path  # type: ignore[attr-defined]
                        ),
                        message_type=constants.MessageType.WARNING,
                    )
            except:
                traceback.print_exc()
                self.main_form.display.repl_display_message(
                    traceback.format_exc(), message_type=constants.MessageType.ERROR
                )

    def __open_items(self, model_index: qt.QModelIndex | None = None) -> None:
        try:
            indexes: tuple[qt.QModelIndex, ...]
            if model_index is not None:
                indexes = (model_index,)
            else:
                indexes = self.selectedIndexes()  # type: ignore[assignment]
            for i in indexes:
                item: qt.QStandardItem = self.model().itemFromIndex(i)  # type: ignore[union-attr]
                if item is None:
                    continue
                self.open_item(item)
        except:
            self.main_form.display.repl_display_error(traceback.format_exc())

    def __item_double_click(self, model_index: qt.QModelIndex) -> None:
        self.__open_items(model_index)

    def scroll_and_ensure_item_visible(self, item: qt.QStandardItem) -> None:
        """Scroll the tree view to ensure the given item is visible.

        Args:
            item: The QStandardItem to scroll into view.
        """
        self.scrollTo(
            item.index(),
            qt.QAbstractItemView.ScrollHint.EnsureVisible,
        )

    def open_item(self, item: qt.QStandardItem) -> None:
        if hasattr(item, "attributes") == False:
            index: qt.QModelIndex = item.index()
            if self.isExpanded(index):
                self.collapse(index)
            else:
                self.expand(index)
            return
        if item.attributes.itype in [  # type: ignore[attr-defined]
            TreeExplorer.ItemType.DIRECTORY,
            TreeExplorer.ItemType.BASE_DIRECTORY,
        ]:
            item_attributes: Any = item.attributes  # type: ignore[attr-defined]
            self.display_directory(
                item_attributes.path,
                disk=item_attributes.disk,
            )
        if item.attributes.itype == TreeExplorer.ItemType.FILE:  # type: ignore[attr-defined]
            self.open_file_signal.emit(item.attributes.path)  # type: ignore[attr-defined]
        if item.attributes.itype == TreeExplorer.ItemType.DISK:  # type: ignore[attr-defined]
            if data.platform == "Windows":
                self.display_windows_disks()

    def display_windows_disks(self) -> None:
        """Populate the view with the logical drives of the machine.

        Drive rows are typed as directories so that they navigate like any
        other folder, and are flagged as disks to keep them out of the
        cut, copy and delete paths, which would otherwise take a whole drive
        with them.
        """
        if data.platform != "Windows":
            return
        tree_model: qt.QStandardItemModel = self.__init_tree_model()
        base_item: qt.QStandardItem = self.create_standard_item(
            "Computer", bold=False, icon=self.computer
        )
        base_item.attributes = self.__create_item_attribute(  # type: ignore[attr-defined]
            TreeExplorer.ItemType.COMPUTER,
            None,  # type: ignore[arg-type]
        )
        tree_model.appendRow(base_item)
        drives: str = win32api.GetLogicalDriveStrings()
        drives_list: list[str] = drives.split("\000")[:-1]
        for d in drives_list:
            d = functions.unixify_path(d)
            item: qt.QStandardItem = self.create_standard_item(
                d, bold=False, icon=self.disk_icon
            )
            item.attributes = self.__create_item_attribute(  # type: ignore[attr-defined]
                TreeExplorer.ItemType.DIRECTORY, d, disk=True
            )
            base_item.appendRow(item)
        self.base_item = base_item
        self.setModel(tree_model)
        tree_model.itemChanged.connect(self.__item_changed)
        self.expand(base_item.index())
        self.__vcs_clear()
        self.__nav_record(NavLocation(None, True))

    def create_directory_list(self, directory: str) -> list[qt.QStandardItem]:
        dir_items: list[qt.QStandardItem] = []
        file_items: list[qt.QStandardItem] = []
        dir_list: list[str] = os.listdir(directory)
        for i in dir_list:
            full_path: str = os.path.join(directory, i)
            full_path = functions.unixify_path_keep_symlink(full_path)
            hidden: bool = self.__is_hidden_item(full_path)
            if os.path.isdir(full_path):
                icon: qt.QIcon = self.folder_icon
                if hidden:
                    icon = functions.change_icon_opacity(icon, 0.3)
                item: qt.QStandardItem = self.create_standard_item(
                    i, bold=False, icon=icon
                )
                item.attributes = self.__create_item_attribute(  # type: ignore[attr-defined]
                    TreeExplorer.ItemType.DIRECTORY, full_path, hidden
                )
                dir_items.append(item)
            else:
                icon = functions.create_language_document_icon_from_path(
                    full_path, check_content=False
                )
                if hidden:
                    icon = functions.change_icon_opacity(icon, 0.3)
                item = self.create_standard_item(i, bold=False, icon=icon)
                item.attributes = self.__create_item_attribute(  # type: ignore[attr-defined]
                    TreeExplorer.ItemType.FILE, full_path, hidden
                )
                file_items.append(item)
        dir_items.sort(key=lambda s: _sort_key(s.text()))
        file_items.sort(key=lambda s: _sort_key(s.text()))
        item_list: list[qt.QStandardItem] = dir_items + file_items
        return item_list

    """
    Overriden events
    """

    def _resolve_item_tooltip(
        self, item: qt.QStandardItem, pos: qt.QPoint
    ) -> str | None:
        """The metadata tooltip, a live line with the VCS state, and for an
        image file its thumbnail (decoded in the background: the first hover
        shows the text, the picture is swapped in when it is ready)."""
        text: str | None = self.__resolve_base_tooltip(item, pos)
        attributes: Any = getattr(item, "attributes", None)
        path: str | None = getattr(attributes, "path", None)
        if text is None or not isinstance(path, str):
            return text
        self.__start_preview(path, getattr(attributes, "itype", None))
        return self.__finish_tooltip(path, text)

    def __finish_tooltip(self, path: str, text: str) -> str:
        """The final tooltip for *path*: the VCS line is added, and when the
        image preview is ready the whole thing becomes rich text with it."""
        text = self.__with_vcs_line(path, text)
        cached: tuple[tuple[int, int], ImagePreview | None] | None = (
            self.__preview_cache.get(path)
        )
        if cached is None or cached[1] is None:
            return text
        return _rich_preview_tooltip(text, cached[1])

    def __start_preview(self, path: str, itype: Any) -> None:
        """Begin decoding a thumbnail for an image file, once per file version.

        The cache entry carries the file's (mtime, size): a file that changed
        is decoded again, and a stale preview is dropped at once rather than
        shown until the new one arrives. A failure is cached too, or a broken
        image would be retried on every hover.
        """
        if itype != TreeExplorer.ItemType.FILE or not _is_previewable_image(path):
            return
        try:
            info: os.stat_result = os.stat(path)
        except OSError:
            return
        signature: tuple[int, int] = (info.st_mtime_ns, info.st_size)
        cached = self.__preview_cache.get(path)
        if cached is not None:
            if cached[0] == signature:
                return
            del self.__preview_cache[path]
        if path in self.__preview_inflight:
            return
        if info.st_size > IMAGE_PREVIEW_MAX_BYTES:
            self.__preview_cache[path] = (signature, None)
            return
        self.__preview_inflight.add(path)
        threading.Thread(
            target=self.__compute_preview, args=(path, signature), daemon=True
        ).start()

    def __compute_preview(self, path: str, signature: tuple[int, int]) -> None:
        """Worker thread: decode the thumbnail, then hand it to the GUI thread."""
        preview: ImagePreview | None = _build_image_preview(path)
        try:
            self.__preview_ready.emit(path, signature, preview)
        except RuntimeError:
            pass  # the explorer was destroyed while the image decoded

    @qt.pyqtSlot(str, object, object)
    def on_preview_ready(self, path: str, signature: object, preview: object) -> None:
        self.__preview_inflight.discard(path)
        self.__preview_cache[path] = (
            cast(tuple[int, int], signature),
            cast("ImagePreview | None", preview),
        )
        if preview is None or self.__tooltip_current is None:
            return
        if self.__tooltip_current[0] != path:
            return
        base: str | None = self.__tooltip_cache.get(path)
        if base is not None and qt.QToolTip.isVisible():
            qt.QToolTip.showText(
                self.__tooltip_current[1], self.__finish_tooltip(path, base), self.tree
            )

    def __with_vcs_line(self, path: str, text: str) -> str:
        """*text* with a 'VCS: <state>' line when *path* has a state.

        The row of the repository's own root directory gets the repository
        block instead: branch, checked-out commit and change counts.
        """
        snapshot = self.__vcs_snapshot
        if snapshot is None or snapshot.error is not None:
            return text
        if components.vcsstatus.path_key(path) == components.vcsstatus.path_key(
            snapshot.root
        ):
            return "{}\n\n{}".format(text, self.__vcs_repository_block(snapshot))
        state = snapshot.state_for(path)
        if state is None:
            return text
        return "{}\nVCS: {} ({})".format(text, state.name.lower(), snapshot.kind)

    def __resolve_base_tooltip(
        self, item: qt.QStandardItem, pos: qt.QPoint
    ) -> str | None:
        """
        The tooltip for *item*, resolved when the tooltip is first shown.

        Nothing is computed while the listing is built. The hover itself pays
        for one stat, which feeds the path, created, modified and accessed
        lines; the recursive directory size is the expensive part, so the
        first hover over a directory shows a 'Size: ...' placeholder, computes
        the total on a worker thread, and swaps the real line in if the
        tooltip is still showing. Resolved text is cached per path and cleared
        on every listing.
        """
        attributes = getattr(item, "attributes", None)
        item_path = getattr(attributes, "path", None)
        itype = getattr(attributes, "itype", None)
        if not isinstance(item_path, str) or itype not in (
            TreeExplorer.ItemType.FILE,
            TreeExplorer.ItemType.DIRECTORY,
            TreeExplorer.ItemType.BASE_DIRECTORY,
        ):
            return None
        cached: str | None = self.__tooltip_cache.get(item_path)
        if cached is not None:
            self.__tooltip_current = (item_path, pos)
            return cached
        try:
            info: os.stat_result = os.stat(item_path)
        except OSError:
            self.__tooltip_complete.add(item_path)
            return None
        if itype == TreeExplorer.ItemType.FILE:
            text: str = _tooltip_lines(item_path, info, None)
            self.__tooltip_cache[item_path] = text
            self.__tooltip_complete.add(item_path)
        else:
            text = _tooltip_lines(item_path, info, "...")
            self.__tooltip_cache[item_path] = text
            if item_path not in self.__tooltip_inflight:
                self.__tooltip_inflight.add(item_path)
                thread: threading.Thread = threading.Thread(
                    target=self.__compute_size_tooltip,
                    args=(item_path,),
                    daemon=True,
                )
                thread.start()
        self.__tooltip_current = (item_path, pos)
        return text

    def __compute_size_tooltip(self, path: str) -> None:
        """Worker thread: the recursive directory total, then the full tooltip."""
        scan: tuple[int, bool] | None = _scan_directory_size(path)
        size_text: str | None
        if scan is None:
            size_text = None
        else:
            total, truncated = scan
            size_text = _format_size(total)
            if truncated:
                size_text = "> " + size_text
        self.__tooltip_ready.emit(path, _tooltip_text(path, size_text))

    @qt.pyqtSlot(str, object)
    def on_tooltip_ready(self, path: str, text: object) -> None:
        self.__tooltip_inflight.discard(path)
        if text is not None:
            self.__tooltip_cache[path] = str(text)
        self.__tooltip_complete.add(path)
        if self.__tooltip_current is not None and self.__tooltip_current[0] == path:
            _path, pos = self.__tooltip_current
            if qt.QToolTip.isVisible() and text is not None:
                shown: str = self.__finish_tooltip(path, str(text))
                qt.QToolTip.showText(pos, shown, self.tree)

    def _on_mouse_pressed(self, event: qt.QMouseEvent) -> None:
        # The view saw a press: the base class handles the bookkeeping, then
        # a right press builds the context menu and a left press on the root
        # row opens the path editor.
        super()._on_mouse_pressed(event)
        if event.button() == qt.Qt.MouseButton.RightButton:
            self.__apply_right_click(event)
        elif event.button() == qt.Qt.MouseButton.LeftButton:
            self.__root_item_pressed(event)
        elif event.button() == qt.Qt.MouseButton.BackButton:
            self.navigate_back()
        elif event.button() == qt.Qt.MouseButton.ForwardButton:
            self.navigate_forward()

    def mousePressEvent(self, event: qt.QMouseEvent) -> None:  # type: ignore[override]
        # A press that reaches the tab directly (rather than the inner view)
        # has to build the same menu.
        super().mousePressEvent(event)
        if event.button() == qt.Qt.MouseButton.RightButton:
            self.__apply_right_click(event)

    def __apply_right_click(self, event: qt.QMouseEvent) -> None:
        # The context menu operates on the current selection, so the pressed
        # row has to be selected before it is built.
        index: qt.QModelIndex = self.indexAt(event.pos())
        selection_model: qt.QItemSelectionModel | None = self.selectionModel()
        if index.isValid() and selection_model is not None:
            # A right click inside the selection keeps it, a click outside
            # it narrows the selection to the pressed row.
            if not selection_model.isSelected(index):
                selection_model.select(
                    index,
                    qt.QItemSelectionModel.SelectionFlag.ClearAndSelect
                    | qt.QItemSelectionModel.SelectionFlag.Rows,
                )
        self.__item_right_click(index)

    """
    Public functions
    """

    def display_directory(
        self, directory: str, disk: bool = False, scroll_restore: bool = False
    ) -> bool:
        """Populate the view with the contents of *directory*.

        Return False (after reporting) when the directory cannot be listed,
        eg. a protected system directory such as 'C:/PerfLogs'. Nothing is
        committed in that case: the previous listing, the current directory
        and the file watcher stay exactly as they were, so the view can never
        end up claiming to show a directory it was never able to read.

        The one exception is a freshly created explorer, which has no model
        to keep (eg. a restored layout pointing at a now protected folder):
        it gets a well-formed empty listing instead of no model at all.
        """
        # Rebuilding the listing replaces the row a root edit is open on: do
        # not leave an edit behind that points at a row the model dropped.
        if self.editing_root_item is not None:
            self.__reset_root_edit()
        readable: bool = True
        try:
            lst: list[qt.QStandardItem] = self.create_directory_list(directory)
        except OSError as error:
            message = "Cannot open directory '{}':\n  {}".format(
                directory, error.strerror or error
            )
            self.main_form.display.repl_display_error(message)
            self.main_form.display.write_to_statusbar("Cannot open directory!", 3000)
            readable = False
            lst = []
            if self.model() is not None:
                return False

        self._refresh_in_progress = True
        watched_directories: list[str] = self.__file_watcher.directories()
        if len(watched_directories) > 0:
            self.__file_watcher.removePaths(watched_directories)
        if readable and os.path.isdir(directory):
            self.__file_watcher.addPath(directory)
        self._refresh_in_progress = False

        scroll_position: tuple[int, int] = (
            self.horizontalScrollBar().value(),
            self.verticalScrollBar().value(),
        )

        self.current_viewed_directory = directory
        # A new listing invalidates every cached tooltip: sizes may have
        # changed, and the items themselves are about to be rebuilt.
        self.__tooltip_cache = {}
        self.__tooltip_inflight = set()
        self.__tooltip_complete = set()
        self.__tooltip_current = None
        self.__preview_cache = {}
        tree_model, base_item = self.__build_directory_model(directory, disk, lst)
        self.base_item = base_item
        self.setModel(tree_model)
        tree_model.itemChanged.connect(self.__item_changed)
        self.expand(base_item.index())
        self.__vcs_refresh(directory)
        # Make sure the base item is visible
        self.scroll_and_ensure_item_visible(base_item)

        if scroll_restore:

            def __scroll_restore() -> None:
                x: int
                y: int
                x, y = scroll_position
                self.horizontalScrollBar().setValue(x)
                self.verticalScrollBar().setValue(y)

            qt.QTimer.singleShot(0, __scroll_restore)

        self.__update_tab_title()
        if readable:
            self.__nav_record(NavLocation(directory, disk))
        return readable

    def __build_directory_model(
        self, directory: str, disk: bool, items: list[qt.QStandardItem]
    ) -> tuple[qt.QStandardItemModel, qt.QStandardItem]:
        """Build the model holding *items* under the row for *directory*."""
        tree_model: qt.QStandardItemModel = self.__init_tree_model()
        sd: tuple[str, str] = os.path.splitdrive(directory)
        base_item: qt.QStandardItem
        if disk == True:
            base_item = self.create_standard_item(
                directory, bold=False, icon=self.disk_icon
            )
            base_item.attributes = self.__create_item_attribute(  # type: ignore[attr-defined]
                TreeExplorer.ItemType.DISK, directory
            )
            tree_model.appendRow(base_item)
        elif sd[1] != "" and sd[1] != "\\":
            base_item = self.create_standard_item(
                functions.unixify_path(directory), bold=False, icon=self.folder_icon
            )
            base_item.attributes = self.__create_item_attribute(  # type: ignore[attr-defined]
                TreeExplorer.ItemType.BASE_DIRECTORY, directory
            )
            tree_model.appendRow(base_item)
        else:
            base_item = self.create_standard_item(
                sd[0], bold=False, icon=self.disk_icon
            )
            base_item.attributes = self.__create_item_attribute(  # type: ignore[attr-defined]
                TreeExplorer.ItemType.DISK, directory
            )
            tree_model.appendRow(base_item)
        for item in items:
            base_item.appendRow(item)
        return tree_model, base_item

    # ------------------------------------------------------------------
    # Navigation history (back / forward / up)
    # ------------------------------------------------------------------
    def __nav_same(self, first: NavLocation | None, second: NavLocation | None) -> bool:
        """Whether two locations are the same place ('D:' and 'd:/' are)."""
        if first is None or second is None:
            return first is second
        if first.path is None or second.path is None:
            return first.path is None and second.path is None
        return self.__path_key(first.path) == self.__path_key(second.path)

    def __nav_record(self, location: NavLocation) -> None:
        """The view has just landed on *location*: remember where it was.

        History follows where the view *lands* rather than who asked, so every
        way of navigating (opening a folder, editing the root path, the main
        window, a restored layout) is covered, and a refresh -- which lands on
        the same place -- records nothing. While back/forward are moving
        through the stacks the stacks are theirs to maintain.
        """
        current: NavLocation | None = self.__nav_current
        if self.__nav_same(current, location):
            self.__nav_current = location
        else:
            if current is not None and not self.__nav_traversing:
                self.__nav_back.append(current)
                del self.__nav_back[:-NAV_HISTORY_LIMIT]
                self.__nav_forward.clear()
            self.__nav_current = location
        self.__update_nav_buttons()

    def __nav_go(self, location: NavLocation) -> bool:
        """Show *location* without recording it as a new navigation."""
        self.__nav_traversing = True
        try:
            if location.path is None:
                if data.platform != "Windows":
                    return False
                self.display_windows_disks()
                return True
            return bool(self.display_directory(location.path, disk=location.disk))
        finally:
            self.__nav_traversing = False

    def navigate_back(self) -> bool:
        """Go to the previous location. False when there is none, or it can
        no longer be shown (the error is reported and the history is kept)."""
        if not self.__nav_back:
            return False
        current: NavLocation | None = self.__nav_current
        if not self.__nav_go(self.__nav_back[-1]):
            return False
        self.__nav_back.pop()
        if current is not None:
            self.__nav_forward.append(current)
        self.__update_nav_buttons()
        return True

    def navigate_forward(self) -> bool:
        """Undo the last Back. Same contract as `navigate_back`."""
        if not self.__nav_forward:
            return False
        current: NavLocation | None = self.__nav_current
        if not self.__nav_go(self.__nav_forward[-1]):
            return False
        self.__nav_forward.pop()
        if current is not None:
            self.__nav_back.append(current)
        self.__update_nav_buttons()
        return True

    def navigate_up(self) -> bool:
        """Go to the parent directory -- or, from a drive root, to the drive
        list -- and select the folder the user came from.

        Unlike Back and Forward this is a new navigation: it is pushed on the
        history like opening a folder.
        """
        current: NavLocation | None = self.__nav_current
        parent: NavLocation | None = self.__nav_parent(current)
        if current is None or parent is None:
            return False
        came_from: str | None = current.path
        if parent.path is None:
            self.display_windows_disks()
            displayed: bool = True
        else:
            displayed = bool(self.display_directory(parent.path, disk=parent.disk))
        if displayed and came_from is not None:
            self.__select_path(came_from)
        return displayed

    def __nav_parent(self, location: NavLocation | None) -> NavLocation | None:
        """The location Up leads to, or None (drive list, filesystem root)."""
        if location is None or location.path is None:
            return None
        parent: str = functions.unixify_path_keep_symlink(
            os.path.join(location.path, os.pardir)
        )
        if self.__path_key(parent) == self.__path_key(location.path):
            # A root: on Windows the next step up is the list of drives
            return NavLocation(None, True) if data.platform == "Windows" else None
        return NavLocation(parent, False)

    def __select_path(self, path: str) -> None:
        """Select and scroll to the row of *path* in the current listing."""
        model: qt.QAbstractItemModel | None = self.model()
        if model is None:
            return
        key: str = self.__path_key(path)
        for item in self.iterate_items(model.invisibleRootItem()):  # type: ignore[attr-defined]
            candidate: Any = getattr(getattr(item, "attributes", None), "path", None)
            if isinstance(candidate, str) and self.__path_key(candidate) == key:
                self.setCurrentIndex(item.index())

                def scroll(row: qt.QStandardItem = item) -> None:
                    try:
                        self.scroll_and_ensure_item_visible(row)
                    except RuntimeError:
                        pass  # the listing was rebuilt in the meantime

                qt.QTimer.singleShot(0, scroll)
                return

    @staticmethod
    def __nav_label(location: NavLocation) -> str:
        return "Computer" if location.path is None else location.path

    def __update_nav_buttons(self) -> None:
        """Enable the footer buttons that lead somewhere, and name where."""
        targets: list[tuple[qt.QPushButton, NavLocation | None, str, str]] = [
            (
                self.nav_back_button,
                self.__nav_back[-1] if self.__nav_back else None,
                "Back",
                "Alt+Left",
            ),
            (
                self.nav_forward_button,
                self.__nav_forward[-1] if self.__nav_forward else None,
                "Forward",
                "Alt+Right",
            ),
            (
                self.nav_up_button,
                self.__nav_parent(self.__nav_current),
                "Up",
                "Alt+Up",
            ),
        ]
        for button, target, verb, shortcut in targets:
            button.setEnabled(target is not None)
            where: str = "" if target is None else " to " + self.__nav_label(target)
            button.setToolTip("{}{} ({})".format(verb, where, shortcut))

    def __vcs_clear(self) -> None:
        """Forget the repository: the listing is not inside one."""
        self.__vcs_repo = None
        self.__vcs_key = None
        self.__vcs_snapshot = None
        self.__vcs_update_label()

    def __vcs_refresh(self, directory: str) -> None:
        """Find the repository of *directory* and ask for fresh status.

        The cached snapshot, when there is one, decorates the rows at once so
        a refresh does not flicker; the answer replaces it a moment later.
        """
        self.__vcs_clear()
        if not settings.get("tree_explorer_vcs_status"):
            return
        repo = components.vcsstatus.find_repo(directory)
        if repo is None:
            return
        provider = components.vcsstatus.provider()
        self.__vcs_repo = repo
        self.__vcs_key = components.vcsstatus.VcsStatusProvider.key_for(repo, directory)
        self.__vcs_snapshot = provider.cached(self.__vcs_key)
        self.__vcs_request(directory, repo)
        self.__vcs_update_label()

    @qt.pyqtSlot(str)
    def __on_vcs_metadata(self, root_key: str) -> None:
        """A commit/checkout changed the repository this tab shows."""
        repo = self.__vcs_repo
        directory = self.current_viewed_directory
        if repo is None or directory is None:
            return
        if components.vcsstatus.path_key(repo.root) == root_key:
            self.__vcs_request(directory, repo)

    @qt.pyqtSlot(str)
    def __on_editor_saved(self, path: str) -> None:
        """A document was saved: re-query when it lies in the shown repository.

        Saving overwrites the file in place, which neither the directory
        watcher nor the repository-metadata watcher can see.
        """
        repo = self.__vcs_repo
        directory = self.current_viewed_directory
        if repo is None or directory is None:
            return
        root: str = components.vcsstatus.path_key(repo.root)
        saved: str = components.vcsstatus.path_key(path)
        if saved.startswith(root + os.sep):
            self.__vcs_request(directory, repo)

    def __vcs_request(
        self, directory: str, repo: components.vcsstatus.RepoInfo
    ) -> None:
        """Ask for fresh status, remembering what the directory looked like.

        The fingerprint is taken *before* the query starts, so an edit made
        while it runs still differs from it at the next poll.
        """
        self.__vcs_fingerprint = components.vcsstatus.directory_fingerprint(
            directory, self.__vcs_is_ignored
        )
        components.vcsstatus.provider().request(directory, repo)

    def __vcs_repository_block(
        self, snapshot: components.vcsstatus.StatusSnapshot
    ) -> str:
        """The repository lines of the root row's tooltip."""
        lines: list[str] = [
            "Repository: {}".format(snapshot.kind),
            "Branch: {}".format(snapshot.branch),
        ]
        tracking = snapshot.tracking
        if tracking is not None and tracking.upstream is not None:
            lines.append("Upstream: {}".format(tracking.describe()))
        head = snapshot.head
        if head is not None:
            lines.append("Commit: {}".format(head.commit))
            lines.append("    {}".format(head.subject))
            lines.append("    {}, {}".format(head.author, head.date))
            if head.tags:
                lines.append("Tags: {}".format(", ".join(head.tags)))
            if head.phase:
                lines.append("Phase: {}".format(head.phase))
        lines.append("Changes: {}".format(snapshot.describe_counts()))
        return "\n".join(lines)

    def __vcs_is_ignored(self, path: str) -> bool:
        """Whether the snapshot marks *path* ignored (kept out of the poll)."""
        snapshot = self.__vcs_snapshot
        if snapshot is None:
            return False
        return snapshot.state_for(path) == components.vcsstatus.VcsState.IGNORED

    def __vcs_poll(self) -> None:
        """Re-query when a file in the listed directory changed on disk.

        Catches an edit by another program (a formatter in the terminal, an
        external editor), which neither the directory watcher, the metadata
        watcher nor ExCo's own save signal can see. Only a *visible* explorer
        polls, and only when the fingerprint moved, so an idle one costs a
        directory scan every few seconds and no process.
        """
        repo = self.__vcs_repo
        directory = self.current_viewed_directory
        if repo is None or directory is None or not self.isVisible():
            return
        fingerprint: int = components.vcsstatus.directory_fingerprint(
            directory, self.__vcs_is_ignored
        )
        if fingerprint != self.__vcs_fingerprint:
            self.__vcs_request(directory, repo)

    @qt.pyqtSlot(str, object)
    def __on_vcs_status(self, key: str, snapshot: Any) -> None:
        if key != self.__vcs_key:
            return
        self.__vcs_snapshot = snapshot
        self.__vcs_update_label()
        if self.model() is not None:
            self.viewport().update()
            self._resize_horizontal_scrollbar()

    def __vcs_update_label(self) -> None:
        """Footer label: 'git: main \u00b7 7b05e612 \u00b7 3M 1A 2?', hidden outside a repo.

        The tool name is a link that opens the copy menu (`__on_vcs_link`); the
        loading and error states are plain text, so nothing there is clickable.
        """
        repo = self.__vcs_repo
        if repo is None:
            self.vcs_label.hide()
            self.vcs_row.hide()
            return
        snapshot = self.__vcs_snapshot
        self.vcs_label.setTextFormat(qt.Qt.TextFormat.PlainText)
        if snapshot is None:
            self.vcs_label.setText(
                "{}: {}".format(repo.kind, components.vcsstatus.read_branch(repo))
            )
            self.vcs_label.setToolTip(repo.root)
        elif snapshot.error is not None:
            self.vcs_label.setText("{} \u00b7 !".format(snapshot.summary()))
            self.vcs_label.setToolTip("{}\n{}".format(repo.root, snapshot.error))
        else:
            self.vcs_label.setTextFormat(qt.Qt.TextFormat.RichText)
            self.vcs_label.setText(snapshot.summary_rich())
            self.vcs_label.setToolTip(
                "{}\nClick '{}' for the branch, commit and more to copy".format(
                    repo.root, repo.kind
                )
            )
        self.vcs_label.show()
        self.__place_vcs_label()

    def resizeEvent(self, event: qt.QResizeEvent) -> None:  # type: ignore[override]
        super().resizeEvent(event)
        self.__place_vcs_label()

    def __footer_buttons_width(self) -> int:
        """The width the button row needs by itself, label excluded.

        The buttons and separators have fixed widths, so their minimum widths
        are their widths -- unlike `width()`, which is meaningless before the
        widgets have been shown.
        """
        layout: qt.QHBoxLayout = self.footer_layout
        margins: qt.QMargins = layout.contentsMargins()
        width: int = margins.left() + margins.right()
        count: int = 0
        for index in range(layout.count()):
            widget: qt.QWidget | None = layout.itemAt(index).widget()
            if widget is None or widget is self.vcs_label:
                continue
            width += widget.minimumWidth()
            count += 1
        return width + layout.spacing() * max(count - 1, 0)

    def __vcs_label_width(self) -> int:
        """The width the label's text needs, in whichever row it is.

        Measured here because `QLabel.sizeHint()` is not stable across a
        re-parenting (450 px before the move, 416 after, for the same text), so
        deciding from it made the placement flap at the threshold.
        """
        label: qt.QLabel = self.vcs_label
        document: qt.QTextDocument = qt.QTextDocument()
        document.setDefaultFont(label.font())
        document.setDocumentMargin(0)
        if label.textFormat() == qt.Qt.TextFormat.RichText:
            document.setHtml(label.text())
        else:
            document.setPlainText(label.text())
        return int(document.idealWidth()) + 1 + VCS_LABEL_PADDING

    def __vcs_inline_width(self) -> int:
        """The tab width from which the label fits in the button row.

        The buttons, then two gaps (before the trailing spacer and between it
        and the label), then the text.
        """
        return (
            self.__footer_buttons_width()
            + 2 * self.footer_layout.spacing()
            + self.__vcs_label_width()
        )

    def __place_vcs_label(self) -> None:
        """Put the repository label where it fits.

        At the right end of the button row when the tab is wide enough for the
        buttons *and* the whole label, otherwise on the line above them. The
        label's own width asks for nothing (see the size policy), so this
        decision cannot feed back into the tab's minimum width.
        """
        label: qt.QLabel = self.vcs_label
        inline: bool = self.width() >= self.__vcs_inline_width()
        in_buttons: bool = self.footer_layout.indexOf(label) >= 0
        if inline != in_buttons:
            # A layout re-shows a re-parented widget unless it was explicitly
            # hidden, which is exactly the state wanted here (no repository).
            if inline:
                self.vcs_row_layout.removeWidget(label)
                # stretch 1: it, not the spacer before it, takes the spare width
                self.footer_layout.addWidget(label, 1)
            else:
                self.footer_layout.removeWidget(label)
                self.vcs_row_layout.addWidget(label)
        label.setAlignment(
            (
                qt.Qt.AlignmentFlag.AlignRight
                if inline
                else qt.Qt.AlignmentFlag.AlignLeft
            )
            | qt.Qt.AlignmentFlag.AlignVCenter
        )
        self.vcs_row.setVisible(not inline and not label.isHidden())

    def __on_vcs_link(self, link: str) -> None:
        """The tool name in the footer label was clicked: pop up the copy menu.

        It lists what `StatusSnapshot.copy_entries` offers for the repository
        (branch, upstream, commit ids, tags, path), each with a feather glyph,
        and opens upward from the label, since the footer is at the bottom of
        the tab.
        """
        snapshot = self.__vcs_snapshot
        if link != "vcs:menu" or snapshot is None or snapshot.error is not None:
            return
        if self.__vcs_menu is not None:
            self.__vcs_menu.setParent(None)  # type: ignore[call-overload]
            self.__vcs_menu.deleteLater()
        menu: Menu = Menu(self)
        self.__vcs_menu = menu
        for entry in snapshot.copy_entries():
            if entry is None:
                menu.addSeparator()
                continue
            text, value, what = entry
            # '&' would be taken for a mnemonic marker (a branch may hold one)
            action: qt.QAction = qt.QAction(text.replace("&", "&&"), menu)
            icon_name: str | None = self.__vcs_menu_icon_name(text)
            if icon_name is not None:
                action.setIcon(_feather_icon(icon_name))
            action.triggered.connect(
                lambda checked=False, value=value, what=what: self.__vcs_copy(
                    value, what
                )
            )
            menu.addAction(action)
        origin: qt.QPoint = self.vcs_label.mapToGlobal(qt.QPoint(0, 0))
        origin.setY(origin.y() - menu.sizeHint().height())
        menu.popup(origin)

    @staticmethod
    def __vcs_menu_icon_name(text: str) -> str | None:
        """The feather glyph that belongs to a copy-entry label, if any"""
        for prefix, icon_name in _VCS_MENU_ICONS:
            if text.startswith(prefix):
                return icon_name
        return None

    def __vcs_copy(self, value: str, what: str) -> None:
        """Put *value* on the clipboard and say so in the statusbar."""
        clipboard = qt.QApplication.clipboard()
        if clipboard is not None:
            clipboard.setText(value)
        self.main_form.display.write_to_statusbar("Copied {}".format(what), 3000)

    def _vcs_decoration(self, item: qt.QStandardItem) -> tuple[str, qt.QColor] | None:
        """(state letter, colour) for the delegate, or None for a clean row.

        Only real files and directories are decorated; the navigation, drive
        and in-progress rows are not versioned things. An ignored entry is
        tinted but carries no letter.
        """
        snapshot = self.__vcs_snapshot
        if snapshot is None or snapshot.error is not None:
            return None
        attributes = getattr(item, "attributes", None)
        if attributes is None or attributes.disk:
            return None
        if attributes.itype not in (
            TreeExplorer.ItemType.FILE,
            TreeExplorer.ItemType.DIRECTORY,
        ):
            return None
        if not isinstance(attributes.path, str):
            return None
        state = snapshot.state_for(attributes.path)
        if state is None:
            return None
        color = qt.QColor(components.vcsstatus.theme_color(settings.get_theme(), state))
        letter: str = (
            "" if state == components.vcsstatus.VcsState.IGNORED else state.letter
        )
        return letter, color

    def __update_tab_title(self) -> None:
        if self.parent() is not None and self.parent().parent() is not None:  # type: ignore[union-attr]
            tab_widget: qt.QWidget = cast(qt.QWidget, self.parent().parent())  # type: ignore[union-attr]
            path: Path = Path(self.current_viewed_directory)  # type: ignore[arg-type]

            base_path: str
            if path.name == "":
                if os.name == "nt" and path.drive:
                    base_path = f"{path.drive}/"
                else:
                    base_path = str(path) if str(path) else "/"
            else:
                base_path = path.name

            tab_widget.set_tab_name(  # type: ignore[attr-defined]
                self,
                f"{constants.SpecialTabNames.FileExplorer.value}: {base_path}",
            )
