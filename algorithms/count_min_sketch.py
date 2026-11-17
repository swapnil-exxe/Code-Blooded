import math
import hashlib
from typing import Any, List, Optional

class CountMinSketch:
    """
    Count-Min Sketch (Cormode & Muthukrishnan) for sublinear-space frequency estimation
    of data streams with theoretical error guarantees.
    With parameters epsilon and delta:
    - Width w = ceil(e / epsilon)
    - Depth d = ceil(ln(1 / delta))
    An estimate satisfies: freq(x) <= estimate(x) <= freq(x) + epsilon * N with probability >= 1 - delta.
    """

    def __init__(
        self,
        epsilon: Optional[float] = None,
        delta: Optional[float] = None,
        width: Optional[int] = None,
        depth: Optional[int] = None
    ):
        if epsilon is not None and delta is not None:
            if not (0.0 < epsilon < 1.0):
                raise ValueError("Epsilon must be strictly between 0 and 1.")
            if not (0.0 < delta < 1.0):
                raise ValueError("Delta must be strictly between 0 and 1.")
            self.width = max(1, int(math.ceil(math.e / epsilon)))
            self.depth = max(1, int(math.ceil(math.log(1.0 / delta))))
        elif width is not None and depth is not None:
            if width <= 0 or depth <= 0:
                raise ValueError("Width and depth must be positive integers.")
            self.width = width
            self.depth = depth
        else:
            # Defaults: epsilon = 0.01, delta = 0.01
            self.width = int(math.ceil(math.e / 0.01))
            self.depth = int(math.ceil(math.log(100.0)))

        self.table: List[List[int]] = [[0] * self.width for _ in range(self.depth)]
        self._total = 0

    @property
    def total_count(self) -> int:
        return self._total

    def _hashes(self, item: Any) -> List[int]:
        item_bytes = str(item).encode('utf-8')
        digest = hashlib.sha256(item_bytes).digest()

        h1 = int.from_bytes(digest[:8], byteorder='little')
        h2 = int.from_bytes(digest[8:16], byteorder='little')

        # Generate d independent hash values via double hashing
        return [(h1 + i * h2) % self.width for i in range(self.depth)]

    def add(self, item: Any, count: int = 1) -> None:
        """Adds count occurrences of item into the sketch."""
        if count < 0:
            raise ValueError("Count cannot be negative in standard Count-Min Sketch.")
        if count == 0:
            return

        for row, col in enumerate(self._hashes(item)):
            self.table[row][col] += count
        self._total += count

    def estimate(self, item: Any) -> int:
        """Estimates frequency of item (guaranteed: estimate >= true_frequency)."""
        return min(self.table[row][col] for row, col in enumerate(self._hashes(item)))

    def merge(self, other: 'CountMinSketch') -> 'CountMinSketch':
        """Merges another sketch with identical dimensions into a new sketch."""
        if self.width != other.width or self.depth != other.depth:
            raise ValueError("Cannot merge sketches with different dimensions.")

        res = CountMinSketch(width=self.width, depth=self.depth)
        for r in range(self.depth):
            for c in range(self.width):
                res.table[r][c] = self.table[r][c] + other.table[r][c]
        res._total = self._total + other._total
        return res

    def inner_product(self, other: 'CountMinSketch') -> int:
        """Estimates the inner product between frequency vectors of two streams."""
        if self.width != other.width or self.depth != other.depth:
            raise ValueError("Cannot compute inner product for sketches with different dimensions.")

        return min(
            sum(self.table[r][c] * other.table[r][c] for c in range(self.width))
            for r in range(self.depth)
        )
