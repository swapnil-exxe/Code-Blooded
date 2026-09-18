import pytest
from algorithms.mst import kruskal_mst, prim_mst

def test_mst_kruskal_and_prim_weight_match():
    num_nodes = 5
    edges = [
        (0, 1, 2),
        (0, 3, 6),
        (1, 2, 3),
        (1, 3, 8),
        (1, 4, 5),
        (2, 4, 7),
        (3, 4, 9)
    ]

    k_weight, k_edges = kruskal_mst(num_nodes, edges)
    p_weight, p_edges = prim_mst(num_nodes, edges)

    assert k_weight == 16.0
    assert p_weight == 16.0
    assert len(k_edges) == 4
    assert len(p_edges) == 4

def test_mst_disconnected_graph():
    num_nodes = 4
    edges = [(0, 1, 1), (2, 3, 2)]

    with pytest.raises(ValueError, match="disconnected"):
        kruskal_mst(num_nodes, edges)

    with pytest.raises(ValueError, match="disconnected"):
        prim_mst(num_nodes, edges)

def test_mst_single_node():
    k_weight, k_edges = kruskal_mst(1, [])
    p_weight, p_edges = prim_mst(1, [])
    assert k_weight == 0.0 and k_edges == []
    assert p_weight == 0.0 and p_edges == []

def test_mst_out_of_bounds_edge():
    with pytest.raises(IndexError):
        kruskal_mst(3, [(0, 5, 2)])
