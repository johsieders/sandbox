"""
Prime Number Theory and Modular Arithmetic Library

This module provides a comprehensive collection of algorithms for prime number theory
and modular arithmetic, essential for algebraic computations and cryptographic applications.

CORE PRIME FUNCTIONS:
- is_prime(n): Trial division primality test, O(√n)
- get_primes(n): Generator yielding all primes < n using trial division sieve
- factorize(m): Prime factorization returning [(prime, exponent)] tuples

MODULAR ARITHMETIC:
- gcd(a, b): Euclidean algorithm for greatest common divisor
- ext_gcd(a, b): Extended Euclidean algorithm returning (gcd, s, t) where gcd = a*s + b*t
- inv_mod(a, m): Modular multiplicative inverse when gcd(a, m) = 1
- chinese_remainder(remainders, moduli): Chinese Remainder Theorem solver

NUMBER THEORETIC FUNCTIONS:
- phi(m): Euler's totient function φ(m), count of integers ≤ m coprime to m
- ord(a, m): Multiplicative order of a modulo m (smallest k where a^k ≡ 1 mod m)
- find_generator(p): Finds primitive root of finite field F_p* for prime p

ALGORITHMIC NOTES:
- factorize() uses optimized trial division up to √m with early termination
- ord() uses factorization-based divisor generation instead of trial division
- phi() computed via φ(m) = m * ∏(1 - 1/p) for all prime factors p of m
- find_generator() uses Lagrange's theorem: tests g^((p-1)/q) ≢ 1 for prime factors q of p-1

MATHEMATICAL FOUNDATIONS:
- Euler's theorem: a^φ(m) ≡ 1 (mod m) when gcd(a, m) = 1
- Lagrange's theorem: ord(a) divides φ(m)
- Primitive root g generates all elements of (Z/pZ)* via powers g^0, g^1, ..., g^(p-2)

The implementation prioritizes mathematical correctness and follows standard number theory
algorithms. All functions handle edge cases and provide appropriate error checking.
Generated for rapid prototyping of algebraic structures and cryptographic primitives.

# js, reworked 19/07/2023
# checked 07/01/2024
# improved 27/09/2025 using Claude.
"""

from typing import Tuple, List, Sequence


def is_prime(n: int) -> bool:
    """
    Check if a number is prime using trial division up to the square root of n.
    """
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def get_primes(n: int):
    """
    Generator that yields all primes p with 2 <= p < n
    :param n: an integer >= 2
    :yields: prime numbers in ascending order
    """
    if n <= 1:
        raise ValueError(f"n must be greater than 1")
    elif n == 2:
        return

    ps = []
    for i in range(2, n):
        for p in ps:
            if i % p == 0:
                break
        else:
            ps.append(i)
            yield i


def gcd(a, b):
    """
    :param a: an element of an Euclidian ring
    :param b: another element of an Euclidian ring
    :return: gcd of a and b
    """
    while b:
        a, b = b, a % b
    return a


def ext_gcd(a, b) -> tuple:
    """
    :param a: an element of an Euclidian ring
    :param b: another element of an Euclidian ring
    :return: three elements g, s, t such that
            g = gcd(a, b) and
            g = a * s + b * t
    """
    s, u = 1, 0
    t, v = 0, 1

    while b:
        q, r = divmod(a, b)
        a, b = b, r
        s, u = u, s - q * u
        t, v = v, t - q * v
    return a, s, t


def inv_mod(a, m):
    """
    :param a: an element of an Euclidian ring
    :param m: another element of an Euclidian ring
    :return: inverse of a modulo m
    The inverse exists iff gcd(a, m) = 1
    Here is how it works:
    a * s + b * t = 1
    => a * s = 1 - b * t
    => a * s = 1 mod b
    """
    g, s, t = ext_gcd(a, m)
    if g != 1:  # g must be 1
        raise ValueError("No inverse for %d modulo %d" % (a, m))
    return s % m


def chinese_remainder(a: Sequence, coprimes: Sequence):
    """
    :param a: list of elements of an Euclidian ring
    :param coprimes: list of coprime elements of an Euclidian ring, often primes
    :return: x such that x = a[i] mod m[i] for all i

    Here is how it works:

    qi = N // pi (all i), so
    (pi, qj) = 1 if i == j, else 0

    xi = inv(qi, pi), so
    xi * qi = 1 mod pj if i == j, else 0
    ai * xi * qi = ai mod pj if i == j, else 0

    and therefore the solution is:

    x = sum_i(ai * xi * qi)
    """

    if len(a) != len(coprimes):
        raise ValueError("a and coprimes must have the same length")

    n = len(a)
    N = 1
    for i in range(n):
        N *= coprimes[i]

    qs = [N // p for p in coprimes]
    xs = [inv_mod(qs[i], coprimes[i]) for i in range(n)]

    x = 0
    for i in range(n):
        x += a[i] * xs[i] * qs[i]
    return x % N


def factorize(m: int) -> List[Tuple[int, int]]:
    """
    Factorize a positive integer n into its prime factors.
    Returns a list of tuples (prime, exponent) where prime^exponent
    divides n. The invariant is: M = product of all prime^exponent.
    """
    if m <= 1:
        return []

    factors = []

    for p in get_primes(int(m ** 0.5) + 1):
        if p * p > m:
            break
        exponent = 0
        while m % p == 0:
            exponent += 1
            m = m // p
        if exponent > 0:
            factors.append((p, exponent))

    if m > 1:
        factors.append((m, 1))

    return factors


def phi(m: int) -> int:
    """
    Compute Euler's totient function φ(m).
    
    φ(m) counts the number of integers from 1 to m that are coprime to m.
    
    Uses the formula: φ(m) = m * ∏(1 - 1/p) for all prime factors p of m
    Equivalently: φ(m) = m * ∏((p-1)/p) for all prime factors p of m
    
    :param m: a positive integer
    :return: φ(m), the number of integers ≤ m that are coprime to m
    """
    if m <= 0:
        raise ValueError("m must be positive")

    if m <= 2:
        return 1

    # Get unique prime factors using factorize
    factors = factorize(m)
    unique_primes = [p for p, exp in factors]

    result = m
    for p in unique_primes:
        # Apply the formula: multiply by (p-1)/p
        result = result * (p - 1) // p

    return result


def ord(a: int, m: int) -> int:
    """
    Compute the multiplicative order of a modulo m.
    
    The order of a modulo m is the smallest positive integer k such that
    a^k ≡ 1 (mod m).
    
    By Lagrange's theorem, ord(a) divides φ(m), so we only need to check
    the divisors of φ(m).
    
    :param a: an integer coprime to m
    :param m: a positive integer > 1
    :return: the multiplicative order of a modulo m
    :raises ValueError: if gcd(a, m) ≠ 1 or m ≤ 1
    """
    if m <= 1:
        raise ValueError("m must be greater than 1")

    if gcd(a, m) != 1:
        raise ValueError(f"gcd({a}, {m}) must be 1, but got {gcd(a, m)}")

    # Normalize a to be in range [0, m-1]
    a = a % m

    if a == 1:
        return 1

    # Get φ(m)
    phi_m = phi(m)

    # Find all divisors of φ(m) using prime factorization
    phi_factors = factorize(phi_m)

    # Generate all divisors from prime factorization
    divisors = [1]
    for prime, exponent in phi_factors:
        new_divisors = []
        for divisor in divisors:
            for exp in range(exponent + 1):
                new_divisors.append(divisor * (prime ** exp))
        divisors = new_divisors

    # Sort divisors to check smallest first
    divisors.sort()

    # Check each divisor to find the smallest k such that a^k ≡ 1 (mod m)
    for k in divisors:
        if pow(a, k, m) == 1:
            return k

    # This should never happen if the math is correct
    raise RuntimeError(f"Could not find order of {a} modulo {m}")


def find_generator(p: int) -> int:
    """
    Find a generator (primitive root) of the multiplicative group F_p*.
    
    A generator g of F_p* is an element such that ord(g) = p-1, meaning
    the powers g^0, g^1, g^2, ..., g^(p-2) generate all non-zero elements of F_p.
    
    Algorithm: Check each candidate g = 2, 3, 4, ... until we find one with
    ord(g) = p-1. For efficiency, we only need to verify that g^((p-1)/q) ≢ 1 (mod p)
    for all prime factors q of p-1.
    
    :param p: a prime number > 2
    :return: a generator of F_p*
    :raises ValueError: if p is not prime or p ≤ 2
    """
    if p <= 2:
        raise ValueError("p must be a prime > 2")

    if not is_prime(p):
        raise ValueError(f"{p} is not prime")

    # Special case for p = 3
    if p == 3:
        return 2  # 2 is a generator of F_3*

    # Find prime factors of p-1
    phi_p = p - 1  # φ(p) = p-1 for prime p
    prime_factors_phi = [prime for prime, exp in factorize(phi_p)]

    # Check candidates starting from 2
    for candidate in range(2, p):
        is_generator = True

        # Check that candidate^((p-1)/q) ≢ 1 (mod p) for all prime factors q of p-1
        for q in prime_factors_phi:
            if pow(candidate, phi_p // q, p) == 1:
                is_generator = False
                break

        if is_generator:
            return candidate

    # This should never happen for a prime p
    raise RuntimeError(f"Could not find generator for prime {p}")
