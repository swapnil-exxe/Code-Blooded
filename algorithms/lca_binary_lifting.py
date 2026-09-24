import math
from typing import List, Tuple, Optional

class LCABinaryLifting:
    """
    Lowest Common Ancestor (LCA) data structure using binary lifting (sparse table) on tree structures.
    Preprocessing Time: O(N log N)
    LCA Query Time: O(log N)
    Distance Query Time: O(log N)
    """

    def __init__(self, num_nodes: int, edges: List[Tuple[int, int]], root: int = 0):
        if num_nodes <= 0:
            raise ValueError("num_nodes must be greater than zero.")
        if root < 0 or root >= num_nodes:
            raise IndexError(f"Root {root} out of bounds for num_nodes={num_nodes}.")

        self.num_nodes = num_nodes
        self.root = root
        self.log_n = math.ceil(math.log2(num_nodes)) + 1

        self.adj: List[List[int]] = [[] for _ in range(num_nodes)]
        for u, v in edges:
            if 0 <= u < num_nodes and 0 <= v < num_nodes:
                self.adj[u].append(v)
                self.adj[v].append(u)
            else:
                raise IndexError(f"Edge ({u}, {v}) out of bounds for num_nodes={num_nodes}.")

        self.depth = [0] * num_nodes
        self.up = [[root] * self.log_n for _ in range(num_nodes)]

        self._dfs(root, root)

    def _dfs(self, u: int, p: int) -> None:
        self.up[u][0] = p
        for j in range(1, self.log_n):
            self.up[u][j] = self.up[self.up[u][j - 1]][j - 1]

        for v in self.adj[u]:
            if v != p:
                self.depth[v] = self.depth[u] + 1
                self._dfs(v, u)

    def query_lca(self, u: int, v: int) -> int:
        """Returns the lowest common ancestor of node u and node v in O(log N) time."""
        if not (0 <= u < self.num_nodes and 0 <= v < self.num_nodes):
            raise IndexError(f"Node query ({u}, {v}) out of bounds for num_nodes={self.num_nodes}.")

        if self.depth[u] < self.depth[v]:
            u, v = v, u

        # Bring u and v to same depth
        diff = self.depth[u] - self.depth[v]
        for j in range(self.log_n):
            if (diff >> j) & 1:
                u = self.up[u][j]

        if u == v:
            return u

        # Lift both u and v simultaneously
        for j in range(self.log_n - 1, -1, -1):
            if self.up[u][j] != self.up[v][j]:
                u = self.up[u][j]
                v = self.up[v][j]

        return self.up[u][0]

    def get_distance(self, u: int, v: int) -> int:
        """Returns tree edge distance between node u and node v in O(log N) time."""
        lca = self.query_lca(u, v)
        return self.depth[u] + self.depth[v] - 2 * self.depth[lca]
