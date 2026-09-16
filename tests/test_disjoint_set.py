import pytest
from algorithms.disjoint_set import DisjointSet

def test_disjoint_set_union_and_find():
    dsu = DisjointSet(5)
    assert dsu.count == 5
    assert dsu.connected(0, 1) is False

    assert dsu.union(0, 1) is True
    assert dsu.connected(0, 1) is True
    assert dsu.count == 4

    assert dsu.union(1, 2) is True
    assert dsu.connected(0, 2) is True
    assert dsu.count == 3

    # Duplicate union returns False
    assert dsu.union(0, 2) is False

def test_disjoint_set_invalid_size():
    with pytest.raises(ValueError, match="greater than zero"):
        DisjointSet(0)
