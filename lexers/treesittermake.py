# -*- coding: utf-8 -*-

"""
Copyright (c) 2022 Matic Kukovec.
"""

import data
import functions
import time

# Relative imports
from typing import *
from .treesitterbase import *


class TreeSitterMakefile(TreeSitterBaseLexer):
    """
    Custom tree-sitter lexer for the Makefile language
    """
    # Constants
    NAME = "Makefile"
    TREE_SITTER_LEXER = "make"

    # Class variables
    styles = {
        "default": 0,
        "comment": 1,
        "string": 2,
        "keyword": 3,
        "topkeyword": 4,
        "basickeyword": 5,
        "error": 6,
        "operator": 7,
    }
    
    symbols = {
        "comment": {
            "index": styles["comment"],
            "items": (
                "comment",
            ),
        },
        "error": {
            "index": styles["error"],
            "items": (
                "error",
            ),
        },
        "string": {
            "index": styles["string"],
            "items": (
                "raw_text",
                "realpath",
                "text",
            ),
        },
        "basickeyword": {
            "index": styles["basickeyword"],
            "items": (
                "define",
                "else",
                "endef",
                "endif",
                "if",
                "ifeq",
                "ifneq",
                "include",
            ),
        },
        "keyword": {
            "index": styles["keyword"],
            "items": (
                "abspath",
                "call",
                "dir",
                "error"
                "filter",
                "firstword",
                "info",
                "lastword",
                "patsubst",
                "shell",
                "sort",
                "subst",
                "vpath",
                "warning",
                "wildcard",
            ),
        },
        "topkeyword": {
            "index": styles["topkeyword"],
            "items": (
                "$",
            ),
        },
        "operator": {
            "index": styles["operator"],
            "items": (
                "(", ")",
                "[", "]",
                "{", "}",
                "+", "-",
                "*", "/",
                ":", "!", "?", "|",
            ),
        },
    }
    
    # Characters that autoindent one level on pressing Return/Enter
    autoindent_characters = [":"]
