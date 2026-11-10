"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

##  FILE DESCRIPTION:
##      Module that holds objects that will be used across modules.

import argparse
import enum
import inspect
import os
import pathlib
import platform as platform_module
import sys
from typing import Any

import qt
from constants import *

# File directory reference
file_directory: str
if getattr(sys, "frozen", False):
    # The application is frozen
    file_directory = os.path.dirname(sys.executable)
else:
    # The application is not frozen
    current_frame = inspect.currentframe()
    assert current_frame is not None
    file_directory = os.path.dirname(os.path.abspath(inspect.getfile(current_frame)))

"""
--------------------------------------------------------
Various stored settings for global use.
These are the DEFAULT values, override them in the user
configuration file!
--------------------------------------------------------
"""
application_version = "7.17.33"
# Global variables
command_line_options: argparse.Namespace | None = None
debug_mode: bool = False
logging_mode: bool = False
# Global referenc to the log display window, so it can be used anywhere
log_window: Any = None
# Global reference to the Qt application
application: Any = None
# Global string with the application directory
application_directory: str = file_directory.replace("\\", "/")
# Home directory
home_directory: str
try:
    home_directory = os.path.realpath(str(pathlib.Path.home())).replace("\\", "/")
except:
    home_directory = os.path.expanduser("~")
# Global string with the resources directory
resources_directory: str = os.path.join(application_directory, "resources").replace(
    "\\", "/"
)
# Global settings directory
settings_directory: str = os.path.join(home_directory, ".exco").replace("\\", "/")
# Fonts directory
fonts_directory: str = os.path.join(resources_directory, "fonts/").replace("\\", "/")
# Global string variable for the current platform name ("Windows", "Linux", ...),
# and a flag if running on the Raspberry PI
platform: str = platform_module.system()
on_windows: bool = platform == "Windows"
on_linux: bool = platform == "Linux"
on_rpi: bool = False
if os.name == "posix":
    on_rpi = getattr(os, "uname")()[1] == "raspberrypi"
# User configuration file
config_file: str = os.path.join(settings_directory, "userfunctions.cfg").replace(
    "\\", "/"
)
# Global signal dispatcher
signal_dispatcher: Any = None
# Application icon image that will be displayed on all Qt widgets
application_icon: str = os.path.join(resources_directory, "exco-icon.png").replace(
    "\\", "/"
)
# Ex.Co. information image displayed when "About Ex.Co"
# action is clicked in the menubar "Help" menu
about_image: str = os.path.join(resources_directory, "exco-info.png").replace("\\", "/")

# Show PyQt/QScintilla version that is being used and if running in
# QScintilla compatibility mode
LIBRARY_VERSIONS: str = "PyQt{} / QScintilla{}".format(
    qt.PyQt.QtCore.PYQT_VERSION_STR, qt.PyQt.Qsci.QSCINTILLA_VERSION_STR
)

# Store all Qt keys as a dictionary
keys: dict[int, str] = {}

global_function_information: dict[str, Any] = {}

for k in dir(qt.Qt.Key):
    if k.startswith("Key_"):
        value = getattr(qt.Qt.Key, k)
        keys[value] = k
