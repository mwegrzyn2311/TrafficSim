import math
from typing import List

from core.model import Lane
from .element import Element
from .node import Node


class Road(Element):
	right_lanes: List[Lane]
	left_lanes: List[Lane]

	left_node: Node
	right_node: Node

	def __init__(self, right_node: Node, left_node: Node, right_lanes_count: int, left_lanes_count: int):
		self.right_node = right_node
		self.left_node = left_node
		num_of_cells = math.floor((right_node.pos + left_node.pos).length()) - right_node.radius - left_node.radius

		self.right_lanes = [Lane(num_of_cells=num_of_cells) for i in range(right_lanes_count)]
		self.left_lanes = [Lane(num_of_cells=num_of_cells) for i in range(left_lanes_count)]

