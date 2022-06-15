from __future__ import annotations
import math


class Vec2d:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def length(self) -> float:
        return math.hypot(self.x, self.y)

    def __equals__(self, other: Vec2d) -> bool:
        return self.x == other.x and self.y == other.y

    def __add__(self, other: Vec2d) -> Vec2d:
        return Vec2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vec2d) -> Vec2d:
        return Vec2d(self.x - other.x, self.y - other.y)
