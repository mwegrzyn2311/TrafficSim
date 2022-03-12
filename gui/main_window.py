from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow

from . import views


class MainWindow(QMainWindow):
	_current_view: views.SwitchableView

	def __init__(self):
		QMainWindow.__init__(self)

		self.setWindowTitle("TrafficSim")
		self.showMaximized()
		self.load_default_window()

	def load_default_window(self) -> None:
		self._current_view = views.WelcomeViewController(self)
		self._current_view.trigger_switch_view.connect(self.switch_current_view)
		self.setCentralWidget(self._current_view)

	@Slot(str)
	def switch_current_view(self, view_str) -> None:
		self._current_view = views.switchable_views_map[view_str]()
		self.setCentralWidget(self._current_view)
