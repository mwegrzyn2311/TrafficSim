from typing import List

from core.model import Car, Intersection
from core.model.gateway import Gateway


class City:
	cars: List[Car]

	intersections: List[Intersection]
	gateways: List[Gateway]
