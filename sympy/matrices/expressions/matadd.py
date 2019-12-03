from __future__ import print_function, division

from sympy.core.compatibility import reduce
from operator import add

from sympy.core import Add, Basic, sympify
from sympy.core.cache import cacheit
from sympy.core.containers import Tuple
from sympy.core.logic import fuzzy_bool, fuzzy_and
from sympy.core.relational import Eq
from sympy.functions import adjoint
from sympy.logic.boolalg import And
from sympy.matrices.matrices import MatrixBase
from sympy.strategies import (rm_id, unpack, flatten, sort, condition,
    exhaust, do_one, glom)
from sympy.utilities import default_sort_key, sift

from .adjoint import Adjoint
from .matexpr import \
    MatrixExpr, ShapeError, ZeroMatrix, GenericZeroMatrix, MatrixElement
from .shape import MatrixShape
from .transpose import transpose, Transpose


# XXX: MatAdd should perhaps not subclass directly from Add
class MatAdd(MatrixExpr, Add):
    """A Sum of Matrix Expressions

    MatAdd inherits from and operates like SymPy Add

    Examples
    ========

    >>> from sympy import MatAdd, MatrixSymbol
    >>> A = MatrixSymbol('A', 5, 5)
    >>> B = MatrixSymbol('B', 5, 5)
    >>> C = MatrixSymbol('C', 5, 5)
    >>> MatAdd(A, B, C)
    A + B + C
    """
    is_MatAdd = True

    identity = GenericZeroMatrix()

    def __new__(cls, *args, **kwargs):
        if not args:
            return cls.identity

        # This must be removed aggressively in the constructor to avoid
        # TypeErrors from GenericZeroMatrix().shape
        args = filter(lambda i: cls.identity != i, args)
        args = list(map(sympify, args))
        check = kwargs.get('check', False)

        obj = Basic.__new__(cls, *args)
        if check:
            if all(not isinstance(i, MatrixExpr) for i in args):
                return Add.fromiter(args)

            if not all(arg.is_Matrix for arg in args):
                raise TypeError("Mix of Matrix and Scalar symbols")

            if obj._is_shape_aligned_predicate() == False:
                raise ShapeError("Matrices are not aligned")
        return obj

    @cacheit
    def _is_shape_aligned_predicate(self):
        A = self.args[0]
        new_args = (Eq(A.shape, B.shape) for B in self.args[1:])
        return And(*new_args)

    def _eval_matrix_shape(self):
        if self._is_shape_aligned_predicate() == True:
            return self.args[0]._eval_matrix_shape()

    def _entry(self, i, j, **kwargs):
        if self._is_shape_aligned_predicate() == True:
            return Add(*[arg._entry(i, j, **kwargs) for arg in self.args])
        return MatrixElement(self, i, j)

    def _eval_transpose(self):
        if self._is_shape_aligned_predicate() == True:
            return MatAdd(*[transpose(arg) for arg in self.args]).doit()
        return Transpose(self)

    def _eval_adjoint(self):
        if self._is_shape_aligned_predicate() == True:
            return MatAdd(*[adjoint(arg) for arg in self.args]).doit()
        return Adjoint(self)

    def _eval_trace(self):
        from .trace import trace, Trace
        if self._is_shape_aligned_predicate() == True:
            return Add(*[trace(arg) for arg in self.args]).doit()
        return Trace(self)

    def doit(self, **kwargs):
        deep = kwargs.get('deep', True)
        if deep:
            args = [arg.doit(**kwargs) for arg in self.args]
        else:
            args = self.args

        if self._is_shape_aligned_predicate() == True:
            return canonicalize(MatAdd(*args))
        return self

    def _eval_derivative_matrix_lines(self, x):
        if self._is_shape_aligned_predicate() == True:
            add_lines = [
                arg._eval_derivative_matrix_lines(x) for arg in self.args]
            return [j for i in add_lines for j in i]
        raise NotImplementedError


factor_of = lambda arg: arg.as_coeff_mmul()[0]
matrix_of = lambda arg: unpack(arg.as_coeff_mmul()[1])
def combine(cnt, mat):
    if cnt == 1:
        return mat
    else:
        return cnt * mat


def merge_explicit(matadd):
    """ Merge explicit MatrixBase arguments

    Examples
    ========

    >>> from sympy import MatrixSymbol, eye, Matrix, MatAdd, pprint
    >>> from sympy.matrices.expressions.matadd import merge_explicit
    >>> A = MatrixSymbol('A', 2, 2)
    >>> B = eye(2)
    >>> C = Matrix([[1, 2], [3, 4]])
    >>> X = MatAdd(A, B, C)
    >>> pprint(X)
        [1  0]   [1  2]
    A + [    ] + [    ]
        [0  1]   [3  4]
    >>> pprint(merge_explicit(X))
        [2  2]
    A + [    ]
        [3  5]
    """
    groups = sift(matadd.args, lambda arg: isinstance(arg, MatrixBase))
    if len(groups[True]) > 1:
        return MatAdd(*(groups[False] + [reduce(add, groups[True])]))
    else:
        return matadd


rules = (rm_id(lambda x: x == 0 or isinstance(x, ZeroMatrix)),
         unpack,
         flatten,
         glom(matrix_of, factor_of, combine),
         merge_explicit,
         sort(default_sort_key))

canonicalize = exhaust(condition(lambda x: isinstance(x, MatAdd),
                                 do_one(*rules)))
