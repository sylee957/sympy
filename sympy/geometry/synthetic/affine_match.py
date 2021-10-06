from sympy.geometry.synthetic.constructions import (
    SyntheticGeometryLRatio as LRatio,
    SyntheticGeometryPRatio as PRatio,
    SyntheticGeometryIntersection as Intersection,
    SyntheticGeometryLine as Line,
    SyntheticGeometryPLine as PLine,
)


def _match_lratio(C):
    if not isinstance(C, LRatio):
        return None
    Y, L, r = C.args
    if not isinstance(L, Line):
        return None
    P, Q = L.args
    return Y, P, Q, r


def _match_pratio(C):
    if not isinstance(C, PRatio):
        return None
    Y, R, L, r = C.args
    if not isinstance(L, Line):
        return None
    P, Q = L.args
    return Y, R, P, Q, r


def _match_inter_line_line(C):
    if not isinstance(C, Intersection):
        return None
    Y, L1, L2 = C.args
    if not isinstance(L1, Line):
        return None
    P, Q = L1.args
    if not isinstance(L2, Line):
        return None
    U, V = L2.args
    return Y, P, Q, U, V


def _match_inter_pline_line(C):
    if not isinstance(C, Intersection):
        return None
    Y, L1, L2 = C.args
    if isinstance(L1, Line) and isinstance(L2, PLine):
        return _match_inter_pline_line(Intersection(Y, L2, L1))
    if not (isinstance(L1, PLine) and isinstance(L2, Line)):
        return None
    R, P, Q = L1.args
    U, V = L2.args
    return Y, R, P, Q, U, V


def _match_inter_pline_pline(C):
    if not isinstance(C, Intersection):
        return None
    Y, L1, L2 = C.args
    if not isinstance(L1, PLine):
        return None
    R, P, Q = L1.args
    if not isinstance(L2, PLine):
        return None
    W, U, V = L2.args
    return Y, R, P, Q, W, U, V
