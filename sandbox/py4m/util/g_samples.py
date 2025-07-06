# tests/py4m/make_samples.py

import random
from itertools import cycle
from typing import Any, Sequence, Iterator, Callable

from sandbox.py4m.mapper.m_complex import Complex
from sandbox.py4m.mapper.m_fraction import Fraction
from sandbox.py4m.mapper.m_matrix import Matrix
from sandbox.py4m.mapper.m_polynomial import Polynomial
from sandbox.py4m.util.utils import close_to
from sandbox.py4m.wrapper.w_complex import NativeComplex
from sandbox.py4m.wrapper.w_float import NativeFloat
from sandbox.py4m.wrapper.w_int import NativeInt


def g_cycle(seq: Sequence[int | float | complex]) -> Iterator[int | float | complex]:
    return cycle(seq)


def g_ints(a, b: int, seed=100, no_zeros=False) -> Iterator[int]:
    random.seed(seed)
    while True:
        k = random.randint(a, b)
        if no_zeros and k == 0:
            continue
        else:
            yield k


def g_floats(a, b: float, seed=100, no_zeros=False) -> Iterator[float]:
    random.seed(seed)
    while True:
        x = random.uniform(a, b)
        if no_zeros and close_to(x, 0.):
            continue
        else:
            yield x


def g_complex_(a, b: float, seed=100, no_zeros=False) -> Iterator[complex]:
    random.seed(seed)
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


def g_make(type, min=1, max=1, min_norm=0.1) -> Callable[[Any], Any]:
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

g_fractions = g_make(Fraction, 2, 2)
g_complex = g_make(Complex, 1, 2)
g_polynomials = g_make(Polynomial, 1, 5)
g_matrices = g_make(Matrix, 9, 9)
