
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2019 Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import os
import sys
import itertools
import inspect
import functools
import keyword
import re
import collections
import textwrap
import importlib
import data
import components
import themes
import functions
import interpreter
import settings
import lexers
import traceback
import gc


"""
-----------------------------
Python REPL widget
-----------------------------
"""
class ReplLineEdit(data.QLineEdit):
    """Custom QLineEdit used for the REPL functionality"""
    #Class variables  (class variables >> this means that these variables are shared accross instances of this class, until you assign a new value to them, then they become instance variables)
    _parent                         = None          #Main window reference
    interpreter                     = None          #Custom interpreter used with the REPL
    #Attribute for indicating if the REPL is indicated
    indicated                       = False
    #List of characters to use for splitting the compare string for sequences. Minus (-) was taken out because it can appear in path names 
    _comparison_list                = [".", "(", " ", "+", "-", "*", "%", ",", "\"", "'"]
    _reduced_comparison_list        = ["(", " ", "+", "-", "*", "%", ",", "\"", "'"]
    #Lists of autocompletions grouped by levels
    _list_first_level_completions   = None
    _list_second_level_completions  = None
    #Generator used to cycle through autocompletions
    _ac_cycler                      = None
    #Dictionary that holds the current buffer position, the whole buffer list and the currently typed input
    _input_buffer                   = {"count": 0,  "list": [], "current_input": ""}
    #Flag that when set, make the next REPL evaluation not focus back on the REPL
    _repl_focus_flag                = False
    
    """
    Built-in and private functions
    """
    def __init__(self, parent, main_form, interpreter_references=None):
        """Initialization"""
        # Initialize superclass class, from which the current class is inherited, THIS MUST BE DONE SO THAT THE SUPERCLASS EXECUTES ITS __init__ !!!!!!
        super().__init__()
        # Initialize the parent references and update the autocompletion lists
        self._parent = parent
        self.main_form = main_form
        # Set default font
        font = data.QFont(
            data.current_font_name,
            data.current_font_size+2,
            data.QFont.Bold
        )
        self.setFont(font)
        # Initialize the interpreter
        self.interpreter = interpreter.CustomInterpreter(
            interpreter_references, 
            main_form.display.repl_display_message
        )
        # Initialize interpreter reference list that will be used for autocompletions
        self._list_repl_references  = [str_ref for str_ref in interpreter_references]
        # Initialize style
        self.update_style()
    
    def update_style(self):
        # REPL and REPL helper have to be set directly
        self.setStyleSheet(f"""
            QLineEdit[indicated=false] {{
                color: {data.theme.Font.DefaultHtml};
                background-color: {data.theme.Indication.PassiveBackGround};
            }}
            QLineEdit[indicated=true] {{
                color: {data.theme.Font.DefaultHtml};
                background-color: {data.theme.Indication.ActiveBackGround};
            }}
        """)
    
    def indication_set(self):
        self.setProperty("indicated", True)
        self.style().unpolish(self)
        self.style().polish(self)
    
    def indication_reset(self):
        self.setProperty("indicated", False)
        self.style().unpolish(self)
        self.style().polish(self)

    def _get_path_list(self, path_string):
        """Return a list of all directories and files if the path string is valid"""
        path_list   = []
        #Strip the path to the last forwardslash character
        base_path   = path_string[:path_string.rfind("/")+1]
        #Check if the base path string is a valid path
        if os.path.isdir(base_path) == False:
            return path_list
        #Add items of directory to list
        for item in os.listdir(base_path):
            path_list.append(os.path.join(base_path, item))
        #Return the path item list
        return path_list

    def _filter_keypress(self, key_event):
        """Filter keypress for appropriate action"""
        pressed_key = key_event.key()
        #Reset the autocompletion cycler
        self._ac_cycler                 = None
        #Get valid sequances used for autocompletion
        current_sequences_list = self._get_valid_sequence_list(self.text())
        #Check and display autocompletions if any are valid
        autocompletion_list = self._find_autocompletions(current_sequences_list)
        if (pressed_key >= 48 and pressed_key <= 57 or
            pressed_key >= 65 and pressed_key <= 90 or
            pressed_key == 95):
            #Return if there are no characters in the current sequence
            if len(current_sequences_list[0]) == 0:
                return
            #A letter or number has been pressed
            self._display_autocompletion(autocompletion_list)
            #Create the cycler that will cycle through the autocompletions
            self._create_ac_cycler(autocompletion_list)
            #A new character has been type, reset the input buffer counter
            self._input_buffer["count"] = 0
        elif pressed_key == 16777235:
            #Cycle input buffer up
            self._input_buffer_cycle(1)
        elif pressed_key == 16777237:
            #Cycle input buffer down
            self._input_buffer_cycle(0)
        elif pressed_key == 16777219:
            #A new character has been typed, reset the input buffer counter
            self._input_buffer["count"] = 0
        elif (pressed_key == data.Qt.Key_Enter or
                pressed_key == data.Qt.Key_Return):
            if self.selectedText() != "":
                self.setCursorPosition(len(self.text()))
            else:
                #Detected ENTER key press, evaluate REPL text
                self._repl_eval()

    def _repl_eval(self, external_string=None, display_action=True):
        """Evaluate string entered into the REPL widget"""
        data.print_log("REPL evaluated")
        #Check if an external evaluation string was specified
        if external_string == None:
            #No external evaluation string, evaluate the REPL text
            current_command = self.text()
        else:
            current_command = external_string
        #Display evaluated command if specified
        current_rm_index = None
        if display_action == True:
            repl_messages = self.main_form.display.find_repl_messages_tab()
            if repl_messages != None:
                if repl_messages._parent.count() > 1:
                    current_rm_index = repl_messages._parent.currentIndex()
            #Display the evaluated command (this sets the focus to the REPL messages tab)
            split_command = current_command.split("\n")
            for i, command in enumerate(split_command):
                if i != 0:
                    self.main_form.display.repl_display_message("... " + command)
                else:
                    self.main_form.display.repl_display_message(">>> " + command)
            if current_rm_index != None:
                #Revert the focus of the BasicWidget that hold the REPL messages tab to
                #whichever widget was focused before
                repl_messages._parent.setCurrentIndex(current_rm_index)
        #Evaluate the REPL text and store the result
        eval_return = self.interpreter.eval_command(current_command, display_action)
        #Save text into the input buffer
        self._input_buffer_add(self.text())
        #Clear the REPL text
        self.setText("")
        #Check if the REPL focus flag is set
        if self._repl_focus_flag == True:
            #Skip setting focus back to the REPL and reset the skip focus flag
            self._repl_focus_flag = False
        else:
            #Set focus back to the REPL
            self.setFocus()
        #Check evaluation return message and display it in the "REPL Messages" tab
        if eval_return is not None:
            data.print_log(eval_return)
            if display_action == True:
                self.main_form.display.repl_display_message(
                    eval_return,
                    message_type=data.MessageType.ERROR
                )
            else:
                return eval_return
        else:
            data.print_log("EVALUATION/EXECUTION SUCCESS")
        return None


    """
    REPL autocompletion functions
    """
    def _display_autocompletion(self, ac_list):
        """Show the autocompletion in the REPL"""
        #Check if there are no autocompletions and that there is no text after the cursor position
        if len(ac_list) > 0 and self.cursorPosition() == len(self.text()):
            start_pos = self.cursorPosition()
            self.setText(self.text() + ac_list[0])
            end_pos = self.cursorPosition()
            #Select the added autocompletion text
            self.setSelection(start_pos, end_pos)
    
    def _create_ac_cycler(self,  autocompletion_list):
        """Create a autocompletion cycler to cycle through all of the autocompletions"""
        if len(autocompletion_list) > 0:
            self._ac_cycler = itertools.cycle(autocompletion_list)
            #Cycle one autocompletion forward, because the first autocompletion is already shown
            next(self._ac_cycler)
        else:
            self._ac_cycler = None
    
    def _cycle_autocompletion(self):
        """Cycle through autocompletion list"""
        #Return if there are no autocompletions
        if self._ac_cycler == None:
            return
        if self.selectedText() == "":
            #Current autocompletion is already shown without a selection area
            ac_start = len(self.text())
            self.setText(self.text() + next(self._ac_cycler))
            end_pos = self.cursorPosition()
            self.setSelection(ac_start, end_pos)
        else:
            #Current autocompletion has a selection area
            ac_start = self.selectionStart()
            self.setText(self.text()[:ac_start] + next(self._ac_cycler))
            end_pos = self.cursorPosition()
            self.setSelection(ac_start, end_pos)

    def _input_buffer_cycle(self, direction=0):
        """Cycle the input buffer into the selected direction"""
        #Check if the input buffer is empty
        if len(self._input_buffer["list"]) == 0:
            return
        #Save currently typed text
        if self._input_buffer["count"] == 0:
            self._input_buffer["current_input"] = self.text()
        #Check what is the current buffer position, change it and put it into the REPL
        if direction == 1:
            if self._input_buffer["count"] > -(len(self._input_buffer["list"])):
                self._input_buffer["count"] -= 1
            self.setText(self._input_buffer["list"][self._input_buffer["count"]])
        else:
            if self._input_buffer["count"] < -1:
                self._input_buffer["count"] += 1
                self.setText(self._input_buffer["list"][self._input_buffer["count"]])
            else:
                #Show currently saved input text (the text that the user typed before pressing up)
                self._input_buffer["count"] = 0
                self.setText(self._input_buffer["current_input"])
    
    def _input_buffer_add(self,  entry):
        """Add a single value to the input buffer"""
        #Check if there is any input text
        if self.text() == "":
            return
        #Check if the last saved input is the same as the current input, otherwise add it to the input buffer
        if len(self._input_buffer["list"]) > 0:
            if self.text() != self._input_buffer["list"][-1]:
                self._input_buffer["list"].append(self.text())
        else:
            #Add the text into the buffer withoit checking if the input buffer is empty
            self._input_buffer["list"].append(self.text())
        #Reset the item counter
        self._input_buffer["count"] = 0
        #Reset the stored current input text
        self._input_buffer["current_input"] = ""

    def input_buffer_clear(self):
        """Clear the input buffer, counter and current saved input"""
        self._input_buffer  = {"count": 0,  "list": [], "current_input": ""}

    def _get_valid_sequence_list(self, string):
        """
        Get the last one or two valid sequence, which will be compared to autocompletion list
        E.G. 1: "print(main.se" returns >> first = "se", second = "main"
        E.G. 2: "print_log(nek" returns >> first = "nek", second = ""
        """
        raw_text                = string
        current_sequence    = ""
        previous_sequence   = ""
        #List the separators as they appear in the raw string
        separator_list = []
        for ch in raw_text:
            if ch in self._comparison_list:
                separator_list.append(ch)
        #Do the standard autocompletion parse
        for i, ch_1 in reversed(list(enumerate(raw_text))):
            #Get the last valid separation character
            if ch_1 in self._comparison_list:
                current_sequence = raw_text[(i+1):]
                #If the character is a dot, return the previous sequence also
                if ch_1 == ".":
                    #The separator is a dot, get the previous sequence in case it's a class
                    for j, ch_2 in reversed(list(enumerate(raw_text[:i]))):
                        if ch_2 in self._reduced_comparison_list:
                            #Found a character from the reduced comparison list
                            previous_sequence = raw_text[(j+1):i]
                            break
                        elif j == 0:
                            #Did not find a character from the reduced comparison list and reached the beggining of text
                            previous_sequence = raw_text[j:i]
                            break
                break
        if not [x for x in raw_text if x in self._comparison_list]:
            #None of the separator characters were found in current text
            current_sequence = self.text()
        data.print_log(previous_sequence + "  " + current_sequence)
        return [current_sequence, previous_sequence]
    
    def _find_autocompletions(self, current_sequences_list):
        """Check and display the current autocompletions, if there are any"""
        current_sequence    = current_sequences_list[0]
        previous_sequence   = current_sequences_list[1]
        found_list              = []
        if previous_sequence != "":
            for ref in self._list_second_level_completions:
                if ref.startswith(previous_sequence + "." + current_sequence):
                    #Autocompletion found, delete the part of the autocompletion that is already written
                    found_list.append(ref.replace(previous_sequence + "." + current_sequence, ""))
        else:
            #Test if autocompletion is a path or an object
            if "/" in current_sequence or "\\" in current_sequence:
                #Replace the windows path backslashes to forwardslashes
                if "\\" in current_sequence:
                    current_sequence = current_sequence.replace("\\", "/")
                #Path (all path searches are done case sensetively)
                path_items = self._get_path_list(current_sequence)
                for item in path_items:
                    if item.startswith(current_sequence):
                        diff_index = re.search(current_sequence, item).end()
                        #Autocompletion found, delete the part of the autocompletion that is already written
                        found_list.append(item[diff_index:])
            else:
                #Object
                for ref in self._list_first_level_completions:
                    if ref.startswith(current_sequence):
                        #Autocompletion found, delete the part of the autocompletion that is already written.
                        #ONLY THE FIRST INSTANCE OF THE ALREADY WRITTEN PART HAS TO BE REPLACED,
                        #ELSE YOU GET:
                        #   "line_list" autocompletion, input_text = "li" >>> output of "ref.replace(current_sequence, "")"
                        #   is "ne_st" instead of "ne_list"
                        found_list.append(ref.replace(current_sequence, "", 1))
        return found_list


    """
    Qt QLineEdit functions
    """
    def event(self, event):
        """Rereferenced/overloaded main QWidget event, that is executed before all other events of the widget"""
        if (event.type() == data.QEvent.KeyPress) and (event.key() == data.Qt.Key_Tab):
            self._cycle_autocompletion()
            return True
        return data.QLineEdit.event(self, event)

    def _keypress_decorator(func):
        """A decorator for the QScintila KeypressEvent, to catch which key was pressed"""
        def key_press(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self._filter_keypress(args[0])
        return key_press

    @_keypress_decorator    #Add decorator to the keypress event
    def keyPressEvent(self, event):
        """QScintila keyPressEvent, to catch which key was pressed"""
        #Return the key event
        return data.QLineEdit.keyPressEvent(self, event)
    
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        # Reset the click&drag context menu action
        components.ActionFilter.clear_action()
    
    def contextMenuEvent(self, event):
        event.accept()

    def focusInEvent(self, event):
        """Event that fires when the REPL gets focus"""
        self.main_form._key_events_lock()
        #Set the focus to the REPL
        self.setFocus()
        #Clear the cursor position from the statusbar
        self.main_form.display.update_cursor_position()
        data.print_log("Entered REPL")
        #Reset the main forms last focused widget
        self.main_form.last_focused_widget = None
        data.print_log("Reset last focused widget attribute")
        #Hide the function wheel if it is shown
        self.main_form.view.hide_all_overlay_widgets()
        #Ignore the event
        event.ignore()
        #Return the focus event
        return data.QLineEdit.focusInEvent(self, event)
    
    def setFocus(self):
        """Overridden focus event"""
        #Execute the supeclass focus function
        super().setFocus()
        #Check indication
        self.main_form.view.indication_check()

    def focusOutEvent(self, event):
        """Event that fires when the REPL loses focus"""
        self.main_form._key_events_unlock()
        data.print_log("Left REPL")
        #Ignore the event
        event.ignore()
        #Return the focus event
        return data.QLineEdit.focusOutEvent(self, event)
    
    def wheelEvent(self, wheel_event):
        """Overridden mouse wheel rotate event"""
        key_modifiers = data.QApplication.keyboardModifiers()
        if data.PYQT_MODE == 4:
            delta = wheel_event.delta()
        else:
            delta = wheel_event.angleDelta().y()
        if delta < 0:
            data.print_log("REPL helper mouse rotate down event")
            if key_modifiers == data.Qt.ControlModifier:
                #Zoom out the scintilla tab view
                self.decrease_text_size()
        else:
            data.print_log("REPL helper mouse rotate up event")
            if key_modifiers == data.Qt.ControlModifier:
                #Zoom in the scintilla tab view
                self.increase_text_size()
        #Handle the event
        if key_modifiers == data.Qt.ControlModifier:
            #Accept the event, the event will not be propageted(sent forward) to the parent
            wheel_event.accept()
        else:
            #Propagate(send forward) the wheel event to the parent
            wheel_event.ignore()
    
    def increase_text_size(self):
        """Increase size of the REPL text"""
        new_font = self.font()
        if new_font.pointSize() > 32:
            return
        new_font.setPointSize(new_font.pointSize() + 1)
        self.setFont(new_font)
        new_font_metric = data.QFontMetrics(new_font)
        self.main_form.view.main_relation = new_font_metric.height() + 48
        self.main_form.view.refresh_main_splitter()
    
    def decrease_text_size(self):
        """Decrease size of the REPL text"""
        new_font = self.font()
        if new_font.pointSize() < 12:
            return
        new_font.setPointSize(new_font.pointSize() - 1)
        self.setFont(new_font)
        new_font_metric = data.QFontMetrics(new_font)
        self.main_form.view.main_relation = new_font_metric.height() + 48
        self.main_form.view.refresh_main_splitter()
    

    """
    REPL interactive interpreter functions
    """
    def interpreter_update_references(self, new_references, first_level_list, second_level_list):
        """Update the references that can be accessed by the interactive interpreter"""
        #Update the interpreter with the new locals
        self.interpreter.update_locals(new_references)
        self._list_first_level_completions = first_level_list
        self._list_second_level_completions = second_level_list
        #Extend the primary autocompletion with the useful custom interpreter methods
        self._list_first_level_completions.extend(self.interpreter.get_default_references())
        #Extend the primary autocompletion with the regular expression dictionary of the REPL CustomInterpreter
        self._list_first_level_completions.extend(self.interpreter.dict_re_references)
        #The keyword dictionary is different from the references, look in the interpreter module
        ext_first_level = [self.interpreter.dict_keywords[keyword][0] for keyword in self.interpreter.dict_keywords]
        self._list_first_level_completions.extend(ext_first_level)
        #Convert lists to sets and back to remove duplicates
        self._list_first_level_completions  = list(set(self._list_first_level_completions))
        self._list_second_level_completions = list(set(self._list_second_level_completions))
        #Sort the new lists alphabetically
        self._list_first_level_completions.sort()
        self._list_second_level_completions.sort()
    
    def interpreter_add_references(self, new_references):
        """Append new references to the existing REPL interpreter references"""
        self._list_first_level_completions = list(self._list_first_level_completions)
        #Extend the primary autocompletions
        self._list_first_level_completions.extend(new_references)
        #Convert list to set and back to remove duplicates
        self._list_first_level_completions = list(set(self._list_first_level_completions))
        #Sort the new lists alphabetically
        self._list_first_level_completions.sort()
    
    def interpreter_reset_references(self, new_references, first_level_list, second_level_list):
        """Clear all of the interpreter references and update them with the new ones"""
        #Clear the references
        self.interpreter.reset_locals
        #Update the references
        self.interpreter_update_references(new_references, first_level_list, second_level_list)
    
    def interpreter_update_windows(self, main, upper, lower):
        """Update the Main, Upper and Lower window references of the interpreter"""
        self.interpreter.locals["main"]     = main
        self.interpreter.locals["upper"]    = upper
        self.interpreter.locals["lower"]    = lower


    """
    Various ReplLineEdit functions
    """
    def skip_next_repl_focus(self):
        """
        Function that sets the flag that makes the next REPL evaluation
        skip setting focus back to the ReplLineEdit
        """
        #Set the skip focus flag
        self._repl_focus_flag = True
    
    def get_repl_references(self):
        """Create and return a dictionary that holds all the REPL references that will be used in the interpreter module"""
        return  dict(
            repl=self,
            interpreter=self.interpreter, 
        )   
    
    def repeat_last_repl_eval(self):
        """Repeat the last command that was evaluated by the REPL if any"""
        #Check the input buffer
        if len(self._input_buffer["list"]) > 0:
            #Set REPL text to the last item in REPL input list by cycling the buffer list up
            self._input_buffer_cycle(1)
            #Evaluate REPL text
            self._repl_eval()
        else:
            self.main_form.display.write_to_statusbar("No commands in REPL input buffer!", 1000)

    def external_eval_request(self, eval_string, calling_widget):
        """An external evaluation request from the ReplHelper or another widget"""
        #Evaluate the external string
        self._repl_eval(eval_string)
        #Set focus back to the calling widget
        calling_widget.setFocus()

