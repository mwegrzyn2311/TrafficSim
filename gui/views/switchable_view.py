from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget


class SwitchableView(QWidget):
    trigger_switch_view: Signal = Signal(str)

    def __init__(self, parent):
        super().__init__(parent)
