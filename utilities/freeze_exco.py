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
import importlib.util
import platform
from typing import Set, List, Dict

import cx_Freeze


def get_all_imports() -> Dict[str, List[str]]:
    """
    Import exco.py and collect all third-party module imports.
    Returns a dict with 'modules' and 'packages' lists.
    - 'modules': Single file modules (.py files)
    - 'packages': Packages with __init__.py (directories)
    """
    project_dir: str = os.path.dirname(os.path.abspath(__file__))
    parent_dir: str = os.path.dirname(project_dir)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)

    before: Set[str] = set(sys.modules.keys())

    try:
        import exco  # type: ignore
    except Exception:
        pass

    after: Set[str] = set(sys.modules.keys())
    new_modules: Set[str] = after - before

    # Test each import to determine if it's a module or package
    modules: List[str] = []
    packages: List[str] = []

    for mod_name in new_modules:
        # Try to find the module/package
        try:
            spec = importlib.util.find_spec(mod_name)
        except (ValueError, ModuleNotFoundError):
            # Some modules have None __spec__ and raise ValueError
            continue

        if spec is None:
            continue

        if spec.submodule_search_locations is None:
            # It's a module (single .py file)
            modules.append(mod_name)
        else:
            # It's a package (has __init__.py)
            packages.append(mod_name)

    return {
        "modules": sorted(modules),
        "packages": sorted(packages),
    }


def main() -> int:
    """
    Main function to build the ExCo application using cx_Freeze.
    Returns exit code (0 = success).
    """
    # Get the project directory (parent of utilities/)
    file_directory: str = os.path.join(
        os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))),
        "..",
    )

    # Output directory name based on OS and architecture
    output_directory: str = "frozen_exco_{}_{}".format(
        platform.system().lower(),
        platform.architecture()[0],
    )

    # Get all imports and separate into modules vs packages
    import_result: Dict[str, List[str]] = get_all_imports()
    includes: List[str] = import_result["modules"]
    packages_list: List[str] = import_result["packages"]

    # Add PyQt6 to packages (needed for proper freezing)
    packages_list.append("PyQt6")

    # Directories to exclude when scanning for local modules
    exclude_dirs: list[str] = [
        "cython",
        "utilities",
        "nim",
        "git_clone",
    ]

    # Specific modules to exclude
    excluded_modules: list[str] = [
        "freeze_exco",
        "git_clone",
    ]

    # Add project directory to Python path
    search_path: list[str] = sys.path
    search_path.append(file_directory)

    # Base type for executable (None = console app)
    base: str | None = None
    excludes: list[str] = [
        "tkinter",
    ]
    executable_name: str = "ExCo"

    # Platform-specific configuration
    if platform.system().lower() == "windows":
        base = "gui"  # GUI app without console

        # Exclude PyQt5 modules to avoid conflicts
        excludes = [
            "tkinter",
            "PyQt5",
            "PyQt5.QtCore",
            "PyQt5.QtWidgets",
            "PyQt5.QtGui",
            "PyQt5.Qsci",
            "PyQt5.QtTest",
            "venv",
        ]

        executable_name = "ExCo.exe"

    elif platform.system().lower() == "linux":
        # Add Linux-specific includes
        includes.extend(["ptyprocess"])

    # Define the executable to create
    executables: list[cx_Freeze.Executable] = [
        cx_Freeze.Executable(
            "exco.py",
            init_script=None,
            base=base,
            icon="resources/exco-icon-win.ico",
            target_name=executable_name,
        )
    ]

    # Configure and run the freezer
    freezer: cx_Freeze.Freezer = cx_Freeze.Freezer(
        executables,
        includes=includes,
        packages=packages_list,
        excludes=excludes,
        replace_paths=[],
        compress=True,
        optimize=True,
        include_msvcr=True,
        path=search_path,
        target_dir=output_directory,
        include_files=[],
        zip_includes=[],
        silent=False,
    )
    freezer.freeze()

    # Copy resources directory to output
    shutil.copytree("resources", output_directory + "/resources")

    return 0


if __name__ == "__main__":
    sys.exit(main())
