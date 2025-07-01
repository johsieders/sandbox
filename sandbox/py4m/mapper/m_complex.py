from __future__ import annotations

from typing import TypeVar

from sandbox.py4m.protocols.p_field import Field
from sandbox.py4m.wrapper.w_complex import NativeComplex

T = TypeVar("T", bound=Field)

from typing import TypeVar, Generic, Any

T = TypeVar("T")  # Typically bound=Field


class Complex(Generic[T]):
    __slots__ = ("_re", "_im")

    def __init__(self, re: Any, im: Any = None):

        # Case 1: Complex(c: Complex[T]) –> Complex[T]
        if im is None and isinstance(re, Complex):
            self._re = re._re
            self._im = re._im
        # Case 2: Complex(c: ComplexNative) –> Complex[int|float]
        elif im is None and isinstance(re, NativeComplex):
            self._re = re._value.real
            self._im = re._value.imag
        # Case 3: Complex(re: Complex[T], im: Complex[T]) -> Complex[T]
        elif isinstance(re, Complex) and isinstance(im, Complex):
            # Combine re and im as a + ib, where a and b are Complex[T]
            # We set: (a + ib) = (re, im)
            # So, re: Complex[T], im: Complex[T]
            # "Flatten" to T
            a, b = re._re, re._im
            c, d = im._re, im._im
            self._re = a - d
            self._im = b + c
        # Case 4: Complex(re: T, im: T) -> Complex[T]
        else:
            self._re = re
            self._im = im

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
        return isinstance(other, Complex) and self._re == other._re and self._im == other._im

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

    def divmod(self, other: Complex[T]) -> tuple[Complex[T], Complex[T]]:
        return (self / other, self.zero())

    def inverse(self) -> Complex[T]:
        c, d = self._re, self._im
        denom = c * c + d * d
        if denom == denom.zero():
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
