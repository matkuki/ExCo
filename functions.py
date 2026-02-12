"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.

FILE DESCRIPTION:
    Module that holds functions for various uses
    that uses only the PyQt and standard libraries.
"""

import ast
import datetime
import json
import operator
import os
import os.path
import re
import shutil
import subprocess
import sys
import threading
import time
import traceback
import webbrowser
from typing import *
from types import TracebackType

import constants
import data
import qt
from filefunctions import *

# REPL message displaying function (that needs to be assigned at runtime!)
repl_print = None


def count_iterator(start=0):
    counter = start
    while True:
        yield counter
        counter += 1


def create_directory(directory):
    if not os.path.isdir(directory):
        os.mkdir(directory)


def create_thread(func, *args):
    t = threading.Thread(target=func, args=args)
    t.daemon = True
    t.start()


icon_cache = {}


def create_icon(icon: Union[qt.QPixmap, str]) -> qt.QIcon:
    """
    Function for initializing and returning an QIcon object

    :param icon: Either a QPixmap object or a string file path.
    :return: A QIcon object initialized from the input.
    """
    # Pixmap
    if isinstance(icon, qt.QPixmap):
        new_icon: qt.QIcon = qt.QIcon(icon)
    # Path
    elif isinstance(icon, str):
        full_icon_path: str = unixify_join(data.resources_directory, icon)

        # Check cache
        if full_icon_path in icon_cache.keys():
            # The cached_icon might be a QIcon or QPixmap depending on how
            # the cache is managed, but we assume it can be used to construct a QIcon.
            cached_icon: Any = icon_cache[full_icon_path]
            return qt.QIcon(cached_icon)

        # Check file existence
        if not os.path.isfile(full_icon_path):
            raise Exception("Icon file doesn't exist: {}".format(full_icon_path))

        # Initialize from path and cache it
        new_icon = qt.QIcon(full_icon_path)
        icon_cache[full_icon_path] = new_icon
    # Unknown
    else:
        # This branch should technically be unreachable if type checking is used,
        # but it remains for runtime safety and handles any unexpected object types.
        raise Exception("Unknown icon construction type: {}".format(icon))

    return new_icon


def get_resource_file(relative_path):
    path = unixify_join(data.resources_directory, relative_path)
    if not os.path.isfile(path):
        raise Exception("[Resources] File does not exist: {}".format(path))
    return path


pixmap_cache = {}


def create_pixmap(pixmap_name, directory=None):
    """
    Function for initializing and returning an QPixmap object
    """
    if directory == None:
        directory = data.resources_directory
    pixmap_path = unixify_join(directory, pixmap_name)
    if pixmap_path in pixmap_cache.keys():
        cached_pixmap = pixmap_cache[pixmap_path]
        return qt.QPixmap(cached_pixmap)
    if not os.path.isfile(pixmap_path):
        raise Exception("Pixmap file doesn't exist: {}".format(pixmap_path))
    new_pixmap = qt.QPixmap(pixmap_path)
    pixmap_cache[pixmap_path] = new_pixmap
    return new_pixmap


def create_pixmap_with_size(pixmap_name, width=None, height=None):
    """
    Function for initializing and returning an QPixmap object with a size
    """
    pixmap = create_pixmap(pixmap_name)
    if width:
        pixmap = pixmap.scaledToWidth(
            int(width), qt.Qt.TransformationMode.SmoothTransformation
        )
    if height:
        pixmap = pixmap.scaledToHeight(
            int(height), qt.Qt.TransformationMode.SmoothTransformation
        )
    return pixmap


__overlay_cache = {}


def ovarlay_images(base_path, overlay_path):
    base_pixmap = create_pixmap(base_path)
    if base_pixmap.isNull():
        raise Exception(f"Cannot create base pixmap: {base_path}")

    overlay_pixmap = create_pixmap(overlay_path)
    if overlay_pixmap.isNull():
        raise Exception(f"Cannot create base pixmap: {overlay_path}")

    if (
        overlay_pixmap.size().width() > base_pixmap.size().width()
        or overlay_pixmap.size().height() > base_pixmap.size().height()
    ):
        overlay_pixmap = overlay_pixmap.scaled(
            base_pixmap.size(), qt.Qt.AspectRatioMode.KeepAspectRatio
        )

    painter = qt.QPainter()
    painter.begin(base_pixmap)
    painter.drawPixmap(0, 0, overlay_pixmap)
    painter.end()

    return base_pixmap


__LANGUAGE_ICON_MAP = {
    # Primary names (lowercase, normalized)
    "python": "language_icons/logo_python.png",
    "cython": "language_icons/logo_cython.png",
    "c": "language_icons/logo_c.png",
    "awk": "language_icons/logo_awk.png",
    "c++": "language_icons/logo_cpp.png",
    "cpp": "language_icons/logo_cpp.png",  # alias
    "c / c++": "language_icons/logo_c_cpp.png",
    "cicode": "language_icons/logo_cicode.png",
    "oberon / modula": "language_icons/logo_oberon.png",
    "d": "language_icons/logo_d.png",
    "nim": "language_icons/logo_nim.png",
    "ada": "language_icons/logo_ada.png",
    "cmake": "language_icons/logo_cmake.png",
    "css": "language_icons/logo_css.png",
    "html": "language_icons/logo_html.png",
    "json": "language_icons/logo_json.png",
    "lua": "language_icons/logo_lua.png",
    "matlab": "language_icons/logo_matlab.png",
    "perl": "language_icons/logo_perl.png",
    "ruby": "language_icons/logo_ruby.png",
    "tcl": "language_icons/logo_tcl.png",
    "tex": "language_icons/logo_tex.png",
    "idl": "language_icons/logo_idl.png",
    "bash": "language_icons/logo_bash.png",
    "batch": "language_icons/logo_batch.png",
    "fortran": "language_icons/logo_fortran.png",
    "fortran77": "language_icons/logo_fortran77.png",
    "coffeescript": "language_icons/logo_coffeescript.png",
    "c#": "language_icons/logo_csharp.png",
    "csharp": "language_icons/logo_csharp.png",  # alias
    "cs": "language_icons/logo_csharp.png",  # another alias
    "java": "language_icons/logo_java.png",
    "javascript": "language_icons/logo_javascript.png",
    "js": "language_icons/logo_javascript.png",  # alias
    "makefile": "language_icons/logo_makefile.png",
    "octave": "language_icons/logo_octave.png",
    "pascal": "language_icons/logo_pascal.png",
    "postscript": "language_icons/logo_postscript.png",
    "routeros": "language_icons/logo_routeros.png",
    "spice": "language_icons/logo_spice.png",
    "sql": "language_icons/logo_sql.png",
    "verilog": "language_icons/logo_verilog.png",
    "vhdl": "language_icons/logo_vhdl.png",
    "xml": "language_icons/logo_xml.png",
    "yaml": "language_icons/logo_yaml.png",
    "zig": "language_icons/logo_zig.png",
    "rust": "language_icons/logo_rust.png",
    # Generic configs/data
    "ini": "tango_icons/document-properties.png",
    # Fallbacks
    "text": "tango_icons/text-x-generic.png",
}

# Default fallback icon
__FALLBACK_ICON = "tango_icons/file.png"


def get_language_file_icon(language_name: str) -> str:
    """
    Get the appropriate icon path for a given programming language name.

    Normalizes input (case-insensitive, strips whitespace), supports aliases,
    and falls back to a generic file icon if unknown.

    Args:
        language_name: Name of the programming language (e.g., 'Python', 'C++').

    Returns:
        Path to the icon file (string).
    """
    if not isinstance(language_name, str):
        language_name = str(language_name)

    # Normalize: lowercase, strip, and replace common variants
    key = language_name.strip().lower()

    # Look up; fallback to default
    icon_path = __LANGUAGE_ICON_MAP.get(key, __FALLBACK_ICON)
    return create_icon(icon_path)


def create_language_document_icon_from_path(path, check_content=True):
    file_type = get_file_type(path, check_content)
    return get_language_file_icon(file_type)


def replace_text_in_files(
    search_text,
    replace_text,
    search_dir,
    case_sensitive=False,
    search_subdirs=True,
    file_filter=None,
):
    """
    Search for the specified text in files in the specified directory and replace all instances
    of the search_text with replace_text and save the changes back to the file.
    """
    # Get the files with the search string in them
    found_files = find_files_with_text(
        search_text,
        search_dir,
        case_sensitive=case_sensitive,
        search_subdirs=search_subdirs,
        break_on_find=False,
        file_filter=file_filter,
    )
    if found_files == None:
        return []
    # Loop through the found list and replace the text
    for file in found_files:
        # Read the file
        file_text = read_file_to_string(file)
        # Compile the regex expression according to case sensitivity
        if case_sensitive == True:
            compiled_search_re = re.compile(search_text)
        else:
            compiled_search_re = re.compile(search_text, re.IGNORECASE)
        # Replace all instances of search text with the replace text
        replaced_text = re.sub(compiled_search_re, replace_text, file_text)
        # Write the replaced text back to the file
        write_to_file(replaced_text, file)
    # Return the found files list
    return found_files


def get_nim_node_tree(nim_code):
    """
    Parse the text and return a node tree as a list.
    The text must be valid Nim/Nimrod code.
    """

    class NimNode:
        def __init__(self):
            # Attributes
            self.name = None
            self.description = None
            self.type = None
            self.parameters = None
            self.return_type = None
            self.line = None
            # Child node lists
            self.imports = []
            self.types = []
            self.consts = []
            self.lets = []
            self.vars = []
            self.procedures = []
            self.forward_declarations = []
            self.converters = []
            self.iterators = []
            self.methods = []
            self.properties = []
            self.templates = []
            self.macros = []
            self.objects = []
            self.namespaces = []

    # Nested function for determining the next blocks indentation level
    def get_next_blocks_indentation(current_step, lines):
        for ln in range(current_step, len(lines)):
            if lines[ln].strip() != "" and lines[ln].strip().startswith("#") == False:
                return get_line_indentation(lines[ln])
        else:
            return 250

    # Nested function for finding the closing parenthesis of parameter definitions
    def get_closing_parenthesis(current_step, lines):
        for ln in range(current_step, len(lines)):
            if ")" in lines[ln] and (
                lines[ln].count(")") == (lines[ln].count("(") + 1)
            ):
                return ln
        else:
            return None

    # Nested function for creating a procedure, method, macro or template node
    def create_node(
        node,
        search_string,
        current_line,
        current_line_number,
        line_list,
        previous_offset=0,
    ):
        # Reset the procedure's starting line adjustment variable
        body_starting_line_number = None
        # Reset the local skip line variable
        local_skip_to_line = None
        # Parse procedure name according to the line characters
        if "(" in current_line:
            # The procedure has parameters
            base_search_string = r"{:s}\s+(.*?)\(|{:s}\s+(.*?)\:|{:s}\s+(.*?)\=".format(
                search_string, search_string, search_string
            )
            proc_name_search_pattern = re.compile(base_search_string, re.IGNORECASE)
            name_match_object = re.search(proc_name_search_pattern, current_line)
            for i in range(1, 4):
                node.name = name_match_object.group(i)
                if node.name != "" and node.name != None:
                    break
            # Skip lines if the parameters stretch over multiple lines
            if not (")" in current_line):
                body_starting_line_number = get_closing_parenthesis(
                    current_line_number + 1, line_list
                )
                current_line = line_list[body_starting_line_number]
            # Parse the procedure parameters and return type
            if search_string == "proc":
                return_type = None
                parameters = None
                # Check if the parameters are declared over multiple lines
                if body_starting_line_number != None:
                    parameter_string = ""
                    open_index = line_list[current_line_number].find("(") + 1
                    parameter_string += line_list[current_line_number][open_index:]
                    for i in range(
                        current_line_number + 1, body_starting_line_number + 1
                    ):
                        if ")" in line_list[i] and (
                            line_list[i].count(")") == (line_list[i].count("(") + 1)
                        ):
                            close_index = line_list[i].find(")")
                            current_parameter = line_list[i][:close_index].strip()
                            # Filter out the parameter initialization
                            if "=" in current_parameter:
                                current_parameter = current_parameter[
                                    : current_parameter.find("=")
                                ]
                            parameter_string += current_parameter
                        else:
                            current_parameter = line_list[i].strip()
                            # Filter out the parameter initialization
                            if "=" in current_parameter:
                                current_parameter = current_parameter[
                                    : current_parameter.find("=")
                                ]
                            parameter_string += current_parameter
                    parameters = [
                        par.strip()
                        for par in parameter_string.split(",")
                        if par.strip() != ""
                    ]
                    # Check the return type
                    split_line = line_list[body_starting_line_number][
                        close_index:
                    ].split(":")
                    if len(split_line) > 1:
                        return_type = split_line[1].replace("=", "")
                        return_type = return_type.strip()
                else:
                    open_index = line_list[current_line_number].find("(") + 1
                    close_index = line_list[current_line_number].find(")")
                    parameter_string = line_list[current_line_number][
                        open_index:close_index
                    ]
                    parameters = [
                        par for par in parameter_string.split(",") if par.strip() != ""
                    ]
                    # Check the return type
                    split_line = line_list[current_line_number][close_index:].split(":")
                    if len(split_line) > 1:
                        return_type = split_line[1].replace("=", "")
                        return_type = return_type.strip()
                node.parameters = parameters
                node.return_type = return_type
        elif ":" in current_line:
            # The procedure/macro/... has no parameters, but has a return type
            node.name = current_line.replace(search_string, "", 1).split(":")[0].strip()
            # Special parsing for classes
            if search_string == "class" or search_string == "property":
                node.name = node.name.split()[0]
        else:
            # The procedure/macro/... has no parameters and no return type
            node.name = current_line.replace(search_string, "", 1).split()[0].strip()

        # Parse node
        if "=" in current_line and current_line.strip().endswith("="):
            # Check if the declaration is a one-liner
            if (current_line.strip().endswith("=") == False) and (
                (
                    len(current_line.split("=")) == 2
                    and current_line.split("=")[1].strip() != ""
                )
                or (
                    len(current_line.split("=")) > 2
                    and current_line[current_line.rfind(")") :].split("=")[1] != ""
                )
            ):
                # One-liner
                pass
            else:
                # Adjust the procedure body starting line as needed
                starting_line_number = current_line_number + 1
                if body_starting_line_number != None:
                    starting_line_number = body_starting_line_number + 1
                # Parse the procedure for its local child nodes
                sub_node_lines = []
                compare_indentation = get_next_blocks_indentation(
                    starting_line_number, line_list
                )
                for ln in range(starting_line_number, len(line_list)):
                    # Skip empty lines
                    if (
                        line_list[ln].strip() == ""
                        or line_list[ln].strip().startswith("#") == True
                    ):
                        # Add the blank space at the correct indentation level
                        # to have the correct number of lines in the list
                        sub_node_lines.append(" " * compare_indentation)
                        continue
                    elif get_line_indentation(line_list[ln]) < compare_indentation:
                        # Store the end of the procedure declaration
                        local_skip_to_line = ln
                        # Reached the last line of the procedure declaration
                        break
                    else:
                        sub_node_lines.append(line_list[ln])
                else:
                    # For loop looped through all of the lines, skip them
                    local_skip_to_line = len(line_list) - 1
                starting_line_number += previous_offset
                node = parse_node(
                    node, sub_node_lines, line_offset=starting_line_number
                )
        elif (
            search_string == "class"
            or search_string == "namespace"
            or search_string == "property"
        ):
            """special macro identifiers: class, namespace, ..."""
            # Adjust the procedure body starting line as needed
            starting_line_number = current_line_number + 1
            if body_starting_line_number != None:
                starting_line_number = body_starting_line_number + 1
            # Parse the procedure for its local child nodes
            sub_node_lines = []
            compare_indentation = get_next_blocks_indentation(
                starting_line_number, line_list
            )
            for ln in range(starting_line_number, len(line_list)):
                # Skip empty lines
                if (
                    line_list[ln].strip() == ""
                    or line_list[ln].strip().startswith("#") == True
                ):
                    # Add the blank space at the correct indentation level
                    # to have the correct number of lines in the list
                    sub_node_lines.append(" " * compare_indentation)
                    continue
                elif get_line_indentation(line_list[ln]) < compare_indentation:
                    # Store the end of the procedure declaration
                    local_skip_to_line = ln
                    # Reached the last line of the procedure declaration
                    break
                else:
                    sub_node_lines.append(line_list[ln])
            else:
                # For loop looped through all of the lines, skip them
                local_skip_to_line = len(line_list) - 1
            starting_line_number += previous_offset
            node = parse_node(node, sub_node_lines, line_offset=starting_line_number)
        else:
            """The procedure is a forward declaracion"""
            node.type = "forward declaration"
        # Return the relevant data
        return node, local_skip_to_line

    # Split the Nim code into lines
    nim_code_lines = nim_code.split("\n")
    # Create and initialize the main node that will hold all other nodes
    main_node = NimNode()
    main_node.name = "main"
    main_node.description = "main node"

    def parse_node(input_node, code_lines, line_offset=0):
        # Initialize the starting indentation levels (number of spaces)
        current_indentation = 0
        compare_indentation = 0
        # Initialize the various state flags
        import_statement = False
        type_statement = False
        const_statement = False
        let_statement = False
        var_statement = False
        proc_statement = False
        converter_statement = False
        iterator_statement = False
        method_statement = False
        macro_statement = False
        template_statement = False
        class_statement = False
        namespace_statement = False
        property_statement = False
        # Initialize the flag for skipping multiple lines
        skip_to_line = None
        # Main loop
        for line_count, line in enumerate(code_lines):
            # Skip blank lines
            if line.strip() == "" or line.strip().startswith("#"):
                continue
            # Check if line needs to be skipped
            if skip_to_line != None:
                if line_count >= skip_to_line:
                    skip_to_line = None
                else:
                    continue
            # Get line indentation and strip leading/trailing whitespaces
            current_indentation = get_line_indentation(line)
            line = line.strip()
            # Discard the comment part of a line, if it's in the line
            if "#" in line:
                stringing = False
                string_character = None
                for ch_count, ch in enumerate(line):
                    if ch == '"' or ch == "'":
                        # Catch the string building characters
                        if stringing == False:
                            stringing = True
                            string_character = ch
                        elif ch == string_character:
                            stringing = False
                            string_character = None
                    elif ch == "#" and stringing == False:
                        # Discrad the part of the line from the
                        # comment character to the end of the line
                        line = line[:ch_count].strip()
                        break

            if import_statement == True:
                if current_indentation == compare_indentation:
                    for module in line.split(","):
                        module_name = module.strip()
                        if module_name != "":
                            import_node = NimNode()
                            import_node.name = module_name
                            import_node.description = "import"
                            import_node.line = line_count + line_offset
                            input_node.imports.append(import_node)
                elif current_indentation < compare_indentation:
                    import_statement = False
            elif type_statement == True:
                if current_indentation == compare_indentation:
                    type_node = NimNode()
                    type_node.name = line.split("=")[0].strip()
                    type_node.description = "type"
                    type_node.line = line_count + line_offset
                    input_node.types.append(type_node)
                elif current_indentation < compare_indentation:
                    type_statement = False
            elif const_statement == True:
                if current_indentation == compare_indentation:
                    const_node = NimNode()
                    if ":" in line:
                        const_node.name = line.split(":")[0].strip()
                        const_node.type = line.split(":")[1].split("=")[0].strip()
                    else:
                        const_node.name = line.split("=")[0].strip()
                        const_node.type = None
                    if const_node.name[0].isalpha():
                        const_node.description = "const"
                        const_node.line = line_count + line_offset
                        input_node.consts.append(const_node)
                elif current_indentation < compare_indentation:
                    const_statement = False
            elif let_statement == True:
                if current_indentation == compare_indentation:
                    let_node = NimNode()
                    if ":" in line:
                        let_node.name = line.split(":")[0].strip()
                        let_node.type = line.split(":")[1].split("=")[0].strip()
                    else:
                        let_node.name = line.split("=")[0].strip()
                        let_node.type = None
                    if let_node.name[0].isalpha():
                        let_node.description = "let"
                        let_node.line = line_count + line_offset
                        input_node.lets.append(let_node)
                elif current_indentation < compare_indentation:
                    let_statement = False
            elif var_statement == True:
                if current_indentation == compare_indentation:
                    if (
                        ":" in line
                        and "=" in line
                        and (line.find(":") < line.find("="))
                    ):
                        type = line.split(":")[1].split("=")[0].strip()
                        line = line.split(":")[0].strip()
                    elif ":" in line and not ("=" in line):
                        type = line.split(":")[1].strip()
                        line = line.split(":")[0].strip()
                    elif "=" in line:
                        type = line.split("=")[1][: line.find("(")].strip()
                        line = line.split("=")[0].strip()
                    for var in line.split(","):
                        var_name = var.strip()
                        if var_name != "" and var_name[0].isalpha():
                            var_node = NimNode()
                            var_node.name = var.strip()
                            var_node.description = "var"
                            var_node.type = type
                            var_node.line = line_count + line_offset
                            input_node.vars.append(var_node)
                elif current_indentation < compare_indentation:
                    var_statement = False
            elif proc_statement == True:
                proc_statement = False
            elif converter_statement == True:
                converter_statement = False
            elif iterator_statement == True:
                iterator_statement = False
            elif method_statement == True:
                method_statement = False
            elif macro_statement == True:
                macro_statement = False
            elif template_statement == True:
                template_statement = False
            elif class_statement == True:
                class_statement = False
            elif namespace_statement == True:
                namespace_statement = False
            elif property_statement == True:
                property_statement = False

            # Testing for base level declarations
            if line.startswith("import ") or line == "import":
                if line == "import":
                    import_statement = True
                    compare_indentation = get_next_blocks_indentation(
                        line_count + 1, code_lines
                    )
                else:
                    line = line.replace("import", "")
                    for module in line.split(","):
                        module_name = module.strip()
                        if module_name != "":
                            import_node = NimNode()
                            import_node.name = module_name
                            import_node.description = "import"
                            import_node.line = line_count + line_offset
                            input_node.imports.append(import_node)
            elif line.startswith("type ") or line == "type":
                if line == "type":
                    type_statement = True
                    compare_indentation = get_next_blocks_indentation(
                        line_count + 1, code_lines
                    )
                else:
                    line = line.replace("type", "")
                    type_node = NimNode()
                    type_node.name = line.split("=")[0].strip()
                    type_node.description = "type"
                    type_node.line = line_count + line_offset
                    input_node.types.append(type_node)
            elif line.startswith("const ") or line == "const":
                if line == "const":
                    const_statement = True
                    compare_indentation = get_next_blocks_indentation(
                        line_count + 1, code_lines
                    )
                else:
                    line = line.replace("const", "")
                    const_node = NimNode()
                    if ":" in line:
                        const_node.name = line.split(":")[0].strip()
                        const_node.type = line.split(":")[1].split("=")[0].strip()
                    else:
                        const_node.name = line.split("=")[0].strip()
                        const_node.type = None
                    const_node.description = "const"
                    const_node.line = line_count + line_offset
                    input_node.consts.append(const_node)
            elif line.startswith("let ") or line == "let":
                if line == "let":
                    let_statement = True
                    compare_indentation = get_next_blocks_indentation(
                        line_count + 1, code_lines
                    )
                else:
                    line = line.replace("let", "")
                    let_node = NimNode()
                    if ":" in line:
                        let_node.name = line.split(":")[0].strip()
                        let_node.type = line.split(":")[1].split("=")[0].strip()
                    else:
                        let_node.name = line.split("=")[0].strip()
                        let_node.type = None
                    let_node.description = "let"
                    let_node.line = line_count + line_offset
                    input_node.lets.append(let_node)
            elif line.startswith("var ") or line == "var":
                if line == "var":
                    var_statement = True
                    compare_indentation = get_next_blocks_indentation(
                        line_count + 1, code_lines
                    )
                else:
                    line = line.replace("var", "")
                    if (
                        ":" in line
                        and "=" in line
                        and (line.find(":") < line.find("="))
                    ):
                        type = line.split(":")[1].split("=")[0].strip()
                        line = line.split(":")[0].strip()
                    elif ":" in line and not ("=" in line):
                        type = line.split(":")[1].strip()
                        line = line.split(":")[0].strip()
                    elif "=" in line:
                        type = line.split("=")[1][: line.find("(")].strip()
                        line = line.split("=")[0].strip()
                    for var in line.split(","):
                        var_name = var.strip()
                        if var_name != "":
                            var_node = NimNode()
                            var_node.name = var_name
                            var_node.description = "var"
                            var_node.type = type
                            var_node.line = line_count + line_offset
                            input_node.vars.append(var_node)
            elif line.startswith("proc "):
                # Create and add the procedure node
                proc_node = NimNode()
                proc_node, skip_to_line = create_node(
                    proc_node, "proc", line, line_count, code_lines, line_offset
                )
                proc_node.description = "procedure"
                proc_node.line = line_count + line_offset
                # Add the procedure to the main node
                if proc_node.type == "forward declaration":
                    input_node.forward_declarations.append(proc_node)
                else:
                    input_node.procedures.append(proc_node)
                # Set the procedure flag
                proc_statement = True
            elif line.startswith("converter "):
                # Create and add the converter node
                converter_node = NimNode()
                converter_node, skip_to_line = create_node(
                    converter_node,
                    "converter",
                    line,
                    line_count,
                    code_lines,
                    line_offset,
                )
                converter_node.description = "converter"
                converter_node.line = line_count + line_offset
                # Add the converter to the main node
                input_node.converters.append(converter_node)
                # Set the converter flag
                converter_statement = True
            elif line.startswith("iterator "):
                # Create and add the converter node
                iterator_node = NimNode()
                iterator_node, skip_to_line = create_node(
                    iterator_node, "iterator", line, line_count, code_lines, line_offset
                )
                iterator_node.description = "iterator"
                iterator_node.line = line_count + line_offset
                # Add the iterator to the main node
                input_node.iterators.append(iterator_node)
                # Set the iterator flag
                iterator_statement = True
            elif line.startswith("method "):
                # Create and add the method node
                method_node = NimNode()
                method_node, skip_to_line = create_node(
                    method_node, "method", line, line_count, code_lines, line_offset
                )
                method_node.description = "method"
                method_node.line = line_count + line_offset
                # Add the procedure to the main node
                input_node.methods.append(method_node)
                # Set the method flag
                method_statement = True
            elif line.startswith("property "):
                # Create and add the property node
                property_node = NimNode()
                property_node, skip_to_line = create_node(
                    property_node, "property", line, line_count, code_lines, line_offset
                )
                property_node.description = "property"
                property_node.line = line_count + line_offset
                # Add the property to the parent node
                input_node.properties.append(property_node)
                # Set the property flag
                property_statement = True
            elif line.startswith("macro "):
                # Create and add the macro node
                macro_node = NimNode()
                macro_node, skip_to_line = create_node(
                    macro_node, "macro", line, line_count, code_lines, line_offset
                )
                macro_node.description = "macro"
                macro_node.line = line_count + line_offset
                # Add the procedure to the main node
                input_node.macros.append(macro_node)
                # Set the macro flag
                macro_statement = True
            elif line.startswith("template "):
                # Create and add the template node
                template_node = NimNode()
                template_node, skip_to_line = create_node(
                    template_node, "template", line, line_count, code_lines, line_offset
                )
                template_node.description = "template"
                template_node.line = line_count + line_offset
                # Add the procedure to the main node
                input_node.templates.append(template_node)
                # Set the template flag
                template_statement = True
            elif line.startswith("class "):
                # Create and add the class node
                search_term = "class"
                object_node = NimNode()
                object_node, skip_to_line = create_node(
                    object_node, search_term, line, line_count, code_lines, line_offset
                )
                object_node.description = search_term
                object_node.line = line_count + line_offset
                # Add the class to the main node
                input_node.objects.append(object_node)
                # Set the class flag
                class_statement = True
            elif line.startswith("namespace "):
                # Create and add the class node
                namespace_node = NimNode()
                namespace_node, skip_to_line = create_node(
                    namespace_node,
                    "namespace",
                    line,
                    line_count,
                    code_lines,
                    line_offset,
                )
                namespace_node.description = "namespace"
                namespace_node.line = line_count + line_offset
                # Add the class to the main node
                input_node.namespaces.append(namespace_node)
                # Set the class flag
                namespace_statement = True
        return input_node

    # Parse the main node
    main_node = parse_node(main_node, nim_code_lines)
    # Return the node list
    return main_node


def get_python_node_list(python_code):
    """
    Parse the text and return nodes as a list.
    The text must be valid Python 3 code.
    """

    # Nested function for recursivly traversing all the child nodes
    def check_children(node, level, function_list):
        lst = []
        for i in ast.iter_child_nodes(node):
            if isinstance(i, ast.ClassDef) or isinstance(i, ast.FunctionDef):
                if isinstance(i, ast.FunctionDef):
                    # Remove the function from the global function list
                    if i in function_list:
                        function_list.remove(i)
                lst.append((level, i))
            # Always descend into the child node to check for nested functions/classes
            lst.extend(check_children(i, level + 1, function_list))
        return lst

    # Parse the file
    parsed_string = ast.parse(python_code)
    nodes = [node for node in ast.walk(parsed_string)]
    # Get import/import_from nodes, combine them into one list and sort them
    import_nodes = [
        (node.names[0].name, node.lineno)
        for node in nodes
        if isinstance(node, ast.Import)
    ]
    importfrom_nodes = [
        (node.module, node.lineno) for node in nodes if isinstance(node, ast.ImportFrom)
    ]
    import_nodes.extend(importfrom_nodes)
    import_nodes.sort(key=operator.itemgetter(0))
    # Other nodes
    class_nodes = [node for node in nodes if isinstance(node, ast.ClassDef)]
    function_nodes = [node for node in nodes if isinstance(node, ast.FunctionDef)]
    global_vars = [node for node in nodes if isinstance(node, ast.Name)]
    # Get child nodes for all of the classes
    children = []
    class_tree_nodes = []
    for c_node in class_nodes:
        # Check if the node has already been parsed as a child node in another class
        if not (c_node in children):
            cc = check_children(c_node, 0, function_nodes)
            class_tree_nodes.append((c_node, cc))
            children.extend([c[1] for c in cc])
    # Return the parse results
    return import_nodes, class_tree_nodes, function_nodes, global_vars


def get_python_node_tree(python_code):
    """
    Parse the text and return nodes as a nested tree.
    The text must be valid Python 3 code.
    """

    # Node object
    class PythonNode:
        def __init__(self, name, type, line_number, level):
            self.name = name
            self.type = type
            self.line_number = line_number
            self.level = level
            self.children = []

    # Main parsing function
    def parse_node(ast_node, level, parent_node=None):
        new_node = None
        if isinstance(ast_node, ast.ClassDef):
            new_node = PythonNode(ast_node.name, "class", ast_node.lineno, level)
            for child_node in ast_node.body:
                result = parse_node(child_node, level + 1, new_node)
                if result != None:
                    if isinstance(result, list):
                        for n in result:
                            new_node.children.append(n)
                    else:
                        new_node.children.append(result)
            new_node.children = sorted(new_node.children, key=lambda x: x.name)
        elif isinstance(ast_node, ast.FunctionDef):
            new_node = PythonNode(ast_node.name, "function", ast_node.lineno, level)
            for child_node in ast_node.body:
                result = parse_node(child_node, level + 1, new_node)
                if result != None:
                    if isinstance(result, list):
                        for n in result:
                            new_node.children.append(n)
                    else:
                        new_node.children.append(result)
            new_node.children = sorted(new_node.children, key=lambda x: x.name)
        elif isinstance(ast_node, ast.Import):
            new_nodes = []
            for imp in ast_node.names:
                new_node = PythonNode(imp.name, "import", ast_node.lineno, level)
                new_nodes.append(new_node)
            return new_nodes
        elif isinstance(ast_node, ast.Assign) and (level == 0 or parent_node == None):
            # Globals that do are not defined with the 'global' keyword,
            # but are defined on the top level
            new_nodes = []
            for target in ast_node.targets:
                if hasattr(target, "id") == True:
                    name = target.id
                    if not (name in globals_list):
                        new_nodes.append(
                            PythonNode(name, "global_variable", ast_node.lineno, level)
                        )
                        globals_list.append(name)
            return new_nodes
        elif isinstance(ast_node, ast.AnnAssign) and (
            level == 0 or parent_node == None
        ):
            # Type annotated globals
            new_nodes = []
            target = ast_node.target
            if hasattr(target, "id") == True:
                name = target.id
                if not (name in globals_list):
                    new_nodes.append(
                        PythonNode(name, "global_variable", ast_node.lineno, level)
                    )
                    globals_list.append(name)
            return new_nodes
        elif isinstance(ast_node, ast.Global):
            # Globals can be nested somewhere deep in the AST, so they
            # are appended directly into the non-local python_node_tree list
            for name in ast_node.names:
                if not (name in globals_list):
                    python_node_tree.append(
                        PythonNode(name, "global_variable", ast_node.lineno, level)
                    )
                    globals_list.append(name)
        else:
            if parent_node != None and hasattr(ast_node, "body"):
                for child_node in ast_node.body:
                    result = parse_node(child_node, level + 1, parent_node)
                    if result != None:
                        if isinstance(result, list):
                            for n in result:
                                parent_node.children.append(n)
                        else:
                            parent_node.children.append(result)
                parent_node.children = sorted(
                    parent_node.children, key=lambda x: x.name
                )
            else:
                new_nodes = []
                if hasattr(ast_node, "body"):
                    for child_node in ast_node.body:
                        result = parse_node(child_node, level + 1, None)
                        if result != None:
                            if isinstance(result, list):
                                for n in result:
                                    new_nodes.append(n)
                            else:
                                new_nodes.append(result)
                if hasattr(ast_node, "orelse"):
                    for child_node in ast_node.orelse:
                        result = parse_node(child_node, level + 1, None)
                        if result != None:
                            if isinstance(result, list):
                                for n in result:
                                    new_nodes.append(n)
                            else:
                                new_nodes.append(result)
                if hasattr(ast_node, "finalbody"):
                    for child_node in ast_node.finalbody:
                        result = parse_node(child_node, level + 1, None)
                        if result != None:
                            if isinstance(result, list):
                                for n in result:
                                    new_nodes.append(n)
                            else:
                                new_nodes.append(result)
                if hasattr(ast_node, "handlers"):
                    for child_node in ast_node.handlers:
                        result = parse_node(child_node, level + 1, None)
                        if result != None:
                            if isinstance(result, list):
                                for n in result:
                                    new_nodes.append(n)
                            else:
                                new_nodes.append(result)
                if new_nodes != []:
                    return new_nodes
        return new_node

    # Initialization
    parsed_string = ast.parse(python_code)
    python_node_tree = []
    # List of globals for testing for duplicates
    globals_list = []
    # Parse the nodes recursively
    for node in ast.iter_child_nodes(parsed_string):
        result = parse_node(node, 0)
        if result != None:
            if isinstance(result, list):
                for n in result:
                    python_node_tree.append(n)
            else:
                python_node_tree.append(result)
    # Sort the node list
    python_node_tree = sorted(python_node_tree, key=lambda x: x.name)
    # Return the resulting tree
    return python_node_tree


def remove_comments_from_c_code(c_code):
    """
    Remove single and multiline comments from C source code
    """
    code_list = c_code.split("\n")
    no_comment_code_list = []
    commenting = False
    for line in code_list:
        if commenting == False:
            if '"' in line and "//" in line:
                stringing = False
                for i, ch in enumerate(line):
                    if ch == '"' and stringing == False:
                        stringing = True
                    elif ch == '"' and line[i - 1] != "\\" and stringing == True:
                        stringing = False
                    elif stringing == False and line[i : i + 2] == "//":
                        line = line[:i]
                        break
                no_comment_code_list.append(line)
            elif '"' in line and "/*" in line:
                stringing = False
                for i, ch in enumerate(line):
                    if ch == '"' and stringing == False:
                        stringing = True
                    elif ch == '"' and line[i - 1] != "\\" and stringing == True:
                        stringing = False
                    elif stringing == False and line[i : i + 2] == "/*":
                        # Remove the closed comments
                        rest_line = re.sub(r"/\*.*?\*/", "", line[i:], flags=re.DOTALL)
                        line = line[:i] + rest_line
                        # Check again if there is a comment sequence left in the line
                        if "/*" in rest_line:
                            line = line[:i] + rest_line[: line.find("/*")]
                            commenting = True
                            break
                no_comment_code_list.append(line)
            elif "//" in line:
                if line.strip().startswith("//"):
                    continue
                else:
                    line = line[: line.find("//")]
                    no_comment_code_list.append(line)
            elif "/*" in line:
                # Remove the closed comments
                line = re.sub(r"/\*.*?\*/", "", line, flags=re.DOTALL)
                # Check again if there is a comment sequence left in the line
                if "/*" in line:
                    line_to_comment = line[: line.find("/*")]
                    if line_to_comment.strip() != "":
                        no_comment_code_list.append(line_to_comment)
                    commenting = True
                else:
                    no_comment_code_list.append(line)
            else:
                no_comment_code_list.append(line)
        else:
            if "*/" in line:
                # Remove the closed comments
                line = re.sub(r"/\*.*?\*/", "", line, flags=re.DOTALL)
                if "*/" in line:
                    if line.strip().endswith("*/"):
                        commenting = False
                    else:
                        line = line[line.find("/*") + 2 :]
                        no_comment_code_list.append(line)
                        commenting = False
    # Return the result
    result = "\n".join(no_comment_code_list)
    return result


def get_c_function_list(c_code):
    """
    Parse the text and return all C functions as a list.
    Made as simple as possible.
    The text must be valid C code.
    """
    # Store the text
    text = c_code
    # Initialize state variables
    curly_count = 0
    parenthesis_count = 0
    singleline_commenting = False
    multiline_commenting = False
    stringing = False
    previous_token = ""
    last_found_function = ""
    last_line = 0
    current_line = 1
    function_list = []
    # Tokenize the text and remove the space characters
    splitter = re.compile(r"(\#\w+|\'|\"|\n|\s+|\w+|\W)")
    tokens = [token for token in splitter.findall(text)]
    # Main Loop for filtering tokens
    for i, token in enumerate(tokens):
        stripped_token = token.strip()
        if "\n" in token:
            newline_count = token.count("\n")
            current_line += newline_count
            # Reset the single line comment flag
            singleline_commenting = False
        if stripped_token == "":
            continue
        # Check for function definitions
        if curly_count == 0:
            if multiline_commenting == False and singleline_commenting == False:
                if token == "{" and previous_token == ")":
                    # The function has passed the filter, add it to the list
                    function_list.append((last_found_function, last_line))
                elif (
                    token == "("
                    and re.match(r"\w", previous_token)
                    and parenthesis_count == 0
                ):
                    last_found_function = previous_token
                    last_line = current_line
        # Check for various state changes
        if (
            multiline_commenting == False
            and singleline_commenting == False
            and stringing == False
        ):
            if token == "{":
                curly_count += 1
            elif token == "}":
                curly_count -= 1
            elif token == "(":
                parenthesis_count += 1
            elif token == ")":
                parenthesis_count -= 1
            elif token == "*" and previous_token == "/":
                multiline_commenting = True
            elif token == "/" and previous_token == "/":
                singleline_commenting = True
        else:
            if token == "/" and previous_token == "*":
                multiline_commenting = False
        # Store the previous token
        if stripped_token != "":
            previous_token = token

    # Sort the functions alphabetically
    def compare_function(item):
        return item[0].lower()

    function_list = sorted(function_list, key=compare_function)
    # Return the function list
    return function_list


def get_node_tree_with_ctags(code, parser):
    # Node object
    class CNode:
        def __init__(self, in_name, in_type, in_line_number, in_level, in_parent=None):
            self.name = in_name.strip()
            self.type = in_type
            self.line_number = in_line_number
            self.level = in_level
            self.parent_type = None
            self.parent = None
            if in_parent is not None:
                self.parent_type = in_parent[0].strip()
                self.parent = in_parent[1].strip()
            self.children = []

    #    # Ctags symbol dictionary
    #    ctags_description_string = """
    #        #LETTER NAME       ENABLED REFONLY NROLES MASTER DESCRIPTION
    #        L       label      no      no      0      C      goto labels
    #        d       macro      yes     no      1      C      macro definitions
    #        e       enumerator yes     no      0      C      enumerators (values inside an enumeration)
    #        f       function   yes     no      0      C      function definitions
    #        g       enum       yes     no      0      C      enumeration names
    #        h       header     yes     yes     2      C      included header files
    #        l       local      no      no      0      C      local variables
    #        m       member     yes     no      0      C      struct, and union members
    #        p       prototype  no      no      0      C      function prototypes
    #        s       struct     yes     no      0      C      structure names
    #        t       typedef    yes     no      0      C      typedefs
    #        u       union      yes     no      0      C      union names
    #        v       variable   yes     no      0      C      variable definitions
    #        x       externvar  no      no      0      C      external and forward variable declarations
    #        z       parameter  no      no      0      C      function parameters inside function definitions
    #    """
    #    c_symbols = dict(
    #        [(x.split()[0], x.split()[1])
    #            for x in ctags_description_string.splitlines()
    #                if x.strip() != ""][1:]
    #    )

    global ctags_program
    # Test for ctags on the system
    ctags_test = ("ctags_present" in locals()) or ("ctags_present" in globals())
    if ctags_test == False:
        global ctags_present
        ctags_present = False
        ctags_program = "ctags"
        try:
            if data.platform == "Windows":
                # SW_HIDE option hides the poping up of the console window on Windows
                si = subprocess.STARTUPINFO()
                si.dwFlags = subprocess.STARTF_USESHOWWINDOW
                si.wShowWindow = subprocess.SW_HIDE
                output = subprocess.Popen(
                    [ctags_program, "--version"],
                    stdout=subprocess.PIPE,
                    startupinfo=si,
                    shell=False,
                ).communicate()[0]
            else:
                output = subprocess.Popen(
                    [ctags_program, "--version"], stdout=subprocess.PIPE, shell=False
                ).communicate()[0]
            output_utf = output.decode("utf-8")
            if output_utf.startswith("Exuberant Ctags") or output_utf.startswith(
                "Universal Ctags"
            ):
                ctags_present = True
        except Exception as ex:
            if data.platform == "Windows":
                repl_print(
                    "Windows operating system detected.\n "
                    + "Using Universal Ctags program from the resources directory."
                )
                ctags_program = os.path.join(
                    data.resources_directory, "programs/ctags.exe"
                ).replace("\\", "/")
                ctags_present = True
            else:
                repl_print(ex)
                ctags_present = False
                raise Exception(
                    "Exuberant or Universal Ctags (ctags) could not be found on the system!\n"
                    + "If you are using a Debian based operating system,\n"
                    + "try executing 'sudo apt-get install exuberant-ctags' to install Exuberant-Ctags."
                )
    # Create the file for parsing
    filename = "temporary_ctags_file"
    replace_word = "/\\/"
    if parser == "JSON":
        filtered_code = code.replace(".", replace_word)
    else:
        filtered_code = code
    with open(filename, "w+") as f:
        f.write(filtered_code)
        f.close()
    # Parse the file with ctags
    try:
        if parser == "ASSEMBLY":
            flags = (
                "-R",
                "--fields=-f-k-t+K+n",
                "--excmd=number",
                "--language-force=Asm",
            )
        elif parser == "C":
            flags = (
                "-R",
                "--fields=-f-k-t+K+n",
                "--kinds-C=+px",
                "--excmd=number",
                "--language-force=C",
            )
        elif parser == "C++":
            flags = (
                "-R",
                "--fields=-f-k-t+K+n",
                "--kinds-C++=+px",
                "--excmd=number",
                "--language-force=C++",
            )
        elif parser == "D":
            flags = (
                "-R",
                "--fields=-f-k-t+K+n",
                "--kinds-D=+px",
                "--excmd=number",
                "--language-force=D",
            )
        elif parser == "PASCAL":
            flags = (
                "-R",
                "--fields=-f-k-t+K+n",
                "--excmd=number",
                "--language-force=Pascal",
            )
        elif parser == "PHP":
            flags = (
                "-R",
                "--fields=-f-k-t+K+n",
                "--excmd=number",
                "--language-force=Php",
            )
        elif parser == "JAVASCRIPT":
            flags = (
                "-R",
                "--fields=-f-k-t+K+n",
                "--excmd=number",
                "--language-force=Javascript",
            )
        elif parser == "MAKEFILE":
            flags = (
                "-R",
                "--fields=-f-k-t+K+n",
                "--excmd=number",
                "--language-force=Make",
            )
        elif parser == "HTML":
            flags = (
                "-R",
                "--fields=-f-k-t+K+n",
                "--excmd=number",
                "--language-force=HTML",
            )
        else:
            raise Exception("[Ctags-parsing] Unsupported file type: {}".format(parser))
        if data.platform == "Windows":
            # SW_HIDE option hides the poping up of the console window on Windows
            si = subprocess.STARTUPINFO()
            si.dwFlags = subprocess.STARTF_USESHOWWINDOW
            si.wShowWindow = subprocess.SW_HIDE
            output = subprocess.Popen(
                [
                    ctags_program,
                    *flags,
                    "--output-format=json",
                    filename,
                ],
                stdout=subprocess.PIPE,
                startupinfo=si,
                shell=False,
            ).communicate()[0]
        else:
            output = subprocess.Popen(
                [ctags_program, *flags, "--output-format=json", filename],
                stdout=subprocess.PIPE,
                shell=False,
            ).communicate()[0]
        output_utf = output.decode("utf-8")
    #        with open("D:/ctags.out.json", 'w+', encoding="utf-8") as f:
    #            lines = f.write(output_utf)
    #            f.close()
    except Exception as ex:
        repl_print(ex)
        raise Exception("Parse error!")
    # Initialize state variables
    main_node = CNode("module", "", 0, -1)
    main_node_list = []
    main_current_line = 1

    # Function for adding a node
    def add_node(in_node):
        if main_node != None:
            main_node.children.append(in_node)
        else:
            main_node_list.append(in_node)

    main_node = CNode("module", "", 0, -1)

    # Parse the output (NEW)
    for line in output_utf.split("\n"):
        # Parse JSON
        if line.strip() == "":
            continue
        try:
            json_data = json.loads(line)
        except:
            traceback.print_exc()
            continue
        # Skip non-tag items
        if json_data["_type"] != "tag":
            continue

        name = json_data["name"]
        line_number = json_data["line"]
        kind = json_data["kind"]
        parent = None
        if "scope" in json_data.keys():
            parent_name = json_data["scope"]
            parent_type = json_data["scopeKind"]
            parent = (parent_type, parent_name)
        add_node(CNode(name, kind, line_number, 0, in_parent=parent))

    # Delete the temporary parsing file
    os.remove(filename)

    # Sort the nodes alphabetically
    def compare_function(item):
        return item.name.lower()

    main_node_list = sorted(main_node_list, key=compare_function)
    main_node_list.append(main_node)
    return main_node_list


def get_c_node_tree(c_code):
    """
    THIS IS A WORK IN PROGRESS ROUTINE!!! IT IS IN A SOMEWHAT USABLE STATE.
    """

    # Node object
    class CNode:
        def __init__(self, in_name, in_type, in_line_number, in_level, in_parent=None):
            self.name = in_name.strip()
            self.type = in_type
            self.line_number = in_line_number
            self.level = in_level
            self.parent = in_parent
            self.children = []

    # C keywords
    keywords = [
        "auto",
        "break",
        "case",
        "const",
        "continue",
        "default",
        "do",
        "else",
        "enum",
        "extern",
        "for",
        "goto",
        "if",
        "register",
        "return",
        "signed",
        "sizeof",
        "static",
        "struct",
        "switch",
        "typedef",
        "union",
        "unsigned",
        "volatile",
        "while",
        "pragma",
    ]
    composite_types = ["typedef", "union", "enum", "struct"]
    macros = ["define", "include", "pragma", "undef", "error"]
    skip_macros = ["if", "ifdef", "ifndef", "else", "endif"]
    """
    Parsing
    """
    # Store the text
    text = c_code
    # Initialize state variables
    main_node = CNode("module", "", 0, -1)  # None
    main_current_line = 1
    main_node_list = [main_node]

    # Function for adding a node
    def add_node(in_node):
        if main_node != None:
            main_node.children.append(in_node)
        else:
            main_node_list.append(in_node)

    # Debugging helpers
    def debug_print(level, *args, **kwargs):
        if False:
            print(level * "    ", *args, **kwargs)

    # Tokenize the text and remove the space characters
    #    splitter = re.compile(r"(\#\s*\w+|\'|\"|\n|\s+|\w+|\W)")
    splitter = re.compile(r"(\#\s*\w+|\n|\s+|\w+|\W)")
    main_tokens = [token for token in splitter.findall(text)]

    # Main parse function
    def parse_loop(tokens, node_list, current_line, index, level):
        singleline_commenting = False
        multiline_commenting = False

        macroing = False
        macro_type = ""
        macro_line = ""
        macro_tokens = []

        stringing = False
        charactering = False

        previous_token = ""
        current_line_tokens = []
        current_statement_tokens = []
        previous_unfiltered_token = None

        skip_to_token = None

        # Main Loop for filtering tokens
        for i, token in enumerate(tokens):
            stripped_token = token.strip()
            # Store the previous token
            if i > 0:
                previous_unfiltered_token = tokens[i - 1]
                if stripped_token != "":
                    previous_token = token
            else:
                previous_unfiltered_token = ""
                previous_token = ""
            # Store the next token
            if i < len(tokens) - 2:
                next_token = tokens[i + 1]
            else:
                next_token = ""

            if "\n" in token:
                # Increase the line counter
                newline_count = token.count("\n")
                current_line += newline_count

                # Reset the line token list
                current_line_tokens = []
                # Reset the single line comment and string flags
                singleline_commenting = False
                stringing = False

            if skip_to_token != None:
                if skip_to_token >= i:
                    continue
                else:
                    skip_to_token = None

            # Check for various special characters
            if "\n" in token:
                if previous_unfiltered_token != "\\":
                    # Check the macro type
                    if macro_type == "include":
                        filtered_macro_tokens = []
                        previous_token = ""
                        for m in macro_tokens:
                            if (m == "*" and previous_token == "/") or (
                                m == "/" and previous_token == "/"
                            ):
                                filtered_macro_tokens = filtered_macro_tokens[:-2]
                                break
                            filtered_macro_tokens.append(m)
                            previous_token = m
                        include_string = "".join(filtered_macro_tokens)
                        debug_print(
                            level,
                            "Found include:\n",
                            (level + 1) * "    ",
                            include_string,
                        )
                        add_node(CNode(include_string, "include", macro_line, 0))
                    elif macro_type == "define":
                        define_macro = macro_tokens[0]
                        debug_print(
                            level, "Found define:\n", (level + 1) * "    ", define_macro
                        )
                        add_node(CNode(define_macro, "define", macro_line, 0))
                    elif macro_type == "undef":
                        undef_macro = macro_tokens[0]
                        debug_print(
                            level, "Found undef:\n", (level + 1) * "    ", undef_macro
                        )
                        add_node(CNode(undef_macro, "undef", macro_line, 0))
                    elif macro_type == "pragma":
                        pragma_macro = macro_tokens[0]
                        # Watcom compiler 'aux' keyword check
                        if pragma_macro == "aux":
                            pragma_macro = macro_tokens[1]
                        debug_print(
                            level, "Found pragma:\n", (level + 1) * "    ", pragma_macro
                        )
                        add_node(CNode(pragma_macro, "pragma", macro_line, 0))
                    elif macro_type == "error":
                        error_macro = " ".join(macro_tokens)[:10] + "..."
                        debug_print(
                            level, "Found error:\n", (level + 1) * "    ", error_macro
                        )
                        add_node(CNode(error_macro, "error", macro_line, 0))
                    # Reset the macroing flag
                    macro_tokens = []
                    macroing = False
                    macro_type = ""

            # Check for an empty token
            if stripped_token == "":
                previous_unfiltered_token = stripped_token
                continue

            if multiline_commenting == True:
                if token == "/" and previous_token == "*":
                    multiline_commenting = False
            elif singleline_commenting == True:
                pass
            elif macroing == True:
                macro_tokens.append(token)
            elif stringing == True:
                if token == '"' and previous_token != "\\":
                    stringing = False
            elif charactering == True:
                if token == "'" and previous_token != "\\":
                    charactering = False
            else:
                current_line_tokens.append(token)

                if token == "*" and previous_unfiltered_token == "/":
                    current_statement_tokens = current_statement_tokens[:-1]
                    multiline_commenting = True
                elif token == "/" and previous_unfiltered_token == "/":
                    current_statement_tokens = current_statement_tokens[:-1]
                    singleline_commenting = True
                elif token == '"':
                    stringing = True
                elif token == "'":
                    charactering = True
                elif token == ";":
                    current_statement_tokens.append(token)
                    first_word = current_statement_tokens[0]
                    if first_word in composite_types:
                        type_desc = first_word
                        if current_statement_tokens[-2].isidentifier():
                            type_name = current_statement_tokens[-2]
                        elif current_statement_tokens[1].isidentifier() and not (
                            current_statement_tokens[1] in keywords
                        ):
                            type_name = current_statement_tokens[1]
                        else:
                            for t in current_statement_tokens:
                                if t.startswith("( *"):
                                    type_name = t[3:-2]
                                    break
                            else:
                                raise Exception(
                                    "'{}' (line:{}) has unknown name! ({})".format(
                                        type_desc,
                                        current_line,
                                        current_statement_tokens,
                                    )
                                )
                        body_test = (
                            current_statement_tokens[-2] == "{ ... }"
                            or current_statement_tokens[-3] == "{ ... }"
                        )
                        if type_name.isidentifier() and body_test:
                            debug_print(
                                level,
                                "Found {}:\n".format(type_desc),
                                (level + 1) * "    ",
                                type_name,
                            )
                            add_node(CNode(type_name, type_desc, current_line, 0))
                    else:

                        def parse_funcs(in_list, pos=0):
                            if in_list == None:
                                return
                            return_list = []
                            for i, item in enumerate(in_list):
                                if item.strip() == "":
                                    continue
                                elif item.startswith("("):
                                    try:
                                        if in_list[i - 1].isidentifier() and not (
                                            in_list[i - 1] in keywords
                                        ):
                                            func = return_list.pop()
                                            return_list.append(func + item)
                                    except:
                                        return_list.append(item)
                                else:
                                    return_list.append(item)
                            return return_list

                        try:
                            result = parse_funcs(current_statement_tokens)
                            #                            print(result)
                            length = len(result)
                            if (
                                "(" in result[-2]
                                and ")" in result[-2]
                                and not ("=" in result[-2])
                                and level == 0
                                and result[-2][: result[-2].find("(")].isidentifier()
                            ):
                                name = current_statement_tokens[-3]
                                if "(" in name and ")" in name and name[2] == "*":
                                    prototype = name[3:-1]
                                else:
                                    prototype = result[-2][: result[-2].find("(")]
                                add_node(CNode(prototype, "prototype", current_line, 0))
                                debug_print(
                                    level,
                                    "Found prototype 0:\n",
                                    (level + 1) * "    ",
                                    prototype,
                                )
                            elif length == 3:
                                if (
                                    "(" in result[1]
                                    and ")" in result[1]
                                    and (level == 0)
                                ):
                                    prototype = result[1][: result[1].find("(")]
                                    add_node(
                                        CNode(prototype, "prototype", current_line, 0)
                                    )
                                    debug_print(
                                        level,
                                        "Found prototype 1:\n",
                                        (level + 1) * "    ",
                                        prototype,
                                    )
                                elif (
                                    result[1].isidentifier()
                                    and not ("=" in result)
                                    and (level == 0)
                                ):
                                    variable = result[1]
                                    add_node(CNode(variable, "var", current_line, 0))
                                    debug_print(
                                        level,
                                        "Found variable 0:\n",
                                        (level + 1) * "    ",
                                        variable,
                                    )
                                else:
                                    pass
                            elif "," in result:
                                # Multiple variable declarations delimited with ','
                                if level == 0:
                                    groups = []
                                    current_group = []
                                    for t in result:
                                        if t == "," or t == ";":
                                            groups.append(current_group)
                                            current_group = []
                                        else:
                                            current_group.append(t)
                                    for g in groups:
                                        if "=" in g:
                                            equal_index = g.index("=")
                                            var_name = g[equal_index - 1]
                                        else:
                                            if ("[" in g) and ("]" in g):
                                                open_index = g.index("[")
                                                var_name = g[open_index - 1]
                                            else:
                                                var_name = g[-1]
                                        if var_name.isidentifier():
                                            add_node(
                                                CNode(var_name, "var", current_line, 0)
                                            )
                                            debug_print(
                                                level,
                                                "Found variable 1:\n",
                                                (level + 1) * "    ",
                                                var_name,
                                            )
                            elif (
                                result[-2].isidentifier()
                                and not ("=" in result)
                                and (level == 0)
                            ):
                                variable = result[-2]
                                add_node(CNode(variable, "var", current_line, 0))
                                debug_print(
                                    level,
                                    "Found variable 2:\n",
                                    (level + 1) * "    ",
                                    variable,
                                )
                            elif (
                                "=" in result
                                and result[result.index("=") - 1].isidentifier()
                                and (level == 0)
                            ):
                                variable = result[result.index("=") - 1]
                                add_node(CNode(variable, "var", current_line, 0))
                                debug_print(
                                    level,
                                    "Found variable 3:\n",
                                    (level + 1) * "    ",
                                    variable,
                                )
                            elif (
                                ("[" in result)
                                and ("]" in result)
                                and result[result.index("[") - 1].isidentifier()
                                and (level == 0)
                            ):
                                variable = result[result.index("[") - 1]
                                add_node(CNode(variable, "var", current_line, 0))
                                debug_print(
                                    level,
                                    "Found array variable:\n",
                                    (level + 1) * "    ",
                                    variable,
                                )
                            else:
                                pass
                        except:
                            debug_print(
                                level - 1,
                                "**** UNKNOWN NODE ****",
                                current_line,
                                i + index,
                            )

                    current_statement_tokens = []
                elif "#" in token and any(x for x in macros if x in token):
                    macroing = True
                    macro_type = token.replace("#", "").strip()
                    macro_line = current_line
                    macro_tokens = []
                elif "#" in token and any(x for x in skip_macros if x in token):
                    # Skip macros that do nothing
                    macroing = True
                elif token == "{" and previous_token != "'" and next_token != "'":
                    try:
                        func_found = False
                        if current_statement_tokens[-1] == "( ... )" or (
                            current_statement_tokens[-1].startswith("(")
                            and current_statement_tokens[-1].endswith(")")
                        ):
                            func_name = current_statement_tokens[-2]
                            if func_name.isidentifier() and not (func_name in keywords):
                                add_node(CNode(func_name, "function", current_line, 0))
                                debug_print(
                                    level,
                                    "Found function:\n",
                                    (level + 1) * "    ",
                                    func_name,
                                )
                                func_found = True
                    except:
                        pass
                    if func_found == False and not (
                        any(x in composite_types for x in current_statement_tokens)
                    ):
                        next_level = level
                    else:
                        next_level = level + 1
                    # Start of a block
                    debug_print(level, "{ ", current_statement_tokens)
                    if func_found:
                        debug_print(
                            level,
                            "function start '{}':".format(func_name),
                            "level:",
                            next_level,
                            i,
                        )
                    node_list, skip_to_token = parse_loop(
                        tokens[i + 1 :], node_list, current_line, i + 1, next_level
                    )
                    current_statement_tokens.append("{ ... }")
                    if func_found:
                        debug_print(
                            level, "function end '{}':".format(func_name), skip_to_token
                        )
                        current_statement_tokens = []
                elif token == "}" and previous_token != "'" and next_token != "'":
                    return node_list, i + index
                #                elif token == ')' and previous_token != '\'' and next_token != '\'':
                #                    debug_print(level-1, ')', current_line, i+index)
                #                    return node_list, i+index
                elif token == "(" and previous_token != "'" and next_token != "'":
                    #                    repl_print(previous_token, token, next_token, tokens[i+2], tokens[i+3], tokens[i+4], tokens[i+5], tokens[i+6], tokens[i+7])
                    #                    repl_print(tokens[i+1],tokens[i+2],tokens[i+3],tokens[i+4],tokens[i+5])
                    paren_tokens = ["("]
                    paren_count = 0
                    skip_to_token = i
                    function_flag = False
                    previous_t = None
                    next_t = None
                    for j, t in enumerate(tokens[i + 1 :]):
                        print(paren_count)
                        skip_to_token += 1
                        paren_tokens.append(t)
                        if j > 0:
                            previous_t = tokens[i + 1 :][j - 1]
                        if j < len(tokens[i + 1 :]) - 1:
                            next_t = tokens[i + 1 :][j + 1]
                        if t == "(" and previous_t != "'" and next_t != "'":
                            paren_count += 1
                        if t == ")" and previous_t != "'" and next_t != "'":
                            if paren_count == 0:
                                #                                repl_print(previous_t, t, next_t)
                                try:
                                    tks = tokens[i + 1 :]
                                    for k in range(3):
                                        if "{" in tks[j + 1 + k].strip():
                                            function_flag = True
                                            break
                                except:
                                    pass
                                break
                            else:
                                paren_count -= 1
                    if paren_tokens[1] == "*" and function_flag == False:
                        current_statement_tokens.append(
                            "( {} )".format("".join(paren_tokens[1:-1]))
                        )
                    elif (
                        len(paren_tokens) > 4
                        and paren_tokens[-3] == "*"
                        and paren_tokens[-2].isidentifier()
                        and not ("," in "".join(paren_tokens))
                        and function_flag == False
                    ):
                        current_statement_tokens.append(
                            "( {} )".format("".join(paren_tokens[-3:-1]))
                        )
                    else:
                        current_statement_tokens.append("( ... )")
                    continue
                else:
                    current_statement_tokens.append(token)

        # Return the accumulated node list
        return node_list, skip_to_token

    main_node_list, skip_to_token = parse_loop(
        main_tokens, main_node_list, main_current_line, 0, 0
    )

    # Sort the nodes alphabetically
    def compare_function(item):
        return item.name.lower()

    main_node_list = sorted(main_node_list, key=compare_function)
    return main_node_list


def list_character_positions(string, character):
    """Return a list of positions of all the instances of character in a string"""
    return [i for i, char in enumerate(string) if char == character]


def index_strings_in_linelist(search_text, list_of_lines, case_sensitive=False):
    """
    Return all instances of the searched text in the list of lines
    as a list of tuples(line, match_start_position, line, match_end_position).
    Line numbers are 0-to-(len(list_of_lines)-1)
    """
    list_of_matches = []
    if case_sensitive == True:
        compiled_search_re = re.compile(re.escape(search_text))
    else:
        compiled_search_re = re.compile(re.escape(search_text), re.IGNORECASE)
    # Check for and extend the list with all matches
    for i, line in enumerate(list_of_lines):
        line_matches = [
            (i, match.start(), i, match.end())
            for match in re.finditer(compiled_search_re, line)
        ]
        list_of_matches.extend(line_matches)
    return list_of_matches


def index_strings_in_text(
    search_text,
    text,
    case_sensitive=False,
    regular_expression=False,
    text_to_bytes=False,
    whole_words=False,
):
    """
    Return all instances of the searched text in the text string
    as a list of tuples(0, match_start_position, 0, match_end_position).

    Parameters:
        - search_text:
            the text/expression to search for in the text parameter
        - text:
            the text that will be searched through
        - case_sensitive:
            case sensitivity of the performed search
        - regular_expression:
            selection of whether the search string is a regular expression or not
        - text_to_bytes:
            whether to transform the search_text and text parameters into byte objects
        - whole_words:
            match only whole words
    """
    # Check if whole words only should be matched
    if whole_words == True:
        search_text = r"\b(" + search_text + r")\b"
    # Convert text to bytes so that utf-8 characters will be parsed correctly
    if text_to_bytes == True:
        search_text = bytes(search_text, "utf-8")
        text = bytes(text, "utf-8")
    # Set the search text according to the regular expression selection
    if regular_expression == False:
        search_text = re.escape(search_text)
    # Compile expression according to case sensitivity flag
    if case_sensitive == True:
        compiled_search_re = re.compile(search_text)
    else:
        compiled_search_re = re.compile(search_text, re.IGNORECASE)
    # Create the list with all of the matches
    list_of_matches = [
        (0, match.start(), 0, match.end())
        for match in re.finditer(compiled_search_re, text)
    ]
    return list_of_matches


def check_unmatched_quotes(string):
    """
    Check if there are unmatched single/double quotes in the text and
    return the position of the last unmatched quote character
    """
    # Define locals
    found_single = False
    found_double = False
    last_quote_position = None
    # Loop through all the characters in the string
    for i, ch in enumerate(string):
        # Check for a double quote
        if ch == '"':
            if found_double == False and found_single == False:
                # Save state that the quote was found
                found_double = True
                # Save quote position
                last_quote_position = i
            elif found_double == True:
                # Reset quote state
                found_double = False
                last_quote_position = None
        # Check for a single quote
        elif ch == "'":
            if found_single == False and found_double == False:
                # Save state that the quote was found
                found_single = True
                # Save quote position
                last_quote_position = i
            elif found_single == True:
                # Reset quote state
                found_single = False
                last_quote_position = None
    # Return the last unclosed quote position
    return last_quote_position


def is_number(string):
    """Check if the string is a number (integer or float)"""
    try:
        float(string)
        return True
    except ValueError:
        if string[0].isdigit():
            return True
    return False


def replace_and_index(
    input_string,
    search_text,
    replace_text,
    case_sensitive=False,
    regular_expression=False,
):
    """
    Function that replaces the search text with replace text in a string,
    using regular expressions if specified, and returns the
    line numbers and indexes of the replacements as a list.
    """
    # First check if the replacement action is needed
    if search_text == replace_text and case_sensitive == True:
        return None, input_string
    elif search_text.lower() == replace_text.lower() and case_sensitive == False:
        return None, input_string
    # Initialize the return variables
    replaced_text = None
    # Find the search text matches that will be highlighted (pre-replacement)
    # Only when not searching with regular expressions
    if regular_expression == False:
        matches = index_strings_in_text(
            search_text,
            input_string,
            case_sensitive,
            regular_expression,
            text_to_bytes=True,
        )
    # Create a matches list according to regular expression selection
    if regular_expression == True:
        # Compile the regular expression object according to the case sensitivity
        if case_sensitive == True:
            compiled_search_re = re.compile(search_text)
        else:
            compiled_search_re = re.compile(search_text, re.IGNORECASE)
        # Replace all instances of search text with the replace text
        replaced_text = re.sub(compiled_search_re, replace_text, input_string)
        replaced_match_indexes = []
        # Split old and new texts into line lists
        split_input_text = input_string.split("\n")
        split_replaced_text = replaced_text.split("\n")
        # Loop through the old text and compare it line-by-line to the old text
        try:
            for i in range(len(split_input_text)):
                if split_input_text[i] != split_replaced_text[i]:
                    replaced_match_indexes.append(i)
        except:
            # If regular expression replaced lines,
            # then we cannot highlight the replacements
            replaced_match_indexes = []
    else:
        replaced_text = None
        if case_sensitive == True:
            # Standard string replace
            replaced_text = input_string.replace(search_text, replace_text)
        else:
            # Escape the regex special characters
            new_search_text = re.escape(search_text)
            # Replace backslashes with double backslashes, so that the
            # regular expression treats backslashes the same as standard
            # Python string replace!
            new_replace_text = replace_text.replace("\\", "\\\\")
            compiled_search_re = re.compile(new_search_text, re.IGNORECASE)
            replaced_text = re.sub(compiled_search_re, new_replace_text, input_string)
        replaced_match_indexes = []
        # Loop while storing the new indexes
        diff = 0
        bl_search = bytes(search_text, "utf-8")
        bl_search = len(bl_search.replace(b"\\", b" "))
        bl_replace = bytes(replace_text, "utf-8")
        bl_replace = len(bl_replace.replace(b"\\", b" "))
        for i, match in enumerate(matches):
            # Subtract the length of the search text from the match index,
            # to offset the shortening of the whole text when the lenght
            # of the replace text is shorter than the search text
            diff = (bl_replace - bl_search) * i
            new_index = match[1] + diff
            # Check if the index correction went into a negative index
            if new_index < 0:
                new_index = 0
            # The line is always 0, because Scintilla also allows
            # indexing over multiple lines! If the index number goes
            # over the length of a line, it "overflows" into the next line.
            # Basically this means that you can access any line/index by
            # treating the whole text not as a list of lines, but as an array.
            replaced_match_indexes.append((0, new_index, 0, new_index + bl_replace))
    # Return the match list and the replaced text
    return replaced_match_indexes, replaced_text


def regex_replace_text(
    input_string,
    search_text,
    replace_text,
    case_sensitive=False,
    regular_expression=False,
):
    """Function that uses the re module to replace text in a string"""
    replaced_text = None
    if regular_expression == True:
        if case_sensitive == True:
            compiled_search_re = re.compile(search_text)
        else:
            compiled_search_re = re.compile(search_text, re.IGNORECASE)
        replaced_text = re.sub(compiled_search_re, replace_text, input_string)
    else:
        if case_sensitive == True:
            replaced_text = input_string.replace(search_text, replace_text)
        else:
            #'re.escape' replaces the re module special characters with literals,
            # so that the search_text is treated as a string literal
            compiled_re = re.compile(re.escape(search_text), re.IGNORECASE)
            replaced_text = re.sub(compiled_re, replace_text, input_string)
    return replaced_text


def is_config_file(file_with_path):
    file_with_path = file_with_path.replace("\\", "/")
    if os.path.isfile(file_with_path) == False:
        return False
    file = os.path.basename(file_with_path)
    path = os.path.dirname(file_with_path)
    data.config_file = data.config_file.replace("\\", "/")
    data.application_directory = data.application_directory.replace("\\", "/")
    if file == data.config_file and path == data.application_directory:
        return True
    else:
        return False


def create_default_config_file():
    user_definitions_file = os.path.join(data.application_directory, data.config_file)
    with open(user_definitions_file, "w") as f:
        f.write(constants.default_config_file_content)
        f.close()


def get_line_indentation(line):
    """Function for determining the indentation level of a line string"""
    indentation = 0
    for char in line:
        if char == " ":
            indentation += 1
        else:
            break
    return indentation


"""
Unixifying functions
"""


def unixify_path(path):
    return os.path.realpath(path).replace("\\", "/")


def unixify_join(*paths) -> str:
    return unixify_path(os.path.join(*paths))


def unixify_remove(whole_path, path_to_remove) -> str:
    return unixify_path(os.path.relpath(whole_path, path_to_remove))


def change_icon_opacity(qicon, opacity):
    pixmap = qicon.pixmap(qicon.actualSize(create_size(256, 256)))
    pixmap = change_opacity(pixmap, opacity)
    return qt.QIcon(pixmap)


def change_opacity(pixmap_or_file, opacity):
    """
    Changes the opacity of a pixmap or image from a file
    """
    base_image = qt.QImage(pixmap_or_file)
    image = qt.QImage(base_image.size(), qt.QImage.Format.Format_ARGB32_Premultiplied)
    image.fill(qt.Qt.GlobalColor.transparent)
    painter = qt.QPainter(image)
    painter.setRenderHints(
        qt.QPainter.RenderHint.Antialiasing
        | qt.QPainter.RenderHint.TextAntialiasing
        | qt.QPainter.RenderHint.SmoothPixmapTransform
    )
    painter.setOpacity(opacity)
    painter.drawImage(create_rect(0, 0, image.width(), image.height()), base_image)
    painter.end()
    pixmap = qt.QPixmap.fromImage(image)
    return pixmap


def get_index(start):
    counter = start
    while True:
        yield counter
        counter += 1


def process_events(cycles: int = 1, delay: float = None) -> None:
    for i in range(cycles):
        qt.QCoreApplication.processEvents()
    if delay is not None:
        time.sleep(delay)


"""
Constructor helper functions
"""


def create_rect(*args):
    if len(args) == 4:
        x, y, width, height = args
        return qt.QRect(int(x), int(y), int(width), int(height))
    elif len(args) == 2:
        point, size = args
        return qt.QRect(point, size)
    else:
        raise Exception("[functions.create_rect] Unknown arguments: {}".format(args))


def create_point(*args):
    if len(args) == 2:
        x, y = args
        return qt.QPoint(int(x), int(y))
    elif len(args) == 0:
        return qt.QPoint()
    else:
        raise Exception("[functions.create_point] Unknown arguments: {}".format(args))


def create_size(*args):
    if len(args) == 2:
        width, height = args
        return qt.QSize(int(width), int(height))
    else:
        raise Exception("[functions.create_point] Unknown arguments: {}".format(args))


PERFORMANCE_MEASURING_FLAG = True


def performance_timer_start():
    if not PERFORMANCE_MEASURING_FLAG:
        return
    global performance_timer_starting_count
    global performance_timer_last_point
    performance_timer_starting_count = time.perf_counter()
    performance_timer_last_point = performance_timer_starting_count


def performance_timer_show(text=None):
    if not PERFORMANCE_MEASURING_FLAG:
        return
    global performance_timer_last_point
    try:
        info_text = "PERFORMANCE-TIMER"
        if text:
            info_text = text
        current_point = time.perf_counter()
        end_count = current_point - performance_timer_starting_count
        diff_count = current_point - performance_timer_last_point
        performance_timer_last_point = current_point
        print(
            "Time: {:.4f}s / diff: {:.4f} -> [{}]".format(
                end_count, diff_count, info_text
            )
        )
    except:
        print("[{}] Error!".format(info_text))


def open_url(url):
    webbrowser.open_new_tab(url)


def open_item_in_explorer(path):
    """
    Return False if the given file or folder cannot be opened in the system's
    file explorer (eg. it doesn't exist).

    """
    if os.path.isfile(path) or os.path.isdir(path):
        path = path.replace("/", os.sep)
        try:
            if data.platform.lower() == "windows":
                subprocess.Popen(
                    'explorer /select,"{}"'.format(path),
                    shell=False,
                )
            else:
                if os.path.isfile(path):
                    subprocess.Popen(["xdg-open", os.path.dirname(path)])
                else:
                    subprocess.Popen(["xdg-open", path])
        except:
            return False
        # No error
        return True
    return False


def get_edges_to_widget(widget, widget_window, size, offset=(0, 0)):
    rect = widget.geometry()
    window_position = widget_window.mapToGlobal(rect.topLeft())
    widget_position = widget.mapToGlobal(rect.topLeft())
    position = widget_position - window_position
    # Center the rectangle to the widget
    center = (
        position.x() + ((rect.width() - size[0]) / 2) + offset[0],
        position.y() + ((rect.height() - size[1]) / 2) + offset[1],
    )
    left = (center[0] - (rect.width() / 2) + (size[0] / 2), center[1])
    right = (center[0] + (rect.width() / 2) - (size[0] / 2), center[1])
    top = (center[0], center[1] - (rect.height() / 2) + (size[1] / 2))
    bottom = (center[0], center[1] + (rect.height() / 2) - (size[1] / 2))
    return (center, left, right, top, bottom)


def get_screen_size():
    size = data.application.primaryScreen().size()
    return size.width(), size.height()


def center_to_current_screen(widget):
    screens = data.application.screens()
    if widget.windowHandle() is None:
        return
    for i, s in enumerate(screens):
        if s is widget.windowHandle().screen():
            geometry = s.geometry()
            left = geometry.left()
            top = geometry.top()
            offset_width = (geometry.width() / 2) - (widget.width() / 2)
            offset_height = (geometry.height() / 2) - (widget.height() / 2)
            center = qt.QPoint(int(left + offset_width), int(top + offset_height))

            def move(*args):
                widget.move(center - qt.QPoint(0, 50))  # Manual offset

            qt.QTimer.singleShot(0, move)


"""
Docking system helpers
"""


def right_replace(
    text: str, old_substring: str, new_substring: str, max_occurrences: int
) -> str:
    """
    Replaces the rightmost occurrences of a substring in a given text.
    """
    parts = text.rsplit(old_substring, max_occurrences)
    return new_substring.join(parts)


def remove_last_box(name):
    split = name.split(".")
    return ".".join(split[:-1])


def remove_tabs_from_name(name):
    return name[: name.index(".Tabs")]


def remove_tab_number_from_name(name):
    tabs_string = ".Tabs"
    return name[: (name.index(tabs_string) + len(tabs_string))]


"""
Output redirect
"""
OUTPUT_FILENAME = "output.txt"


def output_get_backup_directory() -> str:
    # Output backup directory check
    output_backup_directory: str = unixify_join(data.settings_directory, "output")
    if not os.path.isdir(output_backup_directory):
        os.makedirs(output_backup_directory)
    return output_backup_directory


def output_get_file() -> str:
    return unixify_join(
        output_get_backup_directory(),
        OUTPUT_FILENAME,
    )


def output_get_file_with_timestamp() -> str:
    sf = os.path.splitext(OUTPUT_FILENAME)
    return os.path.join(
        output_get_backup_directory(),
        OUTPUT_FILENAME.replace(
            sf[1], get_default_datetime_formatted_string() + ".txt"
        ),
    )


def get_default_datetime_formatted_string() -> str:
    return datetime.datetime.now().strftime(".%Y%m%d_%H%M%S")


def output_redirect() -> None:
    # Store original values
    global original_output_stream
    original_output_stream = sys.stdout
    global original_error_stream
    original_error_stream = sys.stderr
    global original_except_hook
    original_except_hook = sys.excepthook

    # Output file
    output_file: str = output_get_file()

    # Open file and redirect output
    f: TextIOWrapper = open(
        output_file, "w+", encoding="utf-8", newline="\n", errors="replace"
    )
    sys.stdout = f
    sys.stderr = f

    # Adapt exception hook for all threads
    def exception_hook(
        exctype: type, value: BaseException, trace: TracebackType
    ) -> None:
        print("-" * 80)
        print(
            "".join(traceback.format_exception(exctype, value, trace)),
            end="",
        )
        print("-" * 80)
        qt.QApplication.quit()
        # Close file properly
        if hasattr(sys.stdout, "close"):
            sys.stdout.close()
        # Restore original streams before backup
        sys.stdout = original_output_stream
        sys.stderr = original_error_stream
        # Create backup with timestamp
        output_file_with_date: str = output_get_file_with_timestamp()
        shutil.copy(output_file, output_file_with_date)

    sys.excepthook = exception_hook
    init_original: Callable = threading.Thread.__init__

    def init(self: threading.Thread, *args: Any, **kwargs: Any) -> None:
        init_original(self, *args, **kwargs)
        run_original: Callable = self.run

        def run_with_except_hook(*args2: Any, **kwargs2: Any) -> None:
            try:
                run_original(*args2, **kwargs2)
            except Exception:
                sys.excepthook(*sys.exc_info())

        self.run = run_with_except_hook

    threading.Thread.__init__ = init  # type: ignore


def output_backup() -> None:
    # Output file
    output_file: str = output_get_file()
    # Create backup with timestamp
    output_file_with_date: str = output_get_file_with_timestamp()

    # Check if the file exists and has content before copying
    try:
        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            shutil.copy(output_file, output_file_with_date)
    except (OSError, IOError):
        # Handle potential file access errors silently
        traceback.print_exc()


def reorganize_imports(import_code: str) -> str:
    # Split the code into individual lines
    lines = import_code.strip().split("\n")

    # Initialize lists to separate 'import' and 'from ... import' lines
    import_lines = []
    from_import_lines = []

    for line in lines:
        line = line.strip()

        # Process 'import x, y, z' lines
        if line.startswith("import"):
            imports = line.replace("import", "").split(",")
            for imp in imports:
                import_lines.append(f"import {imp.strip()}")

        # Keep 'from x import y' lines intact
        elif line.startswith("from"):
            from_import_lines.append(line)

    # Sort import statements: first by length, then alphabetically
    import_lines.sort(key=lambda x: (len(x), x))

    # Combine import statements followed by from ... import statements
    return "\n".join(import_lines + from_import_lines)


def get_module_attributes(code: str) -> List[str]:
    """
    Analyze Python code and return a list of all module-level attributes.

    Args:
        code (str): Python source code as a string

    Returns:
        List[str]: List of attribute names found at module level
    """
    try:
        tree = ast.parse(code)
        attributes = []

        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                # Function definitions
                attributes.append(node.name)
            elif isinstance(node, ast.AsyncFunctionDef):
                # Async function definitions
                attributes.append(node.name)
            elif isinstance(node, ast.ClassDef):
                # Class definitions
                attributes.append(node.name)
            elif isinstance(node, ast.Assign):
                # Variable assignments
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        attributes.append(target.id)
            elif isinstance(node, ast.AnnAssign):
                # Annotated assignments (e.g., x: int = 5)
                if isinstance(node.target, ast.Name):
                    attributes.append(node.target.id)
            elif isinstance(node, ast.Import):
                # Import statements (e.g., import os)
                for alias in node.names:
                    attributes.append(alias.asname or alias.name)
            elif isinstance(node, ast.ImportFrom):
                # From imports (e.g., from os import path)
                for alias in node.names:
                    attributes.append(alias.asname or alias.name)
            elif isinstance(node, ast.AugAssign):
                # Augmented assignments (e.g., x += 1)
                if isinstance(node.target, ast.Name):
                    attributes.append(node.target.id)

        return sorted(list(set(attributes)))  # Remove duplicates and sort

    except SyntaxError as e:
        raise ValueError(f"Invalid Python code: {e}")


def get_used_symbols(code: str) -> Set[str]:
    """
    Extract all names used in the code (variables, functions, classes, etc.).

    Args:
        code (str): Python source code as a string

    Returns:
        Set[str]: Set of all symbol names used in the code
    """
    try:
        tree = ast.parse(code)
        used_symbols = set()

        class NameVisitor(ast.NodeVisitor):
            def visit_Name(self, node):
                if isinstance(
                    node.ctx, ast.Load
                ):  # Only count when reading/using the name
                    used_symbols.add(node.id)
                self.generic_visit(node)

            def visit_Attribute(self, node):
                # Handle attribute access like module.function, object.method
                if isinstance(node.value, ast.Name):
                    used_symbols.add(node.value.id)
                self.generic_visit(node)

            def visit_Import(self, node):
                for alias in node.names:
                    used_symbols.add(alias.asname or alias.name)
                self.generic_visit(node)

            def visit_ImportFrom(self, node):
                for alias in node.names:
                    used_symbols.add(alias.asname or alias.name)
                self.generic_visit(node)

        visitor = NameVisitor()
        visitor.visit(tree)
        return used_symbols

    except SyntaxError as e:
        raise ValueError(f"Invalid Python code: {e}")


def analyze_symbol_usage(source_file: str, target_file: str) -> Dict[str, List[str]]:
    """
    Analyze which symbols from source_file are used in target_file.

    Args:
        source_file (str): Path to the module providing symbols
        target_file (str): Path to the module using symbols

    Returns:
        Dict[str, List[str]]: Dictionary with analysis results:
            - 'defined_in_source': List of symbols defined in source file
            - 'used_in_target': List of symbols used in target file
            - 'used_from_source': List of symbols from source that are used in target
            - 'unused_from_source': List of symbols from source that are NOT used in target
    """

    # Read and analyze both files
    with open(source_file, "r", encoding="utf-8") as f:
        source_code = f.read()

    with open(target_file, "r", encoding="utf-8") as f:
        target_code = f.read()

    # Get symbols defined in source file
    source_symbols = set(get_module_attributes(source_code))

    # Get all symbols used in target file
    target_used_symbols = get_used_symbols(target_code)

    # Find intersection - symbols from source that are used in target
    used_from_source = source_symbols.intersection(target_used_symbols)

    # Find symbols from source that are NOT used in target
    unused_from_source = source_symbols - target_used_symbols

    return {
        "defined_in_source": sorted(list(source_symbols)),
        "used_in_target": sorted(list(target_used_symbols)),
        "used_from_source": sorted(list(used_from_source)),
        "unused_from_source": sorted(list(unused_from_source)),
        "source_file": os.path.basename(source_file),
        "target_file": os.path.basename(target_file),
    }


def print_symbol_analysis(results: Dict[str, List[str]]):
    """
    Pretty print the symbol usage analysis results.
    """
    print(f"Symbol Usage Analysis:")
    print(f"Source: {results['source_file']} → Target: {results['target_file']}")
    print("=" * 50)

    print(f"\n📁 Defined in source ({len(results['defined_in_source'])}):")
    for symbol in results["defined_in_source"]:
        print(f"   {symbol}")

    print(f"\n🔍 Used from source in target ({len(results['used_from_source'])}):")
    for symbol in results["used_from_source"]:
        print(f"   ✅ {symbol}")

    print(f"\n🚫 Not used from source ({len(results['unused_from_source'])}):")
    for symbol in results["unused_from_source"]:
        print(f"   ❌ {symbol}")

    usage_ratio = (
        len(results["used_from_source"]) / len(results["defined_in_source"])
        if results["defined_in_source"]
        else 0
    )
    print(
        f"\n📊 Usage ratio: {usage_ratio:.1%} ({len(results['used_from_source'])}/{len(results['defined_in_source'])})"
    )


def get_module_attributes_detailed(code: str) -> Dict[str, List[str]]:
    """
    Analyze Python code and return detailed information about module-level attributes.

    Args:
        code (str): Python source code as a string

    Returns:
        Dict[str, List[str]]: Dictionary with attribute types as keys and names as values
    """
    try:
        tree = ast.parse(code)
        result = {
            "functions": [],
            "async_functions": [],
            "classes": [],
            "variables": [],
            "imports": [],
            "constants": [],  # UPPER_CASE variables
        }

        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                result["functions"].append(node.name)
            elif isinstance(node, ast.AsyncFunctionDef):
                result["async_functions"].append(node.name)
            elif isinstance(node, ast.ClassDef):
                result["classes"].append(node.name)
            elif isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
                # Handle different types of assignments
                if isinstance(node, ast.Assign):
                    targets = node.targets
                elif isinstance(node, ast.AnnAssign):
                    targets = [node.target]
                else:  # AugAssign
                    targets = [node.target]

                for target in targets:
                    if isinstance(target, ast.Name):
                        name = target.id
                        result["variables"].append(name)
                        # Check if it looks like a constant (UPPER_CASE)
                        if name.isupper():
                            result["constants"].append(name)
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                for alias in node.names:
                    import_name = alias.asname or alias.name
                    result["imports"].append(import_name)

        # Remove duplicates from each category
        for key in result:
            result[key] = sorted(list(set(result[key])))

        return result

    except SyntaxError as e:
        raise ValueError(f"Invalid Python code: {e}")


def analyze_symbol_usage_detailed(source_file: str, target_file: str) -> Dict[str, any]:
    """
    Enhanced analysis with more detailed information about symbol usage.
    """
    results = analyze_symbol_usage(source_file, target_file)

    # Read target file for context
    with open(target_file, "r", encoding="utf-8") as f:
        target_code = f.read()

    # Find where each used symbol appears in target file
    symbol_locations = {}
    for symbol in results["used_from_source"]:
        lines = []
        for i, line in enumerate(target_code.splitlines(), 1):
            if symbol in line and not line.strip().startswith("#"):
                lines.append((i, line.strip()))
        symbol_locations[symbol] = lines

    results["symbol_locations"] = symbol_locations
    return results


def print_detailed_analysis(results: Dict[str, any], print_func: callable):
    """
    Print detailed analysis with line numbers.
    """
    print_symbol_analysis(results)

    print_func(f"\n📍 Usage locations in target file:")
    for symbol, locations in results["symbol_locations"].items():
        if locations:
            print_func(f"\n   {symbol}:")
            for line_num, line_content in locations[:3]:  # Show first 3 occurrences
                print_func(f"      Line {line_num}: {line_content}")
            if len(locations) > 3:
                print_func(f"      ... and {len(locations) - 3} more occurrences")
