# js 8.6.04
# optimization by binary search
# js 26.6.04
# relaunch 21.11.04
# 26.12.04  ok
# 6.3.2013 major revision: vlists as step functions
# 07.01.2024 general check
# 05.06.2025 restart on Mac

from __future__ import annotations

from collections.abc import Iterable

from sandbox.stepfunctions.stepfun import Stepfun


def vlist2timestamps(vs: Iterable) -> list[tuple]:
    """
    vs: iterable of intervals
    returns: list of timestamps
    """

    ts = [(None, False)]
    rb = None

    for lb, rb in vs:
        if lb is not None:
            ts.append((lb, True))
        else:
            ts[0] = (lb, True)

    if rb is not None:
        ts.append((rb, False))

    return ts


def timestamps2vlist(ts: Iterable) -> list[tuple]:
    """
    ts: iterable of timestamps
    returns: list of intervals
    """
    vs = []

    for t, val in ts:
        if val:  # left bound
            vs.append((t, None))
        elif len(vs) > 0:  # right bound
            vs[-1] = (vs[-1][0], t)

    return vs


class Vlist(object):
    """
    This class implements lists of non-empty intervals (vlists for short).
    Each interval is

    @ left-bound or left-unbound
    @ right-bound or right-unbound
    @ right-open
    @ left-closed if it is left-bounded

    The bounds are assumed to be int, float or None.
    None as left border represents -oo, and +oo as right border

    Each vlist is either empty, that is, it contains no intervals at all.
    Or it contains one or more non-empty disjoint intervals in ascending order.

    Vlists are closed with respect to union (|), complement (-)
    and intersection. (&). They form a Boolean Algebra.

    This class implements the following operations (vs, ws are vlists, v, w intervals, x reals or ints)

    x in vs
    +vs, -vs
    vs|ws, vs&ws, vs-ws, vs^ws, vs|w, vs&w, vs-w, vs^w
    x in vs, v in vs
    vs <, <=, ==, >=, > ws

    [(None, None)] is a vlist with one interval which is the real line.
    """

    def __init__(self, vs: Iterable[tuple] | Stepfun):
        """
        vs: iterable of intervals or a Stepfun
        """
        if isinstance(vs, Stepfun):
            self.stepfun = vs
        elif isinstance(vs, Iterable):
            ts = vlist2timestamps(vs)
            self.stepfun = Stepfun(ts, check=True)

    def __and__(self, vs: Vlist) -> Vlist:
        return Vlist(self.stepfun & vs.stepfun)

    def __or__(self, vs: Vlist) -> Vlist:
        return Vlist(self.stepfun | vs.stepfun)

    def __xor__(self, vs: Vlist) -> Vlist:
        return (self - vs) | (vs - self)

    def __eq__(self, vs: Vlist) -> bool:
        return self.stepfun == vs.stepfun

    def __contains__(self, x) -> bool:
        return self.stepfun(x)

    def __neg__(self) -> Vlist:
        return Vlist(self.stepfun.__not__())

    def __sub__(self, vs):
        """
        vs: vlist
        returns: list of intervals
        """
        return self & -vs

    @classmethod
    def empty(cls) -> Vlist:
        return Vlist(())

    @classmethod
    def all(cls) -> Vlist:
        return Vlist(((None, None),))

    def to_vlist(self):
        return timestamps2vlist(self.stepfun.timestamps)

    def __repr__(self):
        return str(self.to_vlist())

    def __str__(self):
        return str(self.to_vlist())
