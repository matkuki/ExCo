
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
##      Earth theme

import PyQt4.QtGui


Form = "#585a55"
Cursor = PyQt4.QtGui.QColor(0xff, 0xff, 0xff)


class FoldMargin:
    ForeGround = PyQt4.QtGui.QColor(0xffffffff)
    BackGround = PyQt4.QtGui.QColor(0xff2e3436)


class LineMargin:
    ForeGround = PyQt4.QtGui.QColor(0xffffffff)
    BackGround = PyQt4.QtGui.QColor(0xff2e3436)


class Indication:
    Font = "#e6e6e6"
    ActiveBackGround = "#1a0f0b"
    ActiveBorder = "#e6e6e6"
    PassiveBackGround = "#585a55"
    PassiveBorder = "#b3935c"

    
class Font:
    Default = PyQt4.QtGui.QColor(0xfff7f1c1)
    
    class Ada:
        Default = (0xfff7f1c1, None)
        Comment = (0xff679d47, None)
        Keyword = (0xff519872, None)
        String = (0xff7ca563, None)
        Procedure = (0xffb3935c, None)
        Number = (0xff6c9686, None)
        Type = (0xff519872, None)
        Package = (0xffe1aa7d, None)
    
    class Nim:
        Default = (0xfff7f1c1, None)
        Comment = (0xff679d47, False)
        BasicKeyword = (0xff519872, True)
        TopKeyword = (0xff407fc0, True)
        String = (0xff7ca563, None)
        LongString = (0xffe1aa7d, None)
        Number = (0xff6c9686, None)
        Operator = (0xff7f7f7f, None)
        Unsafe = (0xffc00000, True)
        Type = (0xff6e6e00, True)
        DocumentationComment = (0xff7f0a0a, None)
        Definition = (0xff6c9686, None)
        Class = (0xffb3935c, None)
        KeywordOperator = (0xff963cc8, None)
        CharLiteral = (0xff00c8ff, None)
        CaseOf = (0xff8000ff, None)
        UserKeyword = (0xffff8040, None)
        MultilineComment = (0xff006c6c, None)
        MultilineDocumentation = (0xff6e3296, None)
        Pragma = (0xffc07f40, None)
    
    class Oberon:
        Default = (0xfff7f1c1, None)
        Comment = (0xff679d47, None)
        Keyword = (0xff519872, None)
        String = (0xff7ca563, None)
        Procedure = (0xffb3935c, None)
        Module = (0xffe1aa7d, None)
        Number = (0xff6c9686, None)
        Type = (0xff519872, None)
    
    
    class AVS:
        BlockComment = (0xff679d47, None)
        ClipProperty = (0xff519872, None)
        Default = (0xfff7f1c1, None)
        Filter = (0xff519872, None)
        Function = (0xff6c9686, None)
        Identifier = (0xfff7f1c1, None)
        Keyword = (0xff519872, None)
        KeywordSet6 = (0xff8000ff, None)
        LineComment = (0xff679d47, None)
        NestedBlockComment = (0xff679d47, None)
        Number = (0xff6c9686, None)
        Operator = (0xfff7f1c1, None)
        Plugin = (0xff0080c0, None)
        String = (0xff7ca563, None)
        TripleString = (0xff7ca563, None)
    
    class Bash:
        Backticks = (0xffffff00, None)
        Comment = (0xff679d47, None)
        Default = (0xff808080, None)
        DoubleQuotedString = (0xff7ca563, None)
        Error = (0xffffff00, None)
        HereDocumentDelimiter = (0xfff7f1c1, None)
        Identifier = (0xfff7f1c1, None)
        Keyword = (0xff519872, None)
        Number = (0xff6c9686, None)
        Operator = (0xfff7f1c1, None)
        ParameterExpansion = (0xfff7f1c1, None)
        Scalar = (0xfff7f1c1, None)
        SingleQuotedHereDocument = (0xff7ca563, None)
        SingleQuotedString = (0xff7ca563, None)
    
    class Batch:
        Comment = (0xff679d47, None)
        Default = (0xfff7f1c1, None)
        ExternalCommand = (0xff519872, None)
        HideCommandChar = (0xff7f7f00, None)
        Keyword = (0xff519872, None)
        Label = (0xff7ca563, None)
        Operator = (0xfff7f1c1, None)
        Variable = (0xff800080, None)
    
    class CMake:
        BlockForeach = (0xff519872, None)
        BlockIf = (0xff519872, None)
        BlockMacro = (0xff519872, None)
        BlockWhile = (0xff519872, None)
        Comment = (0xff679d47, None)
        Default = (0xfff7f1c1, None)
        Function = (0xff519872, None)
        KeywordSet3 = (0xfff7f1c1, None)
        Label = (0xffcc3300, None)
        Number = (0xff6c9686, None)
        String = (0xff7ca563, None)
        StringLeftQuote = (0xff7ca563, None)
        StringRightQuote = (0xff7ca563, None)
        StringVariable = (0xffcc3300, None)
        Variable = (0xff800000, None)
    
    class CPP:
        Comment = (0xff679d47, None)
        CommentDoc = (0xff3f703f, None)
        CommentDocKeyword = (0xff3060a0, None)
        CommentDocKeywordError = (0xff804020, None)
        CommentLine = (0xff679d47, None)
        CommentLineDoc = (0xff3f703f, None)
        Default = (0xff808080, None)
        DoubleQuotedString = (0xff7ca563, None)
        GlobalClass = (0xfff7f1c1, None)
        HashQuotedString = (0xff679d47, None)
        Identifier = (0xfff7f1c1, None)
        InactiveComment = (0xff90b090, None)
        InactiveCommentDoc = (0xffd0d0d0, None)
        InactiveCommentDocKeyword = (0xffc0c0c0, None)
        InactiveCommentDocKeywordError = (0xffc0c0c0, None)
        InactiveCommentLine = (0xff90b090, None)
        InactiveCommentLineDoc = (0xffc0c0c0, None)
        InactiveDefault = (0xffc0c0c0, None)
        InactiveDoubleQuotedString = (0xffb090b0, None)
        InactiveGlobalClass = (0xffb0b0b0, None)
        InactiveHashQuotedString = (0xfff7f1c1, None)
        InactiveIdentifier = (0xffb0b0b0, None)
        InactiveKeyword = (0xff9090b0, None)
        InactiveKeywordSet2 = (0xffc0c0c0, None)
        InactiveNumber = (0xff90b090, None)
        InactiveOperator = (0xffb0b0b0, None)
        InactivePreProcessor = (0xffb0b090, None)
        InactivePreProcessorComment = (0xff1a0f0b, None)
        InactivePreProcessorCommentLineDoc = (0xffc0c0c0, None)
        InactiveRawString = (0xfff7f1c1, None)
        InactiveRegex = (0xff7faf7f, None)
        InactiveSingleQuotedString = (0xffb090b0, None)
        InactiveTripleQuotedVerbatimString = (0xfff7f1c1, None)
        InactiveUUID = (0xffc0c0c0, None)
        InactiveUnclosedString = (0xfff7f1c1, None)
        InactiveVerbatimString = (0xff90b090, None)
        Keyword = (0xff519872, None)
        KeywordSet2 = (0xfff7f1c1, None)
        Number = (0xff6c9686, None)
        Operator = (0xfff7f1c1, None)
        PreProcessor = (0xff7f7f00, None)
        PreProcessorComment = (0xff659900, None)
        PreProcessorCommentLineDoc = (0xff3f703f, None)
        RawString = (0xff7ca563, None)
        Regex = (0xff3f7f3f, None)
        SingleQuotedString = (0xff7ca563, None)
        TripleQuotedVerbatimString = (0xff679d47, None)
        UUID = (0xfff7f1c1, None)
        UnclosedString = (0xfff7f1c1, None)
        VerbatimString = (0xff679d47, None)
    
    class CSS:
        AtRule = (0xff7f7f00, None)
        Attribute = (0xff800000, None)
        CSS1Property = (0xff0040e0, None)
        CSS2Property = (0xff00a0e0, None)
        CSS3Property = (0xfff7f1c1, None)
        ClassSelector = (0xfff7f1c1, None)
        Comment = (0xff679d47, None)
        Default = (0xffff0080, None)
        DoubleQuotedString = (0xff7ca563, None)
        ExtendedCSSProperty = (0xfff7f1c1, None)
        ExtendedPseudoClass = (0xfff7f1c1, None)
        ExtendedPseudoElement = (0xfff7f1c1, None)
        IDSelector = (0xff6c9686, None)
        Important = (0xffff8000, None)
        MediaRule = (0xff7f7f00, None)
        Operator = (0xfff7f1c1, None)
        PseudoClass = (0xff800000, None)
        PseudoElement = (0xfff7f1c1, None)
        SingleQuotedString = (0xff7ca563, None)
        Tag = (0xff519872, None)
        UnknownProperty = (0xffff0000, None)
        UnknownPseudoClass = (0xffff0000, None)
        Value = (0xff7ca563, None)
        Variable = (0xfff7f1c1, None)
    
    class CSharp:
        Comment = (0xff679d47, None)
        CommentDoc = (0xff3f703f, None)
        CommentDocKeyword = (0xff3060a0, None)
        CommentDocKeywordError = (0xff804020, None)
        CommentLine = (0xff679d47, None)
        CommentLineDoc = (0xff3f703f, None)
        Default = (0xff808080, None)
        DoubleQuotedString = (0xff7ca563, None)
        GlobalClass = (0xfff7f1c1, None)
        HashQuotedString = (0xff679d47, None)
        Identifier = (0xfff7f1c1, None)
        InactiveComment = (0xff90b090, None)
        InactiveCommentDoc = (0xffd0d0d0, None)
        InactiveCommentDocKeyword = (0xffc0c0c0, None)
        InactiveCommentDocKeywordError = (0xffc0c0c0, None)
        InactiveCommentLine = (0xff90b090, None)
        InactiveCommentLineDoc = (0xffc0c0c0, None)
        InactiveDefault = (0xffc0c0c0, None)
        InactiveDoubleQuotedString = (0xffb090b0, None)
        InactiveGlobalClass = (0xffb0b0b0, None)
        InactiveHashQuotedString = (0xfff7f1c1, None)
        InactiveIdentifier = (0xffb0b0b0, None)
        InactiveKeyword = (0xff9090b0, None)
        InactiveKeywordSet2 = (0xffc0c0c0, None)
        InactiveNumber = (0xff90b090, None)
        InactiveOperator = (0xffb0b0b0, None)
        InactivePreProcessor = (0xffb0b090, None)
        InactivePreProcessorComment = (0xff1a0f0b, None)
        InactivePreProcessorCommentLineDoc = (0xffc0c0c0, None)
        InactiveRawString = (0xfff7f1c1, None)
        InactiveRegex = (0xff7faf7f, None)
        InactiveSingleQuotedString = (0xffb090b0, None)
        InactiveTripleQuotedVerbatimString = (0xfff7f1c1, None)
        InactiveUUID = (0xffc0c0c0, None)
        InactiveUnclosedString = (0xfff7f1c1, None)
        InactiveVerbatimString = (0xff90b090, None)
        Keyword = (0xff519872, None)
        KeywordSet2 = (0xfff7f1c1, None)
        Number = (0xff6c9686, None)
        Operator = (0xfff7f1c1, None)
        PreProcessor = (0xff7f7f00, None)
        PreProcessorComment = (0xff659900, None)
        PreProcessorCommentLineDoc = (0xff3f703f, None)
        RawString = (0xff7ca563, None)
        Regex = (0xff3f7f3f, None)
        SingleQuotedString = (0xff7ca563, None)
        TripleQuotedVerbatimString = (0xff679d47, None)
        UUID = (0xfff7f1c1, None)
        UnclosedString = (0xfff7f1c1, None)
        VerbatimString = (0xff679d47, None)
    
    class CoffeeScript:
        BlockRegex = (0xff3f7f3f, None)
        BlockRegexComment = (0xff679d47, None)
        Comment = (0xff679d47, None)
        CommentBlock = (0xff679d47, None)
        CommentDoc = (0xff3f703f, None)
        CommentDocKeyword = (0xff3060a0, None)
        CommentDocKeywordError = (0xff804020, None)
        CommentLine = (0xff679d47, None)
        CommentLineDoc = (0xff3f703f, None)
        Default = (0xff808080, None)
        DoubleQuotedString = (0xff7ca563, None)
        GlobalClass = (0xfff7f1c1, None)
        Identifier = (0xfff7f1c1, None)
        Keyword = (0xff519872, None)
        KeywordSet2 = (0xfff7f1c1, None)
        Number = (0xff6c9686, None)
        Operator = (0xfff7f1c1, None)
        PreProcessor = (0xff7f7f00, None)
        Regex = (0xff3f7f3f, None)
        SingleQuotedString = (0xff7ca563, None)
        UUID = (0xfff7f1c1, None)
        UnclosedString = (0xfff7f1c1, None)
        VerbatimString = (0xff679d47, None)
    
    class D:
        BackquoteString = (0xfff7f1c1, None)
        Character = (0xff7ca563, None)
        Comment = (0xff679d47, None)
        CommentDoc = (0xff3f703f, None)
        CommentDocKeyword = (0xff3060a0, None)
        CommentDocKeywordError = (0xff804020, None)
        CommentLine = (0xff679d47, None)
        CommentLineDoc = (0xff3f703f, None)
        CommentNested = (0xffa0c0a0, None)
        Default = (0xff808080, None)
        Identifier = (0xfff7f1c1, None)
        Keyword = (0xff519872, None)
        KeywordDoc = (0xff519872, None)
        KeywordSecondary = (0xff519872, None)
        KeywordSet5 = (0xfff7f1c1, None)
        KeywordSet6 = (0xfff7f1c1, None)
        KeywordSet7 = (0xfff7f1c1, None)
        Number = (0xff6c9686, None)
        Operator = (0xfff7f1c1, None)
        RawString = (0xfff7f1c1, None)
        String = (0xff7ca563, None)
        Typedefs = (0xff519872, None)
        UnclosedString = (0xfff7f1c1, None)
    
    class Diff:
        Command = (0xff7f7f00, None)
        Comment = (0xff679d47, None)
        Default = (0xfff7f1c1, None)
        Header = (0xffe1aa7d, None)
        LineAdded = (0xff519872, None)
        LineChanged = (0xff7f7f7f, None)
        LineRemoved = (0xff6c9686, None)
        Position = (0xff7ca563, None)
    
    class Fortran:
        Comment = (0xff679d47, None)
        Continuation = (0xfff7f1c1, None)
        Default = (0xff808080, None)
        DottedOperator = (0xfff7f1c1, None)
        DoubleQuotedString = (0xff7ca563, None)
        ExtendedFunction = (0xffb04080, None)
        Identifier = (0xfff7f1c1, None)
        IntrinsicFunction = (0xffb00040, None)
        Keyword = (0xff519872, None)
        Label = (0xffe0c0e0, None)
        Number = (0xff6c9686, None)
        Operator = (0xfff7f1c1, None)
        PreProcessor = (0xff7f7f00, None)
        SingleQuotedString = (0xff7ca563, None)
        UnclosedString = (0xfff7f1c1, None)
    
    class Fortran77:
        Comment = (0xff679d47, None)
        Continuation = (0xfff7f1c1, None)
        Default = (0xff808080, None)
        DottedOperator = (0xfff7f1c1, None)
        DoubleQuotedString = (0xff7ca563, None)
        ExtendedFunction = (0xffb04080, None)
        Identifier = (0xfff7f1c1, None)
        IntrinsicFunction = (0xffb00040, None)
        Keyword = (0xff519872, None)
        Label = (0xffe0c0e0, None)
        Number = (0xff6c9686, None)
        Operator = (0xfff7f1c1, None)
        PreProcessor = (0xff7f7f00, None)
        SingleQuotedString = (0xff7ca563, None)
        UnclosedString = (0xfff7f1c1, None)
    
    class HTML:
        ASPAtStart = (0xfff7f1c1, None)
        ASPJavaScriptComment = (0xff679d47, None)
        ASPJavaScriptCommentDoc = (0xff7f7f7f, None)
        ASPJavaScriptCommentLine = (0xff679d47, None)
        ASPJavaScriptDefault = (0xfff7f1c1, None)
        ASPJavaScriptDoubleQuotedString = (0xff7ca563, None)
        ASPJavaScriptKeyword = (0xff519872, None)
        ASPJavaScriptNumber = (0xff6c9686, None)
        ASPJavaScriptRegex = (0xfff7f1c1, None)
        ASPJavaScriptSingleQuotedString = (0xff7ca563, None)
        ASPJavaScriptStart = (0xff7f7f00, None)
        ASPJavaScriptSymbol = (0xfff7f1c1, None)
        ASPJavaScriptUnclosedString = (0xfff7f1c1, None)
        ASPJavaScriptWord = (0xfff7f1c1, None)
        ASPPythonClassName = (0xffb3935c, None)
        ASPPythonComment = (0xff679d47, None)
        ASPPythonDefault = (0xff808080, None)
        ASPPythonDoubleQuotedString = (0xff7ca563, None)
        ASPPythonFunctionMethodName = (0xff6c9686, None)
        ASPPythonIdentifier = (0xfff7f1c1, None)
        ASPPythonKeyword = (0xff519872, None)
        ASPPythonNumber = (0xff6c9686, None)
        ASPPythonOperator = (0xfff7f1c1, None)
        ASPPythonSingleQuotedString = (0xff7ca563, None)
        ASPPythonStart = (0xff808080, None)
        ASPPythonTripleDoubleQuotedString = (0xffe1aa7d, None)
        ASPPythonTripleSingleQuotedString = (0xffe1aa7d, None)
        ASPStart = (0xfff7f1c1, None)
        ASPVBScriptComment = (0xff008000, None)
        ASPVBScriptDefault = (0xfff7f1c1, None)
        ASPVBScriptIdentifier = (0xff007fff, None)
        ASPVBScriptKeyword = (0xff007fff, None)
        ASPVBScriptNumber = (0xff008080, None)
        ASPVBScriptStart = (0xfff7f1c1, None)
        ASPVBScriptString = (0xff800080, None)
        ASPVBScriptUnclosedString = (0xff007fff, None)
        ASPXCComment = (0xff1a0f0b, None)
        Attribute = (0xff008080, None)
        CDATA = (0xfff7f1c1, None)
        Default = (0xfff7f1c1, None)
        Entity = (0xff800080, None)
        HTMLComment = (0xff808000, None)
        HTMLDoubleQuotedString = (0xff7ca563, None)
        HTMLNumber = (0xff6c9686, None)
        HTMLSingleQuotedString = (0xff7ca563, None)
        HTMLValue = (0xffff00ff, None)
        JavaScriptComment = (0xff679d47, None)
        JavaScriptCommentDoc = (0xff3f703f, None)
        JavaScriptCommentLine = (0xff679d47, None)
        JavaScriptDefault = (0xfff7f1c1, None)
        JavaScriptDoubleQuotedString = (0xff7ca563, None)
        JavaScriptKeyword = (0xff519872, None)
        JavaScriptNumber = (0xff6c9686, None)
        JavaScriptRegex = (0xfff7f1c1, None)
        JavaScriptSingleQuotedString = (0xff7ca563, None)
        JavaScriptStart = (0xff7f7f00, None)
        JavaScriptSymbol = (0xfff7f1c1, None)
        JavaScriptUnclosedString = (0xfff7f1c1, None)
        JavaScriptWord = (0xfff7f1c1, None)
        OtherInTag = (0xff800080, None)
        PHPComment = (0xff999999, None)
        PHPCommentLine = (0xff666666, None)
        PHPDefault = (0xff000033, None)
        PHPDoubleQuotedString = (0xff679d47, None)
        PHPDoubleQuotedVariable = (0xff519872, None)
        PHPKeyword = (0xff7ca563, None)
        PHPNumber = (0xffcc9900, None)
        PHPOperator = (0xfff7f1c1, None)
        PHPSingleQuotedString = (0xff009f00, None)
        PHPStart = (0xffb3935c, None)
        PHPVariable = (0xff519872, None)
        PythonClassName = (0xffb3935c, None)
        PythonComment = (0xff679d47, None)
        PythonDefault = (0xff808080, None)
        PythonDoubleQuotedString = (0xff7ca563, None)
        PythonFunctionMethodName = (0xff6c9686, None)
        PythonIdentifier = (0xfff7f1c1, None)
        PythonKeyword = (0xff519872, None)
        PythonNumber = (0xff6c9686, None)
        PythonOperator = (0xfff7f1c1, None)
        PythonSingleQuotedString = (0xff7ca563, None)
        PythonStart = (0xff808080, None)
        PythonTripleDoubleQuotedString = (0xffe1aa7d, None)
        PythonTripleSingleQuotedString = (0xffe1aa7d, None)
        SGMLBlockDefault = (0xff000066, None)
        SGMLCommand = (0xff007fff, None)
        SGMLComment = (0xff808000, None)
        SGMLDefault = (0xff007fff, None)
        SGMLDoubleQuotedString = (0xff800000, None)
        SGMLEntity = (0xff333333, None)
        SGMLError = (0xff800000, None)
        SGMLParameter = (0xff006600, None)
        SGMLParameterComment = (0xff1a0f0b, None)
        SGMLSingleQuotedString = (0xff993300, None)
        SGMLSpecial = (0xff3366ff, None)
        Script = (0xff007fff, None)
        Tag = (0xff007fff, None)
        UnknownAttribute = (0xffff0000, None)
        UnknownTag = (0xffff0000, None)
        VBScriptComment = (0xff008000, None)
        VBScriptDefault = (0xfff7f1c1, None)
        VBScriptIdentifier = (0xff007fff, None)
        VBScriptKeyword = (0xff007fff, None)
        VBScriptNumber = (0xff008080, None)
        VBScriptStart = (0xfff7f1c1, None)
        VBScriptString = (0xff800080, None)
        VBScriptUnclosedString = (0xff007fff, None)
        XMLEnd = (0xffb3935c, None)
        XMLStart = (0xffb3935c, None)
        XMLTagEnd = (0xff007fff, None)
    
    class IDL:
        Comment = (0xff679d47, None)
        CommentDoc = (0xff3f703f, None)
        CommentDocKeyword = (0xff3060a0, None)
        CommentDocKeywordError = (0xff804020, None)
        CommentLine = (0xff679d47, None)
        CommentLineDoc = (0xff3f703f, None)
        Default = (0xff808080, None)
        DoubleQuotedString = (0xff7ca563, None)
        GlobalClass = (0xfff7f1c1, None)
        HashQuotedString = (0xff679d47, None)
        Identifier = (0xfff7f1c1, None)
        InactiveComment = (0xff90b090, None)
        InactiveCommentDoc = (0xffd0d0d0, None)
        InactiveCommentDocKeyword = (0xffc0c0c0, None)
        InactiveCommentDocKeywordError = (0xffc0c0c0, None)
        InactiveCommentLine = (0xff90b090, None)
        InactiveCommentLineDoc = (0xffc0c0c0, None)
        InactiveDefault = (0xffc0c0c0, None)
        InactiveDoubleQuotedString = (0xffb090b0, None)
        InactiveGlobalClass = (0xffb0b0b0, None)
        InactiveHashQuotedString = (0xfff7f1c1, None)
        InactiveIdentifier = (0xffb0b0b0, None)
        InactiveKeyword = (0xff9090b0, None)
        InactiveKeywordSet2 = (0xffc0c0c0, None)
        InactiveNumber = (0xff90b090, None)
        InactiveOperator = (0xffb0b0b0, None)
        InactivePreProcessor = (0xffb0b090, None)
        InactivePreProcessorComment = (0xff1a0f0b, None)
        InactivePreProcessorCommentLineDoc = (0xffc0c0c0, None)
        InactiveRawString = (0xfff7f1c1, None)
        InactiveRegex = (0xff7faf7f, None)
        InactiveSingleQuotedString = (0xffb090b0, None)
        InactiveTripleQuotedVerbatimString = (0xfff7f1c1, None)
        InactiveUUID = (0xffc0c0c0, None)
        InactiveUnclosedString = (0xfff7f1c1, None)
        InactiveVerbatimString = (0xff90b090, None)
        Keyword = (0xff519872, None)
        KeywordSet2 = (0xfff7f1c1, None)
        Number = (0xff6c9686, None)
        Operator = (0xfff7f1c1, None)
        PreProcessor = (0xff7f7f00, None)
        PreProcessorComment = (0xff659900, None)
        PreProcessorCommentLineDoc = (0xff3f703f, None)
        RawString = (0xff7ca563, None)
        Regex = (0xff3f7f3f, None)
        SingleQuotedString = (0xff7ca563, None)
        TripleQuotedVerbatimString = (0xff679d47, None)
        UUID = (0xff804080, None)
        UnclosedString = (0xfff7f1c1, None)
        VerbatimString = (0xff679d47, None)
    
    class Java:
        Comment = (0xff679d47, None)
        CommentDoc = (0xff3f703f, None)
        CommentDocKeyword = (0xff3060a0, None)
        CommentDocKeywordError = (0xff804020, None)
        CommentLine = (0xff679d47, None)
        CommentLineDoc = (0xff3f703f, None)
        Default = (0xff808080, None)
        DoubleQuotedString = (0xff7ca563, None)
        GlobalClass = (0xfff7f1c1, None)
        HashQuotedString = (0xff679d47, None)
        Identifier = (0xfff7f1c1, None)
        InactiveComment = (0xff90b090, None)
        InactiveCommentDoc = (0xffd0d0d0, None)
        InactiveCommentDocKeyword = (0xffc0c0c0, None)
        InactiveCommentDocKeywordError = (0xffc0c0c0, None)
        InactiveCommentLine = (0xff90b090, None)
        InactiveCommentLineDoc = (0xffc0c0c0, None)
        InactiveDefault = (0xffc0c0c0, None)
        InactiveDoubleQuotedString = (0xffb090b0, None)
        InactiveGlobalClass = (0xffb0b0b0, None)
        InactiveHashQuotedString = (0xfff7f1c1, None)
        InactiveIdentifier = (0xffb0b0b0, None)
        InactiveKeyword = (0xff9090b0, None)
        InactiveKeywordSet2 = (0xffc0c0c0, None)
        InactiveNumber = (0xff90b090, None)
        InactiveOperator = (0xffb0b0b0, None)
        InactivePreProcessor = (0xffb0b090, None)
        InactivePreProcessorComment = (0xff1a0f0b, None)
        InactivePreProcessorCommentLineDoc = (0xffc0c0c0, None)
        InactiveRawString = (0xfff7f1c1, None)
        InactiveRegex = (0xff7faf7f, None)
        InactiveSingleQuotedString = (0xffb090b0, None)
        InactiveTripleQuotedVerbatimString = (0xfff7f1c1, None)
        InactiveUUID = (0xffc0c0c0, None)
        InactiveUnclosedString = (0xfff7f1c1, None)
        InactiveVerbatimString = (0xff90b090, None)
        Keyword = (0xff519872, None)
        KeywordSet2 = (0xfff7f1c1, None)
        Number = (0xff6c9686, None)
        Operator = (0xfff7f1c1, None)
        PreProcessor = (0xff7f7f00, None)
        PreProcessorComment = (0xff659900, None)
        PreProcessorCommentLineDoc = (0xff3f703f, None)
        RawString = (0xff7ca563, None)
        Regex = (0xff3f7f3f, None)
        SingleQuotedString = (0xff7ca563, None)
        TripleQuotedVerbatimString = (0xff679d47, None)
        UUID = (0xfff7f1c1, None)
        UnclosedString = (0xfff7f1c1, None)
        VerbatimString = (0xff679d47, None)
    
    class JavaScript:
        Comment = (0xff679d47, None)
        CommentDoc = (0xff3f703f, None)
        CommentDocKeyword = (0xff3060a0, None)
        CommentDocKeywordError = (0xff804020, None)
        CommentLine = (0xff679d47, None)
        CommentLineDoc = (0xff3f703f, None)
        Default = (0xff808080, None)
        DoubleQuotedString = (0xff7ca563, None)
        GlobalClass = (0xfff7f1c1, None)
        HashQuotedString = (0xff679d47, None)
        Identifier = (0xfff7f1c1, None)
        InactiveComment = (0xff90b090, None)
        InactiveCommentDoc = (0xffd0d0d0, None)
        InactiveCommentDocKeyword = (0xffc0c0c0, None)
        InactiveCommentDocKeywordError = (0xffc0c0c0, None)
        InactiveCommentLine = (0xff90b090, None)
        InactiveCommentLineDoc = (0xffc0c0c0, None)
        InactiveDefault = (0xffc0c0c0, None)
        InactiveDoubleQuotedString = (0xffb090b0, None)
        InactiveGlobalClass = (0xffb0b0b0, None)
        InactiveHashQuotedString = (0xfff7f1c1, None)
        InactiveIdentifier = (0xffb0b0b0, None)
        InactiveKeyword = (0xff9090b0, None)
        InactiveKeywordSet2 = (0xffc0c0c0, None)
        InactiveNumber = (0xff90b090, None)
        InactiveOperator = (0xffb0b0b0, None)
        InactivePreProcessor = (0xffb0b090, None)
        InactivePreProcessorComment = (0xff1a0f0b, None)
        InactivePreProcessorCommentLineDoc = (0xffc0c0c0, None)
        InactiveRawString = (0xfff7f1c1, None)
        InactiveRegex = (0xff7faf7f, None)
        InactiveSingleQuotedString = (0xffb090b0, None)
        InactiveTripleQuotedVerbatimString = (0xfff7f1c1, None)
        InactiveUUID = (0xffc0c0c0, None)
        InactiveUnclosedString = (0xfff7f1c1, None)
        InactiveVerbatimString = (0xff90b090, None)
        Keyword = (0xff519872, None)
        KeywordSet2 = (0xfff7f1c1, None)
        Number = (0xff6c9686, None)
        Operator = (0xfff7f1c1, None)
        PreProcessor = (0xff7f7f00, None)
        PreProcessorComment = (0xff659900, None)
        PreProcessorCommentLineDoc = (0xff3f703f, None)
        RawString = (0xff7ca563, None)
        Regex = (0xff3f7f3f, None)
        SingleQuotedString = (0xff7ca563, None)
        TripleQuotedVerbatimString = (0xff679d47, None)
        UUID = (0xfff7f1c1, None)
        UnclosedString = (0xfff7f1c1, None)
        VerbatimString = (0xff679d47, None)
    
    class Lua:
        BasicFunctions = (0xff519872, None)
        Character = (0xff7ca563, None)
        Comment = (0xff679d47, None)
        CoroutinesIOSystemFacilities = (0xff519872, None)
        Default = (0xfff7f1c1, None)
        Identifier = (0xfff7f1c1, None)
        Keyword = (0xff519872, None)
        KeywordSet5 = (0xfff7f1c1, None)
        KeywordSet6 = (0xfff7f1c1, None)
        KeywordSet7 = (0xfff7f1c1, None)
        KeywordSet8 = (0xfff7f1c1, None)
        Label = (0xff7f7f00, None)
        LineComment = (0xff679d47, None)
        LiteralString = (0xff7ca563, None)
        Number = (0xff6c9686, None)
        Operator = (0xfff7f1c1, None)
        Preprocessor = (0xff7f7f00, None)
        String = (0xff7ca563, None)
        StringTableMathsFunctions = (0xff519872, None)
        UnclosedString = (0xfff7f1c1, None)
    
    class Makefile:
        Comment = (0xff679d47, None)
        Default = (0xfff7f1c1, None)
        Error = (0xffffff00, None)
        Operator = (0xfff7f1c1, None)
        Preprocessor = (0xff7f7f00, None)
        Target = (0xffa00000, None)
        Variable = (0xff007fff, None)
    
    class Matlab:
        Command = (0xff7f7f00, None)
        Comment = (0xff679d47, None)
        Default = (0xfff7f1c1, None)
        DoubleQuotedString = (0xff7ca563, None)
        Identifier = (0xfff7f1c1, None)
        Keyword = (0xff519872, None)
        Number = (0xff6c9686, None)
        Operator = (0xfff7f1c1, None)
        SingleQuotedString = (0xff7ca563, None)
    
    class Octave:
        Command = (0xff7f7f00, None)
        Comment = (0xff679d47, None)
        Default = (0xfff7f1c1, None)
        DoubleQuotedString = (0xff7ca563, None)
        Identifier = (0xfff7f1c1, None)
        Keyword = (0xff519872, None)
        Number = (0xff6c9686, None)
        Operator = (0xfff7f1c1, None)
        SingleQuotedString = (0xff7ca563, None)
    
    class PO:
        Comment = (0xff679d47, None)
        Default = (0xfff7f1c1, None)
        Flags = (0xfff7f1c1, None)
        Fuzzy = (0xfff7f1c1, None)
        MessageContext = (0xfff7f1c1, None)
        MessageContextText = (0xfff7f1c1, None)
        MessageContextTextEOL = (0xfff7f1c1, None)
        MessageId = (0xfff7f1c1, None)
        MessageIdText = (0xfff7f1c1, None)
        MessageIdTextEOL = (0xfff7f1c1, None)
        MessageString = (0xfff7f1c1, None)
        MessageStringText = (0xfff7f1c1, None)
        MessageStringTextEOL = (0xfff7f1c1, None)
        ProgrammerComment = (0xff1a0f0b, None)
        Reference = (0xfff7f1c1, None)
    
    class POV:
        BadDirective = (0xff804020, None)
        Comment = (0xff679d47, None)
        CommentLine = (0xff679d47, None)
        Default = (0xffff0080, None)
        Directive = (0xff7f7f00, None)
        Identifier = (0xfff7f1c1, None)
        KeywordSet6 = (0xff519872, None)
        KeywordSet7 = (0xff519872, None)
        KeywordSet8 = (0xff519872, None)
        Number = (0xff6c9686, None)
        ObjectsCSGAppearance = (0xff519872, None)
        Operator = (0xfff7f1c1, None)
        PredefinedFunctions = (0xff519872, None)
        PredefinedIdentifiers = (0xff519872, None)
        String = (0xff7ca563, None)
        TypesModifiersItems = (0xff519872, None)
        UnclosedString = (0xfff7f1c1, None)
    
    class Pascal:
        Asm = (0xff804080, None)
        Character = (0xff7ca563, None)
        Comment = (0xff679d47, None)
        CommentLine = (0xff679d47, None)
        CommentParenthesis = (0xff679d47, None)
        Default = (0xff808080, None)
        HexNumber = (0xff6c9686, None)
        Identifier = (0xfff7f1c1, None)
        Keyword = (0xff519872, None)
        Number = (0xff6c9686, None)
        Operator = (0xfff7f1c1, None)
        PreProcessor = (0xff7f7f00, None)
        PreProcessorParenthesis = (0xff7f7f00, None)
        SingleQuotedString = (0xff7ca563, None)
        UnclosedString = (0xfff7f1c1, None)
    
    class Perl:
        Array = (0xfff7f1c1, None)
        BacktickHereDocument = (0xff7ca563, None)
        BacktickHereDocumentVar = (0xffd00000, None)
        Backticks = (0xffffff00, None)
        BackticksVar = (0xffd00000, None)
        Comment = (0xff679d47, None)
        DataSection = (0xff600000, None)
        Default = (0xff808080, None)
        DoubleQuotedHereDocument = (0xff7ca563, None)
        DoubleQuotedHereDocumentVar = (0xffd00000, None)
        DoubleQuotedString = (0xff7ca563, None)
        DoubleQuotedStringVar = (0xffd00000, None)
        Error = (0xffffff00, None)
        FormatBody = (0xffc000c0, None)
        FormatIdentifier = (0xffc000c0, None)
        Hash = (0xfff7f1c1, None)
        HereDocumentDelimiter = (0xfff7f1c1, None)
        Identifier = (0xfff7f1c1, None)
        Keyword = (0xff519872, None)
        Number = (0xff6c9686, None)
        Operator = (0xfff7f1c1, None)
        POD = (0xff004000, None)
        PODVerbatim = (0xff004000, None)
        QuotedStringQ = (0xff7ca563, None)
        QuotedStringQQ = (0xff7ca563, None)
        QuotedStringQQVar = (0xffd00000, None)
        QuotedStringQR = (0xfff7f1c1, None)
        QuotedStringQRVar = (0xffd00000, None)
        QuotedStringQW = (0xfff7f1c1, None)
        QuotedStringQX = (0xffffff00, None)
        QuotedStringQXVar = (0xffd00000, None)
        Regex = (0xfff7f1c1, None)
        RegexVar = (0xffd00000, None)
        Scalar = (0xfff7f1c1, None)
        SingleQuotedHereDocument = (0xff7ca563, None)
        SingleQuotedString = (0xff7ca563, None)
        SubroutinePrototype = (0xfff7f1c1, None)
        Substitution = (0xfff7f1c1, None)
        SubstitutionVar = (0xffd00000, None)
        SymbolTable = (0xfff7f1c1, None)
        Translation = (0xfff7f1c1, None)
    
    class PostScript:
        ArrayParenthesis = (0xff519872, None)
        BadStringCharacter = (0xffffff00, None)
        Base85String = (0xff7ca563, None)
        Comment = (0xff679d47, None)
        DSCComment = (0xff3f703f, None)
        DSCCommentValue = (0xff3060a0, None)
        Default = (0xfff7f1c1, None)
        DictionaryParenthesis = (0xff3060a0, None)
        HexString = (0xff3f7f3f, None)
        ImmediateEvalLiteral = (0xff7f7f00, None)
        Keyword = (0xff519872, None)
        Literal = (0xff7f7f00, None)
        Name = (0xfff7f1c1, None)
        Number = (0xff6c9686, None)
        ProcedureParenthesis = (0xfff7f1c1, None)
        Text = (0xff7ca563, None)
    
    class Properties:
        Assignment = (0xffb06000, None)
        Comment = (0xff6c9686, None)
        Default = (0xfff7f1c1, None)
        DefaultValue = (0xff7f7f00, None)
        Key = (0xfff7f1c1, None)
        Section = (0xff7ca563, None)
    
    class Python:
        ClassName = (0xffb3935c, None)
        Comment = (0xff679d47, None)
        CommentBlock = (0xff7f7f7f, None)
        Decorator = (0xff805000, None)
        Default = (0xfff7f1c1, None)
        DoubleQuotedString = (0xff7ca563, None)
        FunctionMethodName = (0xff6c9686, None)
        HighlightedIdentifier = (0xff407090, None)
        Identifier = (0xfff7f1c1, None)
        Inconsistent = (0xff679d47, None)
        Keyword = (0xff519872, None)
        NoWarning = (0xff808080, None)
        Number = (0xff6c9686, None)
        Operator = (0xfff7f1c1, None)
        SingleQuotedString = (0xff7ca563, None)
        Spaces = (0xff7ca563, None)
        Tabs = (0xff7ca563, None)
        TabsAfterSpaces = (0xff6c9686, None)
        TripleDoubleQuotedString = (0xffe1aa7d, None)
        TripleSingleQuotedString = (0xffe1aa7d, None)
        UnclosedString = (0xfff7f1c1, None)
    
    class Ruby:
        Backticks = (0xffffff00, None)
        ClassName = (0xffb3935c, None)
        ClassVariable = (0xff8000b0, None)
        Comment = (0xff679d47, None)
        DataSection = (0xff600000, None)
        Default = (0xff808080, None)
        DemotedKeyword = (0xff519872, None)
        DoubleQuotedString = (0xff7ca563, None)
        Error = (0xfff7f1c1, None)
        FunctionMethodName = (0xff6c9686, None)
        Global = (0xff800080, None)
        HereDocument = (0xff7ca563, None)
        HereDocumentDelimiter = (0xfff7f1c1, None)
        Identifier = (0xfff7f1c1, None)
        InstanceVariable = (0xffb00080, None)
        Keyword = (0xff519872, None)
        ModuleName = (0xffa000a0, None)
        Number = (0xff6c9686, None)
        Operator = (0xfff7f1c1, None)
        POD = (0xff004000, None)
        PercentStringQ = (0xff7ca563, None)
        PercentStringq = (0xff7ca563, None)
        PercentStringr = (0xfff7f1c1, None)
        PercentStringw = (0xfff7f1c1, None)
        PercentStringx = (0xffffff00, None)
        Regex = (0xfff7f1c1, None)
        SingleQuotedString = (0xff7ca563, None)
        Stderr = (0xfff7f1c1, None)
        Stdin = (0xfff7f1c1, None)
        Stdout = (0xfff7f1c1, None)
        Symbol = (0xffc0a030, None)
    
    class SQL:
        Comment = (0xff679d47, None)
        CommentDoc = (0xff7f7f7f, None)
        CommentDocKeyword = (0xff3060a0, None)
        CommentDocKeywordError = (0xff804020, None)
        CommentLine = (0xff679d47, None)
        CommentLineHash = (0xff679d47, None)
        Default = (0xff808080, None)
        DoubleQuotedString = (0xff7ca563, None)
        Identifier = (0xfff7f1c1, None)
        Keyword = (0xff519872, None)
        KeywordSet5 = (0xff4b0082, None)
        KeywordSet6 = (0xffb00040, None)
        KeywordSet7 = (0xff8b0000, None)
        KeywordSet8 = (0xff800080, None)
        Number = (0xff6c9686, None)
        Operator = (0xfff7f1c1, None)
        PlusComment = (0xff679d47, None)
        PlusKeyword = (0xff7f7f00, None)
        PlusPrompt = (0xff679d47, None)
        QuotedIdentifier = (0xfff7f1c1, None)
        SingleQuotedString = (0xff7ca563, None)
    
    class Spice:
        Command = (0xff519872, None)
        Comment = (0xff679d47, None)
        Default = (0xff808080, None)
        Delimiter = (0xfff7f1c1, None)
        Function = (0xff519872, None)
        Identifier = (0xfff7f1c1, None)
        Number = (0xff6c9686, None)
        Parameter = (0xff0040e0, None)
        Value = (0xff7ca563, None)
    
    class TCL:
        Comment = (0xff679d47, None)
        CommentBlock = (0xfff7f1c1, None)
        CommentBox = (0xff679d47, None)
        CommentLine = (0xff679d47, None)
        Default = (0xff808080, None)
        ExpandKeyword = (0xff519872, None)
        ITCLKeyword = (0xff519872, None)
        Identifier = (0xff519872, None)
        KeywordSet6 = (0xff519872, None)
        KeywordSet7 = (0xff519872, None)
        KeywordSet8 = (0xff519872, None)
        KeywordSet9 = (0xff519872, None)
        Modifier = (0xff7ca563, None)
        Number = (0xff6c9686, None)
        Operator = (0xfff7f1c1, None)
        QuotedKeyword = (0xff7ca563, None)
        QuotedString = (0xff7ca563, None)
        Substitution = (0xff7f7f00, None)
        SubstitutionBrace = (0xff7f7f00, None)
        TCLKeyword = (0xff519872, None)
        TkCommand = (0xff519872, None)
        TkKeyword = (0xff519872, None)
    
    class TeX:
        Command = (0xff679d47, None)
        Default = (0xff3f3f3f, None)
        Group = (0xffe1aa7d, None)
        Special = (0xff6c9686, None)
        Symbol = (0xff7f7f00, None)
        Text = (0xfff7f1c1, None)
    
    class VHDL:
        Attribute = (0xff804020, None)
        Comment = (0xff679d47, None)
        CommentLine = (0xff3f7f3f, None)
        Default = (0xff800080, None)
        Identifier = (0xfff7f1c1, None)
        Keyword = (0xff519872, None)
        KeywordSet7 = (0xff804020, None)
        Number = (0xff6c9686, None)
        Operator = (0xfff7f1c1, None)
        StandardFunction = (0xff808020, None)
        StandardOperator = (0xff6c9686, None)
        StandardPackage = (0xff208020, None)
        StandardType = (0xff208080, None)
        String = (0xff7ca563, None)
        UnclosedString = (0xfff7f1c1, None)
    
    class Verilog:
        Comment = (0xff679d47, None)
        CommentBang = (0xff3f7f3f, None)
        CommentLine = (0xff679d47, None)
        Default = (0xff808080, None)
        Identifier = (0xfff7f1c1, None)
        Keyword = (0xff519872, None)
        KeywordSet2 = (0xff6c9686, None)
        Number = (0xff6c9686, None)
        Operator = (0xff007070, None)
        Preprocessor = (0xff7f7f00, None)
        String = (0xff7ca563, None)
        SystemTask = (0xff804020, None)
        UnclosedString = (0xfff7f1c1, None)
        UserKeywordSet = (0xff2a00ff, None)
    
    class XML:
        ASPAtStart = (0xfff7f1c1, None)
        ASPJavaScriptComment = (0xff679d47, None)
        ASPJavaScriptCommentDoc = (0xff7f7f7f, None)
        ASPJavaScriptCommentLine = (0xff679d47, None)
        ASPJavaScriptDefault = (0xfff7f1c1, None)
        ASPJavaScriptDoubleQuotedString = (0xff7ca563, None)
        ASPJavaScriptKeyword = (0xff519872, None)
        ASPJavaScriptNumber = (0xff6c9686, None)
        ASPJavaScriptRegex = (0xfff7f1c1, None)
        ASPJavaScriptSingleQuotedString = (0xff7ca563, None)
        ASPJavaScriptStart = (0xff7f7f00, None)
        ASPJavaScriptSymbol = (0xfff7f1c1, None)
        ASPJavaScriptUnclosedString = (0xfff7f1c1, None)
        ASPJavaScriptWord = (0xfff7f1c1, None)
        ASPPythonClassName = (0xffb3935c, None)
        ASPPythonComment = (0xff679d47, None)
        ASPPythonDefault = (0xff808080, None)
        ASPPythonDoubleQuotedString = (0xff7ca563, None)
        ASPPythonFunctionMethodName = (0xff6c9686, None)
        ASPPythonIdentifier = (0xfff7f1c1, None)
        ASPPythonKeyword = (0xff519872, None)
        ASPPythonNumber = (0xff6c9686, None)
        ASPPythonOperator = (0xfff7f1c1, None)
        ASPPythonSingleQuotedString = (0xff7ca563, None)
        ASPPythonStart = (0xff808080, None)
        ASPPythonTripleDoubleQuotedString = (0xffe1aa7d, None)
        ASPPythonTripleSingleQuotedString = (0xffe1aa7d, None)
        ASPStart = (0xfff7f1c1, None)
        ASPVBScriptComment = (0xff008000, None)
        ASPVBScriptDefault = (0xfff7f1c1, None)
        ASPVBScriptIdentifier = (0xff007fff, None)
        ASPVBScriptKeyword = (0xff007fff, None)
        ASPVBScriptNumber = (0xff008080, None)
        ASPVBScriptStart = (0xfff7f1c1, None)
        ASPVBScriptString = (0xff800080, None)
        ASPVBScriptUnclosedString = (0xff007fff, None)
        ASPXCComment = (0xff1a0f0b, None)
        Attribute = (0xff008080, None)
        CDATA = (0xff800000, None)
        Default = (0xfff7f1c1, None)
        Entity = (0xff800080, None)
        HTMLComment = (0xff808000, None)
        HTMLDoubleQuotedString = (0xff7ca563, None)
        HTMLNumber = (0xff6c9686, None)
        HTMLSingleQuotedString = (0xff7ca563, None)
        HTMLValue = (0xff608060, None)
        JavaScriptComment = (0xff679d47, None)
        JavaScriptCommentDoc = (0xff3f703f, None)
        JavaScriptCommentLine = (0xff679d47, None)
        JavaScriptDefault = (0xfff7f1c1, None)
        JavaScriptDoubleQuotedString = (0xff7ca563, None)
        JavaScriptKeyword = (0xff519872, None)
        JavaScriptNumber = (0xff6c9686, None)
        JavaScriptRegex = (0xfff7f1c1, None)
        JavaScriptSingleQuotedString = (0xff7ca563, None)
        JavaScriptStart = (0xff7f7f00, None)
        JavaScriptSymbol = (0xfff7f1c1, None)
        JavaScriptUnclosedString = (0xfff7f1c1, None)
        JavaScriptWord = (0xfff7f1c1, None)
        OtherInTag = (0xff800080, None)
        PHPComment = (0xff999999, None)
        PHPCommentLine = (0xff666666, None)
        PHPDefault = (0xff000033, None)
        PHPDoubleQuotedString = (0xff679d47, None)
        PHPDoubleQuotedVariable = (0xff519872, None)
        PHPKeyword = (0xff7ca563, None)
        PHPNumber = (0xffcc9900, None)
        PHPOperator = (0xfff7f1c1, None)
        PHPSingleQuotedString = (0xff009f00, None)
        PHPStart = (0xff800000, None)
        PHPVariable = (0xff519872, None)
        PythonClassName = (0xffb3935c, None)
        PythonComment = (0xff679d47, None)
        PythonDefault = (0xff808080, None)
        PythonDoubleQuotedString = (0xff7ca563, None)
        PythonFunctionMethodName = (0xff6c9686, None)
        PythonIdentifier = (0xfff7f1c1, None)
        PythonKeyword = (0xff519872, None)
        PythonNumber = (0xff6c9686, None)
        PythonOperator = (0xfff7f1c1, None)
        PythonSingleQuotedString = (0xff7ca563, None)
        PythonStart = (0xff808080, None)
        PythonTripleDoubleQuotedString = (0xffe1aa7d, None)
        PythonTripleSingleQuotedString = (0xffe1aa7d, None)
        SGMLBlockDefault = (0xff000066, None)
        SGMLCommand = (0xff007fff, None)
        SGMLComment = (0xff808000, None)
        SGMLDefault = (0xff007fff, None)
        SGMLDoubleQuotedString = (0xff800000, None)
        SGMLEntity = (0xff333333, None)
        SGMLError = (0xff800000, None)
        SGMLParameter = (0xff006600, None)
        SGMLParameterComment = (0xff1a0f0b, None)
        SGMLSingleQuotedString = (0xff993300, None)
        SGMLSpecial = (0xff3366ff, None)
        Script = (0xff007fff, None)
        Tag = (0xff007fff, None)
        UnknownAttribute = (0xff008080, None)
        UnknownTag = (0xff007fff, None)
        VBScriptComment = (0xff008000, None)
        VBScriptDefault = (0xfff7f1c1, None)
        VBScriptIdentifier = (0xff007fff, None)
        VBScriptKeyword = (0xff007fff, None)
        VBScriptNumber = (0xff008080, None)
        VBScriptStart = (0xfff7f1c1, None)
        VBScriptString = (0xff800080, None)
        VBScriptUnclosedString = (0xff007fff, None)
        XMLEnd = (0xff800080, None)
        XMLStart = (0xff800080, None)
        XMLTagEnd = (0xff007fff, None)
    
    class YAML:
        Comment = (0xff008800, None)
        Default = (0xfff7f1c1, None)
        DocumentDelimiter = (0xff1a0f0b, None)
        Identifier = (0xff000088, None)
        Keyword = (0xff880088, None)
        Number = (0xff880000, None)
        Operator = (0xfff7f1c1, None)
        Reference = (0xff008888, None)
        SyntaxErrorMarker = (0xffffffff, None)
        TextBlockMarker = (0xff333366, None)


class Paper:
    Default = PyQt4.QtGui.QColor(0xff1a0f0b)
    
    class Ada:
        Default = 0xff1a0f0b
        Comment = 0xff1a0f0b
        Keyword = 0xff1a0f0b
        String = 0xff1a0f0b
        Procedure = 0xff1a0f0b
        Number = 0xff1a0f0b
        Type = 0xff1a0f0b
        Package = 0xff1a0f0b
    
    class Nim:
        Default = 0xff1a0f0b
        Comment = 0xff1a0f0b
        BasicKeyword = 0xff1a0f0b
        TopKeyword = 0xff1a0f0b
        String = 0xff1a0f0b
        LongString = 0xff1a0f0b
        Number = 0xff1a0f0b
        Operator = 0xff1a0f0b
        Unsafe = 0xff1a0f0b
        Type = 0xff1a0f0b
        DocumentationComment = 0xff1a0f0b
        Definition = 0xff1a0f0b
        Class = 0xff1a0f0b
        KeywordOperator = 0xff1a0f0b
        CharLiteral = 0xff1a0f0b
        CaseOf = 0xff1a0f0b
        UserKeyword = 0xff1a0f0b
        MultilineComment = 0xff1a0f0b
        MultilineDocumentation = 0xff1a0f0b
        Pragma = 0xff1a0f0b
    
    class Oberon:
        Default = 0xff1a0f0b
        Comment = 0xff1a0f0b
        Keyword = 0xff1a0f0b
        String = 0xff1a0f0b
        Procedure = 0xff1a0f0b
        Module = 0xff1a0f0b
        Number = 0xff1a0f0b
        Type = 0xff1a0f0b
    
    
    # Generated
    class AVS:
        Function = 0xff1a0f0b
        KeywordSet6 = 0xff1a0f0b
        TripleString = 0xff1a0f0b
        LineComment = 0xff1a0f0b
        Plugin = 0xff1a0f0b
        String = 0xff1a0f0b
        ClipProperty = 0xff1a0f0b
        Default = 0xff1a0f0b
        Operator = 0xff1a0f0b
        Number = 0xff1a0f0b
        Filter = 0xff1a0f0b
        Identifier = 0xff1a0f0b
        NestedBlockComment = 0xff1a0f0b
        Keyword = 0xff1a0f0b
        BlockComment = 0xff1a0f0b
    
    class Bash:
        Error = 0xffff0000
        Backticks = 0xffa08080
        SingleQuotedHereDocument = 0xffddd0dd
        Scalar = 0xffffe0e0
        HereDocumentDelimiter = 0xffddd0dd
        Comment = 0xff1a0f0b
        SingleQuotedString = 0xff1a0f0b
        Default = 0xff1a0f0b
        Operator = 0xff1a0f0b
        ParameterExpansion = 0xffffffe0
        Number = 0xff1a0f0b
        Identifier = 0xff1a0f0b
        Keyword = 0xff1a0f0b
        DoubleQuotedString = 0xff1a0f0b
    
    class Batch:
        Label = 0xff606060
        Default = 0xff1a0f0b
        Keyword = 0xff1a0f0b
        ExternalCommand = 0xff1a0f0b
        Variable = 0xff1a0f0b
        Comment = 0xff1a0f0b
        HideCommandChar = 0xff1a0f0b
        Operator = 0xff1a0f0b
    
    class CMake:
        Function = 0xff1a0f0b
        BlockForeach = 0xff1a0f0b
        BlockWhile = 0xff1a0f0b
        StringLeftQuote = 0xffeeeeee
        Label = 0xff1a0f0b
        Comment = 0xff1a0f0b
        BlockMacro = 0xff1a0f0b
        StringRightQuote = 0xffeeeeee
        Default = 0xff1a0f0b
        Number = 0xff1a0f0b
        BlockIf = 0xff1a0f0b
        Variable = 0xff1a0f0b
        KeywordSet3 = 0xff1a0f0b
        String = 0xffeeeeee
        StringVariable = 0xffeeeeee
    
    class CPP:
        CommentDocKeywordError = 0xff1a0f0b
        InactiveRegex = 0xffe0f0e0
        InactivePreProcessorComment = 0xff1a0f0b
        UUID = 0xff1a0f0b
        InactiveVerbatimString = 0xffe0ffe0
        SingleQuotedString = 0xff1a0f0b
        Operator = 0xff1a0f0b
        InactiveOperator = 0xff1a0f0b
        InactivePreProcessor = 0xff1a0f0b
        UnclosedString = 0xffe0c0e0
        Identifier = 0xff1a0f0b
        InactiveRawString = 0xff1a0f0b
        PreProcessor = 0xff1a0f0b
        KeywordSet2 = 0xff1a0f0b
        InactiveUnclosedString = 0xffe0c0e0
        InactiveCommentLine = 0xff1a0f0b
        InactiveNumber = 0xff1a0f0b
        InactivePreProcessorCommentLineDoc = 0xff1a0f0b
        Number = 0xff1a0f0b
        InactiveUUID = 0xff1a0f0b
        CommentDoc = 0xff1a0f0b
        InactiveCommentDoc = 0xff1a0f0b
        GlobalClass = 0xff1a0f0b
        InactiveSingleQuotedString = 0xff1a0f0b
        HashQuotedString = 0xffe7ffd7
        VerbatimString = 0xffe0ffe0
        InactiveHashQuotedString = 0xff1a0f0b
        Regex = 0xffe0f0e0
        InactiveGlobalClass = 0xff1a0f0b
        InactiveIdentifier = 0xff1a0f0b
        CommentLineDoc = 0xff1a0f0b
        TripleQuotedVerbatimString = 0xffe0ffe0
        InactiveKeywordSet2 = 0xff1a0f0b
        InactiveCommentDocKeyword = 0xff1a0f0b
        Keyword = 0xff1a0f0b
        InactiveCommentLineDoc = 0xff1a0f0b
        InactiveDefault = 0xff1a0f0b
        InactiveCommentDocKeywordError = 0xff1a0f0b
        InactiveTripleQuotedVerbatimString = 0xff1a0f0b
        CommentDocKeyword = 0xff1a0f0b
        InactiveDoubleQuotedString = 0xff1a0f0b
        CommentLine = 0xff1a0f0b
        Comment = 0xff1a0f0b
        PreProcessorComment = 0xff1a0f0b
        InactiveComment = 0xff1a0f0b
        RawString = 0xfffff3ff
        Default = 0xff1a0f0b
        PreProcessorCommentLineDoc = 0xff1a0f0b
        DoubleQuotedString = 0xff1a0f0b
        InactiveKeyword = 0xff1a0f0b
    
    class CSS:
        Important = 0xff1a0f0b
        CSS3Property = 0xff1a0f0b
        Attribute = 0xff1a0f0b
        Comment = 0xff1a0f0b
        SingleQuotedString = 0xff1a0f0b
        MediaRule = 0xff1a0f0b
        AtRule = 0xff1a0f0b
        UnknownPseudoClass = 0xff1a0f0b
        PseudoClass = 0xff1a0f0b
        Tag = 0xff1a0f0b
        CSS2Property = 0xff1a0f0b
        CSS1Property = 0xff1a0f0b
        IDSelector = 0xff1a0f0b
        ExtendedCSSProperty = 0xff1a0f0b
        Variable = 0xff1a0f0b
        ExtendedPseudoClass = 0xff1a0f0b
        ClassSelector = 0xff1a0f0b
        Default = 0xff1a0f0b
        PseudoElement = 0xff1a0f0b
        UnknownProperty = 0xff1a0f0b
        Value = 0xff1a0f0b
        ExtendedPseudoElement = 0xff1a0f0b
        DoubleQuotedString = 0xff1a0f0b
        Operator = 0xff1a0f0b
    
    class CSharp:
        CommentDocKeywordError = 0xff1a0f0b
        InactiveRegex = 0xff1a0f0b
        InactivePreProcessorComment = 0xff1a0f0b
        UUID = 0xff1a0f0b
        InactiveVerbatimString = 0xff1a0f0b
        SingleQuotedString = 0xff1a0f0b
        Operator = 0xff1a0f0b
        InactiveOperator = 0xff1a0f0b
        InactivePreProcessor = 0xff1a0f0b
        UnclosedString = 0xff1a0f0b
        Identifier = 0xff1a0f0b
        InactiveRawString = 0xff1a0f0b
        PreProcessor = 0xff1a0f0b
        KeywordSet2 = 0xff1a0f0b
        InactiveUnclosedString = 0xff1a0f0b
        InactiveCommentLine = 0xff1a0f0b
        InactiveNumber = 0xff1a0f0b
        InactivePreProcessorCommentLineDoc = 0xff1a0f0b
        Number = 0xff1a0f0b
        InactiveUUID = 0xff1a0f0b
        CommentDoc = 0xff1a0f0b
        InactiveCommentDoc = 0xff1a0f0b
        GlobalClass = 0xff1a0f0b
        InactiveSingleQuotedString = 0xff1a0f0b
        HashQuotedString = 0xff1a0f0b
        VerbatimString = 0xffe0ffe0
        InactiveHashQuotedString = 0xff1a0f0b
        Regex = 0xff1a0f0b
        InactiveGlobalClass = 0xff1a0f0b
        InactiveIdentifier = 0xff1a0f0b
        CommentLineDoc = 0xff1a0f0b
        TripleQuotedVerbatimString = 0xff1a0f0b
        InactiveKeywordSet2 = 0xff1a0f0b
        InactiveCommentDocKeyword = 0xff1a0f0b
        Keyword = 0xff1a0f0b
        InactiveCommentLineDoc = 0xff1a0f0b
        InactiveDefault = 0xff1a0f0b
        InactiveCommentDocKeywordError = 0xff1a0f0b
        InactiveTripleQuotedVerbatimString = 0xff1a0f0b
        CommentDocKeyword = 0xff1a0f0b
        InactiveDoubleQuotedString = 0xff1a0f0b
        CommentLine = 0xff1a0f0b
        Comment = 0xff1a0f0b
        PreProcessorComment = 0xff1a0f0b
        InactiveComment = 0xff1a0f0b
        RawString = 0xff1a0f0b
        Default = 0xff1a0f0b
        PreProcessorCommentLineDoc = 0xff1a0f0b
        DoubleQuotedString = 0xff1a0f0b
        InactiveKeyword = 0xff1a0f0b
    
    class CoffeeScript:
        UUID = 0xff1a0f0b
        CommentDocKeywordError = 0xff1a0f0b
        GlobalClass = 0xff1a0f0b
        VerbatimString = 0xffe0ffe0
        SingleQuotedString = 0xff1a0f0b
        Operator = 0xff1a0f0b
        Number = 0xff1a0f0b
        Identifier = 0xff1a0f0b
        Keyword = 0xff1a0f0b
        UnclosedString = 0xffe0c0e0
        Regex = 0xffe0f0e0
        CommentDocKeyword = 0xff1a0f0b
        BlockRegex = 0xff1a0f0b
        CommentLineDoc = 0xff1a0f0b
        PreProcessor = 0xff1a0f0b
        CommentLine = 0xff1a0f0b
        CommentBlock = 0xff1a0f0b
        Comment = 0xff1a0f0b
        KeywordSet2 = 0xff1a0f0b
        BlockRegexComment = 0xff1a0f0b
        Default = 0xff1a0f0b
        DoubleQuotedString = 0xff1a0f0b
        CommentDoc = 0xff1a0f0b
    
    class D:
        BackquoteString = 0xff1a0f0b
        CommentDocKeywordError = 0xff1a0f0b
        Operator = 0xff1a0f0b
        CommentNested = 0xff1a0f0b
        KeywordDoc = 0xff1a0f0b
        KeywordSet7 = 0xff1a0f0b
        Keyword = 0xff1a0f0b
        KeywordSecondary = 0xff1a0f0b
        Identifier = 0xff1a0f0b
        KeywordSet5 = 0xff1a0f0b
        CommentDocKeyword = 0xff1a0f0b
        KeywordSet6 = 0xff1a0f0b
        CommentLineDoc = 0xff1a0f0b
        CommentLine = 0xff1a0f0b
        Comment = 0xff1a0f0b
        Typedefs = 0xff1a0f0b
        Character = 0xff1a0f0b
        RawString = 0xff1a0f0b
        Default = 0xff1a0f0b
        Number = 0xff1a0f0b
        UnclosedString = 0xffe0c0e0
        String = 0xff1a0f0b
        CommentDoc = 0xff1a0f0b
    
    class Diff:
        Header = 0xff1a0f0b
        LineChanged = 0xff1a0f0b
        Default = 0xff1a0f0b
        LineRemoved = 0xff1a0f0b
        Command = 0xff1a0f0b
        Position = 0xff1a0f0b
        LineAdded = 0xff1a0f0b
        Comment = 0xff1a0f0b
    
    class Fortran:
        Label = 0xff1a0f0b
        Identifier = 0xff1a0f0b
        DottedOperator = 0xff1a0f0b
        PreProcessor = 0xff1a0f0b
        Comment = 0xff1a0f0b
        SingleQuotedString = 0xff1a0f0b
        Default = 0xff1a0f0b
        DoubleQuotedString = 0xff1a0f0b
        ExtendedFunction = 0xff1a0f0b
        UnclosedString = 0xffe0c0e0
        Number = 0xff1a0f0b
        Continuation = 0xfff0e080
        IntrinsicFunction = 0xff1a0f0b
        Keyword = 0xff1a0f0b
        Operator = 0xff1a0f0b
    
    class Fortran77:
        Label = 0xff1a0f0b
        Identifier = 0xff1a0f0b
        DottedOperator = 0xff1a0f0b
        PreProcessor = 0xff1a0f0b
        Comment = 0xff1a0f0b
        SingleQuotedString = 0xff1a0f0b
        Default = 0xff1a0f0b
        DoubleQuotedString = 0xff1a0f0b
        ExtendedFunction = 0xff1a0f0b
        UnclosedString = 0xffe0c0e0
        Number = 0xff1a0f0b
        Continuation = 0xfff0e080
        IntrinsicFunction = 0xff1a0f0b
        Keyword = 0xff1a0f0b
        Operator = 0xff1a0f0b
    
    class HTML:
        HTMLValue = 0xffffefff
        PythonDefault = 0xffefffef
        Entity = 0xff1a0f0b
        SGMLParameter = 0xffefefff
        SGMLDefault = 0xffefefff
        PHPVariable = 0xfffff8f8
        SGMLCommand = 0xffefefff
        PythonClassName = 0xffefffef
        VBScriptUnclosedString = 0xff7f7fff
        ASPJavaScriptDefault = 0xffdfdf7f
        ASPVBScriptStart = 0xff1a0f0b
        VBScriptDefault = 0xffefefff
        PythonNumber = 0xffefffef
        PythonOperator = 0xffefffef
        ASPJavaScriptSingleQuotedString = 0xffdfdf7f
        PHPDefault = 0xfffff8f8
        XMLStart = 0xff1a0f0b
        PythonFunctionMethodName = 0xffefffef
        ASPJavaScriptStart = 0xff1a0f0b
        JavaScriptWord = 0xfff0f0ff
        PHPSingleQuotedString = 0xfffff8f8
        PythonTripleDoubleQuotedString = 0xffefffef
        JavaScriptComment = 0xfff0f0ff
        Default = 0xff1a0f0b
        SGMLSingleQuotedString = 0xffefefff
        VBScriptComment = 0xffefefff
        ASPVBScriptNumber = 0xffcfcfef
        ASPJavaScriptCommentDoc = 0xffdfdf7f
        PythonIdentifier = 0xffefffef
        VBScriptKeyword = 0xffefefff
        JavaScriptDefault = 0xfff0f0ff
        PythonStart = 0xff1a0f0b
        ASPPythonComment = 0xffcfefcf
        ASPJavaScriptWord = 0xffdfdf7f
        SGMLParameterComment = 0xff1a0f0b
        JavaScriptSingleQuotedString = 0xfff0f0ff
        PythonSingleQuotedString = 0xffefffef
        HTMLSingleQuotedString = 0xff1a0f0b
        ASPVBScriptString = 0xffcfcfef
        SGMLBlockDefault = 0xffcccce0
        PythonKeyword = 0xffefffef
        XMLTagEnd = 0xff1a0f0b
        ASPVBScriptComment = 0xffcfcfef
        ASPPythonSingleQuotedString = 0xffcfefcf
        PHPDoubleQuotedVariable = 0xfffff8f8
        ASPJavaScriptComment = 0xffdfdf7f
        JavaScriptUnclosedString = 0xffbfbbb0
        JavaScriptDoubleQuotedString = 0xfff0f0ff
        UnknownAttribute = 0xff1a0f0b
        ASPPythonOperator = 0xffcfefcf
        ASPJavaScriptSymbol = 0xffdfdf7f
        ASPPythonFunctionMethodName = 0xffcfefcf
        SGMLDoubleQuotedString = 0xffefefff
        PHPOperator = 0xfffff8f8
        JavaScriptNumber = 0xfff0f0ff
        PythonDoubleQuotedString = 0xffefffef
        ASPAtStart = 0xffffff00
        Script = 0xff1a0f0b
        PHPCommentLine = 0xfffff8f8
        SGMLComment = 0xffefefff
        JavaScriptStart = 0xff1a0f0b
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
        OtherInTag = 0xff1a0f0b
        JavaScriptCommentDoc = 0xfff0f0ff
        Tag = 0xff1a0f0b
        XMLEnd = 0xff1a0f0b
        CDATA = 0xffffdf00
        HTMLNumber = 0xff1a0f0b
        SGMLError = 0xffff6666
        PHPKeyword = 0xfffff8f8
        ASPVBScriptUnclosedString = 0xff7f7fff
        ASPPythonNumber = 0xffcfefcf
        VBScriptString = 0xffefefff
        ASPPythonClassName = 0xffcfefcf
        ASPPythonStart = 0xff1a0f0b
        JavaScriptRegex = 0xffffbbb0
        ASPJavaScriptUnclosedString = 0xffbfbbb0
        ASPJavaScriptCommentLine = 0xffdfdf7f
        SGMLEntity = 0xffefefff
        ASPJavaScriptDoubleQuotedString = 0xffdfdf7f
        ASPStart = 0xffffdf00
        Attribute = 0xff1a0f0b
        ASPJavaScriptKeyword = 0xffdfdf7f
        ASPVBScriptDefault = 0xffcfcfef
        ASPVBScriptIdentifier = 0xffcfcfef
        ASPJavaScriptRegex = 0xffffbbb0
        VBScriptNumber = 0xffefefff
        HTMLDoubleQuotedString = 0xff1a0f0b
        ASPXCComment = 0xff1a0f0b
        VBScriptStart = 0xff1a0f0b
        PHPDoubleQuotedString = 0xfffff8f8
        PHPComment = 0xfffff8f8
        ASPPythonTripleSingleQuotedString = 0xffcfefcf
        ASPPythonDoubleQuotedString = 0xffcfefcf
        JavaScriptKeyword = 0xfff0f0ff
        JavaScriptSymbol = 0xfff0f0ff
        VBScriptIdentifier = 0xffefefff
        HTMLComment = 0xff1a0f0b
        UnknownTag = 0xff1a0f0b
        JavaScriptCommentLine = 0xfff0f0ff
        PythonComment = 0xffefffef
    
    class IDL:
        CommentDocKeywordError = 0xff1a0f0b
        InactiveRegex = 0xffe0f0e0
        InactivePreProcessorComment = 0xff1a0f0b
        UUID = 0xff1a0f0b
        InactiveVerbatimString = 0xffe0ffe0
        SingleQuotedString = 0xff1a0f0b
        Operator = 0xff1a0f0b
        InactiveOperator = 0xff1a0f0b
        InactivePreProcessor = 0xff1a0f0b
        UnclosedString = 0xffe0c0e0
        Identifier = 0xff1a0f0b
        InactiveRawString = 0xff1a0f0b
        PreProcessor = 0xff1a0f0b
        KeywordSet2 = 0xff1a0f0b
        InactiveUnclosedString = 0xffe0c0e0
        InactiveCommentLine = 0xff1a0f0b
        InactiveNumber = 0xff1a0f0b
        InactivePreProcessorCommentLineDoc = 0xff1a0f0b
        Number = 0xff1a0f0b
        InactiveUUID = 0xff1a0f0b
        CommentDoc = 0xff1a0f0b
        InactiveCommentDoc = 0xff1a0f0b
        GlobalClass = 0xff1a0f0b
        InactiveSingleQuotedString = 0xff1a0f0b
        HashQuotedString = 0xffe7ffd7
        VerbatimString = 0xffe0ffe0
        InactiveHashQuotedString = 0xff1a0f0b
        Regex = 0xffe0f0e0
        InactiveGlobalClass = 0xff1a0f0b
        InactiveIdentifier = 0xff1a0f0b
        CommentLineDoc = 0xff1a0f0b
        TripleQuotedVerbatimString = 0xffe0ffe0
        InactiveKeywordSet2 = 0xff1a0f0b
        InactiveCommentDocKeyword = 0xff1a0f0b
        Keyword = 0xff1a0f0b
        InactiveCommentLineDoc = 0xff1a0f0b
        InactiveDefault = 0xff1a0f0b
        InactiveCommentDocKeywordError = 0xff1a0f0b
        InactiveTripleQuotedVerbatimString = 0xff1a0f0b
        CommentDocKeyword = 0xff1a0f0b
        InactiveDoubleQuotedString = 0xff1a0f0b
        CommentLine = 0xff1a0f0b
        Comment = 0xff1a0f0b
        PreProcessorComment = 0xff1a0f0b
        InactiveComment = 0xff1a0f0b
        RawString = 0xfffff3ff
        Default = 0xff1a0f0b
        PreProcessorCommentLineDoc = 0xff1a0f0b
        DoubleQuotedString = 0xff1a0f0b
        InactiveKeyword = 0xff1a0f0b
    
    class Java:
        CommentDocKeywordError = 0xff1a0f0b
        InactiveRegex = 0xffe0f0e0
        InactivePreProcessorComment = 0xff1a0f0b
        UUID = 0xff1a0f0b
        InactiveVerbatimString = 0xffe0ffe0
        SingleQuotedString = 0xff1a0f0b
        Operator = 0xff1a0f0b
        InactiveOperator = 0xff1a0f0b
        InactivePreProcessor = 0xff1a0f0b
        UnclosedString = 0xffe0c0e0
        Identifier = 0xff1a0f0b
        InactiveRawString = 0xff1a0f0b
        PreProcessor = 0xff1a0f0b
        KeywordSet2 = 0xff1a0f0b
        InactiveUnclosedString = 0xffe0c0e0
        InactiveCommentLine = 0xff1a0f0b
        InactiveNumber = 0xff1a0f0b
        InactivePreProcessorCommentLineDoc = 0xff1a0f0b
        Number = 0xff1a0f0b
        InactiveUUID = 0xff1a0f0b
        CommentDoc = 0xff1a0f0b
        InactiveCommentDoc = 0xff1a0f0b
        GlobalClass = 0xff1a0f0b
        InactiveSingleQuotedString = 0xff1a0f0b
        HashQuotedString = 0xffe7ffd7
        VerbatimString = 0xffe0ffe0
        InactiveHashQuotedString = 0xff1a0f0b
        Regex = 0xffe0f0e0
        InactiveGlobalClass = 0xff1a0f0b
        InactiveIdentifier = 0xff1a0f0b
        CommentLineDoc = 0xff1a0f0b
        TripleQuotedVerbatimString = 0xffe0ffe0
        InactiveKeywordSet2 = 0xff1a0f0b
        InactiveCommentDocKeyword = 0xff1a0f0b
        Keyword = 0xff1a0f0b
        InactiveCommentLineDoc = 0xff1a0f0b
        InactiveDefault = 0xff1a0f0b
        InactiveCommentDocKeywordError = 0xff1a0f0b
        InactiveTripleQuotedVerbatimString = 0xff1a0f0b
        CommentDocKeyword = 0xff1a0f0b
        InactiveDoubleQuotedString = 0xff1a0f0b
        CommentLine = 0xff1a0f0b
        Comment = 0xff1a0f0b
        PreProcessorComment = 0xff1a0f0b
        InactiveComment = 0xff1a0f0b
        RawString = 0xfffff3ff
        Default = 0xff1a0f0b
        PreProcessorCommentLineDoc = 0xff1a0f0b
        DoubleQuotedString = 0xff1a0f0b
        InactiveKeyword = 0xff1a0f0b
    
    class JavaScript:
        CommentDocKeywordError = 0xff1a0f0b
        InactiveRegex = 0xff1a0f0b
        InactivePreProcessorComment = 0xff1a0f0b
        UUID = 0xff1a0f0b
        InactiveVerbatimString = 0xff1a0f0b
        SingleQuotedString = 0xff1a0f0b
        Operator = 0xff1a0f0b
        InactiveOperator = 0xff1a0f0b
        InactivePreProcessor = 0xff1a0f0b
        UnclosedString = 0xff1a0f0b
        Identifier = 0xff1a0f0b
        InactiveRawString = 0xff1a0f0b
        PreProcessor = 0xff1a0f0b
        KeywordSet2 = 0xff1a0f0b
        InactiveUnclosedString = 0xff1a0f0b
        InactiveCommentLine = 0xff1a0f0b
        InactiveNumber = 0xff1a0f0b
        InactivePreProcessorCommentLineDoc = 0xff1a0f0b
        Number = 0xff1a0f0b
        InactiveUUID = 0xff1a0f0b
        CommentDoc = 0xff1a0f0b
        InactiveCommentDoc = 0xff1a0f0b
        GlobalClass = 0xff1a0f0b
        InactiveSingleQuotedString = 0xff1a0f0b
        HashQuotedString = 0xff1a0f0b
        VerbatimString = 0xff1a0f0b
        InactiveHashQuotedString = 0xff1a0f0b
        Regex = 0xffe0f0ff
        InactiveGlobalClass = 0xff1a0f0b
        InactiveIdentifier = 0xff1a0f0b
        CommentLineDoc = 0xff1a0f0b
        TripleQuotedVerbatimString = 0xff1a0f0b
        InactiveKeywordSet2 = 0xff1a0f0b
        InactiveCommentDocKeyword = 0xff1a0f0b
        Keyword = 0xff1a0f0b
        InactiveCommentLineDoc = 0xff1a0f0b
        InactiveDefault = 0xff1a0f0b
        InactiveCommentDocKeywordError = 0xff1a0f0b
        InactiveTripleQuotedVerbatimString = 0xff1a0f0b
        CommentDocKeyword = 0xff1a0f0b
        InactiveDoubleQuotedString = 0xff1a0f0b
        CommentLine = 0xff1a0f0b
        Comment = 0xff1a0f0b
        PreProcessorComment = 0xff1a0f0b
        InactiveComment = 0xff1a0f0b
        RawString = 0xff1a0f0b
        Default = 0xff1a0f0b
        PreProcessorCommentLineDoc = 0xff1a0f0b
        DoubleQuotedString = 0xff1a0f0b
        InactiveKeyword = 0xff1a0f0b
    
    class Lua:
        Label = 0xff1a0f0b
        Identifier = 0xff1a0f0b
        StringTableMathsFunctions = 0xffd0d0ff
        CoroutinesIOSystemFacilities = 0xffffd0d0
        KeywordSet5 = 0xff1a0f0b
        KeywordSet6 = 0xff1a0f0b
        PreProcessor = 0xff1a0f0b
        LineComment = 0xff1a0f0b
        Comment = 0xffd0f0f0
        String = 0xff1a0f0b
        Character = 0xff1a0f0b
        Default = 0xff1a0f0b
        Operator = 0xff1a0f0b
        LiteralString = 0xffe0ffff
        Number = 0xff1a0f0b
        KeywordSet8 = 0xff1a0f0b
        KeywordSet7 = 0xff1a0f0b
        BasicFunctions = 0xffd0ffd0
        Keyword = 0xff1a0f0b
        UnclosedString = 0xffe0c0e0
    
    class Makefile:
        Default = 0xff1a0f0b
        Operator = 0xff1a0f0b
        Target = 0xff1a0f0b
        PreProcessor = 0xff1a0f0b
        Variable = 0xff1a0f0b
        Comment = 0xff1a0f0b
        Error = 0xffff0000
    
    class Matlab:
        SingleQuotedString = 0xff1a0f0b
        Default = 0xff1a0f0b
        Keyword = 0xff1a0f0b
        Number = 0xff1a0f0b
        Command = 0xff1a0f0b
        Identifier = 0xff1a0f0b
        Comment = 0xff1a0f0b
        DoubleQuotedString = 0xff1a0f0b
        Operator = 0xff1a0f0b
    
    class Octave:
        SingleQuotedString = 0xff1a0f0b
        Default = 0xff1a0f0b
        Keyword = 0xff1a0f0b
        Number = 0xff1a0f0b
        Command = 0xff1a0f0b
        Identifier = 0xff1a0f0b
        Comment = 0xff1a0f0b
        DoubleQuotedString = 0xff1a0f0b
        Operator = 0xff1a0f0b
    
    class PO:
        ProgrammerComment = 0xff1a0f0b
        Flags = 0xff1a0f0b
        MessageContextText = 0xff1a0f0b
        MessageStringTextEOL = 0xff1a0f0b
        MessageId = 0xff1a0f0b
        MessageIdText = 0xff1a0f0b
        Reference = 0xff1a0f0b
        Comment = 0xff1a0f0b
        MessageStringText = 0xff1a0f0b
        MessageContext = 0xff1a0f0b
        Fuzzy = 0xff1a0f0b
        Default = 0xff1a0f0b
        MessageString = 0xff1a0f0b
        MessageContextTextEOL = 0xff1a0f0b
        MessageIdTextEOL = 0xff1a0f0b
    
    class POV:
        KeywordSet7 = 0xffd0d0d0
        KeywordSet6 = 0xffd0ffd0
        PredefinedFunctions = 0xffd0d0ff
        CommentLine = 0xff1a0f0b
        PredefinedIdentifiers = 0xff1a0f0b
        Comment = 0xff1a0f0b
        Directive = 0xff1a0f0b
        String = 0xff1a0f0b
        BadDirective = 0xff1a0f0b
        TypesModifiersItems = 0xffffffd0
        Default = 0xff1a0f0b
        Operator = 0xff1a0f0b
        Number = 0xff1a0f0b
        KeywordSet8 = 0xffe0e0e0
        Identifier = 0xff1a0f0b
        ObjectsCSGAppearance = 0xffffd0d0
        UnclosedString = 0xffe0c0e0
    
    class Pascal:
        PreProcessorParenthesis = 0xff1a0f0b
        SingleQuotedString = 0xff1a0f0b
        PreProcessor = 0xff1a0f0b
        CommentLine = 0xff1a0f0b
        Comment = 0xff1a0f0b
        CommentParenthesis = 0xff1a0f0b
        Asm = 0xff1a0f0b
        Character = 0xff1a0f0b
        Default = 0xff1a0f0b
        Operator = 0xff1a0f0b
        UnclosedString = 0xffe0c0e0
        Number = 0xff1a0f0b
        Identifier = 0xff1a0f0b
        Keyword = 0xff1a0f0b
        HexNumber = 0xff1a0f0b
    
    class Perl:
        Translation = 0xfff0e080
        BacktickHereDocument = 0xffddd0dd
        Array = 0xffffffe0
        QuotedStringQXVar = 0xffa08080
        PODVerbatim = 0xffc0ffc0
        DoubleQuotedStringVar = 0xff1a0f0b
        Regex = 0xffa0ffa0
        HereDocumentDelimiter = 0xffddd0dd
        SubroutinePrototype = 0xff1a0f0b
        BacktickHereDocumentVar = 0xffddd0dd
        QuotedStringQR = 0xff1a0f0b
        SingleQuotedString = 0xff1a0f0b
        QuotedStringQRVar = 0xff1a0f0b
        SubstitutionVar = 0xff1a0f0b
        Operator = 0xff1a0f0b
        DoubleQuotedHereDocumentVar = 0xffddd0dd
        Identifier = 0xff1a0f0b
        QuotedStringQX = 0xff1a0f0b
        BackticksVar = 0xffa08080
        Keyword = 0xff1a0f0b
        QuotedStringQ = 0xff1a0f0b
        QuotedStringQQVar = 0xff1a0f0b
        QuotedStringQQ = 0xff1a0f0b
        POD = 0xffe0ffe0
        FormatIdentifier = 0xff1a0f0b
        RegexVar = 0xff1a0f0b
        Backticks = 0xffa08080
        DoubleQuotedHereDocument = 0xffddd0dd
        Scalar = 0xffffe0e0
        FormatBody = 0xfffff0ff
        Comment = 0xff1a0f0b
        QuotedStringQW = 0xff1a0f0b
        SymbolTable = 0xffe0e0e0
        Default = 0xff1a0f0b
        Error = 0xffff0000
        SingleQuotedHereDocument = 0xffddd0dd
        Number = 0xff1a0f0b
        Hash = 0xffffe0ff
        Substitution = 0xfff0e080
        DataSection = 0xfffff0d8
        DoubleQuotedString = 0xff1a0f0b
    
    class PostScript:
        DictionaryParenthesis = 0xff1a0f0b
        HexString = 0xff1a0f0b
        DSCCommentValue = 0xff1a0f0b
        ProcedureParenthesis = 0xff1a0f0b
        Comment = 0xff1a0f0b
        ImmediateEvalLiteral = 0xff1a0f0b
        Name = 0xff1a0f0b
        DSCComment = 0xff1a0f0b
        Default = 0xff1a0f0b
        Base85String = 0xff1a0f0b
        Number = 0xff1a0f0b
        ArrayParenthesis = 0xff1a0f0b
        Literal = 0xff1a0f0b
        BadStringCharacter = 0xffff0000
        Text = 0xff1a0f0b
        Keyword = 0xff1a0f0b
    
    class Properties:
        DefaultValue = 0xff1a0f0b
        Default = 0xff1a0f0b
        Section = 0xffe0f0f0
        Assignment = 0xff1a0f0b
        Key = 0xff1a0f0b
        Comment = 0xff1a0f0b
    
    class Python:
        TripleDoubleQuotedString = 0xff1a0f0b
        FunctionMethodName = 0xff1a0f0b
        TabsAfterSpaces = 0xff1a0f0b
        Tabs = 0xff1a0f0b
        Decorator = 0xff1a0f0b
        NoWarning = 0xff1a0f0b
        UnclosedString = 0xffe0c0e0
        Spaces = 0xff1a0f0b
        CommentBlock = 0xff1a0f0b
        Comment = 0xff1a0f0b
        TripleSingleQuotedString = 0xff1a0f0b
        SingleQuotedString = 0xff1a0f0b
        Inconsistent = 0xff1a0f0b
        Default = 0xff1a0f0b
        DoubleQuotedString = 0xff1a0f0b
        Operator = 0xff1a0f0b
        Number = 0xff1a0f0b
        Identifier = 0xff1a0f0b
        ClassName = 0xff1a0f0b
        Keyword = 0xff1a0f0b
        HighlightedIdentifier = 0xff1a0f0b
    
    class Ruby:
        Symbol = 0xff1a0f0b
        Stderr = 0xffff8080
        Global = 0xff1a0f0b
        FunctionMethodName = 0xff1a0f0b
        Stdin = 0xffff8080
        HereDocumentDelimiter = 0xffddd0dd
        PercentStringr = 0xffa0ffa0
        PercentStringQ = 0xff1a0f0b
        ModuleName = 0xff1a0f0b
        HereDocument = 0xffddd0dd
        SingleQuotedString = 0xff1a0f0b
        PercentStringQ = 0xff1a0f0b
        Regex = 0xffa0ffa0
        Operator = 0xff1a0f0b
        PercentStringw = 0xffffffe0
        PercentStringx = 0xffa08080
        POD = 0xffc0ffc0
        Keyword = 0xff1a0f0b
        Stdout = 0xffff8080
        ClassVariable = 0xff1a0f0b
        Identifier = 0xff1a0f0b
        DemotedKeyword = 0xff1a0f0b
        Backticks = 0xffa08080
        InstanceVariable = 0xff1a0f0b
        Comment = 0xff1a0f0b
        Default = 0xff1a0f0b
        Error = 0xffff0000
        Number = 0xff1a0f0b
        DataSection = 0xfffff0d8
        ClassName = 0xff1a0f0b
        DoubleQuotedString = 0xff1a0f0b
    
    class SQL:
        PlusComment = 0xff1a0f0b
        KeywordSet7 = 0xff1a0f0b
        PlusPrompt = 0xffe0ffe0
        CommentDocKeywordError = 0xff1a0f0b
        CommentDocKeyword = 0xff1a0f0b
        KeywordSet6 = 0xff1a0f0b
        CommentLine = 0xff1a0f0b
        Comment = 0xff1a0f0b
        Operator = 0xff1a0f0b
        QuotedIdentifier = 0xff1a0f0b
        SingleQuotedString = 0xff1a0f0b
        PlusKeyword = 0xff1a0f0b
        Default = 0xff1a0f0b
        DoubleQuotedString = 0xff1a0f0b
        CommentLineHash = 0xff1a0f0b
        KeywordSet5 = 0xff1a0f0b
        Number = 0xff1a0f0b
        KeywordSet8 = 0xff1a0f0b
        Identifier = 0xff1a0f0b
        Keyword = 0xff1a0f0b
        CommentDoc = 0xff1a0f0b
    
    class Spice:
        Function = 0xff1a0f0b
        Delimiter = 0xff1a0f0b
        Value = 0xff1a0f0b
        Default = 0xff1a0f0b
        Number = 0xff1a0f0b
        Parameter = 0xff1a0f0b
        Command = 0xff1a0f0b
        Identifier = 0xff1a0f0b
        Comment = 0xff1a0f0b
    
    class TCL:
        SubstitutionBrace = 0xff1a0f0b
        CommentBox = 0xfff0fff0
        ITCLKeyword = 0xfffff0f0
        TkKeyword = 0xffe0fff0
        Operator = 0xff1a0f0b
        QuotedString = 0xfffff0f0
        ExpandKeyword = 0xffffff80
        KeywordSet7 = 0xff1a0f0b
        TCLKeyword = 0xff1a0f0b
        TkCommand = 0xffffd0d0
        Identifier = 0xff1a0f0b
        KeywordSet6 = 0xff1a0f0b
        CommentLine = 0xff1a0f0b
        CommentBlock = 0xfff0fff0
        Comment = 0xfff0ffe0
        Default = 0xff1a0f0b
        KeywordSet9 = 0xff1a0f0b
        Modifier = 0xff1a0f0b
        Number = 0xff1a0f0b
        KeywordSet8 = 0xff1a0f0b
        Substitution = 0xffeffff0
        QuotedKeyword = 0xfffff0f0
    
    class TeX:
        Symbol = 0xff1a0f0b
        Default = 0xff1a0f0b
        Command = 0xff1a0f0b
        Group = 0xff1a0f0b
        Text = 0xff1a0f0b
        Special = 0xff1a0f0b
    
    class VHDL:
        StandardOperator = 0xff1a0f0b
        Attribute = 0xff1a0f0b
        CommentLine = 0xff1a0f0b
        Comment = 0xff1a0f0b
        String = 0xff1a0f0b
        Default = 0xff1a0f0b
        Operator = 0xff1a0f0b
        StandardPackage = 0xff1a0f0b
        Number = 0xff1a0f0b
        Identifier = 0xff1a0f0b
        KeywordSet7 = 0xff1a0f0b
        StandardFunction = 0xff1a0f0b
        StandardType = 0xff1a0f0b
        Keyword = 0xff1a0f0b
        UnclosedString = 0xffe0c0e0
    
    class Verilog:
        CommentBang = 0xffe0f0ff
        UserKeywordSet = 0xff1a0f0b
        PreProcessor = 0xff1a0f0b
        CommentLine = 0xff1a0f0b
        Comment = 0xff1a0f0b
        KeywordSet2 = 0xff1a0f0b
        Default = 0xff1a0f0b
        Operator = 0xff1a0f0b
        Number = 0xff1a0f0b
        Identifier = 0xff1a0f0b
        SystemTask = 0xff1a0f0b
        String = 0xff1a0f0b
        Keyword = 0xff1a0f0b
        UnclosedString = 0xffe0c0e0
    
    class XML:
        HTMLValue = 0xffffefff
        PythonDefault = 0xffefffef
        Entity = 0xff1a0f0b
        SGMLParameter = 0xffefefff
        SGMLDefault = 0xffefefff
        PHPVariable = 0xfffff8f8
        SGMLCommand = 0xffefefff
        PythonClassName = 0xffefffef
        VBScriptUnclosedString = 0xff7f7fff
        ASPJavaScriptDefault = 0xffdfdf7f
        ASPVBScriptStart = 0xff1a0f0b
        VBScriptDefault = 0xffefefff
        PythonNumber = 0xffefffef
        PythonOperator = 0xffefffef
        ASPJavaScriptSingleQuotedString = 0xffdfdf7f
        PHPDefault = 0xfffff8f8
        XMLStart = 0xff1a0f0b
        PythonFunctionMethodName = 0xffefffef
        ASPJavaScriptStart = 0xff1a0f0b
        JavaScriptWord = 0xfff0f0ff
        PHPSingleQuotedString = 0xfffff8f8
        PythonTripleDoubleQuotedString = 0xffefffef
        JavaScriptComment = 0xfff0f0ff
        Default = 0xff1a0f0b
        SGMLSingleQuotedString = 0xffefefff
        VBScriptComment = 0xffefefff
        ASPVBScriptNumber = 0xffcfcfef
        ASPJavaScriptCommentDoc = 0xffdfdf7f
        PythonIdentifier = 0xffefffef
        VBScriptKeyword = 0xffefefff
        JavaScriptDefault = 0xfff0f0ff
        PythonStart = 0xff1a0f0b
        ASPPythonComment = 0xffcfefcf
        ASPJavaScriptWord = 0xffdfdf7f
        SGMLParameterComment = 0xff1a0f0b
        JavaScriptSingleQuotedString = 0xfff0f0ff
        PythonSingleQuotedString = 0xffefffef
        HTMLSingleQuotedString = 0xff1a0f0b
        ASPVBScriptString = 0xffcfcfef
        SGMLBlockDefault = 0xffcccce0
        PythonKeyword = 0xffefffef
        XMLTagEnd = 0xff1a0f0b
        ASPVBScriptComment = 0xffcfcfef
        ASPPythonSingleQuotedString = 0xffcfefcf
        PHPDoubleQuotedVariable = 0xfffff8f8
        ASPJavaScriptComment = 0xffdfdf7f
        JavaScriptUnclosedString = 0xffbfbbb0
        JavaScriptDoubleQuotedString = 0xfff0f0ff
        UnknownAttribute = 0xff1a0f0b
        ASPPythonOperator = 0xffcfefcf
        ASPJavaScriptSymbol = 0xffdfdf7f
        ASPPythonFunctionMethodName = 0xffcfefcf
        SGMLDoubleQuotedString = 0xffefefff
        PHPOperator = 0xfffff8f8
        JavaScriptNumber = 0xfff0f0ff
        PythonDoubleQuotedString = 0xffefffef
        ASPAtStart = 0xffffff00
        Script = 0xff1a0f0b
        PHPCommentLine = 0xfffff8f8
        SGMLComment = 0xffefefff
        JavaScriptStart = 0xff1a0f0b
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
        OtherInTag = 0xff1a0f0b
        JavaScriptCommentDoc = 0xfff0f0ff
        Tag = 0xff1a0f0b
        XMLEnd = 0xff1a0f0b
        CDATA = 0xfffff0f0
        HTMLNumber = 0xff1a0f0b
        SGMLError = 0xffff6666
        PHPKeyword = 0xfffff8f8
        ASPVBScriptUnclosedString = 0xff7f7fff
        ASPPythonNumber = 0xffcfefcf
        VBScriptString = 0xffefefff
        ASPPythonClassName = 0xffcfefcf
        ASPPythonStart = 0xff1a0f0b
        JavaScriptRegex = 0xffffbbb0
        ASPJavaScriptUnclosedString = 0xffbfbbb0
        ASPJavaScriptCommentLine = 0xffdfdf7f
        SGMLEntity = 0xffefefff
        ASPJavaScriptDoubleQuotedString = 0xffdfdf7f
        ASPStart = 0xffffdf00
        Attribute = 0xff1a0f0b
        ASPJavaScriptKeyword = 0xffdfdf7f
        ASPVBScriptDefault = 0xffcfcfef
        ASPVBScriptIdentifier = 0xffcfcfef
        ASPJavaScriptRegex = 0xffffbbb0
        VBScriptNumber = 0xffefefff
        HTMLDoubleQuotedString = 0xff1a0f0b
        ASPXCComment = 0xff1a0f0b
        VBScriptStart = 0xff1a0f0b
        PHPDoubleQuotedString = 0xfffff8f8
        PHPComment = 0xfffff8f8
        ASPPythonTripleSingleQuotedString = 0xffcfefcf
        ASPPythonDoubleQuotedString = 0xffcfefcf
        JavaScriptKeyword = 0xfff0f0ff
        JavaScriptSymbol = 0xfff0f0ff
        VBScriptIdentifier = 0xffefefff
        HTMLComment = 0xff1a0f0b
        UnknownTag = 0xff1a0f0b
        JavaScriptCommentLine = 0xfff0f0ff
        PythonComment = 0xffefffef
    
    class YAML:
        TextBlockMarker = 0xff1a0f0b
        DocumentDelimiter = 0xff000088
        Operator = 0xff1a0f0b
        Number = 0xff1a0f0b
        Default = 0xff1a0f0b
        Identifier = 0xff1a0f0b
        Reference = 0xff1a0f0b
        Comment = 0xff1a0f0b
        Keyword = 0xff1a0f0b
        SyntaxErrorMarker = 0xffff0000

