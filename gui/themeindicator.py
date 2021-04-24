
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2021 Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import os
import sip
import os.path
import traceback
import functions
import data
import components
import themes

class ThemeIndicator(data.QLabel):
    def __init__(self, parent):
        # Initialize superclass
        super().__init__()
        # Store the reference to the parent
        self._parent = parent
    
    def mouseReleaseEvent(self, event):
        # Execute the superclass event method
        super().mouseReleaseEvent(event)
        cursor = data.QCursor.pos()
        self._parent.theme_menu.popup(cursor)
    
    def set_image(self, image):
        raw_picture = data.QPixmap(
            os.path.join(
                data.resources_directory, image
            )
        )
        picture = raw_picture.scaled(16, 16, data.Qt.KeepAspectRatio)
        self.setPixmap(picture)
    
    def restyle(self):
        self.setStyleSheet("""
            QLabel { 
                background-color: transparent;
                border: none;
                padding-top: 0px;
                padding-bottom: 0px;
                padding-left: 0px;
                padding-right: 4px;
            }
            QToolTip { 
                color: black; 
                padding-top: 0px;
                padding-bottom: 0px;
                padding-left: 0px;
                padding-right: 0px; 
            }
        """)




