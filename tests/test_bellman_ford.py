import pytest
from algorithms.bellman_ford import bellman_ford, reconstruct_bellman_ford_path

def test_bellman_ford_positive_and_negative_weights():
    num_nodes = 5
    edges = [
        (0, 1, -1),
        (0, 2, 4),
        (1, 2, 3),
        (1, 3, 2),
        (1, 4, 2),
        (3, 2, 5),
        (3, 1, 1),
        (4, 3, -3)
    ]
    
    distances, predecessors = bellman_ford(num_nodes, edges, start=0)
    assert distances == [0, -1, 2, -2, 1]

    path = reconstruct_bellman_ford_path(predecessors, start=0, target=3)
    assert path == [0, 1, 4, 3]

def test_bellman_ford_negative_cycle_detection():
    num_nodes = 4
    edges = [
        (0, 1, 1),
        (1, 2, -1),
        (2, 3, -1),
        (3, 1, -1)  # Negative cycle: 1 -> 2 -> 3 -> 1 (weight -3)
    ]

    with pytest.raises(ValueError, match="negative-weight cycle"):
        bellman_ford(num_nodes, edges, start=0)

def test_bellman_ford_unreachable_target():
    num_nodes = 4
    edges = [(0, 1, 2), (2, 3, 1)]

    distances, predecessors = bellman_ford(num_nodes, edges, start=0)
    assert distances[0] == 0
    assert distances[1] == 2
    assert distances[2] == float('inf')
    assert distances[3] == float('inf')

    assert reconstruct_bellman_ford_path(predecessors, start=0, target=3) is None

def test_bellman_ford_invalid_start_node():
    with pytest.raises(IndexError):
        bellman_ford(3, [(0, 1, 1)], start=5)
