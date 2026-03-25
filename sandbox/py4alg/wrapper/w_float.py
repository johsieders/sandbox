from __future__ import annotations

import functools
from typing import Any

from sandbox.py4alg.cockpit import params


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
                and abs(self._value - other._value) <= params['atol'] + params['rtol'] * max(abs(self._value), abs(other._value)))

    def __lt__(self, other: NativeFloat) -> bool:
        return self._value < other._value

    def __truediv__(self, other: NativeFloat) -> NativeFloat:
        if not other:
            raise ZeroDivisionError("Float.__truediv__(): division by zero")
        return NativeFloat(self._value / other._value)

    def __floordiv__(self, other: NativeFloat) -> NativeFloat:
        return NativeFloat(self._value / other._value)  # Field: // as /

    def __mod__(self, other: NativeFloat) -> NativeFloat:
        return self.zero()

    def __divmod__(self, other: NativeFloat) -> tuple[NativeFloat, NativeFloat]:
        return self / other, self.zero()

    def inverse(self) -> NativeFloat:
        return NativeFloat(1.0 / self._value)

    def __bool__(self) -> bool:
        return not self == self.zero()

    def euclidean_function(self) -> int:
        if not self:
            raise ValueError("euclidean_function is undefined on zero")
        return 1

    def normalize(self) -> NativeFloat:
        return self.one() if self else self.zero()

    @classmethod
    def zero(cls) -> NativeFloat:
        return cls(0.0)

    @classmethod
    def one(cls) -> NativeFloat:
        return cls(1.0)

    def __str__(self) -> str:
        return str(self._value)

    def __repr__(self) -> str:
        return f"Float({self._value})"

    def descent(self):
        return [NativeFloat]
