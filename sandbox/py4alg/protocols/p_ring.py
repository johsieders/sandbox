from __future__ import annotations

from typing import Protocol, runtime_checkable, Any

from sandbox.py4alg.protocols.p_abelian_group import AbelianGroup


@runtime_checkable
class Ring(AbelianGroup, Protocol):
    def __mul__(self, other: Any) -> Any: ...

    def one(self) -> Any: ...
