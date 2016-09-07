
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
##      Water theme

import PyQt4.QtGui


Form = "#295a88"
Cursor = PyQt4.QtGui.QColor(0xffffffff)


class FoldMargin:
    ForeGround = PyQt4.QtGui.QColor(0xff4096bf)
    BackGround = PyQt4.QtGui.QColor(0xff3476a3)


class LineMargin:
    ForeGround = PyQt4.QtGui.QColor(0xffffffff)
    BackGround = PyQt4.QtGui.QColor(0xff1f4661)


class Indication:
    Font = "#e6e6e6"
    ActiveBackGround = "#112435"
    ActiveBorder = "#e6e6e6"
    PassiveBackGround = "#295a88"
    PassiveBorder = "#33aaff"

    
class Font:
    Default = PyQt4.QtGui.QColor(0xffffffff)
    
    class Ada:
        Default = 0xffffffff
        Comment = 0xff6cab9d
        Keyword = 0xff2389da
        String = 0xffc4bbb8
        Procedure = 0xff5abcd8
        Number = 0xff74ccf4
        Type = 0xff2389da
        Package = 0xfff5b0cb
    
    class Nim:
        Default = 0xffffffff
        Comment = 0xff6cab9d
        BasicKeyword = 0xff2389da
        TopKeyword = 0xff407fc0
        String = 0xffc4bbb8
        LongString = 0xfff5b0cb
        Number = 0xff74ccf4
        Operator = 0xff7f7f7f
        Unsafe = 0xffc00000
        Type = 0xff6e6e00
        DocumentationComment = 0xffc75146
        Definition = 0xff74ccf4
        Class = 0xff5abcd8
        KeywordOperator = 0xff963cc8
        CharLiteral = 0xff00c8ff
        CaseOf = 0xff8000ff
        UserKeyword = 0xffff8040
        MultilineComment = 0xffad2e24
        MultilineDocumentation = 0xffea8c55
        Pragma = 0xffc07f40
    
    class Oberon:
        Default = 0xffffffff
        Comment = 0xff6cab9d
        Keyword = 0xff2389da
        String = 0xffc4bbb8
        Procedure = 0xff5abcd8
        Module = 0xfff5b0cb
        Number = 0xff74ccf4
        Type = 0xff2389da
    
    
    # Generated
    class AVS:
        BlockComment = 0xff6cab9d
        ClipProperty = 0xff2389da
        Default = 0xffffffff
        Filter = 0xff2389da
        Function = 0xff74ccf4
        Identifier = 0xffffffff
        Keyword = 0xff2389da
        KeywordSet6 = 0xff8000ff
        LineComment = 0xff6cab9d
        NestedBlockComment = 0xff6cab9d
        Number = 0xff74ccf4
        Operator = 0xffffffff
        Plugin = 0xff0080c0
        String = 0xffc4bbb8
        TripleString = 0xffc4bbb8
    
    class Bash:
        Backticks = 0xffffff00
        Comment = 0xff6cab9d
        Default = 0xff808080
        DoubleQuotedString = 0xffc4bbb8
        Error = 0xffffff00
        HereDocumentDelimiter = 0xffffffff
        Identifier = 0xffffffff
        Keyword = 0xff2389da
        Number = 0xff74ccf4
        Operator = 0xffffffff
        ParameterExpansion = 0xffffffff
        Scalar = 0xffffffff
        SingleQuotedHereDocument = 0xffc4bbb8
        SingleQuotedString = 0xffc4bbb8
    
    class Batch:
        Comment = 0xff6cab9d
        Default = 0xffffffff
        ExternalCommand = 0xff2389da
        HideCommandChar = 0xff7f7f00
        Keyword = 0xff2389da
        Label = 0xffc4bbb8
        Operator = 0xffffffff
        Variable = 0xff800080
    
    class CMake:
        BlockForeach = 0xff2389da
        BlockIf = 0xff2389da
        BlockMacro = 0xff2389da
        BlockWhile = 0xff2389da
        Comment = 0xff6cab9d
        Default = 0xffffffff
        Function = 0xff2389da
        KeywordSet3 = 0xffffffff
        Label = 0xffcc3300
        Number = 0xff74ccf4
        String = 0xffc4bbb8
        StringLeftQuote = 0xffc4bbb8
        StringRightQuote = 0xffc4bbb8
        StringVariable = 0xffcc3300
        Variable = 0xffedff86
    
    class CPP:
        Comment = 0xff6cab9d
        CommentDoc = 0xff3f703f
        CommentDocKeyword = 0xff3060a0
        CommentDocKeywordError = 0xff804020
        CommentLine = 0xff6cab9d
        CommentLineDoc = 0xff3f703f
        Default = 0xff808080
        DoubleQuotedString = 0xffc4bbb8
        GlobalClass = 0xffffffff
        HashQuotedString = 0xff6cab9d
        Identifier = 0xffffffff
        InactiveComment = 0xff90b090
        InactiveCommentDoc = 0xffd0d0d0
        InactiveCommentDocKeyword = 0xffc0c0c0
        InactiveCommentDocKeywordError = 0xffc0c0c0
        InactiveCommentLine = 0xff90b090
        InactiveCommentLineDoc = 0xffc0c0c0
        InactiveDefault = 0xffc0c0c0
        InactiveDoubleQuotedString = 0xffb090b0
        InactiveGlobalClass = 0xffb0b0b0
        InactiveHashQuotedString = 0xffffffff
        InactiveIdentifier = 0xffb0b0b0
        InactiveKeyword = 0xff9090b0
        InactiveKeywordSet2 = 0xffc0c0c0
        InactiveNumber = 0xff90b090
        InactiveOperator = 0xffb0b0b0
        InactivePreProcessor = 0xffb0b090
        InactivePreProcessorComment = 0xffffffff
        InactivePreProcessorCommentLineDoc = 0xffc0c0c0
        InactiveRawString = 0xffffffff
        InactiveRegex = 0xff7faf7f
        InactiveSingleQuotedString = 0xffb090b0
        InactiveTripleQuotedVerbatimString = 0xffffffff
        InactiveUUID = 0xffc0c0c0
        InactiveUnclosedString = 0xffffffff
        InactiveVerbatimString = 0xff90b090
        Keyword = 0xff2389da
        KeywordSet2 = 0xffffffff
        Number = 0xff74ccf4
        Operator = 0xffffffff
        PreProcessor = 0xff7f7f00
        PreProcessorComment = 0xff659900
        PreProcessorCommentLineDoc = 0xff3f703f
        RawString = 0xffc4bbb8
        Regex = 0xff3f7f3f
        SingleQuotedString = 0xffc4bbb8
        TripleQuotedVerbatimString = 0xff6cab9d
        UUID = 0xffffffff
        UnclosedString = 0xffffffff
        VerbatimString = 0xff6cab9d
    
    class CSS:
        AtRule = 0xff7f7f00
        Attribute = 0xffedff86
        CSS1Property = 0xff0040e0
        CSS2Property = 0xff00a0e0
        CSS3Property = 0xffffffff
        ClassSelector = 0xffffffff
        Comment = 0xff6cab9d
        Default = 0xffff0080
        DoubleQuotedString = 0xffc4bbb8
        ExtendedCSSProperty = 0xffffffff
        ExtendedPseudoClass = 0xffffffff
        ExtendedPseudoElement = 0xffffffff
        IDSelector = 0xff74ccf4
        Important = 0xffff8000
        MediaRule = 0xff7f7f00
        Operator = 0xffffffff
        PseudoClass = 0xffedff86
        PseudoElement = 0xffffffff
        SingleQuotedString = 0xffc4bbb8
        Tag = 0xff2389da
        UnknownProperty = 0xffff0000
        UnknownPseudoClass = 0xffff0000
        Value = 0xffc4bbb8
        Variable = 0xffffffff
    
    class CSharp:
        Comment = 0xff6cab9d
        CommentDoc = 0xff3f703f
        CommentDocKeyword = 0xff3060a0
        CommentDocKeywordError = 0xff804020
        CommentLine = 0xff6cab9d
        CommentLineDoc = 0xff3f703f
        Default = 0xff808080
        DoubleQuotedString = 0xffc4bbb8
        GlobalClass = 0xffffffff
        HashQuotedString = 0xff6cab9d
        Identifier = 0xffffffff
        InactiveComment = 0xff90b090
        InactiveCommentDoc = 0xffd0d0d0
        InactiveCommentDocKeyword = 0xffc0c0c0
        InactiveCommentDocKeywordError = 0xffc0c0c0
        InactiveCommentLine = 0xff90b090
        InactiveCommentLineDoc = 0xffc0c0c0
        InactiveDefault = 0xffc0c0c0
        InactiveDoubleQuotedString = 0xffb090b0
        InactiveGlobalClass = 0xffb0b0b0
        InactiveHashQuotedString = 0xffffffff
        InactiveIdentifier = 0xffb0b0b0
        InactiveKeyword = 0xff9090b0
        InactiveKeywordSet2 = 0xffc0c0c0
        InactiveNumber = 0xff90b090
        InactiveOperator = 0xffb0b0b0
        InactivePreProcessor = 0xffb0b090
        InactivePreProcessorComment = 0xffffffff
        InactivePreProcessorCommentLineDoc = 0xffc0c0c0
        InactiveRawString = 0xffffffff
        InactiveRegex = 0xff7faf7f
        InactiveSingleQuotedString = 0xffb090b0
        InactiveTripleQuotedVerbatimString = 0xffffffff
        InactiveUUID = 0xffc0c0c0
        InactiveUnclosedString = 0xffffffff
        InactiveVerbatimString = 0xff90b090
        Keyword = 0xff2389da
        KeywordSet2 = 0xffffffff
        Number = 0xff74ccf4
        Operator = 0xffffffff
        PreProcessor = 0xff7f7f00
        PreProcessorComment = 0xff659900
        PreProcessorCommentLineDoc = 0xff3f703f
        RawString = 0xffc4bbb8
        Regex = 0xff3f7f3f
        SingleQuotedString = 0xffc4bbb8
        TripleQuotedVerbatimString = 0xff6cab9d
        UUID = 0xffffffff
        UnclosedString = 0xffffffff
        VerbatimString = 0xff6cab9d
    
    class CoffeeScript:
        BlockRegex = 0xff3f7f3f
        BlockRegexComment = 0xff6cab9d
        Comment = 0xff6cab9d
        CommentBlock = 0xff6cab9d
        CommentDoc = 0xff3f703f
        CommentDocKeyword = 0xff3060a0
        CommentDocKeywordError = 0xff804020
        CommentLine = 0xff6cab9d
        CommentLineDoc = 0xff3f703f
        Default = 0xff808080
        DoubleQuotedString = 0xffc4bbb8
        GlobalClass = 0xffffffff
        Identifier = 0xffffffff
        Keyword = 0xff2389da
        KeywordSet2 = 0xffffffff
        Number = 0xff74ccf4
        Operator = 0xffffffff
        PreProcessor = 0xff7f7f00
        Regex = 0xff3f7f3f
        SingleQuotedString = 0xffc4bbb8
        UUID = 0xffffffff
        UnclosedString = 0xffffffff
        VerbatimString = 0xff6cab9d
    
    class D:
        BackquoteString = 0xffffffff
        Character = 0xffc4bbb8
        Comment = 0xff6cab9d
        CommentDoc = 0xff3f703f
        CommentDocKeyword = 0xff3060a0
        CommentDocKeywordError = 0xff804020
        CommentLine = 0xff6cab9d
        CommentLineDoc = 0xff3f703f
        CommentNested = 0xffa0c0a0
        Default = 0xff808080
        Identifier = 0xffffffff
        Keyword = 0xff2389da
        KeywordDoc = 0xff2389da
        KeywordSecondary = 0xff2389da
        KeywordSet5 = 0xffffffff
        KeywordSet6 = 0xffffffff
        KeywordSet7 = 0xffffffff
        Number = 0xff74ccf4
        Operator = 0xffffffff
        RawString = 0xffffffff
        String = 0xffc4bbb8
        Typedefs = 0xff2389da
        UnclosedString = 0xffffffff
    
    class Diff:
        Command = 0xff7f7f00
        Comment = 0xff6cab9d
        Default = 0xffffffff
        Header = 0xfff5b0cb
        LineAdded = 0xff2389da
        LineChanged = 0xff7f7f7f
        LineRemoved = 0xff74ccf4
        Position = 0xffc4bbb8
    
    class Fortran:
        Comment = 0xff6cab9d
        Continuation = 0xffffffff
        Default = 0xff808080
        DottedOperator = 0xffffffff
        DoubleQuotedString = 0xffc4bbb8
        ExtendedFunction = 0xffb04080
        Identifier = 0xffffffff
        IntrinsicFunction = 0xffb00040
        Keyword = 0xff2389da
        Label = 0xffe0c0e0
        Number = 0xff74ccf4
        Operator = 0xffffffff
        PreProcessor = 0xff7f7f00
        SingleQuotedString = 0xffc4bbb8
        UnclosedString = 0xffffffff
    
    class Fortran77:
        Comment = 0xff6cab9d
        Continuation = 0xffffffff
        Default = 0xff808080
        DottedOperator = 0xffffffff
        DoubleQuotedString = 0xffc4bbb8
        ExtendedFunction = 0xffb04080
        Identifier = 0xffffffff
        IntrinsicFunction = 0xffb00040
        Keyword = 0xff2389da
        Label = 0xffe0c0e0
        Number = 0xff74ccf4
        Operator = 0xffffffff
        PreProcessor = 0xff7f7f00
        SingleQuotedString = 0xffc4bbb8
        UnclosedString = 0xffffffff
    
    class HTML:
        ASPAtStart = 0xffffffff
        ASPJavaScriptComment = 0xff6cab9d
        ASPJavaScriptCommentDoc = 0xff7f7f7f
        ASPJavaScriptCommentLine = 0xff6cab9d
        ASPJavaScriptDefault = 0xffffffff
        ASPJavaScriptDoubleQuotedString = 0xffc4bbb8
        ASPJavaScriptKeyword = 0xff2389da
        ASPJavaScriptNumber = 0xff74ccf4
        ASPJavaScriptRegex = 0xffffffff
        ASPJavaScriptSingleQuotedString = 0xffc4bbb8
        ASPJavaScriptStart = 0xff7f7f00
        ASPJavaScriptSymbol = 0xffffffff
        ASPJavaScriptUnclosedString = 0xffffffff
        ASPJavaScriptWord = 0xffffffff
        ASPPythonClassName = 0xff5abcd8
        ASPPythonComment = 0xff6cab9d
        ASPPythonDefault = 0xff808080
        ASPPythonDoubleQuotedString = 0xffc4bbb8
        ASPPythonFunctionMethodName = 0xff74ccf4
        ASPPythonIdentifier = 0xffffffff
        ASPPythonKeyword = 0xff2389da
        ASPPythonNumber = 0xff74ccf4
        ASPPythonOperator = 0xffffffff
        ASPPythonSingleQuotedString = 0xffc4bbb8
        ASPPythonStart = 0xff808080
        ASPPythonTripleDoubleQuotedString = 0xfff5b0cb
        ASPPythonTripleSingleQuotedString = 0xfff5b0cb
        ASPStart = 0xffffffff
        ASPVBScriptComment = 0xff008000
        ASPVBScriptDefault = 0xffffffff
        ASPVBScriptIdentifier = 0xff1f76e4
        ASPVBScriptKeyword = 0xff1f76e4
        ASPVBScriptNumber = 0xff008080
        ASPVBScriptStart = 0xffffffff
        ASPVBScriptString = 0xff800080
        ASPVBScriptUnclosedString = 0xff1f76e4
        ASPXCComment = 0xffffffff
        Attribute = 0xff008080
        CDATA = 0xffffffff
        Default = 0xffffffff
        Entity = 0xff800080
        HTMLComment = 0xff808000
        HTMLDoubleQuotedString = 0xffc4bbb8
        HTMLNumber = 0xff74ccf4
        HTMLSingleQuotedString = 0xffc4bbb8
        HTMLValue = 0xffff00ff
        JavaScriptComment = 0xff6cab9d
        JavaScriptCommentDoc = 0xff3f703f
        JavaScriptCommentLine = 0xff6cab9d
        JavaScriptDefault = 0xffffffff
        JavaScriptDoubleQuotedString = 0xffc4bbb8
        JavaScriptKeyword = 0xff2389da
        JavaScriptNumber = 0xff74ccf4
        JavaScriptRegex = 0xffffffff
        JavaScriptSingleQuotedString = 0xffc4bbb8
        JavaScriptStart = 0xff7f7f00
        JavaScriptSymbol = 0xffffffff
        JavaScriptUnclosedString = 0xffffffff
        JavaScriptWord = 0xffffffff
        OtherInTag = 0xff800080
        PHPComment = 0xff999999
        PHPCommentLine = 0xff666666
        PHPDefault = 0xffc7dbf5
        PHPDoubleQuotedString = 0xff6cab9d
        PHPDoubleQuotedVariable = 0xff2389da
        PHPKeyword = 0xffc4bbb8
        PHPNumber = 0xffcc9900
        PHPOperator = 0xffffffff
        PHPSingleQuotedString = 0xff009f00
        PHPStart = 0xff5abcd8
        PHPVariable = 0xff2389da
        PythonClassName = 0xff5abcd8
        PythonComment = 0xff6cab9d
        PythonDefault = 0xff808080
        PythonDoubleQuotedString = 0xffc4bbb8
        PythonFunctionMethodName = 0xff74ccf4
        PythonIdentifier = 0xffffffff
        PythonKeyword = 0xff2389da
        PythonNumber = 0xff74ccf4
        PythonOperator = 0xffffffff
        PythonSingleQuotedString = 0xffc4bbb8
        PythonStart = 0xff808080
        PythonTripleDoubleQuotedString = 0xfff5b0cb
        PythonTripleSingleQuotedString = 0xfff5b0cb
        SGMLBlockDefault = 0xfffff5b2
        SGMLCommand = 0xff1f76e4
        SGMLComment = 0xff808000
        SGMLDefault = 0xff1f76e4
        SGMLDoubleQuotedString = 0xffedff86
        SGMLEntity = 0xff333333
        SGMLError = 0xffedff86
        SGMLParameter = 0xff006600
        SGMLParameterComment = 0xffffffff
        SGMLSingleQuotedString = 0xff993300
        SGMLSpecial = 0xff3366ff
        Script = 0xff1f76e4
        Tag = 0xff1f76e4
        UnknownAttribute = 0xffff0000
        UnknownTag = 0xffff0000
        VBScriptComment = 0xff008000
        VBScriptDefault = 0xffffffff
        VBScriptIdentifier = 0xff1f76e4
        VBScriptKeyword = 0xff1f76e4
        VBScriptNumber = 0xff008080
        VBScriptStart = 0xffffffff
        VBScriptString = 0xff800080
        VBScriptUnclosedString = 0xff1f76e4
        XMLEnd = 0xff5abcd8
        XMLStart = 0xff5abcd8
        XMLTagEnd = 0xff1f76e4
    
    class IDL:
        Comment = 0xff6cab9d
        CommentDoc = 0xff3f703f
        CommentDocKeyword = 0xff3060a0
        CommentDocKeywordError = 0xff804020
        CommentLine = 0xff6cab9d
        CommentLineDoc = 0xff3f703f
        Default = 0xff808080
        DoubleQuotedString = 0xffc4bbb8
        GlobalClass = 0xffffffff
        HashQuotedString = 0xff6cab9d
        Identifier = 0xffffffff
        InactiveComment = 0xff90b090
        InactiveCommentDoc = 0xffd0d0d0
        InactiveCommentDocKeyword = 0xffc0c0c0
        InactiveCommentDocKeywordError = 0xffc0c0c0
        InactiveCommentLine = 0xff90b090
        InactiveCommentLineDoc = 0xffc0c0c0
        InactiveDefault = 0xffc0c0c0
        InactiveDoubleQuotedString = 0xffb090b0
        InactiveGlobalClass = 0xffb0b0b0
        InactiveHashQuotedString = 0xffffffff
        InactiveIdentifier = 0xffb0b0b0
        InactiveKeyword = 0xff9090b0
        InactiveKeywordSet2 = 0xffc0c0c0
        InactiveNumber = 0xff90b090
        InactiveOperator = 0xffb0b0b0
        InactivePreProcessor = 0xffb0b090
        InactivePreProcessorComment = 0xffffffff
        InactivePreProcessorCommentLineDoc = 0xffc0c0c0
        InactiveRawString = 0xffffffff
        InactiveRegex = 0xff7faf7f
        InactiveSingleQuotedString = 0xffb090b0
        InactiveTripleQuotedVerbatimString = 0xffffffff
        InactiveUUID = 0xffc0c0c0
        InactiveUnclosedString = 0xffffffff
        InactiveVerbatimString = 0xff90b090
        Keyword = 0xff2389da
        KeywordSet2 = 0xffffffff
        Number = 0xff74ccf4
        Operator = 0xffffffff
        PreProcessor = 0xff7f7f00
        PreProcessorComment = 0xff659900
        PreProcessorCommentLineDoc = 0xff3f703f
        RawString = 0xffc4bbb8
        Regex = 0xff3f7f3f
        SingleQuotedString = 0xffc4bbb8
        TripleQuotedVerbatimString = 0xff6cab9d
        UUID = 0xff804080
        UnclosedString = 0xffffffff
        VerbatimString = 0xff6cab9d
    
    class Java:
        Comment = 0xff6cab9d
        CommentDoc = 0xff3f703f
        CommentDocKeyword = 0xff3060a0
        CommentDocKeywordError = 0xff804020
        CommentLine = 0xff6cab9d
        CommentLineDoc = 0xff3f703f
        Default = 0xff808080
        DoubleQuotedString = 0xffc4bbb8
        GlobalClass = 0xffffffff
        HashQuotedString = 0xff6cab9d
        Identifier = 0xffffffff
        InactiveComment = 0xff90b090
        InactiveCommentDoc = 0xffd0d0d0
        InactiveCommentDocKeyword = 0xffc0c0c0
        InactiveCommentDocKeywordError = 0xffc0c0c0
        InactiveCommentLine = 0xff90b090
        InactiveCommentLineDoc = 0xffc0c0c0
        InactiveDefault = 0xffc0c0c0
        InactiveDoubleQuotedString = 0xffb090b0
        InactiveGlobalClass = 0xffb0b0b0
        InactiveHashQuotedString = 0xffffffff
        InactiveIdentifier = 0xffb0b0b0
        InactiveKeyword = 0xff9090b0
        InactiveKeywordSet2 = 0xffc0c0c0
        InactiveNumber = 0xff90b090
        InactiveOperator = 0xffb0b0b0
        InactivePreProcessor = 0xffb0b090
        InactivePreProcessorComment = 0xffffffff
        InactivePreProcessorCommentLineDoc = 0xffc0c0c0
        InactiveRawString = 0xffffffff
        InactiveRegex = 0xff7faf7f
        InactiveSingleQuotedString = 0xffb090b0
        InactiveTripleQuotedVerbatimString = 0xffffffff
        InactiveUUID = 0xffc0c0c0
        InactiveUnclosedString = 0xffffffff
        InactiveVerbatimString = 0xff90b090
        Keyword = 0xff2389da
        KeywordSet2 = 0xffffffff
        Number = 0xff74ccf4
        Operator = 0xffffffff
        PreProcessor = 0xff7f7f00
        PreProcessorComment = 0xff659900
        PreProcessorCommentLineDoc = 0xff3f703f
        RawString = 0xffc4bbb8
        Regex = 0xff3f7f3f
        SingleQuotedString = 0xffc4bbb8
        TripleQuotedVerbatimString = 0xff6cab9d
        UUID = 0xffffffff
        UnclosedString = 0xffffffff
        VerbatimString = 0xff6cab9d
    
    class JavaScript:
        Comment = 0xff6cab9d
        CommentDoc = 0xff3f703f
        CommentDocKeyword = 0xff3060a0
        CommentDocKeywordError = 0xff804020
        CommentLine = 0xff6cab9d
        CommentLineDoc = 0xff3f703f
        Default = 0xff808080
        DoubleQuotedString = 0xffc4bbb8
        GlobalClass = 0xffffffff
        HashQuotedString = 0xff6cab9d
        Identifier = 0xffffffff
        InactiveComment = 0xff90b090
        InactiveCommentDoc = 0xffd0d0d0
        InactiveCommentDocKeyword = 0xffc0c0c0
        InactiveCommentDocKeywordError = 0xffc0c0c0
        InactiveCommentLine = 0xff90b090
        InactiveCommentLineDoc = 0xffc0c0c0
        InactiveDefault = 0xffc0c0c0
        InactiveDoubleQuotedString = 0xffb090b0
        InactiveGlobalClass = 0xffb0b0b0
        InactiveHashQuotedString = 0xffffffff
        InactiveIdentifier = 0xffb0b0b0
        InactiveKeyword = 0xff9090b0
        InactiveKeywordSet2 = 0xffc0c0c0
        InactiveNumber = 0xff90b090
        InactiveOperator = 0xffb0b0b0
        InactivePreProcessor = 0xffb0b090
        InactivePreProcessorComment = 0xffffffff
        InactivePreProcessorCommentLineDoc = 0xffc0c0c0
        InactiveRawString = 0xffffffff
        InactiveRegex = 0xff7faf7f
        InactiveSingleQuotedString = 0xffb090b0
        InactiveTripleQuotedVerbatimString = 0xffffffff
        InactiveUUID = 0xffc0c0c0
        InactiveUnclosedString = 0xffffffff
        InactiveVerbatimString = 0xff90b090
        Keyword = 0xff2389da
        KeywordSet2 = 0xffffffff
        Number = 0xff74ccf4
        Operator = 0xffffffff
        PreProcessor = 0xff7f7f00
        PreProcessorComment = 0xff659900
        PreProcessorCommentLineDoc = 0xff3f703f
        RawString = 0xffc4bbb8
        Regex = 0xff3f7f3f
        SingleQuotedString = 0xffc4bbb8
        TripleQuotedVerbatimString = 0xff6cab9d
        UUID = 0xffffffff
        UnclosedString = 0xffffffff
        VerbatimString = 0xff6cab9d
    
    class Lua:
        BasicFunctions = 0xff2389da
        Character = 0xffc4bbb8
        Comment = 0xff6cab9d
        CoroutinesIOSystemFacilities = 0xff2389da
        Default = 0xffffffff
        Identifier = 0xffffffff
        Keyword = 0xff2389da
        KeywordSet5 = 0xffffffff
        KeywordSet6 = 0xffffffff
        KeywordSet7 = 0xffffffff
        KeywordSet8 = 0xffffffff
        Label = 0xff7f7f00
        LineComment = 0xff6cab9d
        LiteralString = 0xffc4bbb8
        Number = 0xff74ccf4
        Operator = 0xffffffff
        Preprocessor = 0xff7f7f00
        String = 0xffc4bbb8
        StringTableMathsFunctions = 0xff2389da
        UnclosedString = 0xffffffff
    
    class Makefile:
        Comment = 0xff6cab9d
        Default = 0xffffffff
        Error = 0xffffff00
        Operator = 0xffffffff
        Preprocessor = 0xff7f7f00
        Target = 0xffa00000
        Variable = 0xff1f76e4
    
    class Matlab:
        Command = 0xff7f7f00
        Comment = 0xff6cab9d
        Default = 0xffffffff
        DoubleQuotedString = 0xffc4bbb8
        Identifier = 0xffffffff
        Keyword = 0xff2389da
        Number = 0xff74ccf4
        Operator = 0xffffffff
        SingleQuotedString = 0xffc4bbb8
    
    class Octave:
        Command = 0xff7f7f00
        Comment = 0xff6cab9d
        Default = 0xffffffff
        DoubleQuotedString = 0xffc4bbb8
        Identifier = 0xffffffff
        Keyword = 0xff2389da
        Number = 0xff74ccf4
        Operator = 0xffffffff
        SingleQuotedString = 0xffc4bbb8
    
    class PO:
        Comment = 0xff6cab9d
        Default = 0xffffffff
        Flags = 0xffffffff
        Fuzzy = 0xffffffff
        MessageContext = 0xffffffff
        MessageContextText = 0xffffffff
        MessageContextTextEOL = 0xffffffff
        MessageId = 0xffffffff
        MessageIdText = 0xffffffff
        MessageIdTextEOL = 0xffffffff
        MessageString = 0xffffffff
        MessageStringText = 0xffffffff
        MessageStringTextEOL = 0xffffffff
        ProgrammerComment = 0xffffffff
        Reference = 0xffffffff
    
    class POV:
        BadDirective = 0xff804020
        Comment = 0xff6cab9d
        CommentLine = 0xff6cab9d
        Default = 0xffff0080
        Directive = 0xff7f7f00
        Identifier = 0xffffffff
        KeywordSet6 = 0xff2389da
        KeywordSet7 = 0xff2389da
        KeywordSet8 = 0xff2389da
        Number = 0xff74ccf4
        ObjectsCSGAppearance = 0xff2389da
        Operator = 0xffffffff
        PredefinedFunctions = 0xff2389da
        PredefinedIdentifiers = 0xff2389da
        String = 0xffc4bbb8
        TypesModifiersItems = 0xff2389da
        UnclosedString = 0xffffffff
    
    class Pascal:
        Asm = 0xff804080
        Character = 0xffc4bbb8
        Comment = 0xff6cab9d
        CommentLine = 0xff6cab9d
        CommentParenthesis = 0xff6cab9d
        Default = 0xff808080
        HexNumber = 0xff74ccf4
        Identifier = 0xffffffff
        Keyword = 0xff2389da
        Number = 0xff74ccf4
        Operator = 0xffffffff
        PreProcessor = 0xff7f7f00
        PreProcessorParenthesis = 0xff7f7f00
        SingleQuotedString = 0xffc4bbb8
        UnclosedString = 0xffffffff
    
    class Perl:
        Array = 0xffffffff
        BacktickHereDocument = 0xffc4bbb8
        BacktickHereDocumentVar = 0xffd00000
        Backticks = 0xffffff00
        BackticksVar = 0xffd00000
        Comment = 0xff6cab9d
        DataSection = 0xff600000
        Default = 0xff808080
        DoubleQuotedHereDocument = 0xffc4bbb8
        DoubleQuotedHereDocumentVar = 0xffd00000
        DoubleQuotedString = 0xffc4bbb8
        DoubleQuotedStringVar = 0xffd00000
        Error = 0xffffff00
        FormatBody = 0xffc000c0
        FormatIdentifier = 0xffc000c0
        Hash = 0xffffffff
        HereDocumentDelimiter = 0xffffffff
        Identifier = 0xffffffff
        Keyword = 0xff2389da
        Number = 0xff74ccf4
        Operator = 0xffffffff
        POD = 0xff004000
        PODVerbatim = 0xff004000
        QuotedStringQ = 0xffc4bbb8
        QuotedStringQQ = 0xffc4bbb8
        QuotedStringQQVar = 0xffd00000
        QuotedStringQR = 0xffffffff
        QuotedStringQRVar = 0xffd00000
        QuotedStringQW = 0xffffffff
        QuotedStringQX = 0xffffff00
        QuotedStringQXVar = 0xffd00000
        Regex = 0xffffffff
        RegexVar = 0xffd00000
        Scalar = 0xffffffff
        SingleQuotedHereDocument = 0xffc4bbb8
        SingleQuotedString = 0xffc4bbb8
        SubroutinePrototype = 0xffffffff
        Substitution = 0xffffffff
        SubstitutionVar = 0xffd00000
        SymbolTable = 0xffffffff
        Translation = 0xffffffff
    
    class PostScript:
        ArrayParenthesis = 0xff2389da
        BadStringCharacter = 0xffffff00
        Base85String = 0xffc4bbb8
        Comment = 0xff6cab9d
        DSCComment = 0xff3f703f
        DSCCommentValue = 0xff3060a0
        Default = 0xffffffff
        DictionaryParenthesis = 0xff3060a0
        HexString = 0xff3f7f3f
        ImmediateEvalLiteral = 0xff7f7f00
        Keyword = 0xff2389da
        Literal = 0xff7f7f00
        Name = 0xffffffff
        Number = 0xff74ccf4
        ProcedureParenthesis = 0xffffffff
        Text = 0xffc4bbb8
    
    class Properties:
        Assignment = 0xffb06000
        Comment = 0xff74ccf4
        Default = 0xffffffff
        DefaultValue = 0xff7f7f00
        Key = 0xffffffff
        Section = 0xffc4bbb8
    
    class Python:
        ClassName = 0xff5abcd8
        Comment = 0xff6cab9d
        CommentBlock = 0xff7f7f7f
        Decorator = 0xff805000
        Default = 0xffffffff
        DoubleQuotedString = 0xffc4bbb8
        FunctionMethodName = 0xff74ccf4
        HighlightedIdentifier = 0xff407090
        Identifier = 0xffffffff
        Inconsistent = 0xff6cab9d
        Keyword = 0xff2389da
        NoWarning = 0xff808080
        Number = 0xff74ccf4
        Operator = 0xffffffff
        SingleQuotedString = 0xffc4bbb8
        Spaces = 0xffc4bbb8
        Tabs = 0xffc4bbb8
        TabsAfterSpaces = 0xff74ccf4
        TripleDoubleQuotedString = 0xfff5b0cb
        TripleSingleQuotedString = 0xfff5b0cb
        UnclosedString = 0xffffffff
    
    class Ruby:
        Backticks = 0xffffff00
        ClassName = 0xff5abcd8
        ClassVariable = 0xff8000b0
        Comment = 0xff6cab9d
        DataSection = 0xff600000
        Default = 0xff808080
        DemotedKeyword = 0xff2389da
        DoubleQuotedString = 0xffc4bbb8
        Error = 0xffffffff
        FunctionMethodName = 0xff74ccf4
        Global = 0xff800080
        HereDocument = 0xffc4bbb8
        HereDocumentDelimiter = 0xffffffff
        Identifier = 0xffffffff
        InstanceVariable = 0xffb00080
        Keyword = 0xff2389da
        ModuleName = 0xffa000a0
        Number = 0xff74ccf4
        Operator = 0xffffffff
        POD = 0xff004000
        PercentStringQ = 0xffc4bbb8
        PercentStringq = 0xffc4bbb8
        PercentStringr = 0xffffffff
        PercentStringw = 0xffffffff
        PercentStringx = 0xffffff00
        Regex = 0xffffffff
        SingleQuotedString = 0xffc4bbb8
        Stderr = 0xffffffff
        Stdin = 0xffffffff
        Stdout = 0xffffffff
        Symbol = 0xffc0a030
    
    class SQL:
        Comment = 0xff6cab9d
        CommentDoc = 0xff7f7f7f
        CommentDocKeyword = 0xff3060a0
        CommentDocKeywordError = 0xff804020
        CommentLine = 0xff6cab9d
        CommentLineHash = 0xff6cab9d
        Default = 0xff808080
        DoubleQuotedString = 0xffc4bbb8
        Identifier = 0xffffffff
        Keyword = 0xff2389da
        KeywordSet5 = 0xff4b0082
        KeywordSet6 = 0xffb00040
        KeywordSet7 = 0xff8b0000
        KeywordSet8 = 0xff800080
        Number = 0xff74ccf4
        Operator = 0xffffffff
        PlusComment = 0xff6cab9d
        PlusKeyword = 0xff7f7f00
        PlusPrompt = 0xff6cab9d
        QuotedIdentifier = 0xffffffff
        SingleQuotedString = 0xffc4bbb8
    
    class Spice:
        Command = 0xff2389da
        Comment = 0xff6cab9d
        Default = 0xff808080
        Delimiter = 0xffffffff
        Function = 0xff2389da
        Identifier = 0xffffffff
        Number = 0xff74ccf4
        Parameter = 0xff0040e0
        Value = 0xffc4bbb8
    
    class TCL:
        Comment = 0xff6cab9d
        CommentBlock = 0xffffffff
        CommentBox = 0xff6cab9d
        CommentLine = 0xff6cab9d
        Default = 0xff808080
        ExpandKeyword = 0xff2389da
        ITCLKeyword = 0xff2389da
        Identifier = 0xff2389da
        KeywordSet6 = 0xff2389da
        KeywordSet7 = 0xff2389da
        KeywordSet8 = 0xff2389da
        KeywordSet9 = 0xff2389da
        Modifier = 0xffc4bbb8
        Number = 0xff74ccf4
        Operator = 0xffffffff
        QuotedKeyword = 0xffc4bbb8
        QuotedString = 0xffc4bbb8
        Substitution = 0xff7f7f00
        SubstitutionBrace = 0xff7f7f00
        TCLKeyword = 0xff2389da
        TkCommand = 0xff2389da
        TkKeyword = 0xff2389da
    
    class TeX:
        Command = 0xff6cab9d
        Default = 0xff3f3f3f
        Group = 0xfff5b0cb
        Special = 0xff74ccf4
        Symbol = 0xff7f7f00
        Text = 0xffffffff
    
    class VHDL:
        Attribute = 0xff804020
        Comment = 0xff6cab9d
        CommentLine = 0xff3f7f3f
        Default = 0xff800080
        Identifier = 0xffffffff
        Keyword = 0xff2389da
        KeywordSet7 = 0xff804020
        Number = 0xff74ccf4
        Operator = 0xffffffff
        StandardFunction = 0xff808020
        StandardOperator = 0xff74ccf4
        StandardPackage = 0xff208020
        StandardType = 0xff208080
        String = 0xffc4bbb8
        UnclosedString = 0xffffffff
    
    class Verilog:
        Comment = 0xff6cab9d
        CommentBang = 0xff3f7f3f
        CommentLine = 0xff6cab9d
        Default = 0xff808080
        Identifier = 0xffffffff
        Keyword = 0xff2389da
        KeywordSet2 = 0xff74ccf4
        Number = 0xff74ccf4
        Operator = 0xff007070
        Preprocessor = 0xff7f7f00
        String = 0xffc4bbb8
        SystemTask = 0xff804020
        UnclosedString = 0xffffffff
        UserKeywordSet = 0xff2a00ff
    
    class XML:
        ASPAtStart = 0xffffffff
        ASPJavaScriptComment = 0xff6cab9d
        ASPJavaScriptCommentDoc = 0xff7f7f7f
        ASPJavaScriptCommentLine = 0xff6cab9d
        ASPJavaScriptDefault = 0xffffffff
        ASPJavaScriptDoubleQuotedString = 0xffc4bbb8
        ASPJavaScriptKeyword = 0xff2389da
        ASPJavaScriptNumber = 0xff74ccf4
        ASPJavaScriptRegex = 0xffffffff
        ASPJavaScriptSingleQuotedString = 0xffc4bbb8
        ASPJavaScriptStart = 0xff7f7f00
        ASPJavaScriptSymbol = 0xffffffff
        ASPJavaScriptUnclosedString = 0xffffffff
        ASPJavaScriptWord = 0xffffffff
        ASPPythonClassName = 0xff5abcd8
        ASPPythonComment = 0xff6cab9d
        ASPPythonDefault = 0xff808080
        ASPPythonDoubleQuotedString = 0xffc4bbb8
        ASPPythonFunctionMethodName = 0xff74ccf4
        ASPPythonIdentifier = 0xffffffff
        ASPPythonKeyword = 0xff2389da
        ASPPythonNumber = 0xff74ccf4
        ASPPythonOperator = 0xffffffff
        ASPPythonSingleQuotedString = 0xffc4bbb8
        ASPPythonStart = 0xff808080
        ASPPythonTripleDoubleQuotedString = 0xfff5b0cb
        ASPPythonTripleSingleQuotedString = 0xfff5b0cb
        ASPStart = 0xffffffff
        ASPVBScriptComment = 0xff008000
        ASPVBScriptDefault = 0xffffffff
        ASPVBScriptIdentifier = 0xff1f76e4
        ASPVBScriptKeyword = 0xff1f76e4
        ASPVBScriptNumber = 0xff008080
        ASPVBScriptStart = 0xffffffff
        ASPVBScriptString = 0xff800080
        ASPVBScriptUnclosedString = 0xff1f76e4
        ASPXCComment = 0xffffffff
        Attribute = 0xff008080
        CDATA = 0xffedff86
        Default = 0xffffffff
        Entity = 0xff800080
        HTMLComment = 0xff808000
        HTMLDoubleQuotedString = 0xffc4bbb8
        HTMLNumber = 0xff74ccf4
        HTMLSingleQuotedString = 0xffc4bbb8
        HTMLValue = 0xff608060
        JavaScriptComment = 0xff6cab9d
        JavaScriptCommentDoc = 0xff3f703f
        JavaScriptCommentLine = 0xff6cab9d
        JavaScriptDefault = 0xffffffff
        JavaScriptDoubleQuotedString = 0xffc4bbb8
        JavaScriptKeyword = 0xff2389da
        JavaScriptNumber = 0xff74ccf4
        JavaScriptRegex = 0xffffffff
        JavaScriptSingleQuotedString = 0xffc4bbb8
        JavaScriptStart = 0xff7f7f00
        JavaScriptSymbol = 0xffffffff
        JavaScriptUnclosedString = 0xffffffff
        JavaScriptWord = 0xffffffff
        OtherInTag = 0xff800080
        PHPComment = 0xff999999
        PHPCommentLine = 0xff666666
        PHPDefault = 0xffc7dbf5
        PHPDoubleQuotedString = 0xff6cab9d
        PHPDoubleQuotedVariable = 0xff2389da
        PHPKeyword = 0xffc4bbb8
        PHPNumber = 0xffcc9900
        PHPOperator = 0xffffffff
        PHPSingleQuotedString = 0xff009f00
        PHPStart = 0xffedff86
        PHPVariable = 0xff2389da
        PythonClassName = 0xff5abcd8
        PythonComment = 0xff6cab9d
        PythonDefault = 0xff808080
        PythonDoubleQuotedString = 0xffc4bbb8
        PythonFunctionMethodName = 0xff74ccf4
        PythonIdentifier = 0xffffffff
        PythonKeyword = 0xff2389da
        PythonNumber = 0xff74ccf4
        PythonOperator = 0xffffffff
        PythonSingleQuotedString = 0xffc4bbb8
        PythonStart = 0xff808080
        PythonTripleDoubleQuotedString = 0xfff5b0cb
        PythonTripleSingleQuotedString = 0xfff5b0cb
        SGMLBlockDefault = 0xfffff5b2
        SGMLCommand = 0xff1f76e4
        SGMLComment = 0xff808000
        SGMLDefault = 0xff1f76e4
        SGMLDoubleQuotedString = 0xffedff86
        SGMLEntity = 0xff333333
        SGMLError = 0xffedff86
        SGMLParameter = 0xff006600
        SGMLParameterComment = 0xffffffff
        SGMLSingleQuotedString = 0xff993300
        SGMLSpecial = 0xff3366ff
        Script = 0xff1f76e4
        Tag = 0xff1f76e4
        UnknownAttribute = 0xff008080
        UnknownTag = 0xff1f76e4
        VBScriptComment = 0xff008000
        VBScriptDefault = 0xffffffff
        VBScriptIdentifier = 0xff1f76e4
        VBScriptKeyword = 0xff1f76e4
        VBScriptNumber = 0xff008080
        VBScriptStart = 0xffffffff
        VBScriptString = 0xff800080
        VBScriptUnclosedString = 0xff1f76e4
        XMLEnd = 0xff800080
        XMLStart = 0xff800080
        XMLTagEnd = 0xff1f76e4
    
    class YAML:
        Comment = 0xff008800
        Default = 0xffffffff
        DocumentDelimiter = 0xff112435
        Identifier = 0xfff3c969
        Keyword = 0xff880088
        Number = 0xff880000
        Operator = 0xffffffff
        Reference = 0xff008888
        SyntaxErrorMarker = 0xff112435
        TextBlockMarker = 0xff333366


class Paper:
    Default = PyQt4.QtGui.QColor(0xff112435)
    
    class Ada:
        Default = 0xff112435
        Comment = 0xff112435
        Keyword = 0xff112435
        String = 0xff112435
        Procedure = 0xff112435
        Number = 0xff112435
        Type = 0xff112435
        Package = 0xff112435
    
    class Nim:
        Default = 0xff112435
        Comment = 0xff112435
        BasicKeyword = 0xff112435
        TopKeyword = 0xff112435
        String = 0xff112435
        LongString = 0xff112435
        Number = 0xff112435
        Operator = 0xff112435
        Unsafe = 0xff112435
        Type = 0xff112435
        DocumentationComment = 0xff112435
        Definition = 0xff112435
        Class = 0xff112435
        KeywordOperator = 0xff112435
        CharLiteral = 0xff112435
        CaseOf = 0xff112435
        UserKeyword = 0xff112435
        MultilineComment = 0xff112435
        MultilineDocumentation = 0xff112435
        Pragma = 0xff112435
    
    class Oberon:
        Default = 0xff112435
        Comment = 0xff112435
        Keyword = 0xff112435
        String = 0xff112435
        Procedure = 0xff112435
        Module = 0xff112435
        Number = 0xff112435
        Type = 0xff112435
    
    
    # Generated
    class AVS:
        Function = 0xff112435
        KeywordSet6 = 0xff112435
        TripleString = 0xff112435
        LineComment = 0xff112435
        Plugin = 0xff112435
        String = 0xff112435
        ClipProperty = 0xff112435
        Default = 0xff112435
        Operator = 0xff112435
        Number = 0xff112435
        Filter = 0xff112435
        Identifier = 0xff112435
        NestedBlockComment = 0xff112435
        Keyword = 0xff112435
        BlockComment = 0xff112435
    
    class Bash:
        Error = 0xffff0000
        Backticks = 0xffa08080
        SingleQuotedHereDocument = 0xffddd0dd
        Scalar = 0xffffe0e0
        HereDocumentDelimiter = 0xffddd0dd
        Comment = 0xff112435
        SingleQuotedString = 0xff112435
        Default = 0xff112435
        Operator = 0xff112435
        ParameterExpansion = 0xffffffe0
        Number = 0xff112435
        Identifier = 0xff112435
        Keyword = 0xff112435
        DoubleQuotedString = 0xff112435
    
    class Batch:
        Label = 0xff606060
        Default = 0xff112435
        Keyword = 0xff112435
        ExternalCommand = 0xff112435
        Variable = 0xff112435
        Comment = 0xff112435
        HideCommandChar = 0xff112435
        Operator = 0xff112435
    
    class CMake:
        Function = 0xff112435
        BlockForeach = 0xff112435
        BlockWhile = 0xff112435
        StringLeftQuote = 0xffeeeeee
        Label = 0xff112435
        Comment = 0xff112435
        BlockMacro = 0xff112435
        StringRightQuote = 0xffeeeeee
        Default = 0xff112435
        Number = 0xff112435
        BlockIf = 0xff112435
        Variable = 0xff112435
        KeywordSet3 = 0xff112435
        String = 0xffeeeeee
        StringVariable = 0xffeeeeee
    
    class CPP:
        CommentDocKeywordError = 0xff112435
        InactiveRegex = 0xffe0f0e0
        InactivePreProcessorComment = 0xff112435
        UUID = 0xff112435
        InactiveVerbatimString = 0xffe0ffe0
        SingleQuotedString = 0xff112435
        Operator = 0xff112435
        InactiveOperator = 0xff112435
        InactivePreProcessor = 0xff112435
        UnclosedString = 0xffe0c0e0
        Identifier = 0xff112435
        InactiveRawString = 0xff112435
        PreProcessor = 0xff112435
        KeywordSet2 = 0xff112435
        InactiveUnclosedString = 0xffe0c0e0
        InactiveCommentLine = 0xff112435
        InactiveNumber = 0xff112435
        InactivePreProcessorCommentLineDoc = 0xff112435
        Number = 0xff112435
        InactiveUUID = 0xff112435
        CommentDoc = 0xff112435
        InactiveCommentDoc = 0xff112435
        GlobalClass = 0xff112435
        InactiveSingleQuotedString = 0xff112435
        HashQuotedString = 0xffe7ffd7
        VerbatimString = 0xffe0ffe0
        InactiveHashQuotedString = 0xff112435
        Regex = 0xffe0f0e0
        InactiveGlobalClass = 0xff112435
        InactiveIdentifier = 0xff112435
        CommentLineDoc = 0xff112435
        TripleQuotedVerbatimString = 0xffe0ffe0
        InactiveKeywordSet2 = 0xff112435
        InactiveCommentDocKeyword = 0xff112435
        Keyword = 0xff112435
        InactiveCommentLineDoc = 0xff112435
        InactiveDefault = 0xff112435
        InactiveCommentDocKeywordError = 0xff112435
        InactiveTripleQuotedVerbatimString = 0xff112435
        CommentDocKeyword = 0xff112435
        InactiveDoubleQuotedString = 0xff112435
        CommentLine = 0xff112435
        Comment = 0xff112435
        PreProcessorComment = 0xff112435
        InactiveComment = 0xff112435
        RawString = 0xfffff3ff
        Default = 0xff112435
        PreProcessorCommentLineDoc = 0xff112435
        DoubleQuotedString = 0xff112435
        InactiveKeyword = 0xff112435
    
    class CSS:
        Important = 0xff112435
        CSS3Property = 0xff112435
        Attribute = 0xff112435
        Comment = 0xff112435
        SingleQuotedString = 0xff112435
        MediaRule = 0xff112435
        AtRule = 0xff112435
        UnknownPseudoClass = 0xff112435
        PseudoClass = 0xff112435
        Tag = 0xff112435
        CSS2Property = 0xff112435
        CSS1Property = 0xff112435
        IDSelector = 0xff112435
        ExtendedCSSProperty = 0xff112435
        Variable = 0xff112435
        ExtendedPseudoClass = 0xff112435
        ClassSelector = 0xff112435
        Default = 0xff112435
        PseudoElement = 0xff112435
        UnknownProperty = 0xff112435
        Value = 0xff112435
        ExtendedPseudoElement = 0xff112435
        DoubleQuotedString = 0xff112435
        Operator = 0xff112435
    
    class CSharp:
        CommentDocKeywordError = 0xff112435
        InactiveRegex = 0xff112435
        InactivePreProcessorComment = 0xff112435
        UUID = 0xff112435
        InactiveVerbatimString = 0xff112435
        SingleQuotedString = 0xff112435
        Operator = 0xff112435
        InactiveOperator = 0xff112435
        InactivePreProcessor = 0xff112435
        UnclosedString = 0xff112435
        Identifier = 0xff112435
        InactiveRawString = 0xff112435
        PreProcessor = 0xff112435
        KeywordSet2 = 0xff112435
        InactiveUnclosedString = 0xff112435
        InactiveCommentLine = 0xff112435
        InactiveNumber = 0xff112435
        InactivePreProcessorCommentLineDoc = 0xff112435
        Number = 0xff112435
        InactiveUUID = 0xff112435
        CommentDoc = 0xff112435
        InactiveCommentDoc = 0xff112435
        GlobalClass = 0xff112435
        InactiveSingleQuotedString = 0xff112435
        HashQuotedString = 0xff112435
        VerbatimString = 0xffe0ffe0
        InactiveHashQuotedString = 0xff112435
        Regex = 0xff112435
        InactiveGlobalClass = 0xff112435
        InactiveIdentifier = 0xff112435
        CommentLineDoc = 0xff112435
        TripleQuotedVerbatimString = 0xff112435
        InactiveKeywordSet2 = 0xff112435
        InactiveCommentDocKeyword = 0xff112435
        Keyword = 0xff112435
        InactiveCommentLineDoc = 0xff112435
        InactiveDefault = 0xff112435
        InactiveCommentDocKeywordError = 0xff112435
        InactiveTripleQuotedVerbatimString = 0xff112435
        CommentDocKeyword = 0xff112435
        InactiveDoubleQuotedString = 0xff112435
        CommentLine = 0xff112435
        Comment = 0xff112435
        PreProcessorComment = 0xff112435
        InactiveComment = 0xff112435
        RawString = 0xff112435
        Default = 0xff112435
        PreProcessorCommentLineDoc = 0xff112435
        DoubleQuotedString = 0xff112435
        InactiveKeyword = 0xff112435
    
    class CoffeeScript:
        UUID = 0xff112435
        CommentDocKeywordError = 0xff112435
        GlobalClass = 0xff112435
        VerbatimString = 0xffe0ffe0
        SingleQuotedString = 0xff112435
        Operator = 0xff112435
        Number = 0xff112435
        Identifier = 0xff112435
        Keyword = 0xff112435
        UnclosedString = 0xffe0c0e0
        Regex = 0xffe0f0e0
        CommentDocKeyword = 0xff112435
        BlockRegex = 0xff112435
        CommentLineDoc = 0xff112435
        PreProcessor = 0xff112435
        CommentLine = 0xff112435
        CommentBlock = 0xff112435
        Comment = 0xff112435
        KeywordSet2 = 0xff112435
        BlockRegexComment = 0xff112435
        Default = 0xff112435
        DoubleQuotedString = 0xff112435
        CommentDoc = 0xff112435
    
    class D:
        BackquoteString = 0xff112435
        CommentDocKeywordError = 0xff112435
        Operator = 0xff112435
        CommentNested = 0xff112435
        KeywordDoc = 0xff112435
        KeywordSet7 = 0xff112435
        Keyword = 0xff112435
        KeywordSecondary = 0xff112435
        Identifier = 0xff112435
        KeywordSet5 = 0xff112435
        CommentDocKeyword = 0xff112435
        KeywordSet6 = 0xff112435
        CommentLineDoc = 0xff112435
        CommentLine = 0xff112435
        Comment = 0xff112435
        Typedefs = 0xff112435
        Character = 0xff112435
        RawString = 0xff112435
        Default = 0xff112435
        Number = 0xff112435
        UnclosedString = 0xffe0c0e0
        String = 0xff112435
        CommentDoc = 0xff112435
    
    class Diff:
        Header = 0xff112435
        LineChanged = 0xff112435
        Default = 0xff112435
        LineRemoved = 0xff112435
        Command = 0xff112435
        Position = 0xff112435
        LineAdded = 0xff112435
        Comment = 0xff112435
    
    class Fortran:
        Label = 0xff112435
        Identifier = 0xff112435
        DottedOperator = 0xff112435
        PreProcessor = 0xff112435
        Comment = 0xff112435
        SingleQuotedString = 0xff112435
        Default = 0xff112435
        DoubleQuotedString = 0xff112435
        ExtendedFunction = 0xff112435
        UnclosedString = 0xffe0c0e0
        Number = 0xff112435
        Continuation = 0xfff0e080
        IntrinsicFunction = 0xff112435
        Keyword = 0xff112435
        Operator = 0xff112435
    
    class Fortran77:
        Label = 0xff112435
        Identifier = 0xff112435
        DottedOperator = 0xff112435
        PreProcessor = 0xff112435
        Comment = 0xff112435
        SingleQuotedString = 0xff112435
        Default = 0xff112435
        DoubleQuotedString = 0xff112435
        ExtendedFunction = 0xff112435
        UnclosedString = 0xffe0c0e0
        Number = 0xff112435
        Continuation = 0xfff0e080
        IntrinsicFunction = 0xff112435
        Keyword = 0xff112435
        Operator = 0xff112435
    
    class HTML:
        HTMLValue = 0xffffefff
        PythonDefault = 0xffefffef
        Entity = 0xff112435
        SGMLParameter = 0xffefefff
        SGMLDefault = 0xffefefff
        PHPVariable = 0xfffff8f8
        SGMLCommand = 0xffefefff
        PythonClassName = 0xffefffef
        VBScriptUnclosedString = 0xff7f7fff
        ASPJavaScriptDefault = 0xffdfdf7f
        ASPVBScriptStart = 0xff112435
        VBScriptDefault = 0xffefefff
        PythonNumber = 0xffefffef
        PythonOperator = 0xffefffef
        ASPJavaScriptSingleQuotedString = 0xffdfdf7f
        PHPDefault = 0xfffff8f8
        XMLStart = 0xff112435
        PythonFunctionMethodName = 0xffefffef
        ASPJavaScriptStart = 0xff112435
        JavaScriptWord = 0xfff0f0ff
        PHPSingleQuotedString = 0xfffff8f8
        PythonTripleDoubleQuotedString = 0xffefffef
        JavaScriptComment = 0xfff0f0ff
        Default = 0xff112435
        SGMLSingleQuotedString = 0xffefefff
        VBScriptComment = 0xffefefff
        ASPVBScriptNumber = 0xffcfcfef
        ASPJavaScriptCommentDoc = 0xffdfdf7f
        PythonIdentifier = 0xffefffef
        VBScriptKeyword = 0xffefefff
        JavaScriptDefault = 0xfff0f0ff
        PythonStart = 0xff112435
        ASPPythonComment = 0xffcfefcf
        ASPJavaScriptWord = 0xffdfdf7f
        SGMLParameterComment = 0xff112435
        JavaScriptSingleQuotedString = 0xfff0f0ff
        PythonSingleQuotedString = 0xffefffef
        HTMLSingleQuotedString = 0xff112435
        ASPVBScriptString = 0xffcfcfef
        SGMLBlockDefault = 0xffcccce0
        PythonKeyword = 0xffefffef
        XMLTagEnd = 0xff112435
        ASPVBScriptComment = 0xffcfcfef
        ASPPythonSingleQuotedString = 0xffcfefcf
        PHPDoubleQuotedVariable = 0xfffff8f8
        ASPJavaScriptComment = 0xffdfdf7f
        JavaScriptUnclosedString = 0xffbfbbb0
        JavaScriptDoubleQuotedString = 0xfff0f0ff
        UnknownAttribute = 0xff112435
        ASPPythonOperator = 0xffcfefcf
        ASPJavaScriptSymbol = 0xffdfdf7f
        ASPPythonFunctionMethodName = 0xffcfefcf
        SGMLDoubleQuotedString = 0xffefefff
        PHPOperator = 0xfffff8f8
        JavaScriptNumber = 0xfff0f0ff
        PythonDoubleQuotedString = 0xffefffef
        ASPAtStart = 0xffffff00
        Script = 0xff112435
        PHPCommentLine = 0xfffff8f8
        SGMLComment = 0xffefefff
        JavaScriptStart = 0xff112435
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
        OtherInTag = 0xff112435
        JavaScriptCommentDoc = 0xfff0f0ff
        Tag = 0xff112435
        XMLEnd = 0xff112435
        CDATA = 0xffffdf00
        HTMLNumber = 0xff112435
        SGMLError = 0xffff6666
        PHPKeyword = 0xfffff8f8
        ASPVBScriptUnclosedString = 0xff7f7fff
        ASPPythonNumber = 0xffcfefcf
        VBScriptString = 0xffefefff
        ASPPythonClassName = 0xffcfefcf
        ASPPythonStart = 0xff112435
        JavaScriptRegex = 0xffffbbb0
        ASPJavaScriptUnclosedString = 0xffbfbbb0
        ASPJavaScriptCommentLine = 0xffdfdf7f
        SGMLEntity = 0xffefefff
        ASPJavaScriptDoubleQuotedString = 0xffdfdf7f
        ASPStart = 0xffffdf00
        Attribute = 0xff112435
        ASPJavaScriptKeyword = 0xffdfdf7f
        ASPVBScriptDefault = 0xffcfcfef
        ASPVBScriptIdentifier = 0xffcfcfef
        ASPJavaScriptRegex = 0xffffbbb0
        VBScriptNumber = 0xffefefff
        HTMLDoubleQuotedString = 0xff112435
        ASPXCComment = 0xff112435
        VBScriptStart = 0xff112435
        PHPDoubleQuotedString = 0xfffff8f8
        PHPComment = 0xfffff8f8
        ASPPythonTripleSingleQuotedString = 0xffcfefcf
        ASPPythonDoubleQuotedString = 0xffcfefcf
        JavaScriptKeyword = 0xfff0f0ff
        JavaScriptSymbol = 0xfff0f0ff
        VBScriptIdentifier = 0xffefefff
        HTMLComment = 0xff112435
        UnknownTag = 0xff112435
        JavaScriptCommentLine = 0xfff0f0ff
        PythonComment = 0xffefffef
    
    class IDL:
        CommentDocKeywordError = 0xff112435
        InactiveRegex = 0xffe0f0e0
        InactivePreProcessorComment = 0xff112435
        UUID = 0xff112435
        InactiveVerbatimString = 0xffe0ffe0
        SingleQuotedString = 0xff112435
        Operator = 0xff112435
        InactiveOperator = 0xff112435
        InactivePreProcessor = 0xff112435
        UnclosedString = 0xffe0c0e0
        Identifier = 0xff112435
        InactiveRawString = 0xff112435
        PreProcessor = 0xff112435
        KeywordSet2 = 0xff112435
        InactiveUnclosedString = 0xffe0c0e0
        InactiveCommentLine = 0xff112435
        InactiveNumber = 0xff112435
        InactivePreProcessorCommentLineDoc = 0xff112435
        Number = 0xff112435
        InactiveUUID = 0xff112435
        CommentDoc = 0xff112435
        InactiveCommentDoc = 0xff112435
        GlobalClass = 0xff112435
        InactiveSingleQuotedString = 0xff112435
        HashQuotedString = 0xffe7ffd7
        VerbatimString = 0xffe0ffe0
        InactiveHashQuotedString = 0xff112435
        Regex = 0xffe0f0e0
        InactiveGlobalClass = 0xff112435
        InactiveIdentifier = 0xff112435
        CommentLineDoc = 0xff112435
        TripleQuotedVerbatimString = 0xffe0ffe0
        InactiveKeywordSet2 = 0xff112435
        InactiveCommentDocKeyword = 0xff112435
        Keyword = 0xff112435
        InactiveCommentLineDoc = 0xff112435
        InactiveDefault = 0xff112435
        InactiveCommentDocKeywordError = 0xff112435
        InactiveTripleQuotedVerbatimString = 0xff112435
        CommentDocKeyword = 0xff112435
        InactiveDoubleQuotedString = 0xff112435
        CommentLine = 0xff112435
        Comment = 0xff112435
        PreProcessorComment = 0xff112435
        InactiveComment = 0xff112435
        RawString = 0xfffff3ff
        Default = 0xff112435
        PreProcessorCommentLineDoc = 0xff112435
        DoubleQuotedString = 0xff112435
        InactiveKeyword = 0xff112435
    
    class Java:
        CommentDocKeywordError = 0xff112435
        InactiveRegex = 0xffe0f0e0
        InactivePreProcessorComment = 0xff112435
        UUID = 0xff112435
        InactiveVerbatimString = 0xffe0ffe0
        SingleQuotedString = 0xff112435
        Operator = 0xff112435
        InactiveOperator = 0xff112435
        InactivePreProcessor = 0xff112435
        UnclosedString = 0xffe0c0e0
        Identifier = 0xff112435
        InactiveRawString = 0xff112435
        PreProcessor = 0xff112435
        KeywordSet2 = 0xff112435
        InactiveUnclosedString = 0xffe0c0e0
        InactiveCommentLine = 0xff112435
        InactiveNumber = 0xff112435
        InactivePreProcessorCommentLineDoc = 0xff112435
        Number = 0xff112435
        InactiveUUID = 0xff112435
        CommentDoc = 0xff112435
        InactiveCommentDoc = 0xff112435
        GlobalClass = 0xff112435
        InactiveSingleQuotedString = 0xff112435
        HashQuotedString = 0xffe7ffd7
        VerbatimString = 0xffe0ffe0
        InactiveHashQuotedString = 0xff112435
        Regex = 0xffe0f0e0
        InactiveGlobalClass = 0xff112435
        InactiveIdentifier = 0xff112435
        CommentLineDoc = 0xff112435
        TripleQuotedVerbatimString = 0xffe0ffe0
        InactiveKeywordSet2 = 0xff112435
        InactiveCommentDocKeyword = 0xff112435
        Keyword = 0xff112435
        InactiveCommentLineDoc = 0xff112435
        InactiveDefault = 0xff112435
        InactiveCommentDocKeywordError = 0xff112435
        InactiveTripleQuotedVerbatimString = 0xff112435
        CommentDocKeyword = 0xff112435
        InactiveDoubleQuotedString = 0xff112435
        CommentLine = 0xff112435
        Comment = 0xff112435
        PreProcessorComment = 0xff112435
        InactiveComment = 0xff112435
        RawString = 0xfffff3ff
        Default = 0xff112435
        PreProcessorCommentLineDoc = 0xff112435
        DoubleQuotedString = 0xff112435
        InactiveKeyword = 0xff112435
    
    class JavaScript:
        CommentDocKeywordError = 0xff112435
        InactiveRegex = 0xff112435
        InactivePreProcessorComment = 0xff112435
        UUID = 0xff112435
        InactiveVerbatimString = 0xff112435
        SingleQuotedString = 0xff112435
        Operator = 0xff112435
        InactiveOperator = 0xff112435
        InactivePreProcessor = 0xff112435
        UnclosedString = 0xff112435
        Identifier = 0xff112435
        InactiveRawString = 0xff112435
        PreProcessor = 0xff112435
        KeywordSet2 = 0xff112435
        InactiveUnclosedString = 0xff112435
        InactiveCommentLine = 0xff112435
        InactiveNumber = 0xff112435
        InactivePreProcessorCommentLineDoc = 0xff112435
        Number = 0xff112435
        InactiveUUID = 0xff112435
        CommentDoc = 0xff112435
        InactiveCommentDoc = 0xff112435
        GlobalClass = 0xff112435
        InactiveSingleQuotedString = 0xff112435
        HashQuotedString = 0xff112435
        VerbatimString = 0xff112435
        InactiveHashQuotedString = 0xff112435
        Regex = 0xffe0f0ff
        InactiveGlobalClass = 0xff112435
        InactiveIdentifier = 0xff112435
        CommentLineDoc = 0xff112435
        TripleQuotedVerbatimString = 0xff112435
        InactiveKeywordSet2 = 0xff112435
        InactiveCommentDocKeyword = 0xff112435
        Keyword = 0xff112435
        InactiveCommentLineDoc = 0xff112435
        InactiveDefault = 0xff112435
        InactiveCommentDocKeywordError = 0xff112435
        InactiveTripleQuotedVerbatimString = 0xff112435
        CommentDocKeyword = 0xff112435
        InactiveDoubleQuotedString = 0xff112435
        CommentLine = 0xff112435
        Comment = 0xff112435
        PreProcessorComment = 0xff112435
        InactiveComment = 0xff112435
        RawString = 0xff112435
        Default = 0xff112435
        PreProcessorCommentLineDoc = 0xff112435
        DoubleQuotedString = 0xff112435
        InactiveKeyword = 0xff112435
    
    class Lua:
        Label = 0xff112435
        Identifier = 0xff112435
        StringTableMathsFunctions = 0xffd0d0ff
        CoroutinesIOSystemFacilities = 0xffffd0d0
        KeywordSet5 = 0xff112435
        KeywordSet6 = 0xff112435
        Preprocessor = 0xff112435
        LineComment = 0xff112435
        Comment = 0xffd0f0f0
        String = 0xff112435
        Character = 0xff112435
        Default = 0xff112435
        Operator = 0xff112435
        LiteralString = 0xffe0ffff
        Number = 0xff112435
        KeywordSet8 = 0xff112435
        KeywordSet7 = 0xff112435
        BasicFunctions = 0xffd0ffd0
        Keyword = 0xff112435
        UnclosedString = 0xffe0c0e0
    
    class Makefile:
        Default = 0xff112435
        Operator = 0xff112435
        Target = 0xff112435
        Preprocessor = 0xff112435
        Variable = 0xff112435
        Comment = 0xff112435
        Error = 0xffff0000
    
    class Matlab:
        SingleQuotedString = 0xff112435
        Default = 0xff112435
        Keyword = 0xff112435
        Number = 0xff112435
        Command = 0xff112435
        Identifier = 0xff112435
        Comment = 0xff112435
        DoubleQuotedString = 0xff112435
        Operator = 0xff112435
    
    class Octave:
        SingleQuotedString = 0xff112435
        Default = 0xff112435
        Keyword = 0xff112435
        Number = 0xff112435
        Command = 0xff112435
        Identifier = 0xff112435
        Comment = 0xff112435
        DoubleQuotedString = 0xff112435
        Operator = 0xff112435
    
    class PO:
        ProgrammerComment = 0xff112435
        Flags = 0xff112435
        MessageContextText = 0xff112435
        MessageStringTextEOL = 0xff112435
        MessageId = 0xff112435
        MessageIdText = 0xff112435
        Reference = 0xff112435
        Comment = 0xff112435
        MessageStringText = 0xff112435
        MessageContext = 0xff112435
        Fuzzy = 0xff112435
        Default = 0xff112435
        MessageString = 0xff112435
        MessageContextTextEOL = 0xff112435
        MessageIdTextEOL = 0xff112435
    
    class POV:
        KeywordSet7 = 0xffd0d0d0
        KeywordSet6 = 0xffd0ffd0
        PredefinedFunctions = 0xffd0d0ff
        CommentLine = 0xff112435
        PredefinedIdentifiers = 0xff112435
        Comment = 0xff112435
        Directive = 0xff112435
        String = 0xff112435
        BadDirective = 0xff112435
        TypesModifiersItems = 0xffffffd0
        Default = 0xff112435
        Operator = 0xff112435
        Number = 0xff112435
        KeywordSet8 = 0xffe0e0e0
        Identifier = 0xff112435
        ObjectsCSGAppearance = 0xffffd0d0
        UnclosedString = 0xffe0c0e0
    
    class Pascal:
        PreProcessorParenthesis = 0xff112435
        SingleQuotedString = 0xff112435
        PreProcessor = 0xff112435
        CommentLine = 0xff112435
        Comment = 0xff112435
        CommentParenthesis = 0xff112435
        Asm = 0xff112435
        Character = 0xff112435
        Default = 0xff112435
        Operator = 0xff112435
        UnclosedString = 0xffe0c0e0
        Number = 0xff112435
        Identifier = 0xff112435
        Keyword = 0xff112435
        HexNumber = 0xff112435
    
    class Perl:
        Translation = 0xfff0e080
        BacktickHereDocument = 0xffddd0dd
        Array = 0xffffffe0
        QuotedStringQXVar = 0xffa08080
        PODVerbatim = 0xffc0ffc0
        DoubleQuotedStringVar = 0xff112435
        Regex = 0xffa0ffa0
        HereDocumentDelimiter = 0xffddd0dd
        SubroutinePrototype = 0xff112435
        BacktickHereDocumentVar = 0xffddd0dd
        QuotedStringQR = 0xff112435
        SingleQuotedString = 0xff112435
        QuotedStringQRVar = 0xff112435
        SubstitutionVar = 0xff112435
        Operator = 0xff112435
        DoubleQuotedHereDocumentVar = 0xffddd0dd
        Identifier = 0xff112435
        QuotedStringQX = 0xff112435
        BackticksVar = 0xffa08080
        Keyword = 0xff112435
        QuotedStringQ = 0xff112435
        QuotedStringQQVar = 0xff112435
        QuotedStringQQ = 0xff112435
        POD = 0xffe0ffe0
        FormatIdentifier = 0xff112435
        RegexVar = 0xff112435
        Backticks = 0xffa08080
        DoubleQuotedHereDocument = 0xffddd0dd
        Scalar = 0xffffe0e0
        FormatBody = 0xfffff0ff
        Comment = 0xff112435
        QuotedStringQW = 0xff112435
        SymbolTable = 0xffe0e0e0
        Default = 0xff112435
        Error = 0xffff0000
        SingleQuotedHereDocument = 0xffddd0dd
        Number = 0xff112435
        Hash = 0xffffe0ff
        Substitution = 0xfff0e080
        DataSection = 0xfffff0d8
        DoubleQuotedString = 0xff112435
    
    class PostScript:
        DictionaryParenthesis = 0xff112435
        HexString = 0xff112435
        DSCCommentValue = 0xff112435
        ProcedureParenthesis = 0xff112435
        Comment = 0xff112435
        ImmediateEvalLiteral = 0xff112435
        Name = 0xff112435
        DSCComment = 0xff112435
        Default = 0xff112435
        Base85String = 0xff112435
        Number = 0xff112435
        ArrayParenthesis = 0xff112435
        Literal = 0xff112435
        BadStringCharacter = 0xffff0000
        Text = 0xff112435
        Keyword = 0xff112435
    
    class Properties:
        DefaultValue = 0xff112435
        Default = 0xff112435
        Section = 0xffe0f0f0
        Assignment = 0xff112435
        Key = 0xff112435
        Comment = 0xff112435
    
    class Python:
        TripleDoubleQuotedString = 0xff112435
        FunctionMethodName = 0xff112435
        TabsAfterSpaces = 0xff112435
        Tabs = 0xff112435
        Decorator = 0xff112435
        NoWarning = 0xff112435
        UnclosedString = 0xffe0c0e0
        Spaces = 0xff112435
        CommentBlock = 0xff112435
        Comment = 0xff112435
        TripleSingleQuotedString = 0xff112435
        SingleQuotedString = 0xff112435
        Inconsistent = 0xff112435
        Default = 0xff112435
        DoubleQuotedString = 0xff112435
        Operator = 0xff112435
        Number = 0xff112435
        Identifier = 0xff112435
        ClassName = 0xff112435
        Keyword = 0xff112435
        HighlightedIdentifier = 0xff112435
    
    class Ruby:
        Symbol = 0xff112435
        Stderr = 0xffff8080
        Global = 0xff112435
        FunctionMethodName = 0xff112435
        Stdin = 0xffff8080
        HereDocumentDelimiter = 0xffddd0dd
        PercentStringr = 0xffa0ffa0
        PercentStringQ = 0xff112435
        ModuleName = 0xff112435
        HereDocument = 0xffddd0dd
        SingleQuotedString = 0xff112435
        PercentStringq = 0xff112435
        Regex = 0xffa0ffa0
        Operator = 0xff112435
        PercentStringw = 0xffffffe0
        PercentStringx = 0xffa08080
        POD = 0xffc0ffc0
        Keyword = 0xff112435
        Stdout = 0xffff8080
        ClassVariable = 0xff112435
        Identifier = 0xff112435
        DemotedKeyword = 0xff112435
        Backticks = 0xffa08080
        InstanceVariable = 0xff112435
        Comment = 0xff112435
        Default = 0xff112435
        Error = 0xffff0000
        Number = 0xff112435
        DataSection = 0xfffff0d8
        ClassName = 0xff112435
        DoubleQuotedString = 0xff112435
    
    class SQL:
        PlusComment = 0xff112435
        KeywordSet7 = 0xff112435
        PlusPrompt = 0xffe0ffe0
        CommentDocKeywordError = 0xff112435
        CommentDocKeyword = 0xff112435
        KeywordSet6 = 0xff112435
        CommentLine = 0xff112435
        Comment = 0xff112435
        Operator = 0xff112435
        QuotedIdentifier = 0xff112435
        SingleQuotedString = 0xff112435
        PlusKeyword = 0xff112435
        Default = 0xff112435
        DoubleQuotedString = 0xff112435
        CommentLineHash = 0xff112435
        KeywordSet5 = 0xff112435
        Number = 0xff112435
        KeywordSet8 = 0xff112435
        Identifier = 0xff112435
        Keyword = 0xff112435
        CommentDoc = 0xff112435
    
    class Spice:
        Function = 0xff112435
        Delimiter = 0xff112435
        Value = 0xff112435
        Default = 0xff112435
        Number = 0xff112435
        Parameter = 0xff112435
        Command = 0xff112435
        Identifier = 0xff112435
        Comment = 0xff112435
    
    class TCL:
        SubstitutionBrace = 0xff112435
        CommentBox = 0xfff0fff0
        ITCLKeyword = 0xfffff0f0
        TkKeyword = 0xffe0fff0
        Operator = 0xff112435
        QuotedString = 0xfffff0f0
        ExpandKeyword = 0xffffff80
        KeywordSet7 = 0xff112435
        TCLKeyword = 0xff112435
        TkCommand = 0xffffd0d0
        Identifier = 0xff112435
        KeywordSet6 = 0xff112435
        CommentLine = 0xff112435
        CommentBlock = 0xfff0fff0
        Comment = 0xfff0ffe0
        Default = 0xff112435
        KeywordSet9 = 0xff112435
        Modifier = 0xff112435
        Number = 0xff112435
        KeywordSet8 = 0xff112435
        Substitution = 0xffeffff0
        QuotedKeyword = 0xfffff0f0
    
    class TeX:
        Symbol = 0xff112435
        Default = 0xff112435
        Command = 0xff112435
        Group = 0xff112435
        Text = 0xff112435
        Special = 0xff112435
    
    class VHDL:
        StandardOperator = 0xff112435
        Attribute = 0xff112435
        CommentLine = 0xff112435
        Comment = 0xff112435
        String = 0xff112435
        Default = 0xff112435
        Operator = 0xff112435
        StandardPackage = 0xff112435
        Number = 0xff112435
        Identifier = 0xff112435
        KeywordSet7 = 0xff112435
        StandardFunction = 0xff112435
        StandardType = 0xff112435
        Keyword = 0xff112435
        UnclosedString = 0xffe0c0e0
    
    class Verilog:
        CommentBang = 0xffe0f0ff
        UserKeywordSet = 0xff112435
        Preprocessor = 0xff112435
        CommentLine = 0xff112435
        Comment = 0xff112435
        KeywordSet2 = 0xff112435
        Default = 0xff112435
        Operator = 0xff112435
        Number = 0xff112435
        Identifier = 0xff112435
        SystemTask = 0xff112435
        String = 0xff112435
        Keyword = 0xff112435
        UnclosedString = 0xffe0c0e0
    
    class XML:
        HTMLValue = 0xffffefff
        PythonDefault = 0xffefffef
        Entity = 0xff112435
        SGMLParameter = 0xffefefff
        SGMLDefault = 0xffefefff
        PHPVariable = 0xfffff8f8
        SGMLCommand = 0xffefefff
        PythonClassName = 0xffefffef
        VBScriptUnclosedString = 0xff7f7fff
        ASPJavaScriptDefault = 0xffdfdf7f
        ASPVBScriptStart = 0xff112435
        VBScriptDefault = 0xffefefff
        PythonNumber = 0xffefffef
        PythonOperator = 0xffefffef
        ASPJavaScriptSingleQuotedString = 0xffdfdf7f
        PHPDefault = 0xfffff8f8
        XMLStart = 0xff112435
        PythonFunctionMethodName = 0xffefffef
        ASPJavaScriptStart = 0xff112435
        JavaScriptWord = 0xfff0f0ff
        PHPSingleQuotedString = 0xfffff8f8
        PythonTripleDoubleQuotedString = 0xffefffef
        JavaScriptComment = 0xfff0f0ff
        Default = 0xff112435
        SGMLSingleQuotedString = 0xffefefff
        VBScriptComment = 0xffefefff
        ASPVBScriptNumber = 0xffcfcfef
        ASPJavaScriptCommentDoc = 0xffdfdf7f
        PythonIdentifier = 0xffefffef
        VBScriptKeyword = 0xffefefff
        JavaScriptDefault = 0xfff0f0ff
        PythonStart = 0xff112435
        ASPPythonComment = 0xffcfefcf
        ASPJavaScriptWord = 0xffdfdf7f
        SGMLParameterComment = 0xff112435
        JavaScriptSingleQuotedString = 0xfff0f0ff
        PythonSingleQuotedString = 0xffefffef
        HTMLSingleQuotedString = 0xff112435
        ASPVBScriptString = 0xffcfcfef
        SGMLBlockDefault = 0xffcccce0
        PythonKeyword = 0xffefffef
        XMLTagEnd = 0xff112435
        ASPVBScriptComment = 0xffcfcfef
        ASPPythonSingleQuotedString = 0xffcfefcf
        PHPDoubleQuotedVariable = 0xfffff8f8
        ASPJavaScriptComment = 0xffdfdf7f
        JavaScriptUnclosedString = 0xffbfbbb0
        JavaScriptDoubleQuotedString = 0xfff0f0ff
        UnknownAttribute = 0xff112435
        ASPPythonOperator = 0xffcfefcf
        ASPJavaScriptSymbol = 0xffdfdf7f
        ASPPythonFunctionMethodName = 0xffcfefcf
        SGMLDoubleQuotedString = 0xffefefff
        PHPOperator = 0xfffff8f8
        JavaScriptNumber = 0xfff0f0ff
        PythonDoubleQuotedString = 0xffefffef
        ASPAtStart = 0xffffff00
        Script = 0xff112435
        PHPCommentLine = 0xfffff8f8
        SGMLComment = 0xffefefff
        JavaScriptStart = 0xff112435
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
        OtherInTag = 0xff112435
        JavaScriptCommentDoc = 0xfff0f0ff
        Tag = 0xff112435
        XMLEnd = 0xff112435
        CDATA = 0xfffff0f0
        HTMLNumber = 0xff112435
        SGMLError = 0xffff6666
        PHPKeyword = 0xfffff8f8
        ASPVBScriptUnclosedString = 0xff7f7fff
        ASPPythonNumber = 0xffcfefcf
        VBScriptString = 0xffefefff
        ASPPythonClassName = 0xffcfefcf
        ASPPythonStart = 0xff112435
        JavaScriptRegex = 0xffffbbb0
        ASPJavaScriptUnclosedString = 0xffbfbbb0
        ASPJavaScriptCommentLine = 0xffdfdf7f
        SGMLEntity = 0xffefefff
        ASPJavaScriptDoubleQuotedString = 0xffdfdf7f
        ASPStart = 0xffffdf00
        Attribute = 0xff112435
        ASPJavaScriptKeyword = 0xffdfdf7f
        ASPVBScriptDefault = 0xffcfcfef
        ASPVBScriptIdentifier = 0xffcfcfef
        ASPJavaScriptRegex = 0xffffbbb0
        VBScriptNumber = 0xffefefff
        HTMLDoubleQuotedString = 0xff112435
        ASPXCComment = 0xff112435
        VBScriptStart = 0xff112435
        PHPDoubleQuotedString = 0xfffff8f8
        PHPComment = 0xfffff8f8
        ASPPythonTripleSingleQuotedString = 0xffcfefcf
        ASPPythonDoubleQuotedString = 0xffcfefcf
        JavaScriptKeyword = 0xfff0f0ff
        JavaScriptSymbol = 0xfff0f0ff
        VBScriptIdentifier = 0xffefefff
        HTMLComment = 0xff112435
        UnknownTag = 0xff112435
        JavaScriptCommentLine = 0xfff0f0ff
        PythonComment = 0xffefffef
    
    class YAML:
        TextBlockMarker = 0xff112435
        DocumentDelimiter = 0xfff3c969
        Operator = 0xff112435
        Number = 0xff112435
        Default = 0xff112435
        Identifier = 0xff112435
        Reference = 0xff112435
        Comment = 0xff112435
        Keyword = 0xff112435
        SyntaxErrorMarker = 0xffff0000
    




