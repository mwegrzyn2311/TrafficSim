from .element import Element
from .car import Car
from typing import Dict


class Lane(Element):
    with_priority: bool
    # For convenience later on, keep number of cells that should be calculated on init
    num_of_cells: int
    speed_limit: int = 10
    # Mapping cell no. -> Car
    cars: Dict[int, Car]

    def __init__(self, cars: Dict[int, Car] = None, num_of_cells: int = 1):
        self.num_of_cells = num_of_cells
        if cars is None:
            self.cars = {}
        else:
            self.cars = cars

    def add_car(self, cell_no: int, car: Car) -> None:
        self.cars[cell_no] = car
        car.current_node = self

    def remove_car(self, cell_no: int) -> None:
        del self.cars[cell_no]

    def move_car(self, cell_from: int, distance: int) -> None:
        assert(cell_from + distance < self.num_of_cells)

        self.cars[cell_from + distance] = self.cars[cell_from]
        del self.cars[cell_from]
