import pytest
from algorithms.heavy_light_decomposition import HeavyLightDecomposition

def test_hld_path_max_query_and_update():
    #          0 (val 5)
    #        /   \
    #    1 (10)  2 (20)
    #    /
    #  3 (15)
    num_nodes = 4
    edges = [(0, 1), (0, 2), (1, 3)]
    values = [5, 10, 20, 15]

    hld = HeavyLightDecomposition(num_nodes, edges, values, root=0)

    # Path 3 -> 1 -> 0 -> 2: max values are (15, 10, 5, 20) -> max 20
    assert hld.query_path_max(3, 2) == 20
    # Path 3 -> 1: max values (15, 10) -> max 15
    assert hld.query_path_max(3, 1) == 15

    # Update node 1 value to 100
    hld.update_node(1, 100)
    assert hld.query_path_max(3, 1) == 100
    assert hld.query_path_max(3, 2) == 100

def test_hld_invalid_inputs():
    with pytest.raises(ValueError):
        HeavyLightDecomposition(0, [], [])

    with pytest.raises(ValueError):
        HeavyLightDecomposition(2, [(0, 1)], [10])  # values length mismatch
