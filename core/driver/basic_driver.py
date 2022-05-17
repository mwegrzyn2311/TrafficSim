import random
from typing import List

from core.driver.abstract_driver import AbstractDriver
from core.model import Gateway, City, Car, Element, Lane, Node
from core.routing import calculate_dijkstra_route


class BasicDriver(AbstractDriver):
	breaking_chance: float = 0.1

	def __init__(self, city: City, src: Gateway, dest: Gateway, car: Car):
		super(BasicDriver, self).__init__(city, src, dest, car)

		self._init_itinerary()

	def _init_itinerary(self):
		nodes: List[Node] = self.city.intersections
		nodes += self.city.gateways
		self.planned_route = calculate_dijkstra_route(self.src_gateway,  self.dest_gateway, nodes)

	def acceleration(self):
		self.car.velocity += self.car.acceleration

	def breaking(self):
		assert(isinstance(self.car.current_element, Lane))

		lane: Lane = self.car.current_element
		position = lane.get_car_cell(self.car)
		next_car_position = lane.get_car_cell(self.car)
		self.car.velocity = max(self.car.velocity, position - next_car_position)

	def randomization(self):
		breaking = random.random()
		if breaking < self.breaking_chance:
			self.car.velocity -= 1

	def movement(self):
		assert(isinstance(self.car.current_element, Lane))

		self.car.velocity = max(self.car.velocity, self.car.max_velocity)
		lane: Lane = self.car.current_element
		lane.move_car(lane.get_car_cell(self.car), self.car.velocity)

	def step(self):
		current_element: Element = self.car.current_element
		print(current_element)
		if isinstance(current_element, Lane):
			self.acceleration()
			self.breaking()
			self.randomization()
			self.movement()

