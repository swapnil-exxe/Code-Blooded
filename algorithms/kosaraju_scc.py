from typing import List, Tuple

def kosaraju_scc(num_nodes: int, edges: List[Tuple[int, int]]) -> List[List[int]]:
    """
    Kosaraju's algorithm for finding Strongly Connected Components (SCCs) using 2-pass DFS.
    num_nodes: Total 0-indexed vertices (0 to num_nodes - 1).
    edges: List of directed tuples (u, v).

    Time Complexity: O(V + E)
    Space Complexity: O(V + E)

    Returns: List of SCCs, where each SCC is a list of node indices.
    """
    if num_nodes <= 0:
        return []

    adj = [[] for _ in range(num_nodes)]
    adj_rev = [[] for _ in range(num_nodes)]

    for u, v in edges:
        if 0 <= u < num_nodes and 0 <= v < num_nodes:
            adj[u].append(v)
            adj_rev[v].append(u)
        else:
            raise IndexError(f"Edge ({u}, {v}) out of bounds for num_nodes={num_nodes}.")

    # Pass 1: Fill vertices in stack according to their finishing times
    visited = [False] * num_nodes
    stack = []

    def dfs1(u: int) -> None:
        visited[u] = True
        for v in adj[u]:
            if not visited[v]:
                dfs1(v)
        stack.append(u)

    for i in range(num_nodes):
        if not visited[i]:
            dfs1(i)

    # Pass 2: Process all vertices in order defined by stack on reversed graph
    visited = [False] * num_nodes
    sccs = []

    def dfs2(u: int, current_scc: List[int]) -> None:
        visited[u] = True
        current_scc.append(u)
        for v in adj_rev[u]:
            if not visited[v]:
                dfs2(v, current_scc)

    while stack:
        u = stack.pop()
        if not visited[u]:
            component = []
            dfs2(u, component)
            sccs.append(component)

    return sccs
