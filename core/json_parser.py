import json

from .model import City


def load_city_from_json(filename) -> City:
    f = open(filename)
    data = json.load(f)
    for i in data:
        print(i)
    f.close()
