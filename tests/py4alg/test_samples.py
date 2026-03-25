# tests/py4alg/make_samples.py


from itertools import islice

from sandbox.py4alg.util.gen_samples import gen_fractions, gen_matrices, gen_polynomials, gen_field_polynomials
from sandbox.py4alg.util.gen_samples import gen_ints, gen_floats, gen_complex_, gen_tuples, gen_cycle
from sandbox.py4alg.util.gen_samples import gen_nat_ints, gen_nat_floats, gen_nat_complex
from sandbox.py4alg.util.utils import compose, take
from sandbox.py4alg.wrapper.w_int import NativeInt


def test_cycle():
    cs = gen_cycle((1, 0, -1))
    ds = take(5)(gen_nat_ints(cs))

    es = compose(take(5), gen_nat_ints, gen_cycle)((1, 0, -1))
    diff = [c - d for c, d in zip(ds, es)]
    assert sum(diff, NativeInt(0)) == NativeInt(0)


def test_tuples():
    n = 10
    a = gen_ints(0, 20)
    t = gen_tuples(1, 2, a)
    assert len(list(islice(t, n))) == n


def test_g():
    n = 100
    assert len(list(islice(gen_ints(0, 20), n))) == n
    assert len(list(islice(gen_floats(0, 20), n))) == n
    assert len(list(islice(gen_complex_(0, 20), n))) == n

    samples = [''] * 7
    samples[0] = gen_nat_ints(gen_ints(0, 20))
    samples[1] = gen_fractions(gen_nat_ints(gen_ints(10, 20)))
    samples[2] = gen_polynomials(gen_fractions(gen_nat_ints(gen_ints(10, 20))))
    samples[3] = gen_polynomials(gen_fractions(gen_nat_floats(gen_floats(10, 20))))
    samples[4] = gen_fractions(gen_nat_floats(gen_cycle((17.,))))
    samples[5] = gen_polynomials(gen_fractions(gen_nat_floats(gen_cycle((17.,)))))
    samples[6] = gen_polynomials(gen_fractions(gen_nat_complex(gen_cycle(((1. + 1j), (2. + 2j), (3. + 3j))))))

    for s in [s for s in samples if s != '']:
        assert len(list(islice(s, n))) == n


def test_compose():
    n = 10
    samples = [''] * 4
    samples[0] = compose(gen_polynomials, gen_fractions, gen_nat_ints, gen_ints)(10, 20)
    samples[1] = compose(gen_fractions, gen_field_polynomials, gen_nat_floats, gen_floats)(10, 20)
    samples[2] = compose(gen_fractions, gen_fractions, gen_fractions, gen_nat_ints, gen_ints)(10, 20)
    samples[3] = compose(gen_fractions, gen_fractions, gen_nat_floats, gen_floats)(10, 20)

    for s in [s for s in samples if s != '']:
        assert len(list(islice(s, n))) == n
