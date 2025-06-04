# testing collections
# 20/11/2020
# update 29.04.2025

from random import randrange
from timeit import timeit
from typing import Callable, List

from sympy.logic.boolalg import Boolean

from sandbox.basics.sorting import (is_sorted, bubble1, bubble2, bubble3, bubble4,
                                    msort, qsort, hsort1, hsort2)


def tst_sort(xs: List[int], srt: Callable, inplace: bool) -> None:
    if inplace:
        srt(xs)
        assert(is_sorted(xs))
    else:
        assert(is_sorted(srt(xs)))


def test_all():
    n = 600
    xs = [randrange(n) for _ in range(n)]
    t_bubble1 = timeit(lambda: tst_sort(xs, bubble1, False), number=1)
    t_bubble2 = timeit(lambda: tst_sort(xs, bubble2, True), number=1)
    t_bubble3 = timeit(lambda: tst_sort(xs, bubble3, True), number=1)
    t_bubble4 = timeit(lambda: tst_sort(xs, bubble4, True), number=1)
    t_msort = timeit(lambda: tst_sort(xs, msort, False), number=1)
    t_qsort = timeit(lambda: tst_sort(xs, qsort, False), number=1)
    t_hsort1 = timeit(lambda: tst_sort(xs, hsort1, False), number=1)
    t_hsort2 = timeit(lambda: tst_sort(xs, hsort2, False), number=1)

    print(f'\n{t_bubble1 = :.5f}')
    print(f'\n{t_bubble2 = :.5f}')
    print(f'\n{t_bubble3 = :.5f}')
    print(f'\n{t_bubble4 = :.5f}')
    print(f'\n{t_msort = :.5f}')
    print(f'\n{t_qsort = :.5f}')
    print(f'\n{t_hsort1 = :.5f}')
    print(f'\n{t_hsort2 = :.5f}')
