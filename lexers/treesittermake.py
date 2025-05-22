"""
Copyright (c) 2013-present Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import data
import functions
import time

# Relative imports
from typing import *
from .treesitter import *


class TreeSitterMakefile(TreeSitterLexer):
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
        "default": {
            "index": styles["default"],
            "items": (
                "word",
            ),
            "is-span": False,
        },
        "comment": {
            "index": styles["comment"],
            "items": (
                "comment",
            ),
            "is-span": False,
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
                '"',
                "'",
            ),
            "is-span": False,
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
            "is-span": False,
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
            "is-span": False,
        },
        "topkeyword": {
            "index": styles["topkeyword"],
            "items": (
                "$",
                "filter",
                "shell_text",
                "eval",
                "recipe",
            ),
            "is-span": False,
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
                "=", ":=", ",", ";", 
                "^", "<", ">", "@",
            ),
            "is-span": False,
        },
    }
    
    # Characters that autoindent one level on pressing Return/Enter
    autoindent_characters = [":"]
