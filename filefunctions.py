"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import codecs
import json
import locale
import os
import pathlib
import re
import itertools

import data


def write_json_file(filepath, json_data) -> None:
    with open(filepath, "w+", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(json_data, indent=2, ensure_ascii=False))
        f.close()


def load_json_file(filepath) -> str:
    with open(filepath, "r", encoding="utf-8", newline="\n") as f:
        json_data = json.load(f)
        f.close()
    return json_data


def are_paths_same(path1, path2) -> bool:
    return pathlib.Path(path1).resolve() == pathlib.Path(path2).resolve()


def is_parent_directory(base_path: str, tested_path: str) -> bool:
    base = pathlib.Path(base_path).resolve()
    tested = pathlib.Path(tested_path).resolve()

    try:
        tested.relative_to(base)
        return base != tested  # Exclude exact match
    except ValueError:
        return False


def get_file_size_Mb(file_with_path):
    """Get the file size in Mb"""
    size_bytes = os.path.getsize(file_with_path)
    # Convert size into megabytes
    size_Mb = size_bytes / (1024 * 1024)
    # return the size in megabyte
    return size_Mb


def replace_text_in_files_enum(
    search_text,
    replace_text,
    search_dir,
    case_sensitive=False,
    search_subdirs=True,
    file_filter=None,
):
    """
    The second version of replace_text_in_files, that goes line-by-line
    and replaces found instances and stores the line numbers,
    at which the replacements were made
    """
    # Check if the directory is valid
    if not os.path.isdir(search_dir):
        return -1
    # Check if searching over multiple lines
    elif "\n" in search_text:
        return -2
    # Get the files with the search string in them
    found_files = find_files_with_text(
        search_text,
        search_dir,
        case_sensitive=case_sensitive,
        search_subdirs=search_subdirs,
        break_on_find=False,
        file_filter=file_filter,
    )
    if found_files is None:
        return {}
    # Compile the regex expression according to case sensitivity
    if case_sensitive:
        compiled_search_re = re.compile(search_text)
    else:
        compiled_search_re = re.compile(search_text, re.IGNORECASE)
    # Loop through the found list and replace the text
    return_files = {}
    for file in found_files:
        # Read the file
        file_text_list = read_file_to_list(file)
        # Cycle through the lines, replacing text and storing the line numbers of replacements
        for i in range(len(file_text_list)):
            if case_sensitive:
                line = file_text_list[i]
            else:
                search_text = search_text.lower()
                line = file_text_list[i].lower()
            if search_text in line:
                if file in return_files:
                    return_files[file].append(i)
                else:
                    return_files[file] = [i]
                file_text_list[i] = re.sub(
                    compiled_search_re, replace_text, file_text_list[i]
                )
        # Write the replaced text back to the file
        replaced_text = "\n".join(file_text_list)
        write_to_file(replaced_text, file)
    # Return the found files list
    return return_files


def find_files_by_name(
    search_filename, search_dir, case_sensitive=False, search_subdirs=True
):
    """
    Find file with search_filename string in its name in the specified directory.
    """
    # Check if the directory is valid
    if not os.path.isdir(search_dir):
        return None
    # Create an empty file list
    found_file_list = []
    # Check if subdirectories should be included
    if search_subdirs:
        walk_tree = os.walk(search_dir)
    else:
        # Only use the first generator value(only the top directory)
        walk_tree = [next(os.walk(search_dir))]
    for root, subFolders, files in walk_tree:
        for file in files:
            # Merge the path and filename
            full_with_path = os.path.join(root, file)
            # Set the comparison according to case sensitivity
            if not case_sensitive:
                compare_actual_filename = file.lower()
                compare_search_filename = search_filename.lower()
            else:
                compare_actual_filename = file
                compare_search_filename = search_filename
            # Test if the name of the file contains the search string
            if compare_search_filename in compare_actual_filename:
                # On windows, the function "os.path.join(root, file)" line gives a combination of "/" and "\\",
                # which looks weird but works. The replace was added to have things consistent in the return file list.
                full_with_path = full_with_path.replace("\\", "/")
                found_file_list.append(full_with_path)
    # Return the generated list
    return found_file_list


def find_files_with_text(
    search_text,
    search_dir,
    case_sensitive=False,
    search_subdirs=True,
    break_on_find=False,
    file_filter=None,
):
    """
    Search for the specified text in files in the specified directory and return a file list.
    """
    # Check if the directory is valid
    if os.path.isdir(search_dir) == False:
        return None
    # Create an empty file list
    text_file_list = []
    # Check if subdirectories should be included
    if search_subdirs == True:
        walk_tree = os.walk(search_dir)
    else:
        # Only use the first generator value(only the top directory)
        walk_tree = [next(os.walk(search_dir))]
    # "walk" through the directory tree and save the readable files to a list
    for root, subFolders, files in walk_tree:
        for file in files:
            if file_filter is not None:
                filename, file_extension = os.path.splitext(file)
                if file_extension.lower() not in file_filter:
                    continue
            # Merge the path and filename
            full_with_path = os.path.join(root, file)
            if test_text_file(full_with_path) != None:
                # On windows, the function "os.path.join(root, file)" line gives a combination of "/" and "\\",
                # which looks weird but works. The replace was added to have things consistent in the return file list.
                full_with_path = full_with_path.replace("\\", "/")
                text_file_list.append(full_with_path)
    # Search for the text in found files
    return_file_list = []
    for file in text_file_list:
        try:
            file_text = read_file_to_string(file)
            # Set the comparison according to case sensitivity
            if case_sensitive == False:
                compare_file_text = file_text.lower()
                compare_search_text = search_text.lower()
            else:
                compare_file_text = file_text
                compare_search_text = search_text
            #            print(compare_search_text)
            # Check if file contains the search string
            if compare_search_text in compare_file_text:
                return_file_list.append(file)
                # Check if break option on first find is true
                if break_on_find == True:
                    break
        except:
            continue
    # Return the generated list
    return return_file_list


def find_files_with_text_enum(
    search_text,
    search_dir,
    case_sensitive=False,
    search_subdirs=True,
    break_on_find=False,
    file_filter=None,
    cancel_flag=lambda: False,
):
    """
    Search for the specified text in files in the specified directory and return a file list and
    lines where the text was found at.
    """
    if os.path.isdir(search_dir) == False:
        return "Invalid directory!"
    elif "\n" in search_text:
        return "Cannot search over multiple lines!"
    elif search_text == "":
        return "Cannot search for empty string!"

    text_file_list = []

    if search_subdirs:
        walk_tree = os.walk(search_dir)
    else:
        walk_tree = [next(os.walk(search_dir))]

    for root, subFolders, files in walk_tree:
        if cancel_flag():
            return "Search canceled!"
        for file in files:
            if cancel_flag():
                return "Search canceled!"
            if file_filter is not None:
                _, file_extension = os.path.splitext(file)
                if file_extension.lower() not in file_filter:
                    continue
            full_with_path = os.path.join(root, file)
            if test_text_file(full_with_path) is not None:
                full_with_path = full_with_path.replace("\\", "/")
                text_file_list.append(full_with_path)

    return_file_dict = {}
    for file in text_file_list:
        if cancel_flag():
            return "Search canceled!"
        try:
            file_lines = read_file_to_list(file)
            compare_search_text = search_text if case_sensitive else search_text.lower()

            for i, line in enumerate(file_lines):
                if cancel_flag():
                    return "Search canceled!"
                current_line = line if case_sensitive else line.lower()
                if compare_search_text in current_line:
                    return_file_dict.setdefault(file, []).append(i)
                    if break_on_find:
                        return return_file_dict
        except:
            continue

    return return_file_dict


def test_text_file(file_with_path):
    """Test if a file is a plain text file and can be read"""
    # Try to read all of the lines in the file, return None if there is an error
    # (using Grace Hopper's/Alex Martelli's forgivness/permission principle)
    try:
        file = open(
            file_with_path, "r", encoding=locale.getpreferredencoding(), errors="strict"
        )
        # Read only a couple of lines in the file
        for line in itertools.islice(file, 10):
            line = line
        file.readlines()
        # Close the file handle
        file.close()
        # Return the systems preferred encoding
        return locale.getpreferredencoding()
    except:
        test_encodings = ["utf-8", "ascii", "utf-16", "utf-32", "iso-8859-1", "latin-1"]
        for current_encoding in test_encodings:
            try:
                file = open(
                    file_with_path, "r", encoding=current_encoding, errors="strict"
                )
                # Read only a couple of lines in the file
                for line in itertools.islice(file, 10):
                    line = line
                # Close the file handle
                file.close()
                # Return the succeded encoding
                return current_encoding
            except:
                # Error occured while reading the file, skip to next iteration
                continue
    # Error, no encoding was correct
    return None


def test_binary_file(file_with_path):
    """Test if a file is in binary format"""
    file = open(file_with_path, "rb")
    # Read only a couple of lines in the file
    binary_text = None
    for line in itertools.islice(file, 20):
        if b"\x00" in line:
            # Return to the beginning of the binary file
            file.seek(0)
            # Read the file in one step
            binary_text = file.read()
            break
    file.close()
    # Return the result
    return binary_text


def get_file_type(file_with_path, check_content=True):
    """Get file extension and return file type as string"""
    # Initialize it as unknown and change it in the if statement
    file_type = "unknown"
    # Split the file and path
    path, file = os.path.split(file_with_path)
    # Split file name and extension
    file_name, file_extension = os.path.splitext(file)
    if file_with_path.lower() == data.config_file.lower() or file.lower() == "exco.ini":
        # First check to see if the user functions file has been opened
        file_type = "python"
    elif file_name.lower() == "makefile":
        file_type = "makefile"
    elif "cmakelists" in file_name.lower():
        file_type = "cmake"
    else:
        for k, v in data.supported_file_extentions.items():
            if file_extension.lower() in v:
                file_type = k
                break
        else:
            if check_content == True:
                # The file extension was not recognized,
                # try the file contents for more information
                file_type = test_file_content_for_type(file_with_path)
                # If the file content did not give any useful information,
                # set the content as text
                if file_type == "unknown":
                    file_type = "text"
            else:
                file_type = "text"
    # Return file type string
    return file_type


def test_file_content_for_type(file_with_path):
    """Test the first line of a file for relevant file type data"""
    file_type = "unknown"
    try:
        first_line = ""
        # Read the first non-empty line in the file
        with open(file_with_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                if line.strip() == "":
                    continue
                else:
                    first_line = line
                    break
        # Prepare the line
        first_line = first_line.lower().strip()
        # Check the line content
        if "<?xml" in first_line:
            file_type = "xml"
        elif "<?php" in first_line:
            file_type = "php"
        elif "#!" in first_line and "python" in first_line:
            file_type = "python"
        elif "#!" in first_line and "perl" in first_line:
            file_type = "perl"
        elif "#!" in first_line and "ruby" in first_line:
            file_type = "ruby"
        elif (
            ("#!" in first_line and "bash" in first_line)
            or ("#!" in first_line and "dash" in first_line)
            or ("#!" in first_line and "sh" in first_line)
        ):
            file_type = "bash"
        # Return the file type
        return file_type
    except:
        # Error reading the file
        return file_type


def read_file_to_string(file_with_path):
    """Read contents of a text file to a single string"""
    # Test if a file is in binary format
    binary_text = test_binary_file(file_with_path)
    if binary_text != None:
        cleaned_binary_text = binary_text.replace(b"\x00", b"")
        #        cleaned_binary_text = re.sub(b'[\x00]+',b'', binary_text)
        #        cleaned_binary_text = re.sub(b'[\x00-\x7f]+',b'.', binary_text)
        return cleaned_binary_text.decode(encoding="utf-8", errors="replace")
    else:
        # File is not binary, loop through encodings to find the correct one.
        # Try the default Ex.Co. encoding UTF-8 first
        test_encodings = [
            "utf-8",
            "cp1250",
            "ascii",
            "utf-16",
            "utf-32",
            "iso-8859-1",
            "latin-1",
            "gb2312",
        ]
        for current_encoding in test_encodings:
            try:
                # If opening the file in the default Ex.Co. encoding fails,
                # open it using the prefered system encoding!
                with open(
                    file_with_path,
                    "r",
                    encoding=current_encoding,
                    errors="surrogateescape",
                ) as file:
                    # Read the whole file with "read()"
                    text = file.read()
                    # Close the file handle
                    file.close()
                # Return the text string
                return text
            except:
                # Error occured while reading the file, skip to next encoding
                continue
    # Error, no encoding was correct
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
    # Again, the forgiveness principle
    try:
        # Encode the file to the selected encoding
        if encoding != "utf-8":
            # Convert UTF-8 string into a byte array
            byte_string = bytearray(text, encoding=encoding, errors="replace")
            # Convert the byte array into the desired encoding,
            # unknown characters will be displayed as question marks or something similar
            text = codecs.decode(byte_string, encoding, "replace")
        # Open the file for writing, create it if it doesn't exists
        with open(file_with_path, "w", newline="", encoding=encoding) as file:
            # Write text to the file
            file.write(text)
            # Close the file handle
            file.close()
        # Writing to file succeded
        return True
    except Exception as ex:
        # Wrtiting to file failed, return error message
        return ex
