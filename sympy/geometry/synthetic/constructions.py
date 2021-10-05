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
    r"""$LRatio(Y, P, Q, \lambda)$

    Construct a new point $Y$ on line $PQ$ such that
    $\frac{\overline{PY}}{\overline{PQ}} = \lambda$
    """
    def __new__(cls, Y, U, V, l):
        Y = _sympify(Y)
        U = _sympify(U)
        V = _sympify(V)
        l = _sympify(l)
        return super().__new__(cls, Y, U, V, l)

    def __str__(self):
        Y, P, Q, l = self.args
        return f"Take a point {Y} on line {P}{Q} such that {P}{Y}/{P}{Q} = {l}"


class SyntheticGeometryPRatio(SyntheticGeometryConstruction):
    r"""$PRatio(Y, R, P, Q, \lambda)$

    Construct a new point $Y$ such that
    $\frac{\overline{RY}}{\overline{PQ}} = \lambda$ and $RY \parallel PQ$
    """
    def __new__(cls, Y, W, U, V, l):
        Y = _sympify(Y)
        W = _sympify(W)
        U = _sympify(U)
        V = _sympify(V)
        l = _sympify(l)
        return super().__new__(cls, Y, W, U, V, l)

    def __str__(self):
        Y, R, P, Q, l = self.args
        return f"Take a point {Y} on a line passing through {R} and parallel to {P}{Q} such that {R}{Y}/{P}{Q} = {l}"


class SyntheticGeometryTRatio(SyntheticGeometryConstruction):
    def __new__(cls, Y, U, V, l):
        Y = _sympify(Y)
        U = _sympify(U)
        V = _sympify(V)
        l = _sympify(l)
        return super().__new__(cls, Y, U, V, l)


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

    def __str__(self):
        Y, L1, L2 = self.args
        return f"Take a point {Y} as an intersection of {L1} and {L2}"


class SyntheticGeometryMidpoint(SyntheticGeometryConstruction):
    def __new__(cls, Y, U, V):
        Y = _sympify(Y)
        U = _sympify(U)
        V = _sympify(V)
        return super().__new__(cls, Y, U, V)

    def __str__(self):
        Y, U, V = self.args
        return f"Take a point {Y} as a midpoint of {U}{V}"


class SyntheticGeometryFoot(SyntheticGeometryConstruction):
    def __new__(cls, Y, P, U, V):
        Y = _sympify(Y)
        P = _sympify(P)
        U = _sympify(U)
        V = _sympify(V)
        return super().__new__(cls, Y, P, U, V)
