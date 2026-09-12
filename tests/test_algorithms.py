import pytest
from algorithms.trie import Trie
from algorithms.avl_tree import AVLTree
from algorithms.lru_cache import LRUCache
from algorithms.segment_tree import SegmentTree

def test_trie_operations():
    trie = Trie()
    trie.insert("apple")
    trie.insert("app")
    trie.insert("application")
    trie.insert("bat")

    assert trie.search("apple") is True
    assert trie.search("app") is True
    assert trie.search("appl") is False
    assert trie.starts_with("app") is True

    words = trie.get_words_with_prefix("app")
    assert sorted(words) == ["app", "apple", "application"]

def test_avl_tree_balance():
    tree = AVLTree()
    root = None
    keys = [10, 20, 30, 40, 50, 25]

    for key in keys:
        root = tree.insert(root, key)

    assert tree.inorder_traversal(root) == [10, 20, 25, 30, 40, 50]
    assert tree.get_height(root) <= 3
    assert abs(tree.get_balance(root)) <= 1

def test_lru_cache():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1
    cache.put(3, 3)  # evicts key 2
    assert cache.get(2) == -1
    assert cache.get(3) == 3

def test_segment_tree():
    arr = [1, 3, 5, 7, 9, 11]
    st = SegmentTree(arr)
    # Range Sum Query (0, 2) -> 1 + 3 + 5 = 9
    assert st.query(0, 2) == 9
