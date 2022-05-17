import math
from typing import Dict, List

from PySide6.QtCore import QLineF, QPointF
from PySide6.QtGui import QColorConstants, QColor
from PySide6.QtWidgets import QGraphicsItem, QGraphicsItemGroup, QGraphicsLineItem, QGraphicsRectItem

from core.model import Road, Lane, Car
from gui.map_visualizer.item.common import CELL_SIZE, GraphicItem

LANE_WIDTH = 2
LANE_GAP = 1

LEFT_LANE_COLOR = QColorConstants.Cyan
RIGHT_LANE_COLOR = QColorConstants.Red


class RoadItem(GraphicItem):
    item: QGraphicsItemGroup = QGraphicsItemGroup()
    car_items: QGraphicsRectItem
    road: Road

    _car_group: QGraphicsItemGroup = QGraphicsItemGroup()

    def __init__(self, road: Road):
        self.road = road
        self._build_item()

    def _create_lane_cell(self, start_point: QPointF, dir_unit_vec: QLineF,
                          cell: int, normal_diff: QPointF, lane_no: int, color: QColor):
        cell_offset: QPointF = QPointF(dir_unit_vec.dx() * cell, dir_unit_vec.dy() * cell)
        start: QPointF = start_point + cell_offset + normal_diff * (lane_no - 0.5)

        cell = QGraphicsRectItem((start.x() - 0.5) * CELL_SIZE, (start.y() - 0.5) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        center: QPointF = cell.boundingRect().center()

        if math.floor(dir_unit_vec.angle()) % 90 != 0:
            cell.setTransformOriginPoint(center.x(), center.y())
            cell.setRotation(dir_unit_vec.angle() - 45)

        cell.setBrush(color)
        return cell

    def _create_lane(self, lane: Lane, lane_no: int,
                     start_point: QPointF, end_point: QPointF, start_node_radius: int,
                     color: QColorConstants = QColorConstants.Black):
        line_vector = QLineF(start_point, end_point)

        dir_unit_vec: QLineF = line_vector.unitVector()

        start_node_offset: QPointF = QPointF(dir_unit_vec.dx() * (start_node_radius + 0.5),
                                             dir_unit_vec.dy() * (start_node_radius + 0.5))
        start_point += start_node_offset

        normal: QLineF = line_vector.normalVector().unitVector()
        normal_diff = QPointF(normal.dx(), normal.dy())

        lane_group = QGraphicsItemGroup()

        for cell in range(lane.num_of_cells):
            lane_group.addToGroup(self._create_lane_cell(start_point, dir_unit_vec, cell, normal_diff, lane_no, color))

        return lane_group

    def _build_item(self):
        start_node = self.road.right_node
        end_node = self.road.left_node

        start_node_x = start_node.pos.x
        start_node_y = start_node.pos.y

        end_node_x = end_node.pos.x
        end_node_y = end_node.pos.y

        static_group = QGraphicsItemGroup()

        for lane_no, lane in enumerate(self.road.left_lanes):
            start = QPointF(start_node_x, start_node_y)
            end = QPointF(end_node_x, end_node_y)
            static_group.addToGroup(self._create_lane(lane, lane_no, start, end, start_node.radius, LEFT_LANE_COLOR))

        for lane_no, lane in enumerate(self.road.right_lanes):
            start = QPointF(end_node_x, end_node_y)
            end = QPointF(start_node_x, start_node_y)
            static_group.addToGroup(self._create_lane(lane, lane_no, start, end, start_node.radius, RIGHT_LANE_COLOR))

        self.item.addToGroup(static_group)

    def _create_car(self, lane_no, cell_no, start_point, end_point, radius, car_color):
        line_vector = QLineF(start_point, end_point)

        dir_unit_vec: QLineF = line_vector.unitVector()

        start_node_offset: QPointF = QPointF(dir_unit_vec.dx() * (radius + 0.5),
                                             dir_unit_vec.dy() * (radius + 0.5))
        start_point += start_node_offset
        cell_offset: QPointF = QPointF(dir_unit_vec.dx() * cell_no, dir_unit_vec.dy() * cell_no)

        normal: QLineF = line_vector.normalVector().unitVector()
        normal_diff = QPointF(normal.dx(), normal.dy())
        start: QPointF = start_point + cell_offset + normal_diff * (lane_no - 0.5)

        car_item = QGraphicsItemGroup()
        car_bot_x: int = start.x() - 0.4 * dir_unit_vec.dx() - 0.2 * dir_unit_vec.normalVector().dx()
        car_bot_y: int = start.y() - 0.4 * dir_unit_vec.dy() - 0.2 * dir_unit_vec.normalVector().dy()
        car_bottom = QGraphicsRectItem(car_bot_x, car_bot_y, 0.4 * CELL_SIZE, 0.8 * CELL_SIZE)
        car_bottom.setBrush(QColor(car_color[0], car_color[1], car_color[2]))
        car_item.addToGroup(car_bottom)

        car_wind_x: int = start.x() - 0.3 * dir_unit_vec.dx() - 0.1 * dir_unit_vec.normalVector().dx()
        car_wind_y: int = start.y() - 0.3 * dir_unit_vec.dy() - 0.1 * dir_unit_vec.normalVector().dy()
        car_windows = QGraphicsRectItem(car_wind_x, car_wind_y, 0.2 * CELL_SIZE, 0.5 * CELL_SIZE)
        car_windows.setBrush(QColorConstants.DarkCyan)
        car_item.addToGroup(car_windows)

        car_top_x: int = start.x() - 0.2 * dir_unit_vec.dx() - 0.1 * dir_unit_vec.normalVector().dx()
        car_top_y: int = start.y() - 0.2 * dir_unit_vec.dy() - 0.1 * dir_unit_vec.normalVector().dy()
        car_top = QGraphicsRectItem(car_top_x, car_top_y, 0.2 * CELL_SIZE, 0.3 * CELL_SIZE)
        car_item.addToGroup(car_top)

        return car_item

    def update(self):
        self.item.removeFromGroup(self._car_group)
        self._car_group = QGraphicsItemGroup()

        start_node = self.road.right_node
        end_node = self.road.left_node

        start_node_x = start_node.pos.x
        start_node_y = start_node.pos.y

        end_node_x = end_node.pos.x
        end_node_y = end_node.pos.y

        for lane_no, lane in enumerate(self.road.left_lanes):
            start = QPointF(start_node_x, start_node_y)
            end = QPointF(end_node_x, end_node_y)
            for pos, car in lane.cars.items():
                self._car_group.addToGroup(self._create_car(lane_no, pos, start, end, start_node.radius, car.color))

        for lane_no, lane in enumerate(self.road.right_lanes):
            start = QPointF(end_node_x, end_node_y)
            end = QPointF(start_node_x, start_node_y)
            for pos, car in lane.cars.items():
                self._car_group.addToGroup(self._create_car(lane_no, pos, start, end, start_node.radius, car.color))

        self.item.addToGroup(self._car_group)