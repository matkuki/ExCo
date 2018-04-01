
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2018 Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""


##  FILE DESCRIPTION:
##      Cython Ada programming language lexer


from cython_lexers cimport *
#Cython libraries
from libc.stdlib cimport malloc, free
from libc.string cimport strcmp, strstr, strlen, strcpy, strchr, strtok
from cpython.unicode cimport PyUnicode_AsEncodedString


"""
Ada variables and functions
"""
#Ada style enumeration
cdef enum AdaStyles:
    ADA_DEFAULT,
    ADA_COMMENT,
    ADA_KEYWORD,
    ADA_STRING,
    ADA_PROCEDURE,
    ADA_NUMBER,
    ADA_TYPE, 
    ADA_PACKAGE

#Ada node types enumeration
cdef enum EndNodeType:
    NODE_PROCEDURE
    NODE_PACKAGE

#Ada file types enumeration
cdef enum AdaFileType:
    ADA_FILE_BODY
    ADA_FILE_SPECIFICATION

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

def style_ada(int start, int end, lexer, editor):
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





