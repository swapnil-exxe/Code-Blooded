import pytest
from algorithms.scapegoat_tree import ScapegoatTree

def test_scapegoat_tree_insert_search_inorder():
    sgt = ScapegoatTree(alpha=0.6)
    # Insert in strictly increasing order (would degrade regular BST to linked list)
    keys = list(range(1, 20))
    for k in keys:
        sgt.insert(k)

    assert sgt.inorder() == keys
    for k in keys:
        assert sgt.search(k) is True
    assert sgt.search(999) is False

def test_scapegoat_tree_delete():
    sgt = ScapegoatTree(alpha=2.0 / 3.0)
    keys = [15, 10, 20, 8, 12, 18, 25]
    for k in keys:
        sgt.insert(k)

    assert sgt.delete(10) is True
    assert sgt.search(10) is False
    assert sgt.inorder() == [8, 12, 15, 18, 20, 25]
    assert sgt.delete(999) is False

def test_scapegoat_tree_invalid_alpha():
    with pytest.raises(ValueError):
        ScapegoatTree(alpha=0.4)
    with pytest.raises(ValueError):
        ScapegoatTree(alpha=1.0)
