
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
        The Tango Icons I created are released under the GNU General Public License version 3.


    Eric6 LICENSE:
        Eric6 IDE is licensed under the GNU General Public License version 3


    Nuitka LICENSE:
        Nuitka is a Python compiler compatible with Ex.Co..
        Nuitka is licensed under the Apache license.
"""


##  FILE DESCRIPTION:
##      Custom lexers used by the BasicWidgets in the forms.py module

import keyword
import builtins
import re
import PyQt4.QtCore
import PyQt4.QtGui
import PyQt4.Qsci
import functions
import data
#Try importing the Cython module
try:
    import cython_lexers
    cython_found = True
except Exception as ex:
    print(ex)
    cython_found = False
    

class Text(PyQt4.Qsci.QsciLexerCustom):
    """Lexer for styling normal text documents"""
    #Class variables
    default_font = PyQt4.QtGui.QFont('Courier', 10)
    styles = {
        "Default" : 0
    }
    
    def __init__(self, parent=None):
        """Overridden initialization"""
        #Initialize superclass
        super().__init__()
        #Set the font colors
        self.setFont(self.default_font, 0)
        #Reset autoindentation style
        self.setAutoIndentStyle(0)
        #Set the theme
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        def set_color(color, style, bold=False):
            self.setColor(
                color, 
                self.styles[style]
            )
            if bold == True:
                self.setFont(
                    PyQt4.QtGui.QFont(
                        'Courier', 
                        10, 
                        weight=PyQt4.QtGui.QFont.Bold
                    ), 
                    self.styles[style]
                )
        # Papers
        self.setPaper(
            PyQt4.QtGui.QColor(theme.Paper.Python.Default), 
            self.styles["Default"]
        )
        # Fonts
        set_color(PyQt4.QtGui.QColor(theme.Font.Python.Default[0]), "Default")
    
    def language(self):
        return "Plain text"
    
    def description(self, style):
        if style == 0:
            description = "Text"
        else:
            description = ""
        return description
    
    def styleText(self, start, end):
        self.startStyling(start)
        self.setStyling(end - start, 0)


class Python(PyQt4.Qsci.QsciLexerPython):
    """Standard Python lexer with added keywords from built-in functions"""
    #Class variables
    _kwrds = None
    styles = {
        "Default" : 0,
        "Comment" : 1,
        "Number" : 2,
        "DoubleQuotedString" : 3,
        "SingleQuotedString" : 4,
        "Keyword" : 5,
        "TripleSingleQuotedString" : 6,
        "TripleDoubleQuotedString" : 7,
        "ClassName" : 8,
        "FunctionMethodName" : 9,
        "Operator" : 10,
        "Identifier" : 11,
        "CommentBlock" : 12,
        "UnclosedString" : 13,
        "HighlightedIdentifier" : 14,
        "Decorator" : 15
    }
    
    def __init__(self, parent=None):
        """Overridden initialization"""
        #Initialize superclass
        super().__init__()
        #Initialize list with keywords
        self._kwrds = keyword.kwlist
        #Extend the list with built-in functions
        self._kwrds.extend([bi for bi in builtins.__dict__.keys()])
        #Transform list into a single string with spaces between list items
        self._kwrds = " ".join(self._kwrds)
        #Set the theme
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        def set_color(color, style, bold=False):
            self.setColor(
                color, 
                self.styles[style]
            )
            if bold == True:
                self.setFont(
                    PyQt4.QtGui.QFont(
                        'Courier', 
                        10, 
                        weight=PyQt4.QtGui.QFont.Bold
                    ), 
                    self.styles[style]
                )
        for style in self.styles:
            # Papers
            paper = PyQt4.QtGui.QColor(getattr(theme.Paper.Python, style))
            self.setPaper(paper, self.styles[style])
            # Fonts
            color_string, bold = getattr(theme.Font.Python, style)
            color = PyQt4.QtGui.QColor(color_string)
            set_color(color, style, bold)
    
    def keywords(self, state):
        """
        Overridden method for determining keywords,
        read the QScintilla QsciLexer class documentation on the Riverbank website.
        """
        keywords = None
        #Only state 1 returns keywords, don't know why? Check the C++ Scintilla lexer source files.
        if state == 1:
            keywords = self._kwrds
        return keywords


class Cython(PyQt4.Qsci.QsciLexerPython):
    """Cython - basically Python with added keywords"""
    #Class variables
    _kwrds = None
    styles = {
        "Default" : 0,
        "Comment" : 1,
        "Number" : 2,
        "DoubleQuotedString" : 3,
        "SingleQuotedString" : 4,
        "Keyword" : 5,
        "TripleSingleQuotedString" : 6,
        "TripleDoubleQuotedString" : 7,
        "ClassName" : 8,
        "FunctionMethodName" : 9,
        "Operator" : 10,
        "Identifier" : 11,
        "CommentBlock" : 12,
        "UnclosedString" : 13,
        "HighlightedIdentifier" : 14,
        "Decorator" : 15
    }
    _c_kwrds = [
        "void", "char",  "int", "long", "short", "double", "float", 
        "const", "unsigned", "inline"
    ]
    _cython_kwrds = [
        "by", "cdef", "cimport", "cpdef", "ctypedef", "enum", "except?", 
        "extern", "gil", "include", "nogil", "property", "public", 
        "readonly", "struct", "union", "DEF", "IF", "ELIF", "ELSE"
    ]
    
    
    def __init__(self,  parent=None):
        """Overridden initialization"""
        #Initialize superclass
        super().__init__()
        #Initialize list with keywords
        self._kwrds = keyword.kwlist
        #Extend the list with built-in functions
        self._kwrds.extend([bi for bi in builtins.__dict__.keys()])
        #Add the C keywords supported by Cython
        self._kwrds.extend(self._c_kwrds)
        #Add the Cython keywords
        self._kwrds.extend(self._cython_kwrds)
        #Transform list into a single string with spaces between list items
        self._kwrds = " ".join(self._kwrds)
        #Reset autoindentation style
        self.setAutoIndentStyle(0)
        #Set the theme
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        def set_color(color, style, bold=False):
            self.setColor(
                color, 
                self.styles[style]
            )
            if bold == True:
                self.setFont(
                    PyQt4.QtGui.QFont(
                        'Courier', 
                        10, 
                        weight=PyQt4.QtGui.QFont.Bold
                    ), 
                    self.styles[style]
                )
        for style in self.styles:
            # Papers
            self.setPaper(
                PyQt4.QtGui.QColor(theme.Paper.Python.Default), 
                self.styles[style]
            )
            # Fonts
            color_string, bold = getattr(theme.Font.Python, style)
            color = PyQt4.QtGui.QColor(color_string)
            set_color(color, style, bold)
    
    def keywords(self, state):
        """
        Overridden method for determining keywords,
        read the QScintilla QsciLexer class documentation on the Riverbank website.
        """
        keywrds= None
        #Only state 1 returns keywords, don't know why? Check the C++ Scintilla lexer source files.
        if state == 1:
            keywrds = self._kwrds
        return keywrds


class Oberon(PyQt4.Qsci.QsciLexerCustom):
    """
    Custom lexer for the Oberon/Oberon-2/Modula/Modula-2 programming languages
    """
    styles = {
        "Default" : 0,
        "Comment" : 1,
        "Keyword" : 2,
        "String" : 3,
        "Procedure" : 4,
        "Module" : 5,
        "Number" : 6,
        "Type" : 7
    }
    
    #Class variables
    default_color       = PyQt4.QtGui.QColor(data.theme.Font.Oberon.Default[0])
    default_paper       = PyQt4.QtGui.QColor(data.theme.Paper.Oberon.Default)
    default_font        = PyQt4.QtGui.QFont('Courier', 10)
    keyword_list        = [
        'ARRAY', 'IMPORT', 'RETURN', 'BEGIN', 'IN',
        'THEN', 'BY', 'IS', 'TO', 'CASE', 'LOOP', 'Type', 
        'CONST', 'MOD', 'UNTIL', 'DIV', 'MODULE', 'VAR', 
        'DO', 'NIL', 'WHILE', 'ELSE', 'OF', 'WITH', 
        'ELSIF', 'OR', 'END', 'POINTER', 'EXIT',
        'PROCEDURE', 'FOR', 'RECORD', 'IF', 'REPEAT'
    ]
    types_list          =   [
        'BOOLEAN', 'CHAR', 'SHORTINT', 'INTEGER', 
        'LONGINT', 'REAL', 'LONGREAL', 'SET'
    ]
    splitter            = re.compile(r"(\(\*|\*\)|\s+|\w+|\W)")

    def __init__(self,  parent=None):
        """Overridden initialization"""
        #Initialize superclass
        super().__init__()
        #Set the default style values
        self.setDefaultColor(self.default_color)
        self.setDefaultPaper(self.default_paper)
        self.setDefaultFont(self.default_font)
        #Reset autoindentation style
        self.setAutoIndentStyle(0)
        #Set the theme
        self.set_theme(data.theme)
    
    def language(self):
        return "Oberon/Modula-2/Component Pascal"
    
    def description(self, style):
        if style <= 7:
            description = "Custom lexer for the Oberon/Oberon-2/Modula/Modula-2/Component Pascal programming languages"
        else:
            description = ""
        return description
    
    def set_theme(self, theme):
        def set_color(color, style, bold=False):
            self.setColor(
                color, 
                self.styles[style]
            )
            if bold == True:
                self.setFont(
                    PyQt4.QtGui.QFont(
                        'Courier', 
                        10, 
                        weight=PyQt4.QtGui.QFont.Bold
                    ), 
                    self.styles[style]
                )
        for style in self.styles:
            # Papers
            self.setPaper(
                PyQt4.QtGui.QColor(theme.Paper.Oberon.Default), 
                self.styles[style]
            )
            # Fonts
            color_string, bold = getattr(theme.Font.Oberon, style)
            color = PyQt4.QtGui.QColor(color_string)
            set_color(color, style, bold)

    def styleText(self, start, end):
        """
        Overloaded method for styling text.
        NOTE:
            Very slow if done in Python!
            Using the Cython version is better.
            The fastest would probably be adding the lexer directly into
            the QScintilla source. Maybe never :-)
        """
        #Get the global cython flag
        global cython_found
        if cython_found == True:
            #Cython module found
            cython_lexers.style_oberon(start, end, self, self.editor())
        else:
            #Style in pure Python, VERY SLOW!
            editor = self.editor()
            if editor is None:
                return
            #Initialize the styling
            self.startStyling(start)
            #Scintilla works with bytes, so we have to adjust the start and end boundaries
            text = bytearray(editor.text(), "utf-8")[start:end].decode("utf-8")
            #Loop optimizations
            setStyling  = self.setStyling
            kw_list     = self.keyword_list
            types_list  = self.types_list
            DEF = self.styles["Default"]
            KWD = self.styles["Keyword"]
            COM = self.styles["Comment"]
            STR = self.styles["String"]
            PRO = self.styles["Procedure"]
            MOD = self.styles["Module"]
            NUM = self.styles["Number"]
            TYP = self.styles["Type"]
            #Initialize comment state and split the text into tokens
            commenting  = False
            stringing           = False
            tokens = [(token, len(bytearray(token, "utf-8"))) for token in self.splitter.findall(text)]
            #Check if there is a style(comment, string, ...) stretching on from the previous line
            if start != 0:
                previous_style = editor.SendScintilla(editor.SCI_GETSTYLEAT, start - 1)
                if previous_style == COM:
                    commenting = True
            #Style the tokens accordingly
            for i, token in enumerate(tokens):
                if commenting == True:
                    #Continuation of comment
                    setStyling(token[1], COM)
                    #Check if comment ends
                    if token[0] == "*)":
                        commenting = False
                elif stringing == True:
                    #Continuation of a string
                    setStyling(token[1], STR)
                    #Check if string ends
                    if token[0] == "\"" or "\n" in token[0]:
                        stringing = False
                elif token[0] == "\"":
                    #Start of a string
                    setStyling(token[1], STR)
                    stringing = True
                elif token[0] in kw_list:
                    #Keyword
                    setStyling(token[1], KWD)
                elif token[0] in types_list:
                    #Keyword
                    setStyling(token[1], TYP)
                elif token[0] == "(*":
                    #Start of a comment
                    setStyling(token[1], COM)
                    commenting = True
                elif i > 1 and tokens[i-2][0] == "PROCEDURE":
                    #Procedure name
                    setStyling(token[1], PRO)
                elif i > 1 and tokens[i-2][0] == "MODULE":
                    #Module name (beginning)
                    setStyling(token[1], MOD)
                elif (i > 1 and tokens[i-2][0] == "END") and (len(tokens)-1 >= i+1):
                    #Module or procedure name (name)
                    if ";" in tokens[i+1][0]:
                        #Procedure end
                        setStyling(token[1], PRO)
                    elif "." in tokens[i+1][0]:
                        #Module end
                        setStyling(token[1], MOD)
                    else:
                        setStyling(token[1], DEF)
                elif functions.is_number(token[0]):
                    #Number
                    setStyling(token[1], NUM)
                else:
                    setStyling(token[1], DEF)

class Ada(PyQt4.Qsci.QsciLexerCustom):
    """Custom lexer for the Ada programming languages"""
    styles = {
        "Default" : 0,
        "Comment" : 1,
        "Keyword" : 2,
        "String" : 3,
        "Procedure" : 4,
        "Number" : 5,
        "Type" : 6, 
        "Package" : 7
    }
    
    #Class variables
    default_color       = PyQt4.QtGui.QColor(data.theme.Font.Ada.Default[0])
    default_paper       = PyQt4.QtGui.QColor(data.theme.Paper.Ada.Default)
    default_font        = PyQt4.QtGui.QFont('Courier', 10)
    keyword_list        =   [ 
        "abort", "else", "new", "return",
        "abs", "elsif", "not", "reverse",
        "abstract", "end", "null", "accept",
        "entry", "select", "access","exception",
        "of", "separate", "aliased","exit",
        "or", "some", "all", "others", "subtype",
        "and", "for", "out", "synchronized",
        "array", "function", "overriding", "at",
        "tagged", "generic", "package", "task",
        "begin", "goto", "pragma", "terminate",
        "body", "private", "then", "if",
        "procedure", "type", "case", "in", "protected",
        "constant", "interface", "until",
        "is", "raise", "use", "declare",
        "range", "delay", "limited", "record",
        "when", "delta", "loop", "rem",
        "while", "digits", "renames","with", "do",
        "mod", "requeue", "xor",
    ]
    splitter            = re.compile(r"(\-\-|\s+|\w+|\W)")
    
    def __init__(self,  parent=None):
        """Overridden initialization"""
        #Initialize superclass
        super().__init__()
        #Set the default style values
        self.setDefaultColor(self.default_color)
        self.setDefaultPaper(self.default_paper)
        self.setDefaultFont(self.default_font)
        #Reset autoindentation style
        self.setAutoIndentStyle(0)
        #Set the theme
        self.set_theme(data.theme)
    
    def language(self):
        return "Ada"
    
    def description(self, style):
        if style <= 7:
            description = "Custom lexer for the Ada programming languages"
        else:
            description = ""
        return description
    
    def set_theme(self, theme):
        def set_color(color, style, bold=False):
            self.setColor(
                color, 
                self.styles[style]
            )
            if bold == True:
                self.setFont(
                    PyQt4.QtGui.QFont(
                        'Courier', 
                        10, 
                        weight=PyQt4.QtGui.QFont.Bold
                    ), 
                    self.styles[style]
                )
        for style in self.styles:
            # Papers
            self.setPaper(
                PyQt4.QtGui.QColor(theme.Paper.Ada.Default), 
                self.styles[style]
            )
            # Fonts
            color_string, bold = getattr(theme.Font.Ada, style)
            color = PyQt4.QtGui.QColor(color_string)
            set_color(color, style, bold)
        
    def styleText(self, start, end):
        """
        Overloaded method for styling text.
        NOTE:
            Very slow if done in Python!
            Using the Cython version is better.
            The fastest would probably be adding the lexer directly into
            the QScintilla source. Maybe never :-)
        """
        #Get the global cython flag
        global cython_found
        if cython_found == True:
            #Cython module found
            cython_lexers.style_ada(start, end, self, self.editor())
        else:
            #Style in pure Python, VERY SLOW!
            editor = self.editor()
            if editor is None:
                return
            #Initialize the procedure/package counter
            pp_counter = []
            #Initialize the styling
            self.startStyling(0)
            #Scintilla works with bytes, so we have to adjust the start and end boundaries
            text = bytearray(editor.text().lower(), "utf-8").decode("utf-8")
            #Loop optimizations
            setStyling  = self.setStyling
            kw_list     = self.keyword_list
            DEF = self.styles.Default
            KWD = self.styles.KEYWORD
            COM = self.styles.Comment
            STR = self.styles.String
            PRO = self.styles.PROCEDURE
            NUM = self.styles.Number
            PAC = self.styles.PACKAGE
            #Initialize comment state and split the text into tokens
            commenting  = False
            stringing   = False
            tokens = [(token, len(bytearray(token, "utf-8"))) for token in self.splitter.findall(text)]
            #Style the tokens accordingly
            for i, token in enumerate(tokens):
                if commenting == True:
                    #Continuation of comment
                    setStyling(token[1], COM)
                    #Check if comment ends
                    if "\n" in token[0]:
                        commenting = False
                elif stringing == True:
                    #Continuation of a string
                    setStyling(token[1], STR)
                    #Check if string ends
                    if token[0] == "\"" or "\n" in token[0]:
                        stringing = False
                elif token[0] == "\"":
                    #Start of a string
                    setStyling(token[1], STR)
                    stringing = True
                elif token[0] in kw_list:
                    #Keyword
                    setStyling(token[1], KWD)
                elif token[0] == "--":
                    #Start of a comment
                    setStyling(token[1], COM)
                    commenting = True
                elif i > 1 and tokens[i-2][0] == "procedure":
                    #Procedure name
                    setStyling(token[1], PRO)
                    #Mark the procedure
                    if tokens[i+1][0] != ";":
                        pp_counter.append("PROCEDURE")
                elif i > 1 and (tokens[i-2][0] == "package" or tokens[i-2][0] == "body"):
                    #Package name
                    setStyling(token[1], PAC)
                    #Mark the package
                    pp_counter.append("PACKAGE")
                elif (i > 1 and tokens[i-2][0] == "end") and (len(tokens)-1 >= i+1):
                    #Package or procedure name end
                    if len(pp_counter) > 0:
                        if pp_counter.pop() == "PACKAGE":
                            setStyling(token[1], PAC)
                        else:
                            setStyling(token[1], PRO)
                    else:
                        setStyling(token[1], DEF)
                elif functions.is_number(token[0]):
                    #Number
                    setStyling(token[1], NUM)
                else:
                    setStyling(token[1], DEF)

class Nim(PyQt4.Qsci.QsciLexerCustom):
    """Custom lexer for the Nim programming languages"""
    styles = {
        "Default" : 0,
        "Comment" : 1,
        "BasicKeyword" : 2,
        "TopKeyword" : 3,
        "String" :  4,
        "LongString" : 5,
        "Number" :  6,
        "Pragma" : 7,
        "Operator" : 8,
        "Unsafe" : 9,
        "Type" : 10,
        "DocumentationComment" : 11,
        "Definition" : 12,
        "Class" : 13,
        "KeywordOperator" : 14,
        "CharLiteral" :  15,
        "CaseOf" :  16,
        "UserKeyword" :  17,
        "MultilineComment" :  18,
        "MultilineDocumentation" : 19
    }
    
    #Class variables
    default_color       = PyQt4.QtGui.QColor(data.theme.Font.Nim.Default[0])
    default_paper       = PyQt4.QtGui.QColor(data.theme.Paper.Nim.Default)
    default_font        = PyQt4.QtGui.QFont('Courier', 10)
    Number_OF_STYLES    = 19
    #Basic keywords and built-in procedures and templates
    basic_keyword_list  = [
        "as", "atomic", "bind", "sizeof", 
        "break", "case", "continue", "converter",
        "discard", "distinct", "do", "echo", "elif", "else", "end",
        "except", "finally", "for", "from", "defined", 
        "if", "interface", "iterator", "macro", "method", "mixin", 
        "of", "out", "proc", "func", "raise", "ref", "result", 
        "return", "template", "try", "inc", "dec", "new", "quit", 
        "while", "with", "without", "yield", "true", "false", 
        "assert", "min", "max", "newseq", "len", "pred", "succ", 
        "contains", "cmp", "add", "del","deepcopy", "shallowcopy", 
        "abs", "clamp", "isnil", "open", "reopen", "close","readall", 
        "readfile", "writefile", "endoffile", "readline", "writeline", 
    ]
    #Custom keyword created with templates/macros
    user_keyword_list   = [
        "heap_object", "namespace", "property", "stack_object"
    ]
    #Keywords that define a proc-like definition
    def_keyword_list    = ["proc", "method", "template", "macro", "converter", "iterator"]
    #Keywords that can define blocks
    top_keyword_list    = [
        "block", "const", "export", "import", "include", "let", 
        "static", "type", "using", "var", "when", 
    ]
    #Keywords that might be unsafe/dangerous
    unsafe_keyword_list = [
        "asm", "addr", "cast", "ptr", "pointer", "alloc", "alloc0",
        "allocshared0", "dealloc", "realloc", "nil", "gc_ref", 
        "gc_unref", "copymem", "zeromem", "equalmem", "movemem", 
        "gc_disable", "gc_enable", 
    ]
    #Built-in types
    type_keyword_list   = [
        "int", "int8", "int16", "int32", "int64",
        "uint", "uint8", "uint16", "uint32", "uint64",
        "float", "float32", "float64", "bool", "char",
        "string", "cstring", "pointer", "ordinal", "ptr",
        "ref", "expr", "stmt", "typedesc", "void",
        "auto", "any", "untyped", "typed", "somesignedint",
        "someunsignedint", "someinteger", "someordinal", "somereal", "somenumber",
        "range", "array", "openarray", "varargs", "seq",
        "set", "slice", "shared", "guarded", "byte",
        "natural", "positive", "rootobj", "rootref", "rooteffect",
        "timeeffect", "ioeffect", "readioeffect", "writeioeffect", "execioeffect",
        "exception", "systemerror", "ioerror", "oserror", "libraryerror",
        "resourceexhaustederror", "arithmeticerror", "divbyzeroerror", "overflowerror", 
        "accessviolationerror", "assertionerror", "valueerror", "keyerror", 
        "outofmemerror", "indexerror", "fielderror", "rangeerror", "stackoverflowerror", 
        "reraiseerror", "objectassignmenterror", "objectconversionerror", "floatingpointerror", 
        "floatinvalidoperror", "floatdivbyzeroerror", "floatoverflowerror",
        "floatunderflowerror", "floatinexacterror", "deadthreaderror", "tresult", "endianness",
        "taintedstring", "libhandle", "procaddr", "byteaddress", "biggestint",
        "biggestfloat", "clong", "culong", "cchar", "cschar",
        "cshort", "cint", "csize", "clonglong", "cfloat",
        "cdouble", "clongdouble", "cuchar", "cushort", "cuint",
        "culonglong", "cstringarray", "pfloat32", "pfloat64", "pint64",
        "pint32", "gc_strategy", "pframe", "tframe", "file",
        "filemode", "filehandle", "thinstance", "aligntype", "refcount",
        "object", "tuple", "enum",
    ]
    #Sign operators
    operator_list       = [
        "=", "+", "-", "*", "/", "<", ">", "@", "$", ".",
        "~", "&", "%", "|", "!", "?", "^", ".", ":", "\"",
    ]
    #Keyword operators
    keyword_operator_list = [
        "and", "or", "not", "xor", "shl", "shr", "div", "mod", 
        "in", "notin", "is", "isnot",
    ]
    splitter            = re.compile(r"(\{\.|\.\}|\#|\'|\"\"\"|\n|\s+|\w+|\W)")
    #Characters that autoindent one level on pressing Return/Enter
    autoindent_characters = [":", "="]

    def __init__(self, parent=None):
        """Overridden initialization"""
        #Initialize superclass
        super().__init__()
        #Set the default style values
        self.setDefaultColor(self.default_color)
        self.setDefaultPaper(self.default_paper)
        self.setDefaultFont(self.default_font)
        #Reset autoindentation style
        self.setAutoIndentStyle(0)
        #Set the theme
        self.set_theme(data.theme)
    
    def language(self):
        return "Nim"
    
    def description(self, style):
        if style <= self.Number_OF_STYLES:
            description = "Custom lexer for the Nim programming languages"
        else:
            description = ""
        return description
    
    def set_theme(self, theme):
        def set_color(color, style, bold=False):
            self.setColor(
                color, 
                self.styles[style]
            )
            if bold == True:
                self.setFont(
                    PyQt4.QtGui.QFont(
                        'Courier', 
                        10, 
                        weight=PyQt4.QtGui.QFont.Bold
                    ), 
                    self.styles[style]
                )
        for style in self.styles:
            # Papers
            self.setPaper(
                PyQt4.QtGui.QColor(theme.Paper.Nim.Default), 
                self.styles[style]
            )
            # Fonts
            color_string, bold = getattr(theme.Font.Nim, style)
            color = PyQt4.QtGui.QColor(color_string)
            set_color(color, style, bold)
        
    
    def styleText(self, start, end):
        """
        Overloaded method for styling text.
        NOTE:
            Very slow if done in Python!
            Using the Cython version is better.
            The fastest would probably be adding the lexer directly into
            the QScintilla source. Maybe never :-)
        """
        #Get the global cython flag
        global cython_found
        if cython_found == True:
            #Cython module found
            cython_lexers.style_nim(start, end, self, self.editor())
        else:
            #Style in pure Python, VERY SLOW!
            editor = self.editor()
            if editor is None:
                return
            #Initialize the styling
            self.startStyling(start)
            #Scintilla works with bytes, so we have to adjust the start and end boundaries
            text = bytearray(editor.text().lower(), "utf-8")[start:end].decode("utf-8")
            #Loop optimizations
            setStyling      = self.setStyling
            basic_kw_list   = self.basic_keyword_list
            user_kw_list    = self.user_keyword_list
            def_kw_list     = self.def_keyword_list
            top_kw_list     = self.top_keyword_list
            unsafe_kw_list  = self.unsafe_keyword_list
            operator_list   = self.operator_list
            keyword_operator_list = self.keyword_operator_list
            type_kw_list    = self.type_keyword_list
            DEF     = self.styles["Default"]
            B_KWD   = self.styles["BasicKeyword"]
            T_KWD   = self.styles["TopKeyword"]
            COM     = self.styles["Comment"]
            STR     = self.styles["String"]
            L_STR   = self.styles["LongString"]
            NUM     = self.styles["Number"]
            MAC     = self.styles["Pragma"]
            OPE     = self.styles["Operator"]
            UNS     = self.styles["Unsafe"]
            TYP     = self.styles["Type"]
            D_COM   = self.styles["DocumentationComment"]
            DEFIN   = self.styles["Definition"]
            CLS     = self.styles["Class"]
            KOP     = self.styles["KeywordOperator"]
            CHAR    = self.styles["CharLiteral"]
            OF      = self.styles["CaseOf"]
            U_KWD   = self.styles["UserKeyword"]
            M_COM   = self.styles["MultilineComment"]
            M_DOC   = self.styles["MultilineDocumentation"]
            #Initialize various states and split the text into tokens
            commenting          = False
            doc_commenting      = False
            multi_doc_commenting= False
            new_commenting      = False
            stringing           = False
            long_stringing      = False
            char_literal        = False
            pragmaing           = False
            case_of             = False
            cls_descrition      = False
            tokens = [(token, len(bytearray(token, "utf-8"))) for token in self.splitter.findall(text)]
            #Check if there is a style(comment, string, ...) stretching on from the previous line
            if start != 0:
                previous_style = editor.SendScintilla(editor.SCI_GETSTYLEAT, start - 1)
                if previous_style == L_STR:
                    long_stringing = True
                elif previous_style == MAC:
                    pragmaing = True
                elif previous_style == M_COM:
                    new_commenting = True
                elif previous_style == M_DOC:
                    multi_doc_commenting = True
            #Style the tokens accordingly
            for i, token in enumerate(tokens):
    #            print(str(token) + "  " + str(i))
                if commenting == True:
                    #Continuation of comment
                    setStyling(token[1], COM)
                    #Check if comment ends
                    if "\n" in token[0]:
                        commenting = False
                elif doc_commenting == True:
                    #Continuation of comment
                    setStyling(token[1], D_COM)
                    #Check if comment ends
                    if "\n" in token[0]:
                        doc_commenting = False
                elif new_commenting == True:
                    #Continuation of comment
                    setStyling(token[1], M_COM)
                    #Check if comment ends
                    if "#" in token[0] and "]" in tokens[i-1][0]:
                        new_commenting = False
                elif multi_doc_commenting == True:
                    #Continuation of comment
                    setStyling(token[1], M_DOC)
                    #Check if comment ends
                    if "#" in token[0] and "#" in tokens[i-1][0] and "]" in tokens[i-2][0]:
                        multi_doc_commenting = False
                elif stringing == True:
                    #Continuation of a string
                    setStyling(token[1], STR)
                    #Check if string ends
                    if token[0] == "\"" and (tokens[i-1][0] != "\\") or "\n" in token[0]:
                        stringing = False
                elif long_stringing == True:
                    #Continuation of a string
                    setStyling(token[1], L_STR)
                    #Check if string ends
                    if token[0] == "\"\"\"":
                        long_stringing = False
                elif char_literal == True:
                    #Check if string ends
                    if ("\n" in token[0] or 
                        " " in token[0] or
                        "(" in token[0] or
                        ")" in token[0] or
                        "," in token[0] or
                        token[0] in operator_list):
                        #Do not color the separator
                        setStyling(token[1], DEF)
                        char_literal = False
                    elif token[0] == "'":
                        #Continuation of a character
                        setStyling(token[1], CHAR)
                        char_literal = False
                    else:
                        setStyling(token[1], CHAR)
                elif pragmaing == True:
                    #Continuation of a string
                    setStyling(token[1], MAC)
                    #Check if string ends
                    if token[0] == ".}":
                        pragmaing = False
                elif case_of == True:
                    #'Case of' parameter
                    if token[0] == ":" or "\n" in token[0]:
                        setStyling(token[1], DEF)
                        case_of = False
                    else:
                        setStyling(token[1], OF)
                elif cls_descrition == True:
                    #Class/namespace description
                    if token[0] == ":" or "\n" in token[0]:
                        setStyling(token[1], DEF)
                        cls_descrition = False
                    else:
                        setStyling(token[1], CLS)
                elif token[0] == "\"\"\"":
                    #Start of a multi line (long) string
                    setStyling(token[1], L_STR)
                    long_stringing = True
                elif token[0] == "{.":
                    #Start of a multi line (long) string
                    setStyling(token[1], MAC)
                    pragmaing = True
                elif token[0] == "\"":
                    #Start of a string
                    setStyling(token[1], STR)
                    stringing = True
                elif token[0] == "'":
                    #Start of a string
                    setStyling(token[1], CHAR)
                    char_literal = True
                elif token[0] in basic_kw_list:
                    #Basic keyword
                    setStyling(token[1], B_KWD)
                    try:
                        if ((token[0] == "of" and "\n" in tokens[i-2][0]) or
                            ((token[0] == "of" and "\n" in tokens[i-1][0]))):
                            #Start of a CASE
                            case_of = True
                    except IndexError:
                        case_of = False
                elif token[0] in user_kw_list:
                    #User keyword
                    setStyling(token[1], U_KWD)
                elif token[0] in top_kw_list:
                    #Top keyword
                    setStyling(token[1], T_KWD)
                elif token[0] in unsafe_kw_list:
                    #Unsafe/danger keyword
                    setStyling(token[1], UNS)
                elif token[0] in operator_list:
                    #Operator
                    setStyling(token[1], OPE)
                elif token[0] in keyword_operator_list:
                    #Operator
                    setStyling(token[1], KOP)
                elif token[0] in type_kw_list:
                    #Operator
                    setStyling(token[1], TYP)
                elif token[0] == "#":
                    #Start of a comment or documentation comment
                    if len(tokens) > i+2 and tokens[i+1][0] == "#" and tokens[i+2][0] == "[":
                        setStyling(token[1], M_DOC)
                        multi_doc_commenting = True
                    elif len(tokens) > i+1 and tokens[i+1][0] == "#":
                        setStyling(token[1], D_COM)
                        doc_commenting = True
                    elif len(tokens) > i+1 and tokens[i+1][0] == "[":
                        setStyling(token[1], M_COM)
                        new_commenting = True
                    else:
                        setStyling(token[1], COM)
                        commenting = True
                elif (i > 1) and (("\n" in tokens[i-2][0]) or ("  " in tokens[i-2][0])) and (tokens[i-1][0] == "of"):
                    #Case of statement
                    case_of = True
                    setStyling(token[1], OF)
                elif functions.is_number(token[0][0]):
                    #Number
                    #Check only the first character, because Nim has those weird constants e.g.: 12u8, ...)
                    setStyling(token[1], NUM)
                elif ((i > 1) and (tokens[i-2][0] in user_kw_list) and token[0][0].isalpha()):
                    #Class-like definition
                    setStyling(token[1], CLS)
                    cls_descrition = True
                elif (((i > 1) and (tokens[i-2][0] in def_kw_list and tokens[i-1][0] != "(") and token[0][0].isalpha()) or
                      ((i > 2) and (tokens[i-3][0] in def_kw_list and tokens[i-1][0] == '`') and token[0][0].isalpha())):
                    #Proc-like definition
                    setStyling(token[1], DEFIN)
                else:
                    setStyling(token[1], DEF)


"""
Set colors for all other lexers by dynamically creating
derived classes and adding styles to them.
"""
predefined_lexers = [
    "QsciLexerPython",
]

for i in PyQt4.Qsci.__dict__:
    if i.startswith("QsciLexer") and len(i) > len("QsciLexer"):
        if not(i in predefined_lexers):
            lexer_name = i.replace("QsciLexer", "")
            styles = {}
            cls = getattr(PyQt4.Qsci, i)
            for j in dir(cls):
                att_value = getattr(cls, j)
                if j[0].isupper() == True and isinstance(att_value, int):
                    styles[j] = att_value
            cls_text = "class {0}(PyQt4.Qsci.{1}):\n".format(lexer_name, i)
            cls_text += "    styles = {\n"
            for style in styles:
                cls_text += "        \"{0}\" : {1},\n".format(style, styles[style])
            cls_text += "    }\n"
            cls_text += "    \n"
            cls_text += "    def __init__(self, parent=None):\n"
            cls_text += "        super().__init__()\n"
            cls_text += "        self.set_theme(data.theme)\n"
            cls_text += "    \n"
            cls_text += "    def set_theme(self, theme):\n"
            cls_text += "        def set_color(color, style, bold=False):\n"
            cls_text += "            self.setColor(\n"
            cls_text += "                color, \n"
            cls_text += "                self.styles[style]\n"
            cls_text += "            )\n"
            cls_text += "            if bold == True:\n"
            cls_text += "                self.setFont(\n"
            cls_text += "                    PyQt4.QtGui.QFont(\n"
            cls_text += "                        'Courier', \n"
            cls_text += "                        10, \n"
            cls_text += "                        weight=PyQt4.QtGui.QFont.Bold\n"
            cls_text += "                    ), \n"
            cls_text += "                    self.styles[style]\n"
            cls_text += "                )\n"
            cls_text += "        self.setDefaultColor(theme.Font.Default)\n".format(lexer_name)
            cls_text += "        self.setDefaultPaper(theme.Paper.Default)\n".format(lexer_name)
            for style in styles:
                cls_text += "        for style in self.styles:\n"
                cls_text += "            self.setPaper(\n"
                cls_text += "                PyQt4.QtGui.QColor(theme.Paper.{0}.Default), \n".format(lexer_name)
                cls_text += "                self.styles[style]\n"
                cls_text += "            )\n"
                cls_text += "            color_string, bold = getattr(theme.Font.{0}, style)\n".format(lexer_name)
                cls_text += "            color = PyQt4.QtGui.QColor(color_string)\n"
                cls_text += "            set_color(color, style, bold)\n"
#            print(cls_text)
            exec(cls_text)
