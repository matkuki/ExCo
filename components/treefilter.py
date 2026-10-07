"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.

For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

from typing import Any, Callable

import qt

from components.filteredit import FilterField

# PyQt6 does not expose QStandardItem.setHidden/isHidden and QStandardItemModel
# has no concept of a hidden row: nothing Qt draws reads a data role to decide
# row visibility, so writing the role alone does not remove a row from the
# screen. The role is kept only as an in-model marker - the selection handler
# and the tests read it - while the rows are actually taken out of the view by
# QTreeView::setRowHidden, which the filter mirrors whenever it writes the
# marker. Note that a view-hidden row is not dropped from the selection model,
# so a filtered out row would still be handed to whatever acts on the selection.
HIDDEN_ROLE: int = int(qt.Qt.ItemDataRole.UserRole) + 10

# The bar is sized like the action bars it sits next to (the session editor
# footer, the text differ footer), so the two read as the same chrome. It
# spans the full width of its container: the field runs edge to edge, with
# only the vertical breathing room the action bars use.
BAR_HEIGHT: int = 28
BAR_MARGINS: tuple[int, int, int, int] = (0, 0, 0, 2)
BAR_SPACING: int = 8

# Decides whether a row is kept visible no matter what the filter says. The
# sessions editor uses it for the half-created rows, a filtered out "new
# session" row would otherwise look like the action did nothing.
AlwaysVisible = Callable[[qt.QStandardItem], bool]


def normalize_filter_text(text: str) -> str:
    """
    Reduce what the user typed to what is actually compared against.

    Surrounding whitespace is noise, and the comparison itself is done through
    a case insensitive pattern, so lowercasing here is only for the callers
    that want to compare or report the value themselves.
    """
    return str(text).strip().lower()


def build_filter_pattern(needle: str) -> qt.QRegularExpression:
    """
    Build a case insensitive pattern that matches the needle as a literal.

    The escaping is what makes '*', '?' and '.' mean themselves: without it the
    filter would silently turn into a wildcard search the first time a file name
    contains one of them. An empty needle yields an empty pattern, which
    matches every row.
    """
    return qt.QRegularExpression(
        qt.QRegularExpression.escape(normalize_filter_text(needle)),
        qt.QRegularExpression.PatternOption.CaseInsensitiveOption,
    )


def row_matches(item: qt.QStandardItem, needle: str) -> bool:
    """
    Return whether the text of *item* contains *needle*.

    The label of the row is compared, and so is every further column of it, so
    that a multi column tree (the found files views) is filtered on its whole
    row rather than on its first column alone.
    """
    return row_matches_pattern(item, build_filter_pattern(needle))


def row_matches_pattern(item: qt.QStandardItem, pattern: qt.QRegularExpression) -> bool:
    """Match *item* against an already built pattern (one per filtering pass)."""
    if not pattern.pattern():
        return True
    if pattern.match(item.text()).hasMatch():
        return True
    for column in range(1, item.columnCount()):
        cell = item.child(0, column)
        if cell is not None and pattern.match(cell.text()).hasMatch():
            return True
    return False


class TreeFilterBar(qt.QWidget):
    """
    The bar that carries a tree filter: one line, one field, one clear action.

    It is a plain container rather than a bare field so that a caller can add
    its own affordances next to it without every tree reinventing the
    geometry. Nothing here knows about trees; who gets filtered is decided by
    whoever connects to filter_changed. Both the field style and the theme's
    clear glyphs come from the shared FilterField, the same widget the Recent
    Files search box and the settings filter use, so every filter box in the
    app reads as one look.
    """

    filter_changed = qt.pyqtSignal(str)
    focus_in = qt.pyqtSignal()

    def __init__(
        self, parent: qt.QWidget | None = None, placeholder: str = "Filter"
    ) -> None:
        super().__init__(parent)
        self.setObjectName("tree_filter_bar")
        self.setFixedHeight(BAR_HEIGHT)
        layout: qt.QHBoxLayout = qt.QHBoxLayout()
        layout.setContentsMargins(*BAR_MARGINS)
        layout.setSpacing(BAR_SPACING)
        self.setLayout(layout)
        self.filter_edit: FilterField = FilterField(self, placeholder)
        self.filter_edit.setObjectName("tree_filter_edit")
        self.filter_edit.setToolTip("Type to filter the tree below (Escape clears)")
        self.filter_edit.focus_in.connect(self.focus_in)
        layout.addWidget(self.filter_edit)
        self.filter_edit.textChanged.connect(self.filter_changed)

    def filter_text(self) -> str:
        """Return the current filter text, stripped of the surrounding blanks."""
        return self.filter_edit.text().strip()

    def set_filter_text(self, text: str) -> None:
        """Set the filter text without emitting filter_changed again."""
        if self.filter_edit.text() == text:
            return
        self.filter_edit.blockSignals(True)
        try:
            self.filter_edit.setText(text)
        finally:
            self.filter_edit.blockSignals(False)

    def clear_filter(self) -> None:
        self.filter_edit.clear()

    def focus_filter(self) -> None:
        """Put the keyboard on the field, selecting what is already in it."""
        self.filter_edit.setFocus()
        self.filter_edit.selectAll()

    def apply_theme(self, theme: dict[str, Any]) -> None:
        """
        Style the bar with the colours of the active theme.

        The bar itself carries the neutral background and the hairline that
        separates it from the tree below, the same pair the action bars under a
        tree use. The field styles itself through the shared FilterField, so a
        theme change restyles the whole bar in one step.
        """
        self.setStyleSheet(
            """
#tree_filter_bar {{
    background-color: {background};
    border-bottom: 1px solid {border};
}}
""".format(
                background=theme["linemargin"]["background"],
                border=theme["scrollbar"]["handle"],
            )
        )
        self.filter_edit.apply_filter_style()


class SubstringFilterProxy(qt.QSortFilterProxyModel):
    """
    Filter a model on a case insensitive substring, keeping ancestors alive.

    This is the mechanism for a tree whose code is happy to translate indices:
    the rows the proxy drops leave the source model untouched, and a rebuild of
    that model is filtered again on its own. It is recursive, so a group stays
    visible while one of its sessions matches, and it filters on every column
    of a row.

    It never sorts. The trees rely on the order their model built (groups
    before sessions, drive rows first, ...), and a proxy sort would interleave
    a tree with its own container levels.
    """

    def __init__(
        self,
        parent: qt.QObject | None = None,
        always_visible: AlwaysVisible | None = None,
    ) -> None:
        super().__init__(parent)
        self.always_visible = always_visible
        self._needle: str = ""
        self.setFilterKeyColumn(-1)
        self.setRecursiveFilteringEnabled(True)
        self.setDynamicSortFilter(False)
        self.setFilterRegularExpression(build_filter_pattern(""))

    def filter_text(self) -> str:
        return self._needle

    def set_filter_text(self, text: str) -> None:
        needle = normalize_filter_text(text)
        if needle == self._needle:
            return
        self._needle = needle
        self.setFilterRegularExpression(build_filter_pattern(needle))

    def filterAcceptsRow(self, source_row: int, source_parent: qt.QModelIndex) -> bool:
        # PyQt6 has no sourceItem(), so the item is reached through the source
        # model. Note that a QSortFilterProxyModel in Qt calls this method
        # again for every row while it walks a level: keeping the exemption here
        # cheap matters, and returning True early lets Qt do the rest.
        if self.always_visible is not None:
            model: Any = self.sourceModel()
            if model is not None:
                item: qt.QStandardItem | None = model.itemFromIndex(
                    model.index(source_row, 0, source_parent)
                )
                if item is not None and self.always_visible(item):
                    return True
        return super().filterAcceptsRow(source_row, source_parent)


class HiddenRowFilter(qt.QObject):
    """
    Filter a QStandardItemModel in place, by hiding the rows that do not match.

    This is the mechanism for a tree whose code reads indices it never
    translated (TreeDisplay and TreeExplorer both call model.itemFromIndex on
    whatever a selection or a signal handed them). Hiding rows keeps every one
    of those indices valid, at the price of having to keep the hidden state
    itself up to date - which is what the model connections are for.

    Two details are load bearing:

    * Hiding a row does not deselect it. Qt writes the hidden role and stops
      there, so a row filtered out of sight would still be inside
      selectedIndexes() and would be deleted along with the visible ones. Every
      application therefore drops the hidden rows from the selection.
    * Writing the hidden role emits dataChanged *and* itemChanged, exactly like
      any other data change. Code that listens to itemChanged (the explorer
      treats it as "the row was renamed") has to recognise this one.

    The model is rebuilt row by row in places, so the re-application is
    coalesced onto the event loop; a caller that just finished populating a
    model and wants the rows settled can ask for apply_now() instead.
    """

    def __init__(
        self,
        parent: qt.QObject | None = None,
        always_visible: AlwaysVisible | None = None,
    ) -> None:
        super().__init__(parent)
        self.always_visible = always_visible
        self._needle: str = ""
        self._model: qt.QStandardItemModel | None = None
        self._view: qt.QTreeView | None = None
        self._pending: bool = False
        self._applying: bool = False
        self._on_model_change = self._schedule

    def filter_text(self) -> str:
        return self._needle

    @property
    def is_applying(self) -> bool:
        """
        True while this filter is writing the hidden role.

        A tree whose itemChanged handler means "the row was renamed" needs to
        tell its own writes apart from that handler, and it cannot do it from
        the argument: QStandardItemModel does emit itemChanged for the hidden
        role, but PyQt6 hands the slot a role of -1 rather than the role that
        actually changed (verified - the same write reaches a two-argument slot
        as (item, -1)). This flag is the discriminator that does work: the
        filter is inside its own write, and a rename never happens then.
        """
        return self._applying

    def set_filter_text(self, text: str) -> None:
        needle = normalize_filter_text(text)
        if needle == self._needle:
            return
        self._needle = needle
        self.apply_now()

    def attach(self, model: qt.QStandardItemModel | None, view: Any = None) -> None:
        """Filter *model* from now on, as it is shown in *view*."""
        self.detach()
        self._view = view
        self._model = model
        if model is None:
            return
        for signal in (
            model.modelReset,
            model.rowsInserted,
            model.rowsRemoved,
            model.dataChanged,
            model.layoutChanged,
        ):
            signal.connect(self._on_model_change)
        self.apply_now()

    def detach(self) -> None:
        """
        Stop filtering, forget the model, and leave every row visible.

        Clearing the hidden role matters: the rows this filter hid are still
        hidden in the model, and a filter that has been detached - because the
        tab is closing, or because it was re-attached to a different model -
        must not leave rows invisible with nothing left to bring them back.
        """
        self._pending = False
        if self._model is not None:
            self._clear_hidden_role()
            for signal in (
                self._model.modelReset,
                self._model.rowsInserted,
                self._model.rowsRemoved,
                self._model.dataChanged,
                self._model.layoutChanged,
            ):
                try:
                    signal.disconnect(self._on_model_change)
                except (TypeError, RuntimeError):
                    pass
        self._model = None
        self._view = None

    def _clear_hidden_role(self) -> None:
        """Drop the hidden role from every row of the attached model."""
        if self._model is None:
            return
        # _applying keeps the writes below from re-entering this filter, and
        # from the tree's own itemChanged handlers reacting to them.
        self._applying = True
        try:
            root: Any = self._model.invisibleRootItem()
            for row in range(root.rowCount()):
                self._unhide_subtree(root.child(row))
        finally:
            self._applying = False

    def _unhide_subtree(self, item: qt.QStandardItem | None) -> None:
        """Clear the hidden marker on *item* and everything below it."""
        if item is None:
            return
        for row in range(item.rowCount()):
            self._unhide_subtree(item.child(row))
        if item.data(HIDDEN_ROLE):
            item.setData(None, HIDDEN_ROLE)
        self._set_view_hidden(item, False)

    def _schedule(self, *args: Any) -> None:
        """Re-apply once the current burst of model changes has settled."""
        if self._pending or self._applying:
            return
        self._pending = True
        qt.QTimer.singleShot(0, self.apply_now)

    def apply_now(self) -> None:
        """Hide the rows that do not match, right now."""
        self._pending = False
        if self._model is None or self._applying:
            return
        self._applying = True
        try:
            pattern = build_filter_pattern(self._needle)
            root: Any = self._model.invisibleRootItem()
            for row in range(root.rowCount()):
                self._apply_row(root.child(row), pattern)
            self._clear_hidden_selection()
        finally:
            self._applying = False

    def _apply_row(
        self, item: qt.QStandardItem | None, pattern: qt.QRegularExpression
    ) -> bool:
        """
        Hide *item* unless it or one of its descendants matches.

        Returns whether the row has to stay visible. A row that matches on its
        own text keeps its whole subtree: the user asked for that group, and a
        group whose rows were all filtered away reads as an empty heading
        rather than as a group.
        """
        if item is None:
            return True
        needle = self._needle
        if needle == "":
            self._set_hidden(item, False)
            for row in range(item.rowCount()):
                self._apply_row(item.child(row), pattern)
            return True
        if row_matches_pattern(item, pattern) or (
            self.always_visible is not None and self.always_visible(item)
        ):
            self._unhide_subtree(item)
            return True
        child_visible = False
        for row in range(item.rowCount()):
            if self._apply_row(item.child(row), pattern):
                child_visible = True
        self._set_hidden(item, not child_visible)
        return child_visible

    def _set_hidden(self, item: qt.QStandardItem, hidden: bool) -> None:
        """Mark *item* as hidden (or not), in the model and in the view.

        The role and the view state are written independently, so a stale view
        leaves nothing behind: whichever half disagrees with *hidden* is reset,
        the other half is left alone. Writing the role does fire itemChanged,
        which is why the guard in `is_applying` exists; the view write below
        changes no model data, so it emits nothing.
        """
        if bool(item.data(HIDDEN_ROLE)) != hidden:
            item.setData(hidden, HIDDEN_ROLE)
        self._set_view_hidden(item, hidden)

    def _set_view_hidden(self, item: qt.QStandardItem, hidden: bool) -> None:
        """Mirror *hidden* to the row state of the attached view.

        This is what actually takes a row off the screen: QTreeView does not
        read the hidden marker, it keeps a per-row state of its own, and only
        that state is consulted when the rows are laid out and painted. The
        state is keyed by row number, so a model that grew or shrank above the
        row shifts it - re-applying the filter rewrites every row anyway.
        """
        view = self._view
        if view is None or self._model is None or view.model() is not self._model:
            return
        row = item.row()
        if row < 0:
            return
        parent = item.parent()
        parent_index: qt.QModelIndex = (
            parent.index() if parent is not None else qt.QModelIndex()
        )
        if view.isRowHidden(row, parent_index) != hidden:
            view.setRowHidden(row, parent_index, hidden)

    def _clear_hidden_selection(self) -> None:
        """Deselect the rows that are no longer visible."""
        view = self._view
        if view is None:
            return
        selection_model: Any = view.selectionModel()
        if selection_model is None:
            return
        hidden_indexes = [
            index
            for index in selection_model.selectedIndexes()
            if index.data(HIDDEN_ROLE)
        ]
        if not hidden_indexes:
            return
        # PyQt6 has no overload for a list of indexes, so they go one by one.
        for index in hidden_indexes:
            selection_model.select(
                index,
                qt.QItemSelectionModel.SelectionFlag.Deselect
                | qt.QItemSelectionModel.SelectionFlag.Rows,
            )
        current = selection_model.currentIndex()
        if current.isValid() and current.data(HIDDEN_ROLE):
            selection_model.setCurrentIndex(
                qt.QModelIndex(), qt.QItemSelectionModel.SelectionFlag.NoUpdate
            )
