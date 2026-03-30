# py4alg/tests/test_complex.py

import pytest

from sandbox.py4alg.util.gen_samples import (gen_ints, gen_floats, gen_complex_,
                                             gen_nat_complex, gen_nat_ints, gen_nat_floats,
                                             gen_field_complex, gen_fractions)
from sandbox.py4alg.util.utils import compose, take
from tests.py4alg.check_protocols import check_any


# ----- Type/sample groupings -----

def complex_samples(n: int):
    return (compose(take(n), gen_field_complex, gen_nat_complex, gen_complex_)(10, 20),
            compose(take(n), gen_field_complex, gen_nat_floats, gen_floats)(10, 20),
            compose(take(n), gen_field_complex, gen_field_complex, gen_nat_complex, gen_complex_)(10, 20),
            compose(take(n), gen_field_complex, gen_fractions, gen_nat_ints, gen_ints)(10, 20))


@pytest.mark.parametrize("samples", complex_samples(20))
def test_any(samples):
    check_any(samples)
