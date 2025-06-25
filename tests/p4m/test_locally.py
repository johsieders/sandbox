# p4m/tests/test_locally.py

import pytest
import torch

from sandbox.p4m.core.fraction import Fraction
from sandbox.p4m.core.utils import close_to
from sandbox.p4m.core.wrappers import Int, Float, Complex, Tensor

# ----- Type/sample groupings -----

fraction_samples = [
    Fraction(Int(1), Int(2)),
    Fraction(Int(2), Int(3)),
    Fraction(Int(5), Int(4)),
    Fraction(Int(-3), Int(7)),
    Fraction(Int(9)),  # auto-denominator = one (i.e. 9/1)
    Fraction(Int(0), Int(5)),  # zero
]

FIELD_TYPES_AND_SAMPLES = [
    (Float, [Float(2.0), Float(3.0), Float(5.0)]),
    (Complex, [Complex(complex(2.0, 0)), Complex(complex(3.0, 1)), Complex(complex(5.0, 2))]),
    (Fraction, fraction_samples),
    # Add future Field types here (e.g. Fraction, Fp, etc.)
]

EUCLIDIAN_RING_TYPES_AND_SAMPLES = [
    (Int, [Int(2), Int(3), Int(5)]),
    # Add future EuclideanRing types here
] + FIELD_TYPES_AND_SAMPLES

tensor_samples = [
    Tensor(torch.tensor([[1.0, 2.0], [3.0, 4.0]])),
    Tensor(torch.tensor([[4.0, 5.0], [6.0, 7.0]])),
    Tensor(torch.tensor([[0.0, 0.0], [0.0, 0.0]])),
]

RING_TYPES_AND_SAMPLES = [
    (Tensor, tensor_samples),
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
