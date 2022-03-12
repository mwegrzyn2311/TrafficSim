from .welcome_view_controller import WelcomeViewController
from .simulation_view_controller import SimulationViewController
from .switchable_view import SwitchableView

switchable_views_map = {
    "welcome_view": WelcomeViewController,
    "simulation_view": SimulationViewController,
}
