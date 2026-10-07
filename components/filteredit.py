"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.

For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import functions
import qt
import settings

from gui.stylesheets import StyleSheetLineEdit


class FilterField(qt.QLineEdit):
    """
    A filter box, styled identically wherever one appears.

    This is the single place a filter field gets its look: the field style
    sheet, the theme's close glyphs on the clear button and the
    Escape-to-clear behaviour all live here, so the tree filter bar, the
    Recent Files search box and the settings filter read as the same chrome
    without each one re-deriving it.
    """

    focus_in = qt.pyqtSignal()

    def __init__(
        self, parent: qt.QWidget | None = None, placeholder: str = "Filter"
    ) -> None:
        super().__init__(parent)
        self.setObjectName("filter_field")
        self.setPlaceholderText(placeholder)
        self.setClearButtonEnabled(True)
        self.__clear_button: qt.QToolButton | None = self.findChild(qt.QToolButton)
        self.__close_icon = qt.QIcon()
        self.__close_hover_icon = qt.QIcon()
        if self.__clear_button is not None:
            self.__clear_button.installEventFilter(self)
        self.installEventFilter(self)
        self.apply_filter_style()
        # A QLineEdit does not stretch vertically on its own (its vertical
        # size policy is Fixed), so in a bar of fixed height it would sit at
        # its small sizeHint with dead space above and below. Stretch so the
        # field fills whatever vertical room the filter area offers.
        self.setSizePolicy(
            qt.QSizePolicy.Policy.Expanding, qt.QSizePolicy.Policy.Expanding
        )

    def apply_filter_style(self) -> None:
        """Re-read the theme and restyle the field and its clear glyphs."""
        self._apply_close_icons()
        self.setStyleSheet(StyleSheetLineEdit.standard())

    def _apply_close_icons(self) -> None:
        """Put the theme's close glyphs on the clear button, themed again."""
        theme = settings.get_theme()
        self.__close_icon = qt.QIcon(functions.get_resource_file(theme["close-image"]))
        self.__close_hover_icon = qt.QIcon(
            functions.get_resource_file(theme["close-hover-image"])
        )
        if self.__clear_button is not None:
            self.__clear_button.setIcon(self.__close_icon)

    def eventFilter(self, object: qt.QObject, event: qt.QEvent) -> bool:  # type: ignore[override]
        """Swap the clear glyph while hovered; announce when the field gains focus."""
        if object is self.__clear_button:
            if event.type() == qt.QEvent.Type.Enter:
                self.__clear_button.setIcon(self.__close_hover_icon)
            elif event.type() == qt.QEvent.Type.Leave:
                self.__clear_button.setIcon(self.__close_icon)
        elif object is self and event.type() == qt.QEvent.Type.FocusIn:
            self.focus_in.emit()
        return False

    def keyPressEvent(self, event: qt.QKeyEvent) -> None:  # type: ignore[override]
        """Clear the filter when the user presses Escape."""
        if event.key() == qt.Qt.Key.Key_Escape:
            self.clear()
            return
        super().keyPressEvent(event)

    def mousePressEvent(self, event: qt.QMouseEvent) -> None:  # type: ignore[override]
        """Keep a right press inside the field instead of the tree below.

        QLineEdit does not accept the right-button press, so it used to
        propagate to the tree tab, which read the position in the view's own
        coordinates, selected the top row and raised its context menu over the
        field. Swallow the press here, and let the release show the standard
        cut/copy/paste edit menu the field already provides.
        """
        if event.button() == qt.Qt.MouseButton.RightButton:
            event.accept()
            return
        super().mousePressEvent(event)
