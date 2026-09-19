import pytest
from algorithms.max_flow import edmonds_karp

def test_edmonds_karp_standard_network():
    num_nodes = 6
    source = 0
    sink = 5
    edges = [
        (0, 1, 16.0),
        (0, 2, 13.0),
        (1, 2, 10.0),
        (1, 3, 12.0),
        (2, 1, 4.0),
        (2, 4, 14.0),
        (3, 2, 9.0),
        (3, 5, 20.0),
        (4, 3, 7.0),
        (4, 5, 4.0)
    ]

    max_flow, residual = edmonds_karp(num_nodes, edges, source, sink)
    assert max_flow == 23.0

def test_edmonds_karp_disconnected_source_sink():
    num_nodes = 4
    edges = [(0, 1, 10.0), (2, 3, 10.0)]

    max_flow, _ = edmonds_karp(num_nodes, edges, source=0, sink=3)
    assert max_flow == 0.0

def test_edmonds_karp_same_source_and_sink():
    with pytest.raises(ValueError, match="Source and Sink cannot be the same"):
        edmonds_karp(4, [], source=1, sink=1)

def test_edmonds_karp_negative_capacity():
    with pytest.raises(ValueError, match="Negative capacity"):
        edmonds_karp(3, [(0, 1, -5.0)], source=0, sink=1)
