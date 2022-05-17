from PySide6.QtCore import Slot

from ..generated.ui_welcome_view import Ui_welcome_view
from .switchable_view import SwitchableView


class WelcomeViewController(SwitchableView):

	def __init__(self, parent=None):
		super().__init__(parent)
		self.parent = parent
		self.ui = Ui_welcome_view()
		self.ui.setupUi(self)

	# noinspection PyPep8Naming
	@Slot()
	def onStartClicked(self):
		self.trigger_switch_view.emit("simulation_view")

	def preferred_size(self):
		return 400, 300
