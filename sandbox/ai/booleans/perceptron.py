# KI-Gilde
# QAware GmbH, Munich
# 4.3.2021
# revived 17.10.2025

import torch
from torch import tensor, heaviside


class Perceptron(object):
    def __init__(self, n: int, lr: float, weight: tensor = None, bias: tensor = None):
        """
        :param n: dimension of x and w
        :param lr: learning rate
        :param weight: weight if given
        :param bias: bias if given
        """
        self.n = n
        self.bias = torch.rand(1) if bias is None else bias
        self.weight = torch.rand(n) if weight is None else weight
        self.lr = lr

    def predict(self, X: tensor) -> tensor:
        """
        same as applying _predict to all rows of X
        :param X: feature matrix, shape = (m, n)
        :return: prediction vector, shape = (m), values = 0 or 1
        """
        return heaviside(X.mv(self.weight) + self.bias, tensor(1.))

    def _predict(self, X: tensor) -> int:
        """
        :param X: feature vector, shape = (n)
        :return: prediction = 0 or 1
        """
        return 1 if X.matmul(self.weight) + self.bias >= 0 else 0

    def fit(self, X: tensor, Y: tensor, n_epochs=1) -> None:
        """
        fit weight and bias to X, Y
        :param X: feature matrix, shape = (m, n)
        :param Y: target vector, shape = (m), values = 0 or 1
        :return: None
        """
        for _ in range(n_epochs):
            for x, y in zip(X, Y):
                error = y - self._predict(x)  # error = -1, 0, or 1
                self.bias += self.lr * error
                self.weight += self.lr * error * x
