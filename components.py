
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2017 Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

##  FILE DESCRIPTION:
##      All modular components used in various objects

import data
import forms
import helper_forms
import re
import platform


class IconManipulator:
    """
    Icon manipulator for a widget inside a basic widget
    """
    
    def set_icon(self, obj, icon):
        """
        Set the current icon and update it by sending the signal to the 
        parent basic widget
        """
        obj.current_icon = icon
        self.update_icon(obj)
    
    def update_icon(self, obj):
        """
        Update the current icon and update it by sending the signal to the 
        parent basic widget
        """
        if isinstance(obj, forms.CustomEditor):
            obj_parent = obj.parent
            if isinstance(obj_parent, forms.BasicWidget):
                obj_parent.update_tab_icon(obj)
                obj.show_corner_widget()
            elif isinstance(obj_parent, helper_forms.TextDiffer):
                obj_parent.parent.update_tab_icon(obj)
        elif isinstance(obj, forms.PlainEditor):
            obj_parent = obj.parent
            if isinstance(obj_parent, forms.BasicWidget):
                obj_parent.update_tab_icon(obj)
        elif hasattr(obj, "parent") and obj.current_icon != None:
            obj.parent.update_tab_icon(obj)
    
    def update_corner_widget(self, obj, basic_widget):
        result = True
        if isinstance(obj, forms.CustomEditor) == True:
            # Display the 'change lexer' button in the upper right corner of the tab
            obj.show_corner_widget()
        elif isinstance(obj, helper_forms.TextDiffer) == True:
            # Display special find buttons if the current tab is text differ
            obj.show_find_buttons(basic_widget)
        elif isinstance(obj, helper_forms.SessionGuiManipulator) == True:
            # Display the special session buttons
            obj.show_session_buttons(basic_widget)
        elif isinstance(obj, forms.PlainEditor) == True:
            # Display the repl clear button if it's applicable
            obj.show_repl_corner_widget()
        else:
            result = False
        return result


class LineList(list):
    """
    List object that will hold the lines of the CustomEditor.
    It's a subclassed Python built-in list object for easier text manipulation.
    """
    #Class variables
    parent = None
    
    """
    Class functions/methods
    """
    def __init__(self, parent, initial_text):
        """Overridden init function"""
        #Initialize superclass
        super().__init__()
        #Set the reference to the parent object
        self.parent = parent
        #Check if initial text is valid
        if initial_text:
            #Update the list of lines
            self.update_text_to_list(initial_text)

    def __getitem__(self, key):
        """Overridden list method that returns the specified line(item)"""
        #Check if the value is an int or a slice
        if isinstance(key, int):
            #Create a new key variable, because key is ReadOnly
            actual_key = key
            #Check if the key is lower than 1
            if actual_key == 0:
                actual_key = 1
            #Check if the key is greater than 0
            if actual_key > 0:
                actual_key -= 1
            #Return the line string
            return super().__getitem__(actual_key)
        elif isinstance(key, slice):
            #Create new key variables, because key is ReadOnly
            key_min     = key.start
            key_max     = key.stop
            #Check the lower bound of the slice is 0
            if key_min == None:
                key_min = 0
            #Check if the key is greater than 0
            if key_min > 0:
                key_min -= 1
            key_slice = slice(key_min, key_max)
            return super().__getitem__(key_slice)
        #The key is an invalid type
        return None

    def __setitem__(self, key, value):
        """Overridden list method that sets the specified line(item) to a value"""
        #Check if the value is a string or a list
        if isinstance(value, str) == False and isinstance(value, list) == False:
            raise Exception("Value has to be a list or a string!")
        #Check if the value is a string or a list
        if isinstance(value, str):
            #Try to set the line
            try:
                #Create a new key variable, because key is ReadOnly
                actual_key = key
                #Check if the key is 0
                if actual_key == 0:
                    actual_key = 1
                #Check if the key is greater than 0
                if actual_key > 0:
                    actual_key -= 1
                #Set the line
                super().__setitem__(actual_key, value)
            except:
                self.append(value, update_parent=False)
            #Update the custom editor document text
            self.parent.set_line(value, key)
        else:
            #The value is a list
            #Create new key variables, because key is ReadOnly
            key_min     = key.start
            key_max     = key.stop
            #Check if the lower boundary of the slice is 0
            if key_min == 0:
                key_min = 1
            #Check boundary order
            if key_max < key_min:
                raise Exception("First index has to be higher than the second!")
            #Check the boundaries
            if len(value) != (key_max-key_min+1):
                raise Exception("Ranges of assignment don't match!")
            #Insert the range into the custom list object
            super().__setitem__(slice(key_min-1, key_max), value)
            #Adjust the line numbers to standard(0..lines()-1) numbering
            line_from   = key_min - 1
            line_to     = key_max - 1
            #Set the new lines in the custom editor document
            self.parent.set_lines(line_from, line_to, value)
    
    def __iadd__(self, value):
        """Overloaded '+=' operator"""
        raise Exception("'+=' operator not implemented yet!")
    
    def __isub__(self, value):
        """Overloaded '-=' operator"""
        raise Exception("'-=' operator not implemented yet!")
    
    def __imul__(self, value):
        """Overloaded '*=' operator"""
        raise Exception("'*=' operator not implemented yet!")

    def _setitem(self, key, value):
        """Set the item at position-key, without updating the scintilla document"""
        #Check if the value is a string
        if isinstance(value, str) == False:
            return
        #Try to set the line
        try:
            #Create a new key variable, because key is ReadOnly
            actual_key = key
            #Check if the key is 0
            if actual_key == 0:
                actual_key = 1
            #Check if the key is greater than 0
            if actual_key > 0:
                actual_key -= 1
            #Set the line
            super().__setitem__(actual_key, value)
        except:
            self.append(value, update_parent=False)
    
    def _update_list_to_text(self, scroll_to_line=None):
        """Update the list of lines to the parent CustomEditor document"""
        #Merge the list into a single string with the
        #newline character as the delimiter
        text = "\n".join(self)
        #Update the text of the document
        self.parent.set_all_text(text)
        #Check if a line to which to scroll to was specified
        if scroll_to_line == None:
            scroll_to_line = self.parent.lines()
        #Scroll to the desired line of the document
        self.parent.setCursorPosition(scroll_to_line, 0)
    
    def append(self, value, update_parent=True):
        """
        Overloaded list append method
        Special arguments:
            update_parent   - False: append to list internally without updating
                                     the parent CustomEditor document.
                              True:  append to list and update the parent
                                     CustomEditor document.
        """
        #Check the update_parent parameter type
        if isinstance(update_parent, bool) == False:
            raise Exception("'update_parent' parameter must be of type boolean!")
        #Check the append value type
        if isinstance(value, str):
            #Execute the superclass append method
            super().append(value)
        elif isinstance(value, list):
            exception_text = "Use 'extend' to add multiple lines!"
            raise Exception(exception_text)
        else:
            exception_text = "'append' parameter must be a string!"
            raise Exception(exception_text)
        #Check if updating the parent document is needed
        if update_parent == True:
            self._update_list_to_text()
    
    def extend(self, value, update_parent=True):
        """
        Overloaded list extend method
        Special arguments:
            update_parent   - False: append to list internally without updating
                                     the parent CustomEditor document.
                              True:  append to list and update the parent
                                     CustomEditor document.
        """
        #Check the update_parent parameter type
        if isinstance(update_parent, bool) == False:
            raise Exception("'update_parent' parameter must be of type boolean!")
        #Check the extend value type
        if isinstance(value, list) == False:
            raise Exception("Extend parameter must be a list!")
        elif all(isinstance(item, str) for item in value) == False:
            raise Exception("All extend list items must be strings!")
        #Extend the list
        super().extend(value)
        #Check if updating the parent document is needed
        if update_parent == True:
            self._update_list_to_text()
    
    def insert(self, index, value, update_parent=True):
        """Overloaded insert method"""
        #Check the insert index type
        if isinstance(index, int) == False:
            raise Exception("Insert index parameter must be an integer!")
        #Check the insert value type
        if isinstance(value, str) == False:
            raise Exception("Insert parameter must be a string!")
        #Correct and check the index
        index -= 1
        if index < 0:
            index = 0
        #Insert the item
        super().insert(index, value)
        #Check if updating the parent document is needed
        if update_parent == True:
            self._update_list_to_text(index)
    
    def pop(self, index=None, update_parent=True):
        """Overloaded pop method"""
        #Check the insert index type
        if isinstance(index, int) == False:
            raise Exception("Pop index parameter must be an integer!")
        #Correct and check the index
        index -= 1
        if index < 0:
            index = 0
        #Pop out the item
        return_item = super().pop(index)
        #Check if updating the parent document is needed
        if update_parent == True:
            self._update_list_to_text(index)
        #Return the poped line
        return return_item
    
    def remove(self, item, update_parent=True):
        """Overloaded remove method"""
        #Check the insert index type
        if isinstance(item, str) == False:
            raise Exception("Remove item parameter must be a string!")
        #Check if item exists
        if not(item in self):
            raise Exception("Cannot remove item! Item is not in the list!")
        else:
            index = self.index(item) - 1
            #Check the index
            if index < 0:
                index = 0    
        #Remove the item
        super().remove(item)
        #Check if updating the parent document is needed
        if update_parent == True:
            self._update_list_to_text(index)
    
    def reverse(self, update_parent=True):
        """Overloaded reverse method"""
        #Reverse the list
        super().reverse()
        #Check if updating the parent document is needed
        if update_parent == True:
            self._update_list_to_text()
        
    def sort(self, update_parent=True):
        """Overloaded sort method"""
        #Sort the list
        super().sort()
        #Check if updating the parent document is needed
        if update_parent == True:
            self._update_list_to_text()
    
    def update_text_to_list(self, update_text):
        """Update the list from a string"""
        #Check if the value is a string
        if isinstance(update_text, str) == False:
            return
        #Empty the list
        self._clear()
        #Set the new content
        self.extend(re.split("\n", update_text), update_parent=False)
    
    def get_absolute_cursor_position(self):
        """Get the absolute cursor position"""
        line, index = self.parent.getCursorPosition()
        absolute_position = 0
        for i in range(line):
            absolute_position += len(self[i])
        absolute_position += index + 1
        return absolute_position
    
    def _clear(self):
        del self[:]


class Hotspots:
    """
    Functions for styling text with hotspots (used by CustomEditor and PlainEditor)
    """    
    def style(self, editor, index_from, length, color=0xff0000):
        """
        Style the text from/to with a hotspot
        """
        send_scintilla = editor.SendScintilla
        qscintilla_base = data.PyQt.Qsci.QsciScintillaBase
        #Use the scintilla low level messaging system to set the hotspot
        send_scintilla(qscintilla_base.SCI_STYLESETHOTSPOT, 2, True)
        send_scintilla(qscintilla_base.SCI_SETHOTSPOTACTIVEFORE, True, color)
        send_scintilla(qscintilla_base.SCI_SETHOTSPOTACTIVEUNDERLINE, True)
        send_scintilla(qscintilla_base.SCI_STARTSTYLING, index_from, 2)
        send_scintilla(qscintilla_base.SCI_SETSTYLING, length, 2)


class TheSquid:
    """
    The static object for executing functions that encompass multiple objects.
    """
    main_form = None
    main_window = None
    upper_window = None
    lower_window = None
    repl = None
    repl_helper = None
    
    @staticmethod
    def init_objects(main_form):
        TheSquid.main_form = main_form
        TheSquid.main_window = main_form.main_window
        TheSquid.upper_window = main_form.upper_window
        TheSquid.lower_window = main_form.lower_window
        TheSquid.repl = main_form.repl
        TheSquid.repl_helper = main_form.repl_helper
    
    @staticmethod
    def update_objects():
        TheSquid.main_window = TheSquid.main_form.main_window
        TheSquid.upper_window = TheSquid.main_form.upper_window
        TheSquid.lower_window = TheSquid.main_form.lower_window
        TheSquid.repl = TheSquid.main_form.repl
        TheSquid.repl_helper = TheSquid.main_form.repl_helper
    
    @staticmethod
    def update_styles():
        if TheSquid.main_form == None:
            # Do not update if the main form is not initialized
            return
        TheSquid.update_objects()
        
        TheSquid.customize_menu_style(TheSquid.main_form.menubar)
        TheSquid.customize_menu_style(TheSquid.main_form.sessions_menu)
        TheSquid.customize_menu_style(TheSquid.main_form.recent_files_menu)
        TheSquid.customize_menu_style(TheSquid.main_form.save_in_encoding)
        
        def set_style(menu):
            if hasattr(menu, "actions"):
                TheSquid.customize_menu_style(menu)
                for item in menu.actions():
                    if item.menu() != None:
                        TheSquid.customize_menu_style(item.menu())
                        set_style(item)
        set_style(TheSquid.main_form.sessions_menu)
        
        windows = [
            TheSquid.main_window, TheSquid.upper_window, TheSquid.lower_window
        ]
        
        for window in windows:
            window.customize_tab_bar()
        
            for i in range(window.count()):
                if hasattr(window.widget(i), "corner_widget"):
                    TheSquid.customize_menu_style(
                        window.widget(i).corner_widget
                    )
                    if data.custom_menu_scale != None:
                        window.widget(i).corner_widget.setIconSize(
                            data.PyQt.QtCore.QSize(
                                data.custom_menu_scale, data.custom_menu_scale
                            )
                        )
                    else:
                        window.widget(i).corner_widget.setIconSize(
                            data.PyQt.QtCore.QSize(16, 16)
                        )
                if isinstance(window.widget(i), helper_forms.TreeDisplay):
                    window.widget(i).update_icon_size()
    
    @staticmethod
    def customize_menu_style(menu):
        if data.custom_menu_scale != None and data.custom_menu_font != None:
            # Customize the style
            try:
                default_style_name = data.QApplication.style().objectName()
                custom_style = CustomStyle(default_style_name)
                menu.setStyle(custom_style)
            except:
                if platform.system() == "Windows":
                    custom_style = CustomStyle("Windows")
                    menu.setStyle(custom_style)
                else:
                    custom_style = CustomStyle("GTK")
                    menu.setStyle(custom_style)
        else:
            # Reset the style
            menu.setStyle(data.QApplication.style())
    


class ActionFilter(data.PyQt.QtCore.QObject):
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
        if(event.type() == data.PyQt.QtCore.QEvent.MouseButtonPress):
            cursor = data.PyQt.QtGui.QCursor.pos()
            cursor = cursor - receiver.pos()
            if receiver.actionAt(cursor) != None:
                action = receiver.actionAt(cursor)
#                print(action.text())
                # Create the click&drag detect timer
                def click_and_drag():
                    def hide_parents(obj):
                        obj.hide()
                        if obj.parent() != None and (isinstance(obj.parent(), data.QMenu)):
                            hide_parents(obj.parent())
                    hide_parents(receiver)
                    ActionFilter.click_timer = None
                    if hasattr(action, "pixmap"):
                        cursor = data.PyQt.QtGui.QCursor(
                            action.pixmap
                        )
                        data.application.setOverrideCursor(cursor)
                        ActionFilter.click_drag_action = action
                ActionFilter.click_timer = data.PyQt.QtCore.QTimer(self)
                ActionFilter.click_timer.setInterval(400)
                ActionFilter.click_timer.setSingleShot(True)
                ActionFilter.click_timer.timeout.connect(click_and_drag)
                ActionFilter.click_timer.start()
        elif(event.type() == data.PyQt.QtCore.QEvent.MouseButtonRelease):
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
            click_drag_action = None


class CustomStyle(data.QCommonStyle):
    """
    Custom style for changing the look of Ex.Co.'s menubar and menubar submenus.
    """
    
    custom_font = None
    custom_font_metrics = None
    
    def __init__(self, style_name):
        super().__init__()
        self._style = data.QStyleFactory.create(style_name)
        if self._style == None:
            raise Exception(
                "Style '{}' is not valid on this system!".format(style_name)
            )
        """
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        This needs to happen on CustomStyle initialization,
        otherwise the font's bounding rectangle in not calculated
        correctly!
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        """
        self.scale_constant = data.custom_menu_scale
        self.custom_font = data.PyQt.QtGui.QFont(*data.custom_menu_font)
        self.custom_font_metrics = data.PyQt.QtGui.QFontMetrics(self.custom_font)
    
    def drawComplexControl(self, cc, opt, p, widget=None):
        self._style.drawComplexControl(cc, opt, p, widget)
        
    def drawControl(self, element, opt, p, widget=None):
        if element == data.QStyle.CE_MenuItem: 
            # Store the item's pixmap
            pixmap = opt.icon.pixmap(self.scale_constant)
            # Disable the icon from being drawn automatically
            opt.icon = data.PyQt.QtGui.QIcon()
            # Adjust the font
            opt.font = self.custom_font
            # Setup and draw everything except the icon
            opt.maxIconWidth = self.scale_constant
            self._style.drawControl(element, opt, p, widget)
            if pixmap.isNull() == False:
                # Manually draw the icon
                alignment = data.PyQt.QtCore.Qt.AlignLeft
                self.drawItemPixmap(p, opt.rect, alignment, pixmap)
        elif element == data.QStyle.CE_MenuBarItem:
            text = opt.text.replace("&", "")
            opt.text = ""
            self._style.drawControl(element, opt, p, widget)
            alignment = data.PyQt.QtCore.Qt.AlignCenter
            p.setFont(self.custom_font)
            self.drawItemText(
                p, opt.rect, alignment, opt.palette, opt.state, text, data.PyQt.QtGui.QPalette.NoRole
            )
        else:
            self._style.drawControl(element, opt, p, widget)
    
    def drawPrimitive(self, pe, opt, p, widget=None):
        self._style.drawPrimitive(pe, opt, p, widget)
    
    def drawItemPixmap(self, painter, rect, alignment, pixmap):
        scaled_pixmap = pixmap.scaled(
            self.scale_constant, 
            self.scale_constant
        )
        self._style.drawItemPixmap(painter, rect, alignment, scaled_pixmap)
    
    def drawItemText(self, painter, rectangle, alignment, palette, enabled, text, textRole=data.PyQt.QtGui.QPalette.NoRole):
        self._style.drawItemText(painter, rectangle, alignment, palette, enabled, text, textRole)
    
    def itemPixmapRect(self, r, flags, pixmap):
        return self._style.itemPixmapRect(r, flags, pixmap)
    
    def itemTextRect(self, fm, r, flags, enabled, text):
        return self._style.itemTextRect(fm, r, flags, enabled, text)
    
    def generatedIconPixmap(self, iconMode, pixmap, opt):
        return self._style.generatedIconPixmap(iconMode, pixmap, opt)
    
    def hitTestComplexControl(self, cc, opt, pt, widget=None):
        return self._style.hitTestComplexControl(cc, opt, pt, widget)
    
    def pixelMetric(self, m, option=None, widget=None):
        if m == data.QStyle.PM_SmallIconSize:
            return self.scale_constant
        elif m == data.QStyle.PE_IndicatorProgressChunk:
            # This is the Manubar, don't know why it's called IndicatorProgressChunk?
            return 0.5
        else:
            return self._style.pixelMetric(m, option, widget)

    def polish(self, widget):
        return self._style.polish(widget)
    
    def sizeFromContents(self, ct, opt, contentsSize, widget=None):
        if ct == data.QStyle.CT_MenuItem:
            scaled_width = self.scale_constant*1.5
            resized_width = self.custom_font_metrics.width(opt.text) + scaled_width
            result = data.PyQt.QtCore.QSize(resized_width, self.scale_constant)
            return result
        elif ct == data.QStyle.CT_MenuBarItem:
            base_width = self.custom_font_metrics.width(opt.text)
            scaled_width = self.scale_constant*1.5
            if base_width < scaled_width:
                result = data.PyQt.QtCore.QSize(scaled_width, self.scale_constant)
            else:
                result = data.PyQt.QtCore.QSize(base_width, self.scale_constant)
            return result
        else:
            return self._style.sizeFromContents(ct, opt, contentsSize, widget)
    
    def hitTestComplexControl(self, cc, opt, pt, widget = None):
        return self._style.hitTestComplexControl(cc, opt, pt, widget)
    
    def combinedLayoutSpacing(self, controls1, controls2, orientation, option = None, widget = None):
        return self._style.combinedLayoutSpacing(control1, control2, orientation, option, widget)
    
    def layoutSpacing(self, control1, control2, orientation, option = None, widget = None):
        return self._style.layoutSpacing(control1, control2, orientation, option, widget)
    
    def layoutSpacingImplementation(self, control1, control2, orientation, option = None, widget = None):
        return self._style.layoutSpacingImplementation(control1, control2, orientation, option, widget)
    
    def standardIconImplementation(self, standardIcon, option=None, widget=None):
        return self._style.standardIconImplementation(standardIcon, option, widget)
    
    def standardIcon(self, standardIcon, option=None, widget=None):
        return self._style.standardIcon(standardIcon, option, widget)
        
    def standardPalette(self):
        return self._style.standardPalette()
    
    def standardPixmap(self, sp, option=None, widget=None):
        return self._style.standardPixmap(sp, option, widget)
    
    def styleHint(self, sh, option=None, widget=None, returnData=None):
        return self._style.styleHint(sh, option, widget, returnData)
    
    def subControlRect(self, cc, opt, sc, widget=None):
        return self._style.subControlRect(cc, opt, sc, widget)
    
    def subElementRect(self, e, opt, widget=None):
        return self._style.subElementRect(e, opt, widget)
    
    def unpolish(self, widget):
        return self._style.unpolish(widget)
