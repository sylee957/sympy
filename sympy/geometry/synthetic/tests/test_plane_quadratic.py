from sympy.core.symbol import Symbol, symbols
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.quantities import SyntheticGeometryPythagorasDifference as Pythagoras
from sympy.geometry.synthetic.constructions import SyntheticGeometryPRatio as PRatio
from sympy.geometry.synthetic.constructions import SyntheticGeometryIntersection as Intersection
from sympy.geometry.synthetic.constructions import SyntheticGeometryLine as Line
from sympy.geometry.synthetic.constructions import SyntheticGeometryFoot as Foot
from sympy.geometry.synthetic.plane_quadratic import _quadratic_pratio
from sympy.geometry.synthetic.plane_quadratic import _quadratic_inter_line_line
from sympy.geometry.synthetic.plane_quadratic import _quadratic_foot


def test_quadratic_pratio():
    U, V, W = symbols('U V W')
    A, B, C = symbols('A B C')
    l = Symbol('lambda')
    Y = Symbol('Y')

    C = PRatio(Y, W, Line(U, V), l)
    G = lambda Y: Pythagoras(A, Y, B)
    objective = G(Y)
    desired = G(W) + l*(G(V) - G(U) + 2*Pythagoras(W, U, V)) - l*(1 - l)*Pythagoras(U, V, U)
    assert _quadratic_pratio(C, objective) == {objective: desired}


def test_quadratic_inter_line_line():
    U, V = symbols('U V')
    P, Q = symbols('P Q')
    A, B, C = symbols('A B C')
    Y = Symbol('Y')

    C = Intersection(Y, Line(U, V), Line(P, Q))

    G = lambda Y: Pythagoras(A, Y, B)
    objective = G(Y)
    desired = (
        Area(U, P, Q) / Area(U, P, V, Q) * G(V) -
        Area(V, P, Q) / Area(U, P, V, Q) * G(U) +
        Area(U, P, Q) / Area(U, P, V, Q) *
        Area(V, P, Q) / Area(U, P, V, Q) *
        Pythagoras(U, V, U)
    )
    assert _quadratic_inter_line_line(C, objective) == {objective: desired}


def test_quadartic_foot():
    U, V = symbols('U V')
    P = Symbol('P')
    A, B, C = symbols('A B C')
    Y = Symbol('Y')

    C = Foot(Y, P, Line(U, V))

    G = lambda Y: Pythagoras(A, Y, B)
    objective = G(Y)
    desired = (
        Pythagoras(P, U, V) / Pythagoras(U, V, U) * G(V) +
        Pythagoras(P, V, U) / Pythagoras(U, V, U) * G(U) -
        Pythagoras(P, U, V) * Pythagoras(P, V, U) / Pythagoras(U, V, U)
    )
    assert _quadratic_foot(C, objective) == {objective: desired}
