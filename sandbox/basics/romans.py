# j.siedersleben
# fasttrack to professional programming
# lesson 4: classes_
# 13.12.2020
from sympy.codegen.ast import String


def romans():
    """
    :return: romans nums from 1 to 4999
    """
    digits1 = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX']
    digits2 = ['', 'X', 'XX', 'XXX', 'XL', 'L', 'LX', 'LXX', 'LXXX', 'XC']
    digits3 = ['', 'C', 'CC', 'CCC', 'CD', 'D', 'DC', 'DCC', 'DCCC', 'CM']
    digits4 = ['', 'M', 'MM', 'MMM', 'MMMM']

    toRomanList = []
    for d4 in digits4:
        for d3 in digits3:
            for d2 in digits2:
                for d1 in digits1:
                    toRomanList.append(d4 + d3 + d2 + d1)
    fromRomanMap = dict((toRomanList[n], n) for n in range(len(toRomanList)))
    return toRomanList, fromRomanMap


toRomanList, fromRomanMap = romans()


def to_roman_1(n: int) -> None:
    return toRomanList[n]


def from_roman_1(r: String) -> int:
    return fromRomanMap[r]


class Roman(object):
    """
    This is an abstract class for converting integers
    into roman nums and vice versa
    """
    toRomanList, fromRomanMap = romans()

    def __init__(self):
        raise NotImplementedError

    @staticmethod
    def toRoman(n):
        return Roman.toRomanList[n]

    @staticmethod
    def fromRoman(r):
        return Roman.fromRomanMap[r]


def romanfunc():
    toRomanList, fromRomanMap = romans()

    def toRoman(n):
        return toRomanList[n]

    def fromRoman(r):
        return fromRomanMap[r]

    return toRoman, fromRoman


class RomanFunc(object):
    """
    This is an abstract class for converting integers
    into roman nums and vice versa
    """
    toRoman, fromRoman = romanfunc()

    def __init__(self):
        raise NotImplementedError
