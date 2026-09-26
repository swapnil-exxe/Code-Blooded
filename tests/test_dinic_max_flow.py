import pytest
from algorithms.dinic_max_flow import DinicMaxFlow

def test_dinic_max_flow_network():
    dinic = DinicMaxFlow(6)
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
    for u, v, c in edges:
        dinic.add_edge(u, v, c)

    assert dinic.max_flow(0, 5) == 23.0

def test_dinic_disconnected_source_sink():
    dinic = DinicMaxFlow(4)
    dinic.add_edge(0, 1, 10.0)
    dinic.add_edge(2, 3, 10.0)
    assert dinic.max_flow(0, 3) == 0.0

def test_dinic_invalid_inputs():
    with pytest.raises(ValueError):
        DinicMaxFlow(0)

    dinic = DinicMaxFlow(3)
    with pytest.raises(ValueError):
        dinic.add_edge(0, 1, -5.0)

    with pytest.raises(ValueError):
        dinic.max_flow(1, 1)
