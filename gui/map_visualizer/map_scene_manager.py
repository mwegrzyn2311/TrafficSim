from typing import List, Dict

from PySide6.QtWidgets import QGraphicsScene

from core.model import City, Gateway, Road, Intersection, Car
from gui.map_visualizer.item.gateway_item import GatewayItem
from gui.map_visualizer.item.road_item import RoadItem
from gui.map_visualizer.item.intersection_item import IntersectionItem


class MapSceneManager:
	scene: QGraphicsScene
	_gateways: List[GatewayItem]
	_roads: List[RoadItem]
	_intersections: List[IntersectionItem]

	def __init__(self, city: City):
		self.scene = QGraphicsScene()

		self.create_city(city)

	def create_city(self, city: City):
		self._gateways = []
		roads = set()
		for gateway in city.gateways:
			self.create_gateway(gateway)
			if hasattr(gateway, 'road'):
				roads.add(gateway.road)

		self._intersections = []
		for intersection in city.intersections:
			self.create_intersection(intersection)
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

	def create_intersection(self, intersection: Intersection):
		intersection_item = IntersectionItem(intersection)
		self._intersections.append(intersection_item)
		self.scene.addItem(intersection_item.item)

	def update(self):
		for road in self._roads:
			self.scene.removeItem(road.car_group)
			road.update()
			self.scene.addItem(road.car_group)
