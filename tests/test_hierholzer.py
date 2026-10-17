import pytest
from algorithms.hierholzer import Hierholzer

def test_eulerian_circuit_directed():
    # 0 -> 1 -> 2 -> 0
    edges = [(0, 1), (1, 2), (2, 0)]
    path = Hierholzer.find_eulerian_path_directed(3, edges)
    assert path is not None
    assert len(path) == 4
    assert path[0] == path[-1]
    # Check that each step corresponds to an edge
    visited_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
    assert sorted(visited_edges) == sorted(edges)

def test_eulerian_path_directed():
    # 0 -> 1 -> 2 -> 3
    edges = [(0, 1), (1, 2), (2, 3)]
    path = Hierholzer.find_eulerian_path_directed(4, edges)
    assert path == [0, 1, 2, 3]

def test_eulerian_path_directed_impossible():
    # 0 -> 1, 0 -> 2 (both outgoing from 0, no in-degrees)
    edges = [(0, 1), (0, 2)]
    path = Hierholzer.find_eulerian_path_directed(3, edges)
    assert path is None

def test_eulerian_circuit_undirected():
    # Triangle: 0-1, 1-2, 2-0
    edges = [(0, 1), (1, 2), (2, 0)]
    path = Hierholzer.find_eulerian_path_undirected(3, edges)
    assert path is not None
    assert len(path) == 4
    assert path[0] == path[-1]
    visited = [tuple(sorted((path[i], path[i+1]))) for i in range(len(path)-1)]
    expected = [tuple(sorted(e)) for e in edges]
    assert sorted(visited) == sorted(expected)

def test_eulerian_path_undirected_seven_bridges_impossible():
    # Konigsberg 7 bridges graph (4 vertices with odd degree: 3, 3, 3, 5)
    # Impossible to have Eulerian path
    edges = [
        (0, 1), (0, 1),
        (0, 2), (0, 2),
        (0, 3),
        (1, 3),
        (2, 3)
    ]
    path = Hierholzer.find_eulerian_path_undirected(4, edges)
    assert path is None

def test_empty_and_error():
    assert Hierholzer.find_eulerian_path_directed(2, []) == []
    assert Hierholzer.find_eulerian_path_undirected(2, []) == []
    with pytest.raises(IndexError):
        Hierholzer.find_eulerian_path_directed(2, [(0, 5)])
