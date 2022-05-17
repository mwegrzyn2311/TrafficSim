import logging
import os

from PySide6 import QtCore
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QFileDialog, QDialog

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

	# noinspection PyPep8Naming
	@Slot()
	def onMapPathBrowse(self):
		logging.debug("Opening map browser")
		old_value = self.ui.map_path.text()
		if old_value is not None and os.path.isfile(old_value):
			search_dir = os.path.dirname(old_value)
		else:
			search_dir = QtCore.QDir.currentPath()
		filename = QFileDialog.getOpenFileName(self, "Select Map file", search_dir, "Map files (*.json)")
		if filename:
			self.ui.map_path.setText(str(filename[0]))


	def preferred_size(self):
		return 400, 300
