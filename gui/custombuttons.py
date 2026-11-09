"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.

Custom buttons used by the FunctionWheel and ContextMenuHex in the forms module
"""

import math
import traceback
from collections.abc import Callable
from typing import Any, Optional

import components.hexbuilder
import constants
import data
import functions
import qt
import settings


class CustomButton(qt.QLabel):
    """
    Custom button used for displaying and executing Ex.Co. functions
    """

    # Class variables
    group_box_parent: Any = None
    main_form: Any = None
    stored_pixmap: qt.QPixmap | None = None
    stored_font: Any = None
    stored_hex: qt.QPixmap | None = None
    function: Callable[..., Any] | None = None
    function_text: str = ""
    stored_opacity: float = 0.0
    focus_last_widget: Any = True
    no_tab_focus_disable: bool = False
    no_document_focus_disable: bool = True
    check_last_tab_type: bool = False
    check_text_differ: Any = None
    tool_tip: str | None = None
    scale: tuple[float, float] = (1, 1)
    # Class constants
    OPACITY_LOW: float = 0.5
    OPACITY_HIGH: float = 1.0
    """
    This was measured by hand
    """
    INNER_IMAGE_OFFSET: tuple[int, int] = (18, 13)
    """
    This should be the actual pixel dimensions of the hex image file
    """
    HEX_IMAGE_SIZE: tuple[int, int] = (68, 60)

    def __init__(
        self,
        parent: Any,
        main_form: Any,
        input_pixmap: qt.QPixmap,
        input_function: Callable[..., Any] | None = None,
        input_function_text: str = "",
        input_font: qt.QFont = qt.QFont("Courier", 14, weight=qt.QFont.Weight.Bold),
        input_focus_last_widget: constants.HexButtonFocus = constants.HexButtonFocus.NONE,
        input_no_tab_focus_disable: bool = False,
        input_no_document_focus_disable: bool = True,
        input_check_last_tab_type: bool = False,
        input_check_text_differ: bool = False,
        input_tool_tip: str | None = None,
        input_scale: tuple[float, float] = (1, 1),
    ) -> None:
        # Initialize superclass
        super().__init__(parent)
        # Store the reference to the parent
        self._parent = parent
        # Store the reference to the main form
        self.main_form = main_form
        # Set default font
        self.setFont(settings.get_current_font())
        # Store the reference to the group box that holds the parent
        # (the parent of the parent)
        self.group_box_parent = parent.parent
        # Store the main function image
        self.stored_pixmap = input_pixmap
        # Store the hex edge image
        self.__create_hex_pixmap()
        # Store the function that will be executed on the click event
        self.function = input_function
        # Store the function text
        self.function_text = input_function_text
        # Set the attribute that will be check if focus update is needed
        # when the custom button executes its function
        self.focus_last_widget = input_focus_last_widget
        # Set the attribute that checks if any tab is focused
        self.no_tab_focus_disable = input_no_tab_focus_disable
        # Set the attribute that will be check if button will be disabled
        # if there is no focused document tab
        self.no_document_focus_disable = input_no_document_focus_disable
        # Set checking the save state stored in the main form
        self.check_last_tab_type = input_check_last_tab_type
        # Set checking for if the focused tab is a text differer
        self.check_text_differ = input_check_text_differ
        # Set the font that will be used with the button
        self.stored_font = input_font
        # Enable mouse move events
        self.setMouseTracking(True)
        # Set the tooltip if it was set
        if input_tool_tip != None:
            self.setToolTip(input_tool_tip)
        self.setToolTipDuration(0)
        # Set the scaling
        self.scale = input_scale

    @staticmethod
    def __create_hex_pixmap() -> None:
        if CustomButton.stored_hex is None:
            # CustomButton.stored_hex = functions.create_pixmap("various/hex-button-edge.png")
            hex_image_size = CustomButton.HEX_IMAGE_SIZE
            hex_edge_length = 29
            hex_edge_width = 4
            image = qt.QImage(
                *hex_image_size, qt.QImage.Format.Format_ARGB32_Premultiplied
            )
            image.fill(qt.Qt.GlobalColor.transparent)
            painter = qt.QPainter()
            painter.begin(image)

            hex_builder = components.hexbuilder.HexBuilder(
                painter, (0, 0), hex_edge_length
            )
            hex_builder.draw_full_hexagon(
                (int(hex_image_size[0] / 2) + 1, int(hex_image_size[1] / 2)),
                qt.QColor(settings.get_theme()["indication"]["passivebackground"]),
                hex_edge_width,
                qt.QColor(settings.get_theme()["context-menu-hex-edge"]),
            )
            painter.end()
            CustomButton.stored_hex = qt.QPixmap.fromImage(image)

    def _set_opacity(self, input_opacity: float) -> None:
        """Set the opacity of the stored QPixmap image and display it"""
        # Store the opacity
        self.stored_opacity = input_opacity
        # Create and initialize the QImage from the stored QPixmap
        button_image = self.stored_pixmap
        assert button_image is not None
        # Resize the button image to scale
        button_image = button_image.scaled(
            functions.create_size(
                math.ceil(button_image.size().width() * self.scale[0]),
                math.ceil(button_image.size().height() * self.scale[1]),
            ),
            transformMode=qt.Qt.TransformationMode.SmoothTransformation,
        )
        # Scale the hex image
        hex_image = self.stored_hex
        assert hex_image is not None
        scaled_size = functions.create_size(
            math.ceil(hex_image.size().width() * self.scale[0]),
            math.ceil(hex_image.size().height() * self.scale[1]),
        )
        image = qt.QImage(
            scaled_size,  # hex_image.size(),
            qt.QImage.Format.Format_ARGB32_Premultiplied,
        )
        image.fill(qt.Qt.GlobalColor.transparent)
        # Create and initialize the QPainter that will manipulate the QImage
        button_painter = qt.QPainter(image)
        button_painter.setOpacity(input_opacity)
        # Adjust inner button positioning according to the scale
        x_scaled = math.ceil(self.scale[0] * self.INNER_IMAGE_OFFSET[0])
        y_scaled = math.ceil(self.scale[1] * self.INNER_IMAGE_OFFSET[1])
        button_painter.drawPixmap(x_scaled, y_scaled, button_image)
        button_painter.end()
        # Display the manipulated image
        self.setPixmap(qt.QPixmap.fromImage(image))
        # Set the button mask, which sets the button area to the shape of
        # the button image instead of a rectangle
        self.setMask(hex_image.mask())

    def _set_opacity_with_hex_edge(self, input_opacity: float) -> None:
        """
        Set the opacity of the stored QPixmap image and display it
        """
        # Store the opacity
        self.stored_opacity = input_opacity
        # Create and initialize the QImage from the stored QPixmap
        button_image = self.stored_pixmap
        assert button_image is not None
        # Resize the button image to scale
        button_image = button_image.scaled(
            functions.create_size(
                math.ceil(button_image.size().width() * self.scale[0]),
                math.ceil(button_image.size().height() * self.scale[1]),
            ),
            transformMode=qt.Qt.TransformationMode.SmoothTransformation,
        )
        # Scale the hex image
        hex_image = self.stored_hex
        assert hex_image is not None
        scaled_size = functions.create_size(
            math.ceil(hex_image.size().width() * self.scale[0]),
            math.ceil(hex_image.size().height() * self.scale[1]),
        )
        image = qt.QImage(
            scaled_size,
            qt.QImage.Format.Format_ARGB32_Premultiplied,
        )
        image.fill(qt.Qt.GlobalColor.transparent)
        #        image.fill(settings.get_theme()["context-menu-background"])
        # Create and initialize the QPainter that will manipulate the QImage
        button_painter = qt.QPainter(image)
        button_painter.setCompositionMode(
            qt.QPainter.CompositionMode.CompositionMode_SourceOver
        )
        button_painter.setOpacity(input_opacity)
        # Resize the hex image to scale
        hex_image = hex_image.scaled(
            functions.create_size(
                math.ceil(hex_image.size().width() * self.scale[0]),
                math.ceil(hex_image.size().height() * self.scale[1]),
            ),
            transformMode=qt.Qt.TransformationMode.SmoothTransformation,
        )
        # Adjust inner button positioning according to the scale
        button_painter.drawPixmap(0, 0, hex_image)
        x_scaled = math.ceil(self.scale[0] * self.INNER_IMAGE_OFFSET[0])
        y_scaled = math.ceil(self.scale[1] * self.INNER_IMAGE_OFFSET[1])
        button_painter.drawPixmap(x_scaled, y_scaled, button_image)
        button_painter.end()
        # Display the manipulated image
        self.setPixmap(qt.QPixmap.fromImage(image))
        # Set the button mask, which sets the button area to the shape of
        # the button image instead of a rectangle
        self.setMask(hex_image.mask())

    def set_offset(self, offset: tuple[float, float]) -> None:
        self.setGeometry(
            int(offset[0]),
            int(offset[1]),
            math.ceil(self.scale[0] * self.HEX_IMAGE_SIZE[0]),
            math.ceil(self.scale[0] * self.HEX_IMAGE_SIZE[1]),
        )

    def mousePressEvent(self, event: qt.QMouseEvent | None) -> None:
        """Overloaded widget click event"""
        # Execute the superclass mouse click event first
        super().mousePressEvent(event)
        # Execute the function if it was initialized
        if self.function != None:
            try:
                # Set focus to the last focused widget stored on the main form
                if self.focus_last_widget == constants.HexButtonFocus.TAB:
                    self.main_form.last_focused_widget.currentWidget().setFocus()
                elif self.focus_last_widget == constants.HexButtonFocus.WINDOW:
                    self.main_form.last_focused_widget.setFocus()
                # Store the executed function for next cursor placement
                self.main_form.view.last_executed_function_text = self.function_text
                # Execute the buttons stored function
                self.function()
            except:
                traceback.print_exc()
                message = "You need to focus one of the editor windows first!"
                self.main_form.display.repl_display_message(
                    message, message_type=constants.MessageType.ERROR
                )
            # Close the function wheel
            self._parent.hide()

    def mouseMoveEvent(self, event: qt.QMouseEvent | None) -> None:
        """Overloaded mouse move event"""
        super().mouseMoveEvent(event)
        if self.isEnabled() == True:
            self.highlight()

    def enterEvent(self, event: qt.QEnterEvent | None) -> None:
        """Overloaded widget enter event"""
        super().enterEvent(event)
        # Bring the widget to the front of the Z-axis stack
        self.raise_()
        # Highlight the widget only if it's enabled
        if self.isEnabled() == True:
            self.highlight()

    def leaveEvent(self, event: qt.QEvent | None) -> None:
        """Overloaded widget leave event"""
        super().leaveEvent(event)
        # Dim the widget only if it's enabled
        if self.isEnabled() == True:
            self.dim()

    def dim(self, clear_hex_edge: bool = False) -> None:
        """Set the buttons opacity to low and clear the function text"""
        # Set the opacity to low
        if clear_hex_edge == True:
            self._set_opacity(self.OPACITY_LOW)
        else:
            self._set_opacity_with_hex_edge(self.OPACITY_LOW)
        # Clear the text in the parent display label
        self._parent.display("", self.stored_font)

    def highlight(self) -> None:
        """Set the buttons opacity to high and display the buttons function text"""
        # Set the opacity to full
        self._set_opacity_with_hex_edge(self.OPACITY_HIGH)
        # Display the stored function text
        self._parent.display(self.function_text, self.stored_font)


class DoubleButton(CustomButton):
    """
    A CustomButton with an extra button added to itself,
    used for when double functionality is needed, for example when
    a function has a version with or without a dialog window.
    """

    # The extra button reference
    main_form: Any = None
    extra_button: qt.QLabel | None = None
    extra_button_size_factor: float = 1 / 3
    extra_button_position: qt.QPoint = functions.create_point(0, 0)
    extra_button_stored_opacity: float | None = None
    extra_button_stored_pixmap: qt.QPixmap | None = None
    extra_button_function: Callable[..., Any] | None = None
    extra_button_function_text: str | None = None
    # Class constants
    OPACITY_LOW: float = 0.5
    OPACITY_HIGH: float = 1.0

    def init_extra_button(
        self,
        parent: Any,
        main_form: Any,
        input_extra_pixmap: qt.QPixmap,
        input_extra_function: Callable[..., Any] | None = None,
        input_extra_function_text: str = "",
    ) -> None:
        # Store the parent and main form references
        self._parent = parent
        self.main_form = main_form
        # Initialize the extra button
        self.extra_button = qt.QLabel(self)
        assert self.extra_button is not None
        width = int(self.geometry().width() * self.extra_button_size_factor)
        height = int(self.geometry().height() * self.extra_button_size_factor)
        self.extra_button_position = functions.create_point(
            int(self.geometry().width() * 2 / 3 - width),
            int(self.geometry().height() * 1 / 4),
        )
        rectangle = functions.create_rect(
            self.extra_button_position, functions.create_size(width, height)
        )
        self.extra_button.setGeometry(rectangle)
        self.extra_button_stored_pixmap = input_extra_pixmap
        self.extra_button.setPixmap(input_extra_pixmap)
        self.extra_button.setScaledContents(True)
        # Store the function options
        self.extra_button_function = input_extra_function
        self.extra_button_function_text = input_extra_function_text
        # Set the extra button opacity to low
        self._set_extra_button_opacity(self.OPACITY_LOW)
        # Overridden the extra buttons events
        self.extra_button.mousePressEvent = self.extra_button_click  # type: ignore[method-assign, assignment]
        self.extra_button.enterEvent = self.extra_button_enter_event  # type: ignore[method-assign]
        self.extra_button.leaveEvent = self.extra_button_leave_event  # type: ignore[method-assign, assignment]

    def extra_button_click(self, event: qt.QMouseEvent | None) -> None:
        """mousePressEvent for the extra button"""
        # Execute the function if it was initialized
        if self.extra_button_function != None:
            try:
                # Set focus to the last focused widget stored on the main form
                if self.focus_last_widget == constants.HexButtonFocus.TAB:
                    self.main_form.last_focused_widget.currentWidget().setFocus()
                elif self.focus_last_widget == constants.HexButtonFocus.WINDOW:
                    self.main_form.last_focused_widget.setFocus()
                # Store the executed function for next cursor placement
                self.main_form.view.last_executed_function_text = self.function_text
                # Execute the buttons stored function
                self.extra_button_function()
            except Exception as ex:
                message = "You need to focus one of the editor windows first!"
                self.main_form.display.repl_display_error(message)
            # Close the function wheel
            self._parent.hide()

    def extra_button_enter_event(self, event: qt.QEnterEvent | None) -> None:
        """Overloaded widget enter event"""
        # Check if the button is enabled
        if self.isEnabled() == True:
            self._set_extra_button_opacity(self.OPACITY_HIGH)
            # Display the stored extra buttons function text
            extra_button_font = qt.QFont(
                settings.get("current_font_name"),
                self.stored_font.pointSize() - 2,
                weight=qt.QFont.Weight.Bold,
            )
            self._parent.display(self.extra_button_function_text, extra_button_font)

    def extra_button_leave_event(self, event: qt.QEvent | None) -> None:
        """Overloaded widget enter event"""
        # Check if the button is enabled
        if self.isEnabled() == True:
            self._set_extra_button_opacity(self.OPACITY_LOW)
            # Clear the function text
            extra_button_font = qt.QFont(
                "Courier", self.stored_font.pointSize() - 2, weight=qt.QFont.Weight.Bold
            )
            self._parent.display("", extra_button_font)

    def extra_button_enable(self) -> None:
        """Hide and disable the extra button"""
        if self.extra_button is None:
            return
        self.extra_button.setVisible(True)
        self.extra_button.setEnabled(True)

    def extra_button_disable(self) -> None:
        """Hide and disable the extra button"""
        if self.extra_button is None:
            return
        self.extra_button.setVisible(False)
        self.extra_button.setEnabled(False)
        self._set_extra_button_opacity(self.OPACITY_LOW)

    def resizeEvent(self, event: qt.QResizeEvent | None) -> None:
        """Overridden resize event"""
        # Execute the superclass resize function
        super().resizeEvent(event)
        if self.extra_button is None:
            return
        # Update the extra button geometry
        width = int(self.geometry().width() * self.extra_button_size_factor)
        height = int(self.geometry().height() * self.extra_button_size_factor)
        rectangle = functions.create_rect(
            self.extra_button_position, functions.create_size(width, height)
        )
        self.extra_button.setGeometry(rectangle)

    def _set_extra_button_opacity(self, input_opacity: float) -> None:
        """Set the opacity of the extra button"""
        # Store the opacity
        self.extra_button_stored_opacity = input_opacity
        # Create and initialize the QImage from the stored QPixmap
        button_image = self.extra_button_stored_pixmap
        assert button_image is not None
        image = qt.QImage(
            button_image.size(), qt.QImage.Format.Format_ARGB32_Premultiplied
        )
        image.fill(qt.Qt.GlobalColor.transparent)
        # Create and initialize the QPainter that will manipulate the QImage
        button_painter = qt.QPainter(image)
        button_painter.setOpacity(input_opacity)
        button_painter.drawPixmap(0, 0, button_image)
        button_painter.end()
        # Display the manipulated image
        if self.extra_button is not None:
            self.extra_button.setPixmap(qt.QPixmap.fromImage(image))


class PushButtonBase(qt.QPushButton):
    function: Callable[..., Any] | None = None
    enter_function: Callable[..., Any] | None = None
    leave_function: Callable[..., Any] | None = None
    # Signals
    right_clicked = qt.pyqtSignal()
    text_changed = qt.pyqtSignal(str)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.update_style()

    def set_click_function(self, func: Callable[..., Any]) -> None:
        if self.function is not None:
            try:
                self.clicked.disconnect()
            except TypeError as e:
                print("ERROR: Could not disconnect clicked signal")
            self.function = None

        def actual_func(state: bool) -> None:
            func()

        self.clicked.connect(actual_func)
        self.function = func

    def set_enter_function(self, func: Callable[..., Any]) -> None:
        self.enter_function = func

    def set_leave_function(self, func: Callable[..., Any]) -> None:
        self.leave_function = func

    def enable(self) -> None:
        self.setEnabled(True)

    def disable(self) -> None:
        self.setEnabled(False)

    def keyPressEvent(self, e: qt.QKeyEvent | None) -> None:
        super().keyReleaseEvent(e)
        if e is None:
            return
        if e.key() == qt.Qt.Key.Key_Enter or e.key() == qt.Qt.Key.Key_Return:
            self.animateClick()

    def mousePressEvent(self, event: qt.QMouseEvent | None) -> None:
        if event is not None and event.button() == qt.Qt.MouseButton.RightButton:
            self.right_clicked.emit()
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: qt.QMouseEvent | None) -> None:
        super().mouseReleaseEvent(event)
        if event is not None:
            event.ignore()

    def enterEvent(self, e: qt.QEnterEvent | None) -> None:
        super().enterEvent(e)
        if self.isEnabled() == False:
            return
        # Execute the additional enter function
        if self.enter_function is not None:
            self.enter_function()

    def leaveEvent(self, e: qt.QEvent | None) -> None:
        super().leaveEvent(e)
        if self.isEnabled() == False:
            return
        # Execute the additional leave function
        if self.leave_function is not None:
            self.leave_function()

    def setText(self, e: str | None) -> None:
        super().setText(e)
        self.text_changed.emit(self.text())

    def update_style(self) -> None:
        pass


class StandardButton(PushButtonBase):
    # Class variables
    main_form: Any = None
    state: int = 0

    def __init__(
        self, parent: qt.QWidget | None, main_form: Any, *args: Any, **kwargs: Any
    ) -> None:
        super().__init__(parent, *args, **kwargs)
        self.main_form = main_form
        # Initialize focus
        self.set_focused(False)

    def set_focused(self, value: bool) -> None:
        self.setProperty("focused", value)
        style = self.style()
        assert style is not None
        style.unpolish(self)
        style.polish(self)


class CustomCheckBox(qt.QCheckBox):
    """
    A QCheckBox styled to look like a rounded button, displaying an image,
    and changing its background color when checked. Size is controlled via stylesheet
    and can be changed dynamically after instantiation.
    """

    def __init__(
        self,
        icon_path: str,
        width: int,
        height: int,
        parent: Optional[qt.QWidget] = None,
    ) -> None:
        """
        Initializes the custom checkbox.

        Args:
            icon_path (str): The path to the image file to be displayed in the middle.
            width (int): The initial desired width of the checkbox in pixels.
            height (int): The initial desired height of the checkbox in pixels.
            parent (Optional[qt.QWidget]): The parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.setCursor(qt.Qt.CursorShape.PointingHandCursor)

        self._icon_path: str = icon_path
        self.setIcon(qt.QIcon(self._icon_path))

        # Apply initial size and stylesheet
        self._apply_stylesheet_with_size(width, height)

    def _apply_stylesheet_with_size(self, width: int, height: int) -> None:
        """
        Internal helper method to construct and apply the stylesheet with dynamic size.

        Args:
            width (int): The new desired width of the checkbox in pixels.
            height (int): The new desired height of the checkbox in pixels.
        """
        # Adjust icon size proportionally to the new widget size
        self.setIconSize(qt.QSize(int(width * 0.5), int(height * 0.5)))

        self.setStyleSheet(
            f"""
            QCheckBox {{
                /* General button-like styling */
                width: {width}px; /* Set width via stylesheet */
                height: {height}px; /* Set height via stylesheet */
                border: 1px solid gray;
                padding: 5px; /* Padding around content */
                background-color: white; /* Default background color (unchecked) */
            }}
            QCheckBox:hover {{
                border: 1px solid darkgray; /* Subtle border change on hover */
            }}
            QCheckBox:checked {{
                background-color: lightgreen; /* Background color when checked */
            }}
            QCheckBox::indicator {{
                /* Hide the default checkbox indicator */
                width: 0px;
                height: 0px;
            }}
        """
        )

    def set_size(self, width: int, height: int) -> None:
        """
        Changes the size of the checkbox dynamically by updating its stylesheet.

        Args:
            width (int): The new desired width of the checkbox in pixels.
            height (int): The new desired height of the checkbox in pixels.
        """
        self._apply_stylesheet_with_size(width, height)
