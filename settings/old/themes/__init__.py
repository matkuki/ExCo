
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2018 Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""
# Import the themes so that they can be imported directly from the package,
# instead of 'import themes.air.Air'.
from . import air as Air
from . import earth as Earth
from . import water as Water
from . import mc as MC

theme_list = [
    Air,
    Earth,
    Water,
    MC,
]