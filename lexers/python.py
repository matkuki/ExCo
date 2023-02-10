# -*- coding: utf-8 -*-

"""
Copyright (c) 2020 Matic Kukovec. 
"""

import keyword
import builtins
import re
import functions
import data
import time
import lexers


class Python(data.QsciLexerPython):
    """
    Standard Python lexer with added keywords from built-in functions
    """
    # Class variables
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
        "Decorator" : 15,
        "DoubleQuotedFString": 16,
        "SingleQuotedFString": 17,
        "TripleSingleQuotedFString": 18,
        "TripleDoubleQuotedFString": 19,
    }
    
    def __init__(self, parent=None, additional_keywords=[]):
        """Overridden initialization"""
        # Initialize superclass
        super().__init__()
        # Set default colors
        self.setDefaultColor(data.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(data.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.QFont(data.current_font_name, data.current_font_size))
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
            self.setPaper(
                data.QColor(data.theme["fonts"][style.lower()]["background"]), 
                self.styles[style]
            )
            # Fonts
            lexers.set_font(self, style, theme["fonts"][style.lower()])
    
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


class CustomPython(data.QsciLexerCustom):
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
    # Lexer index counter for Nim styling
    _index = 0
    index = 0
    # Styles
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
         # Set the lexer's index
        self.index = CustomPython._index
        CustomPython._index += 1
        # Set the additional keywords
        self.additional_list = ["self"]
        self.additional_list.extend(additional_keywords)
        if lexers.nim_lexers_found == True:
            lexers.nim_lexers.python_set_keywords(self.index, additional_keywords)
        # Set the default style values
        self.setDefaultColor(data.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(data.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
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
    
    def defaultStyle(self):
        return self.styles["Default"]
    
    def braceStyle(self):
        return self.styles["Default"]
    
    def defaultFont(self, style):
        return data.QFont(data.current_font_name, data.current_font_size)
    
    def set_theme(self, theme):
        for style in self.styles:
            # Papers
            self.setPaper(
                data.QColor(data.theme["fonts"][style.lower()]["background"]), 
                self.styles[style]
            )
            # Fonts
            lexers.set_font(self, style, theme["fonts"][style.lower()])
    
    if lexers.nim_lexers_found == True:
        def __del__(self):
            lexers.nim_lexers.python_delete_keywords(self.index)

        def styleText(self, start, end):
            editor = self.editor()
            if editor is None:
                return
#            lexers.nim_lexers.python_style_test(self.index, start, end)
            lexers.nim_lexers.python_style_text(
                self.index, start, end, self, editor
            )
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