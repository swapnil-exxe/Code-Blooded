class TrieNode:
    """Node in a Trie data structure."""
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    """Prefix Tree (Trie) for efficient string retrieval and autocomplete."""
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Inserts a word into the Trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word: str) -> bool:
        """Returns True if the exact word exists in the Trie."""
        node = self._find_node(word)
        return node is not None and node.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        """Returns True if there is any word in the Trie that starts with the given prefix."""
        return self._find_node(prefix) is not None

    def get_words_with_prefix(self, prefix: str) -> list[str]:
        """Finds all words in the Trie starting with the given prefix."""
        node = self._find_node(prefix)
        if not node:
            return []
        
        results = []
        self._dfs(node, prefix, results)
        return results

    def _find_node(self, prefix: str) -> TrieNode | None:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def _dfs(self, node: TrieNode, current_prefix: str, results: list[str]) -> None:
        if node.is_end_of_word:
            results.append(current_prefix)
        for char, child_node in sorted(node.children.items()):
            self._dfs(child_node, current_prefix + char, results)
