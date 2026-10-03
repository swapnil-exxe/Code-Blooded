import math
from typing import List, Callable, Any

class SparseTable:
    """
    Sparse Table data structure for idempotent range queries (e.g. min, max, gcd).
    Preprocessing Time: O(N log N)
    Query Time: O(1)
    """

    def __init__(self, arr: List[Any], func: Callable[[Any, Any], Any] = min):
        if not arr:
            raise ValueError("Array cannot be empty.")
        self.n = len(arr)
        self.func = func
        self.k = math.floor(math.log2(self.n)) + 1
        self.table: List[List[Any]] = [[None] * self.n for _ in range(self.k)]

        # Base level 0
        for i in range(self.n):
            self.table[0][i] = arr[i]

        # Compute higher levels: table[j][i] covers interval [i, i + 2^j - 1]
        for j in range(1, self.k):
            length = 1 << (j - 1)
            for i in range(self.n - (1 << j) + 1):
                self.table[j][i] = self.func(self.table[j - 1][i], self.table[j - 1][i + length])

    def query(self, left: int, right: int) -> Any:
        """Returns the result of combining elements in range [left, right] inclusive in O(1) time."""
        if not (0 <= left <= right < self.n):
            raise IndexError(f"Invalid range [{left}, {right}] for array of length {self.n}.")

        length = right - left + 1
        j = math.floor(math.log2(length))
        return self.func(self.table[j][left], self.table[j][right - (1 << j) + 1])
