from sympy.core.singleton import S
from sympy.geometry.synthetic.predicates import (
    SyntheticGeometryCollinear as Collinear,
    SyntheticGeometryParallel as Parallel)
from sympy.geometry.synthetic.quantities import (
    SyntheticGeometrySignedArea as Area,
    SyntheticGeometrySignedRatio as Ratio)
from sympy.geometry.synthetic.constructions import (
    SyntheticGeometryLRatio as LRatio,
    SyntheticGeometryPRatio as PRatio,
    SyntheticGeometryIntersection as Intersection,
    SyntheticGeometryLine as Line,
    SyntheticGeometryPLine as PLine
)
from sympy.geometry.synthetic.common import (
    _geometric_quantities,
    match_AYCD
)


def _ratio_lratio(C, constructions, area_method, objective):
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Ratio) and isinstance(C, LRatio):
            Y, L, l = C.args
            if isinstance(L, Line):
                P, Q = L.args
                if Y in G.args and len(G.args) == 4:
                    reciprocal, A, Y, C, D = match_AYCD(G, Y)
                    assertion = area_method(constructions, Collinear(A, P, Q))
                    if assertion is S.true:
                        subs[G] = (Ratio(A, P, P, Q) + l) / Ratio(C, D, P, Q)
                    else:
                        subs[G] = Area(A, P, Q) / Area(C, P, D, Q)
                    if reciprocal:
                        subs[G] = 1 / subs[G]
    return subs


def _ratio_pratio(C, constructions, area_method, objective):
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Ratio) and isinstance(C, PRatio):
            Y, R, L, l = C.args
            if isinstance(L, Line):
                P, Q = L.args
                if Y in G.args and len(G.args) == 4:
                    reciprocal, A, Y, C, D = match_AYCD(G, Y)
                    assertion = area_method(constructions, Collinear(A, R, Y))
                    if assertion is S.true:
                        subs[G] = (Ratio(A, R, P, Q) + l) / Ratio(C, D, P, Q)
                    else:
                        subs[G] = Area(A, P, R, Q) / Area(C, P, D, Q)
                    if reciprocal:
                        subs[G] = 1 / subs[G]
    return subs


def _ratio_inter_line_line(C, constructions, area_method, objective):
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Ratio) and isinstance(C, Intersection):
            Y, L1, L2 = C.args
            if isinstance(L1, Line) and isinstance(L2, Line):
                P, Q = L1.args
                U, V = L2.args
                if Y in G.args and len(G.args) == 4:
                    reciprocal, A, Y, C, D = match_AYCD(G, Y)
                    assertion = area_method(constructions, Collinear(A, U, V))
                    if assertion is S.true:
                        subs[G] = Area(A, P, Q) / Area(C, P, D, Q)
                    else:
                        subs[G] = Area(A, U, V) / Area(C, U, D, V)
                    if reciprocal:
                        subs[G] = 1 / subs[G]
    return subs


def _ratio_inter_pline_line(C, constructions, area_method, objective):
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Ratio) and isinstance(C, Intersection):
            Y, L1, L2 = C.args

            if isinstance(L1, Line) and isinstance(L2, PLine):
                L1, L2 = L2, L1

            if isinstance(L1, PLine) and isinstance(L2, Line):
                R, P, Q = L1.args
                U, V = L2.args
                if Y in G.args and len(G.args) == 4:
                    reciprocal, A, Y, C, D = match_AYCD(G, Y)
                    assertion = area_method(constructions, Collinear(A, U, V))
                    if assertion is S.true:
                        subs[G] = Area(A, P, R, Q) / Area(C, P, D, Q)
                    else:
                        subs[G] = Area(A, U, V) / Area(C, U, D, V)
                    if reciprocal:
                        subs[G] = 1 / subs[G]
    return subs


def _ratio_inter_pline_pline(C, constructions, area_method, objective):
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Ratio) and isinstance(C, Intersection):
            Y, L1, L2 = C.args
            if isinstance(L1, PLine) and isinstance(L2, PLine):
                R, P, Q = L1.args
                W, U, V = L2.args
                if Y in G.args and len(G.args) == 4:
                    reciprocal, A, Y, C, D = match_AYCD(G, Y)
                    assertion = area_method(constructions, Parallel(A, Y, P, Q))
                    if assertion is S.true:
                        subs[G] = Area(A, U, W, V) / Area(C, U, D, V)
                    else:
                        subs[G] = Area(A, P, R, Q) / Area(C, P, D, Q)
                    if reciprocal:
                        subs[G] = 1 / subs[G]
    return subs
