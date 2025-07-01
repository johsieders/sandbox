from __future__ import annotations

from typing import Any


class NativeComplex:

    def __init__(self, value: complex | NativeComplex):
        if isinstance(value, NativeComplex):
            self._value = value._value
        elif isinstance(value, complex):
            self._value = value
        else:
            raise TypeError(f"Complex can only wrap complex or Complex, got {type(value)}")

    def __add__(self, other: NativeComplex) -> NativeComplex:
        return NativeComplex(self._value + other._value)

    def __sub__(self, other: NativeComplex) -> NativeComplex:
        return NativeComplex(self._value - other._value)

    def __mul__(self, other: NativeComplex) -> NativeComplex:
        return NativeComplex(self._value * other._value)

    def __neg__(self) -> NativeComplex:
        return NativeComplex(-self._value)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, NativeComplex) and self._value == other._value

    def __floordiv__(self, other: NativeComplex) -> NativeComplex:
        return NativeComplex(self._value / other._value)

    def __mod__(self, other: NativeComplex) -> NativeComplex:
        return self.zero()

    def divmod(self, other: NativeComplex) -> tuple[NativeComplex, NativeComplex]:
        return (self / other, self.zero())

    def __truediv__(self, other: NativeComplex) -> NativeComplex:
        return NativeComplex(self._value / other._value)

    def inverse(self) -> NativeComplex:
        if self._value == 0:
            raise ZeroDivisionError("Complex.inverse(): division by zero")
        return NativeComplex(1 / self._value)

    def degree(self) -> float:
        return abs(self._value)

    def norm(self) -> float:
        return abs(self._value)

    @classmethod
    def zero(cls) -> NativeComplex:
        return cls(0 + 0j)

    @classmethod
    def one(cls) -> NativeComplex:
        return cls(1 + 0j)

    def to_complex(self) -> complex:
        return self._value

    def __str__(self) -> str:
        return str(self._value)

    def __repr__(self) -> str:
        return f"Complex({self._value})"
