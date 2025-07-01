from __future__ import annotations

from typing import TypeVar, Generic, Sequence

from sandbox.py4m.protocols.p_ring import Ring

T = TypeVar("T", bound=Ring)


class Matrix(Generic[T]):
    __slots__ = ("_data", "_rows", "_cols")

    def __init__(self, rows: Sequence[Sequence[T]] | Matrix[T]):
        if isinstance(rows, Matrix):
            # Copy constructor
            self._data = rows._data
            self._rows = rows._rows
            self._cols = rows._cols
        else:
            if not rows or not rows[0]:
                raise ValueError("Matrix must have at least one row and one column")
            row_lengths = {len(row) for row in rows}
            if len(row_lengths) != 1:
                raise ValueError("All rows must have the same length")
            self._rows = len(rows)
            self._cols = len(rows[0])
            self._data = tuple(tuple(row) for row in rows)

    def __add__(self, other: Matrix[T]) -> Matrix[T]:
        self._check_shape(other)
        return Matrix([
            [a + b for a, b in zip(row_a, row_b)]
            for row_a, row_b in zip(self._data, other._data)
        ])

    def __sub__(self, other: Matrix[T]) -> Matrix[T]:
        self._check_shape(other)
        return Matrix([
            [a - b for a, b in zip(row_a, row_b)]
            for row_a, row_b in zip(self._data, other._data)
        ])

    def __mul__(self, other: Matrix[T]) -> Matrix[T]:
        # Matrix multiplication
        if self._cols != other._rows:
            raise ValueError("Incompatible shapes for multiplication")
        result = []
        for i in range(self._rows):
            row = []
            for j in range(other._cols):
                val = self._data[i][0] * other._data[0][j]
                for k in range(1, self._cols):
                    val += self._data[i][k] * other._data[k][j]
                row.append(val)
            result.append(row)
        return Matrix(result)

    def __neg__(self) -> Matrix[T]:
        return Matrix([[-a for a in row] for row in self._data])

    def __eq__(self, other: object) -> bool:
        return (
                isinstance(other, Matrix)
                and self._rows == other._rows
                and self._cols == other._cols
                and self._data == other._data
        )

    def zero(self) -> Matrix[T]:
        """Return the zero matrix of the same shape and type as self."""
        vt = type(self._data[0][0])
        return Matrix([[vt.zero() for _ in range(self._cols)] for _ in range(self._rows)])

    def one(self) -> Matrix[T]:
        """Return the identity matrix of the same shape and type as self (square only)."""
        if self._rows != self._cols:
            raise ValueError("Identity matrix only defined for square matrices")
        vt = type(self._data[0][0])
        return Matrix([
            [vt.one() if i == j else vt.zero() for j in range(self._cols)]
            for i in range(self._rows)
        ])

    def norm(self) -> float:
        return max(a.norm() for row in self._data for a in row)

    def degree(self) -> int:
        return max(a.degree() for row in self._data for a in row)

    def shape(self) -> tuple[int, int]:
        return (self._rows, self._cols)

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
