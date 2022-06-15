import random
from typing import List, Generator

from core.driver.abstract_driver import AbstractDriver


def create_order_activation(drivers: List[AbstractDriver]) -> Generator[AbstractDriver, None, None]:
	for driver in drivers:
		yield driver


def random_activation(drivers: List[AbstractDriver]) -> Generator[AbstractDriver, None, None]:
	length = len(drivers)
	permutation = random.sample(drivers, length)

	for driver in permutation:
		yield driver
