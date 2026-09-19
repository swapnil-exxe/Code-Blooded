from collections import deque
from typing import List, Tuple

def edmonds_karp(
    num_nodes: int,
    capacity_edges: List[Tuple[int, int, float]],
    source: int,
    sink: int
) -> Tuple[float, List[List[float]]]:
    """
    Edmonds-Karp algorithm for computing maximum network flow using BFS augmenting paths.
    num_nodes: Total 0-indexed vertices (0 to num_nodes - 1).
    capacity_edges: List of directed tuples (u, v, capacity).
    source: Source vertex index.
    sink: Sink vertex index.

    Time Complexity: O(V * E^2)
    Space Complexity: O(V^2)

    Returns: (max_flow_value, residual_capacity_matrix)
    Raises: ValueError if capacity is negative or source == sink.
    IndexError if node indices are out of bounds.
    """
    if source < 0 or source >= num_nodes or sink < 0 or sink >= num_nodes:
        raise IndexError(f"Source {source} or Sink {sink} out of bounds for num_nodes={num_nodes}.")

    if source == sink:
        raise ValueError("Source and Sink cannot be the same node.")

    residual = [[0.0] * num_nodes for _ in range(num_nodes)]
    for u, v, cap in capacity_edges:
        if 0 <= u < num_nodes and 0 <= v < num_nodes:
            if cap < 0:
                raise ValueError(f"Negative capacity ({cap}) on edge ({u} -> {v}) not allowed.")
            residual[u][v] += cap
        else:
            raise IndexError(f"Edge ({u}, {v}) out of bounds for num_nodes={num_nodes}.")

    max_flow = 0.0

    while True:
        parent = [-1] * num_nodes
        parent[source] = source
        queue = deque([source])

        while queue and parent[sink] == -1:
            curr = queue.popleft()
            for nxt in range(num_nodes):
                if parent[nxt] == -1 and residual[curr][nxt] > 1e-9:
                    parent[nxt] = curr
                    queue.append(nxt)

        if parent[sink] == -1:
            break  # No more augmenting paths

        # Find bottleneck capacity along augmenting path
        path_flow = float('inf')
        curr = sink
        while curr != source:
            prev = parent[curr]
            path_flow = min(path_flow, residual[prev][curr])
            curr = prev

        # Update residual capacities
        curr = sink
        while curr != source:
            prev = parent[curr]
            residual[prev][curr] -= path_flow
            residual[curr][prev] += path_flow
            curr = prev

        max_flow += path_flow

    return max_flow, residual
