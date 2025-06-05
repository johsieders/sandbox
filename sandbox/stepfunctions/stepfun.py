# trying to understand stepfunctions
# merge revised, fmerge added 3/6/2013
# completely revised 29/1/2020

from bisect import bisect_right
from collections.abc import Iterable, Iterator
from functools import reduce
from operator import add, mul


def assert_ascending(tv):
    """
    :param tv: an iterator of timestamps. The first timestamp can be None in which case it is ignored.
    :return: tv if the times t are ascending, ValueError otherwise
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


def weakop(op, xs):
    ys = [x for x in xs if x is not None]
    return reduce(op, ys) if ys else None


def stepmerge(op, *fs: Iterable) -> Iterator:
    """
    :param op: an operator such as add, min, max
    :param fs: an iterable of lists of timestamps
    :return: merge by op of all f in fs as iterable of timestamps
    """

    fs = [assert_ascending(f) for f in fs]

    head = {}.fromkeys(fs)  # dictionary of last read entries, key = f, value = (x, v)
    val = {}.fromkeys(fs)  # dictionary of current value at f, key = f
    lastval = fs  # any value not occurring in one of the f

    while True:
        for f in fs:  # fill heads by reading next (step, value)
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

        for f in fs:  # update values
            if head[f] and head[f][0] == nextstep:
                val[f] = head[f][1]
                head[f] = None

        v = weakop(op, val.values())
        if v != lastval:  # check if value has changed
            lastval = v
            yield nextstep, v


class Stepfun:
    """
    step functions are stepwise constant. They are given by a list of
    timestamps = (time, value). Step functions are right-continuous, that is:
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

    def __init__(self, sf, check=True):
        # combine intervals with identical values
        self.timestamps = list(stepmerge(mul, sf, ((None, None),)) if check else sf)

        # check input
        if len(self.timestamps) < 1 or self.timestamps[0][0] is not None:
            raise ValueError

    @classmethod
    def const(self, value):
        return Stepfun(((None, value),), check=False)

    def merge(self, op, *others):
        """
        :param op: an binary operator such as add, mul, max, min
        :param others: other stepfunctions
        :return: arguments merged into self by op:
        The result's timestamps are the union of all others;
        the function value is the stepwise sum/mul/max/min
        """
        return Stepfun(stepmerge(op, self.timestamps, *[x.timestamps for x in others]), False)

    def replace_none_with_constant(self, const):
        """
        :param const a constant
        :return: self with all Nones replaced by const
        self not modified
        """
        return self.replace_none_with_function(Stepfun(((None, const),), False))

    def replace_none_with_function(self, sf):
        """
        :param sf a sepfunction to replace all Nones
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

    def __call__(self, x):
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

    def __add__(self, others):
        return self.merge(add, others)

    def __sub__(self, other):
        return self.merge(add, -other)

    def __mul__(self, others):
        return self.merge(mul, others)

    def __abs__(self):
        def weakabs(x):
            return None if x is None else abs(x)

        return Stepfun([(t, weakabs(v)) for t, v in self.timestamps], False)

    def __pos__(self):
        return Stepfun(self.timestamps, False)

    def __neg__(self):
        def weakminus(x):
            return None if x is None else -x

        return Stepfun([(t, weakminus(v)) for t, v in self.timestamps], False)

    def is_positive(self):
        return all(v is not None and v > 0 for t, v in self.timestamps)

    def isnoneorpositive(self):
        return all(v is None or v > 0 for t, v in self.timestamps)

    def isnonnegative(self):
        return all(v is not None and v >= 0 for t, v in self.timestamps)

    def isnoneornonnegative(self):
        return all(v is None or v >= 0 for t, v in self.timestamps)

    def iszero(self):
        return all(v is not None and not v for t, v in self.timestamps)

    def isnoneorzero(self):
        return all(not v for t, v in self.timestamps)

    def __iter__(self):
        return iter(self.timestamps)

    def __len__(self):
        return len(self.timestamps)

    def __le__(self, other):
        return not (self - other).is_positive()

    def __lt__(self, other):
        return (other - self).is_positive()

    def __eq__(self, other):
        return (self - other).isnoneorzero()

    def __repr__(self):
        return repr(list(self.timestamps))

    @classmethod
    def scan(cls, f, start, stop, step=1):
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
