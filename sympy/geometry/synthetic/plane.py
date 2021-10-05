from sympy.geometry.synthetic.constructions import SyntheticGeometryPRatio as PRatio
from sympy.geometry.synthetic.constructions import SyntheticGeometryTRatio as TRatio
from sympy.geometry.synthetic.constructions import SyntheticGeometryIntersection as Intersection
from sympy.geometry.synthetic.constructions import SyntheticGeometryFoot as Foot
from sympy.geometry.synthetic.constructions import SyntheticGeometryLine as Line


def _match_pratio(C):
    if not isinstance(C, PRatio):
        return None

    Y, W, L, l = C.args
    if not isinstance(L, Line):
        return None

    U, V = L.args
    return Y, W, U, V, l


def _match_inter_line_line(C):
    if not isinstance(C, Intersection):
        return None

    Y, L1, L2 = C.args
    if not isinstance(L1, Line):
        return None
    if not isinstance(L2, Line):
        return None

    U, V = L1.args
    P, Q = L2.args
    return Y, U, V, P, Q


def _match_foot(C):
    if not isinstance(C, Foot):
        return None

    Y, P, L = C.args
    if not isinstance(L, Line):
        return None

    U, V = L.args
    return Y, P, U, V


def _match_tratio(C):
    if not isinstance(C, TRatio):
        return None

    Y, L, l = C.args
    if not isinstance(L, Line):
        return None

    P, Q = L.args
    return Y, P, Q, l
