from collections import deque
from typing import List, Dict, Tuple

class AhoCorasickNode:
    def __init__(self):
        self.children: Dict[str, 'AhoCorasickNode'] = {}
        self.fail: 'AhoCorasickNode' = self
        self.output: List[str] = []

class AhoCorasick:
    """
    Aho-Corasick Multi-Pattern String Searching Automaton.
    Constructs Trie + BFS Failure Links for searching K dictionary patterns
    in text of length N in O(N + sum(M_i) + K) time.
    """

    def __init__(self, patterns: List[str]):
        if not patterns:
            raise ValueError("Patterns list cannot be empty.")
        
        self.root = AhoCorasickNode()
        self.patterns = patterns

        # 1. Build Trie
        for pattern in patterns:
            if not pattern:
                continue
            curr = self.root
            for char in pattern:
                if char not in curr.children:
                    curr.children[char] = AhoCorasickNode()
                curr = curr.children[char]
            curr.output.append(pattern)

        # 2. Build Failure Links via BFS
        self._build_failure_links()

    def _build_failure_links(self) -> None:
        queue = deque()

        for child in self.root.children.values():
            child.fail = self.root
            queue.append(child)

        while queue:
            curr = queue.popleft()

            for char, child in curr.children.items():
                fail_state = curr.fail
                while fail_state != self.root and char not in fail_state.children:
                    fail_state = fail_state.fail

                if char in fail_state.children and fail_state.children[char] != child:
                    child.fail = fail_state.children[char]
                else:
                    child.fail = self.root

                child.output.extend(child.fail.output)
                queue.append(child)

    def search(self, text: str) -> List[Tuple[int, str]]:
        """
        Searches text for all matching dictionary patterns.
        Returns list of tuples (end_index_in_text, pattern_string).
        """
        results = []
        curr = self.root

        for i, char in enumerate(text):
            while curr != self.root and char not in curr.children:
                curr = curr.fail

            if char in curr.children:
                curr = curr.children[char]

            for pattern in curr.output:
                results.append((i, pattern))

        return results
