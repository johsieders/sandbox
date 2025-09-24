from __future__ import annotations

from sandbox.py4alg.mapper.m_complex import Complex
from sandbox.py4alg.mapper.m_fraction import Fraction
from sandbox.py4alg.mapper.m_matrix import Matrix
from sandbox.py4alg.mapper.m_polynomial import Polynomial
from sandbox.py4alg.wrapper.w_complex import NativeComplex
from sandbox.py4alg.wrapper.w_float import NativeFloat
from sandbox.py4alg.wrapper.w_int import NativeInt


class Mtype:
    N = 10
    R = 1
    E = 2
    F = 3


pt = {(NativeInt, Mtype.N): Mtype.E,
      (NativeFloat, Mtype.N): Mtype.F,
      (NativeComplex, Mtype.N): Mtype.F,
      (Complex, Mtype.F): Mtype.F,
      (Fraction, Mtype.R): Mtype.R,
      (Fraction, Mtype.E): Mtype.F,
      (Polynomial, Mtype.R): Mtype.R,
      (Polynomial, Mtype.F): Mtype.E,
      (Matrix, Mtype.R): Mtype.R,
      }


def successors(given: int):
    aux = []
    for (type, r) in pt.keys():
        if r == given:
            aux.append(pt[(type, r)])
    result = []
    for s in aux:
        for (type, r) in pt.keys():
            if r <= s:
                result.append(type)
    return set(result)


def test_pt():
    succ = successors(Mtype.E)
    print()
    print(succ)
