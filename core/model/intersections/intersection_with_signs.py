from .intersection import Intersection
from core.model import Vec2d, Road
from typing import Tuple


class IntersectionWithSigns(Intersection):
    prio_roads: Tuple[Road, Road]

    def __init__(self, pos: Vec2d):
        super().__init__(pos)
