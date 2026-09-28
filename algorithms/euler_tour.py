from typing import List, Tuple

class EulerTourTree:
    """
    Euler Tour Technique (Tree Flattening).
    Flattens tree depth-first traversal into linear entry (tin) and exit (tout) timestamps.
    Subtree of node u maps directly to contiguous range [tin[u], tout[u]].
    """

    def __init__(self, num_nodes: int, tree_edges: List[Tuple[int, int]], values: List[int], root: int = 0):
        if num_nodes <= 0:
            raise ValueError("num_nodes must be greater than zero.")
        if len(values) != num_nodes:
            raise ValueError("values length must equal num_nodes.")
        if root < 0 or root >= num_nodes:
            raise IndexError(f"Root {root} out of bounds for num_nodes={num_nodes}.")

        self.n = num_nodes
        self.root = root
        self.node_values = values[:]

        self.adj: List[List[int]] = [[] for _ in range(num_nodes)]
        for u, v in tree_edges:
            if 0 <= u < num_nodes and 0 <= v < num_nodes:
                self.adj[u].append(v)
                self.adj[v].append(u)
            else:
                raise IndexError(f"Edge ({u}, {v}) out of bounds for num_nodes={num_nodes}.")

        self.tin = [0] * num_nodes
        self.tout = [0] * num_nodes
        self.flat_tour: List[int] = []
        self._timer = 0

        self._dfs(root, root)

    def _dfs(self, u: int, p: int) -> None:
        self.tin[u] = self._timer
        self.flat_tour.append(self.node_values[u])
        self._timer += 1

        for v in self.adj[u]:
            if v != p:
                self._dfs(v, u)

        self.tout[u] = self._timer - 1

    def query_subtree_sum(self, u: int) -> int:
        """Returns the sum of node values in the subtree rooted at u in O(tout[u] - tin[u]) time."""
        if not (0 <= u < self.n):
            raise IndexError(f"Node {u} out of bounds.")
        
        start = self.tin[u]
        end = self.tout[u]
        return sum(self.flat_tour[start : end + 1])

    def update_node_val(self, u: int, val: int) -> None:
        """Updates the value of node u."""
        if not (0 <= u < self.n):
            raise IndexError(f"Node {u} out of bounds.")
        self.node_values[u] = val
        self.flat_tour[self.tin[u]] = val
