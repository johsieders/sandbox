# tests/py4alg/gen_samples.py

import random
from itertools import cycle
from typing import Any, Sequence, Iterator, Iterable, Callable, List

from sandbox.py4alg.mapper import Complex, FieldComplex, Fp, Fraction, Matrix, Polynomial, FieldPolynomial
from sandbox.py4alg.mapper.m_modular import Zm
from sandbox.py4alg.util.utils import compose, params, take
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

gen_fractions = gen_make(Fraction, min=1, max=2)
gen_complex = gen_make(Complex, min=1, max=2)
gen_field_complex = gen_make(FieldComplex, min=1, max=2)
gen_polynomials = gen_make(Polynomial, params['poly_min'], params['poly_max'])
gen_field_polynomials = gen_make(FieldPolynomial, params['poly_min'], params['poly_max'])
gen_matrices = gen_make(Matrix, params['matrix_size'], params['matrix_size'])

# meaning of successors:
# gen_x : (gen_y, gen_z) means that gen_y, gen_z accept gen_x as argument
# or compose(gen_y, gen_x), compose(gen_z, gen_x) are legal. 
# Examples:
# gen_nat_ints accepts gen_ints, gen_nat_ints
# gen_fractions accepts gen_nat_ints, gen_floats, gen_complex, gen_field_polynomials, ...
# gen_polynomials accepts gen_fractions, gen_polynomials, gen_matrices, ...
SUCCESSORS = {gen_ints: (gen_nat_ints,),  # compose(gen_nat_ints, gen_ints)
              gen_floats: (gen_nat_floats,),  # compose(gen_nat_floats, gen_floats)
              gen_complex_: (gen_nat_complex,),
              gen_nat_ints: (gen_nat_ints, gen_fractions, gen_matrices, gen_polynomials),
              gen_nat_floats: (gen_nat_floats, gen_complex, gen_field_complex, gen_fractions, gen_matrices,
                               gen_polynomials, gen_field_polynomials),
              gen_nat_complex: (gen_nat_complex, gen_complex, gen_field_complex, gen_fractions, gen_matrices,
                                gen_polynomials, gen_field_polynomials),
              gen_complex: (gen_complex, gen_matrices, gen_polynomials,),
              gen_field_complex: (gen_field_complex, gen_fractions, gen_field_polynomials),
              gen_fractions: (gen_fractions, gen_complex, gen_field_complex, gen_matrices, gen_polynomials,
                              gen_field_polynomials),
              gen_matrices: (gen_matrices, gen_complex, gen_polynomials),
              gen_polynomials: (gen_polynomials, gen_matrices, gen_complex),
              gen_field_polynomials: (gen_field_polynomials, gen_matrices, gen_fractions)
              }


def gen_tree(sources, depth=3, n=5) -> List[Any]:
    """
    This function generates all paths of the given depth, starting from one of the sources
    param n: length of samples
    """
    result = []
    pool = [[arg] for arg in sources]
    while pool:
        gs = pool.pop()
        if len(gs) <= depth:
            for g in SUCCESSORS[gs[-1]]:
                hs = gs + [g]
                pool.append(hs)
        else:
            gs.append(take(n))
            result.append(reversed(gs))
    
    return [compose(*t)(1, 10) for t in result]

