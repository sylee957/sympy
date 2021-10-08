from sympy.core.singleton import S
from sympy.core.symbol import symbols
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.quantities import SyntheticGeometryPythagorasDifference as Pythagoras
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedRatio as Ratio
from sympy.geometry.synthetic.common import _uniformize_pythagoras
from sympy.geometry.synthetic.common import _simplify_pythagoras


def test_uniformize_area():
    A, B, C = symbols("A B C")
    assert _uniformize_area(Area(A, B, C)) == {}
    assert _uniformize_area(Area(A, C, B)) == {Area(A, C, B): -Area(A, B, C)}
    assert _uniformize_area(Area(B, A, C)) == {Area(B, A, C): -Area(A, B, C)}
    assert _uniformize_area(Area(B, C, A)) == {Area(B, C, A): Area(A, B, C)}
    assert _uniformize_area(Area(C, A, B)) == {Area(C, A, B): Area(A, B, C)}
    assert _uniformize_area(Area(C, B, A)) == {Area(C, B, A): -Area(A, B, C)}


def test_uniformize_pythagoras():
    A, B, C = symbols("A B C")
    assert _uniformize_pythagoras(Pythagoras(A, B, C)) == {}
    assert _uniformize_pythagoras(Pythagoras(A, C, B)) == {}
    assert _uniformize_pythagoras(Pythagoras(B, A, C)) == {}
    assert _uniformize_pythagoras(Pythagoras(B, C, A)) == \
        {Pythagoras(B, C, A): Pythagoras(A, C, B)}
    assert _uniformize_pythagoras(Pythagoras(C, A, B)) == \
        {Pythagoras(C, A, B): Pythagoras(B, A, C)}
    assert _uniformize_pythagoras(Pythagoras(C, B, A)) == \
        {Pythagoras(C, B, A): Pythagoras(A, B, C)}

    assert _uniformize_pythagoras(Pythagoras(A, B, A)) == {}
    assert _uniformize_pythagoras(Pythagoras(B, A, B)) == \
        {Pythagoras(B, A, B): Pythagoras(A, B, A)}


def test_simplify_area():
    A, B, C = symbols("A B C")
    assert _simplify_area(Area(A, B, C)) == {}
    assert _simplify_area(Area(A, A, A)) == {Area(A, A, A): S.Zero}
    assert _simplify_area(Area(A, A, B)) == {Area(A, A, B): S.Zero}
    assert _simplify_area(Area(A, B, A)) == {Area(A, B, A): S.Zero}
    assert _simplify_area(Area(B, A, A)) == {Area(B, A, A): S.Zero}


def test_simplify_ratio():
    A, B, C, D = symbols("A B C D")
    assert _simplify_ratio(Ratio(A, B, C, D)) == {}
    assert _simplify_ratio(Ratio(A, A, C, D)) == {Ratio(A, A, C, D): S.Zero}
    assert _simplify_ratio(Ratio(A, B, A, B)) == {Ratio(A, B, A, B): S.One}
    assert _simplify_ratio(Ratio(A, B, B, A)) == {Ratio(A, B, B, A): S.NegativeOne}


def test_simplify_pythagoras():
    A, B, C = symbols("A B C")
    assert _simplify_pythagoras(Pythagoras(A, B, C)) == {}
    assert _simplify_pythagoras(Pythagoras(A, A, B)) == {Pythagoras(A, A, B): S.Zero}
    assert _simplify_pythagoras(Pythagoras(A, B, B)) == {Pythagoras(A, B, B): S.Zero}
