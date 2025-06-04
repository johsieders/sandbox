# testing collections
# 20/11/2020
# update 29.04.2025

from timeit import timeit
from typing import Callable

from sandbox.basics.merge import merge, merge_r


# def list_equal(xs, ys) -> bool:
#     for x, y in zip(xs, ys):
#         if x != y:
#             return False
#     return True


def tst_merge(mrg: Callable) -> None:
    n = 300  # n < 1000 recursion stack overflow
    for i in range(n):
        xs = i * [1]
        ys = 2 * i * [1]
        m = mrg(xs, ys)
        assert (3 * i * [1] == m)

    xs = [9, 11]
    ys = [2, 4, 5, 100]
    expected_result = [2, 4, 5, 9, 11, 100]
    assert (mrg(xs, ys) == expected_result)


def test_all():
    t_fast = timeit(lambda: tst_merge(merge), number=1)
    t_rec = timeit(lambda: tst_merge(merge_r), number=1)

    print(f'\n{t_fast = :.5f}')
    print(f'\n{t_rec = :.5f}')
