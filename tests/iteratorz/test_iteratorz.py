# Python Test iterators
# js, 8.6.04
# edited 21.1.2020
# revised for Mac 6.6.2025

from itertools import count
from itertools import repeat as itrepeat
from operator import add

from sandbox.iteratorz.iteratorz import hamming, inverse, merge, multiply, square, take, sin, cos, exp
from sandbox.stepfunctions.stepfun import merge_op

epsilon = 1e-8

sf = ((None, None), (0, 31), (10, 41), (20, None))
tf = ((None, None), (0, 63), (5, 23), (15, 53), (20, None))
sum_sftf = ((None, None), (0, 94), (5, 54), (10, 64), (15, 94), (20, None))

uf = ((None, None), (0, 100), (10, 200), (20, 100), (30, None))
vf = ((None, None), (0, 200), (10, 100), (20, 200), (30, None))
sum_ufvf = ((None, None), (0, 300), (30, None))

wf = ((None, 500),)
xf = ((None, None), (0, 700))
sum_wfxf = ((None, 500), (0, 1200))

yf = ((None, None),)
zf = ((None, None),)
sum_yfzf = ((None, None),)

sum_all = ((None, 500), (0, 1594), (5, 1554), (10, 1564), (15, 1594), (20, 1500), (30, 1200))
max_all = ((None, 500), (0, 700))
min_all = ((None, 500), (0, 31), (5, 23), (15, 41), (20, 100), (30, 500))


def test_stepmerge():
    assert sum_sftf == take(10, merge_op(add, sf, tf))
    assert sum_ufvf == take(10, merge_op(add, uf, vf))
    assert sum_wfxf == take(10, merge_op(add, wf, xf))
    assert sum_yfzf == take(10, merge_op(add, yf, zf))
    assert sum_all == take(10, merge_op(add, sf, tf, uf, vf, wf, xf))
    assert max_all == take(10, merge_op(max, sf, tf, uf, vf, wf, xf))
    assert min_all == take(10, merge_op(min, sf, tf, uf, vf, wf, xf))


def test_hamming():
    h = hamming(3, 5, 7)
    assert (1, 3, 5, 7, 9, 15) == tuple(take(6, h))


def test_product1():
    p = multiply(itrepeat(1), itrepeat(1))
    q = count()
    next(q)
    assert take(1000, p) == take(1000, q)


def test_product2():
    p = multiply(count(), itrepeat(1))
    assert (0, 1, 3, 6, 10, 15) == take(6, p)
    p = multiply(itrepeat(1), count())
    assert (0, 1, 3, 6, 10, 15) == tuple(take(6, p))


def test_product3():
    """ cos**2 + sin**2 = 1 """
    c2 = square(cos())
    s2 = square(sin())
    p = (x1 + x2 for x1, x2 in zip(c2, s2))
    assert abs(1 - next(p)) < epsilon
    for i in range(1, 100):
        assert abs(0 - next(p)) < epsilon


def test_invert():
    """ exp(x) * exp(-x) = 1 """
    x = inverse(exp())
    p = multiply(exp(), x)
    assert abs(1 - next(p)) < epsilon
    for i in range(1, 100):
        assert abs(0 - next(p)) < epsilon


def test_merge():
    m = merge((), ())
    assert len(tuple(m)) == 0
    m = merge(range(10), range(20))
    assert sum(m) == 235


from timeit import *

def test_time_iterators():
    print()
    t = Timer('take(171, hamming(2,3,5,7,11))', 'from sandbox.iteratorz.iteratorz import hamming, take')
    result = t.repeat(2, 20)
    print('20*take(171, hamming(2,3,5)) : ', result)

    # works with 171 but not with 172
    t = Timer('take(171, multiply(sin(), cos()))', 'from sandbox.iteratorz.iteratorz import multiply, sin, cos, take')
    result = t.repeat(2, 20)
    print('20*take(171, multiply(sin(), cos())) : ', result)

    # works with 171 but not with 172
    t = Timer('take(171, inverse(exp()))', 'from sandbox.iteratorz.iteratorz import inverse, exp, take')
    result = t.repeat(2, 20)
    print('20*take(171, inverse(exp())) : ', result)