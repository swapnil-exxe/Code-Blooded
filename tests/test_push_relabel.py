import pytest
from algorithms.push_relabel import PushRelabelMaxFlow

def test_push_relabel_simple_flow():
    # 0 -> 1 (cap 3), 0 -> 2 (cap 2), 1 -> 2 (cap 5), 1 -> 3 (cap 2), 2 -> 3 (cap 3)
    pr = PushRelabelMaxFlow(4)
    pr.add_edge(0, 1, 3)
    pr.add_edge(0, 2, 2)
    pr.add_edge(1, 2, 5)
    pr.add_edge(1, 3, 2)
    pr.add_edge(2, 3, 3)

    assert pr.max_flow(0, 3) == 5

def test_push_relabel_bottleneck():
    pr = PushRelabelMaxFlow(6)
    # s = 0, t = 5
    pr.add_edge(0, 1, 10)
    pr.add_edge(0, 2, 10)
    pr.add_edge(1, 2, 2)
    pr.add_edge(1, 3, 4)
    pr.add_edge(1, 4, 8)
    pr.add_edge(2, 4, 9)
    pr.add_edge(3, 5, 10)
    pr.add_edge(4, 3, 6)
    pr.add_edge(4, 5, 10)

    assert pr.max_flow(0, 5) == 19

def test_push_relabel_disconnected():
    pr = PushRelabelMaxFlow(4)
    pr.add_edge(0, 1, 10)
    pr.add_edge(2, 3, 10)
    assert pr.max_flow(0, 3) == 0

def test_push_relabel_validation():
    with pytest.raises(ValueError):
        PushRelabelMaxFlow(0)
    pr = PushRelabelMaxFlow(3)
    with pytest.raises(ValueError):
        pr.max_flow(1, 1)
    with pytest.raises(IndexError):
        pr.add_edge(0, 5, 10)
    with pytest.raises(ValueError):
        pr.add_edge(0, 1, -5)
