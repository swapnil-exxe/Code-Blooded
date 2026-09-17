import pytest
from algorithms.graph_algorithms import DijkstraGraph

def test_dijkstra_shortest_path_simple():
    g = DijkstraGraph()
    g.add_edge("A", "B", 4)
    g.add_edge("A", "C", 2)
    g.add_edge("C", "B", 1)
    g.add_edge("B", "D", 5)
    g.add_edge("C", "D", 8)

    distances, _ = g.shortest_path("A")
    assert distances["A"] == 0
    assert distances["C"] == 2
    assert distances["B"] == 3  # A -> C -> B
    assert distances["D"] == 8  # A -> C -> B -> D

    path = g.get_path("A", "D")
    assert path == ["A", "C", "B", "D"]

def test_dijkstra_unreachable_node():
    g = DijkstraGraph()
    g.add_edge("A", "B", 2)
    g.add_edge("C", "D", 1)

    distances, _ = g.shortest_path("A")
    assert distances["A"] == 0
    assert distances["B"] == 2
    assert distances["C"] == float('inf')
    assert distances["D"] == float('inf')

    assert g.get_path("A", "D") is None

def test_dijkstra_negative_weight_validation():
    g = DijkstraGraph()
    with pytest.raises(ValueError):
        g.add_edge("A", "B", -3)

def test_dijkstra_isolated_start():
    g = DijkstraGraph()
    distances, _ = g.shortest_path("X")
    assert distances["X"] == 0
    assert g.get_path("X", "X") == ["X"]
