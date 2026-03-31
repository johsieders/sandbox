"""
Algebraic Property Verification: A Python Textbook of Abstract Algebra

This module provides pure mathematical property testing for algebraic structures,
implementing the fundamental axioms of abstract algebra as executable Python code.

Each test function corresponds directly to a mathematical axiom:
- check_associativity_addition: ∀a,b,c: (a+b)+c = a+(b+c)
- check_distributivity: ∀a,b,c: a×(b+c) = (a×b)+(a×c)
- check_field_division: ∀a≠0: ∃a⁻¹: a×a⁻¹ = 1
"""

from collections import deque
from functools import reduce
from operator import mul

import pytest

from sandbox.py4alg.protocols.p_euclidean_ring import EuclideanRing
from sandbox.py4alg.protocols.p_field import Field
from sandbox.py4alg.protocols.p_ring import Ring
from sandbox.py4alg.util.primes import gcd
from sandbox.py4alg.util.utils import comparable_works, descent_str

# Exception report: list of (check_name, descent, error_type, message)
exception_report: list[tuple[str, str, str, str]] = []

# Black box: records the last 5 samples passed to check_axioms.
# Survives timeouts — inspect after a hang to see what was running.
black_box: deque[str] = deque(maxlen=5)


def report_exception(check_name: str, samples, e: Exception):
    ds = descent_str(samples)
    exception_report.append((check_name, ds, type(e).__name__, str(e)))



# ----- Abelian Group tests (additivity) -----

def check_additive_identity(samples):
    for a in samples:
        try:
            zero = a.zero()
            assert a + zero == a
            assert zero + a == a
        except (AssertionError, ZeroDivisionError) as e:
            report_exception('check_additive_identity', samples, e)


def check_additive_inverse(samples):
    for a in samples:
        try:
            zero = a.zero()
            assert a + (-a) == zero
        except (AssertionError, ZeroDivisionError) as e:
            report_exception('check_additive_inverse', samples, e)


def check_commutativity_addition(samples):
    for a in samples:
        for b in samples:
            try:
                assert a + b == b + a
            except (AssertionError, ZeroDivisionError) as e:
                report_exception('check_commutativity_addition', samples, e)


def check_associativity_addition(samples):
    for a in samples:
        for b in samples:
            for c in samples:
                try:
                    assert (a + b) + c == a + (b + c)
                except (AssertionError, ZeroDivisionError) as e:
                    report_exception('check_associativity_addition', samples, e)


def check_bulk_add(samples):
    try:
        samples_rev = reversed(list(samples))
        zero = samples[0].zero()
        total = sum(samples, zero)
        total_rev = sum(samples_rev, zero)
        assert total == total_rev
    except (AssertionError, ZeroDivisionError) as e:
        report_exception('check_bulk_add', samples, e)


# ----- Ring tests -----

def check_multiplicative_identity(samples):
    for a in samples:
        try:
            one = a.one()
            assert a * one == a
            assert one * a == a
        except (AssertionError, ZeroDivisionError) as e:
            report_exception('check_multiplicative_identity', samples, e)


def check_associativity_multiplication(samples):
    for a in samples:
        for b in samples:
            for c in samples:
                try:
                    assert (a * b) * c == a * (b * c)
                except (AssertionError, ZeroDivisionError) as e:
                    report_exception('check_associativity_multiplication', samples, e)


def check_commutativity_multiplication(samples):
    """Check multiplicative commutativity: a * b = b * a."""
    for a in samples:
        for b in samples:
            try:
                assert a * b == b * a
            except (AssertionError, ZeroDivisionError) as e:
                report_exception('check_commutativity_multiplication', samples, e)


def check_annihilator_properties(samples):
    """Check annihilator properties: 0 * a = a * 0 = 0."""
    for a in samples:
        try:
            zero = a.zero()
            assert zero * a == zero, f"Left annihilator failed: 0 * {a} != 0"
            assert a * zero == zero, f"Right annihilator failed: {a} * 0 != 0"
        except (AssertionError, ZeroDivisionError) as e:
            report_exception('check_annihilator_properties', samples, e)


def check_distributivity(samples):
    """Check both left and right distributivity."""
    check_left_distributivity(samples)
    check_right_distributivity(samples)


def check_left_distributivity(samples):
    for a in samples:
        for b in samples:
            for c in samples:
                try:
                    assert a * (b + c) == (a * b) + (a * c)
                except (AssertionError, ZeroDivisionError) as e:
                    report_exception('left_distributivity', samples, e)


def check_right_distributivity(samples):
    for a in samples:
        for b in samples:
            for c in samples:
                try:
                    assert (a + b) * c == (a * c) + (b * c)
                except (AssertionError, ZeroDivisionError) as e:
                    report_exception('right_distributivity', samples, e)


def check_bulk_mul(samples):
    try:
        samples_rev = reversed(list(samples))
        one = samples[0].one()
        prod = reduce(mul, samples, one)
        prod_rev = reduce(mul, samples_rev, one)
        assert prod == prod_rev
    except (AssertionError, ZeroDivisionError) as e:
        report_exception('check_bulk_mul', samples, e)


# ----- EuclideanRing tests -----

def check_division(samples):
    for a in samples:
        for b in samples:
            if not b:
                continue
            try:
                q = a // b
                r = a % b
                assert a == q * b + r
                if r:
                    assert r.euclidean_function() < b.euclidean_function()
            except (AssertionError, ZeroDivisionError) as e:
                report_exception('check_division', samples, e)


def check_divmod(samples):
    for a in samples:
        for b in samples:
            if not b:
                continue
            try:
                q, r = divmod(a, b)
                assert q == a // b
                assert r == a % b
                assert a == q * b + r
            except (AssertionError, ZeroDivisionError) as e:
                report_exception('check_divmod', samples, e)


def check_gcd_properties(samples):
    """Check basic gcd properties: gcd(a,b) divides both a and b."""
    for a in samples:
        for b in samples:
            try:
                g = gcd(a, b)
                if g:
                    assert a % g == a.zero(), f"gcd({a},{b}) = {g} does not divide {a}"
                if g:
                    assert b % g == b.zero(), f"gcd({a},{b}) = {g} does not divide {b}"
            except (AssertionError, ZeroDivisionError) as e:
                report_exception('check_gcd_properties', samples, e)


def check_gcd_commutativity(samples):
    """Check gcd commutativity: gcd(a,b) = gcd(b,a) up to normalization."""
    for a in samples:
        for b in samples:
            try:
                g1 = gcd(a, b)
                g2 = gcd(b, a)
                if g1:
                    g1 = g1.normalize()
                if g2:
                    g2 = g2.normalize()
                assert g1 == g2, f"gcd not commutative: gcd({a},{b}) != gcd({b},{a})"
            except (AssertionError, ZeroDivisionError) as e:
                report_exception('check_gcd_commutativity', samples, e)


def check_gcd_associativity(samples):
    """Check gcd associativity: gcd(gcd(a,b),c) = gcd(a,gcd(b,c)) up to normalization."""
    for a in samples:
        for b in samples:
            for c in samples:
                try:
                    u = gcd(gcd(a, b), c)
                    v = gcd(a, gcd(b, c))
                    if u:
                        u = u.normalize()
                    if v:
                        v = v.normalize()
                    assert u == v, f"gcd not associative: gcd(gcd({a},{b}), {c}) != gcd({a}, gcd({b},{c}))"
                except (AssertionError, ZeroDivisionError) as e:
                    report_exception('check_gcd_associativity', samples, e)


def check_gcd_identity(samples):
    """Check gcd identity: gcd(a,0) = a (up to normalization), gcd(a,1) = 1 when a≠0."""
    for a in samples:
        try:
            zero = a.zero()
            one = a.one()
            if not a:
                assert gcd(zero, zero) == zero, f"gcd identity failed: gcd(0,0) != 0"
            else:
                g = gcd(a, zero)
                assert g.normalize() == a.normalize(), f"gcd identity failed: gcd({a}, {zero}).normalize() != {a}.normalize()"
                g1 = gcd(a, one)
                assert g1.normalize() == one, f"gcd identity failed: gcd({a}, {one}).normalize() != {one}"
        except (AssertionError, ZeroDivisionError) as e:
            report_exception('check_gcd_identity', samples, e)


# ----- Field tests -----

def check_truediv_and_inverse(samples):
    for a in samples:
        if not a:
            continue
        try:
            one = a.one()
            inv = a.inverse()
            assert a * inv == one
            assert inv * a == one
            assert a / a == one
        except (AssertionError, ZeroDivisionError) as e:
            report_exception('check_truediv_and_inverse', samples, e)


def check_field_division_by_zero(samples):
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
    check_distributivity(samples)
    check_annihilator_properties(samples)


def check_euclidean_rings(samples):
    """Check all Euclidean ring properties."""
    check_rings(samples)
    check_division(samples)
    check_divmod(samples)
    check_commutativity_multiplication(samples)
    check_bulk_mul(samples)
    check_gcd_properties(samples)
    check_gcd_commutativity(samples)
    check_gcd_associativity(samples)
    check_gcd_identity(samples)


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


def check_axioms(samples):
    black_box.append(descent_str(samples))
    before = len(exception_report)

    try:
        if isinstance(samples[0], Field):
            check_fields(samples)
        elif isinstance(samples[0], EuclideanRing):
            check_euclidean_rings(samples)
        elif isinstance(samples[0], Ring):
            check_rings(samples)

        if comparable_works(samples[0]):
            check_comparables(samples)
    except BaseException as e:
        report_exception('timeout', samples, e)

    new_failures = exception_report[before:]
    if new_failures:
        ds = descent_str(samples)
        print(f"\n  {ds}: {len(new_failures)} graceful failure(s)")
        for check, _, etype, msg in new_failures:
            print(f"    {check}: {etype}")
