import json
from typing import Dict

from core.model import *


def vec_from_obj(obj) -> Vec2d:
    return Vec2d(obj["x"], obj["y"])


type_to_intersection = {
    "with_lights": lambda obj: IntersectionWithLights(vec_from_obj(obj)),
    "roundabout": lambda obj: Roundabout(vec_from_obj(obj)),
    "with_signs": lambda obj: IntersectionWithSigns(vec_from_obj(obj)),
    "prio_to_right": lambda obj: IntersectionWithPrioToRight(vec_from_obj(obj))
}


# TODO: Move to another dir if gets used by another parser (xml-parser or sth)
def load_city_from_dict(data: dict) -> City:
    nodes: Dict[str, Node] = {}
    for intersection in data["intersections"]:
        obj_type = intersection["intersection_type"]
        pos = intersection["pos"]
        obj_id = intersection["id"]
        intersection_obj = type_to_intersection[obj_type](pos)
        nodes[obj_id] = intersection_obj
    for gateway in data["gateways"]:
        pos = gateway["pos"]
        obj_id = gateway["id"]
        nodes[obj_id] = Gateway(Vec2d(pos["x"], pos["y"]))
    for road in data["roads"]:
        left_node = nodes[road["left_node"]]
        right_node = nodes[road["right_node"]]
        road_obj = Road(left_node, right_node, road["left_lanes_count"], road["right_lanes_count"])
        left_node.add_road(road_obj)
        right_node.add_road(road_obj)
    # TODO: cast those to proper types
    return City(list(filter(lambda node: isinstance(node, Intersection), nodes.values())), list(filter(lambda node: isinstance(node, Gateway), nodes.values())))


def load_city_from_json(filename) -> City:
    f = open(filename)
    city = load_city_from_dict(json.load(f))
    f.close()
    return city
