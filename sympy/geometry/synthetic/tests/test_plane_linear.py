from sympy.core.symbol import Symbol, symbols
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.quantities import SyntheticGeometryPythagorasDifference as Pythagoras
from sympy.geometry.synthetic.constructions import SyntheticGeometryLine as Line
from sympy.geometry.synthetic.constructions import SyntheticGeometryFoot as Foot
from sympy.geometry.synthetic.constructions import SyntheticGeometryIntersection as Intersection
from sympy.geometry.synthetic.constructions import SyntheticGeometryPRatio as PRatio
from sympy.geometry.synthetic.plane import area_method_plane


def test_linear_pratio():
    U, V, W = symbols('U V W')
    A, B, C = symbols('A B C')
    l = Symbol('lambda')
    Y = Symbol('Y')

    constructions = [PRatio(Y, W, U, V, l)]
    for G in [
        lambda Y: Area(A, B, Y),
        lambda Y: Area(A, B, C, Y),
        lambda Y: Pythagoras(A, B, Y),
        lambda Y: Pythagoras(A, B, C, Y)
    ]:
        objective = G(Y)
        desired = G(W) + l * (G(V) - G(U))
        assert area_method_plane(constructions, objective - desired) == 0


def test_linear_inter_line_line():
    U, V = symbols('U V')
    P, Q = symbols('P Q')
    A, B, C = symbols('A B C')
    Y = Symbol('Y')

    constructions = [Intersection(Y, Line(U, V), Line(P, Q))]

    for G in [
        lambda Y: Area(A, B, Y),
        lambda Y: Area(A, B, C, Y),
        lambda Y: Pythagoras(A, B, Y),
        lambda Y: Pythagoras(A, B, C, Y)
    ]:
        objective = G(Y)
        desired = (Area(U, P, Q) * G(V) - Area(V, P, Q) * G(U)) / Area(U, P, V, Q)
        assert area_method_plane(constructions, objective - desired) == 0

    constructions = [Intersection(Y, Line(P, Q), Line(U, V))]

    for G in [
        lambda Y: Area(A, B, Y),
        lambda Y: Area(A, B, C, Y),
        lambda Y: Pythagoras(A, B, Y),
        lambda Y: Pythagoras(A, B, C, Y)
    ]:
        objective = G(Y)
        desired = (Area(U, P, Q) * G(V) - Area(V, P, Q) * G(U)) / Area(U, P, V, Q)
        assert area_method_plane(constructions, objective - desired) == 0


def test_linear_foot():
    U, V = symbols('U V')
    P = Symbol('P')
    A, B, C = symbols('A B C')
    Y = Symbol('Y')

    constructions = [Foot(Y, P, U, V)]

    for G in [
        lambda Y: Area(A, B, Y),
        lambda Y: Area(A, B, C, Y),
        lambda Y: Pythagoras(A, B, Y),
        lambda Y: Pythagoras(A, B, C, Y)
    ]:
        objective = G(Y)
        desired = (Pythagoras(P, U, V) * G(V) + Pythagoras(P, V, U) * G(U)) / Pythagoras(U, V, U)
        assert area_method_plane(constructions, objective - desired) == 0
