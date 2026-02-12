"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import re

import data
import settings
import functions
import lexers
import qt


class Rust(qt.QsciLexerCustom):
    """
    Custom lexer for the Rust programming language
    """

    styles = {
        "Default": 0,
        "Comment": 1,
        "Keyword": 2,
        "Type": 3,
        "String": 4,
        "Number": 5,
        "Operator": 6,
        "Attribute": 7,
        "Lifetime": 8,
        "Macro": 9,
        "CommentDoc": 10,
        "Unsafe": 11,
        "Function": 12,
    }
    # Class variables
    keyword_dictionary = {
        "Keywords": (
            "as",
            "async",
            "await",
            "break",
            "const",
            "continue",
            "crate",
            "dyn",
            "else",
            "enum",
            "extern",
            "false",
            "fn",
            "for",
            "if",
            "impl",
            "in",
            "let",
            "loop",
            "match",
            "mod",
            "move",
            "mut",
            "pub",
            "ref",
            "return",
            "self",
            "Self",
            "static",
            "struct",
            "super",
            "trait",
            "true",
            "type",
            "union",
            "unsafe",
            "use",
            "where",
            "while",
            "abstract",
            "become",
            "box",
            "do",
            "final",
            "macro",
            "override",
            "priv",
            "typeof",
            "unsized",
            "virtual",
            "yield",
        ),
        "Types": (
            "i8",
            "i16",
            "i32",
            "i64",
            "i128",
            "isize",
            "u8",
            "u16",
            "u32",
            "u64",
            "u128",
            "usize",
            "f32",
            "f64",
            "bool",
            "char",
            "str",
            "String",
            "Vec",
            "Option",
            "Result",
            "Box",
            "Rc",
            "Arc",
            "Cell",
            "RefCell",
            "Mutex",
            "RwLock",
            "HashMap",
            "HashSet",
            "BTreeMap",
            "BTreeSet",
            "VecDeque",
            "LinkedList",
            "BinaryHeap",
            "Cow",
            "PhantomData",
            "ManuallyDrop",
            "MaybeUninit",
            "Pin",
            "UnsafeCell",
            "Once",
            "Never",
            "Slice",
        ),
        "Macros": (
            "assert",
            "assert_eq",
            "assert_ne",
            "debug_assert",
            "debug_assert_eq",
            "debug_assert_ne",
            "cfg",
            "column",
            "compile_error",
            "concat",
            "concat_idents",
            "env",
            "file",
            "format",
            "format_args",
            "include",
            "include_bytes",
            "include_str",
            "line",
            "module_path",
            "option_env",
            "panic",
            "print",
            "println",
            "stringify",
            "thread_local",
            "todo",
            "unimplemented",
            "unreachable",
            "vec",
            "write",
            "writeln",
            "derive",
            "test",
            "inline",
            "repr",
            "allow",
            "warn",
            "deny",
            "forbid",
            "cfg_attr",
            "feature",
            "no_std",
            "no_mangle",
            "used",
            "link",
            "link_name",
            "macro_export",
            "macro_use",
            "path",
        ),
    }
    operator_list = [
        "=",
        "+",
        "-",
        "*",
        "/",
        "%",
        "<",
        ">",
        "!",
        "&",
        "|",
        "^",
        "~",
        ".",
        ",",
        ";",
        ":",
        "?",
        "#",
        "@",
        "$",
        "[",
        "]",
        "{",
        "}",
        "(",
        ")",
        "'",
        '"',
        "++",
        "--",
        "+=",
        "-=",
        "*=",
        "/=",
        "%=",
        "&=",
        "|=",
        "^=",
        "<<=",
        ">>=",
        "==",
        "!=",
        "<=",
        ">=",
        "&&",
        "||",
        "<<",
        ">>",
        "->",
        "=>",
        "::",
        "..",
        "...",
        "..=",
    ]
    splitter = re.compile(
        r'(r#"|"#|#!?\[|///|//!|/\*|\*/|//|\b[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b|\b0x[0-9a-fA-F]+\b|\b0o[0-7]+\b|\b0b[01]+\b|\'[a-zA-Z_][a-zA-Z0-9_]*\b|\b[a-zA-Z_][a-zA-Z0-9_]*!|\b[a-zA-Z_][a-zA-Z0-9_]*\b|\s+|\W)'
    )
    # Characters that autoindent one level on pressing Return/Enter
    autoindent_characters = ["{"]
    # String start/end tokens
    tokens_string = ('"',)
    tokens_raw_string = 'r#"'
    tokens_raw_string_end = '"#'
    # Comment tokens
    tokens_comment = ["//", "///", "//!"]
    tokens_block_comment_start = "/*"
    tokens_block_comment_end = "*/"
    # Attribute tokens
    tokens_attribute = ["#[", "#!["]

    def __init__(self, parent=None):
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

    def language(self):
        return "Rust"

    def description(self, style):
        if style < len(self.styles):
            description = "Custom lexer for the Rust programming language"
        else:
            description = ""
        return description

    def defaultStyle(self):
        return self.styles["Default"]

    def braceStyle(self):
        return self.styles["Default"]

    def defaultFont(self, style):
        return qt.QFont(
            settings.get("current_font_name"), settings.get("current_font_size")
        )

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
        text = bytearray(editor.text(), "utf-8")[start:end].decode("utf-8")
        # Loop optimizations
        setStyling = self.setStyling
        operator_list = self.operator_list
        keyword_dictionary = self.keyword_dictionary
        # Initialize various states and split the text into tokens
        stringing = False
        raw_stringing = False
        commenting = False
        doc_commenting = False
        block_commenting = False
        block_doc_commenting = False
        attributing = False
        raw_string_start_pos = 0
        tokens = [
            (token, len(bytearray(token, "utf-8")))
            for token in self.splitter.findall(text)
        ]
        # Check if there is a style stretching on from the previous line
        if start != 0:
            previous_style = editor.SendScintilla(editor.SCI_GETSTYLEAT, start - 1)
            if previous_style == self.styles["String"]:
                # Check if we're in a raw string by looking back for r#"
                prev_text = editor.text()[:start]
                if prev_text.rfind('r#"') > prev_text.rfind('"#'):
                    raw_stringing = True
                else:
                    stringing = True
            elif previous_style == self.styles["Comment"]:
                block_commenting = True
            elif previous_style == self.styles["CommentDoc"]:
                block_doc_commenting = True
        # Style the tokens accordingly
        i = 0
        while i < len(tokens):
            token = tokens[i]
            token_name = token[0]
            token_length = token[1]

            if block_commenting:
                # Continuation of block comment
                if token_name == "*/":
                    setStyling(token_length, self.styles["Comment"])
                    block_commenting = False
                else:
                    setStyling(token_length, self.styles["Comment"])
            elif block_doc_commenting:
                # Continuation of doc block comment
                if token_name == "*/":
                    setStyling(token_length, self.styles["CommentDoc"])
                    block_doc_commenting = False
                else:
                    setStyling(token_length, self.styles["CommentDoc"])
            elif stringing:
                # Continuation of a string
                setStyling(token_length, self.styles["String"])
                # Check if string ends
                if token_name == '"' and (i == 0 or tokens[i - 1][0] != "\\"):
                    stringing = False
                elif "\n" in token_name:
                    stringing = False
            elif raw_stringing:
                # Continuation of a raw string
                if token_name == '"#':
                    # Check if this is the matching end
                    setStyling(token_length, self.styles["String"])
                    raw_stringing = False
                else:
                    setStyling(token_length, self.styles["String"])
            elif commenting:
                # Continuation of line comment
                setStyling(token_length, self.styles["Comment"])
                if "\n" in token_name:
                    commenting = False
            elif doc_commenting:
                # Continuation of doc comment
                setStyling(token_length, self.styles["CommentDoc"])
                if "\n" in token_name:
                    doc_commenting = False
            elif attributing:
                # Continuation of attribute
                setStyling(token_length, self.styles["Attribute"])
                if token_name == "]":
                    attributing = False
            elif token_name == 'r#"':
                # Start of raw string
                setStyling(token_length, self.styles["String"])
                raw_stringing = True
            elif token_name == "///":
                # Start of outer doc comment
                setStyling(token_length, self.styles["CommentDoc"])
                doc_commenting = True
            elif token_name == "//!":
                # Start of inner doc comment
                setStyling(token_length, self.styles["CommentDoc"])
                doc_commenting = True
            elif token_name == "/*":
                # Start of block comment - check if it's a doc comment
                if i + 1 < len(tokens) and tokens[i + 1][0] == "*":
                    setStyling(token_length, self.styles["CommentDoc"])
                    block_doc_commenting = True
                else:
                    setStyling(token_length, self.styles["Comment"])
                    block_commenting = True
            elif token_name == "//":
                # Start of line comment
                setStyling(token_length, self.styles["Comment"])
                commenting = True
            elif token_name in self.tokens_attribute:
                # Start of attribute
                setStyling(token_length, self.styles["Attribute"])
                attributing = True
            elif token_name in self.tokens_string:
                # Start of a string
                setStyling(token_length, self.styles["String"])
                stringing = True
            elif token_name.startswith("'") and len(token_name) > 1:
                # Lifetime annotation (e.g., 'a, 'static)
                setStyling(token_length, self.styles["Lifetime"])
            elif token_name.endswith("!") and token_name[:-1].isalnum():
                # Macro invocation
                setStyling(token_length, self.styles["Macro"])
            elif token_name in operator_list:
                setStyling(token_length, self.styles["Operator"])
            elif token_name in keyword_dictionary["Keywords"]:
                if token_name == "unsafe":
                    setStyling(token_length, self.styles["Unsafe"])
                else:
                    setStyling(token_length, self.styles["Keyword"])
            elif token_name in keyword_dictionary["Types"]:
                setStyling(token_length, self.styles["Type"])
            elif token_name in keyword_dictionary["Macros"]:
                setStyling(token_length, self.styles["Macro"])
            elif token_name == "fn":
                setStyling(token_length, self.styles["Keyword"])
                # Try to highlight the function name after fn
                if i + 2 < len(tokens) and tokens[i + 2][0].isalnum():
                    setStyling(tokens[i + 1][1], self.styles["Default"])  # whitespace
                    setStyling(tokens[i + 2][1], self.styles["Function"])
                    i += 2
            elif functions.is_number(token_name):
                setStyling(token_length, self.styles["Number"])
            else:
                setStyling(token_length, self.styles["Default"])

            i += 1
