from typing import List

def rabin_karp_search(text: str, pattern: str, prime: int = 101, base: int = 256) -> List[int]:
    """
    Rabin-Karp string matching algorithm using polynomial rolling hash.
    Average Time Complexity: O(N + M)
    Worst-case Time Complexity: O(N * M)
    Space Complexity: O(1)

    Returns list of 0-based starting indices where pattern matches text.
    """
    if not pattern or not text or len(pattern) > len(text):
        return []

    m = len(pattern)
    n = len(text)
    matches = []

    # h = pow(base, m - 1) % prime
    h = 1
    for _ in range(m - 1):
        h = (h * base) % prime

    p_hash = 0  # Hash value for pattern
    t_hash = 0  # Hash value for text sliding window

    # Calculate initial hash for pattern and first window of text
    for i in range(m):
        p_hash = (base * p_hash + ord(pattern[i])) % prime
        t_hash = (base * t_hash + ord(text[i])) % prime

    # Slide pattern over text
    for i in range(n - m + 1):
        if p_hash == t_hash:
            # Check characters on hash match to prevent collision false positives
            if text[i:i + m] == pattern:
                matches.append(i)

        if i < n - m:
            t_hash = (base * (t_hash - ord(text[i]) * h) + ord(text[i + m])) % prime
            if t_hash < 0:
                t_hash += prime

    return matches
