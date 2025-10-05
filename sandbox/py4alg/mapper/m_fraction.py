from __future__ import annotations

from sandbox.py4alg.protocols.p_euclidean_ring import EuclideanRing
from sandbox.py4alg.util.utils import close_to


def gcd[T](a: T, b: T) -> T:
    while not close_to(b.norm(), 0.):
        a, b = b, a % b
    return a


class Fraction[T: EuclideanRing]:
    """
    This constructor accepts one or two arguments, which are of type T or Fraction[T]
    A single argument is interpreted as the numerator;
    the denominator is assumed to be one of the matching type.
    Two fractions are flattened into one.
    For any two fractions r, s !=0, the invariant is
    Fraction(r, s) == r / s
    """

    # functor_map removed - using protocol-based system instead

    # resulting_type() method removed - using protocol-based system instead

    def __init__(self, *args: T | Fraction[T]):

        if len(args) not in (1, 2):
            raise TypeError("Fraction constructor expects one or two arguments")

        # supply denominator = one, if none is given
        numerator = args[0]
        if len(args) == 1:
            denominator = numerator.one()
        else:
            denominator = args[1]

        # flatten if input-type is Fraction
        if isinstance(numerator, Fraction):
            self._descent = args[0].descent()
            num = numerator._num * denominator._den
            den = numerator._den * denominator._num
        else:
            self._descent = [Fraction] + args[0].descent()
            num = numerator
            den = denominator

        # Check if denominator is too small (avoid dividing by near-zero values)
        # For floating-point types, use absolute threshold to handle accumulated errors
        den_norm = den.norm()
        MIN_DENOMINATOR_NORM = 1e-200  # Absolute minimum threshold for denominator

        if den_norm < MIN_DENOMINATOR_NORM:
            raise ZeroDivisionError(f"Denominator too small: norm = {den_norm}")

        # Skip GCD normalization if denominator is already very small
        # This prevents further precision loss with floating-point arithmetic
        NORMALIZATION_THRESHOLD = 1e-50  # Below this, skip normalization to preserve precision

        if den_norm < NORMALIZATION_THRESHOLD:
            # Don't normalize - keep as is to avoid making denominator even smaller
            pass
        else:
            # Normal case: try to normalize with GCD
            try:
                g = gcd(num, den)
                normalized_den = den // g
                normalized_den_norm = normalized_den.norm()

                # Only apply normalization if denominator stays large enough
                if normalized_den_norm >= NORMALIZATION_THRESHOLD:
                    num = num // g
                    den = normalized_den
                # Otherwise skip normalization (would make denominator too small)
            except (ZeroDivisionError, ValueError):
                # If GCD computation fails, just skip normalization
                pass
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
                and close_to(self._num * other._den, self._den * other._num)
        )

    def __floordiv__(self, other: Fraction) -> Fraction:
        return self / other

    def __mod__(self, other: Fraction) -> Fraction:
        return self.zero()

    def __divmod__(self, other: Fraction) -> tuple[Fraction, Fraction]:
        return (self / other, self.zero())

    def inverse(self) -> Fraction:
        if close_to(self._num, self._num.zero()):
            raise ZeroDivisionError("Fraction division by zero")
        return Fraction(self._den, self._num)

    def degree(self) -> int | float:
        return self._num.degree() - self._den.degree()

    def norm(self) -> float:
        return self._num.norm() / self._den.norm()

    def zero(self) -> Fraction:
        return Fraction(self._num.zero(), self._num.one())

    def one(self) -> Fraction:
        return Fraction(self._num.one(), self._num.one())

    def gcd(self, other: Fraction) -> Fraction:
        """GCD for field of fractions: gcd(a,b) = 1 if either is non-zero, 0 if both are zero."""
        if close_to(self, self.zero()) and close_to(other, other.zero()):
            return self.zero()
        else:
            return self.one()

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

    def descent(self):
        return self._descent
