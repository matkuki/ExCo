"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import re
import math
import typing
from typing import Any, Iterator

import qt
import data
import functions
from .gridgenerator import *


class HexBuilder:
    first_position: tuple[float, float]
    painter: qt.QPainter
    edge_length: float
    scale: float

    fill_color: qt.QColor
    line_width: int | float
    line_color: qt.QColor

    steps: dict[str, tuple[float, float]]
    horizontal_step: float
    vertical_step: float
    grid_positions: list[tuple[float, float]]

    painted_hex_counter: int = 0
    SHOW_FIELD_NUMBERS: bool = False

    # List of already painted lines
    stored_lines: list[tuple[tuple[int, int], tuple[int, int]]] = []

    @staticmethod
    def generate_hexagon_points(
        edge_length: float, offset_position: tuple[float, float]
    ) -> Iterator[tuple[float, float]]:
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

    def __init__(
        self,
        painter: qt.QPainter,
        first_position: tuple[float, float],
        edge_length: float,
        scale: float = 1.0,
        fill_color: qt.QColor = qt.QColor(255, 255, 255),
        line_width: int = 1,
        line_color: qt.QColor = qt.QColor(255, 255, 255),
    ) -> None:
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
    def get_single_hex_size(edge_length: float, line_width: int) -> tuple[float, float]:
        width = None
        height = None
        width = 2 * edge_length
        width += 2 * line_width
        height = math.sqrt(3) * edge_length
        height += 2 * line_width
        return (width, height)

    def set_first_position(self, first_position: tuple[float, float]) -> None:
        self.first_position = first_position
        self.grid_positions = [first_position]

    def create_grid(self, *array_grid: Any) -> None:
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
                raise Exception(
                    "create_grid item has to be an int (0 >= i < 6) or a tuple(int, bool)!"
                )
        # Paint the edges as needed
        number_of_steps = len(GridGenerator.directions)
        steps = [
            self.steps[GridGenerator.directions[x]] for x in range(number_of_steps)
        ]
        positions = [(int(x[0]), int(x[1])) for x in self.grid_positions]
        for j, gp in enumerate(self.grid_positions):
            paint_edge = [True, True, True, True, True, True]
            if paint_all_edges[j] != True:
                for i, s in enumerate(steps):
                    test_step = (int(gp[0] + s[0]), int(gp[1] + s[1]))
                    comparisons = [
                        (abs(x[0] - test_step[0]) < 5 and abs(x[1] - test_step[1]) < 5)
                        for x in positions
                    ]
                    if any(comparisons):
                        paint_edge[i] = False
            self.draw_line_hexagon(
                position=gp,
                line_width=self.line_width,
                line_color=self.line_color,
                paint_enabled=paint_edge,
                shadow=True,
            )

    def next_step_draw(self, direction: int) -> None:
        self.next_step_move(direction)
        self.draw()

    def next_step_move(self, direction: int) -> tuple[float, float]:
        next_step = self.steps[GridGenerator.directions[direction]]
        last_position = self.grid_positions[-1]
        self.grid_positions.append(
            (last_position[0] + next_step[0], last_position[1] + next_step[1])
        )
        return self.grid_positions[-1]

    def draw(self) -> None:
        self.draw_filled_hexagon(
            position=self.grid_positions[-1],
            fill_color=self.fill_color,
            number=self.painted_hex_counter,
        )
        self.painted_hex_counter += 1

    def draw_line_hexagon_no_double_paint(
        self,
        position: tuple[float, float],
        line_width: int | float,
        line_color: qt.QColor,
        paint_enabled: list[bool] = [True, True, True, True, True, True],
        shadow: bool = False,
    ) -> None:
        qpainter = self.painter

        if line_width == 0:
            return

        pen = qt.QPen(qt.Qt.PenStyle.SolidLine)
        pen.setCapStyle(qt.Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(qt.Qt.PenJoinStyle.RoundJoin)
        pen.setWidth(int(line_width))
        pen.setColor(line_color)
        qpainter.setPen(pen)
        x_correction = self.edge_length / 2
        y_correction = self.edge_length / (2 * math.tan(math.radians(30)))
        hex_points = [
            (int(x - x_correction), int(y - y_correction))
            for x, y in HexBuilder.generate_hexagon_points(self.edge_length, position)
        ]
        hex_lines: list[qt.QLine] = []

        def line_test(in_line: tuple[tuple[int, int], tuple[int, int]]) -> bool:
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
                if (
                    abs(xl1 - x1) < DIFF
                    and abs(yl1 - y1) < DIFF
                    and abs(xl2 - x2) < DIFF
                    and abs(yl2 - y2) < DIFF
                ):
                    if not (line in self.stored_lines):
                        self.stored_lines.append(line)
                        # self.stored_lines.append(reversed_line)
                    return False
                elif (
                    abs(xl1 - xr1) < DIFF
                    and abs(yl1 - yr1) < DIFF
                    and abs(xl2 - xr2) < DIFF
                    and abs(yl2 - yr2) < DIFF
                ):
                    if not (reversed_line in self.stored_lines):
                        self.stored_lines.append(line)
                        # self.stored_lines.append(reversed_line)
                    return False
            else:
                self.stored_lines.append(line)
                self.stored_lines.append(reversed_line)
                return True

        for i in range(len(hex_points)):
            if paint_enabled[i] == False:
                continue
            n = i + 1
            if n > (len(hex_points) - 1):
                n = 0
            if line_test((hex_points[i], hex_points[n])) == True:
                hex_lines.append(
                    qt.QLine(
                        functions.create_point(*hex_points[i]),
                        functions.create_point(*hex_points[n]),
                    )
                )
        if hex_lines:
            if shadow == True:
                shadow_0_color = qt.QColor(line_color)
                shadow_0_color.setAlpha(64)
                shadow_1_color = qt.QColor(line_color)
                shadow_1_color.setAlpha(128)

                pen.setWidth(int(line_width * 2.0))
                pen.setColor(shadow_0_color)
                qpainter.setPen(pen)
                qpainter.drawLines(*hex_lines)
                pen.setWidth(int(line_width * 1.5))
                pen.setColor(shadow_1_color)
                qpainter.setPen(pen)
                qpainter.drawLines(*hex_lines)
                pen.setWidth(int(line_width))
                pen.setColor(line_color)
                qpainter.setPen(pen)
                qpainter.drawLines(*hex_lines)
            else:
                qpainter.drawLines(*hex_lines)

    def draw_line_hexagon(
        self,
        position: tuple[float, float],
        line_width: int | float,
        line_color: qt.QColor,
        paint_enabled: list[bool] = [True, True, True, True, True, True],
        shadow: bool = False,
    ) -> None:
        qpainter = self.painter

        if line_width == 0:
            return

        pen = qt.QPen(qt.Qt.PenStyle.SolidLine)
        pen.setCapStyle(qt.Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(qt.Qt.PenJoinStyle.RoundJoin)
        pen.setWidth(int(line_width))
        pen.setColor(line_color)
        qpainter.setPen(pen)
        x_correction = self.edge_length / 2
        y_correction = self.edge_length / (2 * math.tan(math.radians(30)))
        hex_points = [
            (int(x - x_correction), int(y - y_correction))
            for x, y in HexBuilder.generate_hexagon_points(self.edge_length, position)
        ]
        hex_lines: list[qt.QLine] = []

        for i in range(len(hex_points)):
            if paint_enabled[i] == False:
                continue
            n = i + 1
            if n > (len(hex_points) - 1):
                n = 0
            hex_lines.append(
                qt.QLine(
                    functions.create_point(*hex_points[i]),
                    functions.create_point(*hex_points[n]),
                )
            )
        if hex_lines:
            if shadow == True:
                shadow_0_color = qt.QColor(line_color)
                shadow_0_color.setAlpha(64)
                shadow_1_color = qt.QColor(line_color)
                shadow_1_color.setAlpha(128)

                pen.setWidth(int(line_width * 2.0))
                pen.setColor(shadow_0_color)
                qpainter.setPen(pen)
                qpainter.drawLines(*hex_lines)
                pen.setWidth(int(line_width * 1.5))
                pen.setColor(shadow_1_color)
                qpainter.setPen(pen)
                qpainter.drawLines(*hex_lines)
                pen.setWidth(int(line_width))
                pen.setColor(line_color)
                qpainter.setPen(pen)
                qpainter.drawLines(*hex_lines)
            else:
                qpainter.drawLines(*hex_lines)

    def draw_filled_hexagon(
        self,
        position: tuple[float, float],
        fill_color: qt.QColor,
        number: int | None = None,
    ) -> None:
        qpainter = self.painter

        pen = qt.QPen(qt.Qt.PenStyle.SolidLine)
        pen.setColor(fill_color)
        brush = qt.QBrush(qt.Qt.BrushStyle.SolidPattern)
        brush.setColor(fill_color)
        qpainter.setBrush(brush)
        qpainter.setPen(pen)
        x_correction = self.edge_length / 2
        y_correction = self.edge_length / (2 * math.tan(math.radians(30)))
        hex_points = [
            (int(x - x_correction), int(y - y_correction))
            for x, y in HexBuilder.generate_hexagon_points(self.edge_length, position)
        ]
        hex_qpoints = [functions.create_point(*x) for x in hex_points]
        qpainter.drawPolygon(*hex_qpoints)

        if (self.SHOW_FIELD_NUMBERS == True) and (number != None):
            font = qt.QFont("Courier", 8)
            font.setBold(True)
            qpainter.setFont(font)
            pen = qt.QPen(qt.Qt.PenStyle.SolidLine)
            pen.setColor(qt.QColor(0, 0, 0))
            qpainter.setPen(pen)

            font_metric = qt.QFontMetrics(font)
            x = int(position[0] - font_metric.horizontalAdvance(str(number)) / 2)
            y = int(position[1] + font_metric.height() / 4)
            qpainter.drawText(functions.create_point(x, y), str(number))

    def draw_full_hexagon(
        self,
        position: tuple[float, float],
        fill_color: qt.QColor,
        line_width: int | float,
        line_color: qt.QColor,
    ) -> None:
        qpainter = self.painter

        pen = qt.QPen(qt.Qt.PenStyle.SolidLine)
        pen.setColor(line_color)
        pen.setCapStyle(qt.Qt.PenCapStyle.RoundCap)
        pen.setWidth(int(line_width))
        brush = qt.QBrush(qt.Qt.BrushStyle.SolidPattern)
        brush.setColor(fill_color)
        qpainter.setBrush(brush)
        qpainter.setPen(pen)
        x_correction = self.edge_length / 2
        y_correction = self.edge_length / (2 * math.tan(math.radians(30)))
        hex_points = [
            (int(x - x_correction), int(y - y_correction))
            for x, y in HexBuilder.generate_hexagon_points(self.edge_length, position)
        ]
        hex_qpoints = [functions.create_point(*x) for x in hex_points]
        qpainter.drawPolygon(*hex_qpoints)

    def draw_full_hexagon_with_shadow(
        self,
        position: tuple[float, float],
        fill_color: qt.QColor,
        line_width: int | float,
        line_color: qt.QColor,
    ) -> None:
        qpainter = self.painter

        self.draw_filled_hexagon(position, fill_color)
        shadow_0_color = qt.QColor(line_color)
        shadow_0_color.setAlpha(64)
        shadow_1_color = qt.QColor(line_color)
        shadow_1_color.setAlpha(128)
        self.draw_line_hexagon(position, line_width * 2.0, shadow_0_color)
        self.draw_line_hexagon(position, line_width * 1.5, shadow_1_color)
        self.draw_line_hexagon(position, line_width, line_color)

    def get_last_position(self) -> tuple[float, float]:
        return self.grid_positions[-1]

    def generate_square_grid_list(
        self, row_length: int, count: int
    ) -> list[tuple[int, bool]]:
        row_counter = 1
        grid_list: list[tuple[int, bool]] = []
        direction = False
        add_down_step = False
        for i in range(count - 1):
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
