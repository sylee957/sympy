from sympy.geometry.synthetic.constructions import SyntheticGeometryLine as Line
from sympy.geometry.synthetic.constructions import SyntheticGeometryFoot as Foot
from sympy.geometry.synthetic.constructions import SyntheticGeometryIntersection as Intersection
from sympy.geometry.synthetic.predicates import SyntheticGeometryPerpendicular as Perpendicular
from sympy.core.symbol import symbols
from sympy.core.singleton import S
from sympy.geometry.synthetic.plane import area_method_plane


def test_orthocenter():
    # Exercise 3.36, Machine Proofs in Geometry
    Y, P, Q, U, V = symbols('Y P Q U V')
    D, E, F = symbols('D E F')
    A, B, C = symbols('A B C')
    E, F, H = symbols('E F H')
    K, L = symbols('K L')

    constructions = [
        Foot(E, B, Line(A, C)),
        Foot(F, A, Line(B, C)),
        Intersection(H, Line(A, F), Line(B, E))
    ]
    objective = Perpendicular(A, B, C, H)
    assert area_method_plane(constructions, objective) is S.true
