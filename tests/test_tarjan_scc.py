import pytest
from algorithms.tarjan_scc import tarjan_scc

def test_tarjan_scc_multiple_components():
    num_nodes = 5
    edges = [
        (1, 0),
        (0, 2),
        (2, 1),
        (0, 3),
        (3, 4)
    ]

    sccs = tarjan_scc(num_nodes, edges)
    # Convert list of lists to sets of frozensets for comparison
    scc_sets = {frozenset(component) for component in sccs}
    expected = {
        frozenset([0, 1, 2]),
        frozenset([3]),
        frozenset([4])
    }
    assert scc_sets == expected

def test_tarjan_scc_dag_each_node_isolated_component():
    num_nodes = 4
    edges = [(0, 1), (1, 2), (2, 3)]

    sccs = tarjan_scc(num_nodes, edges)
    assert len(sccs) == 4
    for component in sccs:
        assert len(component) == 1

def test_tarjan_scc_completely_connected():
    num_nodes = 3
    edges = [(0, 1), (1, 2), (2, 0)]

    sccs = tarjan_scc(num_nodes, edges)
    assert len(sccs) == 1
    assert set(sccs[0]) == {0, 1, 2}

def test_tarjan_scc_out_of_bounds():
    with pytest.raises(IndexError):
        tarjan_scc(3, [(0, 4)])
