# trying to understand intervals
# js 8.6.04
# optimization by binary search
# js 26.6.04
# relaunch 21.11.04
# 26.12.04  ok
# 6.3.2013 major revision: vlists as step functions
# 07.01.2024 general check

from bisect import bisect_right, bisect_left
from itertools import cycle
from operator import and_, or_

from fttp.src.intervals.stepfunctions__ import fmerge, Stepfun

flip = lambda f: lambda x, y: f(y, x)  # flips args


def is_interval(v):
    """ v : list or tuple of length 2 """
    return isinstance(v, (tuple, list)) and len(v) == 2


def isEmptyInterval(v):
    """ v : list or tuple of length 2 """
    if not is_interval(v):
        raise TypeError

    return v[0] is not None and v[1] is not None and v[1] <= v[0]


class Vlist(Stepfun):
    """
    This class implements lists of non-empty intervals (vlists for short).

    An interval is a pair v of two Python objects:
    v[0] is the left bound, v[1] the right bound.

    If v[0] is None, the interval is left unbounded,
    if v[1] is None, the interval is right unbounded.

    The bounds are assumed to support comparisons.

    Each vlist is either empty, that is, it contains no intervals at all.
    Or it contains one or more non-empty disjoint intervals in ascending order.

    All intervals are left-closed and right-open.
    They can be leftbounded, rightbounded or both.

    Vlists are closed with respect to union (|), complement (-)
    and intersection. (&). They form a Boolean Algebra.

    This class implements the following operations (vs, ws are vlists)

    x in vs
    +vs, -vs
    vs|ws, vs&ws, vs-ws, vs^ws, vs|w, vs&w, vs-w, vs^w
    x in vs, v in vs
    vs <, <=, ==, >=, > ws
    """

    def __init__(self, sf):
        """ sf: boolean valued step function  """
        Stepfun.__init__(self, sf)

    def leftunbounded(self):
        return self.values[0]

    def inside(self, k):
        # if leftopen : return true for uneven k
        # else : return true for even k
        return self.leftunbounded() != k % 2

    def __call__(self, x):
        k = bisect_right(self.steps, x) - 1
        return self.inside(k)

    def complement(self):
        self.values[0] = not self.values[0]

    def __contains__(self, x):
        """ x : Interval or any object.
            Returns true iff x is contained in one of self's intervals
        """
        return self.inside(bisect_right(self, x) - 1)

    def __pos__(self):
        return self

    def __neg__(self):
        """ Returns vlist complementary to self
            Invariant:  v | -v == (-oo, +oo)
        """
        result = Vlist(self)
        result.complement()
        return result

    def union(self, v):
        """ v : interval
            Inserts a non-empty interval in the correct place.
            Runs in O(log n)
            Equivalent to "self | Vlist(v)" which runs in O(n)
            Returns None, changes self """

        if isEmptyInterval(v):  # v is empty, nothing to do
            return None

        aux = [(None, False)] if v[0] is not None else []
        aux += [(v[0], True), (v[1], False)]
        self |= Vlist(aux)

    def union_(self, v):
        if isEmptyInterval(v):  # v is empty, nothing to do
            return None

        i = bisect_left(self.steps, v[0])
        j = bisect_right(self.steps, v[1]) if v[1] else len(self.steps)

        middle = []
        if not self(v[0]) and \
                ((i < len(self.steps) and v[0] < self.steps[i]) or
                 i == len(self.steps)):
            middle.append(v[0])

        if not self(v[1]) and \
                ((j < len(self.steps) and v[1] < self.steps[j]) or
                 (j == len(self.steps) and v[1] is not None)):
            middle.append(v[1])

        self.steps[i:j] = middle
        self.values[0] |= v[0] is None

    def union__(self, v):
        if isEmptyInterval(v):  # v is empty, nothing to do
            return None

        i = bisect_left(self.steps, v[0])
        j = bisect_right(self.steps, v[1]) if v[1] else len(self.steps)
        print("i, j : ", i, j)

        middle = []
        if not self(v[0]) and \
                ((i < len(self.steps) and self.steps[i] < v[0]) or
                 i == len(self.steps)):
            middle.append(v[0])

        if not self(v[1]) and \
                ((j < len(self.steps) and v[1] < self.steps[j]) or
                 (j == len(self.steps) and v[1] is not None)):
            middle.append(v[1])

        print("middle", middle)
        self.steps[i:j] = middle
        print("self.steps", self.steps)
        self.values[0] |= v[0] is None

    def __or__(self, vs):
        """ vs: vlist.
            Returns the elementwise union of self and vs.
            Does not change self.
        """
        if not isinstance(vs, Vlist):
            raise TypeError
        return Vlist(fmerge(or_, self, vs))

    def __and__(self, vs):
        """
        vs: vlist.
            Returns the elementwise intersection of self and vs.
            Does not change self.
        """
        if not isinstance(vs, Vlist):
            raise TypeError
        return Vlist(fmerge(and_, self, vs))

    def __ior__(self, vs):
        """ vs: vlist.
            Computes the elementwise union of self and vs.            
            Changes self.
        """
        Stepfun.__init__(self, self | vs)

    def __sub__(self, vs):
        """
        vs: vlist """
        return self & -vs

    def __xor__(self, vs):
        """ vs: vlist """
        return (self | vs) - (self & vs)

    def __le__(self, vs):
        """ vs: vlist
            Returns True iff each v in self is contained in vs
        """
        return self == self & vs

    def __eq__(self, vs):
        return list.__eq__(self.steps, vs.steps) and \
            self.leftunbounded() == vs.leftunbounded()

    def __lt__(self, ws):
        return self <= ws and not self == ws

    __ge__ = flip(__le__)
    __gt__ = flip(__lt__)

    def __iter__(self):
        b = self.leftunbounded()
        return zip(list(self.steps), cycle((b, not b)))

    def __repr__(self):
        txt = (', ', '), [')
        if self.leftunbounded():
            result = '(-oo, '
            i = 1
        else:
            result = '['
            i = 0

        for s in self.steps[1:]:
            result += str(s) + txt[i]
            i = 1 - i

        result = result[:-3] if i == 0 else result + 'oo)'
        return '[' + result + ']'


iv = Vlist

vs = ((None, False), (0, True), (10, False), (20, True), (30, False))
ws = ((None, False), (5, True), (15, False), (25, True), (35, False))
xs = ((None, True), (50, False), (100, True))
ys = ((None, True),)
zs = ((None, True), (30, False))
ts = ((None, False), (30, True))

x = Vlist(xs)
y = Vlist(ys)
z = Vlist(zs)
v = Vlist(vs)
w = Vlist(ws)
t = Vlist(ts)
