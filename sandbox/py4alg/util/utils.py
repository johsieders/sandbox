# py4alg/core/utils.py

from itertools import islice
from typing import Callable, Iterator

from sandbox.py4alg.cockpit import params


def close_to(x, y, rtol=params['rtol'], atol=params['atol']):
    """
    rtol: relative tolerance parameter.
    atol: absolute tolerance parameter.
    Return True if x and y are close to their norm().
    """
    try:
        return (x - y).norm() <= atol + rtol * max(x.norm(), y.norm())
    except AttributeError:
        # Fallback to built-in abs if .norm() is not available
        return abs(x - y) <= atol + rtol * max(abs(x), abs(y))


def compose(*funs):
    """
    This function takes a list of functions f, g, h, ... (at least one). The last function, say h,
    takes any number of arguments (h(*args)). compose returns the function f(g(h))(*args).
    Compose does not check thematch of returned values and required arguments.
    """
    if not funs:
        raise ValueError("At least one function is required")
    if len(funs) == 1:
        return funs[0]

    def composed(*x):
        result = funs[-1](*x)
        for f in reversed(funs[:-1]):
            result = f(result)
        return result

    return composed


def take(n: int) -> Callable[[Iterator], list]:
    def aux(t: Iterator):
        return list(islice(t, n))

    return aux
