# py4m/tests/test_properties.py

import pytest

from sandbox.py4m.util.utils import close_to


# ----- Ring tests -----

def test_additive_identity(samples):
    for a in samples:
        zero = a.zero()
        assert a + zero == a
        assert zero + a == a

def test_multiplicative_identity(samples):
    for a in samples:
        one = a.one()
        assert a * one == a
        assert one * a == a

def test_additive_inverse(samples):
    for a in samples:
        zero = a.zero()
        assert a + (-a) == zero

def test_commutativity_addition(samples):
    for a in samples:
        for b in samples:
            assert a + b == b + a

def test_associativity_addition(samples):
    for a in samples:
        for b in samples:
            for c in samples:
                assert close_to((a + b) + c, a + (b + c))

def test_associativity_multiplication(samples):
    for a in samples:
        for b in samples:
            for c in samples:
                assert close_to((a * b) * c, a * (b * c))

def test_left_distributivity(samples):
    for a in samples:
        for b in samples:
            for c in samples:
                assert close_to(a * (b + c), (a * b) + (a * c))

def test_right_distributivity(samples):
    for a in samples:
        for b in samples:
            for c in samples:
                assert close_to((a + b) * c, (a * c) + (b * c))
    
    
    # ----- EuclideanRing tests -----


def test_division_algorithm(samples):
    for a in samples:
        for b in samples:
            if b == b.zero():
                continue
            q = a // b
            r = a % b
            assert close_to(a, q * b + r)

def test_divmod(samples):
    for a in samples:
        for b in samples:
            if b == b.zero():
                continue
            q, r = a.divmod(b)
            assert close_to(q, a // b)
            assert close_to(r, a % b)
            assert close_to(a, q * b + r)


# ----- Field tests -----

def test_truediv_and_inverse(samples):
    for a in samples:
        one = a.one()
        if a == a.zero():
            continue
        inv = a.inverse()
        assert close_to(a * inv, one)
        assert close_to(inv * a, one)
        assert close_to(a / a, one)


def test_field_division_by_zero(samples):
    for a in samples:
        zero = a.zero()
        with pytest.raises(ZeroDivisionError):
            _ = a / zero


def test_rings(samples):
    test_additive_identity(samples)
    test_multiplicative_identity(samples)
    test_additive_inverse(samples)
    test_commutativity_addition(samples)
    test_associativity_addition(samples)
    test_associativity_multiplication(samples)
    test_left_distributivity(samples)
    test_right_distributivity(samples)

    # ----- EuclideanRing tests -----

def test_euclidean_rings(samples):
    test_rings(samples)
    test_division_algorithm(samples)
    test_divmod(samples)

# ----- Field tests -----

def test_fields(samples):
    test_euclidean_rings(samples)
    test_truediv_and_inverse(samples)
    test_field_division_by_zero(samples)


