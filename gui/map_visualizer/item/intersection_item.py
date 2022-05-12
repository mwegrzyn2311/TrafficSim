from PySide6.QtGui import QColorConstants
from PySide6.QtCore import QLineF
from PySide6.QtWidgets import QGraphicsItem, QGraphicsItemGroup, QGraphicsRectItem

from core.model import Intersection

from gui.map_visualizer.item.common import CELL_SIZE

GATEWAY_DIAMETER = 10


class IntersectionItem:
    item: QGraphicsItem
    intersection: Intersection

    def __init__(self, intersection: Intersection):
        self.intersection = intersection
        self._build_item()

    def _build_item(self):

        mid = self.intersection.pos
        radius = self.intersection.radius

        group = QGraphicsItemGroup()

        # Firstly build 2x2 in the middle
        for x in range(-1, 1):
            for y in range(-1, 1):
                mid_cell = QGraphicsRectItem((mid.x + x) * CELL_SIZE, (mid.y + y) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                mid_cell.setBrush(QColorConstants.Green)
                group.addToGroup(mid_cell)

        # Then build from +1 do begin of road (for in range(1, width): create square)
        for road in self.intersection.roads:
            if mid.__equals__(road.left_node.pos):
                end = road.right_node.pos
            else:
                end = road.left_node.pos
            dir: QLineF = QLineF(mid.x, mid.y, end.x, end.y).unitVector()
            for i in range(1, radius):
                # TODO: create roads from middle to end but let's consider only width == 1 for the time being
                pass

        self.item = group
