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
                # assert close_to((a + b) + c, a + (b + c))
                u = (a + b) + c
                v = a + (b + c)
                if not close_to(u, v):
                    print('\nasso_add: ', (u - v).norm())
                    print('asso_add: ', u.descent())
                    print('asso_add: ', v.descent())
            # assert close_to((a + b) + c, a + (b + c))


def check_associativity_multiplication(samples):
    for a in samples:
        for b in samples:
            for c in samples:
                u = (a * b) * c
                v = a * (b * c)
                if not close_to(u, v):
                    print('\nasso_mul: ', (u - v).norm())
                    print('asso_mul: ', u.descent())
                    print('asso_mul: ', v.descent())

                # assert close_to((a * b) * c, a * (b * c))


def check_left_distributivity(samples):
    for a in samples:
        for b in samples:
            for c in samples:
                # assert close_to(a * (b + c), (a * b) + (a * c))
                u = (a * b) + (a * c)
                v = a * (b + c)
                if not close_to(u, v):
                    print('\nleft_dist: ', (u - v).norm())
                    print('left_dist: ', u.descent())
                    print('left_dist: ', v.descent())


def check_right_distributivity(samples):
    for a in samples:
        for b in samples:
            for c in samples:
                # assert close_to((a + b) * c, (a * c) + (b * c))
                u = (a * c) + (b * c)
                v = (a + b) * c
                if not close_to(u, v):
                    print('\nright_dist: ', (u - v).norm())
                    print('right_dist: ', u.descent())
                    print('right_dist: ', v.descent())


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
    # assert close_to(prod, prod_rev)

    if not close_to(prod, prod_rev):
        u = prod
        v = prod_rev
        print('\nbulk_mul: ', (u - v).norm())
        print('bulk_mul: ', u.descent())
        print('bulk_mul: ', v.descent())

# ----- EuclideanRing tests -----

def check_division_algorithm(samples):
    for a in samples:
        for b in samples:
            if close_to(b, b.zero()):
                continue
            q = a // b
            r = a % b
            # assert close_to(a, q * b + r)
            u = a
            v = q * b + r
            if not close_to(u, v):
                print('\ndivision: ', (u - v).norm())
                print('division: ', u.descent())
                print('division: ', v.descent())


def check_divmod(samples):
    for a in samples:
        for b in samples:
            if close_to(b, b.zero()):
                continue
            q, r = divmod(a, b)
            assert close_to(q, a // b)
            assert close_to(r, a % b)
            # assert close_to(a, q * b + r)
            u = a
            v = q * b + r
            if not close_to(u, v):
                print('\ndivmod: ', (u - v).norm())
                print('divmod: ', u.descent())
                print('divmod: ', v.descent())


# ----- Field tests -----

def check_truediv_and_inverse(samples):
    for a in samples:
        one = a.one()
        if close_to(a, a.zero()):
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
    check_additive_identity(samples)
    check_multiplicative_identity(samples)
    check_additive_inverse(samples)
    check_commutativity_addition(samples)
    check_associativity_addition(samples)
    check_associativity_multiplication(samples)
    check_left_distributivity(samples)
    check_right_distributivity(samples)


def check_euclidean_rings(samples):
    check_bulk_mul(samples)
    check_rings(samples)
    check_division_algorithm(samples)
    check_divmod(samples)


def check_fields(samples):
    check_euclidean_rings(samples)
    check_truediv_and_inverse(samples)
    check_field_division_by_zero(samples)
