import random
from typing import Optional, Tuple, List

class TreapNode:
    def __init__(self, val: int, priority: Optional[float] = None):
        self.val = val
        self.priority = random.random() if priority is None else priority
        self.size = 1
        self.total = val
        self.lazy_rev = False
        self.left: Optional['TreapNode'] = None
        self.right: Optional['TreapNode'] = None

    def update(self) -> None:
        self.size = 1 + (self.left.size if self.left else 0) + (self.right.size if self.right else 0)
        self.total = self.val + (self.left.total if self.left else 0) + (self.right.total if self.right else 0)

    def push(self) -> None:
        if self.lazy_rev:
            self.left, self.right = self.right, self.left
            if self.left:
                self.left.lazy_rev = not self.left.lazy_rev
            if self.right:
                self.right.lazy_rev = not self.right.lazy_rev
            self.lazy_rev = False


class ImplicitTreap:
    """
    Implicit Treap (Cartesian Tree on array indices) supporting
    O(log N) dynamic insertions, deletions, range sum queries,
    and range reversals with lazy propagation.
    """

    def __init__(self):
        self.root: Optional[TreapNode] = None

    def __len__(self) -> int:
        return self.root.size if self.root else 0

    @staticmethod
    def _split(t: Optional[TreapNode], k: int) -> Tuple[Optional[TreapNode], Optional[TreapNode]]:
        """Splits t into t1 (first k elements) and t2 (remaining)."""
        if not t:
            return None, None
        t.push()
        left_sz = t.left.size if t.left else 0
        if left_sz >= k:
            l, r = ImplicitTreap._split(t.left, k)
            t.left = r
            t.update()
            return l, t
        else:
            l, r = ImplicitTreap._split(t.right, k - left_sz - 1)
            t.right = l
            t.update()
            return t, r

    @staticmethod
    def _merge(l: Optional[TreapNode], r: Optional[TreapNode]) -> Optional[TreapNode]:
        """Merges two treaps l and r."""
        if not l or not r:
            return l or r
        l.push()
        r.push()
        if l.priority > r.priority:
            l.right = ImplicitTreap._merge(l.right, r)
            l.update()
            return l
        else:
            r.left = ImplicitTreap._merge(l, r.left)
            r.update()
            return r

    def insert(self, idx: int, val: int) -> None:
        """Inserts val at index idx (0-indexed)."""
        if not (0 <= idx <= len(self)):
            raise IndexError("Insert index out of bounds.")
        l, r = self._split(self.root, idx)
        node = TreapNode(val)
        self.root = self._merge(self._merge(l, node), r)

    def append(self, val: int) -> None:
        """Appends val to the end of the array."""
        self.insert(len(self), val)

    def delete(self, idx: int) -> int:
        """Removes and returns the element at index idx (0-indexed)."""
        if not (0 <= idx < len(self)):
            raise IndexError("Delete index out of bounds.")
        l, r = self._split(self.root, idx)
        target, r_after = self._split(r, 1)
        self.root = self._merge(l, r_after)
        return target.val  # type: ignore

    def range_sum(self, l: int, r: int) -> int:
        """Computes sum of elements in [l, r] inclusive (0-indexed)."""
        if not (0 <= l <= r < len(self)):
            raise IndexError("Range query out of bounds.")
        t1, t2 = self._split(self.root, l)
        mid, t3 = self._split(t2, r - l + 1)
        res = mid.total if mid else 0
        self.root = self._merge(t1, self._merge(mid, t3))
        return res

    def reverse(self, l: int, r: int) -> None:
        """Reverses the subarray in [l, r] inclusive (0-indexed)."""
        if not (0 <= l <= r < len(self)):
            raise IndexError("Range reverse out of bounds.")
        t1, t2 = self._split(self.root, l)
        mid, t3 = self._split(t2, r - l + 1)
        if mid:
            mid.lazy_rev = not mid.lazy_rev
        self.root = self._merge(t1, self._merge(mid, t3))

    def to_list(self) -> List[int]:
        """Returns the elements as a standard Python list."""
        res: List[int] = []

        def _dfs(node: Optional[TreapNode]):
            if not node:
                return
            node.push()
            _dfs(node.left)
            res.append(node.val)
            _dfs(node.right)

        _dfs(self.root)
        return res
