import pytest
from algorithms.bridges_articulation_points import BridgeArticulationFinder

def test_single_bridge_and_articulation_point():
    # 0 - 1 - 2
    finder = BridgeArticulationFinder(3)
    finder.add_edge(0, 1)
    finder.add_edge(1, 2)
    bridges, cut_vertices = finder.analyze()

    assert bridges == [(0, 1), (1, 2)]
    assert cut_vertices == {1}

def test_cycle_no_bridges_no_cut_vertices():
    # Triangle: 0 - 1 - 2 - 0
    finder = BridgeArticulationFinder(3)
    finder.add_edge(0, 1)
    finder.add_edge(1, 2)
    finder.add_edge(2, 0)
    bridges, cut_vertices = finder.analyze()

    assert bridges == []
    assert cut_vertices == set()

def test_barbell_graph():
    # Two triangles connected by a bridge: (0-1-2-0) - 2-3 - (3-4-5-3)
    finder = BridgeArticulationFinder(6)
    finder.add_edge(0, 1)
    finder.add_edge(1, 2)
    finder.add_edge(2, 0)
    finder.add_edge(2, 3) # bridge
    finder.add_edge(3, 4)
    finder.add_edge(4, 5)
    finder.add_edge(5, 3)

    bridges, cut_vertices = finder.analyze()
    assert bridges == [(2, 3)]
    assert cut_vertices == {2, 3}

def test_multiedge_not_bridge():
    # 0 is connected to 1 by two parallel edges
    finder = BridgeArticulationFinder(2)
    finder.add_edge(0, 1)
    finder.add_edge(0, 1)
    bridges, cut_vertices = finder.analyze()

    assert bridges == []
    assert cut_vertices == set()

def test_disconnected_components():
    finder = BridgeArticulationFinder(4)
    finder.add_edge(0, 1)
    # 2 and 3 are isolated or connected separately
    finder.add_edge(2, 3)
    bridges, cut_vertices = finder.analyze()

    assert bridges == [(0, 1), (2, 3)]
    assert cut_vertices == set()

def test_error_handling():
    with pytest.raises(ValueError):
        BridgeArticulationFinder(-1)
    finder = BridgeArticulationFinder(3)
    with pytest.raises(IndexError):
        finder.add_edge(0, 5)
