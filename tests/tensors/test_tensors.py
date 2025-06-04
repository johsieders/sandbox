import torch

m = 7
n = 4
k = 3
A = torch.arange(1, m + 1)
B = torch.arange(1, m * n + 1).view(m, -1)
C = torch.arange(1, m * n * k + 1).view(m, n, -1)


def test_index():
    # useful for subset of entries/rows/columns/matrices
    # B[i] = i-th row of B
    # B[x] = [B[i] for i in x], subset of rows
    # B[:, j] = j-th column of B
    # B[:, y] = [B[j] for j in y], subset of columns
    # B[x, y] = [B[i, j] for (i, j) in zip(x, y)], subset of entries
    # C[i] = i-th matrix
    # C[x] = C[i, :, :] = C[x] = subset of matrices
    # C[:, j] = j-th row of each matrix
    # C[:, y] = subset of rows
    # C[..., k] = C[:, :, k] = k-th column of each matrix
    # C[..., z] = C[:, :, z] subset of columns

    # C[[0, 1], [0, 1], :] size = [2, n]
    # C[[0, 1], :, [0, 1]] size = [m, 2]
    # C[:, [0, 1], [0, 1]] size = [2, k]

    # C[C <= 10] size = [10]

    print()
    print('B = ', B)  # size = [7, 4]
    print('B[0] = ', B[0])  # size = [4]
    print('B[[0]] = ', B[[0]])  # size = [1, 4]
    print('B[0, 1] = ', B[[0, 1]])  # size = [2, 4]
    print('B[1, 3, 5] = ', B[[1, 3, 5]])  # size = [3, 4]
    print('B[[0, 1, 2], [0, 1, 2]] = ', B[[0, 1, 2], [0, 1, 2]])
    print('B[:, 0] = ', B[:, 0])  # size = [7]
    print('B[:, [0]] = ', B[:, [0]])  # size = [7, 1]
    print('B[:, [0, 3]] = ', B[:, [0, 3]])  # size = [7, 2]


def test_flip():
    # A.flip(d1, d2, ..) reverses order of elements in given dims; size unchanged
    # inverse = flip

    R = A.flip(0)
    assert torch.equal(A, R.flip(0))
    R = B.flip(0)  # reverses rows, same size
    assert torch.equal(B, R.flip(0))
    R = B.flip(1)  # reverses columns, same size
    assert torch.equal(B, R.flip(1))
    R = B.flip(0, 1)  # reverses rows and columns, same size
    assert torch.equal(B, R.flip(0, 1))


def test_chunk():
    # useful for splitting a tensor into a given number of chunks; last chunk truncated
    # inverse = cat
    # X.chunk(n_chunks, dim=0) splits X into a tuple of n_chunks chunks along dim
    # n_chunks: number of chunks given; len(chunk) = ceil(X.size[dim] / n_chunks)
    # last chunk truncated
    # invariants
    # cat(X.chunk(n_chunks, dim), dim) == X

    R = B.chunk(1, 0)  # identity
    assert torch.equal(B, R[0])
    R = B.chunk(2, 0)  # X split vertically into two chunks
    assert torch.equal(B, torch.cat(R, 0))
    R = B.chunk(1, 1)  # identity
    assert torch.equal(B, R[0])
    R = B.chunk(2, 1)  # X split horizontally into two chunks
    assert torch.equal(B, torch.cat(R, 1))
    R = B.chunk(3, 1)  # X split horizontally into two chunks
    assert torch.equal(B, torch.cat(R, 1))
    R = B.chunk(4, 1)  # X split horizontally into four column vectors
    assert torch.equal(B, torch.cat(R, 1))


def test_split():
    # useful for splitting a tensor into chunks of given size or sizes; last chunk truncated
    # inverse = cat
    # X.split(chunk_length, dim=0) splits X into a tensor of chunks of given length along dim
    # last chunk truncated
    # X.split(chunk_lengths, dim=0) splits X into a tensor of chunks of lengths given by tuple along dim
    # sum(lengths) == X.size(dim)

    # result always given as list of tensors which can be concatenated by cat
    # invariants
    # cat(X.split(length, dim), dim) == X

    R = B.split(1, 0)  # tuple of 7 tensors (row 0, row 1, .., row 6)
    assert torch.equal(B, torch.cat(R, 0))
    R = B.split(2, 0)  # tuple of four tensors of length 2, 2, 2, 1
    assert torch.equal(B[0:2], R[0])  # first two rows
    R = B.split(2, 1)  # tuple of two tensors of length 2
    assert torch.equal(B, torch.cat(R, 1))
    R = B.split((2, 1, 1), 1)  # tuple of three tensors of lengths 2, 1, 1
    assert torch.equal(B, torch.cat(R, 1))


def test_xstack():
    # Testing vstack, hstack and dstack
    # Tensors are stacked vertically (dim=0), horizontally (dim=1) or depthwise (dim=2)
    # dimensions must match except in given dimension

    # hstack extends nothing
    # vstack extends tensors of size [m] to [1, m]
    # dstack extends tensors of size [m] to [1, m, 1]
    # and tensors of size [m, n] to [m, n, 1]

    R = torch.vstack((A, A))
    assert [2, m] == list(R.size())

    R = torch.vstack((B, B))
    assert [2 * m, n] == list(R.size())

    R = torch.vstack((C, C))
    assert [2 * m, n, k] == list(R.size())

    R = torch.hstack((A, A))
    assert [2 * m] == list(R.size())

    R = torch.hstack((B, B))
    assert [m, 2 * n] == list(R.size())

    R = torch.hstack((C, C))
    assert [m, 2 * n, k] == list(R.size())

    R = torch.dstack((A, A))
    assert [1, m, 2] == list(R.size())

    R = torch.dstack((B, B))
    assert [m, n, 2] == list(R.size())

    R = torch.dstack((C, C))
    assert [m, n, 2 * k] == list(R.size())


def test_stack():
    # arguments must match in all dimensions,
    # they are stacked along dim.
    # There is always a new dimension dim; size[dim] = number of arguments

    # works with X for dim = 0 and dim = 1
    R = torch.stack((A, A), dim=0)
    F = torch.vstack((A, A))
    assert [2, m] == list(R.size())
    assert (torch.equal(R, F))

    R = torch.stack((A, A), dim=1)
    assert [m, 2] == list(R.size())
    assert (torch.equal(A, R[:, 0]))
    assert (torch.equal(A, R[:, 1]))

    # stacks builds a new dimension at dim
    R = torch.stack((B, B), dim=0)
    assert [2, m, n] == list(R.size())

    R = torch.stack((B, B), dim=1)
    assert [m, 2, n] == list(R.size())

    R = torch.stack((B, B), dim=2)
    F = torch.dstack((B, B))
    assert [m, n, 2] == list(R.size())
    assert (torch.equal(R, F))

    R = torch.stack((C, C), dim=0)
    assert [2, m, n, k] == list(R.size())

    R = torch.stack((C, C), dim=1)
    assert [m, 2, n, k] == list(R.size())

    R = torch.stack((C, C), dim=2)
    assert [m, n, 2, k] == list(R.size())

    R = torch.stack((C, C), dim=3)
    assert [m, n, k, 2] == list(R.size())


def test_flatten():
    R0 = C.flatten()
    R1 = C.ravel()
    R2 = C.view(-1)
    assert torch.equal(R0, R1)
    assert torch.equal(R1, R2)
    assert list(R0.size()) == [m * n * k]
    R = C.flatten(0, 1)
    assert list(R.size()) == [m * n, k]
    R = C.flatten(1, 2)
    assert list(R.size()) == [m, n * k]


def test_narrow():
    # X.narrow(dim, start, length) narrows X along dim to length dimensions starting at start
    # size = [dim_0, .., length, .., dim_n], equivalent to size[dim] = length

    R0 = A.narrow(0, 0, 3)  # keeps first three elements of A
    R1 = A.narrow(0, 4, 2)  # keeps last two elements of A
    R2 = B.narrow(0, 5, 2)  # keeps last two rows of B
    R3 = C.narrow(0, 0, 1)  # keeps first slice of C
    R4 = C.narrow(1, 1, 3)  # keeps rows 1, 2, 3 of each slice
    assert list(R0.size()) == [3]
    assert list(R1.size()) == [2]
    assert list(R2.size()) == [2, 4]
    assert list(R4.size()) == [m, 3, k]


def test_gather():
    index = torch.tensor([3, 4, 5])
    R = A.gather(0, index)
    assert (torch.equal(A[index], R))

    # gathering along dim = 0
    # index indicates entries to pick in each row
    index0 = torch.tensor([[0, 0, 0, 0]])  # first row
    index1 = torch.tensor([[1, 1, 1, 1]])  # second row
    index2 = torch.tensor([[1, 2, 0, 3]])  # entry 1 in row 0, entry 2 in row 2, ...
    R = B.gather(0, index0)
    S = B[0].view(1, -1)
    assert torch.equal(R, S)

    R = B.gather(0, index1)
    S = B[1].view(1, -1)
    assert torch.equal(R, S)

    R = B.gather(0, index2)
    S = B[index2, range(4)].view(1, -1)
    assert torch.equal(R, S)

    # gathering along dim = 1
    # index indicates entries to pick in each column
    index0 = torch.tensor([[0], [0], [0], [0], [0], [0], [0]])  # first column
    index1 = torch.tensor([[1], [1], [1], [1], [1], [1], [1]])  # second column
    index2 = torch.tensor([[0], [1], [2], [3], [1], [2], [3]])  # entry 0 in col 0, entry 1 in col 1, ...

    R = B.gather(1, index0)  # first column
    S = B[:, 0].view(-1, 1)
    assert torch.equal(R, S)

    R = B.gather(1, index1)  # second column
    S = B[:, 1].view(-1, 1)
    assert torch.equal(R, S)

    R = B.gather(1, index2)
    # S = B[range(7), [0, 1, 2, 3, 1, 2, 3]].view(-1, 1)
    S = B[range(7), index2.view(-1)].view(-1, 1)
    assert torch.equal(R, S)
