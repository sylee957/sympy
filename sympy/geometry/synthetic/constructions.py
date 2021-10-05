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


class SyntheticGeometryALine(SyntheticGeometryPrimitive):
    r"""A line $l$ passing through $P$ such that
    $\angle[PQ, l] = \angle[UW, WV]$
    """
    def __new__(cls, P, Q, W, U, V):
        P = _sympify(P)
        Q = _sympify(Q)
        W = _sympify(W)
        U = _sympify(U)
        V = _sympify(V)
        return super().__new__(cls, P, Q, W, U, V)


class SyntheticGeometryCircle(SyntheticGeometryPrimitive):
    r"""A circle with point $O$ as its center and passing through point $U$.
    """
    def __new__(cls, O, U):
        O = _sympify(O)
        U = _sympify(U)
        return super().__new__(cls, O, U)


class SyntheticGeometryLRatio(SyntheticGeometryConstruction):
    r"""$LRatio(Y, P, Q, r)$

    Construct a new point $Y$ on line $PQ$ such that
    $\frac{\overline{PY}}{\overline{PQ}} = \lambda$
    """
    def __new__(cls, Y, P, Q, r):
        Y = _sympify(Y)
        P = _sympify(P)
        Q = _sympify(Q)
        r = _sympify(r)
        return super().__new__(cls, Y, P, Q, r)


class SyntheticGeometryMRatio(SyntheticGeometryConstruction):
    r"""$MRatio(Y, U, V, r)$

    Construct a new point $Y$ such that
    $\frac{\overline{UY}}{\overline{YV}} = r$
    """
    def __new__(cls, Y, U, V, r):
        Y = _sympify(Y)
        U = _sympify(U)
        V = _sympify(V)
        r = _sympify(r)
        return super().__new__(cls, Y, U, V, r)


class SyntheticGeometryPRatio(SyntheticGeometryConstruction):
    r"""$PRatio(Y, R, P, Q, r)$

    Construct a new point $Y$ such that
    $\frac{\overline{RY}}{\overline{PQ}} = r$ and $RY \parallel PQ$
    """
    def __new__(cls, Y, W, U, V, r):
        Y = _sympify(Y)
        W = _sympify(W)
        U = _sympify(U)
        V = _sympify(V)
        r = _sympify(r)
        return super().__new__(cls, Y, W, U, V, r)


class SyntheticGeometryTRatio(SyntheticGeometryConstruction):
    r"""$TRatio(Y, P, Q, r)$"""
    def __new__(cls, Y, P, Q, r):
        Y = _sympify(Y)
        P = _sympify(P)
        Q = _sympify(Q)
        r = _sympify(r)
        return super().__new__(cls, Y, P, Q, r)


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
    r"""$Midpoint(Y, U, V)$"""
    def __new__(cls, Y, U, V):
        Y = _sympify(Y)
        U = _sympify(U)
        V = _sympify(V)
        return super().__new__(cls, Y, U, V)


class SyntheticGeometryFoot(SyntheticGeometryConstruction):
    r"""$Foot(Y, P, U, V)$"""
    def __new__(cls, Y, P, U, V):
        Y = _sympify(Y)
        P = _sympify(P)
        U = _sympify(U)
        V = _sympify(V)
        return super().__new__(cls, Y, P, U, V)


class SyntheticGeometryInversion(SyntheticGeometryConstruction):
    """Inversion(P, Q, O, A)"""
    def __new__(cls, P, Q, O, A):
        P = _sympify(P)
        Q = _sympify(Q)
        O = _sympify(O)
        A = _sympify(A)
        return super().__new__(cls, P, Q, O, A)


class SyntheticGeometryARatio(SyntheticGeometryConstruction):
    """ARatio(Y, O, U, V, r_o, r_u, r_v)"""
    def __new__(cls, Y, O, U, V, r_o, r_u, r_v):
        Y = _sympify(Y)
        O = _sympify(O)
        U = _sympify(U)
        V = _sympify(V)
        r_o = _sympify(r_o)
        r_u = _sympify(r_u)
        r_v = _sympify(r_v)
        return super().__new__(cls, Y, O, U, V, r_o, r_u, r_v)


class SyntheticGeometryCentroid(SyntheticGeometryConstruction):
    """Centroid(Y, A, B, C)"""
    def __new__(cls, Y, O, U, V):
        Y = _sympify(Y)
        O = _sympify(O)
        U = _sympify(U)
        V = _sympify(V)
        return super().__new__(cls, Y, O, U, V)


class SyntheticGeometryOrthocenter(SyntheticGeometryConstruction):
    """Orthocenter(Y, A, B, C)"""
    def __new__(cls, Y, O, U, V):
        Y = _sympify(Y)
        O = _sympify(O)
        U = _sympify(U)
        V = _sympify(V)
        return super().__new__(cls, Y, O, U, V)


class SyntheticGeometryCircumcenter(SyntheticGeometryConstruction):
    """Circumcenter(Y, A, B, C)"""
    def __new__(cls, Y, O, U, V):
        Y = _sympify(Y)
        O = _sympify(O)
        U = _sympify(U)
        V = _sympify(V)
        return super().__new__(cls, Y, O, U, V)


class SyntheticGeometryIncenter(SyntheticGeometryConstruction):
    """Circumcenter(C, I, A, B)"""
    def __new__(cls, C, I, A, B):
        C = _sympify(C)
        I = _sympify(I)
        A = _sympify(A)
        B = _sympify(B)
        return super().__new__(cls, C, I, A, B)
