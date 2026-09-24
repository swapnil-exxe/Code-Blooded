import pytest
from algorithms.lca_binary_lifting import LCABinaryLifting

def test_lca_binary_tree_structure():
    #          0
    #        /   \
    #       1     2
    #      / \   / \
    #     3   4 5   6
    num_nodes = 7
    edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]

    lca_tree = LCABinaryLifting(num_nodes, edges, root=0)

    assert lca_tree.query_lca(3, 4) == 1
    assert lca_tree.query_lca(3, 5) == 0
    assert lca_tree.query_lca(1, 3) == 1
    assert lca_tree.query_lca(0, 6) == 0

    assert lca_tree.get_distance(3, 4) == 2
    assert lca_tree.get_distance(3, 5) == 4
    assert lca_tree.get_distance(0, 6) == 2

def test_lca_single_node_tree():
    lca_tree = LCABinaryLifting(1, [], root=0)
    assert lca_tree.query_lca(0, 0) == 0
    assert lca_tree.get_distance(0, 0) == 0

def test_lca_out_of_bounds_and_invalid():
    with pytest.raises(ValueError):
        LCABinaryLifting(0, [])

    with pytest.raises(IndexError):
        LCABinaryLifting(3, [(0, 1)], root=5)

    tree = LCABinaryLifting(3, [(0, 1), (1, 2)], root=0)
    with pytest.raises(IndexError):
        tree.query_lca(0, 10)
