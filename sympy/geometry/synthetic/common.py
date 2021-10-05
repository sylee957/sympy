from sympy.combinatorics.permutations import _af_parity
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.quantities import SyntheticGeometryPythagorasDifference as Pythagoras
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedRatio as Ratio
from sympy.core.singleton import S
from sympy.core.compatibility import default_sort_key


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


def _geometric_quantities(E):
    r"""Get geometric quantities that should be eliminated"""
    if not E.args:
        return set()
    if isinstance(E, (Area, Ratio, Pythagoras)):
        return {E}
    return set.union(*(_geometric_quantities(arg) for arg in E.args))


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


def _uniformize_area(objective):
    r"""Return the substitution that normalizes the ordering of the
    points of the signed areas from the given geometric quantities.

    Explanation
    ===========

    If $A, B, C$ is the canonical ordering of the points,
    the signed area should reordered as:

    - $\mathcal{S}_{A, C, B} = -\mathcal{S}_{A, B, C}$
    - $\mathcal{S}_{B, A, C} = -\mathcal{S}_{A, B, C}$
    - $\mathcal{S}_{B, C, A} = \mathcal{S}_{A, B, C}$
    - $\mathcal{S}_{C, A, B} = \mathcal{S}_{A, B, C}$
    - $\mathcal{S}_{C, B, A} = -\mathcal{S}_{A, B, C}$
    """
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Area) and len(G.args) == 3:
            args = G.args
            args_sorted = tuple(sorted(args, key=default_sort_key))
            if args == args_sorted:
                continue

            permutation = [args_sorted.index(arg) for arg in args]
            parity = _af_parity(permutation)
            if parity == 0:
                subs[G] = Area(*args_sorted)
            else:
                subs[G] = -Area(*args_sorted)
    return subs


def _uniformize_pythagoras(objective):
    r"""Return the substitution that normalizes the ordering of the
    points of the Pythagoras difference from the given geometric
    quantities.

    Explanation
    ===========

    If $A, B$ is the canonical ordering of the points,
    the pythagoras difference should reordered as
    $\mathcal{P}_{B, A, B} = \mathcal{P}_{A, B, A}$

    If $A, C$ is the canonical ordering of the points,
    the pythagoras difference should reordered as
    $\mathcal{P}_{C, B, A} = \mathcal{P}_{A, B, C}$
    """
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Pythagoras) and len(G.args) == 3:
            A, B, C = G.args
            if A == C:
                AA, BB = sorted([A, B], key=default_sort_key)
                if (A, B) != (AA, BB):
                    subs[G] = Pythagoras(AA, BB, AA)
            else:
                AA, CC = sorted([A, C], key=default_sort_key)
                if (A, C) != (AA, CC):
                    subs[G] = Pythagoras(AA, B, CC)
    return subs


def _simplify_area(objective):
    r"""Return the substitution that evaluates trivial areas.

    Explanation
    ===========

    - $\mathcal{S}_{A, A, A} = 0$
    - $\mathcal{S}_{A, A, B} = 0$
    - $\mathcal{S}_{A, B, A} = 0$
    - $\mathcal{S}_{B, A, A} = 0$
    """
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Area):
            if len(G.args) == 3 and len(set(G.args)) != 3:
                subs[G] = S.Zero
    return subs


def _simplify_ratio(objective):
    r"""Return the substitution that evaluates trivial ratios of segments.

    Explanation
    ===========

    - $\frac{\overline{A, A}}{\overline{C, D}} = 0$
    - $\frac{\overline{A, B}}{\overline{A, B}} = 1$
    - $\frac{\overline{A, B}}{\overline{B, A}} = -1$
    """
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Ratio) and len(G.args) == 4:
            A, B, C, D = G.args
            if A == B:
                subs[G] = S.Zero
            if A == C and B == D:
                subs[G] = S.One
            if A == D and B == C:
                subs[G] = S.NegativeOne
    return subs


def _simplify_pythagoras(objective):
    r"""Return the substitution that evaluates trivial pythagoras difference.

    Explanation
    ===========

    - $\mathcal{P}_{A, A, B} = 0$
    - $\mathcal{P}_{A, B, B} = 0$
    """
    subs = {}
    for G in _geometric_quantities(objective):
        if isinstance(G, Pythagoras) and len(G.args) == 3:
            A, B, C = G.args
            if A == B:
                subs[G] = S.Zero
            elif B == C:
                subs[G] = S.Zero
    return subs
