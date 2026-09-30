from __future__ import annotations

from typing import Any

from sympy import Symbol, Abs, Expr, Poly, ZZ

# generator for constants: a sympy Poly needs one; arithmetic unifies generators, so it is harmless
_CONST = Symbol('_', integer=True)


class SymbolicInt:
    """Symbolic integers over sympy: the ring Z[a, b, ...] of polynomials with integer coefficients.

    A Ring, and nothing more:
    - not a EuclideanRing: Z[a, b, ...] has unique factorization, so gcds exist, but no division with
      remainder (not even a principal ideal domain); hence no //, %, divmod, euclidean_function or
      normalize, and no Fraction over it;
    - not Comparable: a < b has no truth value, hence no __lt__.

    The value is a sympy Poly over ZZ: integer coefficients are enforced (a/2 is rejected), the
    arithmetic keeps a normal form, and the zero test is exact and cheap (about 40 times faster than
    expressions that are expanded when compared). Equality is (x - y).is_zero, because Poly's own ==
    also compares the generators (Poly(5, a) != Poly(5, b)).
    """

    def __init__(self,
                 value: str | int | Expr | Poly | SymbolicInt):
        if isinstance(value, SymbolicInt):
            self._value = value._value
        elif isinstance(value, Poly):
            self._value = value
        elif isinstance(value, str):
            self._value = Poly(Symbol(value, integer=True), domain=ZZ)
        elif isinstance(value, (Expr, int)):
            gens = sorted(getattr(value, 'free_symbols', ()), key=str) or [_CONST]
            try:
                self._value = Poly(value, *gens, domain=ZZ)
            except Exception as e:
                raise TypeError(f"SymbolicInt needs a polynomial with integer coefficients, got {value}") from e
        else:
            raise TypeError(f"SymbolicInt can only wrap str, int, Expr, Poly or SymbolicInt, got {type(value)}")

    def __add__(self, other: SymbolicInt) -> SymbolicInt:
        return SymbolicInt(self._value + other._value)

    def __sub__(self, other: SymbolicInt) -> SymbolicInt:
        return SymbolicInt(self._value - other._value)

    def __mul__(self, other: SymbolicInt) -> SymbolicInt:
        return SymbolicInt(self._value * other._value)

    def __neg__(self) -> SymbolicInt:
        return SymbolicInt(-self._value)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, SymbolicInt) and (self._value - other._value).is_zero

    def __bool__(self) -> bool:
        """Nonzero as a polynomial: (a+1)**2 - a**2 - 2*a - 1 is zero."""
        return not self._value.is_zero

    def norm(self) -> Abs:
        return Abs(self._value.as_expr())

    @classmethod
    def zero(cls) -> SymbolicInt:
        return SymbolicInt(0)

    @classmethod
    def one(cls) -> SymbolicInt:
        return SymbolicInt(1)

    def to_symbol(self) -> Expr:
        return self._value.as_expr()

    def __str__(self) -> str:
        return str(self._value.as_expr())

    def __repr__(self) -> str:
        return f"SymbolicInt({self._value.as_expr()})"

    def descent(self):
        return [SymbolicInt]
