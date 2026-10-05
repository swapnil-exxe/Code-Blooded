import pytest
from algorithms.fenwick_tree_range import RangeFenwickTree

def test_range_fenwick_tree_initialization_from_array():
    arr = [1, 2, 3, 4, 5]
    ft = RangeFenwickTree(arr)

    assert ft.range_query(1, 5) == 15
    assert ft.range_query(2, 4) == 9
    assert ft.prefix_query(3) == 6

def test_range_fenwick_tree_range_updates():
    ft = RangeFenwickTree(5)
    # Range update [2, 4] += 5 -> arr: [0, 5, 5, 5, 0]
    ft.range_update(2, 4, 5)
    assert ft.range_query(1, 5) == 15
    assert ft.range_query(2, 4) == 15
    assert ft.range_query(1, 1) == 0
    assert ft.range_query(5, 5) == 0

    # Range update [1, 3] += 2 -> arr: [2, 7, 7, 5, 0]
    ft.range_update(1, 3, 2)
    assert ft.range_query(1, 1) == 2
    assert ft.range_query(2, 2) == 7
    assert ft.range_query(3, 3) == 7
    assert ft.range_query(4, 4) == 5
    assert ft.range_query(1, 5) == 21

def test_range_fenwick_tree_invalid_inputs():
    with pytest.raises(ValueError):
        RangeFenwickTree(0)
    with pytest.raises(ValueError):
        RangeFenwickTree([])

    ft = RangeFenwickTree(4)
    with pytest.raises(IndexError):
        ft.range_update(3, 2, 10)
    with pytest.raises(IndexError):
        ft.range_query(0, 3)
