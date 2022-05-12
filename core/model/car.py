from __future__ import annotations

from random import random
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

    def update_velocity_and_move(self, braking_chance: float):
        updated_velocity = self.velocity

        # TODO: Handle not only lanes but also intersections, etc.
        if isinstance(self.current_ele, Lane):
            lane: Lane = self.current_ele
            # 1: accelerate
            updated_velocity += self.acceleration

            # 2: braking
            curr_pos = lane.get_car_cell(self)
            next_pos = lane.get_car_in_front(self)
            updated_velocity = max(updated_velocity, curr_pos - next_pos)

            # 3: random braking
            a = random()
            if a < braking_chance:
                updated_velocity -= 1

            # 4: update and move
            self.velocity = max(updated_velocity, self.max_velocity)
            lane.move_car(curr_pos, self.velocity)

    def get_curr_lane_cell(self) -> int:
        if not isinstance(self.current_ele, Lane):
            return -1

        return self.current_ele.get_car_cell(self)
