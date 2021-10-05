from sympy.core.symbol import symbols, Symbol
from sympy.geometry.synthetic.constructions import SyntheticGeometryIntersection as Intersection
from sympy.geometry.synthetic.constructions import SyntheticGeometryOn as On
from sympy.geometry.synthetic.constructions import SyntheticGeometryLine as Line
from sympy.geometry.synthetic.constructions import SyntheticGeometryPLine as PLine
from sympy.geometry.synthetic.constructions import SyntheticGeometryPRatio as PRatio
from sympy.geometry.synthetic.constructions import SyntheticGeometryTRatio as TRatio
from sympy.geometry.synthetic.constructions import SyntheticGeometryFoot as Foot
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedRatio as Ratio
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.quantities import SyntheticGeometryPythagorasDifference as Pythagoras
from sympy.geometry.synthetic.plane import area_method_plane


def test_ratio_inter_line_line():
    P, Q = symbols('P Q')
    U, V = symbols('U V')
    A, Y, C, D = symbols('A Y C D')

    objective = Ratio(A, Y, C, D)

    constructions = [Intersection(Y, Line(P, Q), Line(U, V))]
    desired = Area(A, U, V) / Area(C, U, D, V)
    assert area_method_plane(constructions, objective - desired) == 0

    constructions = [Intersection(Y, Line(U, V), Line(P, Q)), On(A, PLine(Y, C, D))]
    desired = Area(A, U, V) / Area(C, U, D, V)
    assert area_method_plane(constructions, objective - desired) == 0

    constructions = [On(A, Line(U, V)), Intersection(Y, Line(P, Q), Line(U, V))]
    desired = Area(A, P, Q) / Area(C, P, D, Q)
    assert area_method_plane(constructions, objective - desired) == 0

    constructions = [On(A, Line(U, V)), Intersection(Y, Line(U, V), Line(P, Q))]
    desired = Area(A, P, Q) / Area(C, P, D, Q)
    assert area_method_plane(constructions, objective - desired) == 0


def test_ratio_pratio():
    P, Q, R = symbols('P Q R')
    A, Y, C, D = symbols('A Y C D')
    l = Symbol('lambda')

    objective = Ratio(A, Y, C, D)

    constructions = [PRatio(Y, R, P, Q, l)]
    desired = Area(A, P, R, Q) / Area(C, P, D, Q)
    assert area_method_plane(constructions, objective - desired) == 0

    constructions = [PRatio(Y, R, P, Q, l), On(A, Line(R, Y))]
    desired = (Ratio(A, R, P, Q) + l) / Ratio(C, D, P, Q)
    assert area_method_plane(constructions, objective - desired) == 0


def test_ratio_foot():
    Y, P, U, V = symbols('Y P U V')
    D, E, F = symbols('D E F')

    objective = Ratio(D, Y, E, F)

    constructions = [On(D, Line(U, V)), Foot(Y, P, U, V)]
    desired = Pythagoras(P, E, D, F) / Pythagoras(E, F, E)
    assert area_method_plane(constructions, objective - desired) == 0

    constructions = [Foot(Y, P, U, V)]
    desired = Area(D, U, V) / Area(E, U, F, V)
    assert area_method_plane(constructions, objective - desired) == 0


def test_ratio_tratio():
    Y, P, Q = symbols('Y P Q')
    D, E, F = symbols('D E F')
    r = Symbol('r')

    objective = Ratio(D, Y, E, F)

    constructions = [TRatio(Y, P, Q, r), On(D, Line(P, Y))]
    desired = (Area(D, P, Q) - r / 4 * Pythagoras(P, Q, P)) / Pythagoras(E, P, F, Q)
    assert area_method_plane(constructions, objective - desired) == 0

    constructions = [TRatio(Y, P, Q, r)]
    desired = Pythagoras(D, P, Q) / Pythagoras(E, P, F, Q)
    assert area_method_plane(constructions, objective - desired) == 0
