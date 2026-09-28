import pytest
from algorithms.manacher import longest_palindromic_substring, manacher_palindromes

def test_manacher_odd_and_even_palindromes():
    assert longest_palindromic_substring("babad") in ["bab", "aba"]
    assert longest_palindromic_substring("cbbd") == "bb"
    assert longest_palindromic_substring("racecar") == "racecar"

def test_manacher_edge_cases():
    assert longest_palindromic_substring("") == ""
    assert longest_palindromic_substring("a") == "a"
    assert longest_palindromic_substring("aaaaa") == "aaaaa"
    assert longest_palindromic_substring("abcde") in ["a", "b", "c", "d", "e"]
