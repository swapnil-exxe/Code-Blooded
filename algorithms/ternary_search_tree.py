from typing import Optional, Any, List

class TSTNode:
    def __init__(self, char: str):
        self.char = char
        self.val: Any = None
        self.is_end: bool = False
        self.left: Optional['TSTNode'] = None
        self.mid: Optional['TSTNode'] = None
        self.right: Optional['TSTNode'] = None

class TernarySearchTree:
    """
    Ternary Search Tree (TST) combining binary search tree space efficiency
    with trie prefix-search performance.
    """

    def __init__(self):
        self.root: Optional[TSTNode] = None
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def insert(self, key: str, val: Any = True) -> None:
        """Inserts a key-value pair into the TST."""
        if not key:
            raise ValueError("Key cannot be empty.")

        def _insert(node: Optional[TSTNode], idx: int) -> TSTNode:
            c = key[idx]
            if node is None:
                node = TSTNode(c)

            if c < node.char:
                node.left = _insert(node.left, idx)
            elif c > node.char:
                node.right = _insert(node.right, idx)
            else:
                if idx + 1 < len(key):
                    node.mid = _insert(node.mid, idx + 1)
                else:
                    if not node.is_end:
                        self._size += 1
                    node.is_end = True
                    node.val = val
            return node

        self.root = _insert(self.root, 0)

    def _get_node(self, node: Optional[TSTNode], key: str, idx: int) -> Optional[TSTNode]:
        if node is None:
            return None
        c = key[idx]
        if c < node.char:
            return self._get_node(node.left, key, idx)
        elif c > node.char:
            return self._get_node(node.right, key, idx)
        else:
            if idx + 1 == len(key):
                return node
            return self._get_node(node.mid, key, idx + 1)

    def search(self, key: str) -> Optional[Any]:
        """Returns the value associated with key, or None if not found."""
        if not key:
            return None
        node = self._get_node(self.root, key, 0)
        if node and node.is_end:
            return node.val
        return None

    def contains(self, key: str) -> bool:
        """Checks whether key exists in the TST."""
        return self.search(key) is not None

    def starts_with(self, prefix: str) -> bool:
        """Checks if any word in the TST starts with prefix."""
        if not prefix:
            return True
        return self._get_node(self.root, prefix, 0) is not None

    def _collect(self, node: Optional[TSTNode], prefix: str, results: List[str]) -> None:
        if node is None:
            return
        self._collect(node.left, prefix, results)
        current = prefix + node.char
        if node.is_end:
            results.append(current)
        self._collect(node.mid, current, results)
        self._collect(node.right, prefix, results)

    def keys_with_prefix(self, prefix: str) -> List[str]:
        """Returns all keys starting with prefix."""
        if not prefix:
            res: List[str] = []
            self._collect(self.root, "", res)
            return res

        node = self._get_node(self.root, prefix, 0)
        if node is None:
            return []

        res: List[str] = []
        if node.is_end:
            res.append(prefix)
        self._collect(node.mid, prefix, res)
        return sorted(res)

    def wildcard_search(self, pattern: str, wildcard: str = '.') -> List[str]:
        """Returns all keys matching pattern with single-character wildcards."""
        results: List[str] = []

        def _search(node: Optional[TSTNode], idx: int, current: str):
            if node is None or idx >= len(pattern):
                return

            c = pattern[idx]

            # If wildcard or c < node.char, explore left
            if c == wildcard or c < node.char:
                _search(node.left, idx, current)

            # If wildcard or match, explore mid
            if c == wildcard or c == node.char:
                next_str = current + node.char
                if idx + 1 == len(pattern) and node.is_end:
                    results.append(next_str)
                if idx + 1 < len(pattern):
                    _search(node.mid, idx + 1, next_str)

            # If wildcard or c > node.char, explore right
            if c == wildcard or c > node.char:
                _search(node.right, idx, current)

        _search(self.root, 0, "")
        return sorted(results)
