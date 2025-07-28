"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import functools
import qt
import data
import functions
import settings

from .custombuttons import *


"""
----------------------------------------------------------------
Overlay helper widget for visually selecting an Ex.Co. function
----------------------------------------------------------------
"""


class SettingsGuiManipulator(qt.QFrame):
    DEFAULT_SIZE = (640, 560)
    # Class variables
    _parent = None
    main_form = None
    background_image = None
    display_label = None
    cursor_show_position = None
    theme_name = None

    def __del__(self):
        try:
            self._parent = None
            self.main_form = None
            for child_widget in self.children():
                child_widget.deleteLater()
            # Clean up self
            self.setParent(None)
            self.deleteLater()
        except:
            pass

    def __init__(self, parent=None, main_form=None, settings_manipulator=None):
        # Initialize the superclass
        super().__init__(parent)
        # Store the reference to the parent
        self._parent = parent
        # Store the reference to the main form
        self.main_form = main_form
        # Set default font
        self.setFont(settings.get_current_font())
        # Set the layout
        #        self.__layout = qt.QGridLayout()
        #        self.__layout.setSpacing(10)
        #        self.__layout.setContentsMargins(
        #            qt.QMargins(0,0,0,0)
        #        )
        #        self.setLayout(self.__layout)
        # Initialize the display label that will display the function names
        # when the mouse cursor is over a function button
        self.display_label = qt.QLabel(self)
        self.display_label.setGeometry(8, 450, 200, 100)
        font = qt.QFont(settings.get("current_font_name"), 14)
        font.setBold(True)
        self.display_label.setFont(font)
        self.display_label.setAlignment(
            qt.Qt.AlignmentFlag.AlignHCenter | qt.Qt.AlignmentFlag.AlignVCenter
        )
        # Initialize all of the hex function buttons
        self.__init_options()
        # Position the overlay to the center of the screen
        self.center(qt.QSize(*self.DEFAULT_SIZE))
        # Scale the function wheel size if needed
        self.scale(1, 1)
        self.update_style()

    def __init_options(self):
        pass

    def hideEvent(self, event):
        """
        Overridden widget hide event
        """
        # Set focus to the last focused widget stored on the main form
        last_widget = self.main_form.last_focused_widget
        if last_widget is not None:
            if last_widget.currentWidget() is not None:
                last_widget.currentWidget().setFocus()

    def display(self, string, font):
        """
        Display string in the display label
        """
        # Setup additional font settings
        font.setBold(True)
        self.display_label.setFont(font)
        self.display_label.setAlignment(
            qt.Qt.AlignmentFlag.AlignHCenter | qt.Qt.AlignmentFlag.AlignVCenter
        )
        # Display the string
        self.display_label.setText(string)

    def hide(self):
        """
        Hide the settings manipulator
        """
        # Disable the function wheel
        self.setVisible(False)
        self.setEnabled(False)

    def show(self):
        """
        Show the settings manipulator
        """
        self.setVisible(True)
        self.setEnabled(True)
        # Center to main form
        self.center(self.size())
        self.setFocus()

    def scale(self, width_scale_factor=1, height_scale_factor=1):
        """
        Scale the size of the function wheel and all of its child widgets
        """
        # Scale the function wheel form
        geo = self.geometry()
        new_width = int(geo.width() * width_scale_factor)
        new_height = int(geo.height() * height_scale_factor)
        rectangle = functions.create_rect(
            geo.topLeft(), functions.create_size(new_width, new_height)
        )
        self.setGeometry(rectangle)
        # Center to main form
        self.center(self.size())

    def center(self, size):
        """
        Center the function wheel to the main form,
        according to the size parameter
        """
        x_offset = int((self.main_form.size().width() - size.width()) / 2)
        y_offset = int((self.main_form.size().height() * 93 / 100 - size.height()) / 2)
        rectangle_top_left = functions.create_point(x_offset, y_offset)
        rectangle_size = size
        rectangle = functions.create_rect(rectangle_top_left, rectangle_size)
        self.setGeometry(rectangle)

    def update_style(self):
        self.setStyleSheet(
            f"""
QFrame {{
    background-color: {settings.get_theme()["fonts"]["default"]["background"]};
    color: {settings.get_theme()["fonts"]["default"]["color"]};
    border: 1px solid {settings.get_theme()["indication"]["passiveborder"]};
    margin: 0px;
    padding: 0px;
    spacing: 0px;
}}
        """
        )
        self.display_label.setStyleSheet(
            f"""
QLabel {{
    background-color: {settings.get_theme()["fonts"]["default"]["background"]};
    color: {settings.get_theme()["fonts"]["default"]["color"]};
    border: 1px solid {settings.get_theme()["indication"]["activeborder"]};
    border-radius: 4px;
}}
        """
        )
