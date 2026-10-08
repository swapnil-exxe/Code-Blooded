import pytest
from algorithms.ternary_search_tree import TernarySearchTree

def test_tst_basic_operations():
    tst = TernarySearchTree()
    assert len(tst) == 0

    tst.insert("cat", 1)
    tst.insert("cats", 2)
    tst.insert("up", 3)
    tst.insert("bug", 4)

    assert len(tst) == 4
    assert tst.search("cat") == 1
    assert tst.search("cats") == 2
    assert tst.search("up") == 3
    assert tst.search("bug") == 4
    assert tst.search("dog") is None

    assert tst.contains("cat") is True
    assert tst.contains("ca") is False

def test_tst_prefix_search():
    tst = TernarySearchTree()
    words = ["apple", "app", "application", "banana", "apply"]
    for w in words:
        tst.insert(w)

    assert tst.starts_with("app") is True
    assert tst.starts_with("ban") is True
    assert tst.starts_with("orange") is False

    assert tst.keys_with_prefix("appl") == ["apple", "application", "apply"]
    assert tst.keys_with_prefix("ban") == ["banana"]
    assert tst.keys_with_prefix("xyz") == []

def test_tst_wildcard_search():
    tst = TernarySearchTree()
    for w in ["cat", "cot", "cut", "bat", "cog", "car"]:
        tst.insert(w)

    assert tst.wildcard_search("c.t") == ["cat", "cot", "cut"]
    assert tst.wildcard_search(".at") == ["bat", "cat"]
    assert tst.wildcard_search("c..") == ["car", "cat", "cog", "cot", "cut"]

def test_tst_empty_and_error():
    tst = TernarySearchTree()
    with pytest.raises(ValueError):
        tst.insert("")
    assert tst.search("") is None
