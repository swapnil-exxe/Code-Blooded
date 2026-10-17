import pytest
from algorithms.karger_min_cut import karger_min_cut, karger_single_trial

def test_karger_barbell_graph():
    # Two triangles joined by a single bridge: (0-1-2-0) - 2-3 - (3-4-5-3)
    # Global min cut is 1 (edge 2-3)
    edges = [
        (0, 1), (1, 2), (2, 0),
        (2, 3), # bridge
        (3, 4), (4, 5), (5, 3)
    ]
    cut_size, part_a, part_b = karger_min_cut(6, edges, trials=50)

    assert cut_size == 1
    assert len(part_a) + len(part_b) == 6
    assert part_a.isdisjoint(part_b)
    # The bridge separates {0, 1, 2} and {3, 4, 5}
    assert (part_a == {0, 1, 2} and part_b == {3, 4, 5}) or (part_a == {3, 4, 5} and part_b == {0, 1, 2})

def test_karger_complete_graph():
    # K4: every vertex has degree 3. Min cut is 3.
    edges = [
        (0, 1), (0, 2), (0, 3),
        (1, 2), (1, 3),
        (2, 3)
    ]
    cut_size, part_a, part_b = karger_min_cut(4, edges, trials=50)
    assert cut_size == 3

def test_karger_disconnected():
    # Disconnected graph: min cut must be 0
    edges = [(0, 1), (2, 3)]
    cut_size, part_a, part_b = karger_min_cut(4, edges, trials=10)
    assert cut_size == 0
    assert len(part_a) > 0 and len(part_b) > 0

def test_karger_empty_and_exceptions():
    cut_size, part_a, part_b = karger_min_cut(3, [])
    assert cut_size == 0
    with pytest.raises(ValueError):
        karger_min_cut(1, [])
    with pytest.raises(IndexError):
        karger_min_cut(3, [(0, 5)])
