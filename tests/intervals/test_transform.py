# js 07.06.2025

# testing transformations from list of intervals to list of timestamps and back

from sandbox.intervals.vlist import vlist2timestamps, timestamps2vlist


tss = [
    [(None, False), (0, True), (10, False), (20, True), (30, False)],
    [(None, False), (5, True), (15, False), (25, True), (35, False)],
    [(None, True), (50, False), (100, True)],
    [(None, True)],
    [(None, True), (30, False)],
    [(None, False), (30, True)]
    ]

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

def test_vs2ts():
    for vs in vss:
        ts = vlist2timestamps(vs)
        ws = timestamps2vlist(ts)
        assert ws == vs

def test_ts2vs():
    for ts in tss:
        vs = timestamps2vlist(ts)
        zs = vlist2timestamps(vs)
        assert ts == zs
