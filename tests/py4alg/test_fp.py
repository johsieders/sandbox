# py4alg/tests/test_fp.py

import pytest

from sandbox.py4alg.mapper.m_fp import Fp
from sandbox.py4alg.protocols.p_abelian_group import AbelianGroup
from sandbox.py4alg.protocols.p_comparable import Comparable
from sandbox.py4alg.protocols.p_euclidean_ring import EuclideanRing
from sandbox.py4alg.protocols.p_field import Field
from sandbox.py4alg.util.primes import get_primes
from tests.py4alg.check_properties import check_euclidean_rings, check_fields


# ----- Type/sample groupings -----

def test_isinstance():
    n = Fp(7, 3)
    assert isinstance(n, Fp)
    assert isinstance(n, Comparable)
    assert isinstance(n, AbelianGroup)
    assert isinstance(n, EuclideanRing)
    assert isinstance(n, Field)


def fp_samples():
    primes = list(get_primes(30))
    samples = []
    for p in primes:
        samples.append([Fp(p, a) for a in range(2 * p)])
    return samples


@pytest.mark.parametrize("samples", fp_samples())
def test_euclidean_rings(samples):
    check_euclidean_rings(samples)


@pytest.mark.parametrize("samples", fp_samples())
def test_fields(samples):
    check_fields(samples)
