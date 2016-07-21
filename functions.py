
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
##      Module that holds functions for various uses


import os
import os.path
import locale
import re
import ast
import codecs
import itertools
import operator
import data

def get_file_size_Mb(file_with_path):
    """Get the file size in Mb"""
    size_bytes = os.path.getsize(file_with_path)
    #Convert size into megabytes
    size_Mb = size_bytes / (1024 * 1024)
    #return the size in megabyte
    return size_Mb

def find_files_with_text(search_text, 
                         search_dir, 
                         case_sensitive=False, 
                         search_subdirs=True, 
                         break_on_find=False):
    """
    Search for the specified text in files in the specified directory and return a file list.
    """
    #Check if the directory is valid
    if os.path.isdir(search_dir) == False:
        return None
    #Create an empty file list
    text_file_list = []
    #Check if subdirectories should be included
    if search_subdirs == True:
        walk_tree = os.walk(search_dir)
    else:
        #Only use the first generator value(only the top directory)
        walk_tree = [next(os.walk(search_dir))]
    #"walk" through the directory tree and save the readable files to a list
    for root, subFolders, files in walk_tree:
        for file in files:
            #Merge the path and filename
            full_with_path = os.path.join(root, file)
            if test_text_file(full_with_path) != None:
                #On windows, the function "os.path.join(root, file)" line gives a combination of "/" and "\\", 
                #which looks weird but works. The replace was added to have things consistent in the return file list.
                full_with_path = full_with_path.replace("\\",  "/")
                text_file_list.append(full_with_path)
    #Search for the text in found files
    return_file_list = []
    for file in text_file_list:
        try:
            file_text = read_file_to_string(file)
            #Set the comparison according to case sensitivity
            if case_sensitive == False:
                compare_file_text = file_text.lower()
                compare_search_text = search_text.lower()
            else:
                compare_file_text = file_text
                compare_search_text = search_text
            #Check if file contains the search string
            if compare_search_text in compare_file_text:
                return_file_list.append(file)
                #Check if break option on first find is true
                if break_on_find == True:
                    break
        except:
            continue
    #Return the generated list
    return return_file_list

def find_files_with_text_enum(search_text, 
                              search_dir, 
                              case_sensitive=False, 
                              search_subdirs=True, 
                              break_on_find=False):
    """
    Search for the specified text in files in the specified directory and return a file list and
    lines where the text was found at.
    """
    #Check if the directory is valid
    if os.path.isdir(search_dir) == False:
        return None
    #Create an empty file list
    text_file_list = []
    #Check if subdirectories should be included
    if search_subdirs == True:
        walk_tree = os.walk(search_dir)
    else:
        #Only use the first generator value(only the top directory)
        walk_tree = [next(os.walk(search_dir))]
    #"walk" through the directory tree and save the readable files to a list
    for root, subFolders, files in walk_tree:
        for file in files:
            #Merge the path and filename
            full_with_path = os.path.join(root, file)
            if test_text_file(full_with_path) != None:
                #On windows, the function "os.path.join(root, file)" line gives a combination of "/" and "\\", 
                #which looks weird but works. The replace was added to have things consistent in the return file list.
                full_with_path = full_with_path.replace("\\",  "/")
                text_file_list.append(full_with_path)
    #Search for the text in found files
    return_file_dict = {}
    for file in text_file_list:
        try:
            file_lines = read_file_to_list(file)
            #Set the comparison according to case sensitivity
            if case_sensitive == False:
                compare_search_text = search_text.lower()
            else:
                compare_search_text = search_text
            #Check the file line by line
            for i, line in enumerate(file_lines):
                if case_sensitive == False:
                    line = line.lower()
                if compare_search_text in line:
                    if file in return_file_dict:
                        return_file_dict[file].append(i)
                    else:
                        return_file_dict[file] = [i]
                    #Check if break option on first find is true
                    if break_on_find == True:
                        break
        except:
            continue
    #Return the generated list
    return return_file_dict

def replace_text_in_files(search_text, 
                          replace_text, 
                          search_dir, 
                          case_sensitive=False, 
                          search_subdirs=True):
    """
    Search for the specified text in files in the specified directory and replace all instances
    of the search_text with replace_text and save the changes back to the file.
    """
    #Get the files with the search string in them
    found_files = find_files_with_text(
                      search_text, 
                      search_dir, 
                      case_sensitive, 
                      search_subdirs 
                  )
    if found_files == None:
        return []
    #Loop through the found list and replace the text
    for file in found_files:
        #Read the file
        file_text = read_file_to_string(file)
        #Compile the regex expression according to case sensitivity
        if case_sensitive == True:
            compiled_search_re = re.compile(search_text)
        else:
            compiled_search_re = re.compile(search_text, re.IGNORECASE)
        #Replace all instances of search text with the replace text
        replaced_text = re.sub(compiled_search_re, replace_text, file_text)
        #Write the replaced text back to the file
        write_to_file(replaced_text, file)
    #Return the found files list
    return found_files
    
def replace_text_in_files_enum(search_text, 
                               replace_text, 
                               search_dir, 
                               case_sensitive=False, 
                               search_subdirs=True):
    """
    The second version of replace_text_in_files, that goes line-by-line 
    and replaces found instances and stores the line numbers,
    at which the replacements were made
    """
    #Get the files with the search string in them
    found_files = find_files_with_text(
                      search_text, 
                      search_dir, 
                      case_sensitive, 
                      search_subdirs 
                  )
    if found_files == None:
        return {}
    #Compile the regex expression according to case sensitivity
    if case_sensitive == True:
        compiled_search_re = re.compile(search_text)
    else:
        compiled_search_re = re.compile(search_text, re.IGNORECASE)
    #Loop through the found list and replace the text
    return_files = {}
    for file in found_files:
        #Read the file
        file_text_list = read_file_to_list(file)
        #Cycle through the lines, replacing text and storing the line numbers of replacements
        for i in range(len(file_text_list)):
            if case_sensitive == True:
                line = file_text_list[i]
            else:
                search_text = search_text.lower()
                line = file_text_list[i].lower()
            if search_text in line:
                if file in return_files:
                    return_files[file].append(i)
                else:
                    return_files[file] = [i]
                file_text_list[i] = re.sub(compiled_search_re, replace_text, file_text_list[i])
        #Write the replaced text back to the file
        replaced_text = "\n".join(file_text_list)
        write_to_file(replaced_text, file)
    #Return the found files list
    return return_files
    

def find_files_by_name(search_filename, 
                       search_dir, 
                       case_sensitive=False, 
                       search_subdirs=True):
    """
    Find file with search_filename string in its name in the specified directory.
    """
    #Check if the directory is valid
    if os.path.isdir(search_dir) == False:
        return None
    #Create an empty file list
    found_file_list = []
    #Check if subdirectories should be included
    if search_subdirs == True:
        walk_tree = os.walk(search_dir)
    else:
        #Only use the first generator value(only the top directory)
        walk_tree = [next(os.walk(search_dir))]
    for root, subFolders, files in walk_tree:
        for file in files:
            #Merge the path and filename
            full_with_path = os.path.join(root, file)
            #Set the comparison according to case sensitivity
            if case_sensitive == False:
                compare_actual_filename = file.lower()
                compare_search_filename = search_filename.lower()
            else:
                compare_actual_filename = file
                compare_search_filename = search_filename
            #Test if the name of the file contains the search string
            if compare_search_filename in compare_actual_filename:
                #On windows, the function "os.path.join(root, file)" line gives a combination of "/" and "\\", 
                #which looks weird but works. The replace was added to have things consistent in the return file list.
                full_with_path = full_with_path.replace("\\",  "/")
                found_file_list.append(full_with_path)
    #Return the generated list
    return found_file_list

def get_nim_node_tree(nim_code):
    """
    Parse the text and return a node tree as a list. 
    The text must be valid Nim/Nimrod code.
    """
    class NimNode():
        def __init__(self):
            #Attributes
            self.name           = None
            self.description    = None
            self.type           = None
            self.parameters     = None
            self.return_type    = None
            self.line           = None
            #Child node lists
            self.imports    = []
            self.types      = []
            self.consts     = []
            self.lets       = []
            self.vars       = []
            self.procedures = []
            self.forward_declarations = []
            self.converters = []
            self.iterators  = []
            self.methods    = []
            self.properties = []
            self.templates  = []
            self.macros     = []
            self.objects    = []
            self.namespaces = []
    #Nested function for determining the next blocks indentation level
    def get_next_blocks_indentation(current_step, lines):
        for ln in range(current_step, len(lines)):
            if lines[ln].strip() != "" and lines[ln].strip().startswith("#") == False:
                return get_line_indentation(lines[ln])
        else:
            return 250
    #Nested function for finding the closing parenthesis of parameter definitions
    def get_closing_parenthesis(current_step, lines):
        for ln in range(current_step, len(lines)):
            if ")" in lines[ln] and (lines[ln].count(")") == (lines[ln].count("(") + 1)):
                return ln
        else:
            return None
    #Nested function for creating a procedure, method, macro or template node
    def create_node(node, 
                    search_string,  
                    current_line, 
                    current_line_number, 
                    line_list, 
                    previous_offset=0):
        #Reset the procedure's starting line adjustment variable
        body_starting_line_number = None
        #Reset the local skip line variable
        local_skip_to_line = None
        #Parse procedure name according to the line characters
        if "(" in current_line:
            #The procedure has parameters
            base_search_string = r"{:s}\s+(.*?)\(|{:s}\s+(.*?)\:|{:s}\s+(.*?)\=".format(
                                                                                search_string, 
                                                                                search_string, 
                                                                                search_string
                                                                            )
            proc_name_search_pattern =  re.compile(
                                            base_search_string, 
                                            re.IGNORECASE
                                        )
            name_match_object       = re.search(proc_name_search_pattern, current_line)
            for i in range(1, 4):
                node.name = name_match_object.group(i)
                if node.name != "" and node.name != None:
                    break
            #Skip lines if the parameters stretch over multiple lines
            if not(")" in current_line):
                body_starting_line_number  =    get_closing_parenthesis(
                                                    current_line_number+1, 
                                                    line_list
                                                )
                current_line = line_list[body_starting_line_number]
            #Parse the procedure parameters and return type
            if search_string == "proc":
                return_type = None
                parameters  = None
                #Check if the parameters are declared over multiple lines
                if body_starting_line_number != None:
                    parameter_string = ""
                    open_index = line_list[current_line_number].find("(") + 1
                    parameter_string += line_list[current_line_number][open_index:]
                    for i in range(current_line_number+1, body_starting_line_number+1):
                        if ")" in line_list[i] and (line_list[i].count(")") == (line_list[i].count("(") + 1)):
                            close_index = line_list[i].find(")")
                            current_parameter = line_list[i][:close_index].strip()
                            #Filter out the parameter initialization
                            if "=" in current_parameter:
                                current_parameter = current_parameter[:current_parameter.find("=")]
                            parameter_string += current_parameter
                        else:
                            current_parameter = line_list[i].strip()
                            #Filter out the parameter initialization
                            if "=" in current_parameter:
                                current_parameter = current_parameter[:current_parameter.find("=")]
                            parameter_string += current_parameter
                    parameters = [par.strip() for par in parameter_string.split(",") if par.strip() != ""]
                    #Check the return type
                    split_line = line_list[body_starting_line_number][close_index:].split(":")
                    if len(split_line) > 1:
                        return_type = split_line[1].replace("=", "")
                        return_type = return_type.strip()
                else:
                    open_index  = line_list[current_line_number].find("(") + 1
                    close_index = line_list[current_line_number].find(")")
                    parameter_string = line_list[current_line_number][open_index:close_index]
                    parameters = [par for par in parameter_string.split(",") if par.strip() != ""]
                    #Check the return type
                    split_line = line_list[current_line_number][close_index:].split(":")
                    if len(split_line) > 1:
                        return_type = split_line[1].replace("=", "")
                        return_type = return_type.strip()
                node.parameters     = parameters
                node.return_type    = return_type
        elif ":" in current_line:
            #The procedure/macro/... has no parameters, but has a return type
            node.name = current_line.replace(search_string, "", 1).split(":")[0].strip()
            #Special parsing for classes
            if (search_string == "heap_object" or 
                search_string == "stack_object" or
                search_string == "property"):
                node.name = node.name.split()[0]
        else:
            #The procedure/macro/... has no parameters and no return type
            node.name = current_line.replace(search_string, "", 1).split()[0].strip()
        
        #Parse node
        if "=" in current_line and current_line.strip().endswith("="):
            #Check if the declaration is a one-liner
            if ((current_line.strip().endswith("=") == False) and
                ((len(current_line.split("=")) == 2 and 
                    current_line.split("=")[1].strip() != "") or
                 (len(current_line.split("=")) > 2 and 
                    current_line[current_line.rfind(")"):].split("=")[1] != ""))):
                #One-liner
                pass
            else:
                #Adjust the procedure body starting line as needed
                starting_line_number = current_line_number + 1
                if body_starting_line_number != None:
                    starting_line_number = body_starting_line_number + 1
                #Parse the procedure for its local child nodes
                sub_node_lines = []
                compare_indentation = get_next_blocks_indentation(starting_line_number, line_list)
                for ln in range(starting_line_number, len(line_list)):
                    #Skip empty lines
                    if line_list[ln].strip() == "" or line_list[ln].strip().startswith("#") == True:
                        #Add the blank space at the correct indentation level
                        #to have the correct number of lines in the list
                        sub_node_lines.append(" " * compare_indentation)
                        continue
                    elif get_line_indentation(line_list[ln]) < compare_indentation:
                        #Store the end of the procedure declaration
                        local_skip_to_line = ln
                        #Reached the last line of the procedure declaration
                        break
                    else:
                        sub_node_lines.append(line_list[ln])
                else:
                    #For loop looped through all of the lines, skip them
                    local_skip_to_line = len(line_list) - 1
                starting_line_number += previous_offset
                node = parse_node(node, sub_node_lines, line_offset=starting_line_number)
        elif (search_string == "heap_object" or 
              search_string == "stack_object" or
              search_string == "namespace" or
              search_string == "property"):
            """special macro identifiers: class, namespace, ..."""
            #Adjust the procedure body starting line as needed
            starting_line_number = current_line_number + 1
            if body_starting_line_number != None:
                starting_line_number = body_starting_line_number + 1
            #Parse the procedure for its local child nodes
            sub_node_lines = []
            compare_indentation = get_next_blocks_indentation(starting_line_number, line_list)
            for ln in range(starting_line_number, len(line_list)):
                #Skip empty lines
                if line_list[ln].strip() == "" or line_list[ln].strip().startswith("#") == True:
                    #Add the blank space at the correct indentation level
                    #to have the correct number of lines in the list
                    sub_node_lines.append(" " * compare_indentation)
                    continue
                elif get_line_indentation(line_list[ln]) < compare_indentation:
                    #Store the end of the procedure declaration
                    local_skip_to_line = ln
                    #Reached the last line of the procedure declaration
                    break
                else:
                    sub_node_lines.append(line_list[ln])
            else:
                #For loop looped through all of the lines, skip them
                local_skip_to_line = len(line_list) - 1
            starting_line_number += previous_offset
            node = parse_node(node, sub_node_lines, line_offset=starting_line_number)
        else:
            """The procedure is a forward declaracion"""
            node.type = "forward declaration"
        #Return the relevant data
        return node, local_skip_to_line
                    
    #Split the Nim code into lines
    nim_code_lines = nim_code.split("\n")
    #Create and initialize the main node that will hold all other nodes
    main_node = NimNode()
    main_node.name          = "main"
    main_node.description   = "main node"
    def parse_node(input_node, code_lines, line_offset=0):
        #Initialize the starting indentation levels (number of spaces)
        current_indentation     = 0
        compare_indentation     = 0
        #Initialize the various state flags
        import_statement    = False
        type_statement      = False
        const_statement     = False
        let_statement       = False
        var_statement       = False
        proc_statement      = False
        converter_statement = False
        iterator_statement  = False
        method_statement    = False
        macro_statement     = False
        template_statement  = False
        class_statement     = False
        namespace_statement = False
        property_statement  = False
        #Initialize the flag for skipping multiple lines
        skip_to_line = None
        #Main loop
        for line_count, line in enumerate(code_lines):
            #Skip blank lines
            if line.strip() == "" or line.strip().startswith("#"):
                continue
            #Check if line needs to be skipped
            if skip_to_line != None:
                if line_count >= skip_to_line:
                    skip_to_line = None
                else:
                    continue
            #Get line indentation and strip leading/trailing whitespaces
            current_indentation = get_line_indentation(line)
            line = line.strip()
            #Discard the comment part of a line, if it's in the line
            if "#" in line:
                stringing           = False
                string_character    = None
                for ch_count, ch in enumerate(line):
                    if ch == "\"" or ch == "\'":
                        #Catch the string building characters
                        if stringing == False:
                            stringing           = True
                            string_character    = ch
                        elif ch == string_character:
                            stringing           = False
                            string_character    = None
                    elif ch == "#" and stringing == False:
                        #Discrad the part of the line from the 
                        #comment character to the end of the line
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
                            import_node.line        = line_count + line_offset
                            input_node.imports.append(import_node)
                elif current_indentation < compare_indentation:
                    import_statement = False
            elif type_statement == True:
                if current_indentation == compare_indentation:
                    type_node = NimNode()
                    type_node.name = line.split("=")[0].strip()
                    type_node.description   = "type"
                    type_node.line          = line_count + line_offset
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
                        const_node.description  = "const"
                        const_node.line         = line_count + line_offset
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
                        let_node.description  = "let"
                        let_node.line         = line_count + line_offset
                        input_node.lets.append(let_node)
                elif current_indentation < compare_indentation:
                    let_statement = False
            elif var_statement == True:
                if current_indentation == compare_indentation:
                    if ":" in line and "=" in line and (line.find(":") < line.find("=")):
                        type = line.split(":")[1].split("=")[0].strip()
                        line = line.split(":")[0].strip()
                    elif ":" in line and not("=" in line):
                        type = line.split(":")[1].strip()
                        line = line.split(":")[0].strip()
                    elif "=" in line:
                        type = line.split("=")[1][:line.find("(")].strip()
                        line = line.split("=")[0].strip()
                    for var in line.split(","):
                        var_name = var.strip()
                        if var_name != "" and var_name[0].isalpha():
                            var_node = NimNode()
                            var_node.name           = var.strip()
                            var_node.description    = "var"
                            var_node.type           = type
                            var_node.line           = line_count + line_offset
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
            
            #Testing for base level declarations
            if line.startswith("import ") or line == "import":
                if line == "import":
                    import_statement    = True
                    compare_indentation = get_next_blocks_indentation(line_count+1, code_lines)
                else:
                    line = line.replace("import", "")
                    for module in line.split(","):
                        module_name = module.strip()
                        if module_name != "":
                            import_node = NimNode()
                            import_node.name        = module_name
                            import_node.description = "import"
                            import_node.line        = line_count + line_offset
                            input_node.imports.append(import_node)
            elif line.startswith("type ") or line == "type":
                if line == "type":
                    type_statement      = True
                    compare_indentation = get_next_blocks_indentation(line_count+1, code_lines)
                else:
                    line = line.replace("type", "")
                    type_node = NimNode()
                    type_node.name          = line.split("=")[0].strip()
                    type_node.description   = "type"
                    type_node.line          = line_count + line_offset
                    input_node.types.append(type_node)
            elif line.startswith("const ") or line == "const":
                if line == "const":
                    const_statement      = True
                    compare_indentation = get_next_blocks_indentation(line_count+1, code_lines)
                else:
                    line = line.replace("const", "")
                    const_node = NimNode()
                    if ":" in line:
                        const_node.name = line.split(":")[0].strip()
                        const_node.type = line.split(":")[1].split("=")[0].strip()
                    else:
                        const_node.name = line.split("=")[0].strip()
                        const_node.type = None
                    const_node.description  = "const"
                    const_node.line         = line_count + line_offset
                    input_node.consts.append(const_node)
            elif line.startswith("let ") or line == "let":
                if line == "let":
                    let_statement       = True
                    compare_indentation = get_next_blocks_indentation(line_count+1, code_lines)
                else:
                    line = line.replace("let", "")
                    let_node = NimNode()
                    if ":" in line:
                        let_node.name = line.split(":")[0].strip()
                        let_node.type = line.split(":")[1].split("=")[0].strip()
                    else:
                        let_node.name = line.split("=")[0].strip()
                        let_node.type = None
                    let_node.description    = "let"
                    let_node.line           = line_count + line_offset
                    input_node.lets.append(let_node)
            elif line.startswith("var ") or line == "var":
                if line == "var":
                    var_statement       = True
                    compare_indentation = get_next_blocks_indentation(line_count+1, code_lines)
                else:
                    line = line.replace("var", "")
                    if ":" in line and "=" in line and (line.find(":") < line.find("=")):
                        type = line.split(":")[1].split("=")[0].strip()
                        line = line.split(":")[0].strip()
                    elif ":" in line and not("=" in line):
                        type = line.split(":")[1].strip()
                        line = line.split(":")[0].strip()
                    elif "=" in line:
                        type = line.split("=")[1][:line.find("(")].strip()
                        line = line.split("=")[0].strip()
                    for var in line.split(","):
                        var_name = var.strip()
                        if var_name != "":
                            var_node = NimNode()
                            var_node.name           = var_name
                            var_node.description    = "var"
                            var_node.type           = type
                            var_node.line           = line_count + line_offset
                            input_node.vars.append(var_node)
            elif line.startswith("proc "):
                #Create and add the procedure node
                proc_node = NimNode()
                proc_node, skip_to_line =   create_node(
                                                proc_node, 
                                                "proc", 
                                                line, 
                                                line_count, 
                                                code_lines, 
                                                line_offset
                                            )
                proc_node.description   = "procedure"
                proc_node.line          = line_count + line_offset
                #Add the procedure to the main node
                if proc_node.type == "forward declaration":
                    input_node.forward_declarations.append(proc_node)
                else:
                    input_node.procedures.append(proc_node)
                #Set the procedure flag
                proc_statement = True
            elif line.startswith("converter "):
                #Create and add the converter node
                converter_node = NimNode()
                converter_node, skip_to_line =  create_node(
                                                    converter_node, 
                                                    "converter", 
                                                    line, 
                                                    line_count, 
                                                    code_lines, 
                                                    line_offset
                                                )
                converter_node.description  = "converter"
                converter_node.line         = line_count + line_offset
                #Add the converter to the main node
                input_node.converters.append(converter_node)
                #Set the converter flag
                converter_statement = True
            elif line.startswith("iterator "):
                #Create and add the converter node
                iterator_node = NimNode()
                iterator_node, skip_to_line =  create_node(
                                                    iterator_node, 
                                                    "iterator", 
                                                    line, 
                                                    line_count, 
                                                    code_lines, 
                                                    line_offset
                                                )
                iterator_node.description  = "iterator"
                iterator_node.line         = line_count + line_offset
                #Add the iterator to the main node
                input_node.iterators.append(iterator_node)
                #Set the iterator flag
                iterator_statement = True
            elif line.startswith("method "):
                #Create and add the method node
                method_node = NimNode()
                method_node, skip_to_line = create_node(
                                                method_node, 
                                                "method", 
                                                line, 
                                                line_count, 
                                                code_lines, 
                                                line_offset
                                            )
                method_node.description = "method"
                method_node.line        = line_count + line_offset
                #Add the procedure to the main node
                input_node.methods.append(method_node)
                #Set the method flag
                method_statement = True
            elif line.startswith("property "):
                #Create and add the property node
                property_node = NimNode()
                property_node, skip_to_line = create_node(
                                                property_node, 
                                                "property", 
                                                line, 
                                                line_count, 
                                                code_lines, 
                                                line_offset
                                            )
                property_node.description = "property"
                property_node.line        = line_count + line_offset
                #Add the property to the parent node
                input_node.properties.append(property_node)
                #Set the property flag
                property_statement = True
            elif line.startswith("macro "):
                #Create and add the macro node
                macro_node = NimNode()
                macro_node, skip_to_line =  create_node(
                                                macro_node, 
                                                "macro", 
                                                line, 
                                                line_count, 
                                                code_lines, 
                                                line_offset
                                            )
                macro_node.description  = "macro"
                macro_node.line         = line_count + line_offset
                #Add the procedure to the main node
                input_node.macros.append(macro_node)
                #Set the macro flag
                macro_statement = True
            elif line.startswith("template "):
                #Create and add the template node
                template_node = NimNode()
                template_node, skip_to_line =   create_node(
                                                    template_node, 
                                                    "template", 
                                                    line, 
                                                    line_count, 
                                                    code_lines, 
                                                    line_offset
                                                )
                template_node.description   = "template"
                template_node.line          = line_count + line_offset
                #Add the procedure to the main node
                input_node.templates.append(template_node)
                #Set the template flag
                template_statement = True
            elif line.startswith("heap_object ") or line.startswith("stack_object "):
                #Create and add the class node
                if line.startswith("heap_object "):
                    search_term = "heap_object"
                else:
                    search_term = "stack_object"
                object_node = NimNode()
                object_node, skip_to_line    =   create_node(
                                                    object_node, 
                                                    search_term, 
                                                    line, 
                                                    line_count, 
                                                    code_lines, 
                                                    line_offset
                                                )
                object_node.description      = search_term
                object_node.line             = line_count + line_offset
                #Add the class to the main node
                input_node.objects.append(object_node)
                #Set the class flag
                class_statement = True
            elif line.startswith("namespace "):
                #Create and add the class node
                namespace_node = NimNode()
                namespace_node, skip_to_line    =   create_node(
                                                        namespace_node, 
                                                        "namespace", 
                                                        line, 
                                                        line_count, 
                                                        code_lines, 
                                                        line_offset
                                                    )
                namespace_node.description  = "namespace"
                namespace_node.line         = line_count + line_offset
                #Add the class to the main node
                input_node.namespaces.append(namespace_node)
                #Set the class flag
                namespace_statement = True
        return input_node
    #Parse the main node
    main_node = parse_node(main_node, nim_code_lines)
    #Return the node list
    return main_node

def get_python_node_tree(python_code):
    """
    Parse the text and return a node tree as a list.
    The text must be valid Python 3 code.
    """
    #Nested function for recursivly traversing all the child nodes
    def check_children(node, level, function_list):
        lst = []
        for i in ast.iter_child_nodes(node):
            if isinstance(i, ast.ClassDef) or isinstance(i, ast.FunctionDef):
                if isinstance(i, ast.FunctionDef):
                    #Remove the function from the global function list
                    if i in function_list:
                        function_list.remove(i)
                lst.append((level, i))
            #Always descend into the child node to check for nested functions/classes
            lst.extend(check_children(i, level+1, function_list))
        return lst
    #Parse the file
    parsed_string       = ast.parse(python_code)
    nodes               = [node for node in ast.walk(parsed_string)]
    #Get import/import_from nodes, combine them into one list and sort them
    import_nodes        = [(node.names[0].name, node.lineno) for node in nodes if isinstance(node, ast.Import)]
    importfrom_nodes    = [(node.module, node.lineno) for node in nodes if isinstance(node, ast.ImportFrom)]
    import_nodes.extend(importfrom_nodes)
    import_nodes.sort(key=operator.itemgetter(0))
    #Other nodes
    class_nodes         = [node for node in nodes if isinstance(node, ast.ClassDef)]
    function_nodes      = [node for node in nodes if isinstance(node, ast.FunctionDef)]
    global_vars         = [node for node in nodes if isinstance(node, ast.Global)]
    #Get child nodes for all of the classes
    children         = []
    class_tree_nodes = []
    for c_node in class_nodes:
        #Check if the node has already been parsed as a child node in another class
        if not(c_node in children):
            cc = check_children(c_node, 0, function_nodes)
            class_tree_nodes.append((c_node, cc))
            children.extend([c[1] for c in cc])
    #Return the parse results
    return import_nodes, class_tree_nodes, function_nodes, global_vars

def get_c_function_list(c_code):
    """
    Parse the text and return all C functions as a list.
    Made as simple as possible.
    The text must be valid C code.
    """
    #Store the text
    text = c_code
    #Initialize state variables
    curly_count = 0
    parenthesis_count = 0
    singleline_commenting = False
    multiline_commenting = False
    previous_token = ""
    last_found_function = ""
    last_line = 0
    current_line = 1
    function_list = []
    #Tokenize the text and remove the space characters
    splitter = re.compile(r"(\{\.|\.\}|\#|\'|\"\"\"|\n|\s+|\w+|\W)")
    tokens = [token for token in splitter.findall(text)]
    #Main Loop for filtering tokens
    for token in tokens:
        stripped_token = token.strip()
        if "\n" in token:
            newline_count = token.count("\n")
            current_line += newline_count
            #Reset the single line comment flag
            singleline_commenting = False
        if stripped_token == "":
            continue
        #Check for function definitions
        if curly_count == 0:
            if multiline_commenting == False and singleline_commenting == False:
                if token == "{" and previous_token == ")":
                    #The function has passed the filter, add it to the list
                    function_list.append((last_found_function, last_line))
                elif token == "(" and re.match(r"\w", previous_token) and parenthesis_count == 0:
                    last_found_function = previous_token
                    last_line = current_line
        #Check for various state changes
        if multiline_commenting == False and singleline_commenting == False:
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
        #Store the previous token
        if stripped_token != "":
            previous_token = token
    #Sort the functions alphabetically
    def compare_function(item):
        return item[0].lower()
    function_list = sorted(function_list, key=compare_function)
    #Return the function list
    return function_list

def test_text_file(file_with_path):
    """Test if a file is a plain text file and can be read"""
    #Try to read all of the lines in the file, return None if there is an error 
    #(using Grace Hopper's/Alex Martelli's forgivness/permission principle)
    try:
        file = open(file_with_path, "r", encoding=locale.getpreferredencoding(), errors="strict")
        #Read only a couple of lines in the file
        for line in itertools.islice(file, 10):
            line = line
        file.readlines()
        #Close the file handle
        file.close()
        #Return the systems preferred encoding 
        return locale.getpreferredencoding()
    except:
        test_encodings = ["utf-8", "ascii", "utf-16", "utf-32", "iso-8859-1", "latin-1"]
        for current_encoding in test_encodings:
            try:
                file = open(file_with_path, "r", encoding=current_encoding, errors="strict")
                #Read only a couple of lines in the file
                for line in itertools.islice(file, 10):
                    line = line
                #Close the file handle
                file.close()
                #Return the succeded encoding
                return current_encoding
            except:
                #Error occured while reading the file, skip to next iteration
                continue
    #Error, no encoding was correct
    return None

def test_binary_file(file_with_path):
    """Test if a file is in binary format"""
    file = open(file_with_path, "rb")
    #Read only a couple of lines in the file
    binary_text = None
    for line in itertools.islice(file, 20):
        if b"\x00" in line:
            #Return to the beginning of the binary file
            file.seek(0)
            #Read the file in one step
            binary_text = file.read()
            break
    file.close()
    #Return the result
    return binary_text

def get_file_type(file_with_path):
    """Get file extension and return file type as string"""
    #Initialize it as unknown and change it in the if statement 
    file_type = "unknown"   
    #Split the file and path
    path, file = os.path.split(file_with_path)
    #Split file name and extension
    file_name, file_extension   = os.path.splitext(file)
    if file.lower() == "user_functions.cfg":
        #First check to see if the user functions file has been opened
        file_type = "python"
    elif file_extension.lower() in data.ext_python:
        file_type = "python"
    elif file_extension.lower() in data.ext_cpython:
        file_type = "cython"
    elif file_extension.lower() in data.ext_c:
        file_type = "c"
    elif file_extension.lower() in data.ext_cpp:
        file_type = "c++"
    elif file_extension.lower() in data.ext_pascal:
        file_type = "pascal"
    elif file_extension.lower() in data.ext_oberon:
        file_type = "oberon/modula"
    elif file_extension.lower() in data.ext_ada:
        file_type = "ada"
    elif file_extension.lower() in data.ext_xml:
        file_type = "xml"
    elif file_extension.lower() in data.ext_d:
        file_type = "d"
    elif file_extension.lower() in data.ext_nim:
        file_type = "nim"
    elif file_extension.lower() in data.ext_json:
        file_type = "json"
    elif file_extension.lower() in data.ext_perl:
        file_type = "perl"
    elif file_extension.lower() in data.ext_ini:
        file_type = "ini"
    elif file_extension.lower() in data.ext_batch:
        file_type = "batch"
    elif file_extension.lower() in data.ext_bash:
        file_type = "bash"
    elif file_name.lower() == "makefile":
        file_type = "makefile"
    elif file_extension.lower() in data.ext_lua:
        file_type = "lua"
    elif file_extension.lower() in data.ext_coffeescript:
        file_type = "coffeescript"
    elif file_extension.lower() in data.ext_csharp:
        file_type = "c#"
    elif file_extension.lower() in data.ext_java:
        file_type = "java"
    elif file_extension.lower() in data.ext_javascript:
        file_type = "javascript"
    elif file_extension.lower() in data.ext_octave:
        file_type = "octave"
    elif file_extension.lower() in data.ext_sql:
        file_type = "sql"
    elif file_extension.lower() in data.ext_postscript:
        file_type = "postscript"
    elif file_extension.lower() in data.ext_fortran:
        file_type = "fortran"
    elif file_extension.lower() in data.ext_fortran77:
        file_type = "fortran77"
    elif file_extension.lower() in data.ext_idl:
        file_type = "idl"
    elif file_extension.lower() in data.ext_ruby:
        file_type = "ruby"
    elif file_extension.lower() in data.ext_html:
        file_type = "html"
    elif file_extension.lower() in data.ext_css:
        file_type = "css"
    else:
        #The file extension was not recognized, 
        #try the file contents for more information
        file_type = test_file_content_for_type(file_with_path)
        #If the file content did not give any useful information,
        #set the content as text
        if file_type == "unknown":
            file_type = "text"
    #Return file type string
    return file_type

def test_file_content_for_type(file_with_path):
    """Test the first line of a file for relevant file type data"""
    file_type = "unknown"
    try:
        first_line = ""
        #Read the first non-empty line in the file
        with open(file_with_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.strip() == "":
                    continue
                else:
                    first_line = line
                    break
        #Prepare the line
        first_line = first_line.lower().strip()
        #Check the line content
        if "<?xml" in first_line:
            file_type = "xml"
        elif "#!" in first_line and "python" in first_line:
            file_type = "python"
        elif "#!" in first_line and "perl" in first_line:
            file_type = "perl"
        elif "#!" in first_line and "ruby" in first_line:
            file_type = "ruby"
        #Return the file type
        return file_type
    except:
        #Error reading the file
        return file_type
    

def read_file_to_string(file_with_path):
    """Read contents of a text file to a single string"""
    #Test if a file is in binary format
    binary_text = test_binary_file(file_with_path)
    if binary_text != None:
        cleaned_binary_text = binary_text.replace(b"\x00",b"")
#        cleaned_binary_text = re.sub(b'[\x00]+',b'', binary_text)
#        cleaned_binary_text = re.sub(b'[\x00-\x7f]+',b'.', binary_text)
        return cleaned_binary_text.decode(encoding="utf-8", errors="replace")
    else:
        #File is not binary, loop through encodings to find the correct one.
        #Try the default Ex.Co. encoding UTF-8 first
        test_encodings = ["utf-8", "cp1250", "ascii", "utf-16", "utf-32", "iso-8859-1", "latin-1"]
        for current_encoding in test_encodings:
            try:
                #If opening the file in the default Ex.Co. encoding fails,
                #open it using the prefered system encoding!
                file = open(file_with_path, "r", encoding=current_encoding, errors="strict")
                #Read the whole file with "read()"
                text = file.read()
                #Close the file handle
                file.close()
                #Return the text string
                return text
            except:
                #Error occured while reading the file, skip to next encoding
                continue
    #Error, no encoding was correct
    return None

def read_binary_file_as_generator(file_object, chunk_size=1024):
    """
    Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k.
    """
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data

def read_file_to_list(file_with_path):
    """Read contents of a text file to a list"""
    text = read_file_to_string(file_with_path)
    if text != None:
        return text.split("\n")
    else:
        return None

def write_to_file(text, file_with_path, encoding="utf-8"):
    """Write text to a file"""
    #Again, the forgiveness principle
    try:
        #Encode the file to the selected encoding
        if encoding != "utf-8":
            #Convert UTF-8 string into a byte array
            byte_string = bytearray(text, encoding=encoding, errors="replace")
            #Convert the byte array into the desired encoding,
            #unknown characters will be displayed as question marks or something similar
            text = codecs.decode(byte_string, encoding, "replace")
        #Open the file for writing, create it if it doesn't exists
        file = open(file_with_path, "w", newline="", encoding=encoding)
        #Write text to the file
        file.write(text)
        #Close the file handle
        file.close()
        #Writing to file succeded
        return True
    except Exception as ex:
        #Wrtiting to file failed, return error message
        return ex

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
    #Check for and extend the list with all matches
    for i, line in enumerate(list_of_lines):
        line_matches = [(i, match.start(), i, match.end()) for match in re.finditer(compiled_search_re, line)]
        list_of_matches.extend(line_matches)
    return list_of_matches

def index_strings_in_text(search_text, 
                          text, 
                          case_sensitive=False, 
                          regular_expression=False, 
                          text_to_bytes=False):
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
    """
    if text_to_bytes == True:
        search_text = bytes(search_text, "utf-8")
        text = bytes(text, "utf-8")
    #Set the search text according to the regular expression selection
    if regular_expression == False:
        search_text     = re.escape(search_text)
    #Compile expression according to case sensitivity flag
    if case_sensitive == True:
        compiled_search_re = re.compile(search_text)
    else:
        compiled_search_re = re.compile(search_text, re.IGNORECASE)
    #Create the list with all of the matches
    list_of_matches = [(0, match.start(), 0, match.end()) for match in re.finditer(compiled_search_re, text)]
    return list_of_matches

def check_unmatched_quotes(string):
    """
    Check if there are unmatched single/double quotes in the text and
    return the position of the last unmatched quote character
    """
    #Define locals
    found_single            = False
    found_double            = False
    last_quote_position     = None
    #Loop through all the characters in the string
    for i, ch in enumerate(string):
        #Check for a double quote
        if ch == "\"":
            if found_double == False and found_single == False:
                #Save state that the quote was found
                found_double            = True
                #Save quote position 
                last_quote_position     = i
            elif found_double == True:
                #Reset quote state
                found_double            = False
                last_quote_position     = None
        #Check for a single quote
        elif ch == "'":
            if found_single == False and found_double == False:
                #Save state that the quote was found
                found_single            = True
                #Save quote position 
                last_quote_position     = i
            elif found_single == True:
                #Reset quote state
                found_single            = False
                last_quote_position     = None
    #Return the last unclosed quote position
    return last_quote_position

def is_number(string):
    """Check if the string is a number (integer or float)"""
    try: 
        float(string)
        return True
    except ValueError:
        return False

def replace_and_index(input_string,  
                      search_text, 
                      replace_text, 
                      case_sensitive=False, 
                      regular_expression=False):
    """
    Function that replaces the search text with replace text in a string,
    using regular expressions if specified, and returns the
    line numbers and indexes of the replacements as a list.
    """
    #First check if the replacement action is needed
    if search_text == replace_text and case_sensitive == True:
        return None, input_string
    elif search_text.lower() == replace_text.lower() and case_sensitive == False:
        return None, input_string
    #Initialize the return variables
    replaced_text   = None
    #Find the search text matches that will be highlighted (pre-replacement)
    #Only when not searching with regular expressions
    if regular_expression == False :
        matches = index_strings_in_text(
                      search_text, 
                      input_string, 
                      case_sensitive, 
                      regular_expression, 
                      text_to_bytes=True
                  )    
    #Create a matches list according to regular expression selection
    if regular_expression == True:
        #Compile the regular expression object according to the case sensitivity
        if case_sensitive == True:
            compiled_search_re = re.compile(search_text)
        else:
            compiled_search_re = re.compile(search_text, re.IGNORECASE)
        #Replace all instances of search text with the replace text
        replaced_text = re.sub(compiled_search_re, replace_text, input_string)
        replaced_match_indexes  = []
        #Split old and new texts into line lists
        split_input_text    = input_string.split("\n")
        split_replaced_text = replaced_text.split("\n")
        #Loop through the old text and compare it line-by-line to the old text
        try:
            for i in range(len(split_input_text)):
                if split_input_text[i] != split_replaced_text[i]:
                    replaced_match_indexes.append(i)
        except:
            #If regular expression replaced lines,
            #then we cannot highlight the replacements
            replaced_match_indexes  = []
    else:
        replaced_text = None
        if case_sensitive == True:
            #Standard string replace
            replaced_text = input_string.replace(search_text, replace_text)
        else:
            #Escape the regex special characters
            new_search_text     = re.escape(search_text)
            #Replace backslashes with double backslashes, so that the
            #regular expression treats backslashes the same as standard
            #Python string replace!
            new_replace_text    = replace_text.replace("\\", "\\\\")
            compiled_search_re  = re.compile(new_search_text, re.IGNORECASE)
            replaced_text       = re.sub(
                                      compiled_search_re, 
                                      new_replace_text, 
                                      input_string
                                  )
        replaced_match_indexes  = []
        #Loop while storing the new indexes
        diff = 0
        bl_search   = bytes(search_text, "utf-8")
        bl_search   = len(bl_search.replace(b"\\", b" "))
        bl_replace  = bytes(replace_text, "utf-8")
        bl_replace  = len(bl_replace.replace(b"\\", b" "))
        for i, match in enumerate(matches):
            #Subtract the length of the search text from the match index,
            #to offset the shortening of the whole text when the lenght
            #of the replace text is shorter than the search text
            diff = (bl_replace - bl_search) * i
            new_index = match[1] + diff
            #Check if the index correction went into a negative index
            if new_index < 0:
                new_index = 0
            #The line is always 0, because Scintilla also allows 
            #indexing over multiple lines! If the index number goes
            #over the length of a line, it "overflows" into the next line.
            #Basically this means that you can access any line/index by
            #treating the whole text not as a list of lines, but as an array.
            replaced_match_indexes.append(
                (
                    0,
                    new_index, 
                    0, 
                    new_index+bl_replace
                )
            )
    #Return the match list and the replaced text
    return replaced_match_indexes, replaced_text

def regex_replace_text(input_string, 
                       search_text, 
                       replace_text, 
                       case_sensitive=False, 
                       regular_expression=False):
    """Function that uses the re module to replace text in a string"""
    replaced_text   = None
    if regular_expression == True:
        if case_sensitive == True:
            compiled_search_re = re.compile(search_text)
        else:
            compiled_search_re = re.compile(search_text, re.IGNORECASE)
        replaced_text   = re.sub(compiled_search_re, replace_text, input_string)
    else:
        if case_sensitive == True:
            replaced_text   = input_string.replace(search_text, replace_text)
        else:
            #'re.escape' replaces the re module special characters with literals,
            #so that the search_text is treated as a string literal
            compiled_re     = re.compile(re.escape(search_text), re.IGNORECASE)
            replaced_text   = re.sub(compiled_re, replace_text, input_string)
    return replaced_text

def right_replace(string, search_str, replace_str, occurrence=1):
    """
    Replace the instance of substring in string,
    beginning from the right side of the string
    """
    split_string = string.rsplit(search_str, occurrence)
    return replace_str.join(split_string)

def get_line_indentation(line):
    """Function for determining the indentation level of a line string"""
    indentation = 0
    for char in line:
        if char == " ":
            indentation += 1
        else:
            break
    return indentation
