import pytest
from algorithms.stoer_wagner import StoerWagnerMinCut

def test_stoer_wagner_barbell_graph():
    # Two triangles joined by a single bridge of weight 1.0: (0-1-2-0) - 2-3 - (3-4-5-3)
    sw = StoerWagnerMinCut(6)
    # Triangle 1
    sw.add_edge(0, 1, 3.0)
    sw.add_edge(1, 2, 3.0)
    sw.add_edge(2, 0, 3.0)
    # Bridge
    sw.add_edge(2, 3, 1.0)
    # Triangle 2
    sw.add_edge(3, 4, 3.0)
    sw.add_edge(4, 5, 3.0)
    sw.add_edge(5, 3, 3.0)

    cut_wt, part_a, part_b = sw.min_cut()
    assert cut_wt == 1.0
    assert len(part_a) + len(part_b) == 6
    assert part_a.isdisjoint(part_b)
    assert (part_a == {0, 1, 2} and part_b == {3, 4, 5}) or (part_a == {3, 4, 5} and part_b == {0, 1, 2})

def test_stoer_wagner_weighted_graph():
    # 4 vertices
    # 0 --(2)-- 1
    # |         |
    # (3)      (1)
    # |         |
    # 2 --(4)-- 3
    sw = StoerWagnerMinCut(4)
    sw.add_edge(0, 1, 2.0)
    sw.add_edge(0, 2, 3.0)
    sw.add_edge(1, 3, 1.0)
    sw.add_edge(2, 3, 4.0)

    # Cut isolating vertex 1 has weight 2 + 1 = 3.0
    # Cut isolating vertex 0 has weight 2 + 3 = 5.0
    # Cut isolating vertex 2 has weight 3 + 4 = 7.0
    # Cut isolating vertex 3 has weight 1 + 4 = 5.0
    # Horizontal cut (0,1) vs (2,3) has weight 3 + 1 = 4.0
    # Min cut is isolating vertex 1 (cut weight 3.0)
    cut_wt, part_a, part_b = sw.min_cut()
    assert cut_wt == 3.0
    assert part_a == {1} or part_b == {1}

def test_stoer_wagner_disconnected():
    sw = StoerWagnerMinCut(4)
    sw.add_edge(0, 1, 5.0)
    sw.add_edge(2, 3, 5.0)
    cut_wt, part_a, part_b = sw.min_cut()
    assert cut_wt == 0.0

def test_stoer_wagner_exceptions():
    with pytest.raises(ValueError):
        StoerWagnerMinCut(1)
    sw = StoerWagnerMinCut(3)
    with pytest.raises(IndexError):
        sw.add_edge(0, 5, 1.0)
    with pytest.raises(ValueError):
        sw.add_edge(0, 1, -2.0)
