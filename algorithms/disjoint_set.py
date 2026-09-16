class DisjointSet:
    """Disjoint Set Union (DSU / Union-Find) with path compression and rank optimization."""

    def __init__(self, size: int):
        if size <= 0:
            raise ValueError("DisjointSet size must be greater than zero.")
        self.parent = list(range(size))
        self.rank = [0] * size
        self.count = size

    def find(self, i: int) -> int:
        """Finds representative of set containing element i with path compression in O(alpha(N)) time."""
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i: int, j: int) -> bool:
        """Unites sets containing elements i and j. Returns True if sets were joined, False if already in same set."""
        root_i = self.find(i)
        root_j = self.find(j)

        if root_i == root_j:
            return False

        if self.rank[root_i] < self.rank[root_j]:
            root_i, root_j = root_j, root_i

        self.parent[root_j] = root_i
        if self.rank[root_i] == self.rank[root_j]:
            self.rank[root_i] += 1

        self.count -= 1
        return True

    def connected(self, i: int, j: int) -> bool:
        """Returns True if i and j belong to the same set."""
        return self.find(i) == self.find(j)
