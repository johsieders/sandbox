from __future__ import annotations

from typing import Any

from sympy import Symbol, Abs, S
from sympy.core.numbers import igcd


class SymbolInt:

    def __init__(self, value: str | Symbol | SymbolInt):
        if isinstance(value, str):
            self._value = Symbol(value, integer=True)
        elif isinstance(value, Symbol):
            self._value = Symbol(str(value), integer=True)
        elif isinstance(value, SymbolInt):
            self._value = value._value
        else:
            raise TypeError(f"SymbolInt can only wrap Symbol or SymbolInt, got {type(value)}")

    def __add__(self, other: SymbolInt) -> SymbolInt:
        return SymbolInt(self._value + other._value)

    def __sub__(self, other: SymbolInt) -> SymbolInt:
        return SymbolInt(self._value - other._value)

    def __mul__(self, other: SymbolInt) -> SymbolInt:
        return SymbolInt(self._value * other._value)

    def __neg__(self) -> SymbolInt:
        return SymbolInt(-self._value)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, SymbolInt) and self._value == other._value

    def __lt__(self, other: SymbolInt) -> bool:
        return self._value < other._value

    def __floordiv__(self, other: SymbolInt) -> SymbolInt:
        return SymbolInt(self._value // other._value)

    def __mod__(self, other: SymbolInt) -> SymbolInt:
        return SymbolInt(self._value % other._value)

    def __divmod__(self, other: SymbolInt) -> tuple[SymbolInt, SymbolInt]:
        q, r = divmod(self._value, other._value)
        return (SymbolInt(q), SymbolInt(r))

    def norm(self) -> Abs:
        return Abs(self._value)

    def __bool__(self):
        return bool(self._value)

    def gcd(self, a: SymbolInt) -> SymbolInt:
        if isinstance(a, SymbolInt):
            return SymbolInt(igcd(self._value, a._value))
        else:
            raise TypeError("Expected SymbolInt for gcd operation")

    @classmethod
    def zero(cls) -> SymbolInt:
        return SymbolInt(S.Zero)

    @classmethod
    def one(cls) -> SymbolInt:
        return SymbolInt(S.One)

    def to_symbol(self) -> Symbol:
        return self._value

    def __str__(self) -> str:
        return str(self._value)

    def __repr__(self) -> str:
        return f"Int({self._value})"

    def descent(self):
        return [SymbolInt]
