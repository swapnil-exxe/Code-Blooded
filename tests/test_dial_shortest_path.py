import pytest
from algorithms.dial_shortest_path import zero_one_bfs, dial_shortest_path

def test_zero_one_bfs_simple():
    # 0 -> 1 (w=1), 0 -> 2 (w=0), 2 -> 1 (w=0), 1 -> 3 (w=1)
    adj = [
        [(1, 1), (2, 0)],
        [(3, 1)],
        [(1, 0)],
        []
    ]
    dist = zero_one_bfs(4, adj, 0)
    assert dist == [0, 0, 0, 1]

def test_dial_shortest_path_simple():
    # Graph with small weights <= 5
    adj = [
        [(1, 4), (2, 2)],
        [(3, 1)],
        [(1, 1), (3, 5)],
        []
    ]
    dist = dial_shortest_path(4, adj, 0, max_weight=5)
    # 0 -> 2 (2) -> 1 (2+1=3) -> 3 (3+1=4)
    assert dist == [0, 3, 2, 4]

def test_disconnected_and_unreachable():
    adj = [
        [(1, 2)],
        [],
        [(3, 1)],
        []
    ]
    dist_bfs = zero_one_bfs(4, [[(1, 1)], [], [(3, 1)], []], 0)
    assert dist_bfs[0] == 0
    assert dist_bfs[1] == 1
    assert dist_bfs[2] == float('inf')
    assert dist_bfs[3] == float('inf')

    dist_dial = dial_shortest_path(4, adj, 0, max_weight=2)
    assert dist_dial[0] == 0
    assert dist_dial[1] == 2
    assert dist_dial[2] == float('inf')
    assert dist_dial[3] == float('inf')

def test_exceptions():
    with pytest.raises(ValueError):
        zero_one_bfs(0, [], 0)
    with pytest.raises(ValueError):
        zero_one_bfs(2, [[(1, 5)]], 0)
    with pytest.raises(IndexError):
        dial_shortest_path(2, [[], []], 5, max_weight=3)
