# tests/py4alg/make_samples.py

import random
from itertools import cycle
from typing import Any, Sequence, Iterator, Iterable, Callable, Tuple

from sandbox.py4alg.cockpit import params
from sandbox.py4alg.mapper import Complex, Fp, Fraction, Matrix, Polynomial, FieldPolynomial
from sandbox.py4alg.protocols.p_euclidean_ring import EuclideanRing
from sandbox.py4alg.protocols.p_field import Field
from sandbox.py4alg.protocols.p_ring import Ring
from sandbox.py4alg.util.utils import take, compose
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


def gen_make(type, min=1, max=1) -> Callable[[Any], Any]:
    def generate(samples: Iterable[Any]):
        t = gen_tuples(min, max, samples)
        while True:
            args = next(t)
            x = type(*args)
            if x:
                yield x

    return generate


gen_fp = gen_make(Fp)
gen_nat_ints = gen_make(NativeInt)
gen_nat_floats = gen_make(NativeFloat)
gen_nat_complex = gen_make(NativeComplex)

gen_fractions = gen_make(Fraction, min=1, max=2)
gen_complex = gen_make(Complex, min=1, max=2)
gen_polynomials = gen_make(Polynomial, params['poly_min'], params['poly_max'])
gen_field_polynomials = gen_make(FieldPolynomial, params['poly_min'], params['poly_max'])
gen_matrices = gen_make(Matrix, params['matrix_size'], params['matrix_size'])


def def_nat_ints(*nn: int) -> Sequence[NativeInt]:
    return [NativeInt(n) for n in nn]


def def_nat_floats(*ff: float) -> Sequence[NativeFloat]:
    return [NativeFloat(f) for f in ff]


def def_nat_complex(*cc: complex) -> Sequence[NativeComplex]:
    return [NativeComplex(c) for c in cc]


def def_fractions(*rr: Tuple[EuclideanRing, EuclideanRing]) -> Sequence[Fraction]:
    return [Fraction(*r) for r in rr]


def def_polynomials(*rr: Sequence[Ring]) -> Sequence[Polynomial]:
    return [Polynomial(*r) for r in rr]


def def_field_polynomials(*rr: Sequence[Field]) -> Sequence[FieldPolynomial]:
    return [FieldPolynomial(*r) for r in rr]


def def_matrices(*rr: Sequence[Ring]) -> Sequence[Matrix]:
    return [Matrix(*r) for r in rr]


# meaning of successors:
# gen_x -> gen_y means that gen_y accepts gen_x as argument
# Examples:
# gen_nat_ints accepts gen_ints, gen_nat_ints
# gen_fractions accepts gen_nat_ints, gen_floats, gen_complex, gen_polynomials
# gen_polynomials accepts gen_fractions, gen_polynomials, gen_matrices
successors = {gen_ints: (gen_nat_ints,),
              gen_floats: (gen_nat_floats,),
              gen_complex_: (gen_nat_complex,),
              gen_nat_ints: (gen_nat_ints, gen_fractions, gen_matrices),  # gen_polynomials (only ring)
              gen_nat_floats: (gen_nat_floats, gen_complex, gen_fractions, gen_matrices, gen_polynomials),
              gen_nat_complex: (gen_nat_complex, gen_complex, gen_fractions, gen_matrices, gen_polynomials),
              gen_complex: (gen_complex, gen_fractions, gen_matrices, gen_polynomials),
              gen_fractions: (gen_fractions, gen_complex, gen_matrices, gen_polynomials),
              gen_matrices: (gen_matrices,),
              gen_polynomials: (gen_polynomials, gen_floats, gen_fractions, gen_ints)
              }


# resulting_type() function removed - using protocol-based system instead


def gen_tree(sources, successors, depth=3, n=5):
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


def test_gen_tree():
    depth = 6
    n = 4
    result = gen_tree((gen_ints, gen_floats, gen_complex_), successors, depth=depth, n=n)

    for g in result:
        s = compose(*g)(10, 20)
        assert len(s) == n

    print()
    print(len(result))
