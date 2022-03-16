import sys
import PySide6.QtCore
from PySide6.QtWidgets import QApplication

from core import load_city_from_json

import gui

print("Traffic simulator")
print("Version: 0.0.1")

print("Pyside version: ", PySide6.__version__)
print("QtCore version: ", PySide6.QtCore.__version__)

city = load_city_from_json("city.json")

app = QApplication(sys.argv)

window = gui.MainWindow()
window.show()

app.exec()