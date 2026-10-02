from typing import List

class BitVector:
    """Helper bit vector for Wavelet Matrix level queries."""
    def __init__(self, bits: List[int]):
        self.bits = bits[:]
        self.prefix_ones = [0] * (len(bits) + 1)
        for i, b in enumerate(bits):
            self.prefix_ones[i + 1] = self.prefix_ones[i] + (1 if b else 0)

    def access(self, idx: int) -> int:
        return self.bits[idx]

    def rank1(self, idx: int) -> int:
        """Returns count of 1s in prefix [0, idx)."""
        return self.prefix_ones[idx]

    def rank0(self, idx: int) -> int:
        """Returns count of 0s in prefix [0, idx)."""
        return idx - self.prefix_ones[idx]

class WaveletMatrix:
    """
    Wavelet Matrix data structure for range quantile (k-th smallest)
    and rank frequency queries in O(log Sigma) time per query.
    """

    def __init__(self, arr: List[int]):
        if not arr:
            raise ValueError("Array cannot be empty.")
        if any(x < 0 for x in arr):
            raise ValueError("WaveletMatrix supports non-negative integers.")

        self.n = len(arr)
        self.max_val = max(arr) if arr else 0
        self.max_bits = self.max_val.bit_length() if self.max_val > 0 else 1

        self.arr = arr[:]
        self.levels: List[BitVector] = []
        self.zeros_count: List[int] = []

        cur = arr[:]
        for b in range(self.max_bits - 1, -1, -1):
            bits = [(val >> b) & 1 for val in cur]
            bv = BitVector(bits)
            self.levels.append(bv)

            zeros = [val for val in cur if ((val >> b) & 1) == 0]
            ones = [val for val in cur if ((val >> b) & 1) == 1]
            self.zeros_count.append(len(zeros))
            cur = zeros + ones

    def access(self, idx: int) -> int:
        """Returns element at 0-based index."""
        if not (0 <= idx < self.n):
            raise IndexError(f"Index {idx} out of bounds.")
        return self.arr[idx]

    def rank(self, val: int, i: int) -> int:
        """Returns number of occurrences of val in prefix [0, i)."""
        if i <= 0:
            return 0
        if i > self.n:
            i = self.n

        l, r = 0, i
        for level_idx in range(self.max_bits):
            bv = self.levels[level_idx]
            z_cnt = self.zeros_count[level_idx]
            bit = (val >> (self.max_bits - 1 - level_idx)) & 1

            if bit == 0:
                l = bv.rank0(l)
                r = bv.rank0(r)
            else:
                l = z_cnt + bv.rank1(l)
                r = z_cnt + bv.rank1(r)

        return r - l

    def quantile(self, left: int, right: int, k: int) -> int:
        """
        Returns the k-th smallest element (0-indexed) in range [left, right] inclusive.
        0 <= k <= right - left.
        """
        if not (0 <= left <= right < self.n):
            raise IndexError(f"Invalid range [{left}, {right}].")
        if not (0 <= k <= right - left):
            raise ValueError(f"k={k} out of range for range size {right - left + 1}.")

        l, r = left, right + 1
        val = 0

        for level_idx in range(self.max_bits):
            bv = self.levels[level_idx]
            z_cnt = self.zeros_count[level_idx]

            zeros_in_range = bv.rank0(r) - bv.rank0(l)

            if k < zeros_in_range:
                l = bv.rank0(l)
                r = bv.rank0(r)
            else:
                val |= (1 << (self.max_bits - 1 - level_idx))
                k -= zeros_in_range
                l = z_cnt + bv.rank1(l)
                r = z_cnt + bv.rank1(r)

        return val
