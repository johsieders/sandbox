from __future__ import annotations

import functools
from typing import Any

from sandbox.py4alg.util.utils import close_to


@functools.total_ordering
class NativeFloat:

    def __init__(self, value: float | NativeFloat):
        if isinstance(value, NativeFloat):
            self._value = value._value
        elif isinstance(value, float):
            self._value = value

    def __add__(self, other: NativeFloat) -> NativeFloat:
        return NativeFloat(self._value + other._value)

    def __sub__(self, other: NativeFloat) -> NativeFloat:
        return NativeFloat(self._value - other._value)

    def __mul__(self, other: NativeFloat) -> NativeFloat:
        return NativeFloat(self._value * other._value)

    def __neg__(self) -> NativeFloat:
        return NativeFloat(-self._value)

    def __eq__(self, other: Any) -> bool:
        return (isinstance(other, NativeFloat)
                and close_to(self._value, other._value))

    def __lt__(self, other: NativeFloat) -> bool:
        return self._value < other._value

    def __floordiv__(self, other: NativeFloat) -> NativeFloat:
        return NativeFloat(self._value / other._value)  # Field: // as /

    def __mod__(self, other: NativeFloat) -> NativeFloat:
        return self.zero()

    def __divmod__(self, other: NativeFloat) -> tuple[NativeFloat, NativeFloat]:
        return (self / other, self.zero())

    def __truediv__(self, other: NativeFloat) -> NativeFloat:
        return NativeFloat(self._value / other._value)

    def inverse(self) -> NativeFloat:
        if close_to(self._value, 0.0):
            raise ZeroDivisionError("Float.inverse(): division by zero")
        return NativeFloat(1.0 / self._value)

    def gcd(self, a: NativeFloat) -> NativeFloat:
        return self.one() if (self or a) else self.zero()

    def __bool__(self) -> bool:
        return bool(self._value)

    def norm(self) -> float:
        return abs(self._value)

    @classmethod
    def zero(cls) -> NativeFloat:
        return cls(0.0)

    @classmethod
    def one(cls) -> NativeFloat:
        return cls(1.0)

    def to_float(self) -> float:
        return self._value

    def __str__(self) -> str:
        return str(self._value)

    def __repr__(self) -> str:
        return f"Float({self._value})"

    def descent(self):
        return [NativeFloat]
