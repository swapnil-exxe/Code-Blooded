from typing import List, Union

class RangeFenwickTree:
    """
    Binary Indexed Tree supporting both Range Updates and Range Queries in O(log N) time.
    Uses two internal Fenwick trees:
    tree1 maintains difference D[i]
    tree2 maintains D[i] * (i - 1)
    Prefix sum up to p is: p * query(tree1, p) - query(tree2, p)
    """

    def __init__(self, size_or_arr: Union[int, List[int]]):
        if isinstance(size_or_arr, int):
            if size_or_arr <= 0:
                raise ValueError("Size must be greater than zero.")
            self.n = size_or_arr
            self.tree1 = [0] * (self.n + 1)
            self.tree2 = [0] * (self.n + 1)
        elif isinstance(size_or_arr, list):
            if not size_or_arr:
                raise ValueError("Array must not be empty.")
            self.n = len(size_or_arr)
            self.tree1 = [0] * (self.n + 1)
            self.tree2 = [0] * (self.n + 1)
            for idx, val in enumerate(size_or_arr, 1):
                self.range_update(idx, idx, val)
        else:
            raise TypeError("Expected int size or list of numbers.")

    def _update_single(self, tree: List[int], idx: int, val: int) -> None:
        while idx <= self.n:
            tree[idx] += val
            idx += idx & (-idx)

    def _query_single(self, tree: List[int], idx: int) -> int:
        total = 0
        while idx > 0:
            total += tree[idx]
            idx -= idx & (-idx)
        return total

    def range_update(self, left: int, right: int, val: int) -> None:
        """Adds val to all elements in 1-based range [left, right] inclusive."""
        if not (1 <= left <= right <= self.n):
            raise IndexError(f"Invalid range [{left}, {right}] for size {self.n}.")

        self._update_single(self.tree1, left, val)
        self._update_single(self.tree1, right + 1, -val)

        self._update_single(self.tree2, left, val * (left - 1))
        self._update_single(self.tree2, right + 1, -val * right)

    def prefix_query(self, p: int) -> int:
        """Returns prefix sum from index 1 to p inclusive in O(log N) time."""
        if p < 0 or p > self.n:
            raise IndexError(f"Index {p} out of bounds for size {self.n}.")
        return p * self._query_single(self.tree1, p) - self._query_single(self.tree2, p)

    def range_query(self, left: int, right: int) -> int:
        """Returns range sum in 1-based range [left, right] inclusive in O(log N) time."""
        if not (1 <= left <= right <= self.n):
            raise IndexError(f"Invalid range [{left}, {right}] for size {self.n}.")
        return self.prefix_query(right) - self.prefix_query(left - 1)
