from sympy.logic.boolalg import Boolean
from sympy.core.symbol import Dummy
from sympy.geometry.synthetic.common import _geometric_quantities
from sympy.geometry.synthetic.constructions import SyntheticGeometryLRatio as LRatio
from sympy.geometry.synthetic.constructions import SyntheticGeometryPRatio as PRatio
from sympy.geometry.synthetic.constructions import SyntheticGeometryIntersection as Intersection
from sympy.core.compatibility import default_sort_key


def _auto_option_prove(objective, prove):
    if prove is None:
        prove = False
        if isinstance(objective, Boolean):
            prove = True
    return prove


def _auto_coordinates_orthogonal(O, U, V):
    if O is None:
        O = Dummy('$O')
    if U is None:
        U = Dummy('$U')
    if V is None:
        V = Dummy('$V')
    return O, U, V


def _auto_coordinates_skew(constructions, objective, O, U, V):
    O, U, V = _auto_coordinates_orthogonal(O, U, V)

    all_points = set()
    for G in _geometric_quantities(objective):
        for point in G.args:
            all_points.add(point)
    constructed_points = set()

    for C in constructions:
        if isinstance(C, LRatio):
            Y, P, Q, _ = C.args
            constructed_points.add(Y)
            all_points.add(Y)
            all_points.add(P)
            all_points.add(Q)
        elif isinstance(C, PRatio):
            Y, R, P, Q, _ = C.args
            constructed_points.add(Y)
            all_points.add(Y)
            all_points.add(P)
            all_points.add(Q)
            all_points.add(R)
        if isinstance(C, Intersection):
            Y, L1, L2 = C.args
            constructed_points.add(Y)
            all_points.add(Y)
            for point in L1.args:
                all_points.add(point)
            for point in L2.args:
                all_points.add(point)
    free_points = all_points.difference(constructed_points)
    free_points = sorted(free_points, key=default_sort_key)

    if not free_points:
        return O, U, V
    if len(free_points) == 1:
        O = free_points
        return O, U, V
    if len(free_points) == 2:
        O, U = free_points
        return O, U, V

    O, U, V, *_ = free_points
    return O, U, V
