from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow

from . import views


class MainWindow(QMainWindow):
	_current_view: views.SwitchableView

	def __init__(self):
		QMainWindow.__init__(self)

		self.setWindowTitle("TrafficSim")
		self.load_default_window()

	def load_default_window(self) -> None:
		self._current_view = views.WelcomeViewController(self)

		preferred_size = self._current_view.preferred_size()
		if preferred_size:
			self.setMaximumSize(preferred_size[0], preferred_size[1])
			self.setMinimumSize(preferred_size[0], preferred_size[1])
			self.setMaximumSize(2048, 2048)
		else:
			self.showMaximized()

		self._current_view.trigger_switch_view.connect(self.switch_current_view)
		self.setCentralWidget(self._current_view)

	@Slot(str)
	def switch_current_view(self, view_str) -> None:
		self._current_view = views.switchable_views_map[view_str]()

		preferred_size = self._current_view.preferred_size()
		if preferred_size:
			self.setMaximumSize(preferred_size[0], preferred_size[1])
			self.setMinimumSize(preferred_size[0], preferred_size[1])
		else:
			self.setMaximumSize(2048, 2048)
			self.showMaximized()

		self.setCentralWidget(self._current_view)
