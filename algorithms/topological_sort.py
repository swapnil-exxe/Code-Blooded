from collections import deque
from typing import List, Tuple

def topological_sort_kahn(num_nodes: int, edges: List[Tuple[int, int]]) -> List[int]:
    """
    Topological Sort using Kahn's algorithm (BFS in-degree reduction).
    Nodes are 0-indexed integers from 0 to num_nodes - 1.
    edges is a list of directed tuples (u, v) representing edge u -> v.
    Returns a valid topological ordering of nodes in O(V + E) time.
    Raises ValueError if a cycle is detected in the directed graph.
    """
    if num_nodes <= 0:
        return []

    in_degree = [0] * num_nodes
    adj = [[] for _ in range(num_nodes)]

    for u, v in edges:
        if 0 <= u < num_nodes and 0 <= v < num_nodes:
            adj[u].append(v)
            in_degree[v] += 1
        else:
            raise IndexError(f"Edge ({u}, {v}) contains node out of bounds for num_nodes={num_nodes}.")

    queue = deque([node for node in range(num_nodes) if in_degree[node] == 0])
    topo_order = []

    while queue:
        u = queue.popleft()
        topo_order.append(u)

        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    if len(topo_order) != num_nodes:
        raise ValueError("Cycle detected in directed graph; topological sort impossible.")

    return topo_order


def topological_sort_dfs(num_nodes: int, edges: List[Tuple[int, int]]) -> List[int]:
    """
    Topological Sort using Depth First Search (DFS) with 3-state cycle detection.
    State 0 = Unvisited, 1 = Visiting (in current recursion stack), 2 = Visited.
    Returns a valid topological ordering in O(V + E) time.
    Raises ValueError if a cycle is detected.
    """
    if num_nodes <= 0:
        return []

    adj = [[] for _ in range(num_nodes)]
    for u, v in edges:
        if 0 <= u < num_nodes and 0 <= v < num_nodes:
            adj[u].append(v)
        else:
            raise IndexError(f"Edge ({u}, {v}) contains node out of bounds for num_nodes={num_nodes}.")

    state = [0] * num_nodes
    stack = []

    def dfs(node: int) -> bool:
        state[node] = 1  # Visiting
        for neighbor in adj[node]:
            if state[neighbor] == 1:
                return False  # Cycle detected
            if state[neighbor] == 0:
                if not dfs(neighbor):
                    return False
        state[node] = 2  # Visited
        stack.append(node)
        return True

    for i in range(num_nodes):
        if state[i] == 0:
            if not dfs(i):
                raise ValueError("Cycle detected in directed graph; topological sort impossible.")

    stack.reverse()
    return stack
