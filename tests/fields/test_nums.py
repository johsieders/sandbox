# checkInvariants Z over p
# js 12/08/2004
# reworked 20/07/2023
# reworked 16/01/2024


from sandbox.fields.fp import Fp
from sandbox.fields.mp import Mp
from sandbox.fields.polynomials import Polynomial
from sandbox.fields.rationals import Rational
from tests.fields.test_abstract import TestAbstract


class TestNums(TestAbstract):
    def challenge_polynomial(self, n, make):
        ps = []
        for a in range(n):
            for b in range(n):
                for c in range(n):
                    ps.append(Polynomial(make(a), make(b), make(c)))

        self.challenge_euclidian_ring(*ps)

        ps = []
        for k in range(n):
            ps.append(Polynomial(*[make(a) for a in range(k, 2 * k + 1)]))

        self.challenge_euclidian_ring(*ps)
        for p in ps:
            for q in ps:
                for x in range(-10, 10):
                    self.assertEqual(p(x) + q(x), (p + q)(x))
                    self.assertEqual(p(x) - q(x), (p - q)(x))
                    self.assertEqual(p(x) * q(x), (p * q)(x))

    def testPolynomialOfX(self):

        #     p = Polynomial(1, 0, 1)
        #     q = Polynomial(1, 1)
        #     r = Rational(1, 2)
        #     # print(p(r))
        #     # print(p(q))
        #
        #     a = Rational(p, q)
        #     b = a ** 2
        #
        #     c = Polynomial(a, b)
        #     print(c)
        #
        self.challenge_polynomial(5, float)
        self.challenge_polynomial(5, Rational)

    def testFpOfInt(self):
        a = Fp(3, 7)
        b = Fp(1, 7)
        c = Fp(7, 7)
        self.challenge_field(a, b, c)

    def testMpOfPolynomialOfFloat(self):
        m = (Polynomial(1, 0, 0, 0, 1),)
        a = Mp(Polynomial(1, 1), m)
        b = Mp(Polynomial(1, 1), m)
        c = Mp(Polynomial(2, 3), m)
        self.challenge_field(a, b, c)

    def testRationalOfInt(self):
        a = Rational(2, 4)
        b = Rational(1, 2)
        c = Rational(4, 7)

        self.challenge_field(a, b, c)

        n = 5
        x = []
        for i in range(n):
            for j in range(1, n):
                x.append(Rational(i, j))
        self.challenge_field(*x)

    def testRationalOfPolynomialOfFloat(self):

        p = Polynomial(1, 0, 1)
        q = Polynomial(1, 1)
        r = Polynomial(1, 2, 3, 4)

        a = Rational(p)
        b = Rational(p, q)
        c = Rational(1, r)

        self.challenge_field(a, b, c)
        u = b(2)
        v = p(2) / q(2)
        d = abs(u - v)
        self.assertEqual(u, v)

    def testRationalOfPolynomialOfMpOfInt(self):
        pass

    def testPolynomialOfMpOfInt(self):
        pass

    def testPolynomialOfMpOfPolynomialOfFloat(self):
        pass

    def testPolynomialOfRationalOfPolynomialOfFloat(self):
        pass
