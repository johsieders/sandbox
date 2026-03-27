# tests/py4alg/def_samples.py

from typing import Sequence, Tuple

from sandbox.py4alg.mapper import Complex, FieldComplex, Fraction, Matrix, Polynomial, FieldPolynomial
from sandbox.py4alg.protocols.p_euclidean_ring import EuclideanRing
from sandbox.py4alg.protocols.p_field import Field
from sandbox.py4alg.protocols.p_ring import Ring
from sandbox.py4alg.wrapper.w_complex import NativeComplex
from sandbox.py4alg.wrapper.w_float import NativeFloat
from sandbox.py4alg.wrapper.w_int import NativeInt


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


def def_complex(*rr: Tuple[Ring, Ring]) -> Sequence[Complex]:
    return [Complex(*r) for r in rr]


def def_field_complex(*rr: Tuple[Field, Field]) -> Sequence[FieldComplex]:
    return [FieldComplex(*r) for r in rr]


def def_matrices(*rr: Sequence[Ring]) -> Sequence[Matrix]:
    return [Matrix(*r) for r in rr]
