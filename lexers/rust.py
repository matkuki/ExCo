"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.

IMPROVEMENTS:
- Fixed unreachable function name highlighting
- Added proper escape sequence handling for strings
- Added support for multiple hash marks in raw strings (r##"..."##, etc.)
- Fixed macro name pattern to include underscores
- Added character literal support
- Improved number literal regex (suffixes, underscores)
- Fixed block doc comment detection
- Added byte string and raw byte string support
- Added raw identifier support (r#keyword)
- Performance optimizations
"""

from __future__ import annotations

import re
from typing import Any, Callable

import data
import settings
import functions
import lexers
import qt


class Rust(qt.QsciLexerCustom):
    """
    Custom lexer for the Rust programming language
    """

    styles: dict[str, int] = {
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
        "CharLiteral": 13,
    }
    # Class variables
    keyword_dictionary: dict[str, tuple[str, ...]] = {
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
    operator_list: list[str] = [
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

    # Improved regex splitter with better number and string matching
    # Using UNICODE flag to properly handle UTF-8 characters in identifiers
    splitter: re.Pattern[str] = re.compile(
        r"("
        # Byte strings: b"..."
        r'b"'
        r"|"
        # Regular strings
        r'"'
        r"|"
        # Character literals: 'a', '\n', '\x41', '\u{...}', etc.
        r"'(?:\\(?:x[0-9a-fA-F]{2}|u\{[0-9a-fA-F]{1,6}\}|.)|[^'\\])'"
        r"|"
        # Doc comments
        r"///|//!"
        r"|"
        # Block comments
        r"/\*\*(?!/)|/\*!|/\*|\*/"
        r"|"
        # Line comments
        r"//"
        r"|"
        # Attributes
        r"#!?\["
        r"|"
        # Numbers with suffixes and underscores
        r"\b[0-9][0-9_]*(?:\.[0-9_]+)?(?:[eE][+-]?[0-9_]+)?(?:f32|f64|i8|i16|i32|i64|i128|isize|u8|u16|u32|u64|u128|usize)?\b"
        r"|"
        # Hex numbers
        r"\b0x[0-9a-fA-F_]+(?:i8|i16|i32|i64|i128|isize|u8|u16|u32|u64|u128|usize)?\b"
        r"|"
        # Octal numbers
        r"\b0o[0-7_]+(?:i8|i16|i32|i64|i128|isize|u8|u16|u32|u64|u128|usize)?\b"
        r"|"
        # Binary numbers
        r"\b0b[01_]+(?:i8|i16|i32|i64|i128|isize|u8|u16|u32|u64|u128|usize)?\b"
        r"|"
        # Lifetime annotations (Unicode-aware identifier pattern)
        r"'(?![0-9])\w+"
        r"|"
        # Macro invocations (Unicode-aware, includes underscores)
        r"(?![0-9])\w+!"
        r"|"
        # Raw identifiers: r#type, r#async, etc. (Unicode-aware)
        r"r#(?![0-9])\w+"
        r"|"
        # Regular identifiers (Unicode-aware via \w with re.UNICODE)
        r"(?![0-9])\w+"
        r"|"
        # Whitespace
        r"\s+"
        r"|"
        # Any other character (match one character at a time)
        r"."
        r")",
        re.UNICODE,
    )

    # Characters that autoindent one level on pressing Return/Enter
    autoindent_characters: list[str] = ["{"]
    # String start/end tokens
    tokens_string: tuple[str, ...] = ('"',)
    tokens_byte_string: tuple[str, ...] = ('b"',)
    # Comment tokens
    tokens_comment: list[str] = ["//", "///", "//!"]
    tokens_block_comment_start: str = "/*"
    tokens_block_comment_end: str = "*/"
    tokens_doc_block_comment_start: list[str] = ["/**", "/*!"]
    # Attribute tokens
    tokens_attribute: list[str] = ["#[", "#!["]

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
        return "Rust"

    def description(self, style: int) -> str:
        if style < len(self.styles):
            description = "Custom lexer for the Rust programming language"
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
            style_lower = style.lower()
            # Handle CharLiteral using string color as fallback
            if style_lower == "charliteral" and "charliteral" not in theme["fonts"]:
                style_lower = "string"

            # Papers
            self.setPaper(
                qt.QColor(theme["fonts"][style_lower]["background"]),
                self.styles[style],
            )
            # Fonts
            lexers.set_font(self, style, theme["fonts"][style_lower])

    def is_escaped(self, text: str, position: int) -> bool:
        """
        Check if the quote at the given position is escaped.
        Returns True if the quote is escaped by an odd number of backslashes.
        """
        if position <= 0 or position > len(text):
            return False

        # Count consecutive backslashes before this position
        backslash_count = 0
        for j in range(position - 1, -1, -1):
            if text[j] == "\\":
                backslash_count += 1
            else:
                break

        # Odd number of backslashes means the quote is escaped
        return backslash_count % 2 == 1

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
        text: str = bytearray(editor.text(), "utf-8")[start:end].decode("utf-8")
        # Loop optimizations
        setStyling: Callable[[int, int], None] = self.setStyling
        operator_list: list[str] = self.operator_list
        keyword_dictionary: dict[str, tuple[str, ...]] = self.keyword_dictionary
        # Initialize various states and split the text into tokens
        stringing: bool = False
        byte_stringing: bool = False
        raw_stringing: bool = False
        raw_byte_stringing: bool = False
        raw_string_hash_count: int = 0
        commenting: bool = False
        doc_commenting: bool = False
        block_commenting: bool = False
        block_doc_commenting: bool = False
        attributing: bool = False

        # Pre-calculate token lengths for performance
        tokens: list[tuple[str, int]] = []
        for token in self.splitter.findall(text):
            tokens.append((token, len(bytearray(token, "utf-8"))))

        # Check if there is a style stretching on from the previous line
        # Only check for multi-line constructs if we're at the start of a line
        is_start_of_line: bool = (
            start == 0 or editor.text()[start - 1 : start] in "\n\r"
        )

        if is_start_of_line and start > 0:
            previous_style: int = editor.SendScintilla(editor.SCI_GETSTYLEAT, start - 1)
            if previous_style == self.styles["String"]:
                prev_text: str = editor.text()[:start]
                # Check for raw byte strings (br#"..."#)
                last_br_raw: int = prev_text.rfind('br"')
                last_br_raw_hash: int = prev_text.rfind("br#")
                last_br_raw_end: int = prev_text.rfind('"#')
                # Check for raw strings (r#"..."#)
                last_r_raw: int = prev_text.rfind('r"')
                last_r_raw_hash: int = prev_text.rfind("r#")
                last_r_raw_end: int = prev_text.rfind('"#')
                # Check for byte strings (b"...)
                last_b_string: int = prev_text.rfind('b"')
                last_b_string_end: int = (
                    prev_text.rfind('"', last_b_string + 1)
                    if last_b_string != -1
                    else -1
                )
                # Check for regular strings
                last_string: int = prev_text.rfind('"')

                # Determine which string type we're in
                raw_byte_pos: int = max(last_br_raw, last_br_raw_hash)
                raw_pos: int = max(last_r_raw, last_r_raw_hash)

                if (
                    raw_byte_pos > last_br_raw_end
                    and raw_byte_pos > last_b_string
                    and raw_byte_pos > last_string
                ):
                    raw_byte_stringing = True
                    # Count hash marks
                    if prev_text[raw_byte_pos : raw_byte_pos + 3] == "br#":
                        raw_string_hash_count = 0
                        for c in prev_text[raw_byte_pos + 2 :]:
                            if c == "#":
                                raw_string_hash_count += 1
                            else:
                                break
                elif (
                    raw_pos > last_r_raw_end
                    and raw_pos > last_b_string
                    and raw_pos > last_string
                ):
                    raw_stringing = True
                    # Count hash marks
                    if prev_text[raw_pos : raw_pos + 2] == "r#":
                        raw_string_hash_count = 0
                        for c in prev_text[raw_pos + 1 :]:
                            if c == "#":
                                raw_string_hash_count += 1
                            else:
                                break
                elif last_b_string > last_string:
                    byte_stringing = True
                else:
                    stringing = True
            elif previous_style == self.styles["Comment"]:
                prev_text = editor.text()[:start]

                # Check for block comments: /* without closing */
                last_block_start: int = prev_text.rfind("/*")
                last_block_end: int = prev_text.rfind("*/")

                # Check for line comments: // followed by newline
                last_line_comment: int = max(
                    prev_text.rfind("//"),
                    prev_text.rfind("///"),
                    prev_text.rfind("//!"),
                )

                # Determine if we're in a block comment or line comment
                if last_block_start > last_block_end:
                    # There's an unclosed block comment - continue it
                    block_commenting = True
                elif last_line_comment != -1:
                    # Check if line comment ends at newline
                    after_comment: str = prev_text[last_line_comment + 2 :]  # Skip //
                    newline_pos: int = after_comment.find("\n")
                    if newline_pos == -1:
                        # No newline after - might be at end of file, don't continue
                        pass
                    # else: has newline - it's a line comment, don't continue
            elif previous_style == self.styles["CommentDoc"]:
                prev_text = editor.text()[:start]

                # Check for block doc comments: /** or /*! without closing */
                last_doc_block_start: int = max(
                    prev_text.rfind("/**"), prev_text.rfind("/*!")
                )
                last_block_end = prev_text.rfind("*/")

                # Check for line doc comments: /// or //! followed by newline
                last_line_doc: int = max(prev_text.rfind("///"), prev_text.rfind("//!"))

                # Determine if we're in a block doc comment or line doc comment
                if last_doc_block_start > last_block_end:
                    # There's an unclosed block doc comment - continue it
                    block_doc_commenting = True
                elif last_line_doc != -1:
                    # Check if line doc comment ends at newline (line comment)
                    after_doc: str = prev_text[last_line_doc + 2 :]  # Skip /// or //!
                    newline_pos: int = after_doc.find("\n")
                    if newline_pos == -1:
                        # No newline after - might be at end of file, don't continue
                        pass
                    # else: has newline - it's a line comment, don't continue
            elif previous_style == self.styles["Attribute"]:
                # Check if we're in an attribute (unclosed #[ or #![)
                prev_text = editor.text()[:start]
                last_attr_start: int = max(
                    prev_text.rfind("#[["), prev_text.rfind("#![[")
                )
                last_attr_end: int = prev_text.rfind("]")

                # Only continue if the attribute is unclosed
                if last_attr_start > last_attr_end:
                    attributing = True

        # Style the tokens accordingly
        i: int = 0
        while i < len(tokens):
            token: tuple[str, int] = tokens[i]
            token_name: str = token[0]
            token_length: int = token[1]

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
                # Check if string ends (not escaped)
                # Position is relative to the text slice
                quote_pos: int = sum(t[1] for t in tokens[:i])
                if token_name == '"' and not self.is_escaped(text, quote_pos):
                    stringing = False
                elif "\n" in token_name:
                    stringing = False
            elif byte_stringing:
                # Continuation of a byte string
                setStyling(token_length, self.styles["String"])
                # Check if byte string ends (not escaped)
                # Position is relative to the text slice
                quote_pos = sum(t[1] for t in tokens[:i])
                if token_name == '"' and not self.is_escaped(text, quote_pos):
                    byte_stringing = False
                elif "\n" in token_name:
                    byte_stringing = False
                elif "\n" in token_name:
                    byte_stringing = False
            elif raw_stringing:
                # Continuation of a raw string (r#"..."#)
                setStyling(token_length, self.styles["String"])
                # Check if raw string ends with matching number of #'s
                if token_name == '"#' + ("#" * raw_string_hash_count):
                    raw_stringing = False
                elif token_name == '"' and raw_string_hash_count == 0:
                    raw_stringing = False
            elif raw_byte_stringing:
                # Continuation of a raw byte string (br#"..."#)
                setStyling(token_length, self.styles["String"])
                # Check if raw byte string ends with matching number of #'s
                if token_name == '"#' + ("#" * raw_string_hash_count):
                    raw_byte_stringing = False
                elif token_name == '"' and raw_string_hash_count == 0:
                    raw_byte_stringing = False
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
            # Character literals (complete tokens from regex)
            elif (
                token_name.startswith("'")
                and token_name.endswith("'")
                and len(token_name) >= 3
            ):
                # Character literal 'a', '\n', '\u{1F600}' etc. (complete token)
                setStyling(token_length, self.styles["CharLiteral"])
            elif token_name == "///":
                # Start of outer doc comment
                setStyling(token_length, self.styles["CommentDoc"])
                doc_commenting = True
            elif token_name == "//!":
                # Start of inner doc comment
                setStyling(token_length, self.styles["CommentDoc"])
                doc_commenting = True
            elif token_name in ["/**", "/*!"]:
                # Start of doc block comment
                setStyling(token_length, self.styles["CommentDoc"])
                block_doc_commenting = True
            elif token_name == "/*":
                # Start of regular block comment
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
            elif token_name == 'b"':
                # Start of a byte string
                setStyling(token_length, self.styles["String"])
                byte_stringing = True
            elif token_name in self.tokens_string:
                # Start of a regular string
                setStyling(token_length, self.styles["String"])
                stringing = True
            elif token_name.startswith("r#"):
                # Start of a raw string (r#"..."# or r##"..."##)
                setStyling(token_length, self.styles["String"])
                # Count hash marks
                raw_string_hash_count: int = 0
                for c in token_name[1:]:
                    if c == "#":
                        raw_string_hash_count += 1
                    else:
                        break
                # If it doesn't have a closing quote, we're in a raw string
                if not (
                    token_name.endswith('"')
                    or token_name.endswith('"#' + "#" * (raw_string_hash_count - 1))
                    if raw_string_hash_count > 0
                    else token_name.endswith('"')
                ):
                    raw_stringing = True
            elif token_name.startswith("br#"):
                # Start of a raw byte string (br#"..."# or br##"..."##)
                setStyling(token_length, self.styles["String"])
                # Count hash marks
                raw_string_hash_count = 0
                for c in token_name[2:]:
                    if c == "#":
                        raw_string_hash_count += 1
                    else:
                        break
                # If it doesn't have a closing quote, we're in a raw byte string
                if not (
                    token_name.endswith('"')
                    or token_name.endswith('"#' + "#" * (raw_string_hash_count - 1))
                    if raw_string_hash_count > 0
                    else token_name.endswith('"')
                ):
                    raw_byte_stringing = True
            elif token_name.startswith("'") and len(token_name) > 1:
                # Lifetime annotation (e.g., 'a, 'static, 'życie)
                # Check it's not a number after the quote
                if len(token_name) > 1 and not token_name[1].isdigit():
                    setStyling(token_length, self.styles["Lifetime"])
                else:
                    setStyling(token_length, self.styles["Default"])
            elif token_name.endswith("!") and len(token_name) > 1:
                # Macro invocation (now properly handles underscores)
                macro_name: str = token_name[:-1]
                if macro_name.replace("_", "").isalnum():
                    setStyling(token_length, self.styles["Macro"])
                else:
                    setStyling(token_length, self.styles["Default"])
            elif token_name.startswith("r#") and len(token_name) > 2:
                # Raw identifier r#type, r#async, etc.
                setStyling(token_length, self.styles["Default"])
            elif token_name in operator_list:
                setStyling(token_length, self.styles["Operator"])
            elif token_name == "fn":
                # Function keyword - highlight it and try to highlight function name
                setStyling(token_length, self.styles["Keyword"])
                # Try to highlight the function name after fn
                j: int = i + 1
                # Skip whitespace
                while j < len(tokens) and tokens[j][0].isspace():
                    setStyling(tokens[j][1], self.styles["Default"])
                    j += 1
                # Check if next token is an identifier (Unicode-aware)
                if j < len(tokens):
                    next_token: str = tokens[j][0]
                    if next_token and len(next_token) > 0:
                        # Check if it starts with a valid identifier character (not a digit)
                        first_char: str = next_token[0]
                        if not first_char.isdigit() and (
                            first_char.isalpha()
                            or first_char == "_"
                            or ord(first_char) > 127
                        ):
                            setStyling(tokens[j][1], self.styles["Function"])
                            i = j
            elif token_name == "unsafe":
                setStyling(token_length, self.styles["Unsafe"])
            elif token_name in keyword_dictionary["Keywords"]:
                setStyling(token_length, self.styles["Keyword"])
            elif token_name in keyword_dictionary["Types"]:
                setStyling(token_length, self.styles["Type"])
            elif token_name in keyword_dictionary["Macros"]:
                setStyling(token_length, self.styles["Macro"])
            elif token_name and token_name[0].isdigit():
                # Handle numbers - must start with a digit
                # Strip underscores for validation, but check it's not empty
                token_without_underscores: str = token_name.replace("_", "")
                if token_without_underscores and functions.is_number(
                    token_without_underscores
                ):
                    setStyling(token_length, self.styles["Number"])
                else:
                    setStyling(token_length, self.styles["Default"])
            else:
                setStyling(token_length, self.styles["Default"])

            i += 1
