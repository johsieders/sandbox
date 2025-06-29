from __future__ import annotations

import functools
from typing import Any


# ----- Float -----
@functools.total_ordering
class NativeFloat:
    __slots__ = ("_value",)

    def __init__(self, value: float | NativeFloat):
        if isinstance(value, NativeFloat):
            self._value = value._value
        elif isinstance(value, float):
            self._value = value
        else:
            raise TypeError(f"Float can only wrap float or Float, got {type(value)}")

    def __add__(self, other: NativeFloat) -> NativeFloat:
        return NativeFloat(self._value + other._value)

    def __sub__(self, other: NativeFloat) -> NativeFloat:
        return NativeFloat(self._value - other._value)

    def __mul__(self, other: NativeFloat) -> NativeFloat:
        return NativeFloat(self._value * other._value)

    def __neg__(self) -> NativeFloat:
        return NativeFloat(-self._value)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, NativeFloat) and self._value == other._value

    def __lt__(self, other: NativeFloat) -> bool:
        return self._value < other._value

    def __floordiv__(self, other: NativeFloat) -> NativeFloat:
        return NativeFloat(self._value / other._value)  # Field: // as /

    def __mod__(self, other: NativeFloat) -> NativeFloat:
        return self.zero()

    def divmod(self, other: NativeFloat) -> tuple[NativeFloat, NativeFloat]:
        return (self / other, self.zero())

    def __truediv__(self, other: NativeFloat) -> NativeFloat:
        return NativeFloat(self._value / other._value)

    def inverse(self) -> NativeFloat:
        if self._value == 0.0:
            raise ZeroDivisionError("Float.inverse(): division by zero")
        return NativeFloat(1.0 / self._value)

    def degree(self) -> float:
        return abs(self._value)

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
