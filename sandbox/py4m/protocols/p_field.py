from __future__ import annotations

from typing import Protocol, runtime_checkable, Any

from sandbox.py4m.protocols.p_euclidean_ring import EuclideanRing


@runtime_checkable
class Field(EuclideanRing, Protocol):
    def __truediv__(self, other: Any) -> Any: ...

    def inverse(self) -> Any: ...
