"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

##  FILE DESCRIPTION:
##      Tab widget for editing the PATH environment variable.
##      Contains the OS read/persist logic and the GUI in a single module.

import os
import re

import components.internals
import constants
import data
import functions
import qt
import settings


def _split_path(path_string):
    """Split a PATH string by the OS path separator, stripping empty segments"""
    if not path_string:
        return []
    return [
        segment.strip() for segment in path_string.split(os.pathsep) if segment.strip()
    ]


def get_os_path_entries():
    """
    Return a (user, system) tuple of the current PATH entries.
    Windows: the user PATH comes from the HKCU registry value, the system
             PATH from the HKLM value.
    Linux:   the whole PATH is user-managed, the system portion is empty.
    """
    if data.on_windows:
        import winreg

        # System PATH (modifying it requires administrator privileges)
        system = []
        try:
            with winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
            ) as key:
                value, _ = winreg.QueryValueEx(key, "PATH")
                system = _split_path(value)
        except OSError:
            system = []
        # User PATH
        user = []
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
                value, _ = winreg.QueryValueEx(key, "PATH")
                user = _split_path(value)
        except OSError:
            user = []
        return user, system
    else:
        return _split_path(os.environ.get("PATH", "")), []


def apply_os_path_entries(user_entries, system_entries):
    """
    Persist the given entries to the OS environment AND apply them to the
    current process. Returns None on success or an error string on failure.
    """
    try:
        # Apply to the current process (expand any %VAR% references so that
        # Python can resolve executables; child shells expand them anyway)
        expanded = [os.path.expandvars(path) for path in system_entries + user_entries]
        os.environ["PATH"] = os.pathsep.join(expanded)
        if data.on_windows:
            return _apply_windows(user_entries, system_entries)
        else:
            return _apply_linux(user_entries + system_entries)
    except Exception as ex:
        return str(ex)


def _apply_windows(user_entries, system_entries):
    """Persist the user entries to the HKCU value and the system entries to HKLM"""
    import winreg

    # --- System PATH (HKLM) ---
    # Only written when it differs from the current value; modifying it
    # requires administrator privileges, so a clear error is reported if denied.
    system_changed = True
    try:
        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
        ) as key:
            value, _ = winreg.QueryValueEx(key, "PATH")
            system_changed = _split_path(value) != system_entries
    except OSError:
        pass
    if system_changed:
        system_value = ";".join(system_entries)
        try:
            with winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
                0,
                winreg.KEY_SET_VALUE,
            ) as key:
                if system_value == "":
                    try:
                        winreg.DeleteValue(key, "PATH")
                    except OSError:
                        pass
                else:
                    # Preserve REG_EXPAND_SZ if any %VAR% references are present
                    value_type = (
                        winreg.REG_EXPAND_SZ
                        if re.search(r"%\w+%", system_value)
                        else winreg.REG_SZ
                    )
                    winreg.SetValueEx(key, "PATH", 0, value_type, system_value)
        except PermissionError:
            return (
                "Failed to modify the system PATH: "
                "administrator privileges are required"
            )

    # --- User PATH (HKCU) ---
    user_value = ";".join(user_entries)
    with winreg.OpenKey(
        winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_SET_VALUE
    ) as key:
        if user_value == "":
            try:
                winreg.DeleteValue(key, "PATH")
            except OSError:
                pass
        else:
            # Preserve REG_EXPAND_SZ if any %VAR% references are present
            value_type = (
                winreg.REG_EXPAND_SZ
                if re.search(r"%\w+%", user_value)
                else winreg.REG_SZ
            )
            winreg.SetValueEx(key, "PATH", 0, value_type, user_value)
    # Notify running processes of the environment change (best effort)
    try:
        import win32con
        import win32gui

        win32gui.SendMessageTimeout(
            win32con.HWND_BROADCAST,
            win32con.WM_SETTINGCHANGE,
            0,
            "Environment",
            win32con.SMTO_ABORTIFHUNG,
            5000,
        )
    except Exception:
        pass
    return None


def _apply_linux(entries):
    """Persist the entries to the systemd user environment file"""
    conf_directory = os.path.join(os.path.expanduser("~"), ".config", "environment.d")
    os.makedirs(conf_directory, exist_ok=True)
    conf_file = os.path.join(conf_directory, "path.conf")
    with open(conf_file, "w", encoding="utf-8") as f:
        f.write('PATH="{}"\n'.format(":".join(entries)))
    return None


class SystemPathManipulator(qt.QWidget):
    """Tab widget for editing the PATH environment variable"""

    # Name of the tab that hosts this widget
    TAB_NAME = "PATH"
    # Displayed name (used by the tab widget status bar)
    name = ""
    # Current tab icon
    current_icon = None
    # This widget is not savable
    savable = constants.CanSave.NO

    def __init__(self, parent=None, main_form=None):
        """Initialization"""
        super().__init__(parent)
        self.main_form = main_form
        self.name = "PATH environment variable editor"
        # Icon/corner-button manipulator used by the tab widget system
        self.internals = components.internals.Internals(parent=self, tab_widget=parent)
        # Set the tab icon
        self.current_icon = functions.create_icon("tango_icons/settings.png")
        self.setFont(settings.get_current_font())
        self._sections = []
        self._build_ui()
        self._reload()
        self.update_style()

    def __del__(self):
        try:
            self.main_form = None
            self.internals = None
            self.setParent(None)
            self.deleteLater()
        except:
            pass

    def _build_ui(self):
        """Create and layout all of the child widgets"""
        main_layout = qt.QVBoxLayout(self)
        main_layout.setContentsMargins(6, 6, 6, 6)
        main_layout.setSpacing(6)

        # Title label
        title_label = qt.QLabel("PATH environment variable", self)
        title_label.setAlignment(qt.Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # Scroll area that hosts the section group boxes
        self._scroll = qt.QScrollArea(self)
        self._scroll.setWidgetResizable(True)
        self._scroll.setFrameShape(qt.QFrame.Shape.NoFrame)
        self._rows_host = qt.QWidget(self._scroll)
        self._rows_layout = qt.QVBoxLayout(self._rows_host)
        self._rows_layout.setContentsMargins(2, 2, 2, 2)
        self._rows_layout.setSpacing(6)
        self._rows_layout.addStretch()
        self._scroll.setWidget(self._rows_host)
        main_layout.addWidget(self._scroll, 1)

        # Section group boxes (global/system and user on Windows, single on Linux)
        if data.on_windows:
            self._create_section(
                "Global PATH (system)",
                system=True,
                add_tooltip="Add a new global (system) path entry",
            )
            self._create_section(
                "User PATH",
                system=False,
                add_tooltip="Add a new user path entry",
            )
        else:
            self._create_section(
                "PATH entries",
                system=False,
                add_tooltip="Add a new path entry",
            )

        # Bottom bar
        bottom_layout = qt.QHBoxLayout()
        bottom_layout.setSpacing(6)

        add_button = qt.QToolButton(self)
        add_button.setIcon(functions.create_icon("tango_icons/session-add.png"))
        if data.on_windows:
            add_button.setToolTip("Add a new user path entry")
        else:
            add_button.setToolTip("Add a new path entry")
        add_button.setAutoRaise(True)
        add_button.clicked.connect(lambda: self._add_empty_row(system=False))
        bottom_layout.addWidget(add_button)

        self._status_label = qt.QLabel("", self)
        bottom_layout.addWidget(self._status_label, 1)

        reload_button = qt.QPushButton("Reload", self)
        reload_button.setToolTip(
            "Discard unsaved changes and reload the PATH from the system"
        )
        reload_button.clicked.connect(self._reload)
        bottom_layout.addWidget(reload_button)

        apply_button = qt.QPushButton("Apply", self)
        apply_button.setToolTip(
            "Apply the changes to the current session and persist them to the OS "
            "environment (modifying system entries requires administrator privileges)"
        )
        apply_button.clicked.connect(self._apply)
        bottom_layout.addWidget(apply_button)

        main_layout.addLayout(bottom_layout)

    def _set_status(self, text):
        """Display a status/feedback message below the list"""
        self._status_label.setText(text)

    def _create_section(self, title, system, add_tooltip):
        """Create a titled section group box hosting its own set of path rows"""
        groupbox = qt.QGroupBox(title, self._rows_host)
        group_layout = qt.QVBoxLayout(groupbox)
        group_layout.setContentsMargins(6, 8, 6, 6)
        group_layout.setSpacing(4)

        rows_layout = qt.QVBoxLayout()
        rows_layout.setSpacing(4)
        group_layout.addLayout(rows_layout)

        # Add button at the bottom, below all of the rows
        add_button_layout = qt.QHBoxLayout()
        add_button_layout.setContentsMargins(0, 0, 0, 0)
        add_button_layout.addStretch()
        add_button = qt.QToolButton(groupbox)
        add_button.setIcon(functions.create_icon("tango_icons/session-add.png"))
        add_button.setToolTip(add_tooltip)
        add_button.setAutoRaise(True)
        add_button.clicked.connect(lambda: self._add_empty_row(system))
        add_button_layout.addWidget(add_button)
        group_layout.addLayout(add_button_layout)

        section = {
            "groupbox": groupbox,
            "rows_layout": rows_layout,
            "rows": [],
            "system": system,
        }
        self._sections.append(section)
        self._rows_layout.insertWidget(self._rows_layout.count() - 1, groupbox)
        return section

    def _section_for(self, system):
        """Return the section that hosts entries of the given scope"""
        for section in self._sections:
            if section["system"] == system:
                return section
        return self._sections[0]

    def _section_containing(self, row):
        """Return the section that currently holds the given row"""
        for section in self._sections:
            if row in section["rows"]:
                return section
        return None

    def _reload(self):
        """Reload all of the rows from the OS PATH value"""
        self._set_status("")
        self._clear_rows()
        user, system = get_os_path_entries()
        # Windows merge order: system entries first, then user entries
        for entry in system:
            self._add_row(entry, system=True)
        for entry in user:
            self._add_row(entry, system=False)
        count = sum(len(section["rows"]) for section in self._sections)
        if count == 1:
            self._set_status("Loaded 1 path entry from the system")
        elif count > 1:
            self._set_status("Loaded {} path entries from the system".format(count))
        else:
            self._set_status("No PATH entries found - use the + button to add one")

    def _clear_rows(self):
        """Remove and delete all of the current rows"""
        for section in self._sections:
            for row in section["rows"]:
                section["rows_layout"].removeWidget(row)
                row.setParent(None)
                row.deleteLater()
            section["rows"] = []

    def _add_row(self, text="", system=False):
        """Append a new row to the given section and return its reference"""
        section = self._section_for(system)
        row = SystemPathManipulator.PathRow(
            section["groupbox"], text=text, system=system, on_delete=self._remove_row
        )
        section["rows"].append(row)
        section["rows_layout"].addWidget(row)
        return row

    def _add_empty_row(self, system=False):
        """Add a new empty row to the given section and start editing it"""
        # Only one empty path entry is allowed at a time
        for section in self._sections:
            for row in section["rows"]:
                if not row.line_edit.text().strip():
                    self._set_status("Only one empty path entry is allowed at a time")
                    row.start_edit()
                    return
        self._set_status("")
        row = self._add_row("", system=system)
        row.start_edit()

    def _remove_row(self, row):
        """Remove a single row from its section"""
        section = self._section_containing(row)
        if section is not None:
            if row in section["rows"]:
                section["rows"].remove(row)
            section["rows_layout"].removeWidget(row)
        row.setParent(None)
        row.deleteLater()
        self._set_status("")

    def _apply(self):
        """Apply the current rows to the OS environment and the current process"""
        user_entries = []
        system_entries = []
        for section in self._sections:
            for row in section["rows"]:
                text = row.line_edit.text().strip()
                if not text:
                    continue
                if row.system:
                    system_entries.append(text)
                else:
                    user_entries.append(text)

        # Warn about duplicates (case-insensitive on Windows)
        all_entries = user_entries + system_entries
        seen = set()
        duplicates = set()
        for entry in all_entries:
            key = os.path.normcase(entry) if data.on_windows else entry
            if key in seen:
                duplicates.add(entry)
            seen.add(key)
        if duplicates:
            self._set_status(
                "Warning: duplicate path entr{} - {}".format(
                    "ies" if len(duplicates) > 1 else "y",
                    ", ".join(sorted(duplicates)),
                )
            )

        error = apply_os_path_entries(user_entries, system_entries)
        if error:
            self._set_status("Error applying PATH: " + error)
            if self.main_form is not None:
                self.main_form.display.repl_display_error("PATH editor: " + error)
        else:
            self._set_status(
                "PATH updated in the current session and persisted to the OS environment."
            )
            if self.main_form is not None:
                self.main_form.display.repl_display_message(
                    "PATH environment variable updated!",
                    message_type=constants.MessageType.SUCCESS,
                )
            # Refresh the rows from the persisted value
            self._reload()

    def update_style(self):
        """Apply the current theme to the widget and its children"""
        theme = settings.get_theme()
        background = theme["fonts"]["default"]["background"]
        color = theme["fonts"]["default"]["color"]
        passive_background = theme["indication"]["passivebackground"]
        passive_border = theme["indication"]["passiveborder"]
        hover = theme["indication"]["hover"]
        active_background = theme["indication"]["activebackground"]
        active_border = theme["indication"]["activeborder"]
        font_name = settings.get("current_font_name")
        font_size = settings.get("current_font_size")
        self.setStyleSheet(f"""
QScrollArea {{
    background: {background};
    border: 1px solid {passive_border};
}}
QScrollArea > QWidget > QWidget {{
    background: {background};
}}
QGroupBox {{
    background: transparent;
    color: {color};
    border: 1px solid {passive_border};
    margin-top: 10px;
    padding: 4px 6px 6px 6px;
    font-family: {font_name};
    font-size: {font_size}pt;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 8px;
    padding: 0 4px;
    color: {color};
    background: {background};
}}
QLabel {{
    background: transparent;
    color: {color};
    border: none;
    font-family: {font_name};
    font-size: {font_size}pt;
}}
QLineEdit {{
    background: {passive_background};
    color: {color};
    border: 1px solid {passive_border};
    padding: 2px 5px;
    font-family: {font_name};
    font-size: {font_size}pt;
}}
QLineEdit[editing=true] {{
    background: {active_background};
    border: 1px solid {active_border};
}}
QToolButton {{
    background: transparent;
    border: none;
}}
QToolButton:hover {{
    background: {hover};
}}
QPushButton {{
    background: {passive_background};
    color: {color};
    border: 1px solid {passive_border};
    padding: 3px 12px;
    font-family: {font_name};
    font-size: {font_size}pt;
}}
QPushButton:hover {{
    background: {hover};
    border: 1px solid {active_border};
}}
        """)

    class PathRow(qt.QWidget):
        """A single row of the PATH list: path text + edit + remove buttons"""

        def __init__(self, parent, text="", system=False, on_delete=None):
            """Initialization"""
            super().__init__(parent)
            self.system = system
            self._on_delete = on_delete
            self._original_text = text
            layout = qt.QHBoxLayout(self)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(4)

            self.line_edit = qt.QLineEdit(text, self)
            self.line_edit.setProperty("system", system)
            self.line_edit.setProperty("editing", False)
            self.line_edit.setReadOnly(True)
            if system:
                self.line_edit.setToolTip(
                    "System PATH entry - administrator privileges required to modify"
                )
            self.line_edit.installEventFilter(self)
            self.line_edit.editingFinished.connect(self._finish_edit)
            layout.addWidget(self.line_edit, 1)

            self.edit_button = qt.QToolButton(self)
            self.edit_button.setIcon(
                functions.create_icon("tango_icons/session-edit.png")
            )
            self.edit_button.setToolTip("Edit this path")
            self.edit_button.setAutoRaise(True)
            self.edit_button.clicked.connect(self.start_edit)
            layout.addWidget(self.edit_button)

            self.remove_button = qt.QToolButton(self)
            self.remove_button.setIcon(
                functions.create_icon("tango_icons/session-remove.png")
            )
            self.remove_button.setToolTip("Remove this path")
            self.remove_button.setAutoRaise(True)
            self.remove_button.clicked.connect(lambda: self._on_delete(self))
            layout.addWidget(self.remove_button)

        def eventFilter(self, obj, event):
            """Reject the current edit with the Escape key"""
            if (
                obj is self.line_edit
                and not self.line_edit.isReadOnly()
                and event.type() == qt.QEvent.Type.KeyPress
                and event.key() == qt.Qt.Key.Key_Escape
            ):
                self.line_edit.setText(self._original_text)
                self._finish_edit()
                return True
            return super().eventFilter(obj, event)

        def start_edit(self):
            """Enter edit mode for this row"""
            self._original_text = self.line_edit.text()
            self.line_edit.setProperty("editing", True)
            self.line_edit.setReadOnly(False)
            self.line_edit.setFocus()
            self.line_edit.selectAll()
            self._repolish()

        def _finish_edit(self):
            """Leave edit mode, committing the current text"""
            self.line_edit.setReadOnly(True)
            self.line_edit.setProperty("editing", False)
            self._repolish()

        def _repolish(self):
            """Force the stylesheet to pick up the property changes"""
            self.line_edit.style().unpolish(self.line_edit)
            self.line_edit.style().polish(self.line_edit)
