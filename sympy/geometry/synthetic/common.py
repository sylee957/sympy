from sympy.combinatorics.permutations import _af_parity
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.quantities import SyntheticGeometryPythagorasDifference as Pythagoras
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedRatio as Ratio
from sympy.core.singleton import S
from sympy.core.compatibility import default_sort_key
from sympy.core.expr import Add, Mul, Pow
from sympy.core.numbers import Integer


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


def _quadrilateral_area(domain, objective):
    r"""Return the substitution that expands the quadrilateral area
    as addition of two triangle areas.

    Explanation
    ===========

    .. math::
        \mathcal{S}_{A, B, C, D} =
        \mathcal{S}_{A, B, C} + \mathcal{S}_{A, C, D}
    """
    for G in domain.symbols:
        if isinstance(G, Area):
            if len(G.args) == 4:
                A, B, C, D = G.args
                eliminant = Area(A, B, C) + Area(A, C, D)
                domain, objective = _inject_new_variables_and_eliminate(domain, objective, eliminant, G)
                domain, objective = _compress(domain, objective)
    return domain, objective


def _quadrilateral_pythagoras(domain, objective):
    r"""Return the substitution that expands the quadrilateral
    Pythagoras difference.

    Explanation
    ===========

    .. math::
        \mathcal{P}_{A, B, C, D} =
        \mathcal{P}_{B, A, C} - \mathcal{P}_{D, A, C}
    """
    for G in domain.symbols:
        if isinstance(G, Pythagoras):
            if len(G.args) == 4:
                A, B, C, D = G.args
                eliminant = Pythagoras(B, A, C) - Pythagoras(D, A, C)
                domain, objective = _inject_new_variables_and_eliminate(domain, objective, eliminant, G)
                domain, objective = _compress(domain, objective)
    return domain, objective


def _uniformize_area(domain, objective):
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
    for G in domain.symbols:
        if isinstance(G, Area) and len(G.args) == 3:
            args = G.args
            args_sorted = tuple(sorted(args, key=default_sort_key))
            if args == args_sorted:
                continue

            permutation = [args_sorted.index(arg) for arg in args]
            parity = _af_parity(permutation)
            if parity == 0:
                eliminant = Area(*args_sorted)
            else:
                eliminant = -Area(*args_sorted)
            domain, objective = _inject_new_variables_and_eliminate(domain, objective, eliminant, G)
            domain, objective = _compress(domain, objective)
    return domain, objective


def _uniformize_pythagoras(domain, objective):
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
    for G in domain.symbols:
        if isinstance(G, Pythagoras) and len(G.args) == 3:
            A, B, C = G.args
            if A == C:
                AA, BB = sorted([A, B], key=default_sort_key)
                if (A, B) != (AA, BB):
                    eliminant = Pythagoras(AA, BB, AA)
            else:
                AA, CC = sorted([A, C], key=default_sort_key)
                if (A, C) != (AA, CC):
                    eliminant = Pythagoras(AA, B, CC)
            domain, objective = _inject_new_variables_and_eliminate(domain, objective, eliminant, G)
            domain, objective = _compress(domain, objective)
    return domain, objective


def _uniformize_ratio(domain, objective):
    for G in domain.symbols:
        if isinstance(G, Ratio) and len(G.args) == 4:
            A, B, C, D = G.args
            AA, BB = sorted([A, B], key=default_sort_key)
            CC, DD = sorted([C, D], key=default_sort_key)
            sign = 1
            if A == BB and B == AA:
                sign *= -1
            if C == DD and D == CC:
                sign *= -1
            eliminant = sign * Ratio(AA, BB, CC, DD)
            domain, objective = _inject_new_variables_and_eliminate(domain, objective, eliminant, G)
            domain, objective = _compress(domain, objective)
    return domain, objective


def _simplify_pythagoras(domain, objective):
    r"""Return the substitution that evaluates trivial pythagoras difference.

    Explanation
    ===========

    - $\mathcal{P}_{A, A, B} = 0$
    - $\mathcal{P}_{A, B, B} = 0$
    """
    for G in domain.symbols:
        if isinstance(G, Pythagoras) and len(G.args) == 3:
            A, B, C = G.args
            eliminant = None
            if A == B:
                eliminant = S.Zero
            elif B == C:
                eliminant = S.Zero

            if eliminant is not None:
                domain, objective = _inject_new_variables_and_eliminate(domain, objective, eliminant, G)
                domain, objective = _compress(domain, objective)
    return domain, objective


def _get_variables(expr):
    if isinstance(expr, Integer):
        return set()
    if isinstance(expr, (Add, Mul)):
        return set.union(*(_get_variables(arg) for arg in expr.args))
    if isinstance(expr, Pow):
        return _get_variables(expr.args[0])
    return {expr}


def _compress(domain, objective):
    nonzeros = (1,) * len(domain.gens)
    for key in objective.keys():
        nonzeros = tuple(i | j for i, j in zip(nonzeros, key))

    zero_gens = tuple(domain.gens[i] for i, x in enumerate(nonzeros) if x == 0)
    for x in reversed(zero_gens):
        objective = objective.drop(x)
    domain = objective.ring.to_domain()
    return domain, objective


def _inject_new_variables_and_eliminate(domain, objective, eliminant, G):
    numer, denom = eliminant.as_numer_denom()

    new_variables = _get_variables(numer).union(_get_variables(denom))
    new_variables = new_variables - set(domain.symbols)
    domain = domain.inject(*new_variables)

    objective = domain.convert(objective)
    remainder = domain.from_sympy(denom * G - numer)

    from .sparse import prem_sparse
    g = domain.symbols.index(G)
    objective = prem_sparse(objective, remainder, g)

    return domain, objective


def _apply_to_image(func, subs):
    return {k: func(v) for k, v in subs.items()}
