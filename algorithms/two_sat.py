from typing import List, Tuple, Optional

class TwoSat:
    """
    Linear-time 2-SAT solver using Tarjan's Strongly Connected Components
    algorithm on the implication graph in O(V + E) time.
    Variables are 1-indexed (e.g. 1, 2, ..., n). Negated variables are negative integers.
    """

    def __init__(self, num_vars: int):
        if num_vars <= 0:
            raise ValueError("Number of variables must be positive.")
        self.num_vars = num_vars
        self.num_nodes = 2 * num_vars
        self.adj: List[List[int]] = [[] for _ in range(self.num_nodes)]

    def _to_node(self, lit: int) -> int:
        if abs(lit) < 1 or abs(lit) > self.num_vars:
            raise IndexError(f"Variable {lit} out of bounds (must be between 1 and {self.num_vars}).")
        var = abs(lit) - 1
        return 2 * var if lit > 0 else 2 * var + 1

    def add_clause(self, lit1: int, lit2: int) -> None:
        """
        Adds a clause (lit1 OR lit2).
        Equivalent to implication edges: NOT lit1 => lit2 and NOT lit2 => lit1.
        """
        u = self._to_node(lit1)
        v = self._to_node(lit2)
        not_u = u ^ 1
        not_v = v ^ 1
        self.adj[not_u].append(v)
        self.adj[not_v].append(u)

    def set_value(self, lit: int) -> None:
        """Forces literal lit to be True (adds clause lit OR lit)."""
        self.add_clause(lit, lit)

    def solve(self) -> Tuple[bool, Optional[List[bool]]]:
        """
        Solves the 2-SAT instance.
        Returns (is_satisfiable, assignment_list), where assignment_list[i]
        is the boolean truth value for variable (i + 1).
        """
        disc = [-1] * self.num_nodes
        low = [-1] * self.num_nodes
        in_stack = [False] * self.num_nodes
        stack: List[int] = []
        scc_id = [-1] * self.num_nodes
        timer = 0
        current_scc = 0

        # Tarjan's SCC algorithm
        for i in range(self.num_nodes):
            if disc[i] != -1:
                continue

            call_stack = [(i, 0)]
            while call_stack:
                u, edge_idx = call_stack[-1]

                if edge_idx == 0:
                    disc[u] = low[u] = timer
                    timer += 1
                    stack.append(u)
                    in_stack[u] = True

                advanced = False
                while edge_idx < len(self.adj[u]):
                    v = self.adj[u][edge_idx]
                    edge_idx += 1
                    call_stack[-1] = (u, edge_idx)

                    if disc[v] == -1:
                        call_stack.append((v, 0))
                        advanced = True
                        break
                    elif in_stack[v]:
                        low[u] = min(low[u], disc[v])

                if advanced:
                    continue

                if low[u] == disc[u]:
                    while True:
                        node = stack.pop()
                        in_stack[node] = False
                        scc_id[node] = current_scc
                        if node == u:
                            break
                    current_scc += 1

                call_stack.pop()
                if call_stack:
                    parent, _ = call_stack[-1]
                    low[parent] = min(low[parent], low[u])

        # Check satisfiability: x and NOT x cannot be in the same SCC
        assignment: List[bool] = [False] * self.num_vars
        for var in range(self.num_vars):
            pos_node = 2 * var
            neg_node = 2 * var + 1
            if scc_id[pos_node] == scc_id[neg_node]:
                return False, None
            # In Tarjan's SCC, components are labeled in reverse topological order.
            # Thus, scc_id[pos] < scc_id[neg] means pos comes AFTER neg topologically,
            # so pos = True is a valid consistent assignment.
            assignment[var] = scc_id[pos_node] < scc_id[neg_node]

        return True, assignment
