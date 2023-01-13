
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


class GridGenerator:
    directions = {
        0: "up",
        1: "up-right",
        2: "down-right",
        3: "down",
        4: "down-left",
        5: "up-left",
    }
    steps = None
    covered_positions = None
    current_direction = None
    first_position = None
    current_position = None
    grid_type = None
    horizontal_step = None
    vertical_step = None
    
    def __init__(self, 
                 starting_position, 
                 edge_length, 
                 grid_type="circular",
                 grid_columns=5,
                 rectangular_grid_first_step="up-right",
                 rectangular_grid_row_addition=0.0,
                 in_scale=1.0):
        self.first_position = (
            starting_position[0],
            starting_position[1]
        )
        self.covered_positions = []
        self.add_position(self.first_position)
        self.current_direction = 1
        if (grid_type != "circular" and 
            grid_type != "trapezoid" and
            grid_type != "rectangular"):
                raise Exception("Unknown grid type specified!")
        elif grid_type == "trapezoid":
            self.grid_columns = grid_columns
            self.step_direction = "down-right"
            self.column_counter = 0
        elif grid_type == "rectangular":
            self.grid_columns = grid_columns
            self.step_direction = rectangular_grid_first_step
            self.rectangular_grid_row_addition = rectangular_grid_row_addition
            self.column_counter = 0
        self.grid_type = grid_type
        
        self.scaling = in_scale
        self.edge_length = edge_length
        self.horizontal_step, self.vertical_step, self.steps = GridGenerator.init_steps(
            self.edge_length, self.scaling
        )
    
    @staticmethod
    def init_steps(edge_length, scaling):
        horizontal_step = (3 * edge_length) / 2
        vertical_step = math.sin(math.pi / 3) * edge_length
        horizontal_step *= scaling
        vertical_step *= scaling
        steps = {
            "down-left": (-horizontal_step, vertical_step),
            "down-right": (horizontal_step, vertical_step),
            "down": (0, 2*vertical_step),
            "up-left": (-horizontal_step, -vertical_step),
            "up-right": (horizontal_step, -vertical_step),
            "up": (0, -2*vertical_step),
        }
        return horizontal_step, vertical_step, steps
    
    def add_position(self, position):
        self.current_position = position
        self.covered_positions.append(position)
    
    def get_position(self):
        return self.current_position
    
    def next(self):
        if self.grid_type == "circular":
            return self.next_circular()
        elif self.grid_type == "trapezoid":
            return self.next_trapezoid()
        elif self.grid_type == "rectangular":
            return self.next_rectangular()
    
    def next_rectangular(self):
        self.column_counter += 1
        spacing_step_x = 0
        spacing_step_y = 0
        spacing = (0, 0)
        if self.column_counter == self.grid_columns:
            self.column_counter = 0
            current_step = self.steps["down"]
            current_step = (
                current_step[0],
                current_step[1] + self.rectangular_grid_row_addition
            )
            spacing = (0, 2 * spacing_step_y)
            if self.step_direction == "down-right":
                self.step_direction = "down-left"
            elif self.step_direction == "up-right":
                self.step_direction = "up-left"
            elif self.step_direction == "down-left":
                self.step_direction = "down-right"
            else:
                self.step_direction = "up-right"
        else:
            current_step = self.steps[self.step_direction]
            if self.step_direction == "down-right":
                self.step_direction = "up-right"
                spacing = (spacing_step_x, spacing_step_y)
            elif self.step_direction == "up-right":
                self.step_direction = "down-right"
                spacing = (spacing_step_x, -spacing_step_y)
            elif self.step_direction == "down-left":
                self.step_direction = "up-left"
                spacing = (-spacing_step_x, spacing_step_y)
            elif self.step_direction == "up-left":
                self.step_direction = "down-left"
                spacing = (-spacing_step_x, -spacing_step_y)
        new_position = (
            self.current_position[0] + current_step[0] + spacing[0],
            self.current_position[1] + current_step[1] + spacing[1],
        )
        new_position = (new_position[0], new_position[1])
        self.add_position(new_position)
        return self.get_position()
    
    def next_trapezoid(self):
        self.column_counter += 1
        if self.column_counter == self.grid_columns:
            self.column_counter = 0
            current_step = self.steps["down"]
            if self.step_direction == "down-right":
                self.step_direction = "up-left"
            else:
                self.step_direction = "down-right"
        else:
            current_step = self.steps[self.step_direction]
        new_position = (
            self.current_position[0] + current_step[0],
            self.current_position[1] + current_step[1],
        )
        self.add_position(new_position)
        return self.get_position()
    
    def next_circular(self):
        current_direction_name = self.directions[self.current_direction]
        current_step = self.steps[current_direction_name]
        new_position = (
            self.current_position[0] + current_step[0],
            self.current_position[1] + current_step[1],
        )
        if new_position in self.covered_positions:
            current_direction = self.current_direction
            for i in range(6):
                current_direction -= 1
                if current_direction < 0:
                    current_direction = 5
                current_direction_name = self.directions[current_direction]
                current_step = self.steps[current_direction_name]
                new_position = (
                    self.current_position[0] + current_step[0],
                    self.current_position[1] + current_step[1],
                )
                if not(new_position in self.covered_positions):
                    break
            self.add_position(new_position)
            return self.get_position()
        else:
            self.current_direction += 1
            if self.current_direction > 5:
                self.current_direction = 0
            self.add_position(new_position)
            return self.get_position()