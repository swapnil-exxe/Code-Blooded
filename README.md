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
* `algorithms/astar.py`: A* search algorithm with heuristic-guided shortest path planning.
* `algorithms/z_algorithm.py`: Z-algorithm for linear-time $O(N + M)$ string pattern matching.
* `algorithms/lca_binary_lifting.py`: Lowest Common Ancestor (LCA) queries in $O(\log N)$ using binary lifting on trees.
* `algorithms/rabin_karp.py`: Rabin-Karp string matching algorithm with rolling hash evaluation.
* `algorithms/treap.py`: Treap randomized binary search tree data structure.
* `algorithms/heavy_light_decomposition.py`: Heavy-Light Decomposition (HLD) for tree path range queries.
* `algorithms/suffix_array.py`: Suffix Array construction and Kasai's $O(N)$ LCP array algorithm.
* `algorithms/kosaraju_scc.py`: Kosaraju's two-pass DFS algorithm for strongly connected components.
* `algorithms/dinic_max_flow.py`: Dinic's maximum flow algorithm using level graphs and blocking flow.
* `algorithms/hopcroft_karp.py`: Hopcroft-Karp algorithm for maximum bipartite matching in $O(E \sqrt{V})$.
* `algorithms/aho_corasick.py`: Aho-Corasick automaton for multi-pattern dictionary string searching.
* `algorithms/suffix_tree.py`: Suffix Tree constructed via Suffix Array & LCP array for $O(M)$ substring searching.
* `algorithms/euler_tour.py`: Euler Tour Technique for tree flattening and subtree range queries.
* `algorithms/manacher.py`: Manacher's algorithm for linear-time $O(N)$ longest palindromic substring discovery.
* `algorithms/min_cost_max_flow.py`: Minimum Cost Maximum Flow (MCMF) using SPFA shortest path augmenting paths.
* `algorithms/fenwick_tree_2d.py`: 2D Binary Indexed Tree (Fenwick Tree 2D) for $O(\log N \cdot \log M)$ subgrid range sum queries.
* `algorithms/boyer_moore.py`: Boyer-Moore string search algorithm using Bad Character Heuristic.
* `algorithms/johnson_algorithm.py`: Johnson's all-pairs shortest paths algorithm using Bellman-Ford potential reweighting & Dijkstra.
* `algorithms/b_tree.py`: B-Tree self-balancing disk-optimized search tree data structure.
* `algorithms/skip_list.py`: Skip List probabilistic search structure providing $O(\log N)$ expected performance.
* `algorithms/dynamic_segment_tree.py`: Dynamic Segment Tree for sparse range queries over large coordinate spaces.
* `algorithms/splay_tree.py`: Splay Tree self-adjusting binary search tree data structure.
* `algorithms/wavelet_matrix.py`: Wavelet Matrix for succinct range quantile and range rank queries.
* `algorithms/persistent_segment_tree.py`: Persistent Segment Tree supporting historical version queries.
* `algorithms/scapegoat_tree.py`: Scapegoat Tree self-balancing binary search tree.
* `algorithms/sparse_table.py`: Sparse Table for $O(1)$ idempotent range minimum and maximum queries.
* `algorithms/hungarian_algorithm.py`: Hungarian Algorithm (Kuhn-Munkres) for optimal weighted bipartite matching.

## Running Tests

Run the PyTest suite across all data structures:

```bash
pytest
```
