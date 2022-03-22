from core.model import City
from threading import Thread
import time


class SimulationController(Thread):
    city: City
    p: float
    is_paused: bool
    sleep_time: float

    def __init__(self, city: City, braking_chance: float):
        super().__init__()
        self.city = city
        self.p = braking_chance
        self.is_paused = True
        self.sleep_time = 5

    def step(self):
        for car in self.city.cars:
            car.update_velocity_and_move(self.p)

    def run(self):
        self.is_paused = False
        while not self.is_paused:
            self.step()
            time.sleep(self.sleep_time)

    def join(self, timeout: float = None):
        self.is_paused = True
        super().join(timeout)
