from typing import Tuple
import random

from .element import Element


class Car:
    current_ele: Element

    velocity: int = 0
    # Cars may differ and have their own limitations
    max_velocity: int

    color: Tuple[int, int, int]

    def __init__(self, current_ele: Element, max_velocity: int = 10):
        self.current_ele = current_ele
        self.max_velocity = max_velocity

        self.color = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))

