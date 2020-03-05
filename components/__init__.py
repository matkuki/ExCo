
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2019 Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

## Explicit
#from .actionfilter import *
#from .customstyle import *
#from .gridgenerator import *
#from .hexbuilder import *
#from .hotspots import *
#from .iconmanipulator import *
#from .linelist import *
#from .thesquid import *

## Dynamic
import os
import importlib

path = os.path.dirname(os.path.abspath(__file__))
for m in os.listdir(path):
    if m.startswith("__"):
        continue
    module_name = "components.{}".format(m.replace(".py", ''))
    module = importlib.import_module(module_name)
    globals().update(
        {n: getattr(module, n) for n in module.__all__} if hasattr(module, '__all__') 
        else 
        {k: v for (k, v) in module.__dict__.items() if not k.startswith('_')
    })
