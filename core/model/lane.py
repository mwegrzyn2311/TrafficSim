from .element import Element
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from .car import Car


# Lane consists of cells numbered from 0 to num of cells - 1 (where 0 is the end for ease of calculations)
class Lane(Element):
    with_priority: bool
    # For convenience later on, keep number of cells that should be calculated on init
    num_of_cells: int
    speed_limit: int = 3
    # Mapping cell no. -> Car
    cars: Dict[int, 'Car']
    road: 'Road'

    def __init__(self, road: 'Road', cars: Dict[int, 'Car'] = None, num_of_cells: int = 1):
        self.num_of_cells = num_of_cells
        self.road = road
        if cars is None:
            self.cars = {}
        else:
            self.cars = cars

    def add_car(self, cell_no: int, car: 'Car') -> None:
        self.cars[cell_no] = car
        car.current_element = self

    def remove_car(self, cell_no: int) -> None:
        del self.cars[cell_no]

    def move_car(self, cell_from: int, distance: int) -> None:
        assert(cell_from + distance < self.num_of_cells)

        self.cars[cell_from + distance] = self.cars[cell_from]
        del self.cars[cell_from]

    def get_cell(self, pos):
        assert(pos < self.num_of_cells)
        if pos in self.cars.keys():
            return self.cars[pos]
        else:
            return None

    def get_car_cell(self, car: 'Car'):
        return list(self.cars.keys())[list(self.cars.values()).index(car)]

    def get_car_in_front(self, car: 'Car') -> 'Car' or None:
        cars_vals = list(self.cars.values())
        try:
            return cars_vals[cars_vals.index(car) - 1]
        except (ValueError, IndexError):
            return None
