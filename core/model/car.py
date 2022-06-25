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
    next_planned_node_idx: int
    # TODO: Add typed next_node here

    color: Tuple[int, int, int]

    def __init__(self, current_ele: Element, max_velocity: int = 10):
        self.current_element = current_ele
        self.max_velocity = max_velocity

        self.velocity = 0
        self.acceleration = 1

        self.driver = None
        self.next_planned_node_idx = -1
        self.planned_route = []
        self.next_planned_node = None

        self.color = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))

    def plan_next_node(self):
        self.next_planned_node_idx += 1
        if self.next_planned_node_idx < len(self.planned_route):
            self.next_planned_node = self.planned_route[self.next_planned_node_idx]

    def get_curr_lane_cell(self) -> int:
        if not isinstance(self.current_element, Lane):
            return -1

        return self.current_element.get_car_cell(self)
