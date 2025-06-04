# testing collections
# 20/11/2020
# 28.04.2025

from sandbox.basics.romans import romanfunc

def test_romans():
    to_roman, from_roman = romanfunc()

    assert('I' == to_roman(1))
    assert('CI' == to_roman(101))

    assert(1 == from_roman('I'))
    assert(100 == from_roman('C'))
