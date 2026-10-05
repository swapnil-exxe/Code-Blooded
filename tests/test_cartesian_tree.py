import pytest
from algorithms.cartesian_tree import CartesianTree

def test_cartesian_tree_build_properties():
    arr = [9, 3, 7, 1, 8, 12, 10, 20, 15, 18, 5]
    ct = CartesianTree(arr)

    # In-order traversal must reproduce input sequence exactly
    assert ct.inorder() == arr

    # Min-heap property must hold everywhere
    assert ct.is_valid_min_heap() is True

    # Root must hold the minimum element (1)
    assert ct.root.val == 1

def test_cartesian_tree_monotonic_increasing_and_decreasing():
    inc = [1, 2, 3, 4, 5]
    ct_inc = CartesianTree(inc)
    assert ct_inc.inorder() == inc
    assert ct_inc.is_valid_min_heap() is True

    dec = [5, 4, 3, 2, 1]
    ct_dec = CartesianTree(dec)
    assert ct_dec.inorder() == dec
    assert ct_dec.is_valid_min_heap() is True

def test_cartesian_tree_empty():
    with pytest.raises(ValueError):
        CartesianTree([])
