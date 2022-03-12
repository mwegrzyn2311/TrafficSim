from ..generated.ui_simulation_view import Ui_simulation_view
from .switchable_view import SwitchableView


class SimulationViewController(SwitchableView):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_simulation_view()
        self.ui.setupUi(self)
