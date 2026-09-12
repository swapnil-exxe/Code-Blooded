import pytest
from algorithms.avl_tree import AVLTree
from algorithms.red_black_tree import RedBlackTree
from utils.tree_analyzer import analyze_tree_structure

def test_tree_analyzer_avl():
    tree = AVLTree()
    root = None
    for k in [10, 20, 30, 40, 50]:
        root = tree.insert(root, k)

    stats = analyze_tree_structure(root)
    assert stats["total_nodes"] == 5
    assert stats["max_height"] == 3
    assert stats["leaf_count"] >= 2
    assert stats["is_balanced"] is True

def test_tree_analyzer_rbt():
    rbt = RedBlackTree()
    for k in [5, 15, 25, 35, 45]:
        rbt.insert(k)

    stats = analyze_tree_structure(rbt.root)
    assert stats["total_nodes"] == 5
    assert stats["max_height"] <= 3
    assert stats["is_balanced"] is True
