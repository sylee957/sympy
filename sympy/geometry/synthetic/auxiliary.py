from sympy.core.expr import Expr
from sympy.core.basic import Basic
from sympy.core.sympify import _sympify


class SyntheticGeometryAuxiliaryRatio(Expr):
    r"""A symbol representating ratio of the signed length of two
    segments $\frac{\overline{A, B}}{\overline{C, D}}$

    Parameters
    ==========

    A, B, C, D : Basic
    """
    def __new__(cls, A, B, C, D):
        A, B, C, D = map(_sympify, (A, B, C, D))
        return super().__new__(cls, A, B, C, D)

    def _eval_is_real(self):
        return True


class SyntheticGeometryAuxiliaryAreaCoordinateO(Basic):
    def __new__(cls):
        return super().__new__(cls)

class SyntheticGeometryAuxiliaryAreaCoordinateU(Basic):
    def __new__(cls):
        return super().__new__(cls)

class SyntheticGeometryAuxiliaryAreaCoordinateV(Basic):
    def __new__(cls):
        return super().__new__(cls)


class SyntheticGeometryAuxiliaryTwolineO1(Basic):
    def __new__(cls):
        return super().__new__(cls)


class SyntheticGeometryAuxiliaryTwolineO2(Basic):
    def __new__(cls):
        return super().__new__(cls)


class SyntheticGeometryAuxiliaryPoint(Basic):
    pass
