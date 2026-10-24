class FenwickTree3D:
    """
    3D Binary Indexed Tree (Fenwick Tree 3D) supporting O(log X * log Y * log Z)
    point updates and 3D subvolume range sum queries over 1-indexed (x, y, z) coordinates.
    """

    def __init__(self, dim_x: int, dim_y: int, dim_z: int):
        if dim_x <= 0 or dim_y <= 0 or dim_z <= 0:
            raise ValueError("All dimensions must be positive integers.")

        self.dim_x = dim_x
        self.dim_y = dim_y
        self.dim_z = dim_z
        self.tree = [
            [[0] * (dim_z + 1) for _ in range(dim_y + 1)]
            for _ in range(dim_x + 1)
        ]

    def update(self, x: int, y: int, z: int, delta: int) -> None:
        """Adds delta to point at 1-based (x, y, z) in O(log X * log Y * log Z) time."""
        if not (1 <= x <= self.dim_x and 1 <= y <= self.dim_y and 1 <= z <= self.dim_z):
            raise IndexError(f"Position ({x}, {y}, {z}) out of bounds.")

        xi = x
        while xi <= self.dim_x:
            yi = y
            while yi <= self.dim_y:
                zi = z
                while zi <= self.dim_z:
                    self.tree[xi][yi][zi] += delta
                    zi += zi & (-zi)
                yi += yi & (-yi)
            xi += xi & (-xi)

    def query(self, x: int, y: int, z: int) -> int:
        """Returns 3D prefix sum from (1, 1, 1) to (x, y, z) inclusive."""
        if x < 0 or y < 0 or z < 0 or x > self.dim_x or y > self.dim_y or z > self.dim_z:
            raise IndexError(f"Position ({x}, {y}, {z}) out of bounds.")

        total = 0
        xi = x
        while xi > 0:
            yi = y
            while yi > 0:
                zi = z
                while zi > 0:
                    total += self.tree[xi][yi][zi]
                    zi -= zi & (-zi)
                yi -= yi & (-yi)
            xi -= xi & (-xi)

        return total

    def range_query(
        self,
        x1: int, y1: int, z1: int,
        x2: int, y2: int, z2: int
    ) -> int:
        """
        Returns sum of elements in 3D subvolume [(x1, y1, z1), (x2, y2, z2)] inclusive
        using 3D Inclusion-Exclusion.
        """
        if not (
            1 <= x1 <= x2 <= self.dim_x and
            1 <= y1 <= y2 <= self.dim_y and
            1 <= z1 <= z2 <= self.dim_z
        ):
            raise IndexError("Invalid 3D subvolume coordinates.")

        return (
            self.query(x2, y2, z2)
            - self.query(x1 - 1, y2, z2)
            - self.query(x2, y1 - 1, z2)
            - self.query(x2, y2, z1 - 1)
            + self.query(x1 - 1, y1 - 1, z2)
            + self.query(x1 - 1, y2, z1 - 1)
            + self.query(x2, y1 - 1, z1 - 1)
            - self.query(x1 - 1, y1 - 1, z1 - 1)
        )
