# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-present Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import re
import math
import typing

import qt
import data
import functions

class Hotspots:
    """
    Functions for styling text with hotspots (used by CustomEditor and PlainEditor)
    """    
    def style(self, editor, index_from, length, color=0xff0000):
        """
        Style the text from/to with a hotspot
        """
        send_scintilla = editor.SendScintilla
        qscintilla_base = qt.QsciScintillaBase
        #Use the scintilla low level messaging system to set the hotspot
        send_scintilla(qscintilla_base.SCI_STYLESETHOTSPOT, 2, True)
        send_scintilla(qscintilla_base.SCI_SETHOTSPOTACTIVEFORE, True, color)
        send_scintilla(qscintilla_base.SCI_SETHOTSPOTACTIVEUNDERLINE, True)
        send_scintilla(qscintilla_base.SCI_STARTSTYLING, index_from, 2)
        send_scintilla(qscintilla_base.SCI_SETSTYLING, length, 2)