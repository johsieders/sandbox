# Python time iterators
# js, 8.6.04
# js, 7.2.2020

from timeit import *


def timeIterators():
    print()
    t = Timer('take(500, hamming(2,3,5))', 'from iterators import hamming, take')
    result = t.repeat(2, 20)
    print('20*take(500, hamming(2,3,5)) : ', result)

    # works with 171 but not with 172
    t = Timer('take(171, multiply(sin(), cos()))', 'from iterators import multiply, sin, cos, take')
    result = t.repeat(2, 20)
    print('20*take(171, multiply(sin(), cos())) : ', result)

    # works with 171 but not with 172
    t = Timer('take(171, inverse(exp()))', 'from iterators import inverse, exp, take')
    result = t.repeat(2, 20)
    print('20*take(171, inverse(exp())) : ', result)


if __name__ == '__main__':
    timeIterators()