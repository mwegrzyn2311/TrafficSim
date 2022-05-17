import sys
import logging

import PySide6.QtCore
from PySide6.QtWidgets import QApplication

from core import load_city_from_json

import gui

logging.basicConfig()
# logging.root.setLevel(logging.INFO)
logging.root.setLevel(logging.DEBUG)

logging.info("Traffic simulator")
logging.info("Version: 0.0.1")

logging.info("Pyside version: " + PySide6.__version__)
logging.info("QtCore version: " + PySide6.QtCore.__version__)

city = load_city_from_json("resources/city.json")

app = QApplication(sys.argv)

window = gui.MainWindow()
window.show()

app.exec()