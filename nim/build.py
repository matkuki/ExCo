
import os
import subprocess
import shutil
import platform

current_platform = platform.system()

if current_platform == "Windows":
    
    commands = []
#    commands.append('CALL "C:\\Program Files (x86)\\Microsoft Visual Studio 10.0\\VC\\vcvarsall.bat" amd64')
    commands.append('CALL "C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Auxiliary\Build\vcvars64.bat"')
    commands.append('C:\\Nim64\\bin\\nim.exe cc --compileOnly --cc:vcc -d:py3_version=3.6 -d:py3_static --noLinking --header:nim_lexers.h nim_lexers.nim')
    commands.append('python setup.py build_ext --inplace')
    
    p = subprocess.Popen(" & ".join(commands), shell=True)
    p.wait()

else:
    
    commands = []
    commands.append('nim cc --app:lib --compileOnly --cc:gcc -d:py3_version=3.5 -d:py3_static --noLinking --header:nim_lexers.h nim_lexers.nim')
    commands.append('python3 setup.py build_ext --inplace')
    
    for c in commands:
        os.system(c)