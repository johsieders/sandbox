# j.siedersleben
# fasttrack to professional programming
# lesson 2: collections
# 17.11.2020
# update 29.04.2025


def histogram_1(xs):
    """
    :param xs: a list
    :return: histogram0 of xs: a map indicating how often each x occurs in xs
    """
    result = {}
    for x in xs:
        if x not in result.keys():
            result[x] = 1
        else:
            result[x] += 1
    return result


def histogram_2(xs):
    """
    :param xs: a list
    :return: histogram0 of xs: a map indicating how often each x occurs in xs
    """
    result = {}
    for x in xs:
        if x not in result.keys():
            result[x] = xs.count(x)
    return result


def histogram_3(xs):
    """
    :param xs: a list
    :return: histogram0 of xs: a map indicating how often each x occurs in xs
    """
    return dict([(x, xs.count(x)) for x in xs])


def histogram_4(xs):
    """
    :param xs: a list
    :return: histogram0 of xs: a map indicating how often each x occurs in xs
    """
    return dict([(x, xs.count(x)) for x in set(xs)])
