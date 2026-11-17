import pytest
from algorithms.link_cut_tree import LinkCutTree

def test_lct_connectivity_and_linking():
    # 5 vertices with values 1, 2, 3, 4, 5
    lct = LinkCutTree([1, 2, 3, 4, 5])

    for i in range(5):
        assert lct.find_root(i) == i

    assert not lct.connected(0, 1)

    assert lct.link(0, 1) is True
    assert lct.connected(0, 1) is True
    assert lct.link(0, 1) is False  # Already connected

    assert lct.link(1, 2) is True
    assert lct.connected(0, 2) is True
    assert not lct.connected(0, 3)

    assert lct.link(3, 4) is True
    assert lct.connected(3, 4) is True
    assert not lct.connected(1, 4)

    assert lct.link(2, 3) is True
    assert lct.connected(0, 4) is True

def test_lct_cut_and_reconnection():
    lct = LinkCutTree([10, 20, 30, 40])
    lct.link(0, 1)
    lct.link(1, 2)
    lct.link(2, 3)

    assert lct.connected(0, 3) is True

    # Cut edge (1, 2)
    assert lct.cut(1, 2) is True
    assert lct.connected(0, 1) is True
    assert lct.connected(2, 3) is True
    assert lct.connected(0, 3) is False

    # Attempt invalid cuts
    assert lct.cut(0, 3) is False  # Not connected
    assert lct.cut(0, 2) is False  # Connected in forest, but no direct edge

    # Re-link differently: 1 - 3
    assert lct.link(1, 3) is True
    assert lct.connected(0, 2) is True

def test_lct_path_sum_and_update():
    # Tree: 0 - 1 - 2 - 3 with values [1, 10, 100, 1000]
    lct = LinkCutTree([1, 10, 100, 1000])
    lct.link(0, 1)
    lct.link(1, 2)
    lct.link(2, 3)

    assert lct.path_sum(0, 3) == 1111
    assert lct.path_sum(1, 2) == 110
    assert lct.path_sum(0, 0) == 1

    # Update value at node 2 from 100 to 500
    lct.update_value(2, 500)
    assert lct.path_sum(0, 3) == 1511
    assert lct.path_sum(1, 2) == 510

def test_lct_exceptions():
    with pytest.raises(ValueError):
        LinkCutTree([])

    lct = LinkCutTree([1, 2, 3])
    with pytest.raises(IndexError):
        lct.link(0, 5)
    with pytest.raises(ValueError):
        lct.path_sum(0, 2)  # Disconnected
