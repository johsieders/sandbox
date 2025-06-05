# trying to understand iterators
# js 14.8.2004
# completely reworked 1/7/2011
# merge revised, fmerge added 3/6/2013
# revised again 22/1/2020

from itertools import cycle, islice, tee
from operator import add

def multiply(s, t):
    """ s, t : series on a ring, assuming iter(s), iter(t) both work
        multiply returns the product of s and t
        if len(s) == 0 or len(t) == 0: StopIteration at first call of next
        works fine with finite series (i.e. polynoms) and infinite ones.
    """
    # This code does basically this:
    #
    # x = 0
    # for i in range(len(xs)):
    #     x += xs[i] * xt[k-i]
    #
    # zeroing missing elements of xs and xt.
    # The values lb (lower bound) and ub(upper bound)
    # describe the rectangle of indices to be considered.

    s, t = iter(s), iter(t)
    xs, xt = [], []  # store elements read from s and t
    k = 0  # count yielded elements

    while True:
        try:
            xs.append(next(s))
        except StopIteration:
            pass
        try:
            xt.append(next(t))
        except StopIteration:
            pass

        x = None  # start without using 0
        lb = max((0, k - len(xt) + 1))  # stay within rectangle
        ub = min((k + 1, len(xs)))
        for i in range(lb, ub):
            if x is None:
                x = xs[i] * xt[k - i]
            else:
                x += xs[i] * xt[k - i]

        if x is None:
            return
        else:
            k += 1  # that many elements yielded
            yield x


def square(s):
    return multiply(*tee(s))


def inverse(s):
    """"
    :param s: s : series on a field;
    :return: a series t such that multiply(s, t) = (1, 0, 0, ...)
    if len(s) == 0: StopIteration at fist call of next
    if len(s) > 0:  s[0] != 0, otherwise division by zero
    returns the inverse t of s
    """
    s = iter(s)  # the iterator to be inverted
    xs, xt = [], []

    x = next(s)  # may raise StopIteration
    one = x / x  # there is no 1
    zero = x - x  # there is no 0

    xs.append(x)  # read part of s
    xt.append(one / x)  # coefficients of t=1/s
    yield xt[-1]

    while True:
        try:
            xs.append(next(s))
        except StopIteration:
            xs.append(zero)

        y = zero
        for (i, x) in enumerate(xt):
            y += x * xs[-i - 1]

        xt.append(-y * xt[0])
        yield xt[-1]


def divide(s, t):
    return multiply(s, inverse(t))


def merge(*ts):
    """
    :param ts: an iterable of iterables
    :return: merge of n iterables into one.
    This is a weak merge: It stops not before t
    the longest iterator is exhausted
    """
    ts = [iter(t) for t in ts]
    head = {}.fromkeys(ts)  # dictionary of last read entries

    while True:
        for t in ts:
            if head[t] is None:
                try:
                    head[t] = (next(t),)  # replace Nones
                except StopIteration:
                    pass

        hs = [h[0] for h in head.values() if h]
        if hs:
            m = min(hs)
        else:  # all ts are done
            return

        for t in ts:
            if head[t] and head[t][0] == m:  # remove used t
                head[t] = None  # but only once to keep duplicates
                break

        yield m


def hamming(*ps):
    """
    :param ps: a list of one or more integers p0, p1, p2, ...
    :return: all multiples of p0, p1, p2, ...
    ps = (p0, p1, p2, ..) contains one or more integers, generally primes
    hamming returns all multiples of p0, p1, p2, ..
    This solution follows Dijkstra: "An exercise attributed to R.W. Hamming":
    Let q be the sequence of multiples produced so far.
    Then append min{p*x | x in q, p in ps, p*x > max(q)} to q.
    The next number to be produced is min(q)
    """
    q = [1]  # q contains all numbers produced so far
    while True:
        yield q[-1]
        mq = max(q)
        q.append(min([p * x for p in ps for x in q if p * x > mq]))

def ari(increment):
    """
    :param increment: the increment
    :return: the arithmetic sequence starting at 0 with given increment
    """
    return fun(lambda x: x + increment, 0)



def remove_dups(t):
    t = iter(t)
    last = next(t)
    yield last

    while True:
        x = next(t)
        if x != last:
            last = x
            yield last


def take(n, j):
    """
    :param n: number of elements requested
    :param j: an iterator
    :return: the first n elements of j
    """
    return tuple(islice(j, n))


def fun(f, *args):
    """ assume two args: arg0, arg1.
        Then fun yields:
        arg0, arg1, f(arg0, arg1), f(arg1, f(arg0, arg1)), ..
    """

    for arg in args:
        yield arg
    while True:
        args = args[1:] + (f(*args),)
        yield args[-1]


def geo(factor):
    """
    :param factor: the factor
    :return: the geometric sequence starting at 1 with given factor
    """
    return fun(lambda x: x * factor, 1)


def fibo():
    """
    :return: the Fibonacci series
    """
    return fun(add, 1, 1)


def faculty():
    """
    :return: the faculty sequence
    """
    factor = 1
    current = 1
    while True:
        yield current
        current *= factor
        factor += 1


def average(xs):
    return sum(xs) / len(xs) if xs else None


def exp():
    return (1.0 / k for k in faculty())


def cos():
    return (a * b for a, b in zip(cycle((1, 0, -1, 0)), exp()))


def sin():
    return (a * b for a, b in zip(cycle((0, 1, 0, -1)), exp()))
