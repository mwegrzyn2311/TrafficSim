import logging
import csv

from PySide6.QtCore import Slot

from core import load_city_from_json
from core.model import City
from simulation.controller.simulation_controller import SimulationController
from .switchable_view import SwitchableView
from ..generated.ui_simulation_view import Ui_simulation_view
from ..map_visualizer import MapSceneManager
from ..util import ScalableMovableViewController
from simulation.stats import SimmStats

import csv


class SimulationViewController(SwitchableView):
    _map_manager: MapSceneManager
    _scalable_movable_view_controller: ScalableMovableViewController
    _simulation_controller: SimulationController
    _city: City

    _is_paused: bool = True

    simm_stats: SimmStats = SimmStats()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_simulation_view()
        self.ui.setupUi(self)
        _scalable_movable_view_controller = ScalableMovableViewController(self.ui.visualization_canvas)

        self._render_map()
        self._init_simulation_thread()

    def _render_map(self):
        self._city = load_city_from_json("resources/city.json")
        self._map_manager = MapSceneManager(self._city)
        self.ui.visualization_canvas.setScene(self._map_manager.scene)

    def _init_simulation_thread(self):
        self._simulation_controller = SimulationController(self._city)
        self._simulation_controller.signal.step.connect(self.update)
        self._simulation_controller.start()

    # noinspection PyPep8Naming
    @Slot()
    def saveStatistic(self) -> None:
        header = ["turn", "total_drivers", "min_speed", "avg_speed", "max_speed"]
        with open("stats.csv", "w+", newline="") as file:
            writer: csv.DictWriter = csv.writer(file)
            writer.writerow(header)
            for turn in self.simm_stats.stats_per_turn.items():
                writer.writerow(
                    [
                        turn[0],
                        turn[1]["city"]["total"],
                        turn[1]["speed"]["min"],
                        turn[1]["speed"]["avg"],
                        turn[1]["speed"]["max"]
                    ]
                )

    # noinspection PyPep8Naming
    @Slot()
    def playPause(self) -> None:
        self._is_paused = not self._is_paused
        if self._is_paused:
            logging.info("Change state: PAUSE")
            self.ui.step_button.setDisabled(False)
            self._simulation_controller.pause()
        else:
            logging.info("Change state: PLAY")
            self.ui.step_button.setDisabled(True)
            self._simulation_controller.play()

    # noinspection PyPep8Naming
    @Slot()
    def step(self) -> None:
        assert self._is_paused
        logging.info("Single STEP")
        self._simulation_controller.step()

    @Slot()
    def update(self) -> None:
        logging.debug("Rendered next frame")
        self._map_manager.update()


