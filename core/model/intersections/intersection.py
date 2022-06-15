from typing import List
from core.model import Node, Road, Vec2d


class Intersection(Node):
    roads: List[Road]

    def __init__(self, pos: Vec2d, radius: int = 1):
        super().__init__(pos, radius)
        self.roads = []

    def add_road(self, road: Road):
        assert(road not in self.roads)

        self.roads.append(road)

    def get_roads(self) -> List["Road"]:
        return self.roads

    def step(self):
        pass
