"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import difflib
import threading
import traceback
from typing import Any, NamedTuple

import constants
import functions
import qt
import settings
import components.actionfilter
import components.internals

from gui.customeditor import CustomEditor

"""
---------------------------------------------------------------------------
Object for displaying text difference between two files
---------------------------------------------------------------------------
"""

# Diff style tags emitted by `compute_diff_rows`. They match the
# `TextDiffer.INDICATOR_*` marker numbers used for rendering.
DIFF_UNIQUE_1 = 1
DIFF_UNIQUE_2 = 2
DIFF_SIMILAR = 3

# Marker masks used by the "find next difference" navigation.
MASK_UNIQUE = 0b0011
MASK_SIMILAR = 0b1100


class DiffResult(NamedTuple):
    """Aligned side-by-side rows for a text difference."""

    rows_1: list[str]
    rows_2: list[str]
    numbers_1: list[str]
    numbers_2: list[str]
    styles_1: list[int | None]
    styles_2: list[int | None]
    ranges_1: list[list[tuple[int, int]]]
    ranges_2: list[list[tuple[int, int]]]


def _split_lines(text: str) -> list[str]:
    """Split text into display lines, normalizing line endings."""
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    return [line[:-1] if line.endswith("\r") else line for line in lines]


def _diff_ranges(
    text_1: str, text_2: str
) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    """Return the differing substrings of two lines as [start, end) character ranges."""
    if text_1 == text_2 or not text_1 or not text_2:
        return [], []
    prefix = 0
    limit = min(len(text_1), len(text_2))
    while prefix < limit and text_1[prefix] == text_2[prefix]:
        prefix += 1
    suffix = 0
    while (
        suffix < len(text_1) - prefix
        and suffix < len(text_2) - prefix
        and text_1[len(text_1) - 1 - suffix] == text_2[len(text_2) - 1 - suffix]
    ):
        suffix += 1
    ranges_1: list[tuple[int, int]] = []
    ranges_2: list[tuple[int, int]] = []
    if prefix < len(text_1) - suffix:
        ranges_1.append((prefix, len(text_1) - suffix))
    if prefix < len(text_2) - suffix:
        ranges_2.append((prefix, len(text_2) - suffix))
    return ranges_1, ranges_2


def compute_diff_rows(text_1: str, text_2: str) -> DiffResult:
    """Align the lines of two texts into side-by-side diff rows.

    The two texts are split into lines, then aligned block-by-block with
    `difflib.SequenceMatcher`. Each output row carries the display line for
    both sides (an empty string marks a filler), the original line numbers,
    a style tag (one of the `DIFF_*` constants or `None`), and the character
    ranges that differ within replaced lines.
    """
    lines_1 = _split_lines(text_1)
    lines_2 = _split_lines(text_2)
    rows_1: list[str] = []
    rows_2: list[str] = []
    numbers_1: list[str] = []
    numbers_2: list[str] = []
    styles_1: list[int | None] = []
    styles_2: list[int | None] = []
    ranges_1: list[list[tuple[int, int]]] = []
    ranges_2: list[list[tuple[int, int]]] = []
    line_counter_1 = 1
    line_counter_2 = 1

    def emit(
        line_1: str,
        line_2: str,
        number_1: str,
        number_2: str,
        style_1: int | None,
        style_2: int | None,
        range_1: list[tuple[int, int]] | None = None,
        range_2: list[tuple[int, int]] | None = None,
    ) -> None:
        """Append one aligned diff row to the result columns."""
        rows_1.append(line_1)
        rows_2.append(line_2)
        numbers_1.append(number_1)
        numbers_2.append(number_2)
        styles_1.append(style_1)
        styles_2.append(style_2)
        ranges_1.append(range_1 if range_1 is not None else [])
        ranges_2.append(range_2 if range_2 is not None else [])

    matcher = difflib.SequenceMatcher(a=lines_1, b=lines_2, autojunk=False)
    for opcode, i_1, i_2, j_1, j_2 in matcher.get_opcodes():
        if opcode == "equal":
            for index in range(i_1, i_2):
                line = lines_1[index]
                emit(line, line, str(line_counter_1), str(line_counter_2), None, None)
                line_counter_1 += 1
                line_counter_2 += 1
        elif opcode == "delete":
            for index in range(i_1, i_2):
                emit(
                    lines_1[index],
                    "",
                    str(line_counter_1),
                    "",
                    DIFF_UNIQUE_1,
                    None,
                )
                line_counter_1 += 1
        elif opcode == "insert":
            for index in range(j_1, j_2):
                emit(
                    "",
                    lines_2[index],
                    "",
                    str(line_counter_2),
                    None,
                    DIFF_UNIQUE_2,
                )
                line_counter_2 += 1
        elif opcode == "replace":
            side_1 = lines_1[i_1:i_2]
            side_2 = lines_2[j_1:j_2]
            for index in range(min(len(side_1), len(side_2))):
                line_1 = side_1[index]
                line_2 = side_2[index]
                range_1, range_2 = _diff_ranges(line_1, line_2)
                emit(
                    line_1,
                    line_2,
                    str(line_counter_1),
                    str(line_counter_2),
                    DIFF_SIMILAR,
                    DIFF_SIMILAR,
                    range_1,
                    range_2,
                )
                line_counter_1 += 1
                line_counter_2 += 1
            for index in range(min(len(side_1), len(side_2)), len(side_1)):
                emit(
                    side_1[index],
                    "",
                    str(line_counter_1),
                    "",
                    DIFF_UNIQUE_1,
                    None,
                )
                line_counter_1 += 1
            for index in range(min(len(side_1), len(side_2)), len(side_2)):
                emit(
                    "",
                    side_2[index],
                    "",
                    str(line_counter_2),
                    None,
                    DIFF_UNIQUE_2,
                )
                line_counter_2 += 1
    return DiffResult(
        rows_1,
        rows_2,
        numbers_1,
        numbers_2,
        styles_1,
        styles_2,
        ranges_1,
        ranges_2,
    )


def diff_tab_text(text_1_name: str, text_2_name: str) -> str:
    """Format the caption shown on a text-difference tab.

    Shared by tab creation and swap_sides so the two cannot drift apart.
    """
    return "DIFF({:s} / {:s})".format(text_1_name, text_2_name)


class TextDiffer(qt.QWidget):
    """A widget that holds two editors for displaying text difference"""

    # Class variables
    _parent: Any = None
    main_form: Any = None
    name: str = ""
    savable = constants.CanSave.NO
    current_icon: Any = None
    internals: Any = None
    focused_editor: Any = None
    text_1: str | None = None
    text_2: str | None = None
    text_1_name: str = ""
    text_2_name: str = ""
    text_1_path: str | None = None
    text_2_path: str | None = None
    # File-type keyword each pane's lexer was resolved from ("text" for an
    # unsaved or unmapped document). Stored so a theme change can re-apply the
    # same lexer instead of resetting both panes to plain text.
    _lexer_1: str = "text"
    _lexer_2: str = "text"
    # Emitted by the diff worker thread as (generation, result). Queued to the
    # GUI thread, where _diff_computed applies it.
    diff_computed = qt.pyqtSignal(object)
    # Class constants
    MARGIN_STYLE = qt.QsciScintilla.STYLE_LINENUMBER
    INDICATOR_UNIQUE_1 = 1
    Indicator_Unique_1_Color = qt.QColor(0x72, 0x9F, 0xCF, 80)
    INDICATOR_UNIQUE_2 = 2
    Indicator_Unique_2_Color = qt.QColor(0xAD, 0x7F, 0xA8, 80)
    INDICATOR_SIMILAR = 3
    Indicator_Similar_Color = qt.QColor(0x8A, 0xE2, 0x34, 80)
    GET_X_OFFSET = qt.QsciScintillaBase.SCI_GETXOFFSET
    SET_X_OFFSET = qt.QsciScintillaBase.SCI_SETXOFFSET
    UPDATE_H_SCROLL = qt.QsciScintillaBase.SC_UPDATE_H_SCROLL
    UPDATE_V_SCROLL = qt.QsciScintillaBase.SC_UPDATE_V_SCROLL
    # Diff icons
    icon_unique_1 = None
    icon_unique_2 = None
    icon_similar = None
    # Marker references
    marker_unique_1: int
    marker_unique_2: int
    marker_unique_symbol_1: int
    marker_unique_symbol_2: int
    marker_similar_1: int
    marker_similar_2: int
    marker_similar_symbol_1: int
    marker_similar_symbol_2: int
    # Child widgets
    splitter: Any = None
    editor_1: CustomEditor
    editor_2: CustomEditor
    main_layout: Any = None
    toolbar: qt.QWidget
    label_1: qt.QPushButton
    label_2: qt.QPushButton
    diff_stat_unique_1: qt.QLabel
    diff_stat_unique_2: qt.QLabel
    diff_stat_similar: qt.QLabel
    swap_button: qt.QPushButton
    re_diff_button: qt.QPushButton
    next_unique_1_button: qt.QPushButton
    next_unique_2_button: qt.QPushButton
    next_similar_button: qt.QPushButton
    # Indicator ranges painted on each editor (position, length)
    _indicator_ranges_1: list[tuple[int, int]]
    _indicator_ranges_2: list[tuple[int, int]]
    # Set once shutdown() (or __del__) has detached the editors, so teardown is
    # idempotent and a second call is a cheap no-op
    _torn_down: bool = False
    # Monotonic counter identifying the most recent compare() request. A worker
    # result whose generation is stale is dropped instead of applied.
    _diff_generation: int = 0
    # Set in shutdown() so a running worker stops instead of emitting into a
    # widget that is going away
    _worker_stop: threading.Event
    _worker_thread: threading.Thread | None = None
    # Default cap, overridable by the "text_differ_async_line_limit" editor
    # setting. Below the cap the diff is computed inline, which keeps small
    # comparisons instantaneous and off the event loop entirely.
    DIFF_ASYNC_LINE_LIMIT_DEFAULT = 20000

    def _detach_editors(self) -> None:
        """
        Break the editor->differ back-references.

        The editors outlive this call only until Qt destroys them with their
        parent, so nothing here may touch the child widgets' own state: the
        event filter and the four signal connections are what would keep the
        differ alive, and both have to go for the widget to be collectable.
        A running diff worker is a referrer too, and would otherwise be able to
        emit into a widget that is being torn down.
        """
        if self._torn_down:
            return
        self._torn_down = True
        self._stop_diff_worker()
        for editor, scn_slot, cursor_slot in (
            (self.editor_1, self._scn_updateui_1, self._cursor_change_1),
            (self.editor_2, self._scn_updateui_2, self._cursor_change_2),
        ):
            try:
                editor.removeEventFilter(self)
                editor.SCN_UPDATEUI.disconnect(scn_slot)
                editor.cursorPositionChanged.disconnect(cursor_slot)
            except (RuntimeError, TypeError):
                # The editor is already finalized, or this slot was never
                # connected on this instance (the differ is built through
                # __new__ in the test suite).
                pass

    def shutdown(self) -> None:
        """
        Release the differ's resources when its tab is closed.

        tabwidget.close_tab() prefers an explicit shutdown() over the legacy
        __del__ convention, so this is the teardown path in normal use.
        """
        self._detach_editors()
        self.deleteLater()

    def __del__(self):
        # Safety net for a differ that is dropped without close_tab() ever
        # calling shutdown(). Real teardown is shutdown(); this only detaches
        # the back-references and never mutates the child editors, so running
        # it late (during collection) cannot leave a None where a method is
        # expected.
        try:
            self._detach_editors()
        except Exception:
            pass

    def __init__(
        self,
        parent: qt.QWidget,
        main_form: Any,
        text_1: str | None = None,
        text_2: str | None = None,
        text_1_name: str = "",
        text_2_name: str = "",
        text_1_path: str | None = None,
        text_2_path: str | None = None,
    ) -> None:
        """Initialization"""
        # Initialize the superclass
        super().__init__(parent)
        # Initialize components
        self.internals = components.internals.Internals(self, parent)
        # Initialize colors according to theme
        self.Indicator_Unique_1_Color = qt.QColor(
            settings.get_theme()["textdiffercolors"]["indicator-unique-1-color"]
        )
        self.Indicator_Unique_2_Color = qt.QColor(
            settings.get_theme()["textdiffercolors"]["indicator-unique-2-color"]
        )
        self.Indicator_Similar_Color = qt.QColor(
            settings.get_theme()["textdiffercolors"]["indicator-similar-color"]
        )
        # Store the reference to the parent
        self._parent = parent
        # Store the reference to the main form
        self.main_form = main_form
        # Store the source paths (may be None for unsaved documents)
        self.text_1_path = text_1_path
        self.text_2_path = text_2_path
        # Set the differ icon
        self.current_icon = functions.create_icon("tango_icons/compare-text.png")
        # Set the name of the differ widget
        if text_1_name is not None and text_2_name is not None:
            self.text_1_name = text_1_name
            self.text_2_name = text_2_name
        else:
            self.text_1_name = "TEXT 1"
            self.text_2_name = "TEXT 2"
        self.name = self._diff_title()
        # Initialize diff icons
        self.icon_unique_1 = functions.create_icon("tango_icons/diff-unique-1.png")
        self.icon_unique_2 = functions.create_icon("tango_icons/diff-unique-2.png")
        self.icon_similar = functions.create_icon("tango_icons/diff-similar.png")
        # Create the horizontal splitter and two editor widgets
        self.splitter = qt.QSplitter(qt.Qt.Orientation.Horizontal, self)
        self.editor_1 = CustomEditor(self, main_form)
        self.init_editor(self.editor_1)
        self.editor_2 = CustomEditor(self, main_form)
        self.init_editor(self.editor_2)
        self._resolve_pane_lexers()
        self.splitter.addWidget(self.editor_1)
        self.splitter.addWidget(self.editor_2)
        self.main_layout = qt.QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.splitter)
        # Set the layout
        self.setLayout(self.main_layout)
        # Create the toolbar
        self._create_toolbar()
        # Connect the necessary signals
        self.editor_1.SCN_UPDATEUI.connect(self._scn_updateui_1)
        self.editor_2.SCN_UPDATEUI.connect(self._scn_updateui_2)
        self.editor_1.cursorPositionChanged.connect(self._cursor_change_1)
        self.editor_2.cursorPositionChanged.connect(self._cursor_change_2)
        # Overwrite the CustomEditor parent widgets to point to the TextDiffers' PARENT
        self.editor_1._parent = self._parent
        self.editor_2._parent = self._parent
        # Add a new attribute to the CustomEditor that will hold the TextDiffer reference
        self.editor_1.actual_parent = self
        self.editor_2.actual_parent = self
        # Set the embedded flag
        self.editor_1.embedded = True
        self.editor_2.embedded = True

        # Track which editor the user last interacted with, so that navigation
        # and the mirrored scroll follow the pane under the mouse. The differ's
        # setFocus() forwards focus *into* self.focused_editor, so the pointer
        # has to be updated before focus settles; an event filter does that
        # without replacing any method on the editor.
        self._torn_down = False
        for editor in (self.editor_1, self.editor_2):
            editor.installEventFilter(self)
        # Focus the first editor on initialization
        self.focused_editor = self.editor_1
        self.focused_editor.setFocus()
        # Initialize markers
        self.init_markers()
        # Initialize the indicator range tracking
        self._indicator_ranges_1 = []
        self._indicator_ranges_2 = []
        # Initialize the scroll synchronization guard
        self._syncing_scroll = False
        # Initialize the off-thread diff plumbing
        self._worker_stop = threading.Event()
        self._diff_generation = 0
        self.diff_computed.connect(self._diff_computed)
        # Set the theme
        self.set_theme(settings.get_theme())
        # Bind the next-difference keyboard shortcuts
        self._create_navigation_shortcuts()
        # Request a jump to the first difference as the text is opened
        self._jump_to_first_diff = True
        # Check the text validity
        if text_1 is None or text_2 is None:
            # One of the texts is unspecified
            return
        # Create the diff
        self.compare(text_1, text_2)

    def _create_toolbar(self) -> None:
        """Create a structured footer bar with side badges, diff stats and actions."""
        self.toolbar = qt.QWidget(self)
        self.toolbar.setObjectName("text_differ_toolbar")
        self.toolbar.setFixedHeight(28)
        toolbar_layout = qt.QHBoxLayout()
        toolbar_layout.setContentsMargins(8, 2, 8, 2)
        toolbar_layout.setSpacing(8)
        self.toolbar.setLayout(toolbar_layout)

        self.label_1 = qt.QPushButton("", self.toolbar)
        self.label_1.setObjectName("text_differ_side_1")
        self.label_1.setFlat(True)
        self.label_1.clicked.connect(self._open_side_1)
        toolbar_layout.addWidget(self.label_1)

        self._make_vline(toolbar_layout)
        self.diff_stat_unique_1 = self._make_stat_label(
            "text_differ_stat_unique_1", toolbar_layout
        )
        self._make_vline(toolbar_layout)
        self.diff_stat_unique_2 = self._make_stat_label(
            "text_differ_stat_unique_2", toolbar_layout
        )
        self._make_vline(toolbar_layout)
        self.diff_stat_similar = self._make_stat_label(
            "text_differ_stat_similar", toolbar_layout
        )

        toolbar_layout.addStretch()

        self.next_unique_1_button = qt.QPushButton(self.toolbar)
        self.next_unique_1_button.setObjectName("text_differ_action_button")
        self.next_unique_1_button.setIcon(
            functions.create_icon("tango_icons/diff-unique-1.png")
        )
        self.next_unique_1_button.setToolTip(
            "Scroll to next unique line\nin document: '{:s}'".format(self.text_1_name)
        )
        self.next_unique_1_button.setFlat(True)
        self.next_unique_1_button.clicked.connect(self.find_next_unique_1)
        toolbar_layout.addWidget(self.next_unique_1_button)

        self.next_unique_2_button = qt.QPushButton(self.toolbar)
        self.next_unique_2_button.setObjectName("text_differ_action_button")
        self.next_unique_2_button.setIcon(
            functions.create_icon("tango_icons/diff-unique-2.png")
        )
        self.next_unique_2_button.setToolTip(
            "Scroll to next unique line\nin document: '{:s}'".format(self.text_2_name)
        )
        self.next_unique_2_button.setFlat(True)
        self.next_unique_2_button.clicked.connect(self.find_next_unique_2)
        toolbar_layout.addWidget(self.next_unique_2_button)

        self.next_similar_button = qt.QPushButton(self.toolbar)
        self.next_similar_button.setObjectName("text_differ_action_button")
        self.next_similar_button.setIcon(
            functions.create_icon("tango_icons/diff-similar.png")
        )
        self.next_similar_button.setToolTip(
            "Scroll to next similar line\nin both documents"
        )
        self.next_similar_button.setFlat(True)
        self.next_similar_button.clicked.connect(self.find_next_similar)
        toolbar_layout.addWidget(self.next_similar_button)

        self.swap_button = qt.QPushButton(self.toolbar)
        self.swap_button.setObjectName("text_differ_action_button")
        self.swap_button.setIcon(functions.create_icon("tango_icons/edit-redo.png"))
        self.swap_button.setToolTip("Swap the two sides")
        self.swap_button.setFlat(True)
        self.swap_button.clicked.connect(self.swap_sides)
        toolbar_layout.addWidget(self.swap_button)

        self.re_diff_button = qt.QPushButton(self.toolbar)
        self.re_diff_button.setObjectName("text_differ_action_button")
        self.re_diff_button.setIcon(
            functions.create_icon("tango_icons/view-refresh.png")
        )
        self.re_diff_button.setToolTip("Re-run the difference")
        self.re_diff_button.setFlat(True)
        self.re_diff_button.clicked.connect(self.re_diff)
        toolbar_layout.addWidget(self.re_diff_button)

        self._make_vline(toolbar_layout)
        self.label_2 = qt.QPushButton("", self.toolbar)
        self.label_2.setObjectName("text_differ_side_2")
        self.label_2.setFlat(True)
        self.label_2.clicked.connect(self._open_side_2)
        toolbar_layout.addWidget(self.label_2)

        self.main_layout.addWidget(self.toolbar)

    def _make_stat_label(self, object_name: str, layout: qt.QHBoxLayout) -> qt.QLabel:
        """Create a colour-coded statistics chip for the footer bar."""
        label = qt.QLabel("", self.toolbar)
        label.setObjectName(object_name)
        layout.addWidget(label)
        return label

    def _make_vline(self, layout: qt.QHBoxLayout) -> None:
        """Create a thin vertical separator for the footer bar."""
        line = qt.QWidget(self.toolbar)
        line.setObjectName("text_differ_vline")
        line.setFixedWidth(1)
        layout.addWidget(line)

    def _set_side_label(self, label: qt.QPushButton, name: str) -> None:
        """Label a side badge with a colour-coded bullet matching its diff accent.

        The bullet and name share the button's foreground colour; the accent is
        applied by the toolbar stylesheet via the button's object name.
        """
        label.setText("\u25cf {:s}".format(name))
        label.setToolTip("Open '{:s}' in the editor".format(name))

    @staticmethod
    def _solid_rgb(hex_color: str) -> str:
        """Reduce an ARGB theme colour to an opaque '#rrggbb' value."""
        color = hex_color.lstrip("#")
        if len(color) == 8:
            color = color[2:]
        return "#{:s}".format(color.upper())

    def _apply_toolbar_theme(self, theme: dict[str, Any]) -> None:
        """Style the footer bar with the colours of the active theme."""
        accent_1 = self._solid_rgb(
            theme["textdiffercolors"]["indicator-unique-1-color"]
        )
        accent_2 = self._solid_rgb(
            theme["textdiffercolors"]["indicator-unique-2-color"]
        )
        accent_similar = self._solid_rgb(
            theme["textdiffercolors"]["indicator-similar-color"]
        )
        background = theme["linemargin"]["background"]
        border = theme["scrollbar"]["handle"]
        button_border = theme["indication"]["passiveborder"]
        hover = theme["indication"]["hover"]
        style_sheet = """
#text_differ_toolbar {{
    background-color: {};
    border-top: 1px solid {};
}}
QPushButton#text_differ_side_1, QPushButton#text_differ_side_2,
QPushButton#text_differ_action_button {{
    background: transparent;
    border: none;
    padding: 1px 3px;
}}
QPushButton#text_differ_side_1, QPushButton#text_differ_side_2,
QPushButton#text_differ_action_button {{
    border: 1px solid {};
    border-radius: 3px;
}}
QPushButton#text_differ_side_1, QPushButton#text_differ_side_2 {{
    font-weight: bold;
}}
QPushButton#text_differ_side_1 {{ color: {}; }}
QPushButton#text_differ_side_2 {{ color: {}; }}
QPushButton#text_differ_side_1:hover, QPushButton#text_differ_side_2:hover,
QPushButton#text_differ_action_button:hover {{
    background: {};
}}
QLabel#text_differ_stat_unique_1 {{ color: {}; font-weight: bold; }}
QLabel#text_differ_stat_unique_2 {{ color: {}; font-weight: bold; }}
QLabel#text_differ_stat_similar {{ color: {}; font-weight: bold; }}
QWidget#text_differ_vline {{
    background-color: {};
    min-width: 1px;
    max-width: 1px;
}}
""".format(
            background,
            border,
            button_border,
            accent_1,
            accent_2,
            hover,
            accent_1,
            accent_2,
            accent_similar,
            border,
        )
        self.toolbar.setStyleSheet(style_sheet)
        self._set_side_label(self.label_1, self.text_1_name)
        self._set_side_label(self.label_2, self.text_2_name)

    def _diff_title(self) -> str:
        """Build the widget name for the current side assignment."""
        if self.text_1_name and self.text_2_name:
            return "Text difference: {:s} / {:s}".format(
                self.text_1_name, self.text_2_name
            )
        return "Text difference"

    def _open_side_1(self) -> None:
        """Open the first compared document in a real editor."""
        if self.text_1_path:
            self.main_form.open_file(self.text_1_path)

    def _open_side_2(self) -> None:
        """Open the second compared document in a real editor."""
        if self.text_2_path:
            self.main_form.open_file(self.text_2_path)

    def re_diff(self) -> None:
        """Re-run the difference on the stored texts."""
        if self.text_1 is not None and self.text_2 is not None:
            self.compare(self.text_1, self.text_2)

    def swap_sides(self) -> None:
        """Swap the two compared documents between the panes."""
        if self.text_1 is None or self.text_2 is None:
            return
        self.Indicator_Unique_1_Color, self.Indicator_Unique_2_Color = (
            self.Indicator_Unique_2_Color,
            self.Indicator_Unique_1_Color,
        )
        self.text_1, self.text_2 = self.text_2, self.text_1
        self.text_1_name, self.text_2_name = self.text_2_name, self.text_1_name
        self.text_1_path, self.text_2_path = self.text_2_path, self.text_1_path
        # Each pane's lexer belongs to the document in it, so it has to follow
        # the swap: after swapping, pane 1 holds the document whose path is
        # now text_1_path.
        self._lexer_1, self._lexer_2 = self._lexer_2, self._lexer_1
        self._reapply_pane_lexers()
        self._set_side_label(self.label_1, self.text_1_name)
        self._set_side_label(self.label_2, self.text_2_name)
        # The tab caption and the widget name name the two documents, so they
        # have to follow the swap as well.
        self.name = self._diff_title()
        self._parent.set_tab_name(
            self, diff_tab_text(self.text_1_name, self.text_2_name)
        )
        # The margin symbols carry each side's own icon. Redefine them
        # crosswise, in place, so they keep matching the background accents
        # that _apply_diff_colors repaints below.
        self.editor_1.markerDefine(self._image_unique_2, self.marker_unique_symbol_1)
        self.editor_2.markerDefine(self._image_unique_1, self.marker_unique_symbol_2)
        self._apply_diff_colors()
        self.compare(self.text_1, self.text_2)

    def _create_navigation_shortcuts(self) -> None:
        """Bind the next-difference shortcuts from the settings."""
        shortcuts = settings.get("keyboard-shortcuts")["general"]
        bindings = (
            (
                "_shortcut_unique_1",
                qt.QKeySequence(
                    shortcuts.get("text_difference_unique_1", "Ctrl+Alt+1")
                ),
                self.find_next_unique_1,
            ),
            (
                "_shortcut_unique_2",
                qt.QKeySequence(
                    shortcuts.get("text_difference_unique_2", "Ctrl+Alt+2")
                ),
                self.find_next_unique_2,
            ),
            (
                "_shortcut_similar",
                qt.QKeySequence(shortcuts.get("text_difference_similar", "Ctrl+Alt+3")),
                self.find_next_similar,
            ),
        )
        for attribute, sequence, slot in bindings:
            shortcut = qt.QShortcut(sequence, self)
            shortcut.activated.connect(slot)
            setattr(self, attribute, shortcut)

    def _update_stats(self, unique_1: int, unique_2: int, similar: int) -> None:
        """Update the colour-coded statistics chips in the footer bar."""
        self.diff_stat_unique_1.setText("{:d} unique".format(unique_1))
        self.diff_stat_unique_1.setToolTip(
            "Unique lines in '{:s}'".format(self.text_1_name)
        )
        self.diff_stat_unique_2.setText("{:d} unique".format(unique_2))
        self.diff_stat_unique_2.setToolTip(
            "Unique lines in '{:s}'".format(self.text_2_name)
        )
        self.diff_stat_similar.setText("{:d} similar".format(similar))
        self.diff_stat_similar.setToolTip("Similar lines in both documents")

    def _sync_scroll(self, source: qt.QsciScintilla, target: qt.QsciScintilla) -> None:
        """Synchronize the scroll position of the target with the source.

        The scroll positions are only written when they differ from the
        values already held by the target. QScintilla emits SCN_UPDATEUI
        for every scroll change, even when the position is unchanged, so
        unconditionally applying the source position to the target would
        drive an endless ping-pong of UI-update notifications between the
        two editors.
        """
        if self._syncing_scroll:
            return
        top_line = source.firstVisibleLine()
        x_offset = source.SendScintilla(self.GET_X_OFFSET)
        if (
            target.firstVisibleLine() == top_line
            and target.SendScintilla(self.GET_X_OFFSET) == x_offset
        ):
            return
        self._syncing_scroll = True
        try:
            target.SendScintilla(self.SET_X_OFFSET, x_offset)
            target.setFirstVisibleLine(top_line)
        finally:
            self._syncing_scroll = False

    def _scn_updateui_1(self, sc_update):
        """Propagate scroll changes from the first editor to the second."""
        if sc_update & (self.UPDATE_H_SCROLL | self.UPDATE_V_SCROLL):
            self._sync_scroll(self.editor_1, self.editor_2)

    def _scn_updateui_2(self, sc_update):
        """Propagate scroll changes from the second editor to the first."""
        if sc_update & (self.UPDATE_H_SCROLL | self.UPDATE_V_SCROLL):
            self._sync_scroll(self.editor_2, self.editor_1)

    def _cursor_change_1(self, line, index):
        """
        Function connected to the cursorPositionChanged signal for
        cursor position change detection
        """
        if self.focused_editor == self.editor_1:
            # Update the cursor position on the opposite editor
            cursor_line, cursor_index = self.editor_1.getCursorPosition()
            # Check if the opposite editor line is long enough
            if self.editor_2.lineLength(cursor_line) > cursor_index:
                self.editor_2.setCursorPosition(cursor_line, cursor_index)
            else:
                self.editor_2.setCursorPosition(cursor_line, 0)
            # Update the first visible line, so that the views in both differs match
            if not self._syncing_scroll:
                self._syncing_scroll = True
                try:
                    self.editor_2.setFirstVisibleLine(self.editor_1.firstVisibleLine())
                finally:
                    self._syncing_scroll = False

    def _cursor_change_2(self, line, index):
        """
        Function connected to the cursorPositionChanged signal for
        cursor position change detection
        """
        if self.focused_editor == self.editor_2:
            # Update the cursor position on the opposite editor
            cursor_line, cursor_index = self.editor_2.getCursorPosition()
            # Check if the opposite editor line is long enough
            if self.editor_1.lineLength(cursor_line) > cursor_index:
                self.editor_1.setCursorPosition(cursor_line, cursor_index)
            else:
                self.editor_1.setCursorPosition(cursor_line, 0)
            # Update the first visible line, so that the views in both differs match
            if not self._syncing_scroll:
                self._syncing_scroll = True
                try:
                    self.editor_1.setFirstVisibleLine(self.editor_2.firstVisibleLine())
                finally:
                    self._syncing_scroll = False

    def _update_margins(self):
        """Update the text margin width"""
        self.editor_1.setMarginWidth(0, "0" * len(str(self.editor_1.lines())))
        self.editor_2.setMarginWidth(0, "0" * len(str(self.editor_2.lines())))

    def _signal_editor_cursor_change(self, cursor_line=None, cursor_column=None):
        """Signal that fires when cursor position changes in one of the editors"""
        self.main_form.display.update_cursor_position(cursor_line, cursor_column)

    def find_text(
        self,
        search_text: str,
        case_sensitive: bool = False,
        search_forward: bool = True,
        regular_expression: bool = False,
    ) -> Any:
        """Forward a find request to the currently focused editor."""
        return self.focused_editor.find_text(
            search_text, case_sensitive, search_forward, regular_expression
        )

    def mousePressEvent(self, event):
        """Overloaded mouse click event"""
        # Execute the superclass mouse click event
        super().mousePressEvent(event)
        # Set focus to the clicked editor
        self.setFocus()
        # Set the last focused widget to the parent basic widget
        self.main_form.last_focused_widget = self._parent
        # Hide the function wheel if it is shown
        self.main_form.view.hide_all_overlay_widgets()
        # Reset the click&drag context menu action
        components.actionfilter.ActionFilter.clear_action()

    def eventFilter(self, object: qt.QObject, event: qt.QEvent) -> bool:  # type: ignore[override]
        """
        Record which editor the user last interacted with.

        Installed on both editors, this replaces the per-editor
        mousePressEvent/wheelEvent wrappers that used to be grafted on as
        instance attributes. Returning False leaves the event to the editor
        itself, so the only difference from the old wrappers is that no method
        on the editor is ever shadowed and nothing has to be undone in a
        destructor.
        """
        if object in (self.editor_1, self.editor_2) and event.type() in (
            qt.QEvent.Type.MouseButtonPress,
            qt.QEvent.Type.Wheel,
        ):
            self.focused_editor = object
        return super().eventFilter(object, event)

    def setFocus(self):
        """Overridden focus event"""
        # Execute the superclass focus function
        super().setFocus()
        # Check indication
        self.main_form.view.indication_check()
        # Focus the last focused editor
        self.focused_editor.setFocus()

    def init_margin(
        self,
        editor,
        marker_unique,
        marker_unique_symbol,
        marker_similar,
        marker_similar_symbol,
    ):
        """Initialize margin for coloring lines showing diff symbols"""
        editor.setMarginWidth(0, "0")
        # Setting the margin width to 0 makes the marker colour the entire line
        # to the marker background color
        editor.setMarginWidth(1, "00")
        editor.setMarginWidth(2, 0)
        editor.setMarginType(0, qt.QsciScintilla.MarginType.TextMargin)
        editor.setMarginType(1, qt.QsciScintilla.MarginType.SymbolMargin)
        editor.setMarginType(2, qt.QsciScintilla.MarginType.SymbolMargin)
        # I DON'T KNOW THE ENTIRE LOGIC BEHIND MARKERS AND MARGINS! If you set
        # something wrong in the margin mask, the markers on a different margin don't appear!
        # http://www.scintilla.org/ScintillaDoc.html#SCI_SETMARGINMASKN
        editor.setMarginMarkerMask(1, ~qt.QsciScintillaBase.SC_MASK_FOLDERS)
        editor.setMarginMarkerMask(2, 0x0)

    def _apply_diff_colors(self) -> None:
        """Push the current diff colours into the markers and indicators.

        Markers are created once, in init_markers, so a theme switch has to
        re-apply the colours. Otherwise the highlight backgrounds keep painting
        with the previous theme's accents, while the toolbar accents below
        them have already changed.
        """
        sides: list[tuple[CustomEditor, qt.QColor, int, int]] = [
            (
                self.editor_1,
                self.Indicator_Unique_1_Color,
                self.marker_unique_1,
                self.marker_similar_1,
            ),
            (
                self.editor_2,
                self.Indicator_Unique_2_Color,
                self.marker_unique_2,
                self.marker_similar_2,
            ),
        ]
        for editor, unique_color, unique_marker, similar_marker in sides:
            # Background colors only for the background markers
            editor.setMarkerBackgroundColor(unique_color, unique_marker)
            editor.setMarkerBackgroundColor(
                self.Indicator_Similar_Color, similar_marker
            )
            editor.setIndicatorForegroundColor(
                self.Indicator_Similar_Color, self.INDICATOR_SIMILAR
            )

    def init_markers(self):
        """Initialize all markers for showing diff symbols"""
        # Set the images
        image_scale_size = functions.create_size(16, 16)
        image_unique_1 = functions.create_pixmap("tango_icons/diff-unique-1.png")
        image_unique_2 = functions.create_pixmap("tango_icons/diff-unique-2.png")
        image_similar = functions.create_pixmap("tango_icons/diff-similar.png")
        # Scale the images to a smaller size
        self._image_unique_1 = image_unique_1.scaled(image_scale_size)
        self._image_unique_2 = image_unique_2.scaled(image_scale_size)
        self._image_similar = image_similar.scaled(image_scale_size)
        # Markers for editor 1
        self.marker_unique_1 = self.editor_1.markerDefine(
            qt.QsciScintilla.MarkerSymbol.Background, 0
        )
        self.marker_unique_symbol_1 = self.editor_1.markerDefine(
            self._image_unique_1, 1
        )
        self.marker_similar_1 = self.editor_1.markerDefine(
            qt.QsciScintilla.MarkerSymbol.Background, 2
        )
        self.marker_similar_symbol_1 = self.editor_1.markerDefine(
            self._image_similar, 3
        )
        # Margins for editor 1
        self.init_margin(
            self.editor_1,
            self.marker_unique_1,
            self.marker_unique_symbol_1,
            self.marker_similar_1,
            self.marker_similar_symbol_1,
        )
        # Markers for editor 2
        self.marker_unique_2 = self.editor_2.markerDefine(
            qt.QsciScintilla.MarkerSymbol.Background, 0
        )
        self.marker_unique_symbol_2 = self.editor_2.markerDefine(
            self._image_unique_2, 1
        )
        self.marker_similar_2 = self.editor_2.markerDefine(
            qt.QsciScintilla.MarkerSymbol.Background, 2
        )
        self.marker_similar_symbol_2 = self.editor_2.markerDefine(
            self._image_similar, 3
        )
        # Margins for editor 2
        self.init_margin(
            self.editor_2,
            self.marker_unique_2,
            self.marker_unique_symbol_2,
            self.marker_similar_2,
            self.marker_similar_symbol_2,
        )
        self._apply_diff_colors()

    def init_indicator(self, editor, indicator, color):
        """
        Set the indicator settings
        """
        editor.indicatorDefine(
            qt.QsciScintilla.IndicatorStyle.RoundBoxIndicator, indicator
        )
        editor.setIndicatorForegroundColor(color, indicator)
        editor.SendScintilla(qt.QsciScintillaBase.SCI_SETINDICATORCURRENT, indicator)

    def init_editor(self, editor: CustomEditor) -> None:
        """Initialize all of the PlainEditor settings for difference displaying"""
        editor.setLexer(None)
        editor.setUtf8(True)
        editor.setIndentationsUseTabs(False)
        editor.setBraceMatching(qt.QsciScintilla.BraceMatch.SloppyBraceMatch)
        editor.setMatchedBraceBackgroundColor(qt.QColor(255, 153, 0))
        editor.setAcceptDrops(False)
        editor.setEolMode(
            qt.QsciScintilla.EolMode(settings.get("editor")["end_of_line_mode"])
        )
        editor.setReadOnly(True)
        editor.savable = constants.CanSave.NO

    @staticmethod
    def _pane_lexer(path: str | None) -> str:
        """
        Resolve a pane's file-type keyword from its source path.

        get_file_type() is the same helper the editor tabs use, so a diff pane
        highlights exactly like the editor that would open the same file.
        check_content=False skips the shebang/XML sniffing, which would open
        the file on disk; the differ already holds the text, and a difference
        between an unsaved buffer and a file should read as the file's type.
        An absent or unmapped path yields "text", which is also what
        choose_lexer() falls back to for an unknown keyword.
        """
        if not path:
            return "text"
        return functions.get_file_type(path, check_content=False)

    def _resolve_pane_lexers(self) -> None:
        """Resolve and install the lexer for each pane."""
        self._lexer_1 = self._pane_lexer(self.text_1_path)
        self._lexer_2 = self._pane_lexer(self.text_2_path)
        self.editor_1.choose_lexer(self._lexer_1)
        self.editor_2.choose_lexer(self._lexer_2)

    def _reapply_pane_lexers(self) -> None:
        """
        Re-install the panes' own lexers, e.g. after a theme change.

        set_theme() reconfigures the editors from scratch and would otherwise
        put both panes back to plain text, losing the per-side highlighting.
        """
        self.editor_1.choose_lexer(self._lexer_1)
        self.editor_2.choose_lexer(self._lexer_2)

    def set_margin_text(self, editor, line, text):
        """Set the editor's margin text at the selected line"""
        editor.setMarginText(line, text, self.MARGIN_STYLE)

    def _set_character_range_indicator(self, editor, line, range_start, range_end):
        """Color a character range of a line with the 'similar' indicator"""
        start_position = editor.positionFromLineIndex(line, range_start)
        end_position = editor.positionFromLineIndex(line, range_end)
        length = end_position - start_position
        editor.SendScintilla(
            qt.QsciScintillaBase.SCI_INDICATORFILLRANGE, start_position, length
        )
        if editor is self.editor_1:
            self._indicator_ranges_1.append((start_position, length))
        else:
            self._indicator_ranges_2.append((start_position, length))

    def _async_line_limit(self) -> int:
        """Line-count cap above which the diff is computed off the GUI thread."""
        editor_settings: Any = settings.get("editor")
        # .get with a default, not [key]: the on-disk settings file is written
        # by older versions and load_settings() overwrites the nested dict
        # wholesale, so the key can legitimately be absent at runtime.
        limit = editor_settings.get(
            "text_differ_async_line_limit", self.DIFF_ASYNC_LINE_LIMIT_DEFAULT
        )
        try:
            return int(limit)
        except (TypeError, ValueError):
            return self.DIFF_ASYNC_LINE_LIMIT_DEFAULT

    def _needs_worker(self, text_1: str, text_2: str) -> bool:
        """
        Decide whether this comparison is large enough to be worth a thread.

        Counting newlines is exact for the cap and, unlike splitlines(), does
        not allocate an intermediate list of every line just to measure them.
        """
        line_count = text_1.count("\n") + text_2.count("\n")
        return line_count > self._async_line_limit()

    def _set_busy(self, busy: bool) -> None:
        """
        Show that a large diff is being computed, in the existing footer chips.

        No new widget: the three statistics labels are already the differ's
        status line, and _update_stats overwrites them when the result lands.
        """
        for label in (
            self.diff_stat_unique_1,
            self.diff_stat_unique_2,
            self.diff_stat_similar,
        ):
            label.setText("computing..." if busy else "")
            label.setToolTip("")

    def _start_worker(self, text_1: str, text_2: str, generation: int) -> None:
        """
        Compute the difference on a worker thread.

        compute_diff_rows is pure -- it touches no widget and no GUI state -- so
        the whole diff can run off the event loop. Only the result crosses back,
        through a queued signal, and it is applied on the GUI thread.
        """
        self._set_busy(True)
        self._worker_thread = threading.Thread(
            target=self._worker_entry,
            args=(text_1, text_2, generation),
            daemon=True,
        )
        self._worker_thread.start()

    def _worker_entry(self, text_1: str, text_2: str, generation: int) -> None:
        """Worker body: compute the diff and hand the result back."""
        try:
            result: DiffResult = compute_diff_rows(text_1, text_2)
        except Exception:
            # A worker thread must not raise into the Qt main loop; report on
            # the GUI thread like any other failure.
            traceback.print_exc()
            return
        if self._worker_stop.is_set():
            return
        self.diff_computed.emit((generation, result))

    def _diff_computed(self, payload: Any) -> None:
        """
        GUI-thread slot applying a worker result.

        The generation check drops a result that a newer compare() has already
        superseded, so a slow diff of large documents cannot overwrite a
        fresher one that was requested while it was running.
        """
        generation, result = payload
        if generation != self._diff_generation or self._torn_down:
            return
        self._set_busy(False)
        self._apply_result(result)

    def _stop_diff_worker(self) -> None:
        """Stop any in-flight diff worker and detach the result signal."""
        self._worker_stop.set()
        try:
            self.diff_computed.disconnect(self._diff_computed)
        except (TypeError, RuntimeError):
            pass

    def compare(self, text_1: str | None, text_2: str | None) -> None:
        """Compare two text strings and display the difference"""
        if text_1 is None or text_2 is None:
            return
        # Store the original text
        self.text_1 = text_1
        self.text_2 = text_2
        # A new request supersedes any worker result still in flight
        self._diff_generation += 1
        generation = self._diff_generation
        # Large comparisons go to a worker so the event loop keeps running;
        # everything else is computed inline, which is both faster and
        # synchronous for the caller.
        if self._needs_worker(text_1, text_2):
            self._start_worker(text_1, text_2, generation)
            return
        self._set_busy(False)
        self._apply_result(compute_diff_rows(text_1, text_2))

    def _apply_result(self, result: DiffResult) -> None:
        """
        Paint a computed difference. Runs only on the GUI thread.

        Everything here -- markers, margin text, indicators, the status messages
        and the first-difference jump -- touches widgets, so none of it may be
        reached from a worker.
        """
        # Clear the previous run's markers, margin texts and indicator ranges
        self.editor_1.markerDeleteAll(self.marker_unique_1)
        self.editor_1.markerDeleteAll(self.marker_unique_symbol_1)
        self.editor_1.markerDeleteAll(self.marker_similar_1)
        self.editor_1.markerDeleteAll(self.marker_similar_symbol_1)
        self.editor_2.markerDeleteAll(self.marker_unique_2)
        self.editor_2.markerDeleteAll(self.marker_unique_symbol_2)
        self.editor_2.markerDeleteAll(self.marker_similar_2)
        self.editor_2.markerDeleteAll(self.marker_similar_symbol_2)
        self.editor_1.clearMarginText()
        self.editor_2.clearMarginText()
        self.init_indicator(
            self.editor_1, self.INDICATOR_SIMILAR, self.Indicator_Similar_Color
        )
        self.init_indicator(
            self.editor_2, self.INDICATOR_SIMILAR, self.Indicator_Similar_Color
        )
        for start_position, length in self._indicator_ranges_1:
            self.editor_1.SendScintilla(
                qt.QsciScintillaBase.SCI_INDICATORCLEARRANGE, start_position, length
            )
        for start_position, length in self._indicator_ranges_2:
            self.editor_2.SendScintilla(
                qt.QsciScintillaBase.SCI_INDICATORCLEARRANGE, start_position, length
            )
        self._indicator_ranges_1 = []
        self._indicator_ranges_2 = []
        # Display the results
        self.editor_1.setText("\n".join(result.rows_1))
        self.editor_2.setText("\n".join(result.rows_2))
        # Set margins and style for both editors
        for index in range(len(result.rows_1)):
            self.set_margin_text(self.editor_1, index, result.numbers_1[index])
            style = result.styles_1[index]
            if style is not None:
                if style == self.INDICATOR_SIMILAR:
                    self.editor_1.markerAdd(index, self.marker_similar_1)
                    self.editor_1.markerAdd(index, self.marker_similar_symbol_1)
                else:
                    self.editor_1.markerAdd(index, self.marker_unique_1)
                    self.editor_1.markerAdd(index, self.marker_unique_symbol_1)
            for range_start, range_end in result.ranges_1[index]:
                self._set_character_range_indicator(
                    self.editor_1, index, range_start, range_end
                )
        for index in range(len(result.rows_2)):
            self.set_margin_text(self.editor_2, index, result.numbers_2[index])
            style = result.styles_2[index]
            if style is not None:
                if style == self.INDICATOR_SIMILAR:
                    self.editor_2.markerAdd(index, self.marker_similar_2)
                    self.editor_2.markerAdd(index, self.marker_similar_symbol_2)
                else:
                    self.editor_2.markerAdd(index, self.marker_unique_2)
                    self.editor_2.markerAdd(index, self.marker_unique_symbol_2)
            for range_start, range_end in result.ranges_2[index]:
                self._set_character_range_indicator(
                    self.editor_2, index, range_start, range_end
                )
        # Count the differences
        unique_1 = sum(1 for style in result.styles_1 if style == DIFF_UNIQUE_1)
        unique_2 = sum(1 for style in result.styles_2 if style == DIFF_UNIQUE_2)
        similar = sum(1 for style in result.styles_1 if style == DIFF_SIMILAR)
        self._update_stats(unique_1, unique_2, similar)
        # Check if there were any differences
        if unique_1 == 0 and unique_2 == 0 and similar == 0:
            self.main_form.display.repl_display_message(
                "No differences between texts.",
                message_type=constants.MessageType.SUCCESS,
            )
        else:
            # Display the differences/similarities messages
            self.main_form.display.repl_display_message(
                "{:d} differences found in '{:s}'!".format(unique_1, self.text_1_name),
                message_type=constants.MessageType.DIFF_UNIQUE_1,
            )
            self.main_form.display.repl_display_message(
                "{:d} differences found in '{:s}'!".format(unique_2, self.text_2_name),
                message_type=constants.MessageType.DIFF_UNIQUE_2,
            )
            self.main_form.display.repl_display_message(
                "{:d} similarities found between documents!".format(similar),
                message_type=constants.MessageType.DIFF_SIMILAR,
            )
        self._update_margins()
        # Reset the caret to the start of the documents for forward navigation
        self.editor_1.setCursorPosition(0, 0)
        self.editor_2.setCursorPosition(0, 0)
        # Jump to the first difference when the documents are opened
        if self._jump_to_first_diff:
            self._jump_to_first_diff = False
            if unique_1 > 0 or unique_2 > 0 or similar > 0:
                first_diff = next(
                    (
                        index
                        for index in range(len(result.styles_1))
                        if result.styles_1[index] is not None
                        or result.styles_2[index] is not None
                    ),
                    None,
                )
                if first_diff is not None:
                    self.editor_1.goto_line(first_diff + 1, skip_repl_focus=False)
                    self.editor_2.goto_line(first_diff + 1, skip_repl_focus=False)

    def find_next_unique_1(self) -> None:
        """Find and scroll to the next unique difference in the first document"""
        self.focused_editor = self.editor_1
        cursor_line, cursor_index = self.editor_1.getCursorPosition()
        next_diff_line = self.editor_1.markerFindNext(cursor_line + 1, MASK_UNIQUE)
        if next_diff_line == -1:
            # Wrap around to the start of the document
            next_diff_line = self.editor_1.markerFindNext(0, MASK_UNIQUE)
            if next_diff_line == -1:
                self.main_form.display.repl_display_message(
                    "No further unique differences found in '{:s}'!".format(
                        self.text_1_name
                    ),
                    message_type=constants.MessageType.DIFF_UNIQUE_1,
                )
                return
            self.main_form.display.repl_display_message(
                "Scrolled back to the start of the document!",
                message_type=constants.MessageType.DIFF_UNIQUE_1,
            )
            self.main_form.display.write_to_statusbar(
                "Scrolled back to the start of the document!"
            )
        self.editor_1.goto_line(next_diff_line + 1, skip_repl_focus=False)
        self.editor_2.goto_line(next_diff_line + 1, skip_repl_focus=False)

    def find_next_unique_2(self) -> None:
        """Find and scroll to the next unique difference in the second document"""
        self.focused_editor = self.editor_2
        cursor_line, cursor_index = self.editor_2.getCursorPosition()
        next_diff_line = self.editor_2.markerFindNext(cursor_line + 1, MASK_UNIQUE)
        if next_diff_line == -1:
            # Wrap around to the start of the document
            next_diff_line = self.editor_2.markerFindNext(0, MASK_UNIQUE)
            if next_diff_line == -1:
                self.main_form.display.repl_display_message(
                    "No further unique differences found in '{:s}'!".format(
                        self.text_2_name
                    ),
                    message_type=constants.MessageType.DIFF_UNIQUE_2,
                )
                return
            self.main_form.display.repl_display_message(
                "Scrolled back to the start of the document!",
                message_type=constants.MessageType.DIFF_UNIQUE_2,
            )
            self.main_form.display.write_to_statusbar(
                "Scrolled back to the start of the document!"
            )
        self.editor_1.goto_line(next_diff_line + 1, skip_repl_focus=False)
        self.editor_2.goto_line(next_diff_line + 1, skip_repl_focus=False)

    def find_next_similar(self) -> None:
        """Find and scroll to the next similar line, starting from the
        currently focused side.

        focused_editor is deliberately left alone: setFocus() re-focuses it and
        the cursor-change handlers use it to decide which side is driving, so
        overwriting it here would move the caret to the other pane.
        """
        editor = self.focused_editor
        cursor_line, cursor_index = editor.getCursorPosition()
        next_diff_line = editor.markerFindNext(cursor_line + 1, MASK_SIMILAR)
        if next_diff_line == -1:
            # Wrap around to the start of the document
            next_diff_line = editor.markerFindNext(0, MASK_SIMILAR)
            if next_diff_line == -1:
                self.main_form.display.repl_display_message(
                    "No further similar lines found between the documents!",
                    message_type=constants.MessageType.DIFF_SIMILAR,
                )
                return
            self.main_form.display.repl_display_message(
                "Scrolled back to the start of the document!",
                message_type=constants.MessageType.DIFF_SIMILAR,
            )
            self.main_form.display.write_to_statusbar(
                "Scrolled back to the start of the document!"
            )
        self.editor_1.goto_line(next_diff_line + 1, skip_repl_focus=False)
        self.editor_2.goto_line(next_diff_line + 1, skip_repl_focus=False)

    def set_theme(self, theme: dict[str, Any]) -> None:
        self.Indicator_Unique_1_Color = qt.QColor(
            theme["textdiffercolors"]["indicator-unique-1-color"]
        )
        self.Indicator_Unique_2_Color = qt.QColor(
            theme["textdiffercolors"]["indicator-unique-2-color"]
        )
        self.Indicator_Similar_Color = qt.QColor(
            theme["textdiffercolors"]["indicator-similar-color"]
        )

        def set_editor_theme(editor: CustomEditor) -> None:
            if theme["name"] == "Air":
                editor.resetFoldMarginColors()
            elif theme["name"] == "Earth":
                editor.setFoldMarginColors(
                    qt.QColor(theme["foldmargin"]["foreground"]),
                    qt.QColor(theme["foldmargin"]["background"]),
                )
            editor.setMarginsForegroundColor(
                qt.QColor(theme["linemargin"]["foreground"])
            )
            editor.setMarginsBackgroundColor(
                qt.QColor(theme["linemargin"]["background"])
            )
            editor.SendScintilla(
                qt.QsciScintillaBase.SCI_STYLESETBACK,
                qt.QsciScintillaBase.STYLE_DEFAULT,
                qt.QColor(theme["fonts"]["default"]["color"]),
            )
            editor.SendScintilla(
                qt.QsciScintillaBase.SCI_STYLESETBACK,
                qt.QsciScintillaBase.STYLE_LINENUMBER,
                qt.QColor(theme["linemargin"]["background"]),
            )
            editor.SendScintilla(
                qt.QsciScintillaBase.SCI_SETCARETFORE, qt.QColor(theme["cursor"])
            )
            # Re-install this pane's own lexer, resolved from its path. A bare
            # "text" here would silently drop the per-side highlighting on
            # every theme change.
            editor.choose_lexer(
                self._lexer_1 if editor is self.editor_1 else self._lexer_2
            )

        set_editor_theme(self.editor_1)
        set_editor_theme(self.editor_2)
        self._apply_diff_colors()
        self._apply_toolbar_theme(theme)
