# tests/py4alg/def_samples.py

import pytest, pytest_benchmark

from typing import List, Sequence, Tuple, Any

from sandbox.py4alg.protocols.p_euclidean_ring import EuclideanRing
from sandbox.py4alg.protocols.p_field import Field
from sandbox.py4alg.protocols.p_ring import Ring

from sandbox.py4alg.mapper import Complex, FieldComplex, Fraction, Matrix, Polynomial, FieldPolynomial

from sandbox.py4alg.wrapper.w_complex import NativeComplex
from sandbox.py4alg.wrapper.w_float import NativeFloat
from sandbox.py4alg.wrapper.w_int import NativeInt


def def_nat_ints(*nn: int) -> List[NativeInt]:
    return [NativeInt(n) for n in nn]


def def_nat_floats(*ff: float) -> List[NativeFloat]:
    return [NativeFloat(f) for f in ff]


def def_nat_complex(*cc: complex) -> List[NativeComplex]:
    return [NativeComplex(c) for c in cc]


def def_fractions(*rr: Tuple[EuclideanRing, EuclideanRing]) -> List[Fraction]:
    return [Fraction(*r) for r in rr]


def def_polynomials(*rr: List[Ring]) -> List[Polynomial]:
    return [Polynomial(*r) for r in rr]


def def_field_polynomials(*rr: List[Field]) -> List[FieldPolynomial]:
    return [FieldPolynomial(*r) for r in rr]


def def_complex(*rr: Tuple[Ring, Ring]) -> List[Complex]:
    return [Complex(*r) for r in rr]


def def_field_complex(*rr: Tuple[Field, Field]) -> List[FieldComplex]:
    return [FieldComplex(*r) for r in rr]


def def_matrices(*rr: List[Ring]) -> List[Matrix]:
    return [Matrix(*r) for r in rr]


def to_pairs(xs: Sequence[Any]) -> List[Tuple[Any, Any]]:
    return list(zip(xs[::2], xs[1::2]))


def to_coeffs(xs: Sequence[Any], cs: Sequence[int]) -> List[Sequence[Any]]:
    result = []
    cursor = 0
    for c in cs:
        d = min(cursor + c, len(xs))
        result.append(xs[cursor:d])
        cursor += c
        if cursor >= len(xs):
            break
    return result




