import pytest
from algorithms.aho_corasick import AhoCorasick

def test_aho_corasick_multi_pattern_search():
    patterns = ["he", "she", "his", "hers"]
    text = "ushers"

    ac = AhoCorasick(patterns)
    matches = ac.search(text)

    # In "ushers":
    # "she" ends at index 3 (u-s-h-e) -> (3, "she")
    # "he" ends at index 3 -> (3, "he")
    # "hers" ends at index 5 -> (5, "hers")
    matched_patterns = [p for idx, p in matches]
    assert "she" in matched_patterns
    assert "he" in matched_patterns
    assert "hers" in matched_patterns
    assert "his" not in matched_patterns

def test_aho_corasick_no_matches():
    ac = AhoCorasick(["cat", "dog"])
    assert ac.search("bird fish") == []

def test_aho_corasick_invalid_patterns():
    with pytest.raises(ValueError):
        AhoCorasick([])
