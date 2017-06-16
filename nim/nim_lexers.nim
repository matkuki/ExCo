
import math
import python3
import tables
import strutils
import future
import sequtils

import nim_styling


var
    nim_method_array: array[3, PyMethodDef] = [
        PyMethodDef(
            mlName:"python_style_text", 
            mlMeth:python_style_text, 
            mlFlags:methVarargs, 
            mlDoc:"style text in Python"
        ), 
        PyMethodDef(
            mlName:"python_set_keywords", 
            mlMeth:python_set_keywords, 
            mlFlags:methVarargs, 
            mlDoc:"style text in Python"
        ), 
        PyMethodDef(mlName:nil, mlMeth:nil, mlFlags:0, mlDoc:nil)
    ]
    nim_methods* {.exportc.}: ptr PyMethodDef = cast[ptr PyMethodDef](addr(nim_method_array))

var nim_lexers* {.exportc.}: PyModuleDef = PyModuleDef(
    m_base: PyModuleDef_Base(ob_base:PyObject(), m_init:nil, m_index:0, m_copy:nil),
    m_name: "nim_lexers",
    m_doc: "",
    m_size: -1,
    m_methods: nim_methods,
)

{.emit: """N_CDECL(void, NimMain)(void);""".}

proc PyInit_nim_lexers(): ptr PyObject {.exportc, cdecl.} =
    {.emit: """NimMain();""".}
    result = PyModule_Create2(addr(nim_lexers), 1013)
    