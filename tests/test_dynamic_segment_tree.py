import pytest
from algorithms.dynamic_segment_tree import DynamicSegmentTree

def test_dynamic_segment_tree_sparse_range():
    # Sparse range 1 to 10^9
    dst = DynamicSegmentTree(1, 10**9)

    dst.update(100, 10)
    dst.update(1000000, 50)
    dst.update(500000000, 25)

    assert dst.query(1, 100) == 10
    assert dst.query(101, 999999) == 0
    assert dst.query(100, 1000000) == 60
    assert dst.query(1, 10**9) == 85

def test_dynamic_segment_tree_invalid_range():
    with pytest.raises(ValueError):
        DynamicSegmentTree(10, 5)
