import pytest
from algorithms.treap import Treap

def test_treap_insert_search_inorder():
    t = Treap()
    keys = [50, 30, 20, 40, 70, 60, 80]
    for k in keys:
        t.insert(k)

    assert t.is_valid_treap()
    assert t.inorder() == [20, 30, 40, 50, 60, 70, 80]

    for k in keys:
        assert t.search(k) is True
    assert t.search(100) is False

def test_treap_delete():
    t = Treap()
    keys = [10, 5, 15, 3, 7, 12, 18]
    for k in keys:
        t.insert(k)

    t.delete(10)
    assert t.search(10) is False
    assert t.is_valid_treap()
    assert t.inorder() == [3, 5, 7, 12, 15, 18]

def test_treap_custom_priorities():
    t = Treap()
    t.insert(10, priority=0.1)
    t.insert(20, priority=0.9)  # Higher priority -> 20 becomes root
    t.insert(5, priority=0.5)

    assert t.is_valid_treap()
    assert t.root.key == 20
    assert t.inorder() == [5, 10, 20]
