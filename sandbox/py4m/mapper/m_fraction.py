from __future__ import annotations

from typing import TypeVar, Generic

from sandbox.py4m.protocols.p_euclidean_ring import EuclideanRing
from sandbox.py4m.util.utils import close_to

T = TypeVar("T", bound=EuclideanRing)


def ext_gcd(a: T, b: T) -> tuple[T, T, T]:
    """
    :param a: an element of an Euclidian ring
    :param b: another element of an Euclidian ring
    :return: three elements g, s, t such that
             g = gcd(a, b) and
             g = a * s + b * t
    """
    zero = a.zero()
    one = a.one()

    s, u = one, zero
    t, v = zero, one

    while not close_to(b, zero):
        q, r = divmod(a, b)
        a, b = b, r
        s, u = u, s - q * u
        t, v = v, t - q * v
    return a, s, t


def gcd(a: T, b: T) -> T:
    # while b != b.zero():
    #     a, b = b, a % b
    # return a

    while not close_to(b.norm(),0.):
        a, b = b, a % b
    return a


class Fraction(Generic[T]):
    """
    This constructor accepts one or two arguments, which are of type T or Fraction[T]
    A single argument is interpreted as the numerator;
    the denominator is assumed to be one of the matching type.
    Two fractions are flattened into one.
    For any two fractions r, s !=0, the invariant is
    Fraction(r, s) == r / s
    """

    def __init__(self, *args: T | Fraction[T]):
        self._num = None
        self._den = None

        if len(args) not in (1, 2):
            raise TypeError("Fraction constructor expects one or two arguments")

        # supply denominator = one, if none is given
        numerator = args[0]
        if len(args) == 1:
            denominator = numerator.one()
        else:
            denominator = args[1]

        # flatten if input type is Fraction
        if isinstance(numerator, Fraction):
            num = numerator._num * denominator._den
            den = numerator._den * denominator._num
        else:
            num = numerator
            den = denominator

        if den == den.zero():
            raise ZeroDivisionError()

        g = gcd(num, den)
        num //= g
        den //= g
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

    def __divmod__(self, other: Fraction) -> tuple[Fraction, Fraction]:
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
