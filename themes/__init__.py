
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2018 Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""
# Import the themes so that they can be imported directly from the package,
# instead of 'import themes.air.Air'.
import themes.air as Air
import themes.earth as Earth
import themes.water as Water
import themes.mc as MC

theme_list = [
    Air,
    Earth,
    Water,
    MC,
]