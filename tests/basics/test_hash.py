# testing collections
# 20/11/2020
# 11/05/2025

from sandbox.basics.hash import make_dict, Hashdict


def test_make_dict():
    g, s = make_dict()

    caught = False
    try:
        g(1)
    except ValueError:
        caught = True
    assert (caught)

    n = 1000

    for i in range(n):
        s(i, str(5 * i))

    for i in range(n):
        s(i, str(10 * i))

    for i in range(n):
        assert (str(10 * i) == g(i))


def test_hash():
    dict = Hashdict()

    caught = False
    try:
        a = dict[1]
    except ValueError:
        caught = True
    assert (caught)

    n = 1000

    for i in range(n):
        dict[i] = str(5 * i)

    for i in range(n):
        dict[i] = str(10 * i)

    for i in range(n):
        assert (str(10 * i) == dict[i])
