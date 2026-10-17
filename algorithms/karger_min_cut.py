import math
import random
from typing import List, Tuple, Set, Optional

class _DSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.num_components = n

    def find(self, i: int) -> int:
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i: int, j: int) -> bool:
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i == root_j:
            return False

        if self.rank[root_i] < self.rank[root_j]:
            self.parent[root_i] = root_j
        elif self.rank[root_i] > self.rank[root_j]:
            self.parent[root_j] = root_i
        else:
            self.parent[root_j] = root_i
            self.rank[root_i] += 1

        self.num_components -= 1
        return True


def karger_single_trial(
    num_vertices: int,
    edges: List[Tuple[int, int]]
) -> Tuple[int, Set[int], Set[int]]:
    """
    Executes a single randomized contraction trial of Karger's Min-Cut algorithm.
    Returns (cut_size, partition_A, partition_B).
    """
    if num_vertices < 2:
        raise ValueError("Graph must contain at least 2 vertices.")

    dsu = _DSU(num_vertices)
    edge_list = list(edges)
    random.shuffle(edge_list)

    for u, v in edge_list:
        if dsu.num_components <= 2:
            break
        dsu.union(u, v)

    # Group vertices by their root component
    roots = {dsu.find(i) for i in range(num_vertices)}
    if len(roots) > 2:
        # If the graph was originally disconnected with >2 components,
        # group any root into partition A and the rest into partition B
        root_list = list(roots)
        comp_a_root = root_list[0]
        part_a = {i for i in range(num_vertices) if dsu.find(i) == comp_a_root}
        part_b = {i for i in range(num_vertices) if i not in part_a}
    else:
        root_list = list(roots)
        comp_a_root = root_list[0]
        part_a = {i for i in range(num_vertices) if dsu.find(i) == comp_a_root}
        part_b = {i for i in range(num_vertices) if dsu.find(i) == root_list[1]}

    # Count cut edges crossing the partition
    cut_size = sum(
        1 for u, v in edges
        if (u in part_a and v in part_b) or (u in part_b and v in part_a)
    )

    return cut_size, part_a, part_b


def karger_min_cut(
    num_vertices: int,
    edges: List[Tuple[int, int]],
    trials: Optional[int] = None
) -> Tuple[int, Set[int], Set[int]]:
    """
    Computes global minimum cut by running repeated independent contraction trials.
    Returns (min_cut_size, partition_A, partition_B).
    """
    if num_vertices < 2:
        raise ValueError("Graph must contain at least 2 vertices.")
    if not edges:
        # 0 edges: min cut is 0
        part_a = {0}
        part_b = set(range(1, num_vertices))
        return 0, part_a, part_b

    for u, v in edges:
        if not (0 <= u < num_vertices and 0 <= v < num_vertices):
            raise IndexError("Vertex index out of bounds.")

    if trials is None:
        # Standard amplification: O(V^2 * ln(V)) bounded for practical execution
        theoretical = int(math.ceil((num_vertices ** 2) * math.log(max(2, num_vertices)) / 2))
        trials = min(150, max(20, theoretical))

    best_cut = float('inf')
    best_part_a: Set[int] = set()
    best_part_b: Set[int] = set()

    for _ in range(trials):
        cut_size, part_a, part_b = karger_single_trial(num_vertices, edges)
        if cut_size < best_cut:
            best_cut = cut_size
            best_part_a = part_a
            best_part_b = part_b
            if best_cut == 0:
                break  # Cannot get lower than 0 cut

    return int(best_cut), best_part_a, best_part_b
