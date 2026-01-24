from sympy import symbols, sin, pprint
from sympy.abc import r, s, t

from sandbox.symbolics.vector_calculus import (make_scalar_field, evaluate)

if __name__ == "__main__":
    print("=" * 60)
    print("Method 1: Using SymPy's range syntax (RECOMMENDED)")
    print("=" * 60)

    # Use range syntax - creates a tuple
    x = symbols('x_1:4', real=True)  # x_1, x_2, x_3
    x_1, x_2, x_3 = x

    f = make_scalar_field('f', list(x))
    val1 = evaluate(f + sin(x_1), x_1=1, x_2=2)
    print("f with x_1=1, x_2=2:")
    pprint(val1)
    print()

    print("=" * 60)
    print("Method 2: Using list comprehension")
    print("=" * 60)

    x_vars = [symbols(f'x_{i}', real=True) for i in range(1, 4)]
    x_1, x_2, x_3 = x_vars

    g = make_scalar_field('g', x_vars)
    val2 = evaluate(g + sin(x_1), x_1=1, x_2=2)
    print("g with x_1=1, x_2=2:")
    pprint(val2)
    print()

    print("=" * 60)
    print("Method 3: Using sympy.abc (works but limited)")
    print("=" * 60)

    # This works because r, s, t are from sympy.abc
    h = make_scalar_field('h', [r, s, t])
    val3 = evaluate(h + sin(r), r=1, s=2)
    print("h with r=1, s=2:")
    pprint(val3)
    print()

    print("=" * 60)
    print("Debugging the original problem")
    print("=" * 60)

    # Your original approach - let's see what's wrong
    x_manual = symbols('x_1, x_2, x_3', real=True)  # This creates a tuple!
    print(f"Type of x_manual: {type(x_manual)}")
    print(f"x_manual = {x_manual}")

    # When you do symbols('x_1, x_2, x_3'), you get a tuple directly
    # But you might not be unpacking it correctly
    if isinstance(x_manual, tuple):
        x_1_m, x_2_m, x_3_m = x_manual
        f_manual = make_scalar_field('f_manual', [x_1_m, x_2_m, x_3_m])
        val4 = evaluate(f_manual + sin(x_1_m), x_1_m=1, x_2_m=2)
        print("f_manual with correct unpacking:")
        pprint(val4)
