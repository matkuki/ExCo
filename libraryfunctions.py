"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

##  FILE DESCRIPTION:
##      Module that holds functions for various uses
##      that uses any library that is needed.

# Standard library
import os
import platform
from typing import *

# Local
import data
import functions

# External
import black
import autopep8
import yapf
import fpdf
import bs4
import isort


def create_pdf_from_text(output_pdf_path, text):
    # Create instance of FPDF class
    pdf = fpdf.FPDF()

    # Add a page
    pdf.add_page()

    # Add the font
    font_file_path = functions.unixify_join(
        data.fonts_directory, "SourceCodePro/SourceCodePro-Regular.ttf"
    )
    pdf.add_font("Source Code Pro", fname=font_file_path, uni=True)
    # Set font
    font_size = data.current_editor_font_size
    line_height = font_size / 2
    pdf.set_font(data.current_editor_font_name, size=font_size)

    # Add multi-cell to handle line wrapping
    pdf.multi_cell(0, line_height, text=text)

    # Save the PDF to the given output path
    pdf.output(output_pdf_path)


def open_pdf(path_to_pdf):
    if data.platform == "Windows":
        os.startfile(path_to_pdf)  # Windows-specific
    elif data.platform == "Darwin":
        os.system(f"open {path_to_pdf}")  # macOS-specific
    else:
        os.system(f"xdg-open {path_to_pdf}")  # Linux-specific


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
        formatted_code = functions.format_ruff_python(code)

    else:
        # Raise a ValueError for unrecognized formatter names
        raise ValueError(
            f"[PYTHON-CODE-FORMATTING] Unknown formatting library selected: {library}"
        )

    # Sort and format imports using isort with Black compatibility
    formatted_code = isort.code(
        formatted_code, config=isort.Config(profile="black")
    )

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
