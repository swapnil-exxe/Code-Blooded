import pytest
from algorithms.boyer_moore import boyer_moore_search, build_bad_char_table

def test_build_bad_char_table():
    table = build_bad_char_table("ABA")
    assert table == {"A": 2, "B": 1}

def test_boyer_moore_single_and_multiple_matches():
    text = "ABAAABCDABC"
    pattern = "ABC"
    matches = boyer_moore_search(text, pattern)
    assert matches == [4, 8]

def test_boyer_moore_edge_cases():
    assert boyer_moore_search("hello", "world") == []
    assert boyer_moore_search("short", "longer_pattern") == []
    assert boyer_moore_search("", "pattern") == []
    assert boyer_moore_search("text", "") == []
    assert boyer_moore_search("aaaaa", "aa") == [0, 1, 2, 3]
