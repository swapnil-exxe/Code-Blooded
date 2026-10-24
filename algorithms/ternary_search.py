import math
from typing import Callable, Tuple

def ternary_search_discrete(
    func: Callable[[int], float],
    left: int,
    right: int,
    find_min: bool = True
) -> Tuple[int, float]:
    """
    Finds the integer argmin (or argmax) of a unimodal function on [left, right].
    Runs in O(log(right - left)) iterations.
    Returns (optimal_x, optimal_f_x).
    """
    if left > right:
        raise ValueError("left must be less than or equal to right.")

    while right - left >= 3:
        m1 = left + (right - left) // 3
        m2 = right - (right - left) // 3

        f1 = func(m1)
        f2 = func(m2)

        if find_min:
            if f1 < f2:
                right = m2
            else:
                left = m1
        else:
            if f1 > f2:
                right = m2
            else:
                left = m1

    best_x = left
    best_val = func(left)

    for x in range(left + 1, right + 1):
        v = func(x)
        if (find_min and v < best_val) or (not find_min and v > best_val):
            best_val = v
            best_x = x

    return best_x, best_val


def golden_section_search(
    func: Callable[[float], float],
    left: float,
    right: float,
    tol: float = 1e-7,
    find_min: bool = True
) -> Tuple[float, float]:
    """
    Finds the continuous local minimum (or maximum) of a strictly unimodal function
    on [left, right] using Golden-Section Search.
    Returns (optimal_x, optimal_f_x).
    """
    if left > right:
        raise ValueError("left must be less than or equal to right.")
    if tol <= 0:
        raise ValueError("Tolerance tol must be positive.")

    invphi = (math.sqrt(5.0) - 1.0) / 2.0  # ~0.6180339887
    invphi2 = (3.0 - math.sqrt(5.0)) / 2.0  # ~0.3819660113

    a, b = left, right
    h = b - a
    if h <= tol:
        mid = (a + b) / 2.0
        return mid, func(mid)

    c = a + invphi2 * h
    d = a + invphi * h
    fc = func(c)
    fd = func(d)

    while (b - a) > tol:
        if find_min:
            if fc < fd:
                b = d
                d = c
                fd = fc
                h = b - a
                c = a + invphi2 * h
                fc = func(c)
            else:
                a = c
                c = d
                fc = fd
                h = b - a
                d = a + invphi * h
                fd = func(d)
        else:
            if fc > fd:
                b = d
                d = c
                fd = fc
                h = b - a
                c = a + invphi2 * h
                fc = func(c)
            else:
                a = c
                c = d
                fc = fd
                h = b - a
                d = a + invphi * h
                fd = func(d)

    opt_x = (a + b) / 2.0
    return opt_x, func(opt_x)
