
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2019 Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import os
import sip
import os.path
import collections
import traceback
import ast
import inspect
import math
import functools
import textwrap
import difflib
import re
import time
import settings
import functions
import data
import components
import themes


"""
-------------------------------------------------
GUI Settings manipulator
-------------------------------------------------
"""
class SettingsGuiManipulator(data.QGroupBox):
    class EnlargeButton(data.QLabel):
        name = None
        animation_duration = 40
        scale_factor = 1.0
        enlargement_ration = 1.25
        DEFAULT_SIZE = 25
        original_size = None
        animation = None
        animating = None
        state = False
        queue = None
        function = None
        starting_position = None
        end_position = None
        enabled = None
        enter_function = None
        leave_function = None
        valid_colors = ["default", "red", "green"]
        current_color = None
        properties = None
        
        def __init__(self, 
                     name, 
                     picture, 
                     scale_factor=1.0, 
                     function=None, 
                     key_combination=None, 
                     starting_position=None, 
                     end_position=None, 
                     parent=None):
            super().__init__(parent)
            
            self.name = name
            self.scale_factor = scale_factor
            self.key_combination = key_combination
            self.animating = False
            self.starting_position = starting_position
            self.end_position = end_position
            self.disable()
            self.properties = {}
            # Set default font
            self.setFont(data.get_current_font())
            # Button image
            self.button_image = data.QPixmap(
                os.path.join(
                    data.resources_directory, 
                    picture
                )
            )
            adjusted_size = self.DEFAULT_SIZE * self.scale_factor
            self.button_image = self.button_image.scaled(
                data.QSize(
                    math.ceil(adjusted_size),
                    math.ceil(adjusted_size),
                ),
                transformMode=data.Qt.SmoothTransformation
            )
            
            width, height = components.HexBuilder.get_single_hex_size(adjusted_size, 2)
            def create_base_image():
                hex_image = data.QImage(
                    data.QSize(width, height),
                    data.QImage.Format_ARGB32_Premultiplied
                )
                hex_image.fill(data.Qt.transparent)
                qpainter = data.QPainter(hex_image)
                qpainter.setRenderHints(
                    data.QPainter.Antialiasing | 
                    data.QPainter.TextAntialiasing | 
                    data.QPainter.SmoothPixmapTransform
                )
                hb = components.HexBuilder(
                    qpainter, 
                    (width/2, height/2), 
                    self.DEFAULT_SIZE, 
                    self.scale_factor, 
                    fill_color=data.theme.Settings_Hex_Background,
                    line_width=2,
                    line_color=data.QColor(64,64,64),
                )
                hb.create_grid(False)
                qpainter.end()
                return data.QPixmap.fromImage(hex_image)
            self.hex_image = create_base_image()
            self.hex_image = self.hex_image.scaled(
                data.QSize(
                    math.ceil(self.hex_image.size().width() * self.scale_factor),
                    math.ceil(self.hex_image.size().height() * self.scale_factor),
                ),
                transformMode=data.Qt.SmoothTransformation
            )
            
            # Green hex background
            def create_color_image(color):
                hex_image = data.QImage(
                    data.QSize(width, height),
                    data.QImage.Format_ARGB32_Premultiplied
                )
                hex_image.fill(data.Qt.transparent)
                qpainter = data.QPainter(hex_image)
                qpainter.setRenderHints(
                    data.QPainter.Antialiasing | 
                    data.QPainter.TextAntialiasing | 
                    data.QPainter.SmoothPixmapTransform
                )
                hb = components.HexBuilder(
                    qpainter, 
                    (width/2, height/2), 
                    self.DEFAULT_SIZE, 
                    self.scale_factor, 
                    fill_color=color,
                    line_width=0,
                    line_color=data.QColor(0,0,0),
                )
                hb.create_grid(False)
                qpainter.end()
                return data.QPixmap.fromImage(hex_image)
            self.hex_image_green = create_color_image(data.QColor(138,226,52))
            self.hex_image_green = self.hex_image_green.scaled(
                data.QSize(
                    math.ceil(self.hex_image_green.size().width() * self.scale_factor) - 1,
                    math.ceil(self.hex_image_green.size().height() * self.scale_factor) - 1,
                ),
                transformMode=data.Qt.SmoothTransformation
            )
            # Red hex background
            self.hex_image_red = create_color_image(data.QColor(239,41,41))
            self.hex_image_red = self.hex_image_red.scaled(
                data.QSize(
                    math.ceil(self.hex_image_red.size().width() * self.scale_factor) - 1,
                    math.ceil(self.hex_image_red.size().height() * self.scale_factor) - 1,
                ),
                transformMode=data.Qt.SmoothTransformation
            )
            
            scaled_size = data.QSize(
                self.hex_image.size().width(),
                self.hex_image.size().height(),
            )
            image = data.QImage(
                scaled_size,
                data.QImage.Format_ARGB32_Premultiplied,
            )
            image.fill(data.Qt.transparent)
            button_painter = data.QPainter(image)
            button_painter.setCompositionMode(
                data.QPainter.CompositionMode_SourceOver
            )
            button_painter.setOpacity(1.0)
            # Adjust inner button positioning according to the scale
            x = (self.hex_image.width() - self.button_image.width()) / 2
            y = (self.hex_image.height() - self.button_image.height()) / 2
            button_painter.drawPixmap(0, 0, self.hex_image)
            
            button_painter.drawPixmap(x, y, self.button_image)
            button_painter.end()
            
            # Set properites
            self.setParent(parent)
            self.setPixmap(data.QPixmap.fromImage(image))
            self.setGeometry(
                0, 
                0, 
                image.width() * self.scale_factor, 
                image.height() * self.scale_factor
            )
            self.setMask(self.hex_image.mask())
            self.setScaledContents(True)
            # Set the non-enlarged dimensions
            self.original_size = (
                self.geometry().width(), 
                self.geometry().height()
            )
            
            # Set the initial color state
            self.current_color = "default"
        
        def set_property(self, property_name, property_value):
            self.properties[property_name] = property_value
        
        def set_enter_function(self, func):
            self.enter_function = func
        
        def set_leave_function(self, func):
            self.leave_function = func
        
        def set_position(self, x, y):
            self.setGeometry(
                data.QRect(
                    x, y, 
                    self.geometry().width(), self.geometry().height()
                )
            )
        
        def goto_starting_position(self):
            self.set_position(
                self.starting_position[0],
                self.starting_position[1],
            )
            self.set_start_position()
        
        def set_start_position(self):
            self.enlarged_width = self.original_size[0] * self.enlargement_ration
            self.enlarged_height = self.original_size[1] * self.enlargement_ration
            x_offset = self.geometry().x()
            x_offset += (self.original_size[0] - self.enlarged_width) / 2
            y_offset = self.geometry().y()
            y_offset += (self.original_size[1] - self.enlarged_height) / 2
            x_offset = math.floor(x_offset)
            y_offset = math.floor(y_offset)
            self.x_offset = x_offset
            self.y_offset = y_offset
            
            self.pre_enlarge_position = (
                self.geometry().x(),
                self.geometry().y(),
            )
            self.post_enlarge_position = (
                self.x_offset,
                self.y_offset,
            )
        
        def add_to_queue(self, direction):
            if self.queue == None:
                self.queue = [direction]
            else:
                self.queue.append(direction)
        
        def add_animation(self, animation):
            self.animation = animation

        def animate(self):
            self.animating = True
            if self.queue != None and len(self.queue) != 0:
                while len(self.queue) > 1:
                    self.queue.pop(0)
                q = self.queue.pop(0)
                if q == "enter" and self.state == False:
                    self.enlarge()
                elif q == "leave" and self.state == True:
                    self.shrink()
                else:
                    self.animate()
            elif self.queue != None and len(self.queue) == 0:
                scaled_pixmap = self.pixmap().scaled(
                    self.size(),
                    transformMode=data.Qt.SmoothTransformation
                )
                self.setMask(
                    scaled_pixmap.mask()
                )
                self.animating = False
        
        def set_color(self, color):
            if not(color in self.valid_colors):
                raise Exception("Invalid EnlargeButton color selected!")
            elif color == "red":
                selected_image = self.hex_image_red
            elif color == "green":
                selected_image = self.hex_image_green
            elif color == "default":
                selected_image = None
            
            self.current_color = color
            
            scaled_size = data.QSize(
                self.hex_image.size().width(),
                self.hex_image.size().height(),
            )
            image = data.QImage(
                scaled_size,
                data.QImage.Format_ARGB32_Premultiplied,
            )
            image.fill(data.Qt.transparent)
            button_painter = data.QPainter(image)
            button_painter.setCompositionMode(
                data.QPainter.CompositionMode_SourceOver
            )
            button_painter.setOpacity(1.0)
            # Adjust inner button positioning according to the scale
            x = (self.hex_image.width() - self.button_image.width()) / 2
            y = (self.hex_image.height() - self.button_image.height()) / 2
            button_painter.drawPixmap(0, 0, self.hex_image)
            if selected_image != None:
                button_painter.drawPixmap(
                    (5 * (self.scale_factor - 1.0)), 
                    (5 * (self.scale_factor - 1.0)), 
                    selected_image
                )
            button_painter.drawPixmap(x, y, self.button_image)
            button_painter.end()
            # Set the image as the pixmap
            self.setPixmap(data.QPixmap.fromImage(image))
        
        def reset_color(self):
            if self.current_color != "default":
                self.set_color("default")
        
        def set_green(self):
            if self.current_color != "green":
                self.set_color("green")
        
        def set_red(self):
            if self.current_color != "red":
                self.set_color("red")
        
        def enlarge(self):
            self._start_animation(
                True, 
                # Start
                self.pre_enlarge_position[0], 
                self.pre_enlarge_position[1], 
                self.original_size[0],
                self.original_size[1],
                # End
                self.x_offset, 
                self.y_offset,
                self.enlarged_width,
                self.enlarged_height,
            )
            self.raise_()
        
        def shrink(self):
            self._start_animation(
                False,
                # Start
                self.post_enlarge_position[0],
                self.post_enlarge_position[1],
                self.enlarged_width,
                self.enlarged_height,
                # End
                self.pre_enlarge_position[0],
                self.pre_enlarge_position[1],
                self.original_size[0],
                self.original_size[1],
            )
        
        def _start_animation(self,
                             state,
                             start_position_x,
                             start_position_y,
                             start_width,
                             start_height,
                             end_position_x,
                             end_position_y,
                             end_width,
                             end_height):
            self.clearMask()
            animation = data.QPropertyAnimation(self, b"geometry")
            animation.setEasingCurve(data.QEasingCurve.Linear)
            animation.setDuration(self.animation_duration)
        
            animation.setStartValue(
                data.QRect(
                    start_position_x,
                    start_position_y,
                    start_width,
                    start_height,
                )
            )
            animation.setEndValue(
                data.QRect(
                    end_position_x,
                    end_position_y,
                    end_width,
                    end_height,
                )
            )
            animation.setDirection(data.QAbstractAnimation.Forward)
            self.state = state
            animation.start()
            self.add_animation(animation)
            animation.stateChanged.connect(self.sig_animation_ended)
        
        def sig_animation_ended(self, new_state, old_state):
            self.animate()
        
        def enable(self):
            self.enabled = True
        
        def disable(self):
            self.enabled = False
        
        """
        Events
        """
        def enterEvent(self, e):
#            print(self.name, "ENTER")
            super().enterEvent(e)
            if self.enabled == False:
                return
            self.add_to_queue("enter")
            if self.animating == False:
                self.add_to_queue("enter")
                self.animate()
            # Execute the additional enter function
            if self.enter_function != None:
                self.enter_function(self)
        
        def leaveEvent(self, e):
#            print(self.name, "LEAVE")
            super().leaveEvent(e)
            if self.enabled == False:
                return
            self.add_to_queue("leave")
            if self.animating == False:
                self.animate()
            # Execute the additional leave function
            if self.leave_function != None:
                self.leave_function(self)
        
        def mousePressEvent(self, event):
            super().mousePressEvent(event)
            if self.enabled == False:
                return
            if self.function != None:
                pass
            else:
                print(self.name, self.key_combination)
                self.add_to_queue("leave")
                self.animate()
                self.parent().hide()
    
    
    # Background image
    settings_background_image = None
    # Shown attribute
    shown = False
    # Scale factor which will affect every child widget size adjustment
    scale_factor = 1.0 #0.9
    # Button list
    buttons = None
    # Animation list
    animations = []
    # Default overlay size
    DEFAULT_SIZE = (800, 600)
    # Stored theme name
    theme_name = None
    
    @staticmethod
    def reset_background_image():
        SettingsGuiManipulator.settings_background_image = None
    
    @staticmethod
    def check_theme_state():
        return SettingsGuiManipulator.theme_name != data.theme.name
    
    @staticmethod
    def create_background_image(in_scale=1.0):
        """
        Dinamically create the settings manipulator's background image
        """
        # Check if the QPixmap has been created already
        if SettingsGuiManipulator.settings_background_image == None:
            scale = in_scale
            edge_length = 27
            scaled_edge_diff = (edge_length - (edge_length * scale)) / edge_length
            back_color = data.theme.Settings_Background
            edge_color = data.QColor(data.theme.Settings_Hex_Edge)
            
            SettingsGuiManipulator.theme_name = data.theme.name
            
            def add_offset(offset):
                x_add = 64.0
                y_add = 20.0
                return (offset[0] + x_add, offset[1] + y_add)
            
            settings_background_image = data.QImage(
                data.QSize(*SettingsGuiManipulator.DEFAULT_SIZE),
                data.QImage.Format_ARGB32_Premultiplied
            )
            settings_background_image.fill(data.Qt.transparent)
#            settings_background_image.fill(data.QColor(255,255,255))
            qpainter = data.QPainter(settings_background_image)
            qpainter.setRenderHints(
                data.QPainter.Antialiasing | 
                data.QPainter.TextAntialiasing | 
                data.QPainter.SmoothPixmapTransform
            )
            
            # Corner options
            x = edge_length + 205
            y = 1.8 * edge_length + 30
            offset = (x, y)
            hb = components.HexBuilder(
                qpainter, 
                offset, 
                edge_length, 
                scale, 
                fill_color=back_color,
                line_width=2,
                line_color=edge_color,
            )
            grid_list = [
                (3, True), (4, True), (4, True), 
                (4, True), (5, True), (1, True),
            ]
            hb.create_grid(*grid_list)
            # Label field
            last_step = hb.get_last_position()
            hb = components.HexBuilder(
                qpainter, 
                offset, 
                edge_length, 
                scale, 
                fill_color=data.theme.Settings_Label_Background,
                line_width=3,
                line_color=data.QColor(146,146,146),
            )
            hb.set_first_position(last_step)
            hb.create_grid(
                5,5,0,2,0,2,3,1,0,2,3,4
            )
            
            # Editor buttons
            offset = (90, 280)
            offset = add_offset(offset)
            row_length = 6
            editor_button_count = 30
            hb = components.HexBuilder(
                qpainter, 
                offset, 
                edge_length, 
                scale, 
                fill_color=back_color,
                line_width=2,
                line_color=edge_color,
            )
            grid_list = hb.generate_square_grid_list(
                row_length, editor_button_count
            )
            hb.create_grid(*grid_list)
            # Editor edge
            hb.next_step_move(3)
            first_edge_hex_position = hb.get_last_position()
            hb = components.HexBuilder(
                qpainter, 
                first_edge_hex_position, 
                edge_length, 
                scale, 
                fill_color=back_color,
                line_width=2,
                line_color=edge_color,
            )
            grid_list = [
                (4, True), (5, True), (4, True), 
                (5, True), (4, True), (5, True), 
                (0, True), (0, True), (0, True),
                (0, True), (0, True), (1, True),
                (1, True), (2, True), (1, True),
                (2, True), (1, True), (2, True),
                (3, True), (3, True), (3, True),
                (3, True), (3, True),
            ]
            hb.create_grid(*grid_list)
            
            # General buttons
            offset = (offset[0]+(8*hb.horizontal_step), offset[1]-(6*hb.vertical_step))
            row_length = 7
            general_button_count = 56
            hb = components.HexBuilder(
                qpainter, 
                offset, 
                edge_length, 
                scale, 
                fill_color=back_color,
                line_width=2,
                line_color=edge_color,
            )
            grid_list = hb.generate_square_grid_list(
                row_length, general_button_count
            )
            hb.create_grid(*grid_list)
            # General edge
            hb.next_step_move(3)
            first_edge_hex_position = hb.get_last_position()
            hb = components.HexBuilder(
                qpainter, 
                first_edge_hex_position, 
                edge_length, 
                scale, 
                fill_color=back_color,
                line_width=2,
                line_color=edge_color,
            )
            grid_list = [
                (1, True), (2, True), (1, True), (2, True), (1, True), (2, True), (1, True), 
                (0, True), (0, True), (0, True), (0, True), (0, True), (0, True), (0, True), 
                (0, True), (5, True), (5, True), (4, True), (5, True), (4, True), (5, True), 
                (4, True), (4, True), (3, True), (3, True), (3, True), (3, True), (3, True), 
                (3, True), (3, True), (3, True), 
            ]
            hb.create_grid(*grid_list)
            
            qpainter.end()
            SettingsGuiManipulator.settings_background_image = data.QPixmap.fromImage(settings_background_image)
        return SettingsGuiManipulator.settings_background_image
    
    def clean_up(self):
        # Clean up main references
        self._parent = None
        self.main_form = None
        # Function for deleting an attribute
        def delete_attribute(att_name):
            attr = getattr(self, att_name)
            attr.setParent(None)
            attr.deleteLater()
            delattr(self, att_name)
        # List of attributes for clean up
        clean_up_list = [
#            "display_label",
#            "layout",
        ]
        for att in clean_up_list:
            delete_attribute(att)
        # Clean up self
        self.setParent(None)
        self.deleteLater()
    
    def __init__(self, parent=None, main_form=None):
        # Initialize the superclass
        super().__init__(parent)
        # Store the reference to the main form
        self.main_form = main_form
        # Set default font
        self.setFont(data.get_current_font())
        # Set the shown property to False
        self.shown = False
        # Initialize button list
        self.buttons = []
        # Initialize the background image
        self._init_background()
        # Position the overlay to the center of the screen
        self.center(
            data.QSize(*self.DEFAULT_SIZE)
        )
        # Scale the size if needed
        self._init_scaling()
        # Initialize the display label that will display the various information
        self._init_info_label()
        # Initialize the buttons
        self._init_key_shortcut_buttons()
    
    def _init_scaling(self):
        main_scale = 1.0
        
        """
        All keyboard shortcut option
        """
        self.scale_factor = main_scale
        self.button_scale_factor = main_scale + ((1.0 - main_scale) * (0.625)) #main_scale + ((1.0 - main_scale) * (0.625))
        self.button_offset_factor = main_scale #main_scale * (((main_scale - 1.0) * 2) + 1.0)
        self.scale(main_scale, main_scale)
        # General buttons
        x = 451
        y = 141
        x_offset = x * (main_scale - 1.0)
        y_offset = y * (main_scale - 1.0)
        x += x_offset
        y += y_offset
        self.buttons_general_position = (x, y)
        # Editor buttons
        x = 135
        y = 277
        x_offset = x * (main_scale - 1.0)
        y_offset = y * (main_scale - 1.0)
        x += x_offset
        y += y_offset
        self.buttons_editor_position = (x, y)
    
    def _init_info_label(self):
        self.display_label = data.QLabel(self)
        self.display_label.setGeometry(20, 50, 200, 100)
        font = data.QFont(data.current_font_name, 14)
        font.setBold(True)
        self.display_label.setFont(font)
        self.display_label.setStyleSheet(
            'color: rgb({}, {}, {})'.format(
                data.theme.Font.Default.red(),
                data.theme.Font.Default.green(),
                data.theme.Font.Default.blue(),
            )
        )
        self.display_label.setAlignment(
            data.Qt.AlignHCenter | data.Qt.AlignVCenter
        )
    
    def _init_background(self):
        sgm_picture = data.QPixmap(
            SettingsGuiManipulator.create_background_image(self.scale_factor)
        )
        self.picture = data.QLabel(self)
        self.picture.setPixmap(sgm_picture)
        self.picture.setScaledContents(True)
        self.layout = data.QGridLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(
            data.QMargins(10,10,10,10)
        )
        self.layout.addWidget(self.picture)
        self.setLayout(self.layout)

        self.setStyleSheet("background-color:transparent;")
        self.setStyleSheet("border:0;")
        
    def _init_key_shortcut_buttons(self):
        def mouse_enter_function(button, info_text, key_combination, func=None):
            info = info_text.split("\n")[0]
            if '\t' in info:
                info = info[:info.find('\t')]
            keys = info_text.split("\n")[1]
            if keys.startswith('(#'):
                keys = '(' + keys[2:]
            if "[" in keys and "]" in keys:
                keys = keys.replace("[", "").replace("]", "").replace("\"", "").replace("'", "")
            text = textwrap.fill(info + "\n" + keys, 14) 
            self.display_label.setText(text)
            # Execute the function
            found_duplicate = False
            for b in self.buttons:
                if b.name != button.name:
                    if b.key_combination == key_combination:
                        b.set_red()
                        found_duplicate = True
            if found_duplicate == True:
                button.set_red()
            else:
                button.set_green()
            if func != None:
                func()
        def mouse_leave_function(button, key_combination, func=None):
            self.display_label.setText("")
            # Execute the function
            for b in self.buttons:
                b.reset_color()
            button.reset_color()
            if func != None:
                func()
        
        # Initialize button list
        self.buttons = []
        # Initialize the button icons and functions
        buttons = []
        editor_buttons = []
        funcs = data.global_function_information
        # Append the Bookmark goto and store button information
        funcs["bookmark_goto"] = (
            "Bookmark Goto", 
            None, 
            data.global_function_information["bookmark_goto_0"][2],
            data.global_function_information["bookmark_goto_0"][3].replace("+0", ""),
            "Goto a stored bookmark"
        )
        funcs["bookmark_store"] = (
            "Bookmark Store", 
            None, 
            data.global_function_information["bookmark_store_0"][2],
            data.global_function_information["bookmark_store_0"][3].replace("+0", ""),
            "Store bookmark"
        )
        key_list = list(funcs.keys())
        key_list.sort()
        for k in key_list:
            # Skip the individual bookmark goto and store key combinations
            if k.startswith("bookmark_goto_") or k.startswith("bookmark_store_"):
                continue
            b_name = funcs[k][0] # Name
            b_icon = funcs[k][2] # Icon
            b_keys = funcs[k][3] # Key combination
            if b_icon != None and b_keys != None:
                # MouseEnter function
                mef = functools.partial(
                    mouse_enter_function, 
                    info_text="{}\n({})".format(b_name, b_keys),
                    key_combination=b_keys
                )
                # MouseLeave function
                mlf = functools.partial(
                    mouse_leave_function, 
                    key_combination=b_keys,
                    func=None
                )
                if settings.Keys.check_combination(b_keys):
                    buttons.append(
                        (b_name, b_icon, b_keys, mef, mlf)
                    )
                elif settings.Editor.Keys.check_combination(b_keys):
                    editor_buttons.append(
                        (b_name, b_icon, b_keys, mef, mlf)
                    )
                else:
                    buttons.append(
                        (b_name, b_icon, b_keys, mef, mlf)
                    )
        
        # Adjusted button edge length relative to the background
        # HexBuilder edge length.
        button_edge_length = 26
        # General button positions
        first_button_position = (
            self.buttons_general_position[0], 
            self.buttons_general_position[1]
        )
        grid_generator = components.GridGenerator(
            first_button_position, 
            edge_length=button_edge_length,
            grid_type="rectangular", 
            grid_columns=7,
            in_scale=self.button_offset_factor
        )
        grid_steps = [grid_generator.get_position()]
        for i in range(len(buttons)):
            next_step = grid_generator.next()
            x_add = 0.0
            y_add = 0.0
            grid_steps.append(
                (next_step[0] + x_add, next_step[1] + y_add)
            )
        positions = [x for x in grid_steps]
        if len(buttons) > len(positions):
            raise Exception("Settings buttons have to have their positions defined!")
        buttons = [((-positions[i][0], -100), positions[i], b[0], b[1], b[2], b[3], b[4]) 
                        for i,b in enumerate(buttons)]
        for b in buttons:
            button = self.EnlargeButton(
                b[2], 
                b[3],
                self.button_scale_factor,
                key_combination=b[4],
                starting_position = b[0],
                end_position = b[1],
                parent=self
            )
            button.set_enter_function(b[5])
            button.set_leave_function(b[6])
            button.goto_starting_position()
            self.buttons.append(button)
        
        # Editor button positions
        first_button_position = (
            self.buttons_editor_position[0], 
            self.buttons_editor_position[1]
        )
        grid_generator = components.GridGenerator(
            first_button_position,
            edge_length=button_edge_length,
            grid_type="rectangular", 
            grid_columns=6,
            in_scale=self.button_offset_factor
        )
        grid_steps = [grid_generator.get_position()]
        for i in range(len(editor_buttons)):
            next_step = grid_generator.next()
            x_add = 0.0
            y_add = 0.0
            grid_steps.append(
                (next_step[0] + x_add, next_step[1] + y_add)
            )
        positions = [x for x in grid_steps]
        if len(editor_buttons) > len(positions):
            raise Exception("Settings buttons have to have their positions defined!")
        editor_buttons = [
            ((-positions[i][0], -100), positions[i], b[0], b[1], b[2], b[3], b[4]) 
                for i,b in enumerate(editor_buttons)
        ]
        for b in editor_buttons:
            button = self.EnlargeButton(
                b[2], 
                b[3],
                self.button_scale_factor,
                key_combination=b[4],
                starting_position = b[0],
                end_position = b[1],
                parent=self
            )
            button.set_enter_function(b[5])
            button.set_leave_function(b[6])
            button.goto_starting_position()
            self.buttons.append(button)
    
    def center(self, size):
        """
        Center the settings GUI manipulator to the main form,
        according to the size parameter
        """
        x_offset = int((self.main_form.size().width() - size.width()) / 2)
        y_offset = int((self.main_form.size().height()*93/100 - size.height()) / 2)
        rectangle_top_left  = data.QPoint(x_offset, y_offset)
        rectangle_size = size
        rectangle = data.QRect(rectangle_top_left, rectangle_size)
        self.setGeometry(rectangle)
    
    def get_center(self):
        """
        Find the center of the widget rectangle
        """
        geometry = self.geometry()
        x = geometry.x()
        y = geometry.y()
        width = geometry.width()
        height = geometry.height()
        return (width / 2), (height / 2)
    
    def scale(self, width_scale_factor=1, height_scale_factor=1):
        """Scale the size of the function wheel and all of its child widgets"""
        #Scale the function wheel form
        geo = self.geometry()
        new_width = int(geo.width() * width_scale_factor)
        new_height = int(geo.height() * height_scale_factor)
        rectangle = data.QRect(
            geo.topLeft(), 
            data.QSize(new_width, new_height)
        )
        self.setGeometry(rectangle)
        #Scale all of the function wheel child widgets
        for button in self.children():
            geo = button.geometry()
            new_topLeft = data.QPoint(
                int(geo.topLeft().x() * width_scale_factor),
                int(geo.topLeft().y() * height_scale_factor)
            )
            new_width = int(geo.width() * width_scale_factor)
            new_height = int(geo.height() * height_scale_factor)
            new_size = data.QSize(new_width, new_height)
            rectangle   = data.QRect(new_topLeft, new_size)
            button.setGeometry(rectangle)
        #Center to main form
        self.center(self.size())
    
    def animate(self):
        def end(new_state, old_state, button):
            button.set_start_position()
            if new_state == data.QPropertyAnimation.Stopped:
#                button.set_green()
                button.enable()
                button.add_to_queue("leave")
                if button.animating == False:
                    button.animate()
                
        animation_time = 300
        animation_delay = 20
        def _animate(animation):
            animation.start()
        for i,b in enumerate(self.buttons):
            b.raise_()
            animation = data.QPropertyAnimation(b, b"geometry")
            animation.setStartValue(
                data.QRect(
                    b.starting_position[0],
                    b.starting_position[1],
                    b.geometry().width(), 
                    b.geometry().height()
                )
            )
            animation.setEndValue(
                data.QRect(
                    b.end_position[0],
                    b.end_position[1],
                    b.geometry().width(), 
                    b.geometry().height()
                )
            )
            animation.stateChanged.connect(functools.partial(end, button=b))
            animation.setDuration(animation_time)
            animation_time += 5
#            animation.setEasingCurve(data.QEasingCurve.InQuad)

#            animation_timer = data.QTimer(self)
#            animation_timer.setInterval(animation_delay)
#            animation_delay += 5
#            animation_timer.setSingleShot(True)
#            animation_timer.timeout.connect(functools.partial(_animate, animation))
#            animation_timer.start()
            
            animation.start()
            self.animations.append(animation)
    
    def show(self):
        self.display_label.setText("")
        self.setVisible(True)
        self.setEnabled(True)
        #Center to main form
        self.center(self.size())
        self.setFocus()
        self.animate()
        self.shown = True
    
    def hide(self):
        for b in self.buttons:
            b.disable()
        #Disable the function wheel
        self.setVisible(False)
        self.setEnabled(False)
        self.shown = False
    
    def keyPressEvent(self, e):
        super().keyPressEvent(e)
        pressed_key = e.key()
        if pressed_key == data.Qt.Key_Escape:
            self.hide()
