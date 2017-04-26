
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2017 Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""


##  FILE DESCRIPTION:
##      Cython implementation module for Ex.Co., 
##      used for various lexers in the lexers.py module.
##      NOTES:
##          Cython build command:
##              python cython_setup.py build_ext --build-lib=cython_build/


# Cython libraries
from libc.stdlib cimport malloc, free
from libc.string cimport strcmp, strstr, strlen, strcpy, strchr, strtok
from cpython.unicode cimport PyUnicode_AsEncodedString

# Include the various lexer implementations
include "cython_lexer_ada.pxi"
include "cython_lexer_nim.pxi"
include "cython_lexer_oberon.pxi"

"""
Common functions and variables
"""
# Separator list
cdef char* extended_separators = [
    ' ', '\t', '(', ')', '.', ';', 
    '+', '-', '/', '*', ':', ',', 
    '\n', '[', ']', '{', '}', '<', 
    '>', '|', '=', '@', '&', '%',
    '!', '?', '^', '~', '\"'
]

# Separator list length
cdef int separator_list_length = strlen(extended_separators)


cdef inline char** to_cstring_array(string_list):
    """C function that transforms a Python list into a C array of strings(char arrays)"""
    # Allocate the array of C strings on the heap
    cdef char **return_array = <char **>malloc(len(string_list) * sizeof(char *))
    # Loop through the python list of strings
    for i in range(len(string_list)):
        # Decode the python string to a byte array
        temp_str = PyUnicode_AsEncodedString(string_list[i], 'utf-8', "strict")
        # Allocate the current C string on the heap (+1 is for the termination character)
        temp_str = <char*>malloc((len(temp_value) * sizeof(char)) + 1)
        # Copy the decoded string into the allocated C string
        strcpy(temp_str, temp_value)
        # Set the reference of the C string in the allocated array at the current index
        return_array[i] = temp_str
    return return_array

cdef inline free_cstring_array(char** cstring_array, int list_length):
    """C function for cleaning up a C array of characters"""
    for i in range(list_length):
        free(cstring_array[i])
    free(cstring_array)

cdef inline char check_extended_separators(char character) nogil:
    cdef int cnt
    for cnt in range(0, separator_list_length):
        if character == extended_separators[cnt]:
            return character
    return 0



