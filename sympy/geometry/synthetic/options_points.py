from sympy.geometry.synthetic.constructions import (
    SyntheticGeometryLRatio as LRatio,
    SyntheticGeometryPRatio as PRatio,
    SyntheticGeometryTRatio as TRatio,
    SyntheticGeometryIntersection as Intersection,
    SyntheticGeometryLine as Line,
    SyntheticGeometryPLine as PLine,
    SyntheticGeometryTLine as TLine,
    SyntheticGeometryBLine as BLine,
    SyntheticGeometryCircle as Circle
)


def _get_points_primitives(C):
    if isinstance(C, (Line, BLine)):
        U, V = C.args
        return {U, V}
    if isinstance(C, (PLine, TLine)):
        W, U, V = C.args
        return {W, U, V}
    elif isinstance(C, Circle):
        O, P = C.args
        return {O, P}


def _get_points_construction(C):
    if isinstance(C, LRatio):
        Y, L, _ = C.args
        return Y, _get_points_primitives(L)
    elif isinstance(C, PRatio):
        Y, R, L, _ = C.args
        return Y, _get_points_primitives(L)
    elif isinstance(C, TRatio):
        Y, R, L, _ = C.args
        return Y, _get_points_primitives(L)
    elif isinstance(C, Intersection):
        Y, L1, L2 = C.args
        L1, L2 = _get_points_primitives(L1), _get_points_primitives(L2)
        return Y, set.union(L1, L2)
