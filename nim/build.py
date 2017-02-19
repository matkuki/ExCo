

#call "C:\Program Files (x86)\Microsoft Visual Studio 10.0\VC\vcvarsall.bat" amd64
#C:\Nim64\bin\nim.exe c --noMain --noLinking --header:nim_lexers.h nim_lexers.nim
#python setup.py build_ext --inplace

import os
import subprocess
import shutil

#os.system('"C:\\Program Files (x86)\\Microsoft Visual Studio 10.0\\VC\\vcvarsall.bat" amd64')
#os.system('C:\\Nim64\\bin\\nim.exe c --noMain --noLinking --header:nim_lexers.h nim_lexers.nim')
#os.system('python setup.py build_ext --inplace')

commands = []
commands.append('CALL "C:\\Program Files (x86)\\Microsoft Visual Studio 10.0\\VC\\vcvarsall.bat" amd64')
commands.append('C:\\Nim64\\bin\\nim.exe c --noMain --noLinking --header:nim_lexers.h nim_lexers.nim')
commands.append('python setup.py build_ext --inplace')

p = subprocess.Popen(" & ".join(commands), shell=True)
p.wait()

shutil.copyfile(
    "C:/Users/Matic/Desktop/NIMROD/exco_lexers/nim_lexers.pyd",
    "D:/Domaci_Projekti/ExCoEdit/nim_lexers.pyd"
)
print("nim_lexers.pyd kopiran.")