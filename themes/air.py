
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
        Default = (0xffff0000, None)
        Comment = (0xff007f00, None)
        Keyword = (0xff00007f, None)
        String = (0xff7f007f, None)
        Procedure = (0xff0000ff, None)
        Number = (0xff007f7f, None)
        Type = (0xff00007f, None)
        Package = (0xff7f0000, None)
    
    class Nim:
        Default = (0xffff0000, None)
        Comment = (0xff007f00, None)
        BasicKeyword = (0xff00007f, True)
        TopKeyword = (0xff407fc0, True)
        String = (0xff7f007f, None)
        LongString = (0xff7f0000, None)
        Number = (0xff007f7f, None)
        Operator = (0xff7f7f7f, None)
        Unsafe = (0xffc00000, True)
        Type = (0xff6e6e00, True)
        DocumentationComment = (0xff7f0a0a, None)
        Definition = (0xff007f7f, None)
        Class = (0xff0000ff, None)
        KeywordOperator = (0xff963cc8, None)
        CharLiteral = (0xff00c8ff, None)
        CaseOf = (0xff8000ff, None)
        UserKeyword = (0xffff8040, None)
        MultilineComment = (0xff006c6c, None)
        MultilineDocumentation = (0xff6e3296, None)
        Pragma = (0xffc07f40, None)
    
    class Oberon:
        Default = (0xff000000, None)
        Comment = (0xff007f00, None)
        Keyword = (0xff00007f, None)
        String = (0xff7f007f, None)
        Procedure = (0xff0000ff, None)
        Module = (0xff7f0000, None)
        Number = (0xff007f7f, None)
        Type = (0xff00007f, None)
    
    
    class AVS:
        BlockComment = (0xff007f00, None)
        ClipProperty = (0xff00007f, None)
        Default = (0xff000000, None)
        Filter = (0xff00007f, None)
        Function = (0xff007f7f, None)
        Identifier = (0xff000000, None)
        Keyword = (0xff00007f, None)
        KeywordSet6 = (0xff8000ff, None)
        LineComment = (0xff007f00, None)
        NestedBlockComment = (0xff007f00, None)
        Number = (0xff007f7f, None)
        Operator = (0xff000000, None)
        Plugin = (0xff0080c0, None)
        String = (0xff7f007f, None)
        TripleString = (0xff7f007f, None)
    
    class Bash:
        Backticks = (0xffadad00, None)
        Comment = (0xff007f00, None)
        Default = (0xff808080, None)
        DoubleQuotedString = (0xff7f007f, True)
        Error = (0xffaa0000, True)
        HereDocumentDelimiter = (0xff000000, None)
        Identifier = (0xff000000, None)
        Keyword = (0xff00007f, None)
        Number = (0xff007f7f, None)
        Operator = (0xff000000, None)
        ParameterExpansion = (0xff000000, None)
        Scalar = (0xffadad00, True)
        SingleQuotedHereDocument = (0xff7f007f, None)
        SingleQuotedString = (0xff7f007f, None)
    
    class Batch:
        Comment = (0xff007f00, None)
        Default = (0xff000000, None)
        ExternalCommand = (0xff00007f, None)
        HideCommandChar = (0xff7f7f00, None)
        Keyword = (0xff00007f, None)
        Label = (0xff7f007f, None)
        Operator = (0xff000000, None)
        Variable = (0xff800080, None)
    
    class CMake:
        BlockForeach = (0xff00007f, None)
        BlockIf = (0xff00007f, None)
        BlockMacro = (0xff00007f, None)
        BlockWhile = (0xff00007f, None)
        Comment = (0xff007f00, None)
        Default = (0xff000000, None)
        Function = (0xff00007f, None)
        KeywordSet3 = (0xff000000, None)
        Label = (0xffcc3300, None)
        Number = (0xff007f7f, None)
        String = (0xff7f007f, None)
        StringLeftQuote = (0xff7f007f, None)
        StringRightQuote = (0xff7f007f, None)
        StringVariable = (0xffcc3300, None)
        Variable = (0xff800000, None)
    
    class CPP:
        Comment = (0xff007f00, None)
        CommentDoc = (0xff3f703f, None)
        CommentDocKeyword = (0xff3060a0, None)
        CommentDocKeywordError = (0xff804020, None)
        CommentLine = (0xff007f00, None)
        CommentLineDoc = (0xff3f703f, None)
        Default = (0xff808080, None)
        DoubleQuotedString = (0xff7f007f, None)
        GlobalClass = (0xff000000, None)
        HashQuotedString = (0xff007f00, None)
        Identifier = (0xff000000, None)
        InactiveComment = (0xff90b090, None)
        InactiveCommentDoc = (0xffd0d0d0, None)
        InactiveCommentDocKeyword = (0xffc0c0c0, None)
        InactiveCommentDocKeywordError = (0xffc0c0c0, None)
        InactiveCommentLine = (0xff90b090, None)
        InactiveCommentLineDoc = (0xffc0c0c0, None)
        InactiveDefault = (0xffc0c0c0, None)
        InactiveDoubleQuotedString = (0xffb090b0, None)
        InactiveGlobalClass = (0xffb0b0b0, None)
        InactiveHashQuotedString = (0xff000000, None)
        InactiveIdentifier = (0xffb0b0b0, None)
        InactiveKeyword = (0xff9090b0, None)
        InactiveKeywordSet2 = (0xffc0c0c0, None)
        InactiveNumber = (0xff90b090, None)
        InactiveOperator = (0xffb0b0b0, None)
        InactivePreProcessor = (0xffb0b090, None)
        InactivePreProcessorComment = (0xff000000, None)
        InactivePreProcessorCommentLineDoc = (0xffc0c0c0, None)
        InactiveRawString = (0xff000000, None)
        InactiveRegex = (0xff7faf7f, None)
        InactiveSingleQuotedString = (0xffb090b0, None)
        InactiveTripleQuotedVerbatimString = (0xff000000, None)
        InactiveUUID = (0xffc0c0c0, None)
        InactiveUnclosedString = (0xff000000, None)
        InactiveVerbatimString = (0xff90b090, None)
        Keyword = (0xff00007f, None)
        KeywordSet2 = (0xff000000, None)
        Number = (0xff007f7f, None)
        Operator = (0xff000000, None)
        PreProcessor = (0xff7f7f00, None)
        PreProcessorComment = (0xff659900, None)
        PreProcessorCommentLineDoc = (0xff3f703f, None)
        RawString = (0xff7f007f, None)
        Regex = (0xff3f7f3f, None)
        SingleQuotedString = (0xff7f007f, None)
        TripleQuotedVerbatimString = (0xff007f00, None)
        UUID = (0xff000000, None)
        UnclosedString = (0xff000000, None)
        VerbatimString = (0xff007f00, None)
    
    class CSS:
        AtRule = (0xff7f7f00, None)
        Attribute = (0xff800000, None)
        CSS1Property = (0xff0040e0, None)
        CSS2Property = (0xff00a0e0, None)
        CSS3Property = (0xff000000, None)
        ClassSelector = (0xff000000, None)
        Comment = (0xff007f00, None)
        Default = (0xffff0080, None)
        DoubleQuotedString = (0xff7f007f, None)
        ExtendedCSSProperty = (0xff000000, None)
        ExtendedPseudoClass = (0xff000000, None)
        ExtendedPseudoElement = (0xff000000, None)
        IDSelector = (0xff007f7f, None)
        Important = (0xffff8000, None)
        MediaRule = (0xff7f7f00, None)
        Operator = (0xff000000, None)
        PseudoClass = (0xff800000, None)
        PseudoElement = (0xff000000, None)
        SingleQuotedString = (0xff7f007f, None)
        Tag = (0xff00007f, None)
        UnknownProperty = (0xffff0000, None)
        UnknownPseudoClass = (0xffff0000, None)
        Value = (0xff7f007f, None)
        Variable = (0xff000000, None)
    
    class CSharp:
        Comment = (0xff007f00, None)
        CommentDoc = (0xff3f703f, None)
        CommentDocKeyword = (0xff3060a0, None)
        CommentDocKeywordError = (0xff804020, None)
        CommentLine = (0xff007f00, None)
        CommentLineDoc = (0xff3f703f, None)
        Default = (0xff808080, None)
        DoubleQuotedString = (0xff7f007f, None)
        GlobalClass = (0xff000000, None)
        HashQuotedString = (0xff007f00, None)
        Identifier = (0xff000000, None)
        InactiveComment = (0xff90b090, None)
        InactiveCommentDoc = (0xffd0d0d0, None)
        InactiveCommentDocKeyword = (0xffc0c0c0, None)
        InactiveCommentDocKeywordError = (0xffc0c0c0, None)
        InactiveCommentLine = (0xff90b090, None)
        InactiveCommentLineDoc = (0xffc0c0c0, None)
        InactiveDefault = (0xffc0c0c0, None)
        InactiveDoubleQuotedString = (0xffb090b0, None)
        InactiveGlobalClass = (0xffb0b0b0, None)
        InactiveHashQuotedString = (0xff000000, None)
        InactiveIdentifier = (0xffb0b0b0, None)
        InactiveKeyword = (0xff9090b0, None)
        InactiveKeywordSet2 = (0xffc0c0c0, None)
        InactiveNumber = (0xff90b090, None)
        InactiveOperator = (0xffb0b0b0, None)
        InactivePreProcessor = (0xffb0b090, None)
        InactivePreProcessorComment = (0xff000000, None)
        InactivePreProcessorCommentLineDoc = (0xffc0c0c0, None)
        InactiveRawString = (0xff000000, None)
        InactiveRegex = (0xff7faf7f, None)
        InactiveSingleQuotedString = (0xffb090b0, None)
        InactiveTripleQuotedVerbatimString = (0xff000000, None)
        InactiveUUID = (0xffc0c0c0, None)
        InactiveUnclosedString = (0xff000000, None)
        InactiveVerbatimString = (0xff90b090, None)
        Keyword = (0xff00007f, None)
        KeywordSet2 = (0xff000000, None)
        Number = (0xff007f7f, None)
        Operator = (0xff000000, None)
        PreProcessor = (0xff7f7f00, None)
        PreProcessorComment = (0xff659900, None)
        PreProcessorCommentLineDoc = (0xff3f703f, None)
        RawString = (0xff7f007f, None)
        Regex = (0xff3f7f3f, None)
        SingleQuotedString = (0xff7f007f, None)
        TripleQuotedVerbatimString = (0xff007f00, None)
        UUID = (0xff000000, None)
        UnclosedString = (0xff000000, None)
        VerbatimString = (0xff007f00, None)
    
    class CoffeeScript:
        BlockRegex = (0xff3f7f3f, None)
        BlockRegexComment = (0xff007f00, None)
        Comment = (0xff007f00, None)
        CommentBlock = (0xff007f00, None)
        CommentDoc = (0xff3f703f, None)
        CommentDocKeyword = (0xff3060a0, None)
        CommentDocKeywordError = (0xff804020, None)
        CommentLine = (0xff007f00, None)
        CommentLineDoc = (0xff3f703f, None)
        Default = (0xff808080, None)
        DoubleQuotedString = (0xff7f007f, None)
        GlobalClass = (0xff000000, None)
        Identifier = (0xff000000, None)
        Keyword = (0xff00007f, None)
        KeywordSet2 = (0xff000000, None)
        Number = (0xff007f7f, None)
        Operator = (0xff000000, None)
        PreProcessor = (0xff7f7f00, None)
        Regex = (0xff3f7f3f, None)
        SingleQuotedString = (0xff7f007f, None)
        UUID = (0xff000000, None)
        UnclosedString = (0xff000000, None)
        VerbatimString = (0xff007f00, None)
    
    class D:
        BackquoteString = (0xff000000, None)
        Character = (0xff7f007f, None)
        Comment = (0xff007f00, None)
        CommentDoc = (0xff3f703f, None)
        CommentDocKeyword = (0xff3060a0, None)
        CommentDocKeywordError = (0xff804020, None)
        CommentLine = (0xff007f00, None)
        CommentLineDoc = (0xff3f703f, None)
        CommentNested = (0xffa0c0a0, None)
        Default = (0xff808080, None)
        Identifier = (0xff000000, None)
        Keyword = (0xff00007f, None)
        KeywordDoc = (0xff00007f, None)
        KeywordSecondary = (0xff00007f, None)
        KeywordSet5 = (0xff000000, None)
        KeywordSet6 = (0xff000000, None)
        KeywordSet7 = (0xff000000, None)
        Number = (0xff007f7f, None)
        Operator = (0xff000000, None)
        RawString = (0xff000000, None)
        String = (0xff7f007f, None)
        Typedefs = (0xff00007f, None)
        UnclosedString = (0xff000000, None)
    
    class Diff:
        Command = (0xff7f7f00, None)
        Comment = (0xff007f00, None)
        Default = (0xff000000, None)
        Header = (0xff7f0000, None)
        LineAdded = (0xff00007f, None)
        LineChanged = (0xff7f7f7f, None)
        LineRemoved = (0xff007f7f, None)
        Position = (0xff7f007f, None)
    
    class Fortran:
        Comment = (0xff007f00, None)
        Continuation = (0xff000000, None)
        Default = (0xff808080, None)
        DottedOperator = (0xff000000, None)
        DoubleQuotedString = (0xff7f007f, None)
        ExtendedFunction = (0xffb04080, None)
        Identifier = (0xff000000, None)
        IntrinsicFunction = (0xffb00040, None)
        Keyword = (0xff00007f, None)
        Label = (0xffe0c0e0, None)
        Number = (0xff007f7f, None)
        Operator = (0xff000000, None)
        PreProcessor = (0xff7f7f00, None)
        SingleQuotedString = (0xff7f007f, None)
        UnclosedString = (0xff000000, None)
    
    class Fortran77:
        Comment = (0xff007f00, None)
        Continuation = (0xff000000, None)
        Default = (0xff808080, None)
        DottedOperator = (0xff000000, None)
        DoubleQuotedString = (0xff7f007f, None)
        ExtendedFunction = (0xffb04080, None)
        Identifier = (0xff000000, None)
        IntrinsicFunction = (0xffb00040, None)
        Keyword = (0xff00007f, None)
        Label = (0xffe0c0e0, None)
        Number = (0xff007f7f, None)
        Operator = (0xff000000, None)
        PreProcessor = (0xff7f7f00, None)
        SingleQuotedString = (0xff7f007f, None)
        UnclosedString = (0xff000000, None)
    
    class HTML:
        ASPAtStart = (0xff000000, None)
        ASPJavaScriptComment = (0xff007f00, None)
        ASPJavaScriptCommentDoc = (0xff7f7f7f, None)
        ASPJavaScriptCommentLine = (0xff007f00, None)
        ASPJavaScriptDefault = (0xff000000, None)
        ASPJavaScriptDoubleQuotedString = (0xff7f007f, None)
        ASPJavaScriptKeyword = (0xff00007f, None)
        ASPJavaScriptNumber = (0xff007f7f, None)
        ASPJavaScriptRegex = (0xff000000, None)
        ASPJavaScriptSingleQuotedString = (0xff7f007f, None)
        ASPJavaScriptStart = (0xff7f7f00, None)
        ASPJavaScriptSymbol = (0xff000000, None)
        ASPJavaScriptUnclosedString = (0xff000000, None)
        ASPJavaScriptWord = (0xff000000, None)
        ASPPythonClassName = (0xff0000ff, None)
        ASPPythonComment = (0xff007f00, None)
        ASPPythonDefault = (0xff808080, None)
        ASPPythonDoubleQuotedString = (0xff7f007f, None)
        ASPPythonFunctionMethodName = (0xff007f7f, None)
        ASPPythonIdentifier = (0xff000000, None)
        ASPPythonKeyword = (0xff00007f, None)
        ASPPythonNumber = (0xff007f7f, None)
        ASPPythonOperator = (0xff000000, None)
        ASPPythonSingleQuotedString = (0xff7f007f, None)
        ASPPythonStart = (0xff808080, None)
        ASPPythonTripleDoubleQuotedString = (0xff7f0000, None)
        ASPPythonTripleSingleQuotedString = (0xff7f0000, None)
        ASPStart = (0xff000000, None)
        ASPVBScriptComment = (0xff008000, None)
        ASPVBScriptDefault = (0xff000000, None)
        ASPVBScriptIdentifier = (0xff000080, None)
        ASPVBScriptKeyword = (0xff000080, None)
        ASPVBScriptNumber = (0xff008080, None)
        ASPVBScriptStart = (0xff000000, None)
        ASPVBScriptString = (0xff800080, None)
        ASPVBScriptUnclosedString = (0xff000080, None)
        ASPXCComment = (0xff000000, None)
        Attribute = (0xff008080, None)
        CDATA = (0xff000000, None)
        Default = (0xff000000, None)
        Entity = (0xff800080, None)
        HTMLComment = (0xff808000, None)
        HTMLDoubleQuotedString = (0xff7f007f, None)
        HTMLNumber = (0xff007f7f, None)
        HTMLSingleQuotedString = (0xff7f007f, None)
        HTMLValue = (0xffff00ff, None)
        JavaScriptComment = (0xff007f00, None)
        JavaScriptCommentDoc = (0xff3f703f, None)
        JavaScriptCommentLine = (0xff007f00, None)
        JavaScriptDefault = (0xff000000, None)
        JavaScriptDoubleQuotedString = (0xff7f007f, None)
        JavaScriptKeyword = (0xff00007f, None)
        JavaScriptNumber = (0xff007f7f, None)
        JavaScriptRegex = (0xff000000, None)
        JavaScriptSingleQuotedString = (0xff7f007f, None)
        JavaScriptStart = (0xff7f7f00, None)
        JavaScriptSymbol = (0xff000000, None)
        JavaScriptUnclosedString = (0xff000000, None)
        JavaScriptWord = (0xff000000, None)
        OtherInTag = (0xff800080, None)
        PHPComment = (0xff999999, None)
        PHPCommentLine = (0xff666666, None)
        PHPDefault = (0xff000033, None)
        PHPDoubleQuotedString = (0xff007f00, None)
        PHPDoubleQuotedVariable = (0xff00007f, None)
        PHPKeyword = (0xff7f007f, None)
        PHPNumber = (0xffcc9900, None)
        PHPOperator = (0xff000000, None)
        PHPSingleQuotedString = (0xff009f00, None)
        PHPStart = (0xff0000ff, None)
        PHPVariable = (0xff00007f, None)
        PythonClassName = (0xff0000ff, None)
        PythonComment = (0xff007f00, None)
        PythonDefault = (0xff808080, None)
        PythonDoubleQuotedString = (0xff7f007f, None)
        PythonFunctionMethodName = (0xff007f7f, None)
        PythonIdentifier = (0xff000000, None)
        PythonKeyword = (0xff00007f, None)
        PythonNumber = (0xff007f7f, None)
        PythonOperator = (0xff000000, None)
        PythonSingleQuotedString = (0xff7f007f, None)
        PythonStart = (0xff808080, None)
        PythonTripleDoubleQuotedString = (0xff7f0000, None)
        PythonTripleSingleQuotedString = (0xff7f0000, None)
        SGMLBlockDefault = (0xff000066, None)
        SGMLCommand = (0xff000080, None)
        SGMLComment = (0xff808000, None)
        SGMLDefault = (0xff000080, None)
        SGMLDoubleQuotedString = (0xff800000, None)
        SGMLEntity = (0xff333333, None)
        SGMLError = (0xff800000, None)
        SGMLParameter = (0xff006600, None)
        SGMLParameterComment = (0xff000000, None)
        SGMLSingleQuotedString = (0xff993300, None)
        SGMLSpecial = (0xff3366ff, None)
        Script = (0xff000080, None)
        Tag = (0xff000080, None)
        UnknownAttribute = (0xffff0000, None)
        UnknownTag = (0xffff0000, None)
        VBScriptComment = (0xff008000, None)
        VBScriptDefault = (0xff000000, None)
        VBScriptIdentifier = (0xff000080, None)
        VBScriptKeyword = (0xff000080, None)
        VBScriptNumber = (0xff008080, None)
        VBScriptStart = (0xff000000, None)
        VBScriptString = (0xff800080, None)
        VBScriptUnclosedString = (0xff000080, None)
        XMLEnd = (0xff0000ff, None)
        XMLStart = (0xff0000ff, None)
        XMLTagEnd = (0xff000080, None)
    
    class IDL:
        Comment = (0xff007f00, None)
        CommentDoc = (0xff3f703f, None)
        CommentDocKeyword = (0xff3060a0, None)
        CommentDocKeywordError = (0xff804020, None)
        CommentLine = (0xff007f00, None)
        CommentLineDoc = (0xff3f703f, None)
        Default = (0xff808080, None)
        DoubleQuotedString = (0xff7f007f, None)
        GlobalClass = (0xff000000, None)
        HashQuotedString = (0xff007f00, None)
        Identifier = (0xff000000, None)
        InactiveComment = (0xff90b090, None)
        InactiveCommentDoc = (0xffd0d0d0, None)
        InactiveCommentDocKeyword = (0xffc0c0c0, None)
        InactiveCommentDocKeywordError = (0xffc0c0c0, None)
        InactiveCommentLine = (0xff90b090, None)
        InactiveCommentLineDoc = (0xffc0c0c0, None)
        InactiveDefault = (0xffc0c0c0, None)
        InactiveDoubleQuotedString = (0xffb090b0, None)
        InactiveGlobalClass = (0xffb0b0b0, None)
        InactiveHashQuotedString = (0xff000000, None)
        InactiveIdentifier = (0xffb0b0b0, None)
        InactiveKeyword = (0xff9090b0, None)
        InactiveKeywordSet2 = (0xffc0c0c0, None)
        InactiveNumber = (0xff90b090, None)
        InactiveOperator = (0xffb0b0b0, None)
        InactivePreProcessor = (0xffb0b090, None)
        InactivePreProcessorComment = (0xff000000, None)
        InactivePreProcessorCommentLineDoc = (0xffc0c0c0, None)
        InactiveRawString = (0xff000000, None)
        InactiveRegex = (0xff7faf7f, None)
        InactiveSingleQuotedString = (0xffb090b0, None)
        InactiveTripleQuotedVerbatimString = (0xff000000, None)
        InactiveUUID = (0xffc0c0c0, None)
        InactiveUnclosedString = (0xff000000, None)
        InactiveVerbatimString = (0xff90b090, None)
        Keyword = (0xff00007f, None)
        KeywordSet2 = (0xff000000, None)
        Number = (0xff007f7f, None)
        Operator = (0xff000000, None)
        PreProcessor = (0xff7f7f00, None)
        PreProcessorComment = (0xff659900, None)
        PreProcessorCommentLineDoc = (0xff3f703f, None)
        RawString = (0xff7f007f, None)
        Regex = (0xff3f7f3f, None)
        SingleQuotedString = (0xff7f007f, None)
        TripleQuotedVerbatimString = (0xff007f00, None)
        UUID = (0xff804080, None)
        UnclosedString = (0xff000000, None)
        VerbatimString = (0xff007f00, None)
    
    class Java:
        Comment = (0xff007f00, None)
        CommentDoc = (0xff3f703f, None)
        CommentDocKeyword = (0xff3060a0, None)
        CommentDocKeywordError = (0xff804020, None)
        CommentLine = (0xff007f00, None)
        CommentLineDoc = (0xff3f703f, None)
        Default = (0xff808080, None)
        DoubleQuotedString = (0xff7f007f, None)
        GlobalClass = (0xff000000, None)
        HashQuotedString = (0xff007f00, None)
        Identifier = (0xff000000, None)
        InactiveComment = (0xff90b090, None)
        InactiveCommentDoc = (0xffd0d0d0, None)
        InactiveCommentDocKeyword = (0xffc0c0c0, None)
        InactiveCommentDocKeywordError = (0xffc0c0c0, None)
        InactiveCommentLine = (0xff90b090, None)
        InactiveCommentLineDoc = (0xffc0c0c0, None)
        InactiveDefault = (0xffc0c0c0, None)
        InactiveDoubleQuotedString = (0xffb090b0, None)
        InactiveGlobalClass = (0xffb0b0b0, None)
        InactiveHashQuotedString = (0xff000000, None)
        InactiveIdentifier = (0xffb0b0b0, None)
        InactiveKeyword = (0xff9090b0, None)
        InactiveKeywordSet2 = (0xffc0c0c0, None)
        InactiveNumber = (0xff90b090, None)
        InactiveOperator = (0xffb0b0b0, None)
        InactivePreProcessor = (0xffb0b090, None)
        InactivePreProcessorComment = (0xff000000, None)
        InactivePreProcessorCommentLineDoc = (0xffc0c0c0, None)
        InactiveRawString = (0xff000000, None)
        InactiveRegex = (0xff7faf7f, None)
        InactiveSingleQuotedString = (0xffb090b0, None)
        InactiveTripleQuotedVerbatimString = (0xff000000, None)
        InactiveUUID = (0xffc0c0c0, None)
        InactiveUnclosedString = (0xff000000, None)
        InactiveVerbatimString = (0xff90b090, None)
        Keyword = (0xff00007f, None)
        KeywordSet2 = (0xff000000, None)
        Number = (0xff007f7f, None)
        Operator = (0xff000000, None)
        PreProcessor = (0xff7f7f00, None)
        PreProcessorComment = (0xff659900, None)
        PreProcessorCommentLineDoc = (0xff3f703f, None)
        RawString = (0xff7f007f, None)
        Regex = (0xff3f7f3f, None)
        SingleQuotedString = (0xff7f007f, None)
        TripleQuotedVerbatimString = (0xff007f00, None)
        UUID = (0xff000000, None)
        UnclosedString = (0xff000000, None)
        VerbatimString = (0xff007f00, None)
    
    class JavaScript:
        Comment = (0xff007f00, None)
        CommentDoc = (0xff3f703f, None)
        CommentDocKeyword = (0xff3060a0, None)
        CommentDocKeywordError = (0xff804020, None)
        CommentLine = (0xff007f00, None)
        CommentLineDoc = (0xff3f703f, None)
        Default = (0xff808080, None)
        DoubleQuotedString = (0xff7f007f, None)
        GlobalClass = (0xff000000, None)
        HashQuotedString = (0xff007f00, None)
        Identifier = (0xff000000, None)
        InactiveComment = (0xff90b090, None)
        InactiveCommentDoc = (0xffd0d0d0, None)
        InactiveCommentDocKeyword = (0xffc0c0c0, None)
        InactiveCommentDocKeywordError = (0xffc0c0c0, None)
        InactiveCommentLine = (0xff90b090, None)
        InactiveCommentLineDoc = (0xffc0c0c0, None)
        InactiveDefault = (0xffc0c0c0, None)
        InactiveDoubleQuotedString = (0xffb090b0, None)
        InactiveGlobalClass = (0xffb0b0b0, None)
        InactiveHashQuotedString = (0xff000000, None)
        InactiveIdentifier = (0xffb0b0b0, None)
        InactiveKeyword = (0xff9090b0, None)
        InactiveKeywordSet2 = (0xffc0c0c0, None)
        InactiveNumber = (0xff90b090, None)
        InactiveOperator = (0xffb0b0b0, None)
        InactivePreProcessor = (0xffb0b090, None)
        InactivePreProcessorComment = (0xff000000, None)
        InactivePreProcessorCommentLineDoc = (0xffc0c0c0, None)
        InactiveRawString = (0xff000000, None)
        InactiveRegex = (0xff7faf7f, None)
        InactiveSingleQuotedString = (0xffb090b0, None)
        InactiveTripleQuotedVerbatimString = (0xff000000, None)
        InactiveUUID = (0xffc0c0c0, None)
        InactiveUnclosedString = (0xff000000, None)
        InactiveVerbatimString = (0xff90b090, None)
        Keyword = (0xff00007f, None)
        KeywordSet2 = (0xff000000, None)
        Number = (0xff007f7f, None)
        Operator = (0xff000000, None)
        PreProcessor = (0xff7f7f00, None)
        PreProcessorComment = (0xff659900, None)
        PreProcessorCommentLineDoc = (0xff3f703f, None)
        RawString = (0xff7f007f, None)
        Regex = (0xff3f7f3f, None)
        SingleQuotedString = (0xff7f007f, None)
        TripleQuotedVerbatimString = (0xff007f00, None)
        UUID = (0xff000000, None)
        UnclosedString = (0xff000000, None)
        VerbatimString = (0xff007f00, None)
    
    class Lua:
        BasicFunctions = (0xff00007f, None)
        Character = (0xff7f007f, None)
        Comment = (0xff007f00, None)
        CoroutinesIOSystemFacilities = (0xff00007f, None)
        Default = (0xff000000, None)
        Identifier = (0xff000000, None)
        Keyword = (0xff00007f, None)
        KeywordSet5 = (0xff000000, None)
        KeywordSet6 = (0xff000000, None)
        KeywordSet7 = (0xff000000, None)
        KeywordSet8 = (0xff000000, None)
        Label = (0xff7f7f00, None)
        LineComment = (0xff007f00, None)
        LiteralString = (0xff7f007f, None)
        Number = (0xff007f7f, None)
        Operator = (0xff000000, None)
        Preprocessor = (0xff7f7f00, None)
        String = (0xff7f007f, None)
        StringTableMathsFunctions = (0xff00007f, None)
        UnclosedString = (0xff000000, None)
    
    class Makefile:
        Comment = (0xff007f00, None)
        Default = (0xff000000, None)
        Error = (0xffffff00, None)
        Operator = (0xff000000, None)
        Preprocessor = (0xff7f7f00, None)
        Target = (0xffa00000, None)
        Variable = (0xff000080, None)
    
    class Matlab:
        Command = (0xff7f7f00, None)
        Comment = (0xff007f00, None)
        Default = (0xff000000, None)
        DoubleQuotedString = (0xff7f007f, None)
        Identifier = (0xff000000, None)
        Keyword = (0xff00007f, None)
        Number = (0xff007f7f, None)
        Operator = (0xff000000, None)
        SingleQuotedString = (0xff7f007f, None)
    
    class Octave:
        Command = (0xff7f7f00, None)
        Comment = (0xff007f00, None)
        Default = (0xff000000, None)
        DoubleQuotedString = (0xff7f007f, None)
        Identifier = (0xff000000, None)
        Keyword = (0xff00007f, None)
        Number = (0xff007f7f, None)
        Operator = (0xff000000, None)
        SingleQuotedString = (0xff7f007f, None)
    
    class PO:
        Comment = (0xff007f00, None)
        Default = (0xff000000, None)
        Flags = (0xff000000, None)
        Fuzzy = (0xff000000, None)
        MessageContext = (0xff000000, None)
        MessageContextText = (0xff000000, None)
        MessageContextTextEOL = (0xff000000, None)
        MessageId = (0xff000000, None)
        MessageIdText = (0xff000000, None)
        MessageIdTextEOL = (0xff000000, None)
        MessageString = (0xff000000, None)
        MessageStringText = (0xff000000, None)
        MessageStringTextEOL = (0xff000000, None)
        ProgrammerComment = (0xff000000, None)
        Reference = (0xff000000, None)
    
    class POV:
        BadDirective = (0xff804020, None)
        Comment = (0xff007f00, None)
        CommentLine = (0xff007f00, None)
        Default = (0xffff0080, None)
        Directive = (0xff7f7f00, None)
        Identifier = (0xff000000, None)
        KeywordSet6 = (0xff00007f, None)
        KeywordSet7 = (0xff00007f, None)
        KeywordSet8 = (0xff00007f, None)
        Number = (0xff007f7f, None)
        ObjectsCSGAppearance = (0xff00007f, None)
        Operator = (0xff000000, None)
        PredefinedFunctions = (0xff00007f, None)
        PredefinedIdentifiers = (0xff00007f, None)
        String = (0xff7f007f, None)
        TypesModifiersItems = (0xff00007f, None)
        UnclosedString = (0xff000000, None)
    
    class Pascal:
        Asm = (0xff804080, None)
        Character = (0xff7f007f, None)
        Comment = (0xff007f00, None)
        CommentLine = (0xff007f00, None)
        CommentParenthesis = (0xff007f00, None)
        Default = (0xff808080, None)
        HexNumber = (0xff007f7f, None)
        Identifier = (0xff000000, None)
        Keyword = (0xff00007f, None)
        Number = (0xff007f7f, None)
        Operator = (0xff000000, None)
        PreProcessor = (0xff7f7f00, None)
        PreProcessorParenthesis = (0xff7f7f00, None)
        SingleQuotedString = (0xff7f007f, None)
        UnclosedString = (0xff000000, None)
    
    class Perl:
        Array = (0xff000000, None)
        BacktickHereDocument = (0xff7f007f, None)
        BacktickHereDocumentVar = (0xffd00000, None)
        Backticks = (0xffffff00, None)
        BackticksVar = (0xffd00000, None)
        Comment = (0xff007f00, None)
        DataSection = (0xff600000, None)
        Default = (0xff808080, None)
        DoubleQuotedHereDocument = (0xff7f007f, None)
        DoubleQuotedHereDocumentVar = (0xffd00000, None)
        DoubleQuotedString = (0xff7f007f, None)
        DoubleQuotedStringVar = (0xffd00000, None)
        Error = (0xffffff00, None)
        FormatBody = (0xffc000c0, None)
        FormatIdentifier = (0xffc000c0, None)
        Hash = (0xff000000, None)
        HereDocumentDelimiter = (0xff000000, None)
        Identifier = (0xff000000, None)
        Keyword = (0xff00007f, None)
        Number = (0xff007f7f, None)
        Operator = (0xff000000, None)
        POD = (0xff004000, None)
        PODVerbatim = (0xff004000, None)
        QuotedStringQ = (0xff7f007f, None)
        QuotedStringQQ = (0xff7f007f, None)
        QuotedStringQQVar = (0xffd00000, None)
        QuotedStringQR = (0xff000000, None)
        QuotedStringQRVar = (0xffd00000, None)
        QuotedStringQW = (0xff000000, None)
        QuotedStringQX = (0xffffff00, None)
        QuotedStringQXVar = (0xffd00000, None)
        Regex = (0xff000000, None)
        RegexVar = (0xffd00000, None)
        Scalar = (0xff000000, None)
        SingleQuotedHereDocument = (0xff7f007f, None)
        SingleQuotedString = (0xff7f007f, None)
        SubroutinePrototype = (0xff000000, None)
        Substitution = (0xff000000, None)
        SubstitutionVar = (0xffd00000, None)
        SymbolTable = (0xff000000, None)
        Translation = (0xff000000, None)
    
    class PostScript:
        ArrayParenthesis = (0xff00007f, None)
        BadStringCharacter = (0xffffff00, None)
        Base85String = (0xff7f007f, None)
        Comment = (0xff007f00, None)
        DSCComment = (0xff3f703f, None)
        DSCCommentValue = (0xff3060a0, None)
        Default = (0xff000000, None)
        DictionaryParenthesis = (0xff3060a0, None)
        HexString = (0xff3f7f3f, None)
        ImmediateEvalLiteral = (0xff7f7f00, None)
        Keyword = (0xff00007f, None)
        Literal = (0xff7f7f00, None)
        Name = (0xff000000, None)
        Number = (0xff007f7f, None)
        ProcedureParenthesis = (0xff000000, None)
        Text = (0xff7f007f, None)
    
    class Properties:
        Assignment = (0xffb06000, None)
        Comment = (0xff007f7f, None)
        Default = (0xff000000, None)
        DefaultValue = (0xff7f7f00, None)
        Key = (0xff000000, None)
        Section = (0xff7f007f, None)
    
    class Python:
        ClassName = (0xff0000ff, None)
        Comment = (0xff007f00, None)
        CommentBlock = (0xff7f7f7f, None)
        Decorator = (0xff805000, None)
        Default = (0xff000000, None)
        DoubleQuotedString = (0xff7f007f, None)
        FunctionMethodName = (0xff007f7f, None)
        HighlightedIdentifier = (0xff407090, None)
        Identifier = (0xff000000, None)
        Inconsistent = (0xff007f00, None)
        Keyword = (0xff00007f, None)
        NoWarning = (0xff808080, None)
        Number = (0xff007f7f, None)
        Operator = (0xff000000, None)
        SingleQuotedString = (0xff7f007f, None)
        Spaces = (0xff7f007f, None)
        Tabs = (0xff7f007f, None)
        TabsAfterSpaces = (0xff007f7f, None)
        TripleDoubleQuotedString = (0xff7f0000, None)
        TripleSingleQuotedString = (0xff7f0000, None)
        UnclosedString = (0xff000000, None)
    
    class Ruby:
        Backticks = (0xffffff00, None)
        ClassName = (0xff0000ff, None)
        ClassVariable = (0xff8000b0, None)
        Comment = (0xff007f00, None)
        DataSection = (0xff600000, None)
        Default = (0xff808080, None)
        DemotedKeyword = (0xff00007f, None)
        DoubleQuotedString = (0xff7f007f, None)
        Error = (0xff000000, None)
        FunctionMethodName = (0xff007f7f, None)
        Global = (0xff800080, None)
        HereDocument = (0xff7f007f, None)
        HereDocumentDelimiter = (0xff000000, None)
        Identifier = (0xff000000, None)
        InstanceVariable = (0xffb00080, None)
        Keyword = (0xff00007f, None)
        ModuleName = (0xffa000a0, None)
        Number = (0xff007f7f, None)
        Operator = (0xff000000, None)
        POD = (0xff004000, None)
        PercentStringQ = (0xff7f007f, None)
        PercentStringq = (0xff7f007f, None)
        PercentStringr = (0xff000000, None)
        PercentStringw = (0xff000000, None)
        PercentStringx = (0xffffff00, None)
        Regex = (0xff000000, None)
        SingleQuotedString = (0xff7f007f, None)
        Stderr = (0xff000000, None)
        Stdin = (0xff000000, None)
        Stdout = (0xff000000, None)
        Symbol = (0xffc0a030, None)
    
    class SQL:
        Comment = (0xff007f00, None)
        CommentDoc = (0xff7f7f7f, None)
        CommentDocKeyword = (0xff3060a0, None)
        CommentDocKeywordError = (0xff804020, None)
        CommentLine = (0xff007f00, None)
        CommentLineHash = (0xff007f00, None)
        Default = (0xff808080, None)
        DoubleQuotedString = (0xff7f007f, None)
        Identifier = (0xff000000, None)
        Keyword = (0xff00007f, None)
        KeywordSet5 = (0xff4b0082, None)
        KeywordSet6 = (0xffb00040, None)
        KeywordSet7 = (0xff8b0000, None)
        KeywordSet8 = (0xff800080, None)
        Number = (0xff007f7f, None)
        Operator = (0xff000000, None)
        PlusComment = (0xff007f00, None)
        PlusKeyword = (0xff7f7f00, None)
        PlusPrompt = (0xff007f00, None)
        QuotedIdentifier = (0xff000000, None)
        SingleQuotedString = (0xff7f007f, None)
    
    class Spice:
        Command = (0xff00007f, None)
        Comment = (0xff007f00, None)
        Default = (0xff808080, None)
        Delimiter = (0xff000000, None)
        Function = (0xff00007f, None)
        Identifier = (0xff000000, None)
        Number = (0xff007f7f, None)
        Parameter = (0xff0040e0, None)
        Value = (0xff7f007f, None)
    
    class TCL:
        Comment = (0xff007f00, None)
        CommentBlock = (0xff000000, None)
        CommentBox = (0xff007f00, None)
        CommentLine = (0xff007f00, None)
        Default = (0xff808080, None)
        ExpandKeyword = (0xff00007f, None)
        ITCLKeyword = (0xff00007f, None)
        Identifier = (0xff00007f, None)
        KeywordSet6 = (0xff00007f, None)
        KeywordSet7 = (0xff00007f, None)
        KeywordSet8 = (0xff00007f, None)
        KeywordSet9 = (0xff00007f, None)
        Modifier = (0xff7f007f, None)
        Number = (0xff007f7f, None)
        Operator = (0xff000000, None)
        QuotedKeyword = (0xff7f007f, None)
        QuotedString = (0xff7f007f, None)
        Substitution = (0xff7f7f00, None)
        SubstitutionBrace = (0xff7f7f00, None)
        TCLKeyword = (0xff00007f, None)
        TkCommand = (0xff00007f, None)
        TkKeyword = (0xff00007f, None)
    
    class TeX:
        Command = (0xff007f00, None)
        Default = (0xff3f3f3f, None)
        Group = (0xff7f0000, None)
        Special = (0xff007f7f, None)
        Symbol = (0xff7f7f00, None)
        Text = (0xff000000, None)
    
    class VHDL:
        Attribute = (0xff804020, None)
        Comment = (0xff007f00, None)
        CommentLine = (0xff3f7f3f, None)
        Default = (0xff800080, None)
        Identifier = (0xff000000, None)
        Keyword = (0xff00007f, None)
        KeywordSet7 = (0xff804020, None)
        Number = (0xff007f7f, None)
        Operator = (0xff000000, None)
        StandardFunction = (0xff808020, None)
        StandardOperator = (0xff007f7f, None)
        StandardPackage = (0xff208020, None)
        StandardType = (0xff208080, None)
        String = (0xff7f007f, None)
        UnclosedString = (0xff000000, None)
    
    class Verilog:
        Comment = (0xff007f00, None)
        CommentBang = (0xff3f7f3f, None)
        CommentLine = (0xff007f00, None)
        Default = (0xff808080, None)
        Identifier = (0xff000000, None)
        Keyword = (0xff00007f, None)
        KeywordSet2 = (0xff007f7f, None)
        Number = (0xff007f7f, None)
        Operator = (0xff007070, None)
        Preprocessor = (0xff7f7f00, None)
        String = (0xff7f007f, None)
        SystemTask = (0xff804020, None)
        UnclosedString = (0xff000000, None)
        UserKeywordSet = (0xff2a00ff, None)
    
    class XML:
        ASPAtStart = (0xff000000, None)
        ASPJavaScriptComment = (0xff007f00, None)
        ASPJavaScriptCommentDoc = (0xff7f7f7f, None)
        ASPJavaScriptCommentLine = (0xff007f00, None)
        ASPJavaScriptDefault = (0xff000000, None)
        ASPJavaScriptDoubleQuotedString = (0xff7f007f, None)
        ASPJavaScriptKeyword = (0xff00007f, None)
        ASPJavaScriptNumber = (0xff007f7f, None)
        ASPJavaScriptRegex = (0xff000000, None)
        ASPJavaScriptSingleQuotedString = (0xff7f007f, None)
        ASPJavaScriptStart = (0xff7f7f00, None)
        ASPJavaScriptSymbol = (0xff000000, None)
        ASPJavaScriptUnclosedString = (0xff000000, None)
        ASPJavaScriptWord = (0xff000000, None)
        ASPPythonClassName = (0xff0000ff, None)
        ASPPythonComment = (0xff007f00, None)
        ASPPythonDefault = (0xff808080, None)
        ASPPythonDoubleQuotedString = (0xff7f007f, None)
        ASPPythonFunctionMethodName = (0xff007f7f, None)
        ASPPythonIdentifier = (0xff000000, None)
        ASPPythonKeyword = (0xff00007f, None)
        ASPPythonNumber = (0xff007f7f, None)
        ASPPythonOperator = (0xff000000, None)
        ASPPythonSingleQuotedString = (0xff7f007f, None)
        ASPPythonStart = (0xff808080, None)
        ASPPythonTripleDoubleQuotedString = (0xff7f0000, None)
        ASPPythonTripleSingleQuotedString = (0xff7f0000, None)
        ASPStart = (0xff000000, None)
        ASPVBScriptComment = (0xff008000, None)
        ASPVBScriptDefault = (0xff000000, None)
        ASPVBScriptIdentifier = (0xff000080, None)
        ASPVBScriptKeyword = (0xff000080, None)
        ASPVBScriptNumber = (0xff008080, None)
        ASPVBScriptStart = (0xff000000, None)
        ASPVBScriptString = (0xff800080, None)
        ASPVBScriptUnclosedString = (0xff000080, None)
        ASPXCComment = (0xff000000, None)
        Attribute = (0xff008080, None)
        CDATA = (0xff800000, None)
        Default = (0xff000000, None)
        Entity = (0xff800080, None)
        HTMLComment = (0xff808000, None)
        HTMLDoubleQuotedString = (0xff7f007f, None)
        HTMLNumber = (0xff007f7f, None)
        HTMLSingleQuotedString = (0xff7f007f, None)
        HTMLValue = (0xff608060, None)
        JavaScriptComment = (0xff007f00, None)
        JavaScriptCommentDoc = (0xff3f703f, None)
        JavaScriptCommentLine = (0xff007f00, None)
        JavaScriptDefault = (0xff000000, None)
        JavaScriptDoubleQuotedString = (0xff7f007f, None)
        JavaScriptKeyword = (0xff00007f, None)
        JavaScriptNumber = (0xff007f7f, None)
        JavaScriptRegex = (0xff000000, None)
        JavaScriptSingleQuotedString = (0xff7f007f, None)
        JavaScriptStart = (0xff7f7f00, None)
        JavaScriptSymbol = (0xff000000, None)
        JavaScriptUnclosedString = (0xff000000, None)
        JavaScriptWord = (0xff000000, None)
        OtherInTag = (0xff800080, None)
        PHPComment = (0xff999999, None)
        PHPCommentLine = (0xff666666, None)
        PHPDefault = (0xff000033, None)
        PHPDoubleQuotedString = (0xff007f00, None)
        PHPDoubleQuotedVariable = (0xff00007f, None)
        PHPKeyword = (0xff7f007f, None)
        PHPNumber = (0xffcc9900, None)
        PHPOperator = (0xff000000, None)
        PHPSingleQuotedString = (0xff009f00, None)
        PHPStart = (0xff800000, None)
        PHPVariable = (0xff00007f, None)
        PythonClassName = (0xff0000ff, None)
        PythonComment = (0xff007f00, None)
        PythonDefault = (0xff808080, None)
        PythonDoubleQuotedString = (0xff7f007f, None)
        PythonFunctionMethodName = (0xff007f7f, None)
        PythonIdentifier = (0xff000000, None)
        PythonKeyword = (0xff00007f, None)
        PythonNumber = (0xff007f7f, None)
        PythonOperator = (0xff000000, None)
        PythonSingleQuotedString = (0xff7f007f, None)
        PythonStart = (0xff808080, None)
        PythonTripleDoubleQuotedString = (0xff7f0000, None)
        PythonTripleSingleQuotedString = (0xff7f0000, None)
        SGMLBlockDefault = (0xff000066, None)
        SGMLCommand = (0xff000080, None)
        SGMLComment = (0xff808000, None)
        SGMLDefault = (0xff000080, None)
        SGMLDoubleQuotedString = (0xff800000, None)
        SGMLEntity = (0xff333333, None)
        SGMLError = (0xff800000, None)
        SGMLParameter = (0xff006600, None)
        SGMLParameterComment = (0xff000000, None)
        SGMLSingleQuotedString = (0xff993300, None)
        SGMLSpecial = (0xff3366ff, None)
        Script = (0xff000080, None)
        Tag = (0xff000080, None)
        UnknownAttribute = (0xff008080, None)
        UnknownTag = (0xff000080, None)
        VBScriptComment = (0xff008000, None)
        VBScriptDefault = (0xff000000, None)
        VBScriptIdentifier = (0xff000080, None)
        VBScriptKeyword = (0xff000080, None)
        VBScriptNumber = (0xff008080, None)
        VBScriptStart = (0xff000000, None)
        VBScriptString = (0xff800080, None)
        VBScriptUnclosedString = (0xff000080, None)
        XMLEnd = (0xff800080, None)
        XMLStart = (0xff800080, None)
        XMLTagEnd = (0xff000080, None)
    
    class YAML:
        Comment = (0xff008800, None)
        Default = (0xff000000, None)
        DocumentDelimiter = (0xffffffff, None)
        Identifier = (0xff000088, None)
        Keyword = (0xff880088, None)
        Number = (0xff880000, None)
        Operator = (0xff000000, None)
        Reference = (0xff008888, None)
        SyntaxErrorMarker = (0xffffffff, None)
        TextBlockMarker = (0xff333366, None)


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
    




