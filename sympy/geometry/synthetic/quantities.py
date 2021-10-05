from sympy.core.expr import Expr
from sympy.core.sympify import _sympify


class SyntheticGeometrySignedArea(Expr):
    r"""A signed area of a triangle
    ($\mathcal{S}_{A, B, C}$) or a quadrilateral
    ($\mathcal{S}_{A, B, C, D}$)

    Parameters
    ==========

    points : Basic
    """
    def __new__(cls, *points):
        points = tuple(map(_sympify, points))
        if len(points) not in (3, 4):
            raise ValueError
        return super().__new__(cls, *points)

    def _eval_is_real(self):
        return True


class SyntheticGeometrySignedRatio(Expr):
    r"""A ratio of the signed length of two segments
    ($\frac{\overline{A, B}}{\overline{C, D}}$)

    Parameters
    ==========

    A, B, C, D : Basic
    """
    def __new__(cls, A, B, C, D):
        A, B, C, D = map(_sympify, (A, B, C, D))
        return super().__new__(cls, A, B, C, D)

    def _eval_is_real(self):
        return True


class SyntheticGeometryPythagorasDifference(Expr):
    r"""A Pythagoras difference of a triangle
    ($\mathcal{P}_{A, B, C}$) or a quadrilateral
    ($\mathcal{P}_{A, B, C, D}$)

    Parameters
    ==========

    points : Basic
    """
    def __new__(cls, *points):
        points = tuple(map(_sympify, points))
        if len(points) not in (3, 4):
            raise ValueError
        return super().__new__(cls, *points)

    def _eval_is_real(self):
        return True


class SyntheticGeometryFrozenSignedRatio(Expr):
    def _eval_is_real(self):
        return True
