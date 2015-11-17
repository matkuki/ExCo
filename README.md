# Ex&#46;Co&#46; #
### Descripton: ###
Ex&#46;Co&#46; (Extensible Coder) is a GUI text editor written in Python that uses PyQt/QScintilla libraries with some lexers available in Cython for more efficient text highlighting.
I developed it with simplicity of use and extensibility in mind.

### License: ###
__GNU General Public License v3.0__

Copyright (c) 2013-2015 Matic Kukovec. All rights reserved.
  
#### Additional licenses: ####
All additional licenses are specified at the beginning of every source code file. If I made any mistakes, please open an issue.


### Some features: ###
- Three window editing system with window spinning, moving, copying, ...
- All standard text editor functionality (copy, cut, paste, ...)
- 'Function wheel' for quick access to most of Ex&#46;Co&#46;'s functionality
- Integrated Python single/multi-line REPL (Read-Eval-Print Loop) for direct access/manipulation of each editor window text and all other functionality
- Text diffing (also between editor windows)
- Execute Terminal shell commands directly from the REPL (Windows or GNU-Linux)
- Ability to add your custom Python functions
- Language syntax highlighting: Python, Nim, C/C++, JavaScript, C#, Ruby, ...
- Code tree displaying for: 
    - Python 3
    - Nim
    - C (very simplistic)

### Dependencies: ###
- Python 3
- PyQt4 version 4.11 or higher

__Optional dependencies:__
- Cython (ONLY FOR BUILDING SPECIAL LEXERS)


### Starting Ex&#46;Co&#46;: ###
```sh
$ python main.py
```
For more startup options add the ```--help``` or ```-h``` flag.

### Quick examples: ###
1. Basic text manipulation with the REPL (very detailed example):
   - start Ex&#46;Co&#46; by executing ```python main.py```
   - focus the main editor window (the big one) with one of the following options:
     - click on it the mouse
     - press ```Ctrl+1```
     - use the menubar by selecting ```View -> Focus Main Window```
     - use the 'Function Wheel' by pressing ```F1``` and selection the ```Focus Main Window``` icon
   - create a new document with one of the following options:
     - pressing ```Ctrl+N```
     - use the menubar by selecting ```File -> New```
     - use the 'Function Wheel' by pressing ```F1``` and selection the ```Create New Document``` icon
   - focus the single-line REPL one of the following options:
     - click on it with the mouse
     - press ```Ctrl+R```
     - use the menubar by selecting ```REPL -> Focus REPL(Single)```
     - use the 'Function Wheel' by pressing ```F1``` and selection the ```REPL Focus (Single Line)``` icon
   - write ```line_list = ["one", "two", "three"]``` and press ```Enter```
   - the main editor window should now contain the three new lines with each line containing the text from the corresponding line_list position
   - __line_list__ is a shorthand for __cmain.line_list__, the same can be done with __cupper.line_list__ for the upper window and __clower.line_list__ for the lower window
   - __NOTES:__ 
     - All commands in the REPL must be valid Python 3 code!
     - ```line_list``` is implemented as a python list so most list operations apply to it: append, insert, sort, ...


2. Manipulate editor lines using the REPL:
   - create a new document in the main editor window (look at previous example for details)
   - focus the REPL (```Ctrl+R```)
   - write __line_list.append("My new line!")__ and press ```Enter```
     - _A new line was inserted into the new document_
   - while the REPL is still focused, press the ```UP``` arrow to scroll up one level to the last command. As soon as you press ```UP``` the command __line_list.append("My new line!")__ should be visible in again and press ```Enter```
   - press ```F3``` to execute the 'last executed REPL command' again
     - _now there should be three 'My new line!' lines in the new document_
   - write ```line_list[1] = "Changed line one"``` and press ```Enter```
     - _the first line in the new document should now read_ ```Changed line one```
   - try the same with ```line_list[2]``` and ```line_list[3]```
   - write ```line_list.insert(2, "Inserted line")``` and press ```Enter```
     - _the second line 'Inserted line' was inserted_
   - write ```line_list.sort()``` and press ```Enter```
     - _the lines in the new document should now be sorted alphabetically_
   - focus the multi-line REPL (```Ctrl+5```)
   - write the text below into the multi-line REPL and press ```Ctrl+Enter```:
        ```python
        for i in range(10):
            line_list.append(str(i))
        ```
      - _ten new lines were added, from "0" to "9"_


3. Text diffing example
   - open the first text document in the main editor window by first focusing the main window and pressing ```Ctrl+O```
   - find and open the file using the popup dialog
   - open another document using the same two steps as above
   - now that the second document is selected and visible, move the mouse to the first documents tab and right click on it
   - a popup menu will be displayed and select the ```Text diff to main window``` option
   - The diff will be displayed in a newly created tab in the main editor window called __DIFF('document_name_1'/document_name_2)__
   - the __REPL MESSAGES__ tab will display the diff detailes
   - when the __DIFF__ tab is selected, you can use the helper buttons in the upper right corner of the main editor window:
      - blue button: got to the next unique line in __document 1__
      - purple button: got to the next unique line in __document 2__
      - green button: got to the next similar line


4. Moving tabs from window to window:
   - focus the main editor window
   - create a new document (```Ctrl+N```)
   - press ```Shift``` and left click-and-hold on the new documents tab
   - drag the mouse into the upper editor window and release the left mouse button
   - the document has now moved to the upper editor window
   - __Copying is the same except you hold down the__ ```Ctrl``` __button__


5. Adding your custom Python functions
   - open the __user_functions__ file by:
     - use the menubar by selecting ```File -> Edit User Functions```
     - use the 'Function Wheel' by pressing ```F1``` and selection the ```Edit User Functions``` icon
   - the __user_functions__ file will open in the main editor window
   - add your Python (Python 3) function to the file and add the custom autocompletion for the function:
   - Example:
```python
        def my_custom_function():
            ...
        my_custom_function.autocompletion = "my_custom_function()"
```
   - reload user functions by:
     - use the menubar by selecting ```File -> Reload User Functions```
     - use the 'Function Wheel' by pressing ```F1``` and selection the ```Reload User Functions``` icon
   - try your newly added function by focusing the REPL (```Ctrl+R```) and start typing the name of your added function, it should automatically add the rest of the function text into the REPL
   - __NOTE:__
     - __if your function name is similar to another already defined function, press__ ```Tab``` __to scroll through all of the similar named function until you reach the newly added one__

### Todo: ###
- add a curses version of Ex&#46;Co&#46; (only an idea at the moment)
- better C code tree displaying
- add more examples
