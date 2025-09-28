from sandbox.py4alg.util.primes import (
    is_prime, get_primes, gcd, lcm, ext_gcd,
    inv_mod, chinese_remainder, factorize, phi, ord, find_generator
)


def test_factorize_product_invariant():
    """Test that the product of factors equals the original number."""
    test_values = [12, 30, 17, 100, 4, 9, 60, 105, 127, 999]
    for n in test_values:
        factors = factorize(n)
        product = 1
        for prime, exponent in factors:
            product *= prime ** exponent
        assert product == n
        # All primes in factors should be prime
        for prime, exponent in factors:
            assert is_prime(prime)
            assert exponent > 0


def test_ext_gcd_diophantine_invariant():
    """Test that ext_gcd satisfies the Diophantine equation: gcd(a,b) = a*s + b*t."""
    test_pairs = [(48, 18), (17, 13), (100, 25), (12, 8), (21, 14), (97, 31), (1001, 91)]
    for a, b in test_pairs:
        g, s, t = ext_gcd(a, b)
        # Check Diophantine equation
        assert g == a * s + b * t
        # Check that g is indeed the gcd
        assert g == gcd(a, b)
        # gcd should divide both a and b
        if g > 0:
            assert a % g == 0
            assert b % g == 0


def test_inv_mod_multiplicative_inverse_invariant():
    """Test that inv_mod returns a true multiplicative inverse: (a * inv) ≡ 1 (mod m)."""
    test_cases = [(3, 7), (5, 11), (7, 13), (17, 23), (19, 29), (13, 31)]
    for a, m in test_cases:
        if gcd(a, m) == 1:  # Only test when inverse exists
            inv = inv_mod(a, m)
            assert (a * inv) % m == 1


def test_find_generator_is_generator_invariant():
    """Test that find_generator returns an element of order p-1."""
    test_primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for p in test_primes:
        g = find_generator(p)
        # Generator must have order p-1
        assert ord(g, p) == p - 1
        # Verify by checking that g^(p-1) ≡ 1 (mod p) and no smaller power works
        assert pow(g, p - 1, p) == 1
        # Check that g generates all elements 1, 2, ..., p-1
        generated = set()
        power = 1
        for i in range(p - 1):
            generated.add(power)
            power = (power * g) % p
        assert generated == set(range(1, p))


def test_ord_divides_phi_invariant():
    """Test that ord(a, m) divides φ(m) (Lagrange's theorem)."""
    test_cases = [(2, 5), (3, 7), (2, 9), (5, 8), (3, 10), (7, 13), (5, 17)]
    for a, m in test_cases:
        if gcd(a, m) == 1:  # Only test when ord is defined
            order = ord(a, m)
            phi_m = phi(m)
            assert phi_m % order == 0
            # Also verify that a^ord(a) ≡ 1 (mod m)
            assert pow(a, order, m) == 1


def test_phi_multiplicative_property():
    """Test multiplicative property of phi: if gcd(a,b)=1, then φ(ab)=φ(a)φ(b)."""
    test_pairs = [(3, 5), (7, 11), (4, 9), (5, 8)]  # Coprime pairs
    for a, b in test_pairs:
        if gcd(a, b) == 1:
            phi_a = phi(a)
            phi_b = phi(b)
            phi_ab = phi(a * b)
            assert phi_ab == phi_a * phi_b


def test_chinese_remainder_solution_invariant():
    """Test that chinese_remainder produces a solution satisfying all congruences."""
    test_cases = [
        ([2, 3, 2], [3, 5, 7]),
        ([1, 2], [3, 5]),
        ([0, 1], [2, 3]),
        ([1, 0, 3], [5, 7, 11])
    ]
    for remainders, moduli in test_cases:
        # Check moduli are pairwise coprime
        for i in range(len(moduli)):
            for j in range(i + 1, len(moduli)):
                if gcd(moduli[i], moduli[j]) != 1:
                    continue  # Skip if not coprime

        x = chinese_remainder(remainders, moduli)
        # Verify x satisfies all congruences
        for i in range(len(remainders)):
            assert x % moduli[i] == remainders[i]


def test_gcd_symmetry_and_properties():
    """Test gcd properties: symmetry, associativity hints, and divisibility."""
    test_triples = [(48, 18, 6), (60, 40, 20), (35, 21, 14)]

    for a, b, c in test_triples:
        g = gcd(a, b)
        # Symmetry
        assert gcd(a, b) == gcd(b, a)
        # gcd divides both operands
        assert a % g == 0
        assert b % g == 0
        # gcd properties with a third number
        assert gcd(gcd(a, b), c) == gcd(a, gcd(b, c))


def test_is_prime_factorization_consistency():
    """Test that is_prime is consistent with factorization."""
    test_numbers = [3, 4, 5, 6, 7, 8, 9, 11, 13, 15, 17, 21, 23, 25, 29]

    for n in test_numbers:
        if n > 1:
            prime_check = is_prime(n)
            factors = factorize(n)
            # If prime, should have exactly one factor (itself with exponent 1)
            if prime_check:
                assert len(factors) == 1
                assert factors[0] == (n, 1)
            # If composite, should have more than one prime factor (counting multiplicity)
            else:
                total_exponents = sum(exp for prime, exp in factors)
                assert total_exponents > 1


def test_get_primes_all_prime_invariant():
    """Test that get_primes returns only prime numbers."""
    for limit in [10, 20, 30, 50]:
        primes = list(get_primes(limit))
        # All returned numbers should be prime
        for p in primes:
            assert is_prime(p)
        # All primes less than limit should be included
        for candidate in range(2, limit):
            if is_prime(candidate):
                assert candidate in primes


def test_lcm_fundamental_property():
    """Test the fundamental lcm property: lcm(a,b) * gcd(a,b) = |a * b|."""
    test_pairs = [
        (12, 18), (15, 25), (7, 11), (8, 12), (21, 14), (100, 25),
        (17, 13), (48, 18), (35, 21), (60, 40), (9, 15), (16, 20)
    ]
    for a, b in test_pairs:
        lcm_ab = lcm(a, b)
        gcd_ab = gcd(a, b)
        assert lcm_ab * gcd_ab == abs(a * b)


def test_lcm_properties():
    """Test lcm mathematical properties: commutativity, associativity, identity."""
    test_triples = [(6, 8, 12), (15, 20, 25), (7, 14, 21), (4, 6, 9)]

    for a, b, c in test_triples:
        # Commutativity: lcm(a,b) = lcm(b,a)
        assert lcm(a, b) == lcm(b, a)

        # Associativity: lcm(lcm(a,b),c) = lcm(a,lcm(b,c))
        assert lcm(lcm(a, b), c) == lcm(a, lcm(b, c))

        # Identity: lcm(a,1) = a for positive a
        assert lcm(a, 1) == a
        assert lcm(1, a) == a

        # Absorption: lcm(a,0) = 0
        assert lcm(a, 0) == 0
        assert lcm(0, a) == 0


def test_lcm_divisibility():
    """Test that lcm(a,b) is divisible by both a and b, and is minimal."""
    test_pairs = [(6, 9), (8, 12), (15, 20), (7, 21), (10, 25), (14, 35)]

    for a, b in test_pairs:
        lcm_ab = lcm(a, b)

        # lcm(a,b) must be divisible by both a and b
        assert lcm_ab % a == 0
        assert lcm_ab % b == 0

        # lcm(a,b) should be the smallest positive number divisible by both
        # Check that any smaller positive number is not divisible by both
        for candidate in range(1, lcm_ab):
            assert not (candidate % a == 0 and candidate % b == 0)


def test_lcm_edge_cases():
    """Test lcm edge cases and error conditions."""
    # lcm with same numbers
    assert lcm(7, 7) == 7
    assert lcm(12, 12) == 12

    # lcm with 1
    assert lcm(1, 15) == 15
    assert lcm(23, 1) == 23
    assert lcm(1, 1) == 1

    # lcm with 0
    assert lcm(0, 5) == 0
    assert lcm(8, 0) == 0
    assert lcm(-7, 0) == 0
    assert lcm(0, -3) == 0

    # lcm with negative numbers (should handle absolute values)
    assert lcm(-6, 8) == lcm(6, 8)
    assert lcm(6, -8) == lcm(6, 8)
    assert lcm(-6, -8) == lcm(6, 8)

    # Error case: lcm(0, 0)
    try:
        lcm(0, 0)
        assert False, "Should raise ValueError for lcm(0, 0)"
    except ValueError:
        pass  # Expected


def test_lcm_coprime_numbers():
    """Test that lcm of coprime numbers equals their product."""
    coprime_pairs = [(3, 7), (5, 11), (8, 9), (7, 15), (13, 17), (4, 25)]

    for a, b in coprime_pairs:
        if gcd(a, b) == 1:  # Verify they are coprime
            assert lcm(a, b) == a * b
