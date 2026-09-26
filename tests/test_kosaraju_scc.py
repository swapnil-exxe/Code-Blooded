import pytest
from algorithms.kosaraju_scc import kosaraju_scc

def test_kosaraju_scc_multiple_components():
    num_nodes = 5
    edges = [
        (1, 0),
        (0, 2),
        (2, 1),
        (0, 3),
        (3, 4)
    ]

    sccs = kosaraju_scc(num_nodes, edges)
    scc_sets = {frozenset(component) for component in sccs}
    expected = {
        frozenset([0, 1, 2]),
        frozenset([3]),
        frozenset([4])
    }
    assert scc_sets == expected

def test_kosaraju_scc_dag():
    num_nodes = 4
    edges = [(0, 1), (1, 2), (2, 3)]

    sccs = kosaraju_scc(num_nodes, edges)
    assert len(sccs) == 4
    for component in sccs:
        assert len(component) == 1

def test_kosaraju_scc_out_of_bounds():
    with pytest.raises(IndexError):
        kosaraju_scc(3, [(0, 5)])
