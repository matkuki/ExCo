"""
Copyright (c) 2013-present Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

##  FILE DESCRIPTION:
##      Setup file for the Cython module
##      NOTES:
##          Build the Cython module with:
##              "python cython_setup.py build_ext --build-lib=cython_build/"

import shutil
import os
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import build_ext

# Clean-up
print("Pre-build clean-up started ...")
if os.path.exists('cython_build'):
    shutil.rmtree('cython_build')
if os.path.exists('build'):
    shutil.rmtree('build')
filelist = [f for f in os.listdir(".") if f.endswith(".c")]
for f in filelist:
    os.remove(f)
print("Pre-build clean-up completed.")

source_files = [
    "cython_lexers.pyx"
]

ext_modules = [
    Extension(  
        "cython_lexers",
        source_files,
        include_dirs = [],
        libraries = [],
        library_dirs = []
    )
]

setup(
    name = 'Ex.Co. Cython extensions',
    cmdclass = {
        'build_ext':    build_ext,
    },
    ext_modules = ext_modules
)

# Clean-up
#print("Post-build clean-up started ...")
#if os.path.exists('build'):
#    shutil.rmtree('build')
#filelist = [f for f in os.listdir(".") if f.endswith(".c")]
#for f in filelist:
#    os.remove(f)
#print("Post-build clean-up completed.")
#
#print("Kopiranje cython_lexers.pyd datoteke ...")
#shutil.copyfile(
#    'D:/Domaci_Projekti/ExCoEdit/cython_build/cython_lexers.pyd', 
#    "D:/Domaci_Projekti/razno_za_exco/Testiranje/cython_lexers.pyd"
#)

