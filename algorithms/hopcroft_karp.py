from collections import deque
from typing import List, Dict, Optional

class HopcroftKarp:
    """
    Hopcroft-Karp algorithm for Maximum Bipartite Matching.
    Calculates maximum cardinal matching in O(E * sqrt(V)) time.
    """

    def __init__(self, left_count: int, right_count: int):
        if left_count <= 0 or right_count <= 0:
            raise ValueError("Left and Right set sizes must be positive integers.")
        
        self.left_count = left_count
        self.right_count = right_count
        self.adj: List[List[int]] = [[] for _ in range(left_count + 1)]
        
        self.pair_left = [0] * (left_count + 1)
        self.pair_right = [0] * (right_count + 1)
        self.dist = [0] * (left_count + 1)

    def add_edge(self, u: int, v: int) -> None:
        """Adds a directed bipartite edge from left node u (1-indexed) to right node v (1-indexed)."""
        if not (1 <= u <= self.left_count and 1 <= v <= self.right_count):
            raise IndexError(f"Edge ({u}, {v}) out of bounds for Left({self.left_count}) and Right({self.right_count}).")
        self.adj[u].append(v)

    def _bfs(self) -> bool:
        queue = deque()
        for u in range(1, self.left_count + 1):
            if self.pair_left[u] == 0:
                self.dist[u] = 0
                queue.append(u)
            else:
                self.dist[u] = float('inf')

        self.dist[0] = float('inf')

        while queue:
            u = queue.popleft()
            if self.dist[u] < self.dist[0]:
                for v in self.adj[u]:
                    if self.dist[self.pair_right[v]] == float('inf'):
                        self.dist[self.pair_right[v]] = self.dist[u] + 1
                        queue.append(self.pair_right[v])

        return self.dist[0] != float('inf')

    def _dfs(self, u: int) -> bool:
        if u != 0:
            for v in self.adj[u]:
                if self.dist[self.pair_right[v]] == self.dist[u] + 1:
                    if self._dfs(self.pair_right[v]):
                        self.pair_right[v] = u
                        self.pair_left[u] = v
                        return True
            self.dist[u] = float('inf')
            return False
        return True

    def max_matching(self) -> int:
        """Computes and returns the maximum number of matching edges."""
        matching = 0
        while self._bfs():
            for u in range(1, self.left_count + 1):
                if self.pair_left[u] == 0 and self._dfs(u):
                    matching += 1
        return matching

    def get_matches(self) -> Dict[int, int]:
        """Returns dictionary mapping left_node -> right_node for matched pairs."""
        return {u: self.pair_left[u] for u in range(1, self.left_count + 1) if self.pair_left[u] != 0}
