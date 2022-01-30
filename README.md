# Ex&#46;Co&#46; <img src="https://github.com/matkuki/Ex-Co/blob/master/resources/exco-icon.png" align="top" width="48" height="48">
### Descripton: ###
Ex&#46;Co&#46; (Extensible Coder) is a GUI text editor written in Python that uses PyQt/QScintilla libraries with some lexers available in Cython for more efficient text highlighting.
I developed it with simplicity of use and extensibility in mind.<br>
For precompiled bundles for Windows see the releases page (https://github.com/matkuki/ExCo/releases/latest).
<br><br>
### Website: ###
http://matkuki.github.io/ExCo/
<br>
### Quick features video: ###
https://www.youtube.com/watch?v=v-7fqJGv7Ts&feature

### License: ###
__GNU General Public License v3.0__

Copyright (c) 2013-2022 Matic Kukovec. All rights reserved.
  
#### Additional licenses: ####
All additional licenses are specified at the beginning of every source code file and in text file format in the ```additional_licenses``` directory. If I made any mistakes, please open an issue.
<br><br>

### Some features: ###
- Three window editing system with window spinning, moving, copying, ...
- All standard text editor functionality (copy, cut, paste, ...)
- 'Function wheel' for quick access to most of Ex&#46;Co&#46;'s functionality
- Integrated Python single/multi-line REPL (Read-Eval-Print Loop) for direct access/manipulation of each editor window text and all other functionality
- Text diffing (also between editor windows)
- Execute Terminal/Shell commands directly from the REPL (Windows or GNU/Linux)
- Ability to add your custom Python functions
- Language syntax highlighting: AVS, Ada, Bash, Batch, CMake, CPP, CSS, CSharp, CoffeeScript, Cython, D, Diff, Fortran, Fortran77, HTML, IDL, Java, JavaScript, Lua, Makefile, Matlab, Nim, Oberon, Octave, PO, POV, Pascal, Perl, PostScript, Properties, Python, RouterOS (MikroTik), Ruby, SQL, Spice, TCL, TeX, Text, VHDL, Verilog, XML and YAML
- Code tree displaying for: 
    - Python 3
    - Nim
    - C
    - Many more to come ...
<br><br>

### Supported platforms: ###
- __Windows__ ([precompiled binaries available](https://github.com/matkuki/ExCo/releases))
- __GNU/Linux__ (tested on Lubuntu, Raspbian (Raspberry pi, pi2 and pi3))
- __Mac OS__ (Many thanks to __zenlc2000__ for testing this on Mac OS 10.11)

### Dependencies: ###
- Python 3
- PyQt5 version 5.7 (or higher) or PyQt4 version 4.10 (or higher)
- QScintilla 2.9 or higher (is bundled in the PyQt installer on Windows)
- pywin32 (required on Windows only)

__Optional dependencies:__
- XTerm terminal editor is used by default on GNU/Linux (can be changed in the config file)
- Cython (ONLY FOR BUILDING SPECIAL LEXERS)
- Nim programming language (ONLY FOR BUILDING SPECIAL LEXERS)
- Universal or Exuberant Ctags (Used with code tree displaying)
<br>

### Installation notes: ###
- __Windows__:<br>
  Method 1 - using the official PyQt installer:<br>
    Install the latest [PyQt4 or PyQt5](https://www.riverbankcomputing.com/software/pyqt/download) library for
    your version of Python3 (QScintilla2 is bundled with the installer). Run Ex.Co. using the command described below in the 'Starting Ex&#46;Co&#46;' section.

  Method 2 - using __pip__:<br>
  If you have pip installed with your Python 3 installation (needs to be Python 3.5 or higher), you can install PyQt5 and QScintilla with the following commands (You will need to run the commands as administrator!):<br>
```sh 
$ pip install PyQt5
```
```sh
$ pip install Qscintilla
```
```sh
$ pip install pywin32
```
- __GNU/Linux__:<br>
  Method 1 - using __apt-get__:<br>
  If you are on Lubuntu, Raspbian or probably most Debian derivatives, install the following libraries using __apt-get__:
  - python3.x (Probably already installed on the system)
  - python3-pyqt4 __or__ python3-pyqt5
  - python3-pyqt4.qsci __or__ python3-pyqt5.qsci
    (If this library is outdated, you will get a 'missing QsciLexerCoffeeScript' or similar exception.
     Update the repositories and try again. If that still doesn't help, try using Ubuntu's 'Universe' repositories.)

  Method 2 - using __pip__:<br>
  If you have pip installed with your Python 3 installation (needs to be Python 3.5 or higher) , you can install PyQt5 and QScintilla with the following commands (You will need to run the commands as sudo!):<br>
```sh 
$ pip install PyQt5
```
```sh
$ pip install Qscintilla
```

  Otherwise you can install PyQt4/PyQt5 and QScintilla (you'll also need the SIP library) from source from their official [website](https://www.riverbankcomputing.com/software/pyqt/download). Download the source code and follow the instructions in the readme/install files. You'll also need the [Qt C++ source code](https://wiki.qt.io/Get_the_Source#Qt_4.x).
- __Mac OS__:<br>
  Try using Anaconda Python 3 and it's package manager to install all dependencies. Here is the more [information](https://github.com/matkuki/ExCo/issues/1).<br>
  I don't know much about Mac's, but you can try using the default Mac package manager to find the PyQt4 and QScintilla
  libraries or install the libraries from source, same as on GNU/Linux.<br><br>
  


### Starting Ex&#46;Co&#46;: ###
On Windows and GNU/Linux where Python 3 is the default interpreter, use the shell/command-line command:
```sh
$ python main.py
```
On GNU/Linux with Python 3 as the non-default interpreter, use the shell/command-line command:
```sh
$ python3 main.py
```

For more startup options add the ```--help``` or ```-h``` flag.
<br><br>

### Quick examples: ###
__1. Basic text manipulation with the REPL (very detailed example):__
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
     - __All commands in the REPL must be valid Python 3 code!__
     - ```line_list``` __is implemented as a python list so most list operations apply to it: append, insert, sort, ...__


__2. Manipulate editor lines using the REPL:__
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


__3. Text diffing example:__
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


__4. Moving tabs from window to window:__
   - focus the main editor window
   - create a new document (```Ctrl+N```)
   - press ```Shift``` and left click-and-hold on the new documents tab
   - drag the mouse into the upper editor window and release the left mouse button
   - the document has now moved to the upper editor window
   - __Copying is the same except you hold down the__ ```Ctrl``` __button__


__5. Adding your custom Python functions:__
   - open the __user_functions__ file by:
     - use the menubar by selecting ```File -> Edit User Functions```
     - use the 'Function Wheel' by pressing ```F1``` and selection the ```Edit User Functions``` icon
   - the __user_functions__ file will open in the main editor window
   - add your Python (Python 3) function to the file and add the custom autocompletion for the function:
   - Example: 
      ```python
      
          def my_custom_function():
              # custom function code
          my_custom_function.autocompletion = 'my_custom_function()'
      ```
   - save the file with one of the following options:
     - press ```Ctrl+S```
     - use the menubar by selecting ```File -> Save```
     - use the 'Function Wheel' by pressing ```F1``` and selection the ```Save``` icon
   - reload user functions with one of the following options:
     - use the menubar by selecting ```File -> Reload User Functions```
     - use the 'Function Wheel' by pressing ```F1``` and selection the ```Reload User Functions``` icon
   - try your newly added function by focusing the REPL (```Ctrl+R```) and start typing the name of your added function, it should automatically add the rest of the function text into the REPL
   - __NOTE:__
     - __if your function name is similar to another already defined function, press__ ```Tab``` __to scroll through all of the similar named function until you reach the newly added one__


__6. Run a terminal/shell command from Ex&#46;Co&#46;:__
   - focus the REPL (```Ctrl+R```)
   - select the run command with one of the following options:
     - use the menubar by selecting ```System -> Run command```
     - use the 'Function Wheel' by pressing ```F1``` and selection the ```Run Console Command``` icon
   - the REPL should now have the text ```run("",show_console=True)``` in it
   - run the command like ```dir``` by entering it into the REPL text: ```run("dir",show_console=True)``` and press ```Enter```
   - a new terminal window will popup and show the output of the ```dir``` command
   - __NOTE:__
     - __insted of the menubar or function wheel shortcuts, you can also use the shorthand for running terminal commands with the REPL command__ ```rc: ```. __The above example using the shorthand would be:__ ```rc: dir``` __(note that there should be no quotes or double-quotes)__

<br><br>

### Todo: ###
- add a curses version of Ex&#46;Co&#46; (only an idea at the moment)
