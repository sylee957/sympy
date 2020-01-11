from sympy.core.compatibility import as_int
from sympy.core.sympify import _sympify
from .matexpr import MatrixExpr


class MinorSubmatrix(MatrixExpr):
    def __new__(cls, m, i, j):
        m = _sympify(m)
        if m.is_Matrix is not True:
            raise ValueError(f"{m} should be a matrix.")

        i, j = _sympify(i), _sympify(j)
        if i.is_integer is False or j.is_integer is False:
            raise ValueError(f"{i}, {j} should be integers.")

        return super(MinorSubmatrix, cls).__new__(cls, m, i, j)

    @property
    def shape(self):
        rows, cols = self.args[0].shape
        return rows-1, cols-1

    def _eval_rewrite_as_MatrixSlice(self, *args, **kwargs):
        from .slice import MatrixSlice

        rows, cols = self.shape
        m, i, j = self.args
        if i == 0 and j == 0:
            return MatrixSlice(m, (1, rows), (1, cols))
        elif i == rows and j == cols:
            return MatrixSlice(m, (0, rows-1), (0, cols-1))
