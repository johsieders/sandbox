# js, 8.6.04
# edited 21.1.2020
# revised 05.06.2025

from itertools import cycle
from operator import add, mul

# from sandbox.iterators import take
from sandbox.stepfunctions.stepfun import Stepfun, assert_ascending

input = [((None, None),),
         ((None, 100),),
         ((None, 100), (0, None)),
         ((None, 100), (0, 200)),
         ((None, None), (0, 31), (10, 41), (20, None)),
         ((None, None), (0, 63), (5, 23), (15, 53), (20, None)),
         ((None, None), (0, 100), (10, 200), (20, 100), (30, None)),
         ((None, None), (-10, 200), (10, 100), (20, 200), (30, None)),
         ((None, None), (-20, 200), (10, None), (20, 200), (30, None)),
         ((None, None), (-20, 200), (10, None), (20, 200), (30, 300)),
         ((None, 200),),
         ((None, 100), (0, None))]

output = [((None, None),),
          ((None, 100),),
          ((None, 200),),
          ((None, None), (0, 94), (5, 54), (10, 64), (15, 94), (20, None)),
          ((None, 300), (-20, 700), (-10, 900), (0, 1094), (5, 1054), (10, 664), (15, 694), (20, 1000), (30, 600)),
          ((None, 1000000), (-20, 40000000000), (-10, 8000000000000), (0, 31248000000000000), (5, 11408000000000000),
           (10, 377200000000), (15, 869200000000), (20, 16000000000000), (30, 6000000)),
          ((None, 100), (-20, 200), (30, 300)),
          ((None, 100), (0, 31), (5, 23), (15, 41), (20, 100))]


def hard(a, b, n):
    """
    :param a: first value
    :param b: second value
    :param n: length of result
    :return: a stepfunction wit n steps, alternating a and b
    """
    ts = [None] + list(range(n))
    timestamps = zip(ts, cycle((a, b)))
    return Stepfun(timestamps, check=False)


def make_hard_test(k, n):
    fs = []
    for i in range(0, k):
        for j in range(k, 2 * k):
            fs.append(hard(i, j, n))
    return fs


fshard = make_hard_test(2, 3)
print(fshard)

k = 2
n = 3

def test_equal():
    for i, f in enumerate(input):
        for j, g in enumerate(input):
            if i == j:
                assert f == g


def test_ascending():
    testcases = [(),
                 ((0, 37),),
                 ((None, None),),
                 ((None, 37),),
                 ((None, 37), (0, 47)),
                 ((None, 37), (0, 47), (1, 57)),
                 ((None, 37), (0, 47), (1, 57), (2, 67)),
                 ((None, 37), (0, 47), (0, 57), (2, 67))]

    for tc in testcases[:-1]:
        assert tc == tuple(assert_ascending(tc))

def test_speed():
    fshard = make_hard_test(k, n)
    c = Stepfun.const(0)
    hugh1 = sum(fshard, c)
    hugh2 = c.merge(add, *fshard)
    hugh3 = c
    for f in fshard:
        hugh3 += f
    assert hugh1 == hugh2
    assert hugh2 == hugh3


def test_speed1():
    fshard = make_hard_test(2, 3)
    c = Stepfun.const(0)
    hugh1 = sum(fshard, c)


def test_speed2():
    c = Stepfun.const(0)
    hugh2: Stepfun = c.merge(add, *fshard)


def test_speed3():
    hugh3 = Stepfun.const(0)
    for f in fshard:
        hugh3 += f


def check_stepfun(sf):
    self.assertEqual(sf, sf)
    self.assertEqual(sf, +sf)
    self.assertEqual(sf, ++sf)
    self.assertEqual(sf, +++sf)
    self.assertEqual(sf, --sf)
    self.assertTrue((sf - sf).isnoneorzero())
    self.assertTrue((sf + -sf).isnoneorzero())
    self.assertTrue((sf - +sf).isnoneorzero())
    self.assertLessEqual(sf, sf)

    tf = sf.replace_none_with_constant(1)
    uf = tf + Stepfunction(((None, 1),))

    self.assertLess(tf, uf)
    self.assertLessEqual(tf, tf)
    self.assertLessEqual(tf, abs(tf))
    self.assertLessEqual(tf, abs(tf) + abs(tf))
    self.assertTrue(abs(tf).isnonnegative())
    self.assertTrue((abs(tf) - abs(tf)).iszero())

    for x in range(-10, 10):
        self.assertEqual(tf(x) + 1, uf(x))


def testHard(self):
    sf = hard(1, 0, 1000000)
    tf = hard(0, 1, 1000000)
    zf = sf + tf
    self.assertEqual(Stepfunction(((None, 1),)), zf)

    for n in range(1, 100):
        self.checkStepfunction(hard(None, 0, n))
        self.checkStepfunction(hard(0, None, n))


def testStepmerge(self):
    replace = lambda x, y: y if x is None else y
    self.assertEqual(output[0], take(10, stepmerge(replace, input[0], input[0])))
    self.assertEqual(output[1], take(10, stepmerge(replace, input[0], input[1])))

    self.assertEqual(output[0], take(10, stepmerge(add, input[0], input[0])))
    self.assertEqual(output[1], take(10, stepmerge(add, input[0], input[1])))
    self.assertEqual(output[2], take(10, stepmerge(add, input[1], input[1])))
    self.assertEqual(output[2], take(10, stepmerge(add, input[2], input[3])))
    self.assertEqual(output[3], take(10, stepmerge(add, input[4], input[5])))

    self.assertEqual(output[-4], take(10, stepmerge(add, *input[:-2])))
    self.assertEqual(output[-3], take(10, stepmerge(mul, *input[:-2])))
    self.assertEqual(output[-2], take(10, stepmerge(max, *input[:-2])))
    self.assertEqual(output[-1], take(10, stepmerge(min, *input[:-2])))


def testRelocate(self):
    sf = Stepfunction(((None, 27),))
    tf = sf.relocate(range(0, 100))
    self.assertEqual(sf, tf)


def testScan(self):
    def g(x):
        return x * x

    f = Stepfunction.scan(g, 0, -1)
    self.assertEqual(Stepfunction(((None, None),)), f)
    f = Stepfunction.scan(g, 0, 0)
    self.assertEqual(Stepfunction(((None, None), (0, 0))), f)
    f = Stepfunction.scan(g, 0, 1)
    self.assertEqual(f(0), g(0))
    self.assertEqual(f(1), g(1))
    self.assertEqual(f(100), g(1))
    self.checkStepfunction(f)


def testIntegral(self):
    f = Stepfunction(((None, None),))
    self.assertEqual(f.integral(0, 1), 0)
    self.assertEqual(f.integral(-1, 100), 0)
    self.assertEqual(f.integral(100, 1000), 0)

    f = Stepfunction(((None, 10),))
    self.assertEqual(f.integral(0, 0), 0)
    self.assertEqual(f.integral(0, 1), 10)
    self.assertEqual(f.integral(-1, 100), 1010)
    self.assertEqual(f.integral(100, 1000), 9000)

    f = Stepfunction(((None, None), (0, 10), (2, 20)))
    self.assertEqual(f.integral(-10, 2), 20)
    self.assertEqual(f.integral(0.5, 2), 15)
    self.assertEqual(f.integral(0, 3), 40)
    self.assertEqual(f.integral(0, 3.5), 50)
    self.assertEqual(f.integral(0, 4), 60)
    self.assertEqual(f.integral(1, 4), 50)
    self.assertEqual(f.integral(2, 4), 40)
    self.assertEqual(f.integral(0, 1), 10)
    self.assertEqual(f.integral(0, 100), 1980)
    self.assertEqual(f.integral(10, 100), 1800)


def testAll(self):
    fs = [Stepfunction(f) for f in input]
    for f in fs:
        self.checkStepfunction(f)


def testStepfunctionBasics(self):
    inpt = [Stepfunction(f) for f in input]
    outpt = [Stepfunction(f) for f in output]

    self.assertEqual(outpt[0], inpt[0] + inpt[0])
    self.assertEqual(outpt[1], inpt[0] + inpt[1])
    self.assertEqual(outpt[2], inpt[1] + inpt[1])
    self.assertEqual(outpt[2], inpt[2] + inpt[3])
    self.assertEqual(outpt[3], inpt[4] + inpt[5])
    self.assertEqual(outpt[-4], Stepfunction(((None, None),)).merge(add, *inpt[:-2]))
    self.assertEqual(outpt[-3], Stepfunction(((None, None),)).merge(mul, *inpt[:-2]))
    self.assertEqual(outpt[-2], Stepfunction(((None, None),)).merge(max, *inpt[:-2]))
    self.assertEqual(outpt[-1], Stepfunction(((None, None),)).merge(min, *inpt[:-2]))
