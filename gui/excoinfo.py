
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2023 Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import os
import os.path
import collections
import traceback
import ast
import inspect
import math
import functools
import textwrap
import difflib
import re
import time
import settings
import functions
import data
import components
import themes


"""
-----------------------------------------------------------------------------------
ExCo Information Widget for displaying the license, used languages and libraries, ...
-----------------------------------------------------------------------------------
"""
class ExCoInfo(data.QDialog):
    #Class variables
    name    = "Ex.Co. Info"
    savable = data.CanSave.NO
    
    #Class functions(methods)
    def __init__(self, parent, app_dir=""):
        """Initialization routine"""
        #Initialize superclass, from which the current class is inherited,
        #THIS MUST BE DONE SO THAT THE SUPERCLASS EXECUTES ITS __init__ !!!!!!
        super().__init__()
        #Setup the window
        self.setWindowTitle("About Ex.Co.")
        self.setWindowFlags(data.Qt.WindowType.WindowStaysOnTopHint)
        #Setup the picture
        exco_picture = data.QPixmap(data.about_image)
        self.picture = data.QLabel(self)
        self.picture.setPixmap(exco_picture)
        self.picture.setGeometry(self.frameGeometry())
        self.picture.setScaledContents(True)
        #Assign events
        self.picture.mousePressEvent        = self._close
        self.picture.mouseDoubleClickEvent  = self._close
        #Initialize layout
        self.layout = data.QGridLayout()
        self.layout.addWidget(self.picture)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(
            data.QMargins(0,0,0,0)
        )
        self.setLayout(self.layout)
        #Set the log window icon
        if os.path.isfile(data.application_icon) == True:
            self.setWindowIcon(data.QIcon(data.application_icon))
        #Save the info window geometry, the values were gotten by showing a dialog with the label containing
        #the ExCo info image with the size set to (50, 50), so it would automatically resize to the label image size
        my_width    = 610
        my_height   = 620
        #Set the info window position
        parent_left     = parent.geometry().left()
        parent_top      = parent.geometry().top()
        parent_width    = parent.geometry().width()
        parent_height   = parent.geometry().height()
        my_left = parent_left + (parent_width/2) - (my_width/2)
        my_top = parent_top + (parent_height/2) - (my_height/2)
        self.setGeometry(
            functions.create_rect(
                my_left,
                my_top,
                my_width,
                my_height
            )
        )
        self.setFixedSize(my_width, my_height)
#        self.setStyleSheet("background-color:transparent;")
#        self.setWindowFlags(data.Qt.WindowType.WindowStaysOnTopHint | data.Qt.Dialog | data.Qt.WindowType.FramelessWindowHint)
#        self.setAttribute(data.Qt.WidgetAttribute.WA_TranslucentBackground)
    
    def _close(self, event):
        """Close the widget"""
        self.picture.setParent(None)
        self.picture = None
        self.layout = None
        self.close()

