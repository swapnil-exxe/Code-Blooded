import pytest
from algorithms.fenwick_tree_3d import FenwickTree3D

def test_fenwick_tree_3d_point_and_prefix():
    bit = FenwickTree3D(4, 4, 4)
    bit.update(2, 3, 4, 10)
    bit.update(1, 1, 1, 5)

    assert bit.query(1, 1, 1) == 5
    assert bit.query(2, 2, 2) == 5
    assert bit.query(2, 3, 4) == 15
    assert bit.query(4, 4, 4) == 15
    assert bit.query(1, 4, 4) == 5
    assert bit.query(0, 0, 0) == 0

def test_fenwick_tree_3d_range_query():
    bit = FenwickTree3D(5, 5, 5)

    # Populate a 3x3x3 block from (2, 2, 2) to (4, 4, 4) with 1
    for x in range(2, 5):
        for y in range(2, 5):
            for z in range(2, 5):
                bit.update(x, y, z, 1)

    # Entire box of 3x3x3 should equal 27
    assert bit.range_query(2, 2, 2, 4, 4, 4) == 27

    # Sub-box of 2x2x2 should equal 8
    assert bit.range_query(2, 2, 2, 3, 3, 3) == 8

    # Single cell
    assert bit.range_query(3, 3, 3, 3, 3, 3) == 1

    # Outside the populated region
    assert bit.range_query(1, 1, 1, 1, 5, 5) == 0

def test_fenwick_tree_3d_exceptions():
    with pytest.raises(ValueError):
        FenwickTree3D(0, 5, 5)
    bit = FenwickTree3D(3, 3, 3)
    with pytest.raises(IndexError):
        bit.update(4, 1, 1, 5)
    with pytest.raises(IndexError):
        bit.query(5, 1, 1)
    with pytest.raises(IndexError):
        bit.range_query(2, 2, 2, 1, 2, 2)
