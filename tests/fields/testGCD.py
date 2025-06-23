# js 27.12.2003
# checked 08/01/2024

import unittest

from sandbox.fields.polynomials import Polynomial
from sandbox.fields.primes import gcd, ext_gcd, inv


class TestGCD(unittest.TestCase):

    def testGcd(self):
        p = Polynomial(7)
        q = Polynomial(3)

        g = gcd(p, q)
        print(p, q, g)
        self.assertFalse(p % g)
        self.assertFalse(q % g)

        p = Polynomial(1, 0, -1)
        q = Polynomial(1, 1)
        g = gcd(p, q)
        print(p, q, g)
        self.assertFalse(p % g)
        self.assertFalse(q % g)

        g = gcd(p * q, p)
        print(p * q, q, g)
        self.assertFalse(p * q % g)
        self.assertFalse(p % g)
        g = gcd(p * q, q)
        print(p * q, p, g)
        self.assertFalse(p * q % g)
        self.assertFalse(q % g)

        p = Polynomial(1, 1)
        q = Polynomial(1, -1)
        g = gcd(p, q)
        print(p, q, g)
        self.assertFalse(p % g)
        self.assertFalse(q % g)

    def testExtGcd(self):
        testcases = [[[7], [3]],
                     [[1, 0, 2], [1]],
                     [[1], [1, 0, 2]],
                     [[1, 0, -1], [1, 1]],
                     [[1, 1], [1, 0, -1]],
                     [[1, 1, 3], [3, 0, -1, 4]]]

        for p, q in testcases:
            p = Polynomial(p)
            q = Polynomial(q)
            f = gcd(p, q)
            g, s, t = ext_gcd(p, q)
            self.assertEqual(f, g)
            self.assertEqual(g, p * s + q * t)
            print(f)

    def testInv(self):
        m = Polynomial(1, 0, 0, 0, 0, 1)
        testcases = [[[1], m],
                     [[7], m],
                     [[1, 0], m],
                     [[1, 2], m],
                     [[1, 0, 0], m],
                     [[1, 1, 1], m],
                     [[1, 1, 3], [3, 0, -1, 4]]]

        for p, m in testcases:
            p = Polynomial(p)
            m = Polynomial(m)
            g = gcd(p, m)
            s = inv(p, m)
            self.assertEqual(1, (p * s) % m)
