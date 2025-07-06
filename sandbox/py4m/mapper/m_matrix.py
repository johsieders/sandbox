from __future__ import annotations

from typing import TypeVar, Generic

from math import sqrt

from sandbox.py4m.protocols.p_ring import Ring
from sandbox.py4m.util.utils import close_to

T = TypeVar("T", bound=Ring)


class Matrix(Generic[T]):

    def __init__(self, *args: T | Matrix[T]):
        """
        This constructor accepts a list of n^2 matrix entries of type T or Matrix[T].
        T must implement the ring protocol.
        Case type = matrix: All arguments must be matrices of the same size m x m.
        The result is an n*m x n*m - matrix
        """
        n = int(sqrt(len(args)))

        if n == 0 or n ** 2 != len(args):
            raise TypeError(f"expected n^2 arguments, got {len(args)}")
        elif isinstance(args[0], Matrix):
            m = args[0]._size
            self._size = m * n
            self._data = [[0 for _ in range(m * n)] for _ in range(m * n)]
            for j in range(n):
                for k in range(n):
                    self._data[m * j:m * (j + 1)][m * k:m * (k + 1)] = args[n * j + k]
                    for i in range(m):
                        for l in range(m):
                            self._data[m * j + i][m * k + l] = args[n * j + k][i][l]

        else:
            self._size = n
            self._data = tuple(tuple([args[k * n: (k + 1) * n] for k in range(n)]))

    def __add__(self, other: Matrix[T]) -> Matrix[T]:
        self._check_shape(other)
        data = []
        for row_a, row_b in zip(self._data, other._data):
            data += [a + b for a, b in zip(row_a, row_b)]
        return Matrix(*data)

    def __sub__(self, other: Matrix[T]) -> Matrix[T]:
        self._check_shape(other)
        data = []
        for row_a, row_b in zip(self._data, other._data):
            data += [a - b for a, b in zip(row_a, row_b)]
        return Matrix(*data)

    def __mul__(self, other: Matrix[T]) -> Matrix[T]:
        # Matrix multiplication
        if self._size != other._size:
            raise ValueError("Incompatible shapes for multiplication")
        data = []
        for i in range(self._size):
            for j in range(other._size):
                val = self._data[i][0] * other._data[0][j]
                for k in range(1, self._size):
                    val += self._data[i][k] * other._data[k][j]
                data.append(val)

        return Matrix(*data)

    def __neg__(self) -> Matrix[T]:
        data = []
        for row in self._data:
            data += [-a for a in row]
        return Matrix(*data)

    def __eq__(self, other: object) -> bool:
        return (
                isinstance(other, Matrix)
                and self._size == other._size
                and close_to(self, other)
        )

    def zero(self) -> Matrix[T]:
        """Return the zero matrix of the same shape and type as self."""
        zero = self._data[0][0].zero()
        return Matrix(*[zero for _ in range(self._size) for _ in range(self._size)])

    def one(self) -> Matrix[T]:
        """Return the identity matrix of the same shape and type as self (square only)."""
        zero = self._data[0][0].zero()
        one = self._data[0][0].one()
        return Matrix(*[
            one if i == j else zero
            for j in range(self._size)
            for i in range(self._size)])

    def norm(self) -> float:
        return max(a.norm() for row in self._data for a in row)

    def degree(self) -> int:
        return max(a.degree() for row in self._data for a in row)

    def shape(self) -> tuple[int, int]:
        return (self._size, self._size)

    def to_tuples(self) -> tuple[tuple[T, ...], ...]:
        return self._data

    def __str__(self) -> str:
        return "\n[" + "\n".join("[" + ", ".join(str(a) for a in row) + "]," for row in self._data) + "]"
        # return str(self._data)

    def __repr__(self) -> str:
        return f"Matrix({self._data})"

    def _check_shape(self, other: Matrix[T]):
        if not isinstance(other, Matrix):
            raise TypeError("Can only operate with another Matrix of same type.")
        if self.shape() != other.shape():
            raise ValueError(f"Matrix shape mismatch: {self.shape()} != {other.shape()}")

    # Optionally, support item access
    def __getitem__(self, idx):
        return self._data[idx]
