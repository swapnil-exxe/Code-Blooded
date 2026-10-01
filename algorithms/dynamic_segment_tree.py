from typing import Optional

class DynamicSegmentNode:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end
        self.val = 0
        self.left: Optional['DynamicSegmentNode'] = None
        self.right: Optional['DynamicSegmentNode'] = None

class DynamicSegmentTree:
    """
    Dynamic Segment Tree (Implicit Segment Tree).
    Allocates tree nodes dynamically on demand for sparse coordinate ranges up to [1, 10^9].
    """

    def __init__(self, start: int = 1, end: int = 10**9):
        if start > end:
            raise ValueError(f"Invalid range [{start}, {end}].")
        self.root = DynamicSegmentNode(start, end)

    def update(self, index: int, delta: int, node: Optional[DynamicSegmentNode] = None) -> None:
        """Adds delta to point at index in O(log(RANGE)) time."""
        curr = node if node is not None else self.root

        if curr.start == curr.end:
            curr.val += delta
            return

        mid = (curr.start + curr.end) // 2
        if index <= mid:
            if curr.left is None:
                curr.left = DynamicSegmentNode(curr.start, mid)
            self.update(index, delta, curr.left)
        else:
            if curr.right is None:
                curr.right = DynamicSegmentNode(mid + 1, curr.end)
            self.update(index, delta, curr.right)

        curr.val = (curr.left.val if curr.left else 0) + (curr.right.val if curr.right else 0)

    def query(self, left: int, right: int, node: Optional[DynamicSegmentNode] = None) -> int:
        """Returns range sum in [left, right] inclusive in O(log(RANGE)) time."""
        curr = node if node is not None else self.root

        if curr is None or left > curr.end or right < curr.start:
            return 0

        if left <= curr.start and curr.end <= right:
            return curr.val

        res = 0
        if curr.left:
            res += self.query(left, right, curr.left)
        if curr.right:
            res += self.query(left, right, curr.right)
        return res
