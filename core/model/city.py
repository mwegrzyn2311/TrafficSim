from typing import List

from core.model import Car, Intersection, Gateway


class City:
	cars: List[Car] = []

	intersections: List[Intersection]
	gateways: List[Gateway]

	def __init__(self, intersections: List[Intersection], gateways: List[Gateway]):
		self.intersections = intersections
		self.gateways = gateways

	def step(self):
		for intersection in self.intersections:
			intersection.step()

		for gateway in self.gateways:
			gateway.step()

	# For debugging purposes
	def print_num_of_cars(self):
		analysed_roads = []
		total = 0
		for intersection in self.intersections:
			for road in intersection.roads:
				if road in analysed_roads:
					continue
				in_road = 0
				for lane in road.left_lanes:
					in_road += len(lane.cars.keys())
				for lane in road.right_lanes:
					in_road += len(lane.cars.keys())
				total += in_road
				print(f"{in_road} in road from ({road.left_node.pos.x},{road.left_node.pos.y}) to ({road.right_node.pos.x},{road.right_node.pos.y})")
				analysed_roads.append(road)
		in_gateways = 0
		for gateway in self.gateways:
			in_gateways += len(gateway.car_queue)
		print(f"{in_gateways} in all gateway queues")
		total += in_gateways
		print(f"TOTAL: {total} cars in the city")
