
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
##      Cython Nim programming language lexer

from cython_lexers cimport *
# Cython libraries
from libc.stdlib cimport malloc, free
from libc.string cimport strcmp, strstr, strlen, strcpy, strchr, strtok
from cpython.unicode cimport PyUnicode_AsEncodedString

# Nim style enumeration
cdef enum NimStyles:
    NIM_DEFAULT , #0
    NIM_COMMENT , #1
    NIM_BASIC_KEYWORD ,   #2
    NIM_TOP_KEYWORD , #3
    NIM_STRING ,  #4
    NIM_LONG_STRING , #5
    NIM_NUMBER ,  #6
    NIM_PRAGMA ,   #7
    NIM_OPERATOR ,    #8
    NIM_UNSAFE,   #9
    NIM_TYPE, #10
    NIM_DOCUMENTATION_COMMENT,    #11
    NIM_DEFINITION,   #12
    NIM_CLASS,    #13
    NIM_KEYWORD_OPERATOR,    #14
    NIM_CHAR_LITERAL,     #15
    NIM_CASE_OF,     #16
    NIM_USER_KEYWORD,  #17
    NIM_MULTILINE_COMMENT,  #18
    NIM_MULTILINE_DOCUMENTATION, #19

# Basic keywords and built-in procedures and templates
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
cdef int basic_kw_list_length = len(basic_keyword_list)
cdef char** c_basic_kw_list = to_cstring_array(basic_keyword_list)

# Custom keyword created with templates/macros
user_keyword_list   = [
    "heap_object", "namespace", "property", "stack_object"
]
cdef int user_kw_list_length = len(user_keyword_list)
cdef char** c_user_kw_list = to_cstring_array(user_keyword_list)

# Keywords that define a proc-like definition
def_keyword_list    = [
    "proc", "method", "template", "macro", "converter", "iterator"
]
cdef int def_kw_list_length = len(def_keyword_list)
cdef char** c_def_kw_list = to_cstring_array(def_keyword_list)

# Keywords that can define blocks
top_keyword_list    = [
    "block", "const", "export", "import", "include", "let", 
    "static", "type", "using", "var", "when", 
]
cdef int top_kw_list_length = len(top_keyword_list)
cdef char** c_top_kw_list = to_cstring_array(top_keyword_list)

# Keywords that might be unsafe/dangerous
unsafe_keyword_list = [
    "asm", "addr", "cast", "ptr", "pointer", "alloc", "alloc0",
    "allocshared0", "dealloc", "realloc", "nil", "gc_ref", 
    "gc_unref", "copymem", "zeromem", "equalmem", "movemem", 
    "gc_disable", "gc_enable", 
]
cdef int unsafe_kw_list_length = len(unsafe_keyword_list)
cdef char** c_unsafe_kw_list = to_cstring_array(unsafe_keyword_list)

# Built-in types
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
cdef int type_kw_list_length = len(type_keyword_list)
cdef char** c_type_kw_list = to_cstring_array(type_keyword_list)

#Sign operators
operator_list = [
    "=", "+", "-", "*", "/", "<", ">", "@", "$", ".",
    "~", "&", "%", "|", "!", "?", "^", ".", ":", "\"",
]
cdef int operator_list_length = len(operator_list)
cdef char** c_operator_list = to_cstring_array(operator_list)

#Keyword operators
keyword_operator_list = [
    "and", "or", "not", "xor", "shl", "shr", "div", "mod", 
    "in", "notin", "is", "isnot",
]
cdef int keyword_op_list_length = len(keyword_operator_list)
cdef char** c_keyword_op_list = to_cstring_array(keyword_operator_list)


def style_nim(int start,
              int end,
              lexer,
              editor):
    # Local variable definitions
    cdef int    i = 0
    cdef char*  c_text
    cdef int    text_length = 0
    # Initialize various states
    cdef char commenting = 0
    cdef char doc_commenting = 0
    cdef char multi_doc_commenting = 0
    cdef char new_commenting = 0
    cdef char stringing = 0
    cdef char long_stringing = 0
    cdef char char_literal = 0
    cdef char pragmaing = 0
    cdef char case_of = 0
    cdef char cls_descrition = 0
    """
        Token arrays have to have the lenght of the maximum word
        of any in the document. Otherwise there will be an out of bounds assignment.
        The other way would be to dynamically allocate the array using malloc,
        if the size gets larger than the predefined one. Maybe someday.
    """
    cdef char[255]  current_token
    cdef char[255]  previous_token
    cdef int        previous_token_type = 0
    cdef int        token_length = 0
    cdef int        temp_state = 0
    # Scintilla works with bytes, so we have to adjust the start and end boundaries
    c_text      = NULL
    py_text     = editor.text().lower()
    text        = bytearray(py_text, "utf-8")[start:end]
    c_text      = text
    text_length = len(text)
    # Loop optimization, but it's still a pure python function, meaning quite slow
    setStyling  = lexer.setStyling
    # Initialize the styling
    lexer.startStyling(start)
    '''TOKENIZATION - THE SLOW PART IF DONE IN PYTHON'''
    # Check if there is a style(comment, string, ...) stretching on from the previous line
    if start != 0:
        previous_style = editor.SendScintilla(editor.SCI_GETSTYLEAT, start - 1)
        if previous_style == NIM_LONG_STRING:
            long_stringing = 1
        elif previous_style == NIM_PRAGMA:
            pragmaing = 1
        elif previous_style == NIM_MULTILINE_COMMENT:
            new_commenting = 1
        elif previous_style == NIM_MULTILINE_DOCUMENTATION:
            multi_doc_commenting = 1
    while i < text_length:
        if (((c_text[i] == '{' and c_text[i+1] == '.') and pragmaing == 0) or
            (pragmaing == 1)):
            """ Pragma statement """
            temp_state = i - temp_state
            # Style the currently accumulated token
            if temp_state > 0:
                current_token[token_length] = 0
                check_nim_token(
                    current_token,
                    previous_token,
                    c_text[i],
                    temp_state,
                    setStyling
                )
            temp_state = i
            # Skip the already counted '{.' characters
            if pragmaing == 0:
                i += 2
            # Loop until the macro ends
            while i < text_length:
                # Check for end of macro
                if c_text[i] == '.' and c_text[i+1] == '}':
                    break
                # Increment the text index only if end of pragma is reached
                i += 1
            # Only style the '.}' characters if it's not the end of the text
            if i < text_length:
                i += 2
            # Style the comment
            temp_state = i - temp_state
            setStyling(temp_state, NIM_PRAGMA)
            temp_state = i
            # Reset the comment flag
            pragmaing = 0
            token_length = 0
            # Skip to the next iteration, because the index is already
            # at the position at the end of the '*)' characters
            continue
        elif ((c_text[i] == '#' and c_text[i+1] == '[' and new_commenting == 0) or
              (new_commenting == 1)):
            """ Multiline comment """
            temp_state = i - temp_state
            # Style the currently accumulated token
            if temp_state > 0:
                current_token[token_length] = 0
                check_nim_token(
                    current_token,
                    previous_token,
                    c_text[i],
                    temp_state,
                    setStyling
                )
            temp_state = i
            # Skip the already counted '#','[' characters
            if new_commenting == 0:
                i += 2
            # Loop until the comment ends
            while i < text_length:
                # Check for end of comment
                if c_text[i] == ']' and c_text[i+1] == '#':
                    break
                # Increment the text index only if comment count is non zero
                i += 1
            # Only style the "]#" characters if it's not the end of the text
            if i < text_length:
                i += 2
            # Style the comment
            temp_state = i - temp_state
            setStyling(temp_state, NIM_MULTILINE_COMMENT)
            # Set the states and reset the flags
            temp_state = i
            new_commenting = 0
            token_length = 0
            # Skip to the next iteration, because the index is already
            # at the position at the end of the string
            continue
        elif ((c_text[i] == '#' and c_text[i+1] == '#' and c_text[i+2] == '[' and multi_doc_commenting == 0) or
              (multi_doc_commenting == 1)):
            """ Multiline documentation comment """
            temp_state = i - temp_state
            # Style the currently accumulated token
            if temp_state > 0:
                current_token[token_length] = 0
                check_nim_token(
                    current_token,
                    previous_token,
                    c_text[i],
                    temp_state,
                    setStyling
                )
            temp_state = i
            # Skip the already counted '#','#','[' characters
            if multi_doc_commenting == 0:
                i += 3
            # Loop until the comment ends
            while i < text_length:
                # Check for end of comment
                if c_text[i] == ']' and c_text[i+1] == '#' and c_text[i+2] == '#':
                    break
                # Increment the text index only if comment count is non zero
                i += 1
            # Only style the "]##" characters if it's not the end of the text
            if i < text_length:
                i += 3
            # Style the comment
            temp_state = i - temp_state
            setStyling(temp_state, NIM_MULTILINE_DOCUMENTATION)
            # Set the states and reset the flags
            temp_state = i
            multi_doc_commenting = 0
            token_length = 0
            # Skip to the next iteration, because the index is already
            # at the position at the end of the string
            continue
        elif c_text[i] == '#' and c_text[i+1] != '[' and c_text[i+2] != '[':
            """ One line comment/documentation comment """
            temp_state = i - temp_state
            # Style the currently accumulated token
            if temp_state > 0:
                setStyling(temp_state, NIM_DEFAULT)
            temp_state = i
            if c_text[i+1] == '#' and c_text[i+2] != '[':
                """ Documentation comment """
                # Skip the already counted '#' character
                i += 1
                while c_text[i] != '\n' and i < text_length:
                    i += 1
                # Style the comment
                temp_state = i - temp_state
                setStyling(temp_state, NIM_DOCUMENTATION_COMMENT)
            else:
                """ Comment """
                # Skip the already counted '#' character
                i += 1
                while c_text[i] != '\n' and i < text_length:
                    i += 1
                # Style the comment
                temp_state = i - temp_state
                setStyling(temp_state, NIM_COMMENT)
            temp_state = i
            token_length = 0
            # Skip to the next iteration, because the index is already
            # at the position at the end of the string
            continue
        elif c_text[i] == '#':
            """ One line comment """
            temp_state = i - temp_state
            # Style the currently accumulated token
            if temp_state > 0:
                setStyling(temp_state, NIM_DEFAULT)
            temp_state = i
            # Skip the already counted '#' character
            i += 1
            while c_text[i] != '\n' and i < text_length:
                i += 1
            # Style the comment
            temp_state = i - temp_state
            setStyling(temp_state, NIM_COMMENT)
            temp_state = i
            token_length = 0
            # Skip to the next iteration, because the index is already
            # at the position at the end of the string
            continue
        elif c_text[i] == '"':
            temp_state = i - temp_state
            #Style the currently accumulated token
            if temp_state > 0:
                setStyling(temp_state, NIM_DEFAULT)
            temp_state = i
            #Skip the already counted '"' character
            i += 1
            #Loop until the string ends or EOL is reached
            while not(c_text[i] == '"' or c_text[i] == '\n') and not(i >= text_length):
                i += 1
            #Only style the '"' character if it's not the end of the text
            if i < text_length:
                i += 1
            #Style the string
            temp_state = i - temp_state
            setStyling(temp_state, NIM_STRING)
            temp_state = i
            #Reset the string flag
            stringing = 0
            token_length = 0
            #Skip to the next iteration, because the index is already
            #at the position at the end of the string
            continue
        elif check_extended_separators(c_text[i]) != 0:
            temp_state = i - temp_state
            # Style the currently accumulated token
            current_token[token_length] = 0
            if temp_state > 0:
                check_nim_token(
                    current_token,
                    previous_token,
                    c_text[i],
                    temp_state,
                    setStyling
                )
            # Skip whitespaces and tabs
            temp_state = i
            i += 1
            while c_text[i] == ' ' or c_text[i] == '\t':
                i += 1
            temp_state = i - temp_state
            setStyling(temp_state, NIM_DEFAULT)
            # SPECIAL CASES
            temp_state = i
            if (strcmp(current_token, "case") == 0 or
                (strcmp(current_token, "of") == 0 and strcmp(previous_token, "") == 0)):
                """ 'case' argument or 'case of' arguments """
                while c_text[i] != ':' and c_text[i] != '\n' and i < text_length:
                    i += 1
                temp_state = i - temp_state
                setStyling(temp_state, NIM_CASE_OF)
            elif (strcmp(current_token, "proc") == 0 or
                  strcmp(current_token, "macro") == 0 or
                  strcmp(current_token, "converter") == 0 or
                  strcmp(current_token, "template") == 0):
                """ 'proc'/'macro'/'template' name """
                if c_text[i-1] != '(':
                    # Skip the whitespaces
                    while c_text[i] == ' ':
                        i += 1
                    temp_state = i - temp_state
                    if temp_state > 0:
                        setStyling(temp_state, NIM_DEFAULT)
                    temp_state = i
                    # Style the procedure/macro/template name
                    while (c_text[i] != '(' and 
                           c_text[i] != ')' and 
                           c_text[i] != '\n' and 
                           i < text_length):
                        i += 1
                    temp_state = i - temp_state
                    if temp_state > 0:
                        setStyling(temp_state, NIM_DEFINITION)
                else:
                    temp_state = i - temp_state
                    if temp_state > 0:
                        setStyling(temp_state, NIM_DEFINITION)
            # Save the token
            strcpy(previous_token, current_token)
            # Set the new index and reset the token lenght
            temp_state = i
            token_length = 0
            # Skip to the next iteration, because the index is already
            # at the position of the next separator
            continue
        elif i < text_length:
            current_token[token_length] = c_text[i]
            token_length += 1
            i += 1
            while (check_extended_separators(c_text[i]) == 0 and 
                   i < text_length):
                current_token[token_length] = c_text[i]
                token_length += 1
                i += 1
            #Correct the index one character back
            i -= 1
        
        #Increment the array index
        i += 1
        #Style the text at the end of the document if
        #the end has been reached
        if i >= text_length:
            temp_state = i - temp_state
            #Style the currently accumulated token
            current_token[token_length] = 0
            if temp_state > 0:
                check_nim_token(
                    current_token,
                    previous_token,
                    c_text[i],
                    temp_state,
                    setStyling
                )
    '''TOKENIZATION - THE SLOW PART IF DONE IN PYTHON'''

cdef inline void check_nim_token(char*  current_token,
                                 char*  previous_token,
                                 char   current_character,
                                 int    temp_state,
                                 setStyling):
    """Check and style a token"""
    if check_nim_keyword(current_token, basic_kw_list_length, c_basic_kw_list) == 1:
        setStyling(temp_state, NIM_BASIC_KEYWORD)
    elif check_nim_keyword(current_token, user_kw_list_length, c_user_kw_list) == 1:
        setStyling(temp_state, NIM_USER_KEYWORD)
    elif check_nim_keyword(current_token, def_kw_list_length, c_def_kw_list) == 1:
        setStyling(temp_state, NIM_DEFINITION)
    elif check_nim_keyword(current_token, top_kw_list_length, c_top_kw_list) == 1:
        setStyling(temp_state, NIM_TOP_KEYWORD)
    elif check_nim_keyword(current_token, unsafe_kw_list_length, c_unsafe_kw_list) == 1:
        setStyling(temp_state, NIM_UNSAFE)
    elif check_nim_keyword(current_token, type_kw_list_length, c_type_kw_list) == 1:
        setStyling(temp_state, NIM_TYPE)
    elif check_nim_keyword(current_token, operator_list_length, c_operator_list) == 1:
        setStyling(temp_state, NIM_OPERATOR)
    elif check_nim_keyword(current_token, keyword_op_list_length, c_keyword_op_list) == 1:
        setStyling(temp_state, NIM_KEYWORD_OPERATOR)
    elif current_token[0] > 47 and current_token[0] < 58:
        setStyling(temp_state, NIM_NUMBER)
    else:
        setStyling(temp_state, NIM_DEFAULT)

cdef inline char check_nim_keyword(char* token_string,
                                   int list_length,
                                   char** kw_list) nogil:
    """C function for checking if the token is a keyword"""
    cdef int i
    for i in range(list_length):
        if strcmp(token_string, kw_list[i]) == 0:
            #String token is a keyword
            return 1
    #Not a keyword
    return 0



