"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

from __future__ import annotations

import functools
from typing import Any, Callable

import components.fonts
import components.thesquid
import functions
import qt
import settings
import themes


class SettingsGuiManipulator(qt.QFrame):
    """
    Overlay widget for dynamically displaying and updating
    a subset of the application settings. Every change is
    applied immediately through the settings facade, and the
    controls stay in sync with changes made from anywhere else.
    """

    DEFAULT_SIZE = (620, 600)
    INHERIT = "(inherit)"
    # Qsci end-of-line modes: value as stored in the "end_of_line_mode" setting
    EOL_MODES = [(0, "LF (Unix)"), (1, "CRLF (Windows)"), (2, "CR (Mac)")]
    TERMINAL_SHELLS = ["cmd.exe", "powershell.exe", "pwsh.exe", "/bin/bash"]
    # Class variables
    _parent: Any = None
    main_form: Any = None
    _setting_listeners: dict[str, Callable[[Any], None]] = {}

    def __del__(self):
        try:
            settings.disconnect_change(self._on_settings_changed)
            self._parent = None
            self.main_form = None
            for child_widget in self.children():
                child_widget.deleteLater()
            self.setParent(None)
            self.deleteLater()
        except:
            pass

    def __init__(self, parent=None, main_form=None) -> None:
        # Initialize the superclass
        super().__init__(parent)
        # Store the reference to the parent
        self._parent = parent
        # Store the reference to the main form
        self.main_form = main_form
        # Set default font
        self.setFont(settings.get_current_font())
        # Anchor the filter bar to the top and keep the settings
        # groups in their own scrollable area below it.
        self.setFrameShape(qt.QFrame.Shape.NoFrame)
        self.__shell_layout = qt.QVBoxLayout(self)
        self.__shell_layout.setSpacing(0)
        self.__shell_layout.setContentsMargins(qt.QMargins(0, 0, 0, 0))
        self.__top_bar = qt.QWidget(self)
        self.__top_bar.setObjectName("SettingsTopBar")
        self.__top_layout = qt.QVBoxLayout(self.__top_bar)
        self.__top_layout.setSpacing(5)
        self.__top_layout.setContentsMargins(qt.QMargins(9, 9, 9, 5))
        self.__shell_layout.addWidget(self.__top_bar)
        self.__scroll = qt.QScrollArea(self)
        self.__scroll.setObjectName("SettingsScroll")
        self.__scroll.setWidgetResizable(True)
        self.__scroll.setFrameShape(qt.QFrame.Shape.NoFrame)
        self.__scroll.setHorizontalScrollBarPolicy(
            qt.Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.__scroll.setVerticalScrollBarPolicy(
            qt.Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.__content = qt.QWidget(self.__scroll)
        self.__content.setObjectName("SettingsContent")
        # Create the layout
        self.__layout = qt.QVBoxLayout(self.__content)
        self.__layout.setSpacing(5)
        self.__layout.setContentsMargins(qt.QMargins(9, 9, 9, 9))
        self.__scroll.setWidget(self.__content)
        self.__shell_layout.addWidget(self.__scroll, 1)
        # Initialize the controls
        self._setting_listeners = {
            "current_font_name": lambda v: self._set_combo(self.app_font_combo, str(v)),
            "current_font_size": lambda v: self._set_spin(
                self.app_font_size_spin, int(v)
            ),
            "current_editor_font_name": lambda v: self._set_combo(
                self.editor_font_combo, str(v)
            ),
            "current_editor_font_size": lambda v: self._set_spin(
                self.editor_font_size_spin, int(v)
            ),
            "terminal-font-name": lambda v: self._set_combo(
                self.terminal_font_combo,
                str(v) if v else self.INHERIT,
            ),
            "terminal-font-size": lambda v: self._set_spin(
                self.terminal_font_size_spin,
                int(v) if v else int(settings.get("current_editor_font_size")),
            ),
            "custom_menu_font": lambda v: self._set_combo(
                self.menu_font_combo,
                str(v[0]) if v else self.INHERIT,
            ),
            "editor": self.__sync_editor_controls,
            "restore_last_session": lambda v: self._set_check(
                self.restore_session_checkbox, bool(v)
            ),
            "open-new-files-in-open-instance": lambda v: self._set_check(
                self.open_in_instance_checkbox, bool(v)
            ),
            "max-number-of-recent-files": lambda v: self._set_spin(
                self.recent_files_spin, int(v)
            ),
            "toplevel_menu_scale": lambda v: self._set_spin(
                self.menu_scale_spin, int(v)
            ),
            "tree_display_icon_size": lambda v: self._set_spin(
                self.tree_icon_size_spin, int(v)
            ),
            "standard_button_size": lambda v: self._set_spin(
                self.button_size_spin, int(v)
            ),
            "terminal-history": lambda v: self._set_spin(
                self.terminal_history_spin, int(v)
            ),
            "terminal-shell": lambda v: self._set_combo(
                self.terminal_shell_combo, str(v)
            ),
            "custom_menu_scale": self.__icon_scale_changed_externally,
            "terminal": lambda v: self._set_line_edit(
                self.terminal_program_edit, str(v)
            ),
            "theme": self.__sync_theme,
        }
        # Initialize the options
        self.__group_filters: dict[Any, str] = {}
        self.__init_options()
        # Position the overlay to the center of the screen
        self.center(qt.QSize(*self.DEFAULT_SIZE))
        # Scale the settings manipulator size if needed
        self.scale(1, 1)
        self.update_style()
        # React to settings changed from anywhere
        settings.connect_change(self._on_settings_changed)

    def __init_options(self) -> None:
        """
        Create and lay out all of the settings controls.
        Each control reflects the current setting value and
        applies the change immediately through the settings facade.
        """
        # Filter field that hides non-matching groups while typing.
        # An empty field shows every group.
        self.__filter_edit = qt.QLineEdit(self.__top_bar)
        self.__filter_edit.setPlaceholderText("Filter settings\u2026")
        self.__filter_edit.setClearButtonEnabled(True)
        self.__filter_edit.textChanged.connect(self.__apply_settings_filter)
        self.__top_layout.addWidget(self.__filter_edit)
        # ------------------------------------------------------------------
        # Fonts
        # ------------------------------------------------------------------
        fonts_group = qt.QGroupBox("Fonts", self)
        fonts_layout = qt.QGridLayout()
        fonts_layout.setSpacing(5)
        # Application font
        self.app_font_combo = qt.QComboBox(fonts_group)
        self._populate_family_combo(self.app_font_combo, include_inherit=False)
        self.app_font_combo.setCurrentText(str(settings.get("current_font_name")))
        self.app_font_combo.currentTextChanged.connect(self.__app_font_family_changed)
        self.app_font_size_spin = qt.QSpinBox(fonts_group)
        self.app_font_size_spin.setRange(1, 96)
        self.app_font_size_spin.setValue(int(settings.get("current_font_size")))
        self.app_font_size_spin.valueChanged.connect(self.__app_font_size_changed)
        fonts_layout.addWidget(qt.QLabel("Application:", fonts_group), 0, 0)
        fonts_layout.addWidget(self.app_font_combo, 0, 1)
        fonts_layout.addWidget(qt.QLabel("Size:", fonts_group), 0, 2)
        fonts_layout.addWidget(self.app_font_size_spin, 0, 3)
        # Editor font
        self.editor_font_combo = qt.QComboBox(fonts_group)
        self._populate_family_combo(self.editor_font_combo, include_inherit=False)
        self.editor_font_combo.setCurrentText(
            str(settings.get("current_editor_font_name"))
        )
        self.editor_font_combo.currentTextChanged.connect(
            self.__editor_font_family_changed
        )
        self.editor_font_size_spin = qt.QSpinBox(fonts_group)
        self.editor_font_size_spin.setRange(1, 96)
        self.editor_font_size_spin.setValue(
            int(settings.get("current_editor_font_size"))
        )
        self.editor_font_size_spin.valueChanged.connect(self.__editor_font_size_changed)
        fonts_layout.addWidget(qt.QLabel("Editor:", fonts_group), 1, 0)
        fonts_layout.addWidget(self.editor_font_combo, 1, 1)
        fonts_layout.addWidget(qt.QLabel("Size:", fonts_group), 1, 2)
        fonts_layout.addWidget(self.editor_font_size_spin, 1, 3)
        # Terminal font (None = inherit editor font)
        self.terminal_font_combo = qt.QComboBox(fonts_group)
        self._populate_family_combo(self.terminal_font_combo, include_inherit=True)
        terminal_font_name = settings.get("terminal-font-name")
        if terminal_font_name:
            self.terminal_font_combo.setCurrentText(str(terminal_font_name))
        else:
            self.terminal_font_combo.setCurrentIndex(0)
        self.terminal_font_combo.currentTextChanged.connect(
            self.__terminal_font_family_changed
        )
        self.terminal_font_size_spin = qt.QSpinBox(fonts_group)
        self.terminal_font_size_spin.setRange(1, 96)
        terminal_font_size = settings.get("terminal-font-size")
        self.terminal_font_size_spin.setValue(
            int(terminal_font_size)
            if terminal_font_size
            else int(settings.get("current_editor_font_size"))
        )
        self.terminal_font_size_spin.valueChanged.connect(
            self.__terminal_font_size_changed
        )
        fonts_layout.addWidget(qt.QLabel("Terminal:", fonts_group), 2, 0)
        fonts_layout.addWidget(self.terminal_font_combo, 2, 1)
        fonts_layout.addWidget(qt.QLabel("Size:", fonts_group), 2, 2)
        fonts_layout.addWidget(self.terminal_font_size_spin, 2, 3)
        # Custom menu font (None = inherit application font)
        self.menu_font_combo = qt.QComboBox(fonts_group)
        self._populate_family_combo(self.menu_font_combo, include_inherit=True)
        custom_menu_font = settings.get("custom_menu_font")
        if custom_menu_font:
            self.menu_font_combo.setCurrentText(str(custom_menu_font[0]))
        else:
            self.menu_font_combo.setCurrentIndex(0)
        self.menu_font_combo.currentTextChanged.connect(self.__menu_font_family_changed)
        self.menu_font_size_spin = qt.QSpinBox(fonts_group)
        self.menu_font_size_spin.setRange(1, 96)
        self.menu_font_size_spin.setValue(
            int(custom_menu_font[1]) if custom_menu_font else 10
        )
        self.menu_font_size_spin.valueChanged.connect(self.__menu_font_size_changed)
        fonts_layout.addWidget(qt.QLabel("Menu:", fonts_group), 3, 0)
        fonts_layout.addWidget(self.menu_font_combo, 3, 1)
        fonts_layout.addWidget(qt.QLabel("Size:", fonts_group), 3, 2)
        fonts_layout.addWidget(self.menu_font_size_spin, 3, 3)
        fonts_layout.setColumnStretch(1, 1)
        fonts_layout.setColumnStretch(3, 1)
        fonts_group.setLayout(fonts_layout)
        self.__register_group(
            fonts_group,
            "font",
            "family",
            "size",
            "application",
            "editor",
            "terminal",
            "menu",
            "emulator",
            "menus",
        )

        # ------------------------------------------------------------------
        # Editor options
        # ------------------------------------------------------------------
        options_group = qt.QGroupBox("Editor", self)
        options_layout = qt.QGridLayout()
        options_layout.setSpacing(5)
        # Editor tab width
        options_layout.addWidget(qt.QLabel("Tab width:", options_group), 0, 0)
        self.tab_width_spinbox = qt.QSpinBox(options_group)
        self.tab_width_spinbox.setRange(1, 16)
        self.tab_width_spinbox.setValue(int(settings.get("editor")["tab_width"]))
        self.tab_width_spinbox.valueChanged.connect(
            functools.partial(self.__editor_setting_handler, "tab_width")
        )
        options_layout.addWidget(self.tab_width_spinbox, 0, 1)
        # Word wrap
        options_layout.addWidget(qt.QLabel("Word wrap:", options_group), 0, 2)
        self.word_wrap_checkbox = qt.QCheckBox(options_group)
        self.word_wrap_checkbox.setChecked(bool(settings.get("editor")["word_wrap"]))
        self.word_wrap_checkbox.toggled.connect(
            functools.partial(self.__editor_setting_handler, "word_wrap")
        )
        options_layout.addWidget(self.word_wrap_checkbox, 0, 3)
        # Editor zoom factor
        options_layout.addWidget(qt.QLabel("Zoom:", options_group), 1, 0)
        self.zoom_factor_spinbox = qt.QSpinBox(options_group)
        self.zoom_factor_spinbox.setRange(-10, 20)
        self.zoom_factor_spinbox.setValue(int(settings.get("editor")["zoom_factor"]))
        self.zoom_factor_spinbox.valueChanged.connect(
            functools.partial(self.__editor_setting_handler, "zoom_factor")
        )
        options_layout.addWidget(self.zoom_factor_spinbox, 1, 1)
        # Theme
        options_layout.addWidget(qt.QLabel("Theme:", options_group), 1, 2)
        self.theme_combobox = qt.QComboBox(options_group)
        self.__theme_list = themes.get_all()
        for theme in self.__theme_list:
            self.theme_combobox.addItem(theme["name"])
        current_theme_name = settings.get("theme")
        current_theme_index = next(
            (
                i
                for i, theme in enumerate(self.__theme_list)
                if theme["name"] == current_theme_name
            ),
            0,
        )
        self.theme_combobox.setCurrentIndex(current_theme_index)
        self.theme_combobox.activated.connect(self.__theme_changed)
        options_layout.addWidget(self.theme_combobox, 1, 3)
        # Autocompletion
        options_layout.addWidget(qt.QLabel("Autocompletion:", options_group), 2, 0)
        self.autocompletion_checkbox = qt.QCheckBox(options_group)
        self.autocompletion_checkbox.setChecked(
            bool(settings.get("editor")["autocompletion"])
        )
        self.autocompletion_checkbox.toggled.connect(
            functools.partial(self.__editor_setting_handler, "autocompletion")
        )
        options_layout.addWidget(self.autocompletion_checkbox, 2, 1)
        # Cursor line highlight
        options_layout.addWidget(qt.QLabel("Cursor line:", options_group), 2, 2)
        self.cursor_line_checkbox = qt.QCheckBox(options_group)
        self.cursor_line_checkbox.setChecked(
            bool(settings.get("editor")["cursor_line_visible"])
        )
        self.cursor_line_checkbox.toggled.connect(
            functools.partial(self.__editor_setting_handler, "cursor_line_visible")
        )
        options_layout.addWidget(self.cursor_line_checkbox, 2, 3)
        # Whitespace markers
        options_layout.addWidget(qt.QLabel("Whitespace:", options_group), 3, 0)
        self.whitespace_checkbox = qt.QCheckBox(options_group)
        self.whitespace_checkbox.setChecked(
            bool(settings.get("editor")["whitespace_visible"])
        )
        self.whitespace_checkbox.toggled.connect(
            functools.partial(self.__editor_setting_handler, "whitespace_visible")
        )
        options_layout.addWidget(self.whitespace_checkbox, 3, 1)
        # Tabs insert spaces
        options_layout.addWidget(qt.QLabel("Tabs→spaces:", options_group), 3, 2)
        self.tabs_spaces_checkbox = qt.QCheckBox(options_group)
        self.tabs_spaces_checkbox.setChecked(
            bool(settings.get("editor")["tabs_use_spaces"])
        )
        self.tabs_spaces_checkbox.toggled.connect(
            functools.partial(self.__editor_setting_handler, "tabs_use_spaces")
        )
        options_layout.addWidget(self.tabs_spaces_checkbox, 3, 3)
        # Edge marker
        options_layout.addWidget(qt.QLabel("Edge marker:", options_group), 4, 0)
        self.edge_marker_checkbox = qt.QCheckBox(options_group)
        self.edge_marker_checkbox.setChecked(
            bool(settings.get("editor")["edge_marker_visible"])
        )
        self.edge_marker_checkbox.toggled.connect(
            functools.partial(self.__editor_setting_handler, "edge_marker_visible")
        )
        options_layout.addWidget(self.edge_marker_checkbox, 4, 1)
        options_layout.addWidget(qt.QLabel("Column:", options_group), 4, 2)
        self.edge_column_spinbox = qt.QSpinBox(options_group)
        self.edge_column_spinbox.setRange(0, 1000)
        self.edge_column_spinbox.setValue(
            int(settings.get("editor")["edge_marker_column"])
        )
        self.edge_column_spinbox.valueChanged.connect(
            functools.partial(self.__editor_setting_handler, "edge_marker_column")
        )
        options_layout.addWidget(self.edge_column_spinbox, 4, 3)
        # Line ending mode
        options_layout.addWidget(qt.QLabel("Line endings:", options_group), 5, 0)
        self.line_endings_combobox = qt.QComboBox(options_group)
        for mode, label in self.EOL_MODES:
            self.line_endings_combobox.addItem(label, mode)
        current_eol_index = self.line_endings_combobox.findData(
            int(settings.get("editor")["end_of_line_mode"])
        )
        if current_eol_index >= 0:
            self.line_endings_combobox.setCurrentIndex(current_eol_index)
        self.line_endings_combobox.activated.connect(self.__eol_mode_changed)
        options_layout.addWidget(self.line_endings_combobox, 5, 1)
        # Makefile-specific overrides
        options_layout.addWidget(qt.QLabel("Makefile tabs:", options_group), 6, 0)
        self.makefile_tabs_checkbox = qt.QCheckBox(options_group)
        self.makefile_tabs_checkbox.setChecked(
            bool(settings.get("editor")["makefile_uses_tabs"])
        )
        self.makefile_tabs_checkbox.toggled.connect(
            functools.partial(self.__editor_setting_handler, "makefile_uses_tabs")
        )
        options_layout.addWidget(self.makefile_tabs_checkbox, 6, 1)
        options_layout.addWidget(qt.QLabel("Makefile whitespace:", options_group), 6, 2)
        self.makefile_ws_checkbox = qt.QCheckBox(options_group)
        self.makefile_ws_checkbox.setChecked(
            bool(settings.get("editor")["makefile_whitespace_visible"])
        )
        self.makefile_ws_checkbox.toggled.connect(
            functools.partial(
                self.__editor_setting_handler, "makefile_whitespace_visible"
            )
        )
        options_layout.addWidget(self.makefile_ws_checkbox, 6, 3)
        # Maximum number of highlight matches
        options_layout.addWidget(qt.QLabel("Max highlights:", options_group), 7, 0)
        self.max_highlights_spin = qt.QSpinBox(options_group)
        self.max_highlights_spin.setRange(10, 2000)
        self.max_highlights_spin.setSingleStep(50)
        self.max_highlights_spin.setValue(
            int(settings.get("editor")["maximum_highlights"])
        )
        self.max_highlights_spin.valueChanged.connect(
            functools.partial(self.__editor_setting_handler, "maximum_highlights")
        )
        options_layout.addWidget(self.max_highlights_spin, 7, 1)
        # Editor colours
        options_layout.addWidget(qt.QLabel("Brace match:", options_group), 8, 0)
        self.brace_color_button = qt.QPushButton(options_group)
        self.brace_color_button.clicked.connect(
            functools.partial(self.__colour_changed, "brace_color")
        )
        options_layout.addWidget(self.brace_color_button, 8, 1)
        options_layout.addWidget(qt.QLabel("Edge marker:", options_group), 8, 2)
        self.edge_color_button = qt.QPushButton(options_group)
        self.edge_color_button.clicked.connect(
            functools.partial(self.__colour_changed, "edge_marker_color")
        )
        options_layout.addWidget(self.edge_color_button, 8, 3)
        self._refresh_colour_buttons()
        options_layout.setColumnStretch(1, 1)
        options_layout.setColumnStretch(3, 1)
        options_group.setLayout(options_layout)
        self.__register_group(
            options_group,
            "tab",
            "wrap",
            "word",
            "zoom",
            "theme",
            "autocomplete",
            "autocompletion",
            "cursor",
            "line",
            "whitespace",
            "tabs",
            "spaces",
            "edge",
            "marker",
            "column",
            "endings",
            "eol",
            "makefile",
            "highlight",
            "highlights",
            "max",
            "colour",
            "color",
            "brace",
        )

        # ------------------------------------------------------------------
        # General startup options
        # ------------------------------------------------------------------
        general_group = qt.QGroupBox("Startup and window", self)
        general_layout = qt.QGridLayout()
        general_layout.setSpacing(5)
        general_layout.addWidget(qt.QLabel("Restore session:", general_group), 0, 0)
        self.restore_session_checkbox = qt.QCheckBox(general_group)
        self.restore_session_checkbox.setChecked(
            bool(settings.get("restore_last_session"))
        )
        self.restore_session_checkbox.toggled.connect(
            functools.partial(self.__simple_setting, "restore_last_session")
        )
        general_layout.addWidget(self.restore_session_checkbox, 0, 1)
        general_layout.addWidget(qt.QLabel("Open in instance:", general_group), 0, 2)
        self.open_in_instance_checkbox = qt.QCheckBox(general_group)
        self.open_in_instance_checkbox.setChecked(
            bool(settings.get("open-new-files-in-open-instance"))
        )
        self.open_in_instance_checkbox.toggled.connect(
            functools.partial(self.__simple_setting, "open-new-files-in-open-instance")
        )
        general_layout.addWidget(self.open_in_instance_checkbox, 0, 3)
        general_layout.addWidget(qt.QLabel("Recent files cap:", general_group), 1, 0)
        self.recent_files_spin = qt.QSpinBox(general_group)
        self.recent_files_spin.setRange(1, 500)
        self.recent_files_spin.setValue(int(settings.get("max-number-of-recent-files")))
        self.recent_files_spin.valueChanged.connect(
            functools.partial(self.__simple_setting, "max-number-of-recent-files")
        )
        general_layout.addWidget(self.recent_files_spin, 1, 1)
        general_layout.addWidget(qt.QLabel("Menu scale %:", general_group), 1, 2)
        self.menu_scale_spin = qt.QSpinBox(general_group)
        self.menu_scale_spin.setRange(80, 120)
        self.menu_scale_spin.setSingleStep(5)
        self.menu_scale_spin.setValue(int(settings.get("toplevel_menu_scale")))
        self.menu_scale_spin.valueChanged.connect(self.__menu_scale_changed)
        general_layout.addWidget(self.menu_scale_spin, 1, 3)
        # Custom menu icon scale override (None = follow toplevel menu scale)
        general_layout.addWidget(qt.QLabel("Icon scale override:", general_group), 2, 0)
        self.icon_scale_override_checkbox = qt.QCheckBox(general_group)
        custom_menu_scale = settings.get("custom_menu_scale")
        self.icon_scale_override_checkbox.setChecked(custom_menu_scale is not None)
        self.icon_scale_override_checkbox.toggled.connect(
            self.__icon_scale_override_toggled
        )
        general_layout.addWidget(self.icon_scale_override_checkbox, 2, 1)
        general_layout.addWidget(qt.QLabel("Icon scale:", general_group), 2, 2)
        self.icon_scale_spin = qt.QSpinBox(general_group)
        self.icon_scale_spin.setRange(50, 200)
        self.icon_scale_spin.setSingleStep(5)
        self.icon_scale_spin.setValue(
            int(custom_menu_scale) if custom_menu_scale else 100
        )
        self.icon_scale_spin.setEnabled(custom_menu_scale is not None)
        self.icon_scale_spin.valueChanged.connect(self.__icon_scale_changed)
        general_layout.addWidget(self.icon_scale_spin, 2, 3)
        general_layout.setColumnStretch(1, 1)
        general_layout.setColumnStretch(3, 1)
        general_group.setLayout(general_layout)
        self.__register_group(
            general_group,
            "startup",
            "session",
            "restore",
            "recent",
            "open",
            "instance",
            "menu",
            "scale",
            "icon",
            "override",
        )

        # ------------------------------------------------------------------
        # Display and terminal sizing
        # ------------------------------------------------------------------
        display_group = qt.QGroupBox("Display and terminal", self)
        display_layout = qt.QGridLayout()
        display_layout.setSpacing(5)
        display_layout.addWidget(qt.QLabel("Tree icon size:", display_group), 0, 0)
        self.tree_icon_size_spin = qt.QSpinBox(display_group)
        self.tree_icon_size_spin.setRange(12, 48)
        self.tree_icon_size_spin.setValue(int(settings.get("tree_display_icon_size")))
        self.tree_icon_size_spin.valueChanged.connect(
            functools.partial(self.__simple_setting, "tree_display_icon_size")
        )
        display_layout.addWidget(self.tree_icon_size_spin, 0, 1)
        display_layout.addWidget(qt.QLabel("Button size:", display_group), 0, 2)
        self.button_size_spin = qt.QSpinBox(display_group)
        self.button_size_spin.setRange(24, 80)
        self.button_size_spin.setValue(int(settings.get("standard_button_size")))
        self.button_size_spin.valueChanged.connect(
            functools.partial(self.__simple_setting, "standard_button_size")
        )
        display_layout.addWidget(self.button_size_spin, 0, 3)
        display_layout.addWidget(qt.QLabel("Terminal history:", display_group), 1, 0)
        self.terminal_history_spin = qt.QSpinBox(display_group)
        self.terminal_history_spin.setRange(100, 10000)
        self.terminal_history_spin.setSingleStep(100)
        self.terminal_history_spin.setValue(int(settings.get("terminal-history")))
        self.terminal_history_spin.valueChanged.connect(
            functools.partial(self.__simple_setting, "terminal-history")
        )
        display_layout.addWidget(self.terminal_history_spin, 1, 1)
        display_layout.addWidget(qt.QLabel("Shell:", display_group), 1, 2)
        self.terminal_shell_combo = qt.QComboBox(display_group)
        self.terminal_shell_combo.setEditable(True)
        self.terminal_shell_combo.addItems(self.TERMINAL_SHELLS)
        self.terminal_shell_combo.setEditText(str(settings.get("terminal-shell")))
        self.terminal_shell_combo.editTextChanged.connect(
            functools.partial(self.__simple_setting, "terminal-shell")
        )
        display_layout.addWidget(self.terminal_shell_combo, 1, 3)
        # External terminal emulator program (Linux)
        display_layout.addWidget(
            qt.QLabel("Ext. terminal (Linux):", display_group), 2, 0
        )
        self.terminal_program_edit = qt.QLineEdit(display_group)
        self.terminal_program_edit.setPlaceholderText("x-terminal-emulator")
        self.terminal_program_edit.setText(str(settings.get("terminal")))
        self.terminal_program_edit.textChanged.connect(
            functools.partial(self.__simple_setting, "terminal")
        )
        display_layout.addWidget(self.terminal_program_edit, 2, 1)
        display_layout.setColumnStretch(1, 1)
        display_layout.setColumnStretch(3, 1)
        display_group.setLayout(display_layout)
        self.__register_group(
            display_group,
            "terminal",
            "tree",
            "icon",
            "button",
            "size",
            "history",
            "shell",
            "ext",
            "linux",
            "external",
        )

    def __editor_setting_handler(self, sub_key: str, value: Any) -> None:
        """
        Apply a single editor sub-setting and re-apply it to all open editors.
        """
        editor_settings = settings.get("editor").copy()
        editor_settings[sub_key] = value
        settings.set("editor", editor_settings)
        # Re-apply the settings to all open editors
        self._tabs_with("update_variable_settings")

    def __sync_editor_controls(self, value: Any) -> None:
        """
        Reflect the whole "editor" settings dict onto every editor control.
        Signal blocks prevent echoing our own changes back out.
        """
        editor_settings = value if isinstance(value, dict) else settings.get("editor")
        self._set_spin(self.tab_width_spinbox, int(editor_settings["tab_width"]))
        self._set_spin(self.zoom_factor_spinbox, int(editor_settings["zoom_factor"]))
        self._set_check(self.word_wrap_checkbox, bool(editor_settings["word_wrap"]))
        self._set_check(
            self.autocompletion_checkbox, bool(editor_settings["autocompletion"])
        )
        self._set_check(
            self.cursor_line_checkbox, bool(editor_settings["cursor_line_visible"])
        )
        self._set_check(
            self.whitespace_checkbox, bool(editor_settings["whitespace_visible"])
        )
        self._set_check(
            self.tabs_spaces_checkbox, bool(editor_settings["tabs_use_spaces"])
        )
        self._set_check(
            self.edge_marker_checkbox, bool(editor_settings["edge_marker_visible"])
        )
        self._set_spin(
            self.edge_column_spinbox, int(editor_settings["edge_marker_column"])
        )
        eol_index = self.line_endings_combobox.findData(
            int(editor_settings["end_of_line_mode"])
        )
        if eol_index >= 0:
            self.line_endings_combobox.blockSignals(True)
            self.line_endings_combobox.setCurrentIndex(eol_index)
            self.line_endings_combobox.blockSignals(False)
        self._set_check(
            self.makefile_tabs_checkbox, bool(editor_settings["makefile_uses_tabs"])
        )
        self._set_check(
            self.makefile_ws_checkbox,
            bool(editor_settings["makefile_whitespace_visible"]),
        )
        self._set_spin(
            self.max_highlights_spin, int(editor_settings["maximum_highlights"])
        )
        self._refresh_colour_buttons()

    def __eol_mode_changed(self, index: int) -> None:
        self.__editor_setting_handler(
            "end_of_line_mode", self.line_endings_combobox.itemData(index)
        )

    def __colour_changed(self, key: str) -> None:
        """
        Open a colour dialog and store the picked colour as an ARGB hex string.
        """
        current = str(settings.get("editor")[key])
        colour = qt.QColorDialog.getColor(
            qt.QColor(current),
            self,
            "Select editor colour",
            qt.QColorDialog.ColorDialogOption.DontUseNativeDialog,
        )
        if colour.isValid():
            self.__editor_setting_handler(
                key, colour.name(qt.QColor.NameFormat.HexArgb)
            )

    def __apply_settings_filter(self, text: str) -> None:
        """
        Show only the group boxes that match the typed filter text.
        An empty field shows every group.
        """
        query = str(text).strip().lower()
        for group, keywords in self.__group_filters.items():
            group.setVisible(not query or query in keywords)

    def __register_group(self, group: qt.QGroupBox, *keywords: str) -> None:
        """
        Add a settings group to the layout and register the searchable
        (title + keyword) text used by the filter field.
        """
        search_text = group.title().lower()
        for keyword in keywords:
            search_text += " " + keyword.lower()
        self.__group_filters[group] = search_text
        self.__layout.addWidget(group)

    def _refresh_colour_buttons(self) -> None:
        editor_settings = settings.get("editor")
        self._set_colour_button(
            self.brace_color_button, str(editor_settings["brace_color"])
        )
        self._set_colour_button(
            self.edge_color_button, str(editor_settings["edge_marker_color"])
        )

    def __simple_setting(self, key: str, value: Any) -> None:
        settings.set(key, value)

    def __menu_scale_changed(self, value: int) -> None:
        settings.set("toplevel_menu_scale", float(value))

    def __icon_scale_override_toggled(self, checked: bool) -> None:
        """
        Enabling the override stores the current spin value; disabling it
        clears the overriding scale back to None (inherit).
        """
        self.icon_scale_spin.setEnabled(checked)
        if checked:
            settings.set("custom_menu_scale", self.icon_scale_spin.value())
        else:
            settings.set("custom_menu_scale", None)

    def __icon_scale_changed(self, value: int) -> None:
        if self.icon_scale_override_checkbox.isChecked():
            settings.set("custom_menu_scale", value)

    def __icon_scale_changed_externally(self, value: Any) -> None:
        """
        Reflect an external change to the menu icon scale onto the controls.
        """
        self.icon_scale_override_checkbox.blockSignals(True)
        self.icon_scale_override_checkbox.setChecked(value is not None)
        self.icon_scale_override_checkbox.blockSignals(False)
        if value is not None:
            self._set_spin(self.icon_scale_spin, int(value))
        self.icon_scale_spin.setEnabled(value is not None)

    def __app_font_family_changed(self, text: str) -> None:
        if text and text in qt.QFontDatabase.families():
            settings.set("current_font_name", text)
            self.__apply_app_font()

    def __app_font_size_changed(self, value: int) -> None:
        settings.set("current_font_size", value)
        self.__apply_app_font()

    def __apply_app_font(self) -> None:
        family = str(settings.get("current_font_name"))
        size = int(settings.get("current_font_size"))
        if family in qt.QFontDatabase.families():
            components.fonts.set_application_font(family, size)
        self.setFont(settings.get_current_font())
        view = getattr(self.main_form, "view", None)
        if view is not None and hasattr(view, "refresh_theme"):
            view.refresh_theme()

    def __editor_font_family_changed(self, text: str) -> None:
        if text and text in qt.QFontDatabase.families():
            settings.set("current_editor_font_name", text)
            self.__apply_editor_font()

    def __editor_font_size_changed(self, value: int) -> None:
        settings.set("current_editor_font_size", value)
        self.__apply_editor_font()

    def __apply_editor_font(self) -> None:
        self._tabs_with("update_variable_settings")

    def __terminal_font_family_changed(self, text: str) -> None:
        if text == self.INHERIT:
            settings.set("terminal-font-name", None)
        elif text and text in qt.QFontDatabase.families():
            settings.set("terminal-font-name", text)
        self.__apply_terminal_font()

    def __terminal_font_size_changed(self, value: int) -> None:
        settings.set("terminal-font-size", value)
        self.__apply_terminal_font()

    def __apply_terminal_font(self) -> None:
        self._tabs_with("update_style", skip_with="update_variable_settings")

    def __menu_font_family_changed(self, _text: str) -> None:
        self.__apply_menu_font()

    def __menu_font_size_changed(self, _value: int) -> None:
        self.__apply_menu_font()

    def __apply_menu_font(self) -> None:
        family = self.menu_font_combo.currentText()
        if family == self.INHERIT:
            settings.set("custom_menu_font", None)
        else:
            settings.set("custom_menu_font", (family, self.menu_font_size_spin.value()))
        components.thesquid.TheSquid.update_styles()

    def __theme_changed(self, index: int) -> None:
        """
        Apply the theme change and refresh the entire application theme.
        """
        theme = self.__theme_list[index]
        settings.set("theme", theme["name"])
        self.main_form.view.refresh_theme()
        self.update_style()

    def __sync_theme(self, value: Any) -> None:
        """
        Reflect an external theme change onto the theme combobox and styles.
        """
        name = str(value if value is not None else settings.get("theme"))
        self.theme_combobox.blockSignals(True)
        index = self.theme_combobox.findText(name)
        if index >= 0:
            self.theme_combobox.setCurrentIndex(index)
        self.theme_combobox.blockSignals(False)
        self.update_style()

    def _tabs_with(self, method_name: str, skip_with: str | None = None) -> None:
        if self.main_form is None:
            return
        windows = self.main_form.get_all_windows()
        for window in windows:
            for i in range(window.count()):
                tab = window.widget(i)
                if skip_with is not None and hasattr(tab, skip_with):
                    continue
                if hasattr(tab, method_name):
                    getattr(tab, method_name)()

    def _on_settings_changed(self, name: str, value: Any) -> None:
        listener = self._setting_listeners.get(name)
        if listener is not None:
            listener(value)

    @staticmethod
    def _set_combo(combo: qt.QComboBox, text: str) -> None:
        if text:
            combo.blockSignals(True)
            if combo.isEditable():
                combo.setEditText(text)
            else:
                index = combo.findText(text)
                if index >= 0:
                    combo.setCurrentIndex(index)
            combo.blockSignals(False)

    @staticmethod
    def _set_check(check: qt.QCheckBox, checked: bool) -> None:
        check.blockSignals(True)
        check.setChecked(bool(checked))
        check.blockSignals(False)

    @staticmethod
    def _set_line_edit(edit: qt.QLineEdit, text: str) -> None:
        edit.blockSignals(True)
        edit.setText(text)
        edit.blockSignals(False)

    @staticmethod
    def _populate_family_combo(combo: qt.QComboBox, include_inherit: bool) -> None:
        if include_inherit:
            combo.addItem(SettingsGuiManipulator.INHERIT)
        for family in qt.QFontDatabase.families():
            if family:
                combo.addItem(str(family))

    @staticmethod
    def _set_spin(spin: qt.QSpinBox, value: int) -> None:
        value = max(spin.minimum(), min(spin.maximum(), value))
        spin.blockSignals(True)
        spin.setValue(int(value))
        spin.blockSignals(False)

    @classmethod
    def _set_colour_button(cls, button: qt.QPushButton, colour_hex: str) -> None:
        """Paint a colour button with the given ARGB/hex string and a readable foreground."""
        colour = qt.QColor(colour_hex)
        text_colour = "#f0f0f0" if colour.lightness() < 140 else "#101010"
        button.setText(colour_hex)
        button.setStyleSheet(
            "QPushButton {"
            "background-color: %s;"
            "color: %s;"
            "border: 1px solid %s;"
            "border-radius: 3px;"
            "padding: 2px 8px 2px 8px;"
            "}"
            % (
                colour.name(),
                text_colour,
                settings.get_theme()["indication"]["passiveborder"],
            )
        )

    def hideEvent(self, event: Any) -> None:
        """
        Overridden widget hide event
        """
        last_widget = self.main_form.last_focused_widget
        if last_widget is not None:
            if last_widget.currentWidget() is not None:
                last_widget.currentWidget().setFocus()

    def hide(self) -> None:
        """
        Hide the settings manipulator
        """
        self.setVisible(False)
        self.setEnabled(False)

    def show(self) -> None:
        """
        Show the settings manipulator
        """
        self.setVisible(True)
        self.setEnabled(True)
        # Center to the main form
        self.center(self.size())
        self.__scroll.setFocus()

    def scale(
        self,
        width_scale_factor: float = 1.0,
        height_scale_factor: float = 1.0,
    ) -> None:
        """
        Scale the size of the settings manipulator and all of its child widgets
        """
        geo = self.geometry()
        new_width = int(geo.width() * width_scale_factor)
        new_height = int(geo.height() * height_scale_factor)
        rectangle = functions.create_rect(
            geo.topLeft(), functions.create_size(new_width, new_height)
        )
        self.setGeometry(rectangle)
        # Center to the main form
        self.center(self.size())

    def center(self, size: qt.QSize) -> None:
        """
        Center the settings manipulator to the main form,
        according to the size parameter
        """
        x_offset = int((self.main_form.size().width() - size.width()) / 2)
        y_offset = int((self.main_form.size().height() * 93 / 100 - size.height()) / 2)
        rectangle_top_left = functions.create_point(x_offset, y_offset)
        rectangle_size = size
        rectangle = functions.create_rect(rectangle_top_left, rectangle_size)
        self.setGeometry(rectangle)

    def update_style(self) -> None:
        theme = settings.get_theme()
        default_color = theme["fonts"]["default"]["color"]
        default_background = theme["fonts"]["default"]["background"]
        passive_background = theme["indication"]["passivebackground"]
        passive_border = theme["indication"]["passiveborder"]
        active_background = theme["indication"]["activebackground"]
        active_border = theme["indication"]["activeborder"]
        hover = theme["indication"]["hover"]
        font_name = settings.get("current_font_name")
        font_size = settings.get("current_font_size")
        chevron_up = functions.get_resource_file(
            "feather/air-light-grey/chevron-up.svg"
        )
        chevron_down = functions.get_resource_file(
            "feather/air-light-grey/chevron-down.svg"
        )
        check_icon = functions.get_resource_file("feather/air-light-grey/check.svg")
        self.setStyleSheet(
            f"""
QFrame {{
    background-color: {default_background};
    color: {default_color};
    border: 1px solid {passive_border};
    margin: 0px;
    padding: 0px;
    spacing: 0px;
}}
QLabel {{
    background: transparent;
    color: {default_color};
    border: none;
    font-family: {font_name};
    font-size: {font_size}pt;
}}
QGroupBox {{
    background: transparent;
    color: {default_color};
    border: 1px solid {passive_border};
    border-radius: 4px;
    margin-top: 8px;
    padding: 2px 6px 6px 6px;
    font-family: {font_name};
    font-size: {font_size}pt;
    font-weight: bold;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 8px;
    padding: 0 4px 0 4px;
    color: {default_color};
    background: {default_background};
}}
QComboBox, QSpinBox, QLineEdit {{
    background: {passive_background};
    color: {default_color};
    border: 1px solid {passive_border};
    border-radius: 3px;
    padding: 1px 4px 1px 4px;
    font-family: {font_name};
    font-size: {font_size}pt;
    font-weight: normal;
    selection-background-color: {active_background};
    selection-color: {default_color};
}}
QComboBox:hover, QSpinBox:hover, QLineEdit:hover {{
    background: {hover};
    border: 1px solid {active_border};
}}
QComboBox:focus, QSpinBox:focus, QLineEdit:focus {{
    background: {active_background};
    border: 1px solid {active_border};
}}
QComboBox::drop-down {{
    border: none;
    width: 16px;
    margin: 0px;
    padding: 0px;
}}
QComboBox::down-arrow {{
    image: url({chevron_down});
    width: 10px;
    height: 10px;
}}
QComboBox QAbstractItemView {{
    background: {passive_background};
    color: {default_color};
    border: 1px solid {passive_border};
    selection-background-color: {active_background};
    selection-color: {default_color};
    outline: 0;
}}
QSpinBox::up-button, QSpinBox::down-button {{
    background: {passive_background};
    border: none;
    width: 14px;
    margin: 0px;
    padding: 0px;
}}
QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
    background: {hover};
}}
QSpinBox::up-arrow {{
    image: url({chevron_up});
    width: 10px;
    height: 10px;
}}
QSpinBox::down-arrow {{
    image: url({chevron_down});
    width: 10px;
    height: 10px;
}}
QScrollArea {{
    background: {default_background};
}}
#SettingsContent {{
    background: transparent;
}}
#SettingsTopBar {{
    background: transparent;
    border-bottom: 1px solid {passive_border};
}}
#SettingsScroll {{
    border: none;
}}
QPushButton {{
    background: {passive_background};
    color: {default_color};
    border: 1px solid {passive_border};
    border-radius: 3px;
    padding: 2px 8px 2px 8px;
    font-family: {font_name};
    font-size: {font_size}pt;
    font-weight: normal;
}}
QPushButton:hover {{
    background: {hover};
    border: 1px solid {active_border};
}}
QPushButton:pressed {{
    background: {active_background};
    border: 1px solid {active_border};
}}
QCheckBox {{
    color: {default_color};
    background: transparent;
    font-weight: normal;
    spacing: 6px;
}}
QCheckBox::indicator {{
    width: 14px;
    height: 14px;
    background: {passive_background};
    border: 1px solid {passive_border};
    border-radius: 3px;
}}
QCheckBox::indicator:hover {{
    background: {hover};
    border: 1px solid {active_border};
}}
QCheckBox::indicator:checked {{
    image: url({check_icon});
    background: {active_background};
    border: 1px solid {active_border};
}}
        """
        )
