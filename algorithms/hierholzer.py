from collections import defaultdict
from typing import List, Tuple, Optional, Dict

class Hierholzer:
    """
    Hierholzer's algorithm to find an Eulerian Path or Eulerian Circuit
    in directed or undirected graphs in linear O(V + E) time.
    """

    @staticmethod
    def find_eulerian_path_directed(
        num_vertices: int,
        edges: List[Tuple[int, int]]
    ) -> Optional[List[int]]:
        """
        Finds an Eulerian path in a directed graph.
        Returns a list of vertices representing the path, or None if impossible.
        """
        if not edges:
            return []

        adj: Dict[int, List[int]] = defaultdict(list)
        in_degree = [0] * num_vertices
        out_degree = [0] * num_vertices

        for u, v in edges:
            if not (0 <= u < num_vertices and 0 <= v < num_vertices):
                raise IndexError("Vertex index out of bounds.")
            adj[u].append(v)
            out_degree[u] += 1
            in_degree[v] += 1

        start_node = -1
        end_node = -1

        for i in range(num_vertices):
            diff = out_degree[i] - in_degree[i]
            if diff == 1:
                if start_node != -1:
                    return None  # Multiple start candidates
                start_node = i
            elif diff == -1:
                if end_node != -1:
                    return None  # Multiple end candidates
                end_node = i
            elif diff != 0:
                return None  # Degree mismatch

        # If it's a circuit, pick any node with outgoing edges as start
        if start_node == -1:
            for i in range(num_vertices):
                if out_degree[i] > 0:
                    start_node = i
                    break

        if start_node == -1:
            return None

        # Hierholzer's traversal
        stack = [start_node]
        path: List[int] = []

        while stack:
            u = stack[-1]
            if adj[u]:
                v = adj[u].pop()
                stack.append(v)
            else:
                path.append(stack.pop())

        path.reverse()

        # Check if all edges were traversed
        if len(path) != len(edges) + 1:
            return None

        return path

    @staticmethod
    def find_eulerian_path_undirected(
        num_vertices: int,
        edges: List[Tuple[int, int]]
    ) -> Optional[List[int]]:
        """
        Finds an Eulerian path in an undirected graph.
        Returns a list of vertices representing the path, or None if impossible.
        """
        if not edges:
            return []

        adj: Dict[int, List[Tuple[int, int]]] = defaultdict(list)
        degree = [0] * num_vertices

        for edge_id, (u, v) in enumerate(edges):
            if not (0 <= u < num_vertices and 0 <= v < num_vertices):
                raise IndexError("Vertex index out of bounds.")
            adj[u].append((v, edge_id))
            adj[v].append((u, edge_id))
            degree[u] += 1
            degree[v] += 1

        odd_nodes = [i for i in range(num_vertices) if degree[i] % 2 != 0]
        if len(odd_nodes) not in (0, 2):
            return None

        start_node = odd_nodes[0] if odd_nodes else -1
        if start_node == -1:
            for i in range(num_vertices):
                if degree[i] > 0:
                    start_node = i
                    break

        if start_node == -1:
            return None

        used_edges = [False] * len(edges)
        stack = [start_node]
        path: List[int] = []

        while stack:
            u = stack[-1]
            # Advance to an unused edge
            while adj[u] and used_edges[adj[u][-1][1]]:
                adj[u].pop()

            if adj[u]:
                v, edge_id = adj[u].pop()
                used_edges[edge_id] = True
                stack.append(v)
            else:
                path.append(stack.pop())

        path.reverse()

        if len(path) != len(edges) + 1:
            return None

        return path
