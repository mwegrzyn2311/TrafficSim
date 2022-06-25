from abc import ABC, abstractmethod
from typing import List

from core.model import Gateway, City, Node, Car


class AbstractDriver(ABC):
	src_gateway: Gateway
	dest_gateway: Gateway

	city: City

	planned_route: List[Node]

	car: Car

	def __init__(self, city: City, src: Gateway, dest: Gateway, car: Car, simulation_controller) -> None:
		self.src_gateway = src
		self.dest_gateway = dest

		self.city = city
		self.car = car
		car.driver = self
		self.simulation_controller = simulation_controller

	@abstractmethod
	def step(self):
		pass

	def unregister(self):
		self.simulation_controller.register_driver_for_removal(self)
