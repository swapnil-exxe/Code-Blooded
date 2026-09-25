import pytest
from algorithms.rabin_karp import rabin_karp_search

def test_rabin_karp_single_and_multiple_matches():
    text = "AABAACAADAABAABA"
    pattern = "AABA"
    assert rabin_karp_search(text, pattern) == [0, 9, 12]

def test_rabin_karp_no_match():
    text = "ABCDEFG"
    pattern = "XYZ"
    assert rabin_karp_search(text, pattern) == []

def test_rabin_karp_edge_cases():
    assert rabin_karp_search("", "PATTERN") == []
    assert rabin_karp_search("TEXT", "") == []
    assert rabin_karp_search("SHORT", "LONGER_PATTERN") == []
    assert rabin_karp_search("EXACT", "EXACT") == [0]

def test_rabin_karp_overlapping_matches():
    assert rabin_karp_search("AAAAA", "AAA") == [0, 1, 2]
