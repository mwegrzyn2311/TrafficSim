from typing import List, Dict
from core.model import Node, Road, Vec2d, Car


# TODO: Add typing for Intersection (1st arg) and Node (2nd arg)
def find_lane_connecting_two_nodes(intersection_from, node_to):
    for road in intersection_from.roads:
        # TODO: Look into that
        if road.left_node == intersection_from and road.right_node == node_to:
            return road.right_lanes[0]
        elif road.right_node == intersection_from and road.left_node == node_to:
            return road.left_lanes[0]

    raise Exception("Road connecting an intersection and a node not found")


class Queue:
    road_from: Road
    # TODO: Add Lane typing
    # lane_to
    car: Car or None

    def __init__(self, road_from: Road):
        self.road_from = road_from
        self.lane_to = None
        self.car = None

    def is_empty(self) -> bool:
        return self.car is None

    # TODO: Add typing for intersection
    def place_car(self, car: Car, intersection_from):
        self.car = car
        self.lane_to = find_lane_connecting_two_nodes(intersection_from, car.next_planned_node)

    def make_empty(self):
        self.car = None
        self.lane_to = None


class Intersection(Node):
    roads: List[Road]
    queues: Dict[Road, Queue]

    def __init__(self, pos: Vec2d, radius: int = 1):
        super().__init__(pos, radius)
        self.roads = []
        # TODO: Should be sorted by "rightness" (either in add_road or in json)
        self.queues = {}

    def add_road(self, road: Road):
        assert (road not in self.roads)

        self.roads.append(road)
        self.queues[road] = Queue(road)

    def get_roads(self) -> List["Road"]:
        return self.roads

    def get_type_str(self) -> str:
        return "intersection"

    def add_car_to_queue(self, car: Car):
        # FIXME: Handle other car elements than lane
        self.queues[car.current_element.road].place_car(car, self)

    def step(self):
        for queue in self.queues.values():
            if not queue.is_empty():
                car = queue.car
                # TODO: Handle cars crossing each other
                dst_lane = queue.lane_to
                # Otherwise the other end is blocked
                if 0 not in dst_lane.cars.keys():
                    car.current_element.remove_car_by_car(car)
                    dst_lane.add_car(0, car)
                    car.plan_next_node()
                    queue.make_empty()
