from sympy.core.singleton import S
from sympy.geometry.synthetic.ecs import (
    AffineECS2 as C4,
    AffineECS4 as C7,
    AffineECS5 as C8
)
from sympy.geometry.synthetic.constructions import (
    SyntheticGeometryLRatio as LRatio,
    SyntheticGeometryPRatio as PRatio
)
from sympy.geometry.synthetic.affine_area import (
    _area_ECS1,
    _area_ECS2,
    _area_ECS3,
    _area_ECS4,
    _area_ECS5
)
from sympy.geometry.synthetic.affine_ratio import (
    _ratio_ECS1,
    _ratio_ECS2,
    _ratio_ECS3,
    _ratio_ECS4,
    _ratio_ECS5
)
from sympy.geometry.synthetic.options import (
    _auto_option_prove
)
from sympy.geometry.synthetic.options_predicate import _normalize_predicate_affine
from sympy.geometry.synthetic.affine_degenerate import _degenerate
from sympy.geometry.synthetic.affine_area_coordinates import _auto_coordinates
from sympy.geometry.synthetic.affine_area_coordinates import _area_coordinates
from sympy.geometry.synthetic.common import _geometric_quantities
from sympy.geometry.synthetic.common import _cascade
from sympy.geometry.synthetic.common import _quadrilateral_area
from sympy.geometry.synthetic.affine_ecs import _constructions_to_ecs
from sympy.core.cache import cacheit
from sympy.geometry.synthetic.simplify import _cancel
from IPython.display import display, Latex
from sympy.printing.latex import latex


def _eliminate_area(C, objective, eliminate, func, debug=False):
    subs = func(C, objective)
    subs = _cascade(eliminate, subs)
    subs = _cascade(_cancel, subs)

    if debug:
        for k, v in subs.items():
            tex = r"$%s =^{%s} %s$" % (latex(k), latex(C.args[0]), latex(v))
            display(Latex(tex))

    return objective.xreplace(subs)


def _eliminate_ratio(C, objective, eliminate, prove, func, debug=False):
    subs = func(C, objective, prove)
    subs = _cascade(eliminate, subs)
    subs = _cascade(_cancel, subs)

    if debug:
        for k, v in subs.items():
            tex = r"$%s =^{%s} %s$" % (latex(k), latex(C.args[0]), latex(v))
            display(Latex(tex))

    return objective.xreplace(subs)


def _eliminate(C, constructions, objective, debug=False):
    def prove(objective):
        return _area_method_affine_prove(constructions + (C,), objective)

    def eliminate(objective):
        return _eliminate(C, constructions, objective)

    while True:
        old = objective
        objective = objective.doit()

        subs = _quadrilateral_area(objective)
        objective = objective.xreplace(subs)

        if isinstance(C, LRatio):
            area_elim = _area_ECS1
            ratio_elim = _ratio_ECS1
        elif isinstance(C, C4):
            area_elim = _area_ECS2
            ratio_elim = _ratio_ECS2
        elif isinstance(C, PRatio):
            area_elim = _area_ECS3
            ratio_elim = _ratio_ECS3
        elif isinstance(C, C7):
            area_elim = _area_ECS4
            ratio_elim = _ratio_ECS4
        elif isinstance(C, C8):
            area_elim = _area_ECS5
            ratio_elim = _ratio_ECS5

        objective = _eliminate_area(C, objective, eliminate, area_elim, debug=debug)
        objective = _eliminate_ratio(C, objective, eliminate, prove, ratio_elim, debug=debug)
        objective = _cancel(objective)

        new = objective
        if old == new:
            break

    Y = C.args[0]
    for G in _geometric_quantities(objective):
        if Y in G.args:
            raise NotImplementedError(f"{Y} from {C} is not properly eliminated from")

    if debug:
        tex = r"$\text{Elimination : } =^{%s} %s$" % (latex(C.args[0]), latex(objective))
        display(Latex(tex))

    return objective


def _apply_area_coordinates(objective, debug=False):
    O, U, V = _auto_coordinates(objective)
    subs = _area_coordinates(O, U, V, objective)
    objective = objective.xreplace(subs)

    objective = _cancel(objective)

    if debug:
        tex = r"$\text{Area Coordinates : } =^{%s, %s, %s} %s$" % (latex(O), latex(U), latex(V), latex(objective))
        display(Latex(tex))

    return objective


@cacheit
def _area_method_affine_prove(constructions, objective, debug=False):
    objective = _normalize_predicate_affine(objective)
    objective = objective.doit()

    for i in reversed(range(len(constructions))):
        C = constructions[i]
        degenerate = _degenerate(C)
        if _area_method_affine_prove(constructions[:i], degenerate):
            return S.true
        objective = _eliminate(C, constructions[:i], objective, debug=debug)

    objective = _apply_area_coordinates(objective, debug=debug)
    if objective is not S.true:
        return S.false
    return S.true


def _area_method_affine_evaluate(constructions, objective, debug=False):
    objective = _normalize_predicate_affine(objective)
    objective = objective.doit()

    for i in reversed(range(len(constructions))):
        C = constructions[i]
        objective = _eliminate(C, constructions[:i], objective, debug=debug)

    objective = _apply_area_coordinates(objective, debug=debug)
    return objective


def area_method_affine(constructions, objective, *, prove=None, debug=False):
    constructions = _constructions_to_ecs(constructions)
    prove = _auto_option_prove(objective, prove)

    if prove:
        return _area_method_affine_prove(constructions, objective, debug=debug)
    return _area_method_affine_evaluate(constructions, objective, debug=debug)
