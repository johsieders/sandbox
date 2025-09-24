# trying to understand primes
# js, reworked 19/07/2023
# checked 07/01/2024

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


def get_primes(n: int) -> list:
    """
    :param n: an integer > 2
    :return: a list of all primes < n
    """
    if n <= 2:
        raise ValueError(f"n must be greater than 2")
    ps = []
    for i in range(2, n):
        for p in ps:
            if i % p == 0:
                break
        else:
            ps.append(i)
    return ps


def primefactors(n: int, primes: List[int]) -> Tuple[List[int], int]:
    """
    :param n: a positive integer
    :param primes: an Iterator of primes in ascending order
    :return: a list of exponents of first N prime factors of n and the remaining factor of n
    """

    def aux(n: int, p: int) -> Tuple[int, int]:
        """
        :param n: an integer
        :param p: a prime number
        :return: exponent e of p in n and remaining factor r, so:
        n = (p ** e) * r
        examples:
        aux(28, 2) -> 2, 7
        aux(28, 5) -> 0, 28
        aux(28, 7) -> 1, 4
        """
        e = 0  # exponent
        r = n  # remaining factor
        while r % p == 0:
            e += 1
            r //= p
        return e, r

    if n < 1:
        raise ValueError('n must be positive')
    result = []
    for p in (q for q in primes if q <= n):
        e, n = aux(n, p)
        result.append(e)
        if n == 1:
            break
    return result, n


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


def factorize(n):
    primes = get_primes(n)
    x = []
    for i in primes:
        while n % i == 0: 
            x.append(i)
            n = n // i
        if i * i > n: 
            break
    if n > 1: 
        x.append(n)
    if len(x) == 1: 
        primes.append(x[0])
    return x


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
    unique_primes = list(set(factors))
    
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
    
    # Find all divisors of φ(m) by trial division
    divisors = []
    for i in range(1, int(phi_m**0.5) + 1):
        if phi_m % i == 0:
            divisors.append(i)
            if i != phi_m // i:
                divisors.append(phi_m // i)
    
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
    prime_factors_phi = list(set(factorize(phi_p)))
    
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




