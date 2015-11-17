
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
##      Cython implementation module for Ex.Co., 
##      used for various lexers in the lexers.py module.
##      NOTES:
##          Cython build command:
##              python cython_setup.py build_ext --build-lib=cython_build/


from cython_definitions cimport *
#Cython libraries
from libc.stdlib cimport malloc, free
from libc.string cimport strcmp, strstr, strlen, strcpy, strchr, strtok
from cpython.unicode cimport PyUnicode_AsEncodedString

"""
Oberon variables and functions
""" 
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

def style_Oberon(int start,
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



"""
Ada variables and functions
"""
#Keyword list
ada_kw_list = [ 
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
#Keyword list length
cdef int ada_kw_list_length = len(ada_kw_list)
#Change python keyword list into a C array
cdef char** c_ada_kw_list = to_cstring_array(ada_kw_list)
#Special array for holding the procedure/package end data
cdef EndData end_data

def style_Ada(int start, int end, lexer, editor):
    #Local variable definitions
    cdef int    i
    cdef char   commenting
    cdef char   stringing
    cdef char*  c_text
    cdef int    text_length
    """
        Token arrays have to have the lenght of the maximum word
        of any in the document. Otherwise there will be an out of bounds assignment.
        The other way would be to dynamically allocate the array using malloc,
        if the size gets larger than the predefined one. Maybe someday.
    """
    cdef char[255]  current_token
    cdef char[255]  previous_token
    cdef int        token_length
    cdef int        temp_state
    #Scintilla works with bytes, so we have to adjust the start and end boundaries
    c_text      = NULL
    text        = bytearray(editor.text().lower(), "utf-8")
    c_text      = text
    text_length = len(text)
    #Loop optimization, but it's still a pure python function, meaning quite slow
    setStyling  = lexer.setStyling
    #Initialize comment state and split the text into tokens
    commenting      = 0
    stringing       = 0
    skip_iteration  = 0
    #Initialize the procedure/package end node array
    end_data.length     = 0
    end_data.file_type  = ADA_FILE_BODY
    #Initialize the styling
    lexer.startStyling(0)
    '''TOKENIZATION - THE SLOW PART IF DONE IN PYTHON'''
    temp_state      = 0
    i               = 0
    token_lenght    = 0
    while i < text_length:
        #Check for a comment
        if ((c_text[i] == '-' and c_text[i+1] == '-') and commenting == 0):
            temp_state = i - temp_state
            #Style the currently accumulated token
            if temp_state > 0:
                current_token[token_lenght] = 0
                check_ada_token(
                    current_token,
                    previous_token,
                    c_text[i],
                    temp_state,
                    setStyling
                )
            temp_state = i
            #Skip the already counted '--' characters
            if commenting == 0:
                i += 2
            #Loop until the comment ends
            while not(c_text[i] == '\n') and not(i >= text_length):
                i += 1
            #Style the comment
            temp_state = i - temp_state
            setStyling(temp_state, ADA_COMMENT)
            temp_state = i
            #Reset the comment flag and token length
            commenting      = 0
            token_lenght    = 0
            #Skip to the next iteration, because the index is already 
            #at the correct character
            continue
        #Check for a string
        elif c_text[i] == '"':
            temp_state = i - temp_state
            #Style the currently accumulated token
            if temp_state > 0:
                setStyling(temp_state, ADA_DEFAULT)
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
            setStyling(temp_state, ADA_STRING)
            temp_state = i
            #Reset the string flag
            stringing       = 0
            token_lenght    = 0
            #Skip to the next iteration, because the index is already
            #at the position at the end of the string
            continue
        elif check_extended_separators(c_text[i]) != 0:
            temp_state = i - temp_state
            #Style the currently accumulated token
            current_token[token_lenght] = 0
            if temp_state > 0:
                check_ada_token(
                    current_token,
                    previous_token,
                    c_text[i],
                    temp_state,
                    setStyling
                )
            #Save the token
            strcpy(previous_token, current_token)
            #Skip the any whitespace and/or tabs
            temp_state = i
            i += 1
            while c_text[i] == ' ' or c_text[i] == '\t':
                i += 1
            temp_state = i - temp_state
            setStyling(temp_state, ADA_DEFAULT)
            #Set the new index and reset the token lenght
            temp_state      = i
            token_lenght    = 0
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
                check_ada_token(
                    current_token,
                    previous_token,
                    c_text[i],
                    temp_state,
                    setStyling
                )
    '''TOKENIZATION - THE SLOW PART IF DONE IN PYTHON'''

cdef inline void check_ada_token(char*  current_token,
                                 char*  previous_token,
                                 char   current_character,
                                 int    temp_state,
                                 setStyling):
    """Check and style a token"""
    if check_ada_keyword(current_token) == 1:
        #Keyword
        setStyling(temp_state, ADA_KEYWORD)
    elif strcmp(previous_token, "procedure") == 0:
        #Procedure declaration (beginning)
        setStyling(temp_state, ADA_PROCEDURE)
        #Add the procedure type to the procedure/package list and increment the list length
        if current_character != ';':
            end_data.data[end_data.length] = NODE_PROCEDURE
            end_data.length += 1
    elif (strcmp(previous_token, "package") == 0 and
          strcmp(current_token, "body") != 0):
        #Package specification declaration, no need to increment the 
        setStyling(temp_state, ADA_PACKAGE)
        #Add the package type to the procedure/package list and increment the list length
        end_data.data[end_data.length] = NODE_PACKAGE
        end_data.length += 1
        #Set the appropriate Ada file type
        end_data.file_type = ADA_FILE_SPECIFICATION
    elif strcmp(previous_token, "body") == 0:
        #Package body declaration (beginning)
        setStyling(temp_state, ADA_PACKAGE)
        #Add the package type to the procedure/package list and increment the list length
        end_data.data[end_data.length] = NODE_PACKAGE
        end_data.length += 1
        #Set the appropriate Ada file type
        end_data.file_type = ADA_FILE_BODY
    elif strcmp(previous_token, "end") == 0:
        if current_character == ';':
            #Style according to the data type
            if end_data.length > 0:
                end_data.length -= 1
                if end_data.data[end_data.length] == NODE_PACKAGE:
                    setStyling(temp_state, ADA_PACKAGE)
                else:
                    setStyling(temp_state, ADA_PROCEDURE)
            else:
               setStyling(temp_state, ADA_DEFAULT) 
        else:
            #Normal token
            setStyling(temp_state, ADA_DEFAULT)
    elif current_token[0] > 47 and current_token[0] < 58:
        #Number constant
        if strchr(current_token, ';') or strchr(current_token, ','):
            setStyling(temp_state-1, ADA_NUMBER)
            setStyling(1, ADA_DEFAULT)
        else:
            setStyling(temp_state, ADA_NUMBER)
    else:
        setStyling(temp_state, ADA_DEFAULT)

cdef inline char check_ada_keyword(char* token_string) nogil:
    """C function for checking if the token is a keyword"""
    global ada_kw_list_length
    global c_ada_kw_list
    cdef int i
    for i in range(ada_kw_list_length):
        if strcmp(token_string, c_ada_kw_list[i]) == 0:
            #String token is a keyword
            return 1
    #Not a keyword
    return 0



"""
Helper functions and variables
"""
#Separator list
cdef char* extended_separators = [' ', '\t', '(', ')', '.', ';', 
                                   '+', '-', '/', '*', ':', ',', 
                                   '\n', '[', ']', '{', '}']
#Separator list length
cdef int separator_list_length = strlen(extended_separators)

cdef inline char** to_cstring_array(string_list):
    """C function that transforms a Python list into a C array of strings(char arrays)"""
    #Allocate the array of C strings on the heap
    cdef char **return_array = <char **>malloc(len(string_list) * sizeof(char *))
    #Loop through the python list of strings
    for i in range(len(string_list)):
        #Allocate the current C string on the heap
        temp_str = <char *>malloc(50)
        #Decode the python string to a byte array
        temp_value = PyUnicode_AsEncodedString(string_list[i], 'utf-8', "strict")
        #Copy the decoded string into the allocated C string
        strcpy(temp_str, temp_value)
        #Set the reference of the C string in the allocated array at the current index
        return_array[i] = temp_str
    return return_array

cdef inline char check_extended_separators(char character) nogil:
    cdef int cnt
    for cnt in range(0, separator_list_length):
        if character == extended_separators[cnt]:
            return character
    return 0





