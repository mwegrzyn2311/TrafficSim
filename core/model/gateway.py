from typing import List

from core.model import Node, Road, Vec2d, Car


class Gateway(Node):
	road: Road
	car_queue: List[Car]

	def __init__(self, pos: Vec2d):
		super().__init__(pos)
		self.car_queue = []

	def add_road(self, road: Road):
		self.road = road

	def get_roads(self) -> List["Road"]:
		return [self.road]

	def get_type_str(self) -> str:
		return "gateway"

	def add_car(self, car: Car) -> None:
		self.car_queue.append(car)

	def step(self) -> None:
		# FIXME: Working only for one-lane roads
		if self.road.right_lanes[0].get_cell(0) is not None:
			return
		if len(self.car_queue) > 0:
			to_push = self.car_queue.pop(0)
			for lane in self.road.right_lanes:
				if not lane.get_cell(0):
					lane.add_car(0, to_push)
					break
