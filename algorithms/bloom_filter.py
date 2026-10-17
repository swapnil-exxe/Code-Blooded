import math
import hashlib
from typing import Any

class BloomFilter:
    """
    Space-efficient probabilistic data structure for set membership testing.
    Uses double-hashing (Kirsch-Mitzenmacher technique) to generate k hash functions
    from two 64-bit halves of an MD5 digest.
    """

    def __init__(self, expected_elements: int, false_positive_rate: float = 0.01):
        if expected_elements <= 0:
            raise ValueError("Expected elements must be greater than 0.")
        if not (0.0 < false_positive_rate < 1.0):
            raise ValueError("False positive rate must be strictly between 0 and 1.")

        self.expected_elements = expected_elements
        self.false_positive_rate = false_positive_rate

        # Optimal bit array size m: - (n * ln(p)) / (ln(2)^2)
        self.size = int(math.ceil(
            - (expected_elements * math.log(false_positive_rate)) / (math.log(2) ** 2)
        ))

        # Optimal number of hash functions k: (m / n) * ln(2)
        self.num_hashes = max(1, int(round((self.size / expected_elements) * math.log(2))))

        self.bit_array = bytearray((self.size + 7) // 8)
        self._items_added = 0

    def __len__(self) -> int:
        return self._items_added

    def _get_hashes(self, item: Any) -> list[int]:
        item_bytes = str(item).encode('utf-8')
        digest = hashlib.md5(item_bytes).digest()

        # Extract two 64-bit unsigned integers from 16-byte MD5 digest
        h1 = int.from_bytes(digest[:8], byteorder='little')
        h2 = int.from_bytes(digest[8:], byteorder='little')

        # Double hashing: g_i(x) = (h1 + i * h2) % size
        return [(h1 + i * h2) % self.size for i in range(self.num_hashes)]

    def add(self, item: Any) -> None:
        """Adds an item into the Bloom filter."""
        for bit_index in self._get_hashes(item):
            byte_idx = bit_index // 8
            bit_offset = bit_index % 8
            self.bit_array[byte_idx] |= (1 << bit_offset)
        self._items_added += 1

    def contains(self, item: Any) -> bool:
        """
        Tests whether an item is likely in the set.
        False positives are possible with rate <= false_positive_rate,
        but false negatives are impossible.
        """
        for bit_index in self._get_hashes(item):
            byte_idx = bit_index // 8
            bit_offset = bit_index % 8
            if not (self.bit_array[byte_idx] & (1 << bit_offset)):
                return False
        return True

    def __contains__(self, item: Any) -> bool:
        return self.contains(item)

    def current_false_positive_probability(self) -> float:
        """Calculates current theoretical false positive rate based on items added."""
        return (1.0 - math.exp(-self.num_hashes * self._items_added / self.size)) ** self.num_hashes

    def approximate_item_count(self) -> int:
        """
        Estimates the number of distinct items added based on the proportion of set bits.
        n* ≈ - (m / k) * ln(1 - X / m) where X is the number of 1-bits.
        """
        set_bits = sum(bin(byte).count('1') for byte in self.bit_array)
        if set_bits == 0:
            return 0
        if set_bits >= self.size:
            return self._items_added
        return int(round(- (self.size / self.num_hashes) * math.log(1.0 - set_bits / self.size)))
