# testing collections
# 20/11/2020
# update 29.04.2025

from random import randrange
from timeit import timeit
from typing import Callable, List

from sandbox.basics.sorting import (is_sorted,
                                    bubble1, bubble2, bubble3, bubble4,
                                    msort, qsort, hsort1, hsort2)


def tst_sort(xs: List[int], srt: Callable, inplace: bool) -> None:
    if inplace:
        srt(xs)
        assert (is_sorted(xs))
    else:
        assert (is_sorted(srt(xs)))


def test_all():
    srt = {bubble1: False,
           bubble2: True,
           bubble3: True,
           bubble4: True,
           msort: False,
           qsort: False,
           hsort1: False,
           hsort2: False}
    time = {}

    n = 900
    xs = [randrange(n) for _ in range(n)]
    for s in srt.keys():
        time[s] = timeit(lambda: tst_sort(xs, s, srt[s]), number=1)

    sorted_time = sorted(time.items(), key=lambda x: x[1])

    print('\n')
    for s, t in sorted_time:
        print(f'{s.__name__} = {t:.5f}')
