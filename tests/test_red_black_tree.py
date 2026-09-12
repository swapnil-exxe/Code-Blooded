import pytest
import random
import time
from algorithms.red_black_tree import RedBlackTree, Color

def test_red_black_tree_basic_insertion():
    rbt = RedBlackTree()
    keys = [20, 15, 25, 10, 5, 1, 30, 17]
    for key in keys:
        rbt.insert(key)

    assert rbt.inorder_traversal() == sorted(keys)
    assert rbt.search(15) is True
    assert rbt.search(100) is False

def test_red_black_tree_invariants():
    rbt = RedBlackTree()
    # Insert 100 random numbers and verify invariants after each insertion
    random.seed(42)
    sample_keys = random.sample(range(1, 1000), 100)

    for k in sample_keys:
        rbt.insert(k)
        assert rbt.verify_properties() is True

    assert rbt.root.color == Color.BLACK
    assert rbt.inorder_traversal() == sorted(sample_keys)

def test_red_black_tree_benchmark():
    rbt = RedBlackTree()
    num_elements = 5000
    data = list(range(num_elements))

    start = time.perf_counter()
    for item in data:
        rbt.insert(item)
    elapsed = time.perf_counter() - start

    assert elapsed < 1.0  # Insertion should take less than 1 second for 5k items
    assert rbt.verify_properties() is True
