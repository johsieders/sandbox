# js, 8.6.04
# edited 21.1.2020
# revised 05.06.2025

from itertools import cycle
from operator import add, mul, and_, or_
from typing import Any

from sandbox.iteratorz.iteratorz import take
from sandbox.stepfunctions.stepfun import Stepfun, check_ascending, merge_op, weak_op

def test_tutorial():
    # A Stepfun is given by a non-empty sequence of time-value pairs, the first timestamp being always None
    # which represents -oo. Stepfuns are declared on the real line from -OO to +oo.
    # The value None means "undefined" or "unknown".
    # The timestamps are strictly ascending; the value changes at each timestamp.
    # Common values are int, float or bool.
    # some interesting stepfunctions:
    funs = [
        Stepfun(((None, None),)),  # undefined on (-oo, +oo)
        Stepfun(((None, 0),)),  #  constant = 0 on (-oo, +oo)
        Stepfun(((None, None), (0, 10))),  # undefined on (-oo,0) and constant = 10 on [0, +oo)
        Stepfun(((None, None), (0, 10), (2, None))),  # undefined on (-oo,0) constant = 10 on [0, 2), undefined on [2, +oo)
        Stepfun(((None, None), (0, 10), (1, 10), (2, 20)))  # undefined om (-oo, 0), 10 on [0, 1), 20 on [2, +oo)
    ]

    # The class Stepfun overloads call, that is: f(x) gives you the value of f at x which can be None
    # It also overloads the usual operands (and, or, not; add, sub, mul, neg) in such a way that None-values are ignored,
    # so: None + 7 == 7 + None == 7 while None + None == None. It always holds that (f+g)(x) == f(x)+g(x)
    # some examples:

    f = Stepfun(((None, None), (2, 20), (4, 40), (5, None)))
    g = Stepfun(((None, None), (1, 10), (3, 30)))

    assert str(-f) == str(((None, None), (2, -20), (4, -40), (5, None)))
    assert str(f - f) == str(((None, None), (2, 0), (5, None)))
    assert str(f + g) == str(((None, None), (1, 10), (2, 30), (3, 50), (4, 70), (5, 30)))
    assert str(f - g) == str(((None, None), (1, -10), (2, 10), (3, -10), (4, 10), (5, -30)))
    assert str(f * g) == str(((None, None), (1, 10), (2, 200), (3, 600), (4, 1200), (5, 30)))

def test_merge_op4():
    t_list = [(None, None), (0,100), (2, 200), (4, 140)]
    s_list = [(None, 100), (0, 200), (2, 100), (3, 230), (5, 500), (6, 600)]
    r_list = merge_op(add, t_list, s_list)
    print()
    print(r_list)


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


def gen_fun(a, b: Any, start=0, stop=10, step=1) -> Stepfun:
    """
    :param a: first value
    :param b: second value
    :start: first timestamp
    :stop: last timestamp + step
    :step: distance between timestamps
    :return: a stepfunction alternating a and b in the range given by start, stop, step.
    """
    ts = [None] + [k * step for k in range(start, stop)]
    return Stepfun(tuple(zip(ts, cycle((a, b)))))


def gen_funs(k, n: int) -> list[Stepfun]:
    fs = []
    for i in range(0, k):
        for j in range(k, 2 * k):
            fs.append(gen_fun(i, j, n))
    return fs


k = 10
n = 30


def test_equal():
    for i, f in enumerate(input):
        for j, g in enumerate(input):
            if i == j:
                assert f == g


def test_weak_op():
    w_or = weak_op(or_)
    assert w_or(()) is None
    assert w_or((True,))
    assert w_or((True, None,))


def test_ascending():
    testcases = [
        ((None, 37),),
        ((None, None),),
        ((None, 37),),
        ((None, 37), (0, 47)),
        ((None, 37), (0, 47), (1, 57)),
        ((None, 37), (0, 47), (1, 57), (2, 67))]

    for tc in testcases:
        assert tc == check_ascending(tc)
        f = Stepfun(tc)


def test_speed1():
    f = gen_fun(10, 20, 0, 200)
    fs = gen_funs(k, n)
    c = Stepfun.const(7)

    hugh1 = sum(fs, c)
    hugh2 = c.merge(add, *fs)
    hugh3 = c
    for f in fs:
        hugh3 += f

    assert hugh1 == hugh2
    assert hugh2 == hugh3


def test_speed2():
    fs = gen_funs(2, 3)
    c = Stepfun.const(20)
    hugh1 = sum(fs, c)
    hugh2 = c
    for f in fs:
        hugh2 += f
    assert hugh1 == hugh2


def check_stepfun(sf: Stepfun):
    assert sf == sf
    assert sf == +sf
    assert sf == ++sf
    assert sf == +++sf
    assert sf == --sf
    assert (sf - sf).is_none_or_zero()
    assert (sf + -sf).is_none_or_zero()
    assert (sf - +sf).is_none_or_zero()
    assert sf <= sf

    tf = sf.replace_none_with_constant(1)
    uf = tf + Stepfun(((None, 1),))

    assert tf == tf
    assert tf <= abs(tf) + abs(tf)
    assert abs(tf).is_non_negative()
    assert (abs(tf) - abs(tf)).is_zero()

    for x in range(-100, 100):
        assert (tf(x) + 1, uf(x))


def test_aux():
    for t in input:
        f = Stepfun(t)
        check_stepfun(f)


def test_hard():
    sf = Stepfun(gen_fun(1, 0, 0, int(1e5)))
    tf = Stepfun(gen_fun(0, 1, 0, int(1e5)))
    zf = sf + tf
    assert Stepfun(((None, 1),)) == zf

    for n in range(1, 100):
        check_stepfun(Stepfun(gen_fun(None, 0, n, 0)))
        check_stepfun(Stepfun(gen_fun(0, None, 0, n)))


def test_merge_op1():
    replace = lambda x, y: y if x is None else y

    assert output[0] == take(10, merge_op(replace, input[0], input[0]))
    assert output[1] == take(10, merge_op(replace, input[0], input[1]))

    assert output[0] == take(10, merge_op(add, input[0], input[0]))
    assert output[1] == take(10, merge_op(add, input[0], input[1]))
    assert output[2] == take(10, merge_op(add, input[1], input[1]))
    assert output[2] == take(10, merge_op(add, input[2], input[3]))
    assert output[3] == take(10, merge_op(add, input[4], input[5]))

    assert output[-4] == take(10, merge_op(add, *input[:-2]))
    assert output[-3] == take(10, merge_op(mul, *input[:-2]))
    assert output[-2] == take(10, merge_op(max, *input[:-2]))
    assert output[-1] == take(10, merge_op(min, *input[:-2]))


def test_merge_op2():
    f = list(gen_fun(True, False, 0, 0))
    g = list(gen_fun(False, True, 0, 2))
    h = list(merge_op(and_, f, g))
    k = list(merge_op(or_, f, g))

    assert h == g
    assert k == f


def test_merge_op3():
    f = Stepfun(gen_fun(True, False, 0, 100, 0.5))
    g = Stepfun(gen_fun(False, True, 0, 100, 0.3))

    h1 = f & g
    k1 = f | g

    for x in range(-100, 100):
        assert h1(x) == (f(x) & g(x))
        assert k1(x) == (f(x) | g(x))


def _test_relocate():
    sf = Stepfun(((None, 27),))
    tf = sf.relocate(range(0, 100))
    assert sf == tf


def test_scan():
    def g(x):
        return x * x

    f = Stepfun.scan(g, 0, -1)
    assert Stepfun(((None, None),)) == f
    f = Stepfun.scan(g, 0, 0)
    assert Stepfun(((None, None), (0, 0))) == f
    f = Stepfun.scan(g, 0, 1)
    assert f(0) == g(0)
    assert f(1) == g(1)
    assert f(100) == g(1)
    check_stepfun(f)


def test_integral():
    f = Stepfun(((None, None),))
    assert f.integral(0, 1) == 0
    assert f.integral(-1, 100) == 0
    assert f.integral(100, 1000) == 0

    f = Stepfun(((None, 10),))
    assert f.integral(0, 0) == 0
    assert f.integral(0, 1) == 10
    assert f.integral(-1, 100) == 1010
    assert f.integral(100, 1000) == 9000

    f = Stepfun(((None, None), (0, 10), (2, 20)))
    assert f.integral(-10, 2) == 20
    assert f.integral(0.5, 2) == 15
    assert f.integral(0, 3) == 40
    assert f.integral(0, 3.5) == 50
    assert f.integral(0, 4) == 60
    assert f.integral(1, 4) == 50
    assert f.integral(2, 4) == 40
    assert f.integral(0, 1) == 10
    assert f.integral(0, 100) == 1980
    assert f.integral(10, 100) == 1800


def test_all():
    fs = [Stepfun(f) for f in input]
    for f in fs:
        check_stepfun(f)


def test_stepfun_basics():
    inpt = [Stepfun(f) for f in input]
    outpt = [Stepfun(f) for f in output]

    assert outpt[0] == inpt[0] + inpt[0]
    assert outpt[1] == inpt[0] + inpt[1]
    assert outpt[2] == inpt[1] + inpt[1]
    assert outpt[2] == inpt[2] + inpt[3]
    assert outpt[3] == inpt[4] + inpt[5]
    assert outpt[-4] == Stepfun(((None, None),)).merge(add, *inpt[:-2])
    assert outpt[-3] == Stepfun(((None, None),)).merge(mul, *inpt[:-2])
    assert outpt[-2] == Stepfun(((None, None),)).merge(max, *inpt[:-2])
    assert outpt[-1] == Stepfun(((None, None),)).merge(min, *inpt[:-2])


def test_not():
    sf = Stepfun(((None, True),))
    assert not sf == Stepfun(((None, False),))

    sf = Stepfun(((None, True), (0, False)))
    assert not sf == Stepfun(((None, False), (0, True)))
