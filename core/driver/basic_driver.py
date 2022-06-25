import random
from typing import List

from core.driver.abstract_driver import AbstractDriver
from core.model import Gateway, City, Car, Element, Lane, Node
from core.routing import calculate_dijkstra_route


class BasicDriver(AbstractDriver):
	breaking_chance: float = 0.1
	planned_route: List[Node]

	def __init__(self, city: City, src: Gateway, dest: Gateway, car: Car, simulation_controller):
		super(BasicDriver, self).__init__(city, src, dest, car, simulation_controller)

		self._init_itinerary()

	def _init_itinerary(self):
		self.car.planned_route = calculate_dijkstra_route(self.src_gateway,  self.dest_gateway, self.city.intersections + self.city.gateways)
		# We skip first element as it's the closest one and we know how to get there while this is needed to navigate to the next one
		self.car.next_planned_node_idx = 1
		if self.car.next_planned_node_idx < len(self.car.planned_route):
			self.car.next_planned_node = self.car.planned_route[self.car.next_planned_node_idx]

	def acceleration(self):
		self.car.velocity += self.car.acceleration

	def breaking(self):
		assert(isinstance(self.car.current_element, Lane))

		lane: Lane = self.car.current_element
		position = lane.get_car_cell(self.car)
		next_car = lane.get_car_in_front(self.car)
		if next_car is None:
			# No need for breaking
			return
		next_car_position = lane.get_car_cell(next_car)
		assert (next_car_position > position)
		self.car.velocity = min(self.car.velocity, next_car_position - position - 1)

	def randomization(self):
		breaking = random.random()
		if breaking < self.breaking_chance:
			self.car.velocity = max(0, self.car.velocity - 1)

	def movement(self):
		assert(isinstance(self.car.current_element, Lane))

		self.car.velocity = min(self.car.velocity, self.car.max_velocity)
		lane: Lane = self.car.current_element
		lane.move_car(lane.get_car_cell(self.car), self.car.velocity)

	def step(self):
		current_element: Element = self.car.current_element
		if isinstance(current_element, Lane):
			self.acceleration()
			self.breaking()
			self.randomization()
			self.movement()

