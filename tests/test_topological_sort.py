import pytest
from algorithms.topological_sort import topological_sort_kahn, topological_sort_dfs

def is_valid_topo_order(num_nodes, edges, order):
    if len(order) != num_nodes:
        return False
    pos = {node: i for i, node in enumerate(order)}
    for u, v in edges:
        if pos[u] >= pos[v]:
            return False
    return True

def test_topological_sort_dag_kahn_and_dfs():
    num_nodes = 6
    edges = [(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)]
    
    kahn_order = topological_sort_kahn(num_nodes, edges)
    assert is_valid_topo_order(num_nodes, edges, kahn_order)

    dfs_order = topological_sort_dfs(num_nodes, edges)
    assert is_valid_topo_order(num_nodes, edges, dfs_order)

def test_topological_sort_cycle_detection():
    num_nodes = 4
    cycle_edges = [(0, 1), (1, 2), (2, 3), (3, 1)]

    with pytest.raises(ValueError, match="Cycle detected"):
        topological_sort_kahn(num_nodes, cycle_edges)

    with pytest.raises(ValueError, match="Cycle detected"):
        topological_sort_dfs(num_nodes, cycle_edges)

def test_topological_sort_disconnected_components():
    num_nodes = 4
    edges = [(0, 1), (2, 3)]

    kahn_order = topological_sort_kahn(num_nodes, edges)
    assert is_valid_topo_order(num_nodes, edges, kahn_order)

    dfs_order = topological_sort_dfs(num_nodes, edges)
    assert is_valid_topo_order(num_nodes, edges, dfs_order)

def test_topological_sort_empty_and_out_of_bounds():
    assert topological_sort_kahn(0, []) == []
    assert topological_sort_dfs(0, []) == []

    with pytest.raises(IndexError):
        topological_sort_kahn(3, [(0, 5)])
