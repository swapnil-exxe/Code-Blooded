# Code-Blooded

Production-grade Data Structures and Algorithmic Problem Solving in Python.

## Implemented Data Structures

* `algorithms/disjoint_set.py`: Disjoint Set Union (DSU / Union-Find) with path compression and rank optimization.
* `algorithms/heap.py`: Binary Max-Heap & Priority Queue supporting $O(\log N)$ insertion, extraction, and $O(N)$ heapify.
* `algorithms/red_black_tree.py`: Self-balancing Red-Black Binary Search Tree enforcing black-height balance invariants.
* `algorithms/trie.py`: Prefix Tree (Trie) for $O(L)$ string retrieval and autocomplete.
* `algorithms/avl_tree.py`: Self-balancing AVL Binary Search Tree with rotation logic.
* `algorithms/lru_cache.py`: $O(1)$ Doubly-linked list + Hash Map LRU Cache implementation.
* `algorithms/segment_tree.py`: $O(\log N)$ Range Minimum & Range Sum Query Segment Tree.
* `algorithms/fenwick_tree.py`: Binary Indexed Tree (Fenwick Tree) supporting $O(\log N)$ point updates and prefix sum queries.
* `algorithms/string_matching.py`: Knuth-Morris-Pratt (KMP) string search algorithm with $O(N + M)$ pattern matching.
* `algorithms/graph_algorithms.py`: Dijkstra's Shortest Path algorithm using $O((V + E) \log V)$ binary min-heap priority queue.
* `algorithms/topological_sort.py`: Topological Sort using Kahn's in-degree BFS and DFS state-based traversal.
* `algorithms/bellman_ford.py`: Bellman-Ford single-source shortest path algorithm with negative edge weight handling.
* `algorithms/mst.py`: Kruskal's (DSU) and Prim's (min-heap) Minimum Spanning Tree (MST) algorithms.
* `algorithms/floyd_warshall.py`: Floyd-Warshall all-pairs shortest path algorithm with path reconstruction.
* `algorithms/tarjan_scc.py`: Tarjan's strongly connected components (SCC) algorithm using DFS discovery times.
* `algorithms/max_flow.py`: Edmonds-Karp maximum flow network algorithm using BFS augmenting paths.

## Running Tests

Run the PyTest suite across all data structures:

```bash
pytest
```
