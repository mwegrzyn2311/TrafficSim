from abc import ABC, abstractmethod
from typing import List

from core.model import Gateway, City, Node, Car


class AbstractDriver(ABC):
	src_gateway: Gateway
	dest_gateway: Gateway

	city: City

	planned_route: List[Node]

	car: Car

	def __init__(self, city: City, src: Gateway, dest: Gateway, car: Car) -> None:
		self.src_gateway = src
		self.dest_gateway = dest

		self.city = city
		self.car = car

	@abstractmethod
	def step(self):
		pass
