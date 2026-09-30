import pytest
from algorithms.fenwick_tree_2d import FenwickTree2D

def test_fenwick_tree_2d_operations():
    ft = FenwickTree2D(4, 4)
    # Update some cells
    ft.update(1, 1, 3)
    ft.update(2, 3, 5)
    ft.update(3, 2, 7)
    ft.update(4, 4, 2)

    assert ft.query(1, 1) == 3
    assert ft.query(2, 3) == 8  # 3 + 5
    assert ft.range_query(2, 2, 4, 4) == 5 + 7 + 2  # 14
    assert ft.range_query(1, 1, 4, 4) == 3 + 5 + 7 + 2  # 17

def test_fenwick_tree_2d_invalid_bounds():
    with pytest.raises(ValueError):
        FenwickTree2D(0, 5)

    ft = FenwickTree2D(3, 3)
    with pytest.raises(IndexError):
        ft.update(0, 1, 5)
    with pytest.raises(IndexError):
        ft.range_query(2, 3, 1, 3)
