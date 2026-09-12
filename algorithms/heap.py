class MaxHeap:
    """Production-grade Binary Max-Heap & Priority Queue implementation."""

    def __init__(self, arr: list[int] | None = None):
        self.heap = []
        if arr:
            self.heapify(arr)

    def insert(self, val: int) -> None:
        """Inserts a new value into the Max-Heap in O(log N) time."""
        self.heap.append(val)
        self._bubble_up(len(self.heap) - 1)

    def extract_max(self) -> int:
        """Removes and returns the maximum value in O(log N) time."""
        if not self.heap:
            raise IndexError("extract_max from empty MaxHeap")
        
        if len(self.heap) == 1:
            return self.heap.pop()

        max_val = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._bubble_down(0)
        return max_val

    def peek(self) -> int:
        """Returns the maximum element without removing it."""
        if not self.heap:
            raise IndexError("peek from empty MaxHeap")
        return self.heap[0]

    def heapify(self, arr: list[int]) -> None:
        """Transforms an unsorted array into a valid Max-Heap in O(N) time."""
        self.heap = list(arr)
        # Start from last non-leaf node down to root
        for i in range(len(self.heap) // 2 - 1, -1, -1):
            self._bubble_down(i)

    def is_valid_heap(self) -> bool:
        """Verifies max-heap invariant for all parent-child relationships."""
        n = len(self.heap)
        for i in range(n):
            left = 2 * i + 1
            right = 2 * i + 2
            if left < n and self.heap[i] < self.heap[left]:
                return False
            if right < n and self.heap[i] < self.heap[right]:
                return False
        return True

    def _bubble_up(self, idx: int) -> None:
        parent = (idx - 1) // 2
        while idx > 0 and self.heap[idx] > self.heap[parent]:
            self.heap[idx], self.heap[parent] = self.heap[parent], self.heap[idx]
            idx = parent
            parent = (idx - 1) // 2

    def _bubble_down(self, idx: int) -> None:
        n = len(self.heap)
        largest = idx
        left = 2 * idx + 1
        right = 2 * idx + 2

        if left < n and self.heap[left] > self.heap[largest]:
            largest = left
        if right < n and self.heap[right] > self.heap[largest]:
            largest = right

        if largest != idx:
            self.heap[idx], self.heap[largest] = self.heap[largest], self.heap[idx]
            self._bubble_down(largest)
