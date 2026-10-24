import pytest
from algorithms.li_chao_tree import LiChaoTree

def test_li_chao_tree_min_queries():
    tree = LiChaoTree(x_min=-100, x_max=100, is_min=True)

    # Add lines: y = 2x + 10, y = -1x + 20, y = 0x + 15
    tree.add_line(2, 10)
    tree.add_line(-1, 20)
    tree.add_line(0, 15)

    # At x = 0: 2(0)+10=10, -0+20=20, 15 -> min is 10
    assert tree.query(0) == 10

    # At x = 10: 2(10)+10=30, -10+20=10, 15 -> min is 10
    assert tree.query(10) == 10

    # At x = 2: 2(2)+10=14, -2+20=18, 15 -> min is 14
    assert tree.query(2) == 14

    # At x = 20: 2(20)+10=50, -20+20=0, 15 -> min is 0
    assert tree.query(20) == 0

def test_li_chao_tree_max_queries():
    tree = LiChaoTree(x_min=-100, x_max=100, is_min=False)
    tree.add_line(3, -5)
    tree.add_line(1, 10)

    # At x = 0: 3(0)-5 = -5, 1(0)+10 = 10 -> max is 10
    assert tree.query(0) == 10
    # At x = 10: 3(10)-5 = 25, 10+10 = 20 -> max is 25
    assert tree.query(10) == 25

def test_li_chao_tree_segments():
    tree = LiChaoTree(x_min=0, x_max=50, is_min=True)
    tree.add_line(0, 100) # baseline
    # Add segment y = -2x + 50 on [10, 20]
    tree.add_segment(-2, 50, 10, 20)

    # Outside [10, 20], baseline applies
    assert tree.query(5) == 100
    assert tree.query(25) == 100

    # Inside [10, 20]: at x = 15, -2(15)+50 = 20 < 100
    assert tree.query(15) == 20

def test_li_chao_tree_exceptions():
    with pytest.raises(ValueError):
        LiChaoTree(x_min=10, x_max=5)
    tree = LiChaoTree(x_min=0, x_max=10)
    with pytest.raises(ValueError):
        tree.query(5)
    with pytest.raises(IndexError):
        tree.add_line(1, 0)
        tree.query(20)
