"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import data

# Tree-sitter modules
import tree_sitter

import functions
import lexers

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
                "lexers/treesitter_parsers_{}.so".format(data.platform.lower()),
            ),
            self.tree_sitter_lexer,
        )
        self.parser = tree_sitter.Parser()
        self.parser.set_language(tree_sitter_language)
        self.tree = None

    def text_modified_callback(
        self,
        position,
        modificationType,
        text,
        length,
        added,
        line,
        foldLevelNow,
        foldLevelPrev,
        token,
        annotationLinesAdded,
    ):
        editor = self.editor()
        if editor is None:
            return
        functions.performance_timer_start()
        # Tree-sitter works with bytes, so we have to adjust the start and end boundaries
        text_bytes = editor.text().encode("utf-8")
        #        self.tree = self.parser.parse(text_bytes)
        if modificationType == editor.SC_MOD_DELETETEXT:
            positions = (
                position,
                position + length,
                position,
                position,
                position + length,
                position,
            )
        else:
            positions = (
                position,
                position,
                position + length,
                position,
                position,
                position + length,
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
            #            new_tree = self.parser.parse(text_bytes, self.tree)
            #            old_tree = self.tree
            #            self.tree = new_tree
            #            print(len(self.tree.get_changed_ranges(old_tree)))
            self.tree = self.parser.parse(text_bytes, self.tree)
        else:
            self.tree = self.parser.parse(text_bytes)

        functions.performance_timer_show("CHANGE")

    def generate_tree(self, tree, start_byte, end_byte):
        functions.performance_timer_start()

        cursor = tree.walk()
        node_list = []
        came_up = False
        level = 0
        while True:
            if not came_up:
                if cursor.node.start_byte > (
                    start_byte - 50
                ) and cursor.node.start_byte < (end_byte + 50):
                    new_node = {
                        "type": cursor.node.type,
                        "start": cursor.node.start_byte,
                        "end": cursor.node.end_byte,
                        "level": level,
                    }
                    #                print(
                    #                    " " * level,
                    #                    new_node["type"],
                    #                    "{}:{}".format(new_node["start"],
                    #                    new_node["end"]),
                    #                )
                    node_list.append(new_node)
                if cursor.goto_first_child():
                    came_up = False
                    level += 1
                    continue
                elif cursor.goto_next_sibling():
                    came_up = False
                    continue
                elif cursor.goto_parent():
                    came_up = True
                    level -= 1
                    continue
            else:
                if cursor.goto_next_sibling():
                    came_up = False
                    continue
                elif cursor.goto_parent():
                    came_up = True
                    level -= 1
                    continue

            break

        functions.performance_timer_show("TREE-GENERATE")

        return node_list

    def styleText(self, start, end):
        """
        Main styling function, called everytime text changes
        """
        editor = self.editor()
        if editor is None:
            return

        node_list = self.generate_tree(self.tree, start, end)

        functions.performance_timer_start()

        # Loop optimizations
        setStyling = self.setStyling

        spanning = None
        spanning_end_index = None
        previous_item = None
        last_item = None
        for node in node_list:
            #            print(node)
            if node["start"] < (start - 50):
                continue
            elif node["start"] > (end + 50):
                continue

            self.startStyling(node["start"])
            length = node["end"] - node["start"]
            _type = node["type"].lower()
            last_item = node

            if spanning_end_index is not None and node["start"] > spanning_end_index:
                spanning = None
                spanning_end_index = None
            #                print("spanning-end", node["start"])
            if spanning is None:
                for kk, vv in self.symbols.items():
                    if _type in vv["items"]:
                        if (
                            "previous-special" in vv.keys()
                            and previous_item is not None
                        ):
                            for ps in vv["previous-special"]:
                                if ps[0] == previous_item["type"]:
                                    setStyling(length, self.symbols[ps[1]]["index"])
                                    break
                            else:
                                setStyling(length, vv["index"])
                        else:
                            setStyling(length, vv["index"])
                        if vv["is-span"]:
                            spanning = kk
                            spanning_end_index = node["end"]
                        #                            print("spanning", kk, node["start"])
                        break
                else:
                    #                    print("NOT FOUND:", f"'{_type}'", bytes(editor.text(), 'utf-8')[node["start"]:node["end"]].decode('utf-8'))
                    setStyling(length, self.styles["default"])
            else:
                setStyling(length, self.styles[spanning])

            previous_item = node
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
            "items": ("comment",),
            "is-span": True,
        },
        "error": {
            "index": styles["error"],
            "items": ("error",),
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
                "error" "filter",
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
            "items": ("integer",),
            "is-span": False,
        },
        "operator": {
            "index": styles["operator"],
            "items": (
                "(",
                ")",
                "[",
                "]",
                "{",
                "}",
                "+",
                "-",
                "*",
                "/",
                ":",
                "!",
                "?",
                "|",
                ">",
                "==",
                "-=",
                ",",
                "<<",
                ">>",
                "<",
                "!=",
                "=",
                "**",
                "%",
                "<=",
                ">=",
                "+=",
                ".",
                "escape_sequence",
            ),
            "is-span": False,
        },
        "identifier": {
            "index": styles["identifier"],
            "items": ("identifier",),
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
