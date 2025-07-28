"""
Copyright (c) 2013-present Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""


##  FILE DESCRIPTION:
##      Cython definition module for Ex.Co.,
##      used for various lexers in the lexers.py module
##      NOTES:
##          Cython build command:
##              python cython_setup.py build_ext --build-lib=cython_build/


#Array for holding data to help with styling the END keyword in the Ada programming language
cdef struct EndData:
    int     length
    char    file_type
    char    data[1024]

cdef inline char** to_cstring_array(object)
cdef inline char check_extended_separators(char) nogil



