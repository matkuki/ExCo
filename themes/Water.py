
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
        Default = (0xffffffff, None)
        Comment = (0xff6cab9d, None)
        Keyword = (0xff2389da, None)
        String = (0xffc4bbb8, None)
        Procedure = (0xff5abcd8, None)
        Number = (0xff74ccf4, None)
        Type = (0xff2389da, None)
        Package = (0xfff5b0cb, None)
    
    class Nim:
        Default = (0xffffffff, None)
        Comment = (0xff6cab9d, None)
        BasicKeyword = (0xff2389da, True)
        TopKeyword = (0xff407fc0, True)
        String = (0xffc4bbb8, None)
        LongString = (0xfff5b0cb, None)
        Number = (0xff74ccf4, None)
        Operator = (0xff7f7f7f, None)
        Unsafe = (0xffc00000, True)
        Type = (0xff6e6e00, True)
        DocumentationComment = (0xffc75146, None)
        Definition = (0xff74ccf4, None)
        Class = (0xff5abcd8, None)
        KeywordOperator = (0xff963cc8, None)
        CharLiteral = (0xff00c8ff, None)
        CaseOf = (0xff8000ff, None)
        UserKeyword = (0xffff8040, None)
        MultilineComment = (0xffad2e24, None)
        MultilineDocumentation = (0xffea8c55, None)
        Pragma = (0xffc07f40, None)
    
    class Oberon:
        Default = (0xffffffff, None)
        Comment = (0xff6cab9d, None)
        Keyword = (0xff2389da, None)
        String = (0xffc4bbb8, None)
        Procedure = (0xff5abcd8, None)
        Module = (0xfff5b0cb, None)
        Number = (0xff74ccf4, None)
        Type = (0xff2389da, None)
    
    
    class AVS:
        BlockComment = (0xff6cab9d, None)
        ClipProperty = (0xff2389da, None)
        Default = (0xffffffff, None)
        Filter = (0xff2389da, None)
        Function = (0xff74ccf4, None)
        Identifier = (0xffffffff, None)
        Keyword = (0xff2389da, None)
        KeywordSet6 = (0xff8000ff, None)
        LineComment = (0xff6cab9d, None)
        NestedBlockComment = (0xff6cab9d, None)
        Number = (0xff74ccf4, None)
        Operator = (0xffffffff, None)
        Plugin = (0xff0080c0, None)
        String = (0xffc4bbb8, None)
        TripleString = (0xffc4bbb8, None)
    
    class Bash:
        Backticks = (0xffffff00, None)
        Comment = (0xff6cab9d, None)
        Default = (0xff808080, None)
        DoubleQuotedString = (0xffc4bbb8, None)
        Error = (0xffffff00, None)
        HereDocumentDelimiter = (0xffffffff, None)
        Identifier = (0xffffffff, None)
        Keyword = (0xff2389da, None)
        Number = (0xff74ccf4, None)
        Operator = (0xffffffff, None)
        ParameterExpansion = (0xffffffff, None)
        Scalar = (0xffffffff, None)
        SingleQuotedHereDocument = (0xffc4bbb8, None)
        SingleQuotedString = (0xffc4bbb8, None)
    
    class Batch:
        Comment = (0xff6cab9d, None)
        Default = (0xffffffff, None)
        ExternalCommand = (0xff2389da, None)
        HideCommandChar = (0xff7f7f00, None)
        Keyword = (0xff2389da, None)
        Label = (0xffc4bbb8, None)
        Operator = (0xffffffff, None)
        Variable = (0xff800080, None)
    
    class CMake:
        BlockForeach = (0xff2389da, None)
        BlockIf = (0xff2389da, None)
        BlockMacro = (0xff2389da, None)
        BlockWhile = (0xff2389da, None)
        Comment = (0xff6cab9d, None)
        Default = (0xffffffff, None)
        Function = (0xff2389da, None)
        KeywordSet3 = (0xffffffff, None)
        Label = (0xffcc3300, None)
        Number = (0xff74ccf4, None)
        String = (0xffc4bbb8, None)
        StringLeftQuote = (0xffc4bbb8, None)
        StringRightQuote = (0xffc4bbb8, None)
        StringVariable = (0xffcc3300, None)
        Variable = (0xffedff86, None)
    
    class CPP:
        Comment = (0xff6cab9d, None)
        CommentDoc = (0xff3f703f, None)
        CommentDocKeyword = (0xff3060a0, None)
        CommentDocKeywordError = (0xff804020, None)
        CommentLine = (0xff6cab9d, None)
        CommentLineDoc = (0xff3f703f, None)
        Default = (0xff808080, None)
        DoubleQuotedString = (0xffc4bbb8, None)
        GlobalClass = (0xffffffff, None)
        HashQuotedString = (0xff6cab9d, None)
        Identifier = (0xffffffff, None)
        InactiveComment = (0xff90b090, None)
        InactiveCommentDoc = (0xffd0d0d0, None)
        InactiveCommentDocKeyword = (0xffc0c0c0, None)
        InactiveCommentDocKeywordError = (0xffc0c0c0, None)
        InactiveCommentLine = (0xff90b090, None)
        InactiveCommentLineDoc = (0xffc0c0c0, None)
        InactiveDefault = (0xffc0c0c0, None)
        InactiveDoubleQuotedString = (0xffb090b0, None)
        InactiveGlobalClass = (0xffb0b0b0, None)
        InactiveHashQuotedString = (0xffffffff, None)
        InactiveIdentifier = (0xffb0b0b0, None)
        InactiveKeyword = (0xff9090b0, None)
        InactiveKeywordSet2 = (0xffc0c0c0, None)
        InactiveNumber = (0xff90b090, None)
        InactiveOperator = (0xffb0b0b0, None)
        InactivePreProcessor = (0xffb0b090, None)
        InactivePreProcessorComment = (0xffffffff, None)
        InactivePreProcessorCommentLineDoc = (0xffc0c0c0, None)
        InactiveRawString = (0xffffffff, None)
        InactiveRegex = (0xff7faf7f, None)
        InactiveSingleQuotedString = (0xffb090b0, None)
        InactiveTripleQuotedVerbatimString = (0xffffffff, None)
        InactiveUUID = (0xffc0c0c0, None)
        InactiveUnclosedString = (0xffffffff, None)
        InactiveVerbatimString = (0xff90b090, None)
        Keyword = (0xff2389da, None)
        KeywordSet2 = (0xffffffff, None)
        Number = (0xff74ccf4, None)
        Operator = (0xffffffff, None)
        PreProcessor = (0xff7f7f00, None)
        PreProcessorComment = (0xff659900, None)
        PreProcessorCommentLineDoc = (0xff3f703f, None)
        RawString = (0xffc4bbb8, None)
        Regex = (0xff3f7f3f, None)
        SingleQuotedString = (0xffc4bbb8, None)
        TripleQuotedVerbatimString = (0xff6cab9d, None)
        UUID = (0xffffffff, None)
        UnclosedString = (0xffffffff, None)
        VerbatimString = (0xff6cab9d, None)
    
    class CSS:
        AtRule = (0xff7f7f00, None)
        Attribute = (0xffedff86, None)
        CSS1Property = (0xff0040e0, None)
        CSS2Property = (0xff00a0e0, None)
        CSS3Property = (0xffffffff, None)
        ClassSelector = (0xffffffff, None)
        Comment = (0xff6cab9d, None)
        Default = (0xffff0080, None)
        DoubleQuotedString = (0xffc4bbb8, None)
        ExtendedCSSProperty = (0xffffffff, None)
        ExtendedPseudoClass = (0xffffffff, None)
        ExtendedPseudoElement = (0xffffffff, None)
        IDSelector = (0xff74ccf4, None)
        Important = (0xffff8000, None)
        MediaRule = (0xff7f7f00, None)
        Operator = (0xffffffff, None)
        PseudoClass = (0xffedff86, None)
        PseudoElement = (0xffffffff, None)
        SingleQuotedString = (0xffc4bbb8, None)
        Tag = (0xff2389da, None)
        UnknownProperty = (0xffff0000, None)
        UnknownPseudoClass = (0xffff0000, None)
        Value = (0xffc4bbb8, None)
        Variable = (0xffffffff, None)
    
    class CSharp:
        Comment = (0xff6cab9d, None)
        CommentDoc = (0xff3f703f, None)
        CommentDocKeyword = (0xff3060a0, None)
        CommentDocKeywordError = (0xff804020, None)
        CommentLine = (0xff6cab9d, None)
        CommentLineDoc = (0xff3f703f, None)
        Default = (0xff808080, None)
        DoubleQuotedString = (0xffc4bbb8, None)
        GlobalClass = (0xffffffff, None)
        HashQuotedString = (0xff6cab9d, None)
        Identifier = (0xffffffff, None)
        InactiveComment = (0xff90b090, None)
        InactiveCommentDoc = (0xffd0d0d0, None)
        InactiveCommentDocKeyword = (0xffc0c0c0, None)
        InactiveCommentDocKeywordError = (0xffc0c0c0, None)
        InactiveCommentLine = (0xff90b090, None)
        InactiveCommentLineDoc = (0xffc0c0c0, None)
        InactiveDefault = (0xffc0c0c0, None)
        InactiveDoubleQuotedString = (0xffb090b0, None)
        InactiveGlobalClass = (0xffb0b0b0, None)
        InactiveHashQuotedString = (0xffffffff, None)
        InactiveIdentifier = (0xffb0b0b0, None)
        InactiveKeyword = (0xff9090b0, None)
        InactiveKeywordSet2 = (0xffc0c0c0, None)
        InactiveNumber = (0xff90b090, None)
        InactiveOperator = (0xffb0b0b0, None)
        InactivePreProcessor = (0xffb0b090, None)
        InactivePreProcessorComment = (0xffffffff, None)
        InactivePreProcessorCommentLineDoc = (0xffc0c0c0, None)
        InactiveRawString = (0xffffffff, None)
        InactiveRegex = (0xff7faf7f, None)
        InactiveSingleQuotedString = (0xffb090b0, None)
        InactiveTripleQuotedVerbatimString = (0xffffffff, None)
        InactiveUUID = (0xffc0c0c0, None)
        InactiveUnclosedString = (0xffffffff, None)
        InactiveVerbatimString = (0xff90b090, None)
        Keyword = (0xff2389da, None)
        KeywordSet2 = (0xffffffff, None)
        Number = (0xff74ccf4, None)
        Operator = (0xffffffff, None)
        PreProcessor = (0xff7f7f00, None)
        PreProcessorComment = (0xff659900, None)
        PreProcessorCommentLineDoc = (0xff3f703f, None)
        RawString = (0xffc4bbb8, None)
        Regex = (0xff3f7f3f, None)
        SingleQuotedString = (0xffc4bbb8, None)
        TripleQuotedVerbatimString = (0xff6cab9d, None)
        UUID = (0xffffffff, None)
        UnclosedString = (0xffffffff, None)
        VerbatimString = (0xff6cab9d, None)
    
    class CoffeeScript:
        BlockRegex = (0xff3f7f3f, None)
        BlockRegexComment = (0xff6cab9d, None)
        Comment = (0xff6cab9d, None)
        CommentBlock = (0xff6cab9d, None)
        CommentDoc = (0xff3f703f, None)
        CommentDocKeyword = (0xff3060a0, None)
        CommentDocKeywordError = (0xff804020, None)
        CommentLine = (0xff6cab9d, None)
        CommentLineDoc = (0xff3f703f, None)
        Default = (0xff808080, None)
        DoubleQuotedString = (0xffc4bbb8, None)
        GlobalClass = (0xffffffff, None)
        Identifier = (0xffffffff, None)
        Keyword = (0xff2389da, None)
        KeywordSet2 = (0xffffffff, None)
        Number = (0xff74ccf4, None)
        Operator = (0xffffffff, None)
        PreProcessor = (0xff7f7f00, None)
        Regex = (0xff3f7f3f, None)
        SingleQuotedString = (0xffc4bbb8, None)
        UUID = (0xffffffff, None)
        UnclosedString = (0xffffffff, None)
        VerbatimString = (0xff6cab9d, None)
    
    class D:
        BackquoteString = (0xffffffff, None)
        Character = (0xffc4bbb8, None)
        Comment = (0xff6cab9d, None)
        CommentDoc = (0xff3f703f, None)
        CommentDocKeyword = (0xff3060a0, None)
        CommentDocKeywordError = (0xff804020, None)
        CommentLine = (0xff6cab9d, None)
        CommentLineDoc = (0xff3f703f, None)
        CommentNested = (0xffa0c0a0, None)
        Default = (0xff808080, None)
        Identifier = (0xffffffff, None)
        Keyword = (0xff2389da, None)
        KeywordDoc = (0xff2389da, None)
        KeywordSecondary = (0xff2389da, None)
        KeywordSet5 = (0xffffffff, None)
        KeywordSet6 = (0xffffffff, None)
        KeywordSet7 = (0xffffffff, None)
        Number = (0xff74ccf4, None)
        Operator = (0xffffffff, None)
        RawString = (0xffffffff, None)
        String = (0xffc4bbb8, None)
        Typedefs = (0xff2389da, None)
        UnclosedString = (0xffffffff, None)
    
    class Diff:
        Command = (0xff7f7f00, None)
        Comment = (0xff6cab9d, None)
        Default = (0xffffffff, None)
        Header = (0xfff5b0cb, None)
        LineAdded = (0xff2389da, None)
        LineChanged = (0xff7f7f7f, None)
        LineRemoved = (0xff74ccf4, None)
        Position = (0xffc4bbb8, None)
    
    class Fortran:
        Comment = (0xff6cab9d, None)
        Continuation = (0xffffffff, None)
        Default = (0xff808080, None)
        DottedOperator = (0xffffffff, None)
        DoubleQuotedString = (0xffc4bbb8, None)
        ExtendedFunction = (0xffb04080, None)
        Identifier = (0xffffffff, None)
        IntrinsicFunction = (0xffb00040, None)
        Keyword = (0xff2389da, None)
        Label = (0xffe0c0e0, None)
        Number = (0xff74ccf4, None)
        Operator = (0xffffffff, None)
        PreProcessor = (0xff7f7f00, None)
        SingleQuotedString = (0xffc4bbb8, None)
        UnclosedString = (0xffffffff, None)
    
    class Fortran77:
        Comment = (0xff6cab9d, None)
        Continuation = (0xffffffff, None)
        Default = (0xff808080, None)
        DottedOperator = (0xffffffff, None)
        DoubleQuotedString = (0xffc4bbb8, None)
        ExtendedFunction = (0xffb04080, None)
        Identifier = (0xffffffff, None)
        IntrinsicFunction = (0xffb00040, None)
        Keyword = (0xff2389da, None)
        Label = (0xffe0c0e0, None)
        Number = (0xff74ccf4, None)
        Operator = (0xffffffff, None)
        PreProcessor = (0xff7f7f00, None)
        SingleQuotedString = (0xffc4bbb8, None)
        UnclosedString = (0xffffffff, None)
    
    class HTML:
        ASPAtStart = (0xffffffff, None)
        ASPJavaScriptComment = (0xff6cab9d, None)
        ASPJavaScriptCommentDoc = (0xff7f7f7f, None)
        ASPJavaScriptCommentLine = (0xff6cab9d, None)
        ASPJavaScriptDefault = (0xffffffff, None)
        ASPJavaScriptDoubleQuotedString = (0xffc4bbb8, None)
        ASPJavaScriptKeyword = (0xff2389da, None)
        ASPJavaScriptNumber = (0xff74ccf4, None)
        ASPJavaScriptRegex = (0xffffffff, None)
        ASPJavaScriptSingleQuotedString = (0xffc4bbb8, None)
        ASPJavaScriptStart = (0xff7f7f00, None)
        ASPJavaScriptSymbol = (0xffffffff, None)
        ASPJavaScriptUnclosedString = (0xffffffff, None)
        ASPJavaScriptWord = (0xffffffff, None)
        ASPPythonClassName = (0xff5abcd8, None)
        ASPPythonComment = (0xff6cab9d, None)
        ASPPythonDefault = (0xff808080, None)
        ASPPythonDoubleQuotedString = (0xffc4bbb8, None)
        ASPPythonFunctionMethodName = (0xff74ccf4, None)
        ASPPythonIdentifier = (0xffffffff, None)
        ASPPythonKeyword = (0xff2389da, None)
        ASPPythonNumber = (0xff74ccf4, None)
        ASPPythonOperator = (0xffffffff, None)
        ASPPythonSingleQuotedString = (0xffc4bbb8, None)
        ASPPythonStart = (0xff808080, None)
        ASPPythonTripleDoubleQuotedString = (0xfff5b0cb, None)
        ASPPythonTripleSingleQuotedString = (0xfff5b0cb, None)
        ASPStart = (0xffffffff, None)
        ASPVBScriptComment = (0xff008000, None)
        ASPVBScriptDefault = (0xffffffff, None)
        ASPVBScriptIdentifier = (0xff1f76e4, None)
        ASPVBScriptKeyword = (0xff1f76e4, None)
        ASPVBScriptNumber = (0xff008080, None)
        ASPVBScriptStart = (0xffffffff, None)
        ASPVBScriptString = (0xff800080, None)
        ASPVBScriptUnclosedString = (0xff1f76e4, None)
        ASPXCComment = (0xffffffff, None)
        Attribute = (0xff008080, None)
        CDATA = (0xffffffff, None)
        Default = (0xffffffff, None)
        Entity = (0xff800080, None)
        HTMLComment = (0xff808000, None)
        HTMLDoubleQuotedString = (0xffc4bbb8, None)
        HTMLNumber = (0xff74ccf4, None)
        HTMLSingleQuotedString = (0xffc4bbb8, None)
        HTMLValue = (0xffff00ff, None)
        JavaScriptComment = (0xff6cab9d, None)
        JavaScriptCommentDoc = (0xff3f703f, None)
        JavaScriptCommentLine = (0xff6cab9d, None)
        JavaScriptDefault = (0xffffffff, None)
        JavaScriptDoubleQuotedString = (0xffc4bbb8, None)
        JavaScriptKeyword = (0xff2389da, None)
        JavaScriptNumber = (0xff74ccf4, None)
        JavaScriptRegex = (0xffffffff, None)
        JavaScriptSingleQuotedString = (0xffc4bbb8, None)
        JavaScriptStart = (0xff7f7f00, None)
        JavaScriptSymbol = (0xffffffff, None)
        JavaScriptUnclosedString = (0xffffffff, None)
        JavaScriptWord = (0xffffffff, None)
        OtherInTag = (0xff800080, None)
        PHPComment = (0xff999999, None)
        PHPCommentLine = (0xff666666, None)
        PHPDefault = (0xffc7dbf5, None)
        PHPDoubleQuotedString = (0xff6cab9d, None)
        PHPDoubleQuotedVariable = (0xff2389da, None)
        PHPKeyword = (0xffc4bbb8, None)
        PHPNumber = (0xffcc9900, None)
        PHPOperator = (0xffffffff, None)
        PHPSingleQuotedString = (0xff009f00, None)
        PHPStart = (0xff5abcd8, None)
        PHPVariable = (0xff2389da, None)
        PythonClassName = (0xff5abcd8, None)
        PythonComment = (0xff6cab9d, None)
        PythonDefault = (0xff808080, None)
        PythonDoubleQuotedString = (0xffc4bbb8, None)
        PythonFunctionMethodName = (0xff74ccf4, None)
        PythonIdentifier = (0xffffffff, None)
        PythonKeyword = (0xff2389da, None)
        PythonNumber = (0xff74ccf4, None)
        PythonOperator = (0xffffffff, None)
        PythonSingleQuotedString = (0xffc4bbb8, None)
        PythonStart = (0xff808080, None)
        PythonTripleDoubleQuotedString = (0xfff5b0cb, None)
        PythonTripleSingleQuotedString = (0xfff5b0cb, None)
        SGMLBlockDefault = (0xfffff5b2, None)
        SGMLCommand = (0xff1f76e4, None)
        SGMLComment = (0xff808000, None)
        SGMLDefault = (0xff1f76e4, None)
        SGMLDoubleQuotedString = (0xffedff86, None)
        SGMLEntity = (0xff333333, None)
        SGMLError = (0xffedff86, None)
        SGMLParameter = (0xff006600, None)
        SGMLParameterComment = (0xffffffff, None)
        SGMLSingleQuotedString = (0xff993300, None)
        SGMLSpecial = (0xff3366ff, None)
        Script = (0xff1f76e4, None)
        Tag = (0xff1f76e4, None)
        UnknownAttribute = (0xffff0000, None)
        UnknownTag = (0xffff0000, None)
        VBScriptComment = (0xff008000, None)
        VBScriptDefault = (0xffffffff, None)
        VBScriptIdentifier = (0xff1f76e4, None)
        VBScriptKeyword = (0xff1f76e4, None)
        VBScriptNumber = (0xff008080, None)
        VBScriptStart = (0xffffffff, None)
        VBScriptString = (0xff800080, None)
        VBScriptUnclosedString = (0xff1f76e4, None)
        XMLEnd = (0xff5abcd8, None)
        XMLStart = (0xff5abcd8, None)
        XMLTagEnd = (0xff1f76e4, None)
    
    class IDL:
        Comment = (0xff6cab9d, None)
        CommentDoc = (0xff3f703f, None)
        CommentDocKeyword = (0xff3060a0, None)
        CommentDocKeywordError = (0xff804020, None)
        CommentLine = (0xff6cab9d, None)
        CommentLineDoc = (0xff3f703f, None)
        Default = (0xff808080, None)
        DoubleQuotedString = (0xffc4bbb8, None)
        GlobalClass = (0xffffffff, None)
        HashQuotedString = (0xff6cab9d, None)
        Identifier = (0xffffffff, None)
        InactiveComment = (0xff90b090, None)
        InactiveCommentDoc = (0xffd0d0d0, None)
        InactiveCommentDocKeyword = (0xffc0c0c0, None)
        InactiveCommentDocKeywordError = (0xffc0c0c0, None)
        InactiveCommentLine = (0xff90b090, None)
        InactiveCommentLineDoc = (0xffc0c0c0, None)
        InactiveDefault = (0xffc0c0c0, None)
        InactiveDoubleQuotedString = (0xffb090b0, None)
        InactiveGlobalClass = (0xffb0b0b0, None)
        InactiveHashQuotedString = (0xffffffff, None)
        InactiveIdentifier = (0xffb0b0b0, None)
        InactiveKeyword = (0xff9090b0, None)
        InactiveKeywordSet2 = (0xffc0c0c0, None)
        InactiveNumber = (0xff90b090, None)
        InactiveOperator = (0xffb0b0b0, None)
        InactivePreProcessor = (0xffb0b090, None)
        InactivePreProcessorComment = (0xffffffff, None)
        InactivePreProcessorCommentLineDoc = (0xffc0c0c0, None)
        InactiveRawString = (0xffffffff, None)
        InactiveRegex = (0xff7faf7f, None)
        InactiveSingleQuotedString = (0xffb090b0, None)
        InactiveTripleQuotedVerbatimString = (0xffffffff, None)
        InactiveUUID = (0xffc0c0c0, None)
        InactiveUnclosedString = (0xffffffff, None)
        InactiveVerbatimString = (0xff90b090, None)
        Keyword = (0xff2389da, None)
        KeywordSet2 = (0xffffffff, None)
        Number = (0xff74ccf4, None)
        Operator = (0xffffffff, None)
        PreProcessor = (0xff7f7f00, None)
        PreProcessorComment = (0xff659900, None)
        PreProcessorCommentLineDoc = (0xff3f703f, None)
        RawString = (0xffc4bbb8, None)
        Regex = (0xff3f7f3f, None)
        SingleQuotedString = (0xffc4bbb8, None)
        TripleQuotedVerbatimString = (0xff6cab9d, None)
        UUID = (0xff804080, None)
        UnclosedString = (0xffffffff, None)
        VerbatimString = (0xff6cab9d, None)
    
    class Java:
        Comment = (0xff6cab9d, None)
        CommentDoc = (0xff3f703f, None)
        CommentDocKeyword = (0xff3060a0, None)
        CommentDocKeywordError = (0xff804020, None)
        CommentLine = (0xff6cab9d, None)
        CommentLineDoc = (0xff3f703f, None)
        Default = (0xff808080, None)
        DoubleQuotedString = (0xffc4bbb8, None)
        GlobalClass = (0xffffffff, None)
        HashQuotedString = (0xff6cab9d, None)
        Identifier = (0xffffffff, None)
        InactiveComment = (0xff90b090, None)
        InactiveCommentDoc = (0xffd0d0d0, None)
        InactiveCommentDocKeyword = (0xffc0c0c0, None)
        InactiveCommentDocKeywordError = (0xffc0c0c0, None)
        InactiveCommentLine = (0xff90b090, None)
        InactiveCommentLineDoc = (0xffc0c0c0, None)
        InactiveDefault = (0xffc0c0c0, None)
        InactiveDoubleQuotedString = (0xffb090b0, None)
        InactiveGlobalClass = (0xffb0b0b0, None)
        InactiveHashQuotedString = (0xffffffff, None)
        InactiveIdentifier = (0xffb0b0b0, None)
        InactiveKeyword = (0xff9090b0, None)
        InactiveKeywordSet2 = (0xffc0c0c0, None)
        InactiveNumber = (0xff90b090, None)
        InactiveOperator = (0xffb0b0b0, None)
        InactivePreProcessor = (0xffb0b090, None)
        InactivePreProcessorComment = (0xffffffff, None)
        InactivePreProcessorCommentLineDoc = (0xffc0c0c0, None)
        InactiveRawString = (0xffffffff, None)
        InactiveRegex = (0xff7faf7f, None)
        InactiveSingleQuotedString = (0xffb090b0, None)
        InactiveTripleQuotedVerbatimString = (0xffffffff, None)
        InactiveUUID = (0xffc0c0c0, None)
        InactiveUnclosedString = (0xffffffff, None)
        InactiveVerbatimString = (0xff90b090, None)
        Keyword = (0xff2389da, None)
        KeywordSet2 = (0xffffffff, None)
        Number = (0xff74ccf4, None)
        Operator = (0xffffffff, None)
        PreProcessor = (0xff7f7f00, None)
        PreProcessorComment = (0xff659900, None)
        PreProcessorCommentLineDoc = (0xff3f703f, None)
        RawString = (0xffc4bbb8, None)
        Regex = (0xff3f7f3f, None)
        SingleQuotedString = (0xffc4bbb8, None)
        TripleQuotedVerbatimString = (0xff6cab9d, None)
        UUID = (0xffffffff, None)
        UnclosedString = (0xffffffff, None)
        VerbatimString = (0xff6cab9d, None)
    
    class JavaScript:
        Comment = (0xff6cab9d, None)
        CommentDoc = (0xff3f703f, None)
        CommentDocKeyword = (0xff3060a0, None)
        CommentDocKeywordError = (0xff804020, None)
        CommentLine = (0xff6cab9d, None)
        CommentLineDoc = (0xff3f703f, None)
        Default = (0xff808080, None)
        DoubleQuotedString = (0xffc4bbb8, None)
        GlobalClass = (0xffffffff, None)
        HashQuotedString = (0xff6cab9d, None)
        Identifier = (0xffffffff, None)
        InactiveComment = (0xff90b090, None)
        InactiveCommentDoc = (0xffd0d0d0, None)
        InactiveCommentDocKeyword = (0xffc0c0c0, None)
        InactiveCommentDocKeywordError = (0xffc0c0c0, None)
        InactiveCommentLine = (0xff90b090, None)
        InactiveCommentLineDoc = (0xffc0c0c0, None)
        InactiveDefault = (0xffc0c0c0, None)
        InactiveDoubleQuotedString = (0xffb090b0, None)
        InactiveGlobalClass = (0xffb0b0b0, None)
        InactiveHashQuotedString = (0xffffffff, None)
        InactiveIdentifier = (0xffb0b0b0, None)
        InactiveKeyword = (0xff9090b0, None)
        InactiveKeywordSet2 = (0xffc0c0c0, None)
        InactiveNumber = (0xff90b090, None)
        InactiveOperator = (0xffb0b0b0, None)
        InactivePreProcessor = (0xffb0b090, None)
        InactivePreProcessorComment = (0xffffffff, None)
        InactivePreProcessorCommentLineDoc = (0xffc0c0c0, None)
        InactiveRawString = (0xffffffff, None)
        InactiveRegex = (0xff7faf7f, None)
        InactiveSingleQuotedString = (0xffb090b0, None)
        InactiveTripleQuotedVerbatimString = (0xffffffff, None)
        InactiveUUID = (0xffc0c0c0, None)
        InactiveUnclosedString = (0xffffffff, None)
        InactiveVerbatimString = (0xff90b090, None)
        Keyword = (0xff2389da, None)
        KeywordSet2 = (0xffffffff, None)
        Number = (0xff74ccf4, None)
        Operator = (0xffffffff, None)
        PreProcessor = (0xff7f7f00, None)
        PreProcessorComment = (0xff659900, None)
        PreProcessorCommentLineDoc = (0xff3f703f, None)
        RawString = (0xffc4bbb8, None)
        Regex = (0xff3f7f3f, None)
        SingleQuotedString = (0xffc4bbb8, None)
        TripleQuotedVerbatimString = (0xff6cab9d, None)
        UUID = (0xffffffff, None)
        UnclosedString = (0xffffffff, None)
        VerbatimString = (0xff6cab9d, None)
    
    class Lua:
        BasicFunctions = (0xff2389da, None)
        Character = (0xffc4bbb8, None)
        Comment = (0xff6cab9d, None)
        CoroutinesIOSystemFacilities = (0xff2389da, None)
        Default = (0xffffffff, None)
        Identifier = (0xffffffff, None)
        Keyword = (0xff2389da, None)
        KeywordSet5 = (0xffffffff, None)
        KeywordSet6 = (0xffffffff, None)
        KeywordSet7 = (0xffffffff, None)
        KeywordSet8 = (0xffffffff, None)
        Label = (0xff7f7f00, None)
        LineComment = (0xff6cab9d, None)
        LiteralString = (0xffc4bbb8, None)
        Number = (0xff74ccf4, None)
        Operator = (0xffffffff, None)
        Preprocessor = (0xff7f7f00, None)
        String = (0xffc4bbb8, None)
        StringTableMathsFunctions = (0xff2389da, None)
        UnclosedString = (0xffffffff, None)
    
    class Makefile:
        Comment = (0xff6cab9d, None)
        Default = (0xffffffff, None)
        Error = (0xffffff00, None)
        Operator = (0xffffffff, None)
        Preprocessor = (0xff7f7f00, None)
        Target = (0xffa00000, None)
        Variable = (0xff1f76e4, None)
    
    class Matlab:
        Command = (0xff7f7f00, None)
        Comment = (0xff6cab9d, None)
        Default = (0xffffffff, None)
        DoubleQuotedString = (0xffc4bbb8, None)
        Identifier = (0xffffffff, None)
        Keyword = (0xff2389da, None)
        Number = (0xff74ccf4, None)
        Operator = (0xffffffff, None)
        SingleQuotedString = (0xffc4bbb8, None)
    
    class Octave:
        Command = (0xff7f7f00, None)
        Comment = (0xff6cab9d, None)
        Default = (0xffffffff, None)
        DoubleQuotedString = (0xffc4bbb8, None)
        Identifier = (0xffffffff, None)
        Keyword = (0xff2389da, None)
        Number = (0xff74ccf4, None)
        Operator = (0xffffffff, None)
        SingleQuotedString = (0xffc4bbb8, None)
    
    class PO:
        Comment = (0xff6cab9d, None)
        Default = (0xffffffff, None)
        Flags = (0xffffffff, None)
        Fuzzy = (0xffffffff, None)
        MessageContext = (0xffffffff, None)
        MessageContextText = (0xffffffff, None)
        MessageContextTextEOL = (0xffffffff, None)
        MessageId = (0xffffffff, None)
        MessageIdText = (0xffffffff, None)
        MessageIdTextEOL = (0xffffffff, None)
        MessageString = (0xffffffff, None)
        MessageStringText = (0xffffffff, None)
        MessageStringTextEOL = (0xffffffff, None)
        ProgrammerComment = (0xffffffff, None)
        Reference = (0xffffffff, None)
    
    class POV:
        BadDirective = (0xff804020, None)
        Comment = (0xff6cab9d, None)
        CommentLine = (0xff6cab9d, None)
        Default = (0xffff0080, None)
        Directive = (0xff7f7f00, None)
        Identifier = (0xffffffff, None)
        KeywordSet6 = (0xff2389da, None)
        KeywordSet7 = (0xff2389da, None)
        KeywordSet8 = (0xff2389da, None)
        Number = (0xff74ccf4, None)
        ObjectsCSGAppearance = (0xff2389da, None)
        Operator = (0xffffffff, None)
        PredefinedFunctions = (0xff2389da, None)
        PredefinedIdentifiers = (0xff2389da, None)
        String = (0xffc4bbb8, None)
        TypesModifiersItems = (0xff2389da, None)
        UnclosedString = (0xffffffff, None)
    
    class Pascal:
        Asm = (0xff804080, None)
        Character = (0xffc4bbb8, None)
        Comment = (0xff6cab9d, None)
        CommentLine = (0xff6cab9d, None)
        CommentParenthesis = (0xff6cab9d, None)
        Default = (0xff808080, None)
        HexNumber = (0xff74ccf4, None)
        Identifier = (0xffffffff, None)
        Keyword = (0xff2389da, None)
        Number = (0xff74ccf4, None)
        Operator = (0xffffffff, None)
        PreProcessor = (0xff7f7f00, None)
        PreProcessorParenthesis = (0xff7f7f00, None)
        SingleQuotedString = (0xffc4bbb8, None)
        UnclosedString = (0xffffffff, None)
    
    class Perl:
        Array = (0xffffffff, None)
        BacktickHereDocument = (0xffc4bbb8, None)
        BacktickHereDocumentVar = (0xffd00000, None)
        Backticks = (0xffffff00, None)
        BackticksVar = (0xffd00000, None)
        Comment = (0xff6cab9d, None)
        DataSection = (0xff600000, None)
        Default = (0xff808080, None)
        DoubleQuotedHereDocument = (0xffc4bbb8, None)
        DoubleQuotedHereDocumentVar = (0xffd00000, None)
        DoubleQuotedString = (0xffc4bbb8, None)
        DoubleQuotedStringVar = (0xffd00000, None)
        Error = (0xffffff00, None)
        FormatBody = (0xffc000c0, None)
        FormatIdentifier = (0xffc000c0, None)
        Hash = (0xffffffff, None)
        HereDocumentDelimiter = (0xffffffff, None)
        Identifier = (0xffffffff, None)
        Keyword = (0xff2389da, None)
        Number = (0xff74ccf4, None)
        Operator = (0xffffffff, None)
        POD = (0xff004000, None)
        PODVerbatim = (0xff004000, None)
        QuotedStringQ = (0xffc4bbb8, None)
        QuotedStringQQ = (0xffc4bbb8, None)
        QuotedStringQQVar = (0xffd00000, None)
        QuotedStringQR = (0xffffffff, None)
        QuotedStringQRVar = (0xffd00000, None)
        QuotedStringQW = (0xffffffff, None)
        QuotedStringQX = (0xffffff00, None)
        QuotedStringQXVar = (0xffd00000, None)
        Regex = (0xffffffff, None)
        RegexVar = (0xffd00000, None)
        Scalar = (0xffffffff, None)
        SingleQuotedHereDocument = (0xffc4bbb8, None)
        SingleQuotedString = (0xffc4bbb8, None)
        SubroutinePrototype = (0xffffffff, None)
        Substitution = (0xffffffff, None)
        SubstitutionVar = (0xffd00000, None)
        SymbolTable = (0xffffffff, None)
        Translation = (0xffffffff, None)
    
    class PostScript:
        ArrayParenthesis = (0xff2389da, None)
        BadStringCharacter = (0xffffff00, None)
        Base85String = (0xffc4bbb8, None)
        Comment = (0xff6cab9d, None)
        DSCComment = (0xff3f703f, None)
        DSCCommentValue = (0xff3060a0, None)
        Default = (0xffffffff, None)
        DictionaryParenthesis = (0xff3060a0, None)
        HexString = (0xff3f7f3f, None)
        ImmediateEvalLiteral = (0xff7f7f00, None)
        Keyword = (0xff2389da, None)
        Literal = (0xff7f7f00, None)
        Name = (0xffffffff, None)
        Number = (0xff74ccf4, None)
        ProcedureParenthesis = (0xffffffff, None)
        Text = (0xffc4bbb8, None)
    
    class Properties:
        Assignment = (0xffb06000, None)
        Comment = (0xff74ccf4, None)
        Default = (0xffffffff, None)
        DefaultValue = (0xff7f7f00, None)
        Key = (0xffffffff, None)
        Section = (0xffc4bbb8, None)
    
    class Python:
        ClassName = (0xff5abcd8, None)
        Comment = (0xff6cab9d, None)
        CommentBlock = (0xff7f7f7f, None)
        Decorator = (0xff805000, None)
        Default = (0xffffffff, None)
        DoubleQuotedString = (0xffc4bbb8, None)
        FunctionMethodName = (0xff74ccf4, None)
        HighlightedIdentifier = (0xff407090, None)
        Identifier = (0xffffffff, None)
        Inconsistent = (0xff6cab9d, None)
        Keyword = (0xff2389da, None)
        NoWarning = (0xff808080, None)
        Number = (0xff74ccf4, None)
        Operator = (0xffffffff, None)
        SingleQuotedString = (0xffc4bbb8, None)
        Spaces = (0xffc4bbb8, None)
        Tabs = (0xffc4bbb8, None)
        TabsAfterSpaces = (0xff74ccf4, None)
        TripleDoubleQuotedString = (0xfff5b0cb, None)
        TripleSingleQuotedString = (0xfff5b0cb, None)
        UnclosedString = (0xffffffff, None)
    
    class Ruby:
        Backticks = (0xffffff00, None)
        ClassName = (0xff5abcd8, None)
        ClassVariable = (0xff8000b0, None)
        Comment = (0xff6cab9d, None)
        DataSection = (0xff600000, None)
        Default = (0xff808080, None)
        DemotedKeyword = (0xff2389da, None)
        DoubleQuotedString = (0xffc4bbb8, None)
        Error = (0xffffffff, None)
        FunctionMethodName = (0xff74ccf4, None)
        Global = (0xff800080, None)
        HereDocument = (0xffc4bbb8, None)
        HereDocumentDelimiter = (0xffffffff, None)
        Identifier = (0xffffffff, None)
        InstanceVariable = (0xffb00080, None)
        Keyword = (0xff2389da, None)
        ModuleName = (0xffa000a0, None)
        Number = (0xff74ccf4, None)
        Operator = (0xffffffff, None)
        POD = (0xff004000, None)
        PercentStringQ = (0xffc4bbb8, None)
        PercentStringq = (0xffc4bbb8, None)
        PercentStringr = (0xffffffff, None)
        PercentStringw = (0xffffffff, None)
        PercentStringx = (0xffffff00, None)
        Regex = (0xffffffff, None)
        SingleQuotedString = (0xffc4bbb8, None)
        Stderr = (0xffffffff, None)
        Stdin = (0xffffffff, None)
        Stdout = (0xffffffff, None)
        Symbol = (0xffc0a030, None)
    
    class SQL:
        Comment = (0xff6cab9d, None)
        CommentDoc = (0xff7f7f7f, None)
        CommentDocKeyword = (0xff3060a0, None)
        CommentDocKeywordError = (0xff804020, None)
        CommentLine = (0xff6cab9d, None)
        CommentLineHash = (0xff6cab9d, None)
        Default = (0xff808080, None)
        DoubleQuotedString = (0xffc4bbb8, None)
        Identifier = (0xffffffff, None)
        Keyword = (0xff2389da, None)
        KeywordSet5 = (0xff4b0082, None)
        KeywordSet6 = (0xffb00040, None)
        KeywordSet7 = (0xff8b0000, None)
        KeywordSet8 = (0xff800080, None)
        Number = (0xff74ccf4, None)
        Operator = (0xffffffff, None)
        PlusComment = (0xff6cab9d, None)
        PlusKeyword = (0xff7f7f00, None)
        PlusPrompt = (0xff6cab9d, None)
        QuotedIdentifier = (0xffffffff, None)
        SingleQuotedString = (0xffc4bbb8, None)
    
    class Spice:
        Command = (0xff2389da, None)
        Comment = (0xff6cab9d, None)
        Default = (0xff808080, None)
        Delimiter = (0xffffffff, None)
        Function = (0xff2389da, None)
        Identifier = (0xffffffff, None)
        Number = (0xff74ccf4, None)
        Parameter = (0xff0040e0, None)
        Value = (0xffc4bbb8, None)
    
    class TCL:
        Comment = (0xff6cab9d, None)
        CommentBlock = (0xffffffff, None)
        CommentBox = (0xff6cab9d, None)
        CommentLine = (0xff6cab9d, None)
        Default = (0xff808080, None)
        ExpandKeyword = (0xff2389da, None)
        ITCLKeyword = (0xff2389da, None)
        Identifier = (0xff2389da, None)
        KeywordSet6 = (0xff2389da, None)
        KeywordSet7 = (0xff2389da, None)
        KeywordSet8 = (0xff2389da, None)
        KeywordSet9 = (0xff2389da, None)
        Modifier = (0xffc4bbb8, None)
        Number = (0xff74ccf4, None)
        Operator = (0xffffffff, None)
        QuotedKeyword = (0xffc4bbb8, None)
        QuotedString = (0xffc4bbb8, None)
        Substitution = (0xff7f7f00, None)
        SubstitutionBrace = (0xff7f7f00, None)
        TCLKeyword = (0xff2389da, None)
        TkCommand = (0xff2389da, None)
        TkKeyword = (0xff2389da, None)
    
    class TeX:
        Command = (0xff6cab9d, None)
        Default = (0xff3f3f3f, None)
        Group = (0xfff5b0cb, None)
        Special = (0xff74ccf4, None)
        Symbol = (0xff7f7f00, None)
        Text = (0xffffffff, None)
    
    class VHDL:
        Attribute = (0xff804020, None)
        Comment = (0xff6cab9d, None)
        CommentLine = (0xff3f7f3f, None)
        Default = (0xff800080, None)
        Identifier = (0xffffffff, None)
        Keyword = (0xff2389da, None)
        KeywordSet7 = (0xff804020, None)
        Number = (0xff74ccf4, None)
        Operator = (0xffffffff, None)
        StandardFunction = (0xff808020, None)
        StandardOperator = (0xff74ccf4, None)
        StandardPackage = (0xff208020, None)
        StandardType = (0xff208080, None)
        String = (0xffc4bbb8, None)
        UnclosedString = (0xffffffff, None)
    
    class Verilog:
        Comment = (0xff6cab9d, None)
        CommentBang = (0xff3f7f3f, None)
        CommentLine = (0xff6cab9d, None)
        Default = (0xff808080, None)
        Identifier = (0xffffffff, None)
        Keyword = (0xff2389da, None)
        KeywordSet2 = (0xff74ccf4, None)
        Number = (0xff74ccf4, None)
        Operator = (0xff007070, None)
        Preprocessor = (0xff7f7f00, None)
        String = (0xffc4bbb8, None)
        SystemTask = (0xff804020, None)
        UnclosedString = (0xffffffff, None)
        UserKeywordSet = (0xff2a00ff, None)
    
    class XML:
        ASPAtStart = (0xffffffff, None)
        ASPJavaScriptComment = (0xff6cab9d, None)
        ASPJavaScriptCommentDoc = (0xff7f7f7f, None)
        ASPJavaScriptCommentLine = (0xff6cab9d, None)
        ASPJavaScriptDefault = (0xffffffff, None)
        ASPJavaScriptDoubleQuotedString = (0xffc4bbb8, None)
        ASPJavaScriptKeyword = (0xff2389da, None)
        ASPJavaScriptNumber = (0xff74ccf4, None)
        ASPJavaScriptRegex = (0xffffffff, None)
        ASPJavaScriptSingleQuotedString = (0xffc4bbb8, None)
        ASPJavaScriptStart = (0xff7f7f00, None)
        ASPJavaScriptSymbol = (0xffffffff, None)
        ASPJavaScriptUnclosedString = (0xffffffff, None)
        ASPJavaScriptWord = (0xffffffff, None)
        ASPPythonClassName = (0xff5abcd8, None)
        ASPPythonComment = (0xff6cab9d, None)
        ASPPythonDefault = (0xff808080, None)
        ASPPythonDoubleQuotedString = (0xffc4bbb8, None)
        ASPPythonFunctionMethodName = (0xff74ccf4, None)
        ASPPythonIdentifier = (0xffffffff, None)
        ASPPythonKeyword = (0xff2389da, None)
        ASPPythonNumber = (0xff74ccf4, None)
        ASPPythonOperator = (0xffffffff, None)
        ASPPythonSingleQuotedString = (0xffc4bbb8, None)
        ASPPythonStart = (0xff808080, None)
        ASPPythonTripleDoubleQuotedString = (0xfff5b0cb, None)
        ASPPythonTripleSingleQuotedString = (0xfff5b0cb, None)
        ASPStart = (0xffffffff, None)
        ASPVBScriptComment = (0xff008000, None)
        ASPVBScriptDefault = (0xffffffff, None)
        ASPVBScriptIdentifier = (0xff1f76e4, None)
        ASPVBScriptKeyword = (0xff1f76e4, None)
        ASPVBScriptNumber = (0xff008080, None)
        ASPVBScriptStart = (0xffffffff, None)
        ASPVBScriptString = (0xff800080, None)
        ASPVBScriptUnclosedString = (0xff1f76e4, None)
        ASPXCComment = (0xffffffff, None)
        Attribute = (0xff008080, None)
        CDATA = (0xffedff86, None)
        Default = (0xffffffff, None)
        Entity = (0xff800080, None)
        HTMLComment = (0xff808000, None)
        HTMLDoubleQuotedString = (0xffc4bbb8, None)
        HTMLNumber = (0xff74ccf4, None)
        HTMLSingleQuotedString = (0xffc4bbb8, None)
        HTMLValue = (0xff608060, None)
        JavaScriptComment = (0xff6cab9d, None)
        JavaScriptCommentDoc = (0xff3f703f, None)
        JavaScriptCommentLine = (0xff6cab9d, None)
        JavaScriptDefault = (0xffffffff, None)
        JavaScriptDoubleQuotedString = (0xffc4bbb8, None)
        JavaScriptKeyword = (0xff2389da, None)
        JavaScriptNumber = (0xff74ccf4, None)
        JavaScriptRegex = (0xffffffff, None)
        JavaScriptSingleQuotedString = (0xffc4bbb8, None)
        JavaScriptStart = (0xff7f7f00, None)
        JavaScriptSymbol = (0xffffffff, None)
        JavaScriptUnclosedString = (0xffffffff, None)
        JavaScriptWord = (0xffffffff, None)
        OtherInTag = (0xff800080, None)
        PHPComment = (0xff999999, None)
        PHPCommentLine = (0xff666666, None)
        PHPDefault = (0xffc7dbf5, None)
        PHPDoubleQuotedString = (0xff6cab9d, None)
        PHPDoubleQuotedVariable = (0xff2389da, None)
        PHPKeyword = (0xffc4bbb8, None)
        PHPNumber = (0xffcc9900, None)
        PHPOperator = (0xffffffff, None)
        PHPSingleQuotedString = (0xff009f00, None)
        PHPStart = (0xffedff86, None)
        PHPVariable = (0xff2389da, None)
        PythonClassName = (0xff5abcd8, None)
        PythonComment = (0xff6cab9d, None)
        PythonDefault = (0xff808080, None)
        PythonDoubleQuotedString = (0xffc4bbb8, None)
        PythonFunctionMethodName = (0xff74ccf4, None)
        PythonIdentifier = (0xffffffff, None)
        PythonKeyword = (0xff2389da, None)
        PythonNumber = (0xff74ccf4, None)
        PythonOperator = (0xffffffff, None)
        PythonSingleQuotedString = (0xffc4bbb8, None)
        PythonStart = (0xff808080, None)
        PythonTripleDoubleQuotedString = (0xfff5b0cb, None)
        PythonTripleSingleQuotedString = (0xfff5b0cb, None)
        SGMLBlockDefault = (0xfffff5b2, None)
        SGMLCommand = (0xff1f76e4, None)
        SGMLComment = (0xff808000, None)
        SGMLDefault = (0xff1f76e4, None)
        SGMLDoubleQuotedString = (0xffedff86, None)
        SGMLEntity = (0xff333333, None)
        SGMLError = (0xffedff86, None)
        SGMLParameter = (0xff006600, None)
        SGMLParameterComment = (0xffffffff, None)
        SGMLSingleQuotedString = (0xff993300, None)
        SGMLSpecial = (0xff3366ff, None)
        Script = (0xff1f76e4, None)
        Tag = (0xff1f76e4, None)
        UnknownAttribute = (0xff008080, None)
        UnknownTag = (0xff1f76e4, None)
        VBScriptComment = (0xff008000, None)
        VBScriptDefault = (0xffffffff, None)
        VBScriptIdentifier = (0xff1f76e4, None)
        VBScriptKeyword = (0xff1f76e4, None)
        VBScriptNumber = (0xff008080, None)
        VBScriptStart = (0xffffffff, None)
        VBScriptString = (0xff800080, None)
        VBScriptUnclosedString = (0xff1f76e4, None)
        XMLEnd = (0xff800080, None)
        XMLStart = (0xff800080, None)
        XMLTagEnd = (0xff1f76e4, None)
    
    class YAML:
        Comment = (0xff008800, None)
        Default = (0xffffffff, None)
        DocumentDelimiter = (0xff112435, None)
        Identifier = (0xfff3c969, None)
        Keyword = (0xff880088, None)
        Number = (0xff880000, None)
        Operator = (0xffffffff, None)
        Reference = (0xff008888, None)
        SyntaxErrorMarker = (0xff112435, None)
        TextBlockMarker = (0xff333366, None)


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
    




