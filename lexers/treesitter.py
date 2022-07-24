
# -*- coding: utf-8 -*-

"""
Copyright (c) 2022 Matic Kukovec.
"""

import data
import functions
import lexers
# Tree-sitter modules
import tree_sitter

# Relative imports
from .baselexer import *


class TreeSitterBaseLexer(BaseLexer):
    """
    Lexer for styling documents with the tree-sitter library
    """
    symbols = {}
    
    def __init__(self, name, tree_sitter_lexer, parent=None):
        """
        Overridden initialization
        """
        # Initialize superclass
        super().__init__(parent)
        # Initialize lexer types
        self.name = name
        self.tree_sitter_lexer = tree_sitter_lexer
        # Tree-sitter initialization
        tree_sitter_language = tree_sitter.Language(
            functions.unixify_join(
                data.resources_directory,
                "lexers/treesitter_parsers_{}.so".format(data.platform.lower())
            ),
            self.tree_sitter_lexer
        )
        self.parser = tree_sitter.Parser()
        self.parser.set_language(tree_sitter_language)
        self.tree = None

    def generate_tree(self, tree):
        cursor = tree.walk()
        node_list = []
        node_dict = {}
        stack = [ node_list ]
        came_up = False
        current_list = node_list
        level = 0
        while True:
            if not came_up:
                new_node = {
                    "type": cursor.node.type,
                    "start": cursor.node.start_byte,
                    "end": cursor.node.end_byte,
                    "level": level,
                    "children": []
                }
#                current_list.append(new_node)
                node_dict[new_node["start"]] = new_node
                if (cursor.goto_first_child()):
#                    stack.append(new_node["children"])
                    came_up = False
#                    current_list = stack[-1]
                    level += 1
                    continue
                elif (cursor.goto_next_sibling()):
                    came_up = False
                    current_list = stack[-1]
                    continue
                elif (cursor.goto_parent()):
#                    stack.pop()
                    came_up = True
#                    current_list = stack[-1]
                    level -= 1
                    continue
            else:
                if (cursor.goto_next_sibling()):
                    came_up = False
#                    current_list = stack[-1]
                    continue
                elif (cursor.goto_parent()):
#                    stack.pop()
                    came_up = True
#                    current_list = stack[-1]
                    level -= 1
                    continue
            
            break
        
        return node_list, node_dict
    
    def text_modified_callback(self,
                               position,
                               modificationType,
                               text,
                               length,
                               added,
                               line,
                               foldLevelNow,
                               foldLevelPrev,
                               token,
                               annotationLinesAdded):
        editor = self.editor()
        if editor is None:
            return
        functions.performance_timer_start()
        # Tree-sitter works with bytes, so we have to adjust the start and end boundaries
        text_bytes = editor.text().encode("utf-8")
        if modificationType == editor.SC_MOD_DELETETEXT:
            positions = (
                position,
                position+length,
                position,
                position,
                position+length,
                position,
            )
        else:
            positions = (
                position,
                position,
                position+length,
                position,
                position,
                position+length,
            )
        if self.tree is not None:
            self.tree.edit(
                start_byte=positions[0],
                old_end_byte=positions[1],
                new_end_byte=positions[2],
                start_point=(0, positions[3]),
                old_end_point=(0, positions[4]),
                new_end_point=(0, positions[5]),
            )
            self.tree = self.parser.parse(text_bytes, self.tree)
        else:
            self.tree = self.parser.parse(text_bytes)
#        self.tree = self.parser.parse(text_bytes)
        node_list, node_dict = self.generate_tree(self.tree)
        self.node_list = node_list
        self.node_dict = node_dict
        functions.performance_timer_show("CHANGE")
    
    def styleText(self, start, end):
        """
        Main styling function, called everytime text changes
        """
        editor = self.editor()
        if editor is None:
            return
        functions.performance_timer_start()
        
        # Initialize the styling
        self.startStyling(start)
        end_position = 0
        # Loop optimizations
        setStyling = self.setStyling
        
        last_item = None
        for k,v in self.node_dict.items():
#            if v["start"] < start:
#               continue
#            elif v["start"] > end:
#                break
            
            self.startStyling(v["start"])
            length = v["end"] - v["start"]
            _type = v["type"]
            last_item = v
            for k,v in self.symbols.items():
                if _type in v["items"]:
                    setStyling(length, v["index"])
                    break
            else:
                setStyling(length, self.styles["default"])
        else:
            if last_item:
                length = end - last_item["end"]
                if length > 0:
                    setStyling(length, self.styles["default"])
            else:
                length = end - start
                if length > 0:
                    setStyling(length, self.styles["default"])
        
        functions.performance_timer_show("STYLE")
        
class TreeSitterLexer(TreeSitterBaseLexer):
    """
    Custom tree-sitter lexer for all supported languages
    """

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
        "identifier": 9,
    }
    
    symbols = {
        "comment": {
            "index": styles["comment"],
            "items": (
                "comment",
            ),
            "is-span": True,
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
                "raw_text",
                "realpath",
                "text",
                '"',
            ),
            "is-span": True,
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
                "except",
                "or",
                "and",
                "continue",
                "for",
                "as",
                "in",
                "pass",
                "try",
                "except",
                "while",
                "elif",
                "break",
                "raise",
                "return",
                "not",
                "is",
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
                "none",
                "false",
                "true",
                "import",
                "class",
                "from",
                "def",
                "module",
            ),
            "is-span": False,
        },
        "integer": {
            "index": styles["number"],
            "items": (
                "integer",
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
                ">", "==", "-=", ",", "<<", ">>", 
                "<", "!=", "=", "**", "%", "<=", ">=",
                "+=", ".", "escape_sequence"
            ),
            "is-span": False,
        },
        "identifier": {
            "index": styles["identifier"],
            "items": (
                "identifier",
            ),
            "is-span": False,
        },
    }
    
    # Characters that autoindent one level on pressing Return/Enter
    autoindents = {
        "make": [":"],
        "python": [":"],
    }

    def __init__(self, name, tree_sitter_lexer, parent=None):
        """
        Overridden initialization
        """
        # Initialize superclass
        super().__init__(name, tree_sitter_lexer, parent)
        # Initialize autoindentation characters
        self.autoindent_characters = self.autoindents[tree_sitter_lexer]
        
