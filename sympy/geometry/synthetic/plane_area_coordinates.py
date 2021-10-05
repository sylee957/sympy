from sympy.geometry.synthetic.common import _geometric_quantities
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.quantities import SyntheticGeometryPythagorasDifference as Pythagoras
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedLength as Length
from sympy.geometry.synthetic.quantities import SyntheticGeometryAreaCoordinateX as AreaCoordinateX
from sympy.geometry.synthetic.quantities import SyntheticGeometryAreaCoordinateY as AreaCoordinateY
from sympy.core.basic import Atom
from sympy.core.expr import Pow
from sympy.matrices import Matrix
from collections import Counter


def _auto_coordinates(objective):
    def _get_points_quantity(expr):
        all_points = Counter()
        for G in _geometric_quantities(expr):
            all_points += Counter(G.args)
        return all_points

    free_points = _get_points_quantity(objective)
    free_points = free_points.most_common(3)

    if len(free_points) < 3:
        return None
    O = free_points[0][0]
    U = free_points[1][0]
    V = free_points[2][0]
    return O, U, V


def _area_coordinates_area(O, U, V, objective):
    r"""Express $\mathcal{S}_{A, B, C}$ as the area coordinates"""
    def X(P):
        return AreaCoordinateX(O, U, V, P).doit()

    def Y(P):
        return AreaCoordinateY(O, U, V, P).doit()

    subs = {}
    for G in _geometric_quantities(objective, Area):
        if isinstance(G, Area) and len(G.args) == 3:
            A, B, C = G.args
            if {A, B, C} == {O, U, V}:
                continue

            subs[G] = -Area(O, U, V) * Matrix(
                [[X(A), Y(A), 1], [X(B), Y(B), 1], [X(C), Y(C), 1]]).det()
            subs[G] = subs[G].doit()
    return subs


def _area_coordinates_pythagoras(O, U, V, objective):
    r"""Express $\mathcal{P}_{A, B, C}$ as the area coordinates"""
    def X(P):
        return AreaCoordinateX(O, U, V, P).doit()

    def Y(P):
        return AreaCoordinateY(O, U, V, P).doit()

    def func(A, B):
        r"""Express $\overline{A, B}^2$ as area coordinates"""
        return (
            Length(O, V)**2 * (X(B) - X(A))**2 +
            Length(O, U)**2 * (Y(B) - Y(A))**2 +
            (X(B) - X(A))*(Y(B) - Y(A))*Pythagoras(U, O, V)
        ).doit()

    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Pythagoras) and len(G.args) == 3:
            A, B, C = G.args
            if A == U and B == O and C == V:
                continue
            if A == V and B == O and C == U:
                continue

            subs[G] = func(A, B) + func(B, C) - func(C, A)
            subs[G] = subs[G].doit()
    return subs


def _algsubs(expr, origin, dest):
    if expr == origin:
        return dest
    if isinstance(origin, Pow) and isinstance(expr, Pow):
        b1, n1 = expr.args
        b2, n2 = origin.args
        if n1.is_Integer and n2.is_Integer and b1 == b2:
            n1 = n1.p
            n2 = n2.p
            return dest**(n1 // n2) * b1**(n1 % n2)
    if isinstance(expr, Atom):
        return expr
    return expr.func(*(_algsubs(arg, origin, dest) for arg in expr.args))


def _area_coordinates_herron(O, U, V, objective):
    r"""Express $\mathcal{S}_{O, U, V}^{2}$ as the area coordinates"""
    subs = {}
    for G in _geometric_quantities(objective):
        if not isinstance(G, Area):
            continue
        if len(G.args) != 3:
            continue

        A, B, C = G.args
        if {O, U, V} != {A, B, C}:
            continue

        subs[G**2] = Length(O, U)**2 * Length(O, V)**2 / 4 - Pythagoras(U, O, V)**2 / 16
        subs[G**2] = subs[G**2].doit()
    return subs
