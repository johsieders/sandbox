from __future__ import annotations

from typing import Protocol, runtime_checkable, Any

from sandbox.py4alg.protocols.p_abelian_group import AbelianGroup


@runtime_checkable
class Ring(AbelianGroup, Protocol):
    def __add__(self, other: Any) -> Any: ...

    def __sub__(self, other: Any) -> Any: ...

    def __neg__(self) -> Any: ...

    def zero(self) -> Any: ...
