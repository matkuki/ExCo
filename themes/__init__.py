
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2022 Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import os
import data
import time
import functools
import traceback
import functions


def get_all():
    theme_files = []
    for item in os.listdir(__get_theme_directory()):
        if item.endswith(".json"):
            try:
                theme = get(item)
                theme_files.append(theme)
            except:
                traceback.print_exc()
                print("[Themes] Invalid theme file:", item)
    return theme_files

def get(theme_name):
    file_name = theme_name
    if not theme_name.endswith(".json"):
        file_name = "{}.json".format(theme_name.lower())
    file_path = functions.unixify_join(
        __get_theme_directory(),
        file_name
    )
    if not os.path.isfile(file_path):
        raise Exception("[Themes] Theme '{}' does not exist!".format(theme_name))
    try:
        theme = functions.load_json_file(file_path)
    except Exception as ex:
        print("[Themes] Cannot parse '{}' theme file!".format(file_name))
        raise ex
    __check(theme)
    return theme

def __get_theme_directory():
    theme_path = functions.unixify_join(
        data.resources_directory,
        "themes",
    )
    return theme_path

def __check_color(field, color_string, prior_keys):
    try:
        data.QColor(color_string)
    except Exception as ex:
        print(
            "[Themes] Color error: {} / '{}'!".format(
                "->".join(prior_keys + (field,)), color_string
            )
        )
        raise ex

def __check_color_list(field, color_list, prior_keys):
    try:
        for color_string in color_list:
            data.QColor(color_string)
    except Exception as ex:
        print(
            "[Themes] Color list error: {}!".format(
                "->".join(prior_keys + (field,))
            )
        )
        raise ex

def __check_string(field, string, prior_keys):
    if not isinstance(string, str):
        raise Exception(
            "[Themes] String error: {} / '{}'!".format(
                "->".join(prior_keys + (field,)), string
            )
        )

def __check_bool(field, boolean, prior_keys):
    if not isinstance(boolean, bool):
        raise Exception(
            "[Themes] Boolean error: {} / '{}'!".format(
                "->".join(prior_keys + (field,)), boolean
            )
        )

def __check_fields(schema, dictionary, prior_keys=()):
    for k,v in dictionary.items():
        try:
            nested_schema_item = functools.reduce(lambda seq, key: seq[key], prior_keys, schema)
        except:
            raise Exception(
                "[Themes] Unknown schema key: {} / '{}'!".format(
                    "->".join(prior_keys + (k,)), v
                )
            )
        if isinstance(v, dict):
            __check_fields(schema, v, (*prior_keys, k))
        elif isinstance(v, int) and not isinstance(v, bool):
            if dictionary[k] != nested_schema_item[k]:
                raise Exception(
                    "[Themes] Integer error: {} / '{}'!".format(
                        "->".join(prior_keys + (k,)), v
                    )
                )
        else:
            try:
                if k not in nested_schema_item:
                    raise Exception(
                        "[Themes] Key is missing: {}!".format(
                            "->".join(prior_keys + (k,)), 
                        )
                    )
                func = nested_schema_item[k]
                func(k, v, prior_keys)
            except Exception as ex:
                print("key:", k)
                print("value:", v)
                print("prior-keys:", prior_keys)
                print("nested_schema_item:", nested_schema_item)
                raise ex

def __check(theme_data):
    performance_timer_starting_count = time.perf_counter()
    schema = {
        "close-hover-image": __check_string,
        "close-image": __check_string,
        "context-menu-background": __check_color,
        "context-menu-hex-edge": __check_color,
        "cursor": __check_color,
        "cursor-line-background": __check_color,        
        "dock_point_color_active": __check_color,
        "dock_point_color_passive": __check_color,
        "foldmargin": {
            "background": __check_color,
            "foreground": __check_color
        },
        "fonts": {
            "array": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "arrayparenthesis": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "asm": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "aspatstart": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "aspjavascriptcomment": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "aspjavascriptcommentdoc": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "aspjavascriptcommentline": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "aspjavascriptdefault": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "aspjavascriptdoublequotedstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "aspjavascriptkeyword": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "aspjavascriptnumber": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "aspjavascriptregex": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "aspjavascriptsinglequotedstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "aspjavascriptstart": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "aspjavascriptsymbol": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "aspjavascriptunclosedstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "aspjavascriptword": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "asppythonclassname": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "asppythoncomment": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "asppythondefault": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "asppythondoublequotedstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "asppythonfunctionmethodname": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "asppythonidentifier": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "asppythonkeyword": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "asppythonnumber": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "asppythonoperator": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "asppythonsinglequotedstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "asppythonstart": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "asppythontripledoublequotedstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "asppythontriplesinglequotedstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "aspstart": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "aspvbscriptcomment": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "aspvbscriptdefault": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "aspvbscriptidentifier": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "aspvbscriptkeyword": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "aspvbscriptnumber": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "aspvbscriptstart": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "aspvbscriptstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "aspvbscriptunclosedstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "aspxccomment": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "assignment": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "atrule": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "attribute": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "backquotestring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "backtickheredocument": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "backtickheredocumentvar": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "backticks": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "backticksvar": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "baddirective": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "badstringcharacter": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "base85string": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "basicfunctions": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "basickeyword": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "blockcomment": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "blockforeach": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "blockif": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "blockmacro": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "blockregex": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "blockregexcomment": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "blockwhile": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "builtinfunction": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "builtinvariable": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "caseof": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "cdata": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "character": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "charliteral": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "class": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "classname": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "classselector": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "classvariable": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "clipproperty": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "command": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "comment": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "commentbang": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "commentblock": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "commentbox": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "commentdoc": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "commentdockeyword": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "commentdockeyworderror": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "commentkeyword": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "commentline": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "commentlinedoc": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "commentlinehash": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "commentnested": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "commentparenthesis": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "continuation": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "coroutinesiosystemfacilities": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "css1property": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "css2property": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "css3property": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "customkeyword": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "datasection": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "declareinputoutputport": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "declareinputport": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "declareoutputport": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "decorator": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "default": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "defaultvalue": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "definition": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "delimiter": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "demotedkeyword": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "dictionaryparenthesis": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "diff-similar": {
                "color": __check_string,
                "bold": __check_bool,
                "background": __check_color
            },
            "diff-unique-1": {
                "color": __check_string,
                "bold": __check_bool,
                "background": __check_color
            },
            "diff-unique-2": {
                "color": __check_string,
                "bold": __check_bool,
                "background": __check_color
            },
            "directive": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "documentationcomment": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "documentdelimiter": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "dottedoperator": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "doublequotedheredocument": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "doublequotedheredocumentvar": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "doublequotedstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "doublequotedstringvar": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "dsccomment": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "dsccommentvalue": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "entity": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "error": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "escapesequence": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "expandkeyword": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "extendedcssproperty": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "extendedfunction": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "extendedpseudoclass": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "extendedpseudoelement": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "externalcommand": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "filter": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "flags": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "formatbody": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "formatidentifier": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "function": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "functionmethodname": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "fuzzy": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "global": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "globalclass": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "group": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "hash": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "hashquotedstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "header": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "heredocument": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "heredocumentdelimiter": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "hexnumber": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "hexstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "hidecommandchar": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "highlightedidentifier": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "htmlcomment": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "htmldoublequotedstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "htmlnumber": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "htmlsinglequotedstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "htmlvalue": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "identifier": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "idselector": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "immediateevalliteral": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "important": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "inactivecomment": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "inactivecommentbang": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "inactivecommentdoc": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "inactivecommentdockeyword": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "inactivecommentdockeyworderror": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "inactivecommentkeyword": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "inactivecommentline": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "inactivecommentlinedoc": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "inactivedeclareinputoutputport": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "inactivedeclareinputport": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "inactivedeclareoutputport": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "inactivedefault": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "inactivedoublequotedstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "inactiveescapesequence": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "inactiveglobalclass": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "inactivehashquotedstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "inactiveidentifier": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "inactivekeyword": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "inactivekeywordset2": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "inactivenumber": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "inactiveoperator": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "inactiveportconnection": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "inactivepreprocessor": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "inactivepreprocessorcomment": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "inactivepreprocessorcommentlinedoc": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "inactiverawstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "inactiveregex": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "inactivesinglequotedstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "inactivestring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "inactivesystemtask": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "inactivetaskmarker": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "inactivetriplequotedverbatimstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "inactiveunclosedstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "inactiveuserkeywordset": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "inactiveuserliteral": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "inactiveuuid": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "inactiveverbatimstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "inconsistent": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "instancevariable": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "intrinsicfunction": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "itclkeyword": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "javascriptcomment": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "javascriptcommentdoc": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "javascriptcommentline": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "javascriptdefault": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "javascriptdoublequotedstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "javascriptkeyword": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "javascriptnumber": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "javascriptregex": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "javascriptsinglequotedstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "javascriptstart": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "javascriptsymbol": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "javascriptunclosedstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "javascriptword": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "key": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "keyword": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "keyword1": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "keyword2": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "keyword3": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "keyworddoc": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "keywordoperator": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "keywordsecondary": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "keywordset2": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "keywordset3": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "keywordset5": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "keywordset6": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "keywordset7": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "keywordset8": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "keywordset9": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "label": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "lineadded": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "linechanged": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "linecomment": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "lineremoved": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "literal": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "literalstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "longstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "mediarule": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "messagecontext": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "messagecontexttext": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "messagecontexttexteol": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "messageid": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "messageidtext": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "messageidtexteol": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "messagestring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "messagestringtext": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "messagestringtexteol": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "modifier": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "module": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "modulename": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "multilinecomment": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "multilinedocumentation": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "name": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "nestedblockcomment": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "nowarning": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "number": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "objectscsgappearance": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "operator": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "otherintag": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "package": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "parameter": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "parameterexpansion": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "percentstringq": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "percentstringr": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "percentstringw": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "percentstringx": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "phpcomment": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "phpcommentline": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "phpdefault": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "phpdoublequotedstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "phpdoublequotedvariable": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "phpkeyword": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "phpnumber": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "phpoperator": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "phpsinglequotedstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "phpstart": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "phpvariable": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "plugin": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "pluscomment": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "pluskeyword": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "plusprompt": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "pod": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "podverbatim": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "portconnection": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "position": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "pragma": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "predefinedfunctions": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "predefinedidentifiers": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "preprocessor": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "preprocessorcomment": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "preprocessorcommentlinedoc": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "preprocessorparenthesis": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "procedure": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "procedureparenthesis": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "programmercomment": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "pseudoclass": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "pseudoelement": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "pythonclassname": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "pythoncomment": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "pythondefault": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "pythondoublequotedstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "pythonfunctionmethodname": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "pythonidentifier": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "pythonkeyword": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "pythonnumber": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "pythonoperator": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "pythonsinglequotedstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "pythonstart": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "pythontripledoublequotedstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "pythontriplesinglequotedstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "quotedidentifier": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "quotedkeyword": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "quotedoperator": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "quotedstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "quotedstringq": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "quotedstringqq": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "quotedstringqqvar": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "quotedstringqr": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "quotedstringqrvar": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "quotedstringqw": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "quotedstringqx": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "quotedstringqxvar": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "rawstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "reference": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "regex": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "regexvar": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "scalar": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "script": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "section": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "sgmlblockdefault": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "sgmlcommand": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "sgmlcomment": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "sgmldefault": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "sgmldoublequotedstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "sgmlentity": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "sgmlerror": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "sgmlparameter": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "sgmlparametercomment": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "sgmlsinglequotedstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "sgmlspecial": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "singlequotedheredocument": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "singlequotedstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "spaces": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "special": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "standardfunction": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "standardoperator": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "standardpackage": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "standardtype": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "stderr": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "stdin": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "stdout": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "string": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "stringleftquote": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "stringrightquote": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "stringtablemathsfunctions": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "stringvariable": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "subroutineprototype": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "substitution": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "substitutionbrace": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "substitutionvar": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "success": {
                "color": __check_string,
                "bold": __check_bool,
                "background": __check_color
            },
            "symbol": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "symboltable": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "syntaxerrormarker": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "systemtask": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "tabs": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "tabsafterspaces": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "tag": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "target": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "taskmarker": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "tclkeyword": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "text": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "textblockmarker": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "tkcommand": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "tkkeyword": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "topkeyword": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "translation": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "tripledoublequotedstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "triplequotedverbatimstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "triplesinglequotedstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "triplestring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "type": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "typedefs": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "typesmodifiersitems": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "unclosedstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "unknownattribute": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "unknownproperty": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "unknownpseudoclass": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "unknowntag": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "unsafe": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "userkeyword": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "userkeywordset": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "userliteral": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "uuid": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "value": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "variable": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "vbscriptcomment": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "vbscriptdefault": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "vbscriptidentifier": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "vbscriptkeyword": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "vbscriptnumber": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "vbscriptstart": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "vbscriptstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "vbscriptunclosedstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "verbatimstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "warning": {
                "color": __check_string,
                "bold": __check_bool,
                "background": __check_color
            },
            "xmlend": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "xmlstart": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "xmltagend": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "doublequotedfstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "singlequotedfstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "tripledoublequotedfstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "triplesinglequotedfstring": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "iri": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "iricompact": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "keywordld": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
            "property": {
                "color": __check_color,
                "bold": __check_bool,
                "background": __check_color
            },
        },
        "form": __check_color,
        "image-file": __check_string,
        "indication": {
            "activebackground": __check_color,
            "activeborder": __check_color,
            "find": __check_color,
            "font": __check_color,
            "highlight": __check_color,
            "hover": __check_color,
            "passivebackground": __check_color,
            "passiveborder": __check_color,
            "replace": __check_color,
            "selection": __check_color
        },
        "left-arrow-hover-image": __check_string,
        "left-arrow-image": __check_string,
        "linemargin": {
            "background": __check_color,
            "foreground": __check_color
        },
        "name": __check_string,
        "right-arrow-hover-image": __check_string,
        "right-arrow-image": __check_string,
        "right-arrow-menu-disabled-image": __check_string,
        "right-arrow-menu-image": __check_string,
        "scrollbar": {
            "background": __check_color,
            "handle": __check_color,
            "handle-hover": __check_color
        },
        "settings-background": __check_color,
        "settings-hex-background": __check_color,
        "settings-hex-edge": __check_color,
        "settings-label-background": __check_color,
        "textdiffercolors": {
            "indicator-similar-color": __check_color,
            "indicator-unique-1-color": __check_color,
            "indicator-unique-2-color": __check_color
        },
        "table-header": __check_color,
        "tooltip": __check_string,
        "yesnodialog-background": __check_color,
        "yesnodialog-edge": __check_color
    }
    __check_fields(schema, theme_data)
    
