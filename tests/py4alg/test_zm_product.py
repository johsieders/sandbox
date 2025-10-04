# py4alg/tests/test_zm_product.py

import pytest

from sandbox.py4alg.mapper.m_modular_product import ZmProduct, FpProduct
from sandbox.py4alg.protocols.p_abelian_group import AbelianGroup
from sandbox.py4alg.protocols.p_euclidean_ring import EuclideanRing
from sandbox.py4alg.protocols.p_ring import Ring
from sandbox.py4alg.util.primes import get_primes
from tests.py4alg.check_properties import check_rings, check_euclidean_rings, check_fields
from tests.py4alg.test_zm import zm_ring_samples, zm_prime_samples
from tests.py4alg.test_fp import fp_samples


# ----- ZmProduct Tests -----

def test_zmproduct_isinstance():
    """Test that ZmProduct implements expected protocols"""
    z = ZmProduct([3, 5], [1, 2])
    assert isinstance(z, ZmProduct)
    assert isinstance(z, AbelianGroup)
    assert isinstance(z, Ring)
    assert isinstance(z, EuclideanRing)


def test_zmproduct_construction():
    """Test ZmProduct construction and validation"""
    # Valid construction
    z = ZmProduct([3, 5, 7], [1, 2, 3])
    assert z.moduli == (3, 5, 7)
    assert z.values == (1, 2, 3)
    assert z.M == 3 * 5 * 7

    # Automatic normalization
    z2 = ZmProduct([3, 5], [7, 11])
    assert z2.values == (1, 1)  # 7 % 3 = 1, 11 % 5 = 1

    # Invalid: mismatched lengths
    with pytest.raises(TypeError):
        ZmProduct([3, 5], [1])

    # Invalid: empty moduli
    with pytest.raises(ValueError):
        ZmProduct([], [])

    # Invalid: modulus <= 1
    with pytest.raises(ValueError):
        ZmProduct([1, 5], [0, 2])

    # Invalid: non-coprime moduli
    with pytest.raises(ValueError):
        ZmProduct([6, 9], [1, 2])  # gcd(6, 9) = 3


def test_zmproduct_chinese_remainder():
    """Test conversion to/from integer via CRT"""
    moduli = [3, 5, 7]

    # Test round-trip
    for n in range(0, 105, 5):  # 105 = 3*5*7
        z = ZmProduct.from_int(moduli, n)
        assert z.to_int() == n

    # Test specific example: x ≡ 2 (mod 3), x ≡ 3 (mod 5), x ≡ 2 (mod 7)
    z = ZmProduct([3, 5, 7], [2, 3, 2])
    x = z.to_int()
    assert x % 3 == 2
    assert x % 5 == 3
    assert x % 7 == 2


def test_zmproduct_basic_operations():
    """Test basic ring operations"""
    moduli = [3, 5]

    a = ZmProduct(moduli, [1, 2])
    b = ZmProduct(moduli, [2, 3])

    # Addition
    c = a + b
    assert c.values == (0, 0)  # (1+2) % 3 = 0, (2+3) % 5 = 0

    # Subtraction
    d = a - b
    assert d.values == (2, 4)  # (1-2) % 3 = 2, (2-3) % 5 = 4

    # Multiplication
    e = a * b
    assert e.values == (2, 1)  # (1*2) % 3 = 2, (2*3) % 5 = 1

    # Negation
    f = -a
    assert f.values == (2, 3)  # -1 % 3 = 2, -2 % 5 = 3

    # Zero and one
    assert a.zero().values == (0, 0)
    assert a.one().values == (1, 1)


def test_zmproduct_division():
    """Test division in ZmProduct"""
    moduli = [5, 7]  # Coprime moduli

    a = ZmProduct(moduli, [3, 4])
    b = ZmProduct(moduli, [2, 3])

    # Division should work when inverse exists
    c = a // b
    # Verify: c * b == a
    assert (c * b).values == a.values

    # Division by zero should fail
    zero = ZmProduct(moduli, [0, 0])
    with pytest.raises(ZeroDivisionError):
        a // zero

    # Division by element with no inverse should fail
    # In Z/4Z, 2 has no inverse (gcd(2,4) = 2)
    moduli2 = [4, 5]
    a2 = ZmProduct(moduli2, [1, 1])
    b2 = ZmProduct(moduli2, [2, 1])  # 2 has no inverse in Z/4Z
    with pytest.raises(ZeroDivisionError):
        a2 // b2


def test_zmproduct_equality():
    """Test equality comparison"""
    moduli = [3, 5]

    a = ZmProduct(moduli, [1, 2])
    b = ZmProduct(moduli, [1, 2])
    c = ZmProduct(moduli, [1, 3])
    d = ZmProduct([3, 7], [1, 2])  # Different moduli

    assert a == b
    assert a != c
    assert a != d
    assert a != "not a ZmProduct"


def test_zmproduct_bool_and_norm():
    """Test boolean conversion and norm"""
    moduli = [3, 5]

    zero = ZmProduct(moduli, [0, 0])
    nonzero1 = ZmProduct(moduli, [1, 0])
    nonzero2 = ZmProduct(moduli, [0, 1])
    nonzero3 = ZmProduct(moduli, [2, 3])

    assert not zero
    assert nonzero1
    assert nonzero2
    assert nonzero3

    # Norm is sum of absolute values
    assert zero.norm() == 0
    assert nonzero1.norm() == 1
    assert nonzero2.norm() == 1
    assert nonzero3.norm() == 5


def test_zmproduct_gcd():
    """Test GCD operation"""
    moduli = [5, 7]  # Coprime moduli

    a = ZmProduct(moduli, [4, 6])
    b = ZmProduct(moduli, [2, 4])

    g = a.gcd(b)
    # gcd(4, 2) = 2 in Z/5Z
    # gcd(6, 4) = 2 in Z/7Z
    assert g.values == (2, 2)


def zmproduct_samples():
    """Generate samples for property-based testing"""
    # Test with various coprime moduli combinations
    moduli_sets = [
        [3, 5],
        [3, 5, 7],
        [4, 9],  # Powers of different primes
        [5, 8, 9],
    ]

    samples = []
    for moduli in moduli_sets:
        M = 1
        for m in moduli:
            M *= m
        # Generate samples from 0 to M-1
        sample_set = [ZmProduct.from_int(moduli, n) for n in range(min(M, 50))]
        samples.append(sample_set)

    return samples


@pytest.mark.parametrize("samples", zmproduct_samples())
def test_zmproduct_rings(samples):
    """Test ring axioms for ZmProduct"""
    check_rings(samples)


# ----- FpProduct Tests -----

def test_fpproduct_isinstance():
    """Test that FpProduct implements expected protocols"""
    f = FpProduct([3, 5], [1, 2])
    assert isinstance(f, FpProduct)
    assert isinstance(f, ZmProduct)  # Test inheritance
    assert isinstance(f, AbelianGroup)
    assert isinstance(f, Ring)
    assert isinstance(f, EuclideanRing)
    # Note: FpProduct is NOT a Field - it has zero divisors like (1,0) * (0,1) = (0,0)


def test_fpproduct_construction():
    """Test FpProduct construction and validation"""
    # Valid construction
    f = FpProduct([3, 5, 7], [1, 2, 3])
    assert f.primes == (3, 5, 7)
    assert f.moduli == (3, 5, 7)  # Alias
    assert f.values == (1, 2, 3)

    # With primality check
    f2 = FpProduct([3, 5], [1, 2], check=True)
    assert f2.values == (1, 2)

    # Invalid: non-prime with check
    with pytest.raises(ValueError):
        FpProduct([4, 5], [1, 2], check=True)

    # Invalid: duplicate primes (not coprime)
    with pytest.raises(ValueError):
        FpProduct([3, 3], [1, 2])


def test_fpproduct_inheritance():
    """Test that FpProduct properly inherits from ZmProduct"""
    f = FpProduct([3, 5], [1, 2])
    assert isinstance(f, ZmProduct)

    # Test that operations return FpProduct type
    f2 = FpProduct([3, 5], [2, 3])
    result = f + f2
    assert isinstance(result, FpProduct)
    assert result.primes == (3, 5)


def test_fpproduct_basic_operations():
    """Test basic field operations"""
    primes = [3, 5]

    a = FpProduct(primes, [1, 2])
    b = FpProduct(primes, [2, 3])

    # Addition
    c = a + b
    assert isinstance(c, FpProduct)
    assert c.values == (0, 0)

    # Subtraction
    d = a - b
    assert isinstance(d, FpProduct)
    assert d.values == (2, 4)

    # Multiplication
    e = a * b
    assert isinstance(e, FpProduct)
    assert e.values == (2, 1)

    # Negation
    f = -a
    assert isinstance(f, FpProduct)
    assert f.values == (2, 3)


def test_fpproduct_division():
    """Test division in FpProduct (always works for non-zero elements)"""
    primes = [3, 5, 7]

    a = FpProduct(primes, [1, 2, 3])
    b = FpProduct(primes, [2, 3, 4])

    # True division
    c = a / b
    assert isinstance(c, FpProduct)
    # Verify: c * b == a
    assert (c * b).values == a.values

    # Floor division (same as true division in fields)
    d = a // b
    assert d.values == c.values

    # Division by zero should fail
    zero = FpProduct(primes, [0, 0, 0])
    with pytest.raises(ZeroDivisionError):
        a / zero


def test_fpproduct_inverse():
    """Test multiplicative inverse"""
    primes = [3, 5, 7]

    # Test inverse of (1, 2, 3)
    a = FpProduct(primes, [1, 2, 3])
    inv = a.inverse()
    product = a * inv
    assert product.values == (1, 1, 1)  # Should be one

    # Test all non-zero elements have inverses
    for i in range(1, 3):
        for j in range(1, 5):
            for k in range(1, 7):
                elem = FpProduct(primes, [i, j, k])
                inv = elem.inverse()
                assert (elem * inv) == elem.one()

    # Zero should not have inverse
    zero = FpProduct(primes, [0, 0, 0])
    with pytest.raises(ZeroDivisionError):
        zero.inverse()

    # Partial zero should not have inverse
    partial = FpProduct(primes, [1, 0, 1])
    with pytest.raises(ZeroDivisionError):
        partial.inverse()


def test_fpproduct_gcd():
    """Test GCD in FpProduct (always 1 unless both are zero)"""
    primes = [3, 5]

    a = FpProduct(primes, [1, 2])
    b = FpProduct(primes, [2, 3])

    # gcd of non-zero elements is one
    g = a.gcd(b)
    assert g.values == (1, 1)

    # gcd with zero
    zero = FpProduct(primes, [0, 0])
    g2 = a.gcd(zero)
    assert g2.values == (1, 1)

    # gcd of two zeros is zero
    g3 = zero.gcd(zero)
    assert g3.values == (0, 0)

    # Partial zeros
    partial1 = FpProduct(primes, [1, 0])
    partial2 = FpProduct(primes, [0, 2])
    g4 = partial1.gcd(partial2)
    assert g4.values == (1, 1)


def test_fpproduct_chinese_remainder():
    """Test CRT conversion for FpProduct"""
    primes = [3, 5, 7]
    M = 3 * 5 * 7

    # Test round-trip
    for n in range(0, M, 7):
        f = FpProduct.from_int(primes, n)
        assert f.to_int() == n


def fpproduct_samples():
    """Generate samples for property-based testing"""
    # Get small primes
    all_primes = list(get_primes(20))

    # Test with various prime combinations
    prime_sets = [
        [2, 3],
        [3, 5],
        [2, 5, 7],
        [3, 5, 7],
        [5, 7, 11],
        [2, 3, 5, 7],
    ]

    samples = []
    for primes in prime_sets:
        M = 1
        for p in primes:
            M *= p
        # Generate samples from 0 to M-1 (or up to 60 elements max)
        sample_set = [FpProduct.from_int(primes, n) for n in range(min(M, 60))]
        samples.append(sample_set)

    return samples


@pytest.mark.parametrize("samples", fpproduct_samples())
def test_fpproduct_rings(samples):
    """Test ring axioms for FpProduct"""
    check_rings(samples)


# Note: FpProduct is NOT a field, so we don't test field axioms
# It has zero divisors: (1,0) * (0,1) = (0,0)
# Only elements with ALL non-zero components are units (have inverses)


def test_fpproduct_divmod():
    """Test divmod operation"""
    primes = [3, 5]

    a = FpProduct(primes, [2, 3])
    b = FpProduct(primes, [1, 2])

    q, r = divmod(a, b)
    assert isinstance(q, FpProduct)
    assert isinstance(r, FpProduct)
    assert r.values == (0, 0)  # Remainder always zero in a field
    assert (q * b) == a


def test_zmproduct_modulo():
    """Test modulo operation"""
    moduli = [3, 5]

    a = ZmProduct(moduli, [2, 3])
    b = ZmProduct(moduli, [1, 2])

    # In rings, modulo returns zero (not a meaningful operation)
    r = a % b
    assert r.values == (0, 0)


# ----- Adapter Tests: ZmProduct/FpProduct with single modulus should behave like Zm/Fp -----

def zm_to_zmproduct_factory(m: int, n: int) -> ZmProduct:
    """Factory adapter: Zm(m, n) → ZmProduct([m], [n])"""
    return ZmProduct([m], [n])


def fp_to_fpproduct_factory(p: int, n: int) -> FpProduct:
    """Factory adapter: Fp(p, n) → FpProduct([p], [n])"""
    return FpProduct([p], [n])


@pytest.mark.parametrize("samples", zm_ring_samples(factory=zm_to_zmproduct_factory))
def test_zmproduct_single_modulus_matches_zm_rings(samples):
    """ZmProduct with single modulus should pass all Zm ring tests"""
    check_rings(samples)


@pytest.mark.parametrize("samples", zm_prime_samples(factory=zm_to_zmproduct_factory))
def test_zmproduct_single_modulus_matches_zm_euclidean_rings(samples):
    """ZmProduct with single prime modulus should pass Zm Euclidean ring tests"""
    check_euclidean_rings(samples)


@pytest.mark.parametrize("samples", fp_samples(factory=fp_to_fpproduct_factory))
def test_fpproduct_single_prime_matches_fp_euclidean_rings(samples):
    """FpProduct with single prime should pass all Fp Euclidean ring tests"""
    check_euclidean_rings(samples)


@pytest.mark.parametrize("samples", fp_samples(factory=fp_to_fpproduct_factory))
def test_fpproduct_single_prime_matches_fp_fields(samples):
    """FpProduct with single prime should pass all Fp field tests"""
    check_fields(samples)
