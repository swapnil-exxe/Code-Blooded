from typing import List, Tuple

class HeavyLightDecomposition:
    """
    Heavy-Light Decomposition (HLD) on trees.
    Decomposes tree paths into O(log N) heavy chains, enabling O(log^2 N) path range queries
    and node updates.
    """

    def __init__(self, num_nodes: int, edges: List[Tuple[int, int]], values: List[int], root: int = 0):
        if num_nodes <= 0:
            raise ValueError("num_nodes must be greater than zero.")
        if len(values) != num_nodes:
            raise ValueError("values length must equal num_nodes.")

        self.n = num_nodes
        self.root = root
        self.node_values = values[:]

        self.adj: List[List[int]] = [[] for _ in range(num_nodes)]
        for u, v in edges:
            if 0 <= u < num_nodes and 0 <= v < num_nodes:
                self.adj[u].append(v)
                self.adj[v].append(u)
            else:
                raise IndexError(f"Edge ({u}, {v}) out of bounds for num_nodes={num_nodes}.")

        self.parent = [0] * num_nodes
        self.depth = [0] * num_nodes
        self.heavy = [-1] * num_nodes
        self.head = [0] * num_nodes
        self.pos = [0] * num_nodes

        self._cur_pos = 0

        # Step 1: DFS to calculate subtree sizes, depths, and heavy edges
        self._dfs_tree(root, root, 0)

        # Step 2: DFS to decompose into heavy chains and assign linear positions
        self._dfs_hld(root, root)

        # Flat array corresponding to linear HLD positions
        self.flat_array = [0] * num_nodes
        for i in range(num_nodes):
            self.flat_array[self.pos[i]] = self.node_values[i]

    def _dfs_tree(self, u: int, p: int, d: int) -> int:
        self.parent[u] = p
        self.depth[u] = d
        size = 1
        max_c_size = 0

        for v in self.adj[u]:
            if v != p:
                c_size = self._dfs_tree(v, u, d + 1)
                size += c_size
                if c_size > max_c_size:
                    max_c_size = c_size
                    self.heavy[u] = v

        return size

    def _dfs_hld(self, u: int, h: int) -> None:
        self.head[u] = h
        self.pos[u] = self._cur_pos
        self._cur_pos += 1

        if self.heavy[u] != -1:
            self._dfs_hld(self.heavy[u], h)

        for v in self.adj[u]:
            if v != self.parent[u] and v != self.heavy[u]:
                self._dfs_hld(v, v)

    def query_path_max(self, u: int, v: int) -> int:
        """Returns the maximum node value along the simple path between u and v in O(log^2 N) time."""
        res = float('-inf')

        while self.head[u] != self.head[v]:
            if self.depth[self.head[u]] < self.depth[self.head[v]]:
                u, v = v, u

            # Query range in flat_array for heavy chain from head[u] to u
            l = self.pos[self.head[u]]
            r = self.pos[u]
            res = max(res, max(self.flat_array[l:r + 1]))
            u = self.parent[self.head[u]]

        if self.depth[u] > self.depth[v]:
            u, v = v, u

        l = self.pos[u]
        r = self.pos[v]
        res = max(res, max(self.flat_array[l:r + 1]))
        return int(res)

    def update_node(self, u: int, val: int) -> None:
        """Updates the value of node u in O(1) time."""
        if not (0 <= u < self.n):
            raise IndexError(f"Node {u} out of bounds.")
        self.node_values[u] = val
        self.flat_array[self.pos[u]] = val
