import pytest
from algorithms.min_cost_max_flow import MinCostMaxFlow

def test_mcmf_standard_network():
    mcmf = MinCostMaxFlow(4)
    # (u, v, cap, cost)
    mcmf.add_edge(0, 1, 3.0, 1.0)
    mcmf.add_edge(0, 2, 2.0, 4.0)
    mcmf.add_edge(1, 2, 1.0, 2.0)
    mcmf.add_edge(1, 3, 2.0, 5.0)
    mcmf.add_edge(2, 3, 3.0, 2.0)

    flow, cost = mcmf.min_cost_max_flow(0, 3)
    assert flow == 5.0
    assert cost == 29.0

def test_mcmf_invalid_inputs():
    with pytest.raises(ValueError):
        MinCostMaxFlow(0)

    m = MinCostMaxFlow(3)
    with pytest.raises(ValueError):
        m.add_edge(0, 1, -2.0, 1.0)
    with pytest.raises(ValueError):
        m.min_cost_max_flow(1, 1)
