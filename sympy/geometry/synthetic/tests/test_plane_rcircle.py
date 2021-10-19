from sympy.core.symbol import symbols
from sympy.geometry.synthetic.constructions import SyntheticGeometryTRatio as TRatio
from sympy.geometry.synthetic.constructions import SyntheticGeometryLRatio as LRatio
from sympy.geometry.synthetic.constructions import SyntheticGeometryOn as On
from sympy.geometry.synthetic.constructions import SyntheticGeometryLine as Line
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.quantities import SyntheticGeometryPythagorasDifference as Pythagoras
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedRatio as Ratio
from sympy.geometry.synthetic.plane import area_method_plane


def test_inter_rcircle_rcircle_mockup():
    A, B, Y = symbols('A B Y')
    D, E, F = symbols('D E F')
    O, O1, O2 = symbols('O O1 O2')
    r, s = symbols('r s')

    constructions = [
        LRatio(O, O1, O2, r),
        TRatio(Y, O, O1, s)
    ]

    # Area
    lhs = Area(A, B, Y)
    rhs = r*Area(A, B, O2) + (1 - r)*Area(A, B, O1) - r*s/4*Pythagoras(O2, A, O1, B)
    objective = lhs - rhs
    assert area_method_plane(constructions, objective) == 0

    # Pythagoras
    lhs = Pythagoras(A, B, Y)
    rhs = r*Pythagoras(A, B, O2) + (1 - r)*Pythagoras(A, B, O1) - 4*r*s*Area(O2, A, O1, B)
    objective = lhs - rhs
    assert area_method_plane(constructions, objective) == 0

    # Quadratic
    lhs = Pythagoras(A, Y, B)
    rhs = (
        Pythagoras(A, O1, B) +
        r*(Pythagoras(A, O2, B) - Pythagoras(A, O1, B)) -
        r*(1 - r)*Pythagoras(O1, O2, O1) +
        r**2*s**2*Pythagoras(O1, O2, O1) +
        4*r*s*(Area(A, O1, O2) + Area(B, O1, O2))
    )
    objective = lhs - rhs
    assert area_method_plane(constructions, objective) == 0

    # Length Ratios
    lhs = Ratio(D, Y, E, F)
    rhs = (Pythagoras(D, O2, O1) - (1 - r)*Pythagoras(O1, O2, O1)) / Pythagoras(E, O2, F, O1)
    objective = lhs - rhs
    assert area_method_plane(constructions, objective) == 0

    constructions = [
        LRatio(O, O1, O2, r),
        TRatio(Y, O, O1, s),
        On(D, Line(O, Y)),
    ]

    lhs = Ratio(D, Y, E, F)
    rhs = (Area(D, O2, O1) - r*s/4*Pythagoras(O1, O2, O1)) / Pythagoras(E, O2, F, O1)
    objective = lhs - rhs
    assert area_method_plane(constructions, objective) == 0
