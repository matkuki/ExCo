# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2023 Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import qt
import data
import constants

from .repllineedit import *
from .replhelper import *


class ReplBox(qt.QGroupBox):
    main_form = None
    repl = None
    repl_helper = None

    def __init__(self, parent, interpreter_references, *args, **kwargs):
        super().__init__(parent)
        self.setObjectName("REPL_Box")
        self.main_form = parent
        self.repl = ReplLineEdit(self, parent, interpreter_references=interpreter_references)
        self.repl.setObjectName("REPL_line")
        self.repl_helper = ReplHelper(self, parent, self.repl)
        self.repl_helper.setObjectName("REPL_multiline")
        # Create layout and children
        repl_layout = qt.QVBoxLayout()
        repl_layout.setContentsMargins(4,4,4,4)
        repl_layout.setSpacing(0)
        repl_layout.addWidget(self.repl)
        repl_layout.addWidget(self.repl_helper)
        self.setLayout(repl_layout)
        # Set the defaults
        self.set_repl(constants.ReplType.SINGLE_LINE, constants.ReplLanguage.Python)
        self.indication_reset()
        # Set default font
        self.setFont(data.get_current_font())

    def set_repl(self,
                 _type: constants.ReplType,
                 language: constants.ReplLanguage) -> None:
        if language == constants.ReplLanguage.Python:
            self.setTitle("Python Interactive Interpreter (REPL)")
        elif language == constants.ReplLanguage.Hy:
            self.setTitle("Hy Interactive Interpreter (REPL)")
        else:
            raise Exception("Unsupported REPL language: {}".format(language))
        # Set the interpreter language
        self.repl.set_language(language)
        # Set which REPL widget will be displayed
        if _type == constants.ReplType.SINGLE_LINE:
            self.repl.setVisible(True)
            self.repl_helper.setVisible(False)
            self.repl_state = constants.ReplType.SINGLE_LINE
        else:
            self.repl.setVisible(False)
            self.repl_helper.setVisible(True)
            self.repl_state = constants.ReplType.MULTI_LINE
    
    def cycle_language(self) -> constants.ReplLanguage:
        for i,lang in enumerate(constants.ReplLanguage):
            if lang == self.repl.get_language():
                if i == (len(constants.ReplLanguage) - 1):
                    new_lang = constants.ReplLanguage(0)
                else:
                    new_lang = constants.ReplLanguage(i + 1)
                self.set_repl(self.repl_state, new_lang)
                self.main_form.display.repl_indicator.set_language(new_lang)
                return

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

