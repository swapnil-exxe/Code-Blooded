from typing import List

def manacher_palindromes(s: str) -> List[int]:
    """
    Computes palindrome radius array P using Manacher's algorithm in O(N) time.
    Transforms s by inserting '#' delimiters so odd and even palindromes are handled uniformly.
    """
    if not s:
        return []

    # Transform string: e.g. "aba" -> "^#a#b#a#$"
    t = "^#" + "#".join(s) + "#$"
    n = len(t)
    p = [0] * n
    c = 0  # Center of current rightmost palindrome
    r = 0  # Right boundary of current rightmost palindrome

    for i in range(1, n - 1):
        i_mirror = 2 * c - i

        if r > i:
            p[i] = min(r - i, p[i_mirror])

        # Expand palindrome centered at i
        while t[i + 1 + p[i]] == t[i - 1 - p[i]]:
            p[i] += 1

        # Update center and right boundary if palindrome expands past r
        if i + p[i] > r:
            c = i
            r = i + p[i]

    return p

def longest_palindromic_substring(s: str) -> str:
    """Returns the longest palindromic substring in O(N) time."""
    if not s:
        return ""

    p = manacher_palindromes(s)
    max_len = 0
    center_idx = 0

    for i in range(1, len(p) - 1):
        if p[i] > max_len:
            max_len = p[i]
            center_idx = i

    start = (center_idx - max_len) // 2
    return s[start : start + max_len]
