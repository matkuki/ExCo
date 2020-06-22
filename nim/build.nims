
#[
    Copyright (c) 2020 Matic Kukovec. 
]#

import os
import strutils
import strformat

mode = ScriptMode.Verbose

var output_executable: string

if defined(windows) or defined(linux):
    output_executable = "nim_lexers.pyd"
else:
    output_executable = "nim_lexers.so"
    
var
    cwd = currentSourcePath().parentDir()
    commands = [
        fmt"nim c --threads:on --app:lib --out:{output_executable} --d:release -d:danger nim_lexers",
    ]
exec commands.join(" & ")
cpFile(joinPath(cwd, output_executable), joinPath(cwd, "..", output_executable))