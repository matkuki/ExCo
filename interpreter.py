
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
##      Python Interactive Interpreter (Read-Eval-Print-Loop) functionality

import os
import sys
import code
import re
import subprocess
import threading
import platform
import traceback
import data


class CustomInterpreter(code.InteractiveInterpreter):
    """SubClassed InteractiveInterpreter object"""
    #Class variables (class variables >> this means that these variables are shared accross instances of this class)
    #Modules that will be used by default by the interactive interpreter
    modules =   [
        "sys", 
        "os", 
        "os.path", 
        "re", 
        "subprocess",
        "threading", 
        "functools", 
        "itertools", 
        "inspect", 
        "collections", 
        "PyQt4.QtCore", 
        "PyQt4.QtGui", 
        "PyQt4.Qsci", 
        "global_module", 
    ]
    #Not None if an exception occurs during the eval_command function
    eval_error      = None
    #Dictionary of constants
    dict_const_references = dict(
        OK          = data.FileStatus.OK, 
        MODIFIED    = data.FileStatus.MODIFIED, 
        FOUND       = data.SearchResult.FOUND, 
        NOT_FOUND   = data.SearchResult.NOT_FOUND, 
        CYCLED      = data.SearchResult.CYCLED, 
        ONE         = data.WindowMode.ONE, 
        THREE       = data.WindowMode.THREE, 
        LEFT        = data.MainWindowSide.LEFT, 
        RIGHT       = data.MainWindowSide.RIGHT, 
    )
    #The escape sequence for built in functions
    re_escape_sequence = "lit#"
    #Dictionary of regular expression sequences for replacing internal keywords with python objects,
    #mostly done for my personal desire to learn and play with regular expressions
    dict_re_references = dict(
        quit                        = (r"^quit$" , r"quit()"),
        exit                        = (r"^exit$", r"exit()"),
        bye                         = (r"^bye\(\)$|^bye$", r"exit()"),
        spin_r                      = (r"^spin_r\(\)$|^spin_r$", r"form.view.spin_basic_widgets()"), 
        spin_l                      = (r"^spin_l\(\)$|^spin_l$", r"form.view.spin_basic_widgets(1)"),       
        clear_repl_tab              = (r"^clear_repl_tab$", r"clear_repl_tab()"), 
        new                         = (r"^new$", r"new()"),
        set_all_text                = (
            r"(?<!\.)(?<!{:s})set_all_text".format(re_escape_sequence), 
            r"main.currentWidget().set_all_text"
        ), 
        get_lines                   = (
            r"(?<!\.)(?<!{:s})get_lines".format(re_escape_sequence), 
            r"main.currentWidget().get_lines",
        ), 
        line_list                   = (
            r"(?<!\.)(?<!{:s})line_list".format(re_escape_sequence), 
            r"main.currentWidget().line_list"
        ), 
        line_count                  = (
            r"(?<!\.)(?<!{:s})line_count".format(re_escape_sequence), 
            r"main.currentWidget().line_count"
        ), 
        lines                       = (
            r"(?<![\.|_|\w|\"])(?<!{:s})lines\(\)|(?<![\.|_|\w|\"])(?<!{:s})lines".format(
                re_escape_sequence, 
                re_escape_sequence
            ), 
            r"main.currentWidget().lines()"
        ),
        find_and_highlight          = (
            r"(?<!\.)(?<!{:s})find_and_highlight.format(re_escape_sequence)", 
            r"main.currentWidget().find_and_highlight"
        ),
        clear_highlights            = (r"^clear_highlights$", r"clear_highlights()"),   
        undo                        = (r"^undo\(\)$|^undo$", r"main.currentWidget().undo()"),
        redo                        = (r"^redo\(\)$|^redo$", r"main.currentWidget().redo()"),
        terminal                    = (r"^terminal$", r"terminal()"),
        get_cwd                     = (r"^get_cwd\(\)$|^get_cwd$", r"get_cwd()"),
        set_cwd                     = (r"^set_cwd\(\)$|^set_cwd$", r"set_cwd()"),
        update_cwd                  = (r"^update_cwd\(\)$|^update_cwd$", r"update_cwd()"),
        toggle_main_window_side     = (r"^toggle_main_window_side$", r"toggle_main_window_side()"),
        append                      = (r"^append\(", r"cmain.append_to_lines("),
        append_all                  = (r"^append_all\((.*)\)", r"cmain.append_to_lines(\g<1>, 1,cmain.lines())"),
        prepend                     = (r"^prepend\(", r"cmain.prepend_to_lines("),
        prepend_all                 = (r"^prepend_all\((.*)\)", r"cmain.prepend_to_lines(\g<1>, 1,cmain.lines())"),
        close_tab                   = (r"^close_tab\(\)|^close_tab", r"main.close_tab()"),
        undo_all                    = (r"^undo_all\(\)$|^undo_all$", r"main.currentWidget().undo_all()"),
        redo_all                    = (r"^redo_all\(\)$|^redo_all$", r"main.currentWidget().redo_all()"),
        indent_with_tabs            = (r"^indent_with_tabs\(\)$|^indent_with_tabs$", r"main.currentWidget().indent_with_tabs(True)"),
        indent_with_spaces          = (r"^indent_with_spaces\(\)$|^indent_with_spaces$", r"main.currentWidget().indent_with_tabs()"),
        tabs_to_spaces              = (r"^tabs_to_spaces\(\)$|^tabs_to_spaces$", r"main.currentWidget().tabs_to_spaces()"),
        show_edge_marker            = (r"^show_edge_marker\(\)$|^show_edge_marker$", r"main.currentWidget().show_edge_marker()"),
        hide_edge_marker            = (r"^hide_edge_marker\(\)$|^hide_edge_marker$", r"main.currentWidget().hide_edge_marker()"),
        reload_file                 = (r"^reload_file|^reload_file\(\)", r"main.currentWidget().reload_file()"),
        show_node_tree              = (r"^show_node_tree|^show_node_tree\(\)", r"show_node_tree(main.currentWidget())"),
    )
    #Keywords that can appear anywhere in the REPL command and need to be replaced
    #The exco standard abbreviation for a function is a character/characters followed by a colon ":". E.G.: "p:('something')" is replaced by "print('something') "
    #"lit#" is an escape sequence for literal printing
    dict_keywords = dict(
        current_main    = (
            "cmain", 
            r"(?<!{:s})cmain\(\)|(?<!{:s})cmain".format(re_escape_sequence, re_escape_sequence), 
            r"main.currentWidget()"
        ),
        current_lower   = (
            "clower", 
            r"(?<!{:s})clower\(\)|(?<!{:s})clower".format(re_escape_sequence, re_escape_sequence), 
            r"lower.currentWidget()"
        ),
        current_upper   = (
            "cupper", 
            r"(?<!{:s})cupper\(\)|(?<!{:s})cupper".format(re_escape_sequence, re_escape_sequence), 
            r"upper.currentWidget()"
        ),
        print           = ("p:", r"^p:((.*)((?=\n)|(?=$)))", r"print(\g<1>)"),
        print_log       = ("pl:", r"^pl:((.*)((?=\n)|(?=$)))", r"print_log(\g<1>)"),
        run             = ("r: ", 
                           [(r"^(r:\s*)((?!\s*\")(.*))((?=\n)|(?=$))", r"run('\g<2>', show_console=False)"), 
                            (r"^r:(\s*)(\")(.*)(\")((?=\n)|(?=$))", r"run(\g<2>\g<3>\g<4>, show_console=False)")]),
        run_output      = ("rco: ", 
                           [(r"^(rco:\s*)((?!\s*\")(.*))((?=\n)|(?=$))", r"run('\g<2>', show_console=False, output_to_repl=True)"),
                            (r"^rco:(\s*)(\")(.*)(\")((?=\n)|(?=$))", r"run(\g<2>\g<3>\g<4>, show_console=False, output_to_repl=True)")]),
        run_console     = ("rc: ", 
                           [(r"^(rc:\s*)((?!\s*\")(.*))((?=\n)|(?=$))", r"run('\g<2>')"), 
                            (r"^rc:(\s*)(\")(.*)(\")((?=\n)|(?=$))", r"run(\g<2>\g<3>\g<4>)")]),
    #The (?=...) regex operator means "stop matching if you get to ..., but ... has to be in the string"
    #The "((.*)(?=\)))" has to be the last expression if using "s:" in a function like "print()" because it captures anything until the closing parenthesis
    )
    """
    Example of replacing a function name with a new function name:
        import re
        a = "old(test)"
        a = re.sub(r"(old)(\(.*\))", r"new\g<2>", a)
        print(a_new) >>> "new(test)"
    """
    
    
    def __init__(self,  initial_references, repl_print):
        """Initialize the interactive interpreter"""
        #Get the default references and add them to the initial_references list
        initial_references.update(self.get_default_references())
        """
        Initialize parent, from which the current class is inherited, 
        THIS MUST BE DONE SO THAT THE SUPERCLASS EXECUTES ITS __init__ !!!!!!
        """
        #the InteractiveInterpreter object takes references as the first argument
        super().__init__(initial_references)
        #Import all the default modules
        for mod in self.modules:
            self.eval_command("import " + mod)
        #Save the REPL print function as a reference
        self.repl_print = repl_print
    
    def eval_command(self, command):
        """
        This EVAL function executes the command by the interactive interpreter.
        (inputted by the REPL ReplLineEdit and pressing enter)
        """
        try:
            #Reset the error message
            self.eval_error = None
            #Replace certain strings with methods
            filtered_command = self.replace_references(self.dict_re_references, command)
            filtered_command = self.replace_keywords(self.dict_keywords, filtered_command)
            #Remove the literal sequences from the command
            filtered_command = filtered_command.replace(self.re_escape_sequence, "")
            data.print_log("------------------")
            data.print_log(">>> " + command)
            data.print_log(">> " + filtered_command)
            #Execute the filtered command string with the custom InteractiveInterpreter
            #First try to evaluate the command string, to see if it's an expression
            try:
                #Try to EVALUATE the command
                data.print_log("Trying to EVALUATE the command.")
                eval_return = eval(filtered_command, self.locals)
                self.repl_print(eval_return)
                data.print_log(eval_return)
                data.print_log("Evaluation succeeded!")
                return None
            except:
                #EXECUTE
                self.eval_error = None
                data.print_log("Evaluation failed! EXECUTING the command.")
                #Execute and return the error message
                return self._custom_runcode(filtered_command)
        except Exception as ex:
            data.print_log("!! Cannot run code: \"" + str(command) + "\"")
            data.print_log(str(ex))
            return "REPL evaluation error!"
    
    def _custom_runcode(self, code):
        """
        Custom runcode method
        NOTES:
            This function had to be added for GNU/Linux as of Python3.4,
            because Python3.4's showtraceback function differs the 'write' function
            if the sys.excepthook is not set.
        """
        try:
            exec(code, self.locals)
        except SystemExit:
            raise
        except:
            return self._custom_showtraceback()
    
    def _custom_showtraceback(self):
        """
        Custom showtraceback function
            NOTES:
                This function had to be added for GNU/Linux as of Python3.4,
                because Python3.4's showtraceback function differs the 'write' function
                if the sys.excepthook is not set.
        """
        try:
            type, value, tb = sys.exc_info()
            sys.last_type = type
            sys.last_value = value
            sys.last_traceback = tb
            tblist = traceback.extract_tb(tb)
            del tblist[:1]
            lines = traceback.format_list(tblist)
            if lines:
                lines.insert(0, "Traceback (most recent call last):\n")
            lines.extend(traceback.format_exception_only(type, value))
        finally:
            tblist = tb = None
            return ''.join(lines)

    def replace_references(self, references, command):
        """Replace references with actual forms module methods and attributes"""
        for key in references:
            #Replace keyword with actual function from the forms module MainWindow class
            command = re.sub(references[key][0],  references[key][1],  command)
        return command
    
    def replace_keywords(self, keywords, command):
        """Replace keywords with actual forms module methods and attributes"""
        for key in keywords:
            #Replace keyword with actual function from the forms module MainWindow class
            if isinstance(keywords[key][1], str):
                #Do a normal RE replace
                command = re.sub(keywords[key][1],  keywords[key][2],  command)
            else:
                #Cycle through list and replace
                for sub in keywords[key][1]:
                    search_exp = sub[0]
                    replace_exp = sub[1]
                    command = re.sub(search_exp,  replace_exp,  command)
        return command
        
    def update_locals(self, new_locals):
        """Add new locals to the existing ones"""
        for new_local in new_locals:
            #Check if the local is already in the current list of locals
            if new_local not in self.locals:
                #Update the locals dictionary with the new item
                self.locals.update({new_local:new_locals[new_local]})
    
    def reset_locals(self):
        """Clear all custom interpreter references in the locals dictionary"""
        self.locals = {}
    
    def run_cmd_process(self, command, show_console=True, output_to_repl=False):
        """Function for running a command line process and return the result"""
        #Check what is the current OS
        if platform.system() == "Windows":
            #Remove the PYTHONHOME environment variable that Nuitka creates. It causes problems
            #when running the system's python interpreter!
            os.environ['PYTHONHOME'] = ''
            if show_console == True:
                #Double quotes have to be handled differently on Windows (don't know about Linux yet)
                if '\"' in command:
                    process_commands = [
                        "command = 'cmd.exe /c {:s} & pause'".format(command), 
                        "subprocess.Popen(command)"
                    ]
                else:
                    process_commands = ["subprocess.Popen(['cmd.exe', '/c', '" + command + " & pause'])"]
            else:
                if output_to_repl == True:
                    options = 'startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.STDOUT'
                    #Double quotes have to be handled differently on Windows (don't know about Linux yet)
                    if '\"' in command:
                        sub_call = 'subprocess.Popen(\'cmd.exe /c {:s}\', {:s})'.format(command, options)
                    else:
                        sub_call = 'subprocess.Popen(["cmd.exe", "/c", "{:s}"], {:s})'.format(command, options)
                    process_commands = ['startupinfo = subprocess.STARTUPINFO()', 
                                        'startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW',
                                        'result = ' + sub_call, 
                                        '(output, err) = result.communicate()',
                                        'print(output)']
                else:
                    options     = 'startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.STDOUT'
                    #Double quotes have to be handled differently on Windows (don't know about Linux yet)
                    if '\"' in command:
                        sub_call = 'subprocess.Popen(\'cmd.exe /c {:s}\', {:s})'.format(command, options)
                    else:
                        sub_call = 'subprocess.Popen(["cmd.exe", "/c", "{:s}"], {:s})'.format(command, options)
                    """
                    'THE THIRD LINE HAS TO CONTAIN MORE THAN JUST sub_call! Otherwise the python
                    interpreter crashes! Don't know why yet.
                    """
                    process_commands = ['startupinfo = subprocess.STARTUPINFO()', 
                                        'startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW',
                                        'try:\n  {:s}\nexcept Exception as ex:\n  print(ex)'.format(sub_call)]
                #Create a function that will evaluate commands in the new thread
                def threaded_function(commands):
                    #Run the commands sequentially and check the result
                    for command in commands:
                        result = self.eval_command(command)
                        if result != None:
                            return
                #Start the new thread
                thread = threading.Thread(target=threaded_function, args=(process_commands, ))
                thread.start()
                return
        else:
            #GNU/Linux (Lubuntu tested)
            if show_console == True:
                #Uses XTerm terminal emulator by default
                end_delimiter_string = "-------------------------"
                end_message_string = "\'Press any key to continue\'"
                process_commands = [
                    """subprocess.Popen(
                            ["{:s}","-e","{:s};echo {:s};read -p {:s}"]
                       )""".format(
                                data.terminal, 
                                command, 
                                end_delimiter_string, 
                                end_message_string
                            )
                ]
            else:
                if output_to_repl == True:
                    options     = 'stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True'
                    sub_call    = 'subprocess.Popen("{:s}", {:s})'.format(command, options)
                    process_commands =  ['result = ' + sub_call,
                                         '(output, err) = result.communicate()',
                                         'print(output)']
                else:
                    options     = 'stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False'
                    sub_call    = 'subprocess.Popen("{:s}", {:s})'.format(command, options)
                    process_commands =  ['result = ' + sub_call,
                                         '(output, err) = result.communicate()']
        #Run the commands sequentially and check the result
        for cmd in process_commands:
            result = self.eval_command(cmd)
            if result != None:
                return
    
    def create_terminal(self, dir=None):
        """Spawn a new "terminal/command line" window asynchronously (currently works only on win32)"""
        #Change current working directory if it was supplied as an argument
        if dir != None:
            try:
                os.chdir(dir)
            except:
                #Return an evaluation error if exception occured (it's horribly side-effect-y but simple)
                self.eval_error = "Invalid directory supplied to \"terminal()\""
        #Check OS and spawn a terminal accordingly
        if platform.system() == "Windows":
            #Remove the PYTHONHOME environment variable that Nuitka creates. It causes problems
            #when running the systems python interpreter!
            os.environ['PYTHONHOME'] = ''
            subprocess.Popen("cmd.exe")
        else:
            #GNU/Linux (Lubuntu tested)
            subprocess.Popen([data.terminal])
    
    def get_default_references(self):
        """Return the references that will be available in for execution"""
        #Create the initial references dictionary
        reference_list = dict(
            interpreter_run = self.run_cmd_process, 
            terminal        = self.create_terminal, 
        )
        #Extend the dictionary with the constants dictionary
        reference_list.update(self.dict_const_references)
        return reference_list
