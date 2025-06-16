"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.

FILE DESCRIPTION:
    Module that holds functions for various uses
    that uses any library that is needed.
"""

import os

import fpdf

import data
import functions


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
