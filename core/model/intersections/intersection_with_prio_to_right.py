from .intersection import Intersection
from core.model import Vec2d


class IntersectionWithPrioToRight(Intersection):
    def __init__(self, pos: Vec2d):
        super().__init__(pos)
