# py4m/tests/check_properties.py

from functools import reduce
from operator import mul

import pytest

from sandbox.py4m.util.utils import close_to


# ----- Ring tests -----

def check_additive_identity(samples):
    for a in samples:
        zero = a.zero()
        assert close_to(a + zero, a)
        assert close_to(zero + a, a)


def check_multiplicative_identity(samples):
    for a in samples:
        one = a.one()
        assert close_to(a * one, a)
        assert close_to(one * a, a)


def check_additive_inverse(samples):
    for a in samples:
        zero = a.zero()
        assert close_to(a + (-a), zero)


def check_commutativity_addition(samples):
    for a in samples:
        for b in samples:
            assert close_to(a + b, b + a)


def check_associativity_addition(samples):
    for a in samples:
        for b in samples:
            for c in samples:
                assert close_to((a + b) + c, a + (b + c))


def check_associativity_multiplication(samples):
    for a in samples:
        for b in samples:
            for c in samples:
                assert close_to((a * b) * c, a * (b * c))


def check_left_distributivity(samples):
    for a in samples:
        for b in samples:
            for c in samples:
                assert close_to(a * (b + c), (a * b) + (a * c))


def check_right_distributivity(samples):
    for a in samples:
        for b in samples:
            for c in samples:
                assert close_to((a + b) * c, (a * c) + (b * c))


def check_bulk_add(samples):
    samples_rev = reversed(list(samples))
    zero = samples[0].zero()
    total = sum(samples, zero)
    total_rev = sum(samples_rev, zero)
    assert close_to(total, total_rev)


def check_bulk_mul(samples):
    samples_rev = reversed(list(samples))
    one = samples[0].one()
    prod = reduce(mul, samples, one)
    prod_rev = reduce(mul, samples_rev, one)
    assert close_to(prod, prod_rev)


# ----- EuclideanRing tests -----

def check_division_algorithm(samples):
    for a in samples:
        for b in samples:
            if b == b.zero():
                continue
            q = a // b
            r = a % b
            assert close_to(a, q * b + r)


def check_divmod(samples):
    for a in samples:
        for b in samples:
            if b == b.zero():
                continue
            q, r = divmod(a, b)
            assert close_to(q, a // b)
            assert close_to(r, a % b)
            assert close_to(a, q * b + r)


# ----- Field tests -----

def check_truediv_and_inverse(samples):
    for a in samples:
        one = a.one()
        if a == a.zero():
            continue
        inv = a.inverse()
        assert close_to(a * inv, one)
        assert close_to(inv * a, one)
        assert close_to(a / a, one)


def check_field_division_by_zero(samples):
    for a in samples:
        zero = a.zero()
        with pytest.raises(ZeroDivisionError):
            _ = a / zero


def check_rings(samples):
    check_bulk_add(samples)
    check_bulk_mul(samples)
    check_additive_identity(samples)
    check_multiplicative_identity(samples)
    check_additive_inverse(samples)
    check_commutativity_addition(samples)
    check_associativity_addition(samples)
    check_associativity_multiplication(samples)
    check_left_distributivity(samples)
    check_right_distributivity(samples)


def check_euclidean_rings(samples):
    check_rings(samples)
    check_division_algorithm(samples)
    check_divmod(samples)


def check_fields(samples):
    check_euclidean_rings(samples)
    check_truediv_and_inverse(samples)
    check_field_division_by_zero(samples)
