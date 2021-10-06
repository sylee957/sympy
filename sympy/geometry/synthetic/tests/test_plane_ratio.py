from sympy.core.symbol import symbols, Symbol
from sympy.geometry.synthetic.constructions import SyntheticGeometryIntersection as Intersection
from sympy.geometry.synthetic.constructions import SyntheticGeometryOn as On
from sympy.geometry.synthetic.constructions import SyntheticGeometryLine as Line
from sympy.geometry.synthetic.constructions import SyntheticGeometryPRatio as PRatio
from sympy.geometry.synthetic.constructions import SyntheticGeometryTRatio as TRatio
from sympy.geometry.synthetic.constructions import SyntheticGeometryFoot as Foot
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedRatio as Ratio
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.quantities import SyntheticGeometryPythagorasDifference as Pythagoras
from sympy.geometry.synthetic.plane import _ratio_inter_line_line
from sympy.geometry.synthetic.plane import _ratio_pratio
from sympy.geometry.synthetic.plane import _ratio_foot
from sympy.geometry.synthetic.plane import _ratio_tratio


def test_ratio_inter_line_line():
    P, Q = symbols('P Q')
    U, V = symbols('U V')
    A, Y, C, D = symbols('A Y C D')

    C = Intersection(Y, Line(P, Q), Line(U, V))
    objective = Ratio(A, Y, C, D)

    constructions = [C]
    desired = Area(A, U, V) / Area(C, U, D, V)
    assert _ratio_inter_line_line(Y, P, Q, U, V, constructions, objective) == {objective: desired}

    constructions = [On(A, Line(U, V)), C]
    desired = Area(A, P, Q) / Area(C, P, D, Q)
    assert _ratio_inter_line_line(Y, P, Q, U, V, constructions, objective) == {objective: desired}


def test_ratio_pratio():
    P, Q, R = symbols('P Q R')
    A, Y, C, D = symbols('A Y C D')
    l = Symbol('lambda')

    C = PRatio(Y, R, Line(P, Q), l)
    objective = Ratio(A, Y, C, D)

    constructions = [C]
    desired = Area(A, P, R, Q) / Area(C, P, D, Q)
    assert _ratio_pratio(Y, R, P, Q, l, constructions, objective) == {objective: desired}

    constructions = [C, On(A, Line(R, Y))]
    desired = (Ratio(A, R, P, Q) + l) / Ratio(C, D, P, Q)
    assert _ratio_pratio(Y, R, P, Q, l, constructions, objective) == {objective: desired}


def test_ratio_foot():
    Y, P, U, V = symbols('Y P U V')
    D, E, F = symbols('D E F')

    C = Foot(Y, P, Line(U, V))
    objective = Ratio(D, Y, E, F)

    constructions = [On(D, Line(U, V)), C]
    desired = Pythagoras(P, E, D, F) / Pythagoras(E, F, E)
    assert _ratio_foot(Y, P, U, V, constructions, objective) == {objective: desired}

    constructions = [C]
    desired = Area(D, U, V) / Area(E, U, F, V)
    assert _ratio_foot(Y, P, U, V, constructions, objective) == {objective: desired}


def test_ratio_tratio():
    Y, P, Q = symbols('Y P Q')
    D, E, F = symbols('D E F')
    r = Symbol('r')

    C = TRatio(Y, Line(P, Q), r)
    objective = Ratio(D, Y, E, F)

    constructions = [C, On(D, Line(P, Y))]
    desired = (Area(D, P, Q) - r / 4 * Pythagoras(P, Q, P)) / Pythagoras(E, P, F, Q)
    _ratio_tratio(Y, P, Q, r, constructions, objective) == {objective: desired}

    constructions = [C]
    desired = Pythagoras(D, P, Q) / Pythagoras(E, P, F, Q)
    _ratio_tratio(Y, P, Q, r, constructions, objective) == {objective: desired}
