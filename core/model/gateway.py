from core.model import Node, Road, Vec2d


class Gateway(Node):
	road: Road

	def __init__(self, pos: Vec2d):
		super().__init__(pos)
