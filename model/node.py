from .vec2d import Vec2d
from .element import Element


class Node(Element):
    pos: Vec2d

    def __init__(self, pos: Vec2d):
        self.pos = pos
