from .road import Road


class Car:
    current_road: Road
    # calculated from end of the road (being right at the lights stop would mean being at cell 0)
    current_cell: int

    def __init__(self, current_road: Road, current_cell: int = -1):
        self.current_road = current_road
        if current_cell == -1:
            self.current_cell = current_road.num_of_cells - 1
        else:
            self.current_cell = current_cell

    def move_to_new_road(self, new_road: Road):
        self.current_road = new_road
        self.current_cell = new_road.num_of_cells - 1
