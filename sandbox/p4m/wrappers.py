from __future__ import annotations
import functools
from typing import Any

# ----- Int -----
@functools.total_ordering
class IntNative:
    __slots__ = ("_value",)

    def __init__(self, value: int | IntNative):
        if isinstance(value, IntNative):
            self._value = value._value
        elif isinstance(value, int):
            self._value = value
        else:
            raise TypeError(f"Int can only wrap int or Int, got {type(value)}")

    def __add__(self, other: IntNative) -> IntNative:
        return IntNative(self._value + other._value)

    def __sub__(self, other: IntNative) -> IntNative:
        return IntNative(self._value - other._value)

    def __mul__(self, other: IntNative) -> IntNative:
        return IntNative(self._value * other._value)

    def __neg__(self) -> IntNative:
        return IntNative(-self._value)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, IntNative) and self._value == other._value

    def __lt__(self, other: IntNative) -> bool:
        return self._value < other._value

    def __floordiv__(self, other: IntNative) -> IntNative:
        return IntNative(self._value // other._value)

    def __mod__(self, other: IntNative) -> IntNative:
        return IntNative(self._value % other._value)

    def divmod(self, other: IntNative) -> tuple[IntNative, IntNative]:
        q, r = divmod(self._value, other._value)
        return (IntNative(q), IntNative(r))

    def degree(self) -> int:
        return abs(self._value)

    def norm(self) -> int:
        return abs(self._value)

    def gcd(self, other: IntNative) -> IntNative:
        a, b = abs(self._value), abs(other._value)
        while b != 0:
            a, b = b, a % b
        return IntNative(a)

    @classmethod
    def zero(cls) -> IntNative:
        return cls(0)

    @classmethod
    def one(cls) -> IntNative:
        return cls(1)

    def to_int(self) -> int:
        return self._value

    def __str__(self) -> str:
        return str(self._value)

    def __repr__(self) -> str:
        return f"Int({self._value})"

# ----- Float -----
@functools.total_ordering
class FloatNative:
    __slots__ = ("_value",)

    def __init__(self, value: float | FloatNative):
        if isinstance(value, FloatNative):
            self._value = value._value
        elif isinstance(value, float):
            self._value = value
        else:
            raise TypeError(f"Float can only wrap float or Float, got {type(value)}")

    def __add__(self, other: FloatNative) -> FloatNative:
        return FloatNative(self._value + other._value)

    def __sub__(self, other: FloatNative) -> FloatNative:
        return FloatNative(self._value - other._value)

    def __mul__(self, other: FloatNative) -> FloatNative:
        return FloatNative(self._value * other._value)

    def __neg__(self) -> FloatNative:
        return FloatNative(-self._value)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, FloatNative) and self._value == other._value

    def __lt__(self, other: FloatNative) -> bool:
        return self._value < other._value

    def __floordiv__(self, other: FloatNative) -> FloatNative:
        return FloatNative(self._value / other._value)  # Field: // as /

    def __mod__(self, other: FloatNative) -> FloatNative:
        return self.zero()

    def divmod(self, other: FloatNative) -> tuple[FloatNative, FloatNative]:
        return (self / other, self.zero())

    def __truediv__(self, other: FloatNative) -> FloatNative:
        return FloatNative(self._value / other._value)

    def inverse(self) -> FloatNative:
        if self._value == 0.0:
            raise ZeroDivisionError("Float.inverse(): division by zero")
        return FloatNative(1.0 / self._value)

    def degree(self) -> float:
        return abs(self._value)

    def norm(self) -> float:
        return abs(self._value)

    @classmethod
    def zero(cls) -> FloatNative:
        return cls(0.0)

    @classmethod
    def one(cls) -> FloatNative:
        return cls(1.0)

    def to_float(self) -> float:
        return self._value

    def __str__(self) -> str:
        return str(self._value)

    def __repr__(self) -> str:
        return f"Float({self._value})"

# ----- Complex -----
class ComplexNative:
    __slots__ = ("_value",)

    def __init__(self, value: complex | ComplexNative):
        if isinstance(value, ComplexNative):
            self._value = value._value
        elif isinstance(value, complex):
            self._value = value
        else:
            raise TypeError(f"Complex can only wrap complex or Complex, got {type(value)}")

    def __add__(self, other: ComplexNative) -> ComplexNative:
        return ComplexNative(self._value + other._value)

    def __sub__(self, other: ComplexNative) -> ComplexNative:
        return ComplexNative(self._value - other._value)

    def __mul__(self, other: ComplexNative) -> ComplexNative:
        return ComplexNative(self._value * other._value)

    def __neg__(self) -> ComplexNative:
        return ComplexNative(-self._value)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, ComplexNative) and self._value == other._value

    def __floordiv__(self, other: ComplexNative) -> ComplexNative:
        return ComplexNative(self._value / other._value)

    def __mod__(self, other: ComplexNative) -> ComplexNative:
        return self.zero()

    def divmod(self, other: ComplexNative) -> tuple[ComplexNative, ComplexNative]:
        return (self / other, self.zero())

    def __truediv__(self, other: ComplexNative) -> ComplexNative:
        return ComplexNative(self._value / other._value)

    def inverse(self) -> ComplexNative:
        if self._value == 0:
            raise ZeroDivisionError("Complex.inverse(): division by zero")
        return ComplexNative(1 / self._value)

    def degree(self) -> float:
        return abs(self._value)

    def norm(self) -> float:
        return abs(self._value)

    @classmethod
    def zero(cls) -> ComplexNative:
        return cls(0 + 0j)

    @classmethod
    def one(cls) -> ComplexNative:
        return cls(1 + 0j)

    def to_complex(self) -> complex:
        return self._value

    def __str__(self) -> str:
        return str(self._value)

    def __repr__(self) -> str:
        return f"Complex({self._value})"
