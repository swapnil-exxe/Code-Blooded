import pytest
from algorithms.suffix_array import build_suffix_array, build_lcp_array

def test_suffix_array_and_kasai_lcp():
    s = "banana"
    sa = build_suffix_array(s)
    # Suffixes sorted: a (5), ana (3), anana (1), banana (0), na (4), nana (2)
    assert sa == [5, 3, 1, 0, 4, 2]

    lcp = build_lcp_array(s, sa)
    # LCPs between adjacent sorted suffixes:
    # LCP(a, ana) = 1
    # LCP(ana, anana) = 3
    # LCP(anana, banana) = 0
    # LCP(banana, na) = 0
    # LCP(na, nana) = 2
    assert lcp == [1, 3, 0, 0, 2]

def test_suffix_array_single_and_repeating():
    s = "aaaa"
    sa = build_suffix_array(s)
    assert sa == [3, 2, 1, 0]
    lcp = build_lcp_array(s, sa)
    assert lcp == [1, 2, 3]

def test_suffix_array_empty():
    assert build_suffix_array("") == []
    assert build_lcp_array("", []) == []
