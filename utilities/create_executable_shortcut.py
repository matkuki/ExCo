"""
Copyright (c) 2013-present Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import os
import sys
import shutil
import subprocess

# Check if we are on Windows
if sys.platform != "win32":
    print("We are not on Windows!")
    sys.exit(1)
# Check if Nim is installed
output = subprocess.check_output(['nim']).decode("utf-8")
if output.startswith("Nim Compiler Version") == False:
    print("Nim is not installed on the system!")
    sys.exit(1)

# Copy the icon to this script's location
shutil.copy("../resources/exco-icon-win.ico", "exco-icon-win.ico")

with open("exco.rs", "w+") as f:
    f.write('0 ICON "exco-icon-win.ico"')
    f.close()

with open("exco.nim", "w+") as f:
    f.write(
"""
#[
    Compile with:
        nim c --out:ExCo.exe --passL:exco.res exco.nim
]#

import os
import ospaths
import osproc

# Parse the arguments
let arguments = os.commandLineParams()
let main_script_path = ospaths.joinPath(
    ospaths.parentDir(os.getAppFilename()), "exco.py"
)
echo main_script_path
var parameters = @[main_script_path]
for arg in arguments:
    parameters.add(arg)
# Run ExCo process
discard osproc.startProcess(
    command="C:/Program Files/Python313/pythonw.exe",
    workingDir="",
    args=parameters,
    env=nil
)
"""
    )
    f.close()

# Create the resource file
os.system("windres exco.rs -O coff -o exco.res")
# Compile with Nim and pass the resource file to the underlying C compiler
os.system('nim c --app:gui --out:ExCo.exe --passL:exco.res exco.nim')

# Clean up
os.remove("exco.rs")
os.remove("exco.res")
os.remove("exco.nim")
os.remove("exco-icon-win.ico")
#shutil.rmtree("nimcache/")
