from sympy.core.singleton import S
from sympy.geometry.synthetic.options import _auto_option_prove

"""
def area_method_plane(constructions, objective, *, O=None, U=None, V=None, prove=None):
    prove = _auto_option_prove(objective, prove)
    constructions = _normalize_constructions(constructions)
    objective = _normalize_proof_objective(objective)
    O, U, V = _normalize_coordinates(O, U, V)
    O, U, V = _auto_coordinates(constructions, objective, O, U, V)

    for i in reversed(range(len(constructions))):
        C = constructions[i]
        if prove and degenerate(C, constructions[:i]) is S.true:
            return S.true

        while True:
            old = objective
            objective = _eliminate(C, constructions[:i + 1], objective)
            new = objective
            if old == new:
                break

    subs = _area_coordinates(O, U, V, objective)
    subs = _simplify_image(_simplify, subs)
    objective = _substitution_rule(subs)(objective)
    objective = _substitution_rule(_simplify_area(objective))(objective)
    objective = _cancel(objective)

    if prove and objective is not S.true:
        objective = S.false
    return objective
"""
