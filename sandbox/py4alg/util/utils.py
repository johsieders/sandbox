# py4alg/core/utils.py

from itertools import islice
from typing import Callable, Iterator


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
