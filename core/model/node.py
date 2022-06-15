from abc import abstractmethod
from typing import TYPE_CHECKING, List

from .vec2d import Vec2d
from .element import Element

if TYPE_CHECKING:
    from . import Road


class Node(Element):
    pos: Vec2d
    radius: int

    def __init__(self, pos: Vec2d, radius: int = 1):
        self.pos = pos
        self.radius = radius

    @abstractmethod
    def add_road(self, road: "Road"):
        pass

    @abstractmethod
    def get_roads(self) -> List["Road"]:
        pass
