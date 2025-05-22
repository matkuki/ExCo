"""
Copyright (c) 2013-present Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import os
import sys
import pprint
import shutil
import inspect
import platform
import cx_Freeze


def main():
    file_directory = os.path.join(
        os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))),
        "..",
    )
    output_directory = "frozen_exco_{}_{}".format(
        platform.system().lower(),
        platform.architecture()[0],
    )
    
    builtin_modules = [
        "PyQt6",
        "PyQt6.Qsci",
        "PyQt6.QtTest",
        "pyte",
        "hy",
        "hy.core",
        "hy.core.result_macros",
        "black",
        "autopep8",
        "yapf",
        "fpdf",
    ]
    local_modules = []
    # List all local modules
    exclude_dirs = [
        'cython',
        'nim',
        'utilities',
        'git_clone',
    ]
    excluded_modules = [
        'freeze_exco',
        'git_clone',
    ]
    for root, dirs, files in os.walk(file_directory):
        base_path = os.path.join(root).replace(file_directory, "")
        if base_path.startswith('/'):
            base_path = base_path[1:]
        if any([x in base_path for x in exclude_dirs]):
            continue
        for f in files:
            if f.endswith('.py'):
                raw_module = f.replace('.py', '') \
                    .replace('.pyd', '') \
                    .replace('.so', '')
                raw_module = raw_module.split('.')[0]
                new_module = f'{base_path}/{raw_module}'
                if new_module.startswith('\\') or new_module.startswith('/'):
                    new_module = new_module[1:]
                new_module = new_module.replace('\\', '.').replace('/', '.')
                if new_module in excluded_modules:
                    continue
                local_modules.append(new_module)
    pprint.pprint(local_modules)
    
    modules = local_modules + builtin_modules
    
    search_path = sys.path
    search_path.append(file_directory)
    
    base = None
    excludes = [
        "tkinter",
    ]
    executable_name = "ExCo"
    if platform.system().lower() == "windows":
        base = "Win32GUI"
        
        builtin_modules.extend([
            "win32api",
            "win32con",
            "win32gui",
            "win32file",
            "winpty"
        ])
        
        excludes = [
            "tkinter",
            "PyQt5",
            "PyQt5.QtCore",
            "PyQt5.QtWidgets",
            "PyQt5.QtGui",
            "PyQt5.Qsci",
            "PyQt5.QtTest",
#            "PyQt6",
#            "PyQt6.QtCore",
#            "PyQt6.QtWidgets",
#            "PyQt6.QtGui",
#            "PyQt6.Qsci",
#            "PyQt6.QtTest",
        ]
        
        executable_name = "ExCo.exe"
    
    elif platform.system().lower() == "linux":
        builtin_modules.extend([
            "ptyprocess",
        ])
    
    executables = [
        cx_Freeze.Executable(
            'exco.py',
            init_script = None,
            base = base,
            icon = "resources/exco-icon-win.ico",
            target_name = executable_name,
        )
    ]
    
    freezer = cx_Freeze.Freezer(
        executables,
        includes = modules,
        excludes = excludes,
        replace_paths = [],
        compress = True,
        optimize = True,
        include_msvcr = True,
        path = search_path,
        target_dir = output_directory,
        include_files = [],
        zip_includes = [],
        silent = False,
    )
    freezer.freeze()
    
    shutil.copytree("resources", output_directory + "/resources")


if __name__ == "__main__":
    main()