from __future__ import annotations

# AlgebraicType import removed - using protocol-based system instead
from sandbox.py4alg.protocols.p_field import Field
from sandbox.py4alg.util.utils import close_to


class Complex[T: Field]:
    # If arg[0] implements a Field, Complex implements a Field
    # functor_map removed - using protocol-based system instead

    def __init__(self, *args: T | Complex[T]):

        if len(args) not in (1, 2):
            raise TypeError(f"expected 1 or 2 arguments, got {len(args)}")

        a = args[0]
        if len(args) == 1:
            b = args[0].zero()
        else:
            b = args[1]

        if isinstance(a, Complex) and isinstance(b, Complex):
            self._descent = args[0].descent()
            self._re = a._re - b._im
            self._im = a._im + b._re
        else:
            self._descent = [Complex] + args[0].descent()
            self._re = a
            self._im = b

    def __add__(self, other: Complex[T]) -> Complex[T]:
        return Complex(self._re + other._re, self._im + other._im)

    def __sub__(self, other: Complex[T]) -> Complex[T]:
        return Complex(self._re - other._re, self._im - other._im)

    def __mul__(self, other: Complex[T]) -> Complex[T]:
        # (a+bi)*(c+di) = (ac-bd) + (ad+bc)i
        a, b = self._re, self._im
        c, d = other._re, other._im
        return Complex(a * c - b * d, a * d + b * c)

    def __neg__(self) -> Complex[T]:
        return Complex(-self._re, -self._im)

    def __eq__(self, other: object) -> bool:
        return (isinstance(other, Complex) and
                close_to(self._re, other._re) and
                close_to(self._im, other._im))

    def __truediv__(self, other: Complex[T]) -> Complex[T]:
        # (a+bi)/(c+di) = [(a+bi)*(c-di)] / (c^2 + d^2)
        c, d = other._re, other._im
        denom = c * c + d * d
        num = self * Complex(c, -d)
        return Complex(num._re / denom, num._im / denom)

    def __floordiv__(self, other: Complex[T]) -> Complex[T]:
        # In a Field, // is the same as /
        return self / other

    def __mod__(self, other: Complex[T]) -> Complex[T]:
        return self.zero()

    def __divmod__(self, other: Complex[T]) -> tuple[Complex[T], Complex[T]]:
        return (self / other, self.zero())

    def inverse(self) -> Complex[T]:
        c, d = self._re, self._im
        denom = c * c + d * d
        if close_to(denom, denom.zero()):
            raise ZeroDivisionError("Complex division by zero")
        return Complex(c / denom, -d / denom)

    def norm(self) -> float:
        # Returns the "absolute value" (in the base field)
        n = self._re * self._re + self._im * self._im
        return n.norm()

    def degree(self) -> int | float:
        # For compatibility: use max degree of components
        return max(self._re.degree(), self._im.degree())

    def zero(self) -> Complex[T]:
        return Complex(self._re.zero(), self._im.zero())

    def one(self) -> Complex[T]:
        return Complex(self._re.one(), self._im.zero())

    @property
    def re(self) -> T:
        return self._re

    @property
    def im(self) -> T:
        return self._im

    def __str__(self) -> str:
        return f"({self._re} + {self._im}i)"

    def __repr__(self) -> str:
        return f"Complex({repr(self._re)}, {repr(self._im)})"

    def descent(self):
        return self._descent
