import math
from typing import List, Tuple, Callable, Any

class SqrtDecomposition:
    """
    Square Root Decomposition data structure for efficient range queries
    and updates in O(sqrt(N)) time per operation.
    """

    def __init__(self, arr: List[int]):
        if not arr:
            raise ValueError("Array cannot be empty.")
        self.n = len(arr)
        self.arr = list(arr)
        self.block_size = max(1, int(math.isqrt(self.n)))
        self.num_blocks = (self.n + self.block_size - 1) // self.block_size
        self.block_sums = [0] * self.num_blocks
        self.lazy = [0] * self.num_blocks

        for i, val in enumerate(self.arr):
            self.block_sums[i // self.block_size] += val

    def point_update(self, idx: int, val: int) -> None:
        """Sets arr[idx] = val in O(1) time."""
        if not (0 <= idx < self.n):
            raise IndexError("Index out of bounds.")
        b = idx // self.block_size
        # Account for any lazy tag applied to the block
        diff = val - (self.arr[idx] + self.lazy[b])
        self.arr[idx] = val - self.lazy[b]
        self.block_sums[b] += diff

    def range_add(self, l: int, r: int, delta: int) -> None:
        """Adds delta to all elements in [l, r] in O(sqrt(N)) time."""
        if not (0 <= l <= r < self.n):
            raise IndexError("Invalid range boundaries.")

        b_left = l // self.block_size
        b_right = r // self.block_size

        if b_left == b_right:
            for i in range(l, r + 1):
                self.arr[i] += delta
            self.block_sums[b_left] += delta * (r - l + 1)
        else:
            # Partial left block
            end_left = (b_left + 1) * self.block_size
            for i in range(l, end_left):
                self.arr[i] += delta
            self.block_sums[b_left] += delta * (end_left - l)

            # Full intermediate blocks
            for b in range(b_left + 1, b_right):
                self.lazy[b] += delta
                self.block_sums[b] += delta * self.block_size

            # Partial right block
            start_right = b_right * self.block_size
            for i in range(start_right, r + 1):
                self.arr[i] += delta
            self.block_sums[b_right] += delta * (r - start_right + 1)

    def query_sum(self, l: int, r: int) -> int:
        """Returns the sum of elements in [l, r] in O(sqrt(N)) time."""
        if not (0 <= l <= r < self.n):
            raise IndexError("Invalid range boundaries.")

        b_left = l // self.block_size
        b_right = r // self.block_size
        total = 0

        if b_left == b_right:
            for i in range(l, r + 1):
                total += self.arr[i] + self.lazy[b_left]
        else:
            # Partial left block
            end_left = (b_left + 1) * self.block_size
            for i in range(l, end_left):
                total += self.arr[i] + self.lazy[b_left]

            # Full intermediate blocks
            for b in range(b_left + 1, b_right):
                total += self.block_sums[b]

            # Partial right block
            start_right = b_right * self.block_size
            for i in range(start_right, r + 1):
                total += self.arr[i] + self.lazy[b_right]

        return total


def mos_algorithm_distinct_count(arr: List[int], queries: List[Tuple[int, int]]) -> List[int]:
    """
    Mo's Algorithm for offline range distinct element counting in O((N + Q) * sqrt(N)).
    Each query is a tuple (l, r) 0-indexed inclusive.
    """
    if not arr:
        return []
    if not queries:
        return []

    n = len(arr)
    block_size = max(1, int(math.isqrt(n)))

    # Store query with original index: (l, r, original_query_idx)
    indexed_queries = [(q[0], q[1], i) for i, q in enumerate(queries)]

    # Sort using serpentine block order for cache locality and fewer pointer shifts
    def sort_key(q: Tuple[int, int, int]):
        b = q[0] // block_size
        return (b, q[1] if b % 2 == 0 else -q[1])

    indexed_queries.sort(key=sort_key)

    freq: dict[int, int] = {}
    distinct_count = 0
    cur_l = 0
    cur_r = -1
    ans = [0] * len(queries)

    def add(idx: int):
        nonlocal distinct_count
        val = arr[idx]
        count = freq.get(val, 0)
        if count == 0:
            distinct_count += 1
        freq[val] = count + 1

    def remove(idx: int):
        nonlocal distinct_count
        val = arr[idx]
        count = freq[val]
        if count == 1:
            distinct_count -= 1
            del freq[val]
        else:
            freq[val] = count - 1

    for l, r, q_idx in indexed_queries:
        if not (0 <= l <= r < n):
            raise IndexError("Query range out of bounds.")

        while cur_l > l:
            cur_l -= 1
            add(cur_l)
        while cur_r < r:
            cur_r += 1
            add(cur_r)
        while cur_l < l:
            remove(cur_l)
            cur_l += 1
        while cur_r > r:
            remove(cur_r)
            cur_r -= 1

        ans[q_idx] = distinct_count

    return ans
