"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.

PyQt / Qt stuff

NOTE:
    Objects are imported so that they can be used either directly with qt.QSize,
    or by specifiying the full namespace with qt.PyQt.QtCore.QSize!
"""
import PyQt6.Qsci
import PyQt6.QtCore
import PyQt6.QtGui
import PyQt6.QtWidgets
import PyQt6.sip

PyQt = PyQt6
sip = PyQt6.sip

from PyQt6.Qsci import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
