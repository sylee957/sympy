from sympy.core.symbol import symbols
from sympy.geometry.synthetic.constructions import SyntheticGeometryIntersection as Intersection
from sympy.geometry.synthetic.constructions import SyntheticGeometryOn as On
from sympy.geometry.synthetic.constructions import SyntheticGeometryLine as Line
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedRatio as Ratio
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.plane import area_method_plane


def test_ratio_inter_line_line_both():
    P, Q = symbols('P Q')
    U, V = symbols('U V')
    A, Y, C = symbols('A Y C')

    objective = Ratio(A, Y, C, Y)

    constructions = [Intersection(Y, Line(P, Q), Line(U, V))]
    desired = Area(A, U, V) / Area(C, U, V)
    assert area_method_plane(constructions, objective - desired) == 0

    constructions = [Intersection(Y, Line(U, V), Line(P, Q)), On(A, Line(Y, C))]
    desired = Area(A, U, V) / Area(C, U, V)
    assert area_method_plane(constructions, objective - desired) == 0

    constructions = [On(A, Line(U, V)), Intersection(Y, Line(P, Q), Line(U, V))]
    desired = Area(A, P, Q) / Area(C, P, Q)
    assert area_method_plane(constructions, objective - desired) == 0

    constructions = [On(A, Line(U, V)), Intersection(Y, Line(U, V), Line(P, Q))]
    desired = Area(A, P, Q) / Area(C, P, Q)
    assert area_method_plane(constructions, objective - desired) == 0
