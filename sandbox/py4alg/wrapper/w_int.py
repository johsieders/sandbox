from __future__ import annotations

import functools
from typing import Any

from sandbox.py4alg.util.primes import gcd


@functools.total_ordering
class NativeInt:

    def __init__(self, value: int | NativeInt):
        if isinstance(value, NativeInt):
            self._value = value._value
        elif isinstance(value, int):
            self._value = value
        else:
            raise TypeError(f"Int can only wrap int or Int, got {type(value)}")

    def __add__(self, other: NativeInt) -> NativeInt:
        return NativeInt(self._value + other._value)

    def __sub__(self, other: NativeInt) -> NativeInt:
        return NativeInt(self._value - other._value)

    def __mul__(self, other: NativeInt) -> NativeInt:
        return NativeInt(self._value * other._value)

    def __neg__(self) -> NativeInt:
        return NativeInt(-self._value)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, NativeInt) and self._value == other._value

    def __lt__(self, other: NativeInt) -> bool:
        return self._value < other._value

    def __floordiv__(self, other: NativeInt) -> NativeInt:
        return NativeInt(self._value // other._value)

    def __mod__(self, other: NativeInt) -> NativeInt:
        return NativeInt(self._value % other._value)

    def __divmod__(self, other: NativeInt) -> tuple[NativeInt, NativeInt]:
        q, r = divmod(self._value, other._value)
        return (NativeInt(q), NativeInt(r))

    def norm(self) -> int:
        return abs(self._value)

    def __bool__(self):
        return bool(self._value)

    def gcd(self, a: NativeInt) -> NativeInt:
        if isinstance(a, NativeInt):
            return NativeInt(gcd(self._value, a._value))
        else:
            raise TypeError("Expected NativeInt for gcd operation")

    @classmethod
    def zero(cls) -> NativeInt:
        return cls(0)

    @classmethod
    def one(cls) -> NativeInt:
        return cls(1)

    def to_int(self) -> int:
        return self._value

    def __str__(self) -> str:
        return str(self._value)

    def __repr__(self) -> str:
        return f"Int({self._value})"

    def descent(self):
        return [NativeInt]
