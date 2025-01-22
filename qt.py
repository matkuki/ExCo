# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-present Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

"""
PyQt4 / PyQt5 / PyQt6 selection

NOTE:
    Objects are imported so that they can be used either directly with qt.QSize,
    or by specifiying the full namespace with qt.PyQt.QtCore.QSize!
"""
try:
    import PyQt6.Qsci
    import PyQt6.QtCore
    import PyQt6.QtGui
    import PyQt6.QtWidgets
    PyQt = PyQt6
    from PyQt6.Qsci import *
    from PyQt6.QtCore import *
    from PyQt6.QtGui import *
    from PyQt6.QtWidgets import *
    PYQT_MODE = 6
except:
    try:
        import PyQt5.Qsci
        import PyQt5.QtCore
        import PyQt5.QtGui
        import PyQt5.QtWidgets
        PyQt = PyQt5
        from PyQt5.Qsci import *
        from PyQt5.QtCore import *
        from PyQt5.QtGui import *
        from PyQt5.QtWidgets import *
        PYQT_MODE = 5
    except:
        import PyQt4.Qsci
        import PyQt4.QtCore
        import PyQt4.QtGui
        PyQt = PyQt4
        from PyQt4.Qsci import *
        from PyQt4.QtCore import *
        from PyQt4.QtGui import *
        PYQT_MODE = 4