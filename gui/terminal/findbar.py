"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

##  FILE DESCRIPTION:
##      Scrollback find bar for the integrated terminal emulator.
##      A small overlay strip holding the query editor, a match counter and
##      previous/next/close buttons. It owns no search state: the view scans
##      the screen stack and drives this widget through signals, so the bar
##      can be tested and re-styled without knowing how the grid is stored.

from typing import Optional, cast

import qt


class _FindEdit(qt.QLineEdit):
    """Query editor that turns Enter / Shift+Enter / Escape into signals.

    QLineEdit accepts Return itself and emits ``returnPressed`` without the
    modifier, so Shift+Enter would be indistinguishable from Enter. Escape is
    ignored by QLineEdit and would propagate to the parent chain, which is not
    where the close logic lives.
    """

    next_pressed = qt.pyqtSignal()
    previous_pressed = qt.pyqtSignal()
    dismissed = qt.pyqtSignal()

    def keyPressEvent(self, event: Optional[qt.QKeyEvent]) -> None:  # type: ignore[override]
        if event is None:
            return super().keyPressEvent(event)
        if event.key() == qt.Qt.Key.Key_Escape:
            self.dismissed.emit()
            event.accept()
            return
        if event.key() in (qt.Qt.Key.Key_Return, qt.Qt.Key.Key_Enter):
            if event.modifiers() & qt.Qt.KeyboardModifier.ShiftModifier:
                self.previous_pressed.emit()
            else:
                self.next_pressed.emit()
            event.accept()
            return
        super().keyPressEvent(event)


class TerminalFindBar(qt.QWidget):
    """Overlay find strip for the terminal's scrollback."""

    query_changed = qt.pyqtSignal(str)
    next_requested = qt.pyqtSignal()
    previous_requested = qt.pyqtSignal()
    closed = qt.pyqtSignal()

    def __init__(self, parent: Optional[qt.QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("TerminalFindBar")
        layout: qt.QHBoxLayout = qt.QHBoxLayout(self)
        layout.setContentsMargins(6, 4, 6, 4)
        layout.setSpacing(4)

        self._edit: _FindEdit = _FindEdit(self)
        self._edit.setPlaceholderText("Find in scrollback")
        self._edit.setClearButtonEnabled(True)
        self._status: qt.QLabel = qt.QLabel("", self)
        self._status.setMinimumWidth(64)
        self._status.setAlignment(
            qt.Qt.AlignmentFlag.AlignRight | qt.Qt.AlignmentFlag.AlignVCenter
        )
        self._previous: qt.QToolButton = qt.QToolButton(self)
        self._previous.setIcon(self._standard_icon(qt.QStyle.StandardPixmap.SP_ArrowUp))
        self._previous.setToolTip("Previous match (Shift+Enter)")
        self._next: qt.QToolButton = qt.QToolButton(self)
        self._next.setIcon(self._standard_icon(qt.QStyle.StandardPixmap.SP_ArrowDown))
        self._next.setToolTip("Next match (Enter)")
        self._close: qt.QToolButton = qt.QToolButton(self)
        self._close.setIcon(
            self._standard_icon(qt.QStyle.StandardPixmap.SP_DialogCloseButton)
        )
        self._close.setToolTip("Close (Esc)")
        layout.addWidget(self._edit, 1)
        layout.addWidget(self._status)
        layout.addWidget(self._previous)
        layout.addWidget(self._next)
        layout.addWidget(self._close)

        self._edit.textChanged.connect(self.query_changed)
        self._edit.next_pressed.connect(self._emit_next)
        self._edit.previous_pressed.connect(self._emit_previous)
        self._edit.dismissed.connect(self._emit_closed)
        self._previous.clicked.connect(self._emit_previous)
        self._next.clicked.connect(self._emit_next)
        self._close.clicked.connect(self._emit_closed)

    # --------------------------------------------------------------
    # Signals (clicked passes a checked bool; these slots drop it)
    # --------------------------------------------------------------
    def _standard_icon(self, pixmap: qt.QStyle.StandardPixmap) -> qt.QIcon:
        """Standard icon from the current style (the stub types both the
        widget's style and the application style as possibly None, which a
        constructed widget's style never is)."""
        style: qt.QStyle = cast(qt.QStyle, self.style() or qt.QApplication.style())
        return style.standardIcon(pixmap)

    def _emit_next(self) -> None:
        self.next_requested.emit()

    def _emit_previous(self) -> None:
        self.previous_requested.emit()

    def _emit_closed(self) -> None:
        self.closed.emit()

    # --------------------------------------------------------------
    # State
    # --------------------------------------------------------------

    def set_status(self, text: str) -> None:
        """Set the match counter / message shown between the editor and the
        buttons ("3 of 12", "No matches")."""
        self._status.setText(text)

    def status_text(self) -> str:
        return self._status.text()

    def query(self) -> str:
        return self._edit.text()

    def set_query(self, text: str) -> None:
        """Replace the query; the editor's textChanged signal reports it back
        to the view exactly as typing would."""
        self._edit.setText(text)

    def focus_editor(self) -> None:
        """Focus the query editor and preselect the previous query."""
        self._edit.setFocus(qt.Qt.FocusReason.ShortcutFocusReason)
        self._edit.selectAll()

    def keyPressEvent(self, event: Optional[qt.QKeyEvent]) -> None:  # type: ignore[override]
        # Escape reaches the bar when a button (not the editor) has focus.
        if event is not None and event.key() == qt.Qt.Key.Key_Escape:
            self.closed.emit()
            event.accept()
            return
        super().keyPressEvent(event)

    # --------------------------------------------------------------
    # Theming
    # --------------------------------------------------------------

    def apply_style(self, fg: qt.QColor, bg: qt.QColor) -> None:
        """Theme the strip from the terminal's default colours so it stays
        readable on any palette, like the copy toast."""
        self.setStyleSheet(
            (
                "#TerminalFindBar {{ background-color: rgba({0},{1},{2},242);"
                " border: 1px solid rgba({3},{4},{5},120); border-radius: 3px; }}"
                "#TerminalFindBar QLabel {{ color: rgba({3},{4},{5},255);"
                " background: transparent; border: none; }}"
                "#TerminalFindBar QLineEdit {{"
                " background-color: rgba({3},{4},{5},22);"
                " color: rgba({3},{4},{5},255);"
                " border: 1px solid rgba({3},{4},{5},90);"
                " border-radius: 2px; padding: 1px 4px; }}"
                "#TerminalFindBar QToolButton {{ border: none;"
                " background: transparent; padding: 2px; }}"
                "#TerminalFindBar QToolButton:hover {{"
                " background-color: rgba({3},{4},{5},30); }}"
            ).format(
                bg.red(),
                bg.green(),
                bg.blue(),
                fg.red(),
                fg.green(),
                fg.blue(),
            )
        )
