from PySide6.QtGui import QColorConstants
from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsItem

from core.model import Gateway

GATEWAY_DIAMETER = 10


class GatewayItem:
	item: QGraphicsItem
	gateway: Gateway

	def __init__(self, gateway: Gateway):
		self.gateway = gateway
		self._build_item()

	def _build_item(self):
		x = self.gateway.pos.x - GATEWAY_DIAMETER / 2
		y = self.gateway.pos.y - GATEWAY_DIAMETER / 2

		self.item = QGraphicsEllipseItem(x, y, GATEWAY_DIAMETER, GATEWAY_DIAMETER)
		self.item.setBrush(QColorConstants.Blue)
		# self.item.setZValue(10)


