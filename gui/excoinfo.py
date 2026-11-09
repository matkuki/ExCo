"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import os
import os.path
import functions
import qt
import data
import constants


"""
-----------------------------------------------------------------------------------
ExCo Information Widget for displaying the license, used languages and libraries, ...
-----------------------------------------------------------------------------------
"""


class ExCoInfo(qt.QDialog):
    # Class variables
    name: str = "Ex.Co. Info"
    savable = constants.CanSave.NO

    # Class functions(methods)
    def __init__(self, parent: qt.QWidget, app_dir: str = "") -> None:
        """Initialization routine"""
        # Initialize superclass, from which the current class is inherited,
        # THIS MUST BE DONE SO THAT THE SUPERCLASS EXECUTES ITS __init__ !!!!!!
        super().__init__()
        # Setup the window
        self.setWindowTitle("About Ex.Co.")
        self.setWindowFlags(qt.Qt.WindowType.WindowStaysOnTopHint)
        # Setup the picture
        exco_picture = qt.QPixmap(data.about_image)
        self.picture: qt.QLabel | None = qt.QLabel(self)
        self.picture.setPixmap(exco_picture)
        self.picture.setGeometry(self.frameGeometry())
        self.picture.setScaledContents(True)
        # Assign events
        self.picture.mousePressEvent = self._close  # type: ignore[assignment]
        self.picture.mouseDoubleClickEvent = self._close  # type: ignore[assignment]
        # Initialize layout
        self.info_layout: qt.QGridLayout | None = qt.QGridLayout()
        self.info_layout.addWidget(self.picture)
        self.info_layout.setSpacing(0)
        self.info_layout.setContentsMargins(qt.QMargins(0, 0, 0, 0))
        self.setLayout(self.info_layout)
        # Set the log window icon
        if os.path.isfile(data.application_icon) == True:
            self.setWindowIcon(qt.QIcon(data.application_icon))
        # Save the info window geometry, the values were gotten by showing a dialog with the label containing
        # the ExCo info image with the size set to (50, 50), so it would automatically resize to the label image size
        my_width = 610
        my_height = 620
        # Set the info window position
        parent_left = parent.geometry().left()
        parent_top = parent.geometry().top()
        parent_width = parent.geometry().width()
        parent_height = parent.geometry().height()
        my_left = parent_left + (parent_width / 2) - (my_width / 2)
        my_top = parent_top + (parent_height / 2) - (my_height / 2)
        self.setGeometry(functions.create_rect(my_left, my_top, my_width, my_height))
        self.setFixedSize(my_width, my_height)

    #        self.setStyleSheet("background-color:transparent;")
    #        self.setWindowFlags(qt.Qt.WindowType.WindowStaysOnTopHint | qt.Qt.Dialog | qt.Qt.WindowType.FramelessWindowHint)
    #        self.setAttribute(qt.Qt.WidgetAttribute.WA_TranslucentBackground)

    def _close(self, event: qt.QMouseEvent | None) -> None:
        """Close the widget"""
        if self.picture is not None:
            self.picture.setParent(None)
        self.picture = None
        self.info_layout = None
        self.close()
