from typing import List, Tuple, Set, Dict

class BridgeArticulationFinder:
    """
    Finds all bridges (cut edges) and articulation points (cut vertices)
    in an undirected graph in O(V + E) time using Tarjan's DFS algorithm.
    """

    def __init__(self, num_vertices: int):
        if num_vertices < 0:
            raise ValueError("Number of vertices cannot be negative.")
        self.num_vertices = num_vertices
        self.adj: Dict[int, List[Tuple[int, int]]] = {i: [] for i in range(num_vertices)}
        self._edge_id = 0

    def add_edge(self, u: int, v: int) -> None:
        """Adds an undirected edge between u and v."""
        if not (0 <= u < self.num_vertices and 0 <= v < self.num_vertices):
            raise IndexError("Vertex index out of bounds.")
        edge_idx = self._edge_id
        self._edge_id += 1
        self.adj[u].append((v, edge_idx))
        self.adj[v].append((u, edge_idx))

    def analyze(self) -> Tuple[List[Tuple[int, int]], Set[int]]:
        """
        Computes and returns (bridges, articulation_points).
        Bridges are returned as sorted tuples (min(u, v), max(u, v)).
        """
        disc = [-1] * self.num_vertices
        low = [-1] * self.num_vertices
        articulation_points: Set[int] = set()
        bridges: List[Tuple[int, int]] = []
        timer = 0

        def dfs(u: int, parent_edge_id: int = -1):
            nonlocal timer
            disc[u] = low[u] = timer
            timer += 1
            children = 0

            for v, edge_id in self.adj[u]:
                if edge_id == parent_edge_id:
                    continue  # Do not traverse back along the same edge

                if disc[v] != -1:
                    # Back-edge
                    low[u] = min(low[u], disc[v])
                else:
                    # Forward tree-edge
                    children += 1
                    dfs(v, edge_id)
                    low[u] = min(low[u], low[v])

                    # Bridge condition
                    if low[v] > disc[u]:
                        bridges.append((min(u, v), max(u, v)))

                    # Articulation point condition (non-root)
                    if parent_edge_id != -1 and low[v] >= disc[u]:
                        articulation_points.add(u)

            # Articulation point condition (root)
            if parent_edge_id == -1 and children > 1:
                articulation_points.add(u)

        for i in range(self.num_vertices):
            if disc[i] == -1:
                dfs(i)

        bridges.sort()
        return bridges, articulation_points
