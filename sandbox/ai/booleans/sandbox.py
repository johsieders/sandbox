
# KI-Gilde
# QAware GmbH, Munich
# 25.3.2021
# revived 17.10.2025

import unittest

import torch
import torch.nn as nn
from torch import tensor

X_in = [[0, 0], [0, 1], [1, 0], [1, 1]]
Y_in = [0, 1, 1, 1]  # OR
Y_onehot = [[1, 0], [0, 1], [0, 1], [0, 1]]   # one hot version of Y_in

class moduleTest(unittest.TestCase):
    def test_reg21(self):
        F = nn.Sequential(nn.Linear(2, 1), nn.Sigmoid())
        d1 = {'0.weight': tensor([[0., 0.]]), '0.bias': tensor([1.])}
        F.load_state_dict(d1)

        d2 = F.state_dict()
        print()
        for k, v in d2.items():
            print(k, v)

        print('\n Parameters:\n', list(F.parameters()))

        loss_fct = nn.MSELoss()
        optimizer = torch.optim.Adam(F.parameters(), lr=1e-0)

        X = tensor(X_in, requires_grad=True, dtype=torch.float32)  # tensor[float](4, 2)
        Y_t = tensor(Y_in, dtype=torch.float32).view(-1, 1)     # tensor[float](4, 1)
        Y = F(X)                                                # tensor[float](4, 1)
        loss = loss_fct(Y, Y_t)                                 # tensor[float](0)
        print(loss)
        loss.backward()
        optimizer.step()
        Y_p = torch.round(Y)                                    # tensor[float](4, 1)
        print('\n', Y_p)

    def test_clf21(self):
        F = nn.Linear(2, 1)
        d1 = {'weight': tensor([[0., 0.]]), 'bias': tensor([1.])}
        F.load_state_dict(d1)

        loss_fct = nn.BCEWithLogitsLoss()
        optimizer = torch.optim.Adam(F.parameters(), lr=1e-0)
        X = tensor(X_in, requires_grad=True, dtype=torch.float32)  # tensor[float](4, 2)
        Y_t = tensor(Y_in, dtype=torch.float32).view(-1, 1)     # tensor[float](4, 1)

        Y = F(X)                                                # tensor[float](4, 1)
        loss = loss_fct(Y, Y_t)                                 # tensor[float](0)
        loss.backward()
        optimizer.step()

        Y_p = torch.heaviside(Y, torch.zeros(1))                # tensor[float](4, 1)
        print(Y_p)

    def test_clf22(self):
        F = nn.Linear(2, 2)
        d1 = {'weight': tensor([[0., 0.], [0., 0.]]), 'bias': tensor([1., 1.])}
        F.load_state_dict(d1)

        loss_fct = nn.CrossEntropyLoss()
        X = tensor(X_in, dtype=torch.float32)                  # tensor[float](4, 2)
        Y_t = tensor(Y_in, dtype=torch.long)                     # tensor[long](4)
        Y = F(X)                                              # tensor[float](4, 2)
        loss = loss_fct(Y, Y_t)                                 # tensor[float](0)
        print(loss)

        Y_p = torch.argmax(Y, dim=1).view(-1, 1)              # tensor[int](4, 1)
        print(Y_p)
