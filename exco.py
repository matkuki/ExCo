#!/usr/bin/python3

# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2023 Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""


##  FILE DESCRIPTION:
##      Execute this file to start Ex.Co.


import sys
import os
import argparse
import data
import components.fonts
import components.signaldispatcher
import components.processcontroller
import components.communicator
import components.thesquid
import gui.mainwindow
import settings


def parse_arguments():
    """
    Parse Ex.Co. command line arguments
    """
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
        version = "Ex.Co. Version: {:s}".format(data.application_version)
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
    """
    Main function of Ex.Co.
    """
    # Check arguments
    options = parse_arguments()
    if options.debug_mode == True:
        data.debug_mode = True
    if options.logging_mode == True:
        data.logging_mode = True
    file_arguments = options.files
    if options.single_file is not None:
        if file_arguments is not None:
            file_list = file_arguments.split(";")
            file_list.append(options.single_file)
            file_arguments = ";".join(file_list)
        else:
            file_arguments = [options.single_file]
    if file_arguments == ['']:
        file_arguments = None
    
    # Create QT application, needed to use QT forms
    app = data.QApplication(sys.argv)
    # Save the Qt application to the global reference
    data.application = app
    
    # Process control
    number_of_instances = components.processcontroller.check_opened_excos()
    if settings.variables["open-new-files-in-open-instance"]:
        if number_of_instances > 1 and file_arguments is not None:
            try:
                _data = {"command": "open", "arguments": file_arguments}
#                components.processcontroller.send_raw_command(_data)
                fc = components.communicator.FileCommunicator("OPEN-IN-EXISTING-INSTANCE")
                fc.send_data(_data)
                return
            except:
                pass
        elif number_of_instances > 1:
            try:
                _data = {"command": "show", "arguments": None}
                fc = components.communicator.FileCommunicator("SHOW-OPEN-INSTANCE")
                fc.send_data(_data)
                return
            except:
                pass
    
    # Set default application font
    components.fonts.set_application_font(
        data.current_font_name,
        data.current_font_size,
    )
    
    # Global signal dispatcher
    data.signal_dispatcher = components.signaldispatcher.GlobalSignalDispatcher()
    
    # Create the main window, pass the filename that may have been passed as an argument
    main_window = gui.mainwindow.MainWindow(
        new_document = options.new_document, 
        logging=data.logging_mode, 
        file_arguments=file_arguments
    )
    components.thesquid.TheSquid.init_objects(main_window)
    main_window.import_user_functions()
    main_window.show()
    sys.exit(app.exec())
    
# Check if this is the main executing script
if __name__ == '__main__':
    main()
elif '__main__' in __name__:
    # cx_freeze mangles the __name__ variable,
    # but it still contains '__main__'
    main()
