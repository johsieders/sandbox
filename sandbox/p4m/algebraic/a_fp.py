from __future__ import annotations

from typing import TypeVar

from sandbox.p4m.protocols.p_euclidean_ring import EuclideanRing
from sandbox.p4m.protocols.p_field import Field

T = TypeVar("T", bound=Field)

from typing import TypeVar, Generic

T = TypeVar("T", bound=EuclideanRing)


class Fp(Generic[T]):
    pass
