# trying to understand stepfunctions
# merge revised, fmerge added 3/6/2013
# completely revised 29/1/2020
# revised for Mac 06.06.2025

from __future__ import annotations

from bisect import bisect_right
from collections.abc import Iterable, Iterator, Callable
from functools import reduce
from operator import add, mul, and_, or_
from typing import Any


def check_ascending(tv: Iterable[tuple]) -> Iterator[tuple]:
    """
    :param tv: an iterator of timestamps. The first timestamp can be None in which case it is ignored.
    :return: true if first timestamp is None and all others strictly ascending
    """
    tv = iter(tv)
    try:
        last = next(tv)
    except StopIteration:
        return
    yield last

    if last[0] is None:
        try:
            last = next(tv)
        except StopIteration:
            return
        yield last

    for t, v in tv:
        if t <= last[0]:
            raise ValueError
        else:
            last = t, v
            yield last


def weak_op(op, xs: Iterable[Any]) -> Any:
    """
    :param op: an operator
    :param xs: an iterable of values
    :return: the resulting value
    weakop applies op to all not-None elements in xs
    None if all elements in xs are None
    """
    ys = [x for x in xs if x is not None]
    return reduce(op, ys) if ys else None


def merge_op(op, *tv: Iterable[tuple]) -> Iterator[tuple]:
    """
    :param op: an operator such as add, min, max
    :param tv: an iterable of lists of timestamps
    :return: merge by op of all f in fs as iterable of timestamps
    It returns None if all lists are empty
    Example:
    stepmerge(add, xs, ys, zs) returns an Iterator of the elementwise sum of xs, ys, zs where
    the lists can be of any length.
    """
    tv = [check_ascending(f) for f in tv]

    head = {}.fromkeys(tv)  # dictionary of last read entries, key = f, value = (x, v)
    val = {}.fromkeys(tv)  # dictionary of current value at f, key = f
    lastval = tv  # any value not occurring in one of the f

    while True:
        for f in tv:  # fill heads by reading next (step, value)
            if head[f] is None:
                try:
                    head[f] = next(f)
                except StopIteration:
                    pass

        heads = [h[0] for h in head.values() if h]
        if heads:  # there are heads left
            aux = [x for x in heads if x is not None]
            nextstep = min(aux) if aux else None
        else:  # return if all f are done
            return

        for f in tv:  # update values
            if head[f] and head[f][0] == nextstep:
                val[f] = head[f][1]
                head[f] = None

        v = weak_op(op, val.values())
        if v != lastval:  # check if value has changed
            lastval = v
            yield nextstep, v


class Stepfun(object):
    """
    Step functions are stepwise constant.
    A step function is given by a list of (time, value)-pairs where the first t is None
    and the following strictly ascending. Values can be of any type, depending on the
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

    weak operators:
    add, sub, mul, abs, pos, neg and equals are weak operators,
    e.g.: None op None == None; None op x == x op None == x; abs(None) == None;
    None == None is true, None == x is false

    strict operators:
    <, <= are strict, so: x op y is false whenever at least one operand ist None
    """

    def __init__(self, ts: Iterable[tuple], check=True):
        # combine intervals with identical values
        if check:
            self.timestamps = tuple(merge_op(mul, ts, ((None, None),)))
        else:
            self.timestamps = tuple(ts)

        # check input
        if len(self.timestamps) < 1 or self.timestamps[0][0] is not None:
            raise ValueError

    @classmethod
    def const(cls, value: Any) -> Stepfun:
        return Stepfun(((None, value),), check=False)

    def merge(self, op: Callable, *others: Stepfun) -> Stepfun:
        """
        :param op: a binary operator such as add, mul, max, min
        :param others: other stepfunctions
        :return: arguments merged into self by op:
        The result's timestamps are the union of all others;
        the function value is the stepwise sum/mul/max/min
        """
        return Stepfun(merge_op(op, self.timestamps, *(x.timestamps for x in others)), False)

    def replace_none_with_constant(self, const: Any) -> Stepfun:
        """
        :param const a constant
        :return: self with all Nones replaced by const
        self not modified
        """
        return self.replace_none_with_function(Stepfun(((None, const),), False))

    def replace_none_with_function(self, sf) -> Stepfun:
        """
        :param sf a stepfunction with all Nones to be replaced
        :return: self with all Nones replaced by the incumbent value of sf
        self not modified
        """
        replace = lambda x, y: y if x is None else x
        return self.merge(replace, sf)

    def relocate(self, ts):
        """
        :param ts: an iterator of ascending timestamps, not None
        :return: a stepfunction with (t, self(t)) as new timestamps
        """

        def aux():
            yield None, self.timestamps[0][1]
            for t in ts:
                yield t, self(t)

        return Stepfun(aux())

    def __call__(self, x: int | float | None) -> Any:
        """
        :param x: the argument (can be None)
        :return: value of self at x
        self(None) returns leftmost value
        """
        # function is constant
        if len(self) == 1 or x is None:
            return self.timestamps[0][1]

        # len(self) >= 2
        ts = [t for t, v in self.timestamps[1:]]
        i = bisect_right(ts, x)
        return self.timestamps[i][1]

    def __and__(self, others: Stepfun) -> Stepfun:
        return self.merge(and_, others)

    def __or__(self, others: Stepfun) -> Stepfun:
        return self.merge(or_, others)

    def __add__(self, others: Stepfun) -> Stepfun:
        return self.merge(add, others)

    def __sub__(self, other: Stepfun) -> Stepfun:
        return self.merge(add, -other)

    def __mul__(self, others: Stepfun) -> Stepfun:
        return self.merge(mul, others)

    def __abs__(self) -> Stepfun:
        def weak_abs(x):
            return None if x is None else abs(x)

        return Stepfun(((t, weak_abs(v)) for t, v in self.timestamps), False)

    def __pos__(self) -> Stepfun:
        return Stepfun(self.timestamps, False)

    def __neg__(self) -> Stepfun:
        def weak_minus(x):
            return None if x is None else -x

        return Stepfun(((t, weak_minus(v)) for t, v in self.timestamps), False)

    def __not__(self) -> Stepfun:
        def weak_not(x):
            return None if x is None else  not x

        return Stepfun(((t, weak_not(v)) for t, v in self.timestamps), False)

    def is_positive(self) -> bool:
        return all(v is not None and v > 0 for t, v in self.timestamps)

    def is_none_or_positive(self) -> bool:
        return all(v is None or v > 0 for t, v in self.timestamps)

    def is_nonnegative(self) -> bool:
        return all(v is not None and v >= 0 for t, v in self.timestamps)

    def is_none_or_nonnegative(self) -> bool:
        return all(v is None or v >= 0 for t, v in self.timestamps)

    def is_zero(self) -> bool:
        return all(v is not None and not v for t, v in self.timestamps)

    def is_none_or_zero(self) -> bool:
        return all(not v for t, v in self.timestamps)

    def __iter__(self):
        return iter(self.timestamps)

    def __len__(self) -> int:
        return len(self.timestamps)

    def __le__(self, other: Stepfun) -> bool:
        return not (self - other).is_positive()

    def __lt__(self, other: Stepfun) -> bool:
        return (other - self).is_positive()

    def __eq__(self, other: Stepfun) -> bool:
        return (self - other).is_none_or_zero()

    def __repr__(self) -> str:
        return repr(self.timestamps)

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

        return Stepfun(tv())

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
            return weakmul(self.timestamps[0][1], stop - start)

        # function is not constant, len(self) >= 2
        aux = self * Stepfun(((None, 0), (start, None), (stop, 0)), False)
        result = 0
        for i in range(2, len(aux)):
            result += weakmul(aux.timestamps[i - 1][1],
                              (aux.timestamps[i][0] - aux.timestamps[i - 1][0]))
        return result
