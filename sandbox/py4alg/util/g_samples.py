# tests/py4alg/make_samples.py

import random
from itertools import cycle
from typing import Any, Sequence, Iterator, Callable

from sandbox.py4alg.cockpit import AlgebraicType, params
from sandbox.py4alg.mapper.m_complex import Complex
from sandbox.py4alg.mapper.m_fp import Fp
from sandbox.py4alg.mapper.m_fraction import Fraction
from sandbox.py4alg.mapper.m_matrix import Matrix
from sandbox.py4alg.mapper.m_polynomial import Polynomial
from sandbox.py4alg.util.utils import close_to, take, compose
from sandbox.py4alg.wrapper.w_complex import NativeComplex
from sandbox.py4alg.wrapper.w_float import NativeFloat
from sandbox.py4alg.wrapper.w_int import NativeInt


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
            if x.norm() >= min_norm:
                yield x

    return generate


g_nat_ints = g_make(NativeInt)
g_nat_floats = g_make(NativeFloat)
g_nat_complex = g_make(NativeComplex)

g_fractions = g_make(Fraction, 1, 2)
g_complex = g_make(Complex, 1, 2)
g_polynomials = g_make(Polynomial, params['poly_min'], params['poly_max'])
g_matrices = g_make(Matrix, params['matrix_size'], params['matrix_size'])


# meaning of successors:
# g_x -> g_y means that g_y accepts g_x as argument
# Examples:
# g_nat_ints accepts g_ints, g_nat_ints
# g_fractions accepts g_nat_ints, g_floats, g_complex, g_polynomials
# g_polynomials accepts g_fractions, g_polynomials, g_matrices
successors = {g_ints: (g_nat_ints,),
              g_floats: (g_nat_floats,),
              g_complex_: (g_nat_complex,),
              g_nat_ints: (g_nat_ints, g_fractions, g_matrices),  # g_polynomials (only ring)
              g_nat_floats: (g_nat_floats, g_complex, g_fractions, g_matrices, g_polynomials),
              g_nat_complex: (g_nat_complex, g_complex, g_fractions, g_matrices, g_polynomials),
              g_complex: (g_complex, g_fractions, g_matrices, g_polynomials),
              g_fractions: (g_fractions, g_complex, g_matrices, g_polynomials),
              g_matrices: (g_matrices,),
              g_polynomials: (g_polynomials, g_floats, g_fractions, g_ints)
              }

def resulting_type(first: AlgebraicType, *types) -> AlgebraicType | None:
    if len(types) == 0:
        return first
    else:
        return resulting_type(types[0].resulting_type(first), *types[1:])

def g_tree(sources, successors, depth=3, n=5):
    """
    This function generates all paths of the given depth, starting from one of the sources
    param n: length of samples
    """
    result = []
    pool = [[arg] for arg in sources]
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
    depth = 6
    n = 4
    result = g_tree((g_ints, g_floats, g_complex_), successors, depth=depth, n=n)

    for g in result:
        s = compose(*g)(10, 20)
        assert len(s) == n

    print()
    print(len(result))
