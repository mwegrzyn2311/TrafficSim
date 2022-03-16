from typing import List

from core.model import Car, Intersection, Gateway


class City:
	cars: List[Car] = []

	intersections: List[Intersection]
	gateways: List[Gateway]

	def __init__(self, intersections: List[Intersection], gateways: List[Gateway]):
		self.intersections = intersections
		self.gateways = gateways
