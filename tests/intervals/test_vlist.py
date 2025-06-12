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
    w = Vlist([(1, 2)])

    print()
    print(v)
    x = v | w
    s = str(x)
    print(s)
    # assert w == v
    # assert w == v | w
    # assert v == v | w

    # w = v | Vlist([(1, 2)])
    # assert w == Vlist([(0, 2)])
    #
    # w = v | Vlist([(2, 3)])
    # assert w == Vlist([(0, 1), (2, 3)])


# def test_intersection():
#     v = Vlist((0, 10), (20, 30))
#     w = v & (-10, -5)
#     assert w == iv()
#
#     w = v.intersect((-10, 0))
#     assert w == iv()
#
#     w = v.intersect((-10, 5))
#     assert w == Vlist((0, 5))
#
#     w = v.intersect((-10, 10))
#     assert w == Vlist((0, 10))
#
#     w = v.intersect((-10, 15))
#     assert w == Vlist((0, 10))
#
#     w = v.intersect((-10, 20))
#     assert w == Vlist((0, 10))
#
#     w = v.intersect((-10, 25))
#     assert w == Vlist((0, 10), (20, 25))
#
#     w = v.intersect((-10, 30))
#     assert w == Vlist((0, 10), (20, 30))
#
#     w = v.intersect((-10, 35))
#     assert w == Vlist((0, 10), (20, 30))
#
#     ## untere Grenze wandert, obere Grenze fest
#     w = v.intersect((35, 40))
#     assert w == Vlist()
#
#     w = v.intersect((30, 40))
#     assert w == Vlist()
#
#     w = v.intersect((25, 40))
#     assert w == Vlist((25, 30))
#
#     w = v.intersect((20, 40))
#     assert w == Vlist((20, 30))
#
#     w = v.intersect((15, 40))
#     assert w, Vlist((20, 30))
#
#     w = v.intersect((10, 40))
#     assert w, Vlist((20, 30))
#
#     w = v.intersect((5, 40))
#     assert w == Vlist((5, 10), (20, 30))
#
#     w = v.intersect((0, 40))
#     assert w == Vlist((0, 10), (20, 30))
#
#     w = v.intersect((-10, 40))
#     assert w == Vlist((0, 10), (20, 30))
#

# def testAppend():
#     v = Vlist((0, 10), (20, 30))
#     v.append((-10, -5))
#     .failUnlessEqual(v, Vlist((-10, -5), (0, 10), (20, 30)))
#
#     v = Vlist((0, 10), (20, 30))
#     v.append((-10, 0))
#     .failUnlessEqual(v, Vlist((-10, 10), (20, 30)))
#
#     v = Vlist((0, 10), (20, 30))
#     v.append((-10, 5))
#     .failUnlessEqual(v, Vlist((-10, 10), (20, 30)))
#
#     v = Vlist((0, 10), (20, 30))
#     v.append((-10, 10))
#     .failUnlessEqual(v, Vlist((-10, 10), (20, 30)))
#
#     v = Vlist((0, 10), (20, 30))
#     v.append((-10, 15))
#     .failUnlessEqual(v, Vlist((-10, 15), (20, 30)))
#
#     v = Vlist((0, 10), (20, 30))
#     v.append((-10, 20))
#     .failUnlessEqual(v, Vlist((-10, 30)))
#
#     v = Vlist((0, 10), (20, 30))
#     v.append((-10, 25))
#     .failUnlessEqual(v, Vlist((-10, 30)))
#
#     v = Vlist((0, 10), (20, 30))
#     v.append((-10, 30))
#     .failUnlessEqual(v, Vlist((-10, 30)))
#
#     v = Vlist((0, 10), (20, 30))
#     v.append((-10, 35))
#     .failUnlessEqual(v, Vlist((-10, 35)))
#
#     ## untere Grenze wandert, obere Grenze fest
#     v = Vlist((0, 10), (20, 30))
#     v.append((35, 40))
#     .failUnlessEqual(v, Vlist((0, 10), (20, 30), (35, 40)))
#
#     v = Vlist((0, 10), (20, 30))
#     v.append((30, 40))
#     .failUnlessEqual(v, Vlist((0, 10), (20, 40)))
#
#     v = Vlist((0, 10), (20, 30))
#     v.append((25, 40))
#     .failUnlessEqual(v, Vlist((0, 10), (20, 40)))
#
#     v = Vlist((0, 10), (20, 30))
#     v.append((20, 40))
#     .failUnlessEqual(v, Vlist((0, 10), (20, 40)))
#
#     v = Vlist((0, 10), (20, 30))
#     v.append((15, 40))
#     .failUnlessEqual(v, Vlist((0, 10), (15, 40)))
#
#     v = Vlist((0, 10), (20, 30))
#     v.append((10, 40))
#     .failUnlessEqual(v, Vlist((0, 40)))
#
#     v = Vlist((0, 10), (20, 30))
#     v.append((5, 40))
#     .failUnlessEqual(v, Vlist((0, 40)))
#
#     v = Vlist((0, 10), (20, 30))
#     v.append((0, 40))
#     .failUnlessEqual(v, Vlist((0, 40)))
#
#     v = Vlist((0, 10), (20, 30))
#     v.append((-10, 40))
#     .failUnlessEqual(v, Vlist((-10, 40)))
#
#
# def testMake():
#     vs = Vlist()
#
#
#
# def testAnd():
#     v = Vlist((None, 0))
#     w = Vlist((0, None))
#     .failUnlessEqual(Vlist(), v & w)
#
#     v = Vlist((0, 10))
#     .failUnlessEqual(v, v & v)
#     .failUnlessEqual(+v, v & +v)
#
#     w = Vlist((0, 20))
#     .failUnlessEqual(v, v & w)
#     .failUnlessEqual(+v, v & +w)
#
#     w = Vlist((5, 15))
#     .failUnlessEqual(Vlist((5, 10)), v & w)
#     .failUnlessEqual(+Vlist((5, 10)), v & +w)
#
#
# def testUnion():
#     v = Vlist((0, 1))
#     w = Vlist((0, 1))
#     .failUnlessEqual(w, v | w)
#     .failUnlessEqual(w, w | v)
#
#     w = v | Vlist((1, 2))
#     .failUnlessEqual(w, Vlist((0, 2)))
#
#     w = v | Vlist((2, 3))
#     .failUnlessEqual(w, Vlist((0, 1), (2, 3)))
#
#
# def testDifference():
#     pass
#     v = Vlist((0, 4))
#     w = Vlist((2, 6))
#     .failUnlessEqual(v - w, Vlist((0, 2)))
#     .failUnlessEqual(w - v, Vlist((4, 6)))
#     .failUnlessEqual(v ^ w, (v - w) | (w - v))
#     .failUnlessEqual(v ^ w, (v | w) - (v & w))
#
#
# def testEmpty():
#     e = Vlist()
#     .failUnlessEqual(e, e)
#     .failUnless(not e < e)
#     .failUnlessEqual('', repr(e))
#     .failIf(-1 in e)
#     .failIf(0 in e)
#     .failIf(1 in e)
#
#
# def testHard():
#     vs = Vlist(*[(a, a + 10) for a in range(0, 1000, 20)])
#     .failUnlessEqual(500, vs.sum())
#     .failUnlessEqual(Vlist((None, None)), vs | -vs)
#     .failUnlessEqual(Vlist(), vs & -vs)
#
#
# def testHarder():
#     vs = Vlist(*[(a, a + 1) for a in range(N)])
#     .failUnlessEqual(Vlist((None, None)), vs | -vs)
#     .failUnlessEqual(Vlist(), vs & -vs)
