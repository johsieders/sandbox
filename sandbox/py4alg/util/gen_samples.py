# tests/py4alg/gen_samples.py

import random

from sympy import Symbol
from itertools import cycle
from typing import Any, Sequence, Iterator, Iterable, Callable, List

from sandbox.py4alg.mapper import Complex, FieldComplex, FieldMatrix, Fp, Fraction, Matrix, Polynomial, FieldPolynomial
from sandbox.py4alg.mapper.m_modular import Zm
from sandbox.py4alg.util.utils import compose, params, take
from sandbox.py4alg.wrapper.s_int import SymbolicInt
from sandbox.py4alg.wrapper.w_complex import NativeComplex
from sandbox.py4alg.wrapper.w_float import NativeFloat
from sandbox.py4alg.wrapper.w_int import NativeInt


def gen_cycle(seq: Sequence[int | float | complex]) -> Iterator[int | float | complex]:
    return cycle(seq)


def gen_ints(a, b: int, no_zeros=params['no_zeros']) -> Iterator[int]:
    while True:
        k = random.randint(a, b)
        if no_zeros and k == 0:
            continue
        else:
            yield k


def gen_floats(a, b: float, no_zeros=params['no_zeros']) -> Iterator[float]:
    while True:
        x = random.uniform(a, b)
        if no_zeros and abs(x) < params['atol']:
            continue
        else:
            yield x


def gen_complex_(a, b: float, no_zeros=params['no_zeros']) -> Iterator[complex]:
    while True:
        re = random.uniform(a, b)
        im = random.uniform(a, b)
        if no_zeros and abs(re) < params['atol'] and abs(im) < params['atol']:
            continue
        else:
            yield complex(re, im)


SYMBOLS = tuple(Symbol(name, integer=True) for name in "abc")


def gen_symbolic_(a, b: int, no_zeros=params['no_zeros']) -> Iterator[Any]:
    """Symbolic integers k0 + k1*s: integer coefficients in [a, b], s one of SYMBOLS (degree 1, so
    products in deep towers stay manageable)."""
    while True:
        k0, k1 = random.randint(a, b), random.randint(a, b)
        x = k0 + k1 * random.choice(SYMBOLS)
        if no_zeros and x == 0:
            continue
        yield x


def gen_tuples(min, max: int, samples: Iterable[Any]) -> Iterator[tuple]:
    """
    This generator returns the samples as tuples of size between min and max included.
    """
    samples = iter(samples)
    while True:
        k = random.randint(min, max)
        next_sample = []
        for _ in range(k):
            next_sample.append(next(samples))
        yield tuple(next_sample)


def gen_make(type, min=1, max=1, max_retries=1000) -> Callable[[Any], Any]:
    def generate(samples: Iterable[Any]):
        t = gen_tuples(min, max, samples)
        retries = 0
        while True:
            args = next(t)
            try:
                x = type(*args)
            except (ZeroDivisionError, ValueError):
                retries += 1
                if retries > max_retries:
                    raise RuntimeError(f"gen_make({type}): too many retries")
                continue
            if x:
                retries = 0
                yield x
            else:
                retries += 1
                if retries > max_retries:
                    raise RuntimeError(f"gen_make({type}): too many zero results")

    return generate


gen_fp = gen_make(lambda n: Fp(params['prime'], n))
gen_zm = gen_make(lambda n: Zm(params['nonprime'], n))
gen_nat_ints = gen_make(NativeInt)
gen_nat_floats = gen_make(NativeFloat)
gen_nat_complex = gen_make(NativeComplex)
gen_sym_ints = gen_make(SymbolicInt)

gen_fractions = gen_make(Fraction, min=1, max=2)
gen_complex = gen_make(Complex, min=1, max=2)
gen_field_complex = gen_make(FieldComplex, min=1, max=2)
gen_polynomials = gen_make(Polynomial, params['poly_min'], params['poly_max'])
gen_field_polynomials = gen_make(FieldPolynomial, params['poly_min'], params['poly_max'])
gen_matrices = gen_make(Matrix, params['matrix_size'], params['matrix_size'])
gen_field_matrices = gen_make(FieldMatrix, params['matrix_size'], params['matrix_size'])

# Type constructors used by gen_tree, and the start of every tower (raw numbers -> wrapper).
# Which constructor may follow which is not written down: it is derived from the constructor's
# type-parameter bound (class Polynomial[T: Ring] -> Ring) and the runtime protocols (see accepts).
CONSTRUCTORS = {gen_polynomials: Polynomial,
                gen_field_polynomials: FieldPolynomial,
                gen_complex: Complex,
                gen_field_complex: FieldComplex,
                gen_fractions: Fraction,
                gen_matrices: Matrix,
                gen_field_matrices: FieldMatrix}

SOURCES = {gen_ints: gen_nat_ints,
           gen_floats: gen_nat_floats,
           gen_complex_: gen_nat_complex,
           gen_symbolic_: gen_sym_ints}


# Rational functions with float coefficients are not generated: the Euclidean gcd over floats is
# ill-conditioned (whether a remainder counts as zero decides the gcd's degree), so Fraction's
# reduction goes wrong and the axioms fail by rounding, not by a bug (implementation.md, "Floats").
INEXACT = (NativeFloat, NativeComplex)


def accepts(cls, x) -> bool:
    """True if the type constructor cls can be applied to elements like x.

    Either x satisfies the bound of cls's type parameter (Polynomial[T: Ring] accepts any Ring),
    or x belongs to cls itself: Polynomial, Complex and Fraction flatten their own type, and
    Matrix builds block matrices, even where the bound alone would not allow it
    (FieldPolynomial of FieldPolynomials, FieldMatrix of FieldMatrix blocks).
    Exception: no Fraction over polynomials with float coefficients (INEXACT).
    """
    (t,) = cls.__type_params__
    if cls is Fraction and isinstance(x, Polynomial) and x.descent()[-1] in INEXACT:
        return False  # rational functions with float coefficients: see INEXACT
    return isinstance(x, t.__bound__) or isinstance(x, cls)


def successors(gs: List[Callable]) -> List[Callable]:
    """The generators that may extend the path gs (a list of generators, source first)."""
    if gs[-1] in SOURCES:
        return [SOURCES[gs[-1]]]
    state = random.getstate()  # probe one element without disturbing the sample sequence
    x = compose(take(1), *reversed(gs))(1, 10)[0]
    random.setstate(state)
    return [g for g, cls in CONSTRUCTORS.items() if accepts(cls, x)]


def gen_tree(sources, depth=3, n=5) -> List[Any]:
    """
    This function generates all paths of the given depth, starting from one of the sources
    (gen_ints, gen_floats, gen_complex_); each path is source, wrapper, then depth - 1 constructors.
    param n: length of samples
    """
    result = []
    pool = [[arg] for arg in sources]
    while pool:
        gs = pool.pop()
        if len(gs) <= depth:
            for g in successors(gs):
                pool.append(gs + [g])
        else:
            gs.append(take(n))
            result.append(reversed(gs))

    return [compose(*t)(1, 10) for t in result]
