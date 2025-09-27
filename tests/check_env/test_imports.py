import numpy as np
import pandas as pd
import torch
from sklearn.ensemble import RandomForestClassifier
from sympy import *


def test_torch_np():
    cpu = torch.device('cpu')
    n = int(1e2)
    t_ones = torch.ones([n, n, n], dtype=torch.int32, device=cpu)
    n_ones = np.array(t_ones)
    s_ones = torch.from_numpy(n_ones)

    n3 = n ** 3
    assert t_ones.sum() == n3
    assert n_ones.sum() == n3
    assert s_ones.sum() == n3


def test_pandas():
    n = int(1e3)
    df = pd.DataFrame(np.random.rand(n, n))
    assert (len(df) == n)


def test_sklearn():
    clf = RandomForestClassifier(random_state=0)
    X = [[1, 2, 3],  # 2 samples, 3 features
         [11, 12, 13]]
    y = [0, 1]  # classes of each sample
    clf.fit(X, y)


def test_sympy():
    x, y = symbols('x y')
    expr = x + 2 * y
    print()
    print(expr)

    expr = diff(sin(x) * exp(x), x)
    print(expr)
