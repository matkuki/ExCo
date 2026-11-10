"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

##  FILE DESCRIPTION:
##      Grapheme-cluster segmentation and display width for the terminal.
##
##      pyte stores one codepoint per cell and takes wcwidth() per codepoint.
##      That is right for plain text and even for composable combining marks
##      (pyte NFC-folds those into the previous cell), but a zero-width
##      codepoint it cannot combine - VS16, ZWJ, a keycap, a tag character -
##      hits pyte's "unprintable" branch and *breaks out of the whole draw()
##      call*, so every remaining character of that chunk silently disappears.
##      Emoji modifiers and regional indicators each take their own cell
##      instead, which doubles the width of a flag or a skin-toned emoji.
##
##      This module is the shared, Qt-free answer: split a chunk into extended
##      grapheme clusters, and give one cell width per cluster. The screen
##      stores a cluster in one cell (plus pyte's two-cell stub when wide), the
##      renderer draws it as one glyph, and reflow counts it as one unit.
##
##      No pyte or Qt imports, so reflow.py can share it without pulling in a
##      QApplication (the reflow suite runs standalone).

import unicodedata
from typing import Generator

from wcwidth import wcwidth

ZWJ: str = "\u200d"
VS16: str = "\ufe0f"


def is_combining(char: str) -> bool:
    """True for a codepoint that attaches to the preceding one.

    ``Mc`` (spacing combining marks - the vowel signs of Devanagari, Bengali,
    Tamil, Khmer and most other Indic scripts) belongs here too: UAX #29 makes
    it extend the cluster, and wcwidth() gives it no width. Left out, pyte met
    a zero-width codepoint it could not fold into the previous cell and
    dropped it, so "\u0939\u093f\u0928\u094d\u0926\u0940" lost both of its vowel signs.
    """
    return unicodedata.combining(char) != 0 or unicodedata.category(char) in (
        "Mn",
        "Mc",
        "Me",
    )


def is_variation_selector(char: str) -> bool:
    return 0xFE00 <= ord(char) <= 0xFE0F or 0xE0100 <= ord(char) <= 0xE01EF


def is_emoji_modifier(char: str) -> bool:
    return 0x1F3FB <= ord(char) <= 0x1F3FF


def is_regional_indicator(char: str) -> bool:
    return 0x1F1E6 <= ord(char) <= 0x1F1FF


def is_tag_character(char: str) -> bool:
    return 0xE0020 <= ord(char) <= 0xE007F


def is_keycap(char: str) -> bool:
    return ord(char) == 0x20E3


def hangul_class(char: str) -> str:
    """Hangul_Syllable_Type of *char*: ``L``, ``V``, ``T`` (conjoining jamo),
    ``LV`` / ``LVT`` (a precomposed syllable) or ``""`` for anything else."""
    code: int = ord(char)
    if 0x1100 <= code <= 0x115F or 0xA960 <= code <= 0xA97C:
        return "L"
    if 0x1160 <= code <= 0x11A7 or 0xD7B0 <= code <= 0xD7C6:
        return "V"
    if 0x11A8 <= code <= 0x11FF or 0xD7CB <= code <= 0xD7FB:
        return "T"
    if 0xAC00 <= code <= 0xD7A3:
        return "LV" if (code - 0xAC00) % 28 == 0 else "LVT"
    return ""


def is_hangul_jamo(char: str) -> bool:
    return hangul_class(char) in ("L", "V", "T")


def hangul_joins(previous: str, char: str) -> bool:
    """UAX #29 GB6-GB8: whether *char* continues a Hangul syllable that ends in
    *previous*. Joining any jamo to any jamo (the old rule) fused a syllable's
    final consonant with the next syllable's initial one, so a decomposed
    "\u1112\u1161\u11ab\u1100\u1173\u11af" became one cluster of two syllables."""
    before: str = hangul_class(previous)
    after: str = hangul_class(char)
    if before == "L":
        return after in ("L", "V", "LV", "LVT")
    if before in ("LV", "V"):
        return after in ("V", "T")
    if before in ("LVT", "T"):
        return after == "T"
    return False


def iter_clusters(data: str) -> Generator[str, None, None]:
    """Yield extended grapheme clusters (the UAX #29 subset a terminal sees).

    Covered: combining marks, VS15/VS16 and the supplementary variation
    selectors, ZWJ sequences, emoji modifiers, regional-indicator flags,
    keycaps, tag sequences and Hangul jamo. A lone control character is its
    own cluster, so the caller's own draw path still decides what to do with
    it.
    """
    cluster: str = ""
    join_next: bool = False
    for char in data:
        if not cluster:
            cluster = char
            join_next = char == ZWJ
            continue
        attach: bool = (
            join_next
            or char == ZWJ
            or is_combining(char)
            or is_variation_selector(char)
            or is_emoji_modifier(char)
            or is_tag_character(char)
            or is_keycap(char)
            or (
                is_regional_indicator(char)
                and len(cluster) == 1
                and is_regional_indicator(cluster)
            )
            or hangul_joins(cluster[-1], char)
        )
        if attach:
            cluster += char
            join_next = char == ZWJ
        else:
            yield cluster
            cluster = char
            join_next = char == ZWJ
    if cluster:
        yield cluster


def cluster_width(cluster: str) -> int:
    """Cell width of one grapheme cluster.

    A cluster that asks for emoji presentation (VS16, ZWJ, keycap, tag
    sequence) or is a regional-indicator pair is two cells wide even when its
    base codepoint's own wcwidth() is 1 - that is what makes an emoji fit the
    same two cells as the CJK glyphs next to it. Everything else keeps the
    width of its base codepoint, so combining marks add nothing. A negative
    result means "unprintable", exactly as wcwidth() reports it.
    """
    if not cluster:
        return 0
    first: int = wcwidth(cluster[0])
    if first < 0:
        return first
    if len(cluster) == 1:
        return first
    if any(is_regional_indicator(char) for char in cluster):
        return 2
    if any(
        char == ZWJ or char == VS16 or is_keycap(char) or is_tag_character(char)
        for char in cluster
    ):
        return 2
    return first
