from sympy.core.symbol import symbols
from sympy.geometry.synthetic.constructions import SyntheticGeometryFoot as Foot
from sympy.geometry.synthetic.constructions import SyntheticGeometryIntersection as Intersection
from sympy.geometry.synthetic.constructions import SyntheticGeometryLine as Line
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
    # TODO slow
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
