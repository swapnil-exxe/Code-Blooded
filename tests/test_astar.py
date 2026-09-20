import pytest
from algorithms.astar import astar_search

def test_astar_simple_path():
    grid = [
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ]
    path = astar_search(grid, (0, 0), (2, 2))
    assert path is not None
    assert path[0] == (0, 0)
    assert path[-1] == (2, 2)
    assert len(path) == 5  # Optimal path around obstacle: 5 steps

def test_astar_unreachable_goal():
    grid = [
        [0, 1, 0],
        [1, 1, 0],
        [0, 0, 0]
    ]
    # (0, 0) is trapped by obstacles
    assert astar_search(grid, (0, 0), (2, 2)) is None

def test_astar_start_equals_goal():
    grid = [[0]]
    assert astar_search(grid, (0, 0), (0, 0)) == [(0, 0)]

def test_astar_heuristics():
    grid = [
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0]
    ]
    path_m = astar_search(grid, (0, 0), (0, 3), heuristic="manhattan")
    path_e = astar_search(grid, (0, 0), (0, 3), heuristic="euclidean")
    assert path_m is not None
    assert path_e is not None

def test_astar_out_of_bounds_and_invalid_heuristic():
    grid = [[0, 0], [0, 0]]
    with pytest.raises(IndexError):
        astar_search(grid, (5, 0), (0, 0))
    with pytest.raises(ValueError):
        astar_search(grid, (0, 0), (1, 1), heuristic="cosine")
