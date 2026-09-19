from typing import List, Tuple

def tarjan_scc(num_nodes: int, edges: List[Tuple[int, int]]) -> List[List[int]]:
    """
    Tarjan's algorithm for finding Strongly Connected Components (SCCs) in a directed graph.
    num_nodes: Total 0-indexed vertices (0 to num_nodes - 1).
    edges: List of directed tuples (u, v).

    Time Complexity: O(V + E)
    Space Complexity: O(V + E)

    Returns: List of SCCs, where each SCC is a list of node indices.
    """
    if num_nodes <= 0:
        return []

    adj = [[] for _ in range(num_nodes)]
    for u, v in edges:
        if 0 <= u < num_nodes and 0 <= v < num_nodes:
            adj[u].append(v)
        else:
            raise IndexError(f"Edge ({u}, {v}) out of bounds for num_nodes={num_nodes}.")

    timer = 0
    discovery = [-1] * num_nodes
    low = [-1] * num_nodes
    on_stack = [False] * num_nodes
    stack = []
    sccs = []

    def dfs(u: int) -> None:
        nonlocal timer
        discovery[u] = low[u] = timer
        timer += 1
        stack.append(u)
        on_stack[u] = True

        for v in adj[u]:
            if discovery[v] == -1:
                dfs(v)
                low[u] = min(low[u], low[v])
            elif on_stack[v]:
                low[u] = min(low[u], discovery[v])

        if low[u] == discovery[u]:
            scc = []
            while True:
                node = stack.pop()
                on_stack[node] = False
                scc.append(node)
                if node == u:
                    break
            sccs.append(scc)

    for i in range(num_nodes):
        if discovery[i] == -1:
            dfs(i)

    return sccs
