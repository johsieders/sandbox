# tests/py4m/make_samples.py

import random

params = {'rtol': 1e-9,
          'atol': 1e-12,
          'lower_bound': 10,
          'upper_bound': 20,
          'seed': 100,
          'min_norm': 1e-1,
          'no_zeros': False,
          'poly_min': 1,
          'poly_max': 5,
          'matrix_size': 9}


def test_seed():
    random.seed(params['seed'])

