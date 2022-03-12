import os
import sys

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget

from ..generated.ui_welcome_view import Ui_welcome_view


class WelcomeViewController(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.ui = Ui_welcome_view()
		self.ui.setupUi(self)

	# noinspection PyPep8Naming
	@Slot()
	def onStart(self):
		print("clicked")

