class FenwickTree2D:
    """
    2D Binary Indexed Tree (Fenwick Tree 2D) supporting O(log N * log M) point updates
    and subgrid range sum queries over 1-indexed (row, col) coordinates.
    """

    def __init__(self, rows: int, cols: int):
        if rows <= 0 or cols <= 0:
            raise ValueError("Rows and cols must be greater than zero.")
        
        self.rows = rows
        self.cols = cols
        self.tree = [[0] * (cols + 1) for _ in range(rows + 1)]

    def update(self, r: int, c: int, delta: int) -> None:
        """Adds delta to cell at 1-based (r, c) in O(log N * log M) time."""
        if not (1 <= r <= self.rows and 1 <= c <= self.cols):
            raise IndexError(f"Position ({r}, {c}) out of bounds for FenwickTree2D ({self.rows}x{self.cols}).")

        r_idx = r
        while r_idx <= self.rows:
            c_idx = c
            while c_idx <= self.cols:
                self.tree[r_idx][c_idx] += delta
                c_idx += c_idx & (-c_idx)
            r_idx += r_idx & (-r_idx)

    def query(self, r: int, c: int) -> int:
        """Returns 2D prefix sum from (1, 1) to (r, c) inclusive in O(log N * log M) time."""
        if r < 0 or c < 0 or r > self.rows or c > self.cols:
            raise IndexError(f"Position ({r}, {c}) out of bounds for FenwickTree2D ({self.rows}x{self.cols}).")

        total = 0
        r_idx = r
        while r_idx > 0:
            c_idx = c
            while c_idx > 0:
                total += self.tree[r_idx][c_idx]
                c_idx -= c_idx & (-c_idx)
            r_idx -= r_idx & (-r_idx)

        return total

    def range_query(self, r1: int, c1: int, r2: int, c2: int) -> int:
        """Returns sum of elements in subgrid [(r1, c1), (r2, c2)] inclusive."""
        if not (1 <= r1 <= r2 <= self.rows and 1 <= c1 <= c2 <= self.cols):
            raise IndexError(f"Invalid 2D subgrid range [({r1}, {c1}), ({r2}, {c2})].")

        return (
            self.query(r2, c2)
            - self.query(r1 - 1, c2)
            - self.query(r2, c1 - 1)
            + self.query(r1 - 1, c1 - 1)
        )
