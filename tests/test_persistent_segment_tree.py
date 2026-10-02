import pytest
from algorithms.persistent_segment_tree import PersistentSegmentTree

def test_persistent_segment_tree_historical_queries():
    arr = [1, 2, 3, 4, 5]
    pst = PersistentSegmentTree(arr)

    # Version 0 query
    assert pst.query(0, 0, 4) == 15
    assert pst.query(0, 1, 3) == 9

    # Version 1: update idx 2 (+10) -> arr[2] becomes 13
    v1 = pst.update(0, 2, 10)
    assert v1 == 1
    assert pst.query(1, 0, 4) == 25
    assert pst.query(1, 1, 3) == 19

    # Historical Version 0 must remain unchanged!
    assert pst.query(0, 0, 4) == 15
    assert pst.query(0, 1, 3) == 9

    # Version 2: update idx 0 (+5) on top of Version 1
    v2 = pst.update(1, 0, 5)
    assert v2 == 2
    assert pst.query(2, 0, 4) == 30
    assert pst.query(1, 0, 4) == 25
    assert pst.query(0, 0, 4) == 15

def test_persistent_segment_tree_invalid_inputs():
    with pytest.raises(ValueError):
        PersistentSegmentTree([])

    pst = PersistentSegmentTree([1, 2, 3])
    with pytest.raises(IndexError):
        pst.query(10, 0, 1)
