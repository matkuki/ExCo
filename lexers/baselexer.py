
# -*- coding: utf-8 -*-

"""
Copyright (c) 2021 Matic Kukovec. 
"""

import keyword
import builtins
import re
import functions
import data
import time

from . import *


class LexerInterface:
    """
    Base virtual lexer for any custom language
    """
    def get_name(self):
        raise Exception(f"[{self.__class__.__name__}] This method needs to be overriden!")
    
    def get_description(self):
        raise Exception(f"[{self.__class__.__name__}] This method needs to be overriden!")
    
    def get_styles(self):
        raise Exception(f"[{self.__class__.__name__}] This method needs to be overriden!")
    
    def get_keywords(self):
        raise Exception(f"[{self.__class__.__name__}] This method needs to be overriden!")
    
    def get_autoindent_characters(self):
        raise Exception(f"[{self.__class__.__name__}] This method needs to be overriden!")
    


class BaseQScintillaLexer(data.QsciLexerCustom):
    """
    Base lexer used by QScintilla
    """
    baselexer = None
    

    def __init__(self, baselexer, parent=None):
        """Overridden initialization"""
        # Initialize superclass
        super().__init__(parent)
        # Store the base lexer
        self.baselexer = baselexer
        # Set the default style values
        self.setDefaultColor(self.baselexer.styles["Default"]["font-color"])
        self.setDefaultPaper(self.baselexer.styles["Default"]["paper-color"])
        self.setDefaultFont(self.baselexer.styles["Default"]["font"])
        # Reset autoindentation style
        self.setAutoIndentStyle(0)
        # Set the theme
        self.set_theme(
            self.baselexer.styles["Default"]["paper-color"],
            self.baselexer.styles["Default"]["font-color"],
        )
    
    def language(self):
        return self.baselexer.name
    
    def description(self, style):
        if style < len(self.styles):
            description = self.baselexer.description
        else:
            description = ""
        return description
    
    def set_theme(self, paper, font):
        for style in self.styles.keys():
            # Papers
            self.setPaper(data.QColor(paper), self.styles[style])
            # Fonts
            set_font(self, style, getattr(font, style))
        
    
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
