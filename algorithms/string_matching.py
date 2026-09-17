from typing import List

def compute_lps(pattern: str) -> List[int]:
    """
    Computes the Longest Prefix Suffix (LPS) table for the given pattern in O(M) time.
    lps[i] stores the length of the longest proper prefix of pattern[0...i]
    that is also a suffix of pattern[0...i].
    """
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps

def kmp_search(text: str, pattern: str) -> List[int]:
    """
    Knuth-Morris-Pratt (KMP) string matching algorithm.
    Returns a list of 0-based starting indices where pattern matches text in O(N + M) time.
    """
    if not pattern or not text or len(pattern) > len(text):
        return []

    lps = compute_lps(pattern)
    matches = []
    
    i = 0  # index for text
    j = 0  # index for pattern

    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == len(pattern):
            matches.append(i - j)
            j = lps[j - 1]
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return matches

def count_occurrences(text: str, pattern: str) -> int:
    """Returns total number of non-overlapping/overlapping occurrences of pattern in text."""
    return len(kmp_search(text, pattern))
