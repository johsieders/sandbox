# js 8.6.04
# optimization by binary search
# js 26.6.04
# relaunch 21.11.04
# 26.12.04  ok
# 6.3.2013 major revision: vlists as step functions
# 07.01.2024 general check
# 05.06.2025 restart on Mac

from __future__ import annotations

from collections.abc import Sequence
from operator import or_

from sandbox.stepfunctions.stepfun_archive import Stepfun, merge_op


def vlist2timestamps(vs: Sequence) -> list[tuple]:
    """
    vs: Sequence of stepfunctions
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


def timestamps2vlist(ts: Sequence) -> list[tuple]:
    """
    ts: Sequence of timestamps
    returns: list of stepfunctions
    """
    vs = []

    for t, val in ts:
        if val:  # left bound
            vs.append((t, None))
        elif len(vs) > 0:  # right bound
            vs[-1] = (vs[-1][0], t)

    return vs


def iv2tv_list(v: tuple) -> tuple:
    """
    v: an interval given as (lower bound, upper bound)
    both bounds can be infinite, represented by None
    returns: a list of tv-pairs that represent the interval given as (lower, upper).
    """
    if v[0] is not None and v[1] is not None:
        if v[0] >= v[1]:
            raise ValueError('lower bound must be smaller than upper bound')

    if v[0] is None and v[1] is not None:
        return (None, True), (v[1], False)
    elif v[0] is not None and v[1] is not None:
        return (None, False), (v[0], True), (v[1], False)
    elif v[0] is not None and v[1] is None:
        return (None, False), (v[0], True)
    else:
        return ((None, True),)


def normalize(ivs: Sequence) -> tuple:
    """
    ivs: Sequence of intervals given as (lower, upper)
    returns: a normalized tv_list, that is, the timestamps are ascending.
    """
    if len(ivs) == 0:
        return ((None, False),)

    aux = [iv2tv_list(iv) for iv in ivs]
    return merge_op(or_, *aux)


class Vlist(object):
    """
    This class implements lists of non-empty stepfunctions (vlists for short).
    Each interval is

    @ left-bound or left-unbound
    @ right-bound or right-unbound
    @ right-open
    @ left-closed if it is left-bounded

    The bounds are assumed to be int, float or None.
    None as left border represents -oo, and +oo as right border

    Each vlist is either empty, that is, it contains no intervals at all.
    Or it contains one or more non-empty disjoint stepfunctions in ascending order.

    Vlists are closed with respect to union (|), complement (-)
    and intersection. (&). They form a Boolean Algebra.

    This class implements the following operations (vs, ws are vlists, v, w stepfunctions, x floats or ints)

    x in vs
    +vs, -vs
    vs|ws, vs&ws, vs-ws, vs^ws, vs|w, vs&w, vs-w, vs^w
    x in vs, v in vs
    vs <, <=, ==, >=, > ws

    [(None, None)] is a vlist with one interval which is the real line.
    """

    def __init__(self, args: Sequence[tuple] | Stepfun | Vlist):
        """
        vs: (Sequence) a list of intervals given as (lower, upper)
        vs: (Stepfun) a stepfun representing a list of intervals.
        vs: (Vlist) another Vlist
        """
        self.stepfun = None
        if isinstance(args, Vlist):
            self.stepfun = args.stepfun
        elif isinstance(args, Stepfun):
            self.stepfun = args
        elif isinstance(args, Sequence):
            self.stepfun = Stepfun(normalize(args))

    def __and__(self, vs: Vlist) -> Vlist:
        return Vlist(self.stepfun & vs.stepfun)

    def __or__(self, vs: Vlist) -> Vlist:
        aux = self.stepfun | vs.stepfun
        return Vlist(aux)

    def __xor__(self, vs: Vlist) -> Vlist:
        return (self - vs) | (vs - self)

    def __eq__(self, vs: Vlist) -> bool:
        return self.stepfun == vs.stepfun

    def __contains__(self, x) -> bool:
        return self.stepfun(x)

    def __neg__(self) -> Vlist:
        """
        returns the complement of self
        """
        return Vlist(self.stepfun.__not__())

    def __sub__(self, vs) -> Vlist:
        """
        returns set difference self - other
        """
        return self & -vs

    @classmethod
    def empty(cls) -> Vlist:
        return Vlist(())

    @classmethod
    def all(cls) -> Vlist:
        return Vlist(((None, None),))

    def to_vlist(self):
        """
        returns self represented as list of intervals
        """
        return timestamps2vlist(self.stepfun.tv_pairs)

    def __repr__(self):
        return str(self.to_vlist())

    def __str__(self):
        return str(self.to_vlist())
