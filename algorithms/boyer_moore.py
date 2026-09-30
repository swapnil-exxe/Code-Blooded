from typing import List, Dict

def build_bad_char_table(pattern: str) -> Dict[str, int]:
    """
    Builds the Bad Character Heuristic lookup table for pattern.
    bad_char[char] stores the last 0-based index of char in pattern.
    """
    bad_char = {}
    for i, char in enumerate(pattern):
        bad_char[char] = i
    return bad_char

def boyer_moore_search(text: str, pattern: str) -> List[int]:
    """
    Boyer-Moore string matching algorithm using Bad Character Heuristic.
    Matches pattern from right to left over text.
    Average Time Complexity: O(N / M) best, O(N + M) average.
    Returns list of 0-based starting indices where pattern occurs in text.
    """
    if not pattern or not text or len(pattern) > len(text):
        return []

    m = len(pattern)
    n = len(text)
    bad_char = build_bad_char_table(pattern)
    matches = []

    s = 0  # s is shift of pattern with respect to text
    while s <= n - m:
        j = m - 1

        # Match characters right-to-left
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1

        if j < 0:
            # Match found at shift s
            matches.append(s)
            # Shift pattern so next character aligns with last occurrence in pattern
            s += (m - bad_char.get(text[s + m], -1)) if s + m < n else 1
        else:
            # Shift pattern to align mismatched character in text with its last occurrence in pattern
            char_in_text = text[s + j]
            s += max(1, j - bad_char.get(char_in_text, -1))

    return matches
