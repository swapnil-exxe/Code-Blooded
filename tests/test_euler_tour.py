import pytest
from algorithms.euler_tour import EulerTourTree

def test_euler_tour_subtree_sum_and_update():
    #          0 (val 10)
    #        /   \
    #    1 (5)   2 (20)
    #    /
    #  3 (15)
    num_nodes = 4
    edges = [(0, 1), (0, 2), (1, 3)]
    values = [10, 5, 20, 15]

    ett = EulerTourTree(num_nodes, edges, values, root=0)

    # Subtree 0 sum: 10 + 5 + 20 + 15 = 50
    assert ett.query_subtree_sum(0) == 50
    # Subtree 1 sum: 5 + 15 = 20
    assert ett.query_subtree_sum(1) == 20
    # Subtree 2 sum: 20
    assert ett.query_subtree_sum(2) == 20
    # Subtree 3 sum: 15
    assert ett.query_subtree_sum(3) == 15

    # Update node 3 value to 25
    ett.update_node_val(3, 25)
    assert ett.query_subtree_sum(1) == 30
    assert ett.query_subtree_sum(0) == 60

def test_euler_tour_invalid_inputs():
    with pytest.raises(ValueError):
        EulerTourTree(0, [], [])
    with pytest.raises(IndexError):
        EulerTourTree(2, [(0, 1)], [10, 20], root=5)
