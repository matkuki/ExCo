"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import re

import data
import settings
import qt

import functions
import lexers


class SmallBasic(qt.QsciLexerCustom):
    """
    Custom lexer for the SmallBasic programming languages
    """

    styles = {
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
    keyword_remap = {
        "ConsoleFunctions": "keyword1",
        "DataFunctions": "keyword2",
        "DateFunctions": "keyword3",
        "FileFunctions": "keywordsecondary",
        "GraphicsFunctions": "keywordset3",
        "LanguageFunctions": "keyword",
        "MathFunctions": "keywordset5",
        "StringFunctions": "keywordset6",
        "SystemFunctions": "keywordset7",
    }
    # Class variables
    keyword_dictionary = {
        "ConsoleFunctions": (
            "AT",
            "BEEP",
            "CAT",
            "CLS",
            "DEFINEKEY",
            "FORM",
            "INKEY",
            "INPUT",
            "LINEINPUT",
            "LINPUT",
            "LOCATE",
            "LOGPRINT",
            "NOSOUND",
            "PEN",
            "PLAY",
            "PRINT",
            "SOUND",
            "TAB",
        ),
        "DataFunctions": (
            "APPEND",
            "ARRAY",
            "DATA",
            "DELETE",
            "DIM",
            "EMPTY",
            "ERASE",
            "INSERT",
            "ISARRAY",
            "ISDIR",
            "ISFILE",
            "ISLINK",
            "ISMAP",
            "ISNUMBER",
            "ISSTRING",
            "LBOUND",
            "LEN",
            "READ",
            "REDIM",
            "RESTORE",
            "SEARCH",
            "SORT",
            "SWAP",
            "UBOUND",
        ),
        "DateFunctions": (
            "DATE",
            "DATEDMY",
            "DATEFMT",
            "JULIAN",
            "TICKS",
            "TIME",
            "TIMEHMS",
            "TIMER",
            "TIMESTAMP",
            "WEEKDAY",
        ),
        "FileFunctions": (
            "ACCESS",
            "BGETC",
            "BLOAD",
            "BPUTC",
            "BSAVE",
            "CHDIR",
            "CHMOD",
            "CLOSE",
            "COPY",
            "DIRWALK",
            "EOF",
            "EXIST",
            "FILES",
            "FREEFILE",
            "INPUT",
            "INPUT",
            "KILL",
            "LOCK",
            "LOF",
            "MKDIR",
            "OPEN",
            "RENAME",
            "RMDIR",
            "SEEK",
            "SEEK",
            "TLOAD",
            "TSAVE",
            "WRITE",
        ),
        "GraphicsFunctions": (
            "ARC",
            "CHART",
            "CIRCLE",
            "COLOR",
            "DRAW",
            "DRAWPOLY",
            "IMAGE",
            "LINE",
            "PAINT",
            "PEN",
            "PLOT",
            "POINT",
            "PSET",
            "RECT",
            "RGB",
            "RGBF",
            "SHOWPAGE",
            "TEXTHEIGHT",
            "TEXTWIDTH",
            "TXTH",
            "TXTW",
            "VIEW",
            "WINDOW",
            "XMAX",
            "XPOS",
            "YMAX",
            "YPOS",
        ),
        "LanguageFunctions": (
            "AND",
            "AS",
            "BAND",
            "BG",
            "BOR",
            "BYREF",
            "CALL",
            "CASE",
            "CATCH",
            "CONST",
            "DECLARE",
            "DEF",
            "DO",
            "ELIF",
            "ELSE",
            "ELSEIF",
            "END",
            "END TRY",
            "ENDIF",
            "EQV",
            "EXIT",
            "FALSE",
            "FI",
            "FOR",
            "FUNC",
            "GOSUB",
            "GOTO",
            "IF",
            "IFF",
            "IMP",
            "IN",
            "LABEL",
            "LET",
            "LIKE",
            "LOCAL",
            "LSHIFT",
            "MDL",
            "MOD",
            "NAND",
            "NEXT",
            "NOR",
            "NOT",
            "ON",
            "OR",
            "REM",
            "REPEAT",
            "RETURN",
            "RSHIFT",
            "SELECT",
            "STEP",
            "STOP",
            "SUB",
            "THEN",
            "THROW",
            "TO",
            "TRUE",
            "TRY",
            "UNTIL",
            "USE",
            "USG",
            "USING",
            "WEND",
            "WHILE",
            "XNOR",
            "XOR",
        ),
        "MathFunctions": (
            "ABS",
            "ABSMAX",
            "ABSMIN",
            "ACOS",
            "ACOSH",
            "ACOT",
            "ACOTH",
            "ACSC",
            "ACSCH",
            "ASEC",
            "ASECH",
            "ASIN",
            "ASINH",
            "ATAN",
            "ATAN2",
            "ATANH",
            "ATN",
            "CEIL",
            "COS",
            "COSH",
            "COT",
            "COTH",
            "CSC",
            "CSCH",
            "DEG",
            "DERIV",
            "DETERM",
            "DIFFEQN",
            "EXP",
            "EXPRSEQ",
            "FIX",
            "FLOOR",
            "FRAC",
            "INT",
            "INTERSECT",
            "INVERSE",
            "LINEQN",
            "LOG",
            "LOG10",
            "M3APPLY",
            "M3IDENT",
            "M3ROTATE",
            "M3SCALE",
            "M3TRANS",
            "MAX",
            "MIN",
            "POLYAREA",
            "POLYCENT",
            "POLYEXT",
            "POW",
            "PTDISTLN",
            "PTDISTSEG",
            "PTSIGN",
            "RAD",
            "RND",
            "ROOT",
            "ROUND",
            "SEC",
            "SECH",
            "SEGCOS",
            "SEGLEN",
            "SEGSIN",
            "SEQ",
            "SGN",
            "SIN",
            "SINH",
            "SQR",
            "STATMEAN",
            "STATMEANDEV",
            "STATMEDIAN",
            "STATSPREADP",
            "STATSPREADS",
            "STATSTD",
            "SUM",
            "SUMSQ",
            "TAN",
            "TANH",
        ),
        "StringFunctions": (
            "ASC",
            "BCS",
            "BIN",
            "CBS",
            "CHOP",
            "CHR",
            "DISCLOSE",
            "ENCLOSE",
            "FORMAT",
            "HEX",
            "INSTR",
            "JOIN",
            "LCASE",
            "LEFT",
            "LEFTOF",
            "LEFTOFLAST",
            "LOWER",
            "LTRIM",
            "MID",
            "OCT",
            "REPLACE",
            "RIGHT",
            "RIGHTOF",
            "RIGHTOFLAST",
            "RINSTR",
            "RTRIM",
            "SINPUT",
            "SPACE",
            "SPC",
            "SPLIT",
            "SPRINT",
            "SQUEEZE",
            "STR",
            "STRING",
            "TRANSLATE",
            "TRIM",
            "UCASE",
            "UPPER",
            "VAL",
        ),
        "SystemFunctions": (
            "CHAIN",
            "COMMAND",
            "CWD",
            "DELAY",
            "ENV",
            "ENV",
            "EXEC",
            "EXPORT",
            "FRE",
            "HOME",
            "IMPORT",
            "INCLUDE",
            "MAXINT",
            "NIL",
            "OPTION",
            "PAUSE",
            "PI",
            "PROGLINE",
            "RANDOMIZE",
            "RUN",
            "SBVER",
            "SELF",
            "STKDUMP",
            "TROFF",
            "TRON",
            "UNIT",
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
        "[",
        "]",
    ]
    splitter = re.compile(r"(\{\.|\.\}|\#|\'|\"\"\"|\n|\s+|\w+|\W)")
    # Characters that autoindent one level on pressing Return/Enter
    autoindent_characters = []
    # String start/end tokens
    tokens_string = ('"',)
    # Comment tokens
    tokens_comment = ["'"]

    def __init__(self, parent=None):
        """
        Overridden initialization
        """
        # Initialize superclass
        super().__init__()
        # Set the default style values
        self.setDefaultColor(qt.QColor(settings.get_theme()["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(settings.get_theme()["fonts"]["default"]["background"]))
        self.setDefaultFont(settings.get_editor_font())
        # Reset autoindentation style
        self.setAutoIndentStyle(0)
        # Set the theme
        self.set_theme(settings.get_theme())

    def language(self):
        return "SmallBasic"

    def description(self, style):
        if style < len(self.styles):
            description = "Custom lexer for the SmallBasic circuit languages"
        else:
            description = ""
        return description

    def defaultStyle(self):
        return self.styles["Default"]

    def braceStyle(self):
        return self.styles["Default"]

    def defaultFont(self, style):
        return qt.QFont(settings.get("current_font_name"), settings.get("current_font_size"))

    def set_theme(self, theme):
        for style in self.styles:
            # Papers
            self.setPaper(
                qt.QColor(settings.get_theme()["fonts"][style.lower()]["background"]),
                self.styles[style],
            )
            # Fonts
            lexers.set_font(self, style, theme["fonts"][style.lower()])

    def styleText(self, start, end):
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
        text = bytearray(editor.text().upper(), "utf-8")[start:end].decode("utf-8")
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
            elif token[0] in keyword_dictionary["ConsoleFunctions"]:
                setStyling(
                    token[1], self.styles[self.keyword_remap["ConsoleFunctions"]]
                )
            elif token[0] in keyword_dictionary["DataFunctions"]:
                setStyling(token[1], self.styles[self.keyword_remap["DataFunctions"]])
            elif token[0] in keyword_dictionary["DateFunctions"]:
                setStyling(token[1], self.styles[self.keyword_remap["DateFunctions"]])
            elif token[0] in keyword_dictionary["FileFunctions"]:
                setStyling(token[1], self.styles[self.keyword_remap["FileFunctions"]])
            elif token[0] in keyword_dictionary["GraphicsFunctions"]:
                setStyling(
                    token[1], self.styles[self.keyword_remap["GraphicsFunctions"]]
                )
            elif token[0] in keyword_dictionary["LanguageFunctions"]:
                setStyling(
                    token[1], self.styles[self.keyword_remap["LanguageFunctions"]]
                )
            elif token[0] in keyword_dictionary["MathFunctions"]:
                setStyling(token[1], self.styles[self.keyword_remap["MathFunctions"]])
            elif token[0] in keyword_dictionary["StringFunctions"]:
                setStyling(token[1], self.styles[self.keyword_remap["StringFunctions"]])
            elif token[0] in keyword_dictionary["SystemFunctions"]:
                setStyling(token[1], self.styles[self.keyword_remap["SystemFunctions"]])
            elif functions.is_number(token[0]):
                setStyling(token[1], self.styles["Number"])
            else:
                setStyling(token[1], self.styles["Default"])
