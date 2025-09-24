from __future__ import annotations

from typing import Protocol, runtime_checkable, Any

from sandbox.py4alg.protocols.p_ring import Ring


@runtime_checkable
class EuclideanRing(Ring, Protocol):
    def __floordiv__(self, other: Any) -> Any: ...

    def __mod__(self, other: Any) -> Any: ...

    def __divmod__(self, other: Any) -> tuple[Any, Any]: ...

    def degree(self) -> int: ...
