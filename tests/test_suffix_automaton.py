import pytest
from algorithms.suffix_automaton import SuffixAutomaton

def test_sam_contains_substrings():
    text = "banana"
    sam = SuffixAutomaton(text)

    # Valid substrings
    for sub in ["", "b", "ba", "ban", "bana", "banan", "banana", "an", "ana", "anan", "anana", "na", "nan", "nana", "a"]:
        assert sam.contains(sub) is True

    # Invalid substrings
    for invalid in ["band", "bananas", "c", "ann", "nab"]:
        assert sam.contains(invalid) is False

def test_sam_distinct_substrings():
    # "aba" -> "", "a", "b", "ab", "ba", "aba" -> 5 non-empty distinct substrings
    sam = SuffixAutomaton("aba")
    assert sam.count_distinct_substrings() == 5

    # "aaaa" -> "a", "aa", "aaa", "aaaa" -> 4 distinct substrings
    sam_a = SuffixAutomaton("aaaa")
    assert sam_a.count_distinct_substrings() == 4

    # "banana" -> 15 distinct substrings
    # ("a", "b", "n", "an", "ba", "na", "ana", "ban", "nan", "anan", "bana", "nana", "anana", "banan", "banana")
    sam_ban = SuffixAutomaton("banana")
    assert sam_ban.count_distinct_substrings() == 15

def test_sam_count_occurrences():
    text = "abracadabra"
    sam = SuffixAutomaton(text)

    assert sam.count_occurrences("a") == 5
    assert sam.count_occurrences("abra") == 2
    assert sam.count_occurrences("cadabra") == 1
    assert sam.count_occurrences("xyz") == 0
    assert sam.count_occurrences("") == 0

def test_sam_longest_common_substring():
    s1 = "abracadabra"
    s2 = "cadabrazzz"
    sam = SuffixAutomaton(s1)

    lcs = sam.longest_common_substring(s2)
    assert lcs == "cadabra"

    assert sam.longest_common_substring("xyz") == ""

def test_sam_exceptions():
    sam = SuffixAutomaton()
    with pytest.raises(ValueError):
        sam.extend("multiple")
