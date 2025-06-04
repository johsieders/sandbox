# testing collections
# 20/11/2020
# updated 11.05.2025


import heapq
import random
import string
from timeit import timeit

import sandbox.basics.heap as heap


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def test_heap() -> None:
    n = 10000
    input = heap.Heap()
    output = []
    for _ in range(n):
        heap.heappush(input, id_generator())
    backup = list(input)
    backup.sort()

    for _ in range(n):
        output.append(heap.heappop(input))
    assert output == backup


def test_heapq() -> None:
    n = 10000
    input = []
    output = []
    for _ in range(n):
        heapq.heappush(input, id_generator())
    backup = list(input)
    backup.sort()

    for _ in range(n):
        output.append(heapq.heappop(input))
    assert output == backup


def test_all():
    t_heap = timeit(lambda: test_heap(), number=1)
    t_deque = timeit(lambda: test_heapq(), number=1)

    print(f'\n{t_heap = :.5f}')
    print(f'\n{t_deque = :.5f}')
