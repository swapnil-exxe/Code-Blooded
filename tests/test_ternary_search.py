import pytest
import math
from algorithms.ternary_search import ternary_search_discrete, golden_section_search

def test_ternary_search_discrete_min():
    # Parabola: f(x) = (x - 42)^2 + 10, minimum at x = 42
    def f(x: int) -> float:
        return (x - 42) ** 2 + 10

    x_opt, val_opt = ternary_search_discrete(f, 0, 100, find_min=True)
    assert x_opt == 42
    assert val_opt == 10

def test_ternary_search_discrete_max():
    # Inverted parabola: f(x) = -(x - 17)^2 + 50, maximum at x = 17
    def f(x: int) -> float:
        return -(x - 17) ** 2 + 50

    x_opt, val_opt = ternary_search_discrete(f, -50, 50, find_min=False)
    assert x_opt == 17
    assert val_opt == 50

def test_golden_section_search_min():
    # Continuous function: f(x) = (x - 3.14159)^2 + 2.71828
    def f(x: float) -> float:
        return (x - 3.1415926535) ** 2 + 2.71828

    x_opt, val_opt = golden_section_search(f, 0.0, 10.0, tol=1e-6, find_min=True)
    assert math.isclose(x_opt, 3.1415926535, abs_tol=1e-5)
    assert math.isclose(val_opt, 2.71828, abs_tol=1e-5)

def test_golden_section_search_max():
    # Continuous max: f(x) = - (x - 1.5)^2 + 4.0
    def f(x: float) -> float:
        return - (x - 1.5) ** 2 + 4.0

    x_opt, val_opt = golden_section_search(f, -5.0, 5.0, tol=1e-6, find_min=False)
    assert math.isclose(x_opt, 1.5, abs_tol=1e-5)
    assert math.isclose(val_opt, 4.0, abs_tol=1e-5)

def test_exceptions():
    with pytest.raises(ValueError):
        ternary_search_discrete(lambda x: x, 10, 5)
    with pytest.raises(ValueError):
        golden_section_search(lambda x: x, 5.0, 1.0)
    with pytest.raises(ValueError):
        golden_section_search(lambda x: x, 0.0, 1.0, tol=0.0)
