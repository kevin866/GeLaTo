# coding: utf-8

import numpy as np
from numpy import linspace, zeros, pi


from sympy.core.containers import Tuple
from sympy import symbols
from sympy import Symbol
from sympy import Lambda
from sympy import IndexedBase

from gelato.glt import glt_symbol
from gelato.calculus   import Constant
from gelato.calculus   import (Dot, Cross, Grad, Curl, Rot, Div)
from gelato.fem.utils    import compile_symbol

from spl.fem.splines import SplineSpace
from spl.fem.tensor  import TensorSpace
from spl.fem.vector  import VectorFemSpace


# ...
def test_3d_1():
    x,y,z = symbols('x y z')

    u = Symbol('u')
    v = Symbol('v')

    a = Lambda((x,y,z,v,u), Dot(Grad(u), Grad(v)))
    print('> input       := {0}'.format(a))

    # ...  create a finite element space
    p1  = 2 ; p2  = 2 ; p3  = 2
    ne1 = 2 ; ne2 = 2 ; ne3 = 2
    # ...

    print('> Grid   :: [{},{},{}]'.format(ne1, ne2, ne3))
    print('> Degree :: [{},{},{}]'.format(p1, p2, p3))

    grid_1 = linspace(0., 1., ne1+1)
    grid_2 = linspace(0., 1., ne2+1)
    grid_3 = linspace(0., 1., ne3+1)

    V1 = SplineSpace(p1, grid=grid_1)
    V2 = SplineSpace(p2, grid=grid_2)
    V3 = SplineSpace(p3, grid=grid_3)

    V = TensorSpace(V1, V2, V3)
    # ...

    # ... create a glt symbol from a string without evaluation
    expr = glt_symbol(a, space=V)
    print('> glt symbol  := {0}'.format(expr))
    # ...

    # ...
    symbol_f90 = compile_symbol('symbol_1', a, V, backend='fortran')
    # ...

    # ... example of symbol evaluation
    t1 = linspace(-pi,pi, ne1+1)
    t2 = linspace(-pi,pi, ne2+1)
    t3 = linspace(-pi,pi, ne3+1)
    x1 = linspace(0.,1., ne1+1)
    x2 = linspace(0.,1., ne2+1)
    x3 = linspace(0.,1., ne3+1)
    e = zeros((ne1+1, ne2+1, ne3+1), order='F')
    symbol_f90(x1,x2,x3,t1,t2,t3, e)
    # ...

    print('')
# ...

# ...
def test_3d_2():
    x,y,z = symbols('x y z')

    u = IndexedBase('u')
    v = IndexedBase('v')


    a = Lambda((x,y,z,v,u), Div(u) * Div(v) + 0.2 * Dot(u, v))
    print('> input       := {0}'.format(a))

    # ... create a glt symbol from a string without evaluation
    #     a discretization is defined as a dictionary
    discretization = {"n_elements": [16, 16, 16], "degrees": [3, 3, 3]}

    expr = glt_symbol(a, discretization=discretization, evaluate=False, is_block=True)
    print('> glt symbol  := {0}'.format(expr))
    # ...

    print('')
# ...

# ...
def test_3d_3():
    x,y,z = symbols('x y z')

    u = IndexedBase('u')
    v = IndexedBase('v')

    a = Lambda((x,y,z,v,u), Dot(Curl(u), Curl(v)) + 0.2 * Dot(u, v))
    print('> input       := {0}'.format(a))

    # ... create a glt symbol from a string without evaluation
    #     a discretization is defined as a dictionary
    discretization = {"n_elements": [16, 16, 16], "degrees": [3, 3, 3]}

    expr = glt_symbol(a, discretization=discretization, evaluate=False, is_block=True)
    print('> glt symbol  := {0}'.format(expr))
    # ...

    print('')
# ...

# ...
def test_3d_4a():
    x,y,z = symbols('x y z')

    u = IndexedBase('u')
    v = IndexedBase('v')

    b = Tuple(1.0, 0., 0.)

    a = Lambda((x,y,z,v,u), Dot(Curl(Cross(b,u)), Curl(Cross(b,v))) + 0.2 * Dot(u, v))
    print('> input       := {0}'.format(a))

    # ... create a glt symbol from a string without evaluation
    #     a discretization is defined as a dictionary
    discretization = {"n_elements": [16, 16, 16], "degrees": [3, 3, 3]}

    expr = glt_symbol(a, discretization=discretization, evaluate=False, is_block=True)
    print('> glt symbol  := {0}'.format(expr))
    # ...

    print('')
# ...

# ...
def test_3d_4b():
    """Alfven operator."""
    x,y,z = symbols('x y z')

    u = IndexedBase('u')
    v = IndexedBase('v')

    bx = Constant('bx')
    by = Constant('by')
    bz = Constant('bz')
    b = Tuple(bx, by, bz)

    c0,c1,c2 = symbols('c0 c1 c2')

    a = Lambda((x,y,z,v,u), (  c0 * Dot(u, v)
                             - c1 * Div(u) * Div(v)
                             + c2 *Dot(Curl(Cross(b,u)), Curl(Cross(b,v)))))
    print('> input       := {0}'.format(a))

    # ... create a glt symbol from a string without evaluation
    #     a discretization is defined as a dictionary
    discretization = {"n_elements": [16, 16, 16], "degrees": [3, 3, 3]}

    expr = glt_symbol(a, discretization=discretization, evaluate=False, is_block=True)
    print('> glt symbol  := {0}'.format(expr))
    # ...

    print('')
# ...

# .....................................................
if __name__ == '__main__':
    test_3d_1()
#    test_3d_2()
#    test_3d_3()
#    test_3d_4a()
#    test_3d_4b()
