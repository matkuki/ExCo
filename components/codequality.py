"""
Prettyfying functions
"""

import collections
import enum
import html
import html.parser
import importlib.util
import io
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import xml.dom.minidom
import xml.etree.ElementTree
from typing import *

import autopep8
import black
import bs4
import isort
import ruff
import yapf


def pretty_print_json(
    input_string: str,
    sort_keys: bool = True,
    key_sort_function: Callable[[str], Any] = None,
) -> str:
    """
    Pretty print JSON with optional key sorting.

    Args:
        input_string: JSON string to format
        sort_keys: Whether to sort keys alphabetically
        key_sort_function: Custom function for sorting keys
                          (e.g., lambda x: x.lower() for case-insensitive sorting)

    Returns:
        Formatted JSON string
    """
    try:
        json_object = json.loads(input_string)
    except json.JSONDecodeError as e:
        raise ValueError("Invalid JSON") from e

    if sort_keys:
        if key_sort_function:
            sorted_object = sort_json_keys_custom(json_object, key_sort_function)
        else:
            sorted_object = sort_json_keys_recursive(json_object)
    else:
        sorted_object = json_object

    pretty_json = json.dumps(sorted_object, indent=2, ensure_ascii=False)
    return pretty_json


def sort_json_keys_recursive(obj):
    """
    Recursively sort JSON keys using OrderedDict for consistent ordering.
    """
    if isinstance(obj, dict):
        return collections.OrderedDict(
            (key, sort_json_keys_recursive(obj[key])) for key in sorted(obj.keys())
        )
    elif isinstance(obj, list):
        return [sort_json_keys_recursive(item) for item in obj]
    else:
        return obj


def sort_json_keys_custom(obj: Any, key_sort_function: Callable[[str], Any]) -> Any:
    """
    Recursively sort JSON keys using a custom sorting function.
    """
    if isinstance(obj, dict):
        sorted_keys = sorted(obj.keys(), key=key_sort_function)
        return {
            key: sort_json_keys_custom(obj[key], key_sort_function)
            for key in sorted_keys
        }
    elif isinstance(obj, list):
        return [sort_json_keys_custom(item, key_sort_function) for item in obj]
    else:
        return obj


def pretty_print_xml(input_string: str) -> str:
    try:
        # Parse the input string to check if it's valid XML
        element = xml.etree.ElementTree.fromstring(input_string)
    except xml.etree.ElementTree.ParseError as e:
        # Raise an exception if the input is not valid XML
        raise ValueError("Invalid XML") from e

    # Convert the ElementTree element back to a string
    rough_string = xml.etree.ElementTree.tostring(element, "utf-8")

    # Use minidom to pretty-print the XML with an indentation level of 2
    reparsed = xml.dom.minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")

    return pretty_xml


def pretty_print_html_python_stdlib(input_string):
    # Validate HTML
    class HTMLValidator(html.parser.HTMLParser):
        def error(self, message):
            raise ValueError("Invalid HTML: " + message)

    validator = HTMLValidator()
    # Unescape HTML entities before validation
    unescaped_input = html.unescape(input_string)
    validator.feed(unescaped_input)

    # Pretty-print HTML
    try:
        dom = xml.dom.minidom.parseString(unescaped_input)
        pretty_html = dom.toprettyxml(indent="  ", newl="\n", encoding="UTF-8").decode(
            "UTF-8"
        )
        return pretty_html
    except Exception as e:
        raise ValueError("Error in pretty-printing HTML: " + str(e))


def format_clangformat_c_cpp(source_code: str, style: str = "LLVM") -> str:
    """Formats C/C++ source code using clang-format."""
    result = subprocess.run(
        ["clang-format", f"--style={{BasedOnStyle: {style}, IndentWidth: 4}}"],
        input=source_code.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return result.stdout.decode()


def format_ruff_python(code: str) -> str:
    with tempfile.TemporaryDirectory() as tmpdir:  # type: ignore
        file_path: pathlib.Path = pathlib.Path(tmpdir) / "temp_ruff_formatting_file.py"
        file_path.write_text(code, encoding="utf-8")

        result: subprocess.CompletedProcess[str] = subprocess.run(
            ["ruff", "format", str(file_path)],
            capture_output=True,
            text=True,
            encoding="utf-8",  # Ensure subprocess handles UTF-8 output
        )

        if result.returncode != 0:
            raise RuntimeError(f"Ruff error:\n{result.stderr}")

        return file_path.read_text(encoding="utf-8")


def format_zig_code(zig_code_string: str) -> str:
    """
    Formats a given Zig source code string using the 'zig fmt --stdin' command.

    Args:
        zig_code_string: The unformatted Zig source code as a string.

    Returns:
        The formatted Zig source code string.

    Raises:
        FileNotFoundError: If 'zig' executable is not found in the system's PATH.
        subprocess.CalledProcessError: If 'zig fmt' exits with a non-zero status
                                       (e.g., due to syntax errors in the input code).
        Exception: For any other unexpected errors during subprocess execution.
    """
    try:
        # Construct the command for zig fmt to read from stdin
        command: list[str] = ["zig", "fmt", "--stdin"]

        # Run the subprocess
        # input: The string to pass to stdin, encoded to bytes
        # capture_output=True: Capture stdout and stderr
        # text=True: Decode stdout/stderr as text using default encoding (usually UTF-8)
        # check=True: Raise CalledProcessError if the command returns a non-zero exit code
        # encoding='utf-8': Explicitly specify encoding for robustness
        result: subprocess.CompletedProcess[str] = subprocess.run(
            command,
            input=zig_code_string,
            capture_output=True,
            text=True,
            check=True,
            encoding="utf-8",
        )

        # The formatted output is in stdout
        return result.stdout.strip()

    except FileNotFoundError:
        # This occurs if the 'zig' executable is not found in PATH
        raise FileNotFoundError(
            "The 'zig' executable was not found. "
            "Please ensure Zig is installed and 'zig' is in your system's PATH."
        )
    except subprocess.CalledProcessError as e:
        # This occurs if 'zig fmt' itself encounters an error (e.g., invalid Zig syntax)
        error_message: str = f"Zig formatting failed with exit code {e.returncode}:\n"
        if e.stdout:
            error_message += f"STDOUT:\n{e.stdout}\n"
        if e.stderr:
            error_message += f"STDERR:\n{e.stderr}\n"
        # Re-raise the original exception with potentially more context
        raise subprocess.CalledProcessError(
            returncode=e.returncode,
            cmd=e.cmd,
            output=e.output,  # Use e.output for combined stdout/stderr if available, or e.stdout
            stderr=e.stderr,  # Explicitly pass stderr
        ) from e
    except Exception as e:
        # Catch any other unexpected exceptions
        raise Exception(f"An unexpected error occurred while formatting Zig code: {e}")


def format_nim_file(file_path: str) -> bool:
    """
    Formats a given Nim source code file in-place using the 'nph --format <file_path>' command.

    Args:
        file_path: The path to the unformatted Nim source code file.

    Returns:
        True if the formatting was successful, False otherwise.

    Raises:
        FileNotFoundError: If 'nph' executable is not found in the system's PATH,
                           or if the specified Nim file does not exist.
        subprocess.CalledProcessError: If 'nph --format' exits with a non-zero status
                                       (e.g., due to syntax errors in the input file).
        Exception: For any other unexpected errors during subprocess execution.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The specified Nim file was not found: {file_path}")

    try:
        # 1. Construct the command: nph <file_path>
        # The formatter modifies the file in-place and doesn't print the output to stdout
        command: List[str] = ["nph", file_path]

        # 2. Run the subprocess
        # input is not needed as the file path is provided in the command
        # capture_output=True: Capture stdout and stderr
        # check=True: Raise CalledProcessError if the command returns a non-zero exit code
        result: subprocess.CompletedProcess[str] = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            encoding="utf-8",
        )

        # nph doesn't typically output formatted code to stdout when modifying a file.
        # It's considered successful if it exits with code 0.
        return True

    except FileNotFoundError:
        # This occurs if the 'nph' executable is not found in PATH
        # We re-raise to indicate the specific issue with the executable
        raise FileNotFoundError(
            "The 'nph' executable was not found. "
            "Please ensure the Nim 'nph' tool is installed and in your system's PATH."
        )
    except CalledProcessError as e:
        # This occurs if 'nph --format' itself encounters an error (e.g., invalid Nim syntax)
        error_message: str = f"Nim formatting (nph) failed with exit code {e.returncode} for file {file_path}:\n"
        if e.stderr:
            error_message += f"STDERR:\n{e.stderr}\n"

        # Re-raise the original exception
        raise CalledProcessError(
            returncode=e.returncode,
            cmd=e.cmd,
            output=e.output,
            stderr=e.stderr,
        ) from e
    except Exception as e:
        # Catch any other unexpected exceptions
        raise Exception(f"An unexpected error occurred while formatting Nim code: {e}")


def format_python_code(code: str, library: str) -> str:
    # Choose formatter based on the specified library
    if library == "black":
        # Format code using Black with default settings
        formatted_code: str = black.format_str(code, mode=black.FileMode())

    elif library == "autopep8":
        # Format code using autopep8
        formatted_code = autopep8.fix_code(code)

    elif library == "yapf":
        # Format code using yapf; returns (formatted_code, changed_flag)
        formatted_code, _ = yapf.yapf_api.FormatCode(code)

    elif library == "ruff":
        # Format code using a custom wrapper for Ruff (assumes string input/output)
        formatted_code = format_ruff_python(code)

    else:
        # Raise a ValueError for unrecognized formatter names
        raise ValueError(
            f"[PYTHON-CODE-FORMATTING] Unknown formatting library selected: {library}"
        )

    # Sort and format imports using isort with Black compatibility
    formatted_code = isort.code(formatted_code, config=isort.Config(profile="black"))

    return formatted_code


def __format_tag_with_attributes_on_separate_lines(
    tag: Union[bs4.Tag, str], indent: int = 0
) -> str:
    """Format a BeautifulSoup tag with each attribute on a separate line.

    Args:
        tag: The BeautifulSoup Tag to format or a string
        indent: The number of spaces to indent the tag

    Returns:
        A formatted HTML string with attributes on separate lines
    """
    if not isinstance(tag, bs4.Tag):
        return str(tag).strip()

    # Initial tag opening
    tag_name: str = tag.name
    indent_str: str = " " * indent

    if not tag.attrs:
        # Simple case - no attributes
        opening: str = f"{indent_str}<{tag_name}>"
    else:
        # Complex case - attributes on separate lines
        opening: str = f"{indent_str}<{tag_name}"
        attr_indent: int = indent + len(tag_name) + 1  # +1 for the "<"
        attr_indent_str: str = " " * attr_indent

        # Add each attribute on a new line
        for attr, value in tag.attrs.items():
            if isinstance(value, list):
                # Handle list attributes like class
                value = " ".join(value)
            elif value is True:
                # Handle boolean attributes
                opening += f"\n{attr_indent_str}{attr}"
                continue

            opening += f'\n{attr_indent_str}{attr}="{value}"'

        opening += ">"

    # If no children, return self-closing tag or simple content
    if not tag.contents:
        if tag.name in ["br", "hr", "img", "input", "meta", "link"]:
            return opening[:-1] + " />"
        return opening + f"</{tag_name}>"

    # For tags with children
    result: str = opening

    # Check if content is just text
    if len(tag.contents) == 1 and isinstance(tag.contents[0], bs4.NavigableString):
        return opening + tag.contents[0].strip() + f"</{tag_name}>"

    # Handle mixed content (tags, text, and comments)
    content_parts: List[str] = []
    for child in tag.contents:
        if isinstance(child, bs4.Tag):
            content_parts.append(
                "\n" + __format_tag_with_attributes_on_separate_lines(child, indent + 2)
            )
        elif isinstance(child, bs4.Comment):
            content_parts.append(f"\n{indent_str}  <!-- {child.strip()} -->")
        elif isinstance(child, bs4.NavigableString) and child.strip():
            content_parts.append(child.strip())

    result += "".join(content_parts)
    result += f"\n{indent_str}</{tag_name}>"
    return result


def custom_format_html_document_beautifulsoup(
    html: str, preserve_doctype: bool = True
) -> str:
    """Format an entire HTML document with attributes on separate lines.

    Args:
        html: HTML string to format
        preserve_doctype: Whether to preserve the DOCTYPE declaration

    Returns:
        A formatted HTML string with attributes on separate lines for all tags
    """
    soup: bs4.BeautifulSoup = bs4.BeautifulSoup(html, "html.parser")

    result: str = ""

    # Preserve DOCTYPE if requested
    if preserve_doctype and "<!DOCTYPE" in html:
        doctype: str = "<!DOCTYPE html>"
        result += doctype + "\n"

    # Format the entire document
    if soup.html:
        result += __format_tag_with_attributes_on_separate_lines(soup.html)
    else:
        # If there's no html tag, format all top-level elements
        for element in soup.contents:
            if isinstance(element, bs4.Tag):
                result += __format_tag_with_attributes_on_separate_lines(element)
            elif isinstance(element, bs4.Comment):
                result += f"<!-- {element.strip()} -->\n"
            elif isinstance(element, bs4.NavigableString) and element.strip():
                result += element.strip()

    return result


"""
Ruff library functions
"""


class RuffCommand(enum.Enum):
    """
    Represents the available subcommands for the Ruff CLI.
    """

    CHECK = "check"
    RULE = "rule"
    CONFIG = "config"
    LINTER = "linter"
    CLEAN = "clean"
    FORMAT = "format"
    SERVER = "server"
    ANALYZE = "analyze"
    VERSION = "version"
    HELP = "help"

    def __str__(self):
        return self.value


def run_ruff_on_code_snippet(
    code: str,
    ruff_subcommand: RuffCommand,
    ruff_args: Optional[List[str]] = None,
    # New argument to indicate if the command modifies the file in place
    modifies_file_in_place: bool = False,
) -> Tuple[int, str, str]:
    """
    Runs a specified Ruff command on a given Python code string,
    using a temporary file.

    Args:
        code: The Python code as a string to be processed by Ruff.
        ruff_subcommand: The specific Ruff subcommand to run (e.g., RuffCommand.CHECK).
        ruff_args: An optional list of additional arguments to pass to the Ruff subcommand.
        modifies_file_in_place: If True, the function will read the modified content
                                from the temporary file after the command executes.
                                Otherwise, it returns Ruff's stdout.

    Returns:
        A tuple containing:
        - int: The exit code of the Ruff process (0 for success, non-zero for error or violations).
        - str: The standard output from the Ruff process (or modified file content if `modifies_file_in_place` is True).
        - str: The standard error from the Ruff process.

    Raises:
        RuntimeError: If the Ruff executable is not found or other non-command-specific
                      subprocess errors occur.
    """
    if ruff_args is None:
        ruff_args = []

    spec = importlib.util.find_spec("ruff")
    if spec is None:
        raise RuntimeError(f"Ruff is not installed!")

    # Determine creationflags for Windows to prevent console window pop-up
    creation_flags = 0
    if sys.platform == "win32":
        creation_flags = subprocess.CREATE_NO_WINDOW

    with tempfile.TemporaryDirectory() as tmpdir:
        file_path: pathlib.Path = pathlib.Path(tmpdir) / "temp_ruff_code.py"
        file_path.write_text(code, encoding="utf-8")

        command: List[str] = [
            "python",
            "-m",
            "ruff",
            str(ruff_subcommand),
            str(file_path),
        ] + ruff_args

        try:
            result: subprocess.CompletedProcess[str] = subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=False,
                creationflags=creation_flags,  # Added for Windows console suppression
            )

            # If the command modifies the file in place, read the updated content
            stdout_output = result.stdout
            if modifies_file_in_place:
                try:
                    stdout_output = file_path.read_text(encoding="utf-8")
                except Exception as e:
                    # Log or handle error if file read fails after command
                    print(f"Warning: Could not read modified file content: {e}")
                    stdout_output = ""  # Return empty or original code as fallback

            return result.returncode, stdout_output, result.stderr
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred while running Ruff: {e}")


def run_ruff_command(
    ruff_subcommand: RuffCommand, ruff_args: Optional[List[str]] = None
) -> Tuple[int, str, str]:
    """
    Runs a specified generic Ruff command (e.g., version, rule, config).

    Args:
        ruff_subcommand: The specific Ruff subcommand to run (e.g., RuffCommand.VERSION).
        ruff_args: An optional list of additional arguments for the subcommand.

    Returns:
        A tuple containing:
        - int: The exit code of the Ruff process (0 for success, non-zero for error).
        - str: The standard output from the Ruff process.
        - str: The standard error from the Ruff process.

    Raises:
        RuntimeError: If the Ruff executable is not found or other non-command-specific
                      subprocess errors occur.
    """
    if ruff_args is None:
        ruff_args = []

    spec = importlib.util.find_spec("ruff")
    if spec is None:
        raise RuntimeError(f"Ruff is not installed!")

    # Determine creationflags for Windows to prevent console window pop-up
    creation_flags = 0
    if sys.platform == "win32":
        creation_flags = subprocess.CREATE_NO_WINDOW

    command: List[str] = ["python", "-m", "ruff", str(ruff_subcommand)] + ruff_args

    try:
        result: subprocess.CompletedProcess[str] = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
            creationflags=creation_flags,  # Added for Windows console suppression
        )
        return result.returncode, result.stdout, result.stderr
    except FileNotFoundError:
        raise RuntimeError(
            "Ruff executable not found. Make sure Ruff is installed and accessible in your PATH."
        )
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred while running Ruff:\n  {e}")


def format_ruff_python(code: str) -> str:
    """
    Formats Python code using Ruff's 'format' command.

    Args:
        code: The input Python code as a string.

    Returns:
        The formatted Python code as a string.

    Raises:
        RuntimeError: If 'ruff format' command returns a non-zero exit code,
                      indicating an error during formatting (e.g., syntax error).
    """
    exit_code, formatted_code_output, stderr = run_ruff_on_code_snippet(
        code=code,
        ruff_subcommand=RuffCommand.FORMAT,
        modifies_file_in_place=True,  # Ruff format modifies the file directly
    )

    if exit_code != 0:
        error_message = stderr.strip() if stderr else "Unknown Ruff formatting error."
        raise RuntimeError(
            f"Ruff formatting failed with exit code {exit_code}:\n{error_message}"
        )
    return formatted_code_output  # This now contains the modified file content


def analyze_ruff_file(
    file_path: Union[str, pathlib.Path], ruff_args: Optional[List[str]] = None
) -> Tuple[int, str]:
    """
    Lints a Python file using Ruff's 'check' command.

    Args:
        file_path: The path to the Python file to lint. Can be a string or pathlib.Path.
        ruff_args: Optional list of additional arguments for the 'ruff check' command.

    Returns:
        A tuple: (exit_code, lint_output_str).
        exit_code 0 means no linting violations found.
        exit_code 1 means violations found.

    Raises:
        ValueError: If the provided file_path does not exist.
    """
    if not isinstance(file_path, pathlib.Path):
        file_path = pathlib.Path(file_path)

    if not file_path.exists():
        raise ValueError(f"File not found: {file_path}")
    if not file_path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    # For linting a file, the `ruff_args` will be passed *after* the file path.
    # So, we append the file path to the list of arguments.
    full_ruff_args = [str(file_path)]
    if ruff_args:
        full_ruff_args.extend(ruff_args)

    # Now, call the generic run_ruff_command
    exit_code, stdout, stderr = run_ruff_command(
        ruff_subcommand=RuffCommand.CHECK, ruff_args=full_ruff_args
    )

    # For 'check', stdout contains the linting results. Stderr is usually for errors.
    if exit_code != 0 and stdout:
        return exit_code, stdout.strip()
    elif exit_code != 0 and stderr:
        # If there's an error and output is on stderr, pass that.
        return exit_code, stderr.strip()
    return exit_code, stdout.strip()  # Or empty string if no violations


def analyze_pyflakes_file(
    file_path: Union[str, pathlib.Path], pyflakes_args: Optional[List[str]] = None
) -> Tuple[int, str, str]:
    """
    Analyzes a Python file using the 'pyflakes' command-line tool.

    Args:
        file_path: The path to the Python file to analyze. Can be a string or pathlib.Path.
        pyflakes_args: An optional list of additional arguments to pass to the 'pyflakes' command.

    Returns:
        A tuple containing:
        - int: The exit code of the 'pyflakes' process (0 for no issues, non-zero if issues are found).
        - str: The standard output from the 'pyflakes' process (contains analysis findings).
        - str: The standard error from the 'pyflakes' process (for process errors).

    Raises:
        FileNotFoundError: If the 'pyflakes' executable is not found in the system's PATH.
        ValueError: If the provided file_path does not exist or is not a file.
        subprocess.CalledProcessError: If the 'pyflakes' command itself fails (e.g., due to internal errors).
        Exception: For any other unexpected errors during subprocess execution.
    """
    if pyflakes_args is None:
        pyflakes_args = []

    spec = importlib.util.find_spec("pyflakes")
    if spec is None:
        raise RuntimeError(f"Pyflakes is not installed!")

    if not isinstance(file_path, pathlib.Path):
        file_path = pathlib.Path(file_path)

    if not file_path.exists():
        raise ValueError(f"File not found: {file_path}")
    if not file_path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    # Determine creationflags for Windows to prevent console window pop-up
    # This flag has no effect on non-Windows platforms.
    creation_flags = 0
    if sys.platform == "win32":
        creation_flags = subprocess.CREATE_NO_WINDOW

    try:
        command: List[str] = [
            "python",
            "-m",
            "pyflakes",
            str(file_path),
        ] + pyflakes_args

        result: subprocess.CompletedProcess[str] = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            encoding="utf-8",
            creationflags=creation_flags,  # <-- Added this line
        )

        return result.returncode, result.stdout.strip(), result.stderr.strip()

    except FileNotFoundError:
        raise FileNotFoundError(
            "The 'pyflakes' executable was not found. "
            "Please ensure pyflakes is installed and 'pyflakes' is in your system's PATH."
        )
    except Exception as e:
        raise Exception(
            f"An unexpected error occurred while running pyflakes on file '{file_path}': {e}"
        )
