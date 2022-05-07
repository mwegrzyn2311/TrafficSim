from .vec2d import Vec2d
from .element import Element


class Node(Element):
    pos: Vec2d
    radius: int

    def __init__(self, pos: Vec2d, radius: int = 1):
        self.pos = pos
        self.radius = radius

    # TODO: Road type annotation gives me circular dependencies but maybe it is possible...
    def add_road(self, road):
        pass
