from collections import deque
from typing import List, Tuple

def zero_one_bfs(num_vertices: int, adj: List[List[Tuple[int, int]]], source: int) -> List[float]:
    """
    0-1 BFS for single-source shortest paths on graphs with edge weights in {0, 1}.
    Runs in linear O(V + E) time using a double-ended queue (deque).
    """
    if num_vertices <= 0:
        raise ValueError("Number of vertices must be positive.")
    if not (0 <= source < num_vertices):
        raise IndexError("Source vertex out of bounds.")

    dist = [float('inf')] * num_vertices
    dist[source] = 0
    q = deque([source])

    while q:
        u = q.popleft()
        d_u = dist[u]

        for v, weight in adj[u]:
            if weight not in (0, 1):
                raise ValueError("Edge weight must be 0 or 1 for 0-1 BFS.")

            if d_u + weight < dist[v]:
                dist[v] = d_u + weight
                if weight == 0:
                    q.appendleft(v)
                else:
                    q.append(v)

    return dist


def dial_shortest_path(
    num_vertices: int,
    adj: List[List[Tuple[int, int]]],
    source: int,
    max_weight: int
) -> List[float]:
    """
    Dial's Algorithm (Bucket Queue Dijkstra) for single-source shortest paths
    where all edge weights are non-negative integers bounded by max_weight (W).
    Runs in O(V * W + E) time.
    """
    if num_vertices <= 0:
        raise ValueError("Number of vertices must be positive.")
    if max_weight <= 0:
        raise ValueError("max_weight must be positive.")
    if not (0 <= source < num_vertices):
        raise IndexError("Source vertex out of bounds.")

    dist = [float('inf')] * num_vertices
    dist[source] = 0

    # Buckets indexed by distance modulo (max_weight + 1)
    bucket_count = max_weight + 1
    buckets: List[List[int]] = [[] for _ in range(bucket_count)]
    buckets[0].append(source)

    num_elements = 1
    idx = 0

    while num_elements > 0:
        while not buckets[idx % bucket_count]:
            idx += 1

        u = buckets[idx % bucket_count].pop()
        num_elements -= 1

        if dist[u] < idx:
            continue

        for v, weight in adj[u]:
            if not (0 <= weight <= max_weight):
                raise ValueError(f"Edge weight must be in range [0, {max_weight}].")

            new_dist = int(dist[u]) + weight
            if new_dist < dist[v]:
                dist[v] = new_dist
                buckets[new_dist % bucket_count].append(v)
                num_elements += 1

    return dist
