from sympy.core.cache import cacheit
from sympy.geometry.synthetic.options_predicate import _normalize_predicate_plane
from sympy.geometry.synthetic.options import _auto_option_prove
from sympy.core.singleton import S
from IPython.display import display, Latex
from sympy.printing.latex import latex
from sympy.geometry.synthetic.ecs import PlaneECS1 as ECS1
from sympy.geometry.synthetic.ecs import PlaneECS5 as ECS5
from sympy.geometry.synthetic.ecs import PlaneECS6 as ECS6
from sympy.geometry.synthetic.ecs import PlaneECS7 as ECS7
from sympy.geometry.synthetic.ecs import PlaneECS8 as ECS8
from sympy.geometry.synthetic.constructions import SyntheticGeometryARatio as ARatio
from sympy.geometry.synthetic.constructions import SyntheticGeometryPRatio as PRatio
from sympy.geometry.synthetic.constructions import SyntheticGeometryTRatio as TRatio
from sympy.geometry.synthetic.constructions import SyntheticGeometryFoot as Foot
from sympy.geometry.synthetic.plane_linear import _linear_ECS1
from sympy.geometry.synthetic.plane_linear import _linear_ECS2
from sympy.geometry.synthetic.plane_linear import _linear_ECS3
from sympy.geometry.synthetic.plane_quadratic import _quadratic_ECS1
from sympy.geometry.synthetic.plane_quadratic import _quadratic_ECS2
from sympy.geometry.synthetic.plane_quadratic import _quadratic_ECS3
from sympy.geometry.synthetic.plane_tratio import _area_ECS4
from sympy.geometry.synthetic.plane_tratio import _pythagoras_ECS4
from sympy.geometry.synthetic.plane_tratio import _quadratic_ECS4
from sympy.geometry.synthetic.plane_ratio import _ratio_ECS1
from sympy.geometry.synthetic.plane_ratio import _ratio_ECS2
from sympy.geometry.synthetic.plane_ratio import _ratio_ECS3
from sympy.geometry.synthetic.plane_ratio import _ratio_ECS4
from sympy.geometry.synthetic.plane_inter_line_pline import _linear_ECS5
from sympy.geometry.synthetic.plane_inter_line_pline import _quadratic_ECS5
from sympy.geometry.synthetic.plane_inter_line_pline import _ratio_ECS5
from sympy.geometry.synthetic.plane_inter_line_tline import _linear_ECS6
from sympy.geometry.synthetic.plane_inter_line_tline import _quadratic_ECS6
from sympy.geometry.synthetic.plane_inter_line_tline import _ratio_ECS6
from sympy.geometry.synthetic.plane_inter_line_bline import _linear_ECS7
from sympy.geometry.synthetic.plane_inter_line_bline import _quadratic_ECS7
from sympy.geometry.synthetic.plane_inter_line_bline import _ratio_ECS7
from sympy.geometry.synthetic.plane_inter_line_circle import _linear_ECS8
from sympy.geometry.synthetic.plane_inter_line_circle import _quadratic_ECS8
from sympy.geometry.synthetic.plane_inter_line_circle import _ratio_ECS8
from sympy.geometry.synthetic.plane_aratio import _linear_ARatio
from sympy.geometry.synthetic.plane_aratio import _quadratic_ARatio
from sympy.geometry.synthetic.plane_aratio import _ratio_ARatio
from sympy.geometry.synthetic.plane_ecs import _PlaneECSConverter
from sympy.geometry.synthetic.plane_degenerate import _degenerate
from sympy.geometry.synthetic.simplify import _cancel
from sympy.geometry.synthetic.auxiliary import SyntheticGeometryAuxiliaryAreaCoordinateO as AreaCoordinateO
from sympy.geometry.synthetic.auxiliary import SyntheticGeometryAuxiliaryAreaCoordinateU as AreaCoordinateU
from sympy.geometry.synthetic.auxiliary import SyntheticGeometryAuxiliaryAreaCoordinateV as AreaCoordinateV
from sympy.geometry.synthetic.common import _geometric_quantities
from sympy.geometry.synthetic.common import _cascade
from sympy.geometry.synthetic.common import _quadrilateral_area
from sympy.geometry.synthetic.common import _quadrilateral_pythagoras
from sympy.geometry.synthetic.plane_area_coordinates import _auto_coordinates
from sympy.geometry.synthetic.plane_area_coordinates import _area_coordinates_area
from sympy.geometry.synthetic.plane_area_coordinates import _area_coordinates_pythagoras
from sympy.geometry.synthetic.plane_area_coordinates import _area_coordinates_herron
from sympy.geometry.synthetic.plane_area_coordinates import _algsubs
from sympy.polys.polytools import Poly


def _eliminate_without_side_condition(C, objective, eliminate, func, debug=False):
    subs = func(C, objective)
    subs = _cascade(eliminate, subs)
    subs = _cascade(_cancel, subs)

    if debug:
        for k, v in subs.items():
            tex = r"$\displaystyle %s =^{%s} %s$" % (latex(k), latex(C.args[0]), latex(v))
            display(Latex(tex))

    return objective.xreplace(subs)


def _eliminate_with_side_condition(C, objective, eliminate, prove, func, debug=False):
    subs = func(C, objective, prove)
    subs = _cascade(eliminate, subs)
    subs = _cascade(_cancel, subs)

    if debug:
        for k, v in subs.items():
            tex = r"$\displaystyle %s =^{%s} %s$" % (latex(k), latex(C.args[0]), latex(v))
            display(Latex(tex))

    return objective.xreplace(subs)


def _eliminate(C, constructions, objective, algebraic=(), debug=False):
    def prove(objective):
        return _area_method_plane_prove(
            constructions + (C,), objective, algebraic=algebraic)

    def eliminate(objective):
        return _eliminate(
            C, constructions, objective, algebraic=algebraic)

    Y = C.args[0]

    while True:
        old = objective
        objective = objective.doit()

        if isinstance(C, ECS1):
            objective = _eliminate_without_side_condition(C, objective, eliminate, _linear_ECS1, debug=debug)
            objective = _eliminate_without_side_condition(C, objective, eliminate, _quadratic_ECS1, debug=debug)
            objective = _eliminate_with_side_condition(C, objective, eliminate, prove, _ratio_ECS1, debug=debug)
        elif isinstance(C, Foot):
            objective = _eliminate_without_side_condition(C, objective, eliminate, _linear_ECS2, debug=debug)
            objective = _eliminate_without_side_condition(C, objective, eliminate, _quadratic_ECS2, debug=debug)
            objective = _eliminate_with_side_condition(C, objective, eliminate, prove, _ratio_ECS2, debug=debug)
        elif isinstance(C, PRatio):
            objective = _eliminate_without_side_condition(C, objective, eliminate, _linear_ECS3, debug=debug)
            objective = _eliminate_without_side_condition(C, objective, eliminate, _quadratic_ECS3, debug=debug)
            objective = _eliminate_with_side_condition(C, objective, eliminate, prove, _ratio_ECS3, debug=debug)
        elif isinstance(C, TRatio):
            objective = _eliminate_without_side_condition(C, objective, eliminate, _area_ECS4, debug=debug)
            objective = _eliminate_without_side_condition(C, objective, eliminate, _pythagoras_ECS4, debug=debug)
            objective = _eliminate_without_side_condition(C, objective, eliminate, _quadratic_ECS4, debug=debug)
            objective = _eliminate_with_side_condition(C, objective, eliminate, prove, _ratio_ECS4, debug=debug)

        # Additional ECS
        elif isinstance(C, ECS5):
            objective = _eliminate_without_side_condition(C, objective, eliminate, _linear_ECS5, debug=debug)
            objective = _eliminate_without_side_condition(C, objective, eliminate, _quadratic_ECS5, debug=debug)
            objective = _eliminate_with_side_condition(C, objective, eliminate, prove, _ratio_ECS5, debug=debug)
        elif isinstance(C, ECS6):
            objective = _eliminate_without_side_condition(C, objective, eliminate, _linear_ECS6, debug=debug)
            objective = _eliminate_without_side_condition(C, objective, eliminate, _quadratic_ECS6, debug=debug)
            objective = _eliminate_with_side_condition(C, objective, eliminate, prove, _ratio_ECS6, debug=debug)
        elif isinstance(C, ECS7):
            objective = _eliminate_without_side_condition(C, objective, eliminate, _linear_ECS7, debug=debug)
            objective = _eliminate_without_side_condition(C, objective, eliminate, _quadratic_ECS7, debug=debug)
            objective = _eliminate_with_side_condition(C, objective, eliminate, prove, _ratio_ECS7, debug=debug)
        elif isinstance(C, ECS8):
            objective = _eliminate_without_side_condition(C, objective, eliminate, _linear_ECS8, debug=debug)
            objective = _eliminate_without_side_condition(C, objective, eliminate, _quadratic_ECS8, debug=debug)
            objective = _eliminate_with_side_condition(C, objective, eliminate, prove, _ratio_ECS8, debug=debug)
        elif isinstance(C, ARatio):
            objective = _eliminate_without_side_condition(C, objective, eliminate, _linear_ARatio, debug=debug)
            objective = _eliminate_without_side_condition(C, objective, eliminate, _quadratic_ARatio, debug=debug)
            objective = _eliminate_with_side_condition(C, objective, eliminate, prove, _ratio_ARatio, debug=debug)

        if any(len(G.args) == 4 for G in _geometric_quantities(objective)):
            subs = _quadrilateral_area(objective)
            subs = {k: v for k, v in subs.items() if Y in k.args}
            objective = objective.xreplace(subs)
            subs = _quadrilateral_pythagoras(objective)
            subs = {k: v for k, v in subs.items() if Y in k.args}
            objective = objective.xreplace(subs)

        new = objective
        if old == new:
            break

    objective = _cancel(objective)
    for origin, dest in algebraic:
        objective = _algsubs(objective, origin, dest)
        objective = _cancel(objective)

    for G in _geometric_quantities(objective):
        if Y in G.args:
            raise NotImplementedError(f"{Y} from {C} is not properly eliminated")

    if debug:
        tex = r"$\displaystyle \text{Elimination} =^{%s} %s$" % (latex(C.args[0]), latex(objective))
        display(Latex(tex))

    return objective


def _apply_area_coordinates(objective, debug=False):
    O = AreaCoordinateO()
    U = AreaCoordinateU()
    V = AreaCoordinateV()

    subs = _quadrilateral_area(objective)
    objective = objective.xreplace(subs)
    subs = _quadrilateral_pythagoras(objective)
    objective = objective.xreplace(subs)
    objective = objective.doit()

    match = _auto_coordinates(objective)
    if match is None:
        return objective
    O, U, V = match

    subs = _area_coordinates_area(O, U, V, objective)
    objective = objective.xreplace(subs)

    if debug:
        for k, v in subs.items():
            tex = r"$\displaystyle %s = %s$" % (latex(k), latex(v))
            display(Latex(tex))

    subs = _area_coordinates_pythagoras(O, U, V, objective)
    objective = objective.xreplace(subs)

    if debug:
        for k, v in subs.items():
            tex = r"$\displaystyle %s = %s$" % (latex(k), latex(v))
            display(Latex(tex))

    objective = _cancel(objective)
    subs = _area_coordinates_herron(O, U, V, objective)
    for k, v in subs.items():
        objective = _algsubs(objective, k, v)

    if debug:
        for k, v in subs.items():
            tex = r"$\displaystyle %s = %s$" % (latex(k), latex(v))
            display(Latex(tex))

    objective = _cancel(objective)
    if debug:
        tex = r"$\displaystyle \text{Area Coordinates} =^{%s, %s, %s} %s$" % (latex(O), latex(U), latex(V), latex(objective))
        display(Latex(tex))

    return objective


@cacheit
def _area_method_plane_prove(constructions, objective, algebraic=(), debug=False):
    objective = _normalize_predicate_plane(objective)
    objective = objective.doit()

    if debug:
        display(Latex(r"$\text{Objective :} %s$" % latex(objective)))

    for i in reversed(range(len(constructions))):
        C = constructions[i]
        degenerate = _degenerate(C)
        if _area_method_plane_prove(constructions[:i], degenerate, algebraic=algebraic):
            return S.true
        objective = _eliminate(
            C, constructions[:i], objective, algebraic=algebraic, debug=debug)

    objective = _apply_area_coordinates(objective, debug=debug)
    if objective is not S.true:
        return S.false
    return S.true


def _area_method_plane_evaluate(constructions, objective, algebraic=(), debug=False):
    objective = objective.doit()

    if debug:
        display(Latex(r"$\text{Objective :} %s$" % latex(objective)))

    for i in reversed(range(len(constructions))):
        C = constructions[i]
        objective = _eliminate(
            C, constructions[:i], objective, algebraic=algebraic, debug=debug)

    objective = _apply_area_coordinates(objective, debug=debug)
    return objective


def area_method_plane(constructions, objective, *, algebraic=(), prove=None, debug=False):
    converter = _PlaneECSConverter(_area_method_plane_prove)
    for C in constructions:
        converter.append(C)
    constructions = tuple(converter.constructions)
    prove = _auto_option_prove(objective, prove)

    # Preprocess minimal polynomials as substitutions
    _algebraic = []
    for minpoly in algebraic:
        minpoly = Poly(minpoly)
        if not minpoly.is_univariate:
            raise NotImplementedError

        coeffs = minpoly.coeffs()
        x, = minpoly.gens

        origin = x**minpoly.degree()
        dest = -Poly(coeffs[1:], x).as_expr() / coeffs[0]
        _algebraic.append((origin, dest))
    algebraic = _algebraic

    if prove:
        return _area_method_plane_prove(constructions, objective, algebraic=algebraic, debug=debug)
    return _area_method_plane_evaluate(constructions, objective, algebraic=algebraic, debug=debug)
