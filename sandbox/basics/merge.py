# j.siedersleben
# fasttrack to professional programming
# lesson 2: collections
# 17.11.2020
# update 29.04.2025

def merge(xs, ys: list) -> list:
    """
    :param xs: a non-descending list
    :param ys: a non-descending list
    :return: merge of xs and ys
    Standard solution. A bit tricky.
    """
    result = []
    # invariants:
    # x, y first elements of xs, ys, None if there is no first element
    x = xs.pop(0) if xs else None
    y = ys.pop(0) if ys else None

    while x and y:  # same as x is not None and y is not None
        if x <= y:  # get next element of xs for next loop
            result.append(x)
            x = xs.pop(0) if xs else None
        else:  # get next element of ys for next loop
            result.append(y)
            y = ys.pop(0) if ys else None

    # x or y may be left behind (but not both)
    if x:
        result.append(x)
    if y:
        result.append(y)

    # one of the remaining xs, ys is empty
    # the one which is not (if any) is appended to result
    if xs:  # same as len(xs) > 0
        result += xs
    if ys:
        result += ys

    return result


def merge_r(xs, ys: list) -> list:
    """
    :param xs: a non-descending list
    :param ys: a non-descending list
    :return: merge of xs and ys
    elegant, recursive but slow
    This the definition of merge, and it happens to run!
    """
    if not xs:
        return list(ys)
    elif not ys:
        return list(xs)
    elif xs[0] <= ys[0]:
        return xs[:1] + merge_r(xs[1:], ys)
    else:
        return ys[:1] + merge_r(xs, ys[1:])


