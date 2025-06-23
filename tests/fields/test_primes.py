# check prime utilities
# reworked 20/07/2023
# checked 07/01/2024

import time
import unittest
from functools import reduce

from sandbox.fields.mp import Mp
from sandbox.fields.polynomials import Polynomial
from sandbox.fields.primes import *


class TestPrimes(unittest.TestCase):

    def test_get_primes(self):
        ps = get_primes(20)
        print(ps)

    def test_aux(self):
        p = 17
        e = 0  # exponent
        r = 17  # remainder
        while r % p == 0:
            e += 1
            r //= p
        print(e, r)

    def testPrimefactors(self):
        ps = get_primes(10000)
        for n in range(2, 1000):
            f = primefactors(n, ps)
            result = reduce(lambda x, y: x * y, [ps[i] ** f[0][i] for i in range(len(f[0]))], 1) * f[1]
            self.assertEqual(n, result)

    def testExtGcd(self):
        data = [(1, 0), (81, 99), (99, 81), (123, 456), (456, 123),
                (123456789, 987654321), (987654321, 123456789)]
        for a, b in data:
            d, s, t = ext_gcd(a, b)
            self.assertEqual(d, a * s + b * t)

    def testInv(self):
        data = [(1, 2), (2, 3), (3, 5), (4, 7), (5, 11), (6, 13), (7, 17)]
        for a, m in data:
            b = inv(a, m)
            self.assertEqual(1, a * b % m)

    def testChineseRemainder(self):
        data = [([3], [7]), ([0, 2], [2, 3]), ([2, 3], [3, 5]), ([2, 3, 2], [3, 5, 7])]
        for a, m in data:
            b = chinese_remainder(a, m)
            for i in range(len(a)):
                self.assertEqual(a[i] % m[i], b % m[i])

    def testChineseRemainderOnPolynomials(self):
        m = Polynomial(1, 0, 1)
        p = Polynomial(1, 1)
        q = inv(p, m)
        print(q)
        self.assertEqual(1, p * q % m)

    def testChineseRemainderOnMp(self):
        p = Mp(3, (7,))
        q = 1 / p
        print(q)
        self.assertEqual(1, p * q)

    def testChineseRemainder_(self):
        m1 = get_primes(200)
        m = [p for p in m1 if p > 100]

        start = time.time()
        for n in range(100000, 120000):
            a = [n % p for p in m]
            k = chinese_remainder_(a, m)
            self.assertEqual(k, n)
        stop = time.time()
        t1 = stop - start

        start = time.time()
        for n in range(100000, 120000):
            a = [n % p for p in m]
            k = chinese_remainder(a, m)
            self.assertEqual(k, n)
        stop = time.time()
        t2 = stop - start

        print(t1, t2)
