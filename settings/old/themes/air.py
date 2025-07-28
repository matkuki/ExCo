"""
Copyright (c) 2013-2023 Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

##  FILE DESCRIPTION:
##      Air theme (Default system form color with white backgrounds and dark text)

import data

name = "Air"
tooltip = "Air"
image_file = "tango_icons/theme-air.png"

close_image = "feather/air-grey/x.svg"
close_hover_image = "feather/air-blue/x.svg"
right_arrow_image = "feather/air-grey/chevron-right.svg"
right_arrow_hover_image = "feather/air-blue/chevron-right.svg"
right_arrow_menu_image = "feather/black/chevron-right.svg"
right_arrow_menu_disabled_image = "feather/air-grey/chevron-right.svg"
left_arrow_image = "feather/air-grey/chevron-left.svg"
left_arrow_hover_image = "feather/air-blue/chevron-left.svg"

Form = "#f0f0f0"
Context_Menu_Background = data.QColor(0xF0, 0xF0, 0xF0)
Cursor = data.QColor(0x00, 0x00, 0x00)
Cursor_Line_Background = data.QColor(0x72, 0x9F, 0xCF, 80)
Settings_Background = data.QColor(0xFFFFFFFF)
Settings_Label_Background = data.QColor(0xFFFFFFFF)
Settings_Hex_Edge = data.QColor(159, 189, 214)
Settings_Hex_Background = data.QColor(0xFF, 0xFF, 0xFF)
YesNoDialog_Edge = data.QColor(159, 189, 214)
YesNoDialog_Background = data.QColor(0xFF, 0xFF, 0xFF)

styles = {
    "case/switch": {
        "color": "#8000ff",
        "paper": "#ffffff",
        "bold": False,
        "italic": False,
    },
    "comment": {
        "color": "#007f00",
        "paper": "#ffffff",
        "bold": False,
        "italic": False,
    },
    "comment-doc": {
        "color": "#7f0a0a",
        "paper": "#ffffff",
        "bold": False,
        "italic": False,
    },
    "comment-multiline": {
        "color": "#6e3296",
        "paper": "#ffffff",
        "bold": False,
        "italic": False,
    },
    "default": {
        "color": "#000000",
        "paper": "#ffffff",
        "bold": False,
        "italic": False,
    },
    "keyword": {
        "color": "#00007f",
        "paper": "#ffffff",
        "bold": True,
        "italic": False,
    },
    "keyword-definition": {
        "color": "#007f7f",
        "paper": "#ffffff",
        "bold": True,
        "italic": False,
    },
    "keyword-top": {
        "color": "#407fc0",
        "paper": "#ffffff",
        "bold": True,
        "italic": False,
    },
    "literal-character": {
        "color": "#00c8ff",
        "paper": "#ffffff",
        "bold": False,
        "italic": False,
    },
    "name-class": {
        "color": "#0000ff",
        "paper": "#ffffff",
        "bold": False,
        "italic": False,
    },
    "number": {
        "color": "#007f7f",
        "paper": "#ffffff",
        "bold": False,
        "italic": False,
    },
    "operator": {
        "color": "#7f7f7f",
        "paper": "#ffffff",
        "bold": False,
        "italic": False,
    },
    "operator-keyword": {
        "color": "#963cc8",
        "paper": "#ffffff",
        "bold": False,
        "italic": False,
    },
    "pragma": {
        "color": "#c07f40",
        "paper": "#ffffff",
        "bold": False,
        "italic": False,
    },
    "string": {
        "color": "#7f007f",
        "paper": "#ffffff",
        "bold": False,
        "italic": False,
    },
    "string-triple-quoted": {
        "color": "#7f0000",
        "paper": "#ffffff",
        "bold": False,
        "italic": False,
    },
    "type": {
        "color": "#6e6e00",
        "paper": "#ffffff",
        "bold": True,
        "italic": False,
    },
    "unsafe": {
        "color": "#c00000",
        "paper": "#ffffff",
        "bold": False,
        "italic": False,
    },
}


class FoldMargin:
    ForeGround = data.QColor(0x000000)
    BackGround = data.QColor(0x000000)


class LineMargin:
    ForeGround = data.QColor(0x000000)
    BackGround = data.QColor(0xE0E0E0)


class ScrollBar:
    background = "#f0f0f0"
    handle = "#cdcdcd"
    handle_hover = "#a6a6a6"


class Indication:
    Font = "#000000"
    ActiveBackGround = "#ffffff"
    ActiveBorder = "#204a87"
    PassiveBackGround = "#f0f0f0"
    PassiveBorder = "#a0a0a0"
    Hover = "#d8eaf9"
    # Editor indicator colors
    Highlight = data.QColor(0, 255, 0, 80)
    Selection = data.QColor(200, 200, 200, 100)
    Replace = data.QColor(50, 180, 255, 80)
    Find = data.QColor(255, 180, 50, 100)


class TextDifferColors:
    Indicator_Unique_1_Color = data.QColor(0x72, 0x9F, 0xCF, 80)
    Indicator_Unique_2_Color = data.QColor(0xAD, 0x7F, 0xA8, 80)
    Indicator_Similar_Color = data.QColor(0x8A, 0xE2, 0x34, 80)


class Font:
    Default = data.QColor(0xFF000000)
    DefaultHtml = "#000000"

    class Repl:
        """
        THE MESSAGE COLORS ARE: 0xBBGGRR (BB-blue,GG-green,RR-red)
        """

        Error = 0x0000FF
        Warning = 0xFF0000
        Success = 0x007F00
        Diff_Unique_1 = 0xCF9F72
        Diff_Unique_2 = 0xA87FAD
        Diff_Similar = 0x069A4E

    class Ada:
        Default = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Comment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        Keyword = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        String = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        Procedure = (
            data.current_editor_font_name,
            0xFF0000FF,
            data.current_editor_font_size,
            None,
        )
        Number = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        Type = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        Package = (
            data.current_editor_font_name,
            0xFF7F0000,
            data.current_editor_font_size,
            None,
        )

    class AWK:
        Default = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Comment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        Keyword = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            True,
        )
        BuiltInVariable = (
            data.current_editor_font_name,
            0xFFC07F40,
            data.current_editor_font_size,
            None,
        )
        BuiltInFunction = (
            data.current_editor_font_name,
            0xFF407FC0,
            data.current_editor_font_size,
            True,
        )
        String = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        Number = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        Operator = (
            data.current_editor_font_name,
            0xFF7F7F7F,
            data.current_editor_font_size,
            None,
        )

    class CiCode:
        Default = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Comment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        MultilineComment = (
            data.current_editor_font_name,
            0xFF006F00,
            data.current_editor_font_size,
            None,
        )
        Keyword = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            True,
        )
        BuiltInFunction = (
            data.current_editor_font_name,
            0xFF407FC0,
            data.current_editor_font_size,
            True,
        )
        String = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        Number = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        Operator = (
            data.current_editor_font_name,
            0xFF7F7F7F,
            data.current_editor_font_size,
            None,
        )
        Function = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )

    class Nim:
        Default = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Comment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        BasicKeyword = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            True,
        )
        TopKeyword = (
            data.current_editor_font_name,
            0xFF407FC0,
            data.current_editor_font_size,
            True,
        )
        String = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        LongString = (
            data.current_editor_font_name,
            0xFF7F0000,
            data.current_editor_font_size,
            None,
        )
        Number = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        Operator = (
            data.current_editor_font_name,
            0xFF7F7F7F,
            data.current_editor_font_size,
            None,
        )
        Unsafe = (
            data.current_editor_font_name,
            0xFFC00000,
            data.current_editor_font_size,
            True,
        )
        Type = (
            data.current_editor_font_name,
            0xFF6E6E00,
            data.current_editor_font_size,
            True,
        )
        DocumentationComment = (
            data.current_editor_font_name,
            0xFF7F0A0A,
            data.current_editor_font_size,
            None,
        )
        Definition = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        Class = (
            data.current_editor_font_name,
            0xFF0000FF,
            data.current_editor_font_size,
            None,
        )
        KeywordOperator = (
            data.current_editor_font_name,
            0xFF963CC8,
            data.current_editor_font_size,
            None,
        )
        CharLiteral = (
            data.current_editor_font_name,
            0xFF00C8FF,
            data.current_editor_font_size,
            None,
        )
        CaseOf = (
            data.current_editor_font_name,
            0xFF8000FF,
            data.current_editor_font_size,
            None,
        )
        UserKeyword = (
            data.current_editor_font_name,
            0xFFFF8040,
            data.current_editor_font_size,
            None,
        )
        MultilineComment = (
            data.current_editor_font_name,
            0xFF006C6C,
            data.current_editor_font_size,
            None,
        )
        MultilineDocumentation = (
            data.current_editor_font_name,
            0xFF6E3296,
            data.current_editor_font_size,
            None,
        )
        Pragma = (
            data.current_editor_font_name,
            0xFFC07F40,
            data.current_editor_font_size,
            None,
        )

    class RouterOS:
        Default = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            True,
        )
        Operator = (
            data.current_editor_font_name,
            0xFFB4B80A,
            data.current_editor_font_size,
            True,
        )
        Comment = (
            data.current_editor_font_name,
            0xFF38B86B,
            data.current_editor_font_size,
            True,
        )
        Keyword1 = (
            data.current_editor_font_name,
            0xFF008000,
            data.current_editor_font_size,
            True,
        )
        Keyword2 = (
            data.current_editor_font_name,
            0xFFB9005C,
            data.current_editor_font_size,
            True,
        )
        Keyword3 = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            True,
        )

    class Oberon:
        Default = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Comment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        Keyword = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        String = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        Procedure = (
            data.current_editor_font_name,
            0xFF0000FF,
            data.current_editor_font_size,
            None,
        )
        Module = (
            data.current_editor_font_name,
            0xFF7F0000,
            data.current_editor_font_size,
            None,
        )
        Number = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        Type = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )

    class AVS:
        BlockComment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        ClipProperty = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        Default = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Filter = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        Function = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        Identifier = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Keyword = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        KeywordSet6 = (
            data.current_editor_font_name,
            0xFF8000FF,
            data.current_editor_font_size,
            None,
        )
        LineComment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        NestedBlockComment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        Number = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        Operator = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Plugin = (
            data.current_editor_font_name,
            0xFF0080C0,
            data.current_editor_font_size,
            None,
        )
        String = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        TripleString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )

    class Bash:
        Backticks = (
            data.current_editor_font_name,
            0xFFADAD00,
            data.current_editor_font_size,
            None,
        )
        Comment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        Default = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        DoubleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            True,
        )
        Error = (
            data.current_editor_font_name,
            0xFFAA0000,
            data.current_editor_font_size,
            True,
        )
        HereDocumentDelimiter = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Identifier = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Keyword = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        Number = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        Operator = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        ParameterExpansion = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Scalar = (
            data.current_editor_font_name,
            0xFFADAD00,
            data.current_editor_font_size,
            True,
        )
        SingleQuotedHereDocument = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        SingleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )

    class Batch:
        Comment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        Default = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        ExternalCommand = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        HideCommandChar = (
            data.current_editor_font_name,
            0xFF7F7F00,
            data.current_editor_font_size,
            None,
        )
        Keyword = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        Label = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        Operator = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Variable = (
            data.current_editor_font_name,
            0xFF800080,
            data.current_editor_font_size,
            None,
        )

    class CMake:
        BlockForeach = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        BlockIf = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        BlockMacro = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        BlockWhile = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        Comment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        Default = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Function = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        KeywordSet3 = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Label = (
            data.current_editor_font_name,
            0xFFCC3300,
            data.current_editor_font_size,
            None,
        )
        Number = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        String = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        StringLeftQuote = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        StringRightQuote = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        StringVariable = (
            data.current_editor_font_name,
            0xFFCC3300,
            data.current_editor_font_size,
            None,
        )
        Variable = (
            data.current_editor_font_name,
            0xFF800000,
            data.current_editor_font_size,
            None,
        )

    class CPP:
        Comment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        CommentDoc = (
            data.current_editor_font_name,
            0xFF3F703F,
            data.current_editor_font_size,
            None,
        )
        CommentDocKeyword = (
            data.current_editor_font_name,
            0xFF3060A0,
            data.current_editor_font_size,
            None,
        )
        CommentDocKeywordError = (
            data.current_editor_font_name,
            0xFF804020,
            data.current_editor_font_size,
            None,
        )
        CommentLine = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        CommentLineDoc = (
            data.current_editor_font_name,
            0xFF3F703F,
            data.current_editor_font_size,
            None,
        )
        Default = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        DoubleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        GlobalClass = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        HashQuotedString = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        Identifier = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactiveComment = (
            data.current_editor_font_name,
            0xFF90B090,
            data.current_editor_font_size,
            None,
        )
        InactiveCommentDoc = (
            data.current_editor_font_name,
            0xFFD0D0D0,
            data.current_editor_font_size,
            None,
        )
        InactiveCommentDocKeyword = (
            data.current_editor_font_name,
            0xFFC0C0C0,
            data.current_editor_font_size,
            None,
        )
        InactiveCommentDocKeywordError = (
            data.current_editor_font_name,
            0xFFC0C0C0,
            data.current_editor_font_size,
            None,
        )
        InactiveCommentLine = (
            data.current_editor_font_name,
            0xFF90B090,
            data.current_editor_font_size,
            None,
        )
        InactiveCommentLineDoc = (
            data.current_editor_font_name,
            0xFFC0C0C0,
            data.current_editor_font_size,
            None,
        )
        InactiveDefault = (
            data.current_editor_font_name,
            0xFFC0C0C0,
            data.current_editor_font_size,
            None,
        )
        InactiveDoubleQuotedString = (
            data.current_editor_font_name,
            0xFFB090B0,
            data.current_editor_font_size,
            None,
        )
        InactiveGlobalClass = (
            data.current_editor_font_name,
            0xFFB0B0B0,
            data.current_editor_font_size,
            None,
        )
        InactiveHashQuotedString = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactiveIdentifier = (
            data.current_editor_font_name,
            0xFFB0B0B0,
            data.current_editor_font_size,
            None,
        )
        InactiveKeyword = (
            data.current_editor_font_name,
            0xFF9090B0,
            data.current_editor_font_size,
            None,
        )
        InactiveKeywordSet2 = (
            data.current_editor_font_name,
            0xFFC0C0C0,
            data.current_editor_font_size,
            None,
        )
        InactiveNumber = (
            data.current_editor_font_name,
            0xFF90B090,
            data.current_editor_font_size,
            None,
        )
        InactiveOperator = (
            data.current_editor_font_name,
            0xFFB0B0B0,
            data.current_editor_font_size,
            None,
        )
        InactivePreProcessor = (
            data.current_editor_font_name,
            0xFFB0B090,
            data.current_editor_font_size,
            None,
        )
        InactivePreProcessorComment = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactivePreProcessorCommentLineDoc = (
            data.current_editor_font_name,
            0xFFC0C0C0,
            data.current_editor_font_size,
            None,
        )
        InactiveRawString = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactiveRegex = (
            data.current_editor_font_name,
            0xFF7FAF7F,
            data.current_editor_font_size,
            None,
        )
        InactiveSingleQuotedString = (
            data.current_editor_font_name,
            0xFFB090B0,
            data.current_editor_font_size,
            None,
        )
        InactiveTripleQuotedVerbatimString = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactiveUUID = (
            data.current_editor_font_name,
            0xFFC0C0C0,
            data.current_editor_font_size,
            None,
        )
        InactiveUnclosedString = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactiveVerbatimString = (
            data.current_editor_font_name,
            0xFF90B090,
            data.current_editor_font_size,
            None,
        )
        Keyword = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        KeywordSet2 = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Number = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        Operator = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        PreProcessor = (
            data.current_editor_font_name,
            0xFF7F7F00,
            data.current_editor_font_size,
            None,
        )
        PreProcessorComment = (
            data.current_editor_font_name,
            0xFF659900,
            data.current_editor_font_size,
            None,
        )
        PreProcessorCommentLineDoc = (
            data.current_editor_font_name,
            0xFF3F703F,
            data.current_editor_font_size,
            None,
        )
        RawString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        Regex = (
            data.current_editor_font_name,
            0xFF3F7F3F,
            data.current_editor_font_size,
            None,
        )
        SingleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        TripleQuotedVerbatimString = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        UUID = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        UnclosedString = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        VerbatimString = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        UserLiteral = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactiveEscapeSequence = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        EscapeSequence = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactiveUserLiteral = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactiveTaskMarker = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        TaskMarker = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )

    class CSS:
        AtRule = (
            data.current_editor_font_name,
            0xFF7F7F00,
            data.current_editor_font_size,
            None,
        )
        Attribute = (
            data.current_editor_font_name,
            0xFF800000,
            data.current_editor_font_size,
            None,
        )
        CSS1Property = (
            data.current_editor_font_name,
            0xFF0040E0,
            data.current_editor_font_size,
            None,
        )
        CSS2Property = (
            data.current_editor_font_name,
            0xFF00A0E0,
            data.current_editor_font_size,
            None,
        )
        CSS3Property = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        ClassSelector = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Comment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        Default = (
            data.current_editor_font_name,
            0xFFFF0080,
            data.current_editor_font_size,
            None,
        )
        DoubleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        ExtendedCSSProperty = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        ExtendedPseudoClass = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        ExtendedPseudoElement = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        IDSelector = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        Important = (
            data.current_editor_font_name,
            0xFFFF8000,
            data.current_editor_font_size,
            None,
        )
        MediaRule = (
            data.current_editor_font_name,
            0xFF7F7F00,
            data.current_editor_font_size,
            None,
        )
        Operator = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        PseudoClass = (
            data.current_editor_font_name,
            0xFF800000,
            data.current_editor_font_size,
            None,
        )
        PseudoElement = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        SingleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        Tag = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        UnknownProperty = (
            data.current_editor_font_name,
            0xFFFF0000,
            data.current_editor_font_size,
            None,
        )
        UnknownPseudoClass = (
            data.current_editor_font_name,
            0xFFFF0000,
            data.current_editor_font_size,
            None,
        )
        Value = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        Variable = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )

    class CSharp:
        Comment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        CommentDoc = (
            data.current_editor_font_name,
            0xFF3F703F,
            data.current_editor_font_size,
            None,
        )
        CommentDocKeyword = (
            data.current_editor_font_name,
            0xFF3060A0,
            data.current_editor_font_size,
            None,
        )
        CommentDocKeywordError = (
            data.current_editor_font_name,
            0xFF804020,
            data.current_editor_font_size,
            None,
        )
        CommentLine = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        CommentLineDoc = (
            data.current_editor_font_name,
            0xFF3F703F,
            data.current_editor_font_size,
            None,
        )
        Default = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        DoubleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        GlobalClass = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        HashQuotedString = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        Identifier = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactiveComment = (
            data.current_editor_font_name,
            0xFF90B090,
            data.current_editor_font_size,
            None,
        )
        InactiveCommentDoc = (
            data.current_editor_font_name,
            0xFFD0D0D0,
            data.current_editor_font_size,
            None,
        )
        InactiveCommentDocKeyword = (
            data.current_editor_font_name,
            0xFFC0C0C0,
            data.current_editor_font_size,
            None,
        )
        InactiveCommentDocKeywordError = (
            data.current_editor_font_name,
            0xFFC0C0C0,
            data.current_editor_font_size,
            None,
        )
        InactiveCommentLine = (
            data.current_editor_font_name,
            0xFF90B090,
            data.current_editor_font_size,
            None,
        )
        InactiveCommentLineDoc = (
            data.current_editor_font_name,
            0xFFC0C0C0,
            data.current_editor_font_size,
            None,
        )
        InactiveDefault = (
            data.current_editor_font_name,
            0xFFC0C0C0,
            data.current_editor_font_size,
            None,
        )
        InactiveDoubleQuotedString = (
            data.current_editor_font_name,
            0xFFB090B0,
            data.current_editor_font_size,
            None,
        )
        InactiveGlobalClass = (
            data.current_editor_font_name,
            0xFFB0B0B0,
            data.current_editor_font_size,
            None,
        )
        InactiveHashQuotedString = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactiveIdentifier = (
            data.current_editor_font_name,
            0xFFB0B0B0,
            data.current_editor_font_size,
            None,
        )
        InactiveKeyword = (
            data.current_editor_font_name,
            0xFF9090B0,
            data.current_editor_font_size,
            None,
        )
        InactiveKeywordSet2 = (
            data.current_editor_font_name,
            0xFFC0C0C0,
            data.current_editor_font_size,
            None,
        )
        InactiveNumber = (
            data.current_editor_font_name,
            0xFF90B090,
            data.current_editor_font_size,
            None,
        )
        InactiveOperator = (
            data.current_editor_font_name,
            0xFFB0B0B0,
            data.current_editor_font_size,
            None,
        )
        InactivePreProcessor = (
            data.current_editor_font_name,
            0xFFB0B090,
            data.current_editor_font_size,
            None,
        )
        InactivePreProcessorComment = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactivePreProcessorCommentLineDoc = (
            data.current_editor_font_name,
            0xFFC0C0C0,
            data.current_editor_font_size,
            None,
        )
        InactiveRawString = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactiveRegex = (
            data.current_editor_font_name,
            0xFF7FAF7F,
            data.current_editor_font_size,
            None,
        )
        InactiveSingleQuotedString = (
            data.current_editor_font_name,
            0xFFB090B0,
            data.current_editor_font_size,
            None,
        )
        InactiveTripleQuotedVerbatimString = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactiveUUID = (
            data.current_editor_font_name,
            0xFFC0C0C0,
            data.current_editor_font_size,
            None,
        )
        InactiveUnclosedString = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactiveVerbatimString = (
            data.current_editor_font_name,
            0xFF90B090,
            data.current_editor_font_size,
            None,
        )
        Keyword = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        KeywordSet2 = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Number = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        Operator = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        PreProcessor = (
            data.current_editor_font_name,
            0xFF7F7F00,
            data.current_editor_font_size,
            None,
        )
        PreProcessorComment = (
            data.current_editor_font_name,
            0xFF659900,
            data.current_editor_font_size,
            None,
        )
        PreProcessorCommentLineDoc = (
            data.current_editor_font_name,
            0xFF3F703F,
            data.current_editor_font_size,
            None,
        )
        RawString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        Regex = (
            data.current_editor_font_name,
            0xFF3F7F3F,
            data.current_editor_font_size,
            None,
        )
        SingleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        TripleQuotedVerbatimString = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        UUID = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        UnclosedString = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        VerbatimString = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        UserLiteral = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactiveEscapeSequence = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        EscapeSequence = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactiveUserLiteral = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactiveTaskMarker = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        TaskMarker = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )

    class CoffeeScript:
        BlockRegex = (
            data.current_editor_font_name,
            0xFF3F7F3F,
            data.current_editor_font_size,
            None,
        )
        BlockRegexComment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        Comment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        CommentBlock = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        CommentDoc = (
            data.current_editor_font_name,
            0xFF3F703F,
            data.current_editor_font_size,
            None,
        )
        CommentDocKeyword = (
            data.current_editor_font_name,
            0xFF3060A0,
            data.current_editor_font_size,
            None,
        )
        CommentDocKeywordError = (
            data.current_editor_font_name,
            0xFF804020,
            data.current_editor_font_size,
            None,
        )
        CommentLine = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        CommentLineDoc = (
            data.current_editor_font_name,
            0xFF3F703F,
            data.current_editor_font_size,
            None,
        )
        Default = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        DoubleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        GlobalClass = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Identifier = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Keyword = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        KeywordSet2 = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Number = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        Operator = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        PreProcessor = (
            data.current_editor_font_name,
            0xFF7F7F00,
            data.current_editor_font_size,
            None,
        )
        Regex = (
            data.current_editor_font_name,
            0xFF3F7F3F,
            data.current_editor_font_size,
            None,
        )
        SingleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        UUID = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        UnclosedString = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        VerbatimString = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )

    class D:
        BackquoteString = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Character = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        Comment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        CommentDoc = (
            data.current_editor_font_name,
            0xFF3F703F,
            data.current_editor_font_size,
            None,
        )
        CommentDocKeyword = (
            data.current_editor_font_name,
            0xFF3060A0,
            data.current_editor_font_size,
            None,
        )
        CommentDocKeywordError = (
            data.current_editor_font_name,
            0xFF804020,
            data.current_editor_font_size,
            None,
        )
        CommentLine = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        CommentLineDoc = (
            data.current_editor_font_name,
            0xFF3F703F,
            data.current_editor_font_size,
            None,
        )
        CommentNested = (
            data.current_editor_font_name,
            0xFFA0C0A0,
            data.current_editor_font_size,
            None,
        )
        Default = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        Identifier = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Keyword = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        KeywordDoc = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        KeywordSecondary = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        KeywordSet5 = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        KeywordSet6 = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        KeywordSet7 = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Number = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        Operator = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        RawString = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        String = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        Typedefs = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        UnclosedString = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )

    class Diff:
        Command = (
            data.current_editor_font_name,
            0xFF7F7F00,
            data.current_editor_font_size,
            None,
        )
        Comment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        Default = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Header = (
            data.current_editor_font_name,
            0xFF7F0000,
            data.current_editor_font_size,
            None,
        )
        LineAdded = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        LineChanged = (
            data.current_editor_font_name,
            0xFF7F7F7F,
            data.current_editor_font_size,
            None,
        )
        LineRemoved = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        Position = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )

    class Fortran:
        Comment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        Continuation = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Default = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        DottedOperator = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        DoubleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        ExtendedFunction = (
            data.current_editor_font_name,
            0xFFB04080,
            data.current_editor_font_size,
            None,
        )
        Identifier = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        IntrinsicFunction = (
            data.current_editor_font_name,
            0xFFB00040,
            data.current_editor_font_size,
            None,
        )
        Keyword = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        Label = (
            data.current_editor_font_name,
            0xFFE0C0E0,
            data.current_editor_font_size,
            None,
        )
        Number = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        Operator = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        PreProcessor = (
            data.current_editor_font_name,
            0xFF7F7F00,
            data.current_editor_font_size,
            None,
        )
        SingleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        UnclosedString = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )

    class Fortran77:
        Comment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        Continuation = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Default = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        DottedOperator = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        DoubleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        ExtendedFunction = (
            data.current_editor_font_name,
            0xFFB04080,
            data.current_editor_font_size,
            None,
        )
        Identifier = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        IntrinsicFunction = (
            data.current_editor_font_name,
            0xFFB00040,
            data.current_editor_font_size,
            None,
        )
        Keyword = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        Label = (
            data.current_editor_font_name,
            0xFFE0C0E0,
            data.current_editor_font_size,
            None,
        )
        Number = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        Operator = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        PreProcessor = (
            data.current_editor_font_name,
            0xFF7F7F00,
            data.current_editor_font_size,
            None,
        )
        SingleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        UnclosedString = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )

    class HTML:
        ASPAtStart = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        ASPJavaScriptComment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        ASPJavaScriptCommentDoc = (
            data.current_editor_font_name,
            0xFF7F7F7F,
            data.current_editor_font_size,
            None,
        )
        ASPJavaScriptCommentLine = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        ASPJavaScriptDefault = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        ASPJavaScriptDoubleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        ASPJavaScriptKeyword = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        ASPJavaScriptNumber = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        ASPJavaScriptRegex = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        ASPJavaScriptSingleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        ASPJavaScriptStart = (
            data.current_editor_font_name,
            0xFF7F7F00,
            data.current_editor_font_size,
            None,
        )
        ASPJavaScriptSymbol = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        ASPJavaScriptUnclosedString = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        ASPJavaScriptWord = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        ASPPythonClassName = (
            data.current_editor_font_name,
            0xFF0000FF,
            data.current_editor_font_size,
            None,
        )
        ASPPythonComment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        ASPPythonDefault = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        ASPPythonDoubleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        ASPPythonFunctionMethodName = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        ASPPythonIdentifier = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        ASPPythonKeyword = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        ASPPythonNumber = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        ASPPythonOperator = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        ASPPythonSingleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        ASPPythonStart = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        ASPPythonTripleDoubleQuotedString = (
            data.current_editor_font_name,
            0xFF7F0000,
            data.current_editor_font_size,
            None,
        )
        ASPPythonTripleSingleQuotedString = (
            data.current_editor_font_name,
            0xFF7F0000,
            data.current_editor_font_size,
            None,
        )
        ASPStart = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        ASPVBScriptComment = (
            data.current_editor_font_name,
            0xFF008000,
            data.current_editor_font_size,
            None,
        )
        ASPVBScriptDefault = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        ASPVBScriptIdentifier = (
            data.current_editor_font_name,
            0xFF000080,
            data.current_editor_font_size,
            None,
        )
        ASPVBScriptKeyword = (
            data.current_editor_font_name,
            0xFF000080,
            data.current_editor_font_size,
            None,
        )
        ASPVBScriptNumber = (
            data.current_editor_font_name,
            0xFF008080,
            data.current_editor_font_size,
            None,
        )
        ASPVBScriptStart = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        ASPVBScriptString = (
            data.current_editor_font_name,
            0xFF800080,
            data.current_editor_font_size,
            None,
        )
        ASPVBScriptUnclosedString = (
            data.current_editor_font_name,
            0xFF000080,
            data.current_editor_font_size,
            None,
        )
        ASPXCComment = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Attribute = (
            data.current_editor_font_name,
            0xFF008080,
            data.current_editor_font_size,
            None,
        )
        CDATA = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Default = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Entity = (
            data.current_editor_font_name,
            0xFF800080,
            data.current_editor_font_size,
            None,
        )
        HTMLComment = (
            data.current_editor_font_name,
            0xFF808000,
            data.current_editor_font_size,
            None,
        )
        HTMLDoubleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        HTMLNumber = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        HTMLSingleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        HTMLValue = (
            data.current_editor_font_name,
            0xFFFF00FF,
            data.current_editor_font_size,
            None,
        )
        JavaScriptComment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        JavaScriptCommentDoc = (
            data.current_editor_font_name,
            0xFF3F703F,
            data.current_editor_font_size,
            None,
        )
        JavaScriptCommentLine = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        JavaScriptDefault = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        JavaScriptDoubleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        JavaScriptKeyword = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        JavaScriptNumber = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        JavaScriptRegex = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        JavaScriptSingleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        JavaScriptStart = (
            data.current_editor_font_name,
            0xFF7F7F00,
            data.current_editor_font_size,
            None,
        )
        JavaScriptSymbol = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        JavaScriptUnclosedString = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        JavaScriptWord = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        OtherInTag = (
            data.current_editor_font_name,
            0xFF800080,
            data.current_editor_font_size,
            None,
        )
        PHPComment = (
            data.current_editor_font_name,
            0xFF999999,
            data.current_editor_font_size,
            None,
        )
        PHPCommentLine = (
            data.current_editor_font_name,
            0xFF666666,
            data.current_editor_font_size,
            None,
        )
        PHPDefault = (
            data.current_editor_font_name,
            0xFF000033,
            data.current_editor_font_size,
            None,
        )
        PHPDoubleQuotedString = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        PHPDoubleQuotedVariable = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        PHPKeyword = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        PHPNumber = (
            data.current_editor_font_name,
            0xFFCC9900,
            data.current_editor_font_size,
            None,
        )
        PHPOperator = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        PHPSingleQuotedString = (
            data.current_editor_font_name,
            0xFF009F00,
            data.current_editor_font_size,
            None,
        )
        PHPStart = (
            data.current_editor_font_name,
            0xFF0000FF,
            data.current_editor_font_size,
            None,
        )
        PHPVariable = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        PythonClassName = (
            data.current_editor_font_name,
            0xFF0000FF,
            data.current_editor_font_size,
            None,
        )
        PythonComment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        PythonDefault = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        PythonDoubleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        PythonFunctionMethodName = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        PythonIdentifier = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        PythonKeyword = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        PythonNumber = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        PythonOperator = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        PythonSingleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        PythonStart = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        PythonTripleDoubleQuotedString = (
            data.current_editor_font_name,
            0xFF7F0000,
            data.current_editor_font_size,
            None,
        )
        PythonTripleSingleQuotedString = (
            data.current_editor_font_name,
            0xFF7F0000,
            data.current_editor_font_size,
            None,
        )
        SGMLBlockDefault = (
            data.current_editor_font_name,
            0xFF000066,
            data.current_editor_font_size,
            None,
        )
        SGMLCommand = (
            data.current_editor_font_name,
            0xFF000080,
            data.current_editor_font_size,
            None,
        )
        SGMLComment = (
            data.current_editor_font_name,
            0xFF808000,
            data.current_editor_font_size,
            None,
        )
        SGMLDefault = (
            data.current_editor_font_name,
            0xFF000080,
            data.current_editor_font_size,
            None,
        )
        SGMLDoubleQuotedString = (
            data.current_editor_font_name,
            0xFF800000,
            data.current_editor_font_size,
            None,
        )
        SGMLEntity = (
            data.current_editor_font_name,
            0xFF333333,
            data.current_editor_font_size,
            None,
        )
        SGMLError = (
            data.current_editor_font_name,
            0xFF800000,
            data.current_editor_font_size,
            None,
        )
        SGMLParameter = (
            data.current_editor_font_name,
            0xFF006600,
            data.current_editor_font_size,
            None,
        )
        SGMLParameterComment = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        SGMLSingleQuotedString = (
            data.current_editor_font_name,
            0xFF993300,
            data.current_editor_font_size,
            None,
        )
        SGMLSpecial = (
            data.current_editor_font_name,
            0xFF3366FF,
            data.current_editor_font_size,
            None,
        )
        Script = (
            data.current_editor_font_name,
            0xFF000080,
            data.current_editor_font_size,
            None,
        )
        Tag = (
            data.current_editor_font_name,
            0xFF000080,
            data.current_editor_font_size,
            None,
        )
        UnknownAttribute = (
            data.current_editor_font_name,
            0xFFFF0000,
            data.current_editor_font_size,
            None,
        )
        UnknownTag = (
            data.current_editor_font_name,
            0xFFFF0000,
            data.current_editor_font_size,
            None,
        )
        VBScriptComment = (
            data.current_editor_font_name,
            0xFF008000,
            data.current_editor_font_size,
            None,
        )
        VBScriptDefault = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        VBScriptIdentifier = (
            data.current_editor_font_name,
            0xFF000080,
            data.current_editor_font_size,
            None,
        )
        VBScriptKeyword = (
            data.current_editor_font_name,
            0xFF000080,
            data.current_editor_font_size,
            None,
        )
        VBScriptNumber = (
            data.current_editor_font_name,
            0xFF008080,
            data.current_editor_font_size,
            None,
        )
        VBScriptStart = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        VBScriptString = (
            data.current_editor_font_name,
            0xFF800080,
            data.current_editor_font_size,
            None,
        )
        VBScriptUnclosedString = (
            data.current_editor_font_name,
            0xFF000080,
            data.current_editor_font_size,
            None,
        )
        XMLEnd = (
            data.current_editor_font_name,
            0xFF0000FF,
            data.current_editor_font_size,
            None,
        )
        XMLStart = (
            data.current_editor_font_name,
            0xFF0000FF,
            data.current_editor_font_size,
            None,
        )
        XMLTagEnd = (
            data.current_editor_font_name,
            0xFF000080,
            data.current_editor_font_size,
            None,
        )

    class IDL:
        Comment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        CommentDoc = (
            data.current_editor_font_name,
            0xFF3F703F,
            data.current_editor_font_size,
            None,
        )
        CommentDocKeyword = (
            data.current_editor_font_name,
            0xFF3060A0,
            data.current_editor_font_size,
            None,
        )
        CommentDocKeywordError = (
            data.current_editor_font_name,
            0xFF804020,
            data.current_editor_font_size,
            None,
        )
        CommentLine = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        CommentLineDoc = (
            data.current_editor_font_name,
            0xFF3F703F,
            data.current_editor_font_size,
            None,
        )
        Default = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        DoubleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        GlobalClass = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        HashQuotedString = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        Identifier = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactiveComment = (
            data.current_editor_font_name,
            0xFF90B090,
            data.current_editor_font_size,
            None,
        )
        InactiveCommentDoc = (
            data.current_editor_font_name,
            0xFFD0D0D0,
            data.current_editor_font_size,
            None,
        )
        InactiveCommentDocKeyword = (
            data.current_editor_font_name,
            0xFFC0C0C0,
            data.current_editor_font_size,
            None,
        )
        InactiveCommentDocKeywordError = (
            data.current_editor_font_name,
            0xFFC0C0C0,
            data.current_editor_font_size,
            None,
        )
        InactiveCommentLine = (
            data.current_editor_font_name,
            0xFF90B090,
            data.current_editor_font_size,
            None,
        )
        InactiveCommentLineDoc = (
            data.current_editor_font_name,
            0xFFC0C0C0,
            data.current_editor_font_size,
            None,
        )
        InactiveDefault = (
            data.current_editor_font_name,
            0xFFC0C0C0,
            data.current_editor_font_size,
            None,
        )
        InactiveDoubleQuotedString = (
            data.current_editor_font_name,
            0xFFB090B0,
            data.current_editor_font_size,
            None,
        )
        InactiveGlobalClass = (
            data.current_editor_font_name,
            0xFFB0B0B0,
            data.current_editor_font_size,
            None,
        )
        InactiveHashQuotedString = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactiveIdentifier = (
            data.current_editor_font_name,
            0xFFB0B0B0,
            data.current_editor_font_size,
            None,
        )
        InactiveKeyword = (
            data.current_editor_font_name,
            0xFF9090B0,
            data.current_editor_font_size,
            None,
        )
        InactiveKeywordSet2 = (
            data.current_editor_font_name,
            0xFFC0C0C0,
            data.current_editor_font_size,
            None,
        )
        InactiveNumber = (
            data.current_editor_font_name,
            0xFF90B090,
            data.current_editor_font_size,
            None,
        )
        InactiveOperator = (
            data.current_editor_font_name,
            0xFFB0B0B0,
            data.current_editor_font_size,
            None,
        )
        InactivePreProcessor = (
            data.current_editor_font_name,
            0xFFB0B090,
            data.current_editor_font_size,
            None,
        )
        InactivePreProcessorComment = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactivePreProcessorCommentLineDoc = (
            data.current_editor_font_name,
            0xFFC0C0C0,
            data.current_editor_font_size,
            None,
        )
        InactiveRawString = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactiveRegex = (
            data.current_editor_font_name,
            0xFF7FAF7F,
            data.current_editor_font_size,
            None,
        )
        InactiveSingleQuotedString = (
            data.current_editor_font_name,
            0xFFB090B0,
            data.current_editor_font_size,
            None,
        )
        InactiveTripleQuotedVerbatimString = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactiveUUID = (
            data.current_editor_font_name,
            0xFFC0C0C0,
            data.current_editor_font_size,
            None,
        )
        InactiveUnclosedString = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactiveVerbatimString = (
            data.current_editor_font_name,
            0xFF90B090,
            data.current_editor_font_size,
            None,
        )
        Keyword = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        KeywordSet2 = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Number = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        Operator = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        PreProcessor = (
            data.current_editor_font_name,
            0xFF7F7F00,
            data.current_editor_font_size,
            None,
        )
        PreProcessorComment = (
            data.current_editor_font_name,
            0xFF659900,
            data.current_editor_font_size,
            None,
        )
        PreProcessorCommentLineDoc = (
            data.current_editor_font_name,
            0xFF3F703F,
            data.current_editor_font_size,
            None,
        )
        RawString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        Regex = (
            data.current_editor_font_name,
            0xFF3F7F3F,
            data.current_editor_font_size,
            None,
        )
        SingleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        TripleQuotedVerbatimString = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        UUID = (
            data.current_editor_font_name,
            0xFF804080,
            data.current_editor_font_size,
            None,
        )
        UnclosedString = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        VerbatimString = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        UserLiteral = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactiveEscapeSequence = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        EscapeSequence = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactiveUserLiteral = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactiveTaskMarker = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        TaskMarker = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )

    class Java:
        Comment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        CommentDoc = (
            data.current_editor_font_name,
            0xFF3F703F,
            data.current_editor_font_size,
            None,
        )
        CommentDocKeyword = (
            data.current_editor_font_name,
            0xFF3060A0,
            data.current_editor_font_size,
            None,
        )
        CommentDocKeywordError = (
            data.current_editor_font_name,
            0xFF804020,
            data.current_editor_font_size,
            None,
        )
        CommentLine = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        CommentLineDoc = (
            data.current_editor_font_name,
            0xFF3F703F,
            data.current_editor_font_size,
            None,
        )
        Default = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        DoubleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        GlobalClass = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        HashQuotedString = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        Identifier = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactiveComment = (
            data.current_editor_font_name,
            0xFF90B090,
            data.current_editor_font_size,
            None,
        )
        InactiveCommentDoc = (
            data.current_editor_font_name,
            0xFFD0D0D0,
            data.current_editor_font_size,
            None,
        )
        InactiveCommentDocKeyword = (
            data.current_editor_font_name,
            0xFFC0C0C0,
            data.current_editor_font_size,
            None,
        )
        InactiveCommentDocKeywordError = (
            data.current_editor_font_name,
            0xFFC0C0C0,
            data.current_editor_font_size,
            None,
        )
        InactiveCommentLine = (
            data.current_editor_font_name,
            0xFF90B090,
            data.current_editor_font_size,
            None,
        )
        InactiveCommentLineDoc = (
            data.current_editor_font_name,
            0xFFC0C0C0,
            data.current_editor_font_size,
            None,
        )
        InactiveDefault = (
            data.current_editor_font_name,
            0xFFC0C0C0,
            data.current_editor_font_size,
            None,
        )
        InactiveDoubleQuotedString = (
            data.current_editor_font_name,
            0xFFB090B0,
            data.current_editor_font_size,
            None,
        )
        InactiveGlobalClass = (
            data.current_editor_font_name,
            0xFFB0B0B0,
            data.current_editor_font_size,
            None,
        )
        InactiveHashQuotedString = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactiveIdentifier = (
            data.current_editor_font_name,
            0xFFB0B0B0,
            data.current_editor_font_size,
            None,
        )
        InactiveKeyword = (
            data.current_editor_font_name,
            0xFF9090B0,
            data.current_editor_font_size,
            None,
        )
        InactiveKeywordSet2 = (
            data.current_editor_font_name,
            0xFFC0C0C0,
            data.current_editor_font_size,
            None,
        )
        InactiveNumber = (
            data.current_editor_font_name,
            0xFF90B090,
            data.current_editor_font_size,
            None,
        )
        InactiveOperator = (
            data.current_editor_font_name,
            0xFFB0B0B0,
            data.current_editor_font_size,
            None,
        )
        InactivePreProcessor = (
            data.current_editor_font_name,
            0xFFB0B090,
            data.current_editor_font_size,
            None,
        )
        InactivePreProcessorComment = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactivePreProcessorCommentLineDoc = (
            data.current_editor_font_name,
            0xFFC0C0C0,
            data.current_editor_font_size,
            None,
        )
        InactiveRawString = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactiveRegex = (
            data.current_editor_font_name,
            0xFF7FAF7F,
            data.current_editor_font_size,
            None,
        )
        InactiveSingleQuotedString = (
            data.current_editor_font_name,
            0xFFB090B0,
            data.current_editor_font_size,
            None,
        )
        InactiveTripleQuotedVerbatimString = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactiveUUID = (
            data.current_editor_font_name,
            0xFFC0C0C0,
            data.current_editor_font_size,
            None,
        )
        InactiveUnclosedString = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactiveVerbatimString = (
            data.current_editor_font_name,
            0xFF90B090,
            data.current_editor_font_size,
            None,
        )
        Keyword = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        KeywordSet2 = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Number = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        Operator = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        PreProcessor = (
            data.current_editor_font_name,
            0xFF7F7F00,
            data.current_editor_font_size,
            None,
        )
        PreProcessorComment = (
            data.current_editor_font_name,
            0xFF659900,
            data.current_editor_font_size,
            None,
        )
        PreProcessorCommentLineDoc = (
            data.current_editor_font_name,
            0xFF3F703F,
            data.current_editor_font_size,
            None,
        )
        RawString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        Regex = (
            data.current_editor_font_name,
            0xFF3F7F3F,
            data.current_editor_font_size,
            None,
        )
        SingleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        TripleQuotedVerbatimString = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        UUID = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        UnclosedString = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        VerbatimString = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        UserLiteral = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactiveEscapeSequence = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        EscapeSequence = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactiveUserLiteral = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactiveTaskMarker = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        TaskMarker = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )

    class JavaScript:
        Comment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        CommentDoc = (
            data.current_editor_font_name,
            0xFF3F703F,
            data.current_editor_font_size,
            None,
        )
        CommentDocKeyword = (
            data.current_editor_font_name,
            0xFF3060A0,
            data.current_editor_font_size,
            None,
        )
        CommentDocKeywordError = (
            data.current_editor_font_name,
            0xFF804020,
            data.current_editor_font_size,
            None,
        )
        CommentLine = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        CommentLineDoc = (
            data.current_editor_font_name,
            0xFF3F703F,
            data.current_editor_font_size,
            None,
        )
        Default = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        DoubleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        GlobalClass = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        HashQuotedString = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        Identifier = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactiveComment = (
            data.current_editor_font_name,
            0xFF90B090,
            data.current_editor_font_size,
            None,
        )
        InactiveCommentDoc = (
            data.current_editor_font_name,
            0xFFD0D0D0,
            data.current_editor_font_size,
            None,
        )
        InactiveCommentDocKeyword = (
            data.current_editor_font_name,
            0xFFC0C0C0,
            data.current_editor_font_size,
            None,
        )
        InactiveCommentDocKeywordError = (
            data.current_editor_font_name,
            0xFFC0C0C0,
            data.current_editor_font_size,
            None,
        )
        InactiveCommentLine = (
            data.current_editor_font_name,
            0xFF90B090,
            data.current_editor_font_size,
            None,
        )
        InactiveCommentLineDoc = (
            data.current_editor_font_name,
            0xFFC0C0C0,
            data.current_editor_font_size,
            None,
        )
        InactiveDefault = (
            data.current_editor_font_name,
            0xFFC0C0C0,
            data.current_editor_font_size,
            None,
        )
        InactiveDoubleQuotedString = (
            data.current_editor_font_name,
            0xFFB090B0,
            data.current_editor_font_size,
            None,
        )
        InactiveGlobalClass = (
            data.current_editor_font_name,
            0xFFB0B0B0,
            data.current_editor_font_size,
            None,
        )
        InactiveHashQuotedString = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactiveIdentifier = (
            data.current_editor_font_name,
            0xFFB0B0B0,
            data.current_editor_font_size,
            None,
        )
        InactiveKeyword = (
            data.current_editor_font_name,
            0xFF9090B0,
            data.current_editor_font_size,
            None,
        )
        InactiveKeywordSet2 = (
            data.current_editor_font_name,
            0xFFC0C0C0,
            data.current_editor_font_size,
            None,
        )
        InactiveNumber = (
            data.current_editor_font_name,
            0xFF90B090,
            data.current_editor_font_size,
            None,
        )
        InactiveOperator = (
            data.current_editor_font_name,
            0xFFB0B0B0,
            data.current_editor_font_size,
            None,
        )
        InactivePreProcessor = (
            data.current_editor_font_name,
            0xFFB0B090,
            data.current_editor_font_size,
            None,
        )
        InactivePreProcessorComment = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactivePreProcessorCommentLineDoc = (
            data.current_editor_font_name,
            0xFFC0C0C0,
            data.current_editor_font_size,
            None,
        )
        InactiveRawString = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactiveRegex = (
            data.current_editor_font_name,
            0xFF7FAF7F,
            data.current_editor_font_size,
            None,
        )
        InactiveSingleQuotedString = (
            data.current_editor_font_name,
            0xFFB090B0,
            data.current_editor_font_size,
            None,
        )
        InactiveTripleQuotedVerbatimString = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactiveUUID = (
            data.current_editor_font_name,
            0xFFC0C0C0,
            data.current_editor_font_size,
            None,
        )
        InactiveUnclosedString = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactiveVerbatimString = (
            data.current_editor_font_name,
            0xFF90B090,
            data.current_editor_font_size,
            None,
        )
        Keyword = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        KeywordSet2 = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Number = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        Operator = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        PreProcessor = (
            data.current_editor_font_name,
            0xFF7F7F00,
            data.current_editor_font_size,
            None,
        )
        PreProcessorComment = (
            data.current_editor_font_name,
            0xFF659900,
            data.current_editor_font_size,
            None,
        )
        PreProcessorCommentLineDoc = (
            data.current_editor_font_name,
            0xFF3F703F,
            data.current_editor_font_size,
            None,
        )
        RawString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        Regex = (
            data.current_editor_font_name,
            0xFF3F7F3F,
            data.current_editor_font_size,
            None,
        )
        SingleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        TripleQuotedVerbatimString = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        UUID = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        UnclosedString = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        VerbatimString = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        UserLiteral = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactiveEscapeSequence = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        EscapeSequence = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactiveUserLiteral = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InactiveTaskMarker = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        TaskMarker = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )

    class Lua:
        BasicFunctions = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        Character = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        Comment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        CoroutinesIOSystemFacilities = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        Default = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Identifier = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Keyword = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        KeywordSet5 = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        KeywordSet6 = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        KeywordSet7 = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        KeywordSet8 = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Label = (
            data.current_editor_font_name,
            0xFF7F7F00,
            data.current_editor_font_size,
            None,
        )
        LineComment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        LiteralString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        Number = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        Operator = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Preprocessor = (
            data.current_editor_font_name,
            0xFF7F7F00,
            data.current_editor_font_size,
            None,
        )
        String = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        StringTableMathsFunctions = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        UnclosedString = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )

    class Makefile:
        Comment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        Default = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Error = (
            data.current_editor_font_name,
            0xFFFFFF00,
            data.current_editor_font_size,
            None,
        )
        Operator = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Preprocessor = (
            data.current_editor_font_name,
            0xFF7F7F00,
            data.current_editor_font_size,
            None,
        )
        Target = (
            data.current_editor_font_name,
            0xFFA00000,
            data.current_editor_font_size,
            None,
        )
        Variable = (
            data.current_editor_font_name,
            0xFF000080,
            data.current_editor_font_size,
            None,
        )

    class Matlab:
        Command = (
            data.current_editor_font_name,
            0xFF7F7F00,
            data.current_editor_font_size,
            None,
        )
        Comment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        Default = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        DoubleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        Identifier = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Keyword = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        Number = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        Operator = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        SingleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )

    class Octave:
        Command = (
            data.current_editor_font_name,
            0xFF7F7F00,
            data.current_editor_font_size,
            None,
        )
        Comment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        Default = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        DoubleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        Identifier = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Keyword = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        Number = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        Operator = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        SingleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )

    class PO:
        Comment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        Default = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Flags = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Fuzzy = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        MessageContext = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        MessageContextText = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        MessageContextTextEOL = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        MessageId = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        MessageIdText = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        MessageIdTextEOL = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        MessageString = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        MessageStringText = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        MessageStringTextEOL = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        ProgrammerComment = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Reference = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )

    class POV:
        BadDirective = (
            data.current_editor_font_name,
            0xFF804020,
            data.current_editor_font_size,
            None,
        )
        Comment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        CommentLine = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        Default = (
            data.current_editor_font_name,
            0xFFFF0080,
            data.current_editor_font_size,
            None,
        )
        Directive = (
            data.current_editor_font_name,
            0xFF7F7F00,
            data.current_editor_font_size,
            None,
        )
        Identifier = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        KeywordSet6 = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        KeywordSet7 = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        KeywordSet8 = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        Number = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        ObjectsCSGAppearance = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        Operator = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        PredefinedFunctions = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        PredefinedIdentifiers = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        String = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        TypesModifiersItems = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        UnclosedString = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )

    class Pascal:
        Asm = (
            data.current_editor_font_name,
            0xFF804080,
            data.current_editor_font_size,
            None,
        )
        Character = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        Comment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        CommentLine = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        CommentParenthesis = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        Default = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        HexNumber = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        Identifier = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Keyword = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        Number = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        Operator = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        PreProcessor = (
            data.current_editor_font_name,
            0xFF7F7F00,
            data.current_editor_font_size,
            None,
        )
        PreProcessorParenthesis = (
            data.current_editor_font_name,
            0xFF7F7F00,
            data.current_editor_font_size,
            None,
        )
        SingleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        UnclosedString = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )

    class Perl:
        Array = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        BacktickHereDocument = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        BacktickHereDocumentVar = (
            data.current_editor_font_name,
            0xFFD00000,
            data.current_editor_font_size,
            None,
        )
        Backticks = (
            data.current_editor_font_name,
            0xFFFFFF00,
            data.current_editor_font_size,
            None,
        )
        BackticksVar = (
            data.current_editor_font_name,
            0xFFD00000,
            data.current_editor_font_size,
            None,
        )
        Comment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        DataSection = (
            data.current_editor_font_name,
            0xFF600000,
            data.current_editor_font_size,
            None,
        )
        Default = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        DoubleQuotedHereDocument = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        DoubleQuotedHereDocumentVar = (
            data.current_editor_font_name,
            0xFFD00000,
            data.current_editor_font_size,
            None,
        )
        DoubleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        DoubleQuotedStringVar = (
            data.current_editor_font_name,
            0xFFD00000,
            data.current_editor_font_size,
            None,
        )
        Error = (
            data.current_editor_font_name,
            0xFFFFFF00,
            data.current_editor_font_size,
            None,
        )
        FormatBody = (
            data.current_editor_font_name,
            0xFFC000C0,
            data.current_editor_font_size,
            None,
        )
        FormatIdentifier = (
            data.current_editor_font_name,
            0xFFC000C0,
            data.current_editor_font_size,
            None,
        )
        Hash = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        HereDocumentDelimiter = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Identifier = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Keyword = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        Number = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        Operator = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        POD = (
            data.current_editor_font_name,
            0xFF004000,
            data.current_editor_font_size,
            None,
        )
        PODVerbatim = (
            data.current_editor_font_name,
            0xFF004000,
            data.current_editor_font_size,
            None,
        )
        QuotedStringQ = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        QuotedStringQQ = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        QuotedStringQQVar = (
            data.current_editor_font_name,
            0xFFD00000,
            data.current_editor_font_size,
            None,
        )
        QuotedStringQR = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        QuotedStringQRVar = (
            data.current_editor_font_name,
            0xFFD00000,
            data.current_editor_font_size,
            None,
        )
        QuotedStringQW = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        QuotedStringQX = (
            data.current_editor_font_name,
            0xFFFFFF00,
            data.current_editor_font_size,
            None,
        )
        QuotedStringQXVar = (
            data.current_editor_font_name,
            0xFFD00000,
            data.current_editor_font_size,
            None,
        )
        Regex = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        RegexVar = (
            data.current_editor_font_name,
            0xFFD00000,
            data.current_editor_font_size,
            None,
        )
        Scalar = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        SingleQuotedHereDocument = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        SingleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        SubroutinePrototype = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Substitution = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        SubstitutionVar = (
            data.current_editor_font_name,
            0xFFD00000,
            data.current_editor_font_size,
            None,
        )
        SymbolTable = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Translation = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )

    class PostScript:
        ArrayParenthesis = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        BadStringCharacter = (
            data.current_editor_font_name,
            0xFFFFFF00,
            data.current_editor_font_size,
            None,
        )
        Base85String = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        Comment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        DSCComment = (
            data.current_editor_font_name,
            0xFF3F703F,
            data.current_editor_font_size,
            None,
        )
        DSCCommentValue = (
            data.current_editor_font_name,
            0xFF3060A0,
            data.current_editor_font_size,
            None,
        )
        Default = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        DictionaryParenthesis = (
            data.current_editor_font_name,
            0xFF3060A0,
            data.current_editor_font_size,
            None,
        )
        HexString = (
            data.current_editor_font_name,
            0xFF3F7F3F,
            data.current_editor_font_size,
            None,
        )
        ImmediateEvalLiteral = (
            data.current_editor_font_name,
            0xFF7F7F00,
            data.current_editor_font_size,
            None,
        )
        Keyword = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        Literal = (
            data.current_editor_font_name,
            0xFF7F7F00,
            data.current_editor_font_size,
            None,
        )
        Name = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Number = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        ProcedureParenthesis = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Text = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )

    class Properties:
        Assignment = (
            data.current_editor_font_name,
            0xFFB06000,
            data.current_editor_font_size,
            None,
        )
        Comment = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        Default = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        DefaultValue = (
            data.current_editor_font_name,
            0xFF7F7F00,
            data.current_editor_font_size,
            None,
        )
        Key = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Section = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )

    class Python:
        ClassName = (
            data.current_editor_font_name,
            0xFF0000FF,
            data.current_editor_font_size,
            None,
        )
        Comment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        CommentBlock = (
            data.current_editor_font_name,
            0xFF52004A,
            data.current_editor_font_size,
            None,
        )
        Decorator = (
            data.current_editor_font_name,
            0xFF805000,
            data.current_editor_font_size,
            None,
        )
        Default = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        DoubleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        FunctionMethodName = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        HighlightedIdentifier = (
            data.current_editor_font_name,
            0xFF407090,
            data.current_editor_font_size,
            None,
        )
        Identifier = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Inconsistent = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        Keyword = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            True,
        )
        NoWarning = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        Number = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        Operator = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        SingleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        Spaces = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        Tabs = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        TabsAfterSpaces = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        TripleDoubleQuotedString = (
            data.current_editor_font_name,
            0xFF7F0000,
            data.current_editor_font_size,
            None,
        )
        TripleSingleQuotedString = (
            data.current_editor_font_name,
            0xFF7F0000,
            data.current_editor_font_size,
            None,
        )
        UnclosedString = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        CustomKeyword = (
            data.current_editor_font_name,
            0xFF6E6E00,
            data.current_editor_font_size,
            True,
        )

    class Ruby:
        Backticks = (
            data.current_editor_font_name,
            0xFFFFFF00,
            data.current_editor_font_size,
            None,
        )
        ClassName = (
            data.current_editor_font_name,
            0xFF0000FF,
            data.current_editor_font_size,
            None,
        )
        ClassVariable = (
            data.current_editor_font_name,
            0xFF8000B0,
            data.current_editor_font_size,
            None,
        )
        Comment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        DataSection = (
            data.current_editor_font_name,
            0xFF600000,
            data.current_editor_font_size,
            None,
        )
        Default = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        DemotedKeyword = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        DoubleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        Error = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        FunctionMethodName = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        Global = (
            data.current_editor_font_name,
            0xFF800080,
            data.current_editor_font_size,
            None,
        )
        HereDocument = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        HereDocumentDelimiter = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Identifier = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        InstanceVariable = (
            data.current_editor_font_name,
            0xFFB00080,
            data.current_editor_font_size,
            None,
        )
        Keyword = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        ModuleName = (
            data.current_editor_font_name,
            0xFFA000A0,
            data.current_editor_font_size,
            None,
        )
        Number = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        Operator = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        POD = (
            data.current_editor_font_name,
            0xFF004000,
            data.current_editor_font_size,
            None,
        )
        PercentStringQ = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        PercentStringq = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        PercentStringr = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        PercentStringw = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        PercentStringx = (
            data.current_editor_font_name,
            0xFFFFFF00,
            data.current_editor_font_size,
            None,
        )
        Regex = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        SingleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        Stderr = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Stdin = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Stdout = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Symbol = (
            data.current_editor_font_name,
            0xFFC0A030,
            data.current_editor_font_size,
            None,
        )

    class SQL:
        Comment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        CommentDoc = (
            data.current_editor_font_name,
            0xFF7F7F7F,
            data.current_editor_font_size,
            None,
        )
        CommentDocKeyword = (
            data.current_editor_font_name,
            0xFF3060A0,
            data.current_editor_font_size,
            None,
        )
        CommentDocKeywordError = (
            data.current_editor_font_name,
            0xFF804020,
            data.current_editor_font_size,
            None,
        )
        CommentLine = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        CommentLineHash = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        Default = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        DoubleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        Identifier = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Keyword = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        KeywordSet5 = (
            data.current_editor_font_name,
            0xFF4B0082,
            data.current_editor_font_size,
            None,
        )
        KeywordSet6 = (
            data.current_editor_font_name,
            0xFFB00040,
            data.current_editor_font_size,
            None,
        )
        KeywordSet7 = (
            data.current_editor_font_name,
            0xFF8B0000,
            data.current_editor_font_size,
            None,
        )
        KeywordSet8 = (
            data.current_editor_font_name,
            0xFF800080,
            data.current_editor_font_size,
            None,
        )
        Number = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        Operator = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        PlusComment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        PlusKeyword = (
            data.current_editor_font_name,
            0xFF7F7F00,
            data.current_editor_font_size,
            None,
        )
        PlusPrompt = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        QuotedIdentifier = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        SingleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        QuotedOperator = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )

    class Spice:
        Command = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        Comment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        Default = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        Delimiter = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Function = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        Identifier = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Number = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        Parameter = (
            data.current_editor_font_name,
            0xFF0040E0,
            data.current_editor_font_size,
            None,
        )
        Value = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )

    class TCL:
        Comment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        CommentBlock = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        CommentBox = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        CommentLine = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        Default = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        ExpandKeyword = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        ITCLKeyword = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        Identifier = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        KeywordSet6 = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        KeywordSet7 = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        KeywordSet8 = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        KeywordSet9 = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        Modifier = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        Number = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        Operator = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        QuotedKeyword = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        QuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        Substitution = (
            data.current_editor_font_name,
            0xFF7F7F00,
            data.current_editor_font_size,
            None,
        )
        SubstitutionBrace = (
            data.current_editor_font_name,
            0xFF7F7F00,
            data.current_editor_font_size,
            None,
        )
        TCLKeyword = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        TkCommand = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        TkKeyword = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )

    class TeX:
        Command = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        Default = (
            data.current_editor_font_name,
            0xFF3F3F3F,
            data.current_editor_font_size,
            None,
        )
        Group = (
            data.current_editor_font_name,
            0xFF7F0000,
            data.current_editor_font_size,
            None,
        )
        Special = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        Symbol = (
            data.current_editor_font_name,
            0xFF7F7F00,
            data.current_editor_font_size,
            None,
        )
        Text = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )

    class VHDL:
        Attribute = (
            data.current_editor_font_name,
            0xFF804020,
            data.current_editor_font_size,
            None,
        )
        Comment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        CommentLine = (
            data.current_editor_font_name,
            0xFF3F7F3F,
            data.current_editor_font_size,
            None,
        )
        Default = (
            data.current_editor_font_name,
            0xFF800080,
            data.current_editor_font_size,
            None,
        )
        Identifier = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Keyword = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        KeywordSet7 = (
            data.current_editor_font_name,
            0xFF804020,
            data.current_editor_font_size,
            None,
        )
        Number = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        Operator = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        StandardFunction = (
            data.current_editor_font_name,
            0xFF808020,
            data.current_editor_font_size,
            None,
        )
        StandardOperator = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        StandardPackage = (
            data.current_editor_font_name,
            0xFF208020,
            data.current_editor_font_size,
            None,
        )
        StandardType = (
            data.current_editor_font_name,
            0xFF208080,
            data.current_editor_font_size,
            None,
        )
        String = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        UnclosedString = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        CommentBlock = (
            data.current_editor_font_name,
            0xFF800080,
            data.current_editor_font_size,
            None,
        )

    class Verilog:
        Comment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        CommentBang = (
            data.current_editor_font_name,
            0xFF3F7F3F,
            data.current_editor_font_size,
            None,
        )
        CommentLine = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        Default = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        Identifier = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Keyword = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        KeywordSet2 = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        Number = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        Operator = (
            data.current_editor_font_name,
            0xFF007070,
            data.current_editor_font_size,
            None,
        )
        Preprocessor = (
            data.current_editor_font_name,
            0xFF7F7F00,
            data.current_editor_font_size,
            None,
        )
        String = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        SystemTask = (
            data.current_editor_font_name,
            0xFF804020,
            data.current_editor_font_size,
            None,
        )
        UnclosedString = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        UserKeywordSet = (
            data.current_editor_font_name,
            0xFF2A00FF,
            data.current_editor_font_size,
            None,
        )
        InactiveDefault = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        InactiveUnclosedString = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        InactiveCommentKeyword = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        InactiveKeywordSet2 = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        InactiveComment = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        DeclareInputOutputPort = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        InactiveString = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        CommentKeyword = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        DeclareOutputPort = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        PortConnection = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        InactiveKeyword = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        DeclareInputPort = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        InactiveDeclareInputPort = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        InactiveDeclareOutputPort = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        InactiveUserKeywordSet = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        InactiveCommentBang = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        InactiveIdentifier = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        InactivePortConnection = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        InactiveNumber = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        InactiveSystemTask = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        InactivePreprocessor = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        InactiveOperator = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        InactiveDeclareInputOutputPort = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        InactiveCommentLine = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )

    class XML:
        ASPAtStart = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        ASPJavaScriptComment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        ASPJavaScriptCommentDoc = (
            data.current_editor_font_name,
            0xFF7F7F7F,
            data.current_editor_font_size,
            None,
        )
        ASPJavaScriptCommentLine = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        ASPJavaScriptDefault = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        ASPJavaScriptDoubleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        ASPJavaScriptKeyword = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        ASPJavaScriptNumber = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        ASPJavaScriptRegex = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        ASPJavaScriptSingleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        ASPJavaScriptStart = (
            data.current_editor_font_name,
            0xFF7F7F00,
            data.current_editor_font_size,
            None,
        )
        ASPJavaScriptSymbol = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        ASPJavaScriptUnclosedString = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        ASPJavaScriptWord = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        ASPPythonClassName = (
            data.current_editor_font_name,
            0xFF0000FF,
            data.current_editor_font_size,
            None,
        )
        ASPPythonComment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        ASPPythonDefault = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        ASPPythonDoubleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        ASPPythonFunctionMethodName = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        ASPPythonIdentifier = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        ASPPythonKeyword = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        ASPPythonNumber = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        ASPPythonOperator = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        ASPPythonSingleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        ASPPythonStart = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        ASPPythonTripleDoubleQuotedString = (
            data.current_editor_font_name,
            0xFF7F0000,
            data.current_editor_font_size,
            None,
        )
        ASPPythonTripleSingleQuotedString = (
            data.current_editor_font_name,
            0xFF7F0000,
            data.current_editor_font_size,
            None,
        )
        ASPStart = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        ASPVBScriptComment = (
            data.current_editor_font_name,
            0xFF008000,
            data.current_editor_font_size,
            None,
        )
        ASPVBScriptDefault = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        ASPVBScriptIdentifier = (
            data.current_editor_font_name,
            0xFF000080,
            data.current_editor_font_size,
            None,
        )
        ASPVBScriptKeyword = (
            data.current_editor_font_name,
            0xFF000080,
            data.current_editor_font_size,
            None,
        )
        ASPVBScriptNumber = (
            data.current_editor_font_name,
            0xFF008080,
            data.current_editor_font_size,
            None,
        )
        ASPVBScriptStart = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        ASPVBScriptString = (
            data.current_editor_font_name,
            0xFF800080,
            data.current_editor_font_size,
            None,
        )
        ASPVBScriptUnclosedString = (
            data.current_editor_font_name,
            0xFF000080,
            data.current_editor_font_size,
            None,
        )
        ASPXCComment = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Attribute = (
            data.current_editor_font_name,
            0xFF008080,
            data.current_editor_font_size,
            None,
        )
        CDATA = (
            data.current_editor_font_name,
            0xFF800000,
            data.current_editor_font_size,
            None,
        )
        Default = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Entity = (
            data.current_editor_font_name,
            0xFF800080,
            data.current_editor_font_size,
            None,
        )
        HTMLComment = (
            data.current_editor_font_name,
            0xFF808000,
            data.current_editor_font_size,
            None,
        )
        HTMLDoubleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        HTMLNumber = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        HTMLSingleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        HTMLValue = (
            data.current_editor_font_name,
            0xFF608060,
            data.current_editor_font_size,
            None,
        )
        JavaScriptComment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        JavaScriptCommentDoc = (
            data.current_editor_font_name,
            0xFF3F703F,
            data.current_editor_font_size,
            None,
        )
        JavaScriptCommentLine = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        JavaScriptDefault = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        JavaScriptDoubleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        JavaScriptKeyword = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        JavaScriptNumber = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        JavaScriptRegex = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        JavaScriptSingleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        JavaScriptStart = (
            data.current_editor_font_name,
            0xFF7F7F00,
            data.current_editor_font_size,
            None,
        )
        JavaScriptSymbol = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        JavaScriptUnclosedString = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        JavaScriptWord = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        OtherInTag = (
            data.current_editor_font_name,
            0xFF800080,
            data.current_editor_font_size,
            None,
        )
        PHPComment = (
            data.current_editor_font_name,
            0xFF999999,
            data.current_editor_font_size,
            None,
        )
        PHPCommentLine = (
            data.current_editor_font_name,
            0xFF666666,
            data.current_editor_font_size,
            None,
        )
        PHPDefault = (
            data.current_editor_font_name,
            0xFF000033,
            data.current_editor_font_size,
            None,
        )
        PHPDoubleQuotedString = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        PHPDoubleQuotedVariable = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        PHPKeyword = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        PHPNumber = (
            data.current_editor_font_name,
            0xFFCC9900,
            data.current_editor_font_size,
            None,
        )
        PHPOperator = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        PHPSingleQuotedString = (
            data.current_editor_font_name,
            0xFF009F00,
            data.current_editor_font_size,
            None,
        )
        PHPStart = (
            data.current_editor_font_name,
            0xFF800000,
            data.current_editor_font_size,
            None,
        )
        PHPVariable = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        PythonClassName = (
            data.current_editor_font_name,
            0xFF0000FF,
            data.current_editor_font_size,
            None,
        )
        PythonComment = (
            data.current_editor_font_name,
            0xFF007F00,
            data.current_editor_font_size,
            None,
        )
        PythonDefault = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        PythonDoubleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        PythonFunctionMethodName = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        PythonIdentifier = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        PythonKeyword = (
            data.current_editor_font_name,
            0xFF00007F,
            data.current_editor_font_size,
            None,
        )
        PythonNumber = (
            data.current_editor_font_name,
            0xFF007F7F,
            data.current_editor_font_size,
            None,
        )
        PythonOperator = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        PythonSingleQuotedString = (
            data.current_editor_font_name,
            0xFF7F007F,
            data.current_editor_font_size,
            None,
        )
        PythonStart = (
            data.current_editor_font_name,
            0xFF808080,
            data.current_editor_font_size,
            None,
        )
        PythonTripleDoubleQuotedString = (
            data.current_editor_font_name,
            0xFF7F0000,
            data.current_editor_font_size,
            None,
        )
        PythonTripleSingleQuotedString = (
            data.current_editor_font_name,
            0xFF7F0000,
            data.current_editor_font_size,
            None,
        )
        SGMLBlockDefault = (
            data.current_editor_font_name,
            0xFF000066,
            data.current_editor_font_size,
            None,
        )
        SGMLCommand = (
            data.current_editor_font_name,
            0xFF000080,
            data.current_editor_font_size,
            None,
        )
        SGMLComment = (
            data.current_editor_font_name,
            0xFF808000,
            data.current_editor_font_size,
            None,
        )
        SGMLDefault = (
            data.current_editor_font_name,
            0xFF000080,
            data.current_editor_font_size,
            None,
        )
        SGMLDoubleQuotedString = (
            data.current_editor_font_name,
            0xFF800000,
            data.current_editor_font_size,
            None,
        )
        SGMLEntity = (
            data.current_editor_font_name,
            0xFF333333,
            data.current_editor_font_size,
            None,
        )
        SGMLError = (
            data.current_editor_font_name,
            0xFF800000,
            data.current_editor_font_size,
            None,
        )
        SGMLParameter = (
            data.current_editor_font_name,
            0xFF006600,
            data.current_editor_font_size,
            None,
        )
        SGMLParameterComment = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        SGMLSingleQuotedString = (
            data.current_editor_font_name,
            0xFF993300,
            data.current_editor_font_size,
            None,
        )
        SGMLSpecial = (
            data.current_editor_font_name,
            0xFF3366FF,
            data.current_editor_font_size,
            None,
        )
        Script = (
            data.current_editor_font_name,
            0xFF000080,
            data.current_editor_font_size,
            None,
        )
        Tag = (
            data.current_editor_font_name,
            0xFF000080,
            data.current_editor_font_size,
            None,
        )
        UnknownAttribute = (
            data.current_editor_font_name,
            0xFF008080,
            data.current_editor_font_size,
            None,
        )
        UnknownTag = (
            data.current_editor_font_name,
            0xFF000080,
            data.current_editor_font_size,
            None,
        )
        VBScriptComment = (
            data.current_editor_font_name,
            0xFF008000,
            data.current_editor_font_size,
            None,
        )
        VBScriptDefault = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        VBScriptIdentifier = (
            data.current_editor_font_name,
            0xFF000080,
            data.current_editor_font_size,
            None,
        )
        VBScriptKeyword = (
            data.current_editor_font_name,
            0xFF000080,
            data.current_editor_font_size,
            None,
        )
        VBScriptNumber = (
            data.current_editor_font_name,
            0xFF008080,
            data.current_editor_font_size,
            None,
        )
        VBScriptStart = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        VBScriptString = (
            data.current_editor_font_name,
            0xFF800080,
            data.current_editor_font_size,
            None,
        )
        VBScriptUnclosedString = (
            data.current_editor_font_name,
            0xFF000080,
            data.current_editor_font_size,
            None,
        )
        XMLEnd = (
            data.current_editor_font_name,
            0xFF800080,
            data.current_editor_font_size,
            None,
        )
        XMLStart = (
            data.current_editor_font_name,
            0xFF800080,
            data.current_editor_font_size,
            None,
        )
        XMLTagEnd = (
            data.current_editor_font_name,
            0xFF000080,
            data.current_editor_font_size,
            None,
        )

    class YAML:
        Comment = (
            data.current_editor_font_name,
            0xFF008800,
            data.current_editor_font_size,
            None,
        )
        Default = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        DocumentDelimiter = (
            data.current_editor_font_name,
            0xFFFFFFFF,
            data.current_editor_font_size,
            None,
        )
        Identifier = (
            data.current_editor_font_name,
            0xFF000088,
            data.current_editor_font_size,
            None,
        )
        Keyword = (
            data.current_editor_font_name,
            0xFF880088,
            data.current_editor_font_size,
            None,
        )
        Number = (
            data.current_editor_font_name,
            0xFF880000,
            data.current_editor_font_size,
            None,
        )
        Operator = (
            data.current_editor_font_name,
            0xFF000000,
            data.current_editor_font_size,
            None,
        )
        Reference = (
            data.current_editor_font_name,
            0xFF008888,
            data.current_editor_font_size,
            None,
        )
        SyntaxErrorMarker = (
            data.current_editor_font_name,
            0xFFFFFFFF,
            data.current_editor_font_size,
            None,
        )
        TextBlockMarker = (
            data.current_editor_font_name,
            0xFF333366,
            data.current_editor_font_size,
            None,
        )


class Paper:
    Default = data.QColor(0xFFFFFFFF)
    DefaultHtml = "#ffffffff"

    class Ada:
        Default = 0xFFFFFFFF
        Comment = 0xFFFFFFFF
        Keyword = 0xFFFFFFFF
        String = 0xFFFFFFFF
        Procedure = 0xFFFFFFFF
        Number = 0xFFFFFFFF
        Type = 0xFFFFFFFF
        Package = 0xFFFFFFFF

    class AWK:
        Default = 0xFFFFFFFF
        Comment = 0xFFFFFFFF
        Keyword = 0xFFFFFFFF
        BuiltInVariable = 0xFFFFFFFF
        BuiltInFunction = 0xFFFFFFFF
        String = 0xFFFFFFFF
        Number = 0xFFFFFFFF
        Operator = 0xFFFFFFFF

    class CiCode:
        Default = 0xFFFFFFFF
        Comment = 0xFFFFFFFF
        Keyword = 0xFFFFFFFF
        BuiltInVariable = 0xFFFFFFFF
        BuiltInFunction = 0xFFFFFFFF
        String = 0xFFFFFFFF
        Number = 0xFFFFFFFF
        Operator = 0xFFFFFFFF

    class Nim:
        Default = 0xFFFFFFFF
        Comment = 0xFFFFFFFF
        BasicKeyword = 0xFFFFFFFF
        TopKeyword = 0xFFFFFFFF
        String = 0xFFFFFFFF
        LongString = 0xFFFFFFFF
        Number = 0xFFFFFFFF
        Operator = 0xFFFFFFFF
        Unsafe = 0xFFFFFFFF
        Type = 0xFFFFFFFF
        DocumentationComment = 0xFFFFFFFF
        Definition = 0xFFFFFFFF
        Class = 0xFFFFFFFF
        KeywordOperator = 0xFFFFFFFF
        CharLiteral = 0xFFFFFFFF
        CaseOf = 0xFFFFFFFF
        UserKeyword = 0xFFFFFFFF
        MultilineComment = 0xFFFFFFFF
        MultilineDocumentation = 0xFFFFFFFF
        Pragma = 0xFFFFFFFF

    class RouterOS:
        Default = 0xFFFFFFFF
        Operator = 0xFFFFFFFF
        Comment = 0xFFFFFFFF
        Keyword1 = 0xFFFFFFFF
        Keyword2 = 0xFFFFFFFF
        Keyword3 = 0xFFFFFFFF

    class Oberon:
        Default = 0xFFFFFFFF
        Comment = 0xFFFFFFFF
        Keyword = 0xFFFFFFFF
        String = 0xFFFFFFFF
        Procedure = 0xFFFFFFFF
        Module = 0xFFFFFFFF
        Number = 0xFFFFFFFF
        Type = 0xFFFFFFFF

    # Generated
    class AVS:
        Function = 0xFFFFFFFF
        KeywordSet6 = 0xFFFFFFFF
        TripleString = 0xFFFFFFFF
        LineComment = 0xFFFFFFFF
        Plugin = 0xFFFFFFFF
        String = 0xFFFFFFFF
        ClipProperty = 0xFFFFFFFF
        Default = 0xFFFFFFFF
        Operator = 0xFFFFFFFF
        Number = 0xFFFFFFFF
        Filter = 0xFFFFFFFF
        Identifier = 0xFFFFFFFF
        NestedBlockComment = 0xFFFFFFFF
        Keyword = 0xFFFFFFFF
        BlockComment = 0xFFFFFFFF

    class Bash:
        Error = 0xFFFF0000
        Backticks = 0xFFA08080
        SingleQuotedHereDocument = 0xFFDDD0DD
        Scalar = 0xFFFFE0E0
        HereDocumentDelimiter = 0xFFDDD0DD
        Comment = 0xFFFFFFFF
        SingleQuotedString = 0xFFFFFFFF
        Default = 0xFFFFFFFF
        Operator = 0xFFFFFFFF
        ParameterExpansion = 0xFFFFFFE0
        Number = 0xFFFFFFFF
        Identifier = 0xFFFFFFFF
        Keyword = 0xFFFFFFFF
        DoubleQuotedString = 0xFFFFFFFF

    class Batch:
        Label = 0xFF606060
        Default = 0xFFFFFFFF
        Keyword = 0xFFFFFFFF
        ExternalCommand = 0xFFFFFFFF
        Variable = 0xFFFFFFFF
        Comment = 0xFFFFFFFF
        HideCommandChar = 0xFFFFFFFF
        Operator = 0xFFFFFFFF

    class CMake:
        Function = 0xFFFFFFFF
        BlockForeach = 0xFFFFFFFF
        BlockWhile = 0xFFFFFFFF
        StringLeftQuote = 0xFFEEEEEE
        Label = 0xFFFFFFFF
        Comment = 0xFFFFFFFF
        BlockMacro = 0xFFFFFFFF
        StringRightQuote = 0xFFEEEEEE
        Default = 0xFFFFFFFF
        Number = 0xFFFFFFFF
        BlockIf = 0xFFFFFFFF
        Variable = 0xFFFFFFFF
        KeywordSet3 = 0xFFFFFFFF
        String = 0xFFEEEEEE
        StringVariable = 0xFFEEEEEE

    class CPP:
        CommentDocKeywordError = 0xFFFFFFFF
        InactiveRegex = 0xFFE0F0E0
        InactivePreProcessorComment = 0xFFFFFFFF
        UUID = 0xFFFFFFFF
        InactiveVerbatimString = 0xFFE0FFE0
        SingleQuotedString = 0xFFFFFFFF
        Operator = 0xFFFFFFFF
        InactiveOperator = 0xFFFFFFFF
        InactivePreProcessor = 0xFFFFFFFF
        UnclosedString = 0xFFE0C0E0
        Identifier = 0xFFFFFFFF
        InactiveRawString = 0xFFFFFFFF
        PreProcessor = 0xFFFFFFFF
        KeywordSet2 = 0xFFFFFFFF
        InactiveUnclosedString = 0xFFE0C0E0
        InactiveCommentLine = 0xFFFFFFFF
        InactiveNumber = 0xFFFFFFFF
        InactivePreProcessorCommentLineDoc = 0xFFFFFFFF
        Number = 0xFFFFFFFF
        InactiveUUID = 0xFFFFFFFF
        CommentDoc = 0xFFFFFFFF
        InactiveCommentDoc = 0xFFFFFFFF
        GlobalClass = 0xFFFFFFFF
        InactiveSingleQuotedString = 0xFFFFFFFF
        HashQuotedString = 0xFFE7FFD7
        VerbatimString = 0xFFE0FFE0
        InactiveHashQuotedString = 0xFFFFFFFF
        Regex = 0xFFE0F0E0
        InactiveGlobalClass = 0xFFFFFFFF
        InactiveIdentifier = 0xFFFFFFFF
        CommentLineDoc = 0xFFFFFFFF
        TripleQuotedVerbatimString = 0xFFE0FFE0
        InactiveKeywordSet2 = 0xFFFFFFFF
        InactiveCommentDocKeyword = 0xFFFFFFFF
        Keyword = 0xFFFFFFFF
        InactiveCommentLineDoc = 0xFFFFFFFF
        InactiveDefault = 0xFFFFFFFF
        InactiveCommentDocKeywordError = 0xFFFFFFFF
        InactiveTripleQuotedVerbatimString = 0xFFFFFFFF
        CommentDocKeyword = 0xFFFFFFFF
        InactiveDoubleQuotedString = 0xFFFFFFFF
        CommentLine = 0xFFFFFFFF
        Comment = 0xFFFFFFFF
        PreProcessorComment = 0xFFFFFFFF
        InactiveComment = 0xFFFFFFFF
        RawString = 0xFFFFF3FF
        Default = 0xFFFFFFFF
        PreProcessorCommentLineDoc = 0xFFFFFFFF
        DoubleQuotedString = 0xFFFFFFFF
        InactiveKeyword = 0xFFFFFFFF
        UserLiteral = 0xFFFFFFFF
        InactiveEscapeSequence = 0xFFFFFFFF
        EscapeSequence = 0xFFFFFFFF
        InactiveUserLiteral = 0xFFFFFFFF
        InactiveTaskMarker = 0xFFFFFFFF
        TaskMarker = 0xFFFFFFFF

    class CSS:
        Important = 0xFFFFFFFF
        CSS3Property = 0xFFFFFFFF
        Attribute = 0xFFFFFFFF
        Comment = 0xFFFFFFFF
        SingleQuotedString = 0xFFFFFFFF
        MediaRule = 0xFFFFFFFF
        AtRule = 0xFFFFFFFF
        UnknownPseudoClass = 0xFFFFFFFF
        PseudoClass = 0xFFFFFFFF
        Tag = 0xFFFFFFFF
        CSS2Property = 0xFFFFFFFF
        CSS1Property = 0xFFFFFFFF
        IDSelector = 0xFFFFFFFF
        ExtendedCSSProperty = 0xFFFFFFFF
        Variable = 0xFFFFFFFF
        ExtendedPseudoClass = 0xFFFFFFFF
        ClassSelector = 0xFFFFFFFF
        Default = 0xFFFFFFFF
        PseudoElement = 0xFFFFFFFF
        UnknownProperty = 0xFFFFFFFF
        Value = 0xFFFFFFFF
        ExtendedPseudoElement = 0xFFFFFFFF
        DoubleQuotedString = 0xFFFFFFFF
        Operator = 0xFFFFFFFF

    class CSharp:
        CommentDocKeywordError = 0xFFFFFFFF
        InactiveRegex = 0xFFFFFFFF
        InactivePreProcessorComment = 0xFFFFFFFF
        UUID = 0xFFFFFFFF
        InactiveVerbatimString = 0xFFFFFFFF
        SingleQuotedString = 0xFFFFFFFF
        Operator = 0xFFFFFFFF
        InactiveOperator = 0xFFFFFFFF
        InactivePreProcessor = 0xFFFFFFFF
        UnclosedString = 0xFFFFFFFF
        Identifier = 0xFFFFFFFF
        InactiveRawString = 0xFFFFFFFF
        PreProcessor = 0xFFFFFFFF
        KeywordSet2 = 0xFFFFFFFF
        InactiveUnclosedString = 0xFFFFFFFF
        InactiveCommentLine = 0xFFFFFFFF
        InactiveNumber = 0xFFFFFFFF
        InactivePreProcessorCommentLineDoc = 0xFFFFFFFF
        Number = 0xFFFFFFFF
        InactiveUUID = 0xFFFFFFFF
        CommentDoc = 0xFFFFFFFF
        InactiveCommentDoc = 0xFFFFFFFF
        GlobalClass = 0xFFFFFFFF
        InactiveSingleQuotedString = 0xFFFFFFFF
        HashQuotedString = 0xFFFFFFFF
        VerbatimString = 0xFFE0FFE0
        InactiveHashQuotedString = 0xFFFFFFFF
        Regex = 0xFFFFFFFF
        InactiveGlobalClass = 0xFFFFFFFF
        InactiveIdentifier = 0xFFFFFFFF
        CommentLineDoc = 0xFFFFFFFF
        TripleQuotedVerbatimString = 0xFFFFFFFF
        InactiveKeywordSet2 = 0xFFFFFFFF
        InactiveCommentDocKeyword = 0xFFFFFFFF
        Keyword = 0xFFFFFFFF
        InactiveCommentLineDoc = 0xFFFFFFFF
        InactiveDefault = 0xFFFFFFFF
        InactiveCommentDocKeywordError = 0xFFFFFFFF
        InactiveTripleQuotedVerbatimString = 0xFFFFFFFF
        CommentDocKeyword = 0xFFFFFFFF
        InactiveDoubleQuotedString = 0xFFFFFFFF
        CommentLine = 0xFFFFFFFF
        Comment = 0xFFFFFFFF
        PreProcessorComment = 0xFFFFFFFF
        InactiveComment = 0xFFFFFFFF
        RawString = 0xFFFFFFFF
        Default = 0xFFFFFFFF
        PreProcessorCommentLineDoc = 0xFFFFFFFF
        DoubleQuotedString = 0xFFFFFFFF
        InactiveKeyword = 0xFFFFFFFF
        UserLiteral = 0xFFFFFFFF
        InactiveEscapeSequence = 0xFFFFFFFF
        EscapeSequence = 0xFFFFFFFF
        InactiveUserLiteral = 0xFFFFFFFF
        InactiveTaskMarker = 0xFFFFFFFF
        TaskMarker = 0xFFFFFFFF

    class CoffeeScript:
        UUID = 0xFFFFFFFF
        CommentDocKeywordError = 0xFFFFFFFF
        GlobalClass = 0xFFFFFFFF
        VerbatimString = 0xFFE0FFE0
        SingleQuotedString = 0xFFFFFFFF
        Operator = 0xFFFFFFFF
        Number = 0xFFFFFFFF
        Identifier = 0xFFFFFFFF
        Keyword = 0xFFFFFFFF
        UnclosedString = 0xFFE0C0E0
        Regex = 0xFFE0F0E0
        CommentDocKeyword = 0xFFFFFFFF
        BlockRegex = 0xFFFFFFFF
        CommentLineDoc = 0xFFFFFFFF
        PreProcessor = 0xFFFFFFFF
        CommentLine = 0xFFFFFFFF
        CommentBlock = 0xFFFFFFFF
        Comment = 0xFFFFFFFF
        KeywordSet2 = 0xFFFFFFFF
        BlockRegexComment = 0xFFFFFFFF
        Default = 0xFFFFFFFF
        DoubleQuotedString = 0xFFFFFFFF
        CommentDoc = 0xFFFFFFFF

    class D:
        BackquoteString = 0xFFFFFFFF
        CommentDocKeywordError = 0xFFFFFFFF
        Operator = 0xFFFFFFFF
        CommentNested = 0xFFFFFFFF
        KeywordDoc = 0xFFFFFFFF
        KeywordSet7 = 0xFFFFFFFF
        Keyword = 0xFFFFFFFF
        KeywordSecondary = 0xFFFFFFFF
        Identifier = 0xFFFFFFFF
        KeywordSet5 = 0xFFFFFFFF
        CommentDocKeyword = 0xFFFFFFFF
        KeywordSet6 = 0xFFFFFFFF
        CommentLineDoc = 0xFFFFFFFF
        CommentLine = 0xFFFFFFFF
        Comment = 0xFFFFFFFF
        Typedefs = 0xFFFFFFFF
        Character = 0xFFFFFFFF
        RawString = 0xFFFFFFFF
        Default = 0xFFFFFFFF
        Number = 0xFFFFFFFF
        UnclosedString = 0xFFE0C0E0
        String = 0xFFFFFFFF
        CommentDoc = 0xFFFFFFFF

    class Diff:
        Header = 0xFFFFFFFF
        LineChanged = 0xFFFFFFFF
        Default = 0xFFFFFFFF
        LineRemoved = 0xFFFFFFFF
        Command = 0xFFFFFFFF
        Position = 0xFFFFFFFF
        LineAdded = 0xFFFFFFFF
        Comment = 0xFFFFFFFF

    class Fortran:
        Label = 0xFFFFFFFF
        Identifier = 0xFFFFFFFF
        DottedOperator = 0xFFFFFFFF
        PreProcessor = 0xFFFFFFFF
        Comment = 0xFFFFFFFF
        SingleQuotedString = 0xFFFFFFFF
        Default = 0xFFFFFFFF
        DoubleQuotedString = 0xFFFFFFFF
        ExtendedFunction = 0xFFFFFFFF
        UnclosedString = 0xFFE0C0E0
        Number = 0xFFFFFFFF
        Continuation = 0xFFF0E080
        IntrinsicFunction = 0xFFFFFFFF
        Keyword = 0xFFFFFFFF
        Operator = 0xFFFFFFFF

    class Fortran77:
        Label = 0xFFFFFFFF
        Identifier = 0xFFFFFFFF
        DottedOperator = 0xFFFFFFFF
        PreProcessor = 0xFFFFFFFF
        Comment = 0xFFFFFFFF
        SingleQuotedString = 0xFFFFFFFF
        Default = 0xFFFFFFFF
        DoubleQuotedString = 0xFFFFFFFF
        ExtendedFunction = 0xFFFFFFFF
        UnclosedString = 0xFFE0C0E0
        Number = 0xFFFFFFFF
        Continuation = 0xFFF0E080
        IntrinsicFunction = 0xFFFFFFFF
        Keyword = 0xFFFFFFFF
        Operator = 0xFFFFFFFF

    class HTML:
        HTMLValue = 0xFFFFEFFF
        PythonDefault = 0xFFEFFFEF
        Entity = 0xFFFFFFFF
        SGMLParameter = 0xFFEFEFFF
        SGMLDefault = 0xFFEFEFFF
        PHPVariable = 0xFFFFF8F8
        SGMLCommand = 0xFFEFEFFF
        PythonClassName = 0xFFEFFFEF
        VBScriptUnclosedString = 0xFF7F7FFF
        ASPJavaScriptDefault = 0xFFDFDF7F
        ASPVBScriptStart = 0xFFFFFFFF
        VBScriptDefault = 0xFFEFEFFF
        PythonNumber = 0xFFEFFFEF
        PythonOperator = 0xFFEFFFEF
        ASPJavaScriptSingleQuotedString = 0xFFDFDF7F
        PHPDefault = 0xFFFFF8F8
        XMLStart = 0xFFFFFFFF
        PythonFunctionMethodName = 0xFFEFFFEF
        ASPJavaScriptStart = 0xFFFFFFFF
        JavaScriptWord = 0xFFF0F0FF
        PHPSingleQuotedString = 0xFFFFF8F8
        PythonTripleDoubleQuotedString = 0xFFEFFFEF
        JavaScriptComment = 0xFFF0F0FF
        Default = 0xFFFFFFFF
        SGMLSingleQuotedString = 0xFFEFEFFF
        VBScriptComment = 0xFFEFEFFF
        ASPVBScriptNumber = 0xFFCFCFEF
        ASPJavaScriptCommentDoc = 0xFFDFDF7F
        PythonIdentifier = 0xFFEFFFEF
        VBScriptKeyword = 0xFFEFEFFF
        JavaScriptDefault = 0xFFF0F0FF
        PythonStart = 0xFFFFFFFF
        ASPPythonComment = 0xFFCFEFCF
        ASPJavaScriptWord = 0xFFDFDF7F
        SGMLParameterComment = 0xFFFFFFFF
        JavaScriptSingleQuotedString = 0xFFF0F0FF
        PythonSingleQuotedString = 0xFFEFFFEF
        HTMLSingleQuotedString = 0xFFFFFFFF
        ASPVBScriptString = 0xFFCFCFEF
        SGMLBlockDefault = 0xFFCCCCE0
        PythonKeyword = 0xFFEFFFEF
        XMLTagEnd = 0xFFFFFFFF
        ASPVBScriptComment = 0xFFCFCFEF
        ASPPythonSingleQuotedString = 0xFFCFEFCF
        PHPDoubleQuotedVariable = 0xFFFFF8F8
        ASPJavaScriptComment = 0xFFDFDF7F
        JavaScriptUnclosedString = 0xFFBFBBB0
        JavaScriptDoubleQuotedString = 0xFFF0F0FF
        UnknownAttribute = 0xFFFFFFFF
        ASPPythonOperator = 0xFFCFEFCF
        ASPJavaScriptSymbol = 0xFFDFDF7F
        ASPPythonFunctionMethodName = 0xFFCFEFCF
        SGMLDoubleQuotedString = 0xFFEFEFFF
        PHPOperator = 0xFFFFF8F8
        JavaScriptNumber = 0xFFF0F0FF
        PythonDoubleQuotedString = 0xFFEFFFEF
        ASPAtStart = 0xFFFFFF00
        Script = 0xFFFFFFFF
        PHPCommentLine = 0xFFFFF8F8
        SGMLComment = 0xFFEFEFFF
        JavaScriptStart = 0xFFFFFFFF
        ASPPythonIdentifier = 0xFFCFEFCF
        ASPVBScriptKeyword = 0xFFCFCFEF
        ASPPythonTripleDoubleQuotedString = 0xFFCFEFCF
        ASPPythonKeyword = 0xFFCFEFCF
        ASPJavaScriptNumber = 0xFFDFDF7F
        PHPStart = 0xFFFFEFBF
        PythonTripleSingleQuotedString = 0xFFEFFFEF
        PHPNumber = 0xFFFFF8F8
        ASPPythonDefault = 0xFFCFEFCF
        SGMLSpecial = 0xFFEFEFFF
        OtherInTag = 0xFFFFFFFF
        JavaScriptCommentDoc = 0xFFF0F0FF
        Tag = 0xFFFFFFFF
        XMLEnd = 0xFFFFFFFF
        CDATA = 0xFFFFDF00
        HTMLNumber = 0xFFFFFFFF
        SGMLError = 0xFFFF6666
        PHPKeyword = 0xFFFFF8F8
        ASPVBScriptUnclosedString = 0xFF7F7FFF
        ASPPythonNumber = 0xFFCFEFCF
        VBScriptString = 0xFFEFEFFF
        ASPPythonClassName = 0xFFCFEFCF
        ASPPythonStart = 0xFFFFFFFF
        JavaScriptRegex = 0xFFFFBBB0
        ASPJavaScriptUnclosedString = 0xFFBFBBB0
        ASPJavaScriptCommentLine = 0xFFDFDF7F
        SGMLEntity = 0xFFEFEFFF
        ASPJavaScriptDoubleQuotedString = 0xFFDFDF7F
        ASPStart = 0xFFFFDF00
        Attribute = 0xFFFFFFFF
        ASPJavaScriptKeyword = 0xFFDFDF7F
        ASPVBScriptDefault = 0xFFCFCFEF
        ASPVBScriptIdentifier = 0xFFCFCFEF
        ASPJavaScriptRegex = 0xFFFFBBB0
        VBScriptNumber = 0xFFEFEFFF
        HTMLDoubleQuotedString = 0xFFFFFFFF
        ASPXCComment = 0xFFFFFFFF
        VBScriptStart = 0xFFFFFFFF
        PHPDoubleQuotedString = 0xFFFFF8F8
        PHPComment = 0xFFFFF8F8
        ASPPythonTripleSingleQuotedString = 0xFFCFEFCF
        ASPPythonDoubleQuotedString = 0xFFCFEFCF
        JavaScriptKeyword = 0xFFF0F0FF
        JavaScriptSymbol = 0xFFF0F0FF
        VBScriptIdentifier = 0xFFEFEFFF
        HTMLComment = 0xFFFFFFFF
        UnknownTag = 0xFFFFFFFF
        JavaScriptCommentLine = 0xFFF0F0FF
        PythonComment = 0xFFEFFFEF

    class IDL:
        CommentDocKeywordError = 0xFFFFFFFF
        InactiveRegex = 0xFFE0F0E0
        InactivePreProcessorComment = 0xFFFFFFFF
        UUID = 0xFFFFFFFF
        InactiveVerbatimString = 0xFFE0FFE0
        SingleQuotedString = 0xFFFFFFFF
        Operator = 0xFFFFFFFF
        InactiveOperator = 0xFFFFFFFF
        InactivePreProcessor = 0xFFFFFFFF
        UnclosedString = 0xFFE0C0E0
        Identifier = 0xFFFFFFFF
        InactiveRawString = 0xFFFFFFFF
        PreProcessor = 0xFFFFFFFF
        KeywordSet2 = 0xFFFFFFFF
        InactiveUnclosedString = 0xFFE0C0E0
        InactiveCommentLine = 0xFFFFFFFF
        InactiveNumber = 0xFFFFFFFF
        InactivePreProcessorCommentLineDoc = 0xFFFFFFFF
        Number = 0xFFFFFFFF
        InactiveUUID = 0xFFFFFFFF
        CommentDoc = 0xFFFFFFFF
        InactiveCommentDoc = 0xFFFFFFFF
        GlobalClass = 0xFFFFFFFF
        InactiveSingleQuotedString = 0xFFFFFFFF
        HashQuotedString = 0xFFE7FFD7
        VerbatimString = 0xFFE0FFE0
        InactiveHashQuotedString = 0xFFFFFFFF
        Regex = 0xFFE0F0E0
        InactiveGlobalClass = 0xFFFFFFFF
        InactiveIdentifier = 0xFFFFFFFF
        CommentLineDoc = 0xFFFFFFFF
        TripleQuotedVerbatimString = 0xFFE0FFE0
        InactiveKeywordSet2 = 0xFFFFFFFF
        InactiveCommentDocKeyword = 0xFFFFFFFF
        Keyword = 0xFFFFFFFF
        InactiveCommentLineDoc = 0xFFFFFFFF
        InactiveDefault = 0xFFFFFFFF
        InactiveCommentDocKeywordError = 0xFFFFFFFF
        InactiveTripleQuotedVerbatimString = 0xFFFFFFFF
        CommentDocKeyword = 0xFFFFFFFF
        InactiveDoubleQuotedString = 0xFFFFFFFF
        CommentLine = 0xFFFFFFFF
        Comment = 0xFFFFFFFF
        PreProcessorComment = 0xFFFFFFFF
        InactiveComment = 0xFFFFFFFF
        RawString = 0xFFFFF3FF
        Default = 0xFFFFFFFF
        PreProcessorCommentLineDoc = 0xFFFFFFFF
        DoubleQuotedString = 0xFFFFFFFF
        InactiveKeyword = 0xFFFFFFFF
        UserLiteral = 0xFFFFFFFF
        InactiveEscapeSequence = 0xFFFFFFFF
        EscapeSequence = 0xFFFFFFFF
        InactiveUserLiteral = 0xFFFFFFFF
        InactiveTaskMarker = 0xFFFFFFFF
        TaskMarker = 0xFFFFFFFF

    class Java:
        CommentDocKeywordError = 0xFFFFFFFF
        InactiveRegex = 0xFFE0F0E0
        InactivePreProcessorComment = 0xFFFFFFFF
        UUID = 0xFFFFFFFF
        InactiveVerbatimString = 0xFFE0FFE0
        SingleQuotedString = 0xFFFFFFFF
        Operator = 0xFFFFFFFF
        InactiveOperator = 0xFFFFFFFF
        InactivePreProcessor = 0xFFFFFFFF
        UnclosedString = 0xFFE0C0E0
        Identifier = 0xFFFFFFFF
        InactiveRawString = 0xFFFFFFFF
        PreProcessor = 0xFFFFFFFF
        KeywordSet2 = 0xFFFFFFFF
        InactiveUnclosedString = 0xFFE0C0E0
        InactiveCommentLine = 0xFFFFFFFF
        InactiveNumber = 0xFFFFFFFF
        InactivePreProcessorCommentLineDoc = 0xFFFFFFFF
        Number = 0xFFFFFFFF
        InactiveUUID = 0xFFFFFFFF
        CommentDoc = 0xFFFFFFFF
        InactiveCommentDoc = 0xFFFFFFFF
        GlobalClass = 0xFFFFFFFF
        InactiveSingleQuotedString = 0xFFFFFFFF
        HashQuotedString = 0xFFE7FFD7
        VerbatimString = 0xFFE0FFE0
        InactiveHashQuotedString = 0xFFFFFFFF
        Regex = 0xFFE0F0E0
        InactiveGlobalClass = 0xFFFFFFFF
        InactiveIdentifier = 0xFFFFFFFF
        CommentLineDoc = 0xFFFFFFFF
        TripleQuotedVerbatimString = 0xFFE0FFE0
        InactiveKeywordSet2 = 0xFFFFFFFF
        InactiveCommentDocKeyword = 0xFFFFFFFF
        Keyword = 0xFFFFFFFF
        InactiveCommentLineDoc = 0xFFFFFFFF
        InactiveDefault = 0xFFFFFFFF
        InactiveCommentDocKeywordError = 0xFFFFFFFF
        InactiveTripleQuotedVerbatimString = 0xFFFFFFFF
        CommentDocKeyword = 0xFFFFFFFF
        InactiveDoubleQuotedString = 0xFFFFFFFF
        CommentLine = 0xFFFFFFFF
        Comment = 0xFFFFFFFF
        PreProcessorComment = 0xFFFFFFFF
        InactiveComment = 0xFFFFFFFF
        RawString = 0xFFFFF3FF
        Default = 0xFFFFFFFF
        PreProcessorCommentLineDoc = 0xFFFFFFFF
        DoubleQuotedString = 0xFFFFFFFF
        InactiveKeyword = 0xFFFFFFFF
        UserLiteral = 0xFFFFFFFF
        InactiveEscapeSequence = 0xFFFFFFFF
        EscapeSequence = 0xFFFFFFFF
        InactiveUserLiteral = 0xFFFFFFFF
        InactiveTaskMarker = 0xFFFFFFFF
        TaskMarker = 0xFFFFFFFF

    class JavaScript:
        CommentDocKeywordError = 0xFFFFFFFF
        InactiveRegex = 0xFFFFFFFF
        InactivePreProcessorComment = 0xFFFFFFFF
        UUID = 0xFFFFFFFF
        InactiveVerbatimString = 0xFFFFFFFF
        SingleQuotedString = 0xFFFFFFFF
        Operator = 0xFFFFFFFF
        InactiveOperator = 0xFFFFFFFF
        InactivePreProcessor = 0xFFFFFFFF
        UnclosedString = 0xFFFFFFFF
        Identifier = 0xFFFFFFFF
        InactiveRawString = 0xFFFFFFFF
        PreProcessor = 0xFFFFFFFF
        KeywordSet2 = 0xFFFFFFFF
        InactiveUnclosedString = 0xFFFFFFFF
        InactiveCommentLine = 0xFFFFFFFF
        InactiveNumber = 0xFFFFFFFF
        InactivePreProcessorCommentLineDoc = 0xFFFFFFFF
        Number = 0xFFFFFFFF
        InactiveUUID = 0xFFFFFFFF
        CommentDoc = 0xFFFFFFFF
        InactiveCommentDoc = 0xFFFFFFFF
        GlobalClass = 0xFFFFFFFF
        InactiveSingleQuotedString = 0xFFFFFFFF
        HashQuotedString = 0xFFFFFFFF
        VerbatimString = 0xFFFFFFFF
        InactiveHashQuotedString = 0xFFFFFFFF
        Regex = 0xFFE0F0FF
        InactiveGlobalClass = 0xFFFFFFFF
        InactiveIdentifier = 0xFFFFFFFF
        CommentLineDoc = 0xFFFFFFFF
        TripleQuotedVerbatimString = 0xFFFFFFFF
        InactiveKeywordSet2 = 0xFFFFFFFF
        InactiveCommentDocKeyword = 0xFFFFFFFF
        Keyword = 0xFFFFFFFF
        InactiveCommentLineDoc = 0xFFFFFFFF
        InactiveDefault = 0xFFFFFFFF
        InactiveCommentDocKeywordError = 0xFFFFFFFF
        InactiveTripleQuotedVerbatimString = 0xFFFFFFFF
        CommentDocKeyword = 0xFFFFFFFF
        InactiveDoubleQuotedString = 0xFFFFFFFF
        CommentLine = 0xFFFFFFFF
        Comment = 0xFFFFFFFF
        PreProcessorComment = 0xFFFFFFFF
        InactiveComment = 0xFFFFFFFF
        RawString = 0xFFFFFFFF
        Default = 0xFFFFFFFF
        PreProcessorCommentLineDoc = 0xFFFFFFFF
        DoubleQuotedString = 0xFFFFFFFF
        InactiveKeyword = 0xFFFFFFFF
        UserLiteral = 0xFFFFFFFF
        InactiveEscapeSequence = 0xFFFFFFFF
        EscapeSequence = 0xFFFFFFFF
        InactiveUserLiteral = 0xFFFFFFFF
        InactiveTaskMarker = 0xFFFFFFFF
        TaskMarker = 0xFFFFFFFF

    class Lua:
        Label = 0xFFFFFFFF
        Identifier = 0xFFFFFFFF
        StringTableMathsFunctions = 0xFFD0D0FF
        CoroutinesIOSystemFacilities = 0xFFFFD0D0
        KeywordSet5 = 0xFFFFFFFF
        KeywordSet6 = 0xFFFFFFFF
        Preprocessor = 0xFFFFFFFF
        LineComment = 0xFFFFFFFF
        Comment = 0xFFD0F0F0
        String = 0xFFFFFFFF
        Character = 0xFFFFFFFF
        Default = 0xFFFFFFFF
        Operator = 0xFFFFFFFF
        LiteralString = 0xFFE0FFFF
        Number = 0xFFFFFFFF
        KeywordSet8 = 0xFFFFFFFF
        KeywordSet7 = 0xFFFFFFFF
        BasicFunctions = 0xFFD0FFD0
        Keyword = 0xFFFFFFFF
        UnclosedString = 0xFFE0C0E0

    class Makefile:
        Default = 0xFFFFFFFF
        Operator = 0xFFFFFFFF
        Target = 0xFFFFFFFF
        Preprocessor = 0xFFFFFFFF
        Variable = 0xFFFFFFFF
        Comment = 0xFFFFFFFF
        Error = 0xFFFF0000

    class Matlab:
        SingleQuotedString = 0xFFFFFFFF
        Default = 0xFFFFFFFF
        Keyword = 0xFFFFFFFF
        Number = 0xFFFFFFFF
        Command = 0xFFFFFFFF
        Identifier = 0xFFFFFFFF
        Comment = 0xFFFFFFFF
        DoubleQuotedString = 0xFFFFFFFF
        Operator = 0xFFFFFFFF

    class Octave:
        SingleQuotedString = 0xFFFFFFFF
        Default = 0xFFFFFFFF
        Keyword = 0xFFFFFFFF
        Number = 0xFFFFFFFF
        Command = 0xFFFFFFFF
        Identifier = 0xFFFFFFFF
        Comment = 0xFFFFFFFF
        DoubleQuotedString = 0xFFFFFFFF
        Operator = 0xFFFFFFFF

    class PO:
        ProgrammerComment = 0xFFFFFFFF
        Flags = 0xFFFFFFFF
        MessageContextText = 0xFFFFFFFF
        MessageStringTextEOL = 0xFFFFFFFF
        MessageId = 0xFFFFFFFF
        MessageIdText = 0xFFFFFFFF
        Reference = 0xFFFFFFFF
        Comment = 0xFFFFFFFF
        MessageStringText = 0xFFFFFFFF
        MessageContext = 0xFFFFFFFF
        Fuzzy = 0xFFFFFFFF
        Default = 0xFFFFFFFF
        MessageString = 0xFFFFFFFF
        MessageContextTextEOL = 0xFFFFFFFF
        MessageIdTextEOL = 0xFFFFFFFF

    class POV:
        KeywordSet7 = 0xFFD0D0D0
        KeywordSet6 = 0xFFD0FFD0
        PredefinedFunctions = 0xFFD0D0FF
        CommentLine = 0xFFFFFFFF
        PredefinedIdentifiers = 0xFFFFFFFF
        Comment = 0xFFFFFFFF
        Directive = 0xFFFFFFFF
        String = 0xFFFFFFFF
        BadDirective = 0xFFFFFFFF
        TypesModifiersItems = 0xFFFFFFD0
        Default = 0xFFFFFFFF
        Operator = 0xFFFFFFFF
        Number = 0xFFFFFFFF
        KeywordSet8 = 0xFFE0E0E0
        Identifier = 0xFFFFFFFF
        ObjectsCSGAppearance = 0xFFFFD0D0
        UnclosedString = 0xFFE0C0E0

    class Pascal:
        PreProcessorParenthesis = 0xFFFFFFFF
        SingleQuotedString = 0xFFFFFFFF
        PreProcessor = 0xFFFFFFFF
        CommentLine = 0xFFFFFFFF
        Comment = 0xFFFFFFFF
        CommentParenthesis = 0xFFFFFFFF
        Asm = 0xFFFFFFFF
        Character = 0xFFFFFFFF
        Default = 0xFFFFFFFF
        Operator = 0xFFFFFFFF
        UnclosedString = 0xFFE0C0E0
        Number = 0xFFFFFFFF
        Identifier = 0xFFFFFFFF
        Keyword = 0xFFFFFFFF
        HexNumber = 0xFFFFFFFF

    class Perl:
        Translation = 0xFFF0E080
        BacktickHereDocument = 0xFFDDD0DD
        Array = 0xFFFFFFE0
        QuotedStringQXVar = 0xFFA08080
        PODVerbatim = 0xFFC0FFC0
        DoubleQuotedStringVar = 0xFFFFFFFF
        Regex = 0xFFA0FFA0
        HereDocumentDelimiter = 0xFFDDD0DD
        SubroutinePrototype = 0xFFFFFFFF
        BacktickHereDocumentVar = 0xFFDDD0DD
        QuotedStringQR = 0xFFFFFFFF
        SingleQuotedString = 0xFFFFFFFF
        QuotedStringQRVar = 0xFFFFFFFF
        SubstitutionVar = 0xFFFFFFFF
        Operator = 0xFFFFFFFF
        DoubleQuotedHereDocumentVar = 0xFFDDD0DD
        Identifier = 0xFFFFFFFF
        QuotedStringQX = 0xFFFFFFFF
        BackticksVar = 0xFFA08080
        Keyword = 0xFFFFFFFF
        QuotedStringQ = 0xFFFFFFFF
        QuotedStringQQVar = 0xFFFFFFFF
        QuotedStringQQ = 0xFFFFFFFF
        POD = 0xFFE0FFE0
        FormatIdentifier = 0xFFFFFFFF
        RegexVar = 0xFFFFFFFF
        Backticks = 0xFFA08080
        DoubleQuotedHereDocument = 0xFFDDD0DD
        Scalar = 0xFFFFE0E0
        FormatBody = 0xFFFFF0FF
        Comment = 0xFFFFFFFF
        QuotedStringQW = 0xFFFFFFFF
        SymbolTable = 0xFFE0E0E0
        Default = 0xFFFFFFFF
        Error = 0xFFFF0000
        SingleQuotedHereDocument = 0xFFDDD0DD
        Number = 0xFFFFFFFF
        Hash = 0xFFFFE0FF
        Substitution = 0xFFF0E080
        DataSection = 0xFFFFF0D8
        DoubleQuotedString = 0xFFFFFFFF

    class PostScript:
        DictionaryParenthesis = 0xFFFFFFFF
        HexString = 0xFFFFFFFF
        DSCCommentValue = 0xFFFFFFFF
        ProcedureParenthesis = 0xFFFFFFFF
        Comment = 0xFFFFFFFF
        ImmediateEvalLiteral = 0xFFFFFFFF
        Name = 0xFFFFFFFF
        DSCComment = 0xFFFFFFFF
        Default = 0xFFFFFFFF
        Base85String = 0xFFFFFFFF
        Number = 0xFFFFFFFF
        ArrayParenthesis = 0xFFFFFFFF
        Literal = 0xFFFFFFFF
        BadStringCharacter = 0xFFFF0000
        Text = 0xFFFFFFFF
        Keyword = 0xFFFFFFFF

    class Properties:
        DefaultValue = 0xFFFFFFFF
        Default = 0xFFFFFFFF
        Section = 0xFFE0F0F0
        Assignment = 0xFFFFFFFF
        Key = 0xFFFFFFFF
        Comment = 0xFFFFFFFF

    class Python:
        TripleDoubleQuotedString = 0xFFFFFFFF
        FunctionMethodName = 0xFFFFFFFF
        TabsAfterSpaces = 0xFFFFFFFF
        Tabs = 0xFFFFFFFF
        Decorator = 0xFFFFFFFF
        NoWarning = 0xFFFFFFFF
        UnclosedString = 0xFFE0C0E0
        Spaces = 0xFFFFFFFF
        CommentBlock = 0xFFFFFFFF
        Comment = 0xFFFFFFFF
        TripleSingleQuotedString = 0xFFFFFFFF
        SingleQuotedString = 0xFFFFFFFF
        Inconsistent = 0xFFFFFFFF
        Default = 0xFFFFFFFF
        DoubleQuotedString = 0xFFFFFFFF
        Operator = 0xFFFFFFFF
        Number = 0xFFFFFFFF
        Identifier = 0xFFFFFFFF
        ClassName = 0xFFFFFFFF
        Keyword = 0xFFFFFFFF
        HighlightedIdentifier = 0xFFFFFFFF
        CustomKeyword = 0xFFFFFFFF

    class Ruby:
        Symbol = 0xFFFFFFFF
        Stderr = 0xFFFF8080
        Global = 0xFFFFFFFF
        FunctionMethodName = 0xFFFFFFFF
        Stdin = 0xFFFF8080
        HereDocumentDelimiter = 0xFFDDD0DD
        PercentStringr = 0xFFA0FFA0
        PercentStringQ = 0xFFFFFFFF
        ModuleName = 0xFFFFFFFF
        HereDocument = 0xFFDDD0DD
        SingleQuotedString = 0xFFFFFFFF
        PercentStringq = 0xFFFFFFFF
        Regex = 0xFFA0FFA0
        Operator = 0xFFFFFFFF
        PercentStringw = 0xFFFFFFE0
        PercentStringx = 0xFFA08080
        POD = 0xFFC0FFC0
        Keyword = 0xFFFFFFFF
        Stdout = 0xFFFF8080
        ClassVariable = 0xFFFFFFFF
        Identifier = 0xFFFFFFFF
        DemotedKeyword = 0xFFFFFFFF
        Backticks = 0xFFA08080
        InstanceVariable = 0xFFFFFFFF
        Comment = 0xFFFFFFFF
        Default = 0xFFFFFFFF
        Error = 0xFFFF0000
        Number = 0xFFFFFFFF
        DataSection = 0xFFFFF0D8
        ClassName = 0xFFFFFFFF
        DoubleQuotedString = 0xFFFFFFFF

    class SQL:
        PlusComment = 0xFFFFFFFF
        KeywordSet7 = 0xFFFFFFFF
        PlusPrompt = 0xFFE0FFE0
        CommentDocKeywordError = 0xFFFFFFFF
        CommentDocKeyword = 0xFFFFFFFF
        KeywordSet6 = 0xFFFFFFFF
        CommentLine = 0xFFFFFFFF
        Comment = 0xFFFFFFFF
        Operator = 0xFFFFFFFF
        QuotedIdentifier = 0xFFFFFFFF
        SingleQuotedString = 0xFFFFFFFF
        PlusKeyword = 0xFFFFFFFF
        Default = 0xFFFFFFFF
        DoubleQuotedString = 0xFFFFFFFF
        CommentLineHash = 0xFFFFFFFF
        KeywordSet5 = 0xFFFFFFFF
        Number = 0xFFFFFFFF
        KeywordSet8 = 0xFFFFFFFF
        Identifier = 0xFFFFFFFF
        Keyword = 0xFFFFFFFF
        CommentDoc = 0xFFFFFFFF
        QuotedOperator = 0xFFFFFFFF

    class Spice:
        Function = 0xFFFFFFFF
        Delimiter = 0xFFFFFFFF
        Value = 0xFFFFFFFF
        Default = 0xFFFFFFFF
        Number = 0xFFFFFFFF
        Parameter = 0xFFFFFFFF
        Command = 0xFFFFFFFF
        Identifier = 0xFFFFFFFF
        Comment = 0xFFFFFFFF

    class TCL:
        SubstitutionBrace = 0xFFFFFFFF
        CommentBox = 0xFFF0FFF0
        ITCLKeyword = 0xFFFFF0F0
        TkKeyword = 0xFFE0FFF0
        Operator = 0xFFFFFFFF
        QuotedString = 0xFFFFF0F0
        ExpandKeyword = 0xFFFFFF80
        KeywordSet7 = 0xFFFFFFFF
        TCLKeyword = 0xFFFFFFFF
        TkCommand = 0xFFFFD0D0
        Identifier = 0xFFFFFFFF
        KeywordSet6 = 0xFFFFFFFF
        CommentLine = 0xFFFFFFFF
        CommentBlock = 0xFFF0FFF0
        Comment = 0xFFF0FFE0
        Default = 0xFFFFFFFF
        KeywordSet9 = 0xFFFFFFFF
        Modifier = 0xFFFFFFFF
        Number = 0xFFFFFFFF
        KeywordSet8 = 0xFFFFFFFF
        Substitution = 0xFFEFFFF0
        QuotedKeyword = 0xFFFFF0F0

    class TeX:
        Symbol = 0xFFFFFFFF
        Default = 0xFFFFFFFF
        Command = 0xFFFFFFFF
        Group = 0xFFFFFFFF
        Text = 0xFFFFFFFF
        Special = 0xFFFFFFFF

    class VHDL:
        StandardOperator = 0xFFFFFFFF
        Attribute = 0xFFFFFFFF
        CommentLine = 0xFFFFFFFF
        Comment = 0xFFFFFFFF
        String = 0xFFFFFFFF
        Default = 0xFFFFFFFF
        Operator = 0xFFFFFFFF
        StandardPackage = 0xFFFFFFFF
        Number = 0xFFFFFFFF
        Identifier = 0xFFFFFFFF
        KeywordSet7 = 0xFFFFFFFF
        StandardFunction = 0xFFFFFFFF
        StandardType = 0xFFFFFFFF
        Keyword = 0xFFFFFFFF
        UnclosedString = 0xFFE0C0E0
        CommentBlock = 0xFFFFFFFF

    class Verilog:
        CommentBang = 0xFFE0F0FF
        UserKeywordSet = 0xFFFFFFFF
        Preprocessor = 0xFFFFFFFF
        CommentLine = 0xFFFFFFFF
        Comment = 0xFFFFFFFF
        KeywordSet2 = 0xFFFFFFFF
        Default = 0xFFFFFFFF
        Operator = 0xFFFFFFFF
        Number = 0xFFFFFFFF
        Identifier = 0xFFFFFFFF
        SystemTask = 0xFFFFFFFF
        String = 0xFFFFFFFF
        Keyword = 0xFFFFFFFF
        UnclosedString = 0xFFE0C0E0
        InactiveDefault = 0xFFFFFFFF
        InactiveUnclosedString = 0xFFFFFFFF
        InactiveCommentKeyword = 0xFFFFFFFF
        InactiveKeywordSet2 = 0xFFFFFFFF
        InactiveComment = 0xFFFFFFFF
        DeclareInputOutputPort = 0xFFFFFFFF
        InactiveString = 0xFFFFFFFF
        CommentKeyword = 0xFFFFFFFF
        DeclareOutputPort = 0xFFFFFFFF
        PortConnection = 0xFFFFFFFF
        InactiveKeyword = 0xFFFFFFFF
        DeclareInputPort = 0xFFFFFFFF
        InactiveDeclareInputPort = 0xFFFFFFFF
        InactiveDeclareOutputPort = 0xFFFFFFFF
        InactiveUserKeywordSet = 0xFFFFFFFF
        InactiveCommentBang = 0xFFFFFFFF
        InactiveIdentifier = 0xFFFFFFFF
        InactivePortConnection = 0xFFFFFFFF
        InactiveNumber = 0xFFFFFFFF
        InactiveSystemTask = 0xFFFFFFFF
        InactivePreprocessor = 0xFFFFFFFF
        InactiveOperator = 0xFFFFFFFF
        InactiveDeclareInputOutputPort = 0xFFFFFFFF
        InactiveCommentLine = 0xFFFFFFFF

    class XML:
        HTMLValue = 0xFFFFEFFF
        PythonDefault = 0xFFEFFFEF
        Entity = 0xFFFFFFFF
        SGMLParameter = 0xFFEFEFFF
        SGMLDefault = 0xFFEFEFFF
        PHPVariable = 0xFFFFF8F8
        SGMLCommand = 0xFFEFEFFF
        PythonClassName = 0xFFEFFFEF
        VBScriptUnclosedString = 0xFF7F7FFF
        ASPJavaScriptDefault = 0xFFDFDF7F
        ASPVBScriptStart = 0xFFFFFFFF
        VBScriptDefault = 0xFFEFEFFF
        PythonNumber = 0xFFEFFFEF
        PythonOperator = 0xFFEFFFEF
        ASPJavaScriptSingleQuotedString = 0xFFDFDF7F
        PHPDefault = 0xFFFFF8F8
        XMLStart = 0xFFFFFFFF
        PythonFunctionMethodName = 0xFFEFFFEF
        ASPJavaScriptStart = 0xFFFFFFFF
        JavaScriptWord = 0xFFF0F0FF
        PHPSingleQuotedString = 0xFFFFF8F8
        PythonTripleDoubleQuotedString = 0xFFEFFFEF
        JavaScriptComment = 0xFFF0F0FF
        Default = 0xFFFFFFFF
        SGMLSingleQuotedString = 0xFFEFEFFF
        VBScriptComment = 0xFFEFEFFF
        ASPVBScriptNumber = 0xFFCFCFEF
        ASPJavaScriptCommentDoc = 0xFFDFDF7F
        PythonIdentifier = 0xFFEFFFEF
        VBScriptKeyword = 0xFFEFEFFF
        JavaScriptDefault = 0xFFF0F0FF
        PythonStart = 0xFFFFFFFF
        ASPPythonComment = 0xFFCFEFCF
        ASPJavaScriptWord = 0xFFDFDF7F
        SGMLParameterComment = 0xFFFFFFFF
        JavaScriptSingleQuotedString = 0xFFF0F0FF
        PythonSingleQuotedString = 0xFFEFFFEF
        HTMLSingleQuotedString = 0xFFFFFFFF
        ASPVBScriptString = 0xFFCFCFEF
        SGMLBlockDefault = 0xFFCCCCE0
        PythonKeyword = 0xFFEFFFEF
        XMLTagEnd = 0xFFFFFFFF
        ASPVBScriptComment = 0xFFCFCFEF
        ASPPythonSingleQuotedString = 0xFFCFEFCF
        PHPDoubleQuotedVariable = 0xFFFFF8F8
        ASPJavaScriptComment = 0xFFDFDF7F
        JavaScriptUnclosedString = 0xFFBFBBB0
        JavaScriptDoubleQuotedString = 0xFFF0F0FF
        UnknownAttribute = 0xFFFFFFFF
        ASPPythonOperator = 0xFFCFEFCF
        ASPJavaScriptSymbol = 0xFFDFDF7F
        ASPPythonFunctionMethodName = 0xFFCFEFCF
        SGMLDoubleQuotedString = 0xFFEFEFFF
        PHPOperator = 0xFFFFF8F8
        JavaScriptNumber = 0xFFF0F0FF
        PythonDoubleQuotedString = 0xFFEFFFEF
        ASPAtStart = 0xFFFFFF00
        Script = 0xFFFFFFFF
        PHPCommentLine = 0xFFFFF8F8
        SGMLComment = 0xFFEFEFFF
        JavaScriptStart = 0xFFFFFFFF
        ASPPythonIdentifier = 0xFFCFEFCF
        ASPVBScriptKeyword = 0xFFCFCFEF
        ASPPythonTripleDoubleQuotedString = 0xFFCFEFCF
        ASPPythonKeyword = 0xFFCFEFCF
        ASPJavaScriptNumber = 0xFFDFDF7F
        PHPStart = 0xFFFFEFBF
        PythonTripleSingleQuotedString = 0xFFEFFFEF
        PHPNumber = 0xFFFFF8F8
        ASPPythonDefault = 0xFFCFEFCF
        SGMLSpecial = 0xFFEFEFFF
        OtherInTag = 0xFFFFFFFF
        JavaScriptCommentDoc = 0xFFF0F0FF
        Tag = 0xFFFFFFFF
        XMLEnd = 0xFFFFFFFF
        CDATA = 0xFFFFF0F0
        HTMLNumber = 0xFFFFFFFF
        SGMLError = 0xFFFF6666
        PHPKeyword = 0xFFFFF8F8
        ASPVBScriptUnclosedString = 0xFF7F7FFF
        ASPPythonNumber = 0xFFCFEFCF
        VBScriptString = 0xFFEFEFFF
        ASPPythonClassName = 0xFFCFEFCF
        ASPPythonStart = 0xFFFFFFFF
        JavaScriptRegex = 0xFFFFBBB0
        ASPJavaScriptUnclosedString = 0xFFBFBBB0
        ASPJavaScriptCommentLine = 0xFFDFDF7F
        SGMLEntity = 0xFFEFEFFF
        ASPJavaScriptDoubleQuotedString = 0xFFDFDF7F
        ASPStart = 0xFFFFDF00
        Attribute = 0xFFFFFFFF
        ASPJavaScriptKeyword = 0xFFDFDF7F
        ASPVBScriptDefault = 0xFFCFCFEF
        ASPVBScriptIdentifier = 0xFFCFCFEF
        ASPJavaScriptRegex = 0xFFFFBBB0
        VBScriptNumber = 0xFFEFEFFF
        HTMLDoubleQuotedString = 0xFFFFFFFF
        ASPXCComment = 0xFFFFFFFF
        VBScriptStart = 0xFFFFFFFF
        PHPDoubleQuotedString = 0xFFFFF8F8
        PHPComment = 0xFFFFF8F8
        ASPPythonTripleSingleQuotedString = 0xFFCFEFCF
        ASPPythonDoubleQuotedString = 0xFFCFEFCF
        JavaScriptKeyword = 0xFFF0F0FF
        JavaScriptSymbol = 0xFFF0F0FF
        VBScriptIdentifier = 0xFFEFEFFF
        HTMLComment = 0xFFFFFFFF
        UnknownTag = 0xFFFFFFFF
        JavaScriptCommentLine = 0xFFF0F0FF
        PythonComment = 0xFFEFFFEF

    class YAML:
        TextBlockMarker = 0xFFFFFFFF
        DocumentDelimiter = 0xFF000088
        Operator = 0xFFFFFFFF
        Number = 0xFFFFFFFF
        Default = 0xFFFFFFFF
        Identifier = 0xFFFFFFFF
        Reference = 0xFFFFFFFF
        Comment = 0xFFFFFFFF
        Keyword = 0xFFFFFFFF
        SyntaxErrorMarker = 0xFFFF0000
