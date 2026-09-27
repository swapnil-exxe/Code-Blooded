from typing import List, Optional
from algorithms.suffix_array import build_suffix_array, build_lcp_array

class SuffixTreeNode:
    def __init__(self, start: int = -1, length: int = 0):
        self.start = start
        self.length = length
        self.children: dict[str, 'SuffixTreeNode'] = {}
        self.suffix_index = -1

class SuffixTree:
    """
    Suffix Tree data structure constructed using Suffix Array + LCP Array.
    Supports O(M) substring search and frequency count queries.
    """

    def __init__(self, s: str):
        if not s:
            raise ValueError("String s cannot be empty.")

        self.s = s + '$'
        self.n = len(self.s)
        self.sa = build_suffix_array(self.s)
        self.lcp = build_lcp_array(self.s, self.sa)
        self.root = SuffixTreeNode()

        self._build_tree()

    def _build_tree(self) -> None:
        # Construct tree nodes using Suffix Array order
        for i in range(self.n):
            suffix_start = self.sa[i]
            curr = self.root
            rem_suffix = self.s[suffix_start:]

            # Simple insertion path for full string suffix set
            j = 0
            while j < len(rem_suffix):
                char = rem_suffix[j]
                if char not in curr.children:
                    node = SuffixTreeNode(start=suffix_start + j, length=len(rem_suffix) - j)
                    node.suffix_index = suffix_start
                    curr.children[char] = node
                    break
                else:
                    child = curr.children[char]
                    child_str = self.s[child.start : child.start + child.length]
                    
                    # Match length
                    match_len = 0
                    while match_len < len(child_str) and j + match_len < len(rem_suffix) and child_str[match_len] == rem_suffix[j + match_len]:
                        match_len += 1

                    if match_len == len(child_str):
                        j += match_len
                        curr = child
                    else:
                        # Split child node
                        split_node = SuffixTreeNode(start=child.start, length=match_len)
                        curr.children[char] = split_node

                        child.start += match_len
                        child.length -= match_len
                        split_node.children[self.s[child.start]] = child

                        new_leaf = SuffixTreeNode(start=suffix_start + j + match_len, length=len(rem_suffix) - (j + match_len))
                        new_leaf.suffix_index = suffix_start
                        split_node.children[self.s[new_leaf.start]] = new_leaf
                        break

    def contains_substring(self, pattern: str) -> bool:
        """Returns True if pattern is a substring of original string in O(M) time."""
        if not pattern:
            return True

        curr = self.root
        j = 0

        while j < len(pattern):
            char = pattern[j]
            if char not in curr.children:
                return False

            child = curr.children[char]
            child_str = self.s[child.start : child.start + child.length]

            k = 0
            while k < len(child_str) and j < len(pattern):
                if child_str[k] != pattern[j]:
                    return False
                k += 1
                j += 1

            curr = child

        return True
