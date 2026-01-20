

from sandbox.symbolics.vector_calculus import (
    make_coords, ScalarField, VectorField, make_vector_field,
    gradient, divergence, curl, laplacian,
    curl_of_gradient_is_zero,
    divergence_of_curl_is_zero,
    laplacian_is_div_grad
)

from sympy import simplify, lambdify

if __name__ == "__main__":
   
    from sympy import Function, Symbol, sin
    from sympy.abc import t, x, y, z
    
    f = Function('f', real=True) (x, y, z)
    g = Function('g', real=True) (x, y, z)
    h = f / g
    d = f + h.diff(x) + sin(x)
    print(d)
    print(type(d))
    # a = Function('a', real=True)(x, y, z)
    # b = Function('a', real=True)(x, y, z) + sin(x)

    a = Function('a')
    # a = Function('a')(x, y, z)

    b = a(x, y, z) + sin(x)
    result = b.subs([(x, 1), (y, 0), (z, 0)])
    print(result)

    b_func = lambdify((x, y, z), b, 'numpy')
    # Now b_func IS callable                                                                                                                                                                                                                                                          
    result = b_func(0, 0, 0)  # Returns numeric value (but a(0,0,0) stays symbolic)  
    # print(result)

    # coords = make_coords('x y z')
    # f = ScalarField('f', coords)
    # g = ScalarField('g', coords)
    # hf = f.func + g.func
    # print(f"Scalar field: h(x, y, z) = {hf}")
    # 
    # grad_f = gradient(f)
    # print(f"Gradient: ∇f = {grad_f}")
    # print(f"Gradient: ∇f = {grad_f.components}")
    # print()
    # 
    # curl_grad_f = curl(grad_f)
    # print(f"Result: {curl_grad_f}")
    # print(f"Simplified: {curl_grad_f.simplify().components}")
    # 
    # coords = make_coords('x y z')
    # E = make_vector_field('E', coords)
    # # Creates E = (E₁(x,y,z), E₂(x,y,z), E₃(x,y,z))
    # print(f"E: {E}")
