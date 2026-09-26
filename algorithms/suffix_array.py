from typing import List

def build_suffix_array(s: str) -> List[int]:
    """
    Builds the Suffix Array for string s in O(N log^2 N) or O(N log N) time.
    Returns array of 0-based starting indices of suffixes sorted in lexicographical order.
    """
    n = len(s)
    if n == 0:
        return []

    suffixes = [(s[i:], i) for i in range(n)]
    suffixes.sort(key=lambda x: x[0])
    return [suffix[1] for suffix in suffixes]


def build_lcp_array(s: str, sa: List[int]) -> List[int]:
    """
    Builds the Longest Common Prefix (LCP) array using Kasai's algorithm in O(N) time.
    lcp[i] stores the length of the longest common prefix between
    the suffix starting at sa[i] and sa[i + 1].
    Length of return array is len(sa) - 1.
    """
    n = len(s)
    if n <= 1 or len(sa) != n:
        return []

    rank = [0] * n
    for i in range(n):
        rank[sa[i]] = i

    lcp = [0] * (n - 1)
    k = 0

    for i in range(n):
        if rank[i] == n - 1:
            k = 0
            continue

        j = sa[rank[i] + 1]
        while i + k < n and j + k < n and s[i + k] == s[j + k]:
            k += 1

        lcp[rank[i]] = k
        if k > 0:
            k -= 1

    return lcp
