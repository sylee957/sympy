from sympy.geometry.synthetic.auxiliary import (
    SyntheticGeometryAuxiliaryAreaCoordinateO as AreaCoordinateO,
    SyntheticGeometryAuxiliaryAreaCoordinateU as AreaCoordinateU,
    SyntheticGeometryAuxiliaryAreaCoordinateV as AreaCoordinateV
)
from sympy.core.compatibility import default_sort_key
from .common import _geometric_quantities
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.matrices import Matrix


def _auto_coordinates(objective):
    O = AreaCoordinateO()
    U = AreaCoordinateU()
    V = AreaCoordinateV()

    def _get_points_quantity(expr):
        all_points = set()
        for G in _geometric_quantities(expr):
            new_points = set(G.args)
            all_points = all_points.union(new_points)
        return all_points

    free_points = _get_points_quantity(objective)
    free_points = sorted(free_points, key=default_sort_key)

    if len(free_points) >= 3:
        O, U, V, *_ = free_points
        return O, U, V
    if len(free_points) >= 2:
        U, V, *_ = free_points
        return O, U, V
    if len(free_points) >= 1:
        O, *_ = free_points
        return O, U, V
    return O, U, V


def _area_coordinates(O, U, V, objective):
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Area) and len(G.args) == 3:
            A, B, Y = G.args
            if {O, U}.issubset({A, B, Y}):
                continue
            if {O, V}.issubset({A, B, Y}):
                continue

            subs[G] = Matrix(
                [[Area(O, U, A), Area(O, V, A), 1],
                 [Area(O, U, B), Area(O, V, B), 1],
                 [Area(O, U, Y), Area(O, V, Y), 1]]
            ).det() / Area(O, U, V)
            subs[G] = subs[G].doit()
            subs[G] = subs[G].cancel()
    return subs
