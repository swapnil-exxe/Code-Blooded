import pytest
from algorithms.z_algorithm import compute_z_array, z_search

def test_compute_z_array():
    assert compute_z_array("aabzaa") == [0, 1, 0, 0, 2, 1]
    assert compute_z_array("aaaaa") == [0, 4, 3, 2, 1]
    assert compute_z_array("abc") == [0, 0, 0]
    assert compute_z_array("") == []

def test_z_search_single_and_multiple_occurrences():
    text = "baabaaab"
    pattern = "baa"
    assert z_search(text, pattern) == [0, 3]

    text2 = "aaaaa"
    pattern2 = "aa"
    assert z_search(text2, pattern2) == [0, 1, 2, 3]

def test_z_search_edge_cases():
    assert z_search("hello", "world") == []
    assert z_search("short", "longer_pattern") == []
    assert z_search("", "pattern") == []
    assert z_search("text", "") == []
