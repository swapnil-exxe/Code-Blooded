import pytest
from algorithms.convex_hull import convex_hull, cross_product

def test_convex_hull_square_with_interior():
    points = [
        (0, 0), (0, 2), (2, 2), (2, 0),
        (1, 1), (0.5, 0.5), (1.5, 1.5)  # Interior points
    ]
    hull = convex_hull(points)
    # Hull should only contain the 4 corners of the square
    assert set(hull) == {(0, 0), (0, 2), (2, 2), (2, 0)}
    assert len(hull) == 4

def test_convex_hull_triangle():
    points = [(0, 0), (4, 0), (2, 3), (2, 1)]
    hull = convex_hull(points)
    assert set(hull) == {(0, 0), (4, 0), (2, 3)}
    assert len(hull) == 3

def test_convex_hull_collinear():
    points = [(0, 0), (1, 1), (2, 2), (3, 3)]
    hull = convex_hull(points)
    # The extreme endpoints form the degenerate hull
    assert (0, 0) in hull
    assert (3, 3) in hull

def test_convex_hull_small():
    assert convex_hull([]) == []
    assert convex_hull([(1, 1)]) == [(1, 1)]
    assert len(convex_hull([(1, 1), (2, 2)])) == 2
