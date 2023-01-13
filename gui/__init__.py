
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2023 Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

## Explicit
from .baseeditor import *
from .contextmenu import *
from .custombuttons import *
from .customeditor import *
from .dialogs import *
from .dockingoverlay import *
from .excoinfo import *
from .functionwheel import *
from .mainwindow import *
from .menu import *
from .messagelogger import *
from .plaineditor import *
from .replbox import *
from .replhelper import *
from .repllineedit import *
from .sessionguimanipulator import *
from .settingsguimanipulator import *
from .stylesheets import *
from .tabwidget import *
from .templates import *
from .textdiffer import *
from .thebox import *
from .themeindicator import *
from .treedisplays import *


## Dynamic
#import os
#import importlib
#
#path = os.path.dirname(os.path.abspath(__file__))
#for m in os.listdir(path):
#    if m.startswith("__"):
#        continue
#    module_name = ".{}".format(m.replace(".pyc", '').replace(".pyd", '').replace(".py", ''))
#    module = importlib.import_module(module_name, "gui")
#    globals().update(
#        {n: getattr(module, n) for n in module.__all__} if hasattr(module, '__all__') 
#        else 
#        {k: v for (k, v) in module.__dict__.items() if not k.startswith('_')
#    })
