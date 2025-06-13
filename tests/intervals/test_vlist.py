# Python Test intervals
# js, 8.6.04
# js 25.12.04
# js 05.06.2025


from sandbox.intervals.vlist import Vlist

N = 10

vss = [
    [],
    [(None, None)],
    [(None, 0)],
    [(0, None)],
    [(0, 1)],
    [(None, 0), (1, None)],
    [(0, 1), (2, 3)],
    [(None, 0), (1, 2), (3, None)]
]


def test_constructor():
    for vs in vss:
        ws = Vlist(vs)
        assert vs == ws.to_vlist()


def test_contains():
    v = Vlist([(None, None)])
    assert -1 in v
    assert 0 in v
    assert 1 in v

    v = Vlist([(0, 10)])
    assert 0 in v
    assert 9.9999 in v
    assert 10 not in v


def test_union():
    v = Vlist([(0, 1)])
    w = Vlist([(-1, 2)])

    assert w == v | w

    w = v | Vlist([(1, 2)])
    assert w == Vlist([(0, 2)])

    w = v | Vlist([(2, 3)])
    assert w == Vlist([(0, 1), (2, 3)])


def test_intersection():
    v = Vlist(((0, 10), (20, 30)))
    w = v & Vlist(((-10, -5),))
    assert w == Vlist.empty()

    w = v & Vlist(((-10, 0),))
    assert w == Vlist.empty()

    w = v & Vlist(((-10, 5),))
    assert w == Vlist(((0, 5),))

    w = v & Vlist(((-10, 10),))
    assert w == Vlist(((0, 10),))

    w = v & Vlist(((-10, 20),))
    assert w == Vlist(((0, 10),))

    w = v & Vlist(((-10, 25),))
    assert w == Vlist(((0, 10), (20, 25)))

    w = v & Vlist(((-10, 30),))
    assert w == Vlist(((0, 10), (20, 30)))

    w = v & Vlist(((-10, 35),))
    assert w == Vlist(((0, 10), (20, 30)))

    ## untere Grenze wandert, obere Grenze fest
    w = v & Vlist(((35, 40),))
    assert w == Vlist.empty()

    w = v & Vlist(((30, 40),))
    assert w == Vlist.empty()

    w = v & Vlist(((25, 40),))
    assert w == Vlist(((25, 30),))


    w = v & Vlist(((20, 40),))
    assert w == Vlist(((20, 30),))

    w = v & Vlist(((15, 40),))
    assert w, Vlist(((20, 30),))

    w = v & Vlist(((10, 40),))
    assert w, Vlist(((20, 30),))

    w = v & Vlist(((5, 40),))
    assert w == Vlist(((5, 10), (20, 30)))

    w = v & Vlist(((0, 40),))
    assert w == Vlist(((0, 10), (20, 30)))

    w = v & Vlist(((-10, 40),))
    assert w == Vlist(((0, 10), (20, 30)))


def test_union1():
    v = Vlist(((0, 10), (20, 30)))
    w = v | Vlist(((-10, -5),))
    assert w == Vlist(((-10, -5), (0, 10), (20, 30)))

    w = v | Vlist(((-10, 0),))
    assert w == Vlist(((-10, 10), (20, 30)))

    w = v | Vlist(((-10, 5),))
    assert w == Vlist(((-10, 10), (20, 30)))

    w = v | Vlist(((-10, 10),))
    assert w == Vlist(((-10, 10), (20, 30)))

    w = v | Vlist(((-10, 10), (20, 30)))
    assert w == Vlist(((-10, 10), (20, 30)))

    w = v | Vlist(((-10, 15),))
    assert w == Vlist(((-10, 15), (20, 30)))

    w = v | Vlist(((-10, 20),))
    assert w == Vlist(((-10, 30),))

    w = v | Vlist(((-10, 25),))
    assert w == Vlist(((-10, 30),))

    w = v | Vlist(((-10, 30),))
    assert w == Vlist(((-10, 30),))

    w = v | Vlist(((-10, 30),))
    assert w == Vlist(((-10, 30),))

    w = v | Vlist(((-10, 35),))
    assert w == Vlist(((-10, 35),))

    w = v | Vlist(((35, 40),))
    assert w == Vlist(((0, 10), (20, 30), (35, 40)))

    w = v | Vlist(((30, 40),))
    assert w == Vlist(((0, 10), (20, 40)))

    w = v | Vlist(((25, 40),))
    assert w == Vlist(((0, 10), (20, 40)))

    w = v | Vlist(((20, 40),))
    assert w == Vlist(((0, 10), (20, 40)))

    w = v | Vlist(((15, 40),))
    assert w == Vlist(((0, 10), (15, 40)))

    w = v | Vlist(((10, 40),))
    assert w == Vlist(((0, 40),))

    w = v | Vlist(((5, 40),))
    assert w == Vlist(((0, 40),))

    w = v | Vlist(((0, 40),))
    assert w == Vlist(((0, 40),))

    w = v | Vlist(((-10, 40),))
    assert w == Vlist(((-10, 40),))


def test_intersection1():
    v = Vlist(((None, 0),))
    w = Vlist(((0, None),))
    assert v & w == Vlist.empty()

    v = Vlist(((0, 10),))
    assert v & v == v
    assert v | v == v

    w = Vlist(((0, 20),))
    assert v & w == v
    assert v | w == w

    w = Vlist(((5, 15),))
    assert v & w == Vlist(((5, 10),))


def test_complement():
    for vs in vss:
        v = Vlist(vs)
        print()
        print(v)
        print(-v)
        assert v == --v


def test_empty():
    e = Vlist.empty()
    assert e == e
    assert not e != e
    assert 0 not in e
    assert 1 not in e
    for vs in vss:
        v = Vlist(vs)
        assert v == v | e
        assert e == v & e

def test_difference():
    e = Vlist.empty()
    for vs in vss:
        v = Vlist(vs)
        for ws in vss:
            w = Vlist(ws)
            assert (v - w) & (w - v) == e
            assert v - w - w == v - w
            assert w - v - v == w - v


def test_difference1():
    v = Vlist(((0, 10), (20, 30)))
    w = Vlist(((5, 20),))
    print()
    print(v - w)
    print(w - v)
#
#
def testHard():

    ts = [(a, a + 1) for a in range(0, 10000, 2)]
    vs = Vlist(ts)

    assert Vlist.all() == vs | -vs
    assert Vlist.empty() == vs & -vs

    ts = [(a, a + 1) for a in range(0, 10000, 1)]
    vs = Vlist(ts)

    assert Vlist.all() == vs | -vs
    assert Vlist.empty() == vs & -vs
