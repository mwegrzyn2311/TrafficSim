from PySide6.QtGui import QColorConstants
from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsItem

from core.model import Gateway
from gui.map_visualizer.item.common import CELL_SIZE, GraphicItem

GATEWAY_DIAMETER = 10


class GatewayItem(GraphicItem):
	item: QGraphicsItem
	gateway: Gateway

	def __init__(self, gateway: Gateway):
		self.gateway = gateway
		self._build_item()

	def _build_item(self):
		radius = self.gateway.radius
		x = self.gateway.pos.x - radius
		y = self.gateway.pos.y - radius

		self.item = QGraphicsEllipseItem(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE * radius * 2, CELL_SIZE * radius * 2)
		self.item.setBrush(QColorConstants.Blue)
		# self.item.setZValue(10)


