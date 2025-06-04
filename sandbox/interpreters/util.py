# diverse Utilities
# js 28.2.2002
# verbessert 3.4.04

from functools import reduce


def curry(f, x):  # binds first arg
    return lambda *xs: f(*(x,) + xs)


def rcurry(f, x):  # binds last arg
    return lambda *xs: f(*xs + (x,))


flip = lambda f: lambda x, y: f(y, x)  # flips args

compose = lambda f, g: lambda *x: f(g(*x))  # composes f and g

binary2nary = lambda f: lambda *args: reduce(f, args)

negate = lambda p: lambda x: not p(x)  # negates a predicate

unaryAnd = lambda p, q: lambda x: p(x) and q(x)

unaryOr = lambda p, q: lambda x: p(x) or q(x)

odd = lambda x: x % 2

even = negate(odd)
