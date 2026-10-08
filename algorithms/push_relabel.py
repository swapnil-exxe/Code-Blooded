from collections import deque
from typing import List

class PushRelabelMaxFlow:
    """
    Goldberg-Tarjan Push-Relabel Maximum Flow algorithm with FIFO vertex selection.
    Runs in O(V^3) time.
    """

    def __init__(self, num_vertices: int):
        if num_vertices <= 0:
            raise ValueError("Number of vertices must be positive.")
        self.n = num_vertices
        self.capacity = [[0] * self.n for _ in range(self.n)]
        self.flow = [[0] * self.n for _ in range(self.n)]
        self.adj: List[List[int]] = [[] for _ in range(self.n)]

    def add_edge(self, u: int, v: int, cap: int) -> None:
        """Adds a directed edge from u to v with capacity cap."""
        if not (0 <= u < self.n and 0 <= v < self.n):
            raise IndexError("Vertex index out of bounds.")
        if cap < 0:
            raise ValueError("Edge capacity cannot be negative.")

        if v not in self.adj[u]:
            self.adj[u].append(v)
            self.adj[v].append(u)
        self.capacity[u][v] += cap

    def max_flow(self, source: int, sink: int) -> int:
        """Computes the maximum flow from source to sink."""
        if not (0 <= source < self.n and 0 <= sink < self.n):
            raise IndexError("Source or sink out of bounds.")
        if source == sink:
            raise ValueError("Source and sink must be distinct.")

        # Reset flows
        self.flow = [[0] * self.n for _ in range(self.n)]
        height = [0] * self.n
        excess = [0] * self.n
        in_queue = [False] * self.n
        queue = deque()

        height[source] = self.n

        # Initial preflow push from source
        for v in self.adj[source]:
            cap = self.capacity[source][v]
            if cap > 0:
                self.flow[source][v] = cap
                self.flow[v][source] = -cap
                excess[v] = cap
                excess[source] -= cap
                if v != source and v != sink and not in_queue[v]:
                    queue.append(v)
                    in_queue[v] = True

        def push(u: int, v: int) -> bool:
            residual = self.capacity[u][v] - self.flow[u][v]
            send = min(excess[u], residual)
            if send > 0 and height[u] == height[v] + 1:
                self.flow[u][v] += send
                self.flow[v][u] -= send
                excess[u] -= send
                excess[v] += send
                if v != source and v != sink and not in_queue[v]:
                    queue.append(v)
                    in_queue[v] = True
                return True
            return False

        def relabel(u: int) -> None:
            min_height = float('inf')
            for v in self.adj[u]:
                if self.capacity[u][v] - self.flow[u][v] > 0:
                    min_height = min(min_height, height[v])
            if min_height < float('inf'):
                height[u] = int(min_height) + 1

        while queue:
            u = queue.popleft()
            in_queue[u] = False

            # Discharge vertex u
            pushed_any = True
            while excess[u] > 0:
                pushed = False
                for v in self.adj[u]:
                    if push(u, v):
                        pushed = True
                        if excess[u] == 0:
                            break
                if not pushed:
                    relabel(u)

            if excess[u] > 0 and not in_queue[u]:
                queue.append(u)
                in_queue[u] = True

        return sum(self.flow[source][v] for v in self.adj[source])
