# KI-Gilde
# QAware GmbH, Munich
# 10.3.2021
# revived 17.10.2025

from collections.abc import Callable, Iterator
from torch import tensor


def conjoin(*gs: Callable) -> Iterator:
    """
    :param gs: list of Callables() -> Iterable
    :return: their cartesian product as iterator
    """
    values = [None] * len(gs)

    def loop(i):
        if i >= len(gs):
            yield list(values)
        else:
            for values[i] in gs[i]():
                yield from loop(i + 1)

    yield from loop(0)


def flatten_to_long(Y: tensor) -> tensor:
    """
    @param Y: target vector, size = (m, 1)
    @return: Y flattened to (m), cast to long
    """
    return Y.view(-1).long()
