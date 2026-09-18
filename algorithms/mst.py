import heapq
from typing import List, Tuple
from algorithms.disjoint_set import DisjointSet

def kruskal_mst(num_nodes: int, edges: List[Tuple[int, int, float]]) -> Tuple[float, List[Tuple[int, int, float]]]:
    """
    Kruskal's Minimum Spanning Tree (MST) algorithm using Union-Find (DisjointSet).
    num_nodes: Total 0-indexed vertices (0 to num_nodes - 1).
    edges: List of undirected tuples (u, v, weight).

    Time Complexity: O(E log E)
    Returns: (total_weight, list_of_mst_edges)
    Raises: ValueError if graph is disconnected or num_nodes <= 0.
    """
    if num_nodes <= 0:
        return 0.0, []

    if num_nodes == 1:
        return 0.0, []

    sorted_edges = sorted(edges, key=lambda edge: edge[2])
    dsu = DisjointSet(num_nodes)
    mst_edges = []
    total_weight = 0.0

    for u, v, w in sorted_edges:
        if 0 <= u < num_nodes and 0 <= v < num_nodes:
            if dsu.union(u, v):
                mst_edges.append((u, v, w))
                total_weight += w
                if len(mst_edges) == num_nodes - 1:
                    break
        else:
            raise IndexError(f"Edge ({u}, {v}) out of bounds for num_nodes={num_nodes}.")

    if len(mst_edges) != num_nodes - 1:
        raise ValueError("Graph is disconnected; Minimum Spanning Tree does not exist.")

    return total_weight, mst_edges


def prim_mst(num_nodes: int, edges: List[Tuple[int, int, float]]) -> Tuple[float, List[Tuple[int, int, float]]]:
    """
    Prim's Minimum Spanning Tree (MST) algorithm using binary min-heap priority queue.
    num_nodes: Total 0-indexed vertices (0 to num_nodes - 1).
    edges: List of undirected tuples (u, v, weight).

    Time Complexity: O(E log V)
    Returns: (total_weight, list_of_mst_edges)
    Raises: ValueError if graph is disconnected or num_nodes <= 0.
    """
    if num_nodes <= 0 or num_nodes == 1:
        return 0.0, []

    adj = [[] for _ in range(num_nodes)]
    for u, v, w in edges:
        if 0 <= u < num_nodes and 0 <= v < num_nodes:
            adj[u].append((v, w))
            adj[v].append((u, w))
        else:
            raise IndexError(f"Edge ({u}, {v}) out of bounds for num_nodes={num_nodes}.")

    visited = [False] * num_nodes
    min_heap = [(0.0, 0, -1)]  # (weight, node, parent)
    total_weight = 0.0
    mst_edges = []

    while min_heap and len(mst_edges) < num_nodes:
        w, u, p = heapq.heappop(min_heap)

        if visited[u]:
            continue

        visited[u] = True
        total_weight += w
        if p != -1:
            mst_edges.append((p, u, w))

        for neighbor, weight in adj[u]:
            if not visited[neighbor]:
                heapq.heappush(min_heap, (weight, neighbor, u))

    if sum(visited) != num_nodes:
        raise ValueError("Graph is disconnected; Minimum Spanning Tree does not exist.")

    return total_weight, mst_edges
