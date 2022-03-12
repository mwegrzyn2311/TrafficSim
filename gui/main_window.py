from PySide6.QtWidgets import QWidget, QMainWindow

from . import views


class MainWindow(QMainWindow):
	_current_view: QWidget

	def __init__(self):
		QMainWindow.__init__(self)

		self.setWindowTitle("TrafficSim")
		self.showMaximized()
		self.load_default_window()

	def load_default_window(self) -> None:
		self._current_view = views.WelcomeViewController()
		self.setCentralWidget(self._current_view)
