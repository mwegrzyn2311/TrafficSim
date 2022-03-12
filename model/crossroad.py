from .road import Road
from typing import List
from enum import Enum


class CrossroadType(Enum):
    LIGHTS = 1,
    ROUNDABOUT = 2,
    PRIO_TO_RIGHT = 3,
    UNMARKED = 4,


class Crossroad:
    x: int
    y: int
    roads: List[Road]
    type: CrossroadType
