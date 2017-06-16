
import os
import subprocess
import shutil
import platform

current_platform = platform.system()

if current_platform == "Windows":
    
    commands = []
    commands.append('CALL "C:\\Program Files (x86)\\Microsoft Visual Studio 10.0\\VC\\vcvarsall.bat" amd64')
    commands.append('C:\\Nim64\\bin\\nim.exe cc --compileOnly -d:py3_version=3.4 -d:py3_static --noLinking --header:nim_lexers.h nim_lexers.nim')
    commands.append('python setup.py build_ext --inplace')
    
    p = subprocess.Popen(" & ".join(commands), shell=True)
    p.wait()

else:
    
    commands = []
    commands.append('nim cc --app:lib --compileOnly -d:py3_version=3.5 -d:py3_static --noLinking --header:nim_lexers.h nim_lexers.nim')
    commands.append('python3 setup.py build_ext --inplace')
    
    for c in commands:
        os.system(c)