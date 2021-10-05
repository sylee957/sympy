from sympy.core.expr import Expr
from sympy.core.sympify import _sympify
from sympy.core.singleton import S
from sympy.core.compatibility import default_sort_key
from sympy.combinatorics.permutations import _af_parity


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
        r"""Simplify and uniformize area

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
        if len(self.args) == 3:
            if len(set(self.args)) != 3:
                return S.Zero

            args = self.args
            args_sorted = tuple(sorted(args, key=default_sort_key))
            if args == args_sorted:
                return self
            permutation = [args_sorted.index(arg) for arg in args]
            parity = _af_parity(permutation)
            if parity == 0:
                return self.func(*args_sorted)
            return -self.func(*args_sorted)

        if len(self.args) == 4:
            A, B, C, D = self.args
            if A == B:
                return self.func(B, C, D).doit()
            if B == C:
                return self.func(A, B, D).doit()
            if C == D:
                return self.func(A, B, C).doit()
            if D == A:
                return self.func(A, B, C).doit()
            if A == C:
                return S.Zero
            if B == D:
                return S.Zero

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
        r"""Simplify and uniformize ratio

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


    def doit(self):
        r"""Simplify and uniformize pythagoras difference

        Explanation
        ===========

        If $A, B$ is the canonical ordering of the points,
        the pythagoras difference should reordered as
        $\mathcal{P}_{B, A, B} = \mathcal{P}_{A, B, A}$

        If $A, C$ is the canonical ordering of the points,
        the pythagoras difference should reordered as
        $\mathcal{P}_{C, B, A} = \mathcal{P}_{A, B, C}$
        """
        if len(self.args) == 3:
            A, B, C = self.args

            if A == B:
                return S.Zero
            elif B == C:
                return S.Zero

            if A == C:
                AA, BB = sorted([A, B], key=default_sort_key)
                if (A, B) != (AA, BB):
                    return self.func(AA, BB, AA)
            else:
                AA, CC = sorted([A, C], key=default_sort_key)
                if (A, C) != (AA, CC):
                    return self.func(AA, B, CC)

        elif len(self.args) == 4:
            A, B, C, D = self.args
            if A == C:
                return S.Zero
            if B == D:
                return S.Zero
            if B == C:
                return self.func(A, B, D).doit()
            if A == B:
                return -self.func(C, A, D).doit()
            if C == D:
                return -self.func(A, C, B).doit()
            if A == D:
                return self.func(B, A, C).doit()

        return self


class SyntheticGeometrySignedLength(Expr):
    r"""A signed length of the segment
    ($\overline{A, B}$)

    Parameters
    ==========

    A, B
    """
    def __new__(cls, A, B):
        A, B = map(_sympify, (A, B))
        return super().__new__(cls, A, B)

    def _eval_is_real(self):
        return True

    def doit(self):
        r"""Simplify and uniformize length

        Explanation
        ===========

        - $\overline{A, A} = 0$
        - $\overline{B, A} = -\overline{B, A}$
        """
        if len(self.args) == 2:
            A, B = self.args

            if A == B:
                return S.Zero
            AA, BB = sorted([A, B], key=default_sort_key)
            if A == BB and B == AA:
                return -self.func(AA, BB)
        return self


class SyntheticGeometryAreaCoordinateX(Expr):
    r"""
    .. math::
        \mathcal{X}_{P} =
        \frac{\mathcal{S}_{O, U, P}}{\mathcal{S}_{O, U, V}}
    """
    def __new__(cls, O, U, V, P):
        P = _sympify(P)
        return super().__new__(cls, O, U, V, P)

    def _eval_is_real(self):
        return True

    def doit(self):
        O, U, V, P = self.args
        if P == O:
            return S.Zero
        elif P == U:
            return S.Zero
        elif P == V:
            return S.One
        return self


class SyntheticGeometryAreaCoordinateY(Expr):
    r"""
    .. math::
        \mathcal{Y}_{P} =
        \frac{\mathcal{S}_{V, O, P}}{\mathcal{S}_{O, U, V}}
    """
    def __new__(cls, O, U, V, P):
        P = _sympify(P)
        return super().__new__(cls, O, U, V, P)

    def _eval_is_real(self):
        return True

    def doit(self):
        O, U, V, P = self.args
        if P == O:
            return S.Zero
        elif P == U:
            return S.One
        elif P == V:
            return S.Zero
        return self


def tan(*args):
    if len(args) == 3:
        A, B, C = args
        Area = SyntheticGeometrySignedArea
        Pythagoras = SyntheticGeometryPythagorasDifference
        return 4 * Area(C, B, A) / Pythagoras(C, B, A)
    elif len(args) == 4:
        A, B, C, D = args
        Area = SyntheticGeometrySignedArea
        Pythagoras = SyntheticGeometryPythagorasDifference
        return 4 * Area(A, C, B, D) / Pythagoras(A, D, B, C)
    raise ValueError
