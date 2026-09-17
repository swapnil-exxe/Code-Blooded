from typing import List, Union

class FenwickTree:
    """
    Binary Indexed Tree (Fenwick Tree) providing O(log N) point updates
    and prefix sum queries over a 1-indexed array structure.
    """

    def __init__(self, size_or_arr: Union[int, List[int]]):
        if isinstance(size_or_arr, int):
            if size_or_arr <= 0:
                raise ValueError("FenwickTree size must be greater than zero.")
            self.size = size_or_arr
            self.tree = [0] * (self.size + 1)
        elif isinstance(size_or_arr, list):
            if not size_or_arr:
                raise ValueError("FenwickTree array must not be empty.")
            self.size = len(size_or_arr)
            self.tree = [0] * (self.size + 1)
            for idx, val in enumerate(size_or_arr, 1):
                self.update(idx, val)
        else:
            raise TypeError("Expected int size or list of numbers.")

    def update(self, index: int, delta: int) -> None:
        """Adds delta to element at 1-based index in O(log N) time."""
        if index < 1 or index > self.size:
            raise IndexError(f"Index {index} out of bounds for FenwickTree of size {self.size}.")
        
        while index <= self.size:
            self.tree[index] += delta
            index += index & (-index)

    def query(self, index: int) -> int:
        """Returns prefix sum from index 1 to index (inclusive) in O(log N) time."""
        if index < 0 or index > self.size:
            raise IndexError(f"Index {index} out of bounds for FenwickTree of size {self.size}.")
        
        total = 0
        while index > 0:
            total += self.tree[index]
            index -= index & (-index)
        return total

    def range_query(self, left: int, right: int) -> int:
        """Returns sum of elements in 1-based range [left, right] inclusive in O(log N) time."""
        if left < 1 or right > self.size or left > right:
            raise IndexError(f"Invalid range [{left}, {right}] for FenwickTree of size {self.size}.")
        
        return self.query(right) - self.query(left - 1)
