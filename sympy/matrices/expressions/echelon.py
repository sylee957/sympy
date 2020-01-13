from sympy.core.sympify import _sympify
from sympy.matrices.matrices import MatrixBase
from sympy.utilities.iterables import sift

from .matexpr import MatrixExpr


class RREF(MatrixExpr):
    """A symbolic representation of a matrix RREF

    Examples
    ========

    RREF of a zero matrix:

    >>> from sympy.matrices.expressions import RREF
    >>> from sympy.matrices.expressions import ZeroMatrix, OneMatrix
    >>> m = ZeroMatrix(3, 4)
    >>> RREF(m).doit()
    0

    RREF of an identity matrix:

    >>> from sympy.matrices.expressions import Identity
    >>> RREF(Identity(3)).doit()
    I

    RREF of a permutation matrix:

    >>> from sympy.combinatorics import Permutation
    >>> from sympy.matrices.expressions import PermutationMatrix
    >>> p = Permutation(0, 1, 2)
    >>> P = PermutationMatrix(p)
    >>> RREF(P).doit()
    I

    RREF of a matrix symbol:

    >>> from sympy.matrices.expressions import MatrixSymbol
    >>> A = MatrixSymbol('A', 3, 3)
    >>> RREF(RREF(A)).doit()
    RREF(A)
    """
    def __new__(cls, m):
        m = _sympify(m)
        if not m.is_Matrix:
            raise ValueError("{} must be a matrix".format(m))

        return super(RREF, cls).__new__(cls, m)

    @property
    def shape(self):
        return self.args[0].shape


    def doit(self, deep=True, **kwargs):
        from sympy.matrices.dense import Matrix

        from .matexpr import Identity, ZeroMatrix, OneMatrix
        from .permutation import PermutationMatrix
        from .blockmatrix import BlockMatrix
        from .diagonal import DiagMatrix
        from .fourier import DFT

        m = self.args[0]
        if deep:
            m = m.doit(deep=deep)

        # XXX Matrix.rref can be logically flawed regarding zero
        # divisions.
        if isinstance(m, MatrixBase):
            rref, _ = m.rref()
            return rref

        if isinstance(m, RREF):
            return m.doit(deep=deep)

        if m.is_Identity:
            return Identity(m.rows)

        if isinstance(m, (PermutationMatrix, DFT)):
            return Identity(m.rows)

        if isinstance(m, ZeroMatrix):
            return m

        # XXX Where to put stuff like
        # RREF(OneMatrix) => BlockMatrix([OneMatrix, ZeroMatrix])

        return self