# py4alg/core/utils.py

import random
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


params = {'rtol': 1e-9,
          'atol': 1e-12,
          'lower_bound': 10,
          'upper_bound': 20,
          'seed': 102,
          'min_norm': 0,
          'no_zeros': True,
          'poly_min': 1,
          'poly_max': 5,
          'prime': 17,
          'nonprime': 21,
          'matrix_size': 9}


def set_test_seed():
    """
    run this before each test session to get identical results
    """
    random.seed(params['seed'])
