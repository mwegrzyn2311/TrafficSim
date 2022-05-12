from PySide6.QtCore import QLineF, QPointF
from PySide6.QtGui import QColorConstants, QColor
from PySide6.QtWidgets import QGraphicsItem, QGraphicsItemGroup, QGraphicsLineItem, QGraphicsRectItem

from core.model import Road, Lane
from gui.map_visualizer.item.common import CELL_SIZE

from typing import Tuple

LANE_WIDTH = 2
LANE_GAP = 1


def new_cell_to_group(group: QGraphicsItemGroup, car_group: QGraphicsItemGroup, start_point: QPointF, dir_unit_vec: QLineF, cell: int, normal_diff: QPointF, lane_no: int,
                      color: QColorConstants, car_color: Tuple[int, int, int] = None):
    cell_offset: QPointF = QPointF(dir_unit_vec.dx() * cell, dir_unit_vec.dy() * cell)
    start: QPointF = start_point + cell_offset + normal_diff * (lane_no - 0.5)
    # start is middle of cell, so we need to get to the corner before multiplying
    cell = QGraphicsRectItem((start.x() - 0.5) * CELL_SIZE, (start.y() - 0.5) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    cell.setBrush(color)

    if car_color:
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
        # TODO: Add car rotation?

    group.addToGroup(cell)


def create_lane(group: QGraphicsItemGroup, car_group: QGraphicsItemGroup, lane: Lane, lane_no: int, start_point: QPointF, end_point: QPointF, start_node_radius: int,
                color: QColorConstants = QColorConstants.Black):
    line_vector = QLineF(start_point, end_point)

    dir_unit_vec: QLineF = line_vector.unitVector()

    start_node_offset: QPointF = QPointF(dir_unit_vec.dx() * (start_node_radius + 0.5), dir_unit_vec.dy() * (start_node_radius + 0.5))
    start_point += start_node_offset

    normal: QLineF = line_vector.normalVector().unitVector()
    normal_diff = QPointF(normal.dx(), normal.dy())

    for cell in range(lane.num_of_cells):
        car_color = None
        if cell in lane.cars:
            car_color = lane.cars[cell].color

        new_cell_to_group(group, car_group, start_point, dir_unit_vec, cell, normal_diff, lane_no, color, car_color)


class RoadItem:
    item: QGraphicsItem
    car_items: QGraphicsRectItem
    road: Road

    def __init__(self, road: Road):
        self.road = road
        self._build_item()
        #self.build_car_items()

    def _build_item(self):
        start_node = self.road.right_node
        end_node = self.road.left_node

        start_node_x = start_node.pos.x
        start_node_y = start_node.pos.y

        end_node_x = end_node.pos.x
        end_node_y = end_node.pos.y

        group = QGraphicsItemGroup()
        car_group = QGraphicsItemGroup()
        for lane_no in range(len(self.road.left_lanes)):
            create_lane(group, car_group, self.road.left_lanes[lane_no], lane_no, QPointF(start_node_x, start_node_y), QPointF(end_node_x, end_node_y), start_node.radius,
                        QColorConstants.Cyan)

        for lane_no in range(len(self.road.right_lanes)):
            create_lane(group, car_group, self.road.right_lanes[lane_no], lane_no, QPointF(end_node_x, end_node_y), QPointF(start_node_x, start_node_y),
                        start_node.radius,
                        QColorConstants.Red)

        self.item = group
        self.car_items = car_group

    # def _build_car_in_lane(self, lane: Lane):
    #     for cell_no in lane.cars:
    #         car = lane.cars[cell_no]
    #
    # def new_cell_to_group(group: QGraphicsItemGroup, start_point: QPointF, dir_unit_vec: QLineF, cell: int, normal_diff: QPointF, lane_no: int, color: QColorConstants):
    #     cell_offset: QPointF = QPointF(dir_unit_vec.dx() * cell, dir_unit_vec.dy() * cell)
    #     start: QPointF = start_point + cell_offset + normal_diff * (lane_no - 0.5)
    #     # start is middle of cell, so we need to get to the corner before multiplying
    #     cell = QGraphicsRectItem((start.x() - 0.5) * CELL_SIZE, (start.y() - 0.5) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    #     cell.setBrush(color)
    #     group.addToGroup(cell)
    #
    # def build_car_items(self):
    #     for lane in self.road.left_lanes:
    #         self._build_car_in_lane(lane)
    #     for lane in self.road_right_lanes:
