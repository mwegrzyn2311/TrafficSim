from .node import Node
from .element import Element
from .car import Car
from .vec2d import vec2d_dist
from typing import Dict


class Road(Element):
    start: Node
    end: Node
    # TODO: Add support for more than what is currently - only one lane
    num_of_lanes: int
    with_priority: bool
    # For convenience later on, keep number of cells that should be calculated on init
    num_of_cells: int
    speed_limit: int = 10
    # Mapping cell no. -> Car
    cars: Dict[int, Car]

    def __init__(self, start: Node, end: Node, with_priority, cars: Dict[int, Car] = None, num_of_lanes: int = 1):
        self.start = start
        self.end = end
        self.with_priority = with_priority
        self.num_of_lanes = num_of_lanes
        self.num_of_cells = vec2d_dist(start.pos, end.pos)
        if cars is None:
            self.cars = {}
        else:
            self.cars = cars

    def add_car(self, cell_no: int, car: Car):
        self.cars[cell_no] = car
        car.current_node = self
