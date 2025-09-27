from __future__ import annotations

from typing import Protocol, runtime_checkable, Any


@runtime_checkable
class Comparable(Protocol):

    def __lt__(self, other: Any) -> bool: ...
