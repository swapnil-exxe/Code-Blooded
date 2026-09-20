from typing import List

def compute_z_array(s: str) -> List[int]:
    """
    Computes the Z-array for string s in O(N) time using Z-box sliding window [L, R].
    Z[i] is the length of the longest substring starting from s[i]
    that is also a prefix of s.
    Z[0] is set to 0 by convention.
    """
    n = len(s)
    if n == 0:
        return []

    z = [0] * n
    l, r = 0, 0

    for i in range(1, n):
        if i <= r:
            z[i] = min(r - i + 1, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] - 1 > r:
            l = i
            r = i + z[i] - 1

    return z

def z_search(text: str, pattern: str) -> List[int]:
    """
    Performs string matching using the Z-algorithm in O(N + M) time.
    Concatenates pattern + '$' + text and computes the Z-array.
    Returns list of 0-based starting indices in text.
    """
    if not pattern or not text or len(pattern) > len(text):
        return []

    # Use delimiter that doesn't appear in text or pattern
    concat = pattern + '$' + text
    m = len(pattern)
    z = compute_z_array(concat)

    matches = []
    for i in range(m + 1, len(concat)):
        if z[i] == m:
            matches.append(i - (m + 1))

    return matches
