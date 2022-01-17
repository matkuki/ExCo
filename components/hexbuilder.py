
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2019 Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import data
import functions
import re
import math
import typing
from .gridgenerator import *


class HexBuilder:
    first_position = None
    painter = None
    edge_length = None
    scale = None
    
    fill_color = None
    line_width = None
    line_color = None
    
    steps = None
    horizontal_step = None
    vertical_step = None
    grid_positions = None
    
    painted_hex_counter = 0
    SHOW_FIELD_NUMBERS = False
    
    # List of already painted lines
    stored_lines = []
    
    @staticmethod
    def generate_hexagon_points(edge_length, offset_position):
        """Generator for coordinates in a hexagon."""
        x, y = offset_position
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
        
        self.horizontal_step, self.vertical_step, self.steps = GridGenerator.init_steps(
            self.edge_length, self.scale
        )
        
        self.fill_color = fill_color
        self.line_width = line_width
        self.line_color = line_color
        
        self.stored_lines = []
    
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
        number_of_steps = len(GridGenerator.directions)
        steps = [self.steps[GridGenerator.directions[x]] for x in range(number_of_steps)]
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
        next_step = self.steps[GridGenerator.directions[direction]]        
        last_position = self.grid_positions[-1]
        self.grid_positions.append(
            (last_position[0] + next_step[0], last_position[1] + next_step[1])
        )
        return self.grid_positions[-1]
    
    def draw(self):
        self.draw_filled_hexagon(
            position = self.grid_positions[-1], 
            fill_color = self.fill_color,
            number = self.painted_hex_counter,
        )
        self.painted_hex_counter += 1
    
    def draw_line_hexagon_no_double_paint(self, 
                                          position, 
                                          line_width, 
                                          line_color,
                                          paint_enabled=[
                                            True,True,True,True,True,True
                                          ],
                                          shadow=False):
        qpainter = self.painter
        
        if line_width == 0:
            return
        
        pen = data.QPen(data.Qt.SolidLine)
        pen.setCapStyle(data.Qt.RoundCap)
        pen.setJoinStyle(data.Qt.RoundJoin)
        pen.setWidth(int(line_width))
        pen.setColor(line_color)
        qpainter.setPen(pen)
        hex_points = list(
            HexBuilder.generate_hexagon_points(self.edge_length, position)
        )
        x_correction = self.edge_length / 2
        y_correction = self.edge_length / (2 * math.tan(math.radians(30)))
        hex_points = [(int(x-x_correction), int(y-y_correction)) for x, y in hex_points]
        hex_lines = []
        
        def line_test(in_line):
            DIFF = 3
            line = in_line
            reversed_line = (line[1], line[0])
            x1, y1 = line[0]
            x2, y2 = line[1]
            xr1, yr1 = reversed_line[0]
            xr2, yr2 = reversed_line[1]
            for l in self.stored_lines:
                xl1, yl1 = l[0]
                xl2, yl2 = l[1]
                if (abs(xl1 - x1) < DIFF and 
                    abs(yl1 - y1) < DIFF and
                    abs(xl2 - x2) < DIFF and 
                    abs(yl2 - y2) < DIFF):
                        if not(line in self.stored_lines):
                            self.stored_lines.append(line)
                            #self.stored_lines.append(reversed_line)
                        return False
                elif (abs(xl1 - xr1) < DIFF and 
                    abs(yl1 - yr1) < DIFF and
                    abs(xl2 - xr2) < DIFF and 
                    abs(yl2 - yr2) < DIFF):
                        if not(reversed_line in self.stored_lines):
                            self.stored_lines.append(line)
                            #self.stored_lines.append(reversed_line)
                        return False
            else:
                self.stored_lines.append(line)
                self.stored_lines.append(reversed_line)
                return True
        
        for i in range(len(hex_points)):
            if paint_enabled[i] == False:
                continue
            n = i + 1
            if n > (len(hex_points)-1):
                n = 0
            if line_test((hex_points[i], hex_points[n])) == True:
                hex_lines.append(
                    data.QLine(
                        functions.create_point(*hex_points[i]), 
                        functions.create_point(*hex_points[n])
                    )
                )
        if hex_lines:
            if shadow == True:
                shadow_0_color = data.QColor(line_color)
                shadow_0_color.setAlpha(64)
                shadow_1_color = data.QColor(line_color)
                shadow_1_color.setAlpha(128)
                
                pen.setWidth(int(line_width*2.0))
                pen.setColor(shadow_0_color)
                qpainter.setPen(pen)
                qpainter.drawLines(*hex_lines)
                pen.setWidth(int(line_width*1.5))
                pen.setColor(shadow_1_color)
                qpainter.setPen(pen)
                qpainter.drawLines(*hex_lines)
                pen.setWidth(int(line_width))
                pen.setColor(line_color)
                qpainter.setPen(pen)
                qpainter.drawLines(*hex_lines)
            else:
                qpainter.drawLines(*hex_lines)
    
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
        pen.setWidth(int(line_width))
        pen.setColor(line_color)
        qpainter.setPen(pen)
        hex_points = list(
            HexBuilder.generate_hexagon_points(self.edge_length, position)
        )
        x_correction = self.edge_length / 2
        y_correction = self.edge_length / (2 * math.tan(math.radians(30)))
        hex_points = [(int(x-x_correction), int(y-y_correction)) for x, y in hex_points]
        hex_lines = []
        
        for i in range(len(hex_points)):
            if paint_enabled[i] == False:
                continue
            n = i + 1
            if n > (len(hex_points)-1):
                n = 0
            hex_lines.append(
                data.QLine(
                    functions.create_point(*hex_points[i]), 
                    functions.create_point(*hex_points[n])
                )
            )
        if hex_lines:
            if shadow == True:
                shadow_0_color = data.QColor(line_color)
                shadow_0_color.setAlpha(64)
                shadow_1_color = data.QColor(line_color)
                shadow_1_color.setAlpha(128)
                
                pen.setWidth(int(line_width*2.0))
                pen.setColor(shadow_0_color)
                qpainter.setPen(pen)
                qpainter.drawLines(*hex_lines)
                pen.setWidth(int(line_width*1.5))
                pen.setColor(shadow_1_color)
                qpainter.setPen(pen)
                qpainter.drawLines(*hex_lines)
                pen.setWidth(int(line_width))
                pen.setColor(line_color)
                qpainter.setPen(pen)
                qpainter.drawLines(*hex_lines)
            else:
                qpainter.drawLines(*hex_lines)
    
    def draw_filled_hexagon(self, position, fill_color, number=None):
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
        hex_points = [(int(x-x_correction), int(y-y_correction)) for x, y in hex_points]
        hex_qpoints = [functions.create_point(*x) for x in hex_points]
        qpainter.drawPolygon(*hex_qpoints)
        
        if (self.SHOW_FIELD_NUMBERS == True) and (number != None):
            font = data.QFont('Courier', 8)
            font.setBold(True)
            qpainter.setFont(font)
            pen = data.QPen(data.Qt.SolidLine)
            pen.setColor(data.QColor(0,0,0))
            qpainter.setPen(pen)
            
            font_metric = data.QFontMetrics(font)
            x = int(position[0] - font_metric.width(str(number)) / 2)
            y = int(position[1] + font_metric.height() / 4)
            qpainter.drawText(functions.create_point(x, y), str(number))
    
    def draw_full_hexagon(self,
                          position,
                          fill_color, 
                          line_width, 
                          line_color):
        qpainter = self.painter
        
        pen = data.QPen(data.Qt.SolidLine)
        pen.setColor(line_color)
        pen.setCapStyle(data.Qt.RoundCap)
        pen.setWidth(int(line_width))
        brush = data.QBrush(data.Qt.SolidPattern)
        brush.setColor(fill_color)
        qpainter.setBrush(brush)
        qpainter.setPen(pen)
        hex_points = list(HexBuilder.generate_hexagon_points(self.edge_length, position))
        x_correction = self.edge_length / 2
        y_correction = self.edge_length / (2 * math.tan(math.radians(30)))
        hex_points = [(int(x-x_correction), int(y-y_correction)) for x, y in hex_points]
        hex_qpoints = [functions.create_point(*x) for x in hex_points]
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