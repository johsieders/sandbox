# py4alg/tests/test_fp.py

import pytest

from sandbox.py4alg.mapper.m_fp import Fp, Zm
from sandbox.py4alg.protocols.p_abelian_group import AbelianGroup
from sandbox.py4alg.protocols.p_comparable import Comparable
from sandbox.py4alg.protocols.p_euclidean_ring import EuclideanRing
from sandbox.py4alg.protocols.p_field import Field
from sandbox.py4alg.protocols.p_ring import Ring
from sandbox.py4alg.util.primes import get_primes
from tests.py4alg.check_properties import check_euclidean_rings, check_fields


# ----- Type/sample groupings -----

def test_isinstance():
    n = Fp(7, 3)
    assert isinstance(n, Fp)
    assert isinstance(n, Zm)  # Test inheritance
    assert isinstance(n, Comparable)
    assert isinstance(n, AbelianGroup)
    assert isinstance(n, Ring)
    assert isinstance(n, EuclideanRing)
    assert isinstance(n, Field)


def test_inheritance():
    # Test that Fp is properly inheriting from Zm
    fp = Fp(7, 3)
    assert isinstance(fp, Zm)

    # Test that operations return the correct type
    fp2 = Fp(7, 4)
    result = fp + fp2
    assert isinstance(result, Fp)
    assert not isinstance(result, Zm) or isinstance(result, Fp)  # Fp is subclass of Zm

    # Test that p property works (specific to Fp)
    assert fp.p == 7
    # Test that m property works (inherited from Zm)
    assert fp.m == 7


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
