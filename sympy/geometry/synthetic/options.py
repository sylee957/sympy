from sympy.logic.boolalg import Boolean
from sympy.core.symbol import Dummy
from sympy.core.compatibility import default_sort_key
from sympy.geometry.synthetic.options_points import _get_points_construction


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
    constructed_points = set()
    for C in constructions:
        Y, new_points = _get_points_construction(C)
        constructed_points.add(Y)
        all_points = all_points.union(new_points)
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
