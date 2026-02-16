"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

from __future__ import annotations

from typing import Any

import re

import qt
import data
import settings
import functions
import lexers


class SKILL(qt.QsciLexerCustom):
    """
    Custom lexer for the SKILL programming languages
    """

    styles: dict[str, int] = {
        "Default": 0,
        "Comment": 1,
        "PredefinedFunctions": 2,
        "Keyword": 3,
        "String": 4,
        "Number": 5,
        "Operator": 6,
    }
    # Class variables
    keyword_dictionary: dict[str, tuple[str, ...]] = {
        "PredefinedFunctions": (
            "alphalessp",
            "alphaNumCmp",
            "append",
            "append1",
            "apply",
            "predefined",
            "predicate",
            "assoc",
            "functions",
            "atom",
            "begin",
            "boundp",
            "break",
            "buildString",
            "string",
            "cadr",
            "callInitProc",
            "car",
            "case",
            "caseq",
            "cdr",
            "cdsGetInstPath",
            "changeWorkingDir",
            "className",
            "classOf",
            "classp",
            "close",
            "compareTime",
            "compress",
            "concat",
            "cond",
            "cons",
            "creating",
            "functions",
            "global",
            "control",
            "copy",
            "copy_<name>",
            "copyDefstructDeep",
            "createDir",
            "csh",
            "declare",
            "defclass",
            "defgeneric",
            "functions",
            "defInitProc",
            "function",
            "defmethod",
            "defprop",
            "defstructp",
            "defUserInitProc",
            "deleteDir",
            "deleteFile",
            "do",
            "documenting",
            "drain",
            "encrypt",
            "envobj",
            "eq",
            "equal",
            "err",
            "error",
            "errset",
            "errsetstring",
            "eval",
            "evalstring",
            "evenp",
            "exists",
            "Fibonacci",
            "fileLength",
            "fileSeek",
            "fileTell",
            "findClass",
            "fix",
            "float",
            "for",
            "forall",
            "foreach",
            "fprintf",
            "fscanf",
            "function",
            "function",
            "function",
            "functions.",
            "funobj",
            "gcsummary",
            "generic",
            "gensym",
            "get",
            "get_pname",
            "getc",
            "getCurrentTime",
            "getd",
            "getDirFiles",
            "getFnWriteProtect",
            "getInstallPath",
            "getqq",
            "gets",
            "getShellEnvVar",
            "getSkillPath",
            "getVarWriteProtect",
            "getVersion",
            "getWarn",
            "getWorkingDir",
            "hiding",
            "if",
            "importSkillVar",
            "include",
            "index",
            "infile",
            "functions",
            "inSkill",
            "instring",
            "isDir",
            "isExecutable",
            "isFile",
            "isFileName",
            "isReadable",
            "isWritable",
            "lambda",
            "last",
            "length",
            "let",
            "letrec",
            "letseq",
            "lineread",
            "linereadstring",
            "list",
            "listp",
            "with",
            "load",
            "loadContext",
            "loadi",
            "loadstring",
            "lowerCase",
            "lowerLeft",
            "macro",
            "make_<name>",
            "makeContext",
            "makeInstance",
            "makeTable",
            "makeTempFileName",
            "map",
            "map",
            "mapc",
            "mapcan",
            "mapcar",
            "maplist",
            "mapping",
            "max",
            "measureTime",
            "member",
            "memq",
            "min",
            "minusp",
            "mprocedure",
            "Cadence-private",
            "functions",
            "nconc",
            "ncons",
            "needNCells",
            "neq",
            "nequal",
            "function",
            "newline",
            "nindex",
            "nlambda",
            "nprocedure",
            "nth",
            "nthcdr",
            "nthelem",
            "numOpenFiles",
            "oddp",
            "onep",
            "outfile",
            "parseString",
            "functions",
            "plist",
            "plusp",
            "pp",
            "pprint",
            "comparing",
            "functions",
            "prependInstallPath",
            "print",
            "printf",
            "printlev",
            "println",
            "printstruct",
            "private",
            "procedure",
            "See",
            "prog",
            "prog1",
            "prog2",
            "putd",
            "putprop",
            "putpropq",
            "putpropqq",
            "readTable",
            "regExitAfter",
            "regExitBefore",
            "remd",
            "remdq",
            "remove",
            "remprop",
            "remq",
            "resume",
            "return",
            "reverse",
            "rexCompile",
            "rexExecute",
            "rexMagic",
            "rexMatchAssocList",
            "rexMatchList",
            "rexMatchp",
            "rexReplace",
            "rindex",
            "rplaca",
            "rplacd",
            "saveContext",
            "functionality",
            "set",
            "setContext",
            "setFnWriteProtect",
            "setof",
            "setplist",
            "setq",
            "setShellEnvVar",
            "setSkillPath",
            "setVarWriteProtect",
            "sh",
            "shell",
            "simplifyFilename",
            "SKILL",
            "conditional",
            "hiding",
            "iteration",
            "selection",
            "calling",
            "creating",
            "function",
            "functions",
            "functions",
            "iteration",
            "returning",
            "sequencing",
            "generic",
            "sharing",
            "SKILL",
            "sort",
            "sortcar",
            "using",
            "using",
            "sprintf",
            "sstatus",
            "stacktrace",
            "status",
            "strcat",
            "strcmp",
            "functions",
            "stringToFunction",
            "strlen",
            "strncat",
            "strncmp",
            "subclassp",
            "subst",
            "substring",
            "superclassesOf",
            "sxtd",
            "symbolp",
            "function",
            "symeval",
            "functions",
            "tablep",
            "tableToList",
            "tailp",
            "tconc",
            "theEnvironment",
            "toplevel",
            "tracef",
            "unless",
            "upperCase",
            "upperRight",
            "warn",
            "when",
            "while",
            "writeTable",
            "xcons",
            "xCoord",
            "yCoord",
            "zerop",
        ),
        "Keyword": ("nil",),
    }
    operator_list = [
        "=",
        "+",
        "-",
        "*",
        "/",
        "<",
        ">",
        "@",
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
        ">>",
        "<<",
        "->",
        "->?",
        "->??",
        "~>",
        "[",
        "]",
    ]
    splitter = re.compile(r"(\{\.|\.\}|\#|\'|\"\"\"|\n|\s+|\w+|\W)")
    # Characters that autoindent one level on pressing Return/Enter
    autoindent_characters = []
    # String start/end tokens
    tokens_string = ('"',)
    # Comment tokens
    tokens_comment = []

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
        return "SKILL"

    def description(self, style: int) -> str:
        if style < len(self.styles):
            description = "Custom lexer for the SKILL circuit languages"
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
            elif token[0] in self.tokens_comment:
                setStyling(token[1], self.styles["Comment"])
                commenting = True
            elif token[0] in self.tokens_string:
                # Start of a string
                setStyling(token[1], self.styles["String"])
                stringing = True
            elif token[0] in operator_list:
                setStyling(token[1], self.styles["Operator"])
            elif token[0] in keyword_dictionary["PredefinedFunctions"]:
                setStyling(token[1], self.styles["PredefinedFunctions"])
            elif token[0] in keyword_dictionary["Keyword"]:
                setStyling(token[1], self.styles["Keyword"])
            elif functions.is_number(token[0]):
                setStyling(token[1], self.styles["Number"])
            else:
                setStyling(token[1], self.styles["Default"])
