# testing collections
# 20/11/2020
# 11/05/2025

from sandbox.basics.histogram import histogram_1, histogram_2, histogram_3, histogram_4
from sandbox.basics.index import index_1, index_2, index_2a


def test_histogram():
    histograms = (histogram_1, histogram_2, histogram_3, histogram_4)
    xss = [[], [1], [0, 1, 2, 2, 3, 3, 3]]
    for hg in histograms:
        for xs in xss:
            h = hg(xs)
            for x in xs:
                assert (h[x] == xs.count(x))


def test_index_1():
    book = [['xx', 'yy', 'zz'],
            ['xx', 'uu', 'zz'],
            ['xx', 'yy', 'vv', 'tt']]

    index = index_1(book)
    for w, ps in index.items():
        for p in ps:
            assert (w in book[p])


def test_index_2():
    book = [['xx', 'yy', 'zz', 'aa'],
            ['xx', 'uu', 'zz'],
            ['xx', 'yy', 'vv', 'tt']]
    keywords = ['xx', 'tt', 'uu', 'bb']
    fs = (index_2, index_2a)
    for f in fs:
        index = f(book, keywords)
        keys = list(index.keys())
        assert (keys.sort() == keywords.sort())
        for w, ps in index.items():
            for p in ps:
                assert (w in book[p])
