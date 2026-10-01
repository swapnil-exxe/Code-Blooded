import random
from typing import Optional, List, Any

class SkipNode:
    def __init__(self, key: Any, height: int):
        self.key = key
        self.forward: List[Optional['SkipNode']] = [None] * height

class SkipList:
    """
    Skip List probabilistic search structure providing O(log N) expected
    search, insert, and delete operations using multi-level linked towers.
    """

    def __init__(self, max_level: int = 16, p: float = 0.5):
        if max_level <= 0 or not (0.0 < p < 1.0):
            raise ValueError("max_level must be positive and p must be in (0, 1).")
        self.max_level = max_level
        self.p = p
        self.header = SkipNode(None, max_level)
        self.level = 1

    def _random_level(self) -> int:
        lvl = 1
        while random.random() < self.p and lvl < self.max_level:
            lvl += 1
        return lvl

    def search(self, key: Any) -> bool:
        """Searches for key in O(log N) expected time."""
        curr = self.header
        for i in range(self.level - 1, -1, -1):
            while curr.forward[i] is not None and curr.forward[i].key < key:
                curr = curr.forward[i]

        curr = curr.forward[0]
        return curr is not None and curr.key == key

    def insert(self, key: Any) -> None:
        """Inserts key into Skip List in O(log N) expected time."""
        update = [None] * self.max_level
        curr = self.header

        for i in range(self.level - 1, -1, -1):
            while curr.forward[i] is not None and curr.forward[i].key < key:
                curr = curr.forward[i]
            update[i] = curr

        curr = curr.forward[0]

        if curr is None or curr.key != key:
            r_level = self._random_level()
            if r_level > self.level:
                for i in range(self.level, r_level):
                    update[i] = self.header
                self.level = r_level

            new_node = SkipNode(key, r_level)
            for i in range(r_level):
                new_node.forward[i] = update[i].forward[i]
                update[i].forward[i] = new_node

    def delete(self, key: Any) -> bool:
        """Deletes key from Skip List if present in O(log N) expected time. Returns True if removed."""
        update = [None] * self.max_level
        curr = self.header

        for i in range(self.level - 1, -1, -1):
            while curr.forward[i] is not None and curr.forward[i].key < key:
                curr = curr.forward[i]
            update[i] = curr

        curr = curr.forward[0]

        if curr is not None and curr.key == key:
            for i in range(self.level):
                if update[i].forward[i] != curr:
                    break
                update[i].forward[i] = curr.forward[i]

            while self.level > 1 and self.header.forward[self.level - 1] is None:
                self.level -= 1

            return True

        return False

    def to_list(self) -> List[Any]:
        """Returns sorted list of elements."""
        res = []
        curr = self.header.forward[0]
        while curr is not None:
            res.append(curr.key)
            curr = curr.forward[0]
        return res
