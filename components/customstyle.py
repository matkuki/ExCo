# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2023 Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import re
import math
import typing

import data
import functions


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
        if data.custom_menu_font is not None:
            self.custom_font = data.QFont(*data.custom_menu_font)
            self.custom_font_metrics = data.QFontMetrics(self.custom_font)
    
    def drawComplexControl(self, cc, opt, p, widget=None):
        self._style.drawComplexControl(cc, opt, p, widget)
        
    def drawControl(self, element, opt, p, widget=None):
        if element == data.QStyle.ControlElement.CE_MenuItem: 
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
                alignment = data.Qt.Alignment.AlignRight
                self.drawItemPixmap(p, opt.rect, alignment, pixmap)
        elif element == data.QStyle.ControlElement.CE_MenuBarItem:
            text = opt.text.replace("&", "")
            opt.text = ""
            self._style.drawControl(element, opt, p, widget)
            alignment = data.Qt.AlignCenter
            p.setFont(self.custom_font)
            self.drawItemText(
                p, opt.rect, alignment, opt.palette, opt.state, text, data.QPalette.ColorRole.NoRole
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
    
    def drawItemText(self, painter, rectangle, alignment, palette, enabled, text, textRole=data.QPalette.ColorRole.NoRole):
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
        if m == data.QStyle.PixelMetric.PM_SmallIconSize:
            if self.scale_constant is None:
                return 16
            else:
                return self.scale_constant
        elif m == data.QStyle.PrimitiveElement.PE_IndicatorProgressChunk:
            # This is the Menubar, don't know why it's called IndicatorProgressChunk?
            return int(0.5)
        else:
            return self._style.pixelMetric(m, option, widget)

    def polish(self, widget):
        return self._style.polish(widget)
    
    def sizeFromContents(self, ct, opt, contentsSize, widget=None):
        if self.custom_font_metrics is not None and ct == data.QStyle.ContentsType.CT_MenuItem:
            scaled_width = self.scale_constant*1.5
            resized_width = self.custom_font_metrics.tightBoundingRect(opt.text).width() + scaled_width
            result = data.QSize(int(resized_width), int(self.scale_constant))
            return result
        elif self.custom_font_metrics is not None and ct == data.QStyle.ContentsType.CT_MenuBarItem:
            base_width = self.custom_font_metrics.tightBoundingRect(opt.text).width()
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