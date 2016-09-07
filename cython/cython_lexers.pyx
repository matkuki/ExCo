
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
        temp_value = PyUnicode_AsEncodedString(string_list[i], 'utf-8', "strict")
        # Allocate the current C string on the heap
        temp_str = <char*>malloc(len(temp_value))
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



