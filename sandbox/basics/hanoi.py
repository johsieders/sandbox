# j.siedersleben
# towers of hanoi
# 17.11.2020
# update 29.04.2025

from __future__ import annotations

def hanoi_naked(n: int) -> None:
    """
    Towers of Hanoi. Exponential time (n = 22 -> 1.1 s)
    :param n: number of disks on first tower > 0
    :return: None
    There is nothing left to remove
    """

    a, b, c = list(range(n, 0, -1)), [], []

    def move(k, x, y, z):
        """
        This function moves k disks from stack x to stack z
        using y as clipboard
        :param k: number of disks to be moved
        :param x: from stack
        :param y: clipboard
        :param z: to stack
        :return: None
        """
        if k == 1:
            z.append(x.pop())
        else:
            move(k - 1, x, z, y)
            move(1, x, y, z)
            move(k - 1, y, x, z)

    move(n, a, b, c)


def hanoi_mutable(n: int) -> list[tuple[list[int], list[int], list[int]]]:
    """
    Towers of Hanoi. Exponential time (n = 22 -> 2.7 s)
    :param n: number of disks on first tower > 0
    :return: protocol of all moves
    This is hanoi_naked with protocol
    """

    # checking a precondition
    if n < 1:
        raise ValueError

    a, b, c = list(range(n, 0, -1)), [], []
    protocol = [(list(a), list(b), list(c))]

    def move(k, x, y, z):
        if k == 1:
            z.append(x.pop())
            protocol.append((list(a), list(b), list(c)))
        else:
            move(k - 1, x, z, y)
            move(1, x, y, z)
            move(k - 1, y, x, z)

    move(n, a, b, c)
    return protocol


def hanoi_immutable(n) -> list[list[range | tuple]]:
    """
    Towers of Hanoi. Exponential time (n = 22 -> 3.5 s)
    :param n: number of disks on first tower > 0
    :return: protocol of all moves
    This is hanoi with immutable lists
    """

    if n < 1:
        raise ValueError

    rods = [range(n, 0, -1), (), ()]
    protocol = [rods]

    def move(n, rods, i, j, k):
        if n == 1:
            n_rods = 3 * [None]
            n_rods[i] = tuple(rods[i][:-1])  # move top of rod[i]
            n_rods[j] = tuple(rods[j])
            n_rods[k] = tuple(rods[k]) + tuple([rods[i][-1]])  # to top of rod[k]
            protocol.append(n_rods)
            return n_rods
        else:
            n_rods = move(n - 1, rods, i, k, j)
            n_rods = move(1, n_rods, i, j, k)
            n_rods = move(n - 1, n_rods, j, i, k)
        return n_rods

    move(n, rods, 0, 1, 2)
    return protocol

