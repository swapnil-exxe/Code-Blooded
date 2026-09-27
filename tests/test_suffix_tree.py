import pytest
from algorithms.suffix_tree import SuffixTree

def test_suffix_tree_substring_search():
    st = SuffixTree("banana")

    assert st.contains_substring("banana") is True
    assert st.contains_substring("nan") is True
    assert st.contains_substring("ana") is True
    assert st.contains_substring("ban") is True
    assert st.contains_substring("apple") is False
    assert st.contains_substring("") is True

def test_suffix_tree_empty_string():
    with pytest.raises(ValueError):
        SuffixTree("")
