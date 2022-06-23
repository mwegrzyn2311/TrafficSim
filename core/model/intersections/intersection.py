from typing import List, Dict, TYPE_CHECKING
from core.model import Node, Road, Vec2d, Car
from enum import Enum
import random

if TYPE_CHECKING:
    from core.model import Lane


# Helper class
class Direction(Enum):
    RIGHT = 1
    FORWARD = 2
    LEFT = 3
    BEHIND = 4


# FIXME: Potentially untested
def direction_between_roads(road_from: Road, road_to: Road, intersection_from: Node) -> Direction:
    a: Vec2d = road_from.get_the_other_end(intersection_from).pos
    b: Vec2d = intersection_from.pos
    c: Vec2d = road_to.get_the_other_end(intersection_from).pos
    # Now we need to get angle between ab and bc
    v_ab: Vec2d = b.__sub__(a)
    v_bc: Vec2d = c.__sub__(b)
    angle = v_ab.__angle__(v_bc)
    if angle == 0.0:
        return Direction.BEHIND
    elif angle == 90.0:
        return Direction.RIGHT
    elif angle == 180.0:
        return Direction.FORWARD
    elif angle == 270.0:
        return Direction.LEFT
    else:
        raise Exception(f"Angle {angle} between two roads not supported")


# TODO: Add typing for Intersection (1st arg) and Node (2nd arg)
def find_lane_connecting_two_nodes(intersection_from, node_to):
    for road in intersection_from.roads:
        # TODO: Look into that
        if road.left_node == intersection_from and road.right_node == node_to:
            return road.right_lanes[0]
        elif road.right_node == intersection_from and road.left_node == node_to:
            return road.left_lanes[0]

    raise Exception("Road connecting an intersection and a node not found")


# Helper class
class Queue:
    road_from: Road
    lane_to: 'Lane' or None
    car: Car or None
    drive_direction: Direction or None

    def __init__(self, road_from: Road):
        self.road_from = road_from
        self.lane_to = None
        self.car = None
        self.drive_direction = None

    def is_empty(self) -> bool:
        return self.car is None

    # TODO: Add typing for intersection
    def place_car(self, car: Car, intersection_from):
        self.car = car
        self.lane_to = find_lane_connecting_two_nodes(intersection_from, car.next_planned_node)
        self.drive_direction = direction_between_roads(self.road_from, self.lane_to.road, intersection_from)

    def make_empty(self):
        self.car = None
        self.lane_to = None
        self.drive_direction = None

    def can_drive(self, all_queues, intersection) -> False:
        # Handle all turn directions
        if self.drive_direction == Direction.BEHIND:
            raise Exception("Turning back not supported")
        elif self.drive_direction == Direction.RIGHT:
            return True

        # At this point LEFT and FORWARD remains
        for other_queue in all_queues:
            if other_queue != self:
                relative_dir: Direction = direction_between_roads(self.road_from, other_queue.road_from, intersection)
                if relative_dir == Direction.FORWARD and (
                        other_queue.drive_direction == Direction.FORWARD or other_queue.drive_direction == Direction.RIGHT) and self.drive_direction == Direction.LEFT:
                    return False
                elif relative_dir == Direction.RIGHT and self.drive_direction == Direction.FORWARD or (
                        self.drive_direction == Direction.LEFT and other_queue.drive_direction == Direction.LEFT or other_queue.drive_direction == Direction.FORWARD):
                    return False
        return True


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
        queues_to_empty = []
        # We only consider queues that are not empty and those were cars are not blocked by busy space on their dst lane
        queues_that_might_drive = list(filter(lambda q: not q.is_empty() and 0 not in q.lane_to.cars.keys(), self.queues.values()))
        for queue in queues_that_might_drive:
            if queue.can_drive(queues_that_might_drive, self):
                queues_to_empty.append(queue)

        # To avoid blocked intersection, let at least one car drive
        if len(queues_that_might_drive) > 0 and len(queues_to_empty) == 0:
            queues_to_empty = random.sample(queues_that_might_drive, k=1)

        for queue in queues_to_empty:
            # Drive those cars that can drive in this turn
            dst_lane = queue.lane_to
            car = queue.car
            car.current_element.remove_car_by_car(car)
            dst_lane.add_car(0, car)
            car.plan_next_node()
            queue.make_empty()
