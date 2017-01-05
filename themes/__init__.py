
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2017 Matic Kukovec. 
Release under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""


"""
This way does not work with the new way themes are reloaded in:
'forms.MainWindow.View.reload_themes'
---------------------------------------------------------------
"""
#import themes.air as Air
#import themes.earth as Earth
#import themes.water as Water
#import themes.mc as MC
"""
---------------------------------------------------------------
"""

import importlib.machinery
Air = importlib.machinery.SourceFileLoader('Air','themes/air.py').load_module()
Earth = importlib.machinery.SourceFileLoader('Earth','themes/earth.py').load_module()
Water = importlib.machinery.SourceFileLoader('Water','themes/water.py').load_module()
MC = importlib.machinery.SourceFileLoader('MC','themes/mc.py').load_module()

