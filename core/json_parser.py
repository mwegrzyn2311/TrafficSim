import json
from typing import Dict

from core.model import *

type_to_intersection = {
    "with_lights": lambda obj: IntersectionWithLights(Vec2d(obj["x"], obj["y"])),
    "roundabout": lambda obj: Roundabout(Vec2d(obj["x"], obj["y"]))
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
