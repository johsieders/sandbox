from __future__ import annotations

from typing import Any

from sandbox.py4alg.cockpit import params


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
        return (isinstance(other, NativeComplex)
                and abs(self._value - other._value) <= params['atol'] + params['rtol'] * max(abs(self._value), abs(other._value)))

    def __truediv__(self, other: NativeComplex) -> NativeComplex:
        if not other:
            raise ZeroDivisionError("Complex.__truediv__(): division by zero")
        return NativeComplex(self._value / other._value)

    def __floordiv__(self, other: NativeComplex) -> NativeComplex:
        return NativeComplex(self._value / other._value)

    def __mod__(self, other: NativeComplex) -> NativeComplex:
        return self.zero()

    def __divmod__(self, other: NativeComplex) -> tuple[NativeComplex, NativeComplex]:
        return self / other, self.zero()

    def inverse(self) -> NativeComplex:
        return NativeComplex(1 / self._value)

    def normalize(self) -> NativeComplex:
        return self.one() if self else self.zero()

    def __bool__(self) -> bool:
        return not self == self.zero()

    def euclidean_function(self) -> int:
        if not self:
            raise ValueError("euclidean_function is undefined on zero")
        return 1

    @classmethod
    def zero(cls) -> NativeComplex:
        return cls(0 + 0j)

    @classmethod
    def one(cls) -> NativeComplex:
        return cls(1 + 0j)

    def __str__(self) -> str:
        return str(self._value)

    def __repr__(self) -> str:
        return f"Complex({self._value})"

    def descent(self):
        return [NativeComplex]
