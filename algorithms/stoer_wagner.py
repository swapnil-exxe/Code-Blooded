from typing import List, Tuple, Set, Dict

class StoerWagnerMinCut:
    """
    Deterministic Stoer-Wagner algorithm for computing the global minimum cut
    in an undirected graph with non-negative edge weights in O(V^3) time.
    """

    def __init__(self, num_vertices: int):
        if num_vertices < 2:
            raise ValueError("Graph must contain at least 2 vertices.")
        self.n = num_vertices
        self.adj = [[0.0] * self.n for _ in range(self.n)]

    def add_edge(self, u: int, v: int, weight: float = 1.0) -> None:
        """Adds an undirected edge between u and v with given weight."""
        if not (0 <= u < self.n and 0 <= v < self.n):
            raise IndexError("Vertex index out of bounds.")
        if u == v:
            return  # Self-loops do not affect cuts
        if weight < 0:
            raise ValueError("Edge weight must be non-negative.")

        self.adj[u][v] += weight
        self.adj[v][u] += weight

    def min_cut(self) -> Tuple[float, Set[int], Set[int]]:
        """
        Computes the global minimum cut.
        Returns (min_cut_weight, partition_A, partition_B).
        """
        # Maintain supernodes: initially each node is its own cluster
        clusters: Dict[int, Set[int]] = {i: {i} for i in range(self.n)}
        active_nodes = list(range(self.n))

        # Working copy of adjacency weights
        w = [row[:] for row in self.adj]

        best_cut_weight = float('inf')
        best_cut_partition: Set[int] = set()

        for _ in range(self.n - 1):
            # Phase: Maximum Adjacency Search (MAS)
            in_a = [False] * self.n
            tightness = [0.0] * self.n

            prev = -1
            curr = -1

            for _ in range(len(active_nodes)):
                # Pick vertex not in A with maximum connection weight to A
                best_val = -1.0
                next_node = -1
                for node in active_nodes:
                    if not in_a[node]:
                        if tightness[node] > best_val or next_node == -1:
                            best_val = tightness[node]
                            next_node = node

                prev = curr
                curr = next_node
                in_a[curr] = True

                # Update tightness of remaining nodes
                for node in active_nodes:
                    if not in_a[node]:
                        tightness[node] += w[curr][node]

            # Last added vertex is `curr` (t), second to last is `prev` (s)
            s = prev
            t = curr
            phase_cut_weight = tightness[t]

            if phase_cut_weight < best_cut_weight:
                best_cut_weight = phase_cut_weight
                best_cut_partition = set(clusters[t])

            # Merge t into s
            clusters[s].update(clusters[t])
            for node in active_nodes:
                if node != s and node != t:
                    w[s][node] += w[t][node]
                    w[node][s] += w[node][t]

            active_nodes.remove(t)

        all_vertices = set(range(self.n))
        part_a = best_cut_partition
        part_b = all_vertices - part_a

        return best_cut_weight, part_a, part_b
