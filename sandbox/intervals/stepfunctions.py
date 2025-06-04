# updated 29.04.2025


from bisect import bisect_right
from collections.abc import Callable, Iterable, Iterator
from functools import reduce

from sandbox.basics.merge import merge


def fmerge(op: Callable, *tv: Iterable) -> Iterator:
    """
    tv: an iterable of (time, value)-pairs
    returns a new step function F stepping at each step of any input function
    values are given by F(x) = fun(*fs(x))
    """

    def weak(xs):
        ys = [x for x in xs if x is not None]
        return reduce(op, ys) if ys else None

    if len(tv) == 0:
        raise ValueError

    tv = [iter(t) for t in tv]
    heads = [next(t) for t in tv]
    val = [h[1] for h in heads]
    yield None, weak(val)

    heads = [next(t, None) for t in tv]
    actives = list(range(len(tv)))
    while True:
        for i in actives:  # fill heads by reading next(step, value)
            if heads[i] is None:
                heads[i] = next(tv[i], None)
                if heads[i] is None:  # this f is done
                    actives.remove(i)
        if not actives:
            return

        i = min(actives, key=lambda i: heads[i][0])
        t = heads[i][0]  # next step
        val[i] = heads[i][1]  # update value
        heads[i] = None  # rewind heads[i]
        yield t, weak(val)


class Stepfun:
    """ step functions are stepwise constant. They are given by a list
        (step, value). Step functions are assumed to be right-continuous.
        The first step is always at -oo represented by None.
        Step functions are constant from and including the last step until
        +oo.
        The value None stands for undefined. The weak functions ignores operands whose
        value is None; it returns None if there is no result.
        Example: The list ((None, None), (0, 100), (10, 200), (20, None))
        defines a function which is 100 on the interval [0, 10),
        200 on [10, 20) and undefined elsewhere.
        Steps must be non-descending.
        The constructor does the following:
        Of n equal steps it keeps the last one: [.., (0, 10), (0, 20)] is the same as [.., (0, 20)]
        Of n equal values, it keeps the first one: [.., (0, 10), (5, 10)] is the same as [.., (0, 10)]
        __call__(x) returns the function value at x
    """

    def __init__(self, sf):
        sf = iter(sf)
        self.steps = []
        self.values = []
        laststep, lastval = next(sf)
        if laststep is not None:
            raise ValueError
        self.steps.append(laststep)
        self.values.append(lastval)
        for s, v in sf:
            if laststep is not None and s < laststep:
                raise ValueError
            if s == laststep:
                self.values[-1] = v
                lastval = v
            elif v != lastval:
                self.steps.append(s)
                self.values.append(v)
                laststep = s
                lastval = v

    def __call__(self, x):
        i = bisect_right(self.steps, x, lo=1) - 1
        return self.values[i]

    def __iter__(self):
        return zip(self.steps, self.values)

    def fmerge(self, op: Callable, *sf):
        def weak(xs):
            ys = [x for x in xs if x is not None]
            return reduce(op, ys) if ys else None

        aux = merge(*[f.steps for f in sf])
        steps = [None]
        values = []
        for s in aux:
            steps.append(s)
            values.append(weak(*[f(s) for f in sf]))
        return fmerge(op, self, *sf)
