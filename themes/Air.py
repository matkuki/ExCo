
# -*- coding: utf-8 -*-

"""
    Ex.Co. LICENSE :
        This file is part of Ex.Co..

        Ex.Co. is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        Ex.Co. is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with Ex.Co..  If not, see <http://www.gnu.org/licenses/>.


    PYTHON LICENSE :
        "Python" and the Python logos are trademarks or registered trademarks of the Python Software Foundation,
        used by Ex.Co. with permission from the Foundation


    Cython LICENSE:
        Cython is freely available under the open source Apache License


    PyQt4 LICENSE :
        PyQt4 is licensed under the GNU General Public License version 3
    PyQt Alternative Logo LICENSE:
        The PyQt Alternative Logo is licensed under Creative Commons CC0 1.0 Universal Public Domain Dedication


    Qt Logo LICENSE:
        The Qt logo is copyright of Digia Plc and/or its subsidiaries.
        Digia, Qt and their respective logos are trademarks of Digia Corporation in Finland and/or other countries worldwide.


    Tango Icons LICENSE:
        The Tango base icon theme is released to the Public Domain.
        The Tango base icon theme is made possible by the Tango Desktop Project.
    
    My Tango Style Icons LICENSE:
        The Tango icons I created are released under the GNU General Public License version 3.
    
    
    Eric6 LICENSE:
        Eric6 IDE is licensed under the GNU General Public License version 3


    Nuitka LICENSE:
        Nuitka is a Python compiler compatible with Ex.Co..
        Nuitka is freely available under the open source Apache License.
"""

##  FILE DESCRIPTION:
##      Air theme (Default system form color with white backgrounds and dark text)

import PyQt4.QtGui


Form = "#f0f0f0"
Cursor = PyQt4.QtGui.QColor(0x00, 0x00, 0x00)


class FoldMargin:
    ForeGround = PyQt4.QtGui.QColor(0x000000)
    BackGround = PyQt4.QtGui.QColor(0x000000)


class LineMargin:
    ForeGround = PyQt4.QtGui.QColor(0x000000)
    BackGround = PyQt4.QtGui.QColor(0xe0e0e0)


class Indication:
    Font = "#000000"
    ActiveBackGround = "#ffffff"
    ActiveBorder = "#204a87"
    PassiveBackGround = "#f0f0f0"
    PassiveBorder = "#a0a0a0"

    
class Font:
    Default = PyQt4.QtGui.QColor(0xff000000)
    
    class Ada:
        Default = 0xff000000
        Comment = 0xff007f00
        Keyword = 0xff00007f
        String = 0xff7f007f
        Procedure = 0xff0000ff
        Number = 0xff007f7f
        Type = 0xff00007f
        Package = 0xff7f0000
    
    class Nim:
        Default = 0xff000000
        Comment = 0xff007f00
        BasicKeyword = 0xff00007f
        TopKeyword = 0xff407fc0
        String = 0xff7f007f
        LongString = 0xff7f0000
        Number = 0xff007f7f
        Operator = 0xff7f7f7f
        Unsafe = 0xffc00000
        Type = 0xff6e6e00
        DocumentationComment = 0xff7f0a0a
        Definition = 0xff007f7f
        Class = 0xff0000ff
        KeywordOperator = 0xff963cc8
        CharLiteral = 0xff00c8ff
        CaseOf = 0xff8000ff
        UserKeyword = 0xffff8040
        MultilineComment = 0xff006c6c
        MultilineDocumentation = 0xff6e3296
        Pragma = 0xffc07f40
    
    class Oberon:
        Default = 0xff000000
        Comment = 0xff007f00
        Keyword = 0xff00007f
        String = 0xff7f007f
        Procedure = 0xff0000ff
        Module = 0xff7f0000
        Number = 0xff007f7f
        Type = 0xff00007f
    
    
    # Generated
    class AVS:
        BlockComment = 0xff007f00
        ClipProperty = 0xff00007f
        Default = 0xff000000
        Filter = 0xff00007f
        Function = 0xff007f7f
        Identifier = 0xff000000
        Keyword = 0xff00007f
        KeywordSet6 = 0xff8000ff
        LineComment = 0xff007f00
        NestedBlockComment = 0xff007f00
        Number = 0xff007f7f
        Operator = 0xff000000
        Plugin = 0xff0080c0
        String = 0xff7f007f
        TripleString = 0xff7f007f
    
    class Bash:
        Backticks = 0xffffff00
        Comment = 0xff007f00
        Default = 0xff808080
        DoubleQuotedString = 0xff7f007f
        Error = 0xffffff00
        HereDocumentDelimiter = 0xff000000
        Identifier = 0xff000000
        Keyword = 0xff00007f
        Number = 0xff007f7f
        Operator = 0xff000000
        ParameterExpansion = 0xff000000
        Scalar = 0xff000000
        SingleQuotedHereDocument = 0xff7f007f
        SingleQuotedString = 0xff7f007f
    
    class Batch:
        Comment = 0xff007f00
        Default = 0xff000000
        ExternalCommand = 0xff00007f
        HideCommandChar = 0xff7f7f00
        Keyword = 0xff00007f
        Label = 0xff7f007f
        Operator = 0xff000000
        Variable = 0xff800080
    
    class CMake:
        BlockForeach = 0xff00007f
        BlockIf = 0xff00007f
        BlockMacro = 0xff00007f
        BlockWhile = 0xff00007f
        Comment = 0xff007f00
        Default = 0xff000000
        Function = 0xff00007f
        KeywordSet3 = 0xff000000
        Label = 0xffcc3300
        Number = 0xff007f7f
        String = 0xff7f007f
        StringLeftQuote = 0xff7f007f
        StringRightQuote = 0xff7f007f
        StringVariable = 0xffcc3300
        Variable = 0xff800000
    
    class CPP:
        Comment = 0xff007f00
        CommentDoc = 0xff3f703f
        CommentDocKeyword = 0xff3060a0
        CommentDocKeywordError = 0xff804020
        CommentLine = 0xff007f00
        CommentLineDoc = 0xff3f703f
        Default = 0xff808080
        DoubleQuotedString = 0xff7f007f
        GlobalClass = 0xff000000
        HashQuotedString = 0xff007f00
        Identifier = 0xff000000
        InactiveComment = 0xff90b090
        InactiveCommentDoc = 0xffd0d0d0
        InactiveCommentDocKeyword = 0xffc0c0c0
        InactiveCommentDocKeywordError = 0xffc0c0c0
        InactiveCommentLine = 0xff90b090
        InactiveCommentLineDoc = 0xffc0c0c0
        InactiveDefault = 0xffc0c0c0
        InactiveDoubleQuotedString = 0xffb090b0
        InactiveGlobalClass = 0xffb0b0b0
        InactiveHashQuotedString = 0xff000000
        InactiveIdentifier = 0xffb0b0b0
        InactiveKeyword = 0xff9090b0
        InactiveKeywordSet2 = 0xffc0c0c0
        InactiveNumber = 0xff90b090
        InactiveOperator = 0xffb0b0b0
        InactivePreProcessor = 0xffb0b090
        InactivePreProcessorComment = 0xff000000
        InactivePreProcessorCommentLineDoc = 0xffc0c0c0
        InactiveRawString = 0xff000000
        InactiveRegex = 0xff7faf7f
        InactiveSingleQuotedString = 0xffb090b0
        InactiveTripleQuotedVerbatimString = 0xff000000
        InactiveUUID = 0xffc0c0c0
        InactiveUnclosedString = 0xff000000
        InactiveVerbatimString = 0xff90b090
        Keyword = 0xff00007f
        KeywordSet2 = 0xff000000
        Number = 0xff007f7f
        Operator = 0xff000000
        PreProcessor = 0xff7f7f00
        PreProcessorComment = 0xff659900
        PreProcessorCommentLineDoc = 0xff3f703f
        RawString = 0xff7f007f
        Regex = 0xff3f7f3f
        SingleQuotedString = 0xff7f007f
        TripleQuotedVerbatimString = 0xff007f00
        UUID = 0xff000000
        UnclosedString = 0xff000000
        VerbatimString = 0xff007f00
    
    class CSS:
        AtRule = 0xff7f7f00
        Attribute = 0xff800000
        CSS1Property = 0xff0040e0
        CSS2Property = 0xff00a0e0
        CSS3Property = 0xff000000
        ClassSelector = 0xff000000
        Comment = 0xff007f00
        Default = 0xffff0080
        DoubleQuotedString = 0xff7f007f
        ExtendedCSSProperty = 0xff000000
        ExtendedPseudoClass = 0xff000000
        ExtendedPseudoElement = 0xff000000
        IDSelector = 0xff007f7f
        Important = 0xffff8000
        MediaRule = 0xff7f7f00
        Operator = 0xff000000
        PseudoClass = 0xff800000
        PseudoElement = 0xff000000
        SingleQuotedString = 0xff7f007f
        Tag = 0xff00007f
        UnknownProperty = 0xffff0000
        UnknownPseudoClass = 0xffff0000
        Value = 0xff7f007f
        Variable = 0xff000000
    
    class CSharp:
        Comment = 0xff007f00
        CommentDoc = 0xff3f703f
        CommentDocKeyword = 0xff3060a0
        CommentDocKeywordError = 0xff804020
        CommentLine = 0xff007f00
        CommentLineDoc = 0xff3f703f
        Default = 0xff808080
        DoubleQuotedString = 0xff7f007f
        GlobalClass = 0xff000000
        HashQuotedString = 0xff007f00
        Identifier = 0xff000000
        InactiveComment = 0xff90b090
        InactiveCommentDoc = 0xffd0d0d0
        InactiveCommentDocKeyword = 0xffc0c0c0
        InactiveCommentDocKeywordError = 0xffc0c0c0
        InactiveCommentLine = 0xff90b090
        InactiveCommentLineDoc = 0xffc0c0c0
        InactiveDefault = 0xffc0c0c0
        InactiveDoubleQuotedString = 0xffb090b0
        InactiveGlobalClass = 0xffb0b0b0
        InactiveHashQuotedString = 0xff000000
        InactiveIdentifier = 0xffb0b0b0
        InactiveKeyword = 0xff9090b0
        InactiveKeywordSet2 = 0xffc0c0c0
        InactiveNumber = 0xff90b090
        InactiveOperator = 0xffb0b0b0
        InactivePreProcessor = 0xffb0b090
        InactivePreProcessorComment = 0xff000000
        InactivePreProcessorCommentLineDoc = 0xffc0c0c0
        InactiveRawString = 0xff000000
        InactiveRegex = 0xff7faf7f
        InactiveSingleQuotedString = 0xffb090b0
        InactiveTripleQuotedVerbatimString = 0xff000000
        InactiveUUID = 0xffc0c0c0
        InactiveUnclosedString = 0xff000000
        InactiveVerbatimString = 0xff90b090
        Keyword = 0xff00007f
        KeywordSet2 = 0xff000000
        Number = 0xff007f7f
        Operator = 0xff000000
        PreProcessor = 0xff7f7f00
        PreProcessorComment = 0xff659900
        PreProcessorCommentLineDoc = 0xff3f703f
        RawString = 0xff7f007f
        Regex = 0xff3f7f3f
        SingleQuotedString = 0xff7f007f
        TripleQuotedVerbatimString = 0xff007f00
        UUID = 0xff000000
        UnclosedString = 0xff000000
        VerbatimString = 0xff007f00
    
    class CoffeeScript:
        BlockRegex = 0xff3f7f3f
        BlockRegexComment = 0xff007f00
        Comment = 0xff007f00
        CommentBlock = 0xff007f00
        CommentDoc = 0xff3f703f
        CommentDocKeyword = 0xff3060a0
        CommentDocKeywordError = 0xff804020
        CommentLine = 0xff007f00
        CommentLineDoc = 0xff3f703f
        Default = 0xff808080
        DoubleQuotedString = 0xff7f007f
        GlobalClass = 0xff000000
        Identifier = 0xff000000
        Keyword = 0xff00007f
        KeywordSet2 = 0xff000000
        Number = 0xff007f7f
        Operator = 0xff000000
        PreProcessor = 0xff7f7f00
        Regex = 0xff3f7f3f
        SingleQuotedString = 0xff7f007f
        UUID = 0xff000000
        UnclosedString = 0xff000000
        VerbatimString = 0xff007f00
    
    class D:
        BackquoteString = 0xff000000
        Character = 0xff7f007f
        Comment = 0xff007f00
        CommentDoc = 0xff3f703f
        CommentDocKeyword = 0xff3060a0
        CommentDocKeywordError = 0xff804020
        CommentLine = 0xff007f00
        CommentLineDoc = 0xff3f703f
        CommentNested = 0xffa0c0a0
        Default = 0xff808080
        Identifier = 0xff000000
        Keyword = 0xff00007f
        KeywordDoc = 0xff00007f
        KeywordSecondary = 0xff00007f
        KeywordSet5 = 0xff000000
        KeywordSet6 = 0xff000000
        KeywordSet7 = 0xff000000
        Number = 0xff007f7f
        Operator = 0xff000000
        RawString = 0xff000000
        String = 0xff7f007f
        Typedefs = 0xff00007f
        UnclosedString = 0xff000000
    
    class Diff:
        Command = 0xff7f7f00
        Comment = 0xff007f00
        Default = 0xff000000
        Header = 0xff7f0000
        LineAdded = 0xff00007f
        LineChanged = 0xff7f7f7f
        LineRemoved = 0xff007f7f
        Position = 0xff7f007f
    
    class Fortran:
        Comment = 0xff007f00
        Continuation = 0xff000000
        Default = 0xff808080
        DottedOperator = 0xff000000
        DoubleQuotedString = 0xff7f007f
        ExtendedFunction = 0xffb04080
        Identifier = 0xff000000
        IntrinsicFunction = 0xffb00040
        Keyword = 0xff00007f
        Label = 0xffe0c0e0
        Number = 0xff007f7f
        Operator = 0xff000000
        PreProcessor = 0xff7f7f00
        SingleQuotedString = 0xff7f007f
        UnclosedString = 0xff000000
    
    class Fortran77:
        Comment = 0xff007f00
        Continuation = 0xff000000
        Default = 0xff808080
        DottedOperator = 0xff000000
        DoubleQuotedString = 0xff7f007f
        ExtendedFunction = 0xffb04080
        Identifier = 0xff000000
        IntrinsicFunction = 0xffb00040
        Keyword = 0xff00007f
        Label = 0xffe0c0e0
        Number = 0xff007f7f
        Operator = 0xff000000
        PreProcessor = 0xff7f7f00
        SingleQuotedString = 0xff7f007f
        UnclosedString = 0xff000000
    
    class HTML:
        ASPAtStart = 0xff000000
        ASPJavaScriptComment = 0xff007f00
        ASPJavaScriptCommentDoc = 0xff7f7f7f
        ASPJavaScriptCommentLine = 0xff007f00
        ASPJavaScriptDefault = 0xff000000
        ASPJavaScriptDoubleQuotedString = 0xff7f007f
        ASPJavaScriptKeyword = 0xff00007f
        ASPJavaScriptNumber = 0xff007f7f
        ASPJavaScriptRegex = 0xff000000
        ASPJavaScriptSingleQuotedString = 0xff7f007f
        ASPJavaScriptStart = 0xff7f7f00
        ASPJavaScriptSymbol = 0xff000000
        ASPJavaScriptUnclosedString = 0xff000000
        ASPJavaScriptWord = 0xff000000
        ASPPythonClassName = 0xff0000ff
        ASPPythonComment = 0xff007f00
        ASPPythonDefault = 0xff808080
        ASPPythonDoubleQuotedString = 0xff7f007f
        ASPPythonFunctionMethodName = 0xff007f7f
        ASPPythonIdentifier = 0xff000000
        ASPPythonKeyword = 0xff00007f
        ASPPythonNumber = 0xff007f7f
        ASPPythonOperator = 0xff000000
        ASPPythonSingleQuotedString = 0xff7f007f
        ASPPythonStart = 0xff808080
        ASPPythonTripleDoubleQuotedString = 0xff7f0000
        ASPPythonTripleSingleQuotedString = 0xff7f0000
        ASPStart = 0xff000000
        ASPVBScriptComment = 0xff008000
        ASPVBScriptDefault = 0xff000000
        ASPVBScriptIdentifier = 0xff000080
        ASPVBScriptKeyword = 0xff000080
        ASPVBScriptNumber = 0xff008080
        ASPVBScriptStart = 0xff000000
        ASPVBScriptString = 0xff800080
        ASPVBScriptUnclosedString = 0xff000080
        ASPXCComment = 0xff000000
        Attribute = 0xff008080
        CDATA = 0xff000000
        Default = 0xff000000
        Entity = 0xff800080
        HTMLComment = 0xff808000
        HTMLDoubleQuotedString = 0xff7f007f
        HTMLNumber = 0xff007f7f
        HTMLSingleQuotedString = 0xff7f007f
        HTMLValue = 0xffff00ff
        JavaScriptComment = 0xff007f00
        JavaScriptCommentDoc = 0xff3f703f
        JavaScriptCommentLine = 0xff007f00
        JavaScriptDefault = 0xff000000
        JavaScriptDoubleQuotedString = 0xff7f007f
        JavaScriptKeyword = 0xff00007f
        JavaScriptNumber = 0xff007f7f
        JavaScriptRegex = 0xff000000
        JavaScriptSingleQuotedString = 0xff7f007f
        JavaScriptStart = 0xff7f7f00
        JavaScriptSymbol = 0xff000000
        JavaScriptUnclosedString = 0xff000000
        JavaScriptWord = 0xff000000
        OtherInTag = 0xff800080
        PHPComment = 0xff999999
        PHPCommentLine = 0xff666666
        PHPDefault = 0xff000033
        PHPDoubleQuotedString = 0xff007f00
        PHPDoubleQuotedVariable = 0xff00007f
        PHPKeyword = 0xff7f007f
        PHPNumber = 0xffcc9900
        PHPOperator = 0xff000000
        PHPSingleQuotedString = 0xff009f00
        PHPStart = 0xff0000ff
        PHPVariable = 0xff00007f
        PythonClassName = 0xff0000ff
        PythonComment = 0xff007f00
        PythonDefault = 0xff808080
        PythonDoubleQuotedString = 0xff7f007f
        PythonFunctionMethodName = 0xff007f7f
        PythonIdentifier = 0xff000000
        PythonKeyword = 0xff00007f
        PythonNumber = 0xff007f7f
        PythonOperator = 0xff000000
        PythonSingleQuotedString = 0xff7f007f
        PythonStart = 0xff808080
        PythonTripleDoubleQuotedString = 0xff7f0000
        PythonTripleSingleQuotedString = 0xff7f0000
        SGMLBlockDefault = 0xff000066
        SGMLCommand = 0xff000080
        SGMLComment = 0xff808000
        SGMLDefault = 0xff000080
        SGMLDoubleQuotedString = 0xff800000
        SGMLEntity = 0xff333333
        SGMLError = 0xff800000
        SGMLParameter = 0xff006600
        SGMLParameterComment = 0xff000000
        SGMLSingleQuotedString = 0xff993300
        SGMLSpecial = 0xff3366ff
        Script = 0xff000080
        Tag = 0xff000080
        UnknownAttribute = 0xffff0000
        UnknownTag = 0xffff0000
        VBScriptComment = 0xff008000
        VBScriptDefault = 0xff000000
        VBScriptIdentifier = 0xff000080
        VBScriptKeyword = 0xff000080
        VBScriptNumber = 0xff008080
        VBScriptStart = 0xff000000
        VBScriptString = 0xff800080
        VBScriptUnclosedString = 0xff000080
        XMLEnd = 0xff0000ff
        XMLStart = 0xff0000ff
        XMLTagEnd = 0xff000080
    
    class IDL:
        Comment = 0xff007f00
        CommentDoc = 0xff3f703f
        CommentDocKeyword = 0xff3060a0
        CommentDocKeywordError = 0xff804020
        CommentLine = 0xff007f00
        CommentLineDoc = 0xff3f703f
        Default = 0xff808080
        DoubleQuotedString = 0xff7f007f
        GlobalClass = 0xff000000
        HashQuotedString = 0xff007f00
        Identifier = 0xff000000
        InactiveComment = 0xff90b090
        InactiveCommentDoc = 0xffd0d0d0
        InactiveCommentDocKeyword = 0xffc0c0c0
        InactiveCommentDocKeywordError = 0xffc0c0c0
        InactiveCommentLine = 0xff90b090
        InactiveCommentLineDoc = 0xffc0c0c0
        InactiveDefault = 0xffc0c0c0
        InactiveDoubleQuotedString = 0xffb090b0
        InactiveGlobalClass = 0xffb0b0b0
        InactiveHashQuotedString = 0xff000000
        InactiveIdentifier = 0xffb0b0b0
        InactiveKeyword = 0xff9090b0
        InactiveKeywordSet2 = 0xffc0c0c0
        InactiveNumber = 0xff90b090
        InactiveOperator = 0xffb0b0b0
        InactivePreProcessor = 0xffb0b090
        InactivePreProcessorComment = 0xff000000
        InactivePreProcessorCommentLineDoc = 0xffc0c0c0
        InactiveRawString = 0xff000000
        InactiveRegex = 0xff7faf7f
        InactiveSingleQuotedString = 0xffb090b0
        InactiveTripleQuotedVerbatimString = 0xff000000
        InactiveUUID = 0xffc0c0c0
        InactiveUnclosedString = 0xff000000
        InactiveVerbatimString = 0xff90b090
        Keyword = 0xff00007f
        KeywordSet2 = 0xff000000
        Number = 0xff007f7f
        Operator = 0xff000000
        PreProcessor = 0xff7f7f00
        PreProcessorComment = 0xff659900
        PreProcessorCommentLineDoc = 0xff3f703f
        RawString = 0xff7f007f
        Regex = 0xff3f7f3f
        SingleQuotedString = 0xff7f007f
        TripleQuotedVerbatimString = 0xff007f00
        UUID = 0xff804080
        UnclosedString = 0xff000000
        VerbatimString = 0xff007f00
    
    class Java:
        Comment = 0xff007f00
        CommentDoc = 0xff3f703f
        CommentDocKeyword = 0xff3060a0
        CommentDocKeywordError = 0xff804020
        CommentLine = 0xff007f00
        CommentLineDoc = 0xff3f703f
        Default = 0xff808080
        DoubleQuotedString = 0xff7f007f
        GlobalClass = 0xff000000
        HashQuotedString = 0xff007f00
        Identifier = 0xff000000
        InactiveComment = 0xff90b090
        InactiveCommentDoc = 0xffd0d0d0
        InactiveCommentDocKeyword = 0xffc0c0c0
        InactiveCommentDocKeywordError = 0xffc0c0c0
        InactiveCommentLine = 0xff90b090
        InactiveCommentLineDoc = 0xffc0c0c0
        InactiveDefault = 0xffc0c0c0
        InactiveDoubleQuotedString = 0xffb090b0
        InactiveGlobalClass = 0xffb0b0b0
        InactiveHashQuotedString = 0xff000000
        InactiveIdentifier = 0xffb0b0b0
        InactiveKeyword = 0xff9090b0
        InactiveKeywordSet2 = 0xffc0c0c0
        InactiveNumber = 0xff90b090
        InactiveOperator = 0xffb0b0b0
        InactivePreProcessor = 0xffb0b090
        InactivePreProcessorComment = 0xff000000
        InactivePreProcessorCommentLineDoc = 0xffc0c0c0
        InactiveRawString = 0xff000000
        InactiveRegex = 0xff7faf7f
        InactiveSingleQuotedString = 0xffb090b0
        InactiveTripleQuotedVerbatimString = 0xff000000
        InactiveUUID = 0xffc0c0c0
        InactiveUnclosedString = 0xff000000
        InactiveVerbatimString = 0xff90b090
        Keyword = 0xff00007f
        KeywordSet2 = 0xff000000
        Number = 0xff007f7f
        Operator = 0xff000000
        PreProcessor = 0xff7f7f00
        PreProcessorComment = 0xff659900
        PreProcessorCommentLineDoc = 0xff3f703f
        RawString = 0xff7f007f
        Regex = 0xff3f7f3f
        SingleQuotedString = 0xff7f007f
        TripleQuotedVerbatimString = 0xff007f00
        UUID = 0xff000000
        UnclosedString = 0xff000000
        VerbatimString = 0xff007f00
    
    class JavaScript:
        Comment = 0xff007f00
        CommentDoc = 0xff3f703f
        CommentDocKeyword = 0xff3060a0
        CommentDocKeywordError = 0xff804020
        CommentLine = 0xff007f00
        CommentLineDoc = 0xff3f703f
        Default = 0xff808080
        DoubleQuotedString = 0xff7f007f
        GlobalClass = 0xff000000
        HashQuotedString = 0xff007f00
        Identifier = 0xff000000
        InactiveComment = 0xff90b090
        InactiveCommentDoc = 0xffd0d0d0
        InactiveCommentDocKeyword = 0xffc0c0c0
        InactiveCommentDocKeywordError = 0xffc0c0c0
        InactiveCommentLine = 0xff90b090
        InactiveCommentLineDoc = 0xffc0c0c0
        InactiveDefault = 0xffc0c0c0
        InactiveDoubleQuotedString = 0xffb090b0
        InactiveGlobalClass = 0xffb0b0b0
        InactiveHashQuotedString = 0xff000000
        InactiveIdentifier = 0xffb0b0b0
        InactiveKeyword = 0xff9090b0
        InactiveKeywordSet2 = 0xffc0c0c0
        InactiveNumber = 0xff90b090
        InactiveOperator = 0xffb0b0b0
        InactivePreProcessor = 0xffb0b090
        InactivePreProcessorComment = 0xff000000
        InactivePreProcessorCommentLineDoc = 0xffc0c0c0
        InactiveRawString = 0xff000000
        InactiveRegex = 0xff7faf7f
        InactiveSingleQuotedString = 0xffb090b0
        InactiveTripleQuotedVerbatimString = 0xff000000
        InactiveUUID = 0xffc0c0c0
        InactiveUnclosedString = 0xff000000
        InactiveVerbatimString = 0xff90b090
        Keyword = 0xff00007f
        KeywordSet2 = 0xff000000
        Number = 0xff007f7f
        Operator = 0xff000000
        PreProcessor = 0xff7f7f00
        PreProcessorComment = 0xff659900
        PreProcessorCommentLineDoc = 0xff3f703f
        RawString = 0xff7f007f
        Regex = 0xff3f7f3f
        SingleQuotedString = 0xff7f007f
        TripleQuotedVerbatimString = 0xff007f00
        UUID = 0xff000000
        UnclosedString = 0xff000000
        VerbatimString = 0xff007f00
    
    class Lua:
        BasicFunctions = 0xff00007f
        Character = 0xff7f007f
        Comment = 0xff007f00
        CoroutinesIOSystemFacilities = 0xff00007f
        Default = 0xff000000
        Identifier = 0xff000000
        Keyword = 0xff00007f
        KeywordSet5 = 0xff000000
        KeywordSet6 = 0xff000000
        KeywordSet7 = 0xff000000
        KeywordSet8 = 0xff000000
        Label = 0xff7f7f00
        LineComment = 0xff007f00
        LiteralString = 0xff7f007f
        Number = 0xff007f7f
        Operator = 0xff000000
        Preprocessor = 0xff7f7f00
        String = 0xff7f007f
        StringTableMathsFunctions = 0xff00007f
        UnclosedString = 0xff000000
    
    class Makefile:
        Comment = 0xff007f00
        Default = 0xff000000
        Error = 0xffffff00
        Operator = 0xff000000
        Preprocessor = 0xff7f7f00
        Target = 0xffa00000
        Variable = 0xff000080
    
    class Matlab:
        Command = 0xff7f7f00
        Comment = 0xff007f00
        Default = 0xff000000
        DoubleQuotedString = 0xff7f007f
        Identifier = 0xff000000
        Keyword = 0xff00007f
        Number = 0xff007f7f
        Operator = 0xff000000
        SingleQuotedString = 0xff7f007f
    
    class Octave:
        Command = 0xff7f7f00
        Comment = 0xff007f00
        Default = 0xff000000
        DoubleQuotedString = 0xff7f007f
        Identifier = 0xff000000
        Keyword = 0xff00007f
        Number = 0xff007f7f
        Operator = 0xff000000
        SingleQuotedString = 0xff7f007f
    
    class PO:
        Comment = 0xff007f00
        Default = 0xff000000
        Flags = 0xff000000
        Fuzzy = 0xff000000
        MessageContext = 0xff000000
        MessageContextText = 0xff000000
        MessageContextTextEOL = 0xff000000
        MessageId = 0xff000000
        MessageIdText = 0xff000000
        MessageIdTextEOL = 0xff000000
        MessageString = 0xff000000
        MessageStringText = 0xff000000
        MessageStringTextEOL = 0xff000000
        ProgrammerComment = 0xff000000
        Reference = 0xff000000
    
    class POV:
        BadDirective = 0xff804020
        Comment = 0xff007f00
        CommentLine = 0xff007f00
        Default = 0xffff0080
        Directive = 0xff7f7f00
        Identifier = 0xff000000
        KeywordSet6 = 0xff00007f
        KeywordSet7 = 0xff00007f
        KeywordSet8 = 0xff00007f
        Number = 0xff007f7f
        ObjectsCSGAppearance = 0xff00007f
        Operator = 0xff000000
        PredefinedFunctions = 0xff00007f
        PredefinedIdentifiers = 0xff00007f
        String = 0xff7f007f
        TypesModifiersItems = 0xff00007f
        UnclosedString = 0xff000000
    
    class Pascal:
        Asm = 0xff804080
        Character = 0xff7f007f
        Comment = 0xff007f00
        CommentLine = 0xff007f00
        CommentParenthesis = 0xff007f00
        Default = 0xff808080
        HexNumber = 0xff007f7f
        Identifier = 0xff000000
        Keyword = 0xff00007f
        Number = 0xff007f7f
        Operator = 0xff000000
        PreProcessor = 0xff7f7f00
        PreProcessorParenthesis = 0xff7f7f00
        SingleQuotedString = 0xff7f007f
        UnclosedString = 0xff000000
    
    class Perl:
        Array = 0xff000000
        BacktickHereDocument = 0xff7f007f
        BacktickHereDocumentVar = 0xffd00000
        Backticks = 0xffffff00
        BackticksVar = 0xffd00000
        Comment = 0xff007f00
        DataSection = 0xff600000
        Default = 0xff808080
        DoubleQuotedHereDocument = 0xff7f007f
        DoubleQuotedHereDocumentVar = 0xffd00000
        DoubleQuotedString = 0xff7f007f
        DoubleQuotedStringVar = 0xffd00000
        Error = 0xffffff00
        FormatBody = 0xffc000c0
        FormatIdentifier = 0xffc000c0
        Hash = 0xff000000
        HereDocumentDelimiter = 0xff000000
        Identifier = 0xff000000
        Keyword = 0xff00007f
        Number = 0xff007f7f
        Operator = 0xff000000
        POD = 0xff004000
        PODVerbatim = 0xff004000
        QuotedStringQ = 0xff7f007f
        QuotedStringQQ = 0xff7f007f
        QuotedStringQQVar = 0xffd00000
        QuotedStringQR = 0xff000000
        QuotedStringQRVar = 0xffd00000
        QuotedStringQW = 0xff000000
        QuotedStringQX = 0xffffff00
        QuotedStringQXVar = 0xffd00000
        Regex = 0xff000000
        RegexVar = 0xffd00000
        Scalar = 0xff000000
        SingleQuotedHereDocument = 0xff7f007f
        SingleQuotedString = 0xff7f007f
        SubroutinePrototype = 0xff000000
        Substitution = 0xff000000
        SubstitutionVar = 0xffd00000
        SymbolTable = 0xff000000
        Translation = 0xff000000
    
    class PostScript:
        ArrayParenthesis = 0xff00007f
        BadStringCharacter = 0xffffff00
        Base85String = 0xff7f007f
        Comment = 0xff007f00
        DSCComment = 0xff3f703f
        DSCCommentValue = 0xff3060a0
        Default = 0xff000000
        DictionaryParenthesis = 0xff3060a0
        HexString = 0xff3f7f3f
        ImmediateEvalLiteral = 0xff7f7f00
        Keyword = 0xff00007f
        Literal = 0xff7f7f00
        Name = 0xff000000
        Number = 0xff007f7f
        ProcedureParenthesis = 0xff000000
        Text = 0xff7f007f
    
    class Properties:
        Assignment = 0xffb06000
        Comment = 0xff007f7f
        Default = 0xff000000
        DefaultValue = 0xff7f7f00
        Key = 0xff000000
        Section = 0xff7f007f
    
    class Python:
        ClassName = 0xff0000ff
        Comment = 0xff007f00
        CommentBlock = 0xff7f7f7f
        Decorator = 0xff805000
        Default = 0xff000000
        DoubleQuotedString = 0xff7f007f
        FunctionMethodName = 0xff007f7f
        HighlightedIdentifier = 0xff407090
        Identifier = 0xff000000
        Inconsistent = 0xff007f00
        Keyword = 0xff00007f
        NoWarning = 0xff808080
        Number = 0xff007f7f
        Operator = 0xff000000
        SingleQuotedString = 0xff7f007f
        Spaces = 0xff7f007f
        Tabs = 0xff7f007f
        TabsAfterSpaces = 0xff007f7f
        TripleDoubleQuotedString = 0xff7f0000
        TripleSingleQuotedString = 0xff7f0000
        UnclosedString = 0xff000000
    
    class Ruby:
        Backticks = 0xffffff00
        ClassName = 0xff0000ff
        ClassVariable = 0xff8000b0
        Comment = 0xff007f00
        DataSection = 0xff600000
        Default = 0xff808080
        DemotedKeyword = 0xff00007f
        DoubleQuotedString = 0xff7f007f
        Error = 0xff000000
        FunctionMethodName = 0xff007f7f
        Global = 0xff800080
        HereDocument = 0xff7f007f
        HereDocumentDelimiter = 0xff000000
        Identifier = 0xff000000
        InstanceVariable = 0xffb00080
        Keyword = 0xff00007f
        ModuleName = 0xffa000a0
        Number = 0xff007f7f
        Operator = 0xff000000
        POD = 0xff004000
        PercentStringQ = 0xff7f007f
        PercentStringq = 0xff7f007f
        PercentStringr = 0xff000000
        PercentStringw = 0xff000000
        PercentStringx = 0xffffff00
        Regex = 0xff000000
        SingleQuotedString = 0xff7f007f
        Stderr = 0xff000000
        Stdin = 0xff000000
        Stdout = 0xff000000
        Symbol = 0xffc0a030
    
    class SQL:
        Comment = 0xff007f00
        CommentDoc = 0xff7f7f7f
        CommentDocKeyword = 0xff3060a0
        CommentDocKeywordError = 0xff804020
        CommentLine = 0xff007f00
        CommentLineHash = 0xff007f00
        Default = 0xff808080
        DoubleQuotedString = 0xff7f007f
        Identifier = 0xff000000
        Keyword = 0xff00007f
        KeywordSet5 = 0xff4b0082
        KeywordSet6 = 0xffb00040
        KeywordSet7 = 0xff8b0000
        KeywordSet8 = 0xff800080
        Number = 0xff007f7f
        Operator = 0xff000000
        PlusComment = 0xff007f00
        PlusKeyword = 0xff7f7f00
        PlusPrompt = 0xff007f00
        QuotedIdentifier = 0xff000000
        SingleQuotedString = 0xff7f007f
    
    class Spice:
        Command = 0xff00007f
        Comment = 0xff007f00
        Default = 0xff808080
        Delimiter = 0xff000000
        Function = 0xff00007f
        Identifier = 0xff000000
        Number = 0xff007f7f
        Parameter = 0xff0040e0
        Value = 0xff7f007f
    
    class TCL:
        Comment = 0xff007f00
        CommentBlock = 0xff000000
        CommentBox = 0xff007f00
        CommentLine = 0xff007f00
        Default = 0xff808080
        ExpandKeyword = 0xff00007f
        ITCLKeyword = 0xff00007f
        Identifier = 0xff00007f
        KeywordSet6 = 0xff00007f
        KeywordSet7 = 0xff00007f
        KeywordSet8 = 0xff00007f
        KeywordSet9 = 0xff00007f
        Modifier = 0xff7f007f
        Number = 0xff007f7f
        Operator = 0xff000000
        QuotedKeyword = 0xff7f007f
        QuotedString = 0xff7f007f
        Substitution = 0xff7f7f00
        SubstitutionBrace = 0xff7f7f00
        TCLKeyword = 0xff00007f
        TkCommand = 0xff00007f
        TkKeyword = 0xff00007f
    
    class TeX:
        Command = 0xff007f00
        Default = 0xff3f3f3f
        Group = 0xff7f0000
        Special = 0xff007f7f
        Symbol = 0xff7f7f00
        Text = 0xff000000
    
    class VHDL:
        Attribute = 0xff804020
        Comment = 0xff007f00
        CommentLine = 0xff3f7f3f
        Default = 0xff800080
        Identifier = 0xff000000
        Keyword = 0xff00007f
        KeywordSet7 = 0xff804020
        Number = 0xff007f7f
        Operator = 0xff000000
        StandardFunction = 0xff808020
        StandardOperator = 0xff007f7f
        StandardPackage = 0xff208020
        StandardType = 0xff208080
        String = 0xff7f007f
        UnclosedString = 0xff000000
    
    class Verilog:
        Comment = 0xff007f00
        CommentBang = 0xff3f7f3f
        CommentLine = 0xff007f00
        Default = 0xff808080
        Identifier = 0xff000000
        Keyword = 0xff00007f
        KeywordSet2 = 0xff007f7f
        Number = 0xff007f7f
        Operator = 0xff007070
        Preprocessor = 0xff7f7f00
        String = 0xff7f007f
        SystemTask = 0xff804020
        UnclosedString = 0xff000000
        UserKeywordSet = 0xff2a00ff
    
    class XML:
        ASPAtStart = 0xff000000
        ASPJavaScriptComment = 0xff007f00
        ASPJavaScriptCommentDoc = 0xff7f7f7f
        ASPJavaScriptCommentLine = 0xff007f00
        ASPJavaScriptDefault = 0xff000000
        ASPJavaScriptDoubleQuotedString = 0xff7f007f
        ASPJavaScriptKeyword = 0xff00007f
        ASPJavaScriptNumber = 0xff007f7f
        ASPJavaScriptRegex = 0xff000000
        ASPJavaScriptSingleQuotedString = 0xff7f007f
        ASPJavaScriptStart = 0xff7f7f00
        ASPJavaScriptSymbol = 0xff000000
        ASPJavaScriptUnclosedString = 0xff000000
        ASPJavaScriptWord = 0xff000000
        ASPPythonClassName = 0xff0000ff
        ASPPythonComment = 0xff007f00
        ASPPythonDefault = 0xff808080
        ASPPythonDoubleQuotedString = 0xff7f007f
        ASPPythonFunctionMethodName = 0xff007f7f
        ASPPythonIdentifier = 0xff000000
        ASPPythonKeyword = 0xff00007f
        ASPPythonNumber = 0xff007f7f
        ASPPythonOperator = 0xff000000
        ASPPythonSingleQuotedString = 0xff7f007f
        ASPPythonStart = 0xff808080
        ASPPythonTripleDoubleQuotedString = 0xff7f0000
        ASPPythonTripleSingleQuotedString = 0xff7f0000
        ASPStart = 0xff000000
        ASPVBScriptComment = 0xff008000
        ASPVBScriptDefault = 0xff000000
        ASPVBScriptIdentifier = 0xff000080
        ASPVBScriptKeyword = 0xff000080
        ASPVBScriptNumber = 0xff008080
        ASPVBScriptStart = 0xff000000
        ASPVBScriptString = 0xff800080
        ASPVBScriptUnclosedString = 0xff000080
        ASPXCComment = 0xff000000
        Attribute = 0xff008080
        CDATA = 0xff800000
        Default = 0xff000000
        Entity = 0xff800080
        HTMLComment = 0xff808000
        HTMLDoubleQuotedString = 0xff7f007f
        HTMLNumber = 0xff007f7f
        HTMLSingleQuotedString = 0xff7f007f
        HTMLValue = 0xff608060
        JavaScriptComment = 0xff007f00
        JavaScriptCommentDoc = 0xff3f703f
        JavaScriptCommentLine = 0xff007f00
        JavaScriptDefault = 0xff000000
        JavaScriptDoubleQuotedString = 0xff7f007f
        JavaScriptKeyword = 0xff00007f
        JavaScriptNumber = 0xff007f7f
        JavaScriptRegex = 0xff000000
        JavaScriptSingleQuotedString = 0xff7f007f
        JavaScriptStart = 0xff7f7f00
        JavaScriptSymbol = 0xff000000
        JavaScriptUnclosedString = 0xff000000
        JavaScriptWord = 0xff000000
        OtherInTag = 0xff800080
        PHPComment = 0xff999999
        PHPCommentLine = 0xff666666
        PHPDefault = 0xff000033
        PHPDoubleQuotedString = 0xff007f00
        PHPDoubleQuotedVariable = 0xff00007f
        PHPKeyword = 0xff7f007f
        PHPNumber = 0xffcc9900
        PHPOperator = 0xff000000
        PHPSingleQuotedString = 0xff009f00
        PHPStart = 0xff800000
        PHPVariable = 0xff00007f
        PythonClassName = 0xff0000ff
        PythonComment = 0xff007f00
        PythonDefault = 0xff808080
        PythonDoubleQuotedString = 0xff7f007f
        PythonFunctionMethodName = 0xff007f7f
        PythonIdentifier = 0xff000000
        PythonKeyword = 0xff00007f
        PythonNumber = 0xff007f7f
        PythonOperator = 0xff000000
        PythonSingleQuotedString = 0xff7f007f
        PythonStart = 0xff808080
        PythonTripleDoubleQuotedString = 0xff7f0000
        PythonTripleSingleQuotedString = 0xff7f0000
        SGMLBlockDefault = 0xff000066
        SGMLCommand = 0xff000080
        SGMLComment = 0xff808000
        SGMLDefault = 0xff000080
        SGMLDoubleQuotedString = 0xff800000
        SGMLEntity = 0xff333333
        SGMLError = 0xff800000
        SGMLParameter = 0xff006600
        SGMLParameterComment = 0xff000000
        SGMLSingleQuotedString = 0xff993300
        SGMLSpecial = 0xff3366ff
        Script = 0xff000080
        Tag = 0xff000080
        UnknownAttribute = 0xff008080
        UnknownTag = 0xff000080
        VBScriptComment = 0xff008000
        VBScriptDefault = 0xff000000
        VBScriptIdentifier = 0xff000080
        VBScriptKeyword = 0xff000080
        VBScriptNumber = 0xff008080
        VBScriptStart = 0xff000000
        VBScriptString = 0xff800080
        VBScriptUnclosedString = 0xff000080
        XMLEnd = 0xff800080
        XMLStart = 0xff800080
        XMLTagEnd = 0xff000080
    
    class YAML:
        Comment = 0xff008800
        Default = 0xff000000
        DocumentDelimiter = 0xffffffff
        Identifier = 0xff000088
        Keyword = 0xff880088
        Number = 0xff880000
        Operator = 0xff000000
        Reference = 0xff008888
        SyntaxErrorMarker = 0xffffffff
        TextBlockMarker = 0xff333366


class Paper:
    Default = PyQt4.QtGui.QColor(0xffffffff)
    
    class Ada:
        Default = 0xffffffff
        Comment = 0xffffffff
        Keyword = 0xffffffff
        String = 0xffffffff
        Procedure = 0xffffffff
        Number = 0xffffffff
        Type = 0xffffffff
        Package = 0xffffffff
    
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
    




