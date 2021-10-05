from sympy.geometry.synthetic.predicates import SyntheticGeometrySamePoints as SamePoints
from sympy.geometry.synthetic.predicates import SyntheticGeometryParallel as Parallel
from sympy.geometry.synthetic.predicates import SyntheticGeometryPerpendicular as Perpendicular
from sympy.geometry.synthetic.predicates import SyntheticGeometryCollinear as Collinear
from sympy.geometry.synthetic.quantities import SyntheticGeometryFrozenSignedRatio as Ratio
from sympy.geometry.synthetic.constructions import SyntheticGeometryLRatio as LRatio
from sympy.geometry.synthetic.constructions import SyntheticGeometryPRatio as PRatio
from sympy.geometry.synthetic.constructions import SyntheticGeometryIntersection as Intersection
from sympy.geometry.synthetic.constructions import SyntheticGeometryOn as On
from sympy.geometry.synthetic.constructions import SyntheticGeometryLine as Line
from sympy.geometry.synthetic.constructions import SyntheticGeometryPLine as PLine
from sympy.geometry.synthetic.constructions import SyntheticGeometryBLine as BLine
from sympy.geometry.synthetic.constructions import SyntheticGeometryTLine as TLine
from sympy.geometry.synthetic.constructions import SyntheticGeometryCircle as Circle
from sympy.geometry.synthetic.common import _geometric_quantities
from sympy.core.singleton import S


def _degenerate_objective(objective):
    degenerate = S.false
    for G in _geometric_quantities(objective):
        if isinstance(G, Ratio):
            A, B, C, D = G.args
            degenerate = degenerate | SamePoints(C, D)
    return degenerate


def _degenerate_construction(C):
    if isinstance(C, (Line, BLine)):
        P, Q =  C.args
        return SamePoints(P, Q)

    if isinstance(C, (PLine, TLine)):
        R, P, Q =  C.args
        return SamePoints(P, Q)

    if isinstance(C, LRatio):
        Y, L, l = C.args
        return _degenerate_construction(L)

    if isinstance(C, PRatio):
        Y, R, L, l = C.args
        return _degenerate_construction(L)

    if isinstance(C, On):
        Y, L = C.args
        return _degenerate_construction(L)

    if isinstance(C, Intersection):
        Y, L1, L2 = C.args
        if isinstance(L1, (Line, PLine)) and isinstance(L2, (Line, PLine)):
            return _degenerate_line_pline_line_pline(L1, L2)
        elif isinstance(L1, (Line, PLine)) and isinstance(L2, (BLine, TLine)):
            return _degenerate_line_pline_bline_tline(L1, L2)
        elif isinstance(L2, (Line, PLine)) and isinstance(L1, (BLine, TLine)):
            return _degenerate_line_pline_bline_tline(L2, L1)
        elif isinstance(L1, (BLine, TLine)) and isinstance(L2, (BLine, TLine)):
            return _degenerate_bline_tline_bline_tline(L1, L2)
        elif isinstance(L1, (Line, PLine, TLine)) and isinstance(L2, Circle):
            O, P = L2.args
            return SamePoints(O, P) | SamePoints(Y, P) | _degenerate_construction(L1)
        elif isinstance(L2, (Line, PLine, TLine)) and isinstance(L1, Circle):
            return _degenerate_construction(Intersection(Y, L2, L1))
        elif isinstance(L1, Circle) and isinstance(L2, Circle):
            O1, P1 = L1.args
            O2, P2 = L2.args
            if P1 == P2:
                P = P1
                return Collinear(O1, O2, P)


def _degenerate_line_pline_line_pline(L1, L2):
    if isinstance(L1, Line):
        U, V = L1.args
    else:
        _, U, V = L1.args
    if isinstance(L2, Line):
        P, Q = L2.args
    else:
        _, P, Q = L2.args
    return Parallel(U, V, P, Q)


def _degenerate_line_pline_bline_tline(L1, L2):
    if isinstance(L1, Line):
        U, V = L1.args
    else:
        _, U, V = L1.args
    if isinstance(L2, BLine):
        P, Q = L2.args
    else:
        _, P, Q = L2.args
    return Perpendicular(U, V, P, Q)


def _degenerate_bline_tline_bline_tline(L1, L2):
    if isinstance(L1, BLine):
        U, V = L1.args
    else:
        _, U, V = L1.args
    if isinstance(L2, BLine):
        P, Q = L2.args
    else:
        _, P, Q = L2.args
    return Parallel(U, V, P, Q)
