from typing import List

from core.model import Car, Intersection, Gateway
from simulation import SimmStats


class City:
	cars: List[Car] = []

	intersections: List[Intersection]
	gateways: List[Gateway]

	stats: SimmStats = SimmStats()

	def __init__(self, intersections: List[Intersection], gateways: List[Gateway]):
		self.intersections = intersections
		self.gateways = gateways

	def step(self):
		for intersection in self.intersections:
			intersection.step()

		for gateway in self.gateways:
			gateway.step()

	# For debugging purposes
	def fill_stats(self):
		analysed_roads = []
		total = 0
		min_spd = 9999
		max_spd = 0
		total_spd = 0

		for intersection in self.intersections:
			for road in intersection.roads:
				if road in analysed_roads:
					continue
				in_road = 0
				for lane in road.left_lanes:
					in_road += len(lane.cars.keys())
					for car in lane.cars.values():
						if car.velocity > max_spd:
							max_spd = car.velocity
						if car.velocity < min_spd:
							min_spd = car.velocity
						total_spd += car.velocity
				for lane in road.right_lanes:
					in_road += len(lane.cars.keys())
					for car in lane.cars.values():
						if car.velocity > max_spd:
							max_spd = car.velocity
						if car.velocity < min_spd:
							min_spd = car.velocity
						total_spd += car.velocity
				total += in_road
				self.stats.register_cars_per_road(road, in_road)
				analysed_roads.append(road)

		avg_spd = total_spd / total
		self.stats.register_speed(min_spd, max_spd, avg_spd)

		in_gateways = 0
		for gateway in self.gateways:
			in_gateway = len(gateway.car_queue)
			in_gateways += in_gateway
			self.stats.register_cars_per_gateway(gateway, in_gateway)
		total += in_gateways
		self.stats.register_total_cars_in_city(total)
