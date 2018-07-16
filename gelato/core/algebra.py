# coding: utf-8

import numpy as np
from itertools import groupby
from collections import OrderedDict

#from sympy.core.sympify import sympify
from sympy.simplify.simplify import simplify
from sympy import Symbol
from sympy import Lambda
from sympy import Function
from sympy import bspline_basis
from sympy import lambdify
from sympy import cos
from sympy import sin
from sympy import Rational
from sympy import diff
from sympy import Matrix, ImmutableDenseMatrix
from sympy import latex
from sympy import Integral
from sympy import I as sympy_I
from sympy.core import Basic
from sympy.core.singleton import S
from sympy.simplify.simplify import nsimplify
from sympy.utilities.lambdify import implemented_function
from sympy.matrices.dense import MutableDenseMatrix
from sympy import Mul, Add
from sympy import postorder_traversal
from sympy import preorder_traversal

from sympy.core.expr import Expr
from sympy.core.containers import Tuple
from sympy import Integer, Float

from sympy import Add, Mul
from sympy import preorder_traversal, Expr
from sympy import simplify
from sympy import S
from sympy.core.compatibility import is_sequence
from sympy import Basic
from sympy import Indexed, IndexedBase

# ...
class LinearOperator(CalculusFunction):
    """

    Examples
    ========

    """

    nargs = None
    name = 'Grad'
    is_commutative = True

    def __new__(cls, *args, **options):
        # (Try to) sympify args first

        if options.pop('evaluate', True):
            r = cls.eval(*args)
        else:
            r = None

        if r is None:
            return Basic.__new__(cls, *args, **options)
        else:
            return r

    def __getitem__(self, indices, **kw_args):
        if is_sequence(indices):
            # Special case needed because M[*my_tuple] is a syntax error.
            return Indexed(self, *indices, **kw_args)
        else:
            return Indexed(self, indices, **kw_args)

    @classmethod
    def eval(cls, *_args):
        """."""

        if not _args:
            return

        expr = _args[0]
        if isinstance(expr, Add):
            args = expr.args
            args = [cls.eval(a) for a in expr.args]
            return Add(*args)

        if isinstance(expr, Mul):
            coeffs  = [a for a in expr.args if isinstance(a, _coeffs_registery)]
            vectors = [a for a in expr.args if not(a in coeffs)]

            a = S.One
            if coeffs:
                a = Mul(*coeffs)

            b = S.One
            if vectors:
                b = cls(Mul(*vectors), evaluate=False)

            return Mul(a, b)

        return cls(expr, evaluate=False)
# ...

# ...
class DotBasic(CalculusFunction):
    """

    Examples
    ========

    """

    nargs = None
    name = 'Dot'

    def __new__(cls, *args, **options):
        # (Try to) sympify args first

        if options.pop('evaluate', True):
            r = cls.eval(*args)
        else:
            r = None

        if r is None:
            return Basic.__new__(cls, *args, **options)
        else:
            return r

class Dot_1d(DotBasic):
    """

    Examples
    ========

    """

    @classmethod
    def eval(cls, *_args):
        """."""

        if not _args:
            return

        if not( len(_args) == 2):
            raise ValueError('Expecting two arguments')

        u = _args[0]
        v = _args[1]

        return u * v

class Dot_2d(DotBasic):
    """

    Examples
    ========

    """

    @classmethod
    def eval(cls, *_args):
        """."""

        if not _args:
            return

        if not( len(_args) == 2):
            raise ValueError('Expecting two arguments')

        u = _args[0]
        v = _args[1]

        if isinstance(u, (Matrix, ImmutableDenseMatrix)):
            if isinstance(v, (Matrix, ImmutableDenseMatrix)):
                raise NotImplementedError('TODO')

            else:
                return Tuple(u[0,0]*v[0] + u[0,1]*v[1], u[1,0]*v[0] + u[1,1]*v[1])

        else:
            if isinstance(v, (Matrix, ImmutableDenseMatrix)):
                raise NotImplementedError('TODO')

            else:
                return u[0]*v[0] + u[1]*v[1]

class Dot_3d(DotBasic):
    """

    Examples
    ========

    """

    @classmethod
    def eval(cls, *_args):
        """."""

        if not _args:
            return

        if not( len(_args) == 2):
            raise ValueError('Expecting two arguments')

        u = _args[0]
        v = _args[1]

        if isinstance(u, (Matrix, ImmutableDenseMatrix)):
            if isinstance(v, (Matrix, ImmutableDenseMatrix)):
                raise NotImplementedError('TODO')

            else:
                return Tuple(u[0,0]*v[0] + u[0,1]*v[1] + u[0,2]*v[2],
                             u[1,0]*v[0] + u[1,1]*v[1] + u[1,2]*v[2],
                             u[2,0]*v[0] + u[2,1]*v[1] + u[2,2]*v[2])

        else:
            if isinstance(v, (Matrix, ImmutableDenseMatrix)):
                raise NotImplementedError('TODO')

            else:
                return u[0]*v[0] + u[1]*v[1] + u[2]*v[2]
# ...

# ...
class CrossBasic(CalculusFunction):
    """

    Examples
    ========

    """

    nargs = None
    name = 'Cross'

    def __new__(cls, *args, **options):
        # (Try to) sympify args first

        if options.pop('evaluate', True):
            r = cls.eval(*args)
        else:
            r = None

        if r is None:
            return Basic.__new__(cls, *args, **options)
        else:
            return r

class Cross_2d(CrossBasic):
    """

    Examples
    ========

    """

    @classmethod
    def eval(cls, *_args):
        """."""

        if not _args:
            return

        u = _args[0]
        v = _args[1]

        return u[0]*v[1] - u[1]*v[0]

class Cross_3d(CrossBasic):
    """

    Examples
    ========

    """

    def __getitem__(self, indices, **kw_args):
        if is_sequence(indices):
            # Special case needed because M[*my_tuple] is a syntax error.
            return Indexed(self, *indices, **kw_args)
        else:
            return Indexed(self, indices, **kw_args)

    @classmethod
    def eval(cls, *_args):
        """."""

        if not _args:
            return

        u = _args[0]
        v = _args[1]

        return Tuple(u[1]*v[2] - u[2]*v[1],
                     u[2]*v[0] - u[0]*v[2],
                     u[0]*v[1] - u[1]*v[0])
# ...
