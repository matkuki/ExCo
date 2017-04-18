
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2017 Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""


##  FILE DESCRIPTION:
##      Cython Oberon programming language lexer


from cython_lexers cimport *
#Cython libraries
from libc.stdlib cimport malloc, free
from libc.string cimport strcmp, strstr, strlen, strcpy, strchr, strtok
from cpython.unicode cimport PyUnicode_AsEncodedString

#Oberon style enumeration
cdef enum OberonStyles:
    OB_DEFAULT,
    OB_COMMENT,
    OB_KEYWORD,
    OB_STRING,
    OB_PROCEDURE,
    OB_MODULE,
    OB_NUMBER,
    OB_TYPE

#Keyword list
oberon_kw_list = [ 
    'ARRAY', 'IMPORT', 'RETURN', 'BEGIN', 'IN',
    'THEN', 'BY', 'IS', 'TO', 'CASE', 'LOOP', 'TYPE',
    'CONST', 'MOD', 'UNTIL', 'DIV', 'MODULE', 'VAR',
    'DO', 'NIL', 'WHILE', 'ELSE', 'OF', 'WITH',
    'ELSIF', 'OR', 'END', 'POINTER', 'EXIT',
    'PROCEDURE', 'FOR', 'RECORD', 'IF', 'REPEAT',
]
#Keyword list length
cdef int oberon_kw_list_length = len(oberon_kw_list)
#Change python keyword list into a C array
cdef char** c_oberon_kw_list = to_cstring_array(oberon_kw_list)

#Types list
oberon_types_list = [
    'BOOLEAN', 'CHAR', 'SHORTINT', 'INTEGER', 
    'LONGINT', 'REAL', 'LONGREAL', 'SET'
]
#Types list length
cdef int oberon_types_list_length = len(oberon_types_list)
#Change python keyword list into a C array
cdef char** c_oberon_types_list = to_cstring_array(oberon_types_list)

def style_oberon(int start,
                 int end,
                 lexer,
                 editor):
    #Local variable definitions
    cdef int    i
    cdef char   commenting = 0
    cdef char   stringing = 0
    cdef char*  c_text
    cdef int    text_length = 0
    cdef int    comment_count = 0
    cdef char   first_comment_pass = 0
    """
        Token arrays have to have the lenght of the maximum word
        of any in the document. Otherwise there will be an out of bounds assignment.
        The other way would be to dynamically allocate the array using malloc,
        if the size gets larger than the predefined one. Maybe someday.
    """
    cdef char[255]  current_token
    cdef char[255]  previous_token
    cdef int        token_length = 0
    cdef int        temp_state = 0
    #Scintilla works with bytes, so we have to adjust the start and end boundaries
    c_text      = NULL
    py_text     = editor.text()
    text        = bytearray(py_text, "utf-8")[start:end]
    c_text      = text
    text_length = len(text)
    #Loop optimization, but it's still a pure python function, meaning quite slow
    setStyling  = lexer.setStyling
    #Initialize comment state and split the text into tokens
    commenting  = 0
    stringing   = 0
    #Initialize the styling
    lexer.startStyling(start)
    '''TOKENIZATION - THE SLOW PART IF DONE IN PYTHON'''
    temp_state = 0
    i = 0
    token_lenght = 0
    #Check if there is a style(comment, string, ...) stretching on from the previous line
    if start != 0:
        previous_style = editor.SendScintilla(editor.SCI_GETSTYLEAT, start - 1)
        if previous_style == OB_COMMENT:
            commenting = 1
            """
            Oberon has nested comments, so it is required to count
            the instances of '(*' and '*)' strings in the text that
            precedes the currently styled text and increment/decrement
            the comment counter to get the correct comment styling
            """
            first_comment_pass = 1
            comment_count = py_text[:start].count("(*")
            comment_count -= py_text[:start].count("*)")
    while i < text_length:
        #Check for a comment
        if ( ((c_text[i] == '(' and c_text[i+1] == '*') and commenting == 0) or
             commenting == 1 ):
            temp_state = i - temp_state
            #Style the currently accumulated token
            if temp_state > 0:
                current_token[token_lenght] = 0
                check_oberon_token(
                    current_token,
                    previous_token,
                    c_text[i],
                    temp_state,
                    setStyling
                )
            temp_state = i
            #Skip the already counted '(*' characters
            if commenting == 0:
                i += 2
            #Initialize the comment counting
            if first_comment_pass == 0:
                comment_count = 1
            first_comment_pass = 0
            #Loop until the comment ends
            while comment_count != 0 and not(i >= text_length):
                #Count the comment beginnings/ends
                if c_text[i] == '*' and c_text[i+1] == ')':
                    comment_count -= 1
                elif c_text[i] == '(' and c_text[i+1] == '*':
                    comment_count += 1
                #Increment the text index only if comment count is non zero
                if comment_count != 0:
                    i += 1
            #Only style the '*)' characters if it's not the end of the text
            if i < text_length:
                i += 2
            #Style the comment
            temp_state = i - temp_state
            setStyling(temp_state, OB_COMMENT)
            temp_state = i
            #Reset the comment flag
            commenting = 0
            token_lenght = 0
            #Skip to the next iteration, because the index is already
            #at the position at the end of the '*)' characters
            continue
        #Check for a string
        elif c_text[i] == '"':
            temp_state = i - temp_state
            #Style the currently accumulated token
            if temp_state > 0:
                setStyling(temp_state, OB_DEFAULT)
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
            setStyling(temp_state, OB_STRING)
            temp_state = i
            #Reset the string flag
            stringing = 0
            token_lenght = 0
            #Skip to the next iteration, because the index is already
            #at the position at the end of the string
            continue
        elif check_extended_separators(c_text[i]) != 0:
            temp_state = i - temp_state
            #Style the currently accumulated token
            current_token[token_lenght] = 0
            if temp_state > 0:
                check_oberon_token(
                    current_token,
                    previous_token,
                    c_text[i],
                    temp_state,
                    setStyling
                )
            #Save the token
            if strcmp(previous_token, "PROCEDURE") == 0:
                if c_text[i] == "(" or c_text[i] == ";" :
                    strcpy(previous_token, current_token)
            elif strcmp(current_token, "PROCEDURE") == 0 and c_text[i] == "(":
                strcpy(previous_token, "(")
            else:
                strcpy(previous_token, current_token)
            
            temp_state = i
            i += 1
            while c_text[i] == ' ' or c_text[i] == '\t':
                i += 1
            temp_state = i - temp_state
            setStyling(temp_state, OB_DEFAULT)
            #Set the new index and reset the token lenght
            temp_state = i
            token_lenght = 0
            #Skip to the next iteration, because the index is already
            #at the position of the next separator
            continue
        elif i < text_length:
            current_token[token_lenght] = c_text[i]
            token_lenght += 1
            i += 1
            while (check_extended_separators(c_text[i]) == 0 and 
                   i < text_length):
                current_token[token_lenght] = c_text[i]
                token_lenght += 1
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
            current_token[token_lenght] = 0
            if temp_state > 0:
                check_oberon_token(
                    current_token,
                    previous_token,
                    c_text[i],
                    temp_state,
                    setStyling
                )
    '''TOKENIZATION - THE SLOW PART IF DONE IN PYTHON'''

cdef inline void check_oberon_token(char*  current_token,
                                    char*  previous_token,
                                    char   current_character,
                                    int    temp_state,
                                    setStyling):
    """Check and style a token"""
    if check_oberon_keyword(current_token) == 1:
        #Keyword
        setStyling(temp_state, OB_KEYWORD)
    elif check_oberon_type(current_token) == 1:
        #Type
        setStyling(temp_state, OB_TYPE)
    elif strcmp(previous_token, "PROCEDURE") == 0:
        #Procedure declaration (beginning)
        setStyling(temp_state, OB_PROCEDURE)
    elif strcmp(previous_token, "MODULE") == 0:
        #Module declaration (beginning)
        setStyling(temp_state, OB_MODULE)
    elif strcmp(previous_token, "END") == 0:
        if current_character == '.':
            #Module declaration (end)
            setStyling(temp_state, OB_MODULE)
        elif current_character == ';':
            #Procedure declaration (end)
            setStyling(temp_state, OB_PROCEDURE)
        else:
            setStyling(temp_state, OB_DEFAULT)
    elif current_token[0] > 47 and current_token[0] < 58:
        #Number constant
        if strchr(current_token, ';') or strchr(current_token, ','):
            setStyling(temp_state-1, OB_NUMBER)
            setStyling(1, OB_DEFAULT)
        else:
            setStyling(temp_state, OB_NUMBER)
    else:
        setStyling(temp_state, OB_DEFAULT)

cdef inline char check_oberon_keyword(char* token_string) nogil:
    """C function for checking if the token is a keyword"""
    global oberon_kw_list_length
    global c_oberon_kw_list
    cdef int i
    for i in range(oberon_kw_list_length):
        if strcmp(token_string, c_oberon_kw_list[i]) == 0:
            #String token is a keyword
            return 1
    #Not a keyword
    return 0
    
cdef inline char check_oberon_type(char* token_string) nogil:
    """C function for checking if the token is a type decleration"""
    global oberon_types_kw_list_length
    global c_oberon_types_list
    cdef int i
    for i in range(oberon_types_list_length):
        if strcmp(token_string, c_oberon_types_list[i]) == 0:
            #String token is a type definition
            return 1
    #Not a type definition
    return 0






