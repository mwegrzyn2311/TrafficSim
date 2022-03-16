from typing import List
from core.model import Node, Road, Vec2d


class Intersection(Node):
    roads: List[Road] = []

    def __init__(self, pos: Vec2d):
        super().__init__(pos)

    def add_road(self, road: Road):
        assert(road not in self.roads)

        self.roads.append(road)
