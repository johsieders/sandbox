import pytest
from sandbox.py4alg.util.primes import (
    is_prime, get_primes, primefactors, gcd, ext_gcd, 
    inv_mod, chinese_remainder, factorize, phi, ord, find_generator
)

# Test cases for is_prime
IS_PRIME_CASES = [
    (0, False), (1, False), (2, True), (3, True), (4, False),
    (5, True), (7, True), (11, True), (13, True), (17, True), (19, True),
    (23, True), (29, True), (31, True), (37, True), (41, True), (43, True),
    (97, True), (101, True), (997, True),
    (6, False), (8, False), (9, False), (10, False), (12, False), (15, False),
    (21, False), (25, False), (27, False), (49, False), (100, False), (121, False),
    (1009, True), (1013, True), (1021, True), (1031, True),
    (1000, False), (1024, False)
]

# Test cases for get_primes
GET_PRIMES_CASES = [
    (3, [2]),
    (10, [2, 3, 5, 7]),
    (20, [2, 3, 5, 7, 11, 13, 17, 19]),
    (30, [2, 3, 5, 7, 11, 13, 17, 19, 23, 29])
]

# Test cases for gcd
GCD_CASES = [
    (48, 18, 6),
    (17, 13, 1),
    (100, 25, 25),
    (0, 5, 5),
    (5, 0, 5),
    (12, 8, 4),
    (21, 14, 7),
    (1, 1, 1)
]

# Test cases for factorize
FACTORIZE_CASES = [
    (12, [2, 2, 3]),
    (30, [2, 3, 5]),
    (17, [17]),
    (100, [2, 2, 5, 5]),
#    (1, []),
#    (2, [2]),
    (4, [2, 2]),
    (9, [3, 3]),
]

# Test cases for phi
PHI_CASES = [
    (1, 1), (2, 1), (3, 2), (4, 2), (5, 4), (6, 2), (7, 6), (8, 4),
    (9, 6), (10, 4), (12, 4), (15, 8), (16, 8), (17, 16), (20, 8),
    (21, 12), (30, 8), (100, 40),
]

# Test cases for ord
ORD_CASES = [
    (1, 5, 1), (2, 5, 4), (3, 5, 4), (4, 5, 2),
    (2, 7, 3), (3, 7, 6), (4, 7, 3), (5, 7, 6), (6, 7, 2),
    (3, 8, 2), (5, 8, 2), (7, 8, 2),
    (2, 9, 6), (4, 9, 3), (5, 9, 6), (7, 9, 3), (8, 9, 2),
    (3, 10, 4), (7, 10, 4), (9, 10, 2),
    (2, 11, 10), (10, 11, 2),
    (2, 13, 12), (3, 13, 3),
]

# Test cases for chinese_remainder
CHINESE_REMAINDER_CASES = [
    ([2, 3, 2], [3, 5, 7], 23),
    ([1, 2], [3, 5], 11),
    ([0], [5], 0),
]

# Test cases for find_generator (just test that result has correct order)
FIND_GENERATOR_CASES = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]

# Test cases for inv_mod
INV_MOD_CASES = [
    (3, 7, 5),   # 3 * 5 = 15 ≡ 1 (mod 7)
    (5, 11, 9),  # 5 * 9 = 45 ≡ 1 (mod 11) 
    (7, 13, 2),  # 7 * 2 = 14 ≡ 1 (mod 13)
]


@pytest.mark.parametrize("n, expected", IS_PRIME_CASES)
def test_is_prime(n, expected):
    assert is_prime(n) == expected


@pytest.mark.parametrize("n, expected", GET_PRIMES_CASES)
def test_get_primes(n, expected):
    assert get_primes(n) == expected


def test_get_primes_error():
    with pytest.raises(ValueError):
        get_primes(1)


@pytest.mark.parametrize("a, b, expected", GCD_CASES)
def test_gcd(a, b, expected):
    assert gcd(a, b) == expected


@pytest.mark.parametrize("a, b", [(48, 18), (17, 13), (100, 25), (12, 8), (21, 14)])
def test_ext_gcd(a, b):
    g, s, t = ext_gcd(a, b)
    expected_gcd = gcd(a, b)
    assert g == expected_gcd
    assert g == a * s + b * t


@pytest.mark.parametrize("a, m, expected_inv", INV_MOD_CASES)
def test_inv_mod(a, m, expected_inv):
    inv = inv_mod(a, m)
    assert (a * inv) % m == 1


def test_inv_mod_error():
    with pytest.raises(ValueError):
        inv_mod(6, 9)  # gcd(6, 9) = 3 ≠ 1


@pytest.mark.parametrize("remainders, moduli, expected", CHINESE_REMAINDER_CASES)
def test_chinese_remainder(remainders, moduli, expected):
    result = chinese_remainder(remainders, moduli)
    # Verify the solution satisfies all congruences
    for i in range(len(remainders)):
        assert result % moduli[i] == remainders[i]


def test_chinese_remainder_error():
    with pytest.raises(ValueError):
        chinese_remainder([1, 2, 3], [4, 5])  # Mismatched lengths


@pytest.mark.parametrize("n, expected_factors", FACTORIZE_CASES)
def test_factorize(n, expected_factors):
    result = factorize(n)
    assert sorted(result) == sorted(expected_factors)
    # Verify product equals original number
    if result:
        product = 1
        for factor in result:
            product *= factor
        assert product == n


def test_primefactors():
    primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    
    # Test a few key cases
    factors, remainder = primefactors(12, primes_list)
    assert factors == [2, 1]
    assert remainder == 1
    
    factors, remainder = primefactors(30, primes_list)
    assert factors == [1, 1, 1]
    assert remainder == 1


def test_primefactors_error():
    with pytest.raises(ValueError):
        primefactors(-1, [2, 3, 5])


@pytest.mark.parametrize("m, expected", PHI_CASES)
def test_phi(m, expected):
    assert phi(m) == expected


def test_phi_error():
    with pytest.raises(ValueError):
        phi(0)
    with pytest.raises(ValueError):
        phi(-5)


@pytest.mark.parametrize("a, m, expected", ORD_CASES)
def test_ord(a, m, expected):
    result = ord(a, m)
    assert result == expected
    # Verify that a^result ≡ 1 (mod m)
    assert pow(a, result, m) == 1


def test_ord_errors():
    with pytest.raises(ValueError):
        ord(2, 1)  # m must be > 1
    with pytest.raises(ValueError):
        ord(4, 8)  # gcd(4, 8) ≠ 1


@pytest.mark.parametrize("p", FIND_GENERATOR_CASES)
def test_find_generator(p):
    result = find_generator(p)
    # Verify that the result is indeed a generator (order = p-1)
    expected_order = p - 1
    actual_order = ord(result, p)
    assert actual_order == expected_order


def test_find_generator_errors():
    with pytest.raises(ValueError):
        find_generator(1)  # p must be > 2
    with pytest.raises(ValueError):
        find_generator(2)  # p must be > 2
    with pytest.raises(ValueError):
        find_generator(4)  # not prime
