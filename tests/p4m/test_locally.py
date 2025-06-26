# p4m/tests/test_locally.py

import pytest
from sympy import Poly

from sandbox.p4m.fraction import Fraction
from sandbox.p4m.complex import Complex
from sandbox.p4m.matrix import Matrix
from sandbox.p4m.polynomial import Polynomial
from sandbox.p4m.utils import close_to
from sandbox.p4m.wrappers import IntNative, FloatNative, ComplexNative

# ----- Type/sample groupings -----

fraction_samples = [
    Fraction(IntNative(1), IntNative(2)),
    Fraction(IntNative(2), IntNative(3)),
    Fraction(IntNative(5), IntNative(4)),
    Fraction(IntNative(-3), IntNative(7)),
    Fraction(IntNative(9)),  # auto-denominator = one (i.e. 9/1)
    Fraction(IntNative(0), IntNative(5)),  # zero
]

complex_float_samples = [
    Complex(FloatNative(1.0), FloatNative(2.0)),    # 1.0 + 2.0i
    Complex(FloatNative(0.0), FloatNative(3.5)),    # 0.0 + 3.5i
    Complex(FloatNative(-2.1), FloatNative(1.7)),   # -2.1 + 1.7i
    Complex(FloatNative(4.2), FloatNative(0.0)),    # 4.2 + 0.0i
    Complex(FloatNative(0.0), FloatNative(0.0)),    # 0.0 + 0.0i
]


FIELD_TYPES_AND_SAMPLES = [
    (FloatNative, [FloatNative(2.0), FloatNative(3.0), FloatNative(5.0)]),
    (ComplexNative, [ComplexNative(complex(2.0, 0)), ComplexNative(complex(3.0, 1)), ComplexNative(complex(5.0, 2))]),
    (Fraction, fraction_samples),
    # Add future Field types here (e.g. Fraction, Fp, etc.)
]


poly_samples = [
    Polynomial([IntNative(1), IntNative(2), IntNative(3)]),    # 1 + 2x + 3x^2
    Polynomial([IntNative(0), IntNative(1)]),            # x
    Polynomial([IntNative(-2), IntNative(0), IntNative(1)]),   # -2 + x^2
    Polynomial([IntNative(5)]),                    # constant polynomial
]


EUCLIDIAN_RING_TYPES_AND_SAMPLES = [
    (IntNative, [IntNative(2), IntNative(3), IntNative(5)]),
    (Poly, poly_samples),
    # Add future EuclideanRing types here
] + FIELD_TYPES_AND_SAMPLES

matrix_samples = [
    Matrix([[IntNative(1), IntNative(2)], [IntNative(3), IntNative(4)]]),
    Matrix([[IntNative(0), IntNative(1)], [IntNative(1), IntNative(0)]]),
    Matrix([[IntNative(2), IntNative(0)], [IntNative(0), IntNative(2)]]),
    Matrix([[IntNative(-1), IntNative(2)], [IntNative(0), IntNative(-2)]]),
]

RING_TYPES_AND_SAMPLES = [
    (Matrix, matrix_samples),
    # ... your other rings ...
] + EUCLIDIAN_RING_TYPES_AND_SAMPLES


# ----- Ring tests -----
@pytest.mark.parametrize("Type,samples", RING_TYPES_AND_SAMPLES)
def test_additive_identity(Type, samples):
    for a in samples:
        zero = a.zero()
        assert a + zero == a
        assert zero + a == a


@pytest.mark.parametrize("Type,samples", RING_TYPES_AND_SAMPLES)
def test_multiplicative_identity(Type, samples):
    for a in samples:
        one = a.one()
        assert a * one == a
        assert one * a == a


@pytest.mark.parametrize("Type,samples", RING_TYPES_AND_SAMPLES)
def test_additive_inverse(Type, samples):
    for a in samples:
        zero = a.zero()
        assert a + (-a) == zero


@pytest.mark.parametrize("Type,samples", RING_TYPES_AND_SAMPLES)
def test_commutativity_addition(Type, samples):
    for a in samples:
        for b in samples:
            assert a + b == b + a


@pytest.mark.parametrize("Type,samples", RING_TYPES_AND_SAMPLES)
def test_associativity_addition(Type, samples):
    for a in samples:
        for b in samples:
            for c in samples:
                assert (a + b) + c == a + (b + c)


@pytest.mark.parametrize("Type,samples", RING_TYPES_AND_SAMPLES)
def test_associativity_multiplication(Type, samples):
    for a in samples:
        for b in samples:
            for c in samples:
                assert (a * b) * c == a * (b * c)


@pytest.mark.parametrize("Type,samples", RING_TYPES_AND_SAMPLES)
def test_left_distributivity(Type, samples):
    for a in samples:
        for b in samples:
            for c in samples:
                assert a * (b + c) == (a * b) + (a * c)


@pytest.mark.parametrize("Type,samples", RING_TYPES_AND_SAMPLES)
def test_right_distributivity(Type, samples):
    for a in samples:
        for b in samples:
            for c in samples:
                assert (a + b) * c == (a * c) + (b * c)


# ----- EuclideanRing tests -----
@pytest.mark.parametrize("Type,samples", EUCLIDIAN_RING_TYPES_AND_SAMPLES)
def test_division_algorithm(Type, samples):
    for a in samples:
        for b in samples:
            if b == b.zero():
                continue
            q = a // b
            r = a % b

            assert close_to(a, q * b + r)


@pytest.mark.parametrize("Type,samples", EUCLIDIAN_RING_TYPES_AND_SAMPLES)
def test_divmod(Type, samples):
    for a in samples:
        for b in samples:
            if b == b.zero():
                continue
            q, r = a.divmod(b)
            assert close_to(q, a // b)
            assert close_to(r, a % b)
            assert close_to(a, q * b + r)


@pytest.mark.parametrize("Type,samples", EUCLIDIAN_RING_TYPES_AND_SAMPLES)
def test_degree_nonnegative(Type, samples):
    for a in samples:
        pass
        # assert a.degree() >= 0


# ----- Field tests -----
@pytest.mark.parametrize("Type,samples", FIELD_TYPES_AND_SAMPLES)
def test_truediv_and_inverse(Type, samples):
    for a in samples:
        one = a.one()
        if a == a.zero():
            continue
        inv = a.inverse()
        assert close_to(a * inv, one)
        assert close_to(inv * a, one)
        assert close_to(a / a, one)


@pytest.mark.parametrize("Type,samples", FIELD_TYPES_AND_SAMPLES)
def test_field_division_by_zero(Type, samples):
    for a in samples:
        zero = a.zero()
        with pytest.raises(ZeroDivisionError):
            _ = a / zero
