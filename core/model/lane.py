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
        print(f"Adding car to a cell at {cell_no}")
        self.cars[cell_no] = car
        car.current_element = self

    def remove_car(self, cell_no: int) -> None:
        del self.cars[cell_no]

    def last_unoccupied_cell(self):
        for i in range(self.num_of_cells - 1, 0, -1):
            if i in self.cars.keys():
                return i
        return -1


    def move_car(self, cell_from: int, distance: int) -> None:
        print(f"moving a car from = {cell_from} by distance = {distance}")
        if distance == 0:
            return
        if cell_from + distance >= self.num_of_cells:
            # This is so that car stops if it reaches the end of the road. Braking would probably be nicer, but let's stick with it for now
            last_unoccupied_cell = self.last_unoccupied_cell()
            assert (last_unoccupied_cell != -1)
            self.cars[last_unoccupied_cell] = self.cars[cell_from]
        else:
            assert cell_from + distance not in self.cars.keys()
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
        cars_positions_sorted = sorted(list(self.cars.keys()), reverse=True)
        # TODO: Remove this comment
        # This code so spaghetti, lmao
        next_car_index = cars_positions_sorted.index(self.get_car_cell(car)) - 1
        if next_car_index < 0:
            return None
        return self.cars[cars_positions_sorted[next_car_index]]
