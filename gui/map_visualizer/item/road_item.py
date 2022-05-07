from PySide6.QtCore import QLineF, QPointF
from PySide6.QtGui import QColorConstants
from PySide6.QtWidgets import QGraphicsItem, QGraphicsItemGroup, QGraphicsLineItem, QGraphicsRectItem

from core.model import Road, Lane
from gui.map_visualizer.item.common import CELL_SIZE

LANE_WIDTH = 2
LANE_GAP = 1


def new_cell_to_group(group: QGraphicsItemGroup, start_point: QPointF, dir_unit_vec: QLineF, cell: int, normal_diff: QPointF, lane_no: int, color: QColorConstants):
    cell_offset: QPointF = QPointF(dir_unit_vec.dx() * cell, dir_unit_vec.dy() * cell)
    start: QPointF = start_point + cell_offset + normal_diff * (lane_no - 0.5)
    # start is middle of cell, so we need to get to the corner before multiplying
    cell = QGraphicsRectItem((start.x() - 0.5) * CELL_SIZE, (start.y() - 0.5) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    cell.setBrush(color)
    group.addToGroup(cell)


def create_lane(group: QGraphicsItemGroup, lane: Lane, lane_no: int, start_point: QPointF, end_point: QPointF, start_node_radius: int,
                color: QColorConstants = QColorConstants.Black):
    line_vector = QLineF(start_point, end_point)

    dir_unit_vec: QLineF = line_vector.unitVector()

    start_node_offset: QPointF = QPointF(dir_unit_vec.dx() * (start_node_radius + 0.5), dir_unit_vec.dy() * (start_node_radius + 0.5))
    start_point += start_node_offset

    normal: QLineF = line_vector.normalVector().unitVector()
    normal_diff = QPointF(normal.dx(), normal.dy())

    for cell in range(lane.num_of_cells):
        new_cell_to_group(group, start_point, dir_unit_vec, cell, normal_diff, lane_no, color)


class RoadItem:
    item: QGraphicsItem
    road: Road

    def __init__(self, road: Road):
        self.road = road
        self._build_item()

    def _build_item(self):
        start_node = self.road.right_node
        end_node = self.road.left_node

        start_node_x = start_node.pos.x
        start_node_y = start_node.pos.y

        end_node_x = end_node.pos.x
        end_node_y = end_node.pos.y

        group = QGraphicsItemGroup()
        for lane_no in range(len(self.road.left_lanes)):
            create_lane(group, self.road.left_lanes[lane_no], lane_no, QPointF(start_node_x, start_node_y), QPointF(end_node_x, end_node_y), start_node.radius,
                        QColorConstants.Cyan)

        for lane_no in range(len(self.road.right_lanes)):
            create_lane(group, self.road.right_lanes[lane_no], lane_no, QPointF(end_node_x, end_node_y), QPointF(start_node_x, start_node_y), start_node.radius,
                        QColorConstants.Red)

        self.item = group
