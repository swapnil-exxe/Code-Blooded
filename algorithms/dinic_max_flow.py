from collections import deque
from typing import List

class Edge:
    def __init__(self, u: int, v: int, cap: float, rev_idx: int):
        self.u = u
        self.v = v
        self.cap = cap
        self.flow = 0.0
        self.rev_idx = rev_idx

class DinicMaxFlow:
    """
    Dinic's Maximum Flow algorithm using level graph (BFS) and blocking flow (DFS).
    Time Complexity: O(V^2 * E) general, O(E * sqrt(V)) unit network.
    Space Complexity: O(V + E)
    """

    def __init__(self, num_nodes: int):
        if num_nodes <= 0:
            raise ValueError("num_nodes must be greater than zero.")
        self.n = num_nodes
        self.graph: List[List[Edge]] = [[] for _ in range(num_nodes)]

    def add_edge(self, u: int, v: int, cap: float) -> None:
        """Adds a directed edge u -> v with non-negative capacity cap."""
        if not (0 <= u < self.n and 0 <= v < self.n):
            raise IndexError(f"Edge ({u}, {v}) out of bounds for num_nodes={self.n}.")
        if cap < 0:
            raise ValueError(f"Negative edge capacity {cap} not allowed.")

        e1 = Edge(u, v, cap, len(self.graph[v]))
        e2 = Edge(v, u, 0.0, len(self.graph[u]))
        self.graph[u].append(e1)
        self.graph[v].append(e2)

    def _bfs_level_graph(self, s: int, t: int, level: List[int]) -> bool:
        for i in range(self.n):
            level[i] = -1

        level[s] = 0
        queue = deque([s])

        while queue:
            u = queue.popleft()
            for edge in self.graph[u]:
                if edge.cap - edge.flow > 1e-9 and level[edge.v] == -1:
                    level[edge.v] = level[u] + 1
                    queue.append(edge.v)

        return level[t] != -1

    def _dfs_blocking_flow(self, u: int, t: int, pushed: float, level: List[int], ptr: List[int]) -> float:
        if pushed <= 0 or u == t:
            return pushed

        for i in range(ptr[u], len(self.graph[u])):
            ptr[u] = i
            edge = self.graph[u][i]
            tr = edge.v

            if level[u] + 1 != level[tr] or edge.cap - edge.flow <= 1e-9:
                continue

            tr_pushed = self._dfs_blocking_flow(
                tr, t, min(pushed, edge.cap - edge.flow), level, ptr
            )

            if tr_pushed <= 0:
                continue

            edge.flow += tr_pushed
            self.graph[tr][edge.rev_idx].flow -= tr_pushed
            return tr_pushed

        return 0.0

    def max_flow(self, s: int, t: int) -> float:
        """Computes the maximum flow from source s to sink t."""
        if not (0 <= s < self.n and 0 <= t < self.n):
            raise IndexError(f"Source {s} or Sink {t} out of bounds for num_nodes={self.n}.")
        if s == t:
            raise ValueError("Source and Sink cannot be the same node.")

        flow = 0.0
        level = [-1] * self.n

        while self._bfs_level_graph(s, t, level):
            ptr = [0] * self.n
            while True:
                pushed = self._dfs_blocking_flow(s, t, float('inf'), level, ptr)
                if pushed <= 0:
                    break
                flow += pushed

        return flow
