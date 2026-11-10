"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

##  FILE DESCRIPTION:
##      Resize reflow: rebuild the scrollback + screen stack by re-wrapping
##      logical lines to a new column count.
##
##      pyte's HistoryScreen.resize() clips columns from the right and drops
##      screen lines from the top; it never re-wraps, so widening a window
##      destroys a wrapped line and narrowing one truncates it. This module
##      reconstructs the logical lines - screen rows joined by the wrap mark
##      ExtendedScreen records while drawing - and re-wraps them to the new
##      width.
##
##      It also reports a position map, so the cursor, the inline images and
##      the view's scroll anchor can follow their text instead of pointing at
##      whatever moved into the old row.
##
##      The visible window is pinned to the bottom of the content (the blank
##      rows below the cursor are padding, not scrollback), and a resize that
##      leaves the column count alone takes a vertical-only fast path that
##      re-slices the source rows instead of copying a single cell - that is
##      what a height drag on the window border hits on every event.
##
##      Rows are built through a make_row(cells, wrapped) callback, so this
##      module never has to know the screen's row class.
##
##      No Qt imports on purpose: this is pure state and is tested standalone.

from bisect import bisect_right
from typing import Any, Callable, List, Optional, Sequence, Tuple

from gui.terminal.graphemes import cluster_width

# A cell whose data is a single space with no background and no reverse video
# is padding, not content: re-wrapping trims it so a short line stays one row.
# A styled space is kept, because it paints (progress bars, prompt backgrounds).
_PAD_DATA: str = " "


def cell_width(cell: Any) -> int:
    """Columns a cell occupies in a re-wrapped row.

    0 is a wide character's stub (the wide cell already claimed both columns),
    2 is a wide character or emoji cluster itself, everything else - including
    a zero-width codepoint pyte stored on its own - is one column.
    """
    data: str = cell.data
    if not data:
        return 0
    return 2 if cluster_width(data) == 2 else 1


def is_padding(cell: Any) -> bool:
    """True when the cell only pads the row out to the old column count."""
    return (
        cell.data == _PAD_DATA
        and getattr(cell, "bg", "default") == "default"
        and not getattr(cell, "reverse", False)
    )


class _LogicalLine:
    """One logical line: every cell of the screen rows it was wrapped over."""

    __slots__ = (
        "cells",
        "widths",
        "row_offsets",
        "start_row",
        "width",
        "starts",
        "base",
    )

    def __init__(self, start_row: int) -> None:
        self.cells: List[Any] = []
        self.widths: List[int] = []
        # Column offset, relative to the start of this logical line, at which
        # each source row begins.
        self.row_offsets: List[int] = []
        self.start_row: int = start_row
        self.width: int = 0
        # Offsets at which each output row starts (relative to this line).
        self.starts: List[int] = []
        # Index of this line's first output row in the whole stack.
        self.base: int = 0

    def append_row(self, row: Any, columns: int) -> None:
        self.row_offsets.append(self.width)
        for x in range(columns):
            cell: Any = row[x]
            self.cells.append(cell)
            width: int = cell_width(cell)
            self.widths.append(width)
            self.width += width

    def trim(self, keep: int, default_char: Any) -> None:
        """Drop trailing padding, but never past *keep* (the cursor column)."""
        while self.cells and self.width > keep and is_padding(self.cells[-1]):
            self.width -= self.widths.pop()
            self.cells.pop()
        while self.width < keep:
            self.cells.append(default_char)
            self.widths.append(1)
            self.width += 1


class ReflowResult:
    """The rebuilt stack plus the old -> new position map.

    ``history`` and ``screen`` are row objects built by the caller's row
    factory, already in stack coordinates: history first, then the visible
    screen rows (exactly *new_lines* of them).
    """

    __slots__ = (
        "history",
        "screen",
        "cursor_row",
        "cursor_col",
        "_lines",
        "_line_of_row",
        "_dropped",
        "_identity_columns",
    )

    def __init__(
        self,
        history: List[Any],
        screen: List[Any],
        cursor_row: int,
        cursor_col: int,
        lines: List[_LogicalLine],
        line_of_row: List[int],
        dropped: int,
        identity_columns: Optional[int] = None,
    ) -> None:
        self.history: List[Any] = history
        self.screen: List[Any] = screen
        self.cursor_row: int = cursor_row
        self.cursor_col: int = cursor_col
        self._lines: List[_LogicalLine] = lines
        self._line_of_row: List[int] = line_of_row
        self._dropped: int = dropped
        # Set by the width-unchanged fast path, whose rows are the source rows
        # themselves: a stack row maps to itself, shifted by the dropped history
        # rows, without a per-cell position lookup.
        self._identity_columns: Optional[int] = identity_columns

    @property
    def history_len(self) -> int:
        return len(self.history)

    def map_position(self, old_row: int, old_column: int) -> Optional[Tuple[int, int]]:
        """Stack position of a cell that was at (*old_row*, *old_column*).

        None when the text fell out of the retained stack (the history bound
        dropped it, or the cursor-visibility window did).
        """
        if self._identity_columns is not None:
            row: int = old_row - self._dropped
            if row < 0 or row >= self.history_len + len(self.screen):
                return None
            return row, max(0, old_column)
        if old_row < 0 or old_row >= len(self._line_of_row):
            return None
        line: _LogicalLine = self._lines[self._line_of_row[old_row]]
        offset: int = line.row_offsets[old_row - line.start_row] + max(0, old_column)
        if offset > line.width:
            offset = line.width
        index: int = bisect_right(line.starts, offset) - 1
        if index < 0:
            index = 0
        row = line.base + index - self._dropped
        column: int = offset - line.starts[index]
        if row < 0 or row >= self.history_len + len(self.screen):
            return None
        return row, column

    def map_row(self, old_row: int) -> Optional[int]:
        """Stack row the first cell of *old_row* moved to, or None."""
        position: Optional[Tuple[int, int]] = self.map_position(old_row, 0)
        if position is None:
            return None
        return position[0]


def reflow(
    rows: Sequence[Any],
    old_columns: int,
    new_columns: int,
    new_lines: int,
    cursor_row: int,
    cursor_column: int,
    default_char: Any,
    history_maxlen: Optional[int],
    make_row: Callable[[List[Any], bool], Any],
) -> ReflowResult:
    """Re-wrap the whole stack to *new_columns* x *new_lines*.

    *rows* -- the old stack, oldest first (history rows, then the live screen).
    *cursor_row* -- the cursor's row in that same stack.
    *history_maxlen* -- the configured scrollback bound; older rows are
    dropped when the re-wrapped stack needs more history than that.
    *make_row* -- builds one output row from a padded cell list and its wrap
    mark, so this module never needs to know the screen's row class.
    """
    old_columns = max(old_columns, 1)
    new_columns = max(new_columns, 1)
    new_lines = max(new_lines, 1)
    cursor_row = max(0, min(cursor_row, len(rows) - 1))
    cursor_column = max(0, cursor_column)
    if old_columns == new_columns:
        # Nothing re-wraps: the stack only has to be re-windowed, and the
        # source rows can be reused as they are. Resizing the window height
        # takes this path on every event of a drag, so it must stay cheap.
        return _vertical_reflow(
            rows,
            new_columns,
            new_lines,
            cursor_row,
            cursor_column,
            default_char,
            history_maxlen,
            make_row,
        )

    logical: List[_LogicalLine] = []
    line_of_row: List[int] = []
    wrapped_before: bool = False
    for index, row in enumerate(rows):
        if not wrapped_before:
            logical.append(_LogicalLine(index))
        line: _LogicalLine = logical[-1]
        line_of_row.append(len(logical) - 1)
        line.append_row(row, old_columns)
        # The next row is a continuation of this one only when the zero-width
        # wrap mark says so; a line that merely filled the row and ended with
        # a newline carries no mark and starts a new logical line.
        wrapped_before = bool(getattr(row, "wrapped", False))
    if not logical:
        logical.append(_LogicalLine(0))
        line_of_row.append(0)

    cursor_line: _LogicalLine = logical[line_of_row[cursor_row]]
    cursor_offset: int = (
        cursor_line.row_offsets[cursor_row - cursor_line.start_row] + cursor_column
    )
    cursor_offset = max(0, min(cursor_offset, cursor_line.width))
    for line in logical:
        # Only the cursor's line keeps padding out to the cursor: every other
        # line must lose its tail or a short line would gain a wrapped row.
        line.trim(cursor_offset if line is cursor_line else 0, default_char)

    out: List[Any] = []
    content: List[bool] = []
    for line in logical:
        line.base = len(out)
        starts: List[int] = [0]
        current: List[Any] = []
        consumed: int = 0
        for cell, width in zip(line.cells, line.widths):
            if width == 0:
                # Wide-character stub: the wide cell already claimed the slot.
                continue
            if width == 2 and new_columns < 2:
                width = 1
            if len(current) + width > new_columns:
                # The next cell does not fit (a full row, or a wide character
                # that would straddle the margin): pad the row and continue on
                # a new one, exactly as a real terminal re-wraps it.
                current.extend([default_char] * (new_columns - len(current)))
                out.append(make_row(current, True))
                content.append(True)
                starts.append(consumed)
                current = []
            current.append(cell)
            if width == 2:
                current.append(cell._replace(data=""))
            consumed += width
        has_content: bool = any(cell != default_char for cell in current)
        if len(current) < new_columns:
            current.extend([default_char] * (new_columns - len(current)))
        out.append(make_row(current, False))
        content.append(has_content)
        line.starts = starts

    cursor_line = logical[line_of_row[cursor_row]]
    cursor_index: int = bisect_right(cursor_line.starts, cursor_offset) - 1
    if cursor_index < 0:
        cursor_index = 0
    cursor_absolute: int = cursor_line.base + cursor_index
    cursor_new_column: int = cursor_offset - cursor_line.starts[cursor_index]

    # The window ends just below the last row that holds anything, or below the
    # cursor when the application left it further down; the blank rows a screen
    # carries below that point are padding, not scrollback, and must not push
    # the content above them into history. Each output row is always a whole
    # logical line, so the rows after the window are blank ones the viewport
    # never showed anyway.
    last_content: int = -1
    for index, has_content in enumerate(content):
        if has_content:
            last_content = index
    bottom: int = max(last_content + 1, cursor_absolute + 1)
    start: int = max(0, bottom - new_lines)
    if cursor_absolute < start:
        # The cursor was left above the content (the window would hide it):
        # it wins over showing the very bottom, as pyte's own resize does.
        start = cursor_absolute

    blanks: List[Any] = [default_char] * new_columns
    while len(out) < start + new_lines:
        out.append(make_row(list(blanks), False))

    dropped: int = 0
    if history_maxlen is not None and start > history_maxlen:
        dropped = start - history_maxlen

    cursor_final_row: int = cursor_absolute - start
    cursor_final_row = max(0, min(cursor_final_row, new_lines - 1))

    return ReflowResult(
        out[dropped:start],
        out[start : start + new_lines],
        cursor_final_row,
        min(cursor_new_column, new_columns),
        logical,
        line_of_row,
        dropped,
    )


def _vertical_reflow(
    rows: Sequence[Any],
    columns: int,
    new_lines: int,
    cursor_row: int,
    cursor_column: int,
    default_char: Any,
    history_maxlen: Optional[int],
    make_row: Callable[[List[Any], bool], Any],
) -> ReflowResult:
    """Re-window a stack whose column count did not change.

    Only the split between history and the visible screen can move, so the
    source rows are handed straight back: no cell is copied, no logical line is
    rebuilt. This is the path a height-only resize takes.
    """
    total: int = len(rows)
    if total == 0:
        rows = [make_row([default_char] * columns, False)]
        total = 1
    cursor_row = max(0, min(cursor_row, total - 1))
    last_content: int = -1
    for index in range(total - 1, -1, -1):
        row: Any = rows[index]
        if any(row[x] != default_char for x in range(columns)):
            last_content = index
            break
    bottom: int = max(last_content + 1, cursor_row + 1)
    start: int = max(0, bottom - new_lines)
    if cursor_row < start:
        start = cursor_row
    dropped: int = 0
    if history_maxlen is not None and start > history_maxlen:
        dropped = start - history_maxlen
    screen: List[Any] = list(rows[start : start + new_lines])
    blanks: List[Any] = [default_char] * columns
    while len(screen) < new_lines:
        screen.append(make_row(list(blanks), False))
    cursor_final_row: int = max(0, min(cursor_row - start, new_lines - 1))
    return ReflowResult(
        list(rows[dropped:start]),
        screen,
        cursor_final_row,
        min(cursor_column, columns),
        [],
        [],
        dropped,
        identity_columns=columns,
    )
