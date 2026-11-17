from typing import Dict, Optional, List

class SAMState:
    def __init__(self, length: int = 0, link: int = -1):
        self.len = length
        self.link = link
        self.next: Dict[str, int] = {}
        self.endpos_size = 0  # number of occurrences in original text


class SuffixAutomaton:
    """
    Suffix Automaton (Directed Acyclic Word Graph - DAWG) representing all substrings
    of a string in linear O(N) states and transitions.
    Supports O(M) substring queries, O(N) distinct substring counting,
    and O(M) Longest Common Substring (LCS) discovery.
    """

    def __init__(self, s: Optional[str] = None):
        self.states: List[SAMState] = [SAMState(length=0, link=-1)]
        self.last = 0
        self._is_dp_ready = False

        if s:
            for char in s:
                self.extend(char)

    def __len__(self) -> int:
        """Returns total number of states in automaton."""
        return len(self.states)

    def extend(self, c: str) -> None:
        """Appends character c to the automaton in amortized O(1) time."""
        if len(c) != 1:
            raise ValueError("Can only extend by a single character.")

        cur = len(self.states)
        self.states.append(SAMState(length=self.states[self.last].len + 1, link=0))
        self.states[cur].endpos_size = 1

        p = self.last
        while p != -1 and c not in self.states[p].next:
            self.states[p].next[c] = cur
            p = self.states[p].link

        if p == -1:
            self.states[cur].link = 0
        else:
            q = self.states[p].next[c]
            if self.states[p].len + 1 == self.states[q].len:
                self.states[cur].link = q
            else:
                clone = len(self.states)
                clone_state = SAMState(length=self.states[p].len + 1, link=self.states[q].link)
                clone_state.next = dict(self.states[q].next)
                clone_state.endpos_size = 0
                self.states.append(clone_state)

                while p != -1 and self.states[p].next.get(c) == q:
                    self.states[p].next[c] = clone
                    p = self.states[p].link

                self.states[q].link = clone
                self.states[cur].link = clone

        self.last = cur
        self._is_dp_ready = False

    def contains(self, sub: str) -> bool:
        """Checks if substring exists in the automaton in O(|sub|) time."""
        curr = 0
        for c in sub:
            if c not in self.states[curr].next:
                return False
            curr = self.states[curr].next[c]
        return True

    def count_distinct_substrings(self) -> int:
        """
        Counts total number of distinct substrings in O(states) time.
        Each state contributes (len(state) - len(link(state))) substrings.
        """
        total = 0
        for i in range(1, len(self.states)):
            link = self.states[i].link
            parent_len = self.states[link].len if link != -1 else 0
            total += self.states[i].len - parent_len
        return total

    def _prepare_dp(self) -> None:
        """Topologically sorts states by length to calculate endpos sizes."""
        if self._is_dp_ready:
            return

        # Bucket sort states by length
        max_len = max(s.len for s in self.states)
        buckets: List[List[int]] = [[] for _ in range(max_len + 1)]
        for idx, s in enumerate(self.states):
            buckets[s.len].append(idx)

        # Propagate endpos_size up the suffix link tree in descending length order
        for length in range(max_len, 0, -1):
            for u in buckets[length]:
                p = self.states[u].link
                if p != -1:
                    self.states[p].endpos_size += self.states[u].endpos_size

        self._is_dp_ready = True

    def count_occurrences(self, sub: str) -> int:
        """Returns the number of occurrences of sub in the original string in O(|sub|)."""
        if not sub:
            return 0
        self._prepare_dp()
        curr = 0
        for c in sub:
            if c not in self.states[curr].next:
                return 0
            curr = self.states[curr].next[c]
        return self.states[curr].endpos_size

    def longest_common_substring(self, other: str) -> str:
        """
        Finds the Longest Common Substring (LCS) between the indexed string and other.
        Runs in O(|other|) time.
        """
        curr = 0
        cur_len = 0
        best_len = 0
        best_end = 0

        for i, c in enumerate(other):
            while curr != 0 and c not in self.states[curr].next:
                curr = self.states[curr].link
                cur_len = self.states[curr].len

            if c in self.states[curr].next:
                curr = self.states[curr].next[c]
                cur_len += 1
            else:
                curr = 0
                cur_len = 0

            if cur_len > best_len:
                best_len = cur_len
                best_end = i

        return other[best_end - best_len + 1 : best_end + 1] if best_len > 0 else ""
