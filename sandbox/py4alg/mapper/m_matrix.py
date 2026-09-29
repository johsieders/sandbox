from __future__ import annotations

from math import sqrt

from sandbox.py4alg.protocols.p_field import Field
from sandbox.py4alg.protocols.p_ring import Ring


class Matrix[T: Ring]:

    def __init__(self, *args: T | Matrix[T]):
        """
        Accepts either:
        - n^2 entries of type T (creates an n x n matrix)
        - n^2 Matrix[T] blocks of equal size m x m (creates a block matrix of size (n*m) x (n*m))
        """
        count = len(args)
        n = int(sqrt(count))
        if n == 0 or n ** 2 != count:
            raise TypeError(f"expected n^2 arguments, got {count}")

        # Block matrix case
        if isinstance(args[0], Matrix):
            # All blocks must be matrices of the same size
            m = args[0]._size
            if not all(isinstance(x, Matrix) and x._size == m for x in args):
                raise TypeError("All blocks must be Matrix objects of the same size")

            # a block matrix is a matrix over the blocks' entries: replace the blocks' class by ours
            self._descent = [type(self)] + args[0].descent()[1:]
            self._size = n * m
            # Build the block matrix using tuple-of-tuples for immutability
            rows = []
            for block_row in range(n):
                for inner_row in range(m):
                    row = []
                    for block_col in range(n):
                        block = args[block_row * n + block_col]
                        row.extend(block[inner_row])
                    rows.append(tuple(row))
            self._data = tuple(rows)
        else:
            # Scalar matrix case
            self._descent = [type(self)] + args[0].descent()
            self._size = n
            self._data = tuple(
                tuple(args[i * n + j] for j in range(n))
                for i in range(n)
            )

    def __add__(self, other: Matrix[T]) -> Matrix[T]:
        self._check_shape(other)
        data = []
        for row_a, row_b in zip(self._data, other._data):
            data += [a + b for a, b in zip(row_a, row_b)]
        return type(self)(*data)

    def __sub__(self, other: Matrix[T]) -> Matrix[T]:
        self._check_shape(other)
        data = []
        for row_a, row_b in zip(self._data, other._data):
            data += [a - b for a, b in zip(row_a, row_b)]
        return type(self)(*data)

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

        return type(self)(*data)

    def __neg__(self) -> Matrix[T]:
        data = []
        for row in self._data:
            data += [-a for a in row]
        return type(self)(*data)

    def __eq__(self, other: object) -> bool:
        return (
                isinstance(other, Matrix)
                and self._size == other._size
                and all(self._data[i][j] == other._data[i][j]
                        for i in range(self._size) for j in range(self._size))
        )

    def zero(self) -> Matrix[T]:
        """Return the zero matrix of the same shape and type as self."""
        zero = self._data[0][0].zero()
        return type(self)(*[zero for _ in range(self._size) for _ in range(self._size)])

    def one(self) -> Matrix[T]:
        """Return the identity matrix of the same shape and type as self (square only)."""
        zero = self._data[0][0].zero()
        one = self._data[0][0].one()
        return type(self)(*[
            one if i == j else zero
            for j in range(self._size)
            for i in range(self._size)])

    def __bool__(self) -> bool:
        return any(bool(a) for row in self._data for a in row)

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
        return f"{type(self).__name__}({self._data})"

    def _check_shape(self, other: Matrix[T]):
        if not isinstance(other, Matrix):
            raise TypeError("Can only operate with another Matrix of same type.")
        if self.shape() != other.shape():
            raise ValueError(f"Matrix shape mismatch: {self.shape()} != {other.shape()}")

    # Optionally, support item access
    def __getitem__(self, idx):
        return self._data[idx]

    def descent(self):
        return self._descent


class FieldMatrix[T: Field](Matrix[T]):
    """Square matrices over a field: Matrix plus det(), inverse() and division.

    Still a Ring, not a Field: matrices do not commute, and singular matrices have no inverse
    (inverse() raises ZeroDivisionError). There is no //, %, euclidean_function or normalize.
    Pivots are the first nonzero entry of a column (entries only need __bool__, not an order).
    """

    def det(self) -> T:
        """Determinant by Gaussian elimination."""
        n = self._size
        a = [list(row) for row in self._data]
        det = a[0][0].one()
        for col in range(n):
            pivot = next((r for r in range(col, n) if a[r][col]), None)
            if pivot is None:
                return a[0][0].zero()
            if pivot != col:
                a[col], a[pivot] = a[pivot], a[col]
                det = -det
            det = det * a[col][col]
            for r in range(col + 1, n):
                if a[r][col]:
                    f = a[r][col] / a[col][col]
                    a[r] = [x - f * y for x, y in zip(a[r], a[col])]
        return det

    def inverse(self) -> FieldMatrix[T]:
        """Inverse by Gauss-Jordan elimination on [self | 1]; ZeroDivisionError if singular."""
        n = self._size
        zero, one = self._data[0][0].zero(), self._data[0][0].one()
        a = [list(row) + [one if i == j else zero for j in range(n)] for i, row in enumerate(self._data)]
        for col in range(n):
            pivot = next((r for r in range(col, n) if a[r][col]), None)
            if pivot is None:
                raise ZeroDivisionError("FieldMatrix.inverse(): matrix is singular")
            a[col], a[pivot] = a[pivot], a[col]
            p = a[col][col]
            a[col] = [x / p for x in a[col]]
            for r in range(n):
                if r != col and a[r][col]:
                    f = a[r][col]
                    a[r] = [x - f * y for x, y in zip(a[r], a[col])]
        return type(self)(*[a[i][n + j] for i in range(n) for j in range(n)])

    def __truediv__(self, other: FieldMatrix[T]) -> FieldMatrix[T]:
        """Right division: self / other == self * other.inverse()."""
        self._check_shape(other)
        return self * other.inverse()
