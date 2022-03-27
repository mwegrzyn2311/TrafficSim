from PySide6.QtCore import Slot

from core import load_city_from_json
from .switchable_view import SwitchableView
from ..generated.ui_simulation_view import Ui_simulation_view
from ..map_visualizer import MapSceneManager
from ..util import ScalableMovableViewController


class SimulationViewController(SwitchableView):
    _map_manager: MapSceneManager
    _scalable_movable_view_controller: ScalableMovableViewController

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_simulation_view()
        self.ui.setupUi(self)
        _scalable_movable_view_controller = ScalableMovableViewController(self.ui.visualization_canvas)

        self._render_map()

    def _render_map(self):
        city = load_city_from_json("resources/city.json")
        self._map_manager = MapSceneManager(city)
        self.ui.visualization_canvas.setScene(self._map_manager.scene)

    # noinspection PyPep8Naming
    @Slot()
    def playPause(self) -> None:
        pass

    # noinspection PyPep8Naming
    @Slot()
    def step(self) -> None:
        pass
