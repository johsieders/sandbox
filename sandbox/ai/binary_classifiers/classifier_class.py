# KI-Gilde
# QAware GmbH, Munich
# 10.3.2021
# revived 17.10.2025


from collections.abc import Callable

import torch
import torch.nn as nn
from torch import Tensor


class Classifier(object):
    def __init__(self,
                 M: nn.Module,
                 optimizer: torch.optim.Optimizer,
                 loss_fct: Callable[[Tensor, Tensor], Tensor],
                 pred_fct: Callable[[Tensor], Tensor],
                 prepare_fct: Callable[[Tensor], Tensor] | None = None):
        """
        @param M: a torch module
        @param optimizer: an optimizer
        @param loss_fct: a loss function
        @param pred_fct: transforms the result of M into a prediction
        @param prepare_fct: transforms Y in a format suitable for M
        """
        self.M = M
        self.optimizer = optimizer
        self.loss_fct = loss_fct
        self.pred_fct = pred_fct
        self.prepare_function = prepare_fct

    def fit(self,
            X: Tensor,
            Y: Tensor,
            n_epochs: int = 1) -> list[float]:
        """
        @param X: feature matrix, size = (m, n)
        @param Y: target vector, size = (m, 1)
        @param n_epochs: a number >= 1
        @return: protocol of losses
        """
        if self.prepare_function is not None:
            Y = self.prepare_function(Y)
        cnt = 0
        history = []

        while cnt < n_epochs:
            loss = self.loss_fct(self.M(X), Y)
            history.append(loss.item())
            loss.backward()
            self.optimizer.step()
            self.optimizer.zero_grad()
            cnt += 1

        return history

    def predict(self, X: Tensor) -> Tensor:
        """
        @param X: feature matrix, size = (m, n)
        @return: prediction Y, size = (m, 1)
        """
        return self.pred_fct(self.M(X))
