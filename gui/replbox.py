
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2021 Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import os
import sys
import itertools
import inspect
import functools
import keyword
import re
import collections
import textwrap
import importlib
import data
import components
import themes
import functions
import interpreter
import settings
import lexers
import traceback
import gc

from .repllineedit import *
from .replhelper import *


class ReplBox(data.QGroupBox):
    _parent = None
    repl = None
    repl_helper = None
    
    def __init__(self, parent, interpreter_references, *args, **kwargs):
        super().__init__("Python Interactive Interpreter (REPL)")
        self.setObjectName("REPL_Box")
        self._parent = parent
        self.repl = ReplLineEdit(self, parent, interpreter_references=interpreter_references)
        self.repl.setObjectName("REPL_line")
        self.repl_helper = ReplHelper(self, parent, self.repl)
        self.repl_helper.setObjectName("REPL_multiline")
        # Create layout and children
        repl_layout = data.QVBoxLayout()
        repl_layout.setContentsMargins(4,4,4,4)
        repl_layout.setSpacing(0)
        repl_layout.addWidget(self.repl)
        repl_layout.addWidget(self.repl_helper)
        self.setLayout(repl_layout)
        # Set the defaults
        self.set_repl(data.ReplType.SINGLE_LINE)
        self.indication_reset()
        # Set default font
        self.setFont(data.get_current_font())
    
    def set_repl(self, type):
        #Set which REPL widget will be displayed
        if type == data.ReplType.SINGLE_LINE:
            self.repl.setVisible(True)
            self.repl_helper.setVisible(False)
            self.repl_state = data.ReplType.SINGLE_LINE
        else:
            self.repl.setVisible(False)
            self.repl_helper.setVisible(True)
            self.repl_state = data.ReplType.MULTI_LINE
    
    def indication_set(self):
        self.set_style(True)
        self.repl.update_style()
        self.repl.indication_set()
    
    def indication_reset(self):
        self.set_style(False)
        self.repl.update_style()
        self.repl.indication_reset()
    
    def set_style(self, indicated):
        if indicated:
            background = data.theme["indication"]["activebackground"]
            border = data.theme["indication"]["activeborder"]
        else:
            background = data.theme["indication"]["passivebackground"]
            border = data.theme["indication"]["passiveborder"]
        self.setStyleSheet("""
#REPL_Box {{
    font-size: 8pt;
    font-weight: bold;
    color: {};
    background-color: {};
    border: 2px solid {};
    border-radius: 0px;
    margin-top: 6px;
    margin-bottom: 0px;
    margin-left: 0px;
    margin-right: 0px;
    padding-top: 4px;
    padding-bottom: 0px;
    padding-left: 0px;
    padding-right: 0px;
}}
#REPL_Box::title {{
    color: {};
    subcontrol-position: top left;
    padding: 0px; 
    left: 8px;
    top: -6px;
}}
        """.format(
                 border,
                 data.theme["indication"]["passivebackground"],
                 border,
                 data.theme["indication"]["activeborder"],
        ))
        
        