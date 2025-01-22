# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-present Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import keyword
import builtins
import re
import functions
import qt
import data
import time
import lexers


class Oberon(qt.QsciLexerCustom):
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
    keyword_list = [
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
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
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
    
    def defaultStyle(self):
        return self.styles["Default"]
    
    def braceStyle(self):
        return self.styles["Default"]
    
    def defaultFont(self, style):
        return qt.QFont(data.current_font_name, data.current_font_size)
    
    def set_theme(self, theme):
        for style in self.styles:
            # Papers
            self.setPaper(
                qt.QColor(data.theme["fonts"][style.lower()]["background"]), 
                self.styles[style]
            )
            # Fonts
            lexers.set_font(self, style, theme["fonts"][style.lower()])

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
        if lexers.cython_lexers_found == True:
            #Cython module found
            lexers.cython_lexers.style_oberon(start, end, self, self.editor())
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