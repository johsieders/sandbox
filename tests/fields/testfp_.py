# checkInvariants Z over p
# js 12/08/2004
# reworked 20/07/2023
# checked 08/01/2024

import unittest

from sandbox.fields.mp import Mp
from sandbox.fields.primes import get_primes


class TestFp(unittest.TestCase):

    def testFp(self):
        primes = [2, 3, 5, 7]
        ma = MA(primes)
        a = Mp(5, ma)
        b = Mp(6, ma)

        self.assertEqual(7, a + 2)
        self.assertEqual(7, 2 + a)
        self.assertEqual(11, a + b)

        self.assertEqual(209, a - 6)  # 209 = -1 mod 201
        self.assertEqual(1, 6 - a)
        self.assertEqual(209, a - b)

        self.assertEqual(30, a * 6)
        self.assertEqual(30, 6 * a)
        self.assertEqual(30, a * b)

        self.assertEqual(1, ~Mp(11, ma) * Mp(11, ma))
        self.assertEqual(0, Mp(11, ma) - Mp(11, ma))
        self.assertEqual(0, - Mp(11, ma) + Mp(11, ma))

        self.assertEqual(1, Mp(11, ma) ** 0)
        self.assertEqual(11, Mp(11, ma) ** 1)
        self.assertEqual(121, Mp(11, ma) ** 2)
        self.assertEqual(71, Mp(11, ma) ** 3)
        self.assertEqual(1, Mp(11, ma) ** -1 * Mp(11, ma))

    def testInv(self):
        # primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        primes1 = get_primes(200)
        primes = [p for p in primes1 if p > 100]
        ma = MA(primes)
        cnt = 0
        for i in range(1000000, 1010000):
            f = Mp(i, ma)
            g = ~ f
            if g:
                self.assertEqual(1, f * g)
                cnt += 1
        # print(cnt)
