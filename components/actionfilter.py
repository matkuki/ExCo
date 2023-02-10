# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2023 Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import data
import functions
import re
import math
import typing
import gui.menu


class ActionFilter(data.QObject):
    """
    Object for connecting to the menubar events and filtering
    the click&drag event for the context menu
    """
    # Timers
    click_timer = None
    reset_timer = None
    click_drag_action = None
    
    # Overridden filter method
    def eventFilter(self, receiver, event):
        if(event.type() == data.QEvent.Type.MouseButtonPress):
            cursor = data.QCursor.pos()
            cursor = cursor - receiver.pos()
            if receiver.actionAt(cursor) != None:
                action = receiver.actionAt(cursor)
                if hasattr(action, "pixmap") and action.pixmap is None:
                    return super().eventFilter(receiver, event)
#                print(action.text())
                # Create the click&drag detect timer
                def click_and_drag():
                    def hide_parents(obj):
                        obj.hide()
                        if obj.parent() != None and (isinstance(obj.parent(), gui.menu.Menu)):
                            hide_parents(obj.parent())
                    hide_parents(receiver)
                    ActionFilter.click_timer = None
                    if hasattr(action, "pixmap"):
                        cursor = data.QCursor(
                            action.pixmap
                        )
                        data.application.setOverrideCursor(cursor)
                        ActionFilter.click_drag_action = action
                ActionFilter.click_timer = data.QTimer(self)
                ActionFilter.click_timer.setInterval(400)
                ActionFilter.click_timer.setSingleShot(True)
                ActionFilter.click_timer.timeout.connect(click_and_drag)
                ActionFilter.click_timer.start()
        elif(event.type() == data.QEvent.Type.MouseButtonRelease):
            ActionFilter.clear_action()
        return super().eventFilter(receiver, event)

    @staticmethod
    def clear_action():
        data.application.restoreOverrideCursor()
        click_timer = ActionFilter.click_timer
        reset_timer = ActionFilter.reset_timer
        if click_timer != None:
            click_timer.stop()
            click_timer = None
        if reset_timer != None:
            reset_timer.stop()
        ActionFilter.click_drag_action = None