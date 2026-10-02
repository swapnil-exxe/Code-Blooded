import pytest
from algorithms.splay_tree import SplayTree

def test_splay_tree_insert_search_root_splay():
    st = SplayTree()
    keys = [50, 20, 80, 10, 30, 70, 90]
    for k in keys:
        st.insert(k)

    # Last inserted element (90) must be root
    assert st.root.key == 90
    assert st.inorder() == sorted(keys)

    # Search for 30 -> 30 becomes root
    assert st.search(30) is True
    assert st.root.key == 30

    assert st.search(999) is False

def test_splay_tree_delete():
    st = SplayTree()
    keys = [10, 20, 30, 40, 50]
    for k in keys:
        st.insert(k)

    assert st.delete(30) is True
    assert st.search(30) is False
    assert st.inorder() == [10, 20, 40, 50]
    assert st.delete(999) is False
