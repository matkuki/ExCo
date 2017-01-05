
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2017 Matic Kukovec. 
Release under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""


import os
import data
import importlib.machinery

base_directory = os.path.dirname(os.path.realpath(__file__))
air_directory = os.path.join(base_directory, 'air.py')
earth_directory = os.path.join(base_directory, 'earth.py')
water_directory = os.path.join(base_directory, 'water.py')
mc_directory = os.path.join(base_directory, 'mc.py')

Air = importlib.machinery.SourceFileLoader('Air', air_directory).load_module()
Earth = importlib.machinery.SourceFileLoader('Earth', earth_directory).load_module()
Water = importlib.machinery.SourceFileLoader('Water', water_directory).load_module()
MC = importlib.machinery.SourceFileLoader('MC', mc_directory).load_module()

"""
For backwards compatibility
"""
air = Air
earth = Earth
water = Water
mc = MC


