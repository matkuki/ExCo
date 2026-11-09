"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import qt
import data
import functions
import re
import math
import typing
import gui.menu


class ActionFilter(qt.QObject):
    """
    Object for connecting to the menubar events and filtering
    the click&drag event for the context menu
    """

    # Timers
    click_timer: qt.QTimer | None = None
    reset_timer: qt.QTimer | None = None
    click_drag_action: qt.QAction | None = None

    # Overridden filter method
    def eventFilter(  # type: ignore[override]
        self, receiver: qt.QMenu, event: qt.QEvent
    ) -> bool:
        if event.type() == qt.QEvent.Type.MouseButtonPress:
            cursor = qt.QCursor.pos()
            cursor = cursor - receiver.pos()
            action = receiver.actionAt(cursor)
            if action is not None:
                pixmap = getattr(action, "pixmap", None)
                if pixmap is None:
                    return super().eventFilter(receiver, event)

                # Create the click&drag detect timer
                def click_and_drag() -> None:
                    def hide_parents(obj: qt.QWidget) -> None:
                        obj.hide()
                        parent = obj.parent()
                        if parent is not None and isinstance(parent, gui.menu.Menu):
                            hide_parents(parent)

                    hide_parents(receiver)
                    ActionFilter.click_timer = None
                    if pixmap is not None:
                        cursor = qt.QCursor(pixmap)
                        data.application.setOverrideCursor(cursor)
                        ActionFilter.click_drag_action = action

                ActionFilter.click_timer = qt.QTimer(self)
                ActionFilter.click_timer.setInterval(400)
                ActionFilter.click_timer.setSingleShot(True)
                ActionFilter.click_timer.timeout.connect(click_and_drag)
                ActionFilter.click_timer.start()
        elif event.type() == qt.QEvent.Type.MouseButtonRelease:
            ActionFilter.clear_action()
        return super().eventFilter(receiver, event)

    @staticmethod
    def clear_action() -> None:
        data.application.restoreOverrideCursor()
        click_timer = ActionFilter.click_timer
        reset_timer = ActionFilter.reset_timer
        if click_timer != None:
            click_timer.stop()
            click_timer = None
        if reset_timer != None:
            reset_timer.stop()
        ActionFilter.click_drag_action = None
