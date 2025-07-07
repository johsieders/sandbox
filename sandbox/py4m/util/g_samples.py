# tests/py4m/make_samples.py

import random
from itertools import cycle
from typing import Any, Sequence, Iterator, Callable

from sandbox.py4m.cockpit import params
from sandbox.py4m.mapper.m_complex import Complex
from sandbox.py4m.mapper.m_fraction import Fraction
from sandbox.py4m.mapper.m_matrix import Matrix
from sandbox.py4m.mapper.m_polynomial import Polynomial
from sandbox.py4m.util.utils import close_to, take, compose
from sandbox.py4m.wrapper.w_complex import NativeComplex
from sandbox.py4m.wrapper.w_float import NativeFloat
from sandbox.py4m.wrapper.w_int import NativeInt


def g_cycle(seq: Sequence[int | float | complex]) -> Iterator[int | float | complex]:
    return cycle(seq)


def g_ints(a, b: int, no_zeros=params['no_zeros']) -> Iterator[int]:
    while True:
        k = random.randint(a, b)
        if no_zeros and k == 0:
            continue
        else:
            yield k


def g_floats(a, b: float, no_zeros=params['no_zeros']) -> Iterator[float]:
    while True:
        x = random.uniform(a, b)
        if no_zeros and close_to(x, 0.):
            continue
        else:
            yield x


def g_complex_(a, b: float, no_zeros=params['no_zeros']) -> Iterator[complex]:
    while True:
        re = random.uniform(a, b)
        im = random.uniform(a, b)
        if no_zeros and close_to(re, 0.) and close_to(im, 0.):
            continue
        else:
            yield complex(re, im)


def g_tuples(min, max: int, samples: Iterator[Any]) -> Iterator[tuple]:
    """
    This generator returns the samples as tuples of size between min and max included.
    """
    while True:
        k = random.randint(min, max)
        next_sample = []
        for _ in range(k):
            next_sample.append(next(samples))
        yield tuple(next_sample)


def g_make(type, min=1, max=1, min_norm=params['min_norm']) -> Callable[[Any], Any]:
    def generate(samples: Iterator[Any]):
        t = g_tuples(min, max, samples)
        while True:
            args = next(t)
            x = type(*args)
            if x.norm() > min_norm:
                yield x

    return generate


g_nat_ints = g_make(NativeInt)
g_nat_floats = g_make(NativeFloat)
g_nat_complex = g_make(NativeComplex)

g_fractions = g_make(Fraction, 1, 2)
g_complex = g_make(Complex, 1, 2)
g_polynomials = g_make(Polynomial, params['poly_min'], params['poly_max'])
g_matrices = g_make(Matrix, params['matrix_size'], params['matrix_size'])

successors = {g_ints: (g_nat_ints,),
              g_floats: (g_nat_floats,),
              g_complex_: (g_nat_complex,),
              g_nat_ints: (g_nat_ints, g_fractions, g_matrices),   # g_polynomials (only ring)
              g_nat_floats: (g_nat_floats, g_complex, g_fractions, g_matrices, g_polynomials),
              g_nat_complex: (g_nat_complex, g_complex, g_fractions, g_matrices, g_polynomials),
              g_complex: (g_complex, g_fractions, g_matrices, g_polynomials),
              g_fractions: (g_complex, g_fractions, g_matrices, g_polynomials),
              g_matrices: (g_matrices, g_polynomials),
              g_polynomials: (g_fractions, g_polynomials),  # g_matrices (only ring)
              }


def g_tree(*args, depth=3, n=5):
    """
    This functions generates all legal chains of given depth of types,
    starting with g_ints, g_floats, g_complex_ or a subset thereof.
    param n: length of samples
    """
    result = []
    pool = [[arg] for arg in args]
    while pool:
        gs = pool.pop()
        if len(gs) < depth:
            for g in successors[gs[-1]]:
                hs = gs + [g]
                pool.append(hs)
        else:
            gs.append(take(n))
            result.append(reversed(gs))
    return result


def test_g_tree():
    depth = 5
    n = 5
    result = g_tree(g_ints, g_floats, g_complex_, depth=depth, n=5)
    # result = g_all(g_ints, depth=depth, n=4)
    print()

    # for i in (0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12):
    # for i in range(len(result)):
    #     g = result[i]
    #     s = compose(*g)(10, 20)
    #     print(i, s)
    #     assert len(s) == n
    # print()
    print(len(result))


