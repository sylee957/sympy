from __future__ import print_function, division

from sympy.core import Basic, Expr
from sympy.core.cache import cacheit
from sympy.core.relational import Eq
from sympy.core.sympify import _sympify
from sympy.logic.boolalg import And, Or
from sympy.matrices.expressions.transpose import transpose
from sympy.strategies.core import condition


class DotProduct(Expr):
    """
    Dot product of vector matrices

    The input should be two 1 x n or n x 1 matrices. The output represents the
    scalar dotproduct.

    This is similar to using MatrixElement and MatMul, except DotProduct does
    not require that one vector to be a row vector and the other vector to be
    a column vector.

    >>> from sympy import MatrixSymbol, DotProduct
    >>> A = MatrixSymbol('A', 1, 3)
    >>> B = MatrixSymbol('B', 1, 3)
    >>> DotProduct(A, B)
    DotProduct(A, B)
    >>> DotProduct(A, B).doit()
    A[0, 0]*B[0, 0] + A[0, 1]*B[0, 1] + A[0, 2]*B[0, 2]
    """

    def __new__(cls, arg1, arg2):
        arg1, arg2 = _sympify((arg1, arg2))

        if not arg1.is_Matrix:
            raise TypeError("Argument 1 of DotProduct is not a matrix")
        if not arg2.is_Matrix:
            raise TypeError("Argument 2 of DotProduct is not a matrix")

        obj = Basic.__new__(cls, arg1, arg2)
        if obj._is_valid_predicate() == False:
            raise TypeError("The shape is not aligned for the dot product.")
        return obj


    @cacheit
    def _is_valid_predicate(self):
        arg1, arg2 = self.args
        pred1 = Or(Eq(arg1.rows, 1), Eq(arg1.cols, 1))
        pred2 = Or(Eq(arg2.rows, 1), Eq(arg2.cols, 1))
        pred3 = Or(
            And(Eq(arg1.rows, arg2.rows), Eq(arg1.cols, arg2.cols)),
            And(Eq(arg1.rows, arg2.cols), Eq(arg1.cols, arg2.rows))
        )

        return And(pred1, pred2, pred3)


    def doit(self, expand=False):
        if self._is_valid_predicate() != True:
            return self

        if self.args[0].shape == self.args[1].shape:
            if self.args[0].shape[0] == 1:
                mul = self.args[0]*transpose(self.args[1])
            else:
                mul = transpose(self.args[0])*self.args[1]
        else:
            if self.args[0].shape[0] == 1:
                mul = self.args[0]*self.args[1]
            else:
                mul = transpose(self.args[0])*transpose(self.args[1])

        return mul[0]
