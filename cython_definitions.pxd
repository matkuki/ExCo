
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
##      Cython definition module for Ex.Co.,
##      used for various lexers in the lexers.py module

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

#Ada tyle enumeration
cdef enum AdaStyles:
    ADA_DEFAULT,
    ADA_COMMENT,
    ADA_KEYWORD,
    ADA_STRING,
    ADA_PROCEDURE,
    ADA_NUMBER,
    ADA_TYPE, 
    ADA_PACKAGE

#Array for holding data to help with styling the END keyword in the Ada programming language
cdef struct EndData:
    int     length
    char    file_type
    char    data[1024]
#Ada node types enumeration
cdef enum EndNodeType:
    NODE_PROCEDURE
    NODE_PACKAGE
#Ada file types enumeration
cdef enum AdaFileType:
    ADA_FILE_BODY
    ADA_FILE_SPECIFICATION


