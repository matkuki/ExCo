# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2023 Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""


import traceback
import data
import functions
import components.actionfilter
import gui.custombuttons
import gui.menu


"""
--------------------------------------------------------------
Custom standard context menu
--------------------------------------------------------------
"""
class ContextMenu(gui.menu.Menu):
    # Main form reference
    main_form = None
    
    def __init__(self, parent=None, main_form=None, menu_type=None):
        # Initialize the superclass
        super().__init__(parent)
        # Store the reference to the parent
        self.setParent(parent)
        # Store the reference to the main form
        self.main_form = main_form
        # Create a menu according to type
        if menu_type == "plain":
            self.create_plain_actions()
        elif menu_type == "special":
            self.create_special_actions()
        elif menu_type == "multiline-repl-normal":
            self.create_multiline_repl_actions()
        elif menu_type == "multiline-repl-horizontal":
            self.create_multiline_repl_actions()
        else:
            raise Exception("Unknown menu type: '{}'".format(menu_type))
    
    def create_plain_actions(self):
        action_names = (
            "copy",
            "cut",
            "paste",
            "line_copy",
            "undo",
            "redo",
            "line_duplicate",
            "line_transpose",
            "line_cut",
            "line_delete",
            "select_all",
            "special_to_uppercase",
            "special_to_lowercase",
            "show_edge",
            "toggle_line_endings",
            "goto_to_end",
            "goto_to_start",
            "special_indent_to_cursor",
            "open_in_browser",
        )
        self.__create_actions(action_names)
    
    def create_special_actions(self):
        action_names = (
            "copy",
            "cut",
            "paste",
            "line_copy",
            "undo",
            "redo",
            "line_duplicate",
            "open_in_browser",
            "line_cut",
            "line_delete",
            "select_all",
            "special_to_uppercase",
            "special_to_lowercase",
            "comment_uncomment",
            "toggle_line_endings",
            "goto_to_end",
            "goto_to_start",
            "special_indent_to_cursor",
            "create_node_tree",
        )
        self.__create_actions(action_names)
    
    def create_multiline_repl_actions(self):
        action_names = (
            "copy",
            "cut",
            "paste",
            "comment_uncomment",
            "undo",
            "redo",
            "line_duplicate",
            "line_transpose",
        )
        self.__create_actions(action_names)
    
    def __create_actions(self, action_names):
        for an in action_names:
            name, function, icon, keys, status_tip = data.global_function_information[an]
            action = data.QAction(name, self)
            action.setToolTip(status_tip)
            action.setStatusTip(status_tip)
            action.setIcon(functions.create_icon(icon))
            if function is not None:
                action.triggered.connect(function)
            action.setEnabled(True)
            self.addAction(action)
    
    def clear_items(self):
        for a in self.actions():
            a.triggered.disconnect()
            a.setParent(None)
    
    def popup_at_cursor(self):
        click_global_position = data.QCursor.pos()
        self.popup(click_global_position)


"""
--------------------------------------------------------------
Custom context menu for the editors and REPL with HEX buttons
--------------------------------------------------------------
"""
class ContextMenuHex(data.QGroupBox):
    # Various references
    main_form = None
    # Painting offset
    offset = (0, 0)
    # Stored menu button
    button_list = None
    # Inner button positions, clockwise from the top,
    # last position is in the middle
    inner_button_positions = [
        (-27, -24, 0),
        (14, 0, 1),
        (14, 48, 2),
        (-27, 72, 3),
        (-68, 48, 4),
        (-68, 0, 5),
        (-27, 24, 6)
    ]
    outer_button_positions = [
        (-27, -72, 7),
        (14, -48, 8),
        (54, -24, 9),
        (54, 24, 10),
        (54, 72, 11),
        (14, 96, 12),
        (-27, 120, 13),
        (-68, 96, 14),
        (-108, 72, 15),
        (-108, 24, 16),
        (-108, -24, 17),
        (-68, -48, 18),
    ]
    horizontal_button_positions = [
        (-148, 0, 19),
        (-108, 24, 20),
        (-68, 0, 21),
        (-27, 24, 22),
        (14, 0, 23),
        (54, 24, 24),
        (94, 0, 25),
    ]
    standard_buttons = {
        "0": "copy",
        "1": "cut",
        "2": "paste",
        "3": "line_copy",
        "4": "undo",
        "5": "redo",
        "6": "line_duplicate",
        "7": "line_transpose",
        "8": "line_cut",
        "9": "line_delete",
        "10": "select_all",
        "11": "special_to_uppercase",
        "12": "special_to_lowercase",
        "13": "show_edge",
        "14": "toggle_line_endings",
        "15": "goto_to_end",
        "16": "goto_to_start",
        "17": "special_indent_to_cursor",
        "18": "open_in_browser",
    }
    # A Copy for when the functions need to be reset
    stored_standard_buttons = dict(standard_buttons)
    special_buttons = {
        "0": "copy",
        "1": "cut",
        "2": "paste",
        "3": "line_copy",
        "4": "undo",
        "5": "redo",
        "6": "line_duplicate",
        "7": "open_in_browser",
        "8": "line_cut",
        "9": "line_delete",
        "10": "select_all",
        "11": "special_to_uppercase",
        "12": "special_to_lowercase",
        "13": "comment_uncomment",
        "14": "toggle_line_endings",
        "15": "goto_to_end",
        "16": "goto_to_start",
        "17": "special_indent_to_cursor",
        "18": "create_node_tree",
    }
    # A Copy for when the functions need to be reset
    stored_special_buttons = dict(special_buttons) # or special_buttons[:]
    horizontal_buttons = {
        "19": "copy",
        "20": "cut",
        "21": "paste",
        "22": "comment_uncomment",
        "23": "undo",
        "24": "redo",
        "25": "line_duplicate",
    }
    # A Copy for when the functions need to be reset
    stored_horizontal_buttons = dict(horizontal_buttons) # or horizontal_buttons[:]
    # Button scaling factor
    x_scale = 0.7
    y_scale = 0.7
    # Total button position offset
    total_offset = (0, -48)
    # Current context menu functions type
    functions_type = None

    def __init__(self, parent=None, main_form=None, offset=(0, 0)):
        # Initialize the superclass
        super().__init__(parent)
        # Store the reference to the parent
        self.setParent(parent)
        # Store the reference to the main form
        self.main_form = main_form
        # Set default font
        self.setFont(data.get_current_font())
        # Store the painting offset
        self.offset = offset
        # Set the background color
        style_sheet = "background-color: transparent;"
        style_sheet += "border: 0 px;"
        self.setStyleSheet(style_sheet)
        # Set the groupbox size
        screen_resolution = data.application.primaryScreen().geometry()
        width, height = screen_resolution.width(), screen_resolution.height()
        self.setGeometry(functions.create_rect(0, 0, width, height))
        self.update_style()
    
    def clear_items(self):
        for b in self.button_list:
            b.setParent(None)
    
    @staticmethod
    def reset_functions():
        """
        Copy stored functions back into the active menu functions
        """
        ContextMenuHex.standard_buttons = dict(ContextMenuHex.stored_standard_buttons)
        ContextMenuHex.special_buttons = dict(ContextMenuHex.stored_special_buttons)
        ContextMenuHex.horizontal_buttons = dict(ContextMenuHex.stored_horizontal_buttons)

    @staticmethod
    def get_settings():
        """
        Return the custom function settings for the settings manipulator
        """
        return {
            "standard_buttons": ContextMenuHex.standard_buttons,
            "special_buttons": ContextMenuHex.special_buttons,
            "horizontal_buttons": ContextMenuHex.horizontal_buttons,
        }

    def check_position_offset(self,
                              inner_buttons=True,
                              outer_buttons=True,
                              horizontal_buttons=False):
        button_positions = []
        if inner_buttons == True:
            button_positions.extend(ContextMenuHex.inner_button_positions)
        if outer_buttons == True:
            button_positions.extend(ContextMenuHex.outer_button_positions)
        if horizontal_buttons == True:
            button_positions.extend(self.horizontal_button_positions)
        hex_x_size = ContextButton.HEX_IMAGE_SIZE[0] * self.x_scale
        hex_y_size = ContextButton.HEX_IMAGE_SIZE[1] * self.y_scale
        window_size = self.parent().size() - functions.create_size(hex_x_size, hex_y_size)
        min_x = 0
        min_y = 0
        max_x = 0
        max_y = 0
        for b in button_positions:
            x = self.offset[0]+ b[0]*self.x_scale/0.8 + self.total_offset[0]
            y = self.offset[1]+ b[1]*self.y_scale/0.8 + self.total_offset[1]
            if x < min_x:
                min_x = x
            if x > window_size.width():
                new_max = x - window_size.width()
                if new_max > max_x:
                    max_x = new_max
            if y < min_y:
                min_y = y
            if y > window_size.height():
                new_max = y - window_size.height()
                if new_max > max_y:
                    max_y = new_max
        if min_x != 0:
            self.offset = (self.offset[0]-min_x, self.offset[1])
        if max_x != 0:
            self.offset = (self.offset[0]-max_x, self.offset[1])
        if min_y != 0:
            self.offset = (self.offset[0], self.offset[1]-min_y)
        if max_y != 0:
            self.offset = (self.offset[0], self.offset[1]-max_y)

    def mousePressEvent(self, event):
        button = event.button()
        super().mousePressEvent(event)
        self.parent().delete_context_menu()

    def add_buttons(self, buttons):
        """
        Add buttons to the context menu
        """
        total_offset = self.total_offset
        for b in buttons:
            function_info = b[0]
            button_position = b[1]
            button_number = button_position[2]
            button = ContextButton(
                self,
                self.main_form,
                input_pixmap=function_info[0],
                input_function=function_info[1],
                input_function_text=function_info[2],
                input_tool_tip=function_info[2],
                input_focus_last_widget=data.HexButtonFocus.TAB,
                input_scale=(self.x_scale, self.y_scale),
            )
            button.number = button_number
            #Set the button size and location
            button.set_offset(
                (self.offset[0]+ button_position[0]*self.x_scale/0.8 + total_offset[0],
                    self.offset[1]+ button_position[1]*self.y_scale/0.8 + total_offset[1])
            )
            button.dim()
            self.button_list.append(button)

    def create_horizontal_multiline_repl_buttons(self):
        # Check if any of the buttons are out of the window and adjust the offset
        self.check_position_offset(
            inner_buttons=False,
            outer_buttons=False,
            horizontal_buttons=True
        )
        buttons = [ContextMenuHex.horizontal_buttons[str(x)] for x in range(19, 26)]
        # Add the buttons
        self.button_list = []
        self.add_horizontal_buttons(buttons)
        self.functions_type = "horizontal"

    def create_multiline_repl_buttons(self):
        inner_buttons = [ContextMenuHex.horizontal_buttons[str(x)] for x in range(19, 26)]
        self.create_buttons(inner_buttons)
        self.functions_type = "horizontal"

    def create_plain_buttons(self):
        inner_buttons = [ContextMenuHex.standard_buttons[str(x)] for x in range(7)]
        self.create_buttons(inner_buttons)
        self.functions_type = "plain"

    def create_standard_buttons(self):
        inner_buttons = [ContextMenuHex.standard_buttons[str(x)] for x in range(7)]
        outer_buttons = [ContextMenuHex.standard_buttons[str(x)] for x in range(7, len(ContextMenuHex.standard_buttons))]
        self.create_buttons(inner_buttons, outer_buttons)
        self.functions_type = "standard"

    def create_special_buttons(self):
        inner_buttons = [ContextMenuHex.special_buttons[str(x)] for x in range(7)]
        outer_buttons = [ContextMenuHex.special_buttons[str(x)] for x in range(7, len(ContextMenuHex.standard_buttons))]
        self.create_buttons(inner_buttons, outer_buttons)
        self.functions_type = "special"

    def create_buttons(self,
                       inner_buttons=[],
                       outer_buttons=[]):
        # Check if any of the buttons are out of the window and adjust the offset
        if outer_buttons == []:
            self.check_position_offset(
                inner_buttons=True,
                outer_buttons=False,
                horizontal_buttons=False
            )
        else:
            self.check_position_offset()
        # Add the buttons
        self.button_list = []
        if inner_buttons != []:
            buttons = inner_buttons
            self.add_inner_buttons(buttons)
        if outer_buttons != []:
            buttons = outer_buttons
            self.add_outer_buttons(outer_buttons)

    def add_inner_buttons(self, in_buttons):
        self.__add_buttons(in_buttons, 7, ContextMenuHex.inner_button_positions)

    def add_outer_buttons(self, in_buttons):
        self.__add_buttons(in_buttons, 12, ContextMenuHex.outer_button_positions)

    def add_horizontal_buttons(self, in_buttons):
        self.__add_buttons(in_buttons, 7, ContextMenuHex.horizontal_button_positions)

    def __add_buttons(self, in_buttons, max_count, positions):
        if len(in_buttons) > max_count:
            raise Exception("Too many inner buttons in context menu!")
        buttons = []
        for i,button in enumerate(in_buttons):
            if (button in function_list) == False:
                self.main_form.display.repl_display_message(
                    "'{}' context menu function does not exist!".format(button),
                    message_type=data.MessageType.ERROR
                )
            else:
                buttons.append(
                    (function_list[button], positions[i])
                )
        self.add_buttons(buttons)

    def update_style(self):
        self.setStyleSheet(f"""
            QGroupBox {{
                /*
                background-color: {data.theme["fonts"]["default"]["background"]};
                */
                background-color: transparent;
                color: {data.theme["fonts"]["default"]["color"]};
                border: 1px solid {data.theme["indication"]["passiveborder"]};
                margin: 0px;
                padding: 0px;
                spacing: 0px;
            }}
            QLabel {{
                background-color: {data.theme["fonts"]["default"]["background"]};
                color: {data.theme["fonts"]["default"]["color"]};
            }}
        """)

    def popup_at_cursor(self):
        super().show()
        # When the context menu is shown it is needed to paint
        # the background or the backgrounds will be transparent
        for button in self.button_list:
            button.setVisible(True)
            button.fill_background_color()


class ContextButton(gui.custombuttons.CustomButton):
    """
    Subclassed custom button
    """
    # The button's number in the context menu
    number = None

    def fill_background_color(self):
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(
            self.backgroundRole(),
            data.QColor(data.theme["context-menu-background"])
        )
        self.setPalette(p)

    def set_opacity(self, input_opacity):
        super().set_opacity(input_opacity)
        self.fill_background_color()

    def set_opacity_with_hex_edge(self, input_opacity):
        super()._set_opacity_with_hex_edge(input_opacity)
        self.fill_background_color()

    def mousePressEvent(self, event):
        """
        Overloaded widget click event
        """
        button = event.button()
        if button == data.Qt.MouseButton.LeftButton:
            # Execute the function if it was initialized
            if self.function is not None:
                if components.actionfilter.ActionFilter.click_drag_action is not None:
                    function_name = components.actionfilter.ActionFilter.click_drag_action.function.__name__
#                        print(self.number, function_name)
                    if self._parent.functions_type == "standard":
                        ContextMenuHex.standard_buttons[str(self.number)] = function_name
                    elif self._parent.functions_type == "plain":
                        ContextMenuHex.standard_buttons[str(self.number)] = function_name
                    elif self._parent.functions_type == "horizontal":
                        ContextMenuHex.horizontal_buttons[str(self.number)] = function_name
                    elif self._parent.functions_type == "special":
                        ContextMenuHex.special_buttons[str(self.number)] = function_name
                    # Show the newly added function
                    message = "Added function '{}' at button number {}".format(
                        components.actionfilter.ActionFilter.click_drag_action.text(),
                        self.number
                    )
                    self.main_form.display.repl_display_message(
                        message,
                        message_type=data.MessageType.SUCCESS
                    )
                    # Reset cursor and stored action
                    data.application.restoreOverrideCursor()
                    components.actionfilter.ActionFilter.click_drag_action = None
                else:
                    try:
                        # Execute the buttons stored function
                        self.function()
                    except:
                        traceback.print_exc()
                        message = "You need to focus one of the editor windows first!"
                        self.main_form.display.repl_display_message(
                            message,
                            message_type=data.MessageType.ERROR
                        )
                # Close the function wheel
                self._parent.hide()
                event.accept()
            else:
                event.ignore()
        elif button == data.Qt.MouseButton.RightButton:
            # Close the function wheel
            self._parent.hide()
            event.accept()
        else:
            event.ignore()

    def dim(self, clear_hex_edge=False):
        """Set the buttons opacity to low and clear the function text"""
        # Set the opacity to low
        if clear_hex_edge == True:
            self.set_opacity(self.OPACITY_LOW)
        else:
            self.set_opacity_with_hex_edge(self.OPACITY_LOW)

    def highlight(self):
        """Set the buttons opacity to high and display the buttons function text"""
        # Set the opacity to full
        self.set_opacity_with_hex_edge(self.OPACITY_HIGH)
        # Display the stored function text
        self.main_form.display.write_to_statusbar(self.function_text)


"""
Context menu helper functions
"""
HEX_STYLE = False
function_list = {}

def create(parent=None, main_form=None, offset=(0, 0), _type=None):
    if HEX_STYLE:
        context_menu = ContextMenuHex(parent, main_form, offset=offset)
        if _type == "special":
            context_menu.create_special_buttons()
        elif _type == "plain":
            context_menu.create_plain_buttons()
        elif _type == "multiline-repl-normal":
            context_menu.create_multiline_repl_buttons()
        elif _type == "multiline-repl-horizontal":
            context_menu.create_horizontal_multiline_repl_buttons()
        else:
            raise Exception("Unknown hex button type: '{}'".format(_type))
    else:
        context_menu = ContextMenu(parent, main_form, menu_type=_type)
    return context_menu

def add_function(name, pixmap, function, function_name):
    function_list[name] = (pixmap, function, function_name)