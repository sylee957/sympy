from __future__ import print_function, division

from sympy.core import Basic
from sympy.functions import adjoint, conjugate

from .matexpr import MatrixExpr, MatrixElement
from .shape import MatrixShape
from .transpose import transpose, Transpose


class Adjoint(MatrixExpr):
    """
    The Hermitian adjoint of a matrix expression.

    This is a symbolic object that simply stores its argument without
    evaluating it. To actually compute the adjoint, use the ``adjoint()``
    function.

    Examples
    ========

    >>> from sympy.matrices import MatrixSymbol, Adjoint
    >>> from sympy.functions import adjoint
    >>> A = MatrixSymbol('A', 3, 5)
    >>> B = MatrixSymbol('B', 5, 3)
    >>> Adjoint(A*B)
    Adjoint(A*B)
    >>> adjoint(A*B)
    Adjoint(B)*Adjoint(A)
    >>> adjoint(A*B) == Adjoint(A*B)
    False
    >>> adjoint(A*B) == Adjoint(A*B).doit()
    True
    """
    is_Adjoint = True

    def doit(self, **hints):
        arg = self.arg
        if hints.get('deep', True) and isinstance(arg, Basic):
            return adjoint(arg.doit(**hints))
        else:
            return adjoint(self.arg)

    @property
    def arg(self):
        return self.args[0]

    def _eval_matrix_shape(self):
        ret = self.arg._eval_matrix_shape()
        if ret is not None:
            return ret[::-1]

    def _entry(self, i, j, **kwargs):
        if self._eval_matrix_shape() is not None:
            return conjugate(self.arg._entry(j, i, **kwargs))
        return MatrixElement(self, i, j)

    def _eval_adjoint(self):
        if self._eval_matrix_shape() is not None:
            return self.arg
        return Adjoint(self)

    def _eval_conjugate(self):
        if self._eval_matrix_shape() is not None:
            return transpose(self.arg)
        return Adjoint(Transpose(self))

    def _eval_trace(self):
        from sympy.matrices.expressions.trace import Trace
        if self._eval_matrix_shape() is not None:
            return conjugate(Trace(self.arg))
        return Trace(self)

    def _eval_transpose(self):
        if self._eval_matrix_shape() is not None:
            return conjugate(self.arg)
        return Transpose(self)
