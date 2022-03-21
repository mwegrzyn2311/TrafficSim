from random import random
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
            updated_velocity = car.velocity

            # 1: accelerate
            updated_velocity += car.acceleration

            # 2: braking
            curr_pos = car.get_cell_no()
            next_pos = car.get_car_in_front().get_cell_no()
            updated_velocity = max(updated_velocity, curr_pos - next_pos)

            # 3: random braking
            a = random()
            if a < self.p:
                updated_velocity -= 1

            # 4: update and move
            car.set_velocity(updated_velocity)
            car.move()

    def run(self):
        self.is_paused = False
        while not self.is_paused:
            self.step()
            time.sleep(self.sleep_time)

    def join(self, timeout: float = None):
        self.is_paused = True
        super().join(timeout)
