from typing import List, Tuple, Optional

def floyd_warshall(
    num_nodes: int,
    graph_matrix: List[List[float]]
) -> Tuple[List[List[float]], List[List[Optional[int]]]]:
    """
    Floyd-Warshall all-pairs shortest path algorithm.
    graph_matrix[i][j] contains edge weight from node i to node j (inf if no direct edge).
    graph_matrix[i][i] should be 0.0.

    Time Complexity: O(V^3)
    Space Complexity: O(V^2)

    Returns: (dist_matrix, next_matrix) where next_matrix helps reconstruct paths.
    Raises: ValueError if a negative-weight cycle exists.
    """
    if num_nodes <= 0:
        return [], []

    dist = [row[:] for row in graph_matrix]
    next_node: List[List[Optional[int]]] = [
        [j if graph_matrix[i][j] != float('inf') and i != j else None for j in range(num_nodes)]
        for i in range(num_nodes)
    ]

    for k in range(num_nodes):
        for i in range(num_nodes):
            for j in range(num_nodes):
                if dist[i][k] != float('inf') and dist[k][j] != float('inf'):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        next_node[i][j] = next_node[i][k]

    # Negative cycle check
    for i in range(num_nodes):
        if dist[i][i] < 0:
            raise ValueError(f"Negative-weight cycle detected at node {i}.")

    return dist, next_node


def reconstruct_fw_path(
    next_node: List[List[Optional[int]]],
    u: int,
    v: int
) -> Optional[List[int]]:
    """
    Reconstructs the shortest path sequence from u to v using next_node matrix.
    Returns list [u, ..., v] or None if v is unreachable from u.
    """
    if u < 0 or u >= len(next_node) or v < 0 or v >= len(next_node):
        return None

    if next_node[u][v] is None and u != v:
        return None

    if u == v:
        return [u]

    path = [u]
    curr = u
    visited = set()

    while curr != v:
        if curr in visited:
            return None  # Cycle safety
        visited.add(curr)
        nxt = next_node[curr][v]
        if nxt is None:
            return None
        path.append(nxt)
        curr = nxt

    return path
