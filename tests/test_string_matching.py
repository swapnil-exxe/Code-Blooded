import pytest
from algorithms.string_matching import compute_lps, kmp_search, count_occurrences

def test_compute_lps():
    assert compute_lps("AAAA") == [0, 1, 2, 3]
    assert compute_lps("ABCDE") == [0, 0, 0, 0, 0]
    assert compute_lps("AABAACAABAA") == [0, 1, 0, 1, 2, 0, 1, 2, 3, 4, 5]

def test_kmp_search_single_and_multiple_matches():
    text = "ABABDABACDABABCABAB"
    pattern = "ABABCABAB"
    matches = kmp_search(text, pattern)
    assert matches == [10]

    text2 = "AABAACAADAABAABA"
    pattern2 = "AABA"
    assert kmp_search(text2, pattern2) == [0, 9, 12]

def test_kmp_search_edge_cases():
    assert kmp_search("SHORT", "LONGER_PATTERN") == []
    assert kmp_search("", "PATTERN") == []
    assert kmp_search("TEXT", "") == []
    assert kmp_search("AAAAA", "AAA") == [0, 1, 2]

def test_count_occurrences():
    assert count_occurrences("ABABAB", "AB") == 3
    assert count_occurrences("XYZ", "ABC") == 0
