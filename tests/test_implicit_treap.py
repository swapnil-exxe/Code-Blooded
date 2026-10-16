import pytest
from algorithms.implicit_treap import ImplicitTreap

def test_implicit_treap_insert_and_to_list():
    treap = ImplicitTreap()
    assert len(treap) == 0

    treap.append(10)
    treap.append(20)
    treap.append(30)
    assert treap.to_list() == [10, 20, 30]
    assert len(treap) == 3

    treap.insert(1, 15)  # [10, 15, 20, 30]
    assert treap.to_list() == [10, 15, 20, 30]

    treap.insert(0, 5)   # [5, 10, 15, 20, 30]
    assert treap.to_list() == [5, 10, 15, 20, 30]

def test_implicit_treap_delete():
    treap = ImplicitTreap()
    for x in [1, 2, 3, 4, 5]:
        treap.append(x)

    val = treap.delete(2)  # delete index 2 (value 3)
    assert val == 3
    assert treap.to_list() == [1, 2, 4, 5]
    assert len(treap) == 4

def test_implicit_treap_range_sum():
    treap = ImplicitTreap()
    for x in [2, 4, 6, 8, 10]:
        treap.append(x)

    assert treap.range_sum(0, 4) == 30
    assert treap.range_sum(1, 3) == 4 + 6 + 8
    assert treap.range_sum(2, 2) == 6

def test_implicit_treap_range_reverse():
    treap = ImplicitTreap()
    for x in range(1, 7):
        treap.append(x)  # [1, 2, 3, 4, 5, 6]

    treap.reverse(1, 4)  # reverse [2, 3, 4, 5] -> [1, 5, 4, 3, 2, 6]
    assert treap.to_list() == [1, 5, 4, 3, 2, 6]
    assert treap.range_sum(1, 4) == 5 + 4 + 3 + 2

    treap.reverse(0, 5)  # reverse entire array
    assert treap.to_list() == [6, 2, 3, 4, 5, 1]

def test_implicit_treap_exceptions():
    treap = ImplicitTreap()
    with pytest.raises(IndexError):
        treap.insert(1, 10)
    with pytest.raises(IndexError):
        treap.delete(0)
    with pytest.raises(IndexError):
        treap.range_sum(0, 0)
    with pytest.raises(IndexError):
        treap.reverse(0, 1)
