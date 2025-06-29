from __future__ import annotations

from typing import Protocol, runtime_checkable, Any

from sandbox.p4m.protocols.p_ring import Ring


@runtime_checkable
class EuclideanRing(Ring, Protocol):
    def __floordiv__(self, other: Any) -> Any: ...

    def __mod__(self, other: Any) -> Any: ...

    def divmod(self, other: Any) -> tuple[Any, Any]: ...

    def degree(self) -> int: ...
