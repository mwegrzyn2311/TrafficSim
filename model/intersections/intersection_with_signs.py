from .intersection import Intersection
from model import Vec2d, Node
from typing import List


class IntersectionWithSigns(Intersection):
    def __init__(self, pos: Vec2d, nodes_in: List[Node], nodes_out: List[Node]):
        super().__init__(pos, nodes_in, nodes_out)
