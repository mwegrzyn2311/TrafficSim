from __future__ import annotations

from random import random
from typing import Tuple
import random

from .element import Element
from .lane import Lane


class Car:
    current_element: Element

    velocity: int
    acceleration: int
    # Cars may differ and have their own limitations
    max_velocity: int

    color: Tuple[int, int, int]

    def __init__(self, current_ele: Element, max_velocity: int = 10):
        self.current_element = current_ele
        self.max_velocity = max_velocity

        self.velocity = 0
        self.acceleration = 1

        self.color = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))

    def get_curr_lane_cell(self) -> int:
        if not isinstance(self.current_ele, Lane):
            return -1

        return self.current_ele.get_car_cell(self)
