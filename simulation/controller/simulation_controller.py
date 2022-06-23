import random
from typing import List, Callable, Generator

from PySide6.QtCore import QThread, QObject, QSemaphore, Signal, Slot

from core.driver.abstract_driver import AbstractDriver
from core.driver.basic_driver import BasicDriver
from core.model import City, Car
import time

from simulation.controller.activation import random_activation


class SimulationControllerSignals(QObject):
    step = Signal()


class SimulationController(QThread):
    city: City
    drivers: List[AbstractDriver] = []
    drivers_to_remove: List[AbstractDriver] = []
    activation_order: Callable[[List[AbstractDriver]], Generator[AbstractDriver, None, None]] = random_activation

    is_paused: bool
    sleep_time: float
    spawn_car_chance = 0.2

    signal = SimulationControllerSignals()
    step_semaphore = QSemaphore(0)

    def __init__(self, city: City, parent=None):
        super(SimulationController, self).__init__(parent)

        self.city = city
        self.is_paused = True
        self.sleep_time = 0.1

    def play(self) -> None:
        if self.is_paused:
            self.is_paused = False
            self.step_semaphore.release()

    def pause(self) -> None:
        if not self.is_paused:
            self.is_paused = True

    def step(self) -> None:
        assert self.is_paused
        self._do_step()

    def _generate_traffic(self):
        gateways = self.city.gateways
        for i in range(3):
            src_dest_gateways = random.sample(gateways, k=2)
            src_gateway = src_dest_gateways[0]
            # Avoid queues with milions of elements
            if len(src_gateway.car_queue) > 10:
                continue
            dest_gateway = src_dest_gateways[1]
            car = Car(src_gateway)
            src_gateway.add_car(car)
            driver = BasicDriver(self.city, src_gateway, dest_gateway, car, self)
            self.drivers.append(driver)

    def register_driver_for_removal(self, driver: AbstractDriver):
        self.drivers_to_remove.append(driver)

    def _cleanup_drivers(self):
        for driver in self.drivers_to_remove:
            self.drivers.remove(driver)
        self.drivers_to_remove = []

    def _do_step(self):
        for driver in self.activation_order.__func__(self.drivers):
            driver.step()

        self._generate_traffic()
        self.city.step()
        self.signal.step.emit()

    def run(self):
        while True:
            self.step_semaphore.acquire()
            self._do_step()

            if not self.is_paused:
                self.step_semaphore.release()
            time.sleep(self.sleep_time)
