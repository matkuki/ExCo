
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2019 Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import data
import functions
import re
import math
import typing


class LineList(list):
    """
    List object that will hold the lines of the CustomEditor.
    It's a subclassed Python built-in list object for easier text manipulation.
    """
    #Class variables
    _parent = None
    
    """
    Class functions/methods
    """
    def __init__(self, parent, initial_text):
        """Overridden init function"""
        #Initialize superclass
        super().__init__()
        #Set the reference to the parent object
        self._parent = parent
        #Check if initial text is valid
        if initial_text:
            #Update the list of lines
            self.update_text_to_list(initial_text)

    def __getitem__(self, key):
        """Overridden list method that returns the specified line(item)"""
        #Check if the value is an int or a slice
        if isinstance(key, int):
            #Create a new key variable, because key is ReadOnly
            actual_key = key
            #Check if the key is lower than 1
            if actual_key == 0:
                actual_key = 1
            #Check if the key is greater than 0
            if actual_key > 0:
                actual_key -= 1
            #Return the line string
            return super().__getitem__(actual_key)
        elif isinstance(key, slice):
            #Create new key variables, because key is ReadOnly
            key_min     = key.start
            key_max     = key.stop
            #Check the lower bound of the slice is 0
            if key_min == None:
                key_min = 0
            #Check if the key is greater than 0
            if key_min > 0:
                key_min -= 1
            key_slice = slice(key_min, key_max)
            return super().__getitem__(key_slice)
        #The key is an invalid type
        return None

    def __setitem__(self, key, value):
        """Overridden list method that sets the specified line(item) to a value"""
        #Check if the value is a string or a list
        if isinstance(value, str) == False and isinstance(value, list) == False:
            raise Exception("Value has to be a list or a string!")
        #Check if the value is a string or a list
        if isinstance(value, str):
            #Try to set the line
            try:
                #Create a new key variable, because key is ReadOnly
                actual_key = key
                #Check if the key is 0
                if actual_key == 0:
                    actual_key = 1
                #Check if the key is greater than 0
                if actual_key > 0:
                    actual_key -= 1
                #Set the line
                super().__setitem__(actual_key, value)
            except:
                self.append(value, update_parent=False)
            #Update the custom editor document text
            self._parent.set_line(value, key)
        else:
            #The value is a list
            #Create new key variables, because key is ReadOnly
            key_min     = key.start
            key_max     = key.stop
            #Check if the lower boundary of the slice is 0
            if key_min == 0:
                key_min = 1
            #Check boundary order
            if key_max < key_min:
                raise Exception("First index has to be higher than the second!")
            #Check the boundaries
            if len(value) != (key_max-key_min+1):
                raise Exception("Ranges of assignment don't match!")
            #Insert the range into the custom list object
            super().__setitem__(slice(key_min-1, key_max), value)
            #Adjust the line numbers to standard(0..lines()-1) numbering
            line_from   = key_min - 1
            line_to     = key_max - 1
            #Set the new lines in the custom editor document
            self._parent.set_lines(line_from, line_to, value)
    
    def __iadd__(self, value):
        """Overloaded '+=' operator"""
        raise Exception("'+=' operator not implemented yet!")
    
    def __isub__(self, value):
        """Overloaded '-=' operator"""
        raise Exception("'-=' operator not implemented yet!")
    
    def __imul__(self, value):
        """Overloaded '*=' operator"""
        raise Exception("'*=' operator not implemented yet!")

    def _setitem(self, key, value):
        """Set the item at position-key, without updating the scintilla document"""
        #Check if the value is a string
        if isinstance(value, str) == False:
            return
        #Try to set the line
        try:
            #Create a new key variable, because key is ReadOnly
            actual_key = key
            #Check if the key is 0
            if actual_key == 0:
                actual_key = 1
            #Check if the key is greater than 0
            if actual_key > 0:
                actual_key -= 1
            #Set the line
            super().__setitem__(actual_key, value)
        except:
            self.append(value, update_parent=False)
    
    def _update_list_to_text(self, scroll_to_line=None):
        """Update the list of lines to the parent CustomEditor document"""
        #Merge the list into a single string with the
        #newline character as the delimiter
        text = "\n".join(self)
        #Update the text of the document
        self._parent.set_all_text(text)
        #Check if a line to which to scroll to was specified
        if scroll_to_line == None:
            scroll_to_line = self._parent.lines()
        #Scroll to the desired line of the document
        self._parent.setCursorPosition(scroll_to_line, 0)
    
    def append(self, value, update_parent=True):
        """
        Overloaded list append method
        Special arguments:
            update_parent   - False: append to list internally without updating
                                     the parent CustomEditor document.
                              True:  append to list and update the parent
                                     CustomEditor document.
        """
        #Check the update_parent parameter type
        if isinstance(update_parent, bool) == False:
            raise Exception("'update_parent' parameter must be of type boolean!")
        #Check the append value type
        if isinstance(value, str):
            #Execute the superclass append method
            super().append(value)
        elif isinstance(value, list):
            exception_text = "Use 'extend' to add multiple lines!"
            raise Exception(exception_text)
        else:
            exception_text = "'append' parameter must be a string!"
            raise Exception(exception_text)
        #Check if updating the parent document is needed
        if update_parent == True:
            self._update_list_to_text()
    
    def extend(self, value, update_parent=True):
        """
        Overloaded list extend method
        Special arguments:
            update_parent   - False: append to list internally without updating
                                     the parent CustomEditor document.
                              True:  append to list and update the parent
                                     CustomEditor document.
        """
        #Check the update_parent parameter type
        if isinstance(update_parent, bool) == False:
            raise Exception("'update_parent' parameter must be of type boolean!")
        #Check the extend value type
        if isinstance(value, list) == False:
            raise Exception("Extend parameter must be a list!")
        elif all(isinstance(item, str) for item in value) == False:
            raise Exception("All extend list items must be strings!")
        #Extend the list
        super().extend(value)
        #Check if updating the parent document is needed
        if update_parent == True:
            self._update_list_to_text()
    
    def insert(self, index, value, update_parent=True):
        """Overloaded insert method"""
        #Check the insert index type
        if isinstance(index, int) == False:
            raise Exception("Insert index parameter must be an integer!")
        #Check the insert value type
        if isinstance(value, str) == False:
            raise Exception("Insert parameter must be a string!")
        #Correct and check the index
        index -= 1
        if index < 0:
            index = 0
        #Insert the item
        super().insert(index, value)
        #Check if updating the parent document is needed
        if update_parent == True:
            self._update_list_to_text(index)
    
    def pop(self, index=None, update_parent=True):
        """Overloaded pop method"""
        #Check the insert index type
        if isinstance(index, int) == False:
            raise Exception("Pop index parameter must be an integer!")
        #Correct and check the index
        index -= 1
        if index < 0:
            index = 0
        #Pop out the item
        return_item = super().pop(index)
        #Check if updating the parent document is needed
        if update_parent == True:
            self._update_list_to_text(index)
        #Return the poped line
        return return_item
    
    def remove(self, item, update_parent=True):
        """Overloaded remove method"""
        #Check the insert index type
        if isinstance(item, str) == False:
            raise Exception("Remove item parameter must be a string!")
        #Check if item exists
        if not(item in self):
            raise Exception("Cannot remove item! Item is not in the list!")
        else:
            index = self.index(item) - 1
            #Check the index
            if index < 0:
                index = 0    
        #Remove the item
        super().remove(item)
        #Check if updating the parent document is needed
        if update_parent == True:
            self._update_list_to_text(index)
    
    def reverse(self, update_parent=True):
        """Overloaded reverse method"""
        #Reverse the list
        super().reverse()
        #Check if updating the parent document is needed
        if update_parent == True:
            self._update_list_to_text()
        
    def sort(self, update_parent=True):
        """Overloaded sort method"""
        #Sort the list
        super().sort()
        #Check if updating the parent document is needed
        if update_parent == True:
            self._update_list_to_text()
    
    def update_text_to_list(self, update_text):
        """Update the list from a string"""
        #Check if the value is a string
        if isinstance(update_text, str) == False:
            return
        #Empty the list
        self._clear()
        #Set the new content
        self.extend(re.split("\n", update_text), update_parent=False)
    
    def get_absolute_cursor_position(self):
        """Get the absolute cursor position"""
        line, index = self._parent.getCursorPosition()
        absolute_position = 0
        for i in range(line):
            absolute_position += len(self[i])
        absolute_position += index + 1
        return absolute_position
    
    def _clear(self):
        del self[:]