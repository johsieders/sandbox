# tests/py4alg/make_samples.py

import random

params = {'rtol': 1e-9,
          'atol': 1e-12,
          'lower_bound': 10,
          'upper_bound': 20,
          'seed': 100,
          'min_norm': 0,
          'no_zeros': False,
          'poly_min': 1,
          'poly_max': 5,
          'matrix_size': 9}


def set_test_seed():
    """
    run this before each test session to get identical results
    """
    random.seed(params['seed'])

# def functor_result(functor: Callable[[Any], Any], algtype: AlgType=None) -> AlgType:
#     tt = {(Matrix, AlgType.Ring): AlgType.Ring,
#           (Matrix, AlgType.CommutativeRing): AlgType.Ring,
#           (Matrix, AlgType.EuclideanRing): AlgType.Ring,
#           (Matrix, AlgType.Field): AlgType.Ring,
#           (Complex, AlgType.Ring): AlgType.Ring,
#           (Complex, AlgType.CommutativeRing): AlgType.CommuntativeRing,
#           (Complex, AlgType.EuclideanRing): AlgType.EuclideanRing,
#           (Complex, AlgType.Field): AlgType.Field,
#           (Fp, AlgType.EuclideanRing): AlgType.Field,
#           (Fp, AlgType.Field): AlgType.Field
#           }
#     return tt[functor, algtype]
