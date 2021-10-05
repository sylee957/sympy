from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.quantities import SyntheticGeometryPythagorasDifference as Pythagoras
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedRatio as Ratio


def _match_ratio(G, Y):
    if isinstance(G, Ratio):
        if Y == G.args[0]:
            Y, A, D, C = G.args
            return False, A, Y, C, D
        if Y == G.args[1]:
            A, Y, C, D = G.args
            return False, A, Y, C, D
        if Y == G.args[2]:
            D, C, Y, A = G.args
            return True, A, Y, C, D
        if Y == G.args[3]:
            C, D, A, Y = G.args
            return True, A, Y, C, D


def match_ABY(G, Y):
    if Y == G.args[0]:
        Y, A, B = G.args
        return A, B, Y
    if Y == G.args[1]:
        B, Y, A = G.args
        return A, B, Y
    if Y == G.args[2]:
        A, B, Y = G.args
        return A, B, Y


def _match_linear_area_3(A, B, C, Y):
    if A == Y:
        Y, A, B = A, B, C
        return A, B, Y
    if B == Y:
        B, Y, A = A, B, C
        return A, B, Y
    if C == Y:
        A, B, Y = A, B, C
        return A, B, Y


def _match_linear_area_4(A, B, C, D, Y):
    if A == Y:
        Y, A, B, C = A, B, C, D
        return A, B, C, Y
    if B == Y:
        C, Y, A, B = A, B, C, D
        return A, B, C, Y
    if C == Y:
        B, C, Y, A = A, B, C, D
        return A, B, C, Y
    if D == Y:
        A, B, C, Y = A, B, C, D
        return A, B, C, Y


def _match_linear_pythagoras_3(A, B, C, Y):
    if A == Y:
        A, B, Y = C, B, A
        return A, B, Y
    if B == Y and A == C:
        A, B, Y = B, A, B
        return A, B, Y
    if C == Y:
        A, B, Y = A, B, C
        return A, B, Y


def _match_linear_pythagoras_4(A, B, C, D, Y):
    if A == Y:
        Y, C, B, A = A, B, C, D
        return A, B, C, Y
    if B == Y:
        C, Y, A, B = A, B, C, D
        return A, B, C, Y
    if C == Y:
        B, A, Y, C = A, B, C, D
        return A, B, C, Y
    if D == Y:
        A, B, C, Y = A, B, C, D
        return A, B, C, Y


def _match_linear(G, Y):
    if isinstance(G, Area):
        if len(G.args) == 3:
            A, B, C = G.args
            match = _match_linear_area_3(A, B, C, Y)
            if match is not None:
                A, B, Y = match
                return lambda Y: Area(A, B, Y)
        elif len(G.args) == 4:
            A, B, C, D = G.args
            match = _match_linear_area_4(A, B, C, D, Y)
            if match is not None:
                A, B, C, Y = match
                return lambda Y: Area(A, B, C, Y)
    elif isinstance(G, Pythagoras):
        if len(G.args) == 3:
            A, B, C = G.args
            match = _match_linear_pythagoras_3(A, B, C, Y)
            if match is not None:
                A, B, Y = match
                return lambda Y: Pythagoras(A, B, Y)
        elif len(G.args) == 4:
            A, B, C, D = G.args
            match = _match_linear_pythagoras_4(A, B, C, D, Y)
            if match is not None:
                A, B, C, Y = match
                return lambda Y: Pythagoras(A, B, C, Y)


def _match_quadratic_pythagoras_3(A, B, C, Y):
    if B == Y:
        A, Y, B = A, B, C
        return A, B, Y
    if A == C and A == Y:
        A, Y, B = B, A, B
        return A, B, Y


def _match_quadratic(G, Y):
    if isinstance(G, Pythagoras):
        if len(G.args) == 3:
            A, B, C = G.args
            if B == Y:
                A, Y, B = A, B, C
                return lambda Y: Pythagoras(A, Y, B)
            if A == C and A == Y:
                A, Y, B = B, A, B
                return lambda Y: Pythagoras(A, Y, B)


def match_AYCD(G, Y):
    if Y == G.args[0]:
        Y, A, D, C = G.args
        return False, A, Y, C, D
    if Y == G.args[1]:
        A, Y, C, D = G.args
        return False, A, Y, C, D
    if Y == G.args[2]:
        D, C, Y, A = G.args
        return True, A, Y, C, D
    if Y == G.args[3]:
        C, D, A, Y = G.args
        return True, A, Y, C, D


def _geometric_quantities(E, classes=(Area, Ratio, Pythagoras)):
    r"""Get geometric quantities that should be eliminated"""
    if not E.args:
        return set()
    if isinstance(E, classes):
        return {E}
    return set.union(*(_geometric_quantities(arg, classes) for arg in E.args))


def _substitution_rule(subs):
    def rule(expr):
        if subs:
            return expr.xreplace(subs)
        return expr
    return rule


def _quadrilateral_area(objective):
    r"""Return the substitution that expands the quadrilateral area
    as addition of two triangle areas.

    Explanation
    ===========

    .. math::
        \mathcal{S}_{A, B, C, D} =
        \mathcal{S}_{A, B, C} + \mathcal{S}_{A, C, D}
    """
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Area):
            if len(G.args) == 4:
                A, B, C, D = G.args
                subs[G] = Area(A, B, C) + Area(A, C, D)
    return subs


def _quadrilateral_pythagoras(objective):
    r"""Return the substitution that expands the quadrilateral
    Pythagoras difference.

    Explanation
    ===========

    .. math::
        \mathcal{P}_{A, B, C, D} =
        \mathcal{P}_{B, A, C} - \mathcal{P}_{D, A, C}
    """
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Pythagoras):
            if len(G.args) == 4:
                A, B, C, D = G.args
                subs[G] = Pythagoras(B, A, C) - Pythagoras(D, A, C)
    return subs


def _cascade(func, subs):
    return {k: func(v) for k, v in subs.items()}
