# tests/py4m/make_samples.py


from itertools import islice

from sandbox.py4m.util.g_samples import g_fractions, g_polynomials
from sandbox.py4m.util.g_samples import g_ints, g_floats, g_complex_, g_tuples, g_cycle
from sandbox.py4m.util.g_samples import g_nat_ints, g_nat_floats, g_nat_complex
from sandbox.py4m.util.utils import compose


def test_tuples():
    n = 10
    a = g_ints(0, 20)
    t = g_tuples(1, 2, a)
    assert len(list(islice(t, n))) == n


def test_g():
    n = 100
    assert len(list(islice(g_ints(0, 20), n))) == n
    assert len(list(islice(g_floats(0, 20), n))) == n
    assert len(list(islice(g_complex_(0, 20), n))) == n

    samples = [''] * 7
    samples[0] = g_nat_ints(g_ints(0, 20))
    samples[1] = g_fractions(g_nat_ints(g_ints(10, 20)))
    samples[2] = g_polynomials(g_fractions(g_nat_ints(g_ints(10, 20))))
    samples[3] = g_polynomials(g_fractions(g_nat_floats(g_floats(10, 20))))
    samples[4] = g_fractions(g_nat_floats(g_cycle((17.,))))
    samples[5] = g_polynomials(g_fractions(g_nat_floats(g_cycle((17.,)))))
    samples[6] = g_polynomials(g_fractions(g_nat_complex(g_cycle(((1. + 1j), (2. + 2j), (3. + 3j))))))

    for s in [s for s in samples if s != '']:
        assert len(list(islice(s, n))) == n


def test_compose():
    n = 10
    samples = [''] * 4
    samples[0] = compose(g_polynomials, g_fractions, g_nat_ints, g_ints)(10, 20)
    samples[1] = compose(g_fractions, g_polynomials, g_nat_floats, g_floats)(10., 20.)
    samples[2] = compose(g_fractions, g_fractions, g_fractions, g_nat_ints, g_ints)(10, 20)
    samples[3] = compose(g_fractions, g_fractions, g_nat_floats, g_floats)(10., 20.)

    for s in [s for s in samples if s != '']:
        assert len(list(islice(s, n))) == n
