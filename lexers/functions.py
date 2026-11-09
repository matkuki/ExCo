"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

##  FILE DESCRIPTION:
##      Functions used by lexers

from __future__ import annotations

from typing import Any

import builtins
import keyword
import re
import time

import data
import functions
import lexers
import qt
import settings


def set_font(lexer: Any, style_name: str, style_options: dict[str, Any]) -> None:
    style_index = lexer.styles[style_name]
    lexer.setColor(qt.QColor(style_options["color"]), style_index)
    weight = qt.QFont.Weight.Normal
    if style_options["bold"]:
        weight = qt.QFont.Weight.Bold
    lexer.setFont(
        qt.QFont(
            settings.get("current_editor_font_name"),
            settings.get("current_editor_font_size"),
            weight=weight,
        ),
        style_index,
    )


_FILE_TYPE_LEXER_MAP: dict[str, Any] | None = None
_COMMENT_STYLE_MAP: dict[type, tuple[bool, str | None, str | None]] | None = None


def _ensure_maps() -> None:
    global _FILE_TYPE_LEXER_MAP, _COMMENT_STYLE_MAP
    if _FILE_TYPE_LEXER_MAP is not None:
        return
    _FILE_TYPE_LEXER_MAP = {
        "python": lambda: (
            lexers.CustomPython() if lexers.nim_lexers_found else lexers.Python()
        ),
        "cython": lambda: lexers.Cython(),
        "c": lambda: lexers.CPP(),
        "c++": lambda: lexers.CPP(),
        "cmake": lambda: lexers.CMake(),
        "pascal": lambda: lexers.Pascal(),
        "oberon/modula": lambda: lexers.Oberon(),
        "ada": lambda: lexers.Ada(),
        "d": lambda: lexers.D(),
        "nim": lambda: lexers.Nim(),
        "makefile": lambda: lexers.Makefile(),
        "xml": lambda: lexers.XML(),
        "batch": lambda: lexers.Batch(),
        "bash": lambda: lexers.Bash(),
        "lua": lambda: lexers.Lua(),
        "markdown": lambda: lexers.Markdown(),
        "c#": lambda: lexers.CPP(),
        "java": lambda: lexers.Java(),
        "javascript": lambda: lexers.JavaScript(),
        "octave": lambda: lexers.Octave(),
        "routeros": lambda: lexers.RouterOS(),
        "sql": lambda: lexers.SQL(),
        "postscript": lambda: lexers.PostScript(),
        "php": lambda: lexers.Php(),
        "fortran": lambda: lexers.Fortran(),
        "fortran77": lambda: lexers.Fortran77(),
        "idl": lambda: lexers.IDL(),
        "ruby": lambda: lexers.Ruby(),
        "html": lambda: lexers.HTML(),
        "css": lambda: lexers.CSS(),
        "awk": lambda: lexers.AWK(),
        "cicode": lambda: lexers.CiCode(),
        "spice": lambda: lexers.Spice(),
        "skill": lambda: lexers.SKILL(),
        "smallbasic": lambda: lexers.SmallBasic(),
        "yaml": lambda: lexers.YAML(),
        "zig": lambda: lexers.Zig(),
        "rust": lambda: lexers.Rust(),
        "go": lambda: lexers.Go(),
    }
    _COMMENT_STYLE_MAP = {
        lexers.CustomPython: (False, "#", None),
        lexers.Python: (False, "#", None),
        lexers.Cython: (False, "#", None),
        lexers.AWK: (False, "#", None),
        lexers.CPP: (False, "//", None),
        lexers.CiCode: (False, "//", None),
        lexers.Pascal: (False, "//", None),
        lexers.Oberon: (True, "(*", "*)"),
        lexers.Ada: (False, "--", None),
        lexers.D: (False, "//", None),
        lexers.Nim: (False, "#", None),
        lexers.Makefile: (False, "#", None),
        lexers.XML: (False, None, None),
        lexers.Batch: (False, "::", None),
        lexers.Bash: (False, "#", None),
        lexers.Lua: (False, "--", None),
        lexers.Markdown: (False, None, None),
        lexers.Java: (False, "//", None),
        lexers.JavaScript: (False, "//", None),
        lexers.Octave: (False, "#", None),
        lexers.RouterOS: (False, "#", None),
        lexers.SQL: (False, "#", None),
        lexers.Spice: (False, "*", None),
        lexers.SKILL: (False, ";", None),
        lexers.SmallBasic: (False, "'", None),
        lexers.PostScript: (False, "%", None),
        lexers.Fortran: (False, "c ", None),
        lexers.Fortran77: (False, "c ", None),
        lexers.IDL: (False, "//", None),
        lexers.Ruby: (False, "#", None),
        lexers.HTML: (True, "<!--", "-->"),
        lexers.CSS: (True, "/*", "*/"),
        lexers.Zig: (False, "//", None),
        lexers.Rust: (False, "//", None),
        lexers.Go: (False, "//", None),
    }


def get_lexer_from_file_type(file_type: str) -> tuple[str, Any]:
    _ensure_maps()
    assert _FILE_TYPE_LEXER_MAP is not None
    current_file_type = file_type
    factory = _FILE_TYPE_LEXER_MAP.get(file_type)
    if factory is not None:
        lexer = factory()
    else:
        current_file_type = "TEXT"
        lexer = lexers.Text()
    return (current_file_type, lexer)


def get_comment_style_for_lexer(
    lexer: Any,
) -> tuple[bool, str | None, str | None]:
    _ensure_maps()
    assert _COMMENT_STYLE_MAP is not None
    return _COMMENT_STYLE_MAP.get(type(lexer), (False, None, None))
