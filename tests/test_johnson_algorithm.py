import pytest
from algorithms.johnson_algorithm import johnson_all_pairs_shortest_paths

def test_johnson_algorithm_sparse_graph_with_negatives():
    num_nodes = 4
    inf = float('inf')
    edges = [
        (0, 1, -2.0),
        (1, 2, -1.0),
        (2, 0, 4.0),
        (0, 3, 3.0),
        (2, 3, 2.0)
    ]

    dist = johnson_all_pairs_shortest_paths(num_nodes, edges)

    assert dist[0][0] == 0.0
    assert dist[0][1] == -2.0
    assert dist[0][2] == -3.0  # 0 -> 1 -> 2
    assert dist[0][3] == -1.0  # 0 -> 1 -> 2 -> 3 (-3 + 2 = -1)

def test_johnson_algorithm_negative_cycle():
    num_nodes = 3
    edges = [
        (0, 1, 1.0),
        (1, 2, -2.0),
        (2, 0, -1.0)  # Total cycle weight = -2
    ]

    with pytest.raises(ValueError, match="negative-weight cycle"):
        johnson_all_pairs_shortest_paths(num_nodes, edges)

def test_johnson_algorithm_unreachable_nodes():
    num_nodes = 3
    edges = [(0, 1, 5.0)]

    dist = johnson_all_pairs_shortest_paths(num_nodes, edges)
    assert dist[0][1] == 5.0
    assert dist[0][2] == float('inf')
