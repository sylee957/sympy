from sympy.logic.boolalg import Boolean
from sympy.core.sympify import _sympify


class SyntheticGeometryCollinear(Boolean):
    pass


class SyntheticGeometryParallel(Boolean):
    pass


class SyntheticGeometryEqpoints(Boolean):
    pass


class SyntheticGeometryPerpendicular(Boolean):
    r"""$A, B \perp C, D$"""
    def __new__(cls, A, B, C, D):
        A = _sympify(A)
        B = _sympify(B)
        C = _sympify(C)
        D = _sympify(D)
        return super().__new__(cls, A, B, C, D)


class SyntheticGeometryHarmonic(Boolean):
    r"""$A, B \perp C, D$"""
    def __new__(cls, A, B, C, D):
        A = _sympify(A)
        B = _sympify(B)
        C = _sympify(C)
        D = _sympify(D)
        return super().__new__(cls, A, B, C, D)



class SyntheticGeometryEqdistance(Boolean):
    r"""
    .. math::
        \overline{A, B}^{2} = \overline{C, D}^{2}
    """
    def __new__(cls, A, B, C, D):
        A = _sympify(A)
        B = _sympify(B)
        C = _sympify(C)
        D = _sympify(D)
        return super().__new__(cls, A, B, C, D)


class SyntheticGeometryEqangle(Boolean):
    r"""
    .. math::
        \angle[A, B, C] = \angle[D, E, F]
    """
    def __new__(cls, A, B, C, D, E, F):
        A = _sympify(A)
        B = _sympify(B)
        C = _sympify(C)
        D = _sympify(D)
        E = _sympify(E)
        F = _sympify(F)
        return super().__new__(cls, A, B, C, D, E, F)


class SyntheticGeometryCocircle(Boolean):
    r"""
    .. math::
        \angle[C, A, D] = \angle[C, B, D]
    """
    def __new__(cls, A, B, C, D):
        A = _sympify(A)
        B = _sympify(B)
        C = _sympify(C)
        D = _sympify(D)
        return super().__new__(cls, A, B, C, D)
