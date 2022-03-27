from typing import List

from PySide6.QtWidgets import QGraphicsScene, QGraphicsEllipseItem

from core.model import City, Gateway, Road
from gui.map_visualizer.item.gateway_item import GatewayItem
from gui.map_visualizer.item.road_item import RoadItem


class MapSceneManager:
	scene: QGraphicsScene
	_gateways: List[GatewayItem]
	_roads: List[RoadItem]

	def __init__(self, city: City):
		self.scene = QGraphicsScene()

		self.create_city(city)

	def create_city(self, city: City):
		self._gateways = []
		roads = set()
		for gateway in city.gateways:
			self.create_gateway(gateway)
			roads.add(gateway.road)

		for intersection in city.intersections:
			for road in intersection.roads:
				roads.add(road)

		self._roads = []
		for road in roads:
			self.create_road(road)
			pass

	def create_gateway(self, gateway: Gateway):
		gateway_item = GatewayItem(gateway)
		self._gateways.append(gateway_item)
		self.scene.addItem(gateway_item.item)

	def create_road(self, road: Road):
		road_item = RoadItem(road)
		self._roads.append(road_item)
		self.scene.addItem(road_item.item)
