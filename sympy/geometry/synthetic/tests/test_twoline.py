from sympy.core.symbol import symbols, Symbol
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedRatio as Ratio
from sympy.geometry.synthetic.twoline import area_method_twoline
from sympy.geometry.synthetic.quantities_twoline import SyntheticGeometryTwolineAlpha as Alpha
from sympy.geometry.synthetic.quantities_twoline import SyntheticGeometryTwolineBeta as Beta
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedLength as Length
from sympy.geometry.synthetic.constructions import SyntheticGeometryIntersection as Intersection
from sympy.geometry.synthetic.constructions import SyntheticGeometryLine as Line


def test_twoline_zero():
    A, B, C, D, E, F = symbols('A B C D E F')
    constructions = []
    line_1 = {A, B, C}
    line_2 = {D, E, F}

    objective = Area(A, B, C)
    assert area_method_twoline(constructions, objective, line_1, line_2) == 0

    objective = Area(D, E, F)
    assert area_method_twoline(constructions, objective, line_1, line_2) == 0


def test_twoline_area_parallel():
    A, B, C, D = symbols('A B C D')
    constructions = []
    line_1 = {A, B}
    line_2 = {C, D}

    desired = Length(C, D) * Alpha() / 2
    objective = Area(A, C, D)
    assert area_method_twoline(constructions, objective - desired, line_1, line_2) == 0
    objective = Area(C, D, A)
    assert area_method_twoline(constructions, objective - desired, line_1, line_2) == 0
    objective = Area(D, A, C)
    assert area_method_twoline(constructions, objective - desired, line_1, line_2) == 0

    desired = -Length(A, B) * Alpha() / 2
    objective = Area(C, A, B)
    assert area_method_twoline(constructions, objective - desired, line_1, line_2) == 0
    objective = Area(A, B, C)
    assert area_method_twoline(constructions, objective - desired, line_1, line_2) == 0
    objective = Area(B, C, A)
    assert area_method_twoline(constructions, objective - desired, line_1, line_2) == 0


def test_twoline_area_nonparallel():
    A, B, C, D, O = symbols('A B C D O')

    constructions = []
    line_1 = {A, B, O}
    line_2 = {C, D, O}

    desired = -Length(A, O) * Length(C, D) * Beta() / 2
    objective = Area(A, C, D)
    assert area_method_twoline(constructions, objective - desired, line_1, line_2) == 0
    objective = Area(C, D, A)
    assert area_method_twoline(constructions, objective - desired, line_1, line_2) == 0
    objective = Area(D, A, C)
    assert area_method_twoline(constructions, objective - desired, line_1, line_2) == 0

    desired = Length(C, O) * Length(A, B) * Beta() / 2
    objective = Area(C, A, B)
    assert area_method_twoline(constructions, objective - desired, line_1, line_2) == 0
    objective = Area(A, B, C)
    assert area_method_twoline(constructions, objective - desired, line_1, line_2) == 0
    objective = Area(B, C, A)
    assert area_method_twoline(constructions, objective - desired, line_1, line_2) == 0


def test_menelaus():
    A, B, C, D, E, F = symbols('A B C D E F')
    constructions = [
        Intersection(F, Line(D, E), Line(A, B)),
    ]
    objective = Ratio(C, E, A, E) * Ratio(B, D, C, D) * Ratio(A, F, B, F)
    assert area_method_twoline(constructions, objective, {A, C, E}, {C, B, D}) == 1


def test_pappus():
    A, B, C = symbols('A B C')
    A1, B1, C1 = symbols('A1 B1 C1')
    O = Symbol('O')
    P, Q, S, T = symbols('P Q S T')
    constructions = [
        Intersection(P, Line(A1, B), Line(A, B1)),
        Intersection(Q, Line(A1, C), Line(A, C1)),
        Intersection(S, Line(B1, C), Line(B, C1)),
        Intersection(T, Line(B1, C), Line(P, Q)),
    ]
    objective = Ratio(B1, S, C, S) - Ratio(B1, T, C, T)
    assert area_method_twoline(constructions, objective, {O, A, B, C}, {O, A1, B1, C1}) == 0
