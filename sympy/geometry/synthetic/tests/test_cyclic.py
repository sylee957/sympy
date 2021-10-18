from sympy.core.symbol import symbols
from sympy.core.numbers import Integer
from sympy.geometry.synthetic.constructions import SyntheticGeometryFoot as Foot
from sympy.geometry.synthetic.constructions import SyntheticGeometryIntersection as Intersection
from sympy.geometry.synthetic.constructions import SyntheticGeometryLine as Line
from sympy.geometry.synthetic.constructions import SyntheticGeometryMidpoint as Midpoint
from sympy.geometry.synthetic.constructions import SyntheticGeometryCircumcenter as Circumcenter
from sympy.geometry.synthetic.constructions import SyntheticGeometryPRatio as PRatio
from sympy.geometry.synthetic.predicates import SyntheticGeometryPerpendicular as Perpendicular
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedRatio as Ratio
from sympy.geometry.synthetic.plane import area_method_plane
from sympy.geometry.synthetic.area_coordinates import SyntheticGeometryCyclicConfiguration as CyclicConfiguration


def test_example_3_79():
    A, B, C, D = symbols('A B C D')
    E, F, G, G1 = symbols('E F G G1')

    constructions = [
        Foot(E, D, B, C),
        Foot(F, D, A, C),
        Foot(G, D, A, B),
        Intersection(G1, Line(E, F), Line(A, B))
    ]

    objective = Ratio(A, G, B, G) - Ratio(A, G1, B, G1)
    assert area_method_plane(
        constructions, objective, area_coordinates=CyclicConfiguration()) == 0


def test_example_3_80():
    A, B, C, D, E, F = symbols('A B C D E F')
    P, Q, S, S1 = symbols('P Q S S1')

    constructions = [
        Intersection(P, Line(D, F), Line(A, B)),
        Intersection(Q, Line(F, E), Line(B, C)),
        Intersection(S, Line(E, A), Line(C, D)),
        Intersection(S1, Line(P, Q), Line(C, D))
    ]

    objective = Ratio(C, S, D, S) - Ratio(C, S1, D, S1)
    assert area_method_plane(
        constructions, objective, area_coordinates=CyclicConfiguration()) == 0


def test_example_3_81():
    A, B, C, D, E, F = symbols('A B C D E F')
    M, N, G, H = symbols('M N G H')

    constructions = [
        Intersection(M, Line(D, C), Line(A, B)),
        Intersection(N, Line(E, F), Line(A, B)),
        Intersection(G, Line(A, B), Line(C, F)),
        Intersection(H, Line(D, E), Line(A, B)),
    ]

    objective = Ratio(M, G, A, G) * Ratio(B, H, N, H) - Ratio(B, M, A, B) * Ratio(B, A, A, N)
    assert area_method_plane(
        constructions, objective, area_coordinates=CyclicConfiguration()) == 0


def test_example_3_82():
    A, B, C, D = symbols('A B C D')
    O, G, F, E, N = symbols('O G F E N')

    constructions = [
        Circumcenter(O, A, B, C),
        Midpoint(G, A, D),
        Midpoint(F, A, B),
        Midpoint(E, C, D),
        PRatio(N, E, O, F, Integer(1))
    ]

    objective = Perpendicular(G, N, B, C)
    assert area_method_plane(
        constructions, objective, area_coordinates=CyclicConfiguration()) == True
