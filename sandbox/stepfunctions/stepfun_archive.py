# trying to understand stepfunctions
# merge revised, fmerge added 3/6/2013
# completely revised 29/1/2020
# rewritten 15.06.2025

from __future__ import annotations

import heapq
from bisect import bisect_right
from collections.abc import Sequence, Callable
from functools import reduce
from operator import add, mul, and_, or_
from typing import Any


def check_ascending(tv_pairs: Sequence) -> tuple:
    """
    :param tv_pairs: a sequence of tv-pairs.
    :return: the given tv-pairs as a tuple.
    An exception is raised if the time of the tv-pairs are not strictly ascending.
    """
    last = None
    for t, v in tv_pairs:
        if last is not None and t <= last:
            raise ValueError()
        else:
            last = t
    return tuple(tv_pairs)


def weak_op(op) -> Callable:
    """
    :param op: a binary operator
    :return: a weak operator covering op
    weak_op applies op to all not-None elements in args
    It returns None if all elements in args are None
    """

    def aux(args) -> Any:
        ys = [x for x in args if x is not None]
        return reduce(op, ys) if ys else None

    return aux


def merge_op(op, *tv_pairs: Sequence) -> tuple:
    """
    :param op: a binary operator such as add, min, max
    :param tv_pairs: a sequence of lists of tv_pairs
    :return: merge by op of all f in fs as Sequence of tv_pairs
    Each tv_list has a first entry with timestamp = None.
    So, ((None,None),) represents a function which is nowhere defined.
    Example: merge_op(add, xs, ys, zs) returns an Iterator of
    the elementwise sum of xs, ys, zs where the lists can be of any length > 0.
    """

    val = {}  # dictionary of current value at tvi, key = #tv_iterator, value = v
    w_op = weak_op(op)
    tv_iterators = []

    for k, tvi in enumerate(tv_pairs):
        if len(tvi) == 0:
            raise ValueError
        t, v = tvi[0]
        if t is not None:
            raise ValueError
        val[k] = v
        tv_iterators.append([(k, p) for p in tvi[1:]])

    result = []
    last_t, last_v = None, ""

    for k, (t, v) in heapq.merge(*tv_iterators, key=lambda p: p[1][0]):
        if t != last_t:
            w = w_op(val.values())
            if last_v != w:
                result.append((last_t, w))
                last_v = w
            last_t = t
        val[k] = v

    w = w_op(val.values())
    if w != last_v:
        result.append((last_t, w))

    return tuple(result)


class Stepfun(object):
    """
    Step functions are stepwise constant.
    A step function f is given by a list of (time, value)-pairs where the first t is None
    and the following timestamps are strictly ascending. Values can be of any type, depending on the
    operands to be applied. The value None means "undefined".
    Step functions are right-continuous, that is:
    f(x) = value[i] with time[i] <= x < time[i+1]
    This class guarantees:
    a) first timestamp is -oo, represented by None
    b) timestamps are strictly increasing
    c) the value changes at each timestamp.
    Step functions are constant from and including the last timestamp until +oo.
    Intervals where the function is undefined are indicated by None.
    Examples:
    (1) ((None, None),) is the function which is nowhere defined
    (2) ((None, None), (0, 100), (10, 200), (20, None))
    is undefined on (-oo, 0), 100 on [0, 10), 200 on [10, 20) and again undefined on [20, +oo)
      __call__(x) returns the function value at x
    Stepfunctions are immutable.

    Stepfunctions can have any value, but integer, float and boolean are frequent.
    Stepfunctions overload the standard operators.
    weak operators:
    add, sub, mul, abs, pos, neg and equals are weak operators,
    e.g.: None op None == None; None op x == x op None == x; abs(None) == None;
    None == None is true, None == x is false

    strict operators:
    <, <= are strict, so: x op y is false whenever at least one operand ist None
    """

    def __init__(self, args: Stepfun | Sequence):
        """
        :param args: a Stepfun or a sequence of tv_pairs
        tv_pairs are assumed to be sorted by timestamp; the first timestamp being None
        If not
        """

        if isinstance(args, Stepfun):
            self.tv_pairs = args.tv_pairs
        elif isinstance(args, Sequence):
            self.tv_pairs = check_ascending(args)
            if len(self.tv_pairs) < 1 or self.tv_pairs[0][0] is not None:
                raise ValueError
        else:
            raise ValueError

    @classmethod
    def const(cls, value: Any) -> Stepfun:
        return Stepfun(((None, value),))

    def merge(self, op: Callable, *others: Stepfun) -> Stepfun:
        """
        :param op: a binary operator such as add, mul, max, min
        :param others: other stepfunctions
        :return: arguments merged into self by op:
        The result's timestamps are the union of all others;
        the function value is the stepwise sum/mul/max/min
        """
        return Stepfun(merge_op(op, self.tv_pairs, *(x.tv_pairs for x in others)))

    def replace_none_with_constant(self, const: Any) -> Stepfun:
        """
        :param const a constant
        :return: self with all Nones replaced by const
        self not modified
        """
        return self.replace_none_with_function(Stepfun(((None, const),)))

    def replace_none_with_function(self, sf) -> Stepfun:
        """
        :param sf a stepfunction with all Nones to be replaced
        :return: self with all Nones replaced by the incumbent value of sf
        self not modified
        """
        replace = lambda x, y: y if x is None else x
        return self.merge(replace, sf)

    def relocate(self, ts) -> Stepfun:
        """
        :param ts: an iterator of ascending timestamps, not None
        :return: a stepfunction with (t, self(t)) as new timestamps
        """

        def aux():
            yield None, self.tv_pairs[0][1]
            for t in ts:
                yield t, self(t)

        return Stepfun(tuple(aux()))

    def __call__(self, x: int | float | None) -> Any:
        """
        :param x: the argument (can be None)
        :return: value of self at x
        self(None) returns leftmost value
        """
        # function is constant
        if len(self) == 1 or x is None:
            return self.tv_pairs[0][1]

        # len(self) >= 2
        ts = [t for t, v in self.tv_pairs[1:]]
        i = bisect_right(ts, x)
        return self.tv_pairs[i][1]

    def __and__(self, other: Stepfun) -> Stepfun:
        return self.merge(and_, other)

    def __or__(self, other: Stepfun) -> Stepfun:
        return self.merge(or_, other)

    def __add__(self, other: Stepfun) -> Stepfun:
        return self.merge(add, other)

    def __sub__(self, other: Stepfun) -> Stepfun:
        return self.merge(add, -other)

    def __mul__(self, other: Stepfun) -> Stepfun:
        return self.merge(mul, other)

    def __abs__(self) -> Stepfun:
        def weak_abs(x):
            return None if x is None else abs(x)

        return Stepfun([(t, weak_abs(v)) for t, v in self.tv_pairs])

    def __pos__(self) -> Stepfun:
        return Stepfun(self.tv_pairs)

    def __neg__(self) -> Stepfun:
        def weak_minus(x):
            return None if x is None else -x

        return Stepfun([(t, weak_minus(v)) for t, v in self.tv_pairs])

    def __not__(self) -> Stepfun:
        def weak_not(x):
            return None if x is None else not x

        return Stepfun([(t, weak_not(v)) for t, v in self.tv_pairs])

    def is_positive(self) -> bool:
        return all(v is not None and v > 0 for t, v in self.tv_pairs)

    def is_none_or_positive(self) -> bool:
        return all(v is None or v > 0 for t, v in self.tv_pairs)

    def is_non_negative(self) -> bool:
        return all(v is not None and v >= 0 for t, v in self.tv_pairs)

    def is_none_or_non_negative(self) -> bool:
        return all(v is None or v >= 0 for t, v in self.tv_pairs)

    def is_zero(self) -> bool:
        return all(v is not None and not v for t, v in self.tv_pairs)

    def is_none_or_zero(self) -> bool:
        return all(not v for t, v in self.tv_pairs)

    def __iter__(self):
        return iter(self.tv_pairs)

    def __len__(self) -> int:
        return len(self.tv_pairs)

    def __le__(self, other: Stepfun) -> bool:
        return not (self - other).is_positive()

    def __lt__(self, other: Stepfun) -> bool:
        return (other - self).is_positive()

    def __eq__(self, other: Stepfun) -> bool:
        return self.tv_pairs == other.tv_pairs

    def __repr__(self) -> str:
        return repr(self.tv_pairs)

    @classmethod
    def scan(cls, f: Callable, start, stop, step=1) -> Stepfun:
        """
        :param f: a function
        :param start: first timestamp scanned
        :param stop: last timestamp scanned
        :param step: distance between timestamps
        :return: a stepfunction with values f(t) at timestamp t.
        It is undefined on (-oo, start) and equal to f(stop) on [stop, +oo)
        """

        def tv():
            yield None, None
            current = start
            while current < stop:
                yield current, f(current)
                current += step
            if start <= stop:
                yield stop, f(stop)

        return Stepfun(tuple(tv()))

    def integral(self, start, stop):
        """
        :param start: lower bound of interval to be integrated
        :param stop: upper bound of interval to be integrated
        :return: integral of self from start to stop
        Nones are counted as zero
        """

        def weakmul(x, y):
            return 0 if x is None else x * y

        # trivial case
        if stop <= start:
            return 0

        # function is constant
        if len(self) == 1:
            return weakmul(self.tv_pairs[0][1], stop - start)

        # function is not constant, len(self) >= 2
        aux = self * Stepfun(((None, 0), (start, None), (stop, 0)))
        result = 0
        for i in range(2, len(aux)):
            result += weakmul(aux.tv_pairs[i - 1][1],
                              (aux.tv_pairs[i][0] - aux.tv_pairs[i - 1][0]))
        return result
