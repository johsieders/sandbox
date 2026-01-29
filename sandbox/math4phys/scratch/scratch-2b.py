
from sympy import diff, symbols, Function, Matrix, pprint, Eq, latex, Symbol, Expr

from sandbox.math4phys.vector_calculus import gradient, euler_lagrange_equation


def test_lagrange1():
    
    # Define time and mass variable        
    t = symbols('t', real=True)
    m = symbols('m', positive=True)

    # Create time-dependent position functions x_i(t)                                                                                                                                                                                                                                          
    x = [Function(f'x_{i + 1}', real=True)(t) for i in range(3)]
    X = Matrix(x)

    # Define velocity as derivative of position: v_i(t) = dx_i/dt                                                                                                                                                                                                                              
    v = [diff(x_i, t) for x_i in x]
    V = Matrix(v)

    # Lagrangian: L = (m/2)v·v - norm(x)**2                                                                                                                                                                                                                                                           
    L = m * (V.T * V)[0, 0] / 2 - m * (X.norm() ** 2)

    euler_lagrange = Eq(diff(gradient(L, v), t), gradient(L, x))
    pprint(euler_lagrange)


def test_lagrange2():
    # Create independent variables for gradient computation                                                                                                                                                                                                                                    
    x = symbols('x_1:4', real=True)
    v = symbols('v_1:4', real=True)

    X = Matrix(x)
    V = Matrix(v)

    # Define time and mass variable        
    t = symbols('t', real=True)
    m = symbols('m', positive=True)

    # Lagrangian with independent variables                                                                                                                                                                                                                                                    
    L = m * (V.T * V)[0, 0] / 2 - X.norm() ** 2

    # substitute time-dependent functions                                                                                                                                                                                                                                                 
    subs_dict = {}
    for i in range(3):
        subs_dict[x[i]] = f = Function(f'x_{i + 1}')(t)
        subs_dict[v[i]] = diff(f, t)

    # Substitute into the gradient expressions
    # compute gradient first, substitute later
    dL_dx = gradient(L, x).subs(subs_dict)  # Now time-dependent   
    dL_dv = gradient(L, v).subs(subs_dict)  # Now time-dependent                                                                                                                                                                                                                                  
                                                                                                                                                                                                                                   
    # Euler-Lagrange                                                                                                                                                                                                                                                              
    euler_lagrange = Eq(diff(dL_dv, t), dL_dx)
    pprint(euler_lagrange)


def test_lagrange3():
    """
    General Euler-Lagrange formulation with substitution of specific Lagrangians.

    Key insight: Define L as function of scalar components, not Matrix objects.
    Then you can take gradients and substitute specific Lagrangians.
    """
    # Create independent variables for gradient computation
    x = symbols('x_1:4', real=True)
    v = symbols('v_1:4', real=True)

    # Define time  variable
    t = symbols('t', real=True)
  
    # General Lagrangian - function of scalar components (not Matrices!)
    L_general = Function('L', real=True)(*x, *v)

    # substitute time-dependent functions
    subs_dict = {}
    for i in range(3):
        subs_dict[x[i]] = f = Function(f'x_{i + 1}')(t)
        subs_dict[v[i]] = diff(f, t)

    # Substitute into the gradient expressions
    # compute gradient first, substitute later
    dL_dx = gradient(L_general, x).subs(subs_dict)  # Now time-dependent
    dL_dv = gradient(L_general, v).subs(subs_dict)  # Now time-dependent

    # General Euler-Lagrange equation
    euler_lagrange_general = Eq(diff(dL_dv, t), dL_dx)
    print("General Euler-Lagrange (symbolic form):")
    pprint(euler_lagrange_general)
    print()

   
def test_lagrange_harmonic1():
    """
    General Euler-Lagrange formulation with substitution of specific Lagrangians.

    Key insight: Define L as function of scalar components, not Matrix objects.
    Then you can take gradients and substitute specific Lagrangians.
    """
    # Create independent variables for gradient computation
    x = symbols('x_1:4', real=True)
    v = symbols('v_1:4', real=True)

    # Define time  variable
    t = symbols('t', real=True)

    # substitute time-dependent functions
    subs_dict = {}
    for i in range(3):
        subs_dict[x[i]] = f = Function(f'x_{i + 1}')(t)
        subs_dict[v[i]] = diff(f, t)

    # ===== For specific Lagrangians, compute directly (not by substitution) =====
    # The general equation is too complex to substitute into cleanly,
    # so we recompute with the specific L

    # Kinetic energy minus harmonic potential
    m = symbols('m', positive=True)
    X = Matrix(x)
    V = Matrix(v)
    L = m * (V.T * V)[0, 0] / 2 - X.norm() ** 2

    # Compute gradients and substitute time-dependence
    dL_dx = gradient(L, x).subs(subs_dict)
    dL_dv = gradient(L, v).subs(subs_dict)

    # Euler-Lagrange for this specific case
    euler_lagrange = Eq(diff(dL_dv, t), dL_dx)
    print("Specific case: L = (m/2)v·v - ||x||²")
    pprint(euler_lagrange)
    print()

    # Simplify to see the physics clearly
    print("Which simplifies to the 3D harmonic oscillator:")
    simplified = euler_lagrange.doit()
    pprint(simplified)

