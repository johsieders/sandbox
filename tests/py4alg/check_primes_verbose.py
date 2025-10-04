#!/usr/bin/env python3
"""
Test driver for all functions in sandbox.py4alg.util.primes module.
Comprehensive testing with edge cases and known mathematical properties.
"""

import traceback

from sandbox.py4alg.util.primes import (
    is_prime, get_primes, gcd, gcd_extended,
    mod_inverse, chinese_remainder, factorize, phi, ord, find_generator
)


def test_is_prime():
    """Test the is_prime function with various inputs."""
    print("Testing is_prime function...")

    # Edge cases
    test_cases = [
        (0, False), (1, False), (2, True), (3, True), (4, False),
        # Known primes
        (5, True), (7, True), (11, True), (13, True), (17, True), (19, True),
        (23, True), (29, True), (31, True), (37, True), (41, True), (43, True),
        (97, True), (101, True), (997, True),
        # Known composites
        (6, False), (8, False), (9, False), (10, False), (12, False), (15, False),
        (21, False), (25, False), (27, False), (49, False), (100, False), (121, False),
        # Larger numbers
        (1009, True), (1013, True), (1021, True), (1031, True),
        (1000, False), (1024, False)
    ]

    passed = 0
    total = len(test_cases)

    for n, expected in test_cases:
        try:
            result = is_prime(n)
            if result == expected:
                passed += 1
                print(f"  ✓ is_prime({n}) = {result}")
            else:
                print(f"  ✗ is_prime({n}) = {result}, expected {expected}")
        except Exception as e:
            print(f"  ✗ is_prime({n}) raised exception: {e}")

    print(f"  Passed: {passed}/{total}\n")
    return passed == total


def test_get_primes():
    """Test the get_primes function."""
    print("Testing get_primes function...")

    test_cases = [
        (3, [2]),
        (10, [2, 3, 5, 7]),
        (20, [2, 3, 5, 7, 11, 13, 17, 19]),
        (30, [2, 3, 5, 7, 11, 13, 17, 19, 23, 29])
    ]

    passed = 0
    total = len(test_cases)

    for n, expected in test_cases:
        try:
            result = list(get_primes(n))
            if result == expected:
                passed += 1
                print(f"  ✓ get_primes({n}) = {result}")
            else:
                print(f"  ✗ get_primes({n}) = {result}, expected {expected}")
        except Exception as e:
            print(f"  ✗ get_primes({n}) raised exception: {e}")

    # Test error case
    try:
        get_primes(1)
        print(f"  ✗ get_primes(1) should raise ValueError")
    except ValueError:
        print(f"  ✓ get_primes(1) correctly raised ValueError")
        passed += 1
        total += 1
    except Exception as e:
        print(f"  ✗ get_primes(1) raised unexpected exception: {e}")
        total += 1

    print(f"  Passed: {passed}/{total}\n")
    return passed == total


def test_gcd():
    """Test the gcd function."""
    print("Testing gcd function...")

    test_cases = [
        (48, 18, 6),
        (17, 13, 1),
        (100, 25, 25),
        (0, 5, 5),
        (5, 0, 5),
        (12, 8, 4),
        (21, 14, 7),
        (1, 1, 1)
    ]

    passed = 0
    total = len(test_cases)

    for a, b, expected in test_cases:
        try:
            result = gcd(a, b)
            if result == expected:
                passed += 1
                print(f"  ✓ gcd({a}, {b}) = {result}")
            else:
                print(f"  ✗ gcd({a}, {b}) = {result}, expected {expected}")
        except Exception as e:
            print(f"  ✗ gcd({a}, {b}) raised exception: {e}")

    print(f"  Passed: {passed}/{total}\n")
    return passed == total


def test_ext_gcd():
    """Test the ext_gcd function."""
    print("Testing ext_gcd function...")

    test_cases = [
        (48, 18),
        (17, 13),
        (100, 25),
        (12, 8),
        (21, 14)
    ]

    passed = 0
    total = len(test_cases)

    for a, b in test_cases:
        try:
            g, s, t = gcd_extended(a, b)
            # Verify that g = gcd(a,b) and g = a*s + b*t
            expected_gcd = gcd(a, b)
            linear_combination = a * s + b * t

            if g == expected_gcd and g == linear_combination:
                passed += 1
                print(f"  ✓ ext_gcd({a}, {b}) = ({g}, {s}, {t})")
                print(f"    Verification: {a}*{s} + {b}*{t} = {linear_combination}")
            else:
                print(f"  ✗ ext_gcd({a}, {b}) = ({g}, {s}, {t})")
                print(f"    Expected gcd: {expected_gcd}, got: {g}")
                print(f"    Linear combination: {a}*{s} + {b}*{t} = {linear_combination}")
        except Exception as e:
            print(f"  ✗ ext_gcd({a}, {b}) raised exception: {e}")

    print(f"  Passed: {passed}/{total}\n")
    return passed == total


def test_inv_mod():
    """Test the inv_mod function."""
    print("Testing inv_mod function...")

    # Test cases where inverse exists
    test_cases = [
        (3, 7),  # 3 * 5 = 15 ≡ 1 (mod 7)
        (5, 11),  # 5 * 9 = 45 ≡ 1 (mod 11)
        (7, 13),  # 7 * 2 = 14 ≡ 1 (mod 13)
    ]

    passed = 0
    total = len(test_cases)

    for a, m in test_cases:
        try:
            inv = mod_inverse(a, m)
            # Verify that (a * inv) % m == 1
            if (a * inv) % m == 1:
                passed += 1
                print(f"  ✓ inv_mod({a}, {m}) = {inv}")
                print(f"    Verification: {a} * {inv} ≡ {(a * inv) % m} (mod {m})")
            else:
                print(f"  ✗ inv_mod({a}, {m}) = {inv}")
                print(f"    Verification failed: {a} * {inv} ≡ {(a * inv) % m} (mod {m})")
        except Exception as e:
            print(f"  ✗ inv_mod({a}, {m}) raised exception: {e}")

    # Test error case (no inverse exists)
    try:
        mod_inverse(6, 9)  # gcd(6, 9) = 3 ≠ 1
        print(f"  ✗ inv_mod(6, 9) should raise ValueError")
    except ValueError:
        print(f"  ✓ inv_mod(6, 9) correctly raised ValueError")
        passed += 1
        total += 1
    except Exception as e:
        print(f"  ✗ inv_mod(6, 9) raised unexpected exception: {e}")
        total += 1

    print(f"  Passed: {passed}/{total}\n")
    return passed == total


def test_chinese_remainder():
    """Test the chinese_remainder function."""
    print("Testing chinese_remainder function...")

    # Test case: x ≡ 2 (mod 3), x ≡ 3 (mod 5), x ≡ 2 (mod 7)
    # Solution: x ≡ 23 (mod 105)
    test_cases = [
        ([2, 3, 2], [3, 5, 7], 23),
        ([1, 2], [3, 5], 11),  # x ≡ 1 (mod 3), x ≡ 2 (mod 5) → x ≡ 7 (mod 15)
        ([0], [5], 0),  # x ≡ 0 (mod 5) → x = 0
    ]

    passed = 0
    total = len(test_cases)

    for remainders, moduli, expected in test_cases:
        try:
            result = chinese_remainder(remainders, moduli)
            # Verify the solution
            valid = True
            for i in range(len(remainders)):
                if result % moduli[i] != remainders[i]:
                    valid = False
                    break

            if valid and result == expected:
                passed += 1
                print(f"  ✓ chinese_remainder({remainders}, {moduli}) = {result}")
                # Show verification
                verification = [f"{result} ≡ {result % moduli[i]} (mod {moduli[i]})" for i in range(len(moduli))]
                print(f"    Verification: {', '.join(verification)}")
            else:
                print(f"  ✗ chinese_remainder({remainders}, {moduli}) = {result}, expected {expected}")
                if not valid:
                    print(f"    Solution doesn't satisfy all congruences")
        except Exception as e:
            print(f"  ✗ chinese_remainder({remainders}, {moduli}) raised exception: {e}")

    # Test error case
    try:
        chinese_remainder([1, 2, 3], [4, 5])  # Mismatched lengths
        print(f"  ✗ chinese_remainder with mismatched lengths should raise ValueError")
    except ValueError:
        print(f"  ✓ chinese_remainder with mismatched lengths correctly raised ValueError")
        passed += 1
        total += 1
    except Exception as e:
        print(f"  ✗ chinese_remainder with mismatched lengths raised unexpected exception: {e}")
        total += 1

    print(f"  Passed: {passed}/{total}\n")
    return passed == total


def test_factorize():
    """Test the factorize function."""
    print("Testing factorize function...")

    test_cases = [
        (12, [2, 2, 3]),
        (30, [2, 3, 5]),
        (17, [17]),  # Prime number
        (100, [2, 2, 5, 5]),
        (1, []),  # Edge case
        (2, [2]),  # Smallest prime
        (4, [2, 2]),  # Power of 2
        (9, [3, 3]),  # Power of 3
    ]

    passed = 0
    total = len(test_cases)

    for n, expected in test_cases:
        try:
            result = factorize(n)
            # Sort both lists to handle order differences
            result_sorted = sorted(result)
            expected_sorted = sorted(expected)

            if result_sorted == expected_sorted:
                passed += 1
                print(f"  ✓ factorize({n}) = {result}")
                # Verify that the product equals the original number
                if result:
                    product = 1
                    for factor in result:
                        product *= factor
                    if product == n:
                        print(f"    Verification: product = {product}")
                    else:
                        print(f"    ✗ Product verification failed: {product} ≠ {n}")
                        passed -= 1
            else:
                print(f"  ✗ factorize({n}) = {result}, expected {expected}")
        except Exception as e:
            print(f"  ✗ factorize({n}) raised exception: {e}")

    print(f"  Passed: {passed}/{total}\n")
    return passed == total


def test_phi():
    """Test the phi (Euler's totient) function."""
    print("Testing phi function...")

    test_cases = [
        (1, 1),  # φ(1) = 1
        (2, 1),  # φ(2) = 1 (only 1 is coprime to 2)
        (3, 2),  # φ(3) = 2 (1, 2 are coprime to 3)
        (4, 2),  # φ(4) = 2 (1, 3 are coprime to 4)
        (5, 4),  # φ(5) = 4 (1, 2, 3, 4 are coprime to 5)
        (6, 2),  # φ(6) = 2 (1, 5 are coprime to 6)
        (7, 6),  # φ(7) = 6 (1, 2, 3, 4, 5, 6 are coprime to 7)
        (8, 4),  # φ(8) = 4 (1, 3, 5, 7 are coprime to 8)
        (9, 6),  # φ(9) = 6 (1, 2, 4, 5, 7, 8 are coprime to 9)
        (10, 4),  # φ(10) = 4 (1, 3, 7, 9 are coprime to 10)
        (12, 4),  # φ(12) = 4 (1, 5, 7, 11 are coprime to 12)
        (15, 8),  # φ(15) = 8 (1, 2, 4, 7, 8, 11, 13, 14 are coprime to 15)
        (16, 8),  # φ(16) = 8 (powers of 2: φ(2^k) = 2^(k-1))
        (17, 16),  # φ(17) = 16 (17 is prime, so φ(p) = p-1)
        (20, 8),  # φ(20) = 8 (20 = 2^2 * 5, so φ(20) = 20 * (1-1/2) * (1-1/5) = 8)
        (21, 12),  # φ(21) = 12 (21 = 3 * 7, so φ(21) = 21 * (1-1/3) * (1-1/7) = 12)
        (30, 8),  # φ(30) = 8 (30 = 2 * 3 * 5, so φ(30) = 30 * 1/2 * 2/3 * 4/5 = 8)
        (100, 40),  # φ(100) = 40 (100 = 2^2 * 5^2, so φ(100) = 100 * (1-1/2) * (1-1/5) = 40)
    ]

    passed = 0
    total = len(test_cases)

    for m, expected in test_cases:
        try:
            result = phi(m)
            if result == expected:
                passed += 1
                print(f"  ✓ phi({m}) = {result}")
            else:
                print(f"  ✗ phi({m}) = {result}, expected {expected}")
        except Exception as e:
            print(f"  ✗ phi({m}) raised exception: {e}")

    # Test error case
    try:
        phi(0)
        print(f"  ✗ phi(0) should raise ValueError")
    except ValueError:
        print(f"  ✓ phi(0) correctly raised ValueError")
        passed += 1
        total += 1
    except Exception as e:
        print(f"  ✗ phi(0) raised unexpected exception: {e}")
        total += 1

    try:
        phi(-5)
        print(f"  ✗ phi(-5) should raise ValueError")
    except ValueError:
        print(f"  ✓ phi(-5) correctly raised ValueError")
        passed += 1
        total += 1
    except Exception as e:
        print(f"  ✗ phi(-5) raised unexpected exception: {e}")
        total += 1

    print(f"  Passed: {passed}/{total}\n")
    return passed == total


def test_ord():
    """Test the ord (multiplicative order) function."""
    print("Testing ord function...")

    test_cases = [
        # Simple cases
        (1, 5, 1),  # 1^1 ≡ 1 (mod 5)
        (2, 5, 4),  # ord(2) mod 5: 2^1=2, 2^2=4, 2^3=3, 2^4=1, so ord=4
        (3, 5, 4),  # ord(3) mod 5: 3^1=3, 3^2=4, 3^3=2, 3^4=1, so ord=4
        (4, 5, 2),  # ord(4) mod 5: 4^1=4, 4^2=1, so ord=2

        # Modulo 7 (prime)
        (2, 7, 3),  # ord(2) mod 7: 2^1=2, 2^2=4, 2^3=1, so ord=3
        (3, 7, 6),  # ord(3) mod 7: primitive root, so ord=φ(7)=6
        (4, 7, 3),  # ord(4) mod 7: 4^1=4, 4^2=2, 4^3=1, so ord=3
        (5, 7, 6),  # ord(5) mod 7: primitive root, so ord=φ(7)=6
        (6, 7, 2),  # ord(6) mod 7: 6^1=6, 6^2=1, so ord=2

        # Modulo 8 (power of 2)
        (3, 8, 2),  # ord(3) mod 8: 3^1=3, 3^2=1, so ord=2
        (5, 8, 2),  # ord(5) mod 8: 5^1=5, 5^2=1, so ord=2
        (7, 8, 2),  # ord(7) mod 8: 7^1=7, 7^2=1, so ord=2

        # Modulo 9 (power of 3)
        (2, 9, 6),  # ord(2) mod 9: ord=6 (since φ(9)=6)
        (4, 9, 3),  # ord(4) mod 9: 4^1=4, 4^2=7, 4^3=1, so ord=3
        (5, 9, 6),  # ord(5) mod 9: primitive root, so ord=φ(9)=6
        (7, 9, 3),  # ord(7) mod 9: 7^1=7, 7^2=4, 7^3=1, so ord=3
        (8, 9, 6),  # ord(8) mod 9: primitive root, so ord=φ(9)=6

        # Modulo 10
        (3, 10, 4),  # ord(3) mod 10: φ(10)=4, ord divides 4
        (7, 10, 4),  # ord(7) mod 10: φ(10)=4, ord divides 4
        (9, 10, 2),  # ord(9) mod 10: 9^2=81≡1 mod 10, so ord=2

        # Modulo 11 (prime)
        (2, 11, 10),  # ord(2) mod 11: primitive root, so ord=φ(11)=10
        (10, 11, 2),  # ord(10) mod 11: 10≡-1, so (-1)^2=1, ord=2

        # Larger modulus
        (2, 13, 12),  # ord(2) mod 13: primitive root, so ord=φ(13)=12
        (3, 13, 3),  # ord(3) mod 13: 3^3=27≡1 mod 13, so ord=3
    ]

    passed = 0
    total = len(test_cases)

    for a, m, expected in test_cases:
        try:
            result = ord(a, m)
            if result == expected:
                passed += 1
                print(f"  ✓ ord({a}, {m}) = {result}")
                # Verify that a^result ≡ 1 (mod m)
                if pow(a, result, m) != 1:
                    print(f"    ✗ Verification failed: {a}^{result} ≢ 1 (mod {m})")
                    passed -= 1
            else:
                print(f"  ✗ ord({a}, {m}) = {result}, expected {expected}")
                # Still verify the result is valid
                if pow(a, result, m) == 1:
                    print(f"    Note: {a}^{result} ≡ 1 (mod {m}), but expected order was {expected}")
        except Exception as e:
            print(f"  ✗ ord({a}, {m}) raised exception: {e}")

    # Test error cases
    error_cases = [
        (2, 1, "m must be greater than 1"),  # m ≤ 1
        (0, 1, "m must be greater than 1"),  # m ≤ 1
        (4, 8, "gcd(4, 8) must be 1"),  # gcd(4, 8) = 4 ≠ 1
        (6, 9, "gcd(6, 9) must be 1"),  # gcd(6, 9) = 3 ≠ 1
        (10, 15, "gcd(10, 15) must be 1"),  # gcd(10, 15) = 5 ≠ 1
    ]

    for a, m, expected_error in error_cases:
        try:
            result = ord(a, m)
            print(f"  ✗ ord({a}, {m}) should raise ValueError: {expected_error}")
        except ValueError as e:
            if expected_error in str(e):
                print(f"  ✓ ord({a}, {m}) correctly raised ValueError: {e}")
                passed += 1
                total += 1
            else:
                print(f"  ✗ ord({a}, {m}) raised ValueError with wrong message: {e}")
                total += 1
        except Exception as e:
            print(f"  ✗ ord({a}, {m}) raised unexpected exception: {e}")
            total += 1

    print(f"  Passed: {passed}/{total}\n")
    return passed == total


def test_find_generator():
    """Test the find_generator function."""
    print("Testing find_generator function...")

    # Known generators for small primes
    test_cases = [
        (3, [2]),  # F_3*: generator is 2
        (5, [2, 3]),  # F_5*: generators are 2, 3
        (7, [3, 5]),  # F_7*: generators are 3, 5
        (11, [2, 6, 7, 8]),  # F_11*: generators are 2, 6, 7, 8
        (13, [2, 6, 7, 11]),  # F_13*: generators are 2, 6, 7, 11
        (17, [3, 5, 6, 7, 10, 11, 12, 14]),  # F_17*: multiple generators
        (19, [2, 3, 10, 13, 14, 15]),  # F_19*: generators include 2, 3, 10, 13, 14, 15
        (23, [5, 7, 10, 11, 14, 15, 17, 19, 20, 21]),  # F_23*: many generators
    ]

    passed = 0
    total = len(test_cases)

    for p, known_generators in test_cases:
        try:
            result = find_generator(p)
            # Verify that the result is indeed a generator
            expected_order = p - 1  # Order of generator should be p-1
            actual_order = ord(result, p)

            if actual_order == expected_order:
                passed += 1
                is_known = result in known_generators
                status = "known" if is_known else "valid"
                print(f"  ✓ find_generator({p}) = {result} ({status} generator, order = {actual_order})")

                # Double-check: verify it's actually in the known list if we have comprehensive data
                if p <= 13 and not is_known:
                    print(f"    Note: {result} not in expected list {known_generators}, but order is correct")
            else:
                print(
                    f"  ✗ find_generator({p}) = {result}, but ord({result}, {p}) = {actual_order}, expected {expected_order}")
        except Exception as e:
            print(f"  ✗ find_generator({p}) raised exception: {e}")

    # Test larger primes to ensure the function works efficiently
    larger_primes = [29, 31, 37, 41, 43, 47]

    for p in larger_primes:
        try:
            result = find_generator(p)
            actual_order = ord(result, p)
            expected_order = p - 1

            if actual_order == expected_order:
                passed += 1
                print(f"  ✓ find_generator({p}) = {result} (order = {actual_order})")
            else:
                print(
                    f"  ✗ find_generator({p}) = {result}, but ord({result}, {p}) = {actual_order}, expected {expected_order}")
            total += 1
        except Exception as e:
            print(f"  ✗ find_generator({p}) raised exception: {e}")
            total += 1

    # Test error cases
    error_cases = [
        (1, "p must be a prime > 2"),  # p ≤ 2
        (2, "p must be a prime > 2"),  # p ≤ 2
        (4, "4 is not prime"),  # Composite number
        (9, "9 is not prime"),  # Composite number
        (15, "15 is not prime"),  # Composite number
        (25, "25 is not prime"),  # Composite number
    ]

    for p, expected_error in error_cases:
        try:
            result = find_generator(p)
            print(f"  ✗ find_generator({p}) should raise ValueError: {expected_error}")
        except ValueError as e:
            if expected_error in str(e):
                print(f"  ✓ find_generator({p}) correctly raised ValueError: {e}")
                passed += 1
                total += 1
            else:
                print(f"  ✗ find_generator({p}) raised ValueError with wrong message: {e}")
                total += 1
        except Exception as e:
            print(f"  ✗ find_generator({p}) raised unexpected exception: {e}")
            total += 1

    print(f"  Passed: {passed}/{total}\n")
    return passed == total


def run_all_tests():
    """Run all test functions and report overall results."""
    print("=" * 60)
    print("PRIMES.PY TEST DRIVER")
    print("=" * 60)
    print()

    test_functions = [
        test_is_prime,
        test_get_primes,
        test_primefactors,
        test_gcd,
        test_ext_gcd,
        test_inv_mod,
        test_chinese_remainder,
        test_factorize,
        test_phi,
        test_ord,
        test_find_generator
    ]

    results = []
    for test_func in test_functions:
        try:
            success = test_func()
            results.append(success)
        except Exception as e:
            print(f"Test function {test_func.__name__} failed with exception:")
            print(traceback.format_exc())
            results.append(False)

    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)

    passed = sum(results)
    total = len(results)

    for i, (test_func, result) in enumerate(zip(test_functions, results)):
        status = "PASS" if result else "FAIL"
        print(f"{test_func.__name__:<25} {status}")

    print(f"\nOverall: {passed}/{total} test suites passed")

    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed.")
        return 1

# if __name__ == "__main__":
#     sys.exit(run_all_tests())
