from PySide6.QtCore import QLineF, QPointF
from PySide6.QtWidgets import QGraphicsItem, QGraphicsItemGroup, QGraphicsLineItem

from core.model import Road

LANE_WIDTH = 2
LANE_GAP = 1


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

		road_start_point = QPointF(start_node_x, start_node_y)
		road_end_point = QPointF(end_node_x, end_node_y)

		line_vector = QLineF(road_start_point, road_end_point)

		normal: QLineF = line_vector.normalVector().unitVector()

		group = QGraphicsItemGroup()

		for num in range(len(self.road.right_lanes)):
			normal.setLength(LANE_GAP * (1 + num) + LANE_WIDTH * num)
			diff = QPointF(normal.dx(), normal.dy())
			start_point = road_start_point - diff
			end_point = road_end_point - diff

			line = QLineF(start_point, end_point)
			line_item = QGraphicsLineItem(line)

			group.addToGroup(line_item)

		for num in range(len(self.road.left_lanes)):
			normal.setLength(LANE_GAP * (1 + num) + LANE_WIDTH * num)
			diff = QPointF(normal.dx(), normal.dy())
			start_point = road_start_point + diff
			end_point = road_end_point + diff

			line = QLineF(start_point, end_point)
			line_item = QGraphicsLineItem(line)

			group.addToGroup(line_item)

		self.item = group
