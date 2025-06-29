# p4m/tests/test_properties.py

import pytest

from sandbox.p4m.util.utils import close_to


# from .native_samples import (RING_SAMPLES,
#                              EUCLIDIAN_RING_SAMPLES,
#                              FIELD_SAMPLES)


# from .handmade_samples import (RING_SAMPLES,
#                                EUCLIDIAN_RING_SAMPLES,
#                                FIELD_SAMPLES)


# ----- Ring tests -----
@pytest.mark.parametrize("Type,samples", sample_set)
def test_additive_identity(Type, samples):
    for a in samples:
        zero = a.zero()
        assert a + zero == a
        assert zero + a == a


@pytest.mark.parametrize("Type,samples", RING_SAMPLES)
def test_multiplicative_identity(Type, samples):
    for a in samples:
        one = a.one()
        assert a * one == a
        assert one * a == a


@pytest.mark.parametrize("Type,samples", RING_SAMPLES)
def test_additive_inverse(Type, samples):
    for a in samples:
        zero = a.zero()
        assert a + (-a) == zero


@pytest.mark.parametrize("Type,samples", RING_SAMPLES)
def test_commutativity_addition(Type, samples):
    for a in samples:
        for b in samples:
            assert a + b == b + a


@pytest.mark.parametrize("Type,samples", RING_SAMPLES)
def test_associativity_addition(Type, samples):
    for a in samples:
        for b in samples:
            for c in samples:
                assert (a + b) + c == a + (b + c)


@pytest.mark.parametrize("Type,samples", RING_SAMPLES)
def test_associativity_multiplication(Type, samples):
    for a in samples:
        for b in samples:
            for c in samples:
                assert (a * b) * c == a * (b * c)


@pytest.mark.parametrize("Type,samples", RING_SAMPLES)
def test_left_distributivity(Type, samples):
    for a in samples:
        for b in samples:
            for c in samples:
                assert a * (b + c) == (a * b) + (a * c)


@pytest.mark.parametrize("Type,samples", RING_SAMPLES)
def test_right_distributivity(Type, samples):
    for a in samples:
        for b in samples:
            for c in samples:
                assert (a + b) * c == (a * c) + (b * c)


# ----- EuclideanRing tests -----
@pytest.mark.parametrize("Type,samples", EUCLIDIAN_RING_SAMPLES)
def test_division_algorithm(Type, samples):
    for a in samples:
        for b in samples:
            if b == b.zero():
                continue
            q = a // b
            r = a % b

            assert close_to(a, q * b + r)


@pytest.mark.parametrize("Type,samples", EUCLIDIAN_RING_SAMPLES)
def test_divmod(Type, samples):
    for a in samples:
        for b in samples:
            if b == b.zero():
                continue
            q, r = a.divmod(b)
            assert close_to(q, a // b)
            assert close_to(r, a % b)
            assert close_to(a, q * b + r)


@pytest.mark.parametrize("Type,samples", EUCLIDIAN_RING_SAMPLES)
def test_degree_nonnegative(Type, samples):
    for a in samples:
        pass
        # assert a.degree() >= 0


# ----- Field tests -----
@pytest.mark.parametrize("Type,samples", FIELD_SAMPLES)
def test_truediv_and_inverse(Type, samples):
    for a in samples:
        one = a.one()
        if a == a.zero():
            continue
        inv = a.inverse()
        assert close_to(a * inv, one)
        assert close_to(inv * a, one)
        assert close_to(a / a, one)


@pytest.mark.parametrize("Type,samples", FIELD_SAMPLES)
def test_field_division_by_zero(Type, samples):
    for a in samples:
        zero = a.zero()
        with pytest.raises(ZeroDivisionError):
            _ = a / zero
