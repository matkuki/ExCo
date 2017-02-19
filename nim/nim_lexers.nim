
# c:\Nim64\bin\nim.exe c --noMain --noLinking --header:nim_lexers.h nim_lexers.nim

import math
import python3
import tables
import strutils
import future
import sequtils

import nim_styling


var
    nim_method_array: array[2, PyMethodDef] = [
        PyMethodDef(
            mlName:"python_style_text", 
            mlMeth:python_style_text, 
            mlFlags:methVarargs, 
            mlDoc:"style text in Python"
        ), 
        PyMethodDef(mlName:nil, mlMeth:nil, mlFlags:0, mlDoc:nil)
    ]
    nim_methods* {.exportc.}: PyMethodDefPtr = cast[PyMethodDefPtr](addr(nim_method_array))

var nim_lexers* {.exportc.}: PyModuleDef = PyModuleDef(
    m_base: PyModuleDefBase(ob_base:PyObject(), m_init:nil, m_index:0, m_copy:nil),
    m_name: "nim_lexers",
    m_doc: "",
    m_size: -1,
    m_methods: nim_methods,
)

{.emit: """N_CDECL(void, NimMain)(void);""".}

proc PyInit_nim_lexers(): PyObjectPtr {.exportc, cdecl.} =
    {.emit: """NimMain();""".}
    result = moduleCreate(addr(nim_lexers))
    