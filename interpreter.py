"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

##  FILE DESCRIPTION:
##      Python Interactive Interpreter (Read-Eval-Print-Loop) functionality

import code
import os
import re
import subprocess
import sys
import threading
import traceback

import data
import hy

import constants


class CustomInterpreter(code.InteractiveInterpreter):
    """
    SubClassed InteractiveInterpreter object
    """

    # Class variables (class variables >> this means that these variables are shared accross instances of this class)
    # Modules that will be used by default by the interactive interpreter
    modules = [
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
    # Not None if an exception occurs during the eval_command function
    eval_error = None
    # Dictionary of constants
    dict_const_references = dict(
        OK=constants.FileStatus.OK,
        MODIFIED=constants.FileStatus.MODIFIED,
        FOUND=constants.SearchResult.FOUND,
        NOT_FOUND=constants.SearchResult.NOT_FOUND,
        CYCLED=constants.SearchResult.CYCLED,
        ONE=constants.WindowMode.ONE,
        THREE=constants.WindowMode.THREE,
        LEFT=constants.MainWindowSide.LEFT,
        RIGHT=constants.MainWindowSide.RIGHT,
    )
    # The escape sequence for built in functions
    re_escape_sequence = "lit#"
    # Dictionary of regular expression sequences for replacing internal keywords with python objects,
    # mostly done for my personal desire to learn and play with regular expressions
    dict_re_references = dict(
        quit=(r"^quit$", r"quit()"),
        exit=(r"^exit$", r"exit()"),
        bye=(r"^bye\(\)$|^bye$", r"exit()"),
        clear_repl_tab=(r"^clear_repl_tab$", r"clear_repl_tab()"),
        new=(r"^new$", r"new()"),
        set_all_text=(
            r"(?<!\.)(?<!{:s})set_all_text".format(re_escape_sequence),
            r"form.get_tab_by_indication().set_all_text",
        ),
        get_lines=(
            r"(?<!\.)(?<!{:s})get_lines".format(re_escape_sequence),
            r"form.get_tab_by_indication().get_lines",
        ),
        line_list=(
            r"(?<!\.)(?<!{:s})line_list".format(re_escape_sequence),
            r"form.get_tab_by_indication().line_list",
        ),
        line_count=(
            r"(?<!\.)(?<!{:s})line_count".format(re_escape_sequence),
            r"form.get_tab_by_indication().line_count",
        ),
        lines=(
            r"(?<![\.|_|\w|\"])(?<!{:s})lines\(\)|(?<![\.|_|\w|\"])(?<!{:s})lines".format(
                re_escape_sequence, re_escape_sequence
            ),
            r"form.get_tab_by_indication().lines()",
        ),
        find_and_highlight=(
            r"(?<!\.)(?<!{:s})find_and_highlight.format(re_escape_sequence)",
            r"form.get_tab_by_indication().find_and_highlight",
        ),
        clear_highlights=(r"^clear_highlights$", r"clear_highlights()"),
        undo=(r"^undo\(\)$|^undo$", r"form.get_tab_by_indication().undo()"),
        redo=(r"^redo\(\)$|^redo$", r"form.get_tab_by_indication().redo()"),
        terminal=(r"^show_terminal$", r"show_terminal()"),
        get_cwd=(r"^get_cwd\(\)$|^get_cwd$", r"get_cwd()"),
        set_cwd=(r"^set_cwd\(\)$|^set_cwd$", r"set_cwd()"),
        update_cwd=(r"^update_cwd\(\)$|^update_cwd$", r"update_cwd()"),
        open_cwd=(r"^open_cwd\(\)$|^open_cwd$", r"open_cwd()"),
        append=(r"^append\(", r"form.get_tab_by_indication().append_to_lines("),
        append_all=(
            r"^append_all\((.*)\)",
            r"form.get_tab_by_indication().append_to_lines(\g<1>, 1,form.get_tab_by_indication().lines())",
        ),
        prepend=(r"^prepend\(", r"form.get_tab_by_indication().prepend_to_lines("),
        prepend_all=(
            r"^prepend_all\((.*)\)",
            r"form.get_tab_by_indication().prepend_to_lines(\g<1>, 1,form.get_tab_by_indication().lines())",
        ),
        close_tab=(
            r"^close_tab\(\)|^close_tab",
            r"form.get_window_by_indication().close_tab()",
        ),
        undo_all=(
            r"^undo_all\(\)$|^undo_all$",
            r"form.get_tab_by_indication().undo_all()",
        ),
        redo_all=(
            r"^redo_all\(\)$|^redo_all$",
            r"form.get_tab_by_indication().redo_all()",
        ),
        indent_with_tabs=(
            r"^indent_with_tabs\(\)$|^indent_with_tabs$",
            r"form.get_tab_by_indication().indent_with_tabs(True)",
        ),
        indent_with_spaces=(
            r"^indent_with_spaces\(\)$|^indent_with_spaces$",
            r"form.get_tab_by_indication().indent_with_tabs()",
        ),
        tabs_to_spaces=(
            r"^tabs_to_spaces\(\)$|^tabs_to_spaces$",
            r"form.get_tab_by_indication().tabs_to_spaces()",
        ),
        show_edge_marker=(
            r"^show_edge_marker\(\)$|^show_edge_marker$",
            r"form.get_tab_by_indication().show_edge_marker()",
        ),
        hide_edge_marker=(
            r"^hide_edge_marker\(\)$|^hide_edge_marker$",
            r"form.get_tab_by_indication().hide_edge_marker()",
        ),
        reload_file=(
            r"^reload_file|^reload_file\(\)",
            r"form.get_tab_by_indication().reload_file()",
        ),
        show_node_tree=(
            r"^show_node_tree|^show_node_tree\(\)",
            r"show_node_tree(form.get_tab_by_indication())",
        ),
        for_each_line=(
            r"(?<!\.)(?<!{:s})for_each_line\(".format(re_escape_sequence),
            r"form.get_tab_by_indication().for_each_line(",
        ),
        remove_empty_lines=(
            r"(?<!\.)(?<!{:s})remove_empty_lines\(".format(re_escape_sequence),
            r"form.get_tab_by_indication().remove_empty_lines(",
        ),
    )
    # Keywords that can appear anywhere in the REPL command and need to be replaced
    # The exco standard abbreviation for a function is a character/characters followed by a colon ":". E.G.: "p:('something')" is replaced by "print('something') "
    # "lit#" is an escape sequence for literal printing
    dict_keywords = dict(
        echo=("p:", r"^p:((.*)((?=\n)|(?=$)))", r"echo(\g<1>)"),
        run=(
            "r: ",
            [
                (
                    r"^(r:\s*)((?!\s*\")(.*))((?=\n)|(?=$))",
                    r"run('\g<2>', show_console=False)",
                ),
                (
                    r"^r:(\s*)(\")(.*)(\")((?=\n)|(?=$))",
                    r"run(\g<2>\g<3>\g<4>, show_console=False)",
                ),
            ],
        ),
        run_output=(
            "rco: ",
            [
                (
                    r"^(rco:\s*)((?!\s*\")(.*))((?=\n)|(?=$))",
                    r"run('\g<2>', show_console=False, output_to_repl=True)",
                ),
                (
                    r"^rco:(\s*)(\")(.*)(\")((?=\n)|(?=$))",
                    r"run(\g<2>\g<3>\g<4>, show_console=False, output_to_repl=True)",
                ),
            ],
        ),
        run_console=(
            "rc: ",
            [
                (r"^(rc:\s*)((?!\s*\")(.*))((?=\n)|(?=$))", r"run('\g<2>')"),
                (r"^rc:(\s*)(\")(.*)(\")((?=\n)|(?=$))", r"run(\g<2>\g<3>\g<4>)"),
            ],
        ),
        # The (?=...) regex operator means "stop matching if you get to ..., but ... has to be in the string"
        # The "((.*)(?=\)))" has to be the last expression if using "s:" in a function like "print()" because it captures anything until the closing parenthesis
    )
    """
    Example of replacing a function name with a new function name:
        import re
        a = "old(test)"
        a = re.sub(r"(old)(\(.*\))", r"new\g<2>", a)
        print(a_new) >>> "new(test)"
    """

    def __init__(self, initial_references, repl_print):
        """
        Initialize the interactive interpreter
        """
        # Get the default references and add them to the initial_references list
        initial_references.update(self.get_default_references())
        """
        Initialize parent, from which the current class is inherited, 
        THIS MUST BE DONE SO THAT THE SUPERCLASS EXECUTES ITS __init__ !!!!!!
        """
        # the InteractiveInterpreter object takes references as the first argument
        super().__init__(initial_references)
        # Import all the default modules
        for mod in self.modules:
            self.eval_command("import " + mod)
        # Save the REPL print function as a reference
        self.repl_print = repl_print

    def eval_command(self, command, display_action=True):
        """
        This EVAL function executes the command by the interactive interpreter.
        (inputted by the REPL ReplLineEdit and pressing enter)
        """
        try:
            # Reset the error message
            self.eval_error = None
            # Replace certain strings with methods
            filtered_command = self.replace_references(self.dict_re_references, command)
            filtered_command = self.replace_keywords(
                self.dict_keywords, filtered_command
            )
            # Remove the literal sequences from the command
            filtered_command = filtered_command.replace(self.re_escape_sequence, "")
            # Execute the filtered command string with the custom InteractiveInterpreter
            # First try to evaluate the command string, to see if it's an expression
            try:
                # Try to EVALUATE the command
                eval_return = eval(filtered_command, self.locals)
                if display_action == True:
                    self.repl_print(eval_return)
                return None
            except:
                # EXECUTE
                self.eval_error = None
                # Execute and return the error message
                return self._custom_runcode(filtered_command)
        except Exception as ex:
            return "REPL evaluation error!"

    def eval_command_hy(self, command, display_action=True):
        try:
            eval_return = hy.eval(hy.read_many(command), self.locals)
            if display_action == True and eval_return is not None:
                self.repl_print(eval_return)
            return None
        except:
            return self._custom_showtraceback()

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
            return "".join(lines)

    def replace_references(self, references, command):
        """Replace references with actual forms module methods and attributes"""
        for key in references:
            # Replace keyword with actual function from the forms module MainWindow class
            command = re.sub(references[key][0], references[key][1], command)
        return command

    def replace_keywords(self, keywords, command):
        """Replace keywords with actual forms module methods and attributes"""
        for key in keywords:
            # Replace keyword with actual function from the forms module MainWindow class
            if isinstance(keywords[key][1], str):
                # Do a normal RE replace
                command = re.sub(keywords[key][1], keywords[key][2], command)
            else:
                # Cycle through list and replace
                for sub in keywords[key][1]:
                    search_exp = sub[0]
                    replace_exp = sub[1]
                    command = re.sub(search_exp, replace_exp, command)
        return command

    def update_locals(self, new_locals):
        """
        Add new locals to the existing ones
        """
        for new_local in new_locals:
            # Check if the local is already in the current list of locals
            if new_local not in self.locals:
                # Update the locals dictionary with the new item
                self.locals.update({new_local: new_locals[new_local]})

    def reset_locals(self):
        """
        Clear all custom interpreter references in the locals dictionary
        """
        self.locals = {}

    def run_cmd_process(self, command, show_console=True, output_to_repl=False):
        """
        Function for running a command line process and return the result
        """
        # Check what is the current OS
        if data.platform == "Windows":
            if show_console == True:
                # Double quotes have to be handled differently on Windows (don't know about Linux yet)
                if '"' in command:
                    process_commands = [
                        "command = 'start cmd.exe /c {:s} & pause'".format(command),
                        "subprocess.Popen(command, shell=True)",
                    ]
                else:
                    process_commands = [
                        "subprocess.Popen(['start', 'cmd.exe', '/c', '"
                        + command
                        + " & pause'], shell=True)"
                    ]
            else:
                if output_to_repl == True:
                    options = "startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True"
                    # Double quotes have to be handled differently on Windows (don't know about Linux yet)
                    if '"' in command:
                        sub_call = (
                            "subprocess.Popen('start cmd.exe /c {:s}', {:s})".format(
                                command, options
                            )
                        )
                    else:
                        sub_call = 'subprocess.Popen(["start", "cmd.exe", "/c", "{:s}"], {:s})'.format(
                            command, options
                        )
                    process_commands = [
                        "startupinfo = subprocess.STARTUPINFO()",
                        "startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW",
                        "result = " + sub_call,
                        "(output, err) = result.communicate()",
                        "print(output)",
                    ]
                else:
                    options = "startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True"
                    # Double quotes have to be handled differently on Windows (don't know about Linux yet)
                    if '"' in command:
                        sub_call = (
                            "subprocess.Popen('start cmd.exe /c {:s}', {:s})".format(
                                command, options
                            )
                        )
                    else:
                        sub_call = 'subprocess.Popen(["start", "cmd.exe", "/c", "{:s}"], {:s})'.format(
                            command, options
                        )
                    """
                    'THE THIRD LINE HAS TO CONTAIN MORE THAN JUST sub_call! Otherwise the python
                    interpreter crashes! Don't know why yet.
                    """
                    process_commands = [
                        "startupinfo = subprocess.STARTUPINFO()",
                        "startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW",
                        "try:\n  {:s}\nexcept Exception as ex:\n  print(ex)".format(
                            sub_call
                        ),
                    ]

                # Create a function that will evaluate commands in the new thread
                def threaded_function(commands):
                    # Run the commands sequentially and check the result
                    for command in commands:
                        result = self.eval_command(command)
                        if result != None:
                            return

                # Start the new thread
                thread = threading.Thread(
                    target=threaded_function, args=(process_commands,)
                )
                thread.start()
                return
        else:
            # GNU/Linux (Lubuntu tested)
            if show_console == True:
                if data.terminal == "x-terminal-emulator":
                    # LXTerminal
                    end_delimiter_string = "-------------------------"
                    end_message_string = "Press ENTER to continue ..."
                    process_commands = [
                        """subprocess.Popen(
                                ["{:s}","-l","-e","{:s};echo {:s};python3 -c 'input(\\"{:s}\\")'"]
                        )""".format(
                            data.terminal,
                            command,
                            end_delimiter_string,
                            end_message_string,
                        )
                    ]
                else:
                    # Others terminals like XTerm
                    end_delimiter_string = "-------------------------"
                    end_message_string = "Press ENTER to continue ..."
                    process_commands = [
                        """subprocess.Popen(
                                ["{:s}","-e","{:s};echo {:s};python3 -c 'input(\\"{:s}\\")'"]
                        )""".format(
                            data.terminal,
                            command,
                            end_delimiter_string,
                            end_message_string,
                        )
                    ]
            else:
                if output_to_repl == True:
                    options = (
                        "stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True"
                    )
                    sub_call = 'subprocess.Popen("{:s}", {:s})'.format(command, options)
                    process_commands = [
                        "result = " + sub_call,
                        "(output, err) = result.communicate()",
                        "print(output)",
                    ]
                else:
                    options = (
                        "stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True"
                    )
                    sub_call = 'subprocess.Popen("{:s}", {:s})'.format(command, options)
                    process_commands = [
                        "result = " + sub_call,
                        "(output, err) = result.communicate()",
                    ]
        # Run the commands sequentially and check the result
        for cmd in process_commands:
            result = self.eval_command(cmd)
            if result != None:
                return

    def create_terminal(self, dir=None):
        """
        Spawn a new "terminal/command line" window asynchronously (currently works only on win32)
        """
        # Change current working directory if it was supplied as an argument
        if dir != None:
            try:
                os.chdir(dir)
            except:
                # Return an evaluation error if exception occured (it's horribly side-effect-y but simple)
                self.eval_error = 'Invalid directory supplied to "show_terminal()"'
        # Check OS and spawn a terminal accordingly
        if data.platform == "Windows":
            # Remove the PYTHONHOME environment variable that Nuitka creates. It causes problems
            # when running the systems python interpreter!
            os.environ["PYTHONHOME"] = ""
            subprocess.Popen("cmd.exe")
        else:
            # GNU/Linux (Lubuntu tested)
            try:
                subprocess.Popen([data.terminal])
            except Exception as ex:
                self.repl_print(
                    "Error creating a '{}' terminal!".format(data.terminal)
                    + "To change the terminal application, edit the user settings.",
                    constants.MessageType.ERROR,
                )

    def get_default_references(self):
        """Return the references that will be available in for execution"""
        # Create the initial references dictionary
        reference_list = dict(
            interpreter_run=self.run_cmd_process,
            show_terminal=self.create_terminal,
        )
        # Extend the dictionary with the constants dictionary
        reference_list.update(self.dict_const_references)
        return reference_list
