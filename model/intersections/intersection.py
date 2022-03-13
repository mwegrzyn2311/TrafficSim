from typing import List
from model import Node, Vec2d


class Intersection(Node):
    nodes_in: List[Node]
    nodes_out: List[Node]

    def __init__(self, pos: Vec2d, nodes_in: List[Node] = None, nodes_out: List[Node] = None):
        super().__init__(pos)

        if nodes_in is None:
            self.nodes_in = list()
        else:
            self.nodes_in = nodes_in

        if nodes_out is None:
            self.nodes_out = list()
        else:
            self.nodes_out = nodes_out
