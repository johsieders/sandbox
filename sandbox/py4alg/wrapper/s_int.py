from __future__ import annotations

from typing import Any

from sympy import Symbol, Abs, S
from sympy.core.numbers import igcd


class SymbolicInt:

    def __init__(self, value: str | Symbol | SymbolicInt):
        if isinstance(value, str):
            self._value = Symbol(value, integer=True)
        elif isinstance(value, Symbol):
            self._value = Symbol(str(value), integer=True)
        elif isinstance(value, SymbolicInt):
            self._value = value._value
        else:
            raise TypeError(f"SymbolicInt can only wrap Symbol or SymbolicInt, got {type(value)}")

    def __add__(self, other: SymbolicInt) -> SymbolicInt:
        return SymbolicInt(self._value + other._value)

    def __sub__(self, other: SymbolicInt) -> SymbolicInt:
        return SymbolicInt(self._value - other._value)

    def __mul__(self, other: SymbolicInt) -> SymbolicInt:
        return SymbolicInt(self._value * other._value)

    def __neg__(self) -> SymbolicInt:
        return SymbolicInt(-self._value)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, SymbolicInt) and self._value == other._value

    def __lt__(self, other: SymbolicInt) -> bool:
        return self._value < other._value

    def __floordiv__(self, other: SymbolicInt) -> SymbolicInt:
        return SymbolicInt(self._value // other._value)

    def __mod__(self, other: SymbolicInt) -> SymbolicInt:
        return SymbolicInt(self._value % other._value)

    def __divmod__(self, other: SymbolicInt) -> tuple[SymbolicInt, SymbolicInt]:
        q, r = divmod(self._value, other._value)
        return (SymbolicInt(q), SymbolicInt(r))

    def norm(self) -> Abs:
        return Abs(self._value)

    def __bool__(self):
        return bool(self._value)

    def gcd(self, a: SymbolicInt) -> SymbolicInt:
        if isinstance(a, SymbolicInt):
            return SymbolicInt(igcd(self._value, a._value))
        else:
            raise TypeError("Expected SymbolInt for gcd operation")

    @classmethod
    def zero(cls) -> SymbolicInt:
        return SymbolicInt(S.Zero)

    @classmethod
    def one(cls) -> SymbolicInt:
        return SymbolicInt(S.One)

    def to_symbol(self) -> Symbol:
        return self._value

    def __str__(self) -> str:
        return str(self._value)

    def __repr__(self) -> str:
        return f"Int({self._value})"

    def descent(self):
        return [SymbolicInt]
