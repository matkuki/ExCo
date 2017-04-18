
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2017 Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""


##  FILE DESCRIPTION:
##      Custom lexers used by the BasicWidgets in the forms.py module

import keyword
import builtins
import re
import functions
import data
import time
# Try importing the Cython module
try:
    import cython_lexers
    cython_found = True
except Exception as ex:
    print(ex)
    cython_found = False
# Try importing the Nim module
try:
    import nim_lexers
    nim_found = True
except Exception as ex:
    print(ex)
    nim_found = False


"""
-------------------------------------------------
Module helper functions
-------------------------------------------------
"""
def set_font(lexer, style_name, style_options):
    font, color, size, bold = style_options
    lexer.setColor(
        data.PyQt.QtGui.QColor(color), 
        lexer.styles[style_name]
    )
    weight = data.PyQt.QtGui.QFont.Normal
    if bold == 1 or bold == True:
        weight = data.PyQt.QtGui.QFont.Bold
    elif bold == 2:
        weight = data.PyQt.QtGui.QFont.Black
    lexer.setFont(
        data.PyQt.QtGui.QFont(font, size, weight=weight), 
        lexer.styles[style_name]
    )

def get_lexer_from_file_type(file_type):
    current_file_type = file_type
    lexer = None
    if file_type == "python":
        if nim_found == True:
            lexer = CustomPython()
        else:
            lexer = Python()
    elif file_type == "cython":
        lexer = Cython()
    elif file_type == "c":
        lexer = CPP()
    elif file_type == "c++":
        lexer = CPP()
    elif file_type == "pascal":
        lexer = Pascal()
    elif file_type == "oberon/modula":
        lexer = Oberon()
    elif file_type == "ada":
        lexer = Ada()
    elif file_type == "d":
        lexer = D()
    elif file_type == "nim":
        lexer = Nim()
    elif file_type == "makefile":
        lexer = Makefile()
    elif file_type == "xml":
        lexer = XML()
    elif file_type == "batch":
        lexer = Batch()
    elif file_type == "bash":
        lexer = Bash()
    elif file_type == "lua":
        lexer = Lua()
    elif file_type == "coffeescript":
        if data.compatibility_mode == False:
            lexer = CoffeeScript()
        else:
            lexer = Text()
    elif file_type == "c#":
        lexer = CPP()
    elif file_type == "java":
        lexer = Java()
    elif file_type == "javascript":
        lexer = JavaScript()
    elif file_type == "octave":
        lexer = Octave()
    elif file_type == "routeros":
        lexer = RouterOS()
    elif file_type == "sql":
        lexer = SQL()
    elif file_type == "postscript":
        lexer = PostScript()
    elif file_type == "fortran":
        lexer = Fortran()
    elif file_type == "fortran77":
        lexer = Fortran77()
    elif file_type == "idl":
        lexer = IDL()
    elif file_type == "ruby":
        lexer = Ruby()
    elif file_type == "html":
        lexer = HTML()
    elif file_type == "css":
        lexer = CSS()
    else:
        #No lexer was chosen, set file type to text and lexer to plain text
        current_file_type = "TEXT"
        lexer = Text()
    return (current_file_type, lexer)

def get_comment_style_for_lexer(lexer):
    open_close_comment_style = False
    comment_string = None
    end_comment_string = None
    if isinstance(lexer, CustomPython):
        comment_string = "#"
    elif isinstance(lexer, Python):
        comment_string = "#"
    elif isinstance(lexer, Cython):
        comment_string = "#"
    elif isinstance(lexer, CPP):
        comment_string = "//"
    elif isinstance(lexer, Pascal):
        comment_string = "//"
    elif isinstance(lexer, Oberon):
        open_close_comment_style = True
        comment_string = "(*"
        end_comment_string = "*)"
    elif isinstance(lexer, Ada):
        comment_string = "--"
    elif isinstance(lexer, D):
        comment_string = "//"
    elif isinstance(lexer, Nim):
        comment_string = "#"
    elif isinstance(lexer, Makefile):
        comment_string = "#"
    elif isinstance(lexer, XML):
        comment_string = None
    elif isinstance(lexer, Batch):
        comment_string = "::"
    elif isinstance(lexer, Bash):
        comment_string = "#"
    elif isinstance(lexer, Lua):
        comment_string = "--"
    elif data.compatibility_mode == False and isinstance(lexer, CoffeeScript):
        comment_string = "#"
    elif isinstance(lexer, Java):
        comment_string = "//"
    elif isinstance(lexer, JavaScript):
        comment_string = "//"
    elif isinstance(lexer, Octave):
        comment_string = "#"
    elif isinstance(lexer, RouterOS):
        comment_string = "#"
    elif isinstance(lexer, SQL):
        comment_string = "#"
    elif isinstance(lexer, PostScript):
        comment_string = "%"
    elif isinstance(lexer, Fortran):
        comment_string = "c "
    elif isinstance(lexer, Fortran77):
        comment_string = "c "
    elif isinstance(lexer, IDL):
        comment_string = "//"
    elif isinstance(lexer, Ruby):
        comment_string = "#"
    elif isinstance(lexer, HTML):
        open_close_comment_style = True
        comment_string = "<!--"
        end_comment_string = "-->"
    elif isinstance(lexer, CSS):
        open_close_comment_style = True
        comment_string = "/*"
        end_comment_string = "*/"
    # Save the comment options to the lexer
    return (open_close_comment_style, comment_string, end_comment_string)


"""
-------------------------------------------------
Module objects
-------------------------------------------------
"""
class Text(data.PyQt.Qsci.QsciLexerCustom):
    """Lexer for styling normal text documents"""
    #Class variables
    default_font = data.PyQt.QtGui.QFont('Courier', 10)
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
        # Papers
        self.setPaper(
            data.PyQt.QtGui.QColor(theme.Paper.Python.Default), 
            self.styles["Default"]
        )
        # Fonts
        set_font(self, "Default", theme.Font.Python.Default)
    
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


class Python(data.PyQt.Qsci.QsciLexerPython):
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
    
    def __init__(self, parent=None, additional_keywords=[]):
        """Overridden initialization"""
        # Initialize superclass
        super().__init__()
        # Initialize the keyword list
        self.init_kwrds(additional_keywords)
        # Set the theme
        self.set_theme(data.theme)
    
    def init_kwrds(self, additional_keywords=[]):
        #Initialize list with keywords
        built_ins = keyword.kwlist
        for i in builtins.__dict__.keys():
            if not(i in built_ins):
                built_ins.append(i)
        self._kwrds = list(set(built_ins + additional_keywords))
        self._kwrds.sort()
        #Transform list into a single string with spaces between list items
        self._kwrds = " ".join(self._kwrds)
    
    def set_theme(self, theme):
        for style in self.styles:
            # Papers
            paper = data.PyQt.QtGui.QColor(getattr(theme.Paper.Python, style))
            self.setPaper(paper, self.styles[style])
            # Fonts
            set_font(self, style, getattr(theme.Font.Python, style))
    
    def keywords(self, state):
        """
        Overridden method for determining keywords,
        read the QScintilla QsciLexer class documentation on the Riverbank website.
        """
        #Only state 1 returns keywords, don't know why? Check the C++ Scintilla lexer source files.
        if state == 1:
            return self._kwrds
        else:
            return None

class CustomPython(data.PyQt.Qsci.QsciLexerCustom):
    class Sequence:
        def __init__(self, 
                     start, 
                     stop_sequences, 
                     stop_characters, 
                     style, 
                     add_to_style):
            self.start = start
            self.stop_sequences = stop_sequences
            self.stop_characters = stop_characters
            self.style = style
            self.add_to_style = add_to_style

    # Class variables
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
        "Decorator" : 15,
        "CustomKeyword" : 16,
    }
    default_color       = data.PyQt.QtGui.QColor(data.theme.Font.Python.Default[1])
    default_paper       = data.PyQt.QtGui.QColor(data.theme.Paper.Python.Default)
    default_font        = data.PyQt.QtGui.QFont('Courier', 10)
    # Styling lists and characters
    keyword_list        = list(set(keyword.kwlist + dir(builtins)))
    additional_list     = []
    sq                  = Sequence('\'', ['\'', '\n'], [], styles["SingleQuotedString"], True)
    dq                  = Sequence('"', ['"', '\n'], [], styles["DoubleQuotedString"], True)
    edq                 = Sequence('""', [], [], styles["DoubleQuotedString"], True)
    esq                 = Sequence('\'\'', [], [], styles["DoubleQuotedString"], True)
    tqd                 = Sequence('\'\'\'', ['\'\'\''], [], styles["TripleSingleQuotedString"], True)
    tqs                 = Sequence('"""', ['"""'], [], styles["TripleDoubleQuotedString"], True)
    cls                 = Sequence('class', [':'], ['(', '\n'], styles["ClassName"], False)
    defi                = Sequence('def', [], ['('], styles["FunctionMethodName"], False)
    comment             = Sequence('#', [], ['\n'], styles["Comment"], True)
    dcomment            = Sequence('##', [], ['\n'], styles["CommentBlock"], True)
    decorator           = Sequence('@', ['\n'], [' '], styles["Decorator"], True)
    sequence_lists      = [
        sq, dq, edq, esq, tqd, tqs, cls, defi, comment, dcomment, decorator
    ]                           
    multiline_sequence_list = [tqd, tqs]
    sequence_start_chrs = [x.start for x in sequence_lists]
    # Regular expression split sequence to tokenize text
    splitter            = re.compile(r"(\\'|\\\"|\(\*|\*\)|\n|\"+|\'+|\#+|\s+|\w+|\W)")
    #Characters that autoindent one level on pressing Return/Enter
    autoindent_characters = [":"]

    def __init__(self, parent=None, additional_keywords=[]):
        """Overridden initialization"""
        # Initialize superclass
        super().__init__()
        # Set the additional keywords
        self.additional_list = ["self"]
        self.additional_list.extend(additional_keywords)
        # Set the default style values
        self.setDefaultColor(self.default_color)
        self.setDefaultPaper(self.default_paper)
        self.setDefaultFont(self.default_font)
        # Reset autoindentation style
        self.setAutoIndentStyle(0)
        # Set the theme
        self.set_theme(data.theme)
    
    def language(self):
        return "Python"
    
    def description(self, style):
        if style <= 16:
            description = "Custom lexer for the Python programming languages"
        else:
            description = ""
        return description
    
    def set_theme(self, theme):
        for style in self.styles:
            # Papers
            paper = data.PyQt.QtGui.QColor(getattr(theme.Paper.Python, style))
            self.setPaper(paper, self.styles[style])
            # Fonts
            set_font(self, style, getattr(theme.Font.Python, style))
    
    if nim_found == True:
        def styleText(self, start, end):
            nim_lexers.python_style_text(start, end, self, self.editor())    
    else:
        def styleText(self, start, end):
            editor = self.editor()
            if editor is None:
                return
            # Initialize the styling
            self.startStyling(start)
            # Scintilla works with bytes, so we have to adjust the start and end boundaries
            text = bytearray(editor.text(), "utf-8")[start:end].decode("utf-8")
            # Loop optimizations
            setStyling  = self.setStyling
            # Initialize comment state and split the text into tokens
            sequence = None
            tokens = [(token, len(bytearray(token, "utf-8"))) for token in self.splitter.findall(text)]
            # Check if there is a style(comment, string, ...) stretching on from the previous line
            if start != 0:
                previous_style = editor.SendScintilla(editor.SCI_GETSTYLEAT, start - 1)
                for i in self.multiline_sequence_list:
                    if previous_style == i.style:
                        sequence = i
                        break
            
            # Style the tokens accordingly
            for i, token in enumerate(tokens):
#                print(token[0].encode("utf-8"))
                token_name = token[0]
                token_length = token[1]
                if sequence != None:
                    if token_name in sequence.stop_sequences:
                        if sequence.add_to_style == True:
                            setStyling(token_length, sequence.style)
                        else:
                            setStyling(token_length, self.styles["Default"])
                        sequence = None
                    elif any(ch in token_name for ch in sequence.stop_characters):
                        if sequence.add_to_style == True:
                            setStyling(token_length, sequence.style)
                        else:
                            setStyling(token_length, self.styles["Default"])
                        sequence = None
                    else:
                        setStyling(token_length, sequence.style)
                elif token_name in self.sequence_start_chrs:
                    for i in self.sequence_lists:
                        if token_name == i.start:
                            if i.stop_sequences == [] and i.stop_characters == []:
                                # Skip styling if both stop sequences and stop characters are empty
                                setStyling(token_length, i.style)
                            else:
                                # Style the sequence and store the reference to it
                                sequence = i
                                if i.add_to_style == True:
                                    setStyling(token_length, sequence.style)
                                else:
                                    if token_name in self.keyword_list:
                                        setStyling(token_length, self.styles["Keyword"])
                                    elif token_name in self.additional_list:
                                        setStyling(token_length, self.styles["CustomKeyword"])
                                    else:
                                        setStyling(token_length, self.styles["Default"])
                            break
                elif token_name in self.keyword_list:
                    setStyling(token_length, self.styles["Keyword"])
                elif token_name in self.additional_list:
                    setStyling(token_length, self.styles["CustomKeyword"])
                elif token_name[0].isdigit():
                    setStyling(token_length, self.styles["Number"])
                else:
                    setStyling(token_length, self.styles["Default"])


class Cython(data.PyQt.Qsci.QsciLexerPython):
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
        "void", "char", "int", "long", "short", "double", "float", 
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
        #Initialize list with keywords
        built_ins = keyword.kwlist
        for i in builtins.__dict__.keys():
            if not(i in built_ins):
                built_ins.append(i)
        self._kwrds = list(set(built_ins))
        #Transform list into a single string with spaces between list items
        #Add the C keywords supported by Cython
        self._kwrds.extend(self._c_kwrds)
        #Add the Cython keywords
        self._kwrds.extend(self._cython_kwrds)
        #Transform list into a single string with spaces between list items
        self._kwrds.sort()
        self._kwrds = " ".join(self._kwrds)
        #Reset autoindentation style
        self.setAutoIndentStyle(0)
        #Set the theme
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        for style in self.styles:
            # Papers
            self.setPaper(
                data.PyQt.QtGui.QColor(theme.Paper.Python.Default), 
                self.styles[style]
            )
            # Fonts
            set_font(self, style, getattr(theme.Font.Python, style))
    
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


class Oberon(data.PyQt.Qsci.QsciLexerCustom):
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
    default_color       = data.PyQt.QtGui.QColor(data.theme.Font.Oberon.Default[1])
    default_paper       = data.PyQt.QtGui.QColor(data.theme.Paper.Oberon.Default)
    default_font        = data.PyQt.QtGui.QFont('Courier', 10)
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
        try:
            import nim_lexers
            nim_lexers.python_style_text(0)
        except Exception as ex:
            print(ex)
        
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
        for style in self.styles:
            # Papers
            self.setPaper(
                data.PyQt.QtGui.QColor(theme.Paper.Oberon.Default), 
                self.styles[style]
            )
            # Fonts
            set_font(self, style, getattr(theme.Font.Oberon, style))

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
            stringing   = False
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

class Ada(data.PyQt.Qsci.QsciLexerCustom):
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
    default_color       = data.PyQt.QtGui.QColor(data.theme.Font.Ada.Default[1])
    default_paper       = data.PyQt.QtGui.QColor(data.theme.Paper.Ada.Default)
    default_font        = data.PyQt.QtGui.QFont('Courier', 10)
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
        for style in self.styles:
            # Papers
            self.setPaper(
                data.PyQt.QtGui.QColor(theme.Paper.Ada.Default), 
                self.styles[style]
            )
            # Fonts
            set_font(self, style, getattr(theme.Font.Ada, style))
        
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
            DEF = self.styles["Default"]
            KWD = self.styles["Keyword"]
            COM = self.styles["Comment"]
            STR = self.styles["String"]
            PRO = self.styles["Procedure"]
            NUM = self.styles["Number"]
            PAC = self.styles["Package"]
#            TYP = self.styles["Type"]
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

class RouterOS(data.PyQt.Qsci.QsciLexerCustom):
    """
    Custom lexer for the RouterOS syntax for MikroTik routers (WinBox)
    """
    styles = {
        "Default" : 0,
        "Operator" : 1,
        "Comment" : 2,
        "Keyword1" : 3,
        "Keyword2" :  4,
        "Keyword3" : 5,
    }
    #Class variables
    default_color       = data.PyQt.QtGui.QColor(data.theme.Font.RouterOS.Default[1])
    default_paper       = data.PyQt.QtGui.QColor(data.theme.Paper.RouterOS.Default)
    default_font        = data.PyQt.QtGui.QFont('Courier', 10)
    #All keywords, operators, ...
    operator_list = [
        '!', '$', '(', ')', ',', ':', '[', ']', '{', '|', '}', "="
    ]
    comment_list = [
        '#'
    ]
    keyword1_list = [
        'ac-name', 'accept', 'accessible-via-web', 'account-local-traffic', 'accounting', 'action', 'active-flow-timeout', 'active-mode', 'add-default-route', 'address-list', 'address-pool', 'address', 'addresses-per-mac', 'admin-mac', 'advertise-dns', 'advertise-mac-address', 'ageing-time', 'allocate-udp-ports-from', 'allow-disable-external-interface', 'allow-guests', 'allow-remote-requests', 'allow', 'allowed-number', 'always-from-cache', 'area-id', 'area', 'arp', 'as', 'audio-max', 'audio-min', 'audio-monitor', 'auth-algorithms', 'auth-method', 'auth', 'authenticate', 'authentication-password', 'authentication-protocol', 'authentication-types', 'authentication', 'authoritative', 'auto-mac', 'auto-negotiation', 'auto-send-supout', 'automatic-supout', 'autonomous', 'backup-allowed', 'baud-rate', 'bidirectional-timeout', 'blank-interval', 'bootp-support', 'bridge-mode', 'bridge', 'broadcast-addresses', 'broadcast', 'bsd-syslog', 'cable-settings', 'cache-administrator', 'cache-entries', 'cache-hit-dscp', 'cache-max-ttl', 'cache-on-disk', 'cache-size', 'certificate', 'chain', 'change-tcp-mss', 'channel-time', 'channel', 'check-interval', 'cipher', 'client-to-client-reflection', 'comment', 'connection-bytes', 'connection-idle-timeout', 'connection-mark', 'connection-state', 'contact', 'contrast', 'cpu', 'data-bits', 'default-ap-tx-limit', 'default-authentication', 'default-client-tx-limit', 'default-forwarding', 'default-group', 'default-profile', 'default-route-distance', 'default', 'dh-group', 'dhcp-option', 'dial-on-demand', 'directory', 'disable-running-check', 'disabled', 'disk-file-count', 'disk-file-name', 'disk-lines-per-file', 'disk-stop-on-full', 'display-time', 'distance', 'distribute-default', 'distribute-for-default-route', 'dns-name', 'dns-server', 'domain', 'dpd-interval', 'dpd-maximum-failures', 'dst-address-list', 'dst-address', 'dst-delta', 'dst-end', 'dst-port', 'dst-start', 'dynamic-label-range', 'e', 'eap-methods', 'enabled', 'enc-algorithm', 'enc-algorithms', 'encryption-password', 'encryption-protocol', 'engine-id', 'exchange-mode', 'exclude-groups', 'file-limit', 'file-name', 'filter-ip-address', 'filter-ip-protocol', 'filter-mac-address', 'filter-mac-protocol', 'filter-mac', 'filter-port', 'filter-stream', 'flow-control', 'forward-delay', 'frame-size', 'frames-per-second', 'from', 'full-duplex', 'garbage-timer', 'gateway-class', 'gateway-keepalive', 'gateway-selection', 'gateway', 'generate-policy', 'generic-timeout', 'group-ciphers', 'group-key-update', 'hash-algorithm', 'hide-ssid', 'hop-limit', 'hotspot-address', 'html-directory', 'http-cookie-lifetime', 'http-proxy', 'i', 'icmp-timeout', 'idle-timeout', 'ignore-as-path-len', 'in-filter', 'in-interface', 'inactive-flow-timeout', 'instance', 'interface', 'interfaces', 'interim-update', 'interval', 'ipsec-protocols', 'jump-target', 'keep-max-sms', 'keepalive-timeout', 'kind', 'l2mtu', 'latency-distribution-scale', 'lease-time', 'level', 'lifebytes', 'lifetime', 'line-count', 'list', 'local-address', 'location', 'log-prefix', 'login-by', 'login', 'loop-detect', 'lsr-id', 'mac-address', 'managed-address-configuration', 'management-protection-key', 'management-protection', 'manycast', 'max-cache-size', 'max-client-connections', 'max-connections', 'max-fresh-time', 'max-message-age', 'max-mru', 'max-mtu', 'max-server-connections', 'max-sessions', 'max-station-count', 'max-udp-packet-size', 'memory-limit', 'memory-lines', 'memory-scroll', 'memory-stop-on-full', 'metric-bgp', 'metric-connected', 'metric-default', 'metric-ospf', 'metric-other-ospf', 'metric-rip', 'metric-static', 'min-rx', 'mode', 'mpls-mtu', 'mq-pfifo-limit', 'mrru', 'mtu', 'multi-cpu', 'multicast', 'multiple-channels', 'multiplier', 'my-id-user-fqdn', 'name', 'nat-traversal', 'netmask', 'network', 'new-connection-mark', 'new-packet-mark', 'new-routing-mark', 'no-ping-delay', 'note', 'ntp-server', 'on-backup', 'on-master', 'only-headers', 'only-one', 'origination-interval', 'other-configuration', 'out-filter', 'out-interface', 'page-refresh', 'parent-proxy-port', 'parent-proxy', 'parent', 'parity', 'passthrough', 'password', 'path-vector-limit', 'paypal-accept-pending', 'paypal-allowed', 'paypal-secure-response', 'permissions', 'pfifo-limit', 'pfs-group', 'policy', 'port', 'ports', 'preemption-mode', 'preferred-gateway', 'preferred-lifetime', 'prefix', 'primary-ntp', 'primary-server', 'priority', 'profile', 'propagate-ttl', 'proposal-check', 'proposal', 'proprietary-extensions', 'protocol-mode', 'protocol', 'query-interval', 'query-response-interval', 'queue', 'quick-leave', 'ra-delay', 'ra-interval', 'ra-lifetime', 'radius-eap-accounting', 'radius-mac-accounting', 'radius-mac-authentication', 'radius-mac-caching', 'radius-mac-format', 'radius-mac-mode', 'ranges', 'rate-limit', 'reachable-time', 'read-access', 'read-only', 'receive-all', 'receive-enabled', 'receive-errors', 'red-avg-packet', 'red-burst', 'red-limit', 'red-max-threshold', 'red-min-threshold', 'redistribute-bgp', 'redistribute-connected', 'redistribute-ospf', 'redistribute-other-bgp', 'redistribute-other-ospf', 'redistribute-rip', 'redistribute-static', 'remember', 'remote-address', 'remote-ipv6-prefix-pool', 'remote-port', 'remote', 'require-client-certificate', 'retransmit-interval', 'router-id', 'routing-mark', 'routing-table', 'sa-dst-address', 'sa-src-address', 'scope', 'secondary-ntp', 'secondary-server', 'secret', 'security-profile', 'security', 'send-initial-contact', 'serialize-connections', 'servers', 'service-name', 'set-system-time', 'sfq-allot', 'sfq-perturb', 'shared-users', 'show-at-login', 'show-dummy-rule', 'signup-allowed', 'sip-direct-media', 'skin', 'smtp-server', 'source', 'speed', 'split-user-domain', 'src-address-list', 'src-address', 'src-port', 'ssid-all', 'ssid', 'state-after-reboot', 'static-algo-0', 'static-algo-1', 'static-algo-2', 'static-algo-3', 'static-key-0', 'static-key-1', 'static-key-2', 'static-key-3', 'static-sta-private-algo', 'static-sta-private-key', 'static-transmit-key', 'status-autorefresh', 'stop-bits', 'store-every', 'store-leases-disk', 'streaming-enabled', 'streaming-max-rate', 'streaming-server', 'supplicant-identity', 'switch-to-spt-bytes', 'switch-to-spt-interval', 'switch-to-spt', 'syslog-facility', 'syslog-severity', 'target-scope', 'target', 'tcp-close-timeout', 'tcp-close-wait-timeout', 'tcp-established-timeout', 'tcp-fin-wait-timeout', 'tcp-last-ack-timeout', 'tcp-syn-received-timeout', 'tcp-syn-sent-timeout', 'tcp-syncookie', 'tcp-time-wait-timeout', 'term', 'test-id', 'threshold', 'time-zone-name', 'time-zone', 'timeout-timer', 'timeout', 'tls-certificate', 'tls-mode', 'to-addresses', 'topics', 'transmit-hold-count', 'transparent-proxy', 'transport-address', 'trap-generators', 'trap-target', 'trap-version', 'ttl', 'tunnel', 'type', 'udp-stream-timeout', 'udp-timeout', 'unicast-ciphers', 'update-stats-interval', 'update-timer', 'use-compression', 'use-encryption', 'use-explicit-null', 'use-ip-firewall-for-pppoe', 'use-ip-firewall-for-vlan', 'use-ip-firewall', 'use-ipv6', 'use-mpls', 'use-peer-dns', 'use-peer-ntp', 'use-radius', 'use-service-tag', 'use-vj-compression', 'user', 'v3-protocol', 'valid-lifetime', 'vcno', 'verify-client-certificate', 'version', 'vlan-id', 'vrid', 'watch-address', 'watchdog-timer', 'wds-cost-range', 'wds-default-bridge', 'wds-default-cost', 'wds-ignore-ssid', 'wds-mode', 'wins-server', 'wmm-support', 'wpa-pre-shared-key', 'wpa2-pre-shared-key', 'write-access', 'burst-limit', 'burst-threshold', 'burst-time', 'limit-at', 'priority', 'max-limit', 'tree', 'packet-mark', 'value', 'option', 'target-addresses', 'queue', 'encryption-password', 'always-broadcast', 'connect-to', 'adaptive-noise-immunity', 'compression', 'band', 'country', 'frequency', 'hw-retries', 'rate-selection', 'scan-list'
    ]
    keyword2_list = [
        'set', 'add', 'delay', 'do', 'error', 'execute', 'find', 'for', 'foreach', 'global', 'if', 'len', 'local', 'nothing', 'parse', 'pick', 'put', 'resolve', 'set', 'time', 'toarray', 'tobool', 'toid', 'toip', 'toip6', 'tonum', 'tostr', 'totime', 'typeof', 'while', 'beep', 'export', 'import', 'led', 'password', 'ping', 'quit', 'redo', 'setup', 'undo', 'print', 'detail', 'file', 'log', 'info', 'get', 'warning', 'critical'
    ]
    keyword3_list = [
        '/', 'aaa', 'accounting', 'address', 'address-list', 'align', 'area', 'bandwidth-server', 'bfd', 'bgp', 'bridge', 'client', 'clock', 'community', 'config', 'connection', 'console', 'customer', 'default', 'dhcp-client', 'dhcp-server', 'discovery', 'dns', 'e-mail', 'ethernet', 'filter', 'firewall', 'firmware', 'gps', 'graphing', 'group', 'hardware', 'health', 'hotspot', 'identity', 'igmp-proxy', 'incoming', 'instance', 'interface0', 'ip', 'ipsec', 'ipv6', 'irq', 'l2tp-server', 'lcd', 'ldp', 'logging', 'mac-server', 'mac-winbox', 'mangle', 'manual', 'mirror', 'mme', 'mpls', 'nat', 'nd', 'neighbor', 'network', 'note', 'ntp', 'ospf', 'ospf-v3', 'ovpn-server', 'page', 'peer', 'pim', 'ping', 'policy', 'pool', 'port', 'ppp', 'pppoe-client', 'pptp-server', 'prefix', 'profile', 'proposal', 'proxy', 'queue', 'radius', 'resource', 'rip', 'ripng', 'route', 'routing', 'screen', 'script', 'security-profiles', 'server', 'service', 'service-port', 'settings', 'shares', 'smb', 'sms', 'sniffer', 'snmp', 'snooper', 'socks', 'sstp-server', 'system', 'tool', 'tracking', 'traffic-flow', 'traffic-generator', 'type', 'upgrade', 'upnp', 'user', 'user-manager', 'users', 'vlan', 'vrrp', 'watchdog', 'web-access', 'wireless', 'pptp', 'pppoe', 'lan', 'wan', 'layer7-protocol', 'eth-', 'wlan-', 'bridge-'
    ]
    
    splitter = re.compile(r"(\{\.|\.\}|\#|\'|\"\"\"|\n|\s+|\w+|\W)")
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
        return "RouterOS"
    
    def description(self, style):
        if style < len(self.styles):
            description = "Custom lexer for the RouterOS syntax by MikroTik"
        else:
            description = ""
        return description
    
    def set_theme(self, theme):
        for style in self.styles:
            # Papers
            self.setPaper(
                data.PyQt.QtGui.QColor(theme.Paper.RouterOS.Default), 
                self.styles[style]
            )
            # Fonts
            set_font(self, style, getattr(theme.Font.RouterOS, style))
    
    def styleText(self, start, end):
        """
        Overloaded method for styling text.
        NOTE:
            Very slow if done in Python!
            Using the Cython version is better.
            The fastest would probably be adding the lexer directly into
            the QScintilla source. Maybe never :-)
        """
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
        operator_list   = self.operator_list
        comment_list    = self.comment_list
        keyword1_list   = self.keyword1_list
        keyword2_list   = self.keyword2_list
        keyword3_list   = self.keyword3_list
        DEFAULT     = self.styles["Default"]
        OPERATOR    = self.styles["Operator"]
        COMMENT     = self.styles["Comment"]
        KEYWORD1    = self.styles["Keyword1"]
        KEYWORD2    = self.styles["Keyword2"]
        KEYWORD3    = self.styles["Keyword3"]
        #Initialize various states and split the text into tokens
        commenting          = False
        tokens = [(token, len(bytearray(token, "utf-8"))) for token in self.splitter.findall(text)]
        #Style the tokens accordingly
        for i, token in enumerate(tokens):
            if commenting == True:
                #Continuation of comment
                setStyling(token[1], COMMENT)
                #Check if comment ends
                if "\n" in token[0]:
                    commenting = False
            elif token[0] in operator_list:
                setStyling(token[1], OPERATOR)
            elif token[0] in comment_list:
                setStyling(token[1], COMMENT)
                commenting = True
            elif token[0] in keyword1_list:
                setStyling(token[1], KEYWORD1)
            elif token[0] in keyword2_list:
                setStyling(token[1], KEYWORD2)
            elif token[0] in keyword3_list:
                setStyling(token[1], KEYWORD3)
            else:
                setStyling(token[1], DEFAULT)


class Nim(data.PyQt.Qsci.QsciLexerCustom):
    """
    Custom lexer for the Nim programming languages
    """
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
    default_color       = data.PyQt.QtGui.QColor(data.theme.Font.Nim.Default[1])
    default_paper       = data.PyQt.QtGui.QColor(data.theme.Paper.Nim.Default)
    default_font        = data.PyQt.QtGui.QFont('Courier', 10)
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
    user_keyword_list = [
        "heap_object", "namespace", "property", "stack_object"
    ]
    #Keywords that define a proc-like definition
    def_keyword_list = ["proc", "method", "template", "macro", "converter", "iterator"]
    #Keywords that can define blocks
    top_keyword_list = [
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
    type_keyword_list = [
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
    operator_list = [
        "=", "+", "-", "*", "/", "<", ">", "@", "$", ".",
        "~", "&", "%", "|", "!", "?", "^", ".", ":", "\"",
    ]
    #Keyword operators
    keyword_operator_list = [
        "and", "or", "not", "xor", "shl", "shr", "div", "mod", 
        "in", "notin", "is", "isnot",
    ]
    splitter = re.compile(r"(\{\.|\.\}|\#|\'|\"\"\"|\n|\s+|\w+|\W)")
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
        if style < len(self.styles):
            description = "Custom lexer for the Nim programming languages"
        else:
            description = ""
        return description
    
    def set_theme(self, theme):
        for style in self.styles:
            # Papers
            self.setPaper(
                data.PyQt.QtGui.QColor(theme.Paper.Nim.Default), 
                self.styles[style]
            )
            # Fonts
            set_font(self, style, getattr(theme.Font.Nim, style))
        
    
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
#                print(str(token) + "  " + str(i))
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
# Lexers that were manually defined above
predefined_lexers = [
    "QsciLexerPython",
]
# Themes that are missing when upgrading QScintilla
missing_themes = {}
# Loop through the Qsci module lexers and adjust them
for i in data.PyQt.Qsci.__dict__:
    if i.startswith("QsciLexer") and len(i) > len("QsciLexer"):
        if not(i in predefined_lexers):
            lexer_name = i.replace("QsciLexer", "")
            styles = {}
            cls = getattr(data.PyQt.Qsci, i)
            for j in dir(cls):
                att_value = getattr(cls, j)
                if j[0].isupper() == True and isinstance(att_value, int):
                    styles[j] = att_value
            cls_text = "class {0}(data.PyQt.Qsci.{1}):\n".format(lexer_name, i)
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
            cls_text += "        self.setDefaultColor(theme.Font.Default)\n".format(lexer_name)
            cls_text += "        self.setDefaultPaper(theme.Paper.Default)\n".format(lexer_name)
            cls_text += "        missing_themes['{}'] = []\n".format(lexer_name)
            for style in styles:
                cls_text += "        for style in self.styles:\n"
                cls_text += "            try:\n"
                cls_text += "                self.setPaper(\n"
                cls_text += "                    data.PyQt.QtGui.QColor(theme.Paper.{0}.Default), \n".format(lexer_name)
                cls_text += "                    self.styles[style]\n"
                cls_text += "                )\n"
                cls_text += "                set_font(self, style, getattr(theme.Font.{0}, style))\n".format(lexer_name)
                cls_text += "            except:\n"
                cls_text += "               if not(style in missing_themes['{}']):\n".format(lexer_name)
                cls_text += "                   missing_themes['{}'].append(style)\n".format(lexer_name)
                cls_text += "        if len(missing_themes['{}']) != 0:\n".format(lexer_name)
                cls_text += "            print(\"Lexer '{}' missing themes:\")\n".format(lexer_name)
                cls_text += "            for mt in missing_themes['{}']:\n".format(lexer_name)
                cls_text += "                print('    - ' + mt)\n"
                cls_text += "            raise Exception(\"Lexer '{}' has missing themes!\")\n".format(lexer_name)
            exec(cls_text)
