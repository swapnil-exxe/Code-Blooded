import heapq
from typing import Dict, List, Tuple, Optional

class DijkstraGraph:
    """
    Weighted directed graph implementation providing Dijkstra's shortest path algorithm
    using a binary min-heap priority queue in O((V + E) log V) time complexity.
    """

    def __init__(self):
        self.adj_list: Dict[str, List[Tuple[str, float]]] = {}

    def add_edge(self, u: str, v: str, weight: float) -> None:
        """Adds a directed edge from node u to node v with non-negative weight."""
        if weight < 0:
            raise ValueError(f"Dijkstra's algorithm does not support negative weight edge ({u} -> {v}, weight={weight}).")
        
        if u not in self.adj_list:
            self.adj_list[u] = []
        if v not in self.adj_list:
            self.adj_list[v] = []
        
        self.adj_list[u].append((v, weight))

    def shortest_path(self, start: str) -> Tuple[Dict[str, float], Dict[str, Optional[str]]]:
        """
        Computes shortest distances and predecessor dictionary from starting node.
        Returns (distances, predecessors).
        """
        if start not in self.adj_list:
            self.adj_list[start] = []

        distances: Dict[str, float] = {node: float('inf') for node in self.adj_list}
        predecessors: Dict[str, Optional[str]] = {node: None for node in self.adj_list}
        
        distances[start] = 0.0
        min_heap: List[Tuple[float, str]] = [(0.0, start)]

        while min_heap:
            current_dist, u = heapq.heappop(min_heap)

            if current_dist > distances[u]:
                continue

            for v, weight in self.adj_list[u]:
                if distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    predecessors[v] = u
                    heapq.heappush(min_heap, (distances[v], v))

        return distances, predecessors

    def get_path(self, start: str, target: str) -> Optional[List[str]]:
        """Reconstructs and returns the shortest path sequence from start to target, or None if unreachable."""
        distances, predecessors = self.shortest_path(start)
        if distances.get(target, float('inf')) == float('inf'):
            return None

        path = []
        curr: Optional[str] = target
        while curr is not None:
            path.append(curr)
            curr = predecessors[curr]

        path.reverse()
        return path
