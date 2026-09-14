"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import qt
import data
import settings
import constants
import functions

from gui.custombuttons import *
from gui.stylesheets import *
from gui.templates import *


"""
---------------------------------------------------------
Custom Yes/No dialog window
---------------------------------------------------------
"""


class BaseDialog(qt.QDialog):
    # Replaced by each subclass: list of (text, tooltip, state_enum, is_wide [, width_scale])
    button_specs: list = []
    # When set, buttons are laid out in a grid with this many columns,
    # flowing column-first so pairs of buttons stack one below the other
    layout_columns: int | None = None

    def __init__(self, text, dialog_type=None, parent=None):
        super().__init__(parent)
        # Set the internal state
        self.state = None
        # Make the dialog stay on top
        self.setWindowFlags(qt.Qt.WindowType.WindowStaysOnTopHint)
        # Set the dialog icon and title
        self.setWindowIcon(qt.QIcon(data.application_icon))
        self.setWindowTitle(dialog_type.title())
        self.init_layout(text, dialog_type)
        # Set default font
        self.setFont(settings.get_current_font())
        # Update style
        self.update_style()

    def create_button_list(self):
        std = settings.get("standard_button_size")
        button_list = []
        for spec in self.button_specs:
            text, tooltip, state_enum, is_wide = spec[:4]
            width_scale: float = spec[4] if len(spec) > 4 else (1.5 if is_wide else 1.0)
            width = int(std * width_scale)
            button_list.append(
                {
                    "text": text,
                    "size": (width, std),
                    "tooltip": tooltip,
                    "state": state_enum.value,
                    "click-func": lambda *args, v=state_enum.value: self.done(v),
                }
            )
        return tuple(button_list)

    def init_layout(self, text, dialog_type):
        self.button_cache = []

        # Create the main layout
        main_layout = create_layout(
            layout=LayoutType.Vertical, margins=(8, 8, 8, 8), spacing=4
        )
        self.setLayout(main_layout)

        # Add the label
        label = qt.QLabel(self)
        label.setWordWrap(True)
        label.setAlignment(qt.Qt.AlignmentFlag.AlignCenter)
        label.setText(text)
        label.setMaximumWidth(700)
        main_layout.addWidget(label)

        # Add the button groupbox
        if self.layout_columns is None:
            button_frame = create_frame(
                layout=LayoutType.Horizontal,
                spacing=10,
                parent=self,
            )
        else:
            button_frame = create_frame(
                layout=LayoutType.Grid,
                spacing=10,
                parent=self,
            )
        button_layout = button_frame.layout()
        main_layout.addWidget(button_frame)

        button_list = self.create_button_list()
        rows_per_column = (
            (len(button_list) + self.layout_columns - 1) // self.layout_columns
            if self.layout_columns is not None
            else 0
        )
        # Create all of the buttons from the list
        for i, button in enumerate(button_list):
            new_button = StandardButton(
                self,
                None,
            )
            if button["text"] is not None:
                new_button.setText(button["text"])
            if button.get("icon") is not None:
                icon = functions.create_icon(button["icon"])
                new_button.setIcon(button)
                if button.get("size") is not None:
                    new_button.setIconSize(
                        qt.QSize(
                            int(button["size"][0] * 0.8), int(button["size"][1] * 0.8)
                        )
                    )
            new_button.setToolTip(button["tooltip"])
            new_button.setStatusTip(button["tooltip"])
            new_button.set_click_function(button["click-func"])
            new_button.state = button["state"]
            #            new_button.set_enter_function(
            #                create_enter_func(button.function_text, button.font)
            #            )
            #            new_button.set_leave_function(
            #                create_leave_func(button.font)
            #            )
            if button["size"] is not None:
                new_button.setFixedSize(
                    qt.QSize(int(button["size"][0]), int(button["size"][1]))
                )

            if self.layout_columns is None:
                button_layout.addWidget(new_button)
            else:
                row = i % rows_per_column
                col = i // rows_per_column
                button_layout.addWidget(
                    new_button, row, col, qt.Qt.AlignmentFlag.AlignHCenter
                )
            self.button_cache.append(new_button)

        self.set_state(len(self.button_cache) - 1)

        self.setWindowFlags(qt.Qt.WindowType.FramelessWindowHint)

    def showEvent(self, event):
        super().showEvent(event)
        self.center()

    def __set_button_states(self, button_states):
        if len(button_states) != len(self.button_cache):
            raise Exception(
                "Length mismatch: {} != {}".format(
                    len(button_states), len(self.button_cache)
                )
            )
        for i, item in enumerate(self.button_cache):
            item.set_focused(button_states[i])

    def __state_cycle(self, none_index, _reversed):
        if self.state is None:
            button = self.button_cache[none_index]
            button.set_focused(True)
            self.state = button.state

        next_state = -1
        button_list = self.button_cache
        if _reversed:
            button_list = reversed(self.button_cache)
        for i, button in enumerate(button_list):
            if self.state == button.state:
                next_state = i + 1 if i < (len(self.button_cache) - 1) else i
            if next_state == i:
                button.set_focused(True)
                self.state = button.state
            else:
                button.set_focused(False)

    def state_cycle_right(self):
        self.__state_cycle(0, False)

    def state_cycle_left(self):
        self.__state_cycle(len(self.button_cache) - 1, True)

    def set_state(self, index):
        for i, button in enumerate(self.button_cache):
            if index == i:
                button.set_focused(True)
                self.state = button.state
            else:
                button.set_focused(False)

    def center(self):
        if self.parent() is not None:
            qr = self.frameGeometry()
            geo = self.parent().frameGeometry()
            cp = functions.create_point(
                int((geo.width() / 2) - (qr.width() / 2)),
                int((geo.height() / 2) - (qr.height() / 2)),
            )
            self.move(cp)
        else:
            qr = self.frameGeometry()
            cp = self.screen().geometry().center()
            qr.moveCenter(cp)
            self.move(qr.topLeft())

    def keyPressEvent(self, key_event):
        pressed_key = key_event.key()
        # Check for escape keypress
        if pressed_key == qt.Qt.Key.Key_Escape:
            rightmost_button = self.button_cache[len(self.button_cache) - 1]
            rightmost_button.set_focused(True)
            self.repaint()
            self.done(rightmost_button.state)
        elif pressed_key == qt.Qt.Key.Key_Right:
            self.state_cycle_right()
        elif pressed_key == qt.Qt.Key.Key_Left:
            self.state_cycle_left()
        elif pressed_key == qt.Qt.Key.Key_Enter or pressed_key == qt.Qt.Key.Key_Return:
            if self.state is None:
                self.state = self.button_cache[len(self.button_cache) - 1].state
            self.done(self.state)

    def update_style(self):
        self.setStyleSheet(
            f"""
QDialog {{
    background-color: {settings.get_theme()["fonts"]["default"]["background"]};
    color: {settings.get_theme()["fonts"]["default"]["color"]};
    border: 1px solid {settings.get_theme()["indication"]["passiveborder"]};
    margin: 0px;
    padding: 0px;
    spacing: 0px;
}}
QGroupBox, QFrame {{
    background-color: {settings.get_theme()["fonts"]["default"]["background"]};
    color: {settings.get_theme()["fonts"]["default"]["color"]};
    border: none;
    margin: 0px;
    padding: 0px;
    spacing: 0px;
}}
QLabel {{
    background-color: {settings.get_theme()["fonts"]["default"]["background"]};
    color: {settings.get_theme()["fonts"]["default"]["color"]};
    border: none;
    font-family: {settings.get("current_font_name")};
    font-size: {settings.get("current_font_size")};
}}
{StyleSheetButton.standard()}
        """
        )
        for button in self.button_cache:
            button.update_style()

    @classmethod
    def blank(cls, text):
        return cls(text).exec()

    @classmethod
    def question(cls, text):
        return cls(text, "question").exec()

    @classmethod
    def warning(cls, text):
        return cls(text, "warning").exec()

    @classmethod
    def error(cls, text):
        return cls(text, "error").exec()


class YesNoDialog(BaseDialog):
    button_specs = [
        ("Yes", "Confirm the action", constants.DialogResult.Yes, False),
        ("No", "Decline the action", constants.DialogResult.No, False),
    ]


class OkDialog(BaseDialog):
    button_specs = [
        ("OK", "Close the dialog window", constants.DialogResult.No, False),
    ]


class DeleteDialog(BaseDialog):
    button_specs = [
        (
            "Move to\nRecycle Bin",
            "Send items to recycle bin (safer, can be recovered)",
            constants.DialogResult.RecycleBin,
            True,
        ),
        (
            "Permanent\nDelete",
            "Permanently delete items (cannot be recovered)",
            constants.DialogResult.PermanentDelete,
            True,
        ),
        ("Cancel", "Cancel the deletion", constants.DialogResult.Cancel, False),
    ]


class OverwriteDialog(BaseDialog):
    layout_columns = 3
    button_specs = [
        (
            "Overwrite",
            "Replace the existing item",
            constants.DialogResult.Yes,
            True,
        ),
        (
            "Overwrite all",
            "Replace all colliding items without asking",
            constants.DialogResult.OverwriteAll,
            True,
        ),
        (
            "Make a copy",
            "Paste it as a renamed copy",
            constants.DialogResult.Rename,
            True,
            2.0,
        ),
        (
            "Make all copies",
            "Paste all colliding items as renamed copies",
            constants.DialogResult.RenameAll,
            True,
            2.0,
        ),
        ("Skip", "Skip this item and continue", constants.DialogResult.No, False),
        (
            "Skip all",
            "Skip all colliding items without asking",
            constants.DialogResult.SkipAll,
            False,
        ),
    ]


class CloseEditorDialog(BaseDialog):
    button_specs = [
        (
            "Save \n&& Close",
            "Save document and close it",
            constants.DialogResult.SaveAndClose,
            True,
        ),
        (
            "Close",
            "Close the document without saving",
            constants.DialogResult.Close,
            False,
        ),
        (
            "Cancel",
            "Cancel closing of the document",
            constants.DialogResult.Cancel,
            False,
        ),
    ]


class ToggleOneWindowDialog(BaseDialog):
    button_specs = [
        (
            "Restore",
            "Restore the layout to the pre-one-window one",
            constants.DialogResult.Restore,
            False,
        ),
        (
            "Cancel",
            "Cancel closing of the document",
            constants.DialogResult.Cancel,
            False,
        ),
    ]


class QuitDialog(BaseDialog):
    button_specs = [
        (
            "Save all\n&& Quit",
            "Save all unsaved documents and quit ExCo",
            constants.DialogResult.SaveAllAndQuit,
            True,
        ),
        ("Quit", "Quit ExCo without saving", constants.DialogResult.Quit, False),
        ("Cancel", "Cancel quitting ExCo", constants.DialogResult.Cancel, False),
    ]


class RestoreSessionDialog(BaseDialog):
    button_specs = [
        (
            "Save \n&& Restore",
            "Save all documents and restore session",
            constants.DialogResult.SaveAndRestore,
            True,
        ),
        (
            "Close",
            "Restore the session without saving",
            constants.DialogResult.Restore,
            False,
        ),
        (
            "Cancel",
            "Cancel restoring of the session",
            constants.DialogResult.Cancel,
            False,
        ),
    ]
