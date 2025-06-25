from __future__ import annotations

from .algebraic import Field, EuclideanRing
from typing import TypeVar


T = TypeVar("T", bound=EuclideanRing)

def gcd(a: T, b: T) -> T:
    """Generic Euclidean GCD for any EuclideanRing."""
    while b != b.zero():
        a, b = b, a % b
    return a

class Fraction(Field):
    """
    Field of fractions over any EuclideanRing type (duck-typed).
    For example: Fraction(Int(2), Int(3)), Fraction(Polynomial(...), Polynomial(...)), etc.
    """

    __slots__ = ("num", "den")

    num: EuclideanRing
    den: EuclideanRing

    def __init__(self, numerator: EuclideanRing, denominator: EuclideanRing = None):
        if denominator is None:
            denominator = numerator.one()
        if denominator == denominator.zero():
            raise ZeroDivisionError("Fraction with denominator zero")
        g = gcd(numerator, denominator)
        num = numerator // g
        den = denominator // g
        if hasattr(den, "__neg__") and den < den.zero():
            num = -num
            den = -den
        self.num = num
        self.den = den

    def __add__(self, other: Fraction) -> Fraction:
        if not isinstance(other, Fraction):
            raise TypeError(f"Cannot add Fraction and {type(other)}")
        num = self.num * other.den + self.den * other.num
        den = self.den * other.den
        return Fraction(num, den)

    def __sub__(self, other: Fraction) -> Fraction:
        if not isinstance(other, Fraction):
            raise TypeError(f"Cannot subtract Fraction and {type(other)}")
        num = self.num * other.den - self.den * other.num
        den = self.den * other.den
        return Fraction(num, den)

    def __mul__(self, other: Fraction) -> Fraction:
        if not isinstance(other, Fraction):
            raise TypeError(f"Cannot multiply Fraction and {type(other)}")
        num = self.num * other.num
        den = self.den * other.den
        return Fraction(num, den)

    def __truediv__(self, other: Fraction) -> Fraction:
        if not isinstance(other, Fraction):
            raise TypeError(f"Cannot divide Fraction and {type(other)}")
        return self * other.inverse()

    def __floordiv__(self, other: Fraction) -> Fraction:
        return self / other

    def __mod__(self, other: Fraction) -> Fraction:
        return self.zero()

    def divmod(self, other: Fraction) -> tuple[Fraction, Fraction]:
        return (self / other, self.zero())

    def degree(self) -> int | float:
        """Degree of a fraction: deg(num) - deg(den)"""
        return self.num.degree() - self.den.degree()

    def __neg__(self) -> Fraction:
        return Fraction(-self.num, self.den)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Fraction):
            return False
        return self.num == other.num and self.den == other.den

    def inverse(self) -> Fraction:
        if self.num == self.num.zero():
            raise ZeroDivisionError("Fraction division by zero")
        return Fraction(self.den, self.num)

    def zero(self) -> Fraction:
        """Zero element of the same type as self."""
        return Fraction(self.num.zero(), self.den.one())

    def one(self) -> Fraction:
        """Multiplicative identity of the same type as self."""
        return Fraction(self.num.one(), self.den.one())

    def norm(self) -> float:
        # "Size" of fraction: norm(num) / norm(den)
        return self.num.norm() / self.den.norm()

    def __str__(self) -> str:
        return f"{self.num}/{self.den}"

    def __repr__(self) -> str:
        return f"Fraction({repr(self.num)}, {repr(self.den)})"

    @property
    def numerator(self) -> EuclideanRing:
        return self.num

    @property
    def denominator(self) -> EuclideanRing:
        return self.den
