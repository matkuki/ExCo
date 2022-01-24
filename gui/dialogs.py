
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
---------------------------------------------------------
Custom Yes/No dialog window
---------------------------------------------------------
""" 
class YesNoDialog(data.QDialog):
    class Button(data.QLabel):
        pixmap = None
        text = None
        return_code = None
        scale = 1.0
        
        on_signal = data.pyqtSignal()
        off_signal = data.pyqtSignal()
        
        def __init__(self, parent, image, text, return_code, scale=1.0):
            # Initialize superclass
            super().__init__(parent)
            # Set the on/off images
            self.pixmap = data.QPixmap(image)
            self.scale = scale
            if scale != 1.0:
                self.pixmap = self.pixmap.scaled(
                    self.pixmap.size() * scale, 
                    transformMode=data.Qt.SmoothTransformation
                )
            # Set the text and return code
            self.text = text
            self.return_code = return_code
            # Enable mouse move events
            self.setMouseTracking(True)
            self.setScaledContents(True)
            # Disable the button on startup
            self.off()
        
        def draw(self, opacity):
            image = data.QImage(
                self.pixmap.size(),
                data.QImage.Format_ARGB32_Premultiplied
            )
            image.fill(data.Qt.transparent)
            painter = data.QPainter(image)
            painter.setOpacity(opacity)
            painter.drawPixmap(0, 0, self.pixmap)
            
            if opacity < 0.5:
                painter.setPen(data.theme.Font.Default)
            else:
                painter.setPen(data.QColor(255, 255, 255))
            painter.setFont(
                data.QFont(
                    'Segoe UI', int(16 * self.scale), data.QFont.Bold
                )
            )
            painter.setOpacity(1.0)
            painter.drawText(
                self.pixmap.rect(), data.Qt.AlignCenter, self.text
            )
            painter.end()
            # Display the manipulated image
            self.setPixmap(data.QPixmap.fromImage(image))
            # Set the button mask, which sets the button area to the shape of
            # the button image instead of a rectangle
            self.setMask(self.pixmap.mask())
        
        def on(self):
            self.draw(1.0)
        
        def off(self):
            self.draw(0.0)
        
        def mouseMoveEvent(self, event):
            super().mouseMoveEvent(event)
            # Show the button
            self.on()
            self.on_signal.emit()
        
        def enterEvent(self, event):
            super().enterEvent(event)
            # Bring the widget to the front of the Z-axis stack
            self.raise_()
            # Show the button
            self.on()
            self.on_signal.emit()
        
        def leaveEvent(self, event):
            super().leaveEvent(event)
            # Hide the button
            self.off()
            self.off_signal.emit()
        
        def mousePressEvent(self, event):
            #Execute the superclass mouse click event first
            super().mousePressEvent(event)
            self.parent().done(self.return_code)
    
    state = False
    scale = 1.0
    
    def __init__(self, text, dialog_type=None, parent=None):
        super().__init__(parent)
        # Make the dialog stay on top
        self.setWindowFlags(data.Qt.WindowStaysOnTopHint)
        # Set the dialog icon and title
        self.setWindowIcon(data.QIcon(data.application_icon))
        self.setWindowTitle(dialog_type.title())
        self.init_layout(text, dialog_type)
        # Set default font
        self.setFont(data.get_current_font())

    def init_layout(self, text, dialog_type):
        # Setup the image
        # First create the background image using the hex builder
        back_image = data.QImage(
            functions.create_size(246, 211),
            data.QImage.Format_ARGB32_Premultiplied
        )
        back_image.fill(data.Qt.transparent)
        painter = data.QPainter(back_image)
        painter.setRenderHints(
            data.QPainter.Antialiasing | 
            data.QPainter.TextAntialiasing | 
            data.QPainter.SmoothPixmapTransform
        )
        hex_builder = components.HexBuilder(
            painter, 
            (123,28), 
            30, 
            1.0, 
            fill_color=data.theme.YesNoDialog_Background,
            line_width=3,
            line_color=data.theme.YesNoDialog_Edge,
        )
        hex_builder.create_grid(
            True,2,2,3,4,0,5,3,(3,True),5,0,0,4,3 # YesNoDialog
        )
        painter.end()
        original_dialog_image = data.QPixmap.fromImage(back_image)
        
        # Now add the images according to the type of dialog
        dialog_image = original_dialog_image.scaled(
            original_dialog_image.size() * self.scale,
            transformMode=data.Qt.SmoothTransformation
        )
        self.image = data.QLabel(self)
        self.image.setPixmap(dialog_image)
        self.image.setGeometry(
            0,
            0,
            int(dialog_image.rect().width() * self.scale),
            int(dialog_image.rect().height() * self.scale),
        )
        self.image.setScaledContents(True)
        # Set the dialog mask to match the image mask
        self.setMask(dialog_image.mask())
        # Setup the image behind the label
        if dialog_type != None:
            if dialog_type == "question":
                type_pixmap = data.QPixmap(
                    os.path.join(
                        data.resources_directory,
                        "various/dialog-question.png"
                    )
                )
            elif dialog_type == "warning":
                type_pixmap = data.QPixmap(
                    os.path.join(
                        data.resources_directory,
                        "various/dialog-warning.png"
                    )
                )
            elif dialog_type == "error":
                type_pixmap = data.QPixmap(
                    os.path.join(
                        data.resources_directory,
                        "various/dialog-error.png"
                    )
                )
            else:
                raise Exception("Wrong dialog type!")
            image = data.QImage(
                type_pixmap.size(),
                data.QImage.Format_ARGB32_Premultiplied
            )
            image.fill(data.Qt.transparent)
            painter = data.QPainter(image)
            painter.setOpacity(0.2)
            painter.drawPixmap(0, 0, type_pixmap)
            painter.end()
            type_pixmap = data.QPixmap.fromImage(image)
            type_pixmap = type_pixmap.scaled(
                type_pixmap.size() * 2.0 * self.scale, 
                transformMode=data.Qt.SmoothTransformation
            )
            self.type_label = data.QLabel(self)
            self.type_label.setPixmap(type_pixmap)
            type_label_rect = functions.create_rect(
                (self.image.rect().width() - type_pixmap.rect().width())/2 * self.scale,
                (self.image.rect().height() - type_pixmap.rect().height())/2 * self.scale,
                type_pixmap.rect().width() * self.scale,
                type_pixmap.rect().height() * self.scale,
            )
            self.type_label.setGeometry(type_label_rect)
        # Setup the text label
        self.text = text
        self.label = data.QLabel(self)
        self.label.setFont(
            data.QFont(
                'Segoe UI', int(12 * self.scale), data.QFont.Bold
            )
        )
        self.label.setWordWrap(True)
        self.label.setAlignment(data.Qt.AlignCenter)
        self.label.setStyleSheet(
            'color: rgb({}, {}, {})'.format(
                data.theme.Font.Default.red(),
                data.theme.Font.Default.green(),
                data.theme.Font.Default.blue(),
            )
        )
        self.label.setText(text)
        width_diff = self.image.rect().width() - original_dialog_image.width()
        height_diff = self.image.rect().height() - original_dialog_image.height()
        x_offset = 20 * (self.scale - 1.0)
        y_offset = 60 * (self.scale - 1.0)
        label_rect = functions.create_rect(
            dialog_image.rect().x() + 20 + x_offset,
            dialog_image.rect().y() + 60 + y_offset,
            dialog_image.rect().width() - (40 * self.scale),
            dialog_image.rect().height() - (120* self.scale),
        )
        self.label.setGeometry(label_rect)
        # Shrink text if needed
        for i in range(10):
            label_width = label_rect.width()
            label_height = label_rect.height()
            font_metrics = data.QFontMetrics(self.label.font())
            bounding_rectangle = font_metrics.boundingRect(
                functions.create_rect(0, 0, label_width, label_height),
                self.label.alignment() | data.Qt.TextWordWrap,
                text
            )
            if (bounding_rectangle.width() > label_width or 
                bounding_rectangle.height() > label_height):
                self.label.setFont(
                    data.QFont(
                        'Segoe UI', int((12-i) * self.scale), data.QFont.Bold
                    )
                )
            else:
                break
        # Setup the buttons
        self.button_yes = self.Button(
            self, 
            os.path.join(
                data.resources_directory,
                "various/hex-green.png"
            ),
            "Yes", 
            data.QMessageBox.Yes, 
            self.scale
        )
        x_offset = 93 * (self.scale - 1.0)
        y_offset = 3 * (self.scale - 1.0)
        self.button_yes.setGeometry(
            int(93+x_offset),
            int(3+y_offset),
            int(59 * self.scale),
            int(50 * self.scale)
        )
        self.button_yes.on_signal.connect(self.update_state_on)
        self.button_yes.off_signal.connect(self.update_state_reset)
        self.button_no = self.Button(
            self, 
            os.path.join(
                data.resources_directory,
                "various/hex-red.png"
            ),
            "No", 
            data.QMessageBox.No, 
            self.scale
        )
        x_offset = 93 * (self.scale - 1.0)
        y_offset = 158 * (self.scale - 1.0)
        self.button_no.setGeometry(
            int(93+x_offset),
            int(158+y_offset),
            int(59 * self.scale),
            int(50 * self.scale)
        )
        self.button_no.on_signal.connect(self.update_state_off)
        self.button_no.off_signal.connect(self.update_state_reset)
        # Setup the layout
        self.layout = data.QGridLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(data.QMargins(0,0,0,0))
        self.layout.addWidget(self.image)
        self.setLayout(self.layout)
        # Setup tranparency and borders
        if data.on_rpi == True:
            self.image.setStyleSheet(
                "border:0;" +
                "background-color:white;"
            )
        else:
            self.image.setAttribute(data.Qt.WA_TranslucentBackground)
            self.image.setStyleSheet(
                "border:0;" +
                "background-color:transparent;"
            )
        self.setAttribute(data.Qt.WA_TranslucentBackground)
        self.setStyleSheet(
            "border:0;" +
            "background-color:transparent;"
        )
        
        self.setGeometry(dialog_image.rect())
        self.center()
        self.setWindowFlags(data.Qt.FramelessWindowHint)
    
    def update_state_on(self):
        self.state = True
        self.button_no.off()
    
    def update_state_off(self):
        self.state = False
        self.button_yes.off()
    
    def update_state_reset(self):
        self.state = None
    
    def state_on(self):
        self.state = True
        self.button_no.off()
        self.button_yes.on()
    
    def state_off(self):
        self.state = False
        self.button_no.on()
        self.button_yes.off()
    
    def state_reset(self):
        self.state = None
        self.button_no.off()
        self.button_yes.off()
    
    def center(self):
        if self.parent() != None:
            qr = self.frameGeometry()
            geo = self.parent().frameGeometry()
            cp = functions.create_point(
                int((geo.width() / 2) - (qr.width() / 2)),
                int((geo.height() / 2) - (qr.height() / 2))
            )
            self.move(cp)
        else:
            qr = self.frameGeometry()
            cp = data.QDesktopWidget().availableGeometry().center()
            qr.moveCenter(cp)
            self.move(qr.topLeft())
    
    def keyPressEvent(self, key_event):
        pressed_key = key_event.key()
        #Check for escape keypress
        if pressed_key == data.Qt.Key_Escape:
            self.button_no.on()
            self.repaint()
            time.sleep(0.1)
            self.done(data.QMessageBox.No)
        elif pressed_key == data.Qt.Key_Down:
            self.state_off()
        elif pressed_key == data.Qt.Key_Up:
            self.state_on()
        elif pressed_key == data.Qt.Key_Enter or pressed_key == data.Qt.Key_Return:
            if self.state == True:
                self.done(data.QMessageBox.Yes)
            elif self.state == False:
                self.done(data.QMessageBox.No)
    
    @classmethod
    def blank(cls, text):
        return cls(text).exec_()
    
    @classmethod
    def question(cls, text):
        return cls(text, "question").exec_()
    
    @classmethod
    def warning(cls, text):
        return cls(text, "warning").exec_()
    
    @classmethod
    def error(cls, text):
        return cls(text, "error").exec_()

class OkDialog(YesNoDialog):
    def init_layout(self, text, dialog_type):
        # Setup the image
        # First create the background image using the hex builder
        back_image = data.QImage(
            functions.create_size(246, 211),
            data.QImage.Format_ARGB32_Premultiplied
        )
        back_image.fill(data.Qt.transparent)
        painter = data.QPainter(back_image)
        painter.setRenderHints(
            data.QPainter.Antialiasing | 
            data.QPainter.TextAntialiasing | 
            data.QPainter.SmoothPixmapTransform
        )
        hex_builder = components.HexBuilder(
            painter, 
            (123,28), 
            30, 
            1.0, 
            fill_color=data.theme.YesNoDialog_Background,
            line_width=3,
            line_color=data.theme.YesNoDialog_Edge,
        )
        hex_builder.create_grid(
            False,2,2,3,4,0,5,3,(3,True),5,0,0,4,3 # OkDialog
        )
        painter.end()
        original_dialog_image = data.QPixmap.fromImage(back_image)
        
        # Now add the images according to the type of dialog
        dialog_image = original_dialog_image.scaled(
            original_dialog_image.size() * self.scale,
            transformMode=data.Qt.SmoothTransformation
        )
        self.image = data.QLabel(self)
        self.image.setPixmap(dialog_image)
        self.image.setGeometry(
            0,
            0,
            int(dialog_image.rect().width() * self.scale),
            int(dialog_image.rect().height() * self.scale),
        )
        self.image.setScaledContents(True)
        # Set the dialog mask to match the image mask
        self.setMask(dialog_image.mask())
        # Setup the image behind the label
        if dialog_type != None:
            if dialog_type == "question":
                type_pixmap = data.QPixmap(
                    os.path.join(
                        data.resources_directory,
                        "various/dialog-question.png"
                    )
                )
            elif dialog_type == "warning":
                type_pixmap = data.QPixmap(
                    os.path.join(
                        data.resources_directory,
                        "various/dialog-warning.png"
                    )
                )
            elif dialog_type == "error":
                type_pixmap = data.QPixmap(
                    os.path.join(
                        data.resources_directory,
                        "various/dialog-error.png"
                    )
                )
            else:
                raise Exception("Wrong dialog type!")
            image = data.QImage(
                type_pixmap.size(),
                data.QImage.Format_ARGB32_Premultiplied
            )
            image.fill(data.Qt.transparent)
            painter = data.QPainter(image)
            painter.setOpacity(0.2)
            painter.drawPixmap(0, 0, type_pixmap)
            painter.end()
            type_pixmap = data.QPixmap.fromImage(image)
            type_pixmap = type_pixmap.scaled(
                type_pixmap.size() * 2.0 * self.scale, 
                transformMode=data.Qt.SmoothTransformation
            )
            self.type_label = data.QLabel(self)
            self.type_label.setPixmap(type_pixmap)
            type_label_rect = functions.create_rect(
                (self.image.rect().width() - type_pixmap.rect().width())/2 * self.scale,
                (self.image.rect().height() - type_pixmap.rect().height())/2 * self.scale,
                type_pixmap.rect().width() * self.scale,
                type_pixmap.rect().height() * self.scale,
            )
            self.type_label.setGeometry(type_label_rect)
        # Setup the text label
        self.text = text
        self.label = data.QLabel(self)
        self.label.setFont(
            data.QFont(
                'Segoe UI', int(12 * self.scale), data.QFont.Bold
            )
        )
        self.label.setWordWrap(True)
        self.label.setAlignment(data.Qt.AlignCenter)
        self.label.setStyleSheet(
            'color: rgb({}, {}, {})'.format(
                data.theme.Font.Default.red(),
                data.theme.Font.Default.green(),
                data.theme.Font.Default.blue(),
            )
        )
        self.label.setText(text)
        width_diff = self.image.rect().width() - original_dialog_image.width()
        height_diff = self.image.rect().height() - original_dialog_image.height()
        x_offset = 20 * (self.scale - 1.0)
        y_offset = 60 * (self.scale - 1.0)
        label_rect = functions.create_rect(
            dialog_image.rect().x() + 20 + x_offset,
            dialog_image.rect().y() + 60 + y_offset,
            dialog_image.rect().width() - (40 * self.scale),
            dialog_image.rect().height() - (120* self.scale),
        )
        self.label.setGeometry(label_rect)
        # Shrink text if needed
        for i in range(10):
            label_width = label_rect.width()
            label_height = label_rect.height()
            font_metrics = data.QFontMetrics(self.label.font())
            bounding_rectangle = font_metrics.boundingRect(
                functions.create_rect(0, 0, label_width, label_height),
                self.label.alignment() | data.Qt.TextWordWrap,
                text
            )
            if (bounding_rectangle.width() > label_width or 
                bounding_rectangle.height() > label_height):
                self.label.setFont(
                    data.QFont(
                        'Segoe UI', int((12-i) * self.scale), data.QFont.Bold
                    )
                )
            else:
                break
        # Setup the buttons
        self.button_no = self.Button(
            self, 
            os.path.join(
                data.resources_directory,
                "various/hex-red.png"
            ),
            "OK", 
            data.QMessageBox.No, 
            self.scale
        )
        x_offset = 93 * (self.scale - 1.0)
        y_offset = 158 * (self.scale - 1.0)
        self.button_no.setGeometry(
            int(93+x_offset),
            int(158+y_offset),
            int(59 * self.scale),
            int(50 * self.scale)
        )
        self.button_no.on_signal.connect(self.update_state_off)
        self.button_no.off_signal.connect(self.update_state_reset)
        # Setup the layout
        self.layout = data.QGridLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(data.QMargins(0,0,0,0))
        self.layout.addWidget(self.image)
        self.setLayout(self.layout)
        # Setup tranparency and borders
        if data.on_rpi == True:
            self.image.setStyleSheet(
                "border:0;" +
                "background-color:white;"
            )
        else:
            self.image.setAttribute(data.Qt.WA_TranslucentBackground)
            self.image.setStyleSheet(
                "border:0;" +
                "background-color:transparent;"
            )
        self.setAttribute(data.Qt.WA_TranslucentBackground)
        self.setStyleSheet(
            "border:0;" +
            "background-color:transparent;"
        )
        
        self.setGeometry(dialog_image.rect())
        self.center()
        self.setWindowFlags(data.Qt.FramelessWindowHint)
    
    def update_state_off(self):
        self.state = False
    
    def keyPressEvent(self, key_event):
        pressed_key = key_event.key()
        # Check for escape keypress
        if pressed_key == data.Qt.Key_Escape:
            self.button_no.on()
            self.repaint()
            time.sleep(0.1)
            self.done(data.QMessageBox.No)
        elif pressed_key == data.Qt.Key_Down:
            self.state_off()
        # Check for Enter/Return keypress
        elif pressed_key == data.Qt.Key_Enter or pressed_key == data.Qt.Key_Return:
            self.done(data.QMessageBox.No)