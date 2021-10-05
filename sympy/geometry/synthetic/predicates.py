from sympy.logic.boolalg import Boolean
from sympy.core.sympify import _sympify


class SyntheticGeometryCollinear(Boolean):
    pass


class SyntheticGeometryParallel(Boolean):
    pass


class SyntheticGeometrySamePoints(Boolean):
    pass


class SyntheticGeometryPerpendicular(Boolean):
    r"""$A, B \perp C, D$"""
    def __new__(cls, A, B, C, D):
        A = _sympify(A)
        B = _sympify(B)
        C = _sympify(C)
        D = _sympify(D)
        return super().__new__(cls, A, B, C, D)


class SyntheticGeometryEqDistance(Boolean):
    r"""|\overline{A, B}| = |\overline{C, D}|"""
    def __new__(cls, A, B, C, D):
        A = _sympify(A)
        B = _sympify(B)
        C = _sympify(C)
        D = _sympify(D)
        return super().__new__(cls, A, B, C, D)
