
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
Context_Menu_Background = data.QColor(0xf0, 0xf0, 0xf0)
Cursor = data.QColor(0x00, 0x00, 0x00)
Cursor_Line_Background = data.QColor(0x72, 0x9f, 0xcf, 80)
Settings_Background = data.QColor(0xffffffff)
Settings_Label_Background = data.QColor(0xffffffff)
Settings_Hex_Edge = data.QColor(159,189,214)
Settings_Hex_Background = data.QColor(0xff, 0xff, 0xff)
YesNoDialog_Edge = data.QColor(159,189,214)
YesNoDialog_Background = data.QColor(0xff, 0xff, 0xff)

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
    BackGround = data.QColor(0xe0e0e0)


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
    Indicator_Unique_1_Color = data.QColor(0x72, 0x9f, 0xcf, 80)
    Indicator_Unique_2_Color = data.QColor(0xad, 0x7f, 0xa8, 80)
    Indicator_Similar_Color = data.QColor(0x8a, 0xe2, 0x34, 80)


class Font:
    Default = data.QColor(0xff000000)
    DefaultHtml = "#000000"
    
    class Repl:
        """
        THE MESSAGE COLORS ARE: 0xBBGGRR (BB-blue,GG-green,RR-red)
        """
        Error = 0x0000ff
        Warning = 0xff0000
        Success = 0x007f00
        Diff_Unique_1 = 0xcf9f72
        Diff_Unique_2 = 0xa87fad
        Diff_Similar = 0x069a4e
    
    class Ada:
        Default = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Comment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        Keyword = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        String = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        Procedure = (data.current_editor_font_name, 0xff0000ff, data.current_editor_font_size, None)
        Number = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        Type = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        Package = (data.current_editor_font_name, 0xff7f0000, data.current_editor_font_size, None)
    
    class AWK:
        Default = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Comment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        Keyword = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, True)
        BuiltInVariable = (data.current_editor_font_name, 0xffc07f40, data.current_editor_font_size, None)
        BuiltInFunction = (data.current_editor_font_name, 0xff407fc0, data.current_editor_font_size, True)
        String = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        Number = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        Operator = (data.current_editor_font_name, 0xff7f7f7f, data.current_editor_font_size, None)
    
    class CiCode:
        Default = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Comment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        MultilineComment = (data.current_editor_font_name, 0xff006f00, data.current_editor_font_size, None)
        Keyword = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, True)
        BuiltInFunction = (data.current_editor_font_name, 0xff407fc0, data.current_editor_font_size, True)
        String = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        Number = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        Operator = (data.current_editor_font_name, 0xff7f7f7f, data.current_editor_font_size, None)
        Function = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
    
    class Nim:
        Default = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Comment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        BasicKeyword = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, True)
        TopKeyword = (data.current_editor_font_name, 0xff407fc0, data.current_editor_font_size, True)
        String = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        LongString = (data.current_editor_font_name, 0xff7f0000, data.current_editor_font_size, None)
        Number = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        Operator = (data.current_editor_font_name, 0xff7f7f7f, data.current_editor_font_size, None)
        Unsafe = (data.current_editor_font_name, 0xffc00000, data.current_editor_font_size, True)
        Type = (data.current_editor_font_name, 0xff6e6e00, data.current_editor_font_size, True)
        DocumentationComment = (data.current_editor_font_name, 0xff7f0a0a, data.current_editor_font_size, None)
        Definition = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        Class = (data.current_editor_font_name, 0xff0000ff, data.current_editor_font_size, None)
        KeywordOperator = (data.current_editor_font_name, 0xff963cc8, data.current_editor_font_size, None)
        CharLiteral = (data.current_editor_font_name, 0xff00c8ff, data.current_editor_font_size, None)
        CaseOf = (data.current_editor_font_name, 0xff8000ff, data.current_editor_font_size, None)
        UserKeyword = (data.current_editor_font_name, 0xffff8040, data.current_editor_font_size, None)
        MultilineComment = (data.current_editor_font_name, 0xff006c6c, data.current_editor_font_size, None)
        MultilineDocumentation = (data.current_editor_font_name, 0xff6e3296, data.current_editor_font_size, None)
        Pragma = (data.current_editor_font_name, 0xffc07f40, data.current_editor_font_size, None)
    
    class RouterOS:
        Default = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, True)
        Operator = (data.current_editor_font_name, 0xffB4B80A, data.current_editor_font_size, True)
        Comment = (data.current_editor_font_name, 0xff38B86B, data.current_editor_font_size, True)
        Keyword1 = (data.current_editor_font_name, 0xff008000, data.current_editor_font_size, True)
        Keyword2 = (data.current_editor_font_name, 0xffB9005C, data.current_editor_font_size, True)
        Keyword3 = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, True)
    
    class Oberon:
        Default = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Comment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        Keyword = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        String = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        Procedure = (data.current_editor_font_name, 0xff0000ff, data.current_editor_font_size, None)
        Module = (data.current_editor_font_name, 0xff7f0000, data.current_editor_font_size, None)
        Number = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        Type = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
    
    
    class AVS:
        BlockComment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        ClipProperty = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        Default = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Filter = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        Function = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        Identifier = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Keyword = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        KeywordSet6 = (data.current_editor_font_name, 0xff8000ff, data.current_editor_font_size, None)
        LineComment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        NestedBlockComment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        Number = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        Operator = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Plugin = (data.current_editor_font_name, 0xff0080c0, data.current_editor_font_size, None)
        String = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        TripleString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
    
    class Bash:
        Backticks = (data.current_editor_font_name, 0xffadad00, data.current_editor_font_size, None)
        Comment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        Default = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        DoubleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, True)
        Error = (data.current_editor_font_name, 0xffaa0000, data.current_editor_font_size, True)
        HereDocumentDelimiter = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Identifier = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Keyword = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        Number = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        Operator = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        ParameterExpansion = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Scalar = (data.current_editor_font_name, 0xffadad00, data.current_editor_font_size, True)
        SingleQuotedHereDocument = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        SingleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
    
    class Batch:
        Comment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        Default = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        ExternalCommand = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        HideCommandChar = (data.current_editor_font_name, 0xff7f7f00, data.current_editor_font_size, None)
        Keyword = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        Label = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        Operator = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Variable = (data.current_editor_font_name, 0xff800080, data.current_editor_font_size, None)
    
    class CMake:
        BlockForeach = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        BlockIf = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        BlockMacro = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        BlockWhile = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        Comment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        Default = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Function = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        KeywordSet3 = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Label = (data.current_editor_font_name, 0xffcc3300, data.current_editor_font_size, None)
        Number = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        String = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        StringLeftQuote = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        StringRightQuote = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        StringVariable = (data.current_editor_font_name, 0xffcc3300, data.current_editor_font_size, None)
        Variable = (data.current_editor_font_name, 0xff800000, data.current_editor_font_size, None)
    
    class CPP:
        Comment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        CommentDoc = (data.current_editor_font_name, 0xff3f703f, data.current_editor_font_size, None)
        CommentDocKeyword = (data.current_editor_font_name, 0xff3060a0, data.current_editor_font_size, None)
        CommentDocKeywordError = (data.current_editor_font_name, 0xff804020, data.current_editor_font_size, None)
        CommentLine = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        CommentLineDoc = (data.current_editor_font_name, 0xff3f703f, data.current_editor_font_size, None)
        Default = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        DoubleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        GlobalClass = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        HashQuotedString = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        Identifier = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactiveComment = (data.current_editor_font_name, 0xff90b090, data.current_editor_font_size, None)
        InactiveCommentDoc = (data.current_editor_font_name, 0xffd0d0d0, data.current_editor_font_size, None)
        InactiveCommentDocKeyword = (data.current_editor_font_name, 0xffc0c0c0, data.current_editor_font_size, None)
        InactiveCommentDocKeywordError = (data.current_editor_font_name, 0xffc0c0c0, data.current_editor_font_size, None)
        InactiveCommentLine = (data.current_editor_font_name, 0xff90b090, data.current_editor_font_size, None)
        InactiveCommentLineDoc = (data.current_editor_font_name, 0xffc0c0c0, data.current_editor_font_size, None)
        InactiveDefault = (data.current_editor_font_name, 0xffc0c0c0, data.current_editor_font_size, None)
        InactiveDoubleQuotedString = (data.current_editor_font_name, 0xffb090b0, data.current_editor_font_size, None)
        InactiveGlobalClass = (data.current_editor_font_name, 0xffb0b0b0, data.current_editor_font_size, None)
        InactiveHashQuotedString = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactiveIdentifier = (data.current_editor_font_name, 0xffb0b0b0, data.current_editor_font_size, None)
        InactiveKeyword = (data.current_editor_font_name, 0xff9090b0, data.current_editor_font_size, None)
        InactiveKeywordSet2 = (data.current_editor_font_name, 0xffc0c0c0, data.current_editor_font_size, None)
        InactiveNumber = (data.current_editor_font_name, 0xff90b090, data.current_editor_font_size, None)
        InactiveOperator = (data.current_editor_font_name, 0xffb0b0b0, data.current_editor_font_size, None)
        InactivePreProcessor = (data.current_editor_font_name, 0xffb0b090, data.current_editor_font_size, None)
        InactivePreProcessorComment = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactivePreProcessorCommentLineDoc = (data.current_editor_font_name, 0xffc0c0c0, data.current_editor_font_size, None)
        InactiveRawString = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactiveRegex = (data.current_editor_font_name, 0xff7faf7f, data.current_editor_font_size, None)
        InactiveSingleQuotedString = (data.current_editor_font_name, 0xffb090b0, data.current_editor_font_size, None)
        InactiveTripleQuotedVerbatimString = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactiveUUID = (data.current_editor_font_name, 0xffc0c0c0, data.current_editor_font_size, None)
        InactiveUnclosedString = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactiveVerbatimString = (data.current_editor_font_name, 0xff90b090, data.current_editor_font_size, None)
        Keyword = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        KeywordSet2 = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Number = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        Operator = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        PreProcessor = (data.current_editor_font_name, 0xff7f7f00, data.current_editor_font_size, None)
        PreProcessorComment = (data.current_editor_font_name, 0xff659900, data.current_editor_font_size, None)
        PreProcessorCommentLineDoc = (data.current_editor_font_name, 0xff3f703f, data.current_editor_font_size, None)
        RawString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        Regex = (data.current_editor_font_name, 0xff3f7f3f, data.current_editor_font_size, None)
        SingleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        TripleQuotedVerbatimString = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        UUID = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        UnclosedString = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        VerbatimString = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        UserLiteral = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactiveEscapeSequence = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        EscapeSequence = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactiveUserLiteral = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactiveTaskMarker = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        TaskMarker = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
    
    class CSS:
        AtRule = (data.current_editor_font_name, 0xff7f7f00, data.current_editor_font_size, None)
        Attribute = (data.current_editor_font_name, 0xff800000, data.current_editor_font_size, None)
        CSS1Property = (data.current_editor_font_name, 0xff0040e0, data.current_editor_font_size, None)
        CSS2Property = (data.current_editor_font_name, 0xff00a0e0, data.current_editor_font_size, None)
        CSS3Property = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        ClassSelector = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Comment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        Default = (data.current_editor_font_name, 0xffff0080, data.current_editor_font_size, None)
        DoubleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        ExtendedCSSProperty = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        ExtendedPseudoClass = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        ExtendedPseudoElement = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        IDSelector = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        Important = (data.current_editor_font_name, 0xffff8000, data.current_editor_font_size, None)
        MediaRule = (data.current_editor_font_name, 0xff7f7f00, data.current_editor_font_size, None)
        Operator = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        PseudoClass = (data.current_editor_font_name, 0xff800000, data.current_editor_font_size, None)
        PseudoElement = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        SingleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        Tag = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        UnknownProperty = (data.current_editor_font_name, 0xffff0000, data.current_editor_font_size, None)
        UnknownPseudoClass = (data.current_editor_font_name, 0xffff0000, data.current_editor_font_size, None)
        Value = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        Variable = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
    
    class CSharp:
        Comment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        CommentDoc = (data.current_editor_font_name, 0xff3f703f, data.current_editor_font_size, None)
        CommentDocKeyword = (data.current_editor_font_name, 0xff3060a0, data.current_editor_font_size, None)
        CommentDocKeywordError = (data.current_editor_font_name, 0xff804020, data.current_editor_font_size, None)
        CommentLine = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        CommentLineDoc = (data.current_editor_font_name, 0xff3f703f, data.current_editor_font_size, None)
        Default = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        DoubleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        GlobalClass = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        HashQuotedString = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        Identifier = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactiveComment = (data.current_editor_font_name, 0xff90b090, data.current_editor_font_size, None)
        InactiveCommentDoc = (data.current_editor_font_name, 0xffd0d0d0, data.current_editor_font_size, None)
        InactiveCommentDocKeyword = (data.current_editor_font_name, 0xffc0c0c0, data.current_editor_font_size, None)
        InactiveCommentDocKeywordError = (data.current_editor_font_name, 0xffc0c0c0, data.current_editor_font_size, None)
        InactiveCommentLine = (data.current_editor_font_name, 0xff90b090, data.current_editor_font_size, None)
        InactiveCommentLineDoc = (data.current_editor_font_name, 0xffc0c0c0, data.current_editor_font_size, None)
        InactiveDefault = (data.current_editor_font_name, 0xffc0c0c0, data.current_editor_font_size, None)
        InactiveDoubleQuotedString = (data.current_editor_font_name, 0xffb090b0, data.current_editor_font_size, None)
        InactiveGlobalClass = (data.current_editor_font_name, 0xffb0b0b0, data.current_editor_font_size, None)
        InactiveHashQuotedString = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactiveIdentifier = (data.current_editor_font_name, 0xffb0b0b0, data.current_editor_font_size, None)
        InactiveKeyword = (data.current_editor_font_name, 0xff9090b0, data.current_editor_font_size, None)
        InactiveKeywordSet2 = (data.current_editor_font_name, 0xffc0c0c0, data.current_editor_font_size, None)
        InactiveNumber = (data.current_editor_font_name, 0xff90b090, data.current_editor_font_size, None)
        InactiveOperator = (data.current_editor_font_name, 0xffb0b0b0, data.current_editor_font_size, None)
        InactivePreProcessor = (data.current_editor_font_name, 0xffb0b090, data.current_editor_font_size, None)
        InactivePreProcessorComment = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactivePreProcessorCommentLineDoc = (data.current_editor_font_name, 0xffc0c0c0, data.current_editor_font_size, None)
        InactiveRawString = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactiveRegex = (data.current_editor_font_name, 0xff7faf7f, data.current_editor_font_size, None)
        InactiveSingleQuotedString = (data.current_editor_font_name, 0xffb090b0, data.current_editor_font_size, None)
        InactiveTripleQuotedVerbatimString = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactiveUUID = (data.current_editor_font_name, 0xffc0c0c0, data.current_editor_font_size, None)
        InactiveUnclosedString = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactiveVerbatimString = (data.current_editor_font_name, 0xff90b090, data.current_editor_font_size, None)
        Keyword = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        KeywordSet2 = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Number = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        Operator = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        PreProcessor = (data.current_editor_font_name, 0xff7f7f00, data.current_editor_font_size, None)
        PreProcessorComment = (data.current_editor_font_name, 0xff659900, data.current_editor_font_size, None)
        PreProcessorCommentLineDoc = (data.current_editor_font_name, 0xff3f703f, data.current_editor_font_size, None)
        RawString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        Regex = (data.current_editor_font_name, 0xff3f7f3f, data.current_editor_font_size, None)
        SingleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        TripleQuotedVerbatimString = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        UUID = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        UnclosedString = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        VerbatimString = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        UserLiteral = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactiveEscapeSequence = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        EscapeSequence = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactiveUserLiteral = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactiveTaskMarker = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        TaskMarker = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
    
    class CoffeeScript:
        BlockRegex = (data.current_editor_font_name, 0xff3f7f3f, data.current_editor_font_size, None)
        BlockRegexComment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        Comment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        CommentBlock = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        CommentDoc = (data.current_editor_font_name, 0xff3f703f, data.current_editor_font_size, None)
        CommentDocKeyword = (data.current_editor_font_name, 0xff3060a0, data.current_editor_font_size, None)
        CommentDocKeywordError = (data.current_editor_font_name, 0xff804020, data.current_editor_font_size, None)
        CommentLine = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        CommentLineDoc = (data.current_editor_font_name, 0xff3f703f, data.current_editor_font_size, None)
        Default = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        DoubleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        GlobalClass = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Identifier = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Keyword = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        KeywordSet2 = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Number = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        Operator = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        PreProcessor = (data.current_editor_font_name, 0xff7f7f00, data.current_editor_font_size, None)
        Regex = (data.current_editor_font_name, 0xff3f7f3f, data.current_editor_font_size, None)
        SingleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        UUID = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        UnclosedString = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        VerbatimString = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
    
    class D:
        BackquoteString = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Character = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        Comment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        CommentDoc = (data.current_editor_font_name, 0xff3f703f, data.current_editor_font_size, None)
        CommentDocKeyword = (data.current_editor_font_name, 0xff3060a0, data.current_editor_font_size, None)
        CommentDocKeywordError = (data.current_editor_font_name, 0xff804020, data.current_editor_font_size, None)
        CommentLine = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        CommentLineDoc = (data.current_editor_font_name, 0xff3f703f, data.current_editor_font_size, None)
        CommentNested = (data.current_editor_font_name, 0xffa0c0a0, data.current_editor_font_size, None)
        Default = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        Identifier = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Keyword = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        KeywordDoc = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        KeywordSecondary = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        KeywordSet5 = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        KeywordSet6 = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        KeywordSet7 = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Number = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        Operator = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        RawString = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        String = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        Typedefs = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        UnclosedString = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
    
    class Diff:
        Command = (data.current_editor_font_name, 0xff7f7f00, data.current_editor_font_size, None)
        Comment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        Default = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Header = (data.current_editor_font_name, 0xff7f0000, data.current_editor_font_size, None)
        LineAdded = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        LineChanged = (data.current_editor_font_name, 0xff7f7f7f, data.current_editor_font_size, None)
        LineRemoved = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        Position = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
    
    class Fortran:
        Comment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        Continuation = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Default = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        DottedOperator = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        DoubleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        ExtendedFunction = (data.current_editor_font_name, 0xffb04080, data.current_editor_font_size, None)
        Identifier = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        IntrinsicFunction = (data.current_editor_font_name, 0xffb00040, data.current_editor_font_size, None)
        Keyword = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        Label = (data.current_editor_font_name, 0xffe0c0e0, data.current_editor_font_size, None)
        Number = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        Operator = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        PreProcessor = (data.current_editor_font_name, 0xff7f7f00, data.current_editor_font_size, None)
        SingleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        UnclosedString = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
    
    class Fortran77:
        Comment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        Continuation = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Default = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        DottedOperator = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        DoubleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        ExtendedFunction = (data.current_editor_font_name, 0xffb04080, data.current_editor_font_size, None)
        Identifier = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        IntrinsicFunction = (data.current_editor_font_name, 0xffb00040, data.current_editor_font_size, None)
        Keyword = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        Label = (data.current_editor_font_name, 0xffe0c0e0, data.current_editor_font_size, None)
        Number = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        Operator = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        PreProcessor = (data.current_editor_font_name, 0xff7f7f00, data.current_editor_font_size, None)
        SingleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        UnclosedString = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
    
    class HTML:
        ASPAtStart = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        ASPJavaScriptComment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        ASPJavaScriptCommentDoc = (data.current_editor_font_name, 0xff7f7f7f, data.current_editor_font_size, None)
        ASPJavaScriptCommentLine = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        ASPJavaScriptDefault = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        ASPJavaScriptDoubleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        ASPJavaScriptKeyword = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        ASPJavaScriptNumber = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        ASPJavaScriptRegex = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        ASPJavaScriptSingleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        ASPJavaScriptStart = (data.current_editor_font_name, 0xff7f7f00, data.current_editor_font_size, None)
        ASPJavaScriptSymbol = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        ASPJavaScriptUnclosedString = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        ASPJavaScriptWord = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        ASPPythonClassName = (data.current_editor_font_name, 0xff0000ff, data.current_editor_font_size, None)
        ASPPythonComment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        ASPPythonDefault = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        ASPPythonDoubleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        ASPPythonFunctionMethodName = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        ASPPythonIdentifier = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        ASPPythonKeyword = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        ASPPythonNumber = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        ASPPythonOperator = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        ASPPythonSingleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        ASPPythonStart = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        ASPPythonTripleDoubleQuotedString = (data.current_editor_font_name, 0xff7f0000, data.current_editor_font_size, None)
        ASPPythonTripleSingleQuotedString = (data.current_editor_font_name, 0xff7f0000, data.current_editor_font_size, None)
        ASPStart = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        ASPVBScriptComment = (data.current_editor_font_name, 0xff008000, data.current_editor_font_size, None)
        ASPVBScriptDefault = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        ASPVBScriptIdentifier = (data.current_editor_font_name, 0xff000080, data.current_editor_font_size, None)
        ASPVBScriptKeyword = (data.current_editor_font_name, 0xff000080, data.current_editor_font_size, None)
        ASPVBScriptNumber = (data.current_editor_font_name, 0xff008080, data.current_editor_font_size, None)
        ASPVBScriptStart = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        ASPVBScriptString = (data.current_editor_font_name, 0xff800080, data.current_editor_font_size, None)
        ASPVBScriptUnclosedString = (data.current_editor_font_name, 0xff000080, data.current_editor_font_size, None)
        ASPXCComment = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Attribute = (data.current_editor_font_name, 0xff008080, data.current_editor_font_size, None)
        CDATA = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Default = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Entity = (data.current_editor_font_name, 0xff800080, data.current_editor_font_size, None)
        HTMLComment = (data.current_editor_font_name, 0xff808000, data.current_editor_font_size, None)
        HTMLDoubleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        HTMLNumber = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        HTMLSingleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        HTMLValue = (data.current_editor_font_name, 0xffff00ff, data.current_editor_font_size, None)
        JavaScriptComment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        JavaScriptCommentDoc = (data.current_editor_font_name, 0xff3f703f, data.current_editor_font_size, None)
        JavaScriptCommentLine = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        JavaScriptDefault = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        JavaScriptDoubleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        JavaScriptKeyword = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        JavaScriptNumber = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        JavaScriptRegex = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        JavaScriptSingleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        JavaScriptStart = (data.current_editor_font_name, 0xff7f7f00, data.current_editor_font_size, None)
        JavaScriptSymbol = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        JavaScriptUnclosedString = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        JavaScriptWord = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        OtherInTag = (data.current_editor_font_name, 0xff800080, data.current_editor_font_size, None)
        PHPComment = (data.current_editor_font_name, 0xff999999, data.current_editor_font_size, None)
        PHPCommentLine = (data.current_editor_font_name, 0xff666666, data.current_editor_font_size, None)
        PHPDefault = (data.current_editor_font_name, 0xff000033, data.current_editor_font_size, None)
        PHPDoubleQuotedString = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        PHPDoubleQuotedVariable = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        PHPKeyword = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        PHPNumber = (data.current_editor_font_name, 0xffcc9900, data.current_editor_font_size, None)
        PHPOperator = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        PHPSingleQuotedString = (data.current_editor_font_name, 0xff009f00, data.current_editor_font_size, None)
        PHPStart = (data.current_editor_font_name, 0xff0000ff, data.current_editor_font_size, None)
        PHPVariable = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        PythonClassName = (data.current_editor_font_name, 0xff0000ff, data.current_editor_font_size, None)
        PythonComment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        PythonDefault = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        PythonDoubleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        PythonFunctionMethodName = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        PythonIdentifier = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        PythonKeyword = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        PythonNumber = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        PythonOperator = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        PythonSingleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        PythonStart = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        PythonTripleDoubleQuotedString = (data.current_editor_font_name, 0xff7f0000, data.current_editor_font_size, None)
        PythonTripleSingleQuotedString = (data.current_editor_font_name, 0xff7f0000, data.current_editor_font_size, None)
        SGMLBlockDefault = (data.current_editor_font_name, 0xff000066, data.current_editor_font_size, None)
        SGMLCommand = (data.current_editor_font_name, 0xff000080, data.current_editor_font_size, None)
        SGMLComment = (data.current_editor_font_name, 0xff808000, data.current_editor_font_size, None)
        SGMLDefault = (data.current_editor_font_name, 0xff000080, data.current_editor_font_size, None)
        SGMLDoubleQuotedString = (data.current_editor_font_name, 0xff800000, data.current_editor_font_size, None)
        SGMLEntity = (data.current_editor_font_name, 0xff333333, data.current_editor_font_size, None)
        SGMLError = (data.current_editor_font_name, 0xff800000, data.current_editor_font_size, None)
        SGMLParameter = (data.current_editor_font_name, 0xff006600, data.current_editor_font_size, None)
        SGMLParameterComment = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        SGMLSingleQuotedString = (data.current_editor_font_name, 0xff993300, data.current_editor_font_size, None)
        SGMLSpecial = (data.current_editor_font_name, 0xff3366ff, data.current_editor_font_size, None)
        Script = (data.current_editor_font_name, 0xff000080, data.current_editor_font_size, None)
        Tag = (data.current_editor_font_name, 0xff000080, data.current_editor_font_size, None)
        UnknownAttribute = (data.current_editor_font_name, 0xffff0000, data.current_editor_font_size, None)
        UnknownTag = (data.current_editor_font_name, 0xffff0000, data.current_editor_font_size, None)
        VBScriptComment = (data.current_editor_font_name, 0xff008000, data.current_editor_font_size, None)
        VBScriptDefault = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        VBScriptIdentifier = (data.current_editor_font_name, 0xff000080, data.current_editor_font_size, None)
        VBScriptKeyword = (data.current_editor_font_name, 0xff000080, data.current_editor_font_size, None)
        VBScriptNumber = (data.current_editor_font_name, 0xff008080, data.current_editor_font_size, None)
        VBScriptStart = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        VBScriptString = (data.current_editor_font_name, 0xff800080, data.current_editor_font_size, None)
        VBScriptUnclosedString = (data.current_editor_font_name, 0xff000080, data.current_editor_font_size, None)
        XMLEnd = (data.current_editor_font_name, 0xff0000ff, data.current_editor_font_size, None)
        XMLStart = (data.current_editor_font_name, 0xff0000ff, data.current_editor_font_size, None)
        XMLTagEnd = (data.current_editor_font_name, 0xff000080, data.current_editor_font_size, None)
    
    class IDL:
        Comment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        CommentDoc = (data.current_editor_font_name, 0xff3f703f, data.current_editor_font_size, None)
        CommentDocKeyword = (data.current_editor_font_name, 0xff3060a0, data.current_editor_font_size, None)
        CommentDocKeywordError = (data.current_editor_font_name, 0xff804020, data.current_editor_font_size, None)
        CommentLine = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        CommentLineDoc = (data.current_editor_font_name, 0xff3f703f, data.current_editor_font_size, None)
        Default = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        DoubleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        GlobalClass = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        HashQuotedString = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        Identifier = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactiveComment = (data.current_editor_font_name, 0xff90b090, data.current_editor_font_size, None)
        InactiveCommentDoc = (data.current_editor_font_name, 0xffd0d0d0, data.current_editor_font_size, None)
        InactiveCommentDocKeyword = (data.current_editor_font_name, 0xffc0c0c0, data.current_editor_font_size, None)
        InactiveCommentDocKeywordError = (data.current_editor_font_name, 0xffc0c0c0, data.current_editor_font_size, None)
        InactiveCommentLine = (data.current_editor_font_name, 0xff90b090, data.current_editor_font_size, None)
        InactiveCommentLineDoc = (data.current_editor_font_name, 0xffc0c0c0, data.current_editor_font_size, None)
        InactiveDefault = (data.current_editor_font_name, 0xffc0c0c0, data.current_editor_font_size, None)
        InactiveDoubleQuotedString = (data.current_editor_font_name, 0xffb090b0, data.current_editor_font_size, None)
        InactiveGlobalClass = (data.current_editor_font_name, 0xffb0b0b0, data.current_editor_font_size, None)
        InactiveHashQuotedString = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactiveIdentifier = (data.current_editor_font_name, 0xffb0b0b0, data.current_editor_font_size, None)
        InactiveKeyword = (data.current_editor_font_name, 0xff9090b0, data.current_editor_font_size, None)
        InactiveKeywordSet2 = (data.current_editor_font_name, 0xffc0c0c0, data.current_editor_font_size, None)
        InactiveNumber = (data.current_editor_font_name, 0xff90b090, data.current_editor_font_size, None)
        InactiveOperator = (data.current_editor_font_name, 0xffb0b0b0, data.current_editor_font_size, None)
        InactivePreProcessor = (data.current_editor_font_name, 0xffb0b090, data.current_editor_font_size, None)
        InactivePreProcessorComment = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactivePreProcessorCommentLineDoc = (data.current_editor_font_name, 0xffc0c0c0, data.current_editor_font_size, None)
        InactiveRawString = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactiveRegex = (data.current_editor_font_name, 0xff7faf7f, data.current_editor_font_size, None)
        InactiveSingleQuotedString = (data.current_editor_font_name, 0xffb090b0, data.current_editor_font_size, None)
        InactiveTripleQuotedVerbatimString = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactiveUUID = (data.current_editor_font_name, 0xffc0c0c0, data.current_editor_font_size, None)
        InactiveUnclosedString = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactiveVerbatimString = (data.current_editor_font_name, 0xff90b090, data.current_editor_font_size, None)
        Keyword = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        KeywordSet2 = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Number = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        Operator = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        PreProcessor = (data.current_editor_font_name, 0xff7f7f00, data.current_editor_font_size, None)
        PreProcessorComment = (data.current_editor_font_name, 0xff659900, data.current_editor_font_size, None)
        PreProcessorCommentLineDoc = (data.current_editor_font_name, 0xff3f703f, data.current_editor_font_size, None)
        RawString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        Regex = (data.current_editor_font_name, 0xff3f7f3f, data.current_editor_font_size, None)
        SingleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        TripleQuotedVerbatimString = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        UUID = (data.current_editor_font_name, 0xff804080, data.current_editor_font_size, None)
        UnclosedString = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        VerbatimString = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        UserLiteral = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactiveEscapeSequence = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        EscapeSequence = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactiveUserLiteral = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactiveTaskMarker = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        TaskMarker = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
    
    class Java:
        Comment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        CommentDoc = (data.current_editor_font_name, 0xff3f703f, data.current_editor_font_size, None)
        CommentDocKeyword = (data.current_editor_font_name, 0xff3060a0, data.current_editor_font_size, None)
        CommentDocKeywordError = (data.current_editor_font_name, 0xff804020, data.current_editor_font_size, None)
        CommentLine = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        CommentLineDoc = (data.current_editor_font_name, 0xff3f703f, data.current_editor_font_size, None)
        Default = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        DoubleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        GlobalClass = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        HashQuotedString = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        Identifier = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactiveComment = (data.current_editor_font_name, 0xff90b090, data.current_editor_font_size, None)
        InactiveCommentDoc = (data.current_editor_font_name, 0xffd0d0d0, data.current_editor_font_size, None)
        InactiveCommentDocKeyword = (data.current_editor_font_name, 0xffc0c0c0, data.current_editor_font_size, None)
        InactiveCommentDocKeywordError = (data.current_editor_font_name, 0xffc0c0c0, data.current_editor_font_size, None)
        InactiveCommentLine = (data.current_editor_font_name, 0xff90b090, data.current_editor_font_size, None)
        InactiveCommentLineDoc = (data.current_editor_font_name, 0xffc0c0c0, data.current_editor_font_size, None)
        InactiveDefault = (data.current_editor_font_name, 0xffc0c0c0, data.current_editor_font_size, None)
        InactiveDoubleQuotedString = (data.current_editor_font_name, 0xffb090b0, data.current_editor_font_size, None)
        InactiveGlobalClass = (data.current_editor_font_name, 0xffb0b0b0, data.current_editor_font_size, None)
        InactiveHashQuotedString = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactiveIdentifier = (data.current_editor_font_name, 0xffb0b0b0, data.current_editor_font_size, None)
        InactiveKeyword = (data.current_editor_font_name, 0xff9090b0, data.current_editor_font_size, None)
        InactiveKeywordSet2 = (data.current_editor_font_name, 0xffc0c0c0, data.current_editor_font_size, None)
        InactiveNumber = (data.current_editor_font_name, 0xff90b090, data.current_editor_font_size, None)
        InactiveOperator = (data.current_editor_font_name, 0xffb0b0b0, data.current_editor_font_size, None)
        InactivePreProcessor = (data.current_editor_font_name, 0xffb0b090, data.current_editor_font_size, None)
        InactivePreProcessorComment = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactivePreProcessorCommentLineDoc = (data.current_editor_font_name, 0xffc0c0c0, data.current_editor_font_size, None)
        InactiveRawString = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactiveRegex = (data.current_editor_font_name, 0xff7faf7f, data.current_editor_font_size, None)
        InactiveSingleQuotedString = (data.current_editor_font_name, 0xffb090b0, data.current_editor_font_size, None)
        InactiveTripleQuotedVerbatimString = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactiveUUID = (data.current_editor_font_name, 0xffc0c0c0, data.current_editor_font_size, None)
        InactiveUnclosedString = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactiveVerbatimString = (data.current_editor_font_name, 0xff90b090, data.current_editor_font_size, None)
        Keyword = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        KeywordSet2 = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Number = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        Operator = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        PreProcessor = (data.current_editor_font_name, 0xff7f7f00, data.current_editor_font_size, None)
        PreProcessorComment = (data.current_editor_font_name, 0xff659900, data.current_editor_font_size, None)
        PreProcessorCommentLineDoc = (data.current_editor_font_name, 0xff3f703f, data.current_editor_font_size, None)
        RawString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        Regex = (data.current_editor_font_name, 0xff3f7f3f, data.current_editor_font_size, None)
        SingleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        TripleQuotedVerbatimString = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        UUID = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        UnclosedString = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        VerbatimString = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        UserLiteral = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactiveEscapeSequence = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        EscapeSequence = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactiveUserLiteral = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactiveTaskMarker = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        TaskMarker = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
    
    class JavaScript:
        Comment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        CommentDoc = (data.current_editor_font_name, 0xff3f703f, data.current_editor_font_size, None)
        CommentDocKeyword = (data.current_editor_font_name, 0xff3060a0, data.current_editor_font_size, None)
        CommentDocKeywordError = (data.current_editor_font_name, 0xff804020, data.current_editor_font_size, None)
        CommentLine = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        CommentLineDoc = (data.current_editor_font_name, 0xff3f703f, data.current_editor_font_size, None)
        Default = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        DoubleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        GlobalClass = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        HashQuotedString = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        Identifier = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactiveComment = (data.current_editor_font_name, 0xff90b090, data.current_editor_font_size, None)
        InactiveCommentDoc = (data.current_editor_font_name, 0xffd0d0d0, data.current_editor_font_size, None)
        InactiveCommentDocKeyword = (data.current_editor_font_name, 0xffc0c0c0, data.current_editor_font_size, None)
        InactiveCommentDocKeywordError = (data.current_editor_font_name, 0xffc0c0c0, data.current_editor_font_size, None)
        InactiveCommentLine = (data.current_editor_font_name, 0xff90b090, data.current_editor_font_size, None)
        InactiveCommentLineDoc = (data.current_editor_font_name, 0xffc0c0c0, data.current_editor_font_size, None)
        InactiveDefault = (data.current_editor_font_name, 0xffc0c0c0, data.current_editor_font_size, None)
        InactiveDoubleQuotedString = (data.current_editor_font_name, 0xffb090b0, data.current_editor_font_size, None)
        InactiveGlobalClass = (data.current_editor_font_name, 0xffb0b0b0, data.current_editor_font_size, None)
        InactiveHashQuotedString = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactiveIdentifier = (data.current_editor_font_name, 0xffb0b0b0, data.current_editor_font_size, None)
        InactiveKeyword = (data.current_editor_font_name, 0xff9090b0, data.current_editor_font_size, None)
        InactiveKeywordSet2 = (data.current_editor_font_name, 0xffc0c0c0, data.current_editor_font_size, None)
        InactiveNumber = (data.current_editor_font_name, 0xff90b090, data.current_editor_font_size, None)
        InactiveOperator = (data.current_editor_font_name, 0xffb0b0b0, data.current_editor_font_size, None)
        InactivePreProcessor = (data.current_editor_font_name, 0xffb0b090, data.current_editor_font_size, None)
        InactivePreProcessorComment = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactivePreProcessorCommentLineDoc = (data.current_editor_font_name, 0xffc0c0c0, data.current_editor_font_size, None)
        InactiveRawString = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactiveRegex = (data.current_editor_font_name, 0xff7faf7f, data.current_editor_font_size, None)
        InactiveSingleQuotedString = (data.current_editor_font_name, 0xffb090b0, data.current_editor_font_size, None)
        InactiveTripleQuotedVerbatimString = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactiveUUID = (data.current_editor_font_name, 0xffc0c0c0, data.current_editor_font_size, None)
        InactiveUnclosedString = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactiveVerbatimString = (data.current_editor_font_name, 0xff90b090, data.current_editor_font_size, None)
        Keyword = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        KeywordSet2 = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Number = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        Operator = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        PreProcessor = (data.current_editor_font_name, 0xff7f7f00, data.current_editor_font_size, None)
        PreProcessorComment = (data.current_editor_font_name, 0xff659900, data.current_editor_font_size, None)
        PreProcessorCommentLineDoc = (data.current_editor_font_name, 0xff3f703f, data.current_editor_font_size, None)
        RawString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        Regex = (data.current_editor_font_name, 0xff3f7f3f, data.current_editor_font_size, None)
        SingleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        TripleQuotedVerbatimString = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        UUID = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        UnclosedString = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        VerbatimString = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        UserLiteral = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactiveEscapeSequence = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        EscapeSequence = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactiveUserLiteral = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InactiveTaskMarker = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        TaskMarker = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
    
    class Lua:
        BasicFunctions = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        Character = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        Comment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        CoroutinesIOSystemFacilities = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        Default = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Identifier = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Keyword = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        KeywordSet5 = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        KeywordSet6 = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        KeywordSet7 = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        KeywordSet8 = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Label = (data.current_editor_font_name, 0xff7f7f00, data.current_editor_font_size, None)
        LineComment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        LiteralString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        Number = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        Operator = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Preprocessor = (data.current_editor_font_name, 0xff7f7f00, data.current_editor_font_size, None)
        String = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        StringTableMathsFunctions = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        UnclosedString = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
    
    class Makefile:
        Comment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        Default = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Error = (data.current_editor_font_name, 0xffffff00, data.current_editor_font_size, None)
        Operator = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Preprocessor = (data.current_editor_font_name, 0xff7f7f00, data.current_editor_font_size, None)
        Target = (data.current_editor_font_name, 0xffa00000, data.current_editor_font_size, None)
        Variable = (data.current_editor_font_name, 0xff000080, data.current_editor_font_size, None)
    
    class Matlab:
        Command = (data.current_editor_font_name, 0xff7f7f00, data.current_editor_font_size, None)
        Comment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        Default = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        DoubleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        Identifier = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Keyword = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        Number = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        Operator = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        SingleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
    
    class Octave:
        Command = (data.current_editor_font_name, 0xff7f7f00, data.current_editor_font_size, None)
        Comment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        Default = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        DoubleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        Identifier = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Keyword = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        Number = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        Operator = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        SingleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
    
    class PO:
        Comment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        Default = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Flags = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Fuzzy = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        MessageContext = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        MessageContextText = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        MessageContextTextEOL = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        MessageId = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        MessageIdText = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        MessageIdTextEOL = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        MessageString = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        MessageStringText = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        MessageStringTextEOL = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        ProgrammerComment = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Reference = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
    
    class POV:
        BadDirective = (data.current_editor_font_name, 0xff804020, data.current_editor_font_size, None)
        Comment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        CommentLine = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        Default = (data.current_editor_font_name, 0xffff0080, data.current_editor_font_size, None)
        Directive = (data.current_editor_font_name, 0xff7f7f00, data.current_editor_font_size, None)
        Identifier = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        KeywordSet6 = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        KeywordSet7 = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        KeywordSet8 = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        Number = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        ObjectsCSGAppearance = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        Operator = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        PredefinedFunctions = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        PredefinedIdentifiers = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        String = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        TypesModifiersItems = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        UnclosedString = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
    
    class Pascal:
        Asm = (data.current_editor_font_name, 0xff804080, data.current_editor_font_size, None)
        Character = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        Comment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        CommentLine = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        CommentParenthesis = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        Default = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        HexNumber = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        Identifier = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Keyword = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        Number = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        Operator = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        PreProcessor = (data.current_editor_font_name, 0xff7f7f00, data.current_editor_font_size, None)
        PreProcessorParenthesis = (data.current_editor_font_name, 0xff7f7f00, data.current_editor_font_size, None)
        SingleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        UnclosedString = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
    
    class Perl:
        Array = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        BacktickHereDocument = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        BacktickHereDocumentVar = (data.current_editor_font_name, 0xffd00000, data.current_editor_font_size, None)
        Backticks = (data.current_editor_font_name, 0xffffff00, data.current_editor_font_size, None)
        BackticksVar = (data.current_editor_font_name, 0xffd00000, data.current_editor_font_size, None)
        Comment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        DataSection = (data.current_editor_font_name, 0xff600000, data.current_editor_font_size, None)
        Default = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        DoubleQuotedHereDocument = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        DoubleQuotedHereDocumentVar = (data.current_editor_font_name, 0xffd00000, data.current_editor_font_size, None)
        DoubleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        DoubleQuotedStringVar = (data.current_editor_font_name, 0xffd00000, data.current_editor_font_size, None)
        Error = (data.current_editor_font_name, 0xffffff00, data.current_editor_font_size, None)
        FormatBody = (data.current_editor_font_name, 0xffc000c0, data.current_editor_font_size, None)
        FormatIdentifier = (data.current_editor_font_name, 0xffc000c0, data.current_editor_font_size, None)
        Hash = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        HereDocumentDelimiter = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Identifier = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Keyword = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        Number = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        Operator = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        POD = (data.current_editor_font_name, 0xff004000, data.current_editor_font_size, None)
        PODVerbatim = (data.current_editor_font_name, 0xff004000, data.current_editor_font_size, None)
        QuotedStringQ = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        QuotedStringQQ = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        QuotedStringQQVar = (data.current_editor_font_name, 0xffd00000, data.current_editor_font_size, None)
        QuotedStringQR = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        QuotedStringQRVar = (data.current_editor_font_name, 0xffd00000, data.current_editor_font_size, None)
        QuotedStringQW = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        QuotedStringQX = (data.current_editor_font_name, 0xffffff00, data.current_editor_font_size, None)
        QuotedStringQXVar = (data.current_editor_font_name, 0xffd00000, data.current_editor_font_size, None)
        Regex = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        RegexVar = (data.current_editor_font_name, 0xffd00000, data.current_editor_font_size, None)
        Scalar = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        SingleQuotedHereDocument = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        SingleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        SubroutinePrototype = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Substitution = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        SubstitutionVar = (data.current_editor_font_name, 0xffd00000, data.current_editor_font_size, None)
        SymbolTable = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Translation = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
    
    class PostScript:
        ArrayParenthesis = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        BadStringCharacter = (data.current_editor_font_name, 0xffffff00, data.current_editor_font_size, None)
        Base85String = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        Comment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        DSCComment = (data.current_editor_font_name, 0xff3f703f, data.current_editor_font_size, None)
        DSCCommentValue = (data.current_editor_font_name, 0xff3060a0, data.current_editor_font_size, None)
        Default = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        DictionaryParenthesis = (data.current_editor_font_name, 0xff3060a0, data.current_editor_font_size, None)
        HexString = (data.current_editor_font_name, 0xff3f7f3f, data.current_editor_font_size, None)
        ImmediateEvalLiteral = (data.current_editor_font_name, 0xff7f7f00, data.current_editor_font_size, None)
        Keyword = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        Literal = (data.current_editor_font_name, 0xff7f7f00, data.current_editor_font_size, None)
        Name = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Number = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        ProcedureParenthesis = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Text = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
    
    class Properties:
        Assignment = (data.current_editor_font_name, 0xffb06000, data.current_editor_font_size, None)
        Comment = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        Default = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        DefaultValue = (data.current_editor_font_name, 0xff7f7f00, data.current_editor_font_size, None)
        Key = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Section = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
    
    class Python:
        ClassName = (data.current_editor_font_name, 0xff0000ff, data.current_editor_font_size, None)
        Comment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        CommentBlock = (data.current_editor_font_name, 0xff52004a, data.current_editor_font_size, None)
        Decorator = (data.current_editor_font_name, 0xff805000, data.current_editor_font_size, None)
        Default = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        DoubleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        FunctionMethodName = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        HighlightedIdentifier = (data.current_editor_font_name, 0xff407090, data.current_editor_font_size, None)
        Identifier = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Inconsistent = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        Keyword = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, True)
        NoWarning = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        Number = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        Operator = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        SingleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        Spaces = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        Tabs = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        TabsAfterSpaces = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        TripleDoubleQuotedString = (data.current_editor_font_name, 0xff7f0000, data.current_editor_font_size, None)
        TripleSingleQuotedString = (data.current_editor_font_name, 0xff7f0000, data.current_editor_font_size, None)
        UnclosedString = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        CustomKeyword = (data.current_editor_font_name, 0xff6e6e00, data.current_editor_font_size, True)
    
    class Ruby:
        Backticks = (data.current_editor_font_name, 0xffffff00, data.current_editor_font_size, None)
        ClassName = (data.current_editor_font_name, 0xff0000ff, data.current_editor_font_size, None)
        ClassVariable = (data.current_editor_font_name, 0xff8000b0, data.current_editor_font_size, None)
        Comment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        DataSection = (data.current_editor_font_name, 0xff600000, data.current_editor_font_size, None)
        Default = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        DemotedKeyword = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        DoubleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        Error = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        FunctionMethodName = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        Global = (data.current_editor_font_name, 0xff800080, data.current_editor_font_size, None)
        HereDocument = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        HereDocumentDelimiter = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Identifier = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        InstanceVariable = (data.current_editor_font_name, 0xffb00080, data.current_editor_font_size, None)
        Keyword = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        ModuleName = (data.current_editor_font_name, 0xffa000a0, data.current_editor_font_size, None)
        Number = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        Operator = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        POD = (data.current_editor_font_name, 0xff004000, data.current_editor_font_size, None)
        PercentStringQ = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        PercentStringq = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        PercentStringr = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        PercentStringw = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        PercentStringx = (data.current_editor_font_name, 0xffffff00, data.current_editor_font_size, None)
        Regex = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        SingleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        Stderr = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Stdin = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Stdout = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Symbol = (data.current_editor_font_name, 0xffc0a030, data.current_editor_font_size, None)
    
    class SQL:
        Comment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        CommentDoc = (data.current_editor_font_name, 0xff7f7f7f, data.current_editor_font_size, None)
        CommentDocKeyword = (data.current_editor_font_name, 0xff3060a0, data.current_editor_font_size, None)
        CommentDocKeywordError = (data.current_editor_font_name, 0xff804020, data.current_editor_font_size, None)
        CommentLine = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        CommentLineHash = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        Default = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        DoubleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        Identifier = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Keyword = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        KeywordSet5 = (data.current_editor_font_name, 0xff4b0082, data.current_editor_font_size, None)
        KeywordSet6 = (data.current_editor_font_name, 0xffb00040, data.current_editor_font_size, None)
        KeywordSet7 = (data.current_editor_font_name, 0xff8b0000, data.current_editor_font_size, None)
        KeywordSet8 = (data.current_editor_font_name, 0xff800080, data.current_editor_font_size, None)
        Number = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        Operator = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        PlusComment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        PlusKeyword = (data.current_editor_font_name, 0xff7f7f00, data.current_editor_font_size, None)
        PlusPrompt = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        QuotedIdentifier = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        SingleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        QuotedOperator = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
    
    class Spice:
        Command = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        Comment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        Default = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        Delimiter = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Function = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        Identifier = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Number = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        Parameter = (data.current_editor_font_name, 0xff0040e0, data.current_editor_font_size, None)
        Value = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
    
    class TCL:
        Comment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        CommentBlock = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        CommentBox = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        CommentLine = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        Default = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        ExpandKeyword = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        ITCLKeyword = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        Identifier = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        KeywordSet6 = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        KeywordSet7 = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        KeywordSet8 = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        KeywordSet9 = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        Modifier = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        Number = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        Operator = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        QuotedKeyword = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        QuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        Substitution = (data.current_editor_font_name, 0xff7f7f00, data.current_editor_font_size, None)
        SubstitutionBrace = (data.current_editor_font_name, 0xff7f7f00, data.current_editor_font_size, None)
        TCLKeyword = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        TkCommand = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        TkKeyword = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
    
    class TeX:
        Command = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        Default = (data.current_editor_font_name, 0xff3f3f3f, data.current_editor_font_size, None)
        Group = (data.current_editor_font_name, 0xff7f0000, data.current_editor_font_size, None)
        Special = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        Symbol = (data.current_editor_font_name, 0xff7f7f00, data.current_editor_font_size, None)
        Text = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
    
    class VHDL:
        Attribute = (data.current_editor_font_name, 0xff804020, data.current_editor_font_size, None)
        Comment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        CommentLine = (data.current_editor_font_name, 0xff3f7f3f, data.current_editor_font_size, None)
        Default = (data.current_editor_font_name, 0xff800080, data.current_editor_font_size, None)
        Identifier = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Keyword = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        KeywordSet7 = (data.current_editor_font_name, 0xff804020, data.current_editor_font_size, None)
        Number = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        Operator = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        StandardFunction = (data.current_editor_font_name, 0xff808020, data.current_editor_font_size, None)
        StandardOperator = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        StandardPackage = (data.current_editor_font_name, 0xff208020, data.current_editor_font_size, None)
        StandardType = (data.current_editor_font_name, 0xff208080, data.current_editor_font_size, None)
        String = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        UnclosedString = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        CommentBlock = (data.current_editor_font_name, 0xff800080, data.current_editor_font_size, None)
    
    class Verilog:
        Comment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        CommentBang = (data.current_editor_font_name, 0xff3f7f3f, data.current_editor_font_size, None)
        CommentLine = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        Default = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        Identifier = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Keyword = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        KeywordSet2 = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        Number = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        Operator = (data.current_editor_font_name, 0xff007070, data.current_editor_font_size, None)
        Preprocessor = (data.current_editor_font_name, 0xff7f7f00, data.current_editor_font_size, None)
        String = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        SystemTask = (data.current_editor_font_name, 0xff804020, data.current_editor_font_size, None)
        UnclosedString = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        UserKeywordSet = (data.current_editor_font_name, 0xff2a00ff, data.current_editor_font_size, None)
        InactiveDefault = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        InactiveUnclosedString = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        InactiveCommentKeyword = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        InactiveKeywordSet2 = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        InactiveComment = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        DeclareInputOutputPort = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        InactiveString = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        CommentKeyword = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        DeclareOutputPort = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        PortConnection = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        InactiveKeyword = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        DeclareInputPort = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        InactiveDeclareInputPort = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        InactiveDeclareOutputPort = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        InactiveUserKeywordSet = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        InactiveCommentBang = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        InactiveIdentifier = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        InactivePortConnection = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        InactiveNumber = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        InactiveSystemTask = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        InactivePreprocessor = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        InactiveOperator = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        InactiveDeclareInputOutputPort = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        InactiveCommentLine = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
    
    class XML:
        ASPAtStart = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        ASPJavaScriptComment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        ASPJavaScriptCommentDoc = (data.current_editor_font_name, 0xff7f7f7f, data.current_editor_font_size, None)
        ASPJavaScriptCommentLine = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        ASPJavaScriptDefault = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        ASPJavaScriptDoubleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        ASPJavaScriptKeyword = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        ASPJavaScriptNumber = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        ASPJavaScriptRegex = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        ASPJavaScriptSingleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        ASPJavaScriptStart = (data.current_editor_font_name, 0xff7f7f00, data.current_editor_font_size, None)
        ASPJavaScriptSymbol = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        ASPJavaScriptUnclosedString = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        ASPJavaScriptWord = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        ASPPythonClassName = (data.current_editor_font_name, 0xff0000ff, data.current_editor_font_size, None)
        ASPPythonComment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        ASPPythonDefault = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        ASPPythonDoubleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        ASPPythonFunctionMethodName = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        ASPPythonIdentifier = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        ASPPythonKeyword = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        ASPPythonNumber = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        ASPPythonOperator = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        ASPPythonSingleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        ASPPythonStart = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        ASPPythonTripleDoubleQuotedString = (data.current_editor_font_name, 0xff7f0000, data.current_editor_font_size, None)
        ASPPythonTripleSingleQuotedString = (data.current_editor_font_name, 0xff7f0000, data.current_editor_font_size, None)
        ASPStart = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        ASPVBScriptComment = (data.current_editor_font_name, 0xff008000, data.current_editor_font_size, None)
        ASPVBScriptDefault = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        ASPVBScriptIdentifier = (data.current_editor_font_name, 0xff000080, data.current_editor_font_size, None)
        ASPVBScriptKeyword = (data.current_editor_font_name, 0xff000080, data.current_editor_font_size, None)
        ASPVBScriptNumber = (data.current_editor_font_name, 0xff008080, data.current_editor_font_size, None)
        ASPVBScriptStart = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        ASPVBScriptString = (data.current_editor_font_name, 0xff800080, data.current_editor_font_size, None)
        ASPVBScriptUnclosedString = (data.current_editor_font_name, 0xff000080, data.current_editor_font_size, None)
        ASPXCComment = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Attribute = (data.current_editor_font_name, 0xff008080, data.current_editor_font_size, None)
        CDATA = (data.current_editor_font_name, 0xff800000, data.current_editor_font_size, None)
        Default = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Entity = (data.current_editor_font_name, 0xff800080, data.current_editor_font_size, None)
        HTMLComment = (data.current_editor_font_name, 0xff808000, data.current_editor_font_size, None)
        HTMLDoubleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        HTMLNumber = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        HTMLSingleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        HTMLValue = (data.current_editor_font_name, 0xff608060, data.current_editor_font_size, None)
        JavaScriptComment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        JavaScriptCommentDoc = (data.current_editor_font_name, 0xff3f703f, data.current_editor_font_size, None)
        JavaScriptCommentLine = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        JavaScriptDefault = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        JavaScriptDoubleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        JavaScriptKeyword = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        JavaScriptNumber = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        JavaScriptRegex = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        JavaScriptSingleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        JavaScriptStart = (data.current_editor_font_name, 0xff7f7f00, data.current_editor_font_size, None)
        JavaScriptSymbol = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        JavaScriptUnclosedString = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        JavaScriptWord = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        OtherInTag = (data.current_editor_font_name, 0xff800080, data.current_editor_font_size, None)
        PHPComment = (data.current_editor_font_name, 0xff999999, data.current_editor_font_size, None)
        PHPCommentLine = (data.current_editor_font_name, 0xff666666, data.current_editor_font_size, None)
        PHPDefault = (data.current_editor_font_name, 0xff000033, data.current_editor_font_size, None)
        PHPDoubleQuotedString = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        PHPDoubleQuotedVariable = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        PHPKeyword = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        PHPNumber = (data.current_editor_font_name, 0xffcc9900, data.current_editor_font_size, None)
        PHPOperator = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        PHPSingleQuotedString = (data.current_editor_font_name, 0xff009f00, data.current_editor_font_size, None)
        PHPStart = (data.current_editor_font_name, 0xff800000, data.current_editor_font_size, None)
        PHPVariable = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        PythonClassName = (data.current_editor_font_name, 0xff0000ff, data.current_editor_font_size, None)
        PythonComment = (data.current_editor_font_name, 0xff007f00, data.current_editor_font_size, None)
        PythonDefault = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        PythonDoubleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        PythonFunctionMethodName = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        PythonIdentifier = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        PythonKeyword = (data.current_editor_font_name, 0xff00007f, data.current_editor_font_size, None)
        PythonNumber = (data.current_editor_font_name, 0xff007f7f, data.current_editor_font_size, None)
        PythonOperator = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        PythonSingleQuotedString = (data.current_editor_font_name, 0xff7f007f, data.current_editor_font_size, None)
        PythonStart = (data.current_editor_font_name, 0xff808080, data.current_editor_font_size, None)
        PythonTripleDoubleQuotedString = (data.current_editor_font_name, 0xff7f0000, data.current_editor_font_size, None)
        PythonTripleSingleQuotedString = (data.current_editor_font_name, 0xff7f0000, data.current_editor_font_size, None)
        SGMLBlockDefault = (data.current_editor_font_name, 0xff000066, data.current_editor_font_size, None)
        SGMLCommand = (data.current_editor_font_name, 0xff000080, data.current_editor_font_size, None)
        SGMLComment = (data.current_editor_font_name, 0xff808000, data.current_editor_font_size, None)
        SGMLDefault = (data.current_editor_font_name, 0xff000080, data.current_editor_font_size, None)
        SGMLDoubleQuotedString = (data.current_editor_font_name, 0xff800000, data.current_editor_font_size, None)
        SGMLEntity = (data.current_editor_font_name, 0xff333333, data.current_editor_font_size, None)
        SGMLError = (data.current_editor_font_name, 0xff800000, data.current_editor_font_size, None)
        SGMLParameter = (data.current_editor_font_name, 0xff006600, data.current_editor_font_size, None)
        SGMLParameterComment = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        SGMLSingleQuotedString = (data.current_editor_font_name, 0xff993300, data.current_editor_font_size, None)
        SGMLSpecial = (data.current_editor_font_name, 0xff3366ff, data.current_editor_font_size, None)
        Script = (data.current_editor_font_name, 0xff000080, data.current_editor_font_size, None)
        Tag = (data.current_editor_font_name, 0xff000080, data.current_editor_font_size, None)
        UnknownAttribute = (data.current_editor_font_name, 0xff008080, data.current_editor_font_size, None)
        UnknownTag = (data.current_editor_font_name, 0xff000080, data.current_editor_font_size, None)
        VBScriptComment = (data.current_editor_font_name, 0xff008000, data.current_editor_font_size, None)
        VBScriptDefault = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        VBScriptIdentifier = (data.current_editor_font_name, 0xff000080, data.current_editor_font_size, None)
        VBScriptKeyword = (data.current_editor_font_name, 0xff000080, data.current_editor_font_size, None)
        VBScriptNumber = (data.current_editor_font_name, 0xff008080, data.current_editor_font_size, None)
        VBScriptStart = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        VBScriptString = (data.current_editor_font_name, 0xff800080, data.current_editor_font_size, None)
        VBScriptUnclosedString = (data.current_editor_font_name, 0xff000080, data.current_editor_font_size, None)
        XMLEnd = (data.current_editor_font_name, 0xff800080, data.current_editor_font_size, None)
        XMLStart = (data.current_editor_font_name, 0xff800080, data.current_editor_font_size, None)
        XMLTagEnd = (data.current_editor_font_name, 0xff000080, data.current_editor_font_size, None)
    
    class YAML:
        Comment = (data.current_editor_font_name, 0xff008800, data.current_editor_font_size, None)
        Default = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        DocumentDelimiter = (data.current_editor_font_name, 0xffffffff, data.current_editor_font_size, None)
        Identifier = (data.current_editor_font_name, 0xff000088, data.current_editor_font_size, None)
        Keyword = (data.current_editor_font_name, 0xff880088, data.current_editor_font_size, None)
        Number = (data.current_editor_font_name, 0xff880000, data.current_editor_font_size, None)
        Operator = (data.current_editor_font_name, 0xff000000, data.current_editor_font_size, None)
        Reference = (data.current_editor_font_name, 0xff008888, data.current_editor_font_size, None)
        SyntaxErrorMarker = (data.current_editor_font_name, 0xffffffff, data.current_editor_font_size, None)
        TextBlockMarker = (data.current_editor_font_name, 0xff333366, data.current_editor_font_size, None)


class Paper:
    Default = data.QColor(0xffffffff)
    DefaultHtml = "#ffffffff"
    
    class Ada:
        Default = 0xffffffff
        Comment = 0xffffffff
        Keyword = 0xffffffff
        String = 0xffffffff
        Procedure = 0xffffffff
        Number = 0xffffffff
        Type = 0xffffffff
        Package = 0xffffffff
    
    class AWK:
        Default = 0xffffffff
        Comment = 0xffffffff
        Keyword = 0xffffffff
        BuiltInVariable = 0xffffffff
        BuiltInFunction = 0xffffffff
        String = 0xffffffff
        Number = 0xffffffff
        Operator = 0xffffffff
        
    class CiCode:
        Default = 0xffffffff
        Comment = 0xffffffff
        Keyword = 0xffffffff
        BuiltInVariable = 0xffffffff
        BuiltInFunction = 0xffffffff
        String = 0xffffffff
        Number = 0xffffffff
        Operator = 0xffffffff
    
    class Nim:
        Default = 0xffffffff
        Comment = 0xffffffff
        BasicKeyword = 0xffffffff
        TopKeyword = 0xffffffff
        String = 0xffffffff
        LongString = 0xffffffff
        Number = 0xffffffff
        Operator = 0xffffffff
        Unsafe = 0xffffffff
        Type = 0xffffffff
        DocumentationComment = 0xffffffff
        Definition = 0xffffffff
        Class = 0xffffffff
        KeywordOperator = 0xffffffff
        CharLiteral = 0xffffffff
        CaseOf = 0xffffffff
        UserKeyword = 0xffffffff
        MultilineComment = 0xffffffff
        MultilineDocumentation = 0xffffffff
        Pragma = 0xffffffff
    
    class RouterOS:
        Default = 0xffffffff
        Operator = 0xffffffff
        Comment = 0xffffffff
        Keyword1 = 0xffffffff
        Keyword2 = 0xffffffff
        Keyword3 = 0xffffffff
    
    class Oberon:
        Default = 0xffffffff
        Comment = 0xffffffff
        Keyword = 0xffffffff
        String = 0xffffffff
        Procedure = 0xffffffff
        Module = 0xffffffff
        Number = 0xffffffff
        Type = 0xffffffff
    
    
    # Generated
    class AVS:
        Function = 0xffffffff
        KeywordSet6 = 0xffffffff
        TripleString = 0xffffffff
        LineComment = 0xffffffff
        Plugin = 0xffffffff
        String = 0xffffffff
        ClipProperty = 0xffffffff
        Default = 0xffffffff
        Operator = 0xffffffff
        Number = 0xffffffff
        Filter = 0xffffffff
        Identifier = 0xffffffff
        NestedBlockComment = 0xffffffff
        Keyword = 0xffffffff
        BlockComment = 0xffffffff
    
    class Bash:
        Error = 0xffff0000
        Backticks = 0xffa08080
        SingleQuotedHereDocument = 0xffddd0dd
        Scalar = 0xffffe0e0
        HereDocumentDelimiter = 0xffddd0dd
        Comment = 0xffffffff
        SingleQuotedString = 0xffffffff
        Default = 0xffffffff
        Operator = 0xffffffff
        ParameterExpansion = 0xffffffe0
        Number = 0xffffffff
        Identifier = 0xffffffff
        Keyword = 0xffffffff
        DoubleQuotedString = 0xffffffff
    
    class Batch:
        Label = 0xff606060
        Default = 0xffffffff
        Keyword = 0xffffffff
        ExternalCommand = 0xffffffff
        Variable = 0xffffffff
        Comment = 0xffffffff
        HideCommandChar = 0xffffffff
        Operator = 0xffffffff
    
    class CMake:
        Function = 0xffffffff
        BlockForeach = 0xffffffff
        BlockWhile = 0xffffffff
        StringLeftQuote = 0xffeeeeee
        Label = 0xffffffff
        Comment = 0xffffffff
        BlockMacro = 0xffffffff
        StringRightQuote = 0xffeeeeee
        Default = 0xffffffff
        Number = 0xffffffff
        BlockIf = 0xffffffff
        Variable = 0xffffffff
        KeywordSet3 = 0xffffffff
        String = 0xffeeeeee
        StringVariable = 0xffeeeeee
    
    class CPP:
        CommentDocKeywordError = 0xffffffff
        InactiveRegex = 0xffe0f0e0
        InactivePreProcessorComment = 0xffffffff
        UUID = 0xffffffff
        InactiveVerbatimString = 0xffe0ffe0
        SingleQuotedString = 0xffffffff
        Operator = 0xffffffff
        InactiveOperator = 0xffffffff
        InactivePreProcessor = 0xffffffff
        UnclosedString = 0xffe0c0e0
        Identifier = 0xffffffff
        InactiveRawString = 0xffffffff
        PreProcessor = 0xffffffff
        KeywordSet2 = 0xffffffff
        InactiveUnclosedString = 0xffe0c0e0
        InactiveCommentLine = 0xffffffff
        InactiveNumber = 0xffffffff
        InactivePreProcessorCommentLineDoc = 0xffffffff
        Number = 0xffffffff
        InactiveUUID = 0xffffffff
        CommentDoc = 0xffffffff
        InactiveCommentDoc = 0xffffffff
        GlobalClass = 0xffffffff
        InactiveSingleQuotedString = 0xffffffff
        HashQuotedString = 0xffe7ffd7
        VerbatimString = 0xffe0ffe0
        InactiveHashQuotedString = 0xffffffff
        Regex = 0xffe0f0e0
        InactiveGlobalClass = 0xffffffff
        InactiveIdentifier = 0xffffffff
        CommentLineDoc = 0xffffffff
        TripleQuotedVerbatimString = 0xffe0ffe0
        InactiveKeywordSet2 = 0xffffffff
        InactiveCommentDocKeyword = 0xffffffff
        Keyword = 0xffffffff
        InactiveCommentLineDoc = 0xffffffff
        InactiveDefault = 0xffffffff
        InactiveCommentDocKeywordError = 0xffffffff
        InactiveTripleQuotedVerbatimString = 0xffffffff
        CommentDocKeyword = 0xffffffff
        InactiveDoubleQuotedString = 0xffffffff
        CommentLine = 0xffffffff
        Comment = 0xffffffff
        PreProcessorComment = 0xffffffff
        InactiveComment = 0xffffffff
        RawString = 0xfffff3ff
        Default = 0xffffffff
        PreProcessorCommentLineDoc = 0xffffffff
        DoubleQuotedString = 0xffffffff
        InactiveKeyword = 0xffffffff
        UserLiteral = 0xffffffff
        InactiveEscapeSequence = 0xffffffff
        EscapeSequence = 0xffffffff
        InactiveUserLiteral = 0xffffffff
        InactiveTaskMarker = 0xffffffff
        TaskMarker = 0xffffffff
    
    class CSS:
        Important = 0xffffffff
        CSS3Property = 0xffffffff
        Attribute = 0xffffffff
        Comment = 0xffffffff
        SingleQuotedString = 0xffffffff
        MediaRule = 0xffffffff
        AtRule = 0xffffffff
        UnknownPseudoClass = 0xffffffff
        PseudoClass = 0xffffffff
        Tag = 0xffffffff
        CSS2Property = 0xffffffff
        CSS1Property = 0xffffffff
        IDSelector = 0xffffffff
        ExtendedCSSProperty = 0xffffffff
        Variable = 0xffffffff
        ExtendedPseudoClass = 0xffffffff
        ClassSelector = 0xffffffff
        Default = 0xffffffff
        PseudoElement = 0xffffffff
        UnknownProperty = 0xffffffff
        Value = 0xffffffff
        ExtendedPseudoElement = 0xffffffff
        DoubleQuotedString = 0xffffffff
        Operator = 0xffffffff
    
    class CSharp:
        CommentDocKeywordError = 0xffffffff
        InactiveRegex = 0xffffffff
        InactivePreProcessorComment = 0xffffffff
        UUID = 0xffffffff
        InactiveVerbatimString = 0xffffffff
        SingleQuotedString = 0xffffffff
        Operator = 0xffffffff
        InactiveOperator = 0xffffffff
        InactivePreProcessor = 0xffffffff
        UnclosedString = 0xffffffff
        Identifier = 0xffffffff
        InactiveRawString = 0xffffffff
        PreProcessor = 0xffffffff
        KeywordSet2 = 0xffffffff
        InactiveUnclosedString = 0xffffffff
        InactiveCommentLine = 0xffffffff
        InactiveNumber = 0xffffffff
        InactivePreProcessorCommentLineDoc = 0xffffffff
        Number = 0xffffffff
        InactiveUUID = 0xffffffff
        CommentDoc = 0xffffffff
        InactiveCommentDoc = 0xffffffff
        GlobalClass = 0xffffffff
        InactiveSingleQuotedString = 0xffffffff
        HashQuotedString = 0xffffffff
        VerbatimString = 0xffe0ffe0
        InactiveHashQuotedString = 0xffffffff
        Regex = 0xffffffff
        InactiveGlobalClass = 0xffffffff
        InactiveIdentifier = 0xffffffff
        CommentLineDoc = 0xffffffff
        TripleQuotedVerbatimString = 0xffffffff
        InactiveKeywordSet2 = 0xffffffff
        InactiveCommentDocKeyword = 0xffffffff
        Keyword = 0xffffffff
        InactiveCommentLineDoc = 0xffffffff
        InactiveDefault = 0xffffffff
        InactiveCommentDocKeywordError = 0xffffffff
        InactiveTripleQuotedVerbatimString = 0xffffffff
        CommentDocKeyword = 0xffffffff
        InactiveDoubleQuotedString = 0xffffffff
        CommentLine = 0xffffffff
        Comment = 0xffffffff
        PreProcessorComment = 0xffffffff
        InactiveComment = 0xffffffff
        RawString = 0xffffffff
        Default = 0xffffffff
        PreProcessorCommentLineDoc = 0xffffffff
        DoubleQuotedString = 0xffffffff
        InactiveKeyword = 0xffffffff
        UserLiteral = 0xffffffff
        InactiveEscapeSequence = 0xffffffff
        EscapeSequence = 0xffffffff
        InactiveUserLiteral = 0xffffffff
        InactiveTaskMarker = 0xffffffff
        TaskMarker = 0xffffffff
    
    class CoffeeScript:
        UUID = 0xffffffff
        CommentDocKeywordError = 0xffffffff
        GlobalClass = 0xffffffff
        VerbatimString = 0xffe0ffe0
        SingleQuotedString = 0xffffffff
        Operator = 0xffffffff
        Number = 0xffffffff
        Identifier = 0xffffffff
        Keyword = 0xffffffff
        UnclosedString = 0xffe0c0e0
        Regex = 0xffe0f0e0
        CommentDocKeyword = 0xffffffff
        BlockRegex = 0xffffffff
        CommentLineDoc = 0xffffffff
        PreProcessor = 0xffffffff
        CommentLine = 0xffffffff
        CommentBlock = 0xffffffff
        Comment = 0xffffffff
        KeywordSet2 = 0xffffffff
        BlockRegexComment = 0xffffffff
        Default = 0xffffffff
        DoubleQuotedString = 0xffffffff
        CommentDoc = 0xffffffff
    
    class D:
        BackquoteString = 0xffffffff
        CommentDocKeywordError = 0xffffffff
        Operator = 0xffffffff
        CommentNested = 0xffffffff
        KeywordDoc = 0xffffffff
        KeywordSet7 = 0xffffffff
        Keyword = 0xffffffff
        KeywordSecondary = 0xffffffff
        Identifier = 0xffffffff
        KeywordSet5 = 0xffffffff
        CommentDocKeyword = 0xffffffff
        KeywordSet6 = 0xffffffff
        CommentLineDoc = 0xffffffff
        CommentLine = 0xffffffff
        Comment = 0xffffffff
        Typedefs = 0xffffffff
        Character = 0xffffffff
        RawString = 0xffffffff
        Default = 0xffffffff
        Number = 0xffffffff
        UnclosedString = 0xffe0c0e0
        String = 0xffffffff
        CommentDoc = 0xffffffff
    
    class Diff:
        Header = 0xffffffff
        LineChanged = 0xffffffff
        Default = 0xffffffff
        LineRemoved = 0xffffffff
        Command = 0xffffffff
        Position = 0xffffffff
        LineAdded = 0xffffffff
        Comment = 0xffffffff
    
    class Fortran:
        Label = 0xffffffff
        Identifier = 0xffffffff
        DottedOperator = 0xffffffff
        PreProcessor = 0xffffffff
        Comment = 0xffffffff
        SingleQuotedString = 0xffffffff
        Default = 0xffffffff
        DoubleQuotedString = 0xffffffff
        ExtendedFunction = 0xffffffff
        UnclosedString = 0xffe0c0e0
        Number = 0xffffffff
        Continuation = 0xfff0e080
        IntrinsicFunction = 0xffffffff
        Keyword = 0xffffffff
        Operator = 0xffffffff
    
    class Fortran77:
        Label = 0xffffffff
        Identifier = 0xffffffff
        DottedOperator = 0xffffffff
        PreProcessor = 0xffffffff
        Comment = 0xffffffff
        SingleQuotedString = 0xffffffff
        Default = 0xffffffff
        DoubleQuotedString = 0xffffffff
        ExtendedFunction = 0xffffffff
        UnclosedString = 0xffe0c0e0
        Number = 0xffffffff
        Continuation = 0xfff0e080
        IntrinsicFunction = 0xffffffff
        Keyword = 0xffffffff
        Operator = 0xffffffff
    
    class HTML:
        HTMLValue = 0xffffefff
        PythonDefault = 0xffefffef
        Entity = 0xffffffff
        SGMLParameter = 0xffefefff
        SGMLDefault = 0xffefefff
        PHPVariable = 0xfffff8f8
        SGMLCommand = 0xffefefff
        PythonClassName = 0xffefffef
        VBScriptUnclosedString = 0xff7f7fff
        ASPJavaScriptDefault = 0xffdfdf7f
        ASPVBScriptStart = 0xffffffff
        VBScriptDefault = 0xffefefff
        PythonNumber = 0xffefffef
        PythonOperator = 0xffefffef
        ASPJavaScriptSingleQuotedString = 0xffdfdf7f
        PHPDefault = 0xfffff8f8
        XMLStart = 0xffffffff
        PythonFunctionMethodName = 0xffefffef
        ASPJavaScriptStart = 0xffffffff
        JavaScriptWord = 0xfff0f0ff
        PHPSingleQuotedString = 0xfffff8f8
        PythonTripleDoubleQuotedString = 0xffefffef
        JavaScriptComment = 0xfff0f0ff
        Default = 0xffffffff
        SGMLSingleQuotedString = 0xffefefff
        VBScriptComment = 0xffefefff
        ASPVBScriptNumber = 0xffcfcfef
        ASPJavaScriptCommentDoc = 0xffdfdf7f
        PythonIdentifier = 0xffefffef
        VBScriptKeyword = 0xffefefff
        JavaScriptDefault = 0xfff0f0ff
        PythonStart = 0xffffffff
        ASPPythonComment = 0xffcfefcf
        ASPJavaScriptWord = 0xffdfdf7f
        SGMLParameterComment = 0xffffffff
        JavaScriptSingleQuotedString = 0xfff0f0ff
        PythonSingleQuotedString = 0xffefffef
        HTMLSingleQuotedString = 0xffffffff
        ASPVBScriptString = 0xffcfcfef
        SGMLBlockDefault = 0xffcccce0
        PythonKeyword = 0xffefffef
        XMLTagEnd = 0xffffffff
        ASPVBScriptComment = 0xffcfcfef
        ASPPythonSingleQuotedString = 0xffcfefcf
        PHPDoubleQuotedVariable = 0xfffff8f8
        ASPJavaScriptComment = 0xffdfdf7f
        JavaScriptUnclosedString = 0xffbfbbb0
        JavaScriptDoubleQuotedString = 0xfff0f0ff
        UnknownAttribute = 0xffffffff
        ASPPythonOperator = 0xffcfefcf
        ASPJavaScriptSymbol = 0xffdfdf7f
        ASPPythonFunctionMethodName = 0xffcfefcf
        SGMLDoubleQuotedString = 0xffefefff
        PHPOperator = 0xfffff8f8
        JavaScriptNumber = 0xfff0f0ff
        PythonDoubleQuotedString = 0xffefffef
        ASPAtStart = 0xffffff00
        Script = 0xffffffff
        PHPCommentLine = 0xfffff8f8
        SGMLComment = 0xffefefff
        JavaScriptStart = 0xffffffff
        ASPPythonIdentifier = 0xffcfefcf
        ASPVBScriptKeyword = 0xffcfcfef
        ASPPythonTripleDoubleQuotedString = 0xffcfefcf
        ASPPythonKeyword = 0xffcfefcf
        ASPJavaScriptNumber = 0xffdfdf7f
        PHPStart = 0xffffefbf
        PythonTripleSingleQuotedString = 0xffefffef
        PHPNumber = 0xfffff8f8
        ASPPythonDefault = 0xffcfefcf
        SGMLSpecial = 0xffefefff
        OtherInTag = 0xffffffff
        JavaScriptCommentDoc = 0xfff0f0ff
        Tag = 0xffffffff
        XMLEnd = 0xffffffff
        CDATA = 0xffffdf00
        HTMLNumber = 0xffffffff
        SGMLError = 0xffff6666
        PHPKeyword = 0xfffff8f8
        ASPVBScriptUnclosedString = 0xff7f7fff
        ASPPythonNumber = 0xffcfefcf
        VBScriptString = 0xffefefff
        ASPPythonClassName = 0xffcfefcf
        ASPPythonStart = 0xffffffff
        JavaScriptRegex = 0xffffbbb0
        ASPJavaScriptUnclosedString = 0xffbfbbb0
        ASPJavaScriptCommentLine = 0xffdfdf7f
        SGMLEntity = 0xffefefff
        ASPJavaScriptDoubleQuotedString = 0xffdfdf7f
        ASPStart = 0xffffdf00
        Attribute = 0xffffffff
        ASPJavaScriptKeyword = 0xffdfdf7f
        ASPVBScriptDefault = 0xffcfcfef
        ASPVBScriptIdentifier = 0xffcfcfef
        ASPJavaScriptRegex = 0xffffbbb0
        VBScriptNumber = 0xffefefff
        HTMLDoubleQuotedString = 0xffffffff
        ASPXCComment = 0xffffffff
        VBScriptStart = 0xffffffff
        PHPDoubleQuotedString = 0xfffff8f8
        PHPComment = 0xfffff8f8
        ASPPythonTripleSingleQuotedString = 0xffcfefcf
        ASPPythonDoubleQuotedString = 0xffcfefcf
        JavaScriptKeyword = 0xfff0f0ff
        JavaScriptSymbol = 0xfff0f0ff
        VBScriptIdentifier = 0xffefefff
        HTMLComment = 0xffffffff
        UnknownTag = 0xffffffff
        JavaScriptCommentLine = 0xfff0f0ff
        PythonComment = 0xffefffef
    
    class IDL:
        CommentDocKeywordError = 0xffffffff
        InactiveRegex = 0xffe0f0e0
        InactivePreProcessorComment = 0xffffffff
        UUID = 0xffffffff
        InactiveVerbatimString = 0xffe0ffe0
        SingleQuotedString = 0xffffffff
        Operator = 0xffffffff
        InactiveOperator = 0xffffffff
        InactivePreProcessor = 0xffffffff
        UnclosedString = 0xffe0c0e0
        Identifier = 0xffffffff
        InactiveRawString = 0xffffffff
        PreProcessor = 0xffffffff
        KeywordSet2 = 0xffffffff
        InactiveUnclosedString = 0xffe0c0e0
        InactiveCommentLine = 0xffffffff
        InactiveNumber = 0xffffffff
        InactivePreProcessorCommentLineDoc = 0xffffffff
        Number = 0xffffffff
        InactiveUUID = 0xffffffff
        CommentDoc = 0xffffffff
        InactiveCommentDoc = 0xffffffff
        GlobalClass = 0xffffffff
        InactiveSingleQuotedString = 0xffffffff
        HashQuotedString = 0xffe7ffd7
        VerbatimString = 0xffe0ffe0
        InactiveHashQuotedString = 0xffffffff
        Regex = 0xffe0f0e0
        InactiveGlobalClass = 0xffffffff
        InactiveIdentifier = 0xffffffff
        CommentLineDoc = 0xffffffff
        TripleQuotedVerbatimString = 0xffe0ffe0
        InactiveKeywordSet2 = 0xffffffff
        InactiveCommentDocKeyword = 0xffffffff
        Keyword = 0xffffffff
        InactiveCommentLineDoc = 0xffffffff
        InactiveDefault = 0xffffffff
        InactiveCommentDocKeywordError = 0xffffffff
        InactiveTripleQuotedVerbatimString = 0xffffffff
        CommentDocKeyword = 0xffffffff
        InactiveDoubleQuotedString = 0xffffffff
        CommentLine = 0xffffffff
        Comment = 0xffffffff
        PreProcessorComment = 0xffffffff
        InactiveComment = 0xffffffff
        RawString = 0xfffff3ff
        Default = 0xffffffff
        PreProcessorCommentLineDoc = 0xffffffff
        DoubleQuotedString = 0xffffffff
        InactiveKeyword = 0xffffffff
        UserLiteral = 0xffffffff
        InactiveEscapeSequence = 0xffffffff
        EscapeSequence = 0xffffffff
        InactiveUserLiteral = 0xffffffff
        InactiveTaskMarker = 0xffffffff
        TaskMarker = 0xffffffff
    
    class Java:
        CommentDocKeywordError = 0xffffffff
        InactiveRegex = 0xffe0f0e0
        InactivePreProcessorComment = 0xffffffff
        UUID = 0xffffffff
        InactiveVerbatimString = 0xffe0ffe0
        SingleQuotedString = 0xffffffff
        Operator = 0xffffffff
        InactiveOperator = 0xffffffff
        InactivePreProcessor = 0xffffffff
        UnclosedString = 0xffe0c0e0
        Identifier = 0xffffffff
        InactiveRawString = 0xffffffff
        PreProcessor = 0xffffffff
        KeywordSet2 = 0xffffffff
        InactiveUnclosedString = 0xffe0c0e0
        InactiveCommentLine = 0xffffffff
        InactiveNumber = 0xffffffff
        InactivePreProcessorCommentLineDoc = 0xffffffff
        Number = 0xffffffff
        InactiveUUID = 0xffffffff
        CommentDoc = 0xffffffff
        InactiveCommentDoc = 0xffffffff
        GlobalClass = 0xffffffff
        InactiveSingleQuotedString = 0xffffffff
        HashQuotedString = 0xffe7ffd7
        VerbatimString = 0xffe0ffe0
        InactiveHashQuotedString = 0xffffffff
        Regex = 0xffe0f0e0
        InactiveGlobalClass = 0xffffffff
        InactiveIdentifier = 0xffffffff
        CommentLineDoc = 0xffffffff
        TripleQuotedVerbatimString = 0xffe0ffe0
        InactiveKeywordSet2 = 0xffffffff
        InactiveCommentDocKeyword = 0xffffffff
        Keyword = 0xffffffff
        InactiveCommentLineDoc = 0xffffffff
        InactiveDefault = 0xffffffff
        InactiveCommentDocKeywordError = 0xffffffff
        InactiveTripleQuotedVerbatimString = 0xffffffff
        CommentDocKeyword = 0xffffffff
        InactiveDoubleQuotedString = 0xffffffff
        CommentLine = 0xffffffff
        Comment = 0xffffffff
        PreProcessorComment = 0xffffffff
        InactiveComment = 0xffffffff
        RawString = 0xfffff3ff
        Default = 0xffffffff
        PreProcessorCommentLineDoc = 0xffffffff
        DoubleQuotedString = 0xffffffff
        InactiveKeyword = 0xffffffff
        UserLiteral = 0xffffffff
        InactiveEscapeSequence = 0xffffffff
        EscapeSequence = 0xffffffff
        InactiveUserLiteral = 0xffffffff
        InactiveTaskMarker = 0xffffffff
        TaskMarker = 0xffffffff
    
    class JavaScript:
        CommentDocKeywordError = 0xffffffff
        InactiveRegex = 0xffffffff
        InactivePreProcessorComment = 0xffffffff
        UUID = 0xffffffff
        InactiveVerbatimString = 0xffffffff
        SingleQuotedString = 0xffffffff
        Operator = 0xffffffff
        InactiveOperator = 0xffffffff
        InactivePreProcessor = 0xffffffff
        UnclosedString = 0xffffffff
        Identifier = 0xffffffff
        InactiveRawString = 0xffffffff
        PreProcessor = 0xffffffff
        KeywordSet2 = 0xffffffff
        InactiveUnclosedString = 0xffffffff
        InactiveCommentLine = 0xffffffff
        InactiveNumber = 0xffffffff
        InactivePreProcessorCommentLineDoc = 0xffffffff
        Number = 0xffffffff
        InactiveUUID = 0xffffffff
        CommentDoc = 0xffffffff
        InactiveCommentDoc = 0xffffffff
        GlobalClass = 0xffffffff
        InactiveSingleQuotedString = 0xffffffff
        HashQuotedString = 0xffffffff
        VerbatimString = 0xffffffff
        InactiveHashQuotedString = 0xffffffff
        Regex = 0xffe0f0ff
        InactiveGlobalClass = 0xffffffff
        InactiveIdentifier = 0xffffffff
        CommentLineDoc = 0xffffffff
        TripleQuotedVerbatimString = 0xffffffff
        InactiveKeywordSet2 = 0xffffffff
        InactiveCommentDocKeyword = 0xffffffff
        Keyword = 0xffffffff
        InactiveCommentLineDoc = 0xffffffff
        InactiveDefault = 0xffffffff
        InactiveCommentDocKeywordError = 0xffffffff
        InactiveTripleQuotedVerbatimString = 0xffffffff
        CommentDocKeyword = 0xffffffff
        InactiveDoubleQuotedString = 0xffffffff
        CommentLine = 0xffffffff
        Comment = 0xffffffff
        PreProcessorComment = 0xffffffff
        InactiveComment = 0xffffffff
        RawString = 0xffffffff
        Default = 0xffffffff
        PreProcessorCommentLineDoc = 0xffffffff
        DoubleQuotedString = 0xffffffff
        InactiveKeyword = 0xffffffff
        UserLiteral = 0xffffffff
        InactiveEscapeSequence = 0xffffffff
        EscapeSequence = 0xffffffff
        InactiveUserLiteral = 0xffffffff
        InactiveTaskMarker = 0xffffffff
        TaskMarker = 0xffffffff
    
    class Lua:
        Label = 0xffffffff
        Identifier = 0xffffffff
        StringTableMathsFunctions = 0xffd0d0ff
        CoroutinesIOSystemFacilities = 0xffffd0d0
        KeywordSet5 = 0xffffffff
        KeywordSet6 = 0xffffffff
        Preprocessor = 0xffffffff
        LineComment = 0xffffffff
        Comment = 0xffd0f0f0
        String = 0xffffffff
        Character = 0xffffffff
        Default = 0xffffffff
        Operator = 0xffffffff
        LiteralString = 0xffe0ffff
        Number = 0xffffffff
        KeywordSet8 = 0xffffffff
        KeywordSet7 = 0xffffffff
        BasicFunctions = 0xffd0ffd0
        Keyword = 0xffffffff
        UnclosedString = 0xffe0c0e0
    
    class Makefile:
        Default = 0xffffffff
        Operator = 0xffffffff
        Target = 0xffffffff
        Preprocessor = 0xffffffff
        Variable = 0xffffffff
        Comment = 0xffffffff
        Error = 0xffff0000
    
    class Matlab:
        SingleQuotedString = 0xffffffff
        Default = 0xffffffff
        Keyword = 0xffffffff
        Number = 0xffffffff
        Command = 0xffffffff
        Identifier = 0xffffffff
        Comment = 0xffffffff
        DoubleQuotedString = 0xffffffff
        Operator = 0xffffffff
    
    class Octave:
        SingleQuotedString = 0xffffffff
        Default = 0xffffffff
        Keyword = 0xffffffff
        Number = 0xffffffff
        Command = 0xffffffff
        Identifier = 0xffffffff
        Comment = 0xffffffff
        DoubleQuotedString = 0xffffffff
        Operator = 0xffffffff
    
    class PO:
        ProgrammerComment = 0xffffffff
        Flags = 0xffffffff
        MessageContextText = 0xffffffff
        MessageStringTextEOL = 0xffffffff
        MessageId = 0xffffffff
        MessageIdText = 0xffffffff
        Reference = 0xffffffff
        Comment = 0xffffffff
        MessageStringText = 0xffffffff
        MessageContext = 0xffffffff
        Fuzzy = 0xffffffff
        Default = 0xffffffff
        MessageString = 0xffffffff
        MessageContextTextEOL = 0xffffffff
        MessageIdTextEOL = 0xffffffff
    
    class POV:
        KeywordSet7 = 0xffd0d0d0
        KeywordSet6 = 0xffd0ffd0
        PredefinedFunctions = 0xffd0d0ff
        CommentLine = 0xffffffff
        PredefinedIdentifiers = 0xffffffff
        Comment = 0xffffffff
        Directive = 0xffffffff
        String = 0xffffffff
        BadDirective = 0xffffffff
        TypesModifiersItems = 0xffffffd0
        Default = 0xffffffff
        Operator = 0xffffffff
        Number = 0xffffffff
        KeywordSet8 = 0xffe0e0e0
        Identifier = 0xffffffff
        ObjectsCSGAppearance = 0xffffd0d0
        UnclosedString = 0xffe0c0e0
    
    class Pascal:
        PreProcessorParenthesis = 0xffffffff
        SingleQuotedString = 0xffffffff
        PreProcessor = 0xffffffff
        CommentLine = 0xffffffff
        Comment = 0xffffffff
        CommentParenthesis = 0xffffffff
        Asm = 0xffffffff
        Character = 0xffffffff
        Default = 0xffffffff
        Operator = 0xffffffff
        UnclosedString = 0xffe0c0e0
        Number = 0xffffffff
        Identifier = 0xffffffff
        Keyword = 0xffffffff
        HexNumber = 0xffffffff
    
    class Perl:
        Translation = 0xfff0e080
        BacktickHereDocument = 0xffddd0dd
        Array = 0xffffffe0
        QuotedStringQXVar = 0xffa08080
        PODVerbatim = 0xffc0ffc0
        DoubleQuotedStringVar = 0xffffffff
        Regex = 0xffa0ffa0
        HereDocumentDelimiter = 0xffddd0dd
        SubroutinePrototype = 0xffffffff
        BacktickHereDocumentVar = 0xffddd0dd
        QuotedStringQR = 0xffffffff
        SingleQuotedString = 0xffffffff
        QuotedStringQRVar = 0xffffffff
        SubstitutionVar = 0xffffffff
        Operator = 0xffffffff
        DoubleQuotedHereDocumentVar = 0xffddd0dd
        Identifier = 0xffffffff
        QuotedStringQX = 0xffffffff
        BackticksVar = 0xffa08080
        Keyword = 0xffffffff
        QuotedStringQ = 0xffffffff
        QuotedStringQQVar = 0xffffffff
        QuotedStringQQ = 0xffffffff
        POD = 0xffe0ffe0
        FormatIdentifier = 0xffffffff
        RegexVar = 0xffffffff
        Backticks = 0xffa08080
        DoubleQuotedHereDocument = 0xffddd0dd
        Scalar = 0xffffe0e0
        FormatBody = 0xfffff0ff
        Comment = 0xffffffff
        QuotedStringQW = 0xffffffff
        SymbolTable = 0xffe0e0e0
        Default = 0xffffffff
        Error = 0xffff0000
        SingleQuotedHereDocument = 0xffddd0dd
        Number = 0xffffffff
        Hash = 0xffffe0ff
        Substitution = 0xfff0e080
        DataSection = 0xfffff0d8
        DoubleQuotedString = 0xffffffff
    
    class PostScript:
        DictionaryParenthesis = 0xffffffff
        HexString = 0xffffffff
        DSCCommentValue = 0xffffffff
        ProcedureParenthesis = 0xffffffff
        Comment = 0xffffffff
        ImmediateEvalLiteral = 0xffffffff
        Name = 0xffffffff
        DSCComment = 0xffffffff
        Default = 0xffffffff
        Base85String = 0xffffffff
        Number = 0xffffffff
        ArrayParenthesis = 0xffffffff
        Literal = 0xffffffff
        BadStringCharacter = 0xffff0000
        Text = 0xffffffff
        Keyword = 0xffffffff
    
    class Properties:
        DefaultValue = 0xffffffff
        Default = 0xffffffff
        Section = 0xffe0f0f0
        Assignment = 0xffffffff
        Key = 0xffffffff
        Comment = 0xffffffff
    
    class Python:
        TripleDoubleQuotedString = 0xffffffff
        FunctionMethodName = 0xffffffff
        TabsAfterSpaces = 0xffffffff
        Tabs = 0xffffffff
        Decorator = 0xffffffff
        NoWarning = 0xffffffff
        UnclosedString = 0xffe0c0e0
        Spaces = 0xffffffff
        CommentBlock = 0xffffffff
        Comment = 0xffffffff
        TripleSingleQuotedString = 0xffffffff
        SingleQuotedString = 0xffffffff
        Inconsistent = 0xffffffff
        Default = 0xffffffff
        DoubleQuotedString = 0xffffffff
        Operator = 0xffffffff
        Number = 0xffffffff
        Identifier = 0xffffffff
        ClassName = 0xffffffff
        Keyword = 0xffffffff
        HighlightedIdentifier = 0xffffffff
        CustomKeyword = 0xffffffff
    
    class Ruby:
        Symbol = 0xffffffff
        Stderr = 0xffff8080
        Global = 0xffffffff
        FunctionMethodName = 0xffffffff
        Stdin = 0xffff8080
        HereDocumentDelimiter = 0xffddd0dd
        PercentStringr = 0xffa0ffa0
        PercentStringQ = 0xffffffff
        ModuleName = 0xffffffff
        HereDocument = 0xffddd0dd
        SingleQuotedString = 0xffffffff
        PercentStringq = 0xffffffff
        Regex = 0xffa0ffa0
        Operator = 0xffffffff
        PercentStringw = 0xffffffe0
        PercentStringx = 0xffa08080
        POD = 0xffc0ffc0
        Keyword = 0xffffffff
        Stdout = 0xffff8080
        ClassVariable = 0xffffffff
        Identifier = 0xffffffff
        DemotedKeyword = 0xffffffff
        Backticks = 0xffa08080
        InstanceVariable = 0xffffffff
        Comment = 0xffffffff
        Default = 0xffffffff
        Error = 0xffff0000
        Number = 0xffffffff
        DataSection = 0xfffff0d8
        ClassName = 0xffffffff
        DoubleQuotedString = 0xffffffff
    
    class SQL:
        PlusComment = 0xffffffff
        KeywordSet7 = 0xffffffff
        PlusPrompt = 0xffe0ffe0
        CommentDocKeywordError = 0xffffffff
        CommentDocKeyword = 0xffffffff
        KeywordSet6 = 0xffffffff
        CommentLine = 0xffffffff
        Comment = 0xffffffff
        Operator = 0xffffffff
        QuotedIdentifier = 0xffffffff
        SingleQuotedString = 0xffffffff
        PlusKeyword = 0xffffffff
        Default = 0xffffffff
        DoubleQuotedString = 0xffffffff
        CommentLineHash = 0xffffffff
        KeywordSet5 = 0xffffffff
        Number = 0xffffffff
        KeywordSet8 = 0xffffffff
        Identifier = 0xffffffff
        Keyword = 0xffffffff
        CommentDoc = 0xffffffff
        QuotedOperator = 0xffffffff
    
    class Spice:
        Function = 0xffffffff
        Delimiter = 0xffffffff
        Value = 0xffffffff
        Default = 0xffffffff
        Number = 0xffffffff
        Parameter = 0xffffffff
        Command = 0xffffffff
        Identifier = 0xffffffff
        Comment = 0xffffffff
    
    class TCL:
        SubstitutionBrace = 0xffffffff
        CommentBox = 0xfff0fff0
        ITCLKeyword = 0xfffff0f0
        TkKeyword = 0xffe0fff0
        Operator = 0xffffffff
        QuotedString = 0xfffff0f0
        ExpandKeyword = 0xffffff80
        KeywordSet7 = 0xffffffff
        TCLKeyword = 0xffffffff
        TkCommand = 0xffffd0d0
        Identifier = 0xffffffff
        KeywordSet6 = 0xffffffff
        CommentLine = 0xffffffff
        CommentBlock = 0xfff0fff0
        Comment = 0xfff0ffe0
        Default = 0xffffffff
        KeywordSet9 = 0xffffffff
        Modifier = 0xffffffff
        Number = 0xffffffff
        KeywordSet8 = 0xffffffff
        Substitution = 0xffeffff0
        QuotedKeyword = 0xfffff0f0
    
    class TeX:
        Symbol = 0xffffffff
        Default = 0xffffffff
        Command = 0xffffffff
        Group = 0xffffffff
        Text = 0xffffffff
        Special = 0xffffffff
    
    class VHDL:
        StandardOperator = 0xffffffff
        Attribute = 0xffffffff
        CommentLine = 0xffffffff
        Comment = 0xffffffff
        String = 0xffffffff
        Default = 0xffffffff
        Operator = 0xffffffff
        StandardPackage = 0xffffffff
        Number = 0xffffffff
        Identifier = 0xffffffff
        KeywordSet7 = 0xffffffff
        StandardFunction = 0xffffffff
        StandardType = 0xffffffff
        Keyword = 0xffffffff
        UnclosedString = 0xffe0c0e0
        CommentBlock = 0xffffffff
    
    class Verilog:
        CommentBang = 0xffe0f0ff
        UserKeywordSet = 0xffffffff
        Preprocessor = 0xffffffff
        CommentLine = 0xffffffff
        Comment = 0xffffffff
        KeywordSet2 = 0xffffffff
        Default = 0xffffffff
        Operator = 0xffffffff
        Number = 0xffffffff
        Identifier = 0xffffffff
        SystemTask = 0xffffffff
        String = 0xffffffff
        Keyword = 0xffffffff
        UnclosedString = 0xffe0c0e0
        InactiveDefault = 0xffffffff
        InactiveUnclosedString = 0xffffffff
        InactiveCommentKeyword = 0xffffffff
        InactiveKeywordSet2 = 0xffffffff
        InactiveComment = 0xffffffff
        DeclareInputOutputPort = 0xffffffff
        InactiveString = 0xffffffff
        CommentKeyword = 0xffffffff
        DeclareOutputPort = 0xffffffff
        PortConnection = 0xffffffff
        InactiveKeyword = 0xffffffff
        DeclareInputPort = 0xffffffff
        InactiveDeclareInputPort = 0xffffffff
        InactiveDeclareOutputPort = 0xffffffff
        InactiveUserKeywordSet = 0xffffffff
        InactiveCommentBang = 0xffffffff
        InactiveIdentifier = 0xffffffff
        InactivePortConnection = 0xffffffff
        InactiveNumber = 0xffffffff
        InactiveSystemTask = 0xffffffff
        InactivePreprocessor = 0xffffffff
        InactiveOperator = 0xffffffff
        InactiveDeclareInputOutputPort = 0xffffffff
        InactiveCommentLine = 0xffffffff
    
    class XML:
        HTMLValue = 0xffffefff
        PythonDefault = 0xffefffef
        Entity = 0xffffffff
        SGMLParameter = 0xffefefff
        SGMLDefault = 0xffefefff
        PHPVariable = 0xfffff8f8
        SGMLCommand = 0xffefefff
        PythonClassName = 0xffefffef
        VBScriptUnclosedString = 0xff7f7fff
        ASPJavaScriptDefault = 0xffdfdf7f
        ASPVBScriptStart = 0xffffffff
        VBScriptDefault = 0xffefefff
        PythonNumber = 0xffefffef
        PythonOperator = 0xffefffef
        ASPJavaScriptSingleQuotedString = 0xffdfdf7f
        PHPDefault = 0xfffff8f8
        XMLStart = 0xffffffff
        PythonFunctionMethodName = 0xffefffef
        ASPJavaScriptStart = 0xffffffff
        JavaScriptWord = 0xfff0f0ff
        PHPSingleQuotedString = 0xfffff8f8
        PythonTripleDoubleQuotedString = 0xffefffef
        JavaScriptComment = 0xfff0f0ff
        Default = 0xffffffff
        SGMLSingleQuotedString = 0xffefefff
        VBScriptComment = 0xffefefff
        ASPVBScriptNumber = 0xffcfcfef
        ASPJavaScriptCommentDoc = 0xffdfdf7f
        PythonIdentifier = 0xffefffef
        VBScriptKeyword = 0xffefefff
        JavaScriptDefault = 0xfff0f0ff
        PythonStart = 0xffffffff
        ASPPythonComment = 0xffcfefcf
        ASPJavaScriptWord = 0xffdfdf7f
        SGMLParameterComment = 0xffffffff
        JavaScriptSingleQuotedString = 0xfff0f0ff
        PythonSingleQuotedString = 0xffefffef
        HTMLSingleQuotedString = 0xffffffff
        ASPVBScriptString = 0xffcfcfef
        SGMLBlockDefault = 0xffcccce0
        PythonKeyword = 0xffefffef
        XMLTagEnd = 0xffffffff
        ASPVBScriptComment = 0xffcfcfef
        ASPPythonSingleQuotedString = 0xffcfefcf
        PHPDoubleQuotedVariable = 0xfffff8f8
        ASPJavaScriptComment = 0xffdfdf7f
        JavaScriptUnclosedString = 0xffbfbbb0
        JavaScriptDoubleQuotedString = 0xfff0f0ff
        UnknownAttribute = 0xffffffff
        ASPPythonOperator = 0xffcfefcf
        ASPJavaScriptSymbol = 0xffdfdf7f
        ASPPythonFunctionMethodName = 0xffcfefcf
        SGMLDoubleQuotedString = 0xffefefff
        PHPOperator = 0xfffff8f8
        JavaScriptNumber = 0xfff0f0ff
        PythonDoubleQuotedString = 0xffefffef
        ASPAtStart = 0xffffff00
        Script = 0xffffffff
        PHPCommentLine = 0xfffff8f8
        SGMLComment = 0xffefefff
        JavaScriptStart = 0xffffffff
        ASPPythonIdentifier = 0xffcfefcf
        ASPVBScriptKeyword = 0xffcfcfef
        ASPPythonTripleDoubleQuotedString = 0xffcfefcf
        ASPPythonKeyword = 0xffcfefcf
        ASPJavaScriptNumber = 0xffdfdf7f
        PHPStart = 0xffffefbf
        PythonTripleSingleQuotedString = 0xffefffef
        PHPNumber = 0xfffff8f8
        ASPPythonDefault = 0xffcfefcf
        SGMLSpecial = 0xffefefff
        OtherInTag = 0xffffffff
        JavaScriptCommentDoc = 0xfff0f0ff
        Tag = 0xffffffff
        XMLEnd = 0xffffffff
        CDATA = 0xfffff0f0
        HTMLNumber = 0xffffffff
        SGMLError = 0xffff6666
        PHPKeyword = 0xfffff8f8
        ASPVBScriptUnclosedString = 0xff7f7fff
        ASPPythonNumber = 0xffcfefcf
        VBScriptString = 0xffefefff
        ASPPythonClassName = 0xffcfefcf
        ASPPythonStart = 0xffffffff
        JavaScriptRegex = 0xffffbbb0
        ASPJavaScriptUnclosedString = 0xffbfbbb0
        ASPJavaScriptCommentLine = 0xffdfdf7f
        SGMLEntity = 0xffefefff
        ASPJavaScriptDoubleQuotedString = 0xffdfdf7f
        ASPStart = 0xffffdf00
        Attribute = 0xffffffff
        ASPJavaScriptKeyword = 0xffdfdf7f
        ASPVBScriptDefault = 0xffcfcfef
        ASPVBScriptIdentifier = 0xffcfcfef
        ASPJavaScriptRegex = 0xffffbbb0
        VBScriptNumber = 0xffefefff
        HTMLDoubleQuotedString = 0xffffffff
        ASPXCComment = 0xffffffff
        VBScriptStart = 0xffffffff
        PHPDoubleQuotedString = 0xfffff8f8
        PHPComment = 0xfffff8f8
        ASPPythonTripleSingleQuotedString = 0xffcfefcf
        ASPPythonDoubleQuotedString = 0xffcfefcf
        JavaScriptKeyword = 0xfff0f0ff
        JavaScriptSymbol = 0xfff0f0ff
        VBScriptIdentifier = 0xffefefff
        HTMLComment = 0xffffffff
        UnknownTag = 0xffffffff
        JavaScriptCommentLine = 0xfff0f0ff
        PythonComment = 0xffefffef
    
    class YAML:
        TextBlockMarker = 0xffffffff
        DocumentDelimiter = 0xff000088
        Operator = 0xffffffff
        Number = 0xffffffff
        Default = 0xffffffff
        Identifier = 0xffffffff
        Reference = 0xffffffff
        Comment = 0xffffffff
        Keyword = 0xffffffff
        SyntaxErrorMarker = 0xffff0000
    




