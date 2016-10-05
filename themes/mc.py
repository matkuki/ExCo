
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
##      'Midnight Commander' theme made for Seba

import PyQt4.QtGui


Form = "#295a88"
Cursor = PyQt4.QtGui.QColor(0xffeeeeec)


class FoldMargin:
    ForeGround = PyQt4.QtGui.QColor(0xff4096bf)
    BackGround = PyQt4.QtGui.QColor(0xff3476a3)


class LineMargin:
    ForeGround = PyQt4.QtGui.QColor(0xffeeeeec)
    BackGround = PyQt4.QtGui.QColor(0xff3465a4)


class Indication:
    Font = "#e6e6e6"
    ActiveBackGround = "#112435"
    ActiveBorder = "#e6e6e6"
    PassiveBackGround = "#295a88"
    PassiveBorder = "#33aaff"

    
class Font:
    Default = PyQt4.QtGui.QColor(0xffeeeeec)
    
    class Ada:
        Default = (0xffeeeeec, None)
        Comment = (0xff6cab9d, None)
        Keyword = (0xffa3c2da, None)
        String = (0xffc4bbb8, None)
        Procedure = (0xff5abcd8, None)
        Number = (0xff74ccf4, None)
        Type = (0xffa3c2da, None)
        Package = (0xfff5b0cb, None)
    
    class Nim:
        Default = (0xffeeeeec, None)
        Comment = (0xff6cab9d, None)
        BasicKeyword = (0xffa3c2da, True)
        TopKeyword = (0xffabb5c0, True)
        String = (0xffc4bbb8, None)
        LongString = (0xfff5b0cb, None)
        Number = (0xff74ccf4, None)
        Operator = (0xff7f7f7f, None)
        Unsafe = (0xffc00000, True)
        Type = (0xffe8e800, True)
        DocumentationComment = (0xffc75146, None)
        Definition = (0xff74ccf4, None)
        Class = (0xff5abcd8, None)
        KeywordOperator = (0xffd891ff, None)
        CharLiteral = (0xff00c8ff, None)
        CaseOf = (0xffd5abff, None)
        UserKeyword = (0xffff8040, None)
        MultilineComment = (0xffad2e24, None)
        MultilineDocumentation = (0xffea8c55, None)
        Pragma = (0xffc07f40, None)
    
    class Oberon:
        Default = (0xffeeeeec, None)
        Comment = (0xff6cab9d, None)
        Keyword = (0xffa3c2da, None)
        String = (0xffc4bbb8, None)
        Procedure = (0xff5abcd8, None)
        Module = (0xfff5b0cb, None)
        Number = (0xff74ccf4, None)
        Type = (0xffa3c2da, None)
    
    
    class AVS:
        BlockComment = (0xff6cab9d, None)
        ClipProperty = (0xffa3c2da, None)
        Default = (0xffeeeeec, None)
        Filter = (0xffa3c2da, None)
        Function = (0xff74ccf4, None)
        Identifier = (0xffeeeeec, None)
        Keyword = (0xffa3c2da, None)
        KeywordSet6 = (0xffd5abff, None)
        LineComment = (0xff6cab9d, None)
        NestedBlockComment = (0xff6cab9d, None)
        Number = (0xff74ccf4, None)
        Operator = (0xffeeeeec, None)
        Plugin = (0xff0080c0, None)
        String = (0xffc4bbb8, None)
        TripleString = (0xffc4bbb8, None)
    
    class Bash:
        Backticks = (0xff8ae234, True)
        Comment = (0xff6cab9d, None)
        Default = (0xff808080, None)
        DoubleQuotedString = (0xffc48e7b, None)
        Error = (0xffaa0000, True)
        HereDocumentDelimiter = (0xffeeeeec, None)
        Identifier = (0xffeeeeec, None)
        Keyword = (0xffa3c2da, None)
        Number = (0xff74ccf4, None)
        Operator = (0xffeeeeec, None)
        ParameterExpansion = (0xffeeeeec, None)
        Scalar = (0xfffce94f, True)
        SingleQuotedHereDocument = (0xffc4bbb8, None)
        SingleQuotedString = (0xffc4bbb8, None)
    
    class Batch:
        Comment = (0xff6cab9d, None)
        Default = (0xffeeeeec, None)
        ExternalCommand = (0xffa3c2da, None)
        HideCommandChar = (0xff7f7f00, None)
        Keyword = (0xffa3c2da, None)
        Label = (0xffc4bbb8, None)
        Operator = (0xffeeeeec, None)
        Variable = (0xff800080, None)
    
    class CMake:
        BlockForeach = (0xffa3c2da, None)
        BlockIf = (0xffa3c2da, None)
        BlockMacro = (0xffa3c2da, None)
        BlockWhile = (0xffa3c2da, None)
        Comment = (0xff6cab9d, None)
        Default = (0xffeeeeec, None)
        Function = (0xffa3c2da, None)
        KeywordSet3 = (0xffeeeeec, None)
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
        GlobalClass = (0xffeeeeec, None)
        HashQuotedString = (0xff6cab9d, None)
        Identifier = (0xffeeeeec, None)
        InactiveComment = (0xff90b090, None)
        InactiveCommentDoc = (0xffd0d0d0, None)
        InactiveCommentDocKeyword = (0xffc0c0c0, None)
        InactiveCommentDocKeywordError = (0xffc0c0c0, None)
        InactiveCommentLine = (0xff90b090, None)
        InactiveCommentLineDoc = (0xffc0c0c0, None)
        InactiveDefault = (0xffc0c0c0, None)
        InactiveDoubleQuotedString = (0xffb090b0, None)
        InactiveGlobalClass = (0xffb0b0b0, None)
        InactiveHashQuotedString = (0xffeeeeec, None)
        InactiveIdentifier = (0xffb0b0b0, None)
        InactiveKeyword = (0xff9090b0, None)
        InactiveKeywordSet2 = (0xffc0c0c0, None)
        InactiveNumber = (0xff90b090, None)
        InactiveOperator = (0xffb0b0b0, None)
        InactivePreProcessor = (0xffb0b090, None)
        InactivePreProcessorComment = (0xffeeeeec, None)
        InactivePreProcessorCommentLineDoc = (0xffc0c0c0, None)
        InactiveRawString = (0xffeeeeec, None)
        InactiveRegex = (0xff7faf7f, None)
        InactiveSingleQuotedString = (0xffb090b0, None)
        InactiveTripleQuotedVerbatimString = (0xffeeeeec, None)
        InactiveUUID = (0xffc0c0c0, None)
        InactiveUnclosedString = (0xffeeeeec, None)
        InactiveVerbatimString = (0xff90b090, None)
        Keyword = (0xffa3c2da, None)
        KeywordSet2 = (0xffeeeeec, None)
        Number = (0xff74ccf4, None)
        Operator = (0xffeeeeec, None)
        PreProcessor = (0xff7f7f00, None)
        PreProcessorComment = (0xff659900, None)
        PreProcessorCommentLineDoc = (0xff3f703f, None)
        RawString = (0xffc4bbb8, None)
        Regex = (0xff3f7f3f, None)
        SingleQuotedString = (0xffc4bbb8, None)
        TripleQuotedVerbatimString = (0xff6cab9d, None)
        UUID = (0xffeeeeec, None)
        UnclosedString = (0xffeeeeec, None)
        VerbatimString = (0xff6cab9d, None)
    
    class CSS:
        AtRule = (0xff7f7f00, None)
        Attribute = (0xffedff86, None)
        CSS1Property = (0xff0040e0, None)
        CSS2Property = (0xff00a0e0, None)
        CSS3Property = (0xffeeeeec, None)
        ClassSelector = (0xffeeeeec, None)
        Comment = (0xff6cab9d, None)
        Default = (0xffff0080, None)
        DoubleQuotedString = (0xffc4bbb8, None)
        ExtendedCSSProperty = (0xffeeeeec, None)
        ExtendedPseudoClass = (0xffeeeeec, None)
        ExtendedPseudoElement = (0xffeeeeec, None)
        IDSelector = (0xff74ccf4, None)
        Important = (0xffff8000, None)
        MediaRule = (0xff7f7f00, None)
        Operator = (0xffeeeeec, None)
        PseudoClass = (0xffedff86, None)
        PseudoElement = (0xffeeeeec, None)
        SingleQuotedString = (0xffc4bbb8, None)
        Tag = (0xffa3c2da, None)
        UnknownProperty = (0xffff0000, None)
        UnknownPseudoClass = (0xffff0000, None)
        Value = (0xffc4bbb8, None)
        Variable = (0xffeeeeec, None)
    
    class CSharp:
        Comment = (0xff6cab9d, None)
        CommentDoc = (0xff3f703f, None)
        CommentDocKeyword = (0xff3060a0, None)
        CommentDocKeywordError = (0xff804020, None)
        CommentLine = (0xff6cab9d, None)
        CommentLineDoc = (0xff3f703f, None)
        Default = (0xff808080, None)
        DoubleQuotedString = (0xffc4bbb8, None)
        GlobalClass = (0xffeeeeec, None)
        HashQuotedString = (0xff6cab9d, None)
        Identifier = (0xffeeeeec, None)
        InactiveComment = (0xff90b090, None)
        InactiveCommentDoc = (0xffd0d0d0, None)
        InactiveCommentDocKeyword = (0xffc0c0c0, None)
        InactiveCommentDocKeywordError = (0xffc0c0c0, None)
        InactiveCommentLine = (0xff90b090, None)
        InactiveCommentLineDoc = (0xffc0c0c0, None)
        InactiveDefault = (0xffc0c0c0, None)
        InactiveDoubleQuotedString = (0xffb090b0, None)
        InactiveGlobalClass = (0xffb0b0b0, None)
        InactiveHashQuotedString = (0xffeeeeec, None)
        InactiveIdentifier = (0xffb0b0b0, None)
        InactiveKeyword = (0xff9090b0, None)
        InactiveKeywordSet2 = (0xffc0c0c0, None)
        InactiveNumber = (0xff90b090, None)
        InactiveOperator = (0xffb0b0b0, None)
        InactivePreProcessor = (0xffb0b090, None)
        InactivePreProcessorComment = (0xffeeeeec, None)
        InactivePreProcessorCommentLineDoc = (0xffc0c0c0, None)
        InactiveRawString = (0xffeeeeec, None)
        InactiveRegex = (0xff7faf7f, None)
        InactiveSingleQuotedString = (0xffb090b0, None)
        InactiveTripleQuotedVerbatimString = (0xffeeeeec, None)
        InactiveUUID = (0xffc0c0c0, None)
        InactiveUnclosedString = (0xffeeeeec, None)
        InactiveVerbatimString = (0xff90b090, None)
        Keyword = (0xffa3c2da, None)
        KeywordSet2 = (0xffeeeeec, None)
        Number = (0xff74ccf4, None)
        Operator = (0xffeeeeec, None)
        PreProcessor = (0xff7f7f00, None)
        PreProcessorComment = (0xff659900, None)
        PreProcessorCommentLineDoc = (0xff3f703f, None)
        RawString = (0xffc4bbb8, None)
        Regex = (0xff3f7f3f, None)
        SingleQuotedString = (0xffc4bbb8, None)
        TripleQuotedVerbatimString = (0xff6cab9d, None)
        UUID = (0xffeeeeec, None)
        UnclosedString = (0xffeeeeec, None)
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
        GlobalClass = (0xffeeeeec, None)
        Identifier = (0xffeeeeec, None)
        Keyword = (0xffa3c2da, None)
        KeywordSet2 = (0xffeeeeec, None)
        Number = (0xff74ccf4, None)
        Operator = (0xffeeeeec, None)
        PreProcessor = (0xff7f7f00, None)
        Regex = (0xff3f7f3f, None)
        SingleQuotedString = (0xffc4bbb8, None)
        UUID = (0xffeeeeec, None)
        UnclosedString = (0xffeeeeec, None)
        VerbatimString = (0xff6cab9d, None)
    
    class D:
        BackquoteString = (0xffeeeeec, None)
        Character = (0xffc4bbb8, None)
        Comment = (0xff6cab9d, None)
        CommentDoc = (0xff3f703f, None)
        CommentDocKeyword = (0xff3060a0, None)
        CommentDocKeywordError = (0xff804020, None)
        CommentLine = (0xff6cab9d, None)
        CommentLineDoc = (0xff3f703f, None)
        CommentNested = (0xffa0c0a0, None)
        Default = (0xff808080, None)
        Identifier = (0xffeeeeec, None)
        Keyword = (0xffa3c2da, None)
        KeywordDoc = (0xffa3c2da, None)
        KeywordSecondary = (0xffa3c2da, None)
        KeywordSet5 = (0xffeeeeec, None)
        KeywordSet6 = (0xffeeeeec, None)
        KeywordSet7 = (0xffeeeeec, None)
        Number = (0xff74ccf4, None)
        Operator = (0xffeeeeec, None)
        RawString = (0xffeeeeec, None)
        String = (0xffc4bbb8, None)
        Typedefs = (0xffa3c2da, None)
        UnclosedString = (0xffeeeeec, None)
    
    class Diff:
        Command = (0xff7f7f00, None)
        Comment = (0xff6cab9d, None)
        Default = (0xffeeeeec, None)
        Header = (0xfff5b0cb, None)
        LineAdded = (0xffa3c2da, None)
        LineChanged = (0xff7f7f7f, None)
        LineRemoved = (0xff74ccf4, None)
        Position = (0xffc4bbb8, None)
    
    class Fortran:
        Comment = (0xff6cab9d, None)
        Continuation = (0xffeeeeec, None)
        Default = (0xff808080, None)
        DottedOperator = (0xffeeeeec, None)
        DoubleQuotedString = (0xffc4bbb8, None)
        ExtendedFunction = (0xffb04080, None)
        Identifier = (0xffeeeeec, None)
        IntrinsicFunction = (0xffb00040, None)
        Keyword = (0xffa3c2da, None)
        Label = (0xffe0c0e0, None)
        Number = (0xff74ccf4, None)
        Operator = (0xffeeeeec, None)
        PreProcessor = (0xff7f7f00, None)
        SingleQuotedString = (0xffc4bbb8, None)
        UnclosedString = (0xffeeeeec, None)
    
    class Fortran77:
        Comment = (0xff6cab9d, None)
        Continuation = (0xffeeeeec, None)
        Default = (0xff808080, None)
        DottedOperator = (0xffeeeeec, None)
        DoubleQuotedString = (0xffc4bbb8, None)
        ExtendedFunction = (0xffb04080, None)
        Identifier = (0xffeeeeec, None)
        IntrinsicFunction = (0xffb00040, None)
        Keyword = (0xffa3c2da, None)
        Label = (0xffe0c0e0, None)
        Number = (0xff74ccf4, None)
        Operator = (0xffeeeeec, None)
        PreProcessor = (0xff7f7f00, None)
        SingleQuotedString = (0xffc4bbb8, None)
        UnclosedString = (0xffeeeeec, None)
    
    class HTML:
        ASPAtStart = (0xffeeeeec, None)
        ASPJavaScriptComment = (0xff6cab9d, None)
        ASPJavaScriptCommentDoc = (0xff7f7f7f, None)
        ASPJavaScriptCommentLine = (0xff6cab9d, None)
        ASPJavaScriptDefault = (0xffeeeeec, None)
        ASPJavaScriptDoubleQuotedString = (0xffc4bbb8, None)
        ASPJavaScriptKeyword = (0xffa3c2da, None)
        ASPJavaScriptNumber = (0xff74ccf4, None)
        ASPJavaScriptRegex = (0xffeeeeec, None)
        ASPJavaScriptSingleQuotedString = (0xffc4bbb8, None)
        ASPJavaScriptStart = (0xff7f7f00, None)
        ASPJavaScriptSymbol = (0xffeeeeec, None)
        ASPJavaScriptUnclosedString = (0xffeeeeec, None)
        ASPJavaScriptWord = (0xffeeeeec, None)
        ASPPythonClassName = (0xff5abcd8, None)
        ASPPythonComment = (0xff6cab9d, None)
        ASPPythonDefault = (0xff808080, None)
        ASPPythonDoubleQuotedString = (0xffc4bbb8, None)
        ASPPythonFunctionMethodName = (0xff74ccf4, None)
        ASPPythonIdentifier = (0xffeeeeec, None)
        ASPPythonKeyword = (0xffa3c2da, None)
        ASPPythonNumber = (0xff74ccf4, None)
        ASPPythonOperator = (0xffeeeeec, None)
        ASPPythonSingleQuotedString = (0xffc4bbb8, None)
        ASPPythonStart = (0xff808080, None)
        ASPPythonTripleDoubleQuotedString = (0xfff5b0cb, None)
        ASPPythonTripleSingleQuotedString = (0xfff5b0cb, None)
        ASPStart = (0xffeeeeec, None)
        ASPVBScriptComment = (0xff008000, None)
        ASPVBScriptDefault = (0xffeeeeec, None)
        ASPVBScriptIdentifier = (0xff1f76e4, None)
        ASPVBScriptKeyword = (0xff1f76e4, None)
        ASPVBScriptNumber = (0xff008080, None)
        ASPVBScriptStart = (0xffeeeeec, None)
        ASPVBScriptString = (0xff800080, None)
        ASPVBScriptUnclosedString = (0xff1f76e4, None)
        ASPXCComment = (0xffeeeeec, None)
        Attribute = (0xff008080, None)
        CDATA = (0xffeeeeec, None)
        Default = (0xffeeeeec, None)
        Entity = (0xff800080, None)
        HTMLComment = (0xff808000, None)
        HTMLDoubleQuotedString = (0xffc4bbb8, None)
        HTMLNumber = (0xff74ccf4, None)
        HTMLSingleQuotedString = (0xffc4bbb8, None)
        HTMLValue = (0xffff00ff, None)
        JavaScriptComment = (0xff6cab9d, None)
        JavaScriptCommentDoc = (0xff3f703f, None)
        JavaScriptCommentLine = (0xff6cab9d, None)
        JavaScriptDefault = (0xffeeeeec, None)
        JavaScriptDoubleQuotedString = (0xffc4bbb8, None)
        JavaScriptKeyword = (0xffa3c2da, None)
        JavaScriptNumber = (0xff74ccf4, None)
        JavaScriptRegex = (0xffeeeeec, None)
        JavaScriptSingleQuotedString = (0xffc4bbb8, None)
        JavaScriptStart = (0xff7f7f00, None)
        JavaScriptSymbol = (0xffeeeeec, None)
        JavaScriptUnclosedString = (0xffeeeeec, None)
        JavaScriptWord = (0xffeeeeec, None)
        OtherInTag = (0xff800080, None)
        PHPComment = (0xff999999, None)
        PHPCommentLine = (0xff666666, None)
        PHPDefault = (0xffc7dbf5, None)
        PHPDoubleQuotedString = (0xff6cab9d, None)
        PHPDoubleQuotedVariable = (0xffa3c2da, None)
        PHPKeyword = (0xffc4bbb8, None)
        PHPNumber = (0xffcc9900, None)
        PHPOperator = (0xffeeeeec, None)
        PHPSingleQuotedString = (0xff009f00, None)
        PHPStart = (0xff5abcd8, None)
        PHPVariable = (0xffa3c2da, None)
        PythonClassName = (0xff5abcd8, None)
        PythonComment = (0xff6cab9d, None)
        PythonDefault = (0xff808080, None)
        PythonDoubleQuotedString = (0xffc4bbb8, None)
        PythonFunctionMethodName = (0xff74ccf4, None)
        PythonIdentifier = (0xffeeeeec, None)
        PythonKeyword = (0xffa3c2da, None)
        PythonNumber = (0xff74ccf4, None)
        PythonOperator = (0xffeeeeec, None)
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
        SGMLParameterComment = (0xffeeeeec, None)
        SGMLSingleQuotedString = (0xff993300, None)
        SGMLSpecial = (0xff3366ff, None)
        Script = (0xff1f76e4, None)
        Tag = (0xff1f76e4, None)
        UnknownAttribute = (0xffff0000, None)
        UnknownTag = (0xffff0000, None)
        VBScriptComment = (0xff008000, None)
        VBScriptDefault = (0xffeeeeec, None)
        VBScriptIdentifier = (0xff1f76e4, None)
        VBScriptKeyword = (0xff1f76e4, None)
        VBScriptNumber = (0xff008080, None)
        VBScriptStart = (0xffeeeeec, None)
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
        GlobalClass = (0xffeeeeec, None)
        HashQuotedString = (0xff6cab9d, None)
        Identifier = (0xffeeeeec, None)
        InactiveComment = (0xff90b090, None)
        InactiveCommentDoc = (0xffd0d0d0, None)
        InactiveCommentDocKeyword = (0xffc0c0c0, None)
        InactiveCommentDocKeywordError = (0xffc0c0c0, None)
        InactiveCommentLine = (0xff90b090, None)
        InactiveCommentLineDoc = (0xffc0c0c0, None)
        InactiveDefault = (0xffc0c0c0, None)
        InactiveDoubleQuotedString = (0xffb090b0, None)
        InactiveGlobalClass = (0xffb0b0b0, None)
        InactiveHashQuotedString = (0xffeeeeec, None)
        InactiveIdentifier = (0xffb0b0b0, None)
        InactiveKeyword = (0xff9090b0, None)
        InactiveKeywordSet2 = (0xffc0c0c0, None)
        InactiveNumber = (0xff90b090, None)
        InactiveOperator = (0xffb0b0b0, None)
        InactivePreProcessor = (0xffb0b090, None)
        InactivePreProcessorComment = (0xffeeeeec, None)
        InactivePreProcessorCommentLineDoc = (0xffc0c0c0, None)
        InactiveRawString = (0xffeeeeec, None)
        InactiveRegex = (0xff7faf7f, None)
        InactiveSingleQuotedString = (0xffb090b0, None)
        InactiveTripleQuotedVerbatimString = (0xffeeeeec, None)
        InactiveUUID = (0xffc0c0c0, None)
        InactiveUnclosedString = (0xffeeeeec, None)
        InactiveVerbatimString = (0xff90b090, None)
        Keyword = (0xffa3c2da, None)
        KeywordSet2 = (0xffeeeeec, None)
        Number = (0xff74ccf4, None)
        Operator = (0xffeeeeec, None)
        PreProcessor = (0xff7f7f00, None)
        PreProcessorComment = (0xff659900, None)
        PreProcessorCommentLineDoc = (0xff3f703f, None)
        RawString = (0xffc4bbb8, None)
        Regex = (0xff3f7f3f, None)
        SingleQuotedString = (0xffc4bbb8, None)
        TripleQuotedVerbatimString = (0xff6cab9d, None)
        UUID = (0xff804080, None)
        UnclosedString = (0xffeeeeec, None)
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
        GlobalClass = (0xffeeeeec, None)
        HashQuotedString = (0xff6cab9d, None)
        Identifier = (0xffeeeeec, None)
        InactiveComment = (0xff90b090, None)
        InactiveCommentDoc = (0xffd0d0d0, None)
        InactiveCommentDocKeyword = (0xffc0c0c0, None)
        InactiveCommentDocKeywordError = (0xffc0c0c0, None)
        InactiveCommentLine = (0xff90b090, None)
        InactiveCommentLineDoc = (0xffc0c0c0, None)
        InactiveDefault = (0xffc0c0c0, None)
        InactiveDoubleQuotedString = (0xffb090b0, None)
        InactiveGlobalClass = (0xffb0b0b0, None)
        InactiveHashQuotedString = (0xffeeeeec, None)
        InactiveIdentifier = (0xffb0b0b0, None)
        InactiveKeyword = (0xff9090b0, None)
        InactiveKeywordSet2 = (0xffc0c0c0, None)
        InactiveNumber = (0xff90b090, None)
        InactiveOperator = (0xffb0b0b0, None)
        InactivePreProcessor = (0xffb0b090, None)
        InactivePreProcessorComment = (0xffeeeeec, None)
        InactivePreProcessorCommentLineDoc = (0xffc0c0c0, None)
        InactiveRawString = (0xffeeeeec, None)
        InactiveRegex = (0xff7faf7f, None)
        InactiveSingleQuotedString = (0xffb090b0, None)
        InactiveTripleQuotedVerbatimString = (0xffeeeeec, None)
        InactiveUUID = (0xffc0c0c0, None)
        InactiveUnclosedString = (0xffeeeeec, None)
        InactiveVerbatimString = (0xff90b090, None)
        Keyword = (0xffa3c2da, None)
        KeywordSet2 = (0xffeeeeec, None)
        Number = (0xff74ccf4, None)
        Operator = (0xffeeeeec, None)
        PreProcessor = (0xff7f7f00, None)
        PreProcessorComment = (0xff659900, None)
        PreProcessorCommentLineDoc = (0xff3f703f, None)
        RawString = (0xffc4bbb8, None)
        Regex = (0xff3f7f3f, None)
        SingleQuotedString = (0xffc4bbb8, None)
        TripleQuotedVerbatimString = (0xff6cab9d, None)
        UUID = (0xffeeeeec, None)
        UnclosedString = (0xffeeeeec, None)
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
        GlobalClass = (0xffeeeeec, None)
        HashQuotedString = (0xff6cab9d, None)
        Identifier = (0xffeeeeec, None)
        InactiveComment = (0xff90b090, None)
        InactiveCommentDoc = (0xffd0d0d0, None)
        InactiveCommentDocKeyword = (0xffc0c0c0, None)
        InactiveCommentDocKeywordError = (0xffc0c0c0, None)
        InactiveCommentLine = (0xff90b090, None)
        InactiveCommentLineDoc = (0xffc0c0c0, None)
        InactiveDefault = (0xffc0c0c0, None)
        InactiveDoubleQuotedString = (0xffb090b0, None)
        InactiveGlobalClass = (0xffb0b0b0, None)
        InactiveHashQuotedString = (0xffeeeeec, None)
        InactiveIdentifier = (0xffb0b0b0, None)
        InactiveKeyword = (0xff9090b0, None)
        InactiveKeywordSet2 = (0xffc0c0c0, None)
        InactiveNumber = (0xff90b090, None)
        InactiveOperator = (0xffb0b0b0, None)
        InactivePreProcessor = (0xffb0b090, None)
        InactivePreProcessorComment = (0xffeeeeec, None)
        InactivePreProcessorCommentLineDoc = (0xffc0c0c0, None)
        InactiveRawString = (0xffeeeeec, None)
        InactiveRegex = (0xff7faf7f, None)
        InactiveSingleQuotedString = (0xffb090b0, None)
        InactiveTripleQuotedVerbatimString = (0xffeeeeec, None)
        InactiveUUID = (0xffc0c0c0, None)
        InactiveUnclosedString = (0xffeeeeec, None)
        InactiveVerbatimString = (0xff90b090, None)
        Keyword = (0xffa3c2da, None)
        KeywordSet2 = (0xffeeeeec, None)
        Number = (0xff74ccf4, None)
        Operator = (0xffeeeeec, None)
        PreProcessor = (0xff7f7f00, None)
        PreProcessorComment = (0xff659900, None)
        PreProcessorCommentLineDoc = (0xff3f703f, None)
        RawString = (0xffc4bbb8, None)
        Regex = (0xff3f7f3f, None)
        SingleQuotedString = (0xffc4bbb8, None)
        TripleQuotedVerbatimString = (0xff6cab9d, None)
        UUID = (0xffeeeeec, None)
        UnclosedString = (0xffeeeeec, None)
        VerbatimString = (0xff6cab9d, None)
    
    class Lua:
        BasicFunctions = (0xffa3c2da, None)
        Character = (0xffc4bbb8, None)
        Comment = (0xff6cab9d, None)
        CoroutinesIOSystemFacilities = (0xffa3c2da, None)
        Default = (0xffeeeeec, None)
        Identifier = (0xffeeeeec, None)
        Keyword = (0xffa3c2da, None)
        KeywordSet5 = (0xffeeeeec, None)
        KeywordSet6 = (0xffeeeeec, None)
        KeywordSet7 = (0xffeeeeec, None)
        KeywordSet8 = (0xffeeeeec, None)
        Label = (0xff7f7f00, None)
        LineComment = (0xff6cab9d, None)
        LiteralString = (0xffc4bbb8, None)
        Number = (0xff74ccf4, None)
        Operator = (0xffeeeeec, None)
        Preprocessor = (0xff7f7f00, None)
        String = (0xffc4bbb8, None)
        StringTableMathsFunctions = (0xffa3c2da, None)
        UnclosedString = (0xffeeeeec, None)
    
    class Makefile:
        Comment = (0xff6cab9d, None)
        Default = (0xffeeeeec, None)
        Error = (0xffffff00, None)
        Operator = (0xffeeeeec, None)
        Preprocessor = (0xff7f7f00, None)
        Target = (0xffa00000, None)
        Variable = (0xff1f76e4, None)
    
    class Matlab:
        Command = (0xff7f7f00, None)
        Comment = (0xff6cab9d, None)
        Default = (0xffeeeeec, None)
        DoubleQuotedString = (0xffc4bbb8, None)
        Identifier = (0xffeeeeec, None)
        Keyword = (0xffa3c2da, None)
        Number = (0xff74ccf4, None)
        Operator = (0xffeeeeec, None)
        SingleQuotedString = (0xffc4bbb8, None)
    
    class Octave:
        Command = (0xff7f7f00, None)
        Comment = (0xff6cab9d, None)
        Default = (0xffeeeeec, None)
        DoubleQuotedString = (0xffc4bbb8, None)
        Identifier = (0xffeeeeec, None)
        Keyword = (0xffa3c2da, None)
        Number = (0xff74ccf4, None)
        Operator = (0xffeeeeec, None)
        SingleQuotedString = (0xffc4bbb8, None)
    
    class PO:
        Comment = (0xff6cab9d, None)
        Default = (0xffeeeeec, None)
        Flags = (0xffeeeeec, None)
        Fuzzy = (0xffeeeeec, None)
        MessageContext = (0xffeeeeec, None)
        MessageContextText = (0xffeeeeec, None)
        MessageContextTextEOL = (0xffeeeeec, None)
        MessageId = (0xffeeeeec, None)
        MessageIdText = (0xffeeeeec, None)
        MessageIdTextEOL = (0xffeeeeec, None)
        MessageString = (0xffeeeeec, None)
        MessageStringText = (0xffeeeeec, None)
        MessageStringTextEOL = (0xffeeeeec, None)
        ProgrammerComment = (0xffeeeeec, None)
        Reference = (0xffeeeeec, None)
    
    class POV:
        BadDirective = (0xff804020, None)
        Comment = (0xff6cab9d, None)
        CommentLine = (0xff6cab9d, None)
        Default = (0xffff0080, None)
        Directive = (0xff7f7f00, None)
        Identifier = (0xffeeeeec, None)
        KeywordSet6 = (0xffa3c2da, None)
        KeywordSet7 = (0xffa3c2da, None)
        KeywordSet8 = (0xffa3c2da, None)
        Number = (0xff74ccf4, None)
        ObjectsCSGAppearance = (0xffa3c2da, None)
        Operator = (0xffeeeeec, None)
        PredefinedFunctions = (0xffa3c2da, None)
        PredefinedIdentifiers = (0xffa3c2da, None)
        String = (0xffc4bbb8, None)
        TypesModifiersItems = (0xffa3c2da, None)
        UnclosedString = (0xffeeeeec, None)
    
    class Pascal:
        Asm = (0xff804080, None)
        Character = (0xffc4bbb8, None)
        Comment = (0xff6cab9d, None)
        CommentLine = (0xff6cab9d, None)
        CommentParenthesis = (0xff6cab9d, None)
        Default = (0xff808080, None)
        HexNumber = (0xff74ccf4, None)
        Identifier = (0xffeeeeec, None)
        Keyword = (0xffa3c2da, None)
        Number = (0xff74ccf4, None)
        Operator = (0xffeeeeec, None)
        PreProcessor = (0xff7f7f00, None)
        PreProcessorParenthesis = (0xff7f7f00, None)
        SingleQuotedString = (0xffc4bbb8, None)
        UnclosedString = (0xffeeeeec, None)
    
    class Perl:
        Array = (0xffeeeeec, None)
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
        Hash = (0xffeeeeec, None)
        HereDocumentDelimiter = (0xffeeeeec, None)
        Identifier = (0xffeeeeec, None)
        Keyword = (0xffa3c2da, None)
        Number = (0xff74ccf4, None)
        Operator = (0xffeeeeec, None)
        POD = (0xff004000, None)
        PODVerbatim = (0xff004000, None)
        QuotedStringQ = (0xffc4bbb8, None)
        QuotedStringQQ = (0xffc4bbb8, None)
        QuotedStringQQVar = (0xffd00000, None)
        QuotedStringQR = (0xffeeeeec, None)
        QuotedStringQRVar = (0xffd00000, None)
        QuotedStringQW = (0xffeeeeec, None)
        QuotedStringQX = (0xffffff00, None)
        QuotedStringQXVar = (0xffd00000, None)
        Regex = (0xffeeeeec, None)
        RegexVar = (0xffd00000, None)
        Scalar = (0xffeeeeec, None)
        SingleQuotedHereDocument = (0xffc4bbb8, None)
        SingleQuotedString = (0xffc4bbb8, None)
        SubroutinePrototype = (0xffeeeeec, None)
        Substitution = (0xffeeeeec, None)
        SubstitutionVar = (0xffd00000, None)
        SymbolTable = (0xffeeeeec, None)
        Translation = (0xffeeeeec, None)
    
    class PostScript:
        ArrayParenthesis = (0xffa3c2da, None)
        BadStringCharacter = (0xffffff00, None)
        Base85String = (0xffc4bbb8, None)
        Comment = (0xff6cab9d, None)
        DSCComment = (0xff3f703f, None)
        DSCCommentValue = (0xff3060a0, None)
        Default = (0xffeeeeec, None)
        DictionaryParenthesis = (0xff3060a0, None)
        HexString = (0xff3f7f3f, None)
        ImmediateEvalLiteral = (0xff7f7f00, None)
        Keyword = (0xffa3c2da, None)
        Literal = (0xff7f7f00, None)
        Name = (0xffeeeeec, None)
        Number = (0xff74ccf4, None)
        ProcedureParenthesis = (0xffeeeeec, None)
        Text = (0xffc4bbb8, None)
    
    class Properties:
        Assignment = (0xffb06000, None)
        Comment = (0xff74ccf4, None)
        Default = (0xffeeeeec, None)
        DefaultValue = (0xff7f7f00, None)
        Key = (0xffeeeeec, None)
        Section = (0xffc4bbb8, None)
    
    class Python:
        ClassName = (0xff5abcd8, None)
        Comment = (0xff6cab9d, None)
        CommentBlock = (0xff7f7f7f, None)
        Decorator = (0xff805000, None)
        Default = (0xffeeeeec, None)
        DoubleQuotedString = (0xffc4bbb8, None)
        FunctionMethodName = (0xff74ccf4, None)
        HighlightedIdentifier = (0xff407090, None)
        Identifier = (0xffeeeeec, None)
        Inconsistent = (0xff6cab9d, None)
        Keyword = (0xffa3c2da, None)
        NoWarning = (0xff808080, None)
        Number = (0xff74ccf4, None)
        Operator = (0xffeeeeec, None)
        SingleQuotedString = (0xffc4bbb8, None)
        Spaces = (0xffc4bbb8, None)
        Tabs = (0xffc4bbb8, None)
        TabsAfterSpaces = (0xff74ccf4, None)
        TripleDoubleQuotedString = (0xfff5b0cb, None)
        TripleSingleQuotedString = (0xfff5b0cb, None)
        UnclosedString = (0xffeeeeec, None)
    
    class Ruby:
        Backticks = (0xffffff00, None)
        ClassName = (0xff5abcd8, None)
        ClassVariable = (0xff8000b0, None)
        Comment = (0xff6cab9d, None)
        DataSection = (0xff600000, None)
        Default = (0xff808080, None)
        DemotedKeyword = (0xffa3c2da, None)
        DoubleQuotedString = (0xffc4bbb8, None)
        Error = (0xffeeeeec, None)
        FunctionMethodName = (0xff74ccf4, None)
        Global = (0xff800080, None)
        HereDocument = (0xffc4bbb8, None)
        HereDocumentDelimiter = (0xffeeeeec, None)
        Identifier = (0xffeeeeec, None)
        InstanceVariable = (0xffb00080, None)
        Keyword = (0xffa3c2da, None)
        ModuleName = (0xffa000a0, None)
        Number = (0xff74ccf4, None)
        Operator = (0xffeeeeec, None)
        POD = (0xff004000, None)
        PercentStringQ = (0xffc4bbb8, None)
        PercentStringq = (0xffc4bbb8, None)
        PercentStringr = (0xffeeeeec, None)
        PercentStringw = (0xffeeeeec, None)
        PercentStringx = (0xffffff00, None)
        Regex = (0xffeeeeec, None)
        SingleQuotedString = (0xffc4bbb8, None)
        Stderr = (0xffeeeeec, None)
        Stdin = (0xffeeeeec, None)
        Stdout = (0xffeeeeec, None)
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
        Identifier = (0xffeeeeec, None)
        Keyword = (0xffa3c2da, None)
        KeywordSet5 = (0xff4b0082, None)
        KeywordSet6 = (0xffb00040, None)
        KeywordSet7 = (0xff8b0000, None)
        KeywordSet8 = (0xff800080, None)
        Number = (0xff74ccf4, None)
        Operator = (0xffeeeeec, None)
        PlusComment = (0xff6cab9d, None)
        PlusKeyword = (0xff7f7f00, None)
        PlusPrompt = (0xff6cab9d, None)
        QuotedIdentifier = (0xffeeeeec, None)
        SingleQuotedString = (0xffc4bbb8, None)
    
    class Spice:
        Command = (0xffa3c2da, None)
        Comment = (0xff6cab9d, None)
        Default = (0xff808080, None)
        Delimiter = (0xffeeeeec, None)
        Function = (0xffa3c2da, None)
        Identifier = (0xffeeeeec, None)
        Number = (0xff74ccf4, None)
        Parameter = (0xff0040e0, None)
        Value = (0xffc4bbb8, None)
    
    class TCL:
        Comment = (0xff6cab9d, None)
        CommentBlock = (0xffeeeeec, None)
        CommentBox = (0xff6cab9d, None)
        CommentLine = (0xff6cab9d, None)
        Default = (0xff808080, None)
        ExpandKeyword = (0xffa3c2da, None)
        ITCLKeyword = (0xffa3c2da, None)
        Identifier = (0xffa3c2da, None)
        KeywordSet6 = (0xffa3c2da, None)
        KeywordSet7 = (0xffa3c2da, None)
        KeywordSet8 = (0xffa3c2da, None)
        KeywordSet9 = (0xffa3c2da, None)
        Modifier = (0xffc4bbb8, None)
        Number = (0xff74ccf4, None)
        Operator = (0xffeeeeec, None)
        QuotedKeyword = (0xffc4bbb8, None)
        QuotedString = (0xffc4bbb8, None)
        Substitution = (0xff7f7f00, None)
        SubstitutionBrace = (0xff7f7f00, None)
        TCLKeyword = (0xffa3c2da, None)
        TkCommand = (0xffa3c2da, None)
        TkKeyword = (0xffa3c2da, None)
    
    class TeX:
        Command = (0xff6cab9d, None)
        Default = (0xff3f3f3f, None)
        Group = (0xfff5b0cb, None)
        Special = (0xff74ccf4, None)
        Symbol = (0xff7f7f00, None)
        Text = (0xffeeeeec, None)
    
    class VHDL:
        Attribute = (0xff804020, None)
        Comment = (0xff6cab9d, None)
        CommentLine = (0xff3f7f3f, None)
        Default = (0xff800080, None)
        Identifier = (0xffeeeeec, None)
        Keyword = (0xffa3c2da, None)
        KeywordSet7 = (0xff804020, None)
        Number = (0xff74ccf4, None)
        Operator = (0xffeeeeec, None)
        StandardFunction = (0xff808020, None)
        StandardOperator = (0xff74ccf4, None)
        StandardPackage = (0xff208020, None)
        StandardType = (0xff208080, None)
        String = (0xffc4bbb8, None)
        UnclosedString = (0xffeeeeec, None)
    
    class Verilog:
        Comment = (0xff6cab9d, None)
        CommentBang = (0xff3f7f3f, None)
        CommentLine = (0xff6cab9d, None)
        Default = (0xff808080, None)
        Identifier = (0xffeeeeec, None)
        Keyword = (0xffa3c2da, None)
        KeywordSet2 = (0xff74ccf4, None)
        Number = (0xff74ccf4, None)
        Operator = (0xff007070, None)
        Preprocessor = (0xff7f7f00, None)
        String = (0xffc4bbb8, None)
        SystemTask = (0xff804020, None)
        UnclosedString = (0xffeeeeec, None)
        UserKeywordSet = (0xff2a00ff, None)
    
    class XML:
        ASPAtStart = (0xffeeeeec, None)
        ASPJavaScriptComment = (0xff6cab9d, None)
        ASPJavaScriptCommentDoc = (0xff7f7f7f, None)
        ASPJavaScriptCommentLine = (0xff6cab9d, None)
        ASPJavaScriptDefault = (0xffeeeeec, None)
        ASPJavaScriptDoubleQuotedString = (0xffc4bbb8, None)
        ASPJavaScriptKeyword = (0xffa3c2da, None)
        ASPJavaScriptNumber = (0xff74ccf4, None)
        ASPJavaScriptRegex = (0xffeeeeec, None)
        ASPJavaScriptSingleQuotedString = (0xffc4bbb8, None)
        ASPJavaScriptStart = (0xff7f7f00, None)
        ASPJavaScriptSymbol = (0xffeeeeec, None)
        ASPJavaScriptUnclosedString = (0xffeeeeec, None)
        ASPJavaScriptWord = (0xffeeeeec, None)
        ASPPythonClassName = (0xff5abcd8, None)
        ASPPythonComment = (0xff6cab9d, None)
        ASPPythonDefault = (0xff808080, None)
        ASPPythonDoubleQuotedString = (0xffc4bbb8, None)
        ASPPythonFunctionMethodName = (0xff74ccf4, None)
        ASPPythonIdentifier = (0xffeeeeec, None)
        ASPPythonKeyword = (0xffa3c2da, None)
        ASPPythonNumber = (0xff74ccf4, None)
        ASPPythonOperator = (0xffeeeeec, None)
        ASPPythonSingleQuotedString = (0xffc4bbb8, None)
        ASPPythonStart = (0xff808080, None)
        ASPPythonTripleDoubleQuotedString = (0xfff5b0cb, None)
        ASPPythonTripleSingleQuotedString = (0xfff5b0cb, None)
        ASPStart = (0xffeeeeec, None)
        ASPVBScriptComment = (0xff008000, None)
        ASPVBScriptDefault = (0xffeeeeec, None)
        ASPVBScriptIdentifier = (0xff1f76e4, None)
        ASPVBScriptKeyword = (0xff1f76e4, None)
        ASPVBScriptNumber = (0xff008080, None)
        ASPVBScriptStart = (0xffeeeeec, None)
        ASPVBScriptString = (0xff800080, None)
        ASPVBScriptUnclosedString = (0xff1f76e4, None)
        ASPXCComment = (0xffeeeeec, None)
        Attribute = (0xff008080, None)
        CDATA = (0xffedff86, None)
        Default = (0xffeeeeec, None)
        Entity = (0xff800080, None)
        HTMLComment = (0xff808000, None)
        HTMLDoubleQuotedString = (0xffc4bbb8, None)
        HTMLNumber = (0xff74ccf4, None)
        HTMLSingleQuotedString = (0xffc4bbb8, None)
        HTMLValue = (0xff608060, None)
        JavaScriptComment = (0xff6cab9d, None)
        JavaScriptCommentDoc = (0xff3f703f, None)
        JavaScriptCommentLine = (0xff6cab9d, None)
        JavaScriptDefault = (0xffeeeeec, None)
        JavaScriptDoubleQuotedString = (0xffc4bbb8, None)
        JavaScriptKeyword = (0xffa3c2da, None)
        JavaScriptNumber = (0xff74ccf4, None)
        JavaScriptRegex = (0xffeeeeec, None)
        JavaScriptSingleQuotedString = (0xffc4bbb8, None)
        JavaScriptStart = (0xff7f7f00, None)
        JavaScriptSymbol = (0xffeeeeec, None)
        JavaScriptUnclosedString = (0xffeeeeec, None)
        JavaScriptWord = (0xffeeeeec, None)
        OtherInTag = (0xff800080, None)
        PHPComment = (0xff999999, None)
        PHPCommentLine = (0xff666666, None)
        PHPDefault = (0xffc7dbf5, None)
        PHPDoubleQuotedString = (0xff6cab9d, None)
        PHPDoubleQuotedVariable = (0xffa3c2da, None)
        PHPKeyword = (0xffc4bbb8, None)
        PHPNumber = (0xffcc9900, None)
        PHPOperator = (0xffeeeeec, None)
        PHPSingleQuotedString = (0xff009f00, None)
        PHPStart = (0xffedff86, None)
        PHPVariable = (0xffa3c2da, None)
        PythonClassName = (0xff5abcd8, None)
        PythonComment = (0xff6cab9d, None)
        PythonDefault = (0xff808080, None)
        PythonDoubleQuotedString = (0xffc4bbb8, None)
        PythonFunctionMethodName = (0xff74ccf4, None)
        PythonIdentifier = (0xffeeeeec, None)
        PythonKeyword = (0xffa3c2da, None)
        PythonNumber = (0xff74ccf4, None)
        PythonOperator = (0xffeeeeec, None)
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
        SGMLParameterComment = (0xffeeeeec, None)
        SGMLSingleQuotedString = (0xff993300, None)
        SGMLSpecial = (0xff3366ff, None)
        Script = (0xff1f76e4, None)
        Tag = (0xff1f76e4, None)
        UnknownAttribute = (0xff008080, None)
        UnknownTag = (0xff1f76e4, None)
        VBScriptComment = (0xff008000, None)
        VBScriptDefault = (0xffeeeeec, None)
        VBScriptIdentifier = (0xff1f76e4, None)
        VBScriptKeyword = (0xff1f76e4, None)
        VBScriptNumber = (0xff008080, None)
        VBScriptStart = (0xffeeeeec, None)
        VBScriptString = (0xff800080, None)
        VBScriptUnclosedString = (0xff1f76e4, None)
        XMLEnd = (0xff800080, None)
        XMLStart = (0xff800080, None)
        XMLTagEnd = (0xff1f76e4, None)
    
    class YAML:
        Comment = (0xff008800, None)
        Default = (0xffeeeeec, None)
        DocumentDelimiter = (0xff112435, None)
        Identifier = (0xfff3c969, None)
        Keyword = (0xff880088, None)
        Number = (0xff880000, None)
        Operator = (0xffeeeeec, None)
        Reference = (0xff008888, None)
        SyntaxErrorMarker = (0xff112435, None)
        TextBlockMarker = (0xff333366, None)


class Paper:
    Default = PyQt4.QtGui.QColor(0xff3465a4)
    
    class Ada:
        Default = 0xff3465a4
        Comment = 0xff3465a4
        Keyword = 0xff3465a4
        String = 0xff3465a4
        Procedure = 0xff3465a4
        Number = 0xff3465a4
        Type = 0xff3465a4
        Package = 0xff3465a4
    
    class Nim:
        Default = 0xff3465a4
        Comment = 0xff3465a4
        BasicKeyword = 0xff3465a4
        TopKeyword = 0xff3465a4
        String = 0xff3465a4
        LongString = 0xff3465a4
        Number = 0xff3465a4
        Operator = 0xff3465a4
        Unsafe = 0xff3465a4
        Type = 0xff3465a4
        DocumentationComment = 0xff3465a4
        Definition = 0xff3465a4
        Class = 0xff3465a4
        KeywordOperator = 0xff3465a4
        CharLiteral = 0xff3465a4
        CaseOf = 0xff3465a4
        UserKeyword = 0xff3465a4
        MultilineComment = 0xff3465a4
        MultilineDocumentation = 0xff3465a4
        Pragma = 0xff3465a4
    
    class Oberon:
        Default = 0xff3465a4
        Comment = 0xff3465a4
        Keyword = 0xff3465a4
        String = 0xff3465a4
        Procedure = 0xff3465a4
        Module = 0xff3465a4
        Number = 0xff3465a4
        Type = 0xff3465a4
    
    
    # Generated
    class AVS:
        Function = 0xff3465a4
        KeywordSet6 = 0xff3465a4
        TripleString = 0xff3465a4
        LineComment = 0xff3465a4
        Plugin = 0xff3465a4
        String = 0xff3465a4
        ClipProperty = 0xff3465a4
        Default = 0xff3465a4
        Operator = 0xff3465a4
        Number = 0xff3465a4
        Filter = 0xff3465a4
        Identifier = 0xff3465a4
        NestedBlockComment = 0xff3465a4
        Keyword = 0xff3465a4
        BlockComment = 0xff3465a4
    
    class Bash:
        Error = 0xffff0000
        Backticks = 0xffa08080
        SingleQuotedHereDocument = 0xffddd0dd
        Scalar = 0xffffe0e0
        HereDocumentDelimiter = 0xffddd0dd
        Comment = 0xff3465a4
        SingleQuotedString = 0xff3465a4
        Default = 0xff3465a4
        Operator = 0xff3465a4
        ParameterExpansion = 0xffffffe0
        Number = 0xff3465a4
        Identifier = 0xff3465a4
        Keyword = 0xff3465a4
        DoubleQuotedString = 0xff3465a4
    
    class Batch:
        Label = 0xff606060
        Default = 0xff3465a4
        Keyword = 0xff3465a4
        ExternalCommand = 0xff3465a4
        Variable = 0xff3465a4
        Comment = 0xff3465a4
        HideCommandChar = 0xff3465a4
        Operator = 0xff3465a4
    
    class CMake:
        Function = 0xff3465a4
        BlockForeach = 0xff3465a4
        BlockWhile = 0xff3465a4
        StringLeftQuote = 0xffeeeeee
        Label = 0xff3465a4
        Comment = 0xff3465a4
        BlockMacro = 0xff3465a4
        StringRightQuote = 0xffeeeeee
        Default = 0xff3465a4
        Number = 0xff3465a4
        BlockIf = 0xff3465a4
        Variable = 0xff3465a4
        KeywordSet3 = 0xff3465a4
        String = 0xffeeeeee
        StringVariable = 0xffeeeeee
    
    class CPP:
        CommentDocKeywordError = 0xff3465a4
        InactiveRegex = 0xffe0f0e0
        InactivePreProcessorComment = 0xff3465a4
        UUID = 0xff3465a4
        InactiveVerbatimString = 0xffe0ffe0
        SingleQuotedString = 0xff3465a4
        Operator = 0xff3465a4
        InactiveOperator = 0xff3465a4
        InactivePreProcessor = 0xff3465a4
        UnclosedString = 0xffe0c0e0
        Identifier = 0xff3465a4
        InactiveRawString = 0xff3465a4
        PreProcessor = 0xff3465a4
        KeywordSet2 = 0xff3465a4
        InactiveUnclosedString = 0xffe0c0e0
        InactiveCommentLine = 0xff3465a4
        InactiveNumber = 0xff3465a4
        InactivePreProcessorCommentLineDoc = 0xff3465a4
        Number = 0xff3465a4
        InactiveUUID = 0xff3465a4
        CommentDoc = 0xff3465a4
        InactiveCommentDoc = 0xff3465a4
        GlobalClass = 0xff3465a4
        InactiveSingleQuotedString = 0xff3465a4
        HashQuotedString = 0xffe7ffd7
        VerbatimString = 0xffe0ffe0
        InactiveHashQuotedString = 0xff3465a4
        Regex = 0xffe0f0e0
        InactiveGlobalClass = 0xff3465a4
        InactiveIdentifier = 0xff3465a4
        CommentLineDoc = 0xff3465a4
        TripleQuotedVerbatimString = 0xffe0ffe0
        InactiveKeywordSet2 = 0xff3465a4
        InactiveCommentDocKeyword = 0xff3465a4
        Keyword = 0xff3465a4
        InactiveCommentLineDoc = 0xff3465a4
        InactiveDefault = 0xff3465a4
        InactiveCommentDocKeywordError = 0xff3465a4
        InactiveTripleQuotedVerbatimString = 0xff3465a4
        CommentDocKeyword = 0xff3465a4
        InactiveDoubleQuotedString = 0xff3465a4
        CommentLine = 0xff3465a4
        Comment = 0xff3465a4
        PreProcessorComment = 0xff3465a4
        InactiveComment = 0xff3465a4
        RawString = 0xfffff3ff
        Default = 0xff3465a4
        PreProcessorCommentLineDoc = 0xff3465a4
        DoubleQuotedString = 0xff3465a4
        InactiveKeyword = 0xff3465a4
    
    class CSS:
        Important = 0xff3465a4
        CSS3Property = 0xff3465a4
        Attribute = 0xff3465a4
        Comment = 0xff3465a4
        SingleQuotedString = 0xff3465a4
        MediaRule = 0xff3465a4
        AtRule = 0xff3465a4
        UnknownPseudoClass = 0xff3465a4
        PseudoClass = 0xff3465a4
        Tag = 0xff3465a4
        CSS2Property = 0xff3465a4
        CSS1Property = 0xff3465a4
        IDSelector = 0xff3465a4
        ExtendedCSSProperty = 0xff3465a4
        Variable = 0xff3465a4
        ExtendedPseudoClass = 0xff3465a4
        ClassSelector = 0xff3465a4
        Default = 0xff3465a4
        PseudoElement = 0xff3465a4
        UnknownProperty = 0xff3465a4
        Value = 0xff3465a4
        ExtendedPseudoElement = 0xff3465a4
        DoubleQuotedString = 0xff3465a4
        Operator = 0xff3465a4
    
    class CSharp:
        CommentDocKeywordError = 0xff3465a4
        InactiveRegex = 0xff3465a4
        InactivePreProcessorComment = 0xff3465a4
        UUID = 0xff3465a4
        InactiveVerbatimString = 0xff3465a4
        SingleQuotedString = 0xff3465a4
        Operator = 0xff3465a4
        InactiveOperator = 0xff3465a4
        InactivePreProcessor = 0xff3465a4
        UnclosedString = 0xff3465a4
        Identifier = 0xff3465a4
        InactiveRawString = 0xff3465a4
        PreProcessor = 0xff3465a4
        KeywordSet2 = 0xff3465a4
        InactiveUnclosedString = 0xff3465a4
        InactiveCommentLine = 0xff3465a4
        InactiveNumber = 0xff3465a4
        InactivePreProcessorCommentLineDoc = 0xff3465a4
        Number = 0xff3465a4
        InactiveUUID = 0xff3465a4
        CommentDoc = 0xff3465a4
        InactiveCommentDoc = 0xff3465a4
        GlobalClass = 0xff3465a4
        InactiveSingleQuotedString = 0xff3465a4
        HashQuotedString = 0xff3465a4
        VerbatimString = 0xffe0ffe0
        InactiveHashQuotedString = 0xff3465a4
        Regex = 0xff3465a4
        InactiveGlobalClass = 0xff3465a4
        InactiveIdentifier = 0xff3465a4
        CommentLineDoc = 0xff3465a4
        TripleQuotedVerbatimString = 0xff3465a4
        InactiveKeywordSet2 = 0xff3465a4
        InactiveCommentDocKeyword = 0xff3465a4
        Keyword = 0xff3465a4
        InactiveCommentLineDoc = 0xff3465a4
        InactiveDefault = 0xff3465a4
        InactiveCommentDocKeywordError = 0xff3465a4
        InactiveTripleQuotedVerbatimString = 0xff3465a4
        CommentDocKeyword = 0xff3465a4
        InactiveDoubleQuotedString = 0xff3465a4
        CommentLine = 0xff3465a4
        Comment = 0xff3465a4
        PreProcessorComment = 0xff3465a4
        InactiveComment = 0xff3465a4
        RawString = 0xff3465a4
        Default = 0xff3465a4
        PreProcessorCommentLineDoc = 0xff3465a4
        DoubleQuotedString = 0xff3465a4
        InactiveKeyword = 0xff3465a4
    
    class CoffeeScript:
        UUID = 0xff3465a4
        CommentDocKeywordError = 0xff3465a4
        GlobalClass = 0xff3465a4
        VerbatimString = 0xffe0ffe0
        SingleQuotedString = 0xff3465a4
        Operator = 0xff3465a4
        Number = 0xff3465a4
        Identifier = 0xff3465a4
        Keyword = 0xff3465a4
        UnclosedString = 0xffe0c0e0
        Regex = 0xffe0f0e0
        CommentDocKeyword = 0xff3465a4
        BlockRegex = 0xff3465a4
        CommentLineDoc = 0xff3465a4
        PreProcessor = 0xff3465a4
        CommentLine = 0xff3465a4
        CommentBlock = 0xff3465a4
        Comment = 0xff3465a4
        KeywordSet2 = 0xff3465a4
        BlockRegexComment = 0xff3465a4
        Default = 0xff3465a4
        DoubleQuotedString = 0xff3465a4
        CommentDoc = 0xff3465a4
    
    class D:
        BackquoteString = 0xff3465a4
        CommentDocKeywordError = 0xff3465a4
        Operator = 0xff3465a4
        CommentNested = 0xff3465a4
        KeywordDoc = 0xff3465a4
        KeywordSet7 = 0xff3465a4
        Keyword = 0xff3465a4
        KeywordSecondary = 0xff3465a4
        Identifier = 0xff3465a4
        KeywordSet5 = 0xff3465a4
        CommentDocKeyword = 0xff3465a4
        KeywordSet6 = 0xff3465a4
        CommentLineDoc = 0xff3465a4
        CommentLine = 0xff3465a4
        Comment = 0xff3465a4
        Typedefs = 0xff3465a4
        Character = 0xff3465a4
        RawString = 0xff3465a4
        Default = 0xff3465a4
        Number = 0xff3465a4
        UnclosedString = 0xffe0c0e0
        String = 0xff3465a4
        CommentDoc = 0xff3465a4
    
    class Diff:
        Header = 0xff3465a4
        LineChanged = 0xff3465a4
        Default = 0xff3465a4
        LineRemoved = 0xff3465a4
        Command = 0xff3465a4
        Position = 0xff3465a4
        LineAdded = 0xff3465a4
        Comment = 0xff3465a4
    
    class Fortran:
        Label = 0xff3465a4
        Identifier = 0xff3465a4
        DottedOperator = 0xff3465a4
        PreProcessor = 0xff3465a4
        Comment = 0xff3465a4
        SingleQuotedString = 0xff3465a4
        Default = 0xff3465a4
        DoubleQuotedString = 0xff3465a4
        ExtendedFunction = 0xff3465a4
        UnclosedString = 0xffe0c0e0
        Number = 0xff3465a4
        Continuation = 0xfff0e080
        IntrinsicFunction = 0xff3465a4
        Keyword = 0xff3465a4
        Operator = 0xff3465a4
    
    class Fortran77:
        Label = 0xff3465a4
        Identifier = 0xff3465a4
        DottedOperator = 0xff3465a4
        PreProcessor = 0xff3465a4
        Comment = 0xff3465a4
        SingleQuotedString = 0xff3465a4
        Default = 0xff3465a4
        DoubleQuotedString = 0xff3465a4
        ExtendedFunction = 0xff3465a4
        UnclosedString = 0xffe0c0e0
        Number = 0xff3465a4
        Continuation = 0xfff0e080
        IntrinsicFunction = 0xff3465a4
        Keyword = 0xff3465a4
        Operator = 0xff3465a4
    
    class HTML:
        HTMLValue = 0xffffefff
        PythonDefault = 0xffefffef
        Entity = 0xff3465a4
        SGMLParameter = 0xffefefff
        SGMLDefault = 0xffefefff
        PHPVariable = 0xfffff8f8
        SGMLCommand = 0xffefefff
        PythonClassName = 0xffefffef
        VBScriptUnclosedString = 0xff7f7fff
        ASPJavaScriptDefault = 0xffdfdf7f
        ASPVBScriptStart = 0xff3465a4
        VBScriptDefault = 0xffefefff
        PythonNumber = 0xffefffef
        PythonOperator = 0xffefffef
        ASPJavaScriptSingleQuotedString = 0xffdfdf7f
        PHPDefault = 0xfffff8f8
        XMLStart = 0xff3465a4
        PythonFunctionMethodName = 0xffefffef
        ASPJavaScriptStart = 0xff3465a4
        JavaScriptWord = 0xfff0f0ff
        PHPSingleQuotedString = 0xfffff8f8
        PythonTripleDoubleQuotedString = 0xffefffef
        JavaScriptComment = 0xfff0f0ff
        Default = 0xff3465a4
        SGMLSingleQuotedString = 0xffefefff
        VBScriptComment = 0xffefefff
        ASPVBScriptNumber = 0xffcfcfef
        ASPJavaScriptCommentDoc = 0xffdfdf7f
        PythonIdentifier = 0xffefffef
        VBScriptKeyword = 0xffefefff
        JavaScriptDefault = 0xfff0f0ff
        PythonStart = 0xff3465a4
        ASPPythonComment = 0xffcfefcf
        ASPJavaScriptWord = 0xffdfdf7f
        SGMLParameterComment = 0xff3465a4
        JavaScriptSingleQuotedString = 0xfff0f0ff
        PythonSingleQuotedString = 0xffefffef
        HTMLSingleQuotedString = 0xff3465a4
        ASPVBScriptString = 0xffcfcfef
        SGMLBlockDefault = 0xffcccce0
        PythonKeyword = 0xffefffef
        XMLTagEnd = 0xff3465a4
        ASPVBScriptComment = 0xffcfcfef
        ASPPythonSingleQuotedString = 0xffcfefcf
        PHPDoubleQuotedVariable = 0xfffff8f8
        ASPJavaScriptComment = 0xffdfdf7f
        JavaScriptUnclosedString = 0xffbfbbb0
        JavaScriptDoubleQuotedString = 0xfff0f0ff
        UnknownAttribute = 0xff3465a4
        ASPPythonOperator = 0xffcfefcf
        ASPJavaScriptSymbol = 0xffdfdf7f
        ASPPythonFunctionMethodName = 0xffcfefcf
        SGMLDoubleQuotedString = 0xffefefff
        PHPOperator = 0xfffff8f8
        JavaScriptNumber = 0xfff0f0ff
        PythonDoubleQuotedString = 0xffefffef
        ASPAtStart = 0xffffff00
        Script = 0xff3465a4
        PHPCommentLine = 0xfffff8f8
        SGMLComment = 0xffefefff
        JavaScriptStart = 0xff3465a4
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
        OtherInTag = 0xff3465a4
        JavaScriptCommentDoc = 0xfff0f0ff
        Tag = 0xff3465a4
        XMLEnd = 0xff3465a4
        CDATA = 0xffffdf00
        HTMLNumber = 0xff3465a4
        SGMLError = 0xffff6666
        PHPKeyword = 0xfffff8f8
        ASPVBScriptUnclosedString = 0xff7f7fff
        ASPPythonNumber = 0xffcfefcf
        VBScriptString = 0xffefefff
        ASPPythonClassName = 0xffcfefcf
        ASPPythonStart = 0xff3465a4
        JavaScriptRegex = 0xffffbbb0
        ASPJavaScriptUnclosedString = 0xffbfbbb0
        ASPJavaScriptCommentLine = 0xffdfdf7f
        SGMLEntity = 0xffefefff
        ASPJavaScriptDoubleQuotedString = 0xffdfdf7f
        ASPStart = 0xffffdf00
        Attribute = 0xff3465a4
        ASPJavaScriptKeyword = 0xffdfdf7f
        ASPVBScriptDefault = 0xffcfcfef
        ASPVBScriptIdentifier = 0xffcfcfef
        ASPJavaScriptRegex = 0xffffbbb0
        VBScriptNumber = 0xffefefff
        HTMLDoubleQuotedString = 0xff3465a4
        ASPXCComment = 0xff3465a4
        VBScriptStart = 0xff3465a4
        PHPDoubleQuotedString = 0xfffff8f8
        PHPComment = 0xfffff8f8
        ASPPythonTripleSingleQuotedString = 0xffcfefcf
        ASPPythonDoubleQuotedString = 0xffcfefcf
        JavaScriptKeyword = 0xfff0f0ff
        JavaScriptSymbol = 0xfff0f0ff
        VBScriptIdentifier = 0xffefefff
        HTMLComment = 0xff3465a4
        UnknownTag = 0xff3465a4
        JavaScriptCommentLine = 0xfff0f0ff
        PythonComment = 0xffefffef
    
    class IDL:
        CommentDocKeywordError = 0xff3465a4
        InactiveRegex = 0xffe0f0e0
        InactivePreProcessorComment = 0xff3465a4
        UUID = 0xff3465a4
        InactiveVerbatimString = 0xffe0ffe0
        SingleQuotedString = 0xff3465a4
        Operator = 0xff3465a4
        InactiveOperator = 0xff3465a4
        InactivePreProcessor = 0xff3465a4
        UnclosedString = 0xffe0c0e0
        Identifier = 0xff3465a4
        InactiveRawString = 0xff3465a4
        PreProcessor = 0xff3465a4
        KeywordSet2 = 0xff3465a4
        InactiveUnclosedString = 0xffe0c0e0
        InactiveCommentLine = 0xff3465a4
        InactiveNumber = 0xff3465a4
        InactivePreProcessorCommentLineDoc = 0xff3465a4
        Number = 0xff3465a4
        InactiveUUID = 0xff3465a4
        CommentDoc = 0xff3465a4
        InactiveCommentDoc = 0xff3465a4
        GlobalClass = 0xff3465a4
        InactiveSingleQuotedString = 0xff3465a4
        HashQuotedString = 0xffe7ffd7
        VerbatimString = 0xffe0ffe0
        InactiveHashQuotedString = 0xff3465a4
        Regex = 0xffe0f0e0
        InactiveGlobalClass = 0xff3465a4
        InactiveIdentifier = 0xff3465a4
        CommentLineDoc = 0xff3465a4
        TripleQuotedVerbatimString = 0xffe0ffe0
        InactiveKeywordSet2 = 0xff3465a4
        InactiveCommentDocKeyword = 0xff3465a4
        Keyword = 0xff3465a4
        InactiveCommentLineDoc = 0xff3465a4
        InactiveDefault = 0xff3465a4
        InactiveCommentDocKeywordError = 0xff3465a4
        InactiveTripleQuotedVerbatimString = 0xff3465a4
        CommentDocKeyword = 0xff3465a4
        InactiveDoubleQuotedString = 0xff3465a4
        CommentLine = 0xff3465a4
        Comment = 0xff3465a4
        PreProcessorComment = 0xff3465a4
        InactiveComment = 0xff3465a4
        RawString = 0xfffff3ff
        Default = 0xff3465a4
        PreProcessorCommentLineDoc = 0xff3465a4
        DoubleQuotedString = 0xff3465a4
        InactiveKeyword = 0xff3465a4
    
    class Java:
        CommentDocKeywordError = 0xff3465a4
        InactiveRegex = 0xffe0f0e0
        InactivePreProcessorComment = 0xff3465a4
        UUID = 0xff3465a4
        InactiveVerbatimString = 0xffe0ffe0
        SingleQuotedString = 0xff3465a4
        Operator = 0xff3465a4
        InactiveOperator = 0xff3465a4
        InactivePreProcessor = 0xff3465a4
        UnclosedString = 0xffe0c0e0
        Identifier = 0xff3465a4
        InactiveRawString = 0xff3465a4
        PreProcessor = 0xff3465a4
        KeywordSet2 = 0xff3465a4
        InactiveUnclosedString = 0xffe0c0e0
        InactiveCommentLine = 0xff3465a4
        InactiveNumber = 0xff3465a4
        InactivePreProcessorCommentLineDoc = 0xff3465a4
        Number = 0xff3465a4
        InactiveUUID = 0xff3465a4
        CommentDoc = 0xff3465a4
        InactiveCommentDoc = 0xff3465a4
        GlobalClass = 0xff3465a4
        InactiveSingleQuotedString = 0xff3465a4
        HashQuotedString = 0xffe7ffd7
        VerbatimString = 0xffe0ffe0
        InactiveHashQuotedString = 0xff3465a4
        Regex = 0xffe0f0e0
        InactiveGlobalClass = 0xff3465a4
        InactiveIdentifier = 0xff3465a4
        CommentLineDoc = 0xff3465a4
        TripleQuotedVerbatimString = 0xffe0ffe0
        InactiveKeywordSet2 = 0xff3465a4
        InactiveCommentDocKeyword = 0xff3465a4
        Keyword = 0xff3465a4
        InactiveCommentLineDoc = 0xff3465a4
        InactiveDefault = 0xff3465a4
        InactiveCommentDocKeywordError = 0xff3465a4
        InactiveTripleQuotedVerbatimString = 0xff3465a4
        CommentDocKeyword = 0xff3465a4
        InactiveDoubleQuotedString = 0xff3465a4
        CommentLine = 0xff3465a4
        Comment = 0xff3465a4
        PreProcessorComment = 0xff3465a4
        InactiveComment = 0xff3465a4
        RawString = 0xfffff3ff
        Default = 0xff3465a4
        PreProcessorCommentLineDoc = 0xff3465a4
        DoubleQuotedString = 0xff3465a4
        InactiveKeyword = 0xff3465a4
    
    class JavaScript:
        CommentDocKeywordError = 0xff3465a4
        InactiveRegex = 0xff3465a4
        InactivePreProcessorComment = 0xff3465a4
        UUID = 0xff3465a4
        InactiveVerbatimString = 0xff3465a4
        SingleQuotedString = 0xff3465a4
        Operator = 0xff3465a4
        InactiveOperator = 0xff3465a4
        InactivePreProcessor = 0xff3465a4
        UnclosedString = 0xff3465a4
        Identifier = 0xff3465a4
        InactiveRawString = 0xff3465a4
        PreProcessor = 0xff3465a4
        KeywordSet2 = 0xff3465a4
        InactiveUnclosedString = 0xff3465a4
        InactiveCommentLine = 0xff3465a4
        InactiveNumber = 0xff3465a4
        InactivePreProcessorCommentLineDoc = 0xff3465a4
        Number = 0xff3465a4
        InactiveUUID = 0xff3465a4
        CommentDoc = 0xff3465a4
        InactiveCommentDoc = 0xff3465a4
        GlobalClass = 0xff3465a4
        InactiveSingleQuotedString = 0xff3465a4
        HashQuotedString = 0xff3465a4
        VerbatimString = 0xff3465a4
        InactiveHashQuotedString = 0xff3465a4
        Regex = 0xffe0f0ff
        InactiveGlobalClass = 0xff3465a4
        InactiveIdentifier = 0xff3465a4
        CommentLineDoc = 0xff3465a4
        TripleQuotedVerbatimString = 0xff3465a4
        InactiveKeywordSet2 = 0xff3465a4
        InactiveCommentDocKeyword = 0xff3465a4
        Keyword = 0xff3465a4
        InactiveCommentLineDoc = 0xff3465a4
        InactiveDefault = 0xff3465a4
        InactiveCommentDocKeywordError = 0xff3465a4
        InactiveTripleQuotedVerbatimString = 0xff3465a4
        CommentDocKeyword = 0xff3465a4
        InactiveDoubleQuotedString = 0xff3465a4
        CommentLine = 0xff3465a4
        Comment = 0xff3465a4
        PreProcessorComment = 0xff3465a4
        InactiveComment = 0xff3465a4
        RawString = 0xff3465a4
        Default = 0xff3465a4
        PreProcessorCommentLineDoc = 0xff3465a4
        DoubleQuotedString = 0xff3465a4
        InactiveKeyword = 0xff3465a4
    
    class Lua:
        Label = 0xff3465a4
        Identifier = 0xff3465a4
        StringTableMathsFunctions = 0xffd0d0ff
        CoroutinesIOSystemFacilities = 0xffffd0d0
        KeywordSet5 = 0xff3465a4
        KeywordSet6 = 0xff3465a4
        Preprocessor = 0xff3465a4
        LineComment = 0xff3465a4
        Comment = 0xffd0f0f0
        String = 0xff3465a4
        Character = 0xff3465a4
        Default = 0xff3465a4
        Operator = 0xff3465a4
        LiteralString = 0xffe0ffff
        Number = 0xff3465a4
        KeywordSet8 = 0xff3465a4
        KeywordSet7 = 0xff3465a4
        BasicFunctions = 0xffd0ffd0
        Keyword = 0xff3465a4
        UnclosedString = 0xffe0c0e0
    
    class Makefile:
        Default = 0xff3465a4
        Operator = 0xff3465a4
        Target = 0xff3465a4
        Preprocessor = 0xff3465a4
        Variable = 0xff3465a4
        Comment = 0xff3465a4
        Error = 0xffff0000
    
    class Matlab:
        SingleQuotedString = 0xff3465a4
        Default = 0xff3465a4
        Keyword = 0xff3465a4
        Number = 0xff3465a4
        Command = 0xff3465a4
        Identifier = 0xff3465a4
        Comment = 0xff3465a4
        DoubleQuotedString = 0xff3465a4
        Operator = 0xff3465a4
    
    class Octave:
        SingleQuotedString = 0xff3465a4
        Default = 0xff3465a4
        Keyword = 0xff3465a4
        Number = 0xff3465a4
        Command = 0xff3465a4
        Identifier = 0xff3465a4
        Comment = 0xff3465a4
        DoubleQuotedString = 0xff3465a4
        Operator = 0xff3465a4
    
    class PO:
        ProgrammerComment = 0xff3465a4
        Flags = 0xff3465a4
        MessageContextText = 0xff3465a4
        MessageStringTextEOL = 0xff3465a4
        MessageId = 0xff3465a4
        MessageIdText = 0xff3465a4
        Reference = 0xff3465a4
        Comment = 0xff3465a4
        MessageStringText = 0xff3465a4
        MessageContext = 0xff3465a4
        Fuzzy = 0xff3465a4
        Default = 0xff3465a4
        MessageString = 0xff3465a4
        MessageContextTextEOL = 0xff3465a4
        MessageIdTextEOL = 0xff3465a4
    
    class POV:
        KeywordSet7 = 0xffd0d0d0
        KeywordSet6 = 0xffd0ffd0
        PredefinedFunctions = 0xffd0d0ff
        CommentLine = 0xff3465a4
        PredefinedIdentifiers = 0xff3465a4
        Comment = 0xff3465a4
        Directive = 0xff3465a4
        String = 0xff3465a4
        BadDirective = 0xff3465a4
        TypesModifiersItems = 0xffffffd0
        Default = 0xff3465a4
        Operator = 0xff3465a4
        Number = 0xff3465a4
        KeywordSet8 = 0xffe0e0e0
        Identifier = 0xff3465a4
        ObjectsCSGAppearance = 0xffffd0d0
        UnclosedString = 0xffe0c0e0
    
    class Pascal:
        PreProcessorParenthesis = 0xff3465a4
        SingleQuotedString = 0xff3465a4
        PreProcessor = 0xff3465a4
        CommentLine = 0xff3465a4
        Comment = 0xff3465a4
        CommentParenthesis = 0xff3465a4
        Asm = 0xff3465a4
        Character = 0xff3465a4
        Default = 0xff3465a4
        Operator = 0xff3465a4
        UnclosedString = 0xffe0c0e0
        Number = 0xff3465a4
        Identifier = 0xff3465a4
        Keyword = 0xff3465a4
        HexNumber = 0xff3465a4
    
    class Perl:
        Translation = 0xfff0e080
        BacktickHereDocument = 0xffddd0dd
        Array = 0xffffffe0
        QuotedStringQXVar = 0xffa08080
        PODVerbatim = 0xffc0ffc0
        DoubleQuotedStringVar = 0xff3465a4
        Regex = 0xffa0ffa0
        HereDocumentDelimiter = 0xffddd0dd
        SubroutinePrototype = 0xff3465a4
        BacktickHereDocumentVar = 0xffddd0dd
        QuotedStringQR = 0xff3465a4
        SingleQuotedString = 0xff3465a4
        QuotedStringQRVar = 0xff3465a4
        SubstitutionVar = 0xff3465a4
        Operator = 0xff3465a4
        DoubleQuotedHereDocumentVar = 0xffddd0dd
        Identifier = 0xff3465a4
        QuotedStringQX = 0xff3465a4
        BackticksVar = 0xffa08080
        Keyword = 0xff3465a4
        QuotedStringQ = 0xff3465a4
        QuotedStringQQVar = 0xff3465a4
        QuotedStringQQ = 0xff3465a4
        POD = 0xffe0ffe0
        FormatIdentifier = 0xff3465a4
        RegexVar = 0xff3465a4
        Backticks = 0xffa08080
        DoubleQuotedHereDocument = 0xffddd0dd
        Scalar = 0xffffe0e0
        FormatBody = 0xfffff0ff
        Comment = 0xff3465a4
        QuotedStringQW = 0xff3465a4
        SymbolTable = 0xffe0e0e0
        Default = 0xff3465a4
        Error = 0xffff0000
        SingleQuotedHereDocument = 0xffddd0dd
        Number = 0xff3465a4
        Hash = 0xffffe0ff
        Substitution = 0xfff0e080
        DataSection = 0xfffff0d8
        DoubleQuotedString = 0xff3465a4
    
    class PostScript:
        DictionaryParenthesis = 0xff3465a4
        HexString = 0xff3465a4
        DSCCommentValue = 0xff3465a4
        ProcedureParenthesis = 0xff3465a4
        Comment = 0xff3465a4
        ImmediateEvalLiteral = 0xff3465a4
        Name = 0xff3465a4
        DSCComment = 0xff3465a4
        Default = 0xff3465a4
        Base85String = 0xff3465a4
        Number = 0xff3465a4
        ArrayParenthesis = 0xff3465a4
        Literal = 0xff3465a4
        BadStringCharacter = 0xffff0000
        Text = 0xff3465a4
        Keyword = 0xff3465a4
    
    class Properties:
        DefaultValue = 0xff3465a4
        Default = 0xff3465a4
        Section = 0xffe0f0f0
        Assignment = 0xff3465a4
        Key = 0xff3465a4
        Comment = 0xff3465a4
    
    class Python:
        TripleDoubleQuotedString = 0xff3465a4
        FunctionMethodName = 0xff3465a4
        TabsAfterSpaces = 0xff3465a4
        Tabs = 0xff3465a4
        Decorator = 0xff3465a4
        NoWarning = 0xff3465a4
        UnclosedString = 0xffe0c0e0
        Spaces = 0xff3465a4
        CommentBlock = 0xff3465a4
        Comment = 0xff3465a4
        TripleSingleQuotedString = 0xff3465a4
        SingleQuotedString = 0xff3465a4
        Inconsistent = 0xff3465a4
        Default = 0xff3465a4
        DoubleQuotedString = 0xff3465a4
        Operator = 0xff3465a4
        Number = 0xff3465a4
        Identifier = 0xff3465a4
        ClassName = 0xff3465a4
        Keyword = 0xff3465a4
        HighlightedIdentifier = 0xff3465a4
    
    class Ruby:
        Symbol = 0xff3465a4
        Stderr = 0xffff8080
        Global = 0xff3465a4
        FunctionMethodName = 0xff3465a4
        Stdin = 0xffff8080
        HereDocumentDelimiter = 0xffddd0dd
        PercentStringr = 0xffa0ffa0
        PercentStringQ = 0xff3465a4
        ModuleName = 0xff3465a4
        HereDocument = 0xffddd0dd
        SingleQuotedString = 0xff3465a4
        PercentStringq = 0xff3465a4
        Regex = 0xffa0ffa0
        Operator = 0xff3465a4
        PercentStringw = 0xffffffe0
        PercentStringx = 0xffa08080
        POD = 0xffc0ffc0
        Keyword = 0xff3465a4
        Stdout = 0xffff8080
        ClassVariable = 0xff3465a4
        Identifier = 0xff3465a4
        DemotedKeyword = 0xff3465a4
        Backticks = 0xffa08080
        InstanceVariable = 0xff3465a4
        Comment = 0xff3465a4
        Default = 0xff3465a4
        Error = 0xffff0000
        Number = 0xff3465a4
        DataSection = 0xfffff0d8
        ClassName = 0xff3465a4
        DoubleQuotedString = 0xff3465a4
    
    class SQL:
        PlusComment = 0xff3465a4
        KeywordSet7 = 0xff3465a4
        PlusPrompt = 0xffe0ffe0
        CommentDocKeywordError = 0xff3465a4
        CommentDocKeyword = 0xff3465a4
        KeywordSet6 = 0xff3465a4
        CommentLine = 0xff3465a4
        Comment = 0xff3465a4
        Operator = 0xff3465a4
        QuotedIdentifier = 0xff3465a4
        SingleQuotedString = 0xff3465a4
        PlusKeyword = 0xff3465a4
        Default = 0xff3465a4
        DoubleQuotedString = 0xff3465a4
        CommentLineHash = 0xff3465a4
        KeywordSet5 = 0xff3465a4
        Number = 0xff3465a4
        KeywordSet8 = 0xff3465a4
        Identifier = 0xff3465a4
        Keyword = 0xff3465a4
        CommentDoc = 0xff3465a4
    
    class Spice:
        Function = 0xff3465a4
        Delimiter = 0xff3465a4
        Value = 0xff3465a4
        Default = 0xff3465a4
        Number = 0xff3465a4
        Parameter = 0xff3465a4
        Command = 0xff3465a4
        Identifier = 0xff3465a4
        Comment = 0xff3465a4
    
    class TCL:
        SubstitutionBrace = 0xff3465a4
        CommentBox = 0xfff0fff0
        ITCLKeyword = 0xfffff0f0
        TkKeyword = 0xffe0fff0
        Operator = 0xff3465a4
        QuotedString = 0xfffff0f0
        ExpandKeyword = 0xffffff80
        KeywordSet7 = 0xff3465a4
        TCLKeyword = 0xff3465a4
        TkCommand = 0xffffd0d0
        Identifier = 0xff3465a4
        KeywordSet6 = 0xff3465a4
        CommentLine = 0xff3465a4
        CommentBlock = 0xfff0fff0
        Comment = 0xfff0ffe0
        Default = 0xff3465a4
        KeywordSet9 = 0xff3465a4
        Modifier = 0xff3465a4
        Number = 0xff3465a4
        KeywordSet8 = 0xff3465a4
        Substitution = 0xffeffff0
        QuotedKeyword = 0xfffff0f0
    
    class TeX:
        Symbol = 0xff3465a4
        Default = 0xff3465a4
        Command = 0xff3465a4
        Group = 0xff3465a4
        Text = 0xff3465a4
        Special = 0xff3465a4
    
    class VHDL:
        StandardOperator = 0xff3465a4
        Attribute = 0xff3465a4
        CommentLine = 0xff3465a4
        Comment = 0xff3465a4
        String = 0xff3465a4
        Default = 0xff3465a4
        Operator = 0xff3465a4
        StandardPackage = 0xff3465a4
        Number = 0xff3465a4
        Identifier = 0xff3465a4
        KeywordSet7 = 0xff3465a4
        StandardFunction = 0xff3465a4
        StandardType = 0xff3465a4
        Keyword = 0xff3465a4
        UnclosedString = 0xffe0c0e0
    
    class Verilog:
        CommentBang = 0xffe0f0ff
        UserKeywordSet = 0xff3465a4
        Preprocessor = 0xff3465a4
        CommentLine = 0xff3465a4
        Comment = 0xff3465a4
        KeywordSet2 = 0xff3465a4
        Default = 0xff3465a4
        Operator = 0xff3465a4
        Number = 0xff3465a4
        Identifier = 0xff3465a4
        SystemTask = 0xff3465a4
        String = 0xff3465a4
        Keyword = 0xff3465a4
        UnclosedString = 0xffe0c0e0
    
    class XML:
        HTMLValue = 0xffffefff
        PythonDefault = 0xffefffef
        Entity = 0xff3465a4
        SGMLParameter = 0xffefefff
        SGMLDefault = 0xffefefff
        PHPVariable = 0xfffff8f8
        SGMLCommand = 0xffefefff
        PythonClassName = 0xffefffef
        VBScriptUnclosedString = 0xff7f7fff
        ASPJavaScriptDefault = 0xffdfdf7f
        ASPVBScriptStart = 0xff3465a4
        VBScriptDefault = 0xffefefff
        PythonNumber = 0xffefffef
        PythonOperator = 0xffefffef
        ASPJavaScriptSingleQuotedString = 0xffdfdf7f
        PHPDefault = 0xfffff8f8
        XMLStart = 0xff3465a4
        PythonFunctionMethodName = 0xffefffef
        ASPJavaScriptStart = 0xff3465a4
        JavaScriptWord = 0xfff0f0ff
        PHPSingleQuotedString = 0xfffff8f8
        PythonTripleDoubleQuotedString = 0xffefffef
        JavaScriptComment = 0xfff0f0ff
        Default = 0xff3465a4
        SGMLSingleQuotedString = 0xffefefff
        VBScriptComment = 0xffefefff
        ASPVBScriptNumber = 0xffcfcfef
        ASPJavaScriptCommentDoc = 0xffdfdf7f
        PythonIdentifier = 0xffefffef
        VBScriptKeyword = 0xffefefff
        JavaScriptDefault = 0xfff0f0ff
        PythonStart = 0xff3465a4
        ASPPythonComment = 0xffcfefcf
        ASPJavaScriptWord = 0xffdfdf7f
        SGMLParameterComment = 0xff3465a4
        JavaScriptSingleQuotedString = 0xfff0f0ff
        PythonSingleQuotedString = 0xffefffef
        HTMLSingleQuotedString = 0xff3465a4
        ASPVBScriptString = 0xffcfcfef
        SGMLBlockDefault = 0xffcccce0
        PythonKeyword = 0xffefffef
        XMLTagEnd = 0xff3465a4
        ASPVBScriptComment = 0xffcfcfef
        ASPPythonSingleQuotedString = 0xffcfefcf
        PHPDoubleQuotedVariable = 0xfffff8f8
        ASPJavaScriptComment = 0xffdfdf7f
        JavaScriptUnclosedString = 0xffbfbbb0
        JavaScriptDoubleQuotedString = 0xfff0f0ff
        UnknownAttribute = 0xff3465a4
        ASPPythonOperator = 0xffcfefcf
        ASPJavaScriptSymbol = 0xffdfdf7f
        ASPPythonFunctionMethodName = 0xffcfefcf
        SGMLDoubleQuotedString = 0xffefefff
        PHPOperator = 0xfffff8f8
        JavaScriptNumber = 0xfff0f0ff
        PythonDoubleQuotedString = 0xffefffef
        ASPAtStart = 0xffffff00
        Script = 0xff3465a4
        PHPCommentLine = 0xfffff8f8
        SGMLComment = 0xffefefff
        JavaScriptStart = 0xff3465a4
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
        OtherInTag = 0xff3465a4
        JavaScriptCommentDoc = 0xfff0f0ff
        Tag = 0xff3465a4
        XMLEnd = 0xff3465a4
        CDATA = 0xfffff0f0
        HTMLNumber = 0xff3465a4
        SGMLError = 0xffff6666
        PHPKeyword = 0xfffff8f8
        ASPVBScriptUnclosedString = 0xff7f7fff
        ASPPythonNumber = 0xffcfefcf
        VBScriptString = 0xffefefff
        ASPPythonClassName = 0xffcfefcf
        ASPPythonStart = 0xff3465a4
        JavaScriptRegex = 0xffffbbb0
        ASPJavaScriptUnclosedString = 0xffbfbbb0
        ASPJavaScriptCommentLine = 0xffdfdf7f
        SGMLEntity = 0xffefefff
        ASPJavaScriptDoubleQuotedString = 0xffdfdf7f
        ASPStart = 0xffffdf00
        Attribute = 0xff3465a4
        ASPJavaScriptKeyword = 0xffdfdf7f
        ASPVBScriptDefault = 0xffcfcfef
        ASPVBScriptIdentifier = 0xffcfcfef
        ASPJavaScriptRegex = 0xffffbbb0
        VBScriptNumber = 0xffefefff
        HTMLDoubleQuotedString = 0xff3465a4
        ASPXCComment = 0xff3465a4
        VBScriptStart = 0xff3465a4
        PHPDoubleQuotedString = 0xfffff8f8
        PHPComment = 0xfffff8f8
        ASPPythonTripleSingleQuotedString = 0xffcfefcf
        ASPPythonDoubleQuotedString = 0xffcfefcf
        JavaScriptKeyword = 0xfff0f0ff
        JavaScriptSymbol = 0xfff0f0ff
        VBScriptIdentifier = 0xffefefff
        HTMLComment = 0xff3465a4
        UnknownTag = 0xff3465a4
        JavaScriptCommentLine = 0xfff0f0ff
        PythonComment = 0xffefffef
    
    class YAML:
        TextBlockMarker = 0xff3465a4
        DocumentDelimiter = 0xfff3c969
        Operator = 0xff3465a4
        Number = 0xff3465a4
        Default = 0xff3465a4
        Identifier = 0xff3465a4
        Reference = 0xff3465a4
        Comment = 0xff3465a4
        Keyword = 0xff3465a4
        SyntaxErrorMarker = 0xffff0000
    




