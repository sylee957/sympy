from sympy.core.basic import Basic
from sympy.core.sympify import _sympify


class SyntheticGeometryConstruction(Basic):
    pass


class SyntheticGeometryPrimitive(Basic):
    pass


class SyntheticGeometryOn(SyntheticGeometryConstruction):
    r"""Take a point $Y$ on either a :class:`SyntheticGeometryLine`,
    :class:`SyntheticGeometryPLine`, :class:`SyntheticGeometryTLine`,
    :class:`SyntheticGeometryBLine`, :class:`SyntheticGeometryCircle`.
    """
    def __new__(cls, Y, obj):
        return super().__new__(cls, Y, obj)

    def __str__(self):
        Y, line = self.args
        return f"Take a point {Y} on {line}"


class SyntheticGeometryLine(SyntheticGeometryPrimitive):
    r"""A line passing through two points $U$ and $V$.
    The nondegenerate condition is $U \ne V$.
    """
    def __new__(cls, U, V):
        U = _sympify(U)
        V = _sympify(V)
        return super().__new__(cls, U, V)

    def __str__(self):
        A, B = self.args
        return f"line {A}{B}"


class SyntheticGeometryPLine(SyntheticGeometryConstruction):
    r"""A line passing through a point $W$ and parallel to $Line(U, V)$.
    The nondegenerate condition is $U \ne V$.
    """
    def __new__(cls, W, U, V):
        W = _sympify(W)
        U = _sympify(U)
        V = _sympify(V)
        return super().__new__(cls, W, U, V)

    def __str__(self):
        A, B, C = self.args
        return f"line passing through {A} and parallel to {B}{C}"


class SyntheticGeometryTLine(SyntheticGeometryConstruction):
    r"""A line passing through a point $W$ and perpendicular to
    $Line(U, V)$. The nondegenerate condition is $U \ne V$.
    """
    def __new__(cls, W, U, V):
        W = _sympify(W)
        U = _sympify(U)
        V = _sympify(V)
        return super().__new__(cls, W, U, V)


class SyntheticGeometryBLine(SyntheticGeometryPrimitive):
    r"""Perpendicular bisector of $Line(U, V)$.
    The nondegenerate condition is $U \ne V$.
    """
    def __new__(cls, U, V):
        U = _sympify(U)
        V = _sympify(V)
        return super().__new__(cls, U, V)


class SyntheticGeometryCircle(SyntheticGeometryPrimitive):
    r"""A circle with point $O$ as its center and passing through point $U$.
    """
    def __new__(cls, O, U):
        O = _sympify(O)
        U = _sympify(U)
        return super().__new__(cls, O, U)


class SyntheticGeometryLRatio(SyntheticGeometryConstruction):
    r"""$LRatio(Y, Line(P, Q), \lambda)$

    Construct a new point $Y$ on line $PQ$ such that
    $\frac{\overline{PY}}{\overline{PQ}} = \lambda$
    """
    def __new__(cls, Y, L, l):
        Y = _sympify(Y)
        L = _sympify(L)
        l = _sympify(l)
        return super().__new__(cls, Y, L, l)


class SyntheticGeometryPRatio(SyntheticGeometryConstruction):
    r"""$PRatio(Y, R, Line(P, Q), \lambda)$

    Construct a new point $Y$ such that
    $\frac{\overline{RY}}{\overline{PQ}} = \lambda$ and $RY \parallel PQ$
    """
    def __new__(cls, Y, W, L, l):
        Y = _sympify(Y)
        W = _sympify(W)
        L = _sympify(L)
        l = _sympify(l)
        return super().__new__(cls, Y, W, L, l)


class SyntheticGeometryTRatio(SyntheticGeometryConstruction):
    r"""$TRatio(Y, Line(P, Q), \lambda)$"""
    def __new__(cls, Y, L, l):
        Y = _sympify(Y)
        L = _sympify(L)
        l = _sympify(l)
        return super().__new__(cls, Y, L, l)


class SyntheticGeometryIntersection(SyntheticGeometryConstruction):
    r"""$Inter(Y, A, B)$ where A, B are either

    - $Line(P, Q)$ and $Line(U, V)$
    - $PLine(R, P, Q)$ and $Line(U, V)$
    - $PLine(R, P, Q)$ and $PLine(W, U, V)$

    Construct a new point $Y$ such that $Y = L1 \cap L2$
    """
    def __new__(cls, Y, A, B):
        Y = _sympify(Y)
        A = _sympify(A)
        B = _sympify(B)
        return super().__new__(cls, Y, A, B)


class SyntheticGeometryMidpoint(SyntheticGeometryConstruction):
    r"""$Midpoint(Y, Line(U, V))$"""
    def __new__(cls, Y, L):
        Y = _sympify(Y)
        L = _sympify(L)
        return super().__new__(cls, Y, L)


class SyntheticGeometryFoot(SyntheticGeometryConstruction):
    r"""$Foot(Y, P, Line(U, V))$"""
    def __new__(cls, Y, P, L):
        Y = _sympify(Y)
        P = _sympify(P)
        L = _sympify(L)
        return super().__new__(cls, Y, P, L)
