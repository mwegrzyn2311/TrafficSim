from .crossroad import Crossroad
import math


class Road:
    crossroad_from: Crossroad
    crossroad_to: Crossroad
    num_of_lanes: int
    with_priority: bool
    # For convenience later on, keep number of cells that should be calculated on init
    num_of_cells: int

    def __init__(self, crossroad_from: Crossroad, crossroad_to: Crossroad, with_priority, num_of_lanes: int = 1):
        self.crossroad_from = crossroad_from
        self.crossroad_to = crossroad_to
        self.with_priority = with_priority
        self.num_of_lanes = num_of_lanes
        self.num_of_cells = self.__calculate_num_of_cells()

    def __calculate_num_of_cells(self) -> int:
        return math.ceil(math.pow(self.crossroad_from.x - self.crossroad_to.x, 2) + math.pow(self.crossroad_from.y - self.crossroad_to.y, 2))
