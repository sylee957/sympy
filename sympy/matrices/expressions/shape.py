from sympy.core.containers import Tuple
from sympy.core.evaluate import global_evaluate
from sympy.core.expr import Expr
from sympy.core.numbers import Integer
from sympy.core.decorators import _sympifyit
from sympy.matrices.matrices import MatrixBase


class MatrixRows(Expr):
    @_sympifyit('mat')
    def __new__(cls, mat, evaluate=global_evaluate[0]):
        if not mat.is_Matrix:
            raise TypeError("{} must be a matrix.".format(mat))

        if not evaluate:
            return Expr.__new__(cls, mat)

        if isinstance(mat, MatrixBase):
            return Integer(mat.rows)

        dispatch = getattr(mat, '_eval_matrix_shape', None)
        if dispatch:
            ret = dispatch()
            if ret is not None:
                return ret[0]

        return Expr.__new__(cls, mat)


class MatrixCols(Expr):
    @_sympifyit('mat')
    def __new__(cls, mat, evaluate=global_evaluate[0]):
        if not mat.is_Matrix:
            raise TypeError("{} must be a matrix.".format(mat))

        if not evaluate:
            return Expr.__new__(cls, mat)

        if isinstance(mat, MatrixBase):
            return Integer(mat.cols)

        dispatch = getattr(mat, '_eval_matrix_shape', None)
        if dispatch:
            ret = dispatch()
            if ret is not None:
                return ret[1]

        return Expr.__new__(cls, mat)


class MatrixShape(Tuple):
    @_sympifyit('mat')
    def __new__(cls, mat, evaluate=global_evaluate[0]):
        if not mat.is_Matrix:
            raise TypeError("{} must be a matrix.".format(mat))

        if not evaluate:
            return Tuple.__new__(cls, mat)

        return Tuple(MatrixRows(mat), MatrixCols(mat))