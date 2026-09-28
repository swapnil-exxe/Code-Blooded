from collections import deque
from typing import List, Tuple

class MCMFEdge:
    def __init__(self, u: int, v: int, cap: float, cost: float, rev_idx: int):
        self.u = u
        self.v = v
        self.cap = cap
        self.flow = 0.0
        self.cost = cost
        self.rev_idx = rev_idx

class MinCostMaxFlow:
    """
    Minimum Cost Maximum Flow (MCMF) using SPFA (Shortest Path Faster Algorithm) / Bellman-Ford
    successive shortest path augmentation on residual graph.
    """

    def __init__(self, num_nodes: int):
        if num_nodes <= 0:
            raise ValueError("num_nodes must be greater than zero.")
        self.n = num_nodes
        self.graph: List[List[MCMFEdge]] = [[] for _ in range(num_nodes)]

    def add_edge(self, u: int, v: int, cap: float, cost: float) -> None:
        """Adds a directed edge from u to v with capacity cap and per-unit cost."""
        if not (0 <= u < self.n and 0 <= v < self.n):
            raise IndexError(f"Edge ({u}, {v}) out of bounds for num_nodes={self.n}.")
        if cap < 0:
            raise ValueError("Edge capacity cannot be negative.")

        e1 = MCMFEdge(u, v, cap, cost, len(self.graph[v]))
        e2 = MCMFEdge(v, u, 0.0, -cost, len(self.graph[u]))
        self.graph[u].append(e1)
        self.graph[v].append(e2)

    def _spfa(self, s: int, t: int, dist: List[float], parent_edge: List[Tuple[int, int]]) -> bool:
        for i in range(self.n):
            dist[i] = float('inf')

        in_queue = [False] * self.n
        queue = deque([s])
        dist[s] = 0.0
        in_queue[s] = True

        while queue:
            u = queue.popleft()
            in_queue[u] = False

            for idx, edge in enumerate(self.graph[u]):
                if edge.cap - edge.flow > 1e-9 and dist[u] + edge.cost < dist[edge.v]:
                    dist[edge.v] = dist[u] + edge.cost
                    parent_edge[edge.v] = (u, idx)
                    if not in_queue[edge.v]:
                        queue.append(edge.v)
                        in_queue[edge.v] = True

        return dist[t] != float('inf')

    def min_cost_max_flow(self, s: int, t: int) -> Tuple[float, float]:
        """Returns tuple (max_flow, min_cost) from source s to sink t."""
        if not (0 <= s < self.n and 0 <= t < self.n):
            raise IndexError(f"Source {s} or Sink {t} out of bounds for num_nodes={self.n}.")
        if s == t:
            raise ValueError("Source and Sink cannot be the same node.")

        max_flow = 0.0
        min_cost = 0.0
        dist = [0.0] * self.n
        parent_edge: List[Tuple[int, int]] = [(-1, -1)] * self.n

        while self._spfa(s, t, dist, parent_edge):
            # Find bottleneck capacity along shortest cost augmenting path
            push_flow = float('inf')
            curr = t
            while curr != s:
                p_node, p_idx = parent_edge[curr]
                edge = self.graph[p_node][p_idx]
                push_flow = min(push_flow, edge.cap - edge.flow)
                curr = p_node

            # Augment flow along path
            curr = t
            while curr != s:
                p_node, p_idx = parent_edge[curr]
                edge = self.graph[p_node][p_idx]
                edge.flow += push_flow
                self.graph[curr][edge.rev_idx].flow -= push_flow
                min_cost += push_flow * edge.cost
                curr = p_node

            max_flow += push_flow

        return max_flow, min_cost
