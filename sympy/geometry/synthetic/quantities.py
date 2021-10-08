from sympy.core.expr import Expr
from sympy.core.sympify import _sympify
from sympy.combinatorics.permutations import _af_parity
from sympy.core.compatibility import default_sort_key
from sympy.core.singleton import S


class SyntheticGeometryMainVariable(Expr):
    def __new__(cls):
        return super().__new__(cls)

    def _eval_is_real(self):
        return True


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

    def doit(self):
        r"""Evaluate trivial areas and sort the argument of areas.

        Explanation
        ===========

        - $\mathcal{S}_{A, A, A} = 0$
        - $\mathcal{S}_{A, A, B} = 0$
        - $\mathcal{S}_{A, B, A} = 0$
        - $\mathcal{S}_{B, A, A} = 0$

        If $A, B, C$ is the canonical ordering of the points,
        the signed area should reordered as:

        - $\mathcal{S}_{A, C, B} = -\mathcal{S}_{A, B, C}$
        - $\mathcal{S}_{B, A, C} = -\mathcal{S}_{A, B, C}$
        - $\mathcal{S}_{B, C, A} = \mathcal{S}_{A, B, C}$
        - $\mathcal{S}_{C, A, B} = \mathcal{S}_{A, B, C}$
        - $\mathcal{S}_{C, B, A} = -\mathcal{S}_{A, B, C}$
        """
        if len(self.args) == 3 and len(set(self.args)) != 3:
            return S.Zero

        if len(self.args) == 3:
            args = self.args
            args_sorted = tuple(sorted(args, key=default_sort_key))
            if args == args_sorted:
                return self

            permutation = [args_sorted.index(arg) for arg in args]
            parity = _af_parity(permutation)
            if parity == 0:
                return self.func(*args_sorted)
            return -self.func(*args_sorted)
        return self


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

    def doit(self):
        r"""Evaluate trivial length ratios.

        Explanation
        ===========

        - $\frac{\overline{A, A}}{\overline{C, D}} = 0$
        - $\frac{\overline{A, B}}{\overline{A, B}} = 1$
        - $\frac{\overline{A, B}}{\overline{B, A}} = -1$
        """
        if len(self.args) == 4:
            A, B, C, D = self.args
            if A == B:
                return S.Zero
            if A == C and B == D:
                return S.One
            if A == D and B == C:
                return S.NegativeOne

            AA, BB = sorted([A, B], key=default_sort_key)
            CC, DD = sorted([C, D], key=default_sort_key)

            if A == AA and B == BB and C == CC and D == DD:
                return self

            sign = 1
            if A == BB and B == AA:
                sign *= -1
            if C == DD and D == CC:
                sign *= -1

            return sign * self.func(AA, BB, CC, DD)
        return self


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
