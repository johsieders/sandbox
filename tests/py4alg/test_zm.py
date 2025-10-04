# py4alg/tests/test_zm.py

import pytest

from sandbox.py4alg.mapper.m_zm import Zm
from sandbox.py4alg.protocols.p_abelian_group import AbelianGroup
from sandbox.py4alg.protocols.p_comparable import Comparable
from sandbox.py4alg.protocols.p_euclidean_ring import EuclideanRing
from sandbox.py4alg.protocols.p_ring import Ring
from tests.py4alg.check_properties import check_euclidean_rings, check_rings


# ----- Type/sample groupings -----

def test_isinstance():
    # Test with a composite modulus (not Euclidean ring)
    n = Zm(6, 3)
    assert isinstance(n, Zm)
    assert isinstance(n, Comparable)
    assert isinstance(n, AbelianGroup)
    assert isinstance(n, Ring)
    assert isinstance(n, EuclideanRing)


def zm_samples():
    moduli = [4, 6, 8, 9, 10, 12, 15, 16, 18, 20]
    samples = []
    for m in moduli:
        samples.append([Zm(m, a) for a in range(2 * m)])
    return samples


def zm_ring_samples():
    # Sample composite moduli for ring testing
    moduli = [4, 6, 8, 9, 10, 12, 15, 16, 18, 20]
    samples = []
    for m in moduli:
        samples.append([Zm(m, a) for a in range(m)])  # Just 0..m-1 to keep test size manageable
    return samples


@pytest.mark.parametrize("samples", zm_ring_samples())
def test_rings(samples):
    check_rings(samples)


# Only test Euclidean ring properties for prime moduli (which should be very limited since Fp handles those)
def zm_prime_samples():
    # These are technically handled by Fp, but we can test a few small ones
    primes = [2, 3, 5, 7]  # Very small primes only
    samples = []
    for p in primes:
        samples.append([Zm(p, a) for a in range(p)])
    return samples


@pytest.mark.parametrize("samples", zm_prime_samples())
def test_euclidean_rings_prime_moduli(samples):
    check_euclidean_rings(samples)


def test_zm_basic_operations():
    # Test basic ring operations for Z/6Z
    z6_2 = Zm(6, 2)
    z6_3 = Zm(6, 3)
    z6_4 = Zm(6, 4)

    # Addition
    assert z6_2 + z6_3 == Zm(6, 5)
    assert z6_3 + z6_4 == Zm(6, 1)  # 7 mod 6 = 1

    # Multiplication
    assert z6_2 * z6_3 == Zm(6, 0)  # 6 mod 6 = 0
    assert z6_2 * z6_2 == Zm(6, 4)

    # Zero divisors exist in Z/6Z
    assert z6_2 * z6_3 == Zm(6, 0)  # 2 * 3 = 6 ≡ 0 (mod 6)


def test_zm_zero_divisors():
    # Test that Z/8Z has zero divisors
    z8_2 = Zm(8, 2)
    z8_4 = Zm(8, 4)

    # 2 * 4 = 8 ≡ 0 (mod 8)
    assert z8_2 * z8_4 == Zm(8, 0)
    assert z8_2 != Zm(8, 0)
    assert z8_4 != Zm(8, 0)


def test_zm_division_fails_appropriately():
    # Test that division by zero divisors fails appropriately
    z6_2 = Zm(6, 2)
    z6_3 = Zm(6, 3)

    # 2 and 3 are not coprime to 6, so division should fail
    with pytest.raises(ZeroDivisionError):
        z6_2 // z6_3

    # Also test division by 1 should work (since gcd(1,6) = 1)
    z6_1 = Zm(6, 1)
    result = z6_2 // z6_1
    assert result == z6_2  # x // 1 = x

    # Test division by 5 should work (since gcd(5,6) = 1)
    z6_5 = Zm(6, 5)
    result = z6_1 // z6_5
    assert result == z6_5  # 1 // 5 = 5^(-1) = 5 (since 5*5 = 25 ≡ 1 (mod 6))