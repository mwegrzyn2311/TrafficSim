import math


class Vec2d:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


def vec2d_dist(a: Vec2d, b: Vec2d):
    return math.ceil(math.pow(a.x - b.x, 2) + math.pow(a.y - b.y, 2))
