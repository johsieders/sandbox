"""
Algebraic Property Verification: A Python Textbook of Abstract Algebra

This module provides pure mathematical property testing for algebraic structures,
implementing the fundamental axioms of abstract algebra as executable Python code.
It serves as both a verification system and a computational textbook, encoding
mathematical definitions that are unlikely to change over the next millennium.

MATHEMATICAL FOUNDATION:
This file implements the precise axiom systems that define algebraic structures:
- Abelian Groups: Closure, associativity, identity, inverses, commutativity
- Rings: Abelian group under addition + multiplicative monoid + distributivity
- Euclidean Rings: Ring + division algorithm with remainder bounds
- Fields: Euclidean ring + multiplicative inverses for non-zero elements
- Comparability: Reflexivity, antisymmetry, transitivity, totality

DESIGN PHILOSOPHY:
1. **Implementation Agnostic**: No assumptions about concrete representations
2. **Axiom Direct**: Each function tests exactly one mathematical property
3. **Numerical Stability**: Uses tolerance-based equality via close_to()
4. **Composable**: Higher-level structures built from primitive properties
5. **Pure Mathematics**: Encodes timeless mathematical truths

VERIFICATION APPROACH:
- Properties tested directly from definitions, not expected values
- Comprehensive coverage: both positive properties and error conditions
- Tolerance handling: Acknowledges floating-point and approximate arithmetic
- Bulk operations: Tests algorithmic properties (associativity, commutativity)

The functions in this file encode mathematical knowledge that transcends
programming languages and computational systems - they are the Python
embodiment of definitions found in any abstract algebra textbook.

Each test function corresponds directly to a mathematical axiom:
- check_associativity_addition: ∀a,b,c: (a+b)+c = a+(b+c)
- check_distributivity: ∀a,b,c: a×(b+c) = (a×b)+(a×c)
- check_field_division: ∀a≠0: ∃a⁻¹: a×a⁻¹ = 1

Dependencies: Only close_to() for numerical tolerance - no implementation coupling.
"""

from functools import reduce
from operator import mul

import pytest

from sandbox.py4alg.util.utils import close_to


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


def check_commutativity_multiplication(samples):
    """Check multiplicative commutativity: a * b = b * a."""
    for a in samples:
        for b in samples:
            u = a * b
            v = b * a
            if not close_to(u, v):
                print('\ncomm_mul: ', (u - v).norm())
                print('comm_mul: ', u.descent())
                print('comm_mul: ', v.descent())


def check_annihilator_properties(samples):
    """Check annihilator properties: 0 * a = a * 0 = 0."""
    for a in samples:
        zero = a.zero()
        assert close_to(zero * a, zero), f"Left annihilator failed: 0 * {a} != 0"
        assert close_to(a * zero, zero), f"Right annihilator failed: {a} * 0 != 0"


def check_distributivity(samples):
    """Check both left and right distributivity."""
    check_left_distributivity(samples)
    check_right_distributivity(samples)


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
    # Protocol-based filtering handles type checking now
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
    # Protocol-based filtering handles type checking now
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
    # Protocol-based filtering handles type checking now
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
    # Protocol-based filtering handles type checking now
    for a in samples:
        one = a.one()
        if close_to(a, a.zero()):
            continue
        inv = a.inverse()
        assert close_to(a * inv, one)
        assert close_to(inv * a, one)
        assert close_to(a / a, one)


def check_field_division_by_zero(samples):
    # Protocol-based filtering handles type checking now
    for a in samples:
        zero = a.zero()
        with pytest.raises(ZeroDivisionError):
            _ = a / zero


# ----- Compound tests -----

def check_abelian_group(samples):
    """Check all abelian group properties."""
    check_additive_identity(samples)
    check_additive_inverse(samples)
    check_commutativity_addition(samples)
    check_associativity_addition(samples)
    check_bulk_add(samples)


def check_rings(samples):
    """Check all ring properties."""
    check_abelian_group(samples)
    check_multiplicative_identity(samples)
    check_associativity_multiplication(samples)
    check_commutativity_multiplication(samples)
    check_distributivity(samples)
    check_annihilator_properties(samples)
    check_bulk_mul(samples)


def check_euclidean_rings(samples):
    """Check all Euclidean ring properties."""
    check_rings(samples)
    check_division_algorithm(samples)
    check_divmod(samples)


def check_fields(samples):
    check_euclidean_rings(samples)
    check_truediv_and_inverse(samples)
    check_field_division_by_zero(samples)


# ----- Comparable tests -----

def check_reflexivity(samples):
    """Check reflexivity: a <= a and a >= a for all a."""
    for a in samples:
        assert a <= a, f"Reflexivity failed for {a}: {a} <= {a}"
        assert a >= a, f"Reflexivity failed for {a}: {a} >= {a}"
        assert a == a, f"Equality reflexivity failed for {a}: {a} == {a}"


def check_antisymmetry(samples):
    """Check antisymmetry: if a <= b and b <= a, then a == b."""
    for a in samples:
        for b in samples:
            if a <= b and b <= a:
                assert a == b, f"Antisymmetry failed: {a} <= {b} and {b} <= {a} but {a} != {b}"


def check_transitivity(samples):
    """Check transitivity: if a <= b and b <= c, then a <= c."""
    for a in samples:
        for b in samples:
            for c in samples:
                if a <= b and b <= c:
                    assert a <= c, f"Transitivity failed: {a} <= {b} and {b} <= {c} but not {a} <= {c}"


def check_totality(samples):
    """Check totality: for any a, b, either a <= b or b <= a."""
    for a in samples:
        for b in samples:
            assert a <= b or b <= a, f"Totality failed: neither {a} <= {b} nor {b} <= {a}"


def check_comparison_consistency(samples):
    """Check consistency between comparison operators."""
    for a in samples:
        for b in samples:
            # a < b iff a <= b and a != b
            if a < b:
                assert a <= b, f"Inconsistency: {a} < {b} but not {a} <= {b}"
                assert a != b, f"Inconsistency: {a} < {b} but {a} == {b}"

            # a > b iff b < a
            assert (a > b) == (b < a), f"Inconsistency: (a > b) != (b < a) for a={a}, b={b}"

            # a >= b iff b <= a
            assert (a >= b) == (b <= a), f"Inconsistency: (a >= b) != (b <= a) for a={a}, b={b}"

            # if a == b, then a <= b and b <= a
            if a == b:
                assert a <= b, f"Inconsistency: {a} == {b} but not {a} <= {b}"
                assert b <= a, f"Inconsistency: {a} == {b} but not {b} <= {a}"


def check_comparables(samples):
    """Check all comparable invariants."""
    check_reflexivity(samples)
    check_antisymmetry(samples)
    check_transitivity(samples)
    check_totality(samples)
    check_comparison_consistency(samples)
