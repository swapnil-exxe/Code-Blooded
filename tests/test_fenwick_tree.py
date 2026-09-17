import pytest
from algorithms.fenwick_tree import FenwickTree

def test_fenwick_tree_initialization_by_size():
    ft = FenwickTree(5)
    assert ft.size == 5
    assert ft.query(5) == 0

def test_fenwick_tree_initialization_by_array():
    arr = [1, 3, 5, 7, 9, 11]
    ft = FenwickTree(arr)
    assert ft.size == 6
    assert ft.query(1) == 1
    assert ft.query(3) == 9
    assert ft.query(6) == 36

def test_fenwick_tree_point_update_and_range_query():
    arr = [2, 4, 6, 8, 10]
    ft = FenwickTree(arr)
    
    assert ft.range_query(2, 4) == 4 + 6 + 8
    
    # Update 3rd element (+5)
    ft.update(3, 5)
    assert ft.query(3) == 2 + 4 + 11
    assert ft.range_query(2, 4) == 4 + 11 + 8

def test_fenwick_tree_edge_cases_and_errors():
    with pytest.raises(ValueError):
        FenwickTree(0)
    
    with pytest.raises(ValueError):
        FenwickTree([])

    ft = FenwickTree(4)
    with pytest.raises(IndexError):
        ft.update(0, 10)
    
    with pytest.raises(IndexError):
        ft.update(5, 10)
    
    with pytest.raises(IndexError):
        ft.range_query(3, 2)
