import pytest
from algorithms.two_sat import TwoSat

def test_two_sat_satisfiable_simple():
    # Formula: (x1 OR x2) AND (NOT x1 OR x2) AND (x1 OR NOT x2)
    # Solution exists: x1 = True, x2 = True
    solver = TwoSat(2)
    solver.add_clause(1, 2)
    solver.add_clause(-1, 2)
    solver.add_clause(1, -2)

    sat, assign = solver.solve()
    assert sat is True
    assert assign is not None
    assert assign[0] is True
    assert assign[1] is True

def test_two_sat_unsatisfiable_contradiction():
    # Formula: (x1 OR x1) AND (NOT x1 OR NOT x1) => x1 AND NOT x1 => Contradiction
    solver = TwoSat(1)
    solver.set_value(1)
    solver.set_value(-1)

    sat, assign = solver.solve()
    assert sat is False
    assert assign is None

def test_two_sat_multiple_variables():
    # 4 variables:
    # (x1 OR x2) AND (NOT x2 OR x3) AND (NOT x3 OR x4) AND (NOT x4 OR NOT x1)
    solver = TwoSat(4)
    solver.add_clause(1, 2)
    solver.add_clause(-2, 3)
    solver.add_clause(-3, 4)
    solver.add_clause(-4, -1)

    sat, assign = solver.solve()
    assert sat is True
    assert assign is not None

    # Verify that each clause is satisfied by the assignment
    clauses = [(1, 2), (-2, 3), (-3, 4), (-4, -1)]
    for c1, c2 in clauses:
        val1 = assign[abs(c1) - 1] if c1 > 0 else not assign[abs(c1) - 1]
        val2 = assign[abs(c2) - 1] if c2 > 0 else not assign[abs(c2) - 1]
        assert val1 or val2

def test_two_sat_error_handling():
    with pytest.raises(ValueError):
        TwoSat(0)
    solver = TwoSat(2)
    with pytest.raises(IndexError):
        solver.add_clause(1, 3)
