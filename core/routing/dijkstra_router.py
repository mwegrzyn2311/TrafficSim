from __future__ import annotations

import pprint
from typing import List, Callable, Set

import heapq
import math

from core.model import Node


def real_distance(lhs: Node, rhs: Node):
	assert(not set(lhs.get_roads()).isdisjoint(rhs.get_roads()))

	return (lhs.pos - rhs.pos).length()


def hop_distance(lhs: Node, rhs: Node):
	return 1


def calculate_dijkstra_route(
		src: Node, dst: Node,
		nodes: List[Node],
		distance: Callable[[Node, Node], float] = hop_distance
) -> List[Node]:
	class DijkstraNode:
		distance: float = math.inf

		node: Node = None
		previous: DijkstraNode = None

		def __lt__(self, other: DijkstraNode):
			return self.distance < other.distance

	node_to_d_node = {}

	heap_queue = []

	for node in nodes:
		new_d_node = DijkstraNode()
		new_d_node.node = node

		if node is src:
			new_d_node.distance = 0

		node_to_d_node[node] = new_d_node

		heapq.heappush(heap_queue, new_d_node)

	while len(heap_queue) > 0:
		current: DijkstraNode = heapq.heappop(heap_queue)
		links = current.node.get_roads()
		neighbour_nodes: Set[Node] = set()

		for link in links:
			neighbour_nodes.add(link.left_node)
			neighbour_nodes.add(link.right_node)

		neighbour_nodes.remove(current.node)

		for node in neighbour_nodes:
			neighbour_d_node = node_to_d_node[node]
			dist_via_neighbour = current.distance + distance(current.node, node)

			if neighbour_d_node.distance > dist_via_neighbour:
				neighbour_d_node.distance = dist_via_neighbour
				neighbour_d_node.previous = current

		heapq.heapify(heap_queue)

	last_d_node = node_to_d_node[dst]

	path: List[Node] = []

	while last_d_node:
		path.append(last_d_node.node)
		last_d_node = last_d_node.previous

	return list(reversed(path))[1::]
