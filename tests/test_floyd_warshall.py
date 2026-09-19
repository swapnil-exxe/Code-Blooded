import pytest
from algorithms.floyd_warshall import floyd_warshall, reconstruct_fw_path

def test_floyd_warshall_all_pairs():
    num_nodes = 4
    inf = float('inf')
    matrix = [
        [0.0, 3.0, inf, 7.0],
        [8.0, 0.0, 2.0, inf],
        [5.0, inf, 0.0, 1.0],
        [2.0, inf, inf, 0.0]
    ]

    dist, next_node = floyd_warshall(num_nodes, matrix)
    assert dist[0][1] == 3.0
    assert dist[0][2] == 5.0  # 0 -> 1 -> 2
    assert dist[0][3] == 6.0  # 0 -> 1 -> 2 -> 3

    path = reconstruct_fw_path(next_node, 0, 3)
    assert path == [0, 1, 2, 3]

def test_floyd_warshall_negative_weights_and_cycle():
    num_nodes = 3
    inf = float('inf')
    matrix = [
        [0.0, 1.0, inf],
        [inf, 0.0, -2.0],
        [-1.0, inf, 0.0]  # Cycle 0->1->2->0 has total weight 1 + (-2) + (-1) = -2
    ]

    with pytest.raises(ValueError, match="Negative-weight cycle"):
        floyd_warshall(num_nodes, matrix)

def test_floyd_warshall_unreachable_pair():
    num_nodes = 3
    inf = float('inf')
    matrix = [
        [0.0, 1.0, inf],
        [inf, 0.0, inf],
        [inf, inf, 0.0]
    ]

    dist, next_node = floyd_warshall(num_nodes, matrix)
    assert dist[0][2] == inf
    assert reconstruct_fw_path(next_node, 0, 2) is None
