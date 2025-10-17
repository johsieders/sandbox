# KI-Gilde
# QAware GmbH, Munich
# 10.3.2021
# revived 17.10.2025

from collections.abc import Callable

import torch
from torch import tensor, heaviside


def circle(radius: float) -> Callable:
    """
    @param radius: radius of a circle with center = origin
    @return: f such that f(X) is a tensor which indicates which rows of X are inside the circle
    """

    def f(X: tensor) -> tensor:
        """
        @param X: size = (m, n)
        @return: tensor of 0 and 1: 1 if xi is inside the circle
        """
        # X.norm(2) is the Euclidean norm
        return tensor([1. if x.norm(2) <= radius else 0. for x in X]).view(-1, 1)

    return f


def rings(radius: float) -> Callable:
    """
    @param radius: radius of a circle with center = origin
    @return: f such that f(X) is a tensor which indicates which rows of X are inside a ring
    """

    def f(X: tensor) -> tensor:
        """
        @param X: size = (m, n)
        @return: tensor of 0 and 1: 1 if xi is inside a ring
        """
        # X.norm(2) is the Euclidean norm
        return tensor([1 - (x.norm(2) // radius) % 2 for x in X]).view(-1, 1)

    return f


def square(length: float) -> Callable:
    """
    @param length: half the side length of a square with center = origin
    @return: f such that f(X) is a tensor that indicates which rows of X are inside the square
    """
    def f(X: tensor) -> tensor:
        """
        @param X: size = (m, n)
        @return: tensor of 0 and 1: 1 if xi is inside the square
        """
        # X.norm(float('inf') is the maximum norm
        # return 1 if X.norm(float('inf')) <= length else 0
        return tensor([1. if x.norm(float('inf')) <= length else 0. for x in X]).view(-1, 1)

    return f


def plane(weight: list, bias: float) -> Callable:
    """
    weight and bias define a hyperplane in R^n
    @param weight: tensor of size = (n)
    @param bias: a float
    @return: f such that f(X) = 1 if X on or above given plane
    """
    weight = tensor(weight, dtype=torch.float)
    bias = tensor(bias, dtype=torch.float)

    def f(X: tensor) -> tensor:
        """
        @param X: size = (m, n), n same as weight
        @return: tensor of 0 and 1: 0 if xi below plane, else 1; size = (m, 1)
        """
        return heaviside(X.mv(weight) + bias, tensor(1.)).view(-1, 1)

    return f


# Native boolean functions cannot be applied to torch tensors.
# But these functions can.

def _and(X: tensor) -> tensor:
    """
    @param X: size = (m, 2)
    :return: xor(X[0], X[1]) by row, size = (m, 1)
    """
    return (X[:, 0] * X[:, 1]).view(-1, 1)


def _or(X: tensor) -> tensor:
    """
    @param X: size = (m, 2)
    :return: xor(X[0], X[1]) by row, size = (m, 1)
    """
    return (X[:, 0] + X[:, 1] - X[:, 0] * X[:, 1]).view(-1, 1)


def _xor(X: tensor) -> tensor:
    """
    @param X: size = (m, 2)
    :return: xor(X[0], X[1]), size = (m, 1)
    """
    return (X[:, 0] + X[:, 1] - 2 * X[:, 0] * X[:, 1]).view(-1, 1)


if __name__ == '__main__':
    x = (0, 0, 0, 1, 1, 0, 1, 1)
    X = tensor(x, dtype=torch.float32).view(-1, 2)

    print()
    print(_and(X))
    print(_or(X))
    print(_xor(X))

    f_and = plane([1, 1], -1.5)    # and
    f_or = plane([1, 1], -0.5)     # or

    u = f_and(X)
    v = f_or(X)

    c = circle(1)
    a = c(X)
    s = square(1)
    b = s(X)

    r = rings(1)
    x = (0, 0, 0, 0.5, 0, 1, 0, 1.5, 0, 2)
    X = tensor(x, dtype=torch.float32).view(-1, 2)
    Y = r(X)
