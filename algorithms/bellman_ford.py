from typing import List, Tuple, Optional, Dict

def bellman_ford(
    num_nodes: int,
    edges: List[Tuple[int, int, float]],
    start: int
) -> Tuple[List[float], List[Optional[int]]]:
    """
    Bellman-Ford single-source shortest path algorithm supporting negative edge weights.
    num_nodes: Total 0-indexed vertices (0 to num_nodes - 1).
    edges: List of directed tuples (u, v, weight).
    start: Source vertex.

    Time Complexity: O(V * E)
    Space Complexity: O(V)

    Returns:
        (distances, predecessors) arrays.

    Raises:
        ValueError: If a negative-weight cycle reachable from start is detected.
        IndexError: If start node or edge node is out of bounds.
    """
    if start < 0 or start >= num_nodes:
        raise IndexError(f"Start node {start} out of bounds for num_nodes={num_nodes}.")

    distances = [float('inf')] * num_nodes
    predecessors: List[Optional[int]] = [None] * num_nodes
    distances[start] = 0.0

    # Relax all edges V - 1 times
    for _ in range(num_nodes - 1):
        updated = False
        for u, v, w in edges:
            if u < 0 or u >= num_nodes or v < 0 or v >= num_nodes:
                raise IndexError(f"Edge ({u}, {v}) contains node out of bounds for num_nodes={num_nodes}.")
            
            if distances[u] != float('inf') and distances[u] + w < distances[v]:
                distances[v] = distances[u] + w
                predecessors[v] = u
                updated = True
        if not updated:
            break

    # Check for negative-weight cycles
    for u, v, w in edges:
        if distances[u] != float('inf') and distances[u] + w < distances[v]:
            raise ValueError("Graph contains a negative-weight cycle reachable from the start node.")

    return distances, predecessors


def reconstruct_bellman_ford_path(predecessors: List[Optional[int]], start: int, target: int) -> Optional[List[int]]:
    """
    Reconstructs the shortest path sequence from start to target node using predecessors array.
    Returns list of nodes [start, ..., target] or None if target is unreachable.
    """
    if target < 0 or target >= len(predecessors):
        return None

    if predecessors[target] is None and start != target:
        return None

    path = []
    curr: Optional[int] = target
    visited = set()

    while curr is not None:
        if curr in visited:
            return None  # Cycle prevention
        visited.add(curr)
        path.append(curr)
        if curr == start:
            break
        curr = predecessors[curr]

    if path[-1] != start:
        return None

    path.reverse()
    return path
