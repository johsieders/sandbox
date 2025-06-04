# testing collections
# 20/11/2020
# update 29.04.2025

from sandbox.basics.hanoi import hanoi_mutable, hanoi_immutable, hanoi_naked

import timeit

def test_hanoi():
    n = 15
    result =[]

    t_naked= timeit.timeit(lambda: hanoi_naked(n), number=1)
    print(f'\n{t_naked = :.5f}')

    t_mutable = timeit.timeit(lambda: result.append(hanoi_mutable(n)), number=1)
    assert (2 ** n == len(result[-1]))
    print(f'\n{t_mutable = :.5f}')

    t_immutable = timeit.timeit(lambda: result.append(hanoi_immutable(n)), number=1)
    assert (2 ** n == len(result[-1]))
    print(f'\n{t_immutable = :.5f}')




