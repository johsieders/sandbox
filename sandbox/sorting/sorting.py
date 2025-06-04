# j.siedersleben
# fasttrack to professional programming
# lesson 5: sorting
# 20.11.2020

import operator
from heapq import heappop, heappush

from collections_.collections2 import merge
from collections_.heap import Heap


def isSorted(xs):
    """
    :param xs: a list
    :return: True iff xs is non-descending
    """
    for i in range(len(xs) - 1):
        if xs[i] > xs[i + 1]:
            return False
    return True


def argmax(xs):
    return max(range(len(xs)), key=lambda i: xs[i])


#########################
####   bubblesort   #####
#########################

def bubble1(xs):
    """
    :param xs: a list
    :return: xs sorted
    recursive, not on place
    """
    k = len(xs)
    if k <= 1:
        return xs

    # bubble rising
    for i in range(k - 1):
        if xs[i] > xs[i + 1]:
            xs[i], xs[i + 1] = xs[i + 1], xs[i]

    # invariant: ys[-1] greater or equal than ys[i]
    # for i <= k -2
    return bubble1(xs[:-1]) + xs[-1:]


def bubble2(xs):
    """
    :param xs: a list
    :return: None
    recursive, on place. Requires indices
    """

    def bubble(k):
        if k <= 1:
            return

        # bubble rising
        for i in range(k - 1):
            if xs[i] > xs[i + 1]:
                xs[i], xs[i + 1] = xs[i + 1], xs[i]

        # invariant: ys[k - 1] greater or equal than ys[i]
        # for i <= k -2
        bubble(k - 1)

    bubble(len(xs))


def bubble3(xs):
    """
    This sorts a list on place
    :param xs: a list
    :return: none
    Standard implementation
    """
    n = len(xs)

    for k in range(n - 1):
        # bubble rising
        for i in range(n - k - 1):
            if xs[i] > xs[i + 1]:
                xs[i], xs[i + 1] = xs[i + 1], xs[i]
        # invariant: top k elements of xs sorted and greater or equal
        # than everything below


def bubble4(xs):
    """
    This sorts a list on place
    :param xs: a list
    :return: none
    Standard implementation improved
    """
    for k in range(len(xs) - 1, 0, -1):
        m = argmax(xs[:k])  # find index of largest element in xs[:k]
        if xs[m] > xs[k]:  # swap xs[m] and xs[k] if necessary
            xs[m], xs[k] = xs[k], xs[m]
        # invariant: top n - k elements of xs sorted and greater or equal
        # than everything below


#########################
#### merge and sort #####
#########################


def msort(xs):
    """
    merge sort
    :param xs: a list
    :param le: a less or equal boolean function
    :return: a new list containing xs sorted
    """
    if len(xs) <= 1:
        return list(xs)
    else:
        m = len(xs) // 2
        return merge(msort(xs[:m]), msort(xs[m:]))


#########################
####   quicksort    #####
#########################

def qsort(xs, le=operator.le):
    """
    quicksort
    :param xs: a list
    :param le: a less or equal boolean function
    :return: a new list containing xs sorted
    """
    if len(xs) <= 1:
        return list(xs)
    else:
        return qsort(list(filter(lambda x: le(x, xs[0]), xs[1:]))) + \
            [xs[0]] + \
            qsort(list(filter(lambda x: not le(x, xs[0]), xs[1:])))


#########################
######  heapsort    #####
#########################

def hsort1(xs):
    """
    heapsort
    :param xs: a list
    :return: a new list containing xs sorted
    Using Python's heapq
    """
    h = []
    for x in xs:
        heappush(h, x)
    return [heappop(h) for _ in range(len(h))]


def hsort2(xs):
    """
    heapsort
    :param xs: a list
    :return: a new list containing xs sorted
    Using our own Heap
    """
    h = Heap()
    for x in xs:
        h.heappush(x)
    return [h.heappop() for _ in range(len(h))]

