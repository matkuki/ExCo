#!/usr/bin/python3

# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2016 Matic Kukovec. 
Release under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""


##  FILE DESCRIPTION:
##      Execute this file to start Ex.Co.


import sys
import os
import argparse
import data
import forms

def parse_arguments():
    """Parse Ex.Co. command line arguments"""
    #Nested function for input file parsing
    def parse_file_list(files_string):
        return files_string.split(";")
    #Initialize the argument parser
    arg_parser = argparse.ArgumentParser()
    #Version number
    arg_parser.add_argument(
        "-v", 
        "--version", 
        action  = "version",
        version = "Ex.Co. Version: {:s}".format(data.APPLICATION_VERSION)
    )
    #Debug mode
    arg_parser.add_argument(
        "-d", 
        "--debug", 
        action  = "store_true",
        default = False, 
        dest    = "debug_mode",
        help    = 'Enable debug mode. Not used anymore.'
    )
    #Logging mode
    arg_parser.add_argument(
        "-l", 
        "--logging", 
        action  = "store_true",
        default = False, 
        dest    = "logging_mode",
        help    = 'Show the logging window on startup.'
    )
    #Logging mode
    arg_parser.add_argument(
        "-n", 
        "--new", 
        action  = "store_true",
        default = False, 
        dest    = "new_document",
        help    = """
                  Create a new document in the main window on startup.
                  This flag can be overriden with the --files flag.
                  """
    )
    #Add a file group to the argument parser
    file_group = arg_parser.add_argument_group(
        "input file options"
    )
    #Input files
    file_group.add_argument(
        "-f", 
        "--files", 
        type    = parse_file_list,
        help    =   """
                    List of files to open on startup, separated
                    by semicolons (';'). This flag overrides the --new flag.
                    """
    )
    #Single file argument
    help_string = 'Single file passed as an argument, '
    help_string += 'Used for openning files with a desktops "Open with..." functionality'
    file_group.add_argument(
        "single_file", 
        action  = "store",
        nargs   = "?", 
        default = None, 
        help    = help_string
    )
    parsed_options = arg_parser.parse_args()
    return parsed_options

def main():
    """Main function of Ex.Co."""
    #Check arguments
    options = parse_arguments()
    if options.debug_mode == True:
        data.debug_mode = True
    if options.logging_mode == True:
        data.logging_mode = True
    file_arguments = options.files
    if options.single_file != None:
        if file_arguments != None:
            file_list = file_arguments.split(";")
            file_list.append(options.single_file)
            file_arguments = ";".join(file_list)
        else:
            file_arguments = [options.single_file]
    #Get the application directory
    data.application_directory = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
    #Check if Ex.Co. is run as a cxfreeze executable (the path will contain library.zip)
    if "library.zip" in data.application_directory:
        data.application_directory = data.application_directory.replace("library.zip", "")
    #Set the resources directory
    data.resources_directory = os.path.join(data.application_directory,  "resources")
    #Combine the application path with the Ex.Co. icon file name (the icon file name is set in the global module)
    data.application_icon = os.path.join(
        data.resources_directory,
        data.application_icon
    )
    #Combine the application path with the Ex.Co. information file name (the information file name is set in the global module)
    data.about_image = os.path.join(
        data.resources_directory,
        data.about_image
    )
    #Create QT application, needed to use QT forms
    app = data.QApplication(sys.argv)
    #Save the Qt application to the global reference
    data.application = app
    #Create the main window, pass the filename that may have been passed as an argument
    wnd = forms.MainWindow(
        new_document = options.new_document, 
        logging=data.logging_mode, 
        file_arguments=file_arguments
    )
    wnd.show()
    sys.exit(app.exec_())
    
#Check if this is the main executing script
if __name__ == '__main__':
    main()
