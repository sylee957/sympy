from sympy.matrices import Matrix
from sympy.matrices.expressions.shape import \
    MatrixRows, MatrixCols, MatrixShape


def test_explicit_matrices():
    m = Matrix([[1, 2], [3, 4], [5, 6]])
    assert MatrixRows(m) == 3
    assert MatrixCols(m) == 2
    assert MatrixShape(m) == (3, 2)
