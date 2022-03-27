from PySide6.QtCore import QObject, QPointF, Signal, QEvent, Qt, QPoint
from PySide6.QtGui import QMouseEvent, QWheelEvent
from PySide6.QtWidgets import QGraphicsView, QApplication


class ScalableMovableViewController(QObject):
	zoomed: Signal = Signal()

	_view: QGraphicsView
	_zoom_factor: float = 1.0015
	_modifiers: Qt.KeyboardModifiers = Qt.ControlModifier

	_target_scene_point: QPoint
	_target_viewport_pos: QPoint

	def __init__(self, view: QGraphicsView):
		super().__init__(view)
		self._view = view

		self._view.setDragMode(QGraphicsView.ScrollHandDrag)

		self._target_scene_point = QPoint()
		self._target_viewport_pos = QPoint()

		self._view.viewport().installEventFilter(self)
		self._view.setMouseTracking(True)

	def set_modifiers(self, modifiers: Qt.KeyboardModifiers):
		self._modifiers = modifiers

	def zoom(self, factor):
		view = self._view
		view.scale(factor, factor)
		view.centerOn(self._target_scene_point)

		center = QPointF(view.viewport().width() / 2, view.viewport().height() / 2).toPoint()

		delta_viewport_pos = self._target_viewport_pos - center

		viewport_center: QPointF = view.mapFromScene(self._target_scene_point) - delta_viewport_pos
		view.centerOn(view.mapToScene(viewport_center))

		self.zoomed.emit()

	def eventFilter(self, watched: QObject, event: QEvent) -> bool:
		if event.type() == QEvent.MouseMove:
			mouse_event: QMouseEvent = event
			delta = self._target_viewport_pos - mouse_event.position().toPoint()
			if abs(delta.x()) > 5 or abs(delta.y()) > 5:
				self._target_viewport_pos = mouse_event.position().toPoint()
				self._target_scene_point = self._view.mapToScene(mouse_event.position().toPoint())
		elif event.type() == QEvent.Wheel:
			wheel_event: QWheelEvent = event
			if QApplication.keyboardModifiers() == self._modifiers:

				angle = wheel_event.angleDelta().y()
				factor = pow(self._zoom_factor, angle)
				self.zoom(factor)
				return True

		return False
