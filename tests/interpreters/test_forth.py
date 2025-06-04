# testing collections
# 20/11/2020
# updated 29.04.2025

from sandbox.interpreters.forth import Forth
from timeit import timeit

def tst_Forth():
    t0 = '7 8 9 DUP'  # 7 8 9 9
    t1 = '7 8 9 2DUP'  # 7 8 9 8 9
    t2 = '7 8 9 SWAP'  # 7 9 8
    t3 = '7 8 9 ROT'  # 8 9 7  third on top
    t4 = '7 8 9 -ROT'  # 9 7 8  top on third
    t5 = '8 5 /'  # 1.6
    t6 = '7 NOT'  # 0
    t7 = '7 1 IF DUP THEN 8 - +'  # 7 + 7 - 8 = 6
    t8 = '7 0 IF DUP THEN 8 -'  # 7 - 8 = -1
    t9 = '7 0 IF DUP ELSE 9 - THEN'  # 7 - 8 = -2
    t10 = '9 1 IF 0 IF 3 + THEN 9 + THEN 17 +'  # 35
    t11 = '9 0 IF 1 IF 3 + THEN 9 + THEN 17 +'  # 26
    t12 = '9 0 IF 8 ELSE 1 THEN +'  # 10
    t13 = '200 BEGIN 1 - DUP NOT UNTIL'  # 0
    t14 = '7 5 BEGIN 1 - SWAP 1 + SWAP DUP NOT UNTIL'  # 0
    t15 = '7 DUP *'  # 49
    t16 = '9 0 IF 8 ELSE 1 IF 5 ELSE 8 THEN THEN +'  # 14
    t17 = '1 10 0 DO DUP + LOOP'  # 1024

    ts = [t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16, t17]

    F = Forth()
    for t in ts:
        F(t)

    F(': SQR ( a - a^2 ) DUP * ;')
    F('7 SQR')  # 49

    F(': GCD ( a b - gcd ) DUP IF TUCK MOD GCD ELSE DROP THEN ;')
    F(': GC_ ( a b - gcd ) BEGIN DUP WHILE TUCK MOD REPEAT DROP ;')

    F('60 40 GCD')  # 20
    F('60 40 GC_')  # 20

    F(': HORNER ( a0 a1 .. an n x - p(x) ) SWAP DUP IF 0 DO DUP >R * +  R> LOOP ELSE DROP THEN DROP ;')
    F(': HORNE_ ( a0 a1 .. an x n - p(x) ) DUP IF 1- >R DUP >R * + R> R> HORNE_ ELSE DROP DROP THEN ;')
    F(': HORNRR ( a0 a1 .. an n x - p(x) ) SWAP HORNE_ ;')

    F(': P0 1 0 ;')
    F(': P1 1 1 1 ;')
    F(': P10 1 1 1 1 1 1 1 1 1 1 1 10 ;')

    F('P0 10 HORNER')  # 1
    F('P1 10 HORNER')  # 11
    F('P10 10 HORNER')  # 11111111111
    F('P0 10 HORNRR')  # 1
    F('P1 10 HORNRR')  # 11
    F('P10 10 HORNRR')  # 11111111111

    # print(F)

def test_forth() -> None:
    t_forth = timeit(tst_Forth, number=10)
    print(f'\n{t_forth = :.5f}')
