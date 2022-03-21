from __future__ import annotations

from typing import Tuple
import random

from .element import Element
from .lane import Lane


class Car:
    current_ele: Element

    velocity: int
    acceleration: int
    # Cars may differ and have their own limitations
    max_velocity: int

    color: Tuple[int, int, int]

    def __init__(self, current_ele: Element, max_velocity: int = 10):
        self.current_ele = current_ele
        self.max_velocity = max_velocity

        self.velocity = 0
        self.acceleration = 1

        self.color = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))

    def get_cell_no(self) -> int or None:
        if isinstance(self.current_ele, Lane):
            lane: Lane = self.current_ele
            return lane.get_car_cell(self)
        return None

    def get_car_in_front(self) -> Car or None:
        if isinstance(self.current_ele, Lane):
            lane: Lane = self.current_ele
            return lane.get_car_in_front(self)
        return None

    def set_velocity(self, velocity):
        self.velocity = max(velocity, self.max_velocity)

    # TODO: Handle not only lanes but also intersections, etc.
    def move(self):
        if isinstance(self.current_ele, Lane):
            lane: Lane = self.current_ele
            curr_pos = self.get_cell_no()
            lane.move_car(curr_pos, self.velocity)
