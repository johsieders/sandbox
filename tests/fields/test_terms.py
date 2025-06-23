# check prime utilities
# reworked 20/07/2023
# checked 07/01/2024


import unittest

from sandbox.fields.terms import *


class TestTerms(unittest.TestCase):

    def test_merge(self):
        a = Product(Power('a'))
        b = Product(Power('b'))
        fs = merge_factors(a.factors, a.factors)
        pass

    def test_product(self):
       a = Product(7) * 'c' * 'd' * 'e' * 5 * 'f' * 6
       b = Product('b') * 'c' * 'd' * 'e' * 5 * 'f' * 6
       u = 2 * (3 * b)
       v = Power(3)
       w = v ** 2
       x = 2 ** v



       # x = b(c=1, d=1, e=1, f=1)
       # y = b(b=1, c=1, d=1, e=1, f=1)

    def test_sum(self):
        a = Sum(7)
        b = Sum('b')
        c = Sum('c')
        # a = Sum(7) * 'c' * 'd' * 'e' * 5 * 'f' * 6
        # b = Product('b') * 'c' * 'd' * 'e' * 5 * 'f' * 6
        u = 3 + b
        v = -b
        w = b - c
        pass

        # self.assertEqual(a_val, V(a_val))
        # self.assertEqual(b_name, Id(b_name))
        # self.assertEqual(a_val, a())
        # self.assertEqual(Id(b_name), b())
        # self.assertEqual(c_val1, c())
        # # self.assertEqual(c_val2, c(c=c_val2))

    def test_product1(self):
        a_val = 2
        b_name = 'b'
        c_name = 'c'
        c_val1 = 3
        d_val = 5
        d_name = 'd'

        a = T(a_val)
        b = T(b_name)
        c = T(c_name, c_val1)
        d = T(d_name, d_val)

        self.assertEqual(0, a * 0)
        self.assertEqual(0, 0 * a)
        self.assertEqual(1, a ** 0)
        self.assertEqual(0, 0 ** a)

        self.assertEqual(a_val * d_val, a * d_val)
        self.assertEqual(a_val * d_val, d_val * a)
        self.assertEqual(a_val * a_val, a * a)

        self.assertEqual(a_val * d_val, d_val * a)
        self.assertEqual(a_val * a_val, a * a)

        self.assertEqual(b * b, b ** 2)
        self.assertEqual(b * b * b, b ** 3)
        self.assertEqual(2 ** 3, (b ** 3)(b=2))
        self.assertEqual(c * c * c * c, c ** 4)
        self.assertEqual(c ** 5, c ** 2 * c ** 3)
        self.assertEqual(2 ** 5, (c ** 5)(c=2))
        self.assertEqual(a_val ** 2, a ** 2)
        self.assertEqual(32, (a ** b)(b=5))
        self.assertEqual(25, (b ** a)(b=5))

        u = b * c * d  # b * 3 * 5
        x1 = u()  # 15 * b
        x2 = u(b=10)  # 150
        x3 = u(c=20)  # 100 * b
        x4 = u(d=30)  # 90 * b
        x5 = u(c=100, d=300)  # 30000 * b
        x6 = u(c=100, b=200)  # 100000
        x7 = u(b=100, c=400)  # 200000

        print(f"x1 = {x1}")
        print(f"x2 = {x2}")
        print(f"x3 = {x3}")
        print(f"x4 = {x4}")
        print(f"x5 = {x5}")
        print(f"x6 = {x6}")
        print(f"x7 = {x7}")

    def test_power(self):
        a_val = 5
        b_name = 'b'
        c_name = 'c'
        c_val1 = 3

        a = T(a_val)
        b = T(b_name)
        c = T(c_name, c_val1)

        self.assertEqual(1, a * a ** -1)
        self.assertEqual(1, b * b ** -1)

        x1 = b ** c
        print(f"x1 = {x1}")

        x2 = b ** 2
        x3 = b ** a
        print(f"x2 = {x2}")
        print(f"x3 = {x3}")

        x2 = b ** 2 ** 3
        x3 = (b ** a) ** 3
        print(f"x2 = {x2}")
        print(f"x3 = {x3}")

        d = T('d', 6)

        x2 = b ** c ** 2
        x3 = (b ** c) ** 2
        print(f"x2 = {x2}")
        print(f"x3 = {x3}")

        x4 = x2(b=10)
        x5 = x3(b=10)
        print(f"x4 = {x4}")
        print(f"x5 = {x5}")

        x4 = b ** c ** d
        x5 = (b ** c) ** d
        print(f"x4 = {x4}")
        print(f"x5 = {x5}")

        x6 = x4(d=3)
        x7 = x5(d=3)
        print(f"x6 = {x6}")
        print(f"x7 = {x7}")

    def test_sum1(self):
        pass
        # e = d + c
        # print(e)
        #
        # b = 2 + a + 1 + 5
        # print(b)
        # v = b.eval()
        # print(v)
        # a.set_value(7)
        # w = b.eval()
        # print(w)
        # a.set_value(8)
        # w = b.eval()
        # print(w)
        # print(a)

        # # s = str(b)     # 'a + 1'
        # c = a + b      # 2 * a + 1
        # s = str(c)     # '2 * a + 1'
        # a.set_value(7)
        # # w = b.eval()    # should be 8
        # d = a + a       # should be 2 * a
        # d = d + a       # should be 3 * a
        # e = a * b + a * c
        # e.factor_out()  #  a * (b + c)
        # f = (a + b) * (c + d)
        # f.expand()      #  a * c + a * d + b * c + c * d
