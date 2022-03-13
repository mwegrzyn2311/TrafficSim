from PySide6.QtGui import QColor

from .element import Element


class Car:
    current_ele: Element
    velocity: int = 0
    # Cars may differ and have their own limitations
    max_velocity: int
    # Not sure whether it should be QColor or rgba structure but I guess QColor gives more options
    color: QColor

    def __init__(self, current_ele: Element, max_velocity: int = 10):
        self.current_ele = current_ele
        self.max_velocity = max_velocity
