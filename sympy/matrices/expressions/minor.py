from sympy.core.compatibility import as_int
from sympy.core.sympify import _sympify
from .matexpr import MatrixExpr


class MinorSubmatrix(MatrixExpr):
    def __new__(cls, i, j):
        i, j = _sympify(i), _sympify(j)
        if i.is_integer is False or j.is_integer is False:
            raise ValueError(f"{i}, {j} should be integers.")

        return super(MinorSubmatrix, cls).__new__(cls, i, j)

    def _eval_rewrite_as_MatrixSlice(self, *args, **kwargs):
        rows, cols = self.shape
        i, j = self.args
        pass
