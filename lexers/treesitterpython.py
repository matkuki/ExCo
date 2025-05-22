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


class TreeSitterPython(TreeSitterLexer):
    """
    Custom tree-sitter lexer for the Makefile language
    """
    # Constants
    NAME = "Python"
    TREE_SITTER_LEXER = "python"

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
        "number": 8,
        "classname": 9,
        "functionmethodname": 10,
    }
    
    symbols = {
        "default": {
            "index": styles["default"],
            "items": (
                "identifier",
            ),
            "previous-special": (
                ("class", "classname"),
                ("def", "functionmethodname"),
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
            "is-span": False,
        },
        "string": {
            "index": styles["string"],
            "items": (
                '"',
                "'",
            ),
            "is-span": True,
        },
        "basickeyword": {
            "index": styles["basickeyword"],
            "items": tuple(
                
            ),
        },
        "keyword": {
            "index": styles["keyword"],
            "items": (
                '_', '__build_class__', '__debug__', '__doc__', '__import__', '__loader__', '__name__', '__package__', '__spec__', 'abs', 'aiter', 'all', 'and', 'anext', 'any', 'arithmeticerror', 'as', 'ascii', 'assert', 'assertionerror', 'async', 'attributeerror', 'await', 'baseexception', 'bin', 'blockingioerror', 'bool', 'break', 'breakpoint', 'brokenpipeerror', 'buffererror', 'bytearray', 'bytes', 'byteswarning', 'callable', 'case', 'childprocesserror', 'chr', 'class', 'classmethod', 'compile', 'complex', 'connectionabortederror', 'connectionerror', 'connectionrefusederror', 'connectionreseterror', 'continue', 'copyright', 'credits', 'def', 'del', 'delattr', 'deprecationwarning', 'dict', 'dir', 'divmod', 'elif', 'ellipsis', 'else', 'encodingwarning', 'enumerate', 'environmenterror', 'eoferror', 'eval', 'except', 'exception', 'exec', 'exit', 'false', 'fileexistserror', 'filenotfounderror', 'filter', 'finally', 'float', 'floatingpointerror', 'for', 'format', 'from', 'frozenset', 'futurewarning', 'generatorexit', 'getattr', 'global', 'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'if', 'import', 'importerror', 'importwarning', 'in', 'indentationerror', 'indexerror', 'input', 'int', 'interruptederror', 'ioerror', 'is', 'isadirectoryerror', 'isinstance', 'issubclass', 'iter', 'keyboardinterrupt', 'keyerror', 'lambda', 'len', 'license', 'list', 'locals', 'lookuperror', 'map', 'match', 'max', 'memoryerror', 'memoryview', 'min', 'modulenotfounderror', 'nameerror', 'next', 'none', 'nonlocal', 'not', 'notadirectoryerror', 'notimplemented', 'notimplementederror', 'object', 'oct', 'open', 'or', 'ord', 'oserror', 'overflowerror', 'pass', 'pendingdeprecationwarning', 'permissionerror', 'pow', 'print', 'processlookuperror', 'property', 'quit', 'raise', 'range', 'recursionerror', 'referenceerror', 'repr', 'resourcewarning', 'return', 'reversed', 'round', 'runtimeerror', 'runtimewarning', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'stopasynciteration', 'stopiteration', 'str', 'sum', 'super', 'syntaxerror', 'syntaxwarning', 'systemerror', 'systemexit', 'taberror', 'timeouterror', 'true', 'try', 'tuple', 'type', 'typeerror', 'unboundlocalerror', 'unicodedecodeerror', 'unicodeencodeerror', 'unicodeerror', 'unicodetranslateerror', 'unicodewarning', 'userwarning', 'valueerror', 'vars', 'warning', 'while', 'windowserror', 'with', 'yield', 'zerodivisionerror', 'zip'
            ),
            "is-span": False,
        },
        "topkeyword": {
            "index": styles["topkeyword"],
            "items": (
                "def",
                "import",
                "class",
#                "function_definition",
            ),
            "is-span": False,
        },
        "operator": {
            "index": styles["operator"],
            "items": (
                "(", ")",
                "[", "]",
                "{", "}",
                "<", ">", 
                "+", "-",
                "*", "**", "/",
                ":", "!", "?", "|",
                ".", ",", "=", "==",
                "+=", "-=", "*=", "/=",
                ">=", "<=", "!=",
                "->", "@",
                "escape_sequence",
            ),
            "is-span": False,
        },
        "number": {
            "index": styles["number"],
            "items": (
                "integer",
                "float",
            ),
            "is-span": False,
        },
        "classname": {
            "index": styles["classname"],
            "items": tuple(),
            "is-span": False,
        },
        "functionmethodname": {
            "index": styles["functionmethodname"],
            "items": tuple(),
            "is-span": False,
        },
    }
    
    # Characters that autoindent one level on pressing Return/Enter
    autoindent_characters = [":"]
