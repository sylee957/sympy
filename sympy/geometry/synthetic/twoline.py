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
from sympy.geometry.synthetic.common import _geometric_quantities
from sympy.geometry.synthetic.common import _cascade
from sympy.geometry.synthetic.common import _quadrilateral_area
from sympy.geometry.synthetic.affine_ecs import _constructions_to_ecs
from sympy.geometry.synthetic.twoline_eliminations import _twoline_area_A
from sympy.geometry.synthetic.twoline_eliminations import _twoline_area_B
from sympy.geometry.synthetic.twoline_eliminations import _twoline_split_ratio
from sympy.geometry.synthetic.twoline_eliminations import _twoline_length_A
from sympy.geometry.synthetic.twoline_eliminations import _twoline_length_B
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


def _eliminate(C, constructions, objective, line_1, line_2, debug=False):
    def prove(objective):
        return _area_method_twoline_prove(constructions + (C,), objective, line_1, line_2)

    def eliminate(objective):
        return _eliminate(C, constructions, objective, line_1, line_2)

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
        tex = r"$\text{Elimination} =^{%s} %s$" % (latex(C.args[0]), latex(objective))
        display(Latex(tex))

    return objective


# XXX All other procedures than this should be identical to area_method_affine
def _apply_twoline_elimination(objective, line_1, line_2, debug=False):
    intersect = line_1.intersection(line_2)

    if intersect:
        O, = intersect
        TYPE = 'B'
    else:
        TYPE = 'A'

    objective = _cancel(objective)

    if TYPE == 'A':
        subs = _twoline_area_A(objective, line_1, line_2)
    else:
        subs = _twoline_area_B(objective, line_1, line_2, O)

    if debug:
        for k, v in subs.items():
            tex = r"$%s = %s$" % (latex(k), latex(v))
            display(Latex(tex))

    objective = objective.xreplace(subs)

    subs = _twoline_split_ratio(objective)
    objective = objective.xreplace(subs)

    if TYPE == 'A':
        subs = _twoline_length_A(objective, line_1, line_2)
        objective = objective.xreplace(subs)
    else:
        subs = _twoline_length_B(objective, line_1, line_2, O)
        objective = objective.xreplace(subs)

    objective = _cancel(objective)

    if debug:
        tex = r"$\text{Twoline Elimination} = %s$" % latex(objective)
        display(Latex(tex))

    return objective


@cacheit
def _area_method_twoline_prove(constructions, objective, line_1, line_2, debug=False):
    objective = _normalize_predicate_affine(objective)
    objective = objective.doit()

    for i in reversed(range(len(constructions))):
        C = constructions[i]
        degenerate = _degenerate(C)
        if _area_method_twoline_prove(constructions[:i], degenerate, line_1, line_2):
            return S.true
        objective = _eliminate(C, constructions[:i], objective, line_1, line_2, debug=debug)

    objective = _apply_twoline_elimination(objective, line_1, line_2, debug=debug)
    if objective is not S.true:
        return S.false
    return S.true


def _area_method_twoline_evaluate(constructions, objective, line_1, line_2, debug=False):
    objective = _normalize_predicate_affine(objective)
    objective = objective.doit()

    for i in reversed(range(len(constructions))):
        C = constructions[i]
        objective = _eliminate(C, constructions[:i], objective, line_1, line_2, debug=debug)

    objective = _apply_twoline_elimination(objective, line_1, line_2, debug=debug)
    return objective


def area_method_twoline(constructions, objective, line_1, line_2, *, prove=None, debug=False):
    r"""Apply the area method for the affine plane geometry
    if the free points are chosen arbitrarily from the two lines.
    """
    constructions = _constructions_to_ecs(constructions)
    prove = _auto_option_prove(objective, prove)

    line_1 = frozenset(line_1)
    line_2 = frozenset(line_2)
    inter = line_1.intersection(line_2)
    if len(inter) not in (0, 1):
        raise ValueError(f"{line_1}, {line_2} must intersect only in one point or be parallel")

    if prove:
        return _area_method_twoline_prove(constructions, objective, line_1, line_2, debug=debug)
    return _area_method_twoline_evaluate(constructions, objective, line_1, line_2, debug=debug)
