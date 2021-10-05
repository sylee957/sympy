from sympy.core.basic import Basic


class AffineECS2(Basic):
    """Take the intersection Y of line PQ and line UV. Point Y is a
    fixed point. The ndg condition is that P , Q, U , V, and the lines
    PQ and UV have one and only one common point, i.e., PQ ∦ UV.
    """
    def __new__(cls, Y, P, Q, U, V):
        return super().__new__(cls, Y, P, Q, U, V)


class AffineECS4(Basic):
    """Take the intersection Y of line UV and the line passing
    through R and parallel to line PQ. Point Y is a fixed point.
    The ndg condition is that PQ ∦ UV.
    """
    def __new__(cls, Y, U, V, R, P, Q):
        return super().__new__(cls, Y, U, V, R, P, Q)


class AffineECS5(Basic):
    """Take the intersection Y of the line passing through point
    R and parallel to PQ and the line passing through point
    W and parallel to line UV. Point Y is a fixed point. The ndg
    condition is that PQ ∦ UV.
    """
    def __new__(cls, Y, W, U, V, R, P, Q):
        return super().__new__(cls, Y, W, U, V, R, P, Q)


class PlaneECS1(Basic):
    """Construction of a point Y such that it is the intersection of two
    lines (LINE U V) and (LINE P Q).
    This construction step is denoted by (INTER Y U V P Q)
    """
    def __new__(cls, Y, U, V, P, Q):
        return super().__new__(cls, Y, U, V, P, Q)


class PlaneECS5(Basic):
    """Inter(Y, Line(U, V), PLine(R, P, Q))"""
    def __new__(cls, Y, U, V, R, P, Q):
        return super().__new__(cls, Y, U, V, R, P, Q)


class PlaneECS6(Basic):
    """Inter(Y, Line(U, V), TLine(R, P, Q))"""
    def __new__(cls, Y, U, V, R, P, Q):
        return super().__new__(cls, Y, U, V, R, P, Q)


class PlaneECS7(Basic):
    """Inter(Y, Line(U, V), BLine(P, Q))"""
    def __new__(cls, Y, U, V, P, Q):
        return super().__new__(cls, Y, U, V, P, Q)


class PlaneECS8(Basic):
    """Inter(Y, Line(U, V), Circle(O, U))"""
    def __new__(cls, Y, U, V, O):
        return super().__new__(cls, Y, U, V, O)
