import pytest
import math
from algorithms.kd_tree import KDTree

def test_kd_tree_build_and_nearest_neighbor():
    points = [
        (2.0, 3.0),
        (5.0, 4.0),
        (9.0, 6.0),
        (4.0, 7.0),
        (8.0, 1.0),
        (7.0, 2.0),
    ]
    tree = KDTree(points)
    assert len(tree) == 6

    # Test exact query
    pt, dist = tree.nearest_neighbor((9.0, 6.0))
    assert pt == (9.0, 6.0)
    assert dist == 0.0

    # Test near query
    pt, dist = tree.nearest_neighbor((8.1, 1.9))
    assert pt == (8.0, 1.0)
    assert math.isclose(dist, math.hypot(8.1 - 8.0, 1.9 - 1.0))

def test_kd_tree_range_search():
    points = [
        (1.0, 1.0),
        (2.0, 2.0),
        (3.0, 3.0),
        (10.0, 10.0),
        (-5.0, -5.0),
    ]
    tree = KDTree(points)
    results = tree.range_search(lower=(0.0, 0.0), upper=(4.0, 4.0))
    assert set(results) == {(1.0, 1.0), (2.0, 2.0), (3.0, 3.0)}

def test_kd_tree_incremental_insert():
    tree = KDTree(k=3)
    assert len(tree) == 0
    tree.insert([1.0, 2.0, 3.0])
    tree.insert([4.0, 5.0, 6.0])
    assert len(tree) == 2

    pt, dist = tree.nearest_neighbor([1.1, 2.1, 3.1])
    assert pt == (1.0, 2.0, 3.0)
    assert dist < 0.2

def test_kd_tree_exceptions():
    with pytest.raises(ValueError):
        KDTree([])
    with pytest.raises(ValueError):
        KDTree([(1.0, 2.0), (1.0, 2.0, 3.0)])
    tree = KDTree([(1.0, 2.0)])
    with pytest.raises(ValueError):
        tree.insert([1.0, 2.0, 3.0])
    with pytest.raises(ValueError):
        tree.nearest_neighbor([1.0])
    with pytest.raises(ValueError):
        tree.range_search([0.0], [1.0])
