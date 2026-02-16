"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

from __future__ import annotations

from typing import Any

import re

import data
import settings
import functions
import lexers
import qt


class Zig(qt.QsciLexerCustom):
    """
    Custom lexer for the Zig programming languages
    """

    styles: dict[str, int] = {
        "Default": 0,
        "Comment": 1,
        "keyword1": 2,
        "keyword2": 3,
        "keyword3": 4,
        "keywordsecondary": 5,
        "keywordset3": 6,
        "keyword": 7,
        "keywordset5": 8,
        "keywordset6": 9,
        "keywordset7": 10,
        "String": 11,
        "Number": 12,
        "Operator": 13,
    }
    keyword_remap: dict[str, str] = {
        "Keywords": "keyword",
        "Builtins": "keyword1",
        "Types": "keyword3",
        "Fields": "keyword3",
    }
    # Class variables
    keyword_dictionary: dict[str, tuple[str, ...]] = {
        "Keywords": (
            "align",
            "allowzero",
            "and",
            "anyframe",
            "anytype",
            "asm",
            "async",
            "await",
            "break",
            "callconv",
            "catch",
            "comptime",
            "const",
            "continue",
            "defer",
            "else",
            "enum",
            "errdefer",
            "error",
            "export",
            "extern",
            "false",
            "fn",
            "for",
            "if",
            "inline",
            "noalias",
            "noinline",
            "null",
            "or",
            "orelse",
            "packed",
            "pub",
            "resume",
            "return",
            "set",
            "sizeof",
            "static",
            "struct",
            "suspend",
            "switch",
            "test",
            "threadlocal",
            "true",
            "try",
            "union",
            "unreachable",
            "usingnamespace",
            "var",
            "volatile",
            "while",
        ),
        "Builtins": (
            "@addrSpaceCast",
            "@addWithOverflow",
            "@alignCast",
            "@alignOf",
            "@as",
            "@atomicLoad",
            "@atomicRmw",
            "@atomicStore",
            "@bitCast",
            "@bitOffsetOf",
            "@bitSizeOf",
            "@branchHint",
            "@breakpoint",
            "@mulAdd",
            "@byteSwap",
            "@bitReverse",
            "@offsetOf",
            "@call",
            "@cDefine",
            "@cImport",
            "@cInclude",
            "@clz",
            "@cmpxchgStrong",
            "@cmpxchgWeak",
            "@compileError",
            "@compileLog",
            "@constCast",
            "@ctz",
            "@cUndef",
            "@cVaArg",
            "@cVaCopy",
            "@cVaEnd",
            "@cVaStart",
            "@divExact",
            "@divFloor",
            "@divTrunc",
            "@embedFile",
            "@enumFromInt",
            "@errorFromInt",
            "@errorName",
            "@errorReturnTrace",
            "@errorCast",
            "@export",
            "@extern",
            "@field",
            "@fieldParentPtr",
            "@FieldType",
            "@floatCast",
            "@floatFromInt",
            "@frameAddress",
            "@hasDecl",
            "@hasField",
            "@import",
            "@inComptime",
            "@intCast",
            "@intFromBool",
            "@intFromEnum",
            "@intFromError",
            "@intFromFloat",
            "@intFromPtr",
            "@max",
            "@memcpy",
            "@memset",
            "@memmove",
            "@min",
            "@wasmMemorySize",
            "@wasmMemoryGrow",
            "@mod",
            "@mulWithOverflow",
            "@panic",
            "@popCount",
            "@prefetch",
            "@ptrCast",
            "@ptrFromInt",
            "@rem",
            "@returnAddress",
            "@select",
            "@setEvalBranchQuota",
            "@setFloatMode",
            "@setRuntimeSafety",
            "@shlExact",
            "@shlWithOverflow",
            "@shrExact",
            "@shuffle",
            "@sizeOf",
            "@splat",
            "@reduce",
            "@src",
            "@sqrt",
            "@sin",
            "@cos",
            "@tan",
            "@exp",
            "@exp2",
            "@log",
            "@log2",
            "@log10",
            "@abs",
            "@floor",
            "@ceil",
            "@trunc",
            "@round",
            "@subWithOverflow",
            "@tagName",
            "@This",
            "@trap",
            "@truncate",
            "@Type",
            "@typeInfo",
            "@typeName",
            "@TypeOf",
            "@unionInit",
            "@Vector",
            "@volatileCast",
            "@workGroupId",
            "@workGroupSize",
            "@workItemId",
        ),
        "Types": (
            "i8",
            "u8",
            "i16",
            "u16",
            "i32",
            "u32",
            "i64",
            "u64",
            "i128",
            "u128",
            "isize",
            "usize",
            "c_char",
            "c_short",
            "c_ushort",
            "c_int",
            "c_uint",
            "c_long",
            "c_ulong",
            "c_longlong",
            "c_ulonglong",
            "c_longdouble",
            "f16",
            "f32",
            "f64",
            "f80",
            "f128",
            "bool",
            "anyopaque",
            "void",
            "noreturn",
            "type",
            "anyerror",
            "comptime_int",
            "comptime_float",
        ),
    }
    operator_list = [
        "=",
        "+",
        "-",
        "*",
        "/",
        "<",
        ">",
        "$",
        ".",
        "~",
        "&",
        "%",
        "|",
        "!",
        "?",
        "^",
        ":",
        '"',
        "[",
        "]",
    ]
    splitter = re.compile(
        r"(\{\.|\.\}|\\\\|///|//|@[a-zA-Z0-9_]*|\.[a-zA-Z0-9_]*(?=\s*=)|\#|\'|\"\"\"|\n|\s+|\w+|\W)"
    )
    # Characters that autoindent one level on pressing Return/Enter
    autoindent_characters = ["{"]
    # String start/end tokens
    tokens_string = ('"',)
    tokens_multiline_string = "\\\\"
    # Comment tokens
    tokens_comment = ["//", "///"]

    def __init__(self, parent: Any = None) -> None:
        """
        Overridden initialization
        """
        # Initialize superclass
        super().__init__()
        # Set the default style values
        self.setDefaultColor(
            qt.QColor(settings.get_theme()["fonts"]["default"]["color"])
        )
        self.setDefaultPaper(
            qt.QColor(settings.get_theme()["fonts"]["default"]["background"])
        )
        self.setDefaultFont(settings.get_editor_font())
        # Reset autoindentation style
        self.setAutoIndentStyle(0)
        # Set the theme
        self.set_theme(settings.get_theme())

    def language(self) -> str:
        return "Zig"

    def description(self, style: int) -> str:
        if style < len(self.styles):
            description = "Custom lexer for the Zig languages"
        else:
            description = ""
        return description

    def defaultStyle(self) -> int:
        return self.styles["Default"]

    def braceStyle(self) -> int:
        return self.styles["Default"]

    def defaultFont(self, style: int | None = None) -> qt.QFont:
        return qt.QFont(
            settings.get("current_font_name"), settings.get("current_font_size")
        )

    def set_theme(self, theme: dict[str, Any]) -> None:
        for style in self.styles:
            # Papers
            self.setPaper(
                qt.QColor(settings.get_theme()["fonts"][style.lower()]["background"]),
                self.styles[style],
            )
            # Fonts
            lexers.set_font(self, style, theme["fonts"][style.lower()])

    def styleText(self, start: int, end: int) -> None:
        """
        Overloaded method for styling text.
        """
        # Style in pure Python, VERY SLOW!
        editor = self.editor()
        if editor is None:
            return
        # Initialize the styling
        self.startStyling(start)
        # Scintilla works with bytes, so we have to adjust
        # the start and end boundaries
        text = bytearray(editor.text(), "utf-8")[start:end].decode("utf-8")
        # Loop optimizations
        setStyling = self.setStyling
        operator_list = self.operator_list
        keyword_dictionary = self.keyword_dictionary
        # Initialize various states and split the text into tokens
        stringing = False
        multiline_stringing = False
        commenting = False
        tokens = [
            (token, len(bytearray(token, "utf-8")))
            for token in self.splitter.findall(text)
        ]
        # Style the tokens accordingly
        for i, token in enumerate(tokens):
            if commenting == True:
                # Continuation of comment
                setStyling(token[1], self.styles["Comment"])
                # Check if comment ends
                if "\n" in token[0]:
                    commenting = False
            elif stringing == True:
                # Continuation of a string
                setStyling(token[1], self.styles["String"])
                # Check if string ends
                if token[0] == '"' and (tokens[i - 1][0] != "\\") or "\n" in token[0]:
                    stringing = False
            elif multiline_stringing == True:
                # Continuation of a string
                setStyling(token[1], self.styles["String"])
                # Check if string ends
                if "\n" in token[0]:
                    multiline_stringing = False
            elif token[0] == self.tokens_multiline_string:
                setStyling(token[1], self.styles["String"])
                multiline_stringing = True
            elif token[0] in self.tokens_comment:
                setStyling(token[1], self.styles["Comment"])
                commenting = True
            elif token[0] in self.tokens_string:
                # Start of a string
                setStyling(token[1], self.styles["String"])
                stringing = True
            elif token[0] in operator_list:
                setStyling(token[1], self.styles["Operator"])
            elif token[0] in keyword_dictionary["Keywords"]:
                setStyling(token[1], self.styles[self.keyword_remap["Keywords"]])
            elif token[0] in keyword_dictionary["Builtins"]:
                setStyling(token[1], self.styles[self.keyword_remap["Builtins"]])
            elif token[0] in keyword_dictionary["Types"]:
                setStyling(token[1], self.styles[self.keyword_remap["Types"]])
            elif token[0].startswith("."):
                setStyling(1, self.styles["Default"])
                setStyling(token[1] - 1, self.styles[self.keyword_remap["Fields"]])
            elif functions.is_number(token[0]):
                setStyling(token[1], self.styles["Number"])
            else:
                setStyling(token[1], self.styles["Default"])
