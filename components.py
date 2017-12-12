
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
import math


class HexBuilder:
    first_position = None
    painter = None
    edge_length = None
    scale = None
    
    fill_color = None
    line_width = None
    line_color = None
    
    directions = {
        0: "up",
        1: "up-right",
        2: "down-right",
        3: "down",
        4: "down-left",
        5: "up-left",
    }
    steps = None
    horizontal_step = None
    vertical_step = None
    grid_positions = None
    
    @staticmethod
    def generate_hexagon_points(edge_length, offset):
        """Generator for coordinates in a hexagon."""
        x, y = offset
        points = []
        for angle in range(0, 360, 60):
            x += math.cos(math.radians(angle)) * edge_length
            y += math.sin(math.radians(angle)) * edge_length
            points.append((x, y))
        last = points.pop()
        points.insert(0, last)
        for p in points:
            yield p[0], p[1]
    
    def __init__(self, 
                 painter, 
                 first_position, 
                 edge_length, 
                 scale=1.0,
                 fill_color=data.QColor(255,255,255),
                 line_width=1,
                 line_color=data.QColor(255,255,255),):
        self.set_first_position(first_position)
        self.painter = painter
        self.scale = scale
        self.edge_length = scale * edge_length
        
        horizontal_step = (3 * self.edge_length) / 2
        vertical_step = math.sin(math.pi / 3) * self.edge_length
        self.steps = {
            "down-left": (-horizontal_step, vertical_step),
            "down-right": (horizontal_step, vertical_step),
            "down": (0, 2*vertical_step),
            "up-left": (-horizontal_step, -vertical_step),
            "up-right": (horizontal_step, -vertical_step),
            "up": (0, -2*vertical_step),
        }
        self.horizontal_step = horizontal_step
        self.vertical_step = vertical_step
        
        self.fill_color = fill_color
        self.line_width = line_width
        self.line_color = line_color
    
    @staticmethod
    def get_single_hex_size(edge_length, line_width):
        width = None
        height = None
        width = 2 * edge_length
        width += 2 * line_width
        height = math.sqrt(3) * edge_length
        height += 2 * line_width
        return (width, height)
    
    def set_first_position(self, first_position):
        self.first_position = first_position
        self.grid_positions = [
            first_position
        ]
    
    def create_grid(self, *array_grid):
        self.draw()
        paint_all_edges = [False]
        if isinstance(array_grid[0], bool):
            paint_all_edges[0] = array_grid[0]
            array_grid = array_grid[1:]
        for ag in array_grid:
            paint_all_edges.append(False)
            if isinstance(ag, int):
                self.next_step_draw(ag)
            elif isinstance(ag, tuple):
                self.next_step_draw(ag[0])
                paint_all_edges[-1] = ag[1]
            else:
                raise Exception("create_grid item has to be an int (0 >= i < 6) or a tuple(int, bool)!")
        # Paint the edges as needed
        number_of_steps = len(self.directions)
        steps = [self.steps[self.directions[x]] for x in range(number_of_steps)]
        positions = [(int(x[0]), int(x[1])) for x in self.grid_positions]
        for j, gp in enumerate(self.grid_positions):
            paint_edge = [True, True, True, True, True, True]
            if paint_all_edges[j] != True:
                for i, s in enumerate(steps):
                    test_step = (int(gp[0] + s[0]), int(gp[1] + s[1]))
                    comparisons = [(abs(x[0]-test_step[0]) < 5 and abs(x[1]-test_step[1]) < 5) for x in positions]
                    if any(comparisons):
                        paint_edge[i] = False
            self.draw_line_hexagon(
                position = gp, 
                line_width = self.line_width,
                line_color = self.line_color,
                paint_enabled = paint_edge,
                shadow = True
            )
    
    def next_step_draw(self, direction):
        self.next_step_move(direction)
        self.draw()
        
    def next_step_move(self, direction):
        next_step = self.steps[self.directions[direction]]        
        last_position = self.grid_positions[-1]
        self.grid_positions.append(
            (last_position[0] + next_step[0], last_position[1] + next_step[1])
        )
        return self.grid_positions[-1]
    
    def draw(self):
        self.draw_filled_hexagon(
            position = self.grid_positions[-1], 
            fill_color = self.fill_color,
        )
    
    def draw_line_hexagon(self, 
                          position, 
                          line_width, 
                          line_color,
                          paint_enabled=[True,True,True,True,True,True],
                          shadow=False):
        qpainter = self.painter
        
        if line_width == 0:
            return
        
        pen = data.QPen(data.Qt.SolidLine)
        pen.setCapStyle(data.Qt.RoundCap)
        pen.setJoinStyle(data.Qt.RoundJoin)
        pen.setWidth(line_width)
        pen.setColor(line_color)
        qpainter.setPen(pen)
        hex_points = list(
            HexBuilder.generate_hexagon_points(self.edge_length, position)
        )
        x_correction = self.edge_length / 2
        y_correction = self.edge_length / (2 * math.tan(math.radians(30)))
        hex_points = [(x-x_correction, y-y_correction) for x, y in hex_points]
        hex_lines = []
        for i in range(len(hex_points)):
            if paint_enabled[i] == False:
                continue
            n = i + 1
            if n > (len(hex_points)-1):
                n = 0
            hex_lines.append(
                data.QLine(
                    data.QPoint(*hex_points[i]), data.QPoint(*hex_points[n])
                )
            )
        if hex_lines:
            if shadow == True:
                shadow_0_color = data.QColor(line_color)
                shadow_0_color.setAlpha(64)
                shadow_1_color = data.QColor(line_color)
                shadow_1_color.setAlpha(128)
                
                pen.setWidth(line_width*2.0)
                pen.setColor(shadow_0_color)
                qpainter.setPen(pen)
                qpainter.drawLines(*hex_lines)
                pen.setWidth(line_width*1.5)
                pen.setColor(shadow_1_color)
                qpainter.setPen(pen)
                qpainter.drawLines(*hex_lines)
                pen.setWidth(line_width)
                pen.setColor(line_color)
                qpainter.setPen(pen)
                qpainter.drawLines(*hex_lines)
            else:
                qpainter.drawLines(*hex_lines)
    
    def draw_filled_hexagon(self, position, fill_color):
        qpainter = self.painter
        
        pen = data.QPen(data.Qt.SolidLine)
        pen.setColor(fill_color)
        brush = data.QBrush(data.Qt.SolidPattern)
        brush.setColor(fill_color)
        qpainter.setBrush(brush)
        qpainter.setPen(pen)
        hex_points = list(HexBuilder.generate_hexagon_points(self.edge_length, position))
        x_correction = self.edge_length / 2
        y_correction = self.edge_length / (2 * math.tan(math.radians(30)))
        hex_points = [(x-x_correction, y-y_correction) for x, y in hex_points]
        hex_qpoints = [data.QPoint(*x) for x in hex_points]
        qpainter.drawPolygon(*hex_qpoints)
    
    def draw_full_hexagon(self,
                          position,
                          fill_color, 
                          line_width, 
                          line_color):
        qpainter = self.painter
        
        pen = data.QPen(data.Qt.SolidLine)
        pen.setColor(line_color)
        pen.setCapStyle(data.Qt.RoundCap)
        pen.setWidth(line_width)
        brush = data.QBrush(data.Qt.SolidPattern)
        brush.setColor(fill_color)
        qpainter.setBrush(brush)
        qpainter.setPen(pen)
        hex_points = list(HexBuilder.generate_hexagon_points(self.edge_length, position))
        x_correction = self.edge_length / 2
        y_correction = self.edge_length / (2 * math.tan(math.radians(30)))
        hex_points = [(x-x_correction, y-y_correction) for x, y in hex_points]
        hex_qpoints = [data.QPoint(*x) for x in hex_points]
        qpainter.drawPolygon(*hex_qpoints)
    
    def draw_full_hexagon_with_shadow(self,
                                      position,
                                      fill_color, 
                                      line_width, 
                                      line_color):
        qpainter = self.painter
        
        self.draw_filled_hexagon(position, fill_color)
        shadow_0_color = data.QColor(line_color)
        shadow_0_color.setAlpha(64)
        shadow_1_color = data.QColor(line_color)
        shadow_1_color.setAlpha(128)
        self.draw_line_hexagon(position, line_width*2.0, shadow_0_color)
        self.draw_line_hexagon(position, line_width*1.5, shadow_1_color)
        self.draw_line_hexagon(position, line_width, line_color)
    
    def get_last_position(self):
        return self.grid_positions[-1]
    
    def generate_square_grid_list(self, row_length, count):
        row_counter = 1
        grid_list = []
        direction = False
        add_down_step = False
        for i in range(count-1):
            if add_down_step == True:
                add_down_step = False
                grid_list.append((3, True))
            elif direction == True:
                if (row_counter % 2) == 0:
                    grid_list.append((4, True))
                else:
                    grid_list.append((5, True))
                row_counter -= 1
                if row_counter == 1:
                    add_down_step = True
                    direction = False
            else:
                if (row_counter % 2) == 0:
                    grid_list.append((2, True))
                else:
                    grid_list.append((1, True))
                row_counter += 1 
                if row_counter == row_length:
                    add_down_step = True
                    direction = True
        return grid_list


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
        qscintilla_base = data.QsciScintillaBase
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
                            data.QSize(
                                data.custom_menu_scale, data.custom_menu_scale
                            )
                        )
                    else:
                        window.widget(i).corner_widget.setIconSize(
                            data.QSize(16, 16)
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
                if data.platform == "Windows":
                    custom_style = CustomStyle("Windows")
                    menu.setStyle(custom_style)
                else:
                    custom_style = CustomStyle("GTK")
                    menu.setStyle(custom_style)
        else:
            # Reset the style
            menu.setStyle(data.QApplication.style())
    


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
        if(event.type() == data.QEvent.MouseButtonPress):
            cursor = data.QCursor.pos()
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
        elif(event.type() == data.QEvent.MouseButtonRelease):
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
        self.custom_font = data.QFont(*data.custom_menu_font)
        self.custom_font_metrics = data.QFontMetrics(self.custom_font)
    
    def drawComplexControl(self, cc, opt, p, widget=None):
        self._style.drawComplexControl(cc, opt, p, widget)
        
    def drawControl(self, element, opt, p, widget=None):
        if element == data.QStyle.CE_MenuItem: 
            # Store the item's pixmap
            pixmap = opt.icon.pixmap(self.scale_constant)
            # Disable the icon from being drawn automatically
            opt.icon = data.QIcon()
            # Adjust the font
            opt.font = self.custom_font
            # Setup and draw everything except the icon
            opt.maxIconWidth = self.scale_constant
            self._style.drawControl(element, opt, p, widget)
            if pixmap.isNull() == False:
                # Manually draw the icon
                alignment = data.Qt.AlignLeft
                self.drawItemPixmap(p, opt.rect, alignment, pixmap)
        elif element == data.QStyle.CE_MenuBarItem:
            text = opt.text.replace("&", "")
            opt.text = ""
            self._style.drawControl(element, opt, p, widget)
            alignment = data.Qt.AlignCenter
            p.setFont(self.custom_font)
            self.drawItemText(
                p, opt.rect, alignment, opt.palette, opt.state, text, data.QPalette.NoRole
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
    
    def drawItemText(self, painter, rectangle, alignment, palette, enabled, text, textRole=data.QPalette.NoRole):
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
            result = data.QSize(resized_width, self.scale_constant)
            return result
        elif ct == data.QStyle.CT_MenuBarItem:
            base_width = self.custom_font_metrics.width(opt.text)
            scaled_width = self.scale_constant*1.5
            if base_width < scaled_width:
                result = data.QSize(scaled_width, self.scale_constant)
            else:
                result = data.QSize(base_width, self.scale_constant)
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
