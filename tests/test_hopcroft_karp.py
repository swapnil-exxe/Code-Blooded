import pytest
from algorithms.hopcroft_karp import HopcroftKarp

def test_hopcroft_karp_bipartite_matching():
    # 4 left nodes, 4 right nodes
    hk = HopcroftKarp(4, 4)
    edges = [
        (1, 1), (1, 2),
        (2, 2), (2, 3),
        (3, 3), (3, 4),
        (4, 4)
    ]
    for u, v in edges:
        hk.add_edge(u, v)

    assert hk.max_matching() == 4
    matches = hk.get_matches()
    assert len(matches) == 4

def test_hopcroft_karp_partial_matching():
    hk = HopcroftKarp(3, 3)
    edges = [(1, 1), (2, 1), (3, 1)]
    for u, v in edges:
        hk.add_edge(u, v)

    assert hk.max_matching() == 1

def test_hopcroft_karp_invalid_inputs():
    with pytest.raises(ValueError):
        HopcroftKarp(0, 5)

    hk = HopcroftKarp(2, 2)
    with pytest.raises(IndexError):
        hk.add_edge(3, 1)
