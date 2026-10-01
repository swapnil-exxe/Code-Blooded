import pytest
from algorithms.b_tree import BTree

def test_b_tree_insertion_and_search():
    bt = BTree(t=3)  # Max keys per node = 5
    keys = [10, 20, 5, 6, 12, 30, 7, 17]
    for k in keys:
        bt.insert(k)

    assert bt.traverse() == [5, 6, 7, 10, 12, 17, 20, 30]

    for k in keys:
        assert bt.search(k) is True

    assert bt.search(100) is False

def test_b_tree_min_degree_2():
    bt = BTree(t=2)  # 2-3-4 tree (Max keys per node = 3)
    keys = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for k in keys:
        bt.insert(k)

    assert bt.traverse() == list(range(1, 11))

def test_b_tree_invalid_t():
    with pytest.raises(ValueError):
        BTree(t=1)
