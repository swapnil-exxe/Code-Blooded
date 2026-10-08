import pytest
from algorithms.convex_hull_trick import ConvexHullTrick

def test_cht_maximum_queries():
    cht = ConvexHullTrick(is_max=True)
    # Add lines: y = 2x + 1, y = 1x + 4, y = 3x - 2
    cht.add_line(2, 1)
    cht.add_line(1, 4)
    cht.add_line(3, -2)

    # At x = 0: 2(0)+1=1, 1(0)+4=4, 3(0)-2=-2 -> max is 4
    assert cht.query(0) == 4
    # At x = 2: 2(2)+1=5, 1(2)+4=6, 3(2)-2=4 -> max is 6
    assert cht.query(2) == 6
    # At x = 5: 2(5)+1=11, 1(5)+4=9, 3(5)-2=13 -> max is 13
    assert cht.query(5) == 13

def test_cht_minimum_queries():
    cht = ConvexHullTrick(is_max=False)
    cht.add_line(2, 3)
    cht.add_line(-1, 5)
    cht.add_line(0, 4)

    # At x = 1: 2(1)+3=5, -1(1)+5=4, 0+4=4 -> min is 4
    assert cht.query(1) == 4
    # At x = 3: 2(3)+3=9, -1(3)+5=2, 4 -> min is 2
    assert cht.query(3) == 2
    # At x = -2: 2(-2)+3=-1, -1(-2)+5=7, 4 -> min is -1
    assert cht.query(-2) == -1

def test_cht_parallel_and_redundant_lines():
    cht = ConvexHullTrick(is_max=True)
    cht.add_line(2, 5)
    cht.add_line(2, 3) # parallel and lower, should be ignored
    assert len(cht) == 1
    assert cht.query(1) == 7

    cht.add_line(2, 10) # parallel and higher, should replace previous
    assert cht.query(1) == 12

def test_cht_empty():
    cht = ConvexHullTrick()
    with pytest.raises(ValueError):
        cht.query(10)
