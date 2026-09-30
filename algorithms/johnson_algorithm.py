import heapq
from typing import List, Tuple, Dict, Optional
from algorithms.bellman_ford import bellman_ford

def johnson_all_pairs_shortest_paths(
    num_nodes: int,
    edges: List[Tuple[int, int, float]]
) -> List[List[float]]:
    """
    Johnson's All-Pairs Shortest Paths algorithm for sparse directed graphs with arbitrary edge weights.
    1. Creates dummy vertex node N connected to all nodes with 0-weight edges.
    2. Runs Bellman-Ford from dummy node to calculate vertex potentials h[u].
    3. Reweights all edges: w'(u, v) = w(u, v) + h[u] - h[v] >= 0.
    4. Runs Dijkstra from each node using reweighted non-negative edge weights.
    5. Converts distances back: dist(u, v) = dist'(u, v) - h[u] + h[v].

    Time Complexity: O(V^2 log V + V * E)
    Space Complexity: O(V^2 + E)

    Returns: V x V distance matrix.
    Raises: ValueError if a negative-weight cycle exists.
    """
    if num_nodes <= 0:
        return []

    # Step 1: Add dummy vertex N connected to all vertices (0..N-1) with 0-weight edges
    dummy_node = num_nodes
    augmented_edges = edges[:]
    for u in range(num_nodes):
        augmented_edges.append((dummy_node, u, 0.0))

    # Step 2: Run Bellman-Ford to get vertex potentials h
    try:
        potentials, _ = bellman_ford(num_nodes + 1, augmented_edges, start=dummy_node)
    except ValueError:
        raise ValueError("Graph contains a negative-weight cycle; Johnson's algorithm cannot compute shortest paths.")

    # Slice potentials for original nodes 0..N-1
    h = potentials[:num_nodes]

    # Step 3: Reweight edges & construct adjacency list
    adj: List[List[Tuple[int, float]]] = [[] for _ in range(num_nodes)]
    for u, v, w in edges:
        if 0 <= u < num_nodes and 0 <= v < num_nodes:
            reweighted_w = w + h[u] - h[v]
            adj[u].append((v, reweighted_w))
        else:
            raise IndexError(f"Edge ({u}, {v}) out of bounds for num_nodes={num_nodes}.")

    # Step 4: Run Dijkstra from each node using reweighted edges
    all_pairs_dist = [[float('inf')] * num_nodes for _ in range(num_nodes)]

    for src in range(num_nodes):
        d_reweighted = [float('inf')] * num_nodes
        d_reweighted[src] = 0.0
        min_heap = [(0.0, src)]

        while min_heap:
            d_curr, u = heapq.heappop(min_heap)

            if d_curr > d_reweighted[u]:
                continue

            for v, w_prime in adj[u]:
                if d_reweighted[u] + w_prime < d_reweighted[v]:
                    d_reweighted[v] = d_reweighted[u] + w_prime
                    heapq.heappush(min_heap, (d_reweighted[v], v))

        # Step 5: Restore true distances
        for dst in range(num_nodes):
            if d_reweighted[dst] != float('inf'):
                all_pairs_dist[src][dst] = d_reweighted[dst] - h[src] + h[dst]

    return all_pairs_dist
