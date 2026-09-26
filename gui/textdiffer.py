"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import difflib
import functools
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
    matcher = difflib.SequenceMatcher(a=lines_1, b=lines_2, autojunk=False)
    for opcode, i_1, i_2, j_1, j_2 in matcher.get_opcodes():
        if opcode == "equal":
            for index in range(i_1, i_2):
                line = lines_1[index]
                rows_1.append(line)
                rows_2.append(line)
                numbers_1.append(str(line_counter_1))
                numbers_2.append(str(line_counter_2))
                styles_1.append(None)
                styles_2.append(None)
                ranges_1.append([])
                ranges_2.append([])
                line_counter_1 += 1
                line_counter_2 += 1
        elif opcode == "delete":
            for index in range(i_1, i_2):
                rows_1.append(lines_1[index])
                rows_2.append("")
                numbers_1.append(str(line_counter_1))
                numbers_2.append("")
                styles_1.append(DIFF_UNIQUE_1)
                styles_2.append(None)
                ranges_1.append([])
                ranges_2.append([])
                line_counter_1 += 1
        elif opcode == "insert":
            for index in range(j_1, j_2):
                rows_1.append("")
                rows_2.append(lines_2[index])
                numbers_1.append("")
                numbers_2.append(str(line_counter_2))
                styles_1.append(None)
                styles_2.append(DIFF_UNIQUE_2)
                ranges_1.append([])
                ranges_2.append([])
                line_counter_2 += 1
        elif opcode == "replace":
            side_1 = lines_1[i_1:i_2]
            side_2 = lines_2[j_1:j_2]
            for index in range(min(len(side_1), len(side_2))):
                line_1 = side_1[index]
                line_2 = side_2[index]
                rows_1.append(line_1)
                rows_2.append(line_2)
                numbers_1.append(str(line_counter_1))
                numbers_2.append(str(line_counter_2))
                styles_1.append(DIFF_SIMILAR)
                styles_2.append(DIFF_SIMILAR)
                range_1, range_2 = _diff_ranges(line_1, line_2)
                ranges_1.append(range_1)
                ranges_2.append(range_2)
                line_counter_1 += 1
                line_counter_2 += 1
            for index in range(min(len(side_1), len(side_2)), len(side_1)):
                rows_1.append(side_1[index])
                rows_2.append("")
                numbers_1.append(str(line_counter_1))
                numbers_2.append("")
                styles_1.append(DIFF_UNIQUE_1)
                styles_2.append(None)
                ranges_1.append([])
                ranges_2.append([])
                line_counter_1 += 1
            for index in range(min(len(side_1), len(side_2)), len(side_2)):
                rows_1.append("")
                rows_2.append(side_2[index])
                numbers_1.append("")
                numbers_2.append(str(line_counter_2))
                styles_1.append(None)
                styles_2.append(DIFF_UNIQUE_2)
                ranges_1.append([])
                ranges_2.append([])
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
    # Class constants
    DEFAULT_FONT = qt.QFont(
        settings.get("current_font_name"), settings.get("current_font_size")
    )
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
    # Indicator ranges painted on each editor (position, length)
    _indicator_ranges_1: list[tuple[int, int]]
    _indicator_ranges_2: list[tuple[int, int]]

    def __del__(self):
        try:
            self.editor_1.mousePressEvent = None
            self.editor_1.wheelEvent = None
            self.editor_2.mousePressEvent = None
            self.editor_2.wheelEvent = None
            self.editor_1.actual_parent = None
            self.editor_2.actual_parent = None
            self.editor_1.__del__()
            self.editor_2.__del__()
            self.editor_1 = None
            self.editor_2 = None
            self.focused_editor = None
            self.splitter.setParent(None)
            self.splitter = None
            self.main_layout = None
            self._parent = None
            self.main_form = None
            self.internals = None
            # Clean up self
            self.setParent(None)
            self.deleteLater()
            """
            The actual clean up will occur when the next garbage collection
            cycle is executed, probably because of the nested functions and
            the focus decorator.
            """
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
            self.name = "Text difference: {:s} / {:s}".format(text_1_name, text_2_name)
            self.text_1_name = text_1_name
            self.text_2_name = text_2_name
        else:
            self.name = "Text difference"
            self.text_1_name = "TEXT 1"
            self.text_2_name = "TEXT 2"
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
        self.editor_1.choose_lexer("text")
        self.editor_2.choose_lexer("text")
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

        # Add decorators to each editors mouse clicks and mouse wheel scrolls
        def focus_decorator(function_to_decorate, focused_editor):
            def decorated_function(*args, **kwargs):
                self.focused_editor = focused_editor
                function_to_decorate(*args, **kwargs)

            return decorated_function

        def redefine_event_handler(editor: qt.QsciScintilla, method_name: str) -> None:
            if hasattr(editor, method_name):
                setattr(
                    editor,
                    method_name,
                    focus_decorator(getattr(editor, method_name), editor),
                )

        for editor in (self.editor_1, self.editor_2):
            redefine_event_handler(editor, "mousePressEvent")
            redefine_event_handler(editor, "wheelEvent")
        # Add corner buttons
        self.add_corner_buttons()
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
        # Set the theme
        self.set_theme(settings.get_theme())
        # Set editor functions that have to be propagated from the TextDiffer
        # to the child editor
        self._init_editor_functions()
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

    def _open_side_1(self) -> None:
        """Open the first compared document in a real editor."""
        if self.text_1_path is not None:
            self.main_form.open_file(self.text_1_path)

    def _open_side_2(self) -> None:
        """Open the second compared document in a real editor."""
        if self.text_2_path is not None:
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
        self._set_side_label(self.label_1, self.text_1_name)
        self._set_side_label(self.label_2, self.text_2_name)
        self.editor_1.setMarkerBackgroundColor(
            self.Indicator_Unique_1_Color, self.marker_unique_1
        )
        self.editor_2.setMarkerBackgroundColor(
            self.Indicator_Unique_2_Color, self.marker_unique_2
        )
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

    def _init_editor_functions(self):
        """
        Initialize the editor functions that are called on the TextDiffer widget,
        but need to be executed on one of the editors
        """

        # Find text function propagated to the focused editor
        def enabled_function(function_name, *args, **kwargs):
            # Get the function
            function = getattr(self.focused_editor, function_name)
            # Call the function, leaving out the "function name" argument
            function(*args, **kwargs)

        enabled_functions = [
            "find_text",
        ]
        # Check methods
        for function_name in enabled_functions:
            setattr(
                self,
                function_name,
                functools.partial(enabled_function, function_name),
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

    def init_markers(self):
        """Initialize all markers for showing diff symbols"""
        # Set the images
        image_scale_size = functions.create_size(16, 16)
        image_unique_1 = functions.create_pixmap("tango_icons/diff-unique-1.png")
        image_unique_2 = functions.create_pixmap("tango_icons/diff-unique-2.png")
        image_similar = functions.create_pixmap("tango_icons/diff-similar.png")
        # Scale the images to a smaller size
        image_unique_1 = image_unique_1.scaled(image_scale_size)
        image_unique_2 = image_unique_2.scaled(image_scale_size)
        image_similar = image_similar.scaled(image_scale_size)
        # Markers for editor 1
        self.marker_unique_1 = self.editor_1.markerDefine(
            qt.QsciScintilla.MarkerSymbol.Background, 0
        )
        self.marker_unique_symbol_1 = self.editor_1.markerDefine(image_unique_1, 1)
        self.marker_similar_1 = self.editor_1.markerDefine(
            qt.QsciScintilla.MarkerSymbol.Background, 2
        )
        self.marker_similar_symbol_1 = self.editor_1.markerDefine(image_similar, 3)
        # Set background colors only for the background markers
        self.editor_1.setMarkerBackgroundColor(
            self.Indicator_Unique_1_Color, self.marker_unique_1
        )
        self.editor_1.setMarkerBackgroundColor(
            self.Indicator_Similar_Color, self.marker_similar_1
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
        self.marker_unique_symbol_2 = self.editor_2.markerDefine(image_unique_2, 1)
        self.marker_similar_2 = self.editor_2.markerDefine(
            qt.QsciScintilla.MarkerSymbol.Background, 2
        )
        self.marker_similar_symbol_2 = self.editor_2.markerDefine(image_similar, 3)
        # Set background colors only for the background markers
        self.editor_2.setMarkerBackgroundColor(
            self.Indicator_Unique_2_Color, self.marker_unique_2
        )
        self.editor_2.setMarkerBackgroundColor(
            self.Indicator_Similar_Color, self.marker_similar_2
        )
        # Margins for editor 2
        self.init_margin(
            self.editor_2,
            self.marker_unique_2,
            self.marker_unique_symbol_2,
            self.marker_similar_2,
            self.marker_similar_symbol_2,
        )

    def init_indicator(self, editor, indicator, color):
        """
        Set the indicator settings
        """
        editor.indicatorDefine(
            qt.QsciScintilla.IndicatorStyle.RoundBoxIndicator, indicator
        )
        editor.setIndicatorForegroundColor(color, indicator)
        editor.SendScintilla(qt.QsciScintillaBase.SCI_SETINDICATORCURRENT, indicator)

    def init_editor(self, editor):
        """Initialize all of the PlainEditor settings for difference displaying"""
        editor.setLexer(None)
        editor.setUtf8(True)
        editor.setIndentationsUseTabs(False)
        editor.setFont(self.DEFAULT_FONT)
        editor.setBraceMatching(qt.QsciScintilla.BraceMatch.SloppyBraceMatch)
        editor.setMatchedBraceBackgroundColor(qt.QColor(255, 153, 0))
        editor.setAcceptDrops(False)
        editor.setEolMode(
            qt.QsciScintilla.EolMode(settings.get("editor")["end_of_line_mode"])
        )
        editor.setReadOnly(True)
        editor.savable = constants.CanSave.NO

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

    def compare(self, text_1: str | None, text_2: str | None) -> None:
        """Compare two text strings and display the difference"""
        if text_1 is None or text_2 is None:
            return
        # Store the original text
        self.text_1 = text_1
        self.text_2 = text_2
        # Create the difference
        result = compute_diff_rows(text_1, text_2)
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
        """Find and scroll to the next similar line"""
        self.focused_editor = self.editor_1
        cursor_line, cursor_index = self.editor_1.getCursorPosition()
        next_diff_line = self.editor_1.markerFindNext(cursor_line + 1, MASK_SIMILAR)
        if next_diff_line == -1:
            # Wrap around to the start of the document
            next_diff_line = self.editor_1.markerFindNext(0, MASK_SIMILAR)
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

    def add_corner_buttons(self):
        # Unique 1 button
        self.internals.add_corner_button(
            functions.create_icon("tango_icons/diff-unique-1.png"),
            "Scroll to next unique line\nin document: '{:s}'".format(self.text_1_name),
            self.find_next_unique_1,
        )
        # Unique 2 button
        self.internals.add_corner_button(
            functions.create_icon("tango_icons/diff-unique-2.png"),
            "Scroll to next unique line\nin document: '{:s}'".format(self.text_2_name),
            self.find_next_unique_2,
        )
        # Similar button
        self.internals.add_corner_button(
            functions.create_icon("tango_icons/diff-similar.png"),
            "Scroll to next similar line\nin both documents",
            self.find_next_similar,
        )

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
            editor.choose_lexer("text")

        set_editor_theme(self.editor_1)
        set_editor_theme(self.editor_2)
        self._apply_toolbar_theme(theme)
