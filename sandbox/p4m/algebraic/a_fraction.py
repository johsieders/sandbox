from __future__ import annotations

from typing import TypeVar, Generic

from sandbox.p4m.protocols.p_euclidean_ring import EuclideanRing

T = TypeVar("T", bound=EuclideanRing)


def gcd(a: T, b: T) -> T:
    while b != b.zero():
        a, b = b, a % b
    return a


class Fraction(Generic[T]):
    __slots__ = ("_num", "_den")

    def __init__(self, numerator: T | Fraction[T], denominator: T | None = None):
        if isinstance(numerator, Fraction):
            # Copy constructor: ignore denominator argument
            self._num = numerator._num
            self._den = numerator._den
        else:
            if denominator is None:
                denominator = numerator.one()
            if denominator == denominator.zero():
                raise ZeroDivisionError("Fraction with denominator zero")

            g = gcd(numerator, denominator)
            num = numerator // g
            den = denominator // g
            # Optional: sign normalization if possible
            try:
                if den < den.zero():
                    num = -num
                    den = -den
            except (TypeError, AttributeError):
                pass
            self._num = num
            self._den = den

    def __add__(self, other: Fraction) -> Fraction:
        return Fraction(
            self._num * other._den + self._den * other._num,
            self._den * other._den,
        )

    def __sub__(self, other: Fraction) -> Fraction:
        return Fraction(
            self._num * other._den - self._den * other._num,
            self._den * other._den,
        )

    def __mul__(self, other: Fraction) -> Fraction:
        return Fraction(self._num * other._num, self._den * other._den)

    def __truediv__(self, other: Fraction) -> Fraction:
        return self * other.inverse()

    def __neg__(self) -> Fraction:
        return Fraction(-self._num, self._den)

    def __eq__(self, other: object) -> bool:
        return (
                isinstance(other, Fraction)
                and self._num == other._num
                and self._den == other._den
        )

    def __floordiv__(self, other: Fraction) -> Fraction:
        return self / other

    def __mod__(self, other: Fraction) -> Fraction:
        return self.zero()

    def divmod(self, other: Fraction) -> tuple[Fraction, Fraction]:
        return (self / other, self.zero())

    def inverse(self) -> Fraction:
        if self._num == self._num.zero():
            raise ZeroDivisionError("Fraction division by zero")
        return Fraction(self._den, self._num)

    def degree(self) -> int | float:
        return self._num.degree() - self._den.degree()

    def norm(self) -> float:
        return self._num.norm() / self._den.norm()

    def zero(self) -> Fraction:
        return Fraction(self._num.zero(), self._den.one())

    def one(self) -> Fraction:
        return Fraction(self._num.one(), self._den.one())

    @property
    def numerator(self) -> T:
        return self._num

    @property
    def denominator(self) -> T:
        return self._den

    def to_pair(self) -> tuple[T, T]:
        return (self._num, self._den)

    def __str__(self) -> str:
        return f"{self._num}/{self._den}"

    def __repr__(self) -> str:
        return f"Fraction({repr(self._num)}, {repr(self._den)})"
